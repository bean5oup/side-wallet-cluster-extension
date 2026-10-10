"""Recover the bounded owner history in full RPC pages, including token accounts."""

import argparse
import json
import time
from collections import Counter
from urllib.parse import urlparse

from .bigquery import _write
from .bigquery_solana import _delta_map, parse_wallet_row
from .bridge import _post
from .config import DEFAULT_DATABASE, load_solana_rpc_url
from .research import CLASSIFICATION_VERSION, _timestamp, _wallet_changes
from .store import Store, _json, utc_now

SCHEMA = """
CREATE TABLE IF NOT EXISTS bigquery_solana_owner_rpc_pages (
    collection_key TEXT NOT NULL REFERENCES bigquery_solana_collections(collection_key),
    page_index INTEGER NOT NULL,
    request_cursor TEXT,
    response_cursor TEXT,
    row_count INTEGER NOT NULL,
    request_json TEXT NOT NULL,
    raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
    captured_at_utc TEXT NOT NULL,
    PRIMARY KEY(collection_key,page_index)
);
"""


def collect(database):
    store = Store(database)
    with store.connect() as connection:
        connection.executescript(SCHEMA)
        collection = connection.execute("SELECT * FROM bigquery_solana_collections WHERE role='owner_details' AND retrieval_status='complete' ORDER BY imported_at_utc DESC LIMIT 1").fetchone()
        if not collection:
            raise ValueError('Import owner_details first')
        scope = json.loads(collection['scope_json'])
        rows = {r['signature']:json.loads(r['row_json']) for r in connection.execute('SELECT signature,row_json FROM bigquery_solana_transactions WHERE collection_key=?',(collection['collection_key'],))}
        pages = [dict(r) for r in connection.execute('SELECT * FROM bigquery_solana_owner_rpc_pages WHERE collection_key=? ORDER BY page_index',(collection['collection_key'],))]
    cursor = pages[-1]['response_cursor'] if pages else None
    index = len(pages)
    start = int(_timestamp(scope['window_start_utc']))
    end = int(_timestamp(scope['window_end_utc']))
    seen_cursors = {p['request_cursor'] for p in pages}
    while not pages or cursor is not None:
        if cursor in seen_cursors:
            raise ValueError('Owner RPC pagination cursor repeated')
        rpc_url = load_solana_rpc_url()
        if not (urlparse(rpc_url).hostname or '').endswith('.quiknode.pro'):
            raise ValueError('This optional owner-history route requires the authorized QuickNode endpoint in SOLANA_RPC_URL')
        config = {'transactionDetails':'full','encoding':'jsonParsed','maxSupportedTransactionVersion':1,
                  'commitment':'finalized','limit':1000,'sortOrder':'desc',
                  'filters':{'blockTime':{'gte':start,'lt':end},'tokenAccounts':'balanceChanged'}}
        if cursor is not None:
            config['paginationToken'] = cursor
        body = {'jsonrpc':'2.0','id':1,'method':'getTransactionsForAddress','params':[scope['wallet'],config]}
        for attempt in range(3):
            record = _post(rpc_url,body,'solana-quicknode-owner')
            record['route'] = 'getTransactionsForAddress'
            result = record['response'].get('result')
            if record['http_status'] == 200 and isinstance(result,dict) and isinstance(result.get('data'),list):
                break
            with store.connect() as connection:
                store.save_raw(connection,'solana-quicknode-owner','getTransactionsForAddress?collection=' + collection['collection_key'],record,record['completed_at'],record['http_status'])
            if record['http_status'] not in (None,429,500,502,503,504):
                raise RuntimeError('Owner RPC page failed; HTTP ' + str(record['http_status']) + '; error ' + _json(record['response'].get('error')))
            time.sleep(1 + attempt)
        else:
            raise RuntimeError('Owner RPC page failed after retries; retained raw attempts')
        signatures = set()
        for item in result['data']:
            signature = item['transaction']['signatures'][0]
            if signature in signatures or not start <= item['blockTime'] < end:
                raise ValueError('Duplicate signature or out-of-range owner RPC record')
            signatures.add(signature)
        with store.connect() as connection:
            raw_id = store.save_raw(connection,'solana-quicknode-owner','getTransactionsForAddress?collection=' + collection['collection_key'] + '&page=' + str(index + 1),record,record['completed_at'],record['http_status'])
            connection.execute('INSERT INTO bigquery_solana_owner_rpc_pages VALUES (?,?,?,?,?,?,?,?)',
                               (collection['collection_key'],index,cursor,result.get('paginationToken'),len(result['data']),_json(body),raw_id,record['completed_at']))
        pages.append({'page_index':index,'row_count':len(result['data']),'response_cursor':result.get('paginationToken'),'raw_payload_id':raw_id})
        seen_cursors.add(cursor)
        cursor = result.get('paginationToken')
        index += 1
        print(_json({'phase':'owner_rpc_page','page':index,'page_rows':len(result['data']),'fetched_rows':sum(p['row_count'] for p in pages),'has_next':cursor is not None}),flush=True)
    matches, mismatch, observed = {}, [], set()
    counts = Counter()
    with store.connect() as connection:
        for page in pages:
            raw = connection.execute('SELECT payload_json FROM raw_payloads WHERE id=?',(page['raw_payload_id'],)).fetchone()
            payload = json.loads(raw[0])['response']['result']
            for item in payload['data']:
                signature = item['transaction']['signatures'][0]
                if signature in observed:
                    raise ValueError('Duplicate signature across owner RPC pages')
                observed.add(signature)
                rpc = _wallet_changes(item,scope['wallet'])
                counts[rpc['action_type']] += 1
                if signature not in rows:
                    continue
                indexed = parse_wallet_row(rows[signature],scope['wallet'])
                checks = {field:rpc[field] == indexed[field] for field in ('signature','slot','block_time_utc','successful')}
                checks['token_deltas'] = _delta_map(rpc) == _delta_map(indexed)
                status = 'verified' if all(checks.values()) else 'mismatch'
                evidence = {'checks':checks,'provider':'solana-quicknode-owner','rpc_page':page['page_index'],
                            'normalized_rpc_action':rpc,'replaces_unavailable_point_response':True}
                connection.execute('INSERT INTO bigquery_solana_rpc_checks VALUES (?,?,?,?,?,?) '
                                   'ON CONFLICT(collection_key,signature) DO UPDATE SET status=excluded.status,raw_payload_id=excluded.raw_payload_id,'
                                   'checks_json=excluded.checks_json,captured_at_utc=excluded.captured_at_utc',
                                   (collection['collection_key'],signature,status,page['raw_payload_id'],_json(evidence),utc_now()))
                if status=='verified':
                    matches[signature] = page['raw_payload_id']
                else:
                    mismatch.append(signature)
        report = {'collection_key':collection['collection_key'],'scope':scope,'provider':'solana-quicknode-owner',
                  'method':'getTransactionsForAddress','filter_token_accounts':'balanceChanged','classification_version':CLASSIFICATION_VERSION,
                  'max_supported_transaction_version':1,'page_count':len(pages),'retrieved_unique_rpc_signatures':len(observed),
                  'rpc_pagination':'exhausted' if cursor is None else 'incomplete','bigquery_owner_signatures':len(rows),
                  'matched_bigquery_signatures':len(matches),'mismatched_signatures':mismatch,'bigquery_not_in_rpc':sorted(set(rows)-observed),
                  'rpc_not_in_bigquery':sorted(observed-set(rows)),'rpc_action_counts':dict(counts),
                  'documented_quicknode_credits_estimate':len(pages)*120,'quicknode_balance':'unknown',
                  'history_coverage':'only the fixed window and provider-returned owner activity; indexing/closed-account completeness not guaranteed',
                  'generated_at_utc':utc_now()}
    _write(store.database.parent / 'rank9-solana-owner-rpc.json',report)
    if mismatch:
        raise ValueError('Owner RPC/BigQuery mismatch: ' + ','.join(mismatch[:3]))
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database',default=str(DEFAULT_DATABASE))
    args=parser.parse_args()
    report=collect(args.database)
    print(json.dumps({k:report[k] for k in ('collection_key','page_count','retrieved_unique_rpc_signatures','rpc_pagination','matched_bigquery_signatures','rpc_action_counts','documented_quicknode_credits_estimate')},indent=2))


if __name__=='__main__':
    main()
