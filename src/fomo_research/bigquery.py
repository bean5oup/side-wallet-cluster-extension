"""Collect the authorized Ethereum ERC-20 pilot through the authenticated bq CLI."""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from .config import DEFAULT_DATABASE, REPO_ROOT
from .store import Store, _json, utc_now


QUERY_VERSION = "ethereum_erc20_v1"
DATASET = "bigquery-public-data.goog_blockchain_ethereum_mainnet_us"
LOCATION = "US"
USDC = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
SQL = f"""SELECT block_hash, block_number, block_timestamp, transaction_hash,
       transaction_index, event_index, batch_index, address AS token_address,
       event_type, from_address, to_address, quantity AS quantity_raw, removed
FROM `{DATASET}.token_transfers`
WHERE block_timestamp >= @start_utc AND block_timestamp < @end_utc
  AND (from_address = @wallet OR to_address = @wallet)
  AND event_type = 'ERC-20' AND COALESCE(removed, FALSE) = FALSE
ORDER BY block_timestamp, block_number, transaction_index, event_index,
         batch_index, transaction_hash
"""

SCHEMA = """
CREATE TABLE IF NOT EXISTS bigquery_collections (
    collection_key TEXT PRIMARY KEY,
    case_key TEXT NOT NULL REFERENCES evm_flow_cases(case_key),
    fomo_user_id TEXT NOT NULL REFERENCES traders(fomo_user_id),
    chain_id INTEGER NOT NULL,
    wallet TEXT NOT NULL,
    query_version TEXT NOT NULL,
    sql_text TEXT NOT NULL,
    sql_sha256 TEXT NOT NULL,
    parameters_json TEXT NOT NULL,
    project_id TEXT NOT NULL,
    dataset_id TEXT NOT NULL,
    location TEXT NOT NULL,
    job_id TEXT NOT NULL,
    window_start_utc TEXT NOT NULL,
    window_end_utc TEXT NOT NULL,
    maximum_bytes_billed TEXT NOT NULL,
    estimated_bytes_processed TEXT NOT NULL,
    bytes_processed TEXT NOT NULL,
    bytes_billed TEXT NOT NULL,
    cache_hit INTEGER NOT NULL,
    total_rows INTEGER NOT NULL,
    fetched_rows INTEGER NOT NULL,
    retrieval_status TEXT NOT NULL,
    history_coverage_json TEXT NOT NULL,
    report_json TEXT NOT NULL,
    raw_metadata_id INTEGER NOT NULL REFERENCES raw_payloads(id),
    imported_at_utc TEXT NOT NULL,
    UNIQUE(project_id, location, job_id)
);
CREATE TABLE IF NOT EXISTS bigquery_result_pages (
    collection_key TEXT NOT NULL REFERENCES bigquery_collections(collection_key),
    page_index INTEGER NOT NULL,
    start_row INTEGER NOT NULL,
    row_count INTEGER NOT NULL,
    captured_at_utc TEXT NOT NULL,
    raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
    PRIMARY KEY(collection_key, page_index),
    UNIQUE(collection_key, start_row)
);
CREATE TABLE IF NOT EXISTS bigquery_erc20_transfers (
    collection_key TEXT NOT NULL REFERENCES bigquery_collections(collection_key),
    chain_id INTEGER NOT NULL,
    tx_hash TEXT NOT NULL,
    event_index INTEGER NOT NULL,
    batch_index INTEGER NOT NULL,
    block_hash TEXT NOT NULL,
    block_number INTEGER NOT NULL,
    transaction_index INTEGER NOT NULL,
    block_time_utc TEXT NOT NULL,
    token_address TEXT NOT NULL,
    from_address TEXT NOT NULL,
    to_address TEXT NOT NULL,
    quantity_raw TEXT NOT NULL,
    action_type TEXT NOT NULL CHECK(action_type='TRANSFER'),
    raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
    receipt_log_index INTEGER,
    receipt_raw_payload_id INTEGER REFERENCES raw_payloads(id),
    receipt_comparison_status TEXT NOT NULL,
    PRIMARY KEY(collection_key, tx_hash, event_index, batch_index)
);
CREATE INDEX IF NOT EXISTS idx_bigquery_erc20_wallet_time
    ON bigquery_erc20_transfers(chain_id, from_address, to_address, block_time_utc);
"""


