"""Rebuild rank-9 owner/event evidence from retained SQLite sources only."""

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .bigquery import _write
from .bigquery_solana import parse_wallet_row
from .config import DEFAULT_DATABASE
from .research import CLASSIFICATION_VERSION, build_top_solana_timeline
from .store import Store, _json, utc_now

SCHEMA = """
CREATE TABLE IF NOT EXISTS bigquery_solana_event_windows (
    collection_key TEXT NOT NULL REFERENCES bigquery_solana_collections(collection_key),
    event_id TEXT NOT NULL REFERENCES fomo_events(event_id),
    wallet TEXT NOT NULL,
    token_address TEXT NOT NULL,
    event_type TEXT NOT NULL,
    fomo_at_utc TEXT NOT NULL,
    prior_window_start_utc TEXT NOT NULL,
    following_window_end_utc TEXT NOT NULL,
    prior_window_within_query_scope INTEGER NOT NULL,
    following_window_within_query_scope INTEGER NOT NULL,
    prior_24h_buy_count INTEGER NOT NULL,
    following_24h_sell_count INTEGER NOT NULL,
    first_observed_buy_in_query_at_utc TEXT,
    nearest_prior_buy_at_utc TEXT,
    first_following_sell_at_utc TEXT,
    buy_to_fomo_seconds INTEGER,
    evidence_json TEXT NOT NULL,
    generated_at_utc TEXT NOT NULL,
    PRIMARY KEY(collection_key,event_id)
);
CREATE TABLE IF NOT EXISTS bigquery_solana_analyses (
    collection_key TEXT PRIMARY KEY REFERENCES bigquery_solana_collections(collection_key),
    analysis_version TEXT NOT NULL,
    report_json TEXT NOT NULL,
    generated_at_utc TEXT NOT NULL
);
"""


def _dt(stamp):
    return datetime.fromisoformat(stamp.replace('Z', '+00:00'))


def _utc(stamp):
    return stamp.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')


