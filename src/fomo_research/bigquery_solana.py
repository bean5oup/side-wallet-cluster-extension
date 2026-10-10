"""Collect bounded, historical Solana token-owner activity with the existing bq CLI."""

import argparse
import hashlib
import json
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from .bigquery import _call, _digest, _scope as ethereum_scope, _stamp, _write
from .config import DEFAULT_DATABASE, REPO_ROOT
from .store import Store, _json, utc_now

QUERY_VERSION = "solana_owner_v1"
DATASET = "bigquery-public-data.crypto_solana_mainnet_us"
LOCATION = "us-central1"
DISCOVERY_SQL = f"""SELECT signature, block_slot, block_timestamp, status, err
FROM `{DATASET}.Transactions`
WHERE block_timestamp >= @start_utc AND block_timestamp < @end_utc
  AND (EXISTS(SELECT 1 FROM UNNEST(pre_token_balances) WHERE owner = @wallet)
       OR EXISTS(SELECT 1 FROM UNNEST(post_token_balances) WHERE owner = @wallet))
ORDER BY block_timestamp, block_slot, signature
"""
DETAIL_SQL = f"""SELECT signature, block_slot, block_timestamp, status, err,
       CAST(fee AS STRING) AS fee_raw, accounts, log_messages,
       ARRAY(SELECT AS STRUCT account, CAST(before AS STRING) AS before_raw,
                    CAST(after AS STRING) AS after_raw
             FROM UNNEST(balance_changes) WHERE account = @wallet) AS owned_native_balances,
       ARRAY(SELECT AS STRUCT account_index, mint, owner,
                    CAST(amount AS STRING) AS amount_raw, decimals,
                    accounts[SAFE_OFFSET(account_index)].pubkey AS token_account
             FROM UNNEST(pre_token_balances) WHERE owner = @wallet) AS owned_pre_token_balances,
       ARRAY(SELECT AS STRUCT account_index, mint, owner,
                    CAST(amount AS STRING) AS amount_raw, decimals,
                    accounts[SAFE_OFFSET(account_index)].pubkey AS token_account
             FROM UNNEST(post_token_balances) WHERE owner = @wallet) AS owned_post_token_balances
FROM `{DATASET}.Transactions`
WHERE block_timestamp >= @start_utc AND block_timestamp < @end_utc
  AND signature IN UNNEST(@signatures)
ORDER BY block_timestamp, block_slot, signature
"""
BALANCE_SQL = f"""SELECT signature, block_slot, block_timestamp, status, err,
       ARRAY(SELECT AS STRUCT account_index, mint, owner,
                    CAST(amount AS STRING) AS amount_raw, decimals
             FROM UNNEST(pre_token_balances) WHERE owner = @wallet) AS owned_pre_token_balances,
       ARRAY(SELECT AS STRUCT account_index, mint, owner,
                    CAST(amount AS STRING) AS amount_raw, decimals
             FROM UNNEST(post_token_balances) WHERE owner = @wallet) AS owned_post_token_balances
FROM `{DATASET}.Transactions`
WHERE block_timestamp >= @start_utc AND block_timestamp < @end_utc
  AND signature IN UNNEST(@signatures)
ORDER BY block_timestamp, block_slot, signature
"""

SCHEMA = """
CREATE TABLE IF NOT EXISTS bigquery_solana_collections (
    collection_key TEXT PRIMARY KEY,
    case_key TEXT NOT NULL REFERENCES evm_flow_cases(case_key),
    fomo_user_id TEXT NOT NULL REFERENCES traders(fomo_user_id),
    wallet TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('known_receipts','owner_discovery','owner_details')),
    query_version TEXT NOT NULL,
    sql_text TEXT NOT NULL,
    sql_sha256 TEXT NOT NULL,
    parameters_json TEXT NOT NULL,
    scope_json TEXT NOT NULL,
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
    retrieval_status TEXT NOT NULL CHECK(retrieval_status='complete'),
    history_coverage_json TEXT NOT NULL,
    report_json TEXT NOT NULL,
    raw_metadata_id INTEGER NOT NULL REFERENCES raw_payloads(id),
    imported_at_utc TEXT NOT NULL,
    UNIQUE(project_id, location, job_id)
);
CREATE TABLE IF NOT EXISTS bigquery_solana_result_pages (
    collection_key TEXT NOT NULL REFERENCES bigquery_solana_collections(collection_key),
    page_index INTEGER NOT NULL,
    start_row INTEGER NOT NULL,
    row_count INTEGER NOT NULL,
    captured_at_utc TEXT NOT NULL,
    raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
    PRIMARY KEY(collection_key, page_index),
    UNIQUE(collection_key, start_row)
);
CREATE TABLE IF NOT EXISTS bigquery_solana_transactions (
    collection_key TEXT NOT NULL REFERENCES bigquery_solana_collections(collection_key),
    signature TEXT NOT NULL,
    block_slot INTEGER NOT NULL,
    block_time_utc TEXT NOT NULL,
    transaction_successful INTEGER NOT NULL,
    row_json TEXT NOT NULL,
    raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
    PRIMARY KEY(collection_key, signature)
);
CREATE INDEX IF NOT EXISTS idx_bigquery_solana_signature
    ON bigquery_solana_transactions(signature,block_time_utc);
CREATE TABLE IF NOT EXISTS bigquery_solana_rpc_checks (
    collection_key TEXT NOT NULL REFERENCES bigquery_solana_collections(collection_key),
    signature TEXT NOT NULL,
    status TEXT NOT NULL,
    raw_payload_id INTEGER REFERENCES raw_payloads(id),
    checks_json TEXT NOT NULL,
    captured_at_utc TEXT NOT NULL,
    PRIMARY KEY(collection_key,signature),
    FOREIGN KEY(collection_key,signature) REFERENCES bigquery_solana_transactions(collection_key,signature)
);
"""


