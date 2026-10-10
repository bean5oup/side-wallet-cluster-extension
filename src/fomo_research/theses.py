"""Normalize retained THESIS evidence; never infer market cap, buys or ownership."""
import hashlib
import json
from datetime import datetime, timezone
from decimal import Decimal

from .store import _json, _timestamp, utc_now

SCHEMA = """
CREATE TABLE IF NOT EXISTS fomo_thesis_observations (
 thesis_key TEXT NOT NULL,
 raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
 source_locator TEXT NOT NULL, source_kind TEXT NOT NULL,
 provider_thesis_id TEXT, fomo_user_id TEXT NOT NULL REFERENCES traders(fomo_user_id),
 handle TEXT, chain TEXT NOT NULL, chain_id INTEGER,
 token_address TEXT NOT NULL, token_symbol TEXT,
 published_at_utc TEXT NOT NULL, source_timestamp_raw TEXT NOT NULL,
 trade_id TEXT, thesis_text TEXT NOT NULL, source_row_json TEXT NOT NULL,
 evidence_status TEXT NOT NULL, first_public_status TEXT NOT NULL,
 captured_at_utc TEXT NOT NULL,
 PRIMARY KEY(thesis_key,raw_payload_id,source_locator)
);
CREATE INDEX IF NOT EXISTS idx_theses_user_time
 ON fomo_thesis_observations(fomo_user_id,published_at_utc);
CREATE TABLE IF NOT EXISTS lowcap_thesis_screens (
 review_key TEXT NOT NULL, thesis_key TEXT NOT NULL,
 fomo_user_id TEXT NOT NULL REFERENCES traders(fomo_user_id),
 chain TEXT NOT NULL, token_address TEXT NOT NULL,
 threshold_usd TEXT NOT NULL, status TEXT NOT NULL, valuation_basis TEXT,
 market_cap_usd TEXT, fdv_proxy_usd TEXT, valuation_at_utc TEXT,
 historical_total_supply_raw TEXT, decimals INTEGER,
 source_refs_json TEXT NOT NULL, screen_json TEXT NOT NULL,
 review_raw_payload_id INTEGER NOT NULL REFERENCES raw_payloads(id),
 PRIMARY KEY(review_key,thesis_key)
);
"""

CHAINS = {1:'ethereum',56:'bsc',8453:'base',1399811149:'solana',4663:'robinhood',5042:'arc',143:'monad'}


def _observation(row, raw_id, locator, source_kind, captured, handles):
    user = row.get('userId')
    if not user or user not in handles:
        raise ValueError('THESIS author is absent from authorized cohort')
    token = row.get('token')
    token = token if isinstance(token,dict) else {'symbol':token,'address':row.get('tokenAddress')}
    address = token.get('address')
    chain_id = row.get('networkId') or row.get('chainId')
    chain = CHAINS.get(chain_id) or row.get('chain')
    raw_time, at = _timestamp(row.get('ts'))
    text = row.get('text')
    if not address or not chain or not at or not isinstance(text,str):
        raise ValueError('THESIS source lacks token, chain, source timestamp or text')
    if address.startswith('0x'):
        address=address.lower()
    if source_kind == 'retained_alert':
        marker=' posted a thesis on $' + str(token.get('symbol')) + ': '
        if marker in text:
            text=text.split(marker,1)[1]
    identity=[user,chain,address,at,row.get('tradeId'),text]
    key=hashlib.sha256(_json(identity).encode()).hexdigest()
    return [key,raw_id,locator,source_kind,row.get('id') or row.get('eventId'),user,
            handles[user],chain,chain_id,address,token.get('symbol'),at,raw_time,
            row.get('tradeId'),text,_json(row),'provider_publication_assertion',
            'earliest_retained_is_not_absolute_first',captured]