def _digest(value):
    return hashlib.sha256(_json(value).encode()).hexdigest()


def _stamp(value):
    stamp = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    return stamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(_json(payload) + "\n", encoding="utf-8")
    os.chmod(temporary, 0o600)
    temporary.replace(path)


def _scope(connection, case_key):
    row = connection.execute(
        "SELECT * FROM evm_flow_cases WHERE case_key=?", (case_key,)
    ).fetchone() if case_key else connection.execute(
        "SELECT * FROM evm_flow_cases WHERE rank=9 AND chain_id=1 ORDER BY imported_at_utc DESC LIMIT 1"
    ).fetchone()
    if row is None or row["rank"] != 9 or row["chain_id"] != 1:
        raise ValueError("An existing rank-9 Ethereum Flow case is required")
    scope = {key: row[key] for key in ("case_key", "fomo_user_id", "rank", "seed_address",
                                      "leaderboard_snapshot_at_utc", "window_start_utc", "window_end_utc")}
    wallet = scope["seed_address"].lower()
    if not re.fullmatch(r"0x[0-9a-f]{40}", wallet):
        raise ValueError("Invalid verified Ethereum address")
    if not connection.execute(
        "SELECT 1 FROM wallet_resolutions WHERE fomo_user_id=? AND chain='ethereum' AND lower(address)=? AND status='verified'",
        (scope["fomo_user_id"], wallet),
    ).fetchone() or not connection.execute(
        "SELECT 1 FROM top10_wallet_inventory WHERE fomo_user_id=? AND rank=9 AND snapshot_at_utc=? AND lower(evm_wallet_candidate)=?",
        (scope["fomo_user_id"], scope["leaderboard_snapshot_at_utc"], wallet),
    ).fetchone():
        raise ValueError("Case seed must belong to the verified fixed Top 10 cohort")
    start, end = _stamp(scope["window_start_utc"]), _stamp(scope["window_end_utc"])
    seconds = (datetime.fromisoformat(end.replace("Z", "+00:00")) -
               datetime.fromisoformat(start.replace("Z", "+00:00"))).total_seconds()
    if seconds <= 0 or seconds > 31 * 86400:
        raise ValueError("The pilot requires a bounded window of at most 31 days")
    scope.update(seed_address=wallet, window_start_utc=start, window_end_utc=end)
    return scope


def _call(directory, manifest, arguments, sql=None):
    executable = shutil.which("bq")
    if executable is None:
        raise RuntimeError("The authenticated bq CLI must be available on PATH")
    command = [executable, "--quiet", "--format=json", "--project_id=" + manifest["project_id"],
               "--location=" + manifest["location"], *arguments]
    captured_at = utc_now()
    try:
        result = subprocess.run(command, input=sql, text=True, capture_output=True, timeout=90)
        stdout, stderr, code = result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout or ""
        stderr = error.stderr or ""
        stdout = stdout.decode() if isinstance(stdout, bytes) else stdout
        stderr = stderr.decode() if isinstance(stderr, bytes) else stderr
        code = -1
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        payload = None
    record = {"captured_at_utc": captured_at, "completed_at_utc": utc_now(),
              "arguments": command[1:], "stdin_sha256": hashlib.sha256(sql.encode()).hexdigest() if sql else None,
              "exit_code": code, "stdout": stdout, "stderr": stderr, "payload": payload}
    reference = "captures/" + _digest(record) + ".json"
    _write(directory / reference, record)
    manifest["requests"].append(reference)
    _write(directory / "manifest.json", manifest)
    if code != 0 or payload is None:
        raise RuntimeError(f"bq capture failed ({code}); evidence: {directory / reference}")
    return reference, payload


def _identity(row):
    return (row["tx_hash"], row["token_address"], row["from_address"],
            row["to_address"], row["quantity_raw"])