def _scope(connection, case_key=None):
    case = ethereum_scope(connection, case_key)
    wallet = connection.execute(
        "SELECT solana_wallet_candidate FROM top10_wallet_inventory "
        "WHERE snapshot_at_utc=? AND fomo_user_id=? AND rank=9 AND solana_resolution_status='verified'",
        (case['leaderboard_snapshot_at_utc'], case['fomo_user_id']),
    ).fetchone()
    if wallet is None or not connection.execute(
        "SELECT 1 FROM wallet_resolutions WHERE fomo_user_id=? AND chain='solana' AND address=? AND status='verified'",
        (case['fomo_user_id'], wallet[0]),
    ).fetchone():
        raise ValueError("A verified fixed-cohort rank-9 Solana wallet is required")
    routes = []
    for row in connection.execute(
        "SELECT r.* FROM bridge_routes r JOIN bridge_deposits d USING(deposit_key) "
        "WHERE d.case_key=? AND r.destination_wallet=? AND r.evidence_status='order_correlated' "
        "ORDER BY r.destination_at_utc,r.route_key", (case['case_key'], wallet[0]),
    ):
        check = json.loads(row['evidence_json']).get('direct_rpc_check')
        if not check or check.get('status') != 'order_correlated':
            raise ValueError("A bridge route lacks retained direct RPC proof")
        route = {k: row[k] for k in ('route_key','deposit_key','destination_tx_hash','destination_wallet',
                 'destination_asset','destination_amount_raw','destination_decimals','destination_at_utc','destination_raw_payload_id')}
        routes.append(route | {'rpc_check': check})
    if not routes:
        raise ValueError("No known bridge receipts in the authorized wallet")
    return {k: case[k] for k in ('case_key','fomo_user_id','rank','leaderboard_snapshot_at_utc',
                                'window_start_utc','window_end_utc')} | {'wallet': wallet[0], 'bridge_routes': routes}


def _parameters(scope, signatures=None):
    values = [{"name": name, "parameterType": {"type": kind}, "parameterValue": {"value": value}}
              for name, kind, value in (("wallet", "STRING", scope['wallet']),
                                       ("start_utc", "TIMESTAMP", scope['window_start_utc']),
                                       ("end_utc", "TIMESTAMP", scope['window_end_utc']))]
    if signatures is not None:
        values.append({"name": "signatures", "parameterType": {"type": "ARRAY", "arrayType": {"type": "STRING"}},
                       "parameterValue": {"arrayValues": [{"value": s} for s in sorted(set(signatures))]}})
    return values


def _manifest(root, scope, project, role, signatures, cap):
    sql = {'owner_discovery': DISCOVERY_SQL, 'known_receipts': DETAIL_SQL, 'owner_details': BALANCE_SQL}[role]
    version = 'solana_owner_balances_v1' if role == 'owner_details' else QUERY_VERSION
    identity = {'scope': scope, 'role': role, 'sql': sql, 'sql_sha256': hashlib.sha256(sql.encode()).hexdigest(),
                'query_version': version, 'parameters': _parameters(scope, signatures),
                'project_id': project, 'dataset_id': DATASET, 'location': LOCATION}
    key = _digest(identity)
    directory = Path(root) / key
    path = directory / 'manifest.json'
    if path.exists():
        manifest = json.loads(path.read_text())
        if any(manifest.get(k) != v for k, v in identity.items()) or manifest['collection_key'] != key:
            raise ValueError("Existing query manifest differs from its requested identity")
        if 'maximum_bytes_billed' not in manifest:
            manifest['maximum_bytes_billed'] = str(cap)
    else:
        manifest = identity | {'collection_key': key, 'job_id': 'fomo_sol_' + key, 'maximum_bytes_billed': str(cap),
                               'created_at_utc': utc_now(), 'requests': [], 'pages': [], 'retrieval_status': 'pending'}
    _write(path, manifest)
    _write(directory / 'parameters.json', manifest['parameters'])
    return directory, manifest


