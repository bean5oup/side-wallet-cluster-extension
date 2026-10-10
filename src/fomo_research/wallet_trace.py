"""Offline ingestion of reviewed wallet tracing evidence; adds no network calls."""
import argparse
import hashlib
import json
from pathlib import Path
from .store import Store, _json, utc_now
from .config import DEFAULT_DATABASE

SCHEMA = """
CREATE TABLE IF NOT EXISTS wallet_trace_edges (
 edge_key TEXT PRIMARY KEY,
 fomo_user_id TEXT NOT NULL REFERENCES traders(fomo_user_id),
 rank INTEGER NOT NULL,
 edge_type TEXT NOT NULL CHECK(edge_type IN ('TRANSFER','BRIDGE')),
 evidence_status TEXT NOT NULL,
 ownership_status TEXT NOT NULL CHECK(ownership_status='unknown'),
 from_chain TEXT NOT NULL, from_address TEXT NOT NULL, from_tx TEXT NOT NULL,
 from_locator TEXT NOT NULL, from_at_utc TEXT NOT NULL,
 from_asset TEXT NOT NULL, from_amount_raw TEXT NOT NULL, from_decimals INTEGER,
 to_chain TEXT NOT NULL, to_address TEXT NOT NULL, to_tx TEXT NOT NULL,
 to_locator TEXT NOT NULL, to_at_utc TEXT NOT NULL,
 to_asset TEXT NOT NULL, to_amount_raw TEXT NOT NULL, to_decimals INTEGER,
 from_raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
 to_raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
 provider_raw_payload_id INTEGER REFERENCES raw_payloads(id),
 scope_context TEXT NOT NULL,
 evidence_json TEXT NOT NULL,
 first_recorded_at_utc TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_trace_from ON wallet_trace_edges(from_chain,from_address,from_at_utc);
CREATE INDEX IF NOT EXISTS idx_trace_to ON wallet_trace_edges(to_chain,to_address,to_at_utc);
"""

def import_report(report_path, capture_directory, database):
    """Persist reviewed evidence. This importer does not establish blockchain truth."""
    report = json.loads(Path(report_path).read_text())
    store = Store(database)
    raw_ids = {}
    with store.connect() as c:
        c.executescript(SCHEMA)
        for path in sorted(Path(capture_directory).glob('*.json')):
            record = json.loads(path.read_text())
            if 'request' not in record or 'response' not in record:
                continue
            # RPC records must not retain credential URLs.
            if record.get('provider') and 'url' in record:
                raise ValueError('RPC capture contains a URL; redact at capture time')
            source = record.get('provider') or 'local_bridge_api'
            route = record.get('route') or '/v1/bridge/resolve-transaction'
            digest = hashlib.sha256(_json(record).encode()).hexdigest()
            row = c.execute('SELECT id FROM raw_payloads WHERE source=? AND route=? AND sha256=?', (source,route,digest)).fetchone()
            raw_ids[path.name] = row[0] if row else store.save_raw(c,source,route,record,record['completed_at'],status=record.get('http_status'))
        for edge in report['edges']:
            source, destination = edge['source'], edge['destination']
            def ref(leg):
                raw_id = leg.get('raw_payload_id') or raw_ids[leg['capture_file']]
                if not c.execute('SELECT 1 FROM raw_payloads WHERE id=?',(raw_id,)).fetchone():
                    raise ValueError('Missing source evidence')
                return raw_id
            provider_id = raw_ids[edge['provider_capture_file']] if edge.get('provider_capture_file') else None
            identity = {k:edge[k] for k in ['edge_type','source','destination']}
            for leg in ['source','destination']:
                identity[leg] = {k:identity[leg][k] for k in ['chain','address','tx','locator','asset']}
            key = hashlib.sha256(_json(identity).encode()).hexdigest()
            edge['edge_key'] = key
            edge['source']['raw_payload_id'],edge['destination']['raw_payload_id'] = ref(source),ref(destination)
            edge['provider_raw_payload_id'] = provider_id
            values = [key,report['fomo_user_id'],report['rank'],edge['edge_type'],edge['evidence_status'],'unknown']
            for leg in [source,destination]:
                values.extend(leg[k] for k in ['chain','address','tx','locator','at_utc','asset','amount_raw','decimals'])
            values.extend([source['raw_payload_id'],destination['raw_payload_id'],provider_id,edge['scope_context'],_json(edge.get('evidence',{})),report['generated_at_utc']])
            c.execute('INSERT OR IGNORE INTO wallet_trace_edges VALUES ('+','.join('?' for _ in values)+')', values)
        report['capture_raw_payload_ids'] = raw_ids
        digest = hashlib.sha256(_json(report).encode()).hexdigest()
        old = c.execute("SELECT id FROM raw_payloads WHERE source='wallet_trace_review' AND sha256=?",(digest,)).fetchone()
        report_id = old[0] if old else store.save_raw(c,'wallet_trace_review','/rank9/relay-funder-continuation',report,report['generated_at_utc'],status=None)
        state = dict(report['frontier'],report_raw_payload_id=report_id)
        c.execute('INSERT INTO collector_state VALUES (?,?,?) ON CONFLICT(state_key) DO UPDATE SET state_value=excluded.state_value,updated_at_utc=excluded.updated_at_utc',('rzd_wallet_trace_v1',_json(state),utc_now()))
    return {'report_raw_payload_id':report_id,'reviewed_edges':len(report['edges']),'capture_count':len(raw_ids)}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--report',type=Path,required=True)
    p.add_argument('--captures',type=Path,required=True)
    p.add_argument('--database',type=Path,default=DEFAULT_DATABASE)
    a=p.parse_args()
    print(json.dumps(import_report(a.report,a.captures,a.database),indent=2))

if __name__=='__main__': main()