def _rows(directory, manifest):
    rows, offset, seen = [], 0, set()
    start = datetime.fromisoformat(manifest["scope"]["window_start_utc"].replace("Z", "+00:00"))
    end = datetime.fromisoformat(manifest["scope"]["window_end_utc"].replace("Z", "+00:00"))
    for page in manifest["pages"]:
        record = json.loads((directory / page["capture"]).read_text())
        values = record["payload"]
        if page["start_row"] != offset or not isinstance(values, list) or len(values) != page["row_count"]:
            raise ValueError("Non-contiguous or inconsistent result pages")
        for value in values:
            # bq JSON prints BOOLEAN cells as strings; retain that raw CLI value.
            if value["event_type"] != "ERC-20" or value.get("removed") not in (None, False, "false"):
                raise ValueError("Unexpected event type or removed log")
            quantity = value["quantity_raw"]
            if not isinstance(quantity, str) or not quantity.isascii() or not quantity.isdigit() or int(quantity) >= 2 ** 256:
                raise ValueError("Quantity must be an exact uint256 string")
            row = {"chain_id": 1, "tx_hash": value["transaction_hash"].lower(),
                   "event_index": int(value["event_index"]),
                   "batch_index": int(value["batch_index"]) if value["batch_index"] is not None else -1,
                   "block_hash": value["block_hash"].lower(), "block_number": int(value["block_number"]),
                   "transaction_index": int(value["transaction_index"]),
                   "block_time_utc": _stamp(value["block_timestamp"]),
                   "token_address": value["token_address"].lower(),
                   "from_address": value["from_address"].lower(), "to_address": value["to_address"].lower(),
                   "quantity_raw": str(int(quantity)), "action_type": "TRANSFER", "capture": page["capture"],
                   "receipt_log_index": None, "receipt_raw_payload_id": None,
                   "receipt_comparison_status": "not_in_retained_baseline"}
            for field in ("token_address", "from_address", "to_address"):
                if not re.fullmatch(r"0x[0-9a-f]{40}", row[field]):
                    raise ValueError("Invalid result address")
            if not re.fullmatch(r"0x[0-9a-f]{64}", row["tx_hash"]) or not re.fullmatch(r"0x[0-9a-f]{64}", row["block_hash"]):
                raise ValueError("Invalid transaction or block hash")
            stamp = datetime.fromisoformat(row["block_time_utc"].replace("Z", "+00:00"))
            if not start <= stamp < end or manifest["scope"]["seed_address"] not in (row["from_address"], row["to_address"]):
                raise ValueError("Result falls outside the authorized wallet/window")
            key = (row["tx_hash"], row["event_index"], row["batch_index"])
            if key in seen:
                raise ValueError("Duplicate transfer identity across result pages")
            seen.add(key)
            rows.append(row)
        offset += len(values)
    if offset != manifest["total_rows"]:
        raise ValueError("Fetched row count does not equal the query result total")
    return rows