def _fetch(directory, manifest, cap, page_size, dry_only=False):
    flags = ['--parameter=' + str(directory.resolve() / 'parameters.json')]
    if manifest['retrieval_status'] == 'complete':
        return
    if 'dry_run_capture' not in manifest:
        ref, dry = _call(directory, manifest, ['query','--use_legacy_sql=false','--dry_run=true', *flags], manifest['sql'])
        estimate = int(dry['statistics'].get('query', {}).get('totalBytesProcessed', dry['statistics'].get('totalBytesProcessed', '0')))
        manifest.update(dry_run_capture=ref, estimated_bytes_processed=str(estimate))
        _write(directory / 'manifest.json', manifest)
    print(_json({'phase': 'dry_run', 'role': manifest['role'], 'collection_key': manifest['collection_key'],
                 'estimated_bytes_processed': manifest['estimated_bytes_processed'],
                 'maximum_bytes_billed': manifest['maximum_bytes_billed']}), flush=True)
    if dry_only:
        return
    if int(manifest['estimated_bytes_processed']) > min(cap, int(manifest['maximum_bytes_billed'])):
        raise ValueError("Dry-run estimate exceeds the billing cap; no query submitted")
    if 'submission_capture' not in manifest:
        try:
            ref, _ = _call(directory, manifest, ['--synchronous_mode=false','--job_id=' + manifest['job_id'],
                        'query','--use_legacy_sql=false','--maximum_bytes_billed=' + manifest['maximum_bytes_billed'],
                        '--max_rows=0','--label=fomo_research:rank9_solana', *flags], manifest['sql'])
        except RuntimeError:
            # A timed-out submission may already exist: recover its stable ID, never start a second job.
            ref, recovered = _call(directory, manifest, ['show','--job=true', manifest['job_id']])
            if recovered.get('configuration', {}).get('query', {}).get('query') != manifest['sql']:
                raise ValueError("Recovered job has unexpected SQL")
        manifest['submission_capture'] = ref
        _write(directory / 'manifest.json', manifest)
    deadline = time.monotonic() + 900
    while True:
        ref, job = _call(directory, manifest, ['show','--job=true', manifest['job_id']])
        manifest['job_capture'] = ref
        _write(directory / 'manifest.json', manifest)
        if job.get('status', {}).get('state') == 'DONE':
            if job['status'].get('errorResult'):
                raise RuntimeError('Query failed; retained capture: ' + str(directory / ref))
            break
        if time.monotonic() >= deadline:
            raise RuntimeError('Job is pending; rerun this stage to resume its existing job')
        time.sleep(5)
    destination = job['configuration']['query']['destinationTable']
    ref, table = _call(directory, manifest, ['show', destination['projectId'] + ':' + destination['datasetId'] + '.' + destination['tableId']])
    manifest.update(result_table_capture=ref, total_rows=int(table['numRows']), retrieval_status='fetching')
    _write(directory / 'manifest.json', manifest)
    offset = sum(p['row_count'] for p in manifest['pages'])
    while offset < manifest['total_rows']:
        ref, rows = _call(directory, manifest, ['head','--job=true','--start_row=' + str(offset),
                          '--max_rows=' + str(min(page_size, manifest['total_rows'] - offset)), manifest['job_id']])
        if not isinstance(rows, list) or not rows or offset + len(rows) > manifest['total_rows']:
            raise ValueError('Result pagination did not advance consistently')
        manifest['pages'].append({'capture': ref, 'start_row': offset, 'row_count': len(rows)})
        offset += len(rows)
        _write(directory / 'manifest.json', manifest)
        print(_json({'phase': 'result_page','role': manifest['role'],'fetched_rows': offset,'total_rows': manifest['total_rows']}), flush=True)
    _read_rows(directory, manifest)
    manifest.update(retrieval_status='complete', completed_at_utc=utc_now())
    _write(directory / 'manifest.json', manifest)


