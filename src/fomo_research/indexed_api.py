"""Offline ingestion of retained Nodit discovery pages, with exact raw amounts."""
import hashlib
import json
from datetime import datetime, timezone

from .store import _json, utc_now

SCHEMA = """
CREATE TABLE IF NOT EXISTS indexed_api_collections (
 collection_key TEXT PRIMARY KEY,
 fomo_user_id TEXT REFERENCES traders(fomo_user_id),
 provider TEXT NOT NULL, chain TEXT NOT NULL, route TEXT NOT NULL,
 window_start_utc TEXT NOT NULL, window_end_utc TEXT NOT NULL,
 request_json TEXT NOT NULL, retrieval_status TEXT NOT NULL,
 reported_rows INTEGER, fetched_unique_rows INTEGER NOT NULL,
 coverage_status TEXT NOT NULL,
 manifest_raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
 manifest_json TEXT NOT NULL, captured_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS indexed_api_movements (
 collection_key TEXT NOT NULL REFERENCES indexed_api_collections(collection_key),
 movement_key TEXT NOT NULL, transaction_hash TEXT NOT NULL, locator TEXT NOT NULL,
 block_number INTEGER NOT NULL, at_utc TEXT NOT NULL,
 from_address TEXT NOT NULL, to_address TEXT,
 asset TEXT NOT NULL, amount_raw TEXT NOT NULL, decimals INTEGER,
 input_selector TEXT, movement_type TEXT NOT NULL,
 evidence_status TEXT NOT NULL,
 raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
 row_json TEXT NOT NULL, caution_json TEXT NOT NULL,
 PRIMARY KEY(collection_key,movement_key)
);
CREATE INDEX IF NOT EXISTS idx_indexed_from ON indexed_api_movements(from_address,at_utc);
CREATE INDEX IF NOT EXISTS idx_indexed_to ON indexed_api_movements(to_address,at_utc);
"""


def movement(row, method, chain, raw_id):
    """Index discovery evidence only; neither token ownership nor a swap is inferred."""
    token = method.startswith('token/')
    tx = row['transactionHash'].lower()
    locator = 'erc20_log:' + str(row['logIndex']) if token else 'transaction'
    if row.get('batchIndex') is not None:
        locator += ':batch:' + str(row['batchIndex'])
    contract = row.get('contract') or {}
    asset = contract['address'].lower() if token else 'native:' + ('BNB' if chain == 'eip155:56' else 'ETH')
    amount = str(row['value'])
    if not amount.isdigit():
        raise ValueError('Raw quantities must be nonnegative integer strings')
    at = datetime.fromtimestamp(int(row['timestamp']), timezone.utc).isoformat().replace('+00:00', 'Z')
    selector = row.get('functionSelector') or (row.get('function') or {}).get('selector')
    caution = ['provider_indexed_assertion', 'ownership_unknown']
    if token:
        caution.append('transfer_event_is_not_a_purchase')
    else:
        if int(amount) == 0:
            caution.append('zero_native_value')
        if row.get('input') != '0x':
            caution.append('contract_call_not_automatic_funding')
        if row.get('status') not in ('1', '0x1', 1):
            caution.append('success_not_confirmed_by_index')
        if 0 < int(amount) <= 10**10:
            caution.append('dust_not_automatic_funding')
    identity = {'tx': tx, 'locator': locator, 'asset': asset}
    key = hashlib.sha256(_json(identity).encode()).hexdigest()
    return [key, tx, locator, int(row['blockNumber']), at, row['from'].lower(),
            row['to'].lower() if row.get('to') else None, asset, amount,
            contract.get('decimals') if token else 18, selector,
            'TOKEN_TRANSFER_EVENT' if token else 'TOP_LEVEL_TRANSACTION',
            'provider_indexed_assertion', raw_id, _json(row), _json(caution)]


def import_collection(store, manifest, fomo_user_id=None):
    """Read saved DB pages. Makes no provider requests and changes no wallet resolution."""
    chain = {'bnb': 'eip155:56', 'ethereum': 'eip155:1'}[manifest['chain']]
    identity = {'provider': 'nodit_web3_data_api', 'chain': chain,
                'method': manifest['method'], 'request': manifest['request']}
    key = hashlib.sha256(_json(identity).encode()).hexdigest()
    rows = {}
    with store.connect() as c:
        c.executescript(SCHEMA)
        for page in manifest['pages']:
            raw = c.execute('SELECT payload_json FROM raw_payloads WHERE id=?', (page['raw_payload_id'],)).fetchone()
            if raw is None:
                raise ValueError('Missing saved page')
            record = json.loads(raw[0])
            if record.get('http_status') != 200:
                continue
            for item in record['response']['items']:
                row = movement(item, manifest['method'], chain, page['raw_payload_id'])
                if row[0] in rows and rows[row[0]][1:11] != row[1:11]:
                    raise ValueError('Conflicting movement identity in saved pages')
                rows.setdefault(row[0], row)
        total = manifest.get('reported_count')
        if manifest['retrieval_status'] == 'complete' and total is not None and len(rows) != total:
            raise ValueError('Complete manifest does not match unique saved rows')
        capture = manifest['captured_at_utc']
        body = _json(manifest)
        digest = hashlib.sha256(body.encode()).hexdigest()
        route = '/offline/nodit/' + manifest['name']
        prior = c.execute('SELECT id FROM raw_payloads WHERE source=? AND route=? AND sha256=?',
                          ('indexed_api_manifest', route, digest)).fetchone()
        raw_id = prior[0] if prior else store.save_raw(c, 'indexed_api_manifest', route, manifest, capture, status=None)
        values = [key, fomo_user_id, identity['provider'], chain, manifest['method'],
                  manifest['request']['fromDate'], manifest['request']['toDate'],
                  _json(manifest['request']), manifest['retrieval_status'], total, len(rows),
                  manifest.get('chain_history_coverage', 'unknown'), raw_id, body, capture]
        old = c.execute('SELECT fetched_unique_rows FROM indexed_api_collections WHERE collection_key=?', (key,)).fetchone()
        if old and old[0] > len(rows):
            raise ValueError('Do not replace a larger saved collection with a partial capture')
        c.execute('''INSERT INTO indexed_api_collections VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
          ON CONFLICT(collection_key) DO UPDATE SET
          retrieval_status=excluded.retrieval_status,reported_rows=excluded.reported_rows,
          fetched_unique_rows=excluded.fetched_unique_rows,coverage_status=excluded.coverage_status,
          manifest_raw_payload_id=excluded.manifest_raw_payload_id,
          manifest_json=excluded.manifest_json,captured_at_utc=excluded.captured_at_utc''', values)
        inserted = 0
        for row in rows.values():
            prior = c.execute('SELECT transaction_hash,locator,block_number,at_utc,from_address,to_address,asset,amount_raw,decimals FROM indexed_api_movements WHERE collection_key=? AND movement_key=?',
                              (key,row[0])).fetchone()
            if prior and list(prior) != row[1:10]:
                raise ValueError('Conflicting previously normalized movement')
            cur = c.execute('INSERT OR IGNORE INTO indexed_api_movements VALUES (' + ','.join('?' for _ in range(17)) + ')', [key] + row)
            inserted += cur.rowcount
    return {'name':manifest['name'],'collection_key':key,'rows':len(rows),'inserted':inserted,
            'manifest_raw_payload_id':raw_id,'retrieval_status':manifest['retrieval_status']}
