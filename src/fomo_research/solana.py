import json
import re
import sqlite3
from datetime import datetime, timezone
from decimal import Decimal
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .config import load_solana_rpc_url
from .store import Store, utc_now


SWAP_LOG = re.compile(r"\b(swap|route|jupiter|raydium|orca|meteora)\b", re.IGNORECASE)


def _iso_from_seconds(value):
    if value is None:
        return None
    return datetime.fromtimestamp(value, timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _post_rpc(method, params, route, store, timeout=30):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode("utf-8")
    request = Request(load_solana_rpc_url(), data=body, headers={"Content-Type": "application/json", "Accept": "application/json"})
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
            captured_at = utc_now()
            with store.connect() as connection:
                raw_id = store.save_raw(connection, "solana", route, payload, captured_at, response.status)
            return payload, raw_id, captured_at
    except HTTPError as error:
        raise RuntimeError("Solana RPC request failed: HTTP {} for {}".format(error.code, route)) from None
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        raise RuntimeError("Solana RPC request failed for {} ({})".format(route, type(error).__name__)) from None


def _token_amounts(rows, wallet):
    amounts = {}
    for row in rows or []:
        if row.get("owner") != wallet or not row.get("mint"):
            continue
        amount = row.get("uiTokenAmount") or {}
        mint = row["mint"]
        decimals = amount.get("decimals")
        prior = amounts.get(mint, {"amount": 0, "decimals": decimals})
        prior["amount"] += int(amount.get("amount", "0"))
        if decimals is not None:
            prior["decimals"] = decimals
        amounts[mint] = prior
    return amounts


def _ui_amount(raw, decimals):
    return Decimal(raw) / (Decimal(10) ** (decimals or 0))


def _transaction_evidence(transaction, wallet, token, expected_side):
    meta = transaction.get("meta") or {}
    message = ((transaction.get("transaction") or {}).get("message") or {})
    keys = message.get("accountKeys") or []
    wallet_index = None
    signer = False
    for index, key in enumerate(keys):
        if isinstance(key, dict):
            if key.get("pubkey") == wallet:
                wallet_index = index
                signer = key.get("signer") is True
                break
        elif key == wallet:
            wallet_index = index
            signer = index == 0
            break

    pre = _token_amounts(meta.get("preTokenBalances"), wallet)
    post = _token_amounts(meta.get("postTokenBalances"), wallet)
    all_mints = set(pre) | set(post)
    deltas = {}
    decimals = {}
    for mint in all_mints:
        before = pre.get(mint, {}).get("amount", 0)
        after = post.get(mint, {}).get("amount", 0)
        deltas[mint] = after - before
        decimals[mint] = post.get(mint, {}).get("decimals", pre.get(mint, {}).get("decimals"))

    token_delta = deltas.get(token, 0)
    token_decimals = decimals.get(token)
    side_matches = token_delta > 0 if expected_side == "BUY" else token_delta < 0 if expected_side == "SELL" else False
    quote_direction = -1 if expected_side == "BUY" else 1
    quote_candidates = [
        (mint, delta, decimals.get(mint))
        for mint, delta in deltas.items()
        if mint != token and delta * quote_direction > 0
    ]
    quote_candidates.sort(key=lambda item: abs(_ui_amount(item[1], item[2])), reverse=True)
    quote_mint, quote_delta, quote_decimals = quote_candidates[0] if quote_candidates else (None, None, None)

    pre_balances = meta.get("preBalances") or []
    post_balances = meta.get("postBalances") or []
    native_delta = None
    if wallet_index is not None and wallet_index < len(pre_balances) and wallet_index < len(post_balances):
        native_delta = post_balances[wallet_index] - pre_balances[wallet_index]
    fee = meta.get("fee") or 0
    native_quote_move = (
        native_delta is not None and
        ((expected_side == "BUY" and -native_delta > fee) or
         (expected_side == "SELL" and native_delta > fee))
    )
    log_messages = meta.get("logMessages") or []
    swap_log_marker = any(SWAP_LOG.search(line) for line in log_messages)
    successful = meta.get("err") is None
    quote_move = quote_delta is not None or native_quote_move
    strong = successful and signer and side_matches and (quote_move or swap_log_marker)

    return {
        "successful": successful,
        "wallet_is_signer": signer,
        "wallet_index": wallet_index,
        "token_delta_raw": token_delta,
        "token_decimals": token_decimals,
        "expected_side": expected_side,
        "side_matches_token_delta": side_matches,
        "quote_mint": quote_mint,
        "quote_delta_raw": quote_delta,
        "quote_decimals": quote_decimals,
        "native_balance_delta_lamports": native_delta,
        "transaction_fee_lamports": fee,
        "native_quote_move": native_quote_move,
        "swap_log_marker": swap_log_marker,
        "strong_match": strong,
        "transaction": transaction,
    }


def _candidate_event(database, rank=None):
    with sqlite3.connect(str(database)) as connection:
        row = connection.execute(
            """SELECT e.event_id, e.fomo_user_id, e.event_type, e.token_address,
                      e.source_at_utc, t.solana_wallet_candidate, ls.rank
               FROM fomo_events e
               JOIN traders t ON t.fomo_user_id=e.fomo_user_id
               JOIN leaderboard_snapshots ls
                 ON ls.fomo_user_id=e.fomo_user_id
                AND ls.period='30d'
                AND ls.captured_at_utc=(
                    SELECT MAX(captured_at_utc) FROM leaderboard_snapshots WHERE period='30d'
                )
               WHERE e.chain='solana' AND e.event_type IN ('BUY','SELL')
                 AND e.token_address IS NOT NULL AND t.solana_wallet_candidate IS NOT NULL
                 AND ls.rank BETWEEN 1 AND 10
                 AND (? IS NULL OR ls.rank=?)
                 AND NOT EXISTS (
                     SELECT 1 FROM event_trade_matches m WHERE m.fomo_event_id=e.event_id
                 )
               ORDER BY ls.rank, e.source_at_utc DESC
               LIMIT 1""",
            (rank, rank),
        ).fetchone()
    if not row:
        return None
    keys = ("event_id", "fomo_user_id", "event_type", "token_address", "source_at_utc", "wallet", "rank")
    return dict(zip(keys, row))


def match_top_solana_event(database, window_seconds=120, max_pages=10, page_size=100, rank=None):
    if window_seconds < 1 or max_pages < 1 or page_size < 1 or page_size > 1000:
        raise ValueError("window_seconds/max_pages must be positive and page_size must be 1-1000")
    if rank is not None and (rank < 1 or rank > 10):
        raise ValueError("rank must be between 1 and 10")
    store = Store(database)
    store.initialize()
    event = _candidate_event(database, rank)
    if not event:
        return {"pending_events": 0, "match_attempted": False, "stored": False}
    event_at = datetime.fromisoformat(event["source_at_utc"].replace("Z", "+00:00"))
    event_ts = event_at.timestamp()
    before = None
    signatures = []
    pages = 0

    for page_number in range(max_pages):
        options = {"commitment": "finalized", "limit": page_size}
        if before:
            options["before"] = before
        payload, _raw_id, _captured = _post_rpc(
            "getSignaturesForAddress", [event["wallet"], options],
            "/getSignaturesForAddress?limit={}&page={}".format(page_size, page_number + 1), store)
        if payload.get("error"):
            error = payload["error"]
            raise RuntimeError("Solana RPC returned error code {} for getSignaturesForAddress".format(error.get("code")))
        rows = payload.get("result")
        if not isinstance(rows, list):
            raise RuntimeError("Solana RPC returned no signature list")
        pages += 1
        signatures.extend(row for row in rows if row.get("blockTime") is not None and row.get("err") is None)
        if not rows or len(rows) < page_size:
            break
        before = rows[-1].get("signature")
        oldest = min((row.get("blockTime") for row in rows if row.get("blockTime") is not None), default=None)
        if oldest is not None and oldest < event_ts - window_seconds:
            break

    nearby = [row for row in signatures if abs(row["blockTime"] - event_ts) <= window_seconds]
    nearby.sort(key=lambda row: abs(row["blockTime"] - event_ts))
    candidates = []
    checked = 0
    for signature_row in nearby[:50]:
        signature = signature_row["signature"]
        max_version = 1
        tx_payload = None
        raw_id = None
        captured_at = None
        for _attempt in range(3):
            tx_payload, raw_id, captured_at = _post_rpc(
                "getTransaction",
                [signature, {"commitment": "confirmed", "encoding": "jsonParsed",
                             "maxSupportedTransactionVersion": max_version}],
                "/getTransaction?encoding=jsonParsed&maxSupportedTransactionVersion={}".format(max_version), store)
            rpc_error = tx_payload.get("error") or {}
            if not rpc_error:
                break
            required = re.search(r"maxSupportedTransactionVersion[^0-9]*(\d+)", str(rpc_error.get("message", "")))
            if not required or int(required.group(1)) <= max_version:
                tx_payload = None
                break
            max_version = int(required.group(1))
        checked += 1
        if not tx_payload or not tx_payload.get("result"):
            continue
        transaction = tx_payload["result"]
        evidence = _transaction_evidence(transaction, event["wallet"], event["token_address"], event["event_type"])
        block_time = transaction.get("blockTime") or signature_row.get("blockTime")
        delta = abs(block_time - event_ts) if block_time is not None else abs(signature_row["blockTime"] - event_ts)
        candidates.append({"signature": signature, "slot": transaction.get("slot"),
                           "block_time_utc": _iso_from_seconds(block_time), "delta_seconds": delta,
                           "raw_payload_id": raw_id, "captured_at": captured_at, "evidence": evidence})

    strong = [candidate for candidate in candidates
              if candidate["delta_seconds"] <= window_seconds and candidate["evidence"]["strong_match"]]
    result = {"rank": event["rank"], "event_type": event["event_type"], "signature_pages": pages,
              "nearby_signatures": len(nearby), "transactions_checked": checked,
              "strong_matches": len(strong), "event_match_found": len(strong) == 1,
              "verified": False,
              "time_delta_seconds": strong[0]["delta_seconds"] if len(strong) == 1 else None}
    if len(strong) == 1:
        candidate = strong[0]
        proof = candidate["evidence"]
        evidence = {
            "source": "solana-mainnet-public-rpc",
            "fomo_event_type": event["event_type"],
            "transaction_success": proof["successful"],
            "wallet_is_signer": proof["wallet_is_signer"],
            "token_side_matches": proof["side_matches_token_delta"],
            "quote_asset_balance_move": proof["quote_delta_raw"] is not None or proof["native_quote_move"],
            "swap_log_marker": proof["swap_log_marker"],
            "delta_seconds": candidate["delta_seconds"],
        }
        with sqlite3.connect(str(database)) as connection:
            raw_row = connection.execute("SELECT id FROM raw_payloads WHERE id=?", (candidate["raw_payload_id"],)).fetchone()
        if raw_row:
            saved = store.save_onchain_match(
                event["event_id"], event["fomo_user_id"], event["wallet"], candidate["signature"],
                candidate["slot"], candidate["block_time_utc"], event["token_address"],
                event["event_type"], abs(proof["token_delta_raw"]), proof["token_decimals"],
                proof["quote_mint"], abs(proof["quote_delta_raw"]) if proof["quote_delta_raw"] is not None else None,
                proof["quote_decimals"], candidate["raw_payload_id"], candidate["captured_at"],
                candidate["delta_seconds"], evidence)
            result["stored"] = saved["inserted"]
            result["wallet_status"] = saved["status"]
            result["matched_event_count"] = saved["matched_event_count"]
            result["matched_signature_count"] = saved["matched_signature_count"]
            result["verified"] = saved["status"] == "verified"
            result["event_match_status"] = "verified" if result["verified"] else "candidate"
            result["evidence"] = {key: value for key, value in evidence.items() if key != "source"}
    elif len(strong) > 1:
        ambiguous_stored = 0
        for candidate in strong:
            proof = candidate["evidence"]
            evidence = {
                "source": "solana-mainnet-public-rpc",
                "fomo_event_type": event["event_type"],
                "transaction_success": proof["successful"],
                "wallet_is_signer": proof["wallet_is_signer"],
                "token_side_matches": proof["side_matches_token_delta"],
                "quote_asset_balance_move": proof["quote_delta_raw"] is not None or proof["native_quote_move"],
                "swap_log_marker": proof["swap_log_marker"],
                "delta_seconds": candidate["delta_seconds"],
                "strong_candidates_for_event": len(strong),
            }
            saved = store.save_ambiguous_onchain_match(
                event["event_id"], event["wallet"], candidate["signature"], candidate["slot"],
                candidate["block_time_utc"], event["token_address"], event["event_type"],
                abs(proof["token_delta_raw"]), proof["token_decimals"], proof["quote_mint"],
                abs(proof["quote_delta_raw"]) if proof["quote_delta_raw"] is not None else None,
                proof["quote_decimals"], candidate["raw_payload_id"], candidate["captured_at"],
                candidate["delta_seconds"], evidence,
            )
            ambiguous_stored += int(saved["inserted"])
        result["stored_ambiguous_matches"] = ambiguous_stored
        result["event_match_status"] = "ambiguous"
        result["stored"] = ambiguous_stored > 0
    else:
        resolution = store.refresh_wallet_resolution(event["fomo_user_id"], event["wallet"])
        if resolution["recorded"]:
            result["wallet_status"] = resolution["status"]
            result["matched_event_count"] = resolution["matched_event_count"]
            result["matched_signature_count"] = resolution["matched_signature_count"]
            result["verified"] = resolution["status"] == "verified"
    return result


def _event_count(database, user_id):
    with sqlite3.connect(str(database)) as connection:
        return connection.execute(
            "SELECT COUNT(*) FROM fomo_events WHERE fomo_user_id=? AND chain='solana'",
            (user_id,),
        ).fetchone()[0]