def build(database):
    normalization = build_top_solana_timeline(database, rank_limit=10)
    store = Store(database)
    with store.connect() as connection:
        connection.executescript(SCHEMA)
        collection = connection.execute(
            "SELECT * FROM bigquery_solana_collections WHERE role='owner_details' AND retrieval_status='complete' ORDER BY imported_at_utc DESC LIMIT 1"
        ).fetchone()
        if not collection:
            raise ValueError('A complete owner balance collection is required')
        key, wallet, user = collection['collection_key'], collection['wallet'], collection['fomo_user_id']
        scope = json.loads(collection['scope_json'])
        start, end = _dt(scope['window_start_utc']), _dt(scope['window_end_utc'])
        indexed = [dict(r) for r in connection.execute('SELECT * FROM bigquery_solana_transactions WHERE collection_key=? ORDER BY block_time_utc,signature', (key,))]
        actions = {r['signature']: dict(r) for r in connection.execute(
            "SELECT * FROM solana_normalized_actions WHERE leaderboard_captured_at_utc=? AND wallet=? AND fomo_user_id=?",
            (scope['leaderboard_snapshot_at_utc'],wallet,user),
        )}
        token_actions = defaultdict(list)
        for row in connection.execute(
            "SELECT a.signature,a.block_time_utc,a.action_type,a.transaction_successful,a.raw_source,a.raw_payload_id,"
            "d.token_address,d.delta_raw,d.token_decimals,d.swap_side "
            "FROM solana_normalized_actions a JOIN solana_action_token_deltas d "
            "ON d.leaderboard_captured_at_utc=a.leaderboard_captured_at_utc AND d.signature=a.signature AND d.wallet=a.wallet "
            "WHERE a.leaderboard_captured_at_utc=? AND a.wallet=? AND a.fomo_user_id=? "
            "AND a.block_time_utc>=? AND a.block_time_utc<? ORDER BY a.block_time_utc,a.signature",
            (scope['leaderboard_snapshot_at_utc'],wallet,user,scope['window_start_utc'],scope['window_end_utc']),
        ):
            token_actions[row['token_address']].append(dict(row))
        events = [dict(r) for r in connection.execute(
            "SELECT event_id,event_type,token_address,token_symbol,source_at_utc FROM fomo_events "
            "WHERE fomo_user_id=? AND lower(chain)='solana' AND source_at_utc>=? AND source_at_utc<? ORDER BY source_at_utc,event_id",
            (user,scope['window_start_utc'],scope['window_end_utc']),
        )]
        tracked_mints = {e['token_address'] for e in events} | {'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'}
        changed, unchanged, failed, semantic_missing, relevant_missing = [], 0, 0, [], []
        indexed_by_mint = defaultdict(list)
        for row in indexed:
            parsed = parse_wallet_row(json.loads(row['row_json']),wallet)
            if not parsed['successful']:
                failed += 1
            if not parsed['token_deltas']:
                unchanged += 1
                continue
            changed.append(row['signature'])
            for delta in parsed['token_deltas']:
                indexed_by_mint[delta['token_address']].append({'signature':row['signature'],'at_utc':row['block_time_utc'],
                                                              'successful':parsed['successful'],**delta})
            if row['signature'] not in actions:
                semantic_missing.append(row['signature'])
                if parsed['successful'] and any(d['token_address'] in tracked_mints for d in parsed['token_deltas']):
                    relevant_missing.append(row['signature'])
        generated = utc_now()
        window_rows = []
        for event in events:
            stamp = _dt(event['source_at_utc'])
            left, right = stamp - timedelta(hours=24), stamp + timedelta(hours=24)
            movements = token_actions.get(event['token_address'], [])
            buys = [m for m in movements if m['transaction_successful'] and m['action_type']=='SWAP' and m['swap_side']=='BUY']
            sells = [m for m in movements if m['transaction_successful'] and m['action_type']=='SWAP' and m['swap_side']=='SELL']
            prior = [m for m in buys if left <= _dt(m['block_time_utc']) < stamp]
            after = [m for m in sells if stamp < _dt(m['block_time_utc']) <= right]
            nearest = prior[-1] if prior else None
            first_after = after[0] if after else None
            owner_rows = [m for m in indexed_by_mint.get(event['token_address'], []) if left <= _dt(m['at_utc']) <= right]
            unresolved = [m for m in owner_rows if m['successful'] and
                          (m['signature'] not in actions or actions[m['signature']]['action_type']=='UNKNOWN')]
            evidence = {'token_symbol':event['token_symbol'],'prior_buys':prior,'following_sells':after,
                        'observed_owner_token_deltas_in_window':owner_rows,'unclassified_owner_deltas_in_window':unresolved,
                        'classification':'provisional transaction-level swap/log and opposing-balance heuristic',
                        'history_coverage':'indexed owner history completeness unknown; window flags describe time scope only'}
            item = {'collection_key':key,'event_id':event['event_id'],'wallet':wallet,'token_address':event['token_address'],
                    'event_type':event['event_type'],'fomo_at_utc':event['source_at_utc'],'prior_window_start_utc':_utc(left),
                    'following_window_end_utc':_utc(right),'prior_window_within_query_scope':int(left >= start),
                    'following_window_within_query_scope':int(right <= end),'prior_24h_buy_count':len(prior),
                    'following_24h_sell_count':len(after),'first_observed_buy_in_query_at_utc':buys[0]['block_time_utc'] if buys else None,
                    'nearest_prior_buy_at_utc':nearest['block_time_utc'] if nearest else None,
                    'first_following_sell_at_utc':first_after['block_time_utc'] if first_after else None,
                    'buy_to_fomo_seconds':int((stamp-_dt(nearest['block_time_utc'])).total_seconds()) if nearest else None,
                    'evidence_json':_json(evidence),'generated_at_utc':generated}
            columns = list(item)
            connection.execute('INSERT INTO bigquery_solana_event_windows (' + ','.join(columns) + ') VALUES (' + ','.join('?' for _ in columns) + ') '
                               'ON CONFLICT(collection_key,event_id) DO UPDATE SET ' + ','.join(c+'=excluded.'+c for c in columns if c not in ('collection_key','event_id')),
                               tuple(item[c] for c in columns))
            window_rows.append({k:v for k,v in item.items() if k!='evidence_json'} | {'token_symbol':event['token_symbol'],
                                'unclassified_owner_delta_count':len(unresolved)})
        tokens = []
        for mint in sorted({e['token_address'] for e in events}):
            rows = token_actions[mint]
            buys = [r for r in rows if r['action_type']=='SWAP' and r['swap_side']=='BUY' and r['transaction_successful']]
            sells = [r for r in rows if r['action_type']=='SWAP' and r['swap_side']=='SELL' and r['transaction_successful']]
            tokens.append({'mint':mint,'symbol':next((e['token_symbol'] for e in events if e['token_address']==mint),None),
                           'observed_swap_buys_in_query':len(buys),'observed_swap_sells_in_query':len(sells),
                           'first_buy_in_query_at_utc':buys[0]['block_time_utc'] if buys else None,
                           'first_sell_in_query_at_utc':sells[0]['block_time_utc'] if sells else None,
                           'owner_delta_rows_in_query':len(indexed_by_mint[mint]),
                           'fomo_events':[w for w in window_rows if w['token_address']==mint]})
        jobs = [dict(r) for r in connection.execute(
            'SELECT collection_key,role,job_id,bytes_processed,bytes_billed,total_rows,fetched_rows,report_json FROM bigquery_solana_collections WHERE case_key=? ORDER BY imported_at_utc',
            (scope['case_key'],),
        )]
        bridge_report = next(json.loads(r['report_json']) for r in jobs if r['role']=='known_receipts')
        selected_bridge_checks = bridge_report['bridge_comparisons']
        billed = sum(int(r['bytes_billed']) for r in jobs)
        rpc_counts = dict(Counter(r[0] for r in connection.execute('SELECT status FROM bigquery_solana_rpc_checks WHERE collection_key=?',(key,))))
        report = {'analysis_version':'solana_owner_events_v1','classification_version':CLASSIFICATION_VERSION,'generated_at_utc':generated,'scope':scope,'collection_key':key,
                  'owner_rows':len(indexed),'owner_rows_with_nonzero_token_delta':len(changed),'owner_rows_without_net_token_delta':unchanged,
                  'failed_owner_rows':failed,'rpc_status_counts':rpc_counts,'unclassified_changed_rows_without_rpc_count':len(semantic_missing),
                  'unclassified_relevant_rows_without_rpc':relevant_missing,'fomo_event_count':len(events),'event_windows':window_rows,
                  'token_timelines':tokens,'bridge_comparisons':selected_bridge_checks,
                  'normalized_rzd_action_count':len(actions),'normalized_rzd_action_counts':dict(Counter(r['action_type'] for r in actions.values())),
                  'normalization_summary':normalization,'solana_bigquery_billed_bytes':str(billed),
                  'reference_usd_at_6_25_per_TiB':round(billed/1024**4*6.25,4),
                  'jobs':[{k:v for k,v in j.items() if k!='report_json'} for j in jobs],
                  'limits':['complete query retrieval does not prove complete chain history',
                            'native-only transactions and missing owner metadata are outside owner discovery',
                            'balance-only rows retain unknown signer and trade semantics',
                            'full owner RPC pages recover nonzero indexed token movements; classification remains provisional',
                            'transfers and chronological receipt/buy ordering do not prove common ownership or unique use of funds',
                            'pre-call timing in the verified wallet does not identify a secondary wallet',
                            'quote attribution, fee configuration, opening lots and cost basis are required before PnL']}
        connection.execute('INSERT INTO bigquery_solana_analyses VALUES (?,?,?,?) ON CONFLICT(collection_key) DO UPDATE SET '
                           'analysis_version=excluded.analysis_version,report_json=excluded.report_json,generated_at_utc=excluded.generated_at_utc',
                           (key,report['analysis_version'],_json(report),generated))
    path = store.database.parent / 'rank9-solana-owner-analysis.json'
    _write(path, report)
    return report | {'report_path':str(path)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database',default=str(DEFAULT_DATABASE))
    args = parser.parse_args()
    report = build(args.database)
    print(json.dumps({k:report[k] for k in ('collection_key','owner_rows','owner_rows_with_nonzero_token_delta','owner_rows_without_net_token_delta',
                     'failed_owner_rows','rpc_status_counts','unclassified_changed_rows_without_rpc_count','fomo_event_count','normalized_rzd_action_count',
                     'normalized_rzd_action_counts','solana_bigquery_billed_bytes','reference_usd_at_6_25_per_TiB','report_path')},indent=2))


if __name__=='__main__':
    main()
