"""Import an evidence-backed Etherscan Flow case into the local research DB."""

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

from .config import DEFAULT_DATABASE
from .store import Store, _json, utc_now


FLOW_SCHEMA = """
CREATE TABLE IF NOT EXISTS evm_flow_cases (
    case_key TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    fomo_user_id TEXT NOT NULL REFERENCES traders(fomo_user_id),
    leaderboard_snapshot_at_utc TEXT NOT NULL,
    rank INTEGER NOT NULL,
    chain_id INTEGER NOT NULL,
    seed_address TEXT NOT NULL,
    window_start_utc TEXT NOT NULL,
    window_end_utc TEXT NOT NULL,
    coverage_json TEXT NOT NULL,
    case_json TEXT NOT NULL,
    created_at_utc TEXT NOT NULL,
    imported_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS evm_flow_requests (
    case_key TEXT NOT NULL REFERENCES evm_flow_cases(case_key),
    query_key TEXT NOT NULL,
    raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
    transport TEXT NOT NULL,
    module TEXT NOT NULL,
    action TEXT NOT NULL,
    params_json TEXT NOT NULL,
    fetched_at_utc TEXT NOT NULL,
    exit_code INTEGER NOT NULL,
    attempt_count INTEGER NOT NULL,
    elapsed_ms INTEGER NOT NULL,
    PRIMARY KEY (case_key, query_key)
);
CREATE TABLE IF NOT EXISTS evm_flow_movements (
    case_key TEXT NOT NULL REFERENCES evm_flow_cases(case_key),
    chain_id INTEGER NOT NULL,
    tx_hash TEXT NOT NULL,
    log_index INTEGER NOT NULL,
    block_number INTEGER NOT NULL,
    transaction_index INTEGER NOT NULL,
    block_time_utc TEXT NOT NULL,
    from_address TEXT NOT NULL,
    to_address TEXT NOT NULL,
    token_address TEXT NOT NULL,
    token_symbol TEXT,
    amount_raw TEXT NOT NULL,
    token_decimals INTEGER NOT NULL,
    relation TEXT NOT NULL CHECK (relation IN ('seed', 'counterparty_sample')),
    action_type TEXT NOT NULL CHECK (action_type = 'TRANSFER'),
    receipt_status TEXT NOT NULL,
    raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
    PRIMARY KEY (case_key, chain_id, tx_hash, log_index)
);
CREATE INDEX IF NOT EXISTS idx_evm_flow_movements_wallet_time
    ON evm_flow_movements(chain_id, from_address, to_address, block_time_utc);
"""


def _result(row):
    payload = row["result"]
    return payload.get("result", payload) if isinstance(payload, dict) else payload


def _units(raw, decimals):
    digits = str(int(raw))
    if int(raw) == 0:
        return "0"
    if decimals == 0:
        return digits
    padded = digits.zfill(decimals + 1)
    fraction = padded[-decimals:].rstrip("0")
    return (padded[:-decimals].lstrip("0") or "0") + ("." + fraction if fraction else "")


def _query_key(row):
    query = {key: row[key] for key in ("transport", "chainid", "module", "action", "params")}
    return hashlib.sha256(_json(query).encode("utf-8")).hexdigest()


