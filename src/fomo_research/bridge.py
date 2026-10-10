"""Resolve a bounded set of receipt-backed bridge deposits and preserve evidence."""

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from .config import DEFAULT_DATABASE, REPO_ROOT, load_solana_rpc_url
from .etherscan_flow import _units
from .store import Store, _json, utc_now


SOLANA_MAINNET = "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp"
SOLANA_PUBLIC_RPC = "https://api.mainnet-beta.solana.com"
DEPOSIT_TOPIC = "0x49fed1d0b752ce30eee63c7a81133f3363b532fec5d4d7dd1ccfd005de4555e1"
SCHEMA = """
CREATE TABLE IF NOT EXISTS bridge_deposits (
    deposit_key TEXT PRIMARY KEY,
    case_key TEXT NOT NULL REFERENCES evm_flow_cases(case_key),
    source_chain_id INTEGER NOT NULL,
    source_tx_hash TEXT NOT NULL,
    source_log_index INTEGER NOT NULL,
    source_at_utc TEXT NOT NULL,
    from_address TEXT NOT NULL,
    to_address TEXT NOT NULL,
    token_address TEXT NOT NULL,
    amount_raw TEXT NOT NULL,
    token_decimals INTEGER NOT NULL,
    deposit_id TEXT,
    deposit_event_locator TEXT,
    source_raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
    FOREIGN KEY (case_key, source_chain_id, source_tx_hash, source_log_index)
      REFERENCES evm_flow_movements(case_key, chain_id, tx_hash, log_index)
);
CREATE TABLE IF NOT EXISTS bridge_resolve_requests (
    request_key TEXT PRIMARY KEY,
    case_key TEXT NOT NULL REFERENCES evm_flow_cases(case_key),
    endpoint TEXT NOT NULL,
    source_chain TEXT NOT NULL,
    source_tx_hash TEXT NOT NULL,
    fetched_at_utc TEXT NOT NULL,
    http_status INTEGER,
    raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
    evaluation_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS bridge_rpc_requests (
    request_key TEXT PRIMARY KEY,
    chain TEXT NOT NULL,
    tx_hash TEXT NOT NULL,
    provider TEXT NOT NULL,
    fetched_at_utc TEXT NOT NULL,
    http_status INTEGER,
    result_state TEXT NOT NULL,
    raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id)
);
CREATE TABLE IF NOT EXISTS bridge_routes (
    route_key TEXT PRIMARY KEY,
    deposit_key TEXT NOT NULL REFERENCES bridge_deposits(deposit_key),
    request_key TEXT NOT NULL REFERENCES bridge_resolve_requests(request_key),
    provider TEXT NOT NULL,
    operation_id TEXT NOT NULL,
    provider_status TEXT NOT NULL,
    provider_raw_status TEXT NOT NULL,
    observed_at_utc TEXT,
    output_leg_index INTEGER NOT NULL,
    destination_chain TEXT NOT NULL,
    destination_tx_hash TEXT NOT NULL,
    destination_wallet TEXT NOT NULL,
    destination_asset TEXT NOT NULL,
    destination_asset_kind TEXT NOT NULL,
    destination_amount_raw TEXT NOT NULL,
    destination_decimals INTEGER,
    destination_at_utc TEXT,
    wallet_resolution_status TEXT NOT NULL,
    evidence_status TEXT NOT NULL,
    destination_raw_payload_id INTEGER REFERENCES raw_payloads(id),
    evidence_json TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_bridge_routes_destination
 ON bridge_routes(destination_chain,destination_wallet,destination_tx_hash);
"""


def _digest(value):
    return hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


def _iso(timestamp):
    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat().replace("+00:00", "Z") if timestamp is not None else None


def _post(url, body, provider=None):
    started = utc_now()
    request = Request(url, data=_json(body).encode(), headers={"Content-Type": "application/json", "Accept": "application/json"}, method="POST")
    try:
        with urlopen(request, timeout=55) as response:
            status, text = response.status, response.read().decode()
    except HTTPError as error:
        status, text = error.code, error.read().decode()
    except (URLError, TimeoutError, OSError) as error:
        status, text = None, _json({"transport_error": type(error).__name__})
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        payload = {"unparsed_body": text}
    record = {"request": body, "started_at": started, "completed_at": utc_now(), "http_status": status, "response": payload}
    if provider:
        record.update(provider=provider, route="getTransaction")
    else:
        record["url"] = url
    return record