def _reconcile(connection, scope, rows):
    baseline = connection.execute(
        "SELECT * FROM evm_flow_movements WHERE case_key=? AND relation='seed' ORDER BY block_number,transaction_index,log_index",
        (scope["case_key"],),
    ).fetchall()
    candidates = defaultdict(list)
    for row in rows:
        candidates[_identity(row)].append(row)
    comparisons, matched = [], {}
    for source in baseline:
        receipt = json.loads(connection.execute("SELECT payload_json FROM raw_payloads WHERE id=?", (source["raw_payload_id"],)).fetchone()[0])["result"]
        if receipt.get("status") != "0x1":
            raise ValueError("Retained baseline receipt is not successful")
        reference = dict(source)
        reference["quantity_raw"] = str(int(reference["amount_raw"]))
        reference["block_hash"] = receipt["blockHash"].lower()
        reference["block_time_utc"] = _stamp(reference["block_time_utc"])
        logs = [log for log in receipt["logs"] if int(log["logIndex"], 16) == reference["log_index"]]
        if len(logs) != 1 or receipt["transactionHash"].lower() != reference["tx_hash"]:
            raise ValueError("Retained receipt does not contain its referenced log")
        log = logs[0]
        topics = log["topics"]
        if len(topics) != 3 or topics[0] != "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef" or \
                log["address"].lower() != reference["token_address"] or \
                "0x" + topics[1][-40:].lower() != reference["from_address"] or \
                "0x" + topics[2][-40:].lower() != reference["to_address"] or \
                str(int(log["data"], 16)) != reference["quantity_raw"] or \
                int(receipt["blockNumber"], 16) != reference["block_number"] or \
                int(receipt["transactionIndex"], 16) != reference["transaction_index"]:
            raise ValueError("Retained movement disagrees with its raw receipt log")
        options = candidates[_identity(reference)]
        exact = [r for r in options if all(r[k] == reference[k] for k in ("block_hash", "block_number", "transaction_index", "block_time_utc"))]
        same_index = [r for r in exact if r["event_index"] == reference["log_index"]]
        chosen = same_index[0] if len(same_index) == 1 else exact[0] if len(exact) == 1 else None
        detail = {"tx_hash": reference["tx_hash"], "receipt_log_index": reference["log_index"],
                  "receipt_raw_payload_id": reference["raw_payload_id"], "token_address": reference["token_address"],
                  "quantity_raw": reference["quantity_raw"]}
        if chosen is not None and chosen["receipt_log_index"] is None:
            chosen.update(receipt_log_index=reference["log_index"], receipt_raw_payload_id=reference["raw_payload_id"],
                          receipt_comparison_status="exact" if same_index else "content_matches_index_differs")
            detail.update(status=chosen["receipt_comparison_status"], bigquery_event_index=chosen["event_index"],
                          batch_index=chosen["batch_index"], capture=chosen["capture"])
            matched[(reference["tx_hash"], reference["log_index"])] = chosen
        else:
            detail.update(status="ambiguous" if len(exact) > 1 else "different_block_fields" if options else "missing",
                          candidates=[{k: r[k] for k in ("event_index", "block_hash", "block_number", "transaction_index", "block_time_utc")} for r in options])
        comparisons.append(detail)
    deposits = connection.execute("SELECT * FROM bridge_deposits WHERE case_key=? ORDER BY source_at_utc,source_log_index", (scope["case_key"],)).fetchall()
    bridge_checks = []
    for deposit in deposits:
        row = matched.get((deposit["source_tx_hash"], deposit["source_log_index"]))
        agrees = row is not None and all(row[k] == deposit[k] for k in ("from_address", "to_address", "token_address")) and row["quantity_raw"] == str(int(deposit["amount_raw"]))
        bridge_checks.append({"deposit_key": deposit["deposit_key"], "source_tx_hash": deposit["source_tx_hash"],
                              "receipt_log_index": deposit["source_log_index"], "deposit_id": deposit["deposit_id"],
                              "quantity_raw": deposit["amount_raw"], "status": "matched" if agrees else "not_matched"})
    totals = {}
    for row in rows:
        token = totals.setdefault(row["token_address"], {"token_address": row["token_address"],
                                  "canonical_ethereum_usdc": row["token_address"] == USDC,
                                  "inbound_count": 0, "outbound_count": 0, "inbound_raw": 0, "outbound_raw": 0})
        for side, field in (("inbound", "to_address"), ("outbound", "from_address")):
            if row[field] == scope["seed_address"]:
                token[side + "_count"] += 1
                token[side + "_raw"] += int(row["quantity_raw"])
    for token in totals.values():
        token["inbound_raw"], token["outbound_raw"] = str(token["inbound_raw"]), str(token["outbound_raw"])
    return {"baseline_receipt_logs": len(baseline), "matched_receipt_logs": len(matched),
            "equal_event_and_log_indexes": sum(c["status"] == "exact" for c in comparisons),
            "receipt_comparisons": comparisons, "baseline_bridge_deposits": len(deposits),
            "matched_bridge_deposits": sum(c["status"] == "matched" for c in bridge_checks),
            "bridge_comparisons": bridge_checks, "tokens": list(totals.values()),
            "additional_transfers": [{k: r[k] for k in ("tx_hash", "event_index", "block_time_utc", "token_address", "from_address", "to_address", "quantity_raw")}
                                     for r in rows if r["receipt_log_index"] is None]}


