import hashlib
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS raw_payloads (
    id INTEGER PRIMARY KEY,
    source TEXT NOT NULL,
    route TEXT NOT NULL,
    captured_at_utc TEXT NOT NULL,
    http_status INTEGER,
    credits_cost TEXT,
    credits_remaining TEXT,
    sha256 TEXT NOT NULL,
    payload_json TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_raw_payloads_captured_at
    ON raw_payloads(captured_at_utc);

CREATE TABLE IF NOT EXISTS traders (
    fomo_user_id TEXT PRIMARY KEY,
    handle TEXT,
    display_name TEXT,
    evm_wallet_candidate TEXT,
    solana_wallet_candidate TEXT,
    first_seen_at_utc TEXT NOT NULL,
    updated_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS leaderboard_snapshots (
    period TEXT NOT NULL,
    snapshot_at_utc TEXT NOT NULL,
    captured_at_utc TEXT NOT NULL,
    fomo_user_id TEXT NOT NULL REFERENCES traders(fomo_user_id),
    rank INTEGER,
    reported_pnl_usd REAL,
    reported_volume_usd REAL,
    reported_trade_count INTEGER,
    raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
    PRIMARY KEY (period, captured_at_utc, fomo_user_id)
);
CREATE INDEX IF NOT EXISTS idx_leaderboard_snapshots_rank
    ON leaderboard_snapshots(period, captured_at_utc, rank);

CREATE TABLE IF NOT EXISTS fomo_events (
    event_id TEXT PRIMARY KEY,
    event_id_kind TEXT NOT NULL,
    fomo_user_id TEXT,
    handle TEXT,
    event_type TEXT NOT NULL CHECK (event_type IN ('BUY', 'SELL', 'THESIS')),
    chain TEXT,
    chain_id INTEGER,
    token_address TEXT,
    token_symbol TEXT,
    source_timestamp_raw TEXT,
    source_at_utc TEXT,
    amount_usd REAL,
    trade_id TEXT,
    captured_at_utc TEXT NOT NULL,
    raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id)
);
CREATE INDEX IF NOT EXISTS idx_fomo_events_source_at
    ON fomo_events(source_at_utc);
CREATE INDEX IF NOT EXISTS idx_fomo_events_trader_token
    ON fomo_events(fomo_user_id, chain_id, token_address, source_at_utc);

CREATE TABLE IF NOT EXISTS onchain_trades (
    signature TEXT PRIMARY KEY,
    chain TEXT NOT NULL,
    wallet TEXT NOT NULL,
    slot INTEGER,
    block_time_utc TEXT,
    token_address TEXT NOT NULL,
    side TEXT NOT NULL CHECK (side IN ('BUY', 'SELL', 'UNKNOWN')),
    token_amount_raw TEXT NOT NULL,
    token_decimals INTEGER,
    quote_asset_address TEXT,
    quote_amount_raw TEXT,
    quote_decimals INTEGER,
    amount_usd REAL,
    protocol TEXT,
    dex TEXT,
    source TEXT NOT NULL,
    raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
    captured_at_utc TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_onchain_trades_wallet_time
    ON onchain_trades(chain, wallet, block_time_utc);
CREATE INDEX IF NOT EXISTS idx_onchain_trades_token_time
    ON onchain_trades(chain, token_address, block_time_utc);

CREATE TABLE IF NOT EXISTS wallet_resolutions (
    fomo_user_id TEXT NOT NULL REFERENCES traders(fomo_user_id),
    chain TEXT NOT NULL,
    address TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('candidate', 'verified', 'rejected')),
    evidence_json TEXT NOT NULL,
    resolved_at_utc TEXT NOT NULL,
    PRIMARY KEY (fomo_user_id, chain, address)
);

CREATE TABLE IF NOT EXISTS event_trade_matches (
    fomo_event_id TEXT NOT NULL REFERENCES fomo_events(event_id),
    signature TEXT NOT NULL REFERENCES onchain_trades(signature),
    delta_seconds REAL NOT NULL,
    match_status TEXT NOT NULL CHECK (match_status IN ('candidate', 'verified', 'ambiguous')),
    evidence_json TEXT NOT NULL,
    created_at_utc TEXT NOT NULL,
    PRIMARY KEY (fomo_event_id, signature)
);

CREATE TABLE IF NOT EXISTS collector_state (
    state_key TEXT PRIMARY KEY,
    state_value TEXT NOT NULL,
    updated_at_utc TEXT NOT NULL
);

-- Derived research outputs are additive and reproducible from raw_payloads.
CREATE TABLE IF NOT EXISTS solana_normalized_actions (
    leaderboard_captured_at_utc TEXT NOT NULL,
    signature TEXT NOT NULL,
    wallet TEXT NOT NULL,
    fomo_user_id TEXT NOT NULL REFERENCES traders(fomo_user_id),
    rank INTEGER NOT NULL,
    handle TEXT,
    slot INTEGER,
    block_time_utc TEXT,
    transaction_successful INTEGER NOT NULL CHECK (transaction_successful IN (0, 1)),
    wallet_is_signer INTEGER NOT NULL CHECK (wallet_is_signer IN (0, 1)),
    action_type TEXT NOT NULL CHECK (action_type IN ('SWAP', 'TRANSFER', 'UNKNOWN')),
    classification_confidence TEXT NOT NULL,
    swap_log_marker INTEGER NOT NULL CHECK (swap_log_marker IN (0, 1)),
    transfer_log_marker INTEGER NOT NULL CHECK (transfer_log_marker IN (0, 1)),
    native_balance_delta_lamports INTEGER,
    raw_source TEXT NOT NULL,
    raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
    classification_version TEXT NOT NULL,
    generated_at_utc TEXT NOT NULL,
    PRIMARY KEY (leaderboard_captured_at_utc, signature, wallet)
);
CREATE INDEX IF NOT EXISTS idx_solana_actions_rank_time
    ON solana_normalized_actions(leaderboard_captured_at_utc, rank, block_time_utc);
CREATE INDEX IF NOT EXISTS idx_solana_actions_wallet_time
    ON solana_normalized_actions(wallet, block_time_utc);

CREATE TABLE IF NOT EXISTS solana_action_token_deltas (
    leaderboard_captured_at_utc TEXT NOT NULL,
    signature TEXT NOT NULL,
    wallet TEXT NOT NULL,
    token_address TEXT NOT NULL,
    delta_raw TEXT NOT NULL,
    token_decimals INTEGER,
    delta_amount TEXT NOT NULL,
    swap_side TEXT CHECK (swap_side IN ('BUY', 'SELL') OR swap_side IS NULL),
    PRIMARY KEY (leaderboard_captured_at_utc, signature, wallet, token_address),
    FOREIGN KEY (leaderboard_captured_at_utc, signature, wallet)
        REFERENCES solana_normalized_actions(leaderboard_captured_at_utc, signature, wallet)
        ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_solana_action_deltas_token
    ON solana_action_token_deltas(token_address, leaderboard_captured_at_utc);

CREATE TABLE IF NOT EXISTS trader_token_timeline (
    leaderboard_captured_at_utc TEXT NOT NULL,
    rank INTEGER NOT NULL,
    fomo_user_id TEXT NOT NULL REFERENCES traders(fomo_user_id),
    handle TEXT,
    chain TEXT NOT NULL,
    wallet TEXT NOT NULL,
    token_address TEXT NOT NULL,
    token_symbol TEXT,
    wallet_resolution_status TEXT NOT NULL,
    t1_first_observed_onchain_buy_at_utc TEXT,
    t2_fomo_buy_at_utc TEXT,
    fomo_sell_at_utc TEXT,
    t3_fomo_thesis_at_utc TEXT,
    t4_x_post_at_utc TEXT,
    t5_first_observed_onchain_sell_at_utc TEXT,
    matched_onchain_at_utc TEXT,
    verified_match_count INTEGER NOT NULL,
    matched_event_delta_seconds TEXT,
    first_observed_buy_to_fomo_buy_seconds REAL,
    swap_buy_count_in_history INTEGER NOT NULL,
    swap_sell_count_in_history INTEGER NOT NULL,
    history_start_at_utc TEXT,
    history_end_at_utc TEXT,
    history_normalization TEXT NOT NULL,
    coverage_note TEXT NOT NULL,
    generated_at_utc TEXT NOT NULL,
    PRIMARY KEY (leaderboard_captured_at_utc, fomo_user_id, chain, token_address)
);
CREATE INDEX IF NOT EXISTS idx_trader_token_timeline_rank
    ON trader_token_timeline(leaderboard_captured_at_utc, rank, chain, token_address);

CREATE TABLE IF NOT EXISTS top10_wallet_inventory (
    snapshot_at_utc TEXT NOT NULL,
    rank INTEGER NOT NULL,
    fomo_user_id TEXT NOT NULL REFERENCES traders(fomo_user_id),
    handle TEXT,
    display_name TEXT,
    reported_pnl_usd REAL,
    reported_volume_usd REAL,
    solana_wallet_candidate TEXT,
    solana_resolution_status TEXT NOT NULL,
    evm_wallet_candidate TEXT,
    evm_resolution_status TEXT NOT NULL,
    solana_fomo_events INTEGER NOT NULL,
    other_chain_fomo_events INTEGER NOT NULL,
    solana_rpc_source TEXT,
    solana_rpc_observed_at_utc TEXT,
    solana_history_state TEXT NOT NULL,
    solana_signature_pages INTEGER NOT NULL,
    solana_signatures_60d INTEGER NOT NULL,
    solana_history_earliest_at_utc TEXT,
    solana_history_latest_at_utc TEXT,
    solana_observed_age_days REAL,
    total_fomo_events_current INTEGER NOT NULL,
    fomo_events_since_snapshot INTEGER NOT NULL,
    event_chains_json TEXT NOT NULL,
    event_chain_ids_json TEXT NOT NULL,
    raw_page_ids_json TEXT NOT NULL,
    generated_at_utc TEXT NOT NULL,
    PRIMARY KEY (snapshot_at_utc, fomo_user_id)
);
CREATE INDEX IF NOT EXISTS idx_top10_inventory_rank
    ON top10_wallet_inventory(snapshot_at_utc, rank);
"""


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _json(payload):
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _timestamp(value):
    if value is None:
        return None, None
    raw = str(value)
    try:
        if isinstance(value, (int, float)) or raw.isdigit():
            number = float(value)
            seconds = number / 1000 if number > 100000000000 else number
            stamp = datetime.fromtimestamp(seconds, timezone.utc)
        else:
            stamp = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            if stamp.tzinfo is None:
                stamp = stamp.replace(tzinfo=timezone.utc)
            stamp = stamp.astimezone(timezone.utc)
        return raw, stamp.isoformat(timespec="milliseconds").replace("+00:00", "Z")
    except (ValueError, OverflowError, OSError, TypeError):
        return raw, None


def _number(value):
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _event_type(payload):
    value = payload.get("alertType") or payload.get("type") or ""
    value = str(value).lower()
    if value in ("buy", "sell", "thesis", "call"):
        return "THESIS" if value in ("thesis", "call") else value.upper()
    return None


def _alerts(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("alerts", "events"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    raise ValueError("Fomo alerts response did not contain a documented alert list")


class Store:
    def __init__(self, database):
        self.database = Path(database).expanduser()
        if not self.database.is_absolute():
            self.database = Path.cwd() / self.database

    def connect(self):
        self.database.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        if not self.database.exists():
            descriptor = os.open(str(self.database), os.O_CREAT | os.O_RDWR, 0o600)
            os.close(descriptor)
        os.chmod(str(self.database), 0o600)
        connection = sqlite3.connect(str(self.database), timeout=30)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 30000")
        return connection

    def initialize(self):
        with self.connect() as connection:
            connection.executescript(SCHEMA)
            columns = {row[1] for row in connection.execute("PRAGMA table_info(raw_payloads)")}
            if "credits_cost" not in columns:
                connection.execute("ALTER TABLE raw_payloads ADD COLUMN credits_cost TEXT")
            if "credits_remaining" not in columns:
                connection.execute("ALTER TABLE raw_payloads ADD COLUMN credits_remaining TEXT")

    def get_state(self, state_key):
        with self.connect() as connection:
            row = connection.execute(
                "SELECT state_value FROM collector_state WHERE state_key=?", (state_key,)
            ).fetchone()
            return row[0] if row else None

    def set_state(self, state_key, state_value, updated_at=None):
        updated_at = updated_at or utc_now()
        with self.connect() as connection:
            connection.execute(
                """INSERT INTO collector_state(state_key, state_value, updated_at_utc)
                   VALUES (?, ?, ?)
                   ON CONFLICT(state_key) DO UPDATE SET
                     state_value=excluded.state_value, updated_at_utc=excluded.updated_at_utc""",
                (state_key, state_value, updated_at),
            )

    def delete_state(self, state_key):
        with self.connect() as connection:
            connection.execute("DELETE FROM collector_state WHERE state_key=?", (state_key,))

    def save_raw(self, connection, source, route, payload, captured_at, status=200,
                 credits_cost=None, credits_remaining=None):
        body = _json(payload)
        digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
        cursor = connection.execute(
            "INSERT INTO raw_payloads(source, route, captured_at_utc, http_status, credits_cost, "
            "credits_remaining, sha256, payload_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (source, route, captured_at, status, credits_cost, credits_remaining, digest, body),
        )
        return cursor.lastrowid

    def save_leaderboard(self, response, period, captured_at=None):
        captured_at = captured_at or utc_now()
        payload = response.payload
        rows = payload.get("traders") if isinstance(payload, dict) else None
        if not isinstance(rows, list):
            raise ValueError("Leaderboard response did not contain a traders list")
        _, provider_time = _timestamp(payload.get("capturedAt"))
        snapshot_at = provider_time or captured_at
        inserted = 0
        with self.connect() as connection:
            raw_id = self.save_raw(connection, "fomo", response.route, payload, captured_at,
                                   response.status, response.credits_cost, response.credits_remaining)
            for trader in rows:
                user_id = trader.get("userId")
                if not user_id:
                    continue
                wallets = trader.get("wallets") or {}
                connection.execute(
                    """INSERT INTO traders(
                           fomo_user_id, handle, display_name, evm_wallet_candidate,
                           solana_wallet_candidate, first_seen_at_utc, updated_at_utc
                       ) VALUES (?, ?, ?, ?, ?, ?, ?)
                       ON CONFLICT(fomo_user_id) DO UPDATE SET
                           handle=COALESCE(excluded.handle, traders.handle),
                           display_name=COALESCE(excluded.display_name, traders.display_name),
                           evm_wallet_candidate=COALESCE(excluded.evm_wallet_candidate, traders.evm_wallet_candidate),
                           solana_wallet_candidate=COALESCE(excluded.solana_wallet_candidate, traders.solana_wallet_candidate),
                           updated_at_utc=excluded.updated_at_utc""",
                    (user_id, trader.get("handle"), trader.get("displayName"),
                     wallets.get("evm"), wallets.get("solana"), captured_at, captured_at),
                )
                cursor = connection.execute(
                    """INSERT OR IGNORE INTO leaderboard_snapshots(
                           period, snapshot_at_utc, captured_at_utc, fomo_user_id, rank,
                           reported_pnl_usd, reported_volume_usd, reported_trade_count, raw_payload_id
                       ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (period, snapshot_at, captured_at, user_id, trader.get("rank"),
                     _number(trader.get("pnlUsd")), _number(trader.get("volumeUsd")),
                     trader.get("trades"), raw_id),
                )
                inserted += cursor.rowcount
        return len(rows), inserted

    def save_alerts(self, response, captured_at=None, existing_raw_payload_id=None,
                    authorized_user_ids=None, start_at_utc=None, end_at_utc=None):
        captured_at = captured_at or utc_now()
        rows = _alerts(response.payload)
        inserted = duplicates = ignored = synthetic_ids = 0
        with self.connect() as connection:
            if existing_raw_payload_id is None:
                raw_id = self.save_raw(connection, "fomo", response.route, response.payload, captured_at,
                                       response.status, response.credits_cost, response.credits_remaining)
            else:
                prior = connection.execute("SELECT * FROM raw_payloads WHERE id=?", (existing_raw_payload_id,)).fetchone()
                if prior is None or prior["payload_json"] != _json(response.payload) or prior["route"] != response.route:
                    raise ValueError("Saved raw alert evidence does not match the response")
                raw_id = existing_raw_payload_id
            allowed = set(authorized_user_ids) if authorized_user_ids is not None else None
            start_bound = datetime.fromisoformat(start_at_utc.replace("Z", "+00:00")) if start_at_utc else None
            end_bound = datetime.fromisoformat(end_at_utc.replace("Z", "+00:00")) if end_at_utc else None
            for alert in rows:
                if not isinstance(alert, dict):
                    ignored += 1
                    continue
                kind = _event_type(alert)
                if kind is None:
                    ignored += 1
                    continue
                stable_id = alert.get("eventId") or alert.get("event_id") or alert.get("id")
                if stable_id:
                    event_id = str(stable_id)
                    id_kind = "provider"
                else:
                    event_id = "sha256:" + hashlib.sha256(_json(alert).encode("utf-8")).hexdigest()
                    id_kind = "payload_hash"
                    synthetic_ids += 1
                source_raw, source_at = _timestamp(alert.get("ts"))
                if allowed is not None and alert.get("userId") not in allowed:
                    ignored += 1
                    continue
                if start_bound or end_bound:
                    source_time = datetime.fromisoformat(source_at.replace("Z", "+00:00")) if source_at else None
                    if source_time is None or (start_bound and source_time < start_bound) or (end_bound and source_time >= end_bound):
                        ignored += 1
                        continue
                token = alert.get("token")
                if isinstance(token, dict):
                    token_symbol = token.get("symbol") or token.get("name")
                    token_address = alert.get("tokenAddress") or token.get("address")
                else:
                    token_symbol = token
                    token_address = alert.get("tokenAddress")
                trader_value = alert.get("trader")
                if isinstance(trader_value, str):
                    handle = trader_value
                elif isinstance(trader_value, dict):
                    handle = trader_value.get("handle")
                else:
                    handle = None
                user_id = alert.get("userId")
                if user_id:
                    connection.execute(
                        """INSERT INTO traders(
                               fomo_user_id, handle, first_seen_at_utc, updated_at_utc
                           ) VALUES (?, ?, ?, ?)
                           ON CONFLICT(fomo_user_id) DO UPDATE SET
                               handle=COALESCE(excluded.handle, traders.handle),
                               updated_at_utc=excluded.updated_at_utc""",
                        (user_id, handle, captured_at, captured_at),
                    )
                cursor = connection.execute(
                    """INSERT OR IGNORE INTO fomo_events(
                           event_id, event_id_kind, fomo_user_id, handle, event_type,
                           chain, chain_id, token_address, token_symbol,
                           source_timestamp_raw, source_at_utc, amount_usd, trade_id,
                           captured_at_utc, raw_payload_id
                       ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (event_id, id_kind, user_id, handle, kind, alert.get("chain"),
                     alert.get("chainId"), token_address, token_symbol,
                     source_raw, source_at, _number(alert.get("usdValue")),
                     alert.get("tradeId"), captured_at, raw_id),
                )
                if cursor.rowcount:
                    inserted += 1
                    if source_at:
                        connection.execute(
                            """INSERT INTO collector_state(state_key, state_value, updated_at_utc)
                               VALUES ('newest_event_at_utc', ?, ?)
                               ON CONFLICT(state_key) DO UPDATE SET
                                 state_value=CASE WHEN excluded.state_value > collector_state.state_value
                                                  THEN excluded.state_value ELSE collector_state.state_value END,
                                 updated_at_utc=excluded.updated_at_utc""",
                            (source_at, captured_at),
                        )
                else:
                    duplicates += 1
        return {"received": len(rows), "inserted": inserted, "duplicates": duplicates,
                "ignored": ignored, "synthetic_ids": synthetic_ids}

    def status(self):
        self.initialize()
        with self.connect() as connection:
            result = {
                "database": str(self.database),
                "traders": connection.execute("SELECT COUNT(*) FROM traders").fetchone()[0],
                "leaderboard_rows": connection.execute("SELECT COUNT(*) FROM leaderboard_snapshots").fetchone()[0],
                "fomo_events": connection.execute("SELECT COUNT(*) FROM fomo_events").fetchone()[0],
                "onchain_trades": connection.execute("SELECT COUNT(*) FROM onchain_trades").fetchone()[0],
                "verified_wallets": connection.execute("SELECT COUNT(*) FROM wallet_resolutions WHERE status='verified'").fetchone()[0],
                "verified_matches": connection.execute("SELECT COUNT(*) FROM event_trade_matches WHERE match_status='verified'").fetchone()[0],
                "raw_payloads": connection.execute("SELECT COUNT(*) FROM raw_payloads").fetchone()[0],
                "normalized_solana_actions": connection.execute("SELECT COUNT(*) FROM solana_normalized_actions").fetchone()[0],
                "solana_action_token_deltas": connection.execute("SELECT COUNT(*) FROM solana_action_token_deltas").fetchone()[0],
                "trader_token_timeline_rows": connection.execute("SELECT COUNT(*) FROM trader_token_timeline").fetchone()[0],
                "top10_wallet_inventory_rows": connection.execute("SELECT COUNT(*) FROM top10_wallet_inventory").fetchone()[0],
            }
            state = connection.execute(
                "SELECT state_value FROM collector_state WHERE state_key='newest_event_at_utc'"
            ).fetchone()
            result["newest_event_at_utc"] = state[0] if state else None
            snapshot = connection.execute(
                "SELECT MAX(captured_at_utc) FROM leaderboard_snapshots"
            ).fetchone()[0]
            result["latest_snapshot_captured_at_utc"] = snapshot
            return result

    def save_onchain_match(self, event_id, user_id, wallet, signature, slot, block_time_utc,
                           token_address, side, token_amount_raw, token_decimals,
                           quote_asset_address, quote_amount_raw, quote_decimals,
                           raw_payload_id, captured_at, delta_seconds, evidence):
        evidence_json = _json(evidence)
        with self.connect() as connection:
            connection.execute(
                """INSERT OR IGNORE INTO onchain_trades(
                       signature, chain, wallet, slot, block_time_utc, token_address, side,
                       token_amount_raw, token_decimals, quote_asset_address, quote_amount_raw,
                       quote_decimals, amount_usd, protocol, dex, source, raw_payload_id, captured_at_utc
                   ) VALUES (?, 'solana', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL,
                             'solana-rpc', ?, ?)""",
                (signature, wallet, slot, block_time_utc, token_address, side,
                 str(token_amount_raw), token_decimals, quote_asset_address,
                 str(quote_amount_raw) if quote_amount_raw is not None else None,
                 quote_decimals, raw_payload_id, captured_at),
            )
            cursor = connection.execute(
                """INSERT OR IGNORE INTO event_trade_matches(
                       fomo_event_id, signature, delta_seconds, match_status, evidence_json, created_at_utc
                   ) VALUES (?, ?, ?, 'candidate', ?, ?)""",
                (event_id, signature, delta_seconds, evidence_json, captured_at),
            )
        resolution = self.refresh_wallet_resolution(user_id, wallet, evidence, captured_at)
        resolution["inserted"] = cursor.rowcount == 1
        return resolution

    def save_ambiguous_onchain_match(self, event_id, wallet, signature, slot, block_time_utc,
                                     token_address, side, token_amount_raw, token_decimals,
                                     quote_asset_address, quote_amount_raw, quote_decimals,
                                     raw_payload_id, captured_at, delta_seconds, evidence):
        evidence_json = _json(evidence)
        with self.connect() as connection:
            connection.execute(
                """INSERT OR IGNORE INTO onchain_trades(
                       signature, chain, wallet, slot, block_time_utc, token_address, side,
                       token_amount_raw, token_decimals, quote_asset_address, quote_amount_raw,
                       quote_decimals, amount_usd, protocol, dex, source, raw_payload_id, captured_at_utc
                   ) VALUES (?, 'solana', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL,
                             'solana-rpc', ?, ?)""",
                (signature, wallet, slot, block_time_utc, token_address, side,
                 str(token_amount_raw), token_decimals, quote_asset_address,
                 str(quote_amount_raw) if quote_amount_raw is not None else None,
                 quote_decimals, raw_payload_id, captured_at),
            )
            cursor = connection.execute(
                """INSERT OR IGNORE INTO event_trade_matches(
                       fomo_event_id, signature, delta_seconds, match_status, evidence_json, created_at_utc
                   ) VALUES (?, ?, ?, 'ambiguous', ?, ?)""",
                (event_id, signature, delta_seconds, evidence_json, captured_at),
            )
        return {"inserted": cursor.rowcount == 1}

    def refresh_wallet_resolution(self, user_id, wallet, evidence=None, resolved_at=None):
        resolved_at = resolved_at or utc_now()
        with self.connect() as connection:
            counts = connection.execute(
                """SELECT COUNT(DISTINCT e.event_id), COUNT(DISTINCT m.signature)
                   FROM event_trade_matches m
                   JOIN fomo_events e ON e.event_id=m.fomo_event_id
                   JOIN onchain_trades t ON t.signature=m.signature
                   WHERE e.fomo_user_id=? AND t.chain='solana' AND t.wallet=?
                     AND m.match_status IN ('candidate','verified')""",
                (user_id, wallet),
            ).fetchone()
            matched_events, matched_signatures = counts
            status = "verified" if matched_events >= 2 and matched_signatures >= 2 else "candidate"
            row = connection.execute(
                """SELECT evidence_json FROM wallet_resolutions
                   WHERE fomo_user_id=? AND chain='solana' AND address=?""",
                (user_id, wallet),
            ).fetchone()
            if evidence is not None:
                evidence_data = dict(evidence)
            elif row:
                try:
                    evidence_data = json.loads(row[0])
                except (TypeError, json.JSONDecodeError):
                    evidence_data = {}
            else:
                evidence_data = {}
            evidence_data["matched_event_count"] = matched_events
            evidence_data["matched_signature_count"] = matched_signatures
            evidence_json = _json(evidence_data)
            if row or matched_events or evidence is not None:
                connection.execute(
                    """INSERT INTO wallet_resolutions(
                           fomo_user_id, chain, address, status, evidence_json, resolved_at_utc
                       ) VALUES (?, 'solana', ?, ?, ?, ?)
                       ON CONFLICT(fomo_user_id, chain, address) DO UPDATE SET
                           status=excluded.status, evidence_json=excluded.evidence_json,
                           resolved_at_utc=excluded.resolved_at_utc""",
                    (user_id, wallet, status, evidence_json, resolved_at),
                )
                connection.execute(
                    """UPDATE event_trade_matches SET match_status=?
                       WHERE fomo_event_id IN (
                           SELECT event_id FROM fomo_events WHERE fomo_user_id=?
                       ) AND signature IN (
                           SELECT signature FROM onchain_trades WHERE chain='solana' AND wallet=?
                       ) AND match_status IN ('candidate','verified')""",
                    (status, user_id, wallet),
                )
            return {"status": status, "matched_event_count": matched_events,
                    "matched_signature_count": matched_signatures,
                    "recorded": bool(row or matched_events or evidence is not None)}