def _write_capture(directory, record):
    path = directory / (_digest(record) + ".json")
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    os.chmod(path, 0o600)


def _load_scope(connection, case_key, recipient):
    case = connection.execute("SELECT * FROM evm_flow_cases WHERE case_key=?", (case_key,)).fetchone() if case_key else connection.execute("SELECT * FROM evm_flow_cases ORDER BY imported_at_utc DESC LIMIT 1").fetchone()
    if case is None or case["chain_id"] != 1:
        raise ValueError("Select an existing Ethereum tracing case")
    if not connection.execute("SELECT 1 FROM wallet_resolutions WHERE fomo_user_id=? AND chain='ethereum' AND lower(address)=? AND status='verified'", (case["fomo_user_id"], case["seed_address"].lower())).fetchone():
        raise ValueError("The tracing seed must still have a verified Ethereum resolution")
    rows = connection.execute("SELECT * FROM evm_flow_movements WHERE case_key=? AND relation='seed' AND from_address=? AND to_address=? ORDER BY block_time_utc,log_index", (case["case_key"], case["seed_address"].lower(), recipient.lower())).fetchall()
    if not rows:
        raise ValueError("No receipt-backed outbound seed transfers to this recipient")
    return dict(case), [dict(row) for row in rows]


def collect(database, recipient, case_key, api_url, directory, max_transactions):
    parsed = urlsplit(api_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("Use a credential-free HTTP(S) Bridge API base URL")
    with Store(database).connect() as connection:
        case, movements = _load_scope(connection, case_key, recipient)
    hashes = list(dict.fromkeys(row["tx_hash"] for row in movements))
    if len(hashes) > max_transactions:
        raise ValueError("Requested deposits exceed the explicit transaction limit")
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    checked = set()
    for tx_hash in hashes:
        record = _post(api_url.rstrip("/") + "/v1/bridge/resolve", {"sourceChain": "eip155:1", "sourceTransactionHash": tx_hash})
        _write_capture(directory, record)
        payload = record["response"]
        for observation in payload.get("observations", []):
            # A batch transaction may contain orders from multiple users.
            if not any(leg.get("role") == "input" and leg.get("accountAddress", "").lower() == case["seed_address"].lower() for leg in observation.get("providerAssertion", {}).get("assetLegs", [])):
                continue
            for destination in observation.get("providerAssertion", {}).get("destinations", []):
                signature = destination.get("transactionHash")
                if destination.get("chain") != SOLANA_MAINNET or not signature or signature in checked:
                    continue
                checked.add(signature)
                body = {"jsonrpc": "2.0", "id": 1, "method": "getTransaction", "params": [signature, {"encoding": "jsonParsed", "commitment": "finalized", "maxSupportedTransactionVersion": 0}]}
                rpc = _post(load_solana_rpc_url(), body, "configured_solana_rpc")
                _write_capture(directory, rpc)
                if rpc["http_status"] == 200 and rpc["response"].get("result") is None and "error" not in rpc["response"]:
                    _write_capture(directory, _post(SOLANA_PUBLIC_RPC, body, "solana_public_mainnet"))
    return case["case_key"]


def _receipt(connection, movement):
    raw = json.loads(connection.execute("SELECT payload_json FROM raw_payloads WHERE id=?", (movement["raw_payload_id"],)).fetchone()[0])["result"]
    receipt = raw.get("result", raw)
    if receipt.get("status") != "0x1" or receipt["transactionHash"].lower() != movement["tx_hash"]:
        raise ValueError("Source movement lacks a successful matching receipt")
    deposits = []
    for log in receipt.get("logs", []):
        data = log.get("data", "")[2:]
        if log["address"].lower() != movement["to_address"] or log.get("topics", []) != [DEPOSIT_TOPIC] or len(data) != 256:
            continue
        if ("0x" + data[24:64]).lower() == movement["from_address"] and ("0x" + data[88:128]).lower() == movement["token_address"] and int(data[128:192], 16) == int(movement["amount_raw"]):
            deposits.append(("0x" + data[192:256], "log:" + str(int(log["logIndex"], 16))))
    if len(deposits) > 1:
        raise ValueError("Ambiguous deposit events for the selected source transfer")
    return receipt, deposits[0] if deposits else (None, None)


def _input_matches(observation, payload, movement, receipt):
    transaction = {"chain": "eip155:1", "transactionHash": movement["tx_hash"]}
    if observation.get("source") != transaction:
        return False
    source = observation.get("canonicalSourceEvidence") or payload.get("sourceEvidence") or payload.get("seedEvidence") or {}
    if source.get("transaction") != transaction or source.get("blockHash", "").lower() != receipt["blockHash"].lower() or int(source.get("blockNumber") or "0", 0) != int(receipt["blockNumber"], 16):
        return False
    transfers = (source.get("assetEvidence") or {}).get("transfers", [])
    actual = any(t.get("transaction") == transaction and t.get("asset", {}).get("identifier", "").lower() == movement["token_address"] and t.get("asset", {}).get("chain") == "eip155:1" and t.get("asset", {}).get("kind") == "erc20" and t.get("fromAddress", "").lower() == movement["from_address"] and t.get("toAddress", "").lower() == movement["to_address"] and t.get("rawAmount") == movement["amount_raw"] and t.get("locator") == "log:" + str(movement["log_index"]) for t in transfers)
    return actual and any(leg.get("role") == "input" and leg.get("basis") == "actual" and leg.get("transaction") == transaction and leg.get("asset", {}).get("identifier", "").lower() == movement["token_address"] and leg.get("asset", {}).get("chain") == "eip155:1" and leg.get("asset", {}).get("kind") == "erc20" and leg.get("accountAddress", "").lower() == movement["from_address"] and leg.get("rawAmount") == movement["amount_raw"] for leg in observation.get("providerAssertion", {}).get("assetLegs", []))


def _verify_solana(record, leg, observation, deposit_id):
    result = record["response"].get("result")
    if not isinstance(result, dict):
        return None
    meta = result.get("meta") or {}
    transaction = result.get("transaction") or {}
    signature = leg["transaction"]["transactionHash"]
    message = transaction.get("message") or {}
    keys = [key.get("pubkey") if isinstance(key, dict) else key for key in message.get("accountKeys", [])]
    balances = {(b["accountIndex"], b["mint"]): b for b in meta.get("postTokenBalances", [])}
    before = {(b["accountIndex"], b["mint"]): b for b in meta.get("preTokenBalances", [])}
    instructions = list(message.get("instructions", []))
    for inner in meta.get("innerInstructions", []):
        instructions.extend(inner.get("instructions", []))
    memos = [i["parsed"].strip().lower() for i in instructions if i.get("program") == "spl-memo" and isinstance(i.get("parsed"), str)]
    matches = []
    for instruction in instructions:
        parsed = instruction.get("parsed") or {}
        if not isinstance(parsed, dict) or instruction.get("program") != "spl-token" or parsed.get("type") not in ("transfer", "transferChecked"):
            continue
        info = parsed.get("info") or {}
        if info.get("destination") not in keys:
            continue
        index = keys.index(info["destination"])
        balance = balances.get((index, leg["asset"]["identifier"]))
        raw_amount = info.get("amount") or info.get("tokenAmount", {}).get("amount")
        if not balance or balance.get("owner") != leg["accountAddress"] or raw_amount != leg["rawAmount"]:
            continue
        previous = before.get((index, balance["mint"]), {}).get("uiTokenAmount", {}).get("amount", "0")
        delta = int(balance["uiTokenAmount"]["amount"]) - int(previous)
        matches.append({"source_token_account": info.get("source"), "token_account": info["destination"], "owner": balance["owner"], "mint": balance["mint"], "raw_amount": raw_amount, "delta_raw": str(delta), "decimals": balance["uiTokenAmount"]["decimals"], "balance_delta_matches": delta == int(raw_amount)})
    canonical = [e for e in observation.get("canonicalEvidence", []) if e.get("transaction") == leg["transaction"]]
    succeeded = "err" in meta and meta["err"] is None and signature in transaction.get("signatures", [])
    slot_matches = any(e.get("state") == "succeeded" and str(e.get("blockNumber")) == str(result.get("slot")) for e in canonical)
    canonical_transfer_matches = len(matches) == 1 and any(t.get("transaction") == leg["transaction"] and t.get("asset") == leg["asset"] and t.get("rawAmount") == leg["rawAmount"] and t.get("fromAddress") == matches[0]["source_token_account"] and t.get("toAddress") == matches[0]["token_account"] for e in canonical for t in (e.get("assetEvidence") or {}).get("transfers", []))
    deposit_memo = deposit_id is not None and deposit_id.lower() in memos
    operation_memo = observation["operationId"]["value"].lower() in memos
    destination_matches = succeeded and slot_matches and canonical_transfer_matches and len(matches) == 1 and matches[0]["balance_delta_matches"]
    status = "order_correlated" if destination_matches and deposit_memo and operation_memo else "destination_verified" if destination_matches else "conflict"
    return {"status": status, "succeeded": succeeded, "slot": result.get("slot"), "slot_matches": slot_matches, "canonical_transfer_matches": canonical_transfer_matches, "deposit_id_memo_matches": deposit_memo, "operation_id_memo_matches": operation_memo, "transfers": matches, "block_time_utc": _iso(result.get("blockTime")), "decimals": matches[0]["decimals"] if len(matches) == 1 else None}


def import_captures(directory, database, recipient, case_key=None):
    records = []
    for path in sorted(Path(directory).glob("*.json")):
        value = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(value, dict) and isinstance(value.get("request"), dict) and isinstance(value.get("response"), dict) and "completed_at" in value:
            records.append(value)
    store = Store(database)
    store.initialize()
    with store.connect() as connection:
        case, movements = _load_scope(connection, case_key, recipient)
        connection.executescript(SCHEMA)
        deposits = []
        for movement in movements:
            receipt, (deposit_id, locator) = _receipt(connection, movement)
            key = _digest([case["case_key"], movement["chain_id"], movement["tx_hash"], movement["log_index"]])
            connection.execute("INSERT OR IGNORE INTO bridge_deposits VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (key, case["case_key"], movement["chain_id"], movement["tx_hash"], movement["log_index"], movement["block_time_utc"], movement["from_address"], movement["to_address"], movement["token_address"], movement["amount_raw"], movement["token_decimals"], deposit_id, locator, movement["raw_payload_id"]))
            deposits.append((key, movement, receipt, deposit_id))
        rpc_records = {}
        for record in records:
            body = record["request"]
            if body.get("method") != "getTransaction" or not body.get("params"):
                continue
            key = _digest(record)
            row = connection.execute("SELECT raw_payload_id FROM bridge_rpc_requests WHERE request_key=?", (key,)).fetchone()
            result = record["response"].get("result")
            state = "succeeded" if isinstance(result, dict) and "err" in (result.get("meta") or {}) and result["meta"]["err"] is None else "reverted" if isinstance(result, dict) else "not_found" if record["http_status"] == 200 and "error" not in record["response"] else "unavailable"
            if row:
                raw_id = row[0]
            else:
                raw_id = store.save_raw(connection, record.get("provider", "configured_solana_rpc"), "getTransaction", record, record["completed_at"], record["http_status"])
                connection.execute("INSERT INTO bridge_rpc_requests VALUES (?,?,?,?,?,?,?,?)", (key, SOLANA_MAINNET, body["params"][0], record.get("provider", "configured_solana_rpc"), record["completed_at"], record["http_status"], state, raw_id))
            rpc_records.setdefault(body["params"][0], []).append((record, raw_id))
        for record in records:
            body, payload = record["request"], record["response"]
            source_hash = body.get("sourceTransactionHash") or body.get("transactionHash")
            source_chain = body.get("sourceChain") or body.get("transactionChain")
            scoped = [d for d in deposits if source_chain == "eip155:1" and d[1]["tx_hash"] == source_hash]
            if not scoped:
                continue
            key = _digest(record)
            existing = connection.execute("SELECT raw_payload_id FROM bridge_resolve_requests WHERE request_key=?", (key,)).fetchone()
            raw_id = existing[0] if existing else store.save_raw(connection, "bridge_api_aggregator", record["url"], record, record["completed_at"], record["http_status"])
            evaluation = {"matched_operations": [], "excluded_operations": [], "provider_issues": payload.get("providerIssues", []), "verification_issues": payload.get("verificationIssues", []), "attempt_issues": payload.get("attemptIssues", []), "source_hydration_issues": payload.get("sourceHydrationIssues", [])}
            routes = []
            for observation in payload.get("observations", []) if record["http_status"] == 200 else []:
                matched = [d for d in scoped if _input_matches(observation, payload, d[1], d[2])]
                if not matched:
                    evaluation["excluded_operations"].append({"operation_id": observation.get("operationId"), "reason": "input does not match the seed receipt transfer"})
                    continue
                evaluation["matched_operations"].append(observation["operationId"])
                assertion = observation["providerAssertion"]
                for deposit_key, movement, receipt, deposit_id in matched:
                    for index, leg in enumerate(assertion.get("assetLegs", [])):
                        if leg.get("role") != "output" or leg.get("basis") != "actual" or not leg.get("transaction") or leg["transaction"] not in assertion.get("destinations", []) or leg["transaction"].get("chain") != leg["asset"].get("chain"):
                            continue
                        proof, rpc_raw_id = {"status": "provider_only"}, None
                        if leg["asset"]["chain"] == SOLANA_MAINNET and leg["asset"]["kind"] == "spl":
                            checked = [(p, raw) for r, raw in rpc_records.get(leg["transaction"]["transactionHash"], []) if (p := _verify_solana(r, leg, observation, deposit_id)) is not None]
                            if checked:
                                proof, rpc_raw_id = checked[0]
                                if any(p != proof for p, _ in checked[1:]):
                                    proof = {"status": "conflict", "reason": "independent RPC responses disagree", "checks": [p for p, _ in checked]}
                        chain_name = "solana" if leg["asset"]["chain"] == SOLANA_MAINNET else "ethereum" if leg["asset"]["chain"] == "eip155:1" else None
                        resolution = connection.execute("SELECT status FROM wallet_resolutions WHERE fomo_user_id=? AND chain=? AND address=?", (case["fomo_user_id"], chain_name, leg["accountAddress"])).fetchone() if chain_name else None
                        evidence = {"source_transfer_locator": "log:" + str(movement["log_index"]), "deposit_id": deposit_id, "provider_provenance": observation.get("provenance"), "provider_assertion": assertion, "canonical_evidence": observation.get("canonicalEvidence", []), "direct_rpc_check": proof}
                        values = (_digest([key, deposit_key, observation["operationId"], index]), deposit_key, key, observation["operationId"]["provider"], observation["operationId"]["value"], assertion["status"], assertion["rawStatus"], assertion.get("observedAt"), index, leg["asset"]["chain"], leg["transaction"]["transactionHash"], leg["accountAddress"], leg["asset"]["identifier"], leg["asset"]["kind"], leg["rawAmount"], proof.get("decimals"), proof.get("block_time_utc"), resolution[0] if resolution else "unknown", proof["status"], rpc_raw_id, _json(evidence))
                        routes.append(values)
            connection.execute("INSERT INTO bridge_resolve_requests VALUES (?,?,?,?,?,?,?,?,?) ON CONFLICT(request_key) DO UPDATE SET evaluation_json=excluded.evaluation_json", (key, case["case_key"], record["url"], source_chain, source_hash, record["completed_at"], record["http_status"], raw_id, _json(evaluation)))
            for values in routes:
                connection.execute("INSERT INTO bridge_routes VALUES (" + ",".join("?" for _ in values) + ") ON CONFLICT(route_key) DO UPDATE SET destination_decimals=excluded.destination_decimals,destination_at_utc=excluded.destination_at_utc,wallet_resolution_status=excluded.wallet_resolution_status,evidence_status=excluded.evidence_status,destination_raw_payload_id=excluded.destination_raw_payload_id,evidence_json=excluded.evidence_json", values)
    return build_report(database, case["case_key"], recipient)


def build_report(database, case_key, recipient):
    with Store(database).connect() as connection:
        case, _ = _load_scope(connection, case_key, recipient)
        deposits = [dict(r) for r in connection.execute("SELECT * FROM bridge_deposits WHERE case_key=? AND to_address=? ORDER BY source_at_utc,source_log_index", (case_key, recipient.lower()))]
        route_rows = connection.execute("SELECT r.* FROM bridge_routes r JOIN bridge_deposits d ON d.deposit_key=r.deposit_key JOIN bridge_resolve_requests q ON q.request_key=r.request_key WHERE d.case_key=? AND d.to_address=? ORDER BY q.fetched_at_utc DESC", (case_key, recipient.lower())).fetchall()
        routes = {}
        for row in route_rows:
            row = dict(row)
            row["evidence"] = json.loads(row.pop("evidence_json"))
            logical = (row["deposit_key"], row["provider"], row["operation_id"], row["destination_chain"], row["destination_tx_hash"], row["destination_asset"], row["destination_wallet"])
            routes.setdefault(logical, row)
        requests = [dict(row) for row in connection.execute("SELECT request_key,endpoint,source_tx_hash,http_status,raw_payload_id,evaluation_json FROM bridge_resolve_requests WHERE case_key=? ORDER BY fetched_at_utc", (case_key,))]
        for row in requests:
            row["evaluation"] = json.loads(row.pop("evaluation_json"))
        capture_gaps = [{"raw_payload_id": row["id"], "details": json.loads(row["payload_json"])} for row in connection.execute("SELECT id,payload_json FROM raw_payloads WHERE source='bridge_capture_gap' AND route=? ORDER BY id", (case_key,))]
        resolved = {r["deposit_key"] for r in routes.values() if r["evidence_status"] == "order_correlated" and r["provider_status"] == "completed"}
        totals = {}
        for deposit in deposits:
            group = (deposit["token_address"], deposit["token_decimals"])
            item = totals.setdefault(group, {"token_address": group[0], "decimals": group[1], "source_amount_raw": 0, "order_correlated_amount_raw": 0})
            item["source_amount_raw"] += int(deposit["amount_raw"])
            if deposit["deposit_key"] in resolved:
                item["order_correlated_amount_raw"] += int(deposit["amount_raw"])
        for total in totals.values():
            for key in ("source_amount_raw", "order_correlated_amount_raw"):
                total[key.replace("_raw", "_units")] = _units(total[key], total["decimals"])
                total[key] = str(total[key])
        return {"case_key": case_key, "fomo_user_id": case["fomo_user_id"], "rank": case["rank"], "ethereum_wallet": case["seed_address"], "recipient_contract": recipient.lower(), "generated_at_utc": utc_now(), "summary": {"source_deposits": len(deposits), "order_correlated_deposits": len(resolved), "unresolved_deposits": len(deposits) - len(resolved), "bridge_api_requests": len(requests), "totals": list(totals.values())}, "deposits": deposits, "routes": sorted(routes.values(), key=lambda r: r.get("destination_at_utc") or ""), "unresolved": [d for d in deposits if d["deposit_key"] not in resolved], "requests": requests, "capture_gaps": capture_gaps, "limitations": ["Bounded to the selected verified Ethereum seed and recipient.", "Source and destination asset amounts are transfers, not swaps or PnL.", "Provider assertions, canonical API evidence, and independent RPC evidence are kept separately.", "Other users' operations in shared transactions are excluded.", "Existing verified destination wallets are recognized without assigning any other address to the trader.", "A missing provider order or RPC result is incomplete coverage, not proof that no bridge occurred."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recipient", required=True)
    parser.add_argument("--case-key")
    parser.add_argument("--database", default=str(DEFAULT_DATABASE))
    parser.add_argument("--api-url", default="http://127.0.0.1:8080")
    parser.add_argument("--captures", help="Import existing API/RPC captures without new requests")
    parser.add_argument("--max-transactions", type=int, default=20)
    parser.add_argument("--report", default=str(REPO_ROOT / "data/research/rank9-bridge-evidence.json"))
    args = parser.parse_args()
    directory = Path(args.captures) if args.captures else REPO_ROOT / "data/raw/bridge" / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    case_key = args.case_key
    if not args.captures:
        case_key = collect(args.database, args.recipient, case_key, args.api_url, directory, args.max_transactions)
    report = import_captures(directory, args.database, args.recipient, case_key)
    path = Path(args.report)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    os.chmod(path, 0o600)
    print(json.dumps({"report": str(path), **report["summary"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