def import_capture(directory, database=DEFAULT_DATABASE):
    directory = Path(directory)
    manifest = json.loads((directory / "manifest.json").read_text())
    if manifest.get("retrieval_status") != "complete":
        raise ValueError("Only a completely retrieved job can be normalized")
    identity = {k: manifest[k] for k in ("scope", "sql", "sql_sha256", "query_version", "parameters", "project_id", "dataset_id", "location")}
    if _digest(identity) != manifest["collection_key"] or manifest["sql"] != SQL or manifest["sql_sha256"] != hashlib.sha256(SQL.encode()).hexdigest():
        raise ValueError("Query manifest does not match the implemented query")
    rows = _rows(directory, manifest)
    store = Store(database)
    store.initialize()
    with store.connect() as connection:
        connection.executescript(SCHEMA)
        existing = connection.execute("SELECT report_json FROM bigquery_collections WHERE collection_key=?", (manifest["collection_key"],)).fetchone()
        if existing:
            report = json.loads(existing[0])
            _write(directory / "report.json", report)
            return report
        scope = _scope(connection, manifest["scope"]["case_key"])
        if scope != manifest["scope"]:
            raise ValueError("Imported scope differs from the verified source case")
        report = _reconcile(connection, scope, rows)
        job_record = json.loads((directory / manifest["job_capture"]).read_text())
        job = job_record["payload"]
        if job.get("status", {}).get("state") != "DONE" or job["status"].get("errorResult"):
            raise ValueError("The query job did not finish successfully")
        if job["jobReference"] != {"projectId": manifest["project_id"], "jobId": manifest["job_id"], "location": LOCATION}:
            raise ValueError("Unexpected job reference")
        statistics = job["statistics"].get("query", {})
        coverage = {"history_status": "unknown", "scope": "ERC-20 transfer rows only; not all wallet actions",
                    "known_receipt_logs_matched": report["matched_receipt_logs"],
                    "known_receipt_logs_expected": report["baseline_receipt_logs"],
                    "native_transfers_nfts_failed_transactions_swaps_quotes": "not collected by this query"}
        report.update(collection_key=manifest["collection_key"], query_version=QUERY_VERSION, scope=scope,
                      project_id=manifest["project_id"], dataset_id=DATASET, location=LOCATION, job_id=manifest["job_id"],
                      sql_sha256=manifest["sql_sha256"], maximum_bytes_billed=manifest["maximum_bytes_billed"],
                      estimated_bytes_processed=manifest["estimated_bytes_processed"],
                      bytes_processed=statistics.get("totalBytesProcessed", "0"), bytes_billed=statistics.get("totalBytesBilled", "0"),
                      cache_hit=bool(statistics.get("cacheHit", False)), total_rows=manifest["total_rows"],
                      fetched_rows=len(rows), page_count=len(manifest["pages"]), retrieval_status="complete", history_coverage=coverage,
                      capture_directory=str(directory.resolve()), imported_at_utc=utc_now())
        raw_ids = {}
        for reference in dict.fromkeys(manifest["requests"]):
            record = json.loads((directory / reference).read_text())
            if _digest(record) != Path(reference).stem:
                raise ValueError("Capture content hash mismatch")
            raw_ids[reference] = store.save_raw(connection, "bigquery_bq_cli", manifest["project_id"] + "/" + LOCATION + "/" + manifest["job_id"],
                                               record, record["completed_at_utc"], status=None)
        collection = {"collection_key": manifest["collection_key"], "case_key": scope["case_key"], "fomo_user_id": scope["fomo_user_id"],
                      "chain_id": 1, "wallet": scope["seed_address"], "query_version": QUERY_VERSION, "sql_text": SQL,
                      "sql_sha256": manifest["sql_sha256"], "parameters_json": _json(manifest["parameters"]),
                      "project_id": manifest["project_id"], "dataset_id": DATASET, "location": LOCATION, "job_id": manifest["job_id"],
                      "window_start_utc": scope["window_start_utc"], "window_end_utc": scope["window_end_utc"],
                      **{k: str(report[k]) for k in ("maximum_bytes_billed", "estimated_bytes_processed", "bytes_processed", "bytes_billed")},
                      "cache_hit": int(report["cache_hit"]), "total_rows": report["total_rows"], "fetched_rows": len(rows),
                      "retrieval_status": "complete", "history_coverage_json": _json(coverage), "report_json": _json(report),
                      "raw_metadata_id": raw_ids[manifest["job_capture"]], "imported_at_utc": report["imported_at_utc"]}
        columns = list(collection)
        connection.execute("INSERT INTO bigquery_collections (" + ",".join(columns) + ") VALUES (" + ",".join("?" for _ in columns) + ")", tuple(collection[k] for k in columns))
        for index, page in enumerate(manifest["pages"]):
            record = json.loads((directory / page["capture"]).read_text())
            connection.execute("INSERT INTO bigquery_result_pages VALUES (?,?,?,?,?,?)", (manifest["collection_key"], index,
                               page["start_row"], page["row_count"], record["completed_at_utc"], raw_ids[page["capture"]]))
        for row in rows:
            row = {k: v for k, v in row.items() if k != "capture"} | {"collection_key": manifest["collection_key"], "raw_payload_id": raw_ids[row["capture"]]}
            columns = list(row)
            connection.execute("INSERT INTO bigquery_erc20_transfers (" + ",".join(columns) + ") VALUES (" + ",".join("?" for _ in columns) + ")", tuple(row[k] for k in columns))
    _write(directory / "report.json", report)
    return report


