"""Offline SQLite ingestion of a reviewed counterparty/CEX/pre-buy evidence slice."""
import argparse
import hashlib
import json
from pathlib import Path
from .store import Store, _json, utc_now
from .wallet_trace import import_report

SCHEMA = """
CREATE TABLE IF NOT EXISTS wallet_trace_discovery_collections (
 collection_key TEXT PRIMARY KEY, fomo_user_id TEXT NOT NULL REFERENCES traders(fomo_user_id),
 query_kind TEXT NOT NULL, project_id TEXT NOT NULL, job_id TEXT NOT NULL,
 window_start_utc TEXT NOT NULL, window_end_utc TEXT NOT NULL,
 total_rows INTEGER NOT NULL, retrieval_status TEXT NOT NULL,
 metadata_raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
 manifest_json TEXT NOT NULL, UNIQUE(project_id,job_id)
);
CREATE TABLE IF NOT EXISTS wallet_trace_discovery_rows (
 collection_key TEXT NOT NULL REFERENCES wallet_trace_discovery_collections(collection_key),
 row_index INTEGER NOT NULL, row_json TEXT NOT NULL,
 raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
 caution_json TEXT NOT NULL, PRIMARY KEY(collection_key,row_index)
);
CREATE TABLE IF NOT EXISTS wallet_trace_acquisitions (
 acquisition_key TEXT PRIMARY KEY, fomo_user_id TEXT NOT NULL REFERENCES traders(fomo_user_id),
 chain TEXT NOT NULL, address TEXT NOT NULL, tx TEXT NOT NULL,
 at_utc TEXT NOT NULL, token_address TEXT NOT NULL, token_amount_raw TEXT NOT NULL,
 token_decimals INTEGER NOT NULL, quote_asset TEXT NOT NULL, quote_supplied_raw TEXT NOT NULL,
 wrapped_weth_raw TEXT NOT NULL, network_fee_raw TEXT NOT NULL,
 evidence_status TEXT NOT NULL, ownership_status TEXT NOT NULL CHECK(ownership_status='unknown'),
 receipt_raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
 transaction_raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
 block_raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
 query_raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
 evidence_json TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_wallet_trace_acquisition_time
 ON wallet_trace_acquisitions(chain,address,token_address,at_utc);
"""

