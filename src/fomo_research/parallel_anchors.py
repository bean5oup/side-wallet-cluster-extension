"""Build THESIS and independent BUY screening anchors from retained evidence only."""
import argparse
import hashlib
import json
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from .config import DEFAULT_DATABASE, REPO_ROOT
from .store import Store, _json, utc_now


def moment(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('Anchor timestamps require a UTC offset')
    return parsed.astimezone(timezone.utc)


def token_identity(row):
    address = row['token_address']
    if not row['chain'] or not address:
        raise ValueError('Anchor lacks an exact chain/token identity')
    return row['chain'], address.lower() if address.startswith('0x') else address



def apply_retained_buy_reviews(anchors, reviews, policy):
    """Reuse additive primary reviews without replacing source clocks or ownership."""
    by_key = {a['anchor_key']: a for a in anchors if a['anchor_type'] == 'BUY'}
    fields = ('actual_swap_at_utc', 'actual_swap_review_status', 'actual_swap_evidence_refs',
              'public_visibility_at_utc', 'public_visibility_status', 'cap_status',
              'market_cap_usd', 'valuation_at_utc', 'cap_evidence_refs', 'cap_gap',
              'cap_sample_lag_seconds', 'historical_price_proxy', 'token_delivery_proof',
              'receipt_backed_token_at_utc', 'economic_quote_attribution_status')
    applied = set()
    for raw_id, review in reviews:
        if review.get('policy_version') != policy['policy_version']:
            continue
        if review.get('cohort') != policy['cohort'] or review.get('historical_window') != policy['historical_window']:
            continue
        if review.get('primary_review_status') != 'reviewed':
            continue
        if review.get('cap_threshold_usd') != policy['token_gate']['max_usd_inclusive']:
            continue
        for row in review.get('anchor_reviews', []):
            anchor = by_key.get(row.get('anchor_key'))
            if not anchor:
                continue
            identity = ('fomo_event_id', 'fomo_user_id', 'chain', 'token_address', 'fomo_buy_source_at_utc')
            if any(row.get(k) != anchor[k] for k in identity):
                raise ValueError('Retained BUY review conflicts with source identity')
            status = row.get('cap_status')
            if status not in policy['token_gate']['statuses']:
                raise ValueError('Retained BUY review has an invalid cap status')
            if status in ('eligible', 'excluded_above_cap'):
                if row.get('actual_swap_review_status') != 'verified' or not row.get('actual_swap_evidence_refs'):
                    raise ValueError('BUY cap decision requires a reviewed actual swap')
                actual_at = moment(row['actual_swap_at_utc'])
                value_at = moment(row['valuation_at_utc'])
                age = (actual_at - value_at).total_seconds()
                value = Decimal(row['market_cap_usd'])
                maximum = Decimal(policy['token_gate']['max_usd_inclusive'])
                if value <= 0 or not 0 <= age <= policy['token_gate']['sample_max_age_seconds_working_assumption']:
                    raise ValueError('BUY cap sample is invalid for the actual clock')
                if (value <= maximum) != (status == 'eligible'):
                    raise ValueError('BUY cap decision conflicts with its value')
            for field in fields:
                if field in row:
                    anchor[field] = row[field]
            anchor['cap_review_raw_payload_id'] = raw_id
            anchor['primary_buy_review_raw_payload_id'] = raw_id
            if anchor['actual_swap_review_status'] == 'verified':
                if not anchor.get('actual_swap_at_utc') or not anchor.get('actual_swap_evidence_refs'):
                    raise ValueError('Verified BUY lacks its actual clock or evidence')
                anchor['reference_at_utc'] = anchor['actual_swap_at_utc']
                anchor['reference_time_basis'] = 'reviewed_actual_wallet_swap'
            applied.add(anchor['anchor_key'])
    return len(applied)


def build_inventory(database, policy):
    """Retain every BUY even when this trader or the cohort has no retained THESIS."""
    window = policy['historical_window']
    start, end = moment(window['start_utc_inclusive']), moment(window['end_utc_exclusive'])
    if (end - start).total_seconds() != 5184000:
        raise ValueError('The frozen research window must be exactly 60 days')
    if 'BUY' not in policy['token_gate'].get('anchor_types', []):
        raise ValueError('The current policy must explicitly authorize BUY anchors')
    with sqlite3.connect(Path(database).resolve().as_uri() + '?mode=ro', uri=True) as c:
        c.row_factory = sqlite3.Row
        users = {r['fomo_user_id']: dict(r) for r in c.execute('''
            SELECT l.rank,l.fomo_user_id,t.handle FROM leaderboard_snapshots l
            JOIN traders t USING(fomo_user_id)
            WHERE l.raw_payload_id=? AND l.period=? AND l.rank BETWEEN 1 AND 100
            ORDER BY l.rank''', (policy['cohort']['leaderboard_raw_payload_id'], policy['cohort']['period']))}
        if len(users) != 100 or {u['rank'] for u in users.values()} != set(range(1, 101)):
            raise ValueError('The frozen Top100 must contain 100 distinct users and ranks')
        def retained(row, time_field):
            return row['fomo_user_id'] in users and row[time_field] and start <= moment(row[time_field]) < end
        events = [dict(r) for r in c.execute('SELECT * FROM fomo_events') if retained(r, 'source_at_utc')]
        observations = [dict(r) for r in c.execute('SELECT * FROM fomo_thesis_observations') if retained(r, 'published_at_utc')]
        matched = defaultdict(list)
        for r in c.execute('''SELECT m.fomo_event_id,m.match_status,m.signature,
                t.chain,t.wallet,t.side,t.block_time_utc,t.token_address,t.raw_payload_id,
                t.quote_asset_address,t.quote_amount_raw
                FROM event_trade_matches m JOIN onchain_trades t USING(signature)'''):
            matched[r['fomo_event_id']].append(dict(r))
        screens = {}
        for r in c.execute('SELECT * FROM lowcap_thesis_screens WHERE threshold_usd=? ORDER BY review_raw_payload_id',
                           (policy['token_gate']['max_usd_inclusive'],)):
            screens[r['thesis_key']] = dict(r)
        retained_buy_reviews = [(r['id'], json.loads(r['payload_json'])) for r in c.execute(
            "SELECT id,payload_json FROM raw_payloads WHERE source='top100_buy_anchor_review' ORDER BY id")]

    documents = {}
    for o in observations:
        documents.setdefault(o['thesis_key'], dict(o, source_refs=[]))['source_refs'].append(
            {'raw_payload_id': o['raw_payload_id'], 'source_locator': o['source_locator']})
    token_docs, author_docs, sells = defaultdict(list), defaultdict(list), defaultdict(list)
    for o in documents.values():
        key = token_identity(o)
        token_docs[key].append(o)
        author_docs[(o['fomo_user_id'],) + key].append(o)
    for e in events:
        if e['event_type'] == 'SELL':
            sells[(e['fomo_user_id'],) + token_identity(e)].append(e['event_id'])

    anchors, gaps = [], []
    for o in documents.values():
        chain, address = token_identity(o)
        screen = screens.get(o['thesis_key'])
        if screen and moment(json.loads(screen['screen_json'])['published_at_utc']) != moment(o['published_at_utc']):
            screen = None
        anchors.append({'anchor_key': 'thesis:' + o['thesis_key'], 'anchor_type': 'THESIS',
            'thesis_key': o['thesis_key'], 'fomo_user_id': o['fomo_user_id'],
            'handle': users[o['fomo_user_id']]['handle'], 'rank': users[o['fomo_user_id']]['rank'],
            'chain': chain, 'chain_id': o['chain_id'], 'token_address': address, 'token_symbol': o['token_symbol'],
            'reference_at_utc': o['published_at_utc'], 'reference_time_basis': 'thesis_published_at',
            'earliest_public_status': 'retained_record_not_absolute_first', 'source_refs': o['source_refs'],
            'cap_status': screen['status'] if screen else 'pending_cap',
            'cap_review_raw_payload_id': screen['review_raw_payload_id'] if screen else None,
            'cap_threshold_usd': policy['token_gate']['max_usd_inclusive'],
            'market_cap_usd': screen['market_cap_usd'] if screen else None,
            'valuation_at_utc': screen['valuation_at_utc'] if screen else None,
            'cap_evidence_refs': json.loads(screen['source_refs_json']) if screen else []})
    for e in events:
        if e['event_type'] != 'BUY':
            continue
        try:
            chain, address = token_identity(e)
        except ValueError as error:
            gaps.append({'event_id': e['event_id'], 'reason': str(error)})
            continue
        own_docs = author_docs[(e['fomo_user_id'], chain, address)]
        own_keys = [o['thesis_key'] for o in own_docs]
        refs = [r for r in matched[e['event_id']] if token_identity(r) == (chain, address)]
        # A verified event/token match is not automatically a fully proven economic BUY.
        # All BUY clocks remain provisional until the actual swap and owner are reviewed.
        anchors.append({'anchor_key': 'buy:' + e['event_id'], 'anchor_type': 'BUY',
            'fomo_event_id': e['event_id'], 'trade_id': e['trade_id'], 'fomo_user_id': e['fomo_user_id'],
            'handle': users[e['fomo_user_id']]['handle'], 'rank': users[e['fomo_user_id']]['rank'],
            'chain': chain, 'chain_id': e['chain_id'], 'token_address': address, 'token_symbol': e['token_symbol'],
            'reference_at_utc': e['source_at_utc'], 'reference_time_basis': 'fomo_reported_buy_time_pending_swap_review',
            'fomo_buy_source_at_utc': e['source_at_utc'], 'captured_at_utc': e['captured_at_utc'],
            'actual_swap_at_utc': None, 'actual_swap_review_status': 'pending', 'actual_swap_evidence_refs': [],
            'public_visibility_at_utc': None, 'public_visibility_status': 'unknown',
            'source_refs': [{'raw_payload_id': e['raw_payload_id'], 'source_locator': 'event:' + e['event_id']}],
            'onchain_match_refs': refs, 'same_author_retained_thesis_keys': own_keys,
            'same_author_thesis_before_buy_keys': [o['thesis_key'] for o in own_docs if moment(o['published_at_utc']) < moment(e['source_at_utc'])],
            'cohort_retained_thesis_keys': [o['thesis_key'] for o in token_docs[(chain, address)]],
            'no_retained_thesis_by_same_author': not own_keys,
            'no_retained_thesis_in_cohort': not token_docs[(chain, address)],
            'same_author_retained_sell_event_ids': sells[(e['fomo_user_id'], chain, address)],
            'cap_status': 'pending_cap', 'cap_threshold_usd': policy['token_gate']['max_usd_inclusive'],
            'market_cap_usd': None, 'valuation_at_utc': None, 'cap_evidence_refs': [],
            'cap_gap': 'historical_circulating_cap_at_BUY_not_reviewed'})
    applied_buy_reviews = apply_retained_buy_reviews(anchors, retained_buy_reviews, policy)
    discovery = policy['discovery_windows_working_assumptions']
    for a in anchors:
        at = moment(a['reference_at_utc'])
        a['provisional_discovery_window'] = {
            'start_utc_inclusive': max(start, at - timedelta(seconds=discovery['pre_public_seconds'])).isoformat().replace('+00:00', 'Z'),
            'end_utc_exclusive': min(end, at + timedelta(seconds=discovery['post_public_seconds'])).isoformat().replace('+00:00', 'Z'),
            'exit_end_utc_exclusive': min(end, at + timedelta(seconds=discovery['initial_exit_post_public_seconds'])).isoformat().replace('+00:00', 'Z'),
            'status': ('actual_swap_slice' if a['anchor_type'] == 'BUY' and a['actual_swap_review_status'] == 'verified'
                       else 'reanchor_after_actual_swap_review' if a['anchor_type'] == 'BUY' else 'public_event_slice'),
            'not_complete_token_or_wallet_history': True}
        a['deep_onchain_task_allowed'] = a['cap_status'] == 'eligible' and (
            a['anchor_type'] != 'BUY' or a['actual_swap_review_status'] == 'verified')
    anchors.sort(key=lambda a: (moment(a['reference_at_utc']), a['anchor_key']))
    grouped = defaultdict(list)
    for a in anchors:
        grouped[token_identity(a)].append(a)
    queue = []
    for (chain, address), group in sorted(grouped.items()):
        types = Counter(a['anchor_type'] for a in group)
        queue.append({'chain': chain, 'chain_id': group[0]['chain_id'], 'token_address': address,
            'token_symbols': sorted({a['token_symbol'] for a in group if a['token_symbol']}),
            'anchor_keys': [a['anchor_key'] for a in group], 'anchor_type_counts': dict(types),
            'buy_only_in_retained_cohort': not types['THESIS'],
            'distinct_buy_trader_count': len({a['fomo_user_id'] for a in group if a['anchor_type'] == 'BUY'}),
            'distinct_thesis_author_count': len({a['fomo_user_id'] for a in group if a['anchor_type'] == 'THESIS'}),
            'cap_status_counts': dict(Counter(a['cap_status'] for a in group)),
            'eligible_anchor_keys': [a['anchor_key'] for a in group if a['deep_onchain_task_allowed']],
            'traders': [users[uid] for uid in sorted({a['fomo_user_id'] for a in group}, key=lambda uid: users[uid]['rank'])]})
    buys = [a for a in anchors if a['anchor_type'] == 'BUY']
    summary = {'cohort_accounts': len(users), 'thesis_anchors': len(documents), 'buy_anchors': len(buys),
        'thesis_token_count': len({token_identity(o) for o in documents.values()}), 'buy_token_count': len({token_identity(a) for a in buys}),
        'combined_token_count': len(queue), 'buy_only_cohort_token_count': sum(q['buy_only_in_retained_cohort'] for q in queue),
        'buys_without_same_author_retained_thesis': sum(a['no_retained_thesis_by_same_author'] for a in buys),
        'buys_without_cohort_retained_thesis': sum(a['no_retained_thesis_in_cohort'] for a in buys),
        'buys_with_retained_onchain_match_refs': sum(bool(a['onchain_match_refs']) for a in buys),
        'anchor_cap_status_counts': dict(Counter(a['cap_status'] for a in anchors)),
        'deep_onchain_allowed_anchors': sum(a['deep_onchain_task_allowed'] for a in anchors),
        'skipped_invalid_buy_events': len(gaps), 'retained_reviewed_buy_anchors': applied_buy_reviews,
        'actual_buy_verified_anchors': sum(a['actual_swap_review_status'] == 'verified' for a in buys),
        'new_external_requests': 0}
    return {'policy_version': policy['policy_version'], 'inventory_version': 'thesis-and-buy-anchors-v2',
        'cohort': policy['cohort'], 'historical_window': window, 'summary': summary,
        'anchors': anchors, 'token_queue': queue, 'gaps': gaps,
        'history_coverage_status': 'partial_not_60_day_complete',
        'source_code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'token_gate': policy['token_gate'],
        'next_frontier': ['review_historical_circulating_cap_for_BUY_and_THESIS',
                          'verify_actual_fomo_wallet_swap_and_independent_public_visibility_clock',
                          'dispatch_eligible_prebuy_cluster_and_post_signal_exit_windows'],
        'interpretation': 'Retained source assertions; missing THESIS is not proof of no THESIS. No new prebuy cluster, ownership, copy-trading intent or PnL conclusion.'}


def save_inventory(store, inventory):
    digest = hashlib.sha256(_json(inventory).encode()).hexdigest()
    with store.connect() as c:
        prior = c.execute("SELECT id FROM raw_payloads WHERE source='lowcap_event_inventory' AND sha256=?", (digest,)).fetchone()
        raw_id = prior[0] if prior else store.save_raw(c, 'lowcap_event_inventory', '/offline/top100/thesis-and-buy-anchors',
                                                     inventory, utc_now(), status=None)
    return raw_id


def refresh_inventory(store, policy, output_directory):
    inventory = build_inventory(store.database, policy)
    raw_id = save_inventory(store, inventory)
    output_directory = Path(output_directory).resolve()
    output_directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    for name, value in (('review.json', dict(inventory, review_raw_payload_id=raw_id)),
                        ('anchors.json', inventory['anchors']), ('token-queue.json', inventory['token_queue'])):
        path = output_directory / name
        temporary = path.with_suffix('.json.tmp')
        temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
        temporary.chmod(0o600)
        temporary.replace(path)
    pointer = {'policy_version': policy['policy_version'], 'review_raw_payload_id': raw_id,
               'review_path': str(output_directory / 'review.json'), 'summary': inventory['summary'],
               'next_frontier': inventory['next_frontier'], 'historical_window': inventory['historical_window']}
    store.set_state('top100_lowcap_event_inventory_v2', _json(pointer))
    return pointer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-directory', type=Path, required=True)
    args = parser.parse_args()
    policy = json.loads((REPO_ROOT / 'docs/agent-research-policy.json').read_text())
    print(json.dumps(refresh_inventory(Store(DEFAULT_DATABASE), policy, args.output_directory), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
