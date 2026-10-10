import csv
import json
import re
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from .store import Store, utc_now


RANK_ROUTE = re.compile(r"leaderboard_rank=(\d+)")
SWAP_LOG = re.compile(
    r"\b(swap|route|jupiter|raydium|orca|meteora)\b|"
    r"Program log: (?:Instruction: (?:Swap|Route)[A-Za-z0-9_]*\b|SwapEvent\b)",
    re.IGNORECASE,
)
TRANSFER_LOG = re.compile(r"Instruction: Transfer(?:Checked)?\b", re.IGNORECASE)


def _utc(seconds):
    if seconds is None:
        return None
    return datetime.fromtimestamp(seconds, timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _timestamp(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def _wallet_changes(item, wallet, verified_matches_by_signature=None):
    transaction = item.get("transaction") or {}
    message = transaction.get("message") or {}
    meta = item.get("meta") or {}
    keys = message.get("accountKeys") or []
    addresses = [key.get("pubkey") if isinstance(key, dict) else key for key in keys]
    wallet_index = addresses.index(wallet) if wallet in addresses else None
    required_signatures = (message.get("header") or {}).get("numRequiredSignatures", 1)
    signer = wallet_index is not None and wallet_index < required_signatures
    if wallet_index is not None and isinstance(keys[wallet_index], dict) and 'signer' in keys[wallet_index]:
        signer = keys[wallet_index]['signer'] is True

    amounts = defaultdict(int)
    decimals = {}
    for rows, sign in ((meta.get("preTokenBalances") or [], -1),
                       (meta.get("postTokenBalances") or [], 1)):
        for row in rows:
            if row.get("owner") != wallet or not row.get("mint"):
                continue
            token_amount = row.get("uiTokenAmount") or {}
            mint = row["mint"]
            amounts[mint] += sign * int(token_amount.get("amount", "0"))
            if token_amount.get("decimals") is not None:
                decimals[mint] = token_amount["decimals"]
    deltas = {mint: raw for mint, raw in amounts.items() if raw}

    pre = meta.get("preBalances") or []
    post = meta.get("postBalances") or []
    native_delta = None
    if wallet_index is not None and wallet_index < min(len(pre), len(post)):
        native_delta = post[wallet_index] - pre[wallet_index]
    fee = meta.get("fee") or 0
    logs = meta.get("logMessages") or []
    successful = "err" in meta and meta["err"] is None
    signatures = transaction.get("signatures") or []
    signature = signatures[0] if signatures else item.get("signature")

    return _classify_balance_changes(signature, item.get("slot"), _utc(item.get("blockTime")),
                                     successful, signer, deltas, decimals, native_delta,
                                     fee, logs, verified_matches_by_signature)


def _classify_balance_changes(signature, slot, block_time_utc, successful, signer, deltas,
                              decimals, native_delta, fee, logs, verified_matches_by_signature=None):
    """Shared provisional classification for RPC and indexed historical owner balances."""
    swap_marker = any(SWAP_LOG.search(line) for line in logs)
    transfer_marker = any(TRANSFER_LOG.search(line) for line in logs)
    positive = any(value > 0 for value in deltas.values())
    negative = any(value < 0 for value in deltas.values())
    opposing_balance_move = (positive and negative) or (
        (positive and native_delta is not None and native_delta < -fee) or
        (negative and native_delta is not None and native_delta > fee)
    )
    matched_sides = (verified_matches_by_signature or {}).get(signature, {})
    verified_match_direction = any(
        (side == "BUY" and deltas.get(mint, 0) > 0) or
        (side == "SELL" and deltas.get(mint, 0) < 0)
        for mint, side in matched_sides.items()
    )
    if successful and signer and swap_marker and deltas and opposing_balance_move:
        action_type = "SWAP"
        confidence = "swap_log_and_opposing_balance_changes"
    elif successful and signer and verified_match_direction and deltas and opposing_balance_move:
        action_type = "SWAP"
        confidence = "verified_fomo_match_and_opposing_balance_changes"
    elif successful and not swap_marker and transfer_marker and deltas:
        action_type = "TRANSFER"
        confidence = "transfer_instruction_log_and_wallet_token_delta"
    else:
        action_type = "UNKNOWN"
        confidence = "insufficient_semantic_evidence"

    changes = []
    for mint, raw in sorted(deltas.items()):
        scale = decimals.get(mint, 0)
        ui_amount = Decimal(raw) / (Decimal(10) ** scale)
        side = ("BUY" if raw > 0 else "SELL") if action_type == "SWAP" else None
        changes.append({"token_address": mint, "delta_raw": str(raw),
                        "token_decimals": decimals.get(mint), "delta_amount": format(ui_amount, "f"),
                        "swap_side": side})

    return {
        "signature": signature,
        "slot": slot,
        "block_time_utc": block_time_utc,
        "successful": successful,
        "wallet_is_signer": signer,
        "action_type": action_type,
        "classification_confidence": confidence,
        "swap_log_marker": swap_marker,
        "transfer_log_marker": transfer_marker,
        "native_balance_delta_lamports": native_delta,
        "token_deltas": changes,
    }


def _write_csv(path, fields, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


ACTION_FIELDS = ["rank", "fomo_user_id", "handle", "wallet", "signature", "slot",
                 "block_time_utc", "transaction_successful", "wallet_is_signer", "action_type",
                 "classification_confidence", "swap_log_marker", "transfer_log_marker",
                 "native_balance_delta_lamports", "token_deltas_json", "raw_source", "raw_payload_id"]
TIMELINE_FIELDS = ["rank", "fomo_user_id", "handle", "chain", "wallet", "token_address",
                   "token_symbol", "wallet_resolution_status", "t1_first_observed_onchain_buy_at_utc",
                   "t2_fomo_buy_at_utc", "fomo_sell_at_utc", "t3_fomo_thesis_at_utc",
                   "t4_x_post_at_utc", "t5_first_observed_onchain_sell_at_utc",
                   "matched_onchain_at_utc", "verified_match_count", "matched_event_delta_seconds",
                   "first_observed_buy_to_fomo_buy_seconds", "swap_buy_count_in_history",
                   "swap_sell_count_in_history", "history_start_at_utc", "history_end_at_utc",
                   "history_normalization", "coverage_note"]
INVENTORY_FIELDS = ["rank", "snapshot_at_utc", "fomo_user_id", "handle", "display_name",
                    "reported_pnl_usd", "reported_volume_usd", "solana_wallet_candidate",
                    "solana_resolution_status", "evm_wallet_candidate", "evm_resolution_status",
                    "solana_fomo_events", "other_chain_fomo_events", "solana_rpc_source",
                    "solana_rpc_observed_at_utc", "solana_history_state", "solana_signature_pages",
                    "solana_signatures_60d", "solana_history_earliest_at_utc",
                    "solana_history_latest_at_utc", "solana_observed_age_days",
                    "total_fomo_events_current", "fomo_events_since_snapshot",
                    "event_chains_json", "event_chain_ids_json"]
INVENTORY_DB_FIELDS = ["snapshot_at_utc", "rank", "fomo_user_id", "handle", "display_name",
                       "reported_pnl_usd", "reported_volume_usd", "solana_wallet_candidate",
                       "solana_resolution_status", "evm_wallet_candidate", "evm_resolution_status",
                       "solana_fomo_events", "other_chain_fomo_events", "solana_rpc_source",
                       "solana_rpc_observed_at_utc", "solana_history_state", "solana_signature_pages",
                       "solana_signatures_60d", "solana_history_earliest_at_utc",
                       "solana_history_latest_at_utc", "solana_observed_age_days",
                       "total_fomo_events_current", "fomo_events_since_snapshot",
                       "event_chains_json", "event_chain_ids_json", "raw_page_ids_json",
                       "generated_at_utc"]
EVENT_MATCH_FIELDS = ["rank", "fomo_user_id", "handle", "chain", "token_address",
                      "token_symbol", "fomo_event_type", "fomo_event_at_utc",
                      "matched_onchain_at_utc", "matched_onchain_side", "delta_seconds",
                      "event_match_status", "wallet_resolution_status"]
CLASSIFICATION_VERSION = "solana-heuristic-v3"


def _persist_research_rows(database, snapshot, rank_limit, verified_user_ids, action_rows, timeline_rows):
    store = Store(database)
    store.initialize()
    generated_at = utc_now()
    with store.connect() as connection:
        if verified_user_ids:
            placeholders = ",".join("?" for _ in verified_user_ids)
            connection.execute(
                "DELETE FROM solana_normalized_actions WHERE leaderboard_captured_at_utc=? "
                "AND fomo_user_id IN ({})".format(placeholders),
                [snapshot] + list(verified_user_ids),
            )
        for row in action_rows:
            connection.execute(
                """INSERT INTO solana_normalized_actions(
                       leaderboard_captured_at_utc,signature,wallet,fomo_user_id,rank,handle,slot,
                       block_time_utc,transaction_successful,wallet_is_signer,action_type,
                       classification_confidence,swap_log_marker,transfer_log_marker,
                       native_balance_delta_lamports,raw_source,raw_payload_id,
                       classification_version,generated_at_utc
                   ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (snapshot, row["signature"], row["wallet"], row["fomo_user_id"], row["rank"],
                 row["handle"], row["slot"], row["block_time_utc"],
                 int(bool(row["transaction_successful"])), int(bool(row["wallet_is_signer"])),
                 row["action_type"], row["classification_confidence"],
                 int(bool(row["swap_log_marker"])), int(bool(row["transfer_log_marker"])),
                 row["native_balance_delta_lamports"], row["raw_source"], row["raw_payload_id"],
                 CLASSIFICATION_VERSION, generated_at),
            )
            deltas = json.loads(row["token_deltas_json"])
            for delta in deltas:
                connection.execute(
                    """INSERT INTO solana_action_token_deltas(
                           leaderboard_captured_at_utc,signature,wallet,token_address,delta_raw,
                           token_decimals,delta_amount,swap_side
                       ) VALUES (?,?,?,?,?,?,?,?)""",
                    (snapshot, row["signature"], row["wallet"], delta["token_address"],
                     str(delta["delta_raw"]), delta.get("token_decimals"),
                     str(delta["delta_amount"]), delta.get("swap_side")),
                )

        connection.execute(
            "DELETE FROM trader_token_timeline WHERE leaderboard_captured_at_utc=? AND rank<=?",
            (snapshot, rank_limit),
        )
        timeline_columns = ["leaderboard_captured_at_utc"] + TIMELINE_FIELDS + ["generated_at_utc"]
        placeholders = ",".join("?" for _ in timeline_columns)
        insert_sql = "INSERT INTO trader_token_timeline({}) VALUES ({})".format(
            ",".join(timeline_columns), placeholders
        )
        for row in timeline_rows:
            connection.execute(
                insert_sql,
                [snapshot] + [row.get(field) for field in TIMELINE_FIELDS] + [generated_at],
            )


def _signature_scan_summary(connection, rank, snapshot_captured_at_utc):
    raw_pages = connection.execute(
        """SELECT id,source,route,captured_at_utc,payload_json FROM raw_payloads
           WHERE source='solana' AND route LIKE ? AND captured_at_utc>=?
           ORDER BY id""",
        ("%leaderboard_rank={}&page=%".format(rank), snapshot_captured_at_utc),
    ).fetchall()
    parsed_pages = []
    for raw in raw_pages:
        page_match = re.search(r"(?:^|[?&])page=(\d+)", raw["route"])
        if not page_match:
            continue
        try:
            payload = json.loads(raw["payload_json"])
        except (TypeError, json.JSONDecodeError):
            continue
        result = payload.get("result") if isinstance(payload, dict) else None
        if not isinstance(result, list):
            result = []
        parsed_pages.append({
            "id": raw["id"], "page": int(page_match.group(1)),
            "captured_at_utc": raw["captured_at_utc"], "items": result,
        })
    starts = [index for index, page in enumerate(parsed_pages) if page["page"] == 1]
    if starts:
        parsed_pages = parsed_pages[starts[-1]:]

    signatures = {}
    for page in parsed_pages:
        for item in page["items"]:
            if isinstance(item, dict) and item.get("signature"):
                signatures[item["signature"]] = item
    observed_at = parsed_pages[-1]["captured_at_utc"] if parsed_pages else None
    cutoff = _timestamp(observed_at) - 60 * 86400 if observed_at else None
    block_times = []
    signatures_60d = 0
    for item in signatures.values():
        try:
            block_time = float(item["blockTime"])
        except (KeyError, TypeError, ValueError):
            continue
        block_times.append(block_time)
        if cutoff is not None and block_time >= cutoff:
            signatures_60d += 1
    earliest = min(block_times) if block_times else None
    latest = max(block_times) if block_times else None
    last_page_size = len(parsed_pages[-1]["items"]) if parsed_pages else 0
    if cutoff is None:
        state = "not_collected"
    elif earliest is not None and earliest <= cutoff:
        state = "covers_60d"
    elif parsed_pages and last_page_size < 1000:
        state = "history_exhausted"
    elif parsed_pages:
        state = "partial_coverage"
    else:
        state = "not_collected"
    age_days = round((latest - earliest) / 86400, 2) if earliest is not None and latest is not None else None
    return {
        "page_ids": [page["id"] for page in parsed_pages],
        "page_count": len(parsed_pages),
        "signature_count_60d": signatures_60d,
        "observed_at_utc": observed_at,
        "history_state": state,
        "earliest_at_utc": _utc(earliest),
        "latest_at_utc": _utc(latest),
        "observed_age_days": age_days,
    }


def build_top10_wallet_inventory(database, rank_limit=10, export=True):
    if rank_limit < 1:
        raise ValueError("rank_limit must be positive")
    store = Store(database)
    store.initialize()
    with store.connect() as connection:
        snapshot = connection.execute(
            "SELECT MAX(captured_at_utc) FROM leaderboard_snapshots WHERE period='30d'"
        ).fetchone()[0]
        if not snapshot:
            raise RuntimeError("No 30-day leaderboard snapshot is available")
        cohort = connection.execute(
            """SELECT l.rank,l.captured_at_utc,l.reported_pnl_usd,l.reported_volume_usd,
                      t.fomo_user_id,t.handle,t.display_name,t.solana_wallet_candidate,
                      t.evm_wallet_candidate
               FROM leaderboard_snapshots l JOIN traders t USING(fomo_user_id)
               WHERE l.period='30d' AND l.captured_at_utc=? AND l.rank<=?
               ORDER BY l.rank""",
            (snapshot, rank_limit),
        ).fetchall()
        generated_at = utc_now()
        for trader in cohort:
            rank = trader["rank"]
            user_id = trader["fomo_user_id"]
            scan = _signature_scan_summary(connection, rank, trader["captured_at_utc"])
            events = connection.execute(
                """SELECT chain,chain_id,captured_at_utc FROM fomo_events
                   WHERE fomo_user_id=?""",
                (user_id,),
            ).fetchall()
            chain_counts = Counter()
            chain_id_counts = Counter()
            solana_events = other_chain_events = since_snapshot = 0
            for event in events:
                chain = event["chain"] or "unknown"
                chain_counts[chain] += 1
                chain_key = "{}:{}".format(chain, event["chain_id"]) if event["chain_id"] is not None else chain
                chain_id_counts[chain_key] += 1
                if chain.lower() == "solana":
                    solana_events += 1
                else:
                    other_chain_events += 1
                if event["captured_at_utc"] and event["captured_at_utc"] > trader["captured_at_utc"]:
                    since_snapshot += 1

            def resolution_status(address):
                if not address:
                    return "not_available"
                resolution = connection.execute(
                    """SELECT status FROM wallet_resolutions
                       WHERE fomo_user_id=? AND lower(address)=lower(?)
                       ORDER BY CASE status WHEN 'verified' THEN 0 WHEN 'rejected' THEN 1 ELSE 2 END
                       LIMIT 1""",
                    (user_id, address),
                ).fetchone()
                if not resolution:
                    return "candidate_unverified"
                return {"verified": "verified", "rejected": "rejected"}.get(
                    resolution["status"], "candidate_unverified"
                )

            values = {
                "snapshot_at_utc": trader["captured_at_utc"],
                "rank": rank,
                "fomo_user_id": user_id,
                "handle": trader["handle"],
                "display_name": trader["display_name"],
                "reported_pnl_usd": trader["reported_pnl_usd"],
                "reported_volume_usd": trader["reported_volume_usd"],
                "solana_wallet_candidate": trader["solana_wallet_candidate"],
                "solana_resolution_status": resolution_status(trader["solana_wallet_candidate"]),
                "evm_wallet_candidate": trader["evm_wallet_candidate"],
                "evm_resolution_status": resolution_status(trader["evm_wallet_candidate"]),
                "solana_fomo_events": solana_events,
                "other_chain_fomo_events": other_chain_events,
                "solana_rpc_source": "Solana public mainnet RPC" if scan["page_count"] else None,
                "solana_rpc_observed_at_utc": scan["observed_at_utc"],
                "solana_history_state": scan["history_state"],
                "solana_signature_pages": scan["page_count"],
                "solana_signatures_60d": scan["signature_count_60d"],
                "solana_history_earliest_at_utc": scan["earliest_at_utc"],
                "solana_history_latest_at_utc": scan["latest_at_utc"],
                "solana_observed_age_days": scan["observed_age_days"],
                "total_fomo_events_current": len(events),
                "fomo_events_since_snapshot": since_snapshot,
                "event_chains_json": json.dumps(dict(sorted(chain_counts.items())),
                                                ensure_ascii=False, separators=(",", ":")),
                "event_chain_ids_json": json.dumps(dict(sorted(chain_id_counts.items())),
                                                   ensure_ascii=False, separators=(",", ":")),
                "raw_page_ids_json": json.dumps(scan["page_ids"], separators=(",", ":")),
                "generated_at_utc": generated_at,
            }
            columns = INVENTORY_DB_FIELDS
            update_columns = [field for field in columns
                              if field not in ("snapshot_at_utc", "fomo_user_id")]
            connection.execute(
                "INSERT INTO top10_wallet_inventory({}) VALUES ({}) "
                "ON CONFLICT(snapshot_at_utc,fomo_user_id) DO UPDATE SET {}".format(
                    ",".join(columns), ",".join("?" for _ in columns),
                    ",".join("{}=excluded.{}".format(field, field) for field in update_columns),
                ),
                [values[field] for field in columns],
            )

    output = store.database.parent / "top10_wallet_inventory.csv"
    if export:
        with store.connect() as connection:
            rows = [dict(row) for row in connection.execute(
                "SELECT {} FROM top10_wallet_inventory WHERE snapshot_at_utc=? AND rank<=? ORDER BY rank".format(
                    ",".join(INVENTORY_FIELDS)
                ),
                (snapshot, rank_limit),
            ).fetchall()]
        _write_csv(output, INVENTORY_FIELDS, rows)
    return {"snapshot_at_utc": snapshot, "inventory_rows": len(cohort), "output": str(output) if export else None}


def _export_research_csvs(database, snapshot, rank_limit, output_dir):
    store = Store(database)
    with store.connect() as connection:
        action_rows = [dict(row) for row in connection.execute(
            """SELECT rank,fomo_user_id,handle,wallet,signature,slot,block_time_utc,
                      transaction_successful,wallet_is_signer,action_type,classification_confidence,
                      swap_log_marker,transfer_log_marker,native_balance_delta_lamports,raw_source,raw_payload_id
               FROM solana_normalized_actions
               WHERE leaderboard_captured_at_utc=? AND rank<=?
               ORDER BY rank,block_time_utc,signature""",
            (snapshot, rank_limit),
        ).fetchall()]
        for row in action_rows:
            deltas = connection.execute(
                """SELECT token_address,delta_raw,token_decimals,delta_amount,swap_side
                   FROM solana_action_token_deltas
                   WHERE leaderboard_captured_at_utc=? AND signature=? AND wallet=?
                   ORDER BY token_address""",
                (snapshot, row["signature"], row["wallet"]),
            ).fetchall()
            row["transaction_successful"] = bool(row["transaction_successful"])
            row["wallet_is_signer"] = bool(row["wallet_is_signer"])
            row["swap_log_marker"] = bool(row["swap_log_marker"])
            row["transfer_log_marker"] = bool(row["transfer_log_marker"])
            row["token_deltas_json"] = json.dumps([dict(delta) for delta in deltas],
                                                  ensure_ascii=False, separators=(",", ":"))
        timeline_rows = [dict(row) for row in connection.execute(
            "SELECT {} FROM trader_token_timeline WHERE leaderboard_captured_at_utc=? AND rank<=? "
            "ORDER BY rank,token_address".format(",".join(TIMELINE_FIELDS)),
            (snapshot, rank_limit),
        ).fetchall()]
        inventory_rows = [dict(row) for row in connection.execute(
            "SELECT {} FROM top10_wallet_inventory WHERE snapshot_at_utc=? AND rank<=? ORDER BY rank".format(
                ",".join(INVENTORY_FIELDS)
            ),
            (snapshot, rank_limit),
        ).fetchall()]
        match_rows = [dict(row) for row in connection.execute(
            """SELECT l.rank,e.fomo_user_id,t.handle,e.chain,e.token_address,e.token_symbol,
                      e.event_type AS fomo_event_type,e.source_at_utc AS fomo_event_at_utc,
                      o.block_time_utc AS matched_onchain_at_utc,o.side AS matched_onchain_side,
                      m.delta_seconds,m.match_status AS event_match_status,
                      COALESCE(w.status,'candidate_unverified') AS wallet_resolution_status
               FROM event_trade_matches m
               JOIN fomo_events e ON e.event_id=m.fomo_event_id
               JOIN onchain_trades o ON o.signature=m.signature
               JOIN traders t ON t.fomo_user_id=e.fomo_user_id
               JOIN leaderboard_snapshots l ON l.fomo_user_id=e.fomo_user_id
               LEFT JOIN wallet_resolutions w ON w.fomo_user_id=e.fomo_user_id
                    AND lower(w.address)=lower(o.wallet)
               WHERE l.period='30d' AND l.captured_at_utc=? AND l.rank<=?
               ORDER BY l.rank,e.source_at_utc""",
            (snapshot, rank_limit),
        ).fetchall()]

    output_paths = {
        "inventory": output_dir / "top10_wallet_inventory.csv",
        "matches": output_dir / "top10_event_trade_matches.csv",
        "actions": output_dir / "solana_normalized_actions.csv",
        "timeline": output_dir / "trader_token_timeline.csv",
    }
    _write_csv(output_paths["inventory"], INVENTORY_FIELDS, inventory_rows)
    _write_csv(output_paths["matches"], EVENT_MATCH_FIELDS, match_rows)
    _write_csv(output_paths["actions"], ACTION_FIELDS, action_rows)
    _write_csv(output_paths["timeline"], TIMELINE_FIELDS, timeline_rows)
    return {key: str(value) for key, value in output_paths.items()}


def build_top_solana_timeline(database, rank_limit=10):
    if rank_limit < 1:
        raise ValueError("rank_limit must be positive")
    store = Store(database)
    store.initialize()
    output_dir = store.database.parent

    with store.connect() as connection:
        connection.row_factory = sqlite3.Row
        snapshot = connection.execute(
            "SELECT MAX(captured_at_utc) FROM leaderboard_snapshots WHERE period='30d'"
        ).fetchone()[0]
        if not snapshot:
            raise RuntimeError("No 30-day leaderboard snapshot is available")
        cohort = connection.execute(
            """SELECT l.rank,t.fomo_user_id,t.handle,t.solana_wallet_candidate AS wallet,
                      w.status AS wallet_status
               FROM leaderboard_snapshots l JOIN traders t USING(fomo_user_id)
               LEFT JOIN wallet_resolutions w ON w.fomo_user_id=t.fomo_user_id
                    AND w.chain='solana' AND lower(w.address)=lower(t.solana_wallet_candidate)
               WHERE l.period='30d' AND l.captured_at_utc=? AND l.rank<=?
               ORDER BY l.rank""",
            (snapshot, rank_limit),
        ).fetchall()
        verified = {row["rank"]: dict(row) for row in cohort
                    if row["wallet"] and row["wallet_status"] == "verified"}
        raw_pages = connection.execute(
            """SELECT id,route,payload_json FROM raw_payloads
               WHERE source='solana-quicknode'
                 AND route LIKE '/getTransactionsForAddress?leaderboard_rank=%'
                 AND captured_at_utc>=?
               ORDER BY id""",
            (snapshot,),
        ).fetchall()
        events = connection.execute(
            """SELECT l.rank,e.fomo_user_id,e.event_id,e.event_type,e.chain,e.token_address,
                      e.token_symbol,e.source_at_utc,e.captured_at_utc,t.handle
               FROM leaderboard_snapshots l JOIN fomo_events e USING(fomo_user_id)
               JOIN traders t USING(fomo_user_id)
               WHERE l.period='30d' AND l.captured_at_utc=? AND l.rank<=?
                 AND lower(COALESCE(e.chain,''))='solana' AND e.token_address IS NOT NULL
               ORDER BY l.rank,e.source_at_utc""",
            (snapshot, rank_limit),
        ).fetchall()
        indexed_pages = []
        owner_rpc_pages = []
        if connection.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='bigquery_solana_transactions'").fetchone():
            from .bigquery_solana import parse_wallet_row
            indexed_pages = connection.execute(
                """SELECT c.scope_json,c.wallet,c.fomo_user_id,c.role,t.signature,t.row_json,t.raw_payload_id
                   FROM bigquery_solana_transactions t JOIN bigquery_solana_collections c USING(collection_key)
                   WHERE c.retrieval_status='complete' AND c.role IN ('known_receipts','owner_details')
                   ORDER BY c.imported_at_utc,t.block_time_utc,t.signature"""
            ).fetchall()
        if indexed_pages:
            owner_rpc_pages = connection.execute(
                """SELECT c.scope_json,c.wallet,c.fomo_user_id,p.id,p.source,p.payload_json
                   FROM bigquery_solana_collections c JOIN bridge_routes b
                        ON b.destination_wallet=c.wallet AND b.evidence_status='order_correlated'
                   JOIN bridge_deposits d ON d.deposit_key=b.deposit_key AND d.case_key=c.case_key
                   JOIN raw_payloads p ON p.id=b.destination_raw_payload_id
                   WHERE c.role='known_receipts' AND c.retrieval_status='complete'"""
            ).fetchall()
            if connection.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='bigquery_solana_rpc_checks'").fetchone():
                owner_rpc_pages += connection.execute(
                    """SELECT c.scope_json,c.wallet,c.fomo_user_id,p.id,p.source,p.payload_json
                       FROM bigquery_solana_collections c JOIN raw_payloads p ON p.id IN (
                           SELECT DISTINCT raw_payload_id FROM bigquery_solana_rpc_checks v
                           WHERE v.collection_key=c.collection_key AND v.status='verified')
                       WHERE c.role='owner_details' AND c.retrieval_status='complete'"""
                ).fetchall()
            if connection.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='bigquery_solana_owner_rpc_pages'").fetchone():
                owner_rpc_pages += connection.execute(
                    """SELECT c.scope_json,c.wallet,c.fomo_user_id,p.id,p.source,p.payload_json
                       FROM bigquery_solana_collections c JOIN bigquery_solana_owner_rpc_pages v USING(collection_key)
                       JOIN raw_payloads p ON p.id=v.raw_payload_id
                       WHERE c.role='owner_details' AND c.retrieval_status='complete' ORDER BY v.page_index"""
                ).fetchall()
        matches = connection.execute(
            """SELECT e.fomo_user_id,e.token_address,e.event_id,m.signature,m.delta_seconds,
                      m.match_status,o.block_time_utc,o.side
               FROM fomo_events e JOIN event_trade_matches m ON m.fomo_event_id=e.event_id
               JOIN onchain_trades o ON o.signature=m.signature
               WHERE lower(COALESCE(e.chain,''))='solana'"""
        ).fetchall()

    matches_by_signature = defaultdict(dict)
    for match in matches:
        if match["match_status"] == "verified":
            matches_by_signature[match["signature"]][match["token_address"]] = match["side"]

    action_rows = []
    actions_by_rank_mint = defaultdict(list)
    transaction_counts = Counter()
    signatures_seen = set()
    latest_time_by_rank = {}
    source_pages = []
    known_bridge_receipts = {}
    for page in indexed_pages:
        if page["role"] == "known_receipts":
            for route in json.loads(page["scope_json"])["bridge_routes"]:
                known_bridge_receipts[(route["destination_tx_hash"], page["wallet"])] = route
    for page in raw_pages:
        source_pages.append({"id": page["id"], "route": page["route"], "raw_source": "solana-quicknode",
                             "items": (json.loads(page["payload_json"]).get("result") or {}).get("data") or []})
    for page in owner_rpc_pages:
        scope = json.loads(page["scope_json"])
        trader = verified.get(scope["rank"])
        if scope["leaderboard_snapshot_at_utc"] != snapshot or not trader or trader["fomo_user_id"] != page["fomo_user_id"] or trader["wallet"] != page["wallet"]:
            continue
        item = json.loads(page["payload_json"])["response"].get("result")
        if isinstance(item, dict):
            items = item.get("data") if isinstance(item.get("data"), list) else [item]
            source_pages.append({"id": page["id"], "route": "leaderboard_rank=" + str(scope["rank"]),
                                 "raw_source": page["source"], "items": items})
    for page in indexed_pages:
        scope = json.loads(page["scope_json"])
        trader = verified.get(scope["rank"])
        if scope["leaderboard_snapshot_at_utc"] != snapshot or not trader or trader["fomo_user_id"] != page["fomo_user_id"] or trader["wallet"] != page["wallet"]:
            continue
        source_pages.append({"id": page["raw_payload_id"], "route": "leaderboard_rank=" + str(scope["rank"]),
                             "raw_source": "bigquery_solana", "items": [json.loads(page["row_json"])]})
    for raw_page in source_pages:
        match = RANK_ROUTE.search(raw_page["route"])
        rank = int(match.group(1)) if match else None
        trader = verified.get(rank)
        if not trader or not trader["wallet"]:
            continue
        for item in raw_page["items"]:
            parsed = (parse_wallet_row(item, trader["wallet"], matches_by_signature)
                      if raw_page["raw_source"] == "bigquery_solana"
                      else _wallet_changes(item, trader["wallet"], matches_by_signature))
            bridge = known_bridge_receipts.get((parsed["signature"], trader["wallet"]))
            if bridge:
                proof = bridge["rpc_check"]
                expected = (bridge["destination_amount_raw"], bridge["destination_decimals"])
                delta = next((d for d in parsed["token_deltas"] if d["token_address"] == bridge["destination_asset"]), None)
                if not (proof["canonical_transfer_matches"] and proof["deposit_id_memo_matches"] and proof["operation_id_memo_matches"]
                        and parsed["successful"] and parsed["slot"] == proof["slot"] and parsed["block_time_utc"] == bridge["destination_at_utc"]
                        and delta and (delta["delta_raw"], delta["token_decimals"]) == expected):
                    raise ValueError("Retained bridge transfer proof differs from normalized owner evidence")
                parsed["action_type"] = "TRANSFER"
                parsed["classification_confidence"] = "verified_bridge_order_and_spl_transfer_balance_delta"
                for change in parsed["token_deltas"]:
                    change["swap_side"] = None
            # Balance-only discovery has unknown signer/instruction semantics; retain it in source tables.
            if parsed["wallet_is_signer"] is None:
                continue
            # A signature can involve multiple tracked wallets; retain one action per wallet.
            signature_key = (rank, parsed["signature"])
            if not parsed["signature"] or signature_key in signatures_seen:
                continue
            signatures_seen.add(signature_key)
            transaction_counts[parsed["action_type"]] += 1
            if parsed["block_time_utc"]:
                prev = latest_time_by_rank.get(rank)
                if not prev:
                    latest_time_by_rank[rank] = [parsed["block_time_utc"], parsed["block_time_utc"]]
                else:
                    prev[0] = min(prev[0], parsed["block_time_utc"])
                    prev[1] = max(prev[1], parsed["block_time_utc"])
            action_rows.append({
                "rank": rank,
                "fomo_user_id": trader["fomo_user_id"],
                "handle": trader["handle"],
                "wallet": trader["wallet"],
                "signature": parsed["signature"],
                "slot": parsed["slot"],
                "block_time_utc": parsed["block_time_utc"],
                "transaction_successful": parsed["successful"],
                "wallet_is_signer": parsed["wallet_is_signer"],
                "action_type": parsed["action_type"],
                "classification_confidence": parsed["classification_confidence"],
                "swap_log_marker": parsed["swap_log_marker"],
                "transfer_log_marker": parsed["transfer_log_marker"],
                "native_balance_delta_lamports": parsed["native_balance_delta_lamports"],
                "token_deltas_json": json.dumps(parsed["token_deltas"], ensure_ascii=False, separators=(",", ":")),
                "raw_source": raw_page["raw_source"],
                "raw_payload_id": raw_page["id"],
            })
            for change in parsed["token_deltas"]:
                if parsed["action_type"] == "SWAP" and change["swap_side"]:
                    actions_by_rank_mint[(rank, change["token_address"])].append(
                        (parsed["block_time_utc"], change["swap_side"], parsed["signature"])
                    )

    timeline_rows = []
    events_by_token = defaultdict(list)
    for event in events:
        trader = verified.get(event["rank"])
        if trader and event["fomo_user_id"] == trader["fomo_user_id"]:
            events_by_token[(event["rank"], event["fomo_user_id"], event["token_address"])].append(dict(event))

    matches_by_token = defaultdict(list)
    for match in matches:
        matches_by_token[(match["fomo_user_id"], match["token_address"])].append(dict(match))

    for (rank, user_id, token), token_events in sorted(events_by_token.items()):
        trader = verified[rank]
        fomo_by_type = defaultdict(list)
        for event in token_events:
            if event["source_at_utc"]:
                fomo_by_type[event["event_type"]].append(event["source_at_utc"])
        swaps = actions_by_rank_mint.get((rank, token), [])
        buys = sorted((row for row in swaps if row[1] == "BUY" and row[0]), key=lambda row: row[0])
        sells = sorted((row for row in swaps if row[1] == "SELL" and row[0]), key=lambda row: row[0])
        token_matches = matches_by_token.get((user_id, token), [])
        verified_matches = [row for row in token_matches if row["match_status"] == "verified"]
        matched_times = sorted({row["block_time_utc"] for row in verified_matches if row["block_time_utc"]})
        first_buy = buys[0][0] if buys else None
        fomo_buy = min(fomo_by_type.get("BUY", []), default=None)
        first_sell = sells[0][0] if sells else None
        buy_delay = None
        if first_buy and fomo_buy and _timestamp(first_buy) is not None and _timestamp(fomo_buy) is not None:
            buy_delay = _timestamp(fomo_buy) - _timestamp(first_buy)
        window = latest_time_by_rank.get(rank, [None, None])
        timeline_rows.append({
            "rank": rank,
            "fomo_user_id": user_id,
            "handle": trader["handle"],
            "chain": "solana",
            "wallet": trader["wallet"],
            "token_address": token,
            "token_symbol": next((event["token_symbol"] for event in token_events if event["token_symbol"]), None),
            "wallet_resolution_status": trader["wallet_status"],
            "t1_first_observed_onchain_buy_at_utc": first_buy,
            "t2_fomo_buy_at_utc": fomo_buy,
            "fomo_sell_at_utc": min(fomo_by_type.get("SELL", []), default=None),
            "t3_fomo_thesis_at_utc": min(fomo_by_type.get("THESIS", []), default=None),
            "t4_x_post_at_utc": None,
            "t5_first_observed_onchain_sell_at_utc": first_sell,
            "matched_onchain_at_utc": ";".join(matched_times),
            "verified_match_count": len(verified_matches),
            "matched_event_delta_seconds": ";".join(str(row["delta_seconds"]) for row in verified_matches),
            "first_observed_buy_to_fomo_buy_seconds": buy_delay,
            "swap_buy_count_in_history": len(buys),
            "swap_sell_count_in_history": len(sells),
            "history_start_at_utc": window[0],
            "history_end_at_utc": window[1],
            "history_normalization": "SWAP: swap instruction/event log or verified Fomo match plus signer and opposing balances; TRANSFER: transfer log or verified bridge SPL transfer proof",
            "coverage_note": "Observed EOA history plus full owner/token-account RPC pages in a fixed window. Balance-only rows without RPC retain unknown semantics. Earlier activity, historical-owner indexing and full native-only coverage are not proven complete. X posts are not collected.",
        })

    _persist_research_rows(
        database, snapshot, rank_limit,
        [trader["fomo_user_id"] for trader in verified.values()],
        action_rows, timeline_rows,
    )
    inventory_result = build_top10_wallet_inventory(database, rank_limit, export=False)
    outputs = _export_research_csvs(database, snapshot, rank_limit, output_dir)
    return {
        "snapshot_at_utc": snapshot,
        "rank_limit": rank_limit,
        "verified_wallets_processed": len(verified),
        "transactions_processed": len(action_rows),
        "action_counts": dict(transaction_counts),
        "timeline_rows": len(timeline_rows),
        "inventory_rows": inventory_result["inventory_rows"],
        "sqlite_tables": ["solana_normalized_actions", "solana_action_token_deltas",
                          "trader_token_timeline", "top10_wallet_inventory"],
        "outputs": outputs,
    }