def _read_rows(directory, manifest):
    rows, seen, offset = [], set(), 0
    start = datetime.fromisoformat(manifest['scope']['window_start_utc'].replace('Z', '+00:00'))
    end = datetime.fromisoformat(manifest['scope']['window_end_utc'].replace('Z', '+00:00'))
    for page in manifest['pages']:
        record = json.loads((directory / page['capture']).read_text())
        if _digest(record) != Path(page['capture']).stem:
            raise ValueError('Page content hash differs from its filename')
        values = record['payload']
        if page['start_row'] != offset or not isinstance(values, list) or len(values) != page['row_count']:
            raise ValueError('Non-contiguous result pages')
        for row in values:
            signature = row['signature']
            stamp = datetime.fromisoformat(_stamp(row['block_timestamp']).replace('Z', '+00:00'))
            if signature in seen or not re.fullmatch(r'[1-9A-HJ-NP-Za-km-z]{64,90}', signature) or not start <= stamp < end:
                raise ValueError('Duplicate/invalid signature or out-of-window timestamp')
            int(row['block_slot'])
            _successful(row)
            seen.add(signature)
            rows.append((row, page['capture']))
        offset += len(values)
    if offset != manifest['total_rows']:
        raise ValueError('Retrieved rows differ from result total')
    if manifest['role'] != 'owner_discovery':
        expected = {s['value'] for p in manifest['parameters'] if p['name'] == 'signatures' for s in p['parameterValue']['arrayValues']}
        if seen != expected:
            raise ValueError('Detailed signatures differ from the requested signature set')
    return rows


def _successful(row):
    if row['status'] == 'Success' and row.get('err') in (None, ''):
        return True
    if row['status'] != 'Success' and row.get('err') not in (None, ''):
        return False
    raise ValueError('Unrecognized or inconsistent Solana transaction success fields')


def _integer(value):
    amount = Decimal(str(value))
    if not amount.is_finite() or amount != amount.to_integral_value():
        raise ValueError('Expected an exact integer raw amount')
    return int(amount)


def _boolean(value):
    if value in (True, 'true'):
        return True
    if value in (False, 'false'):
        return False
    raise ValueError('Expected a BOOLEAN account field')


def parse_wallet_row(row, wallet, verified_matches=None):
    from .research import _classify_balance_changes
    amounts, decimals = defaultdict(int), {}
    accounts = row.get('accounts')
    for key, sign in (('owned_pre_token_balances', -1), ('owned_post_token_balances', 1)):
        for balance in row[key]:
            index = int(balance['account_index'])
            mint, scale, amount = balance['mint'], int(balance['decimals']), _integer(balance['amount_raw'])
            if balance['owner'] != wallet or index < 0 or accounts is not None and (index >= len(accounts) or accounts[index]['pubkey'] != balance['token_account']):
                raise ValueError('Historical owner or token-account index mismatch')
            if not 0 <= amount < 2 ** 64 or not 0 <= scale <= 255 or mint in decimals and decimals[mint] != scale:
                raise ValueError('Invalid amount/decimals or mixed mint scale')
            amounts[mint] += sign * amount
            decimals[mint] = scale
    if not amounts:
        raise ValueError('Detailed row lacks the tracked historical token owner')
    natives = row.get('owned_native_balances', [])
    if len(natives) > 1 or any(r['account'] != wallet for r in natives):
        raise ValueError('Ambiguous native balance row')
    # A missing native balance change is unknown, never an invented zero.
    native_delta = _integer(natives[0]['after_raw']) - _integer(natives[0]['before_raw']) if natives else None
    signer = any(a['pubkey'] == wallet and _boolean(a['signer']) for a in accounts) if accounts is not None else None
    result = _classify_balance_changes(row['signature'], int(row['block_slot']), _stamp(row['block_timestamp']),
                                      _successful(row), signer, {m: a for m, a in amounts.items() if a}, decimals,
                                      native_delta, _integer(row.get('fee_raw', '0')), row.get('log_messages', []), verified_matches)
    if signer is None:
        result['classification_confidence'] = 'historical_owner_balances_semantics_unknown'
    return result


def _rpc_baseline(connection, scope):
    baseline = {}
    for raw in connection.execute(
        "SELECT id,payload_json FROM raw_payloads WHERE source='solana-quicknode' "
        "AND route LIKE ? AND captured_at_utc>=? ORDER BY id",
        ('/getTransactionsForAddress?leaderboard_rank=' + str(scope['rank']) + '%', scope['leaderboard_snapshot_at_utc']),
    ):
        for item in (json.loads(raw['payload_json']).get('result') or {}).get('data') or []:
            signatures = (item.get('transaction') or {}).get('signatures') or []
            signature = signatures[0] if signatures else item.get('signature')
            if signature:
                baseline.setdefault(signature, (item, raw['id']))
    for route in scope['bridge_routes']:
        raw = connection.execute('SELECT payload_json FROM raw_payloads WHERE id=?', (route['destination_raw_payload_id'],)).fetchone()
        item = json.loads(raw[0])['response']['result']
        baseline[route['destination_tx_hash']] = (item, route['destination_raw_payload_id'])
    if connection.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='bigquery_solana_owner_rpc_pages'").fetchone():
        for page in connection.execute(
            "SELECT p.payload_json,p.id FROM bigquery_solana_owner_rpc_pages v JOIN bigquery_solana_collections c USING(collection_key) "
            "JOIN raw_payloads p ON p.id=v.raw_payload_id WHERE c.case_key=? AND c.wallet=? ORDER BY v.page_index",
            (scope['case_key'],scope['wallet']),
        ):
            for item in json.loads(page['payload_json'])['response']['result']['data']:
                baseline.setdefault(item['transaction']['signatures'][0],(item,page['id']))
    return baseline