def import_saved_theses(store, page_raw_ids, cohort_raw_id, additional_user_ids=()):
    """Offline, idempotent observation ingestion, scoped to saved cohort + explicit users."""
    with store.connect() as c:
        c.executescript(SCHEMA)
        scope={r[0] for r in c.execute('SELECT fomo_user_id FROM leaderboard_snapshots WHERE raw_payload_id=? AND rank<=10',(cohort_raw_id,))}
        if len(scope)!=10:
            raise ValueError('Fixed Top 10 snapshot not found')
        scope.update(additional_user_ids)
        handles={r['fomo_user_id']:r['handle'] for r in c.execute('SELECT fomo_user_id,handle FROM traders') if r['fomo_user_id'] in scope}
        values=[]; pages=[]
        for raw_id in page_raw_ids:
            raw=c.execute('SELECT * FROM raw_payloads WHERE id=?',(raw_id,)).fetchone()
            if raw is None: raise ValueError('Missing raw THESIS page')
            payload=json.loads(raw['payload_json'])
            if payload.get('available') is False or raw['http_status']!=200:
                pages.append({'raw_payload_id':raw_id,'status':'unavailable','history_coverage':'unknown','reason':payload.get('reason')})
                continue
            if not isinstance(payload.get('theses'),list): raise ValueError('Missing THESIS list')
            for i,row in enumerate(payload['theses']):
                values.append(_observation(row,raw_id,'theses:'+str(i),'user_thesis_api',raw['captured_at_utc'],handles))
            pages.append({'raw_payload_id':raw_id,'status':'returned_list','received_rows':len(payload['theses']),'history_coverage':'unknown','has_more':payload.get('hasMore'),'cursor':payload.get('nextCursor')})
        query='SELECT * FROM fomo_events WHERE event_type=\'THESIS\' AND event_id_kind!=\'derived_thesis_document\' AND fomo_user_id IN ('+','.join('?' for _ in scope)+')'
        for event in c.execute(query,sorted(scope)):
            raw=c.execute('SELECT * FROM raw_payloads WHERE id=?',(event['raw_payload_id'],)).fetchone()
            payload=json.loads(raw['payload_json'])
            rows=payload if isinstance(payload,list) else payload.get('alerts',payload.get('events',[payload]))
            row=next((v for v in rows if (v.get('eventId') or v.get('id'))==event['event_id']),None)
            if row is None: raise ValueError('Cannot locate retained THESIS event in original raw')
            values.append(_observation(row,event['raw_payload_id'],'event:'+event['event_id'],'retained_alert',raw['captured_at_utc'],handles))
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
        return {'inserted_observations':inserted,'inserted_canonical_thesis_events':inserted_events,'imported_observations':len(values),'unique_retained_documents':len({v[0] for v in values}),'pages':pages,'scope_user_ids':sorted(scope)}


def last_closed_candle(payload, published_at_utc, token_address, maximum_age_seconds=300):
    """Reject the CALL's unfinished minute, even if before_timestamp returned it."""
    meta=payload.get('meta') or {}
    addresses=[(meta.get(k) or {}).get('address') for k in ('base','quote')]
    normalized=lambda v: v.lower() if isinstance(v,str) and v.startswith('0x') else v
    if normalized(token_address) not in [normalized(v) for v in addresses]:
        return None
    call=datetime.fromisoformat(published_at_utc.replace('Z','+00:00')).timestamp()
    rows=(payload.get('data') or {}).get('attributes',{}).get('ohlcv_list',[])
    valid=[r for r in rows if len(r)>=6 and int(r[0])+60<=call and 0<=call-(int(r[0])+60)<=maximum_age_seconds and Decimal(str(r[4]))>0]
    if not valid: return None
    row=max(valid,key=lambda r:int(r[0]))
    stamp=lambda t:datetime.fromtimestamp(t,timezone.utc).isoformat().replace('+00:00','Z')
    return {'open_at_utc':stamp(int(row[0])),'close_at_utc':stamp(int(row[0])+60),
            'open_usd':str(row[1]),'high_usd':str(row[2]),'low_usd':str(row[3]),
            'close_usd':str(row[4]),'volume_usd':str(row[5]),
            'lag_seconds':call-int(row[0])-60,'source':'geckoterminal_pool_ohlcv_assertion'}


def cap_band(amount):
    value=Decimal(str(amount))
    if value<30000:return 'below_30k'
    if value<200000:return '30k_to_200k'
    if value<1000000:return '200k_to_1m'
    if value<=10000000:return '1m_to_10m'
    return 'above_10m'


def save_screens(store, review, screens):
    """Append a versioned review; no existing funding or wallet-resolution table is changed."""
    at=utc_now()
    digest=hashlib.sha256(_json(review).encode()).hexdigest()
    with store.connect() as c:
        c.executescript(SCHEMA)
        prior=c.execute("SELECT id FROM raw_payloads WHERE source='lowcap_thesis_review' AND sha256=?",(digest,)).fetchone()
        raw_id=prior[0] if prior else store.save_raw(c,'lowcap_thesis_review','/offline/lowcap-thesis',review,at,status=None)
        key='lowcap-v1:'+digest
        for s in screens:
            values=[key,s['thesis_key'],s['fomo_user_id'],s['chain'],s['token_address'],'10000000',s['status'],s.get('valuation_basis'),s.get('market_cap_usd'),s.get('fdv_proxy_usd'),s.get('valuation_at_utc'),s.get('historical_total_supply_raw'),s.get('decimals'),_json(s['source_refs']),_json(s),raw_id]
            c.execute('INSERT OR IGNORE INTO lowcap_thesis_screens VALUES ('+','.join('?' for _ in values)+')',values)
        return {'review_key':key,'review_raw_payload_id':raw_id,'screen_rows':len(screens)}