def import_case(case_path, fetchlog_path, database=DEFAULT_DATABASE, rank=9):
    case = json.loads(Path(case_path).read_text(encoding="utf-8"))
    requests = [json.loads(line) for line in Path(fetchlog_path).read_text(encoding="utf-8").splitlines() if line.strip()]
    meta = case["_meta"]
    if meta["chainid"] != 1 or len(meta["seed_addresses"]) != 1:
        raise ValueError("This pilot importer accepts one Ethereum seed address")
    seed = meta["seed_addresses"][0].lower()
    nodes = {node["id"]: node["address"].lower() for node in case["nodes"]}
    if any(not re.fullmatch(r"0x[0-9a-f]{40}", address) for address in nodes.values()):
        raise ValueError("Invalid case address")
    if any(row["chainid"] != 1 or row["transport"] != "cli" for row in requests):
        raise ValueError("Expected Ethereum CLI provenance")
    if any(any(key.lower() in {"apikey", "api-key", "authorization", "cookie"} for key in row["params"]) for row in requests):
        raise ValueError("Credentials cannot appear in query provenance")
    query_keys = [_query_key(row) for row in requests]
    if len(set(query_keys)) != len(query_keys):
        raise ValueError("Duplicate query ledger entries")
    tokens = {}
    timestamps = {}
    for row in requests:
        values = _result(row)
        if row["action"] != "tokentx" or not isinstance(values, list):
            continue
        for value in values:
            address = value["contractAddress"].lower()
            token = (value["tokenSymbol"], int(value["tokenDecimal"]))
            if address in tokens and tokens[address] != token:
                raise ValueError("Conflicting token metadata")
            tokens[address] = token
            timestamps[value["hash"].lower()] = int(value["timeStamp"])
    edges = {}
    for edge in case["edges"]:
        if edge["chainid"] != 1 or edge["type"] != "token_transfer":
            raise ValueError("This pilot imports ERC-20 transfers only")
        pair = (nodes[edge["source"]], nodes[edge["target"]], edge["token_address"].lower())
        if pair in edges:
            raise ValueError("Case edges must already be merged")
        edges[pair] = edge
    movements = []
    for row in requests:
        if row["action"] != "eth_getTransactionReceipt":
            continue
        receipt = _result(row)
        if not isinstance(receipt, dict) or receipt.get("status") != "0x1":
            continue
        txhash = receipt["transactionHash"].lower()
        if txhash != row["params"]["txhash"].lower():
            raise ValueError("Receipt hash does not match requested hash")
        for log in receipt.get("logs", []):
            topics = log.get("topics", [])
            if len(topics) != 3 or topics[0] != "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef":
                continue
            source, target = "0x" + topics[1][-40:].lower(), "0x" + topics[2][-40:].lower()
            token_address = log["address"].lower()
            pair = (source, target, token_address)
            edge = edges.get(pair)
            if edge is None or txhash not in edge.get("txhashes", [edge["txhash"]]):
                continue
            symbol, decimals = tokens[token_address]
            timestamp = int(log["blockTimestamp"], 16) if log.get("blockTimestamp") else timestamps[txhash]
            movements.append({
                "chain_id": 1, "tx_hash": txhash, "log_index": int(log["logIndex"], 16),
                "block_number": int(receipt["blockNumber"], 16),
                "transaction_index": int(receipt["transactionIndex"], 16),
                "block_time_utc": datetime.fromtimestamp(timestamp, timezone.utc).isoformat().replace("+00:00", "Z"),
                "from_address": source, "to_address": target, "token_address": token_address,
                "token_symbol": symbol, "amount_raw": str(int(log["data"], 16)),
                "token_decimals": decimals, "relation": "seed" if seed in pair[:2] else "counterparty_sample",
                "query_key": _query_key(row),
            })
    for pair, edge in edges.items():
        evidence = sorted([m for m in movements if (m["from_address"], m["to_address"], m["token_address"]) == pair],
                          key=lambda m: (m["block_number"], m["transaction_index"], m["log_index"]))
        if not evidence:
            raise ValueError("Case edge lacks receipt evidence")
        hashes = list(dict.fromkeys(m["tx_hash"] for m in evidence))
        total = sum(int(m["amount_raw"]) for m in evidence)
        if edge["amount"] != _units(str(total), evidence[0]["token_decimals"]) or edge.get("txhashes", [edge["txhash"]]) != hashes:
            raise ValueError("Case edge amount or hashes disagree with receipts")
        if edge["txhash"] != hashes[0] or edge["txcount"] != len(hashes):
            raise ValueError("Case edge chronology or transaction count disagrees with receipts")
    body = _json(case)
    case_key = hashlib.sha256(body.encode("utf-8")).hexdigest()
    store = Store(database)
    store.initialize()
    with store.connect() as connection:
        connection.executescript(FLOW_SCHEMA)
        existing = connection.execute("SELECT case_key FROM evm_flow_cases WHERE case_key=?", (case_key,)).fetchone()
        if existing:
            return {"case_key": case_key, "already_imported": True}
        trader = connection.execute(
            "SELECT * FROM top10_wallet_inventory WHERE rank=? AND lower(evm_wallet_candidate)=? ORDER BY snapshot_at_utc DESC LIMIT 1",
            (rank, seed),
        ).fetchone()
        if trader is None or not connection.execute(
            "SELECT 1 FROM wallet_resolutions WHERE fomo_user_id=? AND chain='ethereum' AND lower(address)=? AND status='verified'",
            (trader["fomo_user_id"], seed),
        ).fetchone():
            raise ValueError("Seed must match a verified Ethereum wallet in the fixed Top 10")
        connection.execute(
            "INSERT INTO evm_flow_cases VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (case_key, case["id"], trader["fomo_user_id"], trader["snapshot_at_utc"], rank, 1, seed,
             meta["trace_window"]["start_timestamp"], meta["trace_window"]["end_timestamp"],
             _json(meta["trace_window"]), body, meta["created_at"], utc_now()),
        )
        raw_ids = {}
        for row, query_key in zip(requests, query_keys):
            route = "https://api.etherscan.io/v2/api?" + urlencode({"chainid": 1, "module": row["module"], "action": row["action"], **row["params"]})
            raw_id = store.save_raw(connection, "etherscan_v2_cli", route, row, row["fetched_at"], status=None)
            raw_ids[query_key] = raw_id
            connection.execute(
                "INSERT INTO evm_flow_requests VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (case_key, query_key, raw_id, row["transport"], row["module"], row["action"],
                 _json(row["params"]), row["fetched_at"], row["exit_code"], row.get("attempt_count", 1), row["elapsed_ms"]),
            )
        for movement in movements:
            connection.execute(
                "INSERT INTO evm_flow_movements VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (case_key, movement["chain_id"], movement["tx_hash"], movement["log_index"], movement["block_number"],
                 movement["transaction_index"], movement["block_time_utc"], movement["from_address"], movement["to_address"],
                 movement["token_address"], movement["token_symbol"], movement["amount_raw"], movement["token_decimals"],
                 movement["relation"], "TRANSFER", "0x1", raw_ids[movement["query_key"]]),
            )
    return {"case_key": case_key, "requests": len(requests), "movements": len(movements),
            "seed_movements": sum(m["relation"] == "seed" for m in movements), "already_imported": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", required=True)
    parser.add_argument("--fetchlog", required=True)
    parser.add_argument("--database", default=str(DEFAULT_DATABASE))
    parser.add_argument("--rank", type=int, default=9)
    args = parser.parse_args()
    print(json.dumps(import_case(args.case, args.fetchlog, args.database, args.rank), ensure_ascii=False))


if __name__ == "__main__":
    main()