def _delta_map(parsed):
    return {r['token_address']: (r['delta_raw'], r['token_decimals']) for r in parsed['token_deltas']}


def _reconcile(connection, scope, role, rows):
    from .research import _wallet_changes
    report = {'baseline_rpc_rows': 0, 'matched_rpc_rows': 0, 'new_owner_signatures': [],
              'rpc_comparisons': [], 'bridge_comparisons': [], 'action_counts': {}}
    if role == 'owner_discovery':
        return report
    baseline = _rpc_baseline(connection, scope)
    parsed_by_signature = {}
    counts = Counter()
    for row, _ in rows:
        parsed = parse_wallet_row(row, scope['wallet'])
        parsed_by_signature[row['signature']] = (row, parsed)
        counts[parsed['action_type']] += 1
        retained = baseline.get(row['signature'])
        if not retained:
            report['new_owner_signatures'].append(row['signature'])
            continue
        item, raw_id = retained
        rpc = _wallet_changes(item, scope['wallet'])
        checks = {k: parsed[k] == rpc[k] for k in ('slot','block_time_utc','successful')}
        checks['wallet_is_signer'] = parsed['wallet_is_signer'] == rpc['wallet_is_signer'] if parsed['wallet_is_signer'] is not None else None
        checks['token_deltas'] = _delta_map(parsed) == _delta_map(rpc)
        checks['fee_lamports'] = _integer(row['fee_raw']) == (item.get('meta') or {}).get('fee') if 'fee_raw' in row else None
        checks['native_delta_lamports'] = (parsed['native_balance_delta_lamports'] == rpc['native_balance_delta_lamports']
                                          if parsed['native_balance_delta_lamports'] is not None else None)
        report['baseline_rpc_rows'] += 1
        comparison = {'signature': row['signature'], 'rpc_raw_payload_id': raw_id, 'checks': checks,
                      'status': 'available_fields_matched' if all(v is not False for v in checks.values()) else 'mismatch',
                      'bigquery_native_balance_present': bool(row.get('owned_native_balances'))}
        report['rpc_comparisons'].append(comparison)
        if any(v is False for v in checks.values()):
            raise ValueError('Retained RPC comparison mismatch: ' + _json(comparison))
        report['matched_rpc_rows'] += 1
    for route in scope['bridge_routes']:
        if route['destination_tx_hash'] not in parsed_by_signature:
            if role == 'known_receipts':
                raise ValueError('Known bridge receipt missing from query results')
            continue
        row, parsed = parsed_by_signature[route['destination_tx_hash']]
        origin = connection.execute(
            'SELECT d.deposit_id,r.operation_id FROM bridge_deposits d JOIN bridge_routes r USING(deposit_key) WHERE r.route_key=?',
            (route['route_key'],),
        ).fetchone()
        memo_logs = [s for s in row.get('log_messages', []) if 'Program log: Memo ' in s]
        checks = {'successful': parsed['successful'], 'slot': parsed['slot'] == route['rpc_check']['slot'],
                  'block_time': parsed['block_time_utc'] == route['destination_at_utc'],
                  'mint_owner_delta': _delta_map(parsed).get(route['destination_asset']) ==
                                      (route['destination_amount_raw'], route['destination_decimals']),
                  'deposit_id_memo': any(origin['deposit_id'] in s for s in memo_logs) if memo_logs else None,
                  'operation_id_memo': any(origin['operation_id'] in s for s in memo_logs) if memo_logs else None}
        expected_accounts = {t['token_account'] for t in route['rpc_check']['transfers']}
        actual_accounts = {b['token_account'] for b in row['owned_post_token_balances']
                           if b['mint'] == route['destination_asset'] and b['owner'] == scope['wallet'] and 'token_account' in b}
        checks['token_account'] = expected_accounts <= actual_accounts if actual_accounts else None
        comparison = {'route_key': route['route_key'], 'deposit_key': route['deposit_key'],
                      'signature': row['signature'], 'checks': checks, 'amount_raw': route['destination_amount_raw'],
                      'status': ('core_matched_memos_rpc_only' if not memo_logs else 'matched') if all(v is not False for v in checks.values()) else 'mismatch',
                      'rpc_order_memos_verified': route['rpc_check']['deposit_id_memo_matches'] and route['rpc_check']['operation_id_memo_matches'],
                      'bigquery_logs_available': any(row.get('log_messages', [])),
                      'owner_present_in_account_keys': any(a['pubkey'] == scope['wallet'] for a in row['accounts']) if 'accounts' in row else None}
        report['bridge_comparisons'].append(comparison)
        if any(v is False for v in checks.values()):
            raise ValueError('Bridge receipt comparison mismatch: ' + _json(comparison))
    report['action_counts'] = dict(counts)
    report['rows_with_nonempty_logs'] = sum(bool(any(r.get('log_messages', []))) for r, _ in rows)
    return report