def collect(database, project, directory, maximum_bytes_billed, page_size, case_key=None):
    if not re.fullmatch(r"[a-z][a-z0-9-]{4,61}[a-z0-9]", project) or maximum_bytes_billed <= 0 or not 1 <= page_size <= 10000:
        raise ValueError("Invalid project, billing cap, or page size")
    store = Store(database)
    with store.connect() as connection:
        scope = _scope(connection, case_key)
    parameters = {"wallet": {"type": "STRING", "value": scope["seed_address"]},
                  "start_utc": {"type": "TIMESTAMP", "value": scope["window_start_utc"]},
                  "end_utc": {"type": "TIMESTAMP", "value": scope["window_end_utc"]}}
    identity = {"scope": scope, "sql": SQL, "sql_sha256": hashlib.sha256(SQL.encode()).hexdigest(),
                "query_version": QUERY_VERSION, "parameters": parameters, "project_id": project,
                "dataset_id": DATASET, "location": LOCATION}
    key = _digest(identity)
    directory = Path(directory) / key
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    path = directory / "manifest.json"
    if path.exists():
        manifest = json.loads(path.read_text())
        if manifest["collection_key"] != key:
            raise ValueError("Unexpected existing manifest")
    else:
        manifest = identity | {"collection_key": key, "job_id": "fomo_eth_" + key,
                               "maximum_bytes_billed": str(maximum_bytes_billed), "created_at_utc": utc_now(),
                               "requests": [], "pages": [], "retrieval_status": "pending"}
        _write(path, manifest)
    if manifest["retrieval_status"] == "complete":
        return import_capture(directory, database)
    if "total_rows" in manifest and sum(p["row_count"] for p in manifest["pages"]) == manifest["total_rows"]:
        _rows(directory, manifest)
        manifest.update(retrieval_status="complete", completed_at_utc=utc_now())
        _write(path, manifest)
        return import_capture(directory, database)
    parameter_flags = ["--parameter=" + name + ":" + p["type"] + ":" + p["value"] for name, p in parameters.items()]
    if "dry_run_capture" not in manifest:
        reference, dry = _call(directory, manifest, ["query", "--use_legacy_sql=false", "--dry_run=true", *parameter_flags], SQL)
        estimate = int(dry["statistics"].get("query", {}).get("totalBytesProcessed", dry["statistics"].get("totalBytesProcessed", "0")))
        manifest.update(dry_run_capture=reference, estimated_bytes_processed=str(estimate))
        _write(path, manifest)
    if int(manifest["estimated_bytes_processed"]) > min(maximum_bytes_billed, int(manifest["maximum_bytes_billed"])):
        raise ValueError("Dry-run estimate exceeds the requested billing cap; no query submitted")
    print(_json({"phase": "dry_run", "estimated_bytes_processed": manifest["estimated_bytes_processed"],
                 "maximum_bytes_billed": manifest["maximum_bytes_billed"], "job_id": manifest["job_id"]}), flush=True)
    if "submission_capture" not in manifest:
        reference, _ = _call(directory, manifest, ["--synchronous_mode=false", "--job_id=" + manifest["job_id"],
                            "query", "--use_legacy_sql=false", "--maximum_bytes_billed=" + manifest["maximum_bytes_billed"],
                            "--max_rows=0", "--label=fomo_research:rank9_ethereum", *parameter_flags], SQL)
        manifest["submission_capture"] = reference
        _write(path, manifest)
    deadline = time.monotonic() + 600
    while True:
        reference, job = _call(directory, manifest, ["show", "--job=true", manifest["job_id"]])
        manifest["job_capture"] = reference
        _write(path, manifest)
        if job.get("status", {}).get("state") == "DONE":
            if job["status"].get("errorResult"):
                raise RuntimeError("Query job failed; retained capture: " + str(directory / reference))
            break
        if time.monotonic() >= deadline:
            raise RuntimeError("Job is still pending; rerun the same command to resume without a new query")
        time.sleep(2)
    destination = job["configuration"]["query"]["destinationTable"]
    table_name = destination["projectId"] + ":" + destination["datasetId"] + "." + destination["tableId"]
    reference, table = _call(directory, manifest, ["show", table_name])
    manifest.update(result_table_capture=reference, total_rows=int(table["numRows"]), retrieval_status="fetching")
    _write(path, manifest)
    offset = sum(p["row_count"] for p in manifest["pages"])
    while offset < manifest["total_rows"]:
        reference, values = _call(directory, manifest, ["head", "--job=true", "--start_row=" + str(offset),
                                 "--max_rows=" + str(min(page_size, manifest["total_rows"] - offset)), manifest["job_id"]])
        if not isinstance(values, list) or not values or offset + len(values) > manifest["total_rows"]:
            raise ValueError("Result pagination did not advance consistently")
        manifest["pages"].append({"capture": reference, "start_row": offset, "row_count": len(values)})
        offset += len(values)
        _write(path, manifest)
        print(_json({"phase": "result_page", "fetched_rows": offset, "total_rows": manifest["total_rows"]}), flush=True)
    _rows(directory, manifest)
    manifest.update(retrieval_status="complete", completed_at_utc=utc_now())
    _write(path, manifest)
    return import_capture(directory, database)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", default=str(DEFAULT_DATABASE))
    parser.add_argument("--project", default="exchange-labs")
    parser.add_argument("--case-key")
    parser.add_argument("--directory", default=str(REPO_ROOT / "data/raw/bigquery"))
    parser.add_argument("--maximum-bytes-billed", type=int, default=40 * 1024 ** 3)
    parser.add_argument("--page-size", type=int, default=1000)
    parser.add_argument("--import-capture", help="Import complete saved evidence without any cloud calls")
    args = parser.parse_args()
    try:
        report = import_capture(args.import_capture, args.database) if args.import_capture else collect(
            args.database, args.project, args.directory, args.maximum_bytes_billed, args.page_size, args.case_key)
        print(json.dumps({k: report[k] for k in ("collection_key", "job_id", "total_rows", "fetched_rows", "page_count",
                         "bytes_processed", "bytes_billed", "cache_hit", "baseline_receipt_logs", "matched_receipt_logs",
                         "equal_event_and_log_indexes", "baseline_bridge_deposits", "matched_bridge_deposits", "capture_directory")}, indent=2))
        return 0
    except (RuntimeError, ValueError, OSError, KeyError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