def ingest(report_path, directory, database):
    """A review stores evidence provenance; this importer is not a chain validator."""
    directory=Path(directory); report_path=Path(report_path)
    report=json.loads(report_path.read_text())
    result=import_report(report_path,directory,database)
    store=Store(database)
    with store.connect() as c:
        c.executescript(SCHEMA)
        reviewed=json.loads(c.execute('SELECT payload_json FROM raw_payloads WHERE id=?',(result['report_raw_payload_id'],)).fetchone()[0])
        raw_ids=reviewed['capture_raw_payload_ids'];query_ids={}
        for collection in reviewed['discovery_collections']:
            kind=collection['kind'];d=directory/('bigquery-'+kind)
            m=json.loads((d/'manifest.json').read_text())
            if m['retrieval_status']!='complete' or hashlib.sha256(m['sql'].encode()).hexdigest()!=m['sql_sha256']:
                raise ValueError('Incomplete query or SQL hash mismatch')
            for ref in dict.fromkeys(m['requests']):
                record=json.loads((d/ref).read_text());digest=hashlib.sha256(_json(record).encode()).hexdigest()
                if digest!=Path(ref).stem:raise ValueError('Query capture hash mismatch')
                route=m['project_id']+'/'+m['location']+'/'+m['job_id']
                prior=c.execute('SELECT id FROM raw_payloads WHERE source=? AND route=? AND sha256=?',('bigquery_bq_cli',route,digest)).fetchone()
                query_ids[(kind,ref)]=prior[0] if prior else store.save_raw(c,'bigquery_bq_cli',route,record,record['completed_at_utc'],status=None)
            job=json.loads((d/m['job_capture']).read_text())['payload']
            if job['status']['state']!='DONE' or job['status'].get('errorResult'):raise ValueError('Query job failed')
            key=hashlib.sha256(_json({'project':m['project_id'],'job':m['job_id'],'location':m['location']}).encode()).hexdigest()
            c.execute('INSERT OR IGNORE INTO wallet_trace_discovery_collections VALUES (?,?,?,?,?,?,?,?,?,?,?)',(key,reviewed['fomo_user_id'],kind,m['project_id'],m['job_id'],m['window_start_utc'],m['window_end_utc'],m['total_rows'],'complete',query_ids[(kind,m['job_capture'])],_json(m)))
            offset=0
            for page in m['pages']:
                values=json.loads((d/page['capture']).read_text())['payload']
                if page['start_row']!=offset or page['row_count']!=len(values):raise ValueError('Non-contiguous query page')
                for row in values:
                    caution=['discovery_only_not_identity_or_ownership_evidence']
                    qty=int(row.get('quantity_raw') or '0')
                    if qty==0:caution.append('zero_value')
                    if row.get('error'):caution.append('failed_trace')
                    if kind=='tokens' and row['token_address'] not in ['0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48','0x75e2fc69ff2ac12af65ba7d321bbf4f878c535d2']:caution.append('token_contract_not_validated_in_this_slice')
                    if kind!='tokens' and 0<qty<=1000000000:caution.append('dust_not_strong_relationship_evidence')
                    c.execute('INSERT OR IGNORE INTO wallet_trace_discovery_rows VALUES (?,?,?,?,?)',(key,offset,_json(row),query_ids[(kind,page['capture'])],_json(caution)))
                    offset+=1
            if offset!=m['total_rows']:raise ValueError('Incomplete result rows')
        for a in reviewed['acquisitions']:
            key=hashlib.sha256(_json({k:a[k] for k in ['chain','address','tx','token_address']}).encode()).hexdigest()
            a['acquisition_key']=key
            for name in ['receipt','transaction','block']:a[name+'_raw_payload_id']=raw_ids[a[name+'_capture_file']]
            a['query_raw_payload_id']=query_ids[(a['query_kind'],a['query_capture_file'])]
            c.execute('INSERT OR IGNORE INTO wallet_trace_acquisitions VALUES ('+','.join('?' for _ in range(20))+')',([key,reviewed['fomo_user_id']]+[a[k] for k in ['chain','address','tx','at_utc','token_address','token_amount_raw','token_decimals','quote_asset','quote_supplied_raw','wrapped_weth_raw','network_fee_raw','evidence_status','ownership_status','receipt_raw_payload_id','transaction_raw_payload_id','block_raw_payload_id','query_raw_payload_id']]+[_json(a)]))
        reviewed['query_capture_raw_payload_ids']={kind:{ref:rid for (k,ref),rid in query_ids.items() if k==kind} for kind in ['tokens','native','traces']}
        report_id=store.save_raw(c,'cex_prebuy_review','/rank9/cex-prebuy',reviewed,reviewed['generated_at_utc'],status=None)
        state=dict(reviewed['frontier'],report_raw_payload_id=report_id)
        c.execute('UPDATE collector_state SET state_value=?,updated_at_utc=? WHERE state_key=?',(_json(state),utc_now(),'rzd_wallet_trace_v1'))
    report_path.write_text(_json(reviewed)+'\n')
    return dict(result,report_raw_payload_id=report_id,acquisitions=len(reviewed['acquisitions']),discovery_rows=sum(x['manifest']['total_rows'] for x in reviewed['discovery_collections']))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',type=Path,required=True);p.add_argument('--captures',type=Path,required=True);p.add_argument('--database',type=Path,required=True)
    a=p.parse_args();print(json.dumps(ingest(a.report,a.captures,a.database),indent=2))

if __name__=='__main__':main()