def import_capture(directory, database):
    directory = Path(directory)
    manifest = json.loads((directory / 'manifest.json').read_text())
    identity = {k: manifest[k] for k in ('scope','role','sql','sql_sha256','query_version','parameters','project_id','dataset_id','location')}
    if _digest(identity) != manifest['collection_key'] or manifest['retrieval_status'] != 'complete':
        raise ValueError('Incomplete or inconsistent collection manifest')
    expected_version = 'solana_owner_balances_v1' if manifest['role'] == 'owner_details' else QUERY_VERSION
    if manifest['query_version'] != expected_version or manifest['dataset_id'] != DATASET or manifest['location'] != LOCATION:
        raise ValueError('Unexpected query version/dataset/location')
    expected_sql = {'owner_discovery': DISCOVERY_SQL, 'known_receipts': DETAIL_SQL, 'owner_details': BALANCE_SQL}[manifest['role']]
    if manifest['sql'] != expected_sql or hashlib.sha256(expected_sql.encode()).hexdigest() != manifest['sql_sha256']:
        raise ValueError('Unexpected collector SQL')
    rows = _read_rows(directory, manifest)
    store = Store(database)
    with store.connect() as connection:
        connection.executescript(SCHEMA)
        existing = connection.execute('SELECT report_json FROM bigquery_solana_collections WHERE collection_key=?', (manifest['collection_key'],)).fetchone()
        if existing:
            return json.loads(existing[0])
        scope = manifest['scope']
        if _scope(connection, scope['case_key']) != scope:
            raise ValueError('Collection no longer matches its verified retained scope')
        report = _reconcile(connection, scope, manifest['role'], rows)
        record = json.loads((directory / manifest['job_capture']).read_text())
        job = record['payload']
        if job.get('status', {}).get('state') != 'DONE' or job['status'].get('errorResult'):
            raise ValueError('Job has not succeeded')
        if job['jobReference'] != {'projectId': manifest['project_id'],'jobId': manifest['job_id'],'location': LOCATION}:
            raise ValueError('Unexpected job identity')
        if job['configuration']['query']['query'] != manifest['sql'] or job['configuration']['query'].get('queryParameters') != manifest['parameters']:
            raise ValueError('Job SQL or typed parameters differ from the manifest')
        stats = job['statistics'].get('query', {})
        coverage = {'history_status': 'unknown', 'scope': 'Transactions containing tracked owner in historical pre/post token balances',
                    'query_result_retrieval': 'complete', 'native_only_activity': 'excluded by owner discovery',
                    'provider_indexing_and_missing_owner_metadata': 'not proven complete',
                    'detailed_balances': 'tracked owner only; original accounts and available logs retained; blank logs do not prove absence of swap/memo instructions',
                    'zero_native_change': 'unknown when no balance-change row is present',
                    'failed_transactions': 'retained; never classified as executed buys/sells'}
        report.update(collection_key=manifest['collection_key'], role=manifest['role'], query_version=manifest['query_version'],
                      scope=scope, job_id=manifest['job_id'], project_id=manifest['project_id'], dataset_id=DATASET, location=LOCATION,
                      sql_sha256=manifest['sql_sha256'], maximum_bytes_billed=manifest['maximum_bytes_billed'],
                      estimated_bytes_processed=manifest['estimated_bytes_processed'], bytes_processed=stats.get('totalBytesProcessed','0'),
                      bytes_billed=stats.get('totalBytesBilled','0'), cache_hit=bool(stats.get('cacheHit', False)),
                      total_rows=manifest['total_rows'], fetched_rows=len(rows), page_count=len(manifest['pages']),
                      retrieval_status='complete', history_coverage=coverage, capture_directory=str(directory.resolve()), imported_at_utc=utc_now())
        raw_ids = {}
        for reference in dict.fromkeys(manifest['requests']):
            record = json.loads((directory / reference).read_text())
            if _digest(record) != Path(reference).stem:
                raise ValueError('Capture content hash mismatch')
            raw_ids[reference] = store.save_raw(connection, 'bigquery_bq_cli', manifest['project_id'] + '/' + LOCATION + '/' + manifest['job_id'],
                                               record, record['completed_at_utc'], status=None)
        collection = {k: report[k] for k in ('collection_key','role','query_version','job_id','project_id','dataset_id','location','sql_sha256',
                      'maximum_bytes_billed','estimated_bytes_processed','bytes_processed','bytes_billed','total_rows','fetched_rows','retrieval_status','imported_at_utc')}
        collection.update(case_key=scope['case_key'],fomo_user_id=scope['fomo_user_id'],wallet=scope['wallet'],
                          sql_text=manifest['sql'],parameters_json=_json(manifest['parameters']),scope_json=_json(scope),
                          window_start_utc=scope['window_start_utc'],window_end_utc=scope['window_end_utc'],cache_hit=int(report['cache_hit']),
                          history_coverage_json=_json(coverage),report_json=_json(report),raw_metadata_id=raw_ids[manifest['job_capture']])
        columns = list(collection)
        connection.execute('INSERT INTO bigquery_solana_collections (' + ','.join(columns) + ') VALUES (' + ','.join('?' for _ in columns) + ')', tuple(collection[k] for k in columns))
        for index, page in enumerate(manifest['pages']):
            record = json.loads((directory / page['capture']).read_text())
            connection.execute('INSERT INTO bigquery_solana_result_pages VALUES (?,?,?,?,?,?)',
                               (manifest['collection_key'],index,page['start_row'],page['row_count'],record['completed_at_utc'],raw_ids[page['capture']]))
        for row, reference in rows:
            connection.execute('INSERT INTO bigquery_solana_transactions VALUES (?,?,?,?,?,?,?)',
                               (manifest['collection_key'],row['signature'],int(row['block_slot']),_stamp(row['block_timestamp']),
                                int(_successful(row)),_json(row),raw_ids[reference]))
    _write(directory / 'report.json', report)
    return report


