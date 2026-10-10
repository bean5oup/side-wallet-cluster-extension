"""Frozen-cohort ingestion using the existing THESIS schema and observation semantics.

Legacy Top10 import and $10M reviews remain in theses.py. This entry point requires
explicit authors and an explicit screening threshold for the Top100 workflow.
"""
import hashlib
import json
from datetime import datetime
from .store import _json, utc_now
from .theses import SCHEMA, _observation

def import_saved_theses(store, page_raw_ids, cohort_raw_id, additional_user_ids=(),
                        authorized_user_ids=None, start_at_utc=None, end_at_utc=None,
                        strict=True):
    """Offline, idempotent observation ingestion, scoped to saved cohort + explicit users."""
    with store.connect() as c:
        c.executescript(SCHEMA)
        if authorized_user_ids is None or additional_user_ids:
            raise ValueError('Frozen-cohort ingestion requires explicit authorized users')
        frozen={r[0] for r in c.execute('SELECT fomo_user_id FROM leaderboard_snapshots WHERE raw_payload_id=?',(cohort_raw_id,))}
        scope=set(authorized_user_ids)
        if not scope or not scope.issubset(frozen):
            raise ValueError('Explicit authors must belong to the fixed snapshot')
        handles={r['fomo_user_id']:r['handle'] for r in c.execute('SELECT fomo_user_id,handle FROM traders') if r['fomo_user_id'] in scope}
        values=[]; pages=[]; rejected=[]
        start=datetime.fromisoformat(start_at_utc.replace('Z','+00:00')) if start_at_utc else None
        end=datetime.fromisoformat(end_at_utc.replace('Z','+00:00')) if end_at_utc else None
        def append_observation(row, raw_id, locator, kind, captured):
            try:
                value=_observation(row,raw_id,locator,kind,captured,handles)
                at=datetime.fromisoformat(value[11].replace('Z','+00:00'))
                if (start and at<start) or (end and at>=end):
                    return
                values.append(value)
            except (ValueError,TypeError,AttributeError) as error:
                if strict:
                    raise
                rejected.append({'raw_payload_id':raw_id,'locator':locator,'reason':str(error)})
        for raw_id in page_raw_ids:
            raw=c.execute('SELECT * FROM raw_payloads WHERE id=?',(raw_id,)).fetchone()
            if raw is None: raise ValueError('Missing raw THESIS page')
            payload=json.loads(raw['payload_json'])
            if payload.get('available') is False or raw['http_status']!=200:
                pages.append({'raw_payload_id':raw_id,'status':'unavailable','history_coverage':'unknown','reason':payload.get('reason')})
                continue
            if not isinstance(payload.get('theses'),list): raise ValueError('Missing THESIS list')
            for i,row in enumerate(payload['theses']):
                append_observation(row,raw_id,'theses:'+str(i),'user_thesis_api',raw['captured_at_utc'])
            pages.append({'raw_payload_id':raw_id,'status':'returned_list','received_rows':len(payload['theses']),'history_coverage':'unknown','has_more':payload.get('hasMore'),'cursor':payload.get('nextCursor')})
        query='SELECT * FROM fomo_events WHERE event_type=\'THESIS\' AND event_id_kind!=\'derived_thesis_document\' AND fomo_user_id IN ('+','.join('?' for _ in scope)+')'
        for event in c.execute(query,sorted(scope)):
            raw=c.execute('SELECT * FROM raw_payloads WHERE id=?',(event['raw_payload_id'],)).fetchone()
            payload=json.loads(raw['payload_json'])
            rows=payload if isinstance(payload,list) else payload.get('alerts',payload.get('events',[payload]))
            row=next((v for v in rows if (v.get('eventId') or v.get('id'))==event['event_id']),None)
            if row is None:
                if strict:
                    raise ValueError('Cannot locate retained THESIS event in original raw')
                rejected.append({'raw_payload_id':event['raw_payload_id'],'locator':'event:'+event['event_id'],'reason':'Cannot locate retained THESIS event in original raw'})
                continue
            append_observation(row,event['raw_payload_id'],'event:'+event['event_id'],'retained_alert',raw['captured_at_utc'])
        inserted=0
        for value in values:
            prior=c.execute('SELECT source_row_json FROM fomo_thesis_observations WHERE thesis_key=? AND raw_payload_id=? AND source_locator=?',value[:3]).fetchone()
            if prior and prior[0]!=value[15]: raise ValueError('Conflicting immutable source observation')
            if not prior:
                c.execute('INSERT INTO fomo_thesis_observations VALUES ('+','.join('?' for _ in value)+')',value)
                inserted+=1
        # THESIS post observations also belong in the canonical event timeline.
        # A derived document key is explicitly labelled; it is never a claimed native alert ID.
        # Native alert checkpoints are unaffected by this separate historical source.
        alert_keys={v[0] for v in values if v[3]=='retained_alert'}
        inserted_events=0
        for v in values:
            if v[3]!='user_thesis_api' or v[0] in alert_keys:
                continue
            cursor=c.execute('''INSERT OR IGNORE INTO fomo_events
              (event_id,event_id_kind,fomo_user_id,handle,event_type,chain,chain_id,
               token_address,token_symbol,source_timestamp_raw,source_at_utc,
               amount_usd,trade_id,captured_at_utc,raw_payload_id)
              VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
              ['thesis_doc_'+v[0],'derived_thesis_document',v[5],v[6],'THESIS',v[7],v[8],
               v[9],v[10],v[12],v[11],None,v[13],v[18],v[1]])
            inserted_events+=cursor.rowcount
        return {'inserted_observations':inserted,'inserted_canonical_thesis_events':inserted_events,'imported_observations':len(values),'unique_retained_documents':len({v[0] for v in values}),'pages':pages,'scope_user_ids':sorted(scope),'rejected_rows':rejected}


def save_screens(store, review, screens, threshold_usd):
    """Append a versioned review; no existing funding or wallet-resolution table is changed."""
    at=utc_now()
    digest=hashlib.sha256(_json(review).encode()).hexdigest()
    with store.connect() as c:
        c.executescript(SCHEMA)
        prior=c.execute("SELECT id FROM raw_payloads WHERE source='lowcap_thesis_review' AND sha256=?",(digest,)).fetchone()
        raw_id=prior[0] if prior else store.save_raw(c,'lowcap_thesis_review','/offline/lowcap-thesis',review,at,status=None)
        key='lowcap-v1:'+digest
        for s in screens:
            values=[key,s['thesis_key'],s['fomo_user_id'],s['chain'],s['token_address'],str(threshold_usd),s['status'],s.get('valuation_basis'),s.get('market_cap_usd'),s.get('fdv_proxy_usd'),s.get('valuation_at_utc'),s.get('historical_total_supply_raw'),s.get('decimals'),_json(s['source_refs']),_json(s),raw_id]
            c.execute('INSERT OR IGNORE INTO lowcap_thesis_screens VALUES ('+','.join('?' for _ in values)+')',values)
        return {'review_key':key,'review_raw_payload_id':raw_id,'screen_rows':len(screens)}