def collect(database, project, directory, role, cap, page_size, dry_only=False, case_key=None):
    if not re.fullmatch(r'[a-z][a-z0-9-]{4,61}[a-z0-9]', project) or cap <= 0 or not 1 <= page_size <= 10000:
        raise ValueError('Invalid query project, cap, or page size')
    store = Store(database)
    with store.connect() as connection:
        scope = _scope(connection, case_key)
        signatures = None
        if role == 'known_receipts':
            signatures = [r['destination_tx_hash'] for r in scope['bridge_routes']]
        elif role == 'owner_details':
            discovery = connection.execute(
                "SELECT collection_key FROM bigquery_solana_collections WHERE case_key=? AND wallet=? "
                "AND role='owner_discovery' AND retrieval_status='complete' AND window_start_utc=? AND window_end_utc=? ORDER BY imported_at_utc DESC LIMIT 1",
                (scope['case_key'],scope['wallet'],scope['window_start_utc'],scope['window_end_utc']),
            ).fetchone()
            if not discovery:
                raise ValueError('Run/import the complete owner_discovery stage first')
            signatures = [r[0] for r in connection.execute('SELECT signature FROM bigquery_solana_transactions WHERE collection_key=? ORDER BY signature', (discovery[0],))]
            if not signatures:
                raise ValueError('Discovery contains no signatures; detailed coverage cannot be established')
    directory, manifest = _manifest(directory, scope, project, role, signatures, cap)
    _fetch(directory, manifest, cap, page_size, dry_only)
    return {'collection_key': manifest['collection_key'], 'role': role, 'estimated_bytes_processed': manifest['estimated_bytes_processed'],
            'capture_directory': str(directory.resolve()), 'dry_run_only': True} if dry_only else import_capture(directory, database)


def enrich_missing_rpc(database, case_key=None):
    """Fetch only newly discovered owner signatures absent from retained RPC history."""
    from .bridge import _post
    from .config import load_solana_rpc_url
    from .research import _wallet_changes
    store = Store(database)
    with store.connect() as connection:
        connection.executescript(SCHEMA)
        scope = _scope(connection, case_key)
        collection = connection.execute(
            "SELECT collection_key FROM bigquery_solana_collections WHERE case_key=? AND wallet=? AND role='owner_details' "
            "AND retrieval_status='complete' ORDER BY imported_at_utc DESC LIMIT 1", (scope['case_key'],scope['wallet']),
        ).fetchone()
        if not collection:
            raise ValueError('Import owner_details first')
        baseline = _rpc_baseline(connection, scope)
        tracked_mints = {r[0] for r in connection.execute(
            "SELECT DISTINCT token_address FROM fomo_events WHERE fomo_user_id=? AND lower(chain)='solana' AND token_address IS NOT NULL",
            (scope['fomo_user_id'],),
        )} | {'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'}
        new_rows = [dict(r) for r in connection.execute('SELECT * FROM bigquery_solana_transactions WHERE collection_key=? ORDER BY block_time_utc,signature', (collection[0],))
                    if r['signature'] not in baseline]
        pending = []
        for row in new_rows:
            action = parse_wallet_row(json.loads(row['row_json']),scope['wallet'])
            if action['successful'] and any(d['token_address'] in tracked_mints for d in action['token_deltas']):
                pending.append(row)
        previous = {r['signature']: r['status'] for r in connection.execute('SELECT signature,status FROM bigquery_solana_rpc_checks WHERE collection_key=?', (collection[0],))}
    counts = Counter(previous.values())
    for i, indexed in enumerate(pending):
        signature = indexed['signature']
        if signature in previous:
            continue
        row = json.loads(indexed['row_json'])
        params = [signature, {'encoding': 'jsonParsed','commitment': 'finalized','maxSupportedTransactionVersion': 0}]
        body = {'jsonrpc': '2.0','id': 1,'method': 'getTransaction','params': params}
        attempts = []
        for attempt in range(3):
            record = _post(load_solana_rpc_url(), body, 'configured_solana_rpc')
            with store.connect() as connection:
                raw_id = store.save_raw(connection, 'configured_solana_rpc', 'getTransaction?bigquery_collection=' + collection[0],
                                         record, record['completed_at'], record['http_status'])
            attempts.append(raw_id)
            if record['http_status'] not in (None,429,500,502,503,504):
                break
            time.sleep(1 + attempt)
        item = record['response'].get('result')
        checks = {'attempt_raw_payload_ids': attempts}
        status = 'unavailable'
        if isinstance(item, dict):
            rpc = _wallet_changes(item, scope['wallet'])
            indexed_action = parse_wallet_row(row, scope['wallet'])
            equality = {k: rpc[k] == indexed_action[k] for k in ('signature','slot','block_time_utc','successful')}
            equality['wallet_is_signer'] = rpc['wallet_is_signer'] == indexed_action['wallet_is_signer'] if indexed_action['wallet_is_signer'] is not None else None
            equality['token_deltas'] = _delta_map(rpc) == _delta_map(indexed_action)
            equality['fee_lamports'] = item['meta']['fee'] == _integer(row['fee_raw']) if 'fee_raw' in row else None
            equality['native_delta_lamports'] = (rpc['native_balance_delta_lamports'] == indexed_action['native_balance_delta_lamports']
                                                 if indexed_action['native_balance_delta_lamports'] is not None else None)
            status = 'verified' if all(v is not False for v in equality.values()) else 'mismatch'
            checks.update(checks=equality, normalized_rpc_action=rpc, native_balance_comparison_available=equality['native_delta_lamports'] is not None)
        else:
            checks.update(http_status=record['http_status'], rpc_result='null' if item is None else 'unknown',
                          rpc_error=record['response'].get('error'))
        with store.connect() as connection:
            connection.execute('INSERT INTO bigquery_solana_rpc_checks VALUES (?,?,?,?,?,?)',
                               (collection[0],signature,status,raw_id,_json(checks),record['completed_at']))
        counts[status] += 1
        if status == 'mismatch':
            raise ValueError('RPC disagrees with indexed owner row: ' + signature)
        if (i + 1) % 10 == 0 or i + 1 == len(pending):
            print(_json({'phase':'rpc_enrichment','candidates':len(pending),'processed':i+1,'status_counts':dict(counts)}), flush=True)
        time.sleep(0.15)
    return {'collection_key': collection[0], 'new_owner_rows': len(new_rows), 'new_owner_rpc_candidates': len(pending),
            'rpc_scope': 'successful new owner rows with nonzero USDC or current Fomo Solana-token deltas',
            'rpc_status_counts': dict(counts)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', default=str(DEFAULT_DATABASE))
    parser.add_argument('--project', default='exchange-labs')
    parser.add_argument('--case-key')
    parser.add_argument('--directory', default=str(REPO_ROOT / 'data/raw/bigquery-solana'))
    parser.add_argument('--stage', choices=('known_receipts','owner_discovery','owner_details'), default='known_receipts')
    parser.add_argument('--maximum-bytes-billed', type=int, default=128 * 1024 ** 3)
    parser.add_argument('--page-size', type=int, default=200)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--import-capture', help='Import complete saved evidence without cloud calls')
    parser.add_argument('--enrich-missing-rpc', action='store_true', help='Fetch RPC only for new owner rows absent from retained RPC history')
    args = parser.parse_args()
    try:
        if args.enrich_missing_rpc:
            print(json.dumps(enrich_missing_rpc(args.database,args.case_key), indent=2))
            return 0
        report = import_capture(args.import_capture, args.database) if args.import_capture else collect(
            args.database,args.project,args.directory,args.stage,args.maximum_bytes_billed,args.page_size,args.dry_run,args.case_key)
        print(json.dumps({k: report[k] for k in ('collection_key','role','estimated_bytes_processed','total_rows','fetched_rows','page_count',
                         'bytes_processed','bytes_billed','baseline_rpc_rows','matched_rpc_rows','action_counts','capture_directory','dry_run_only') if k in report}, indent=2))
        return 0
    except (RuntimeError,ValueError,OSError,KeyError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
