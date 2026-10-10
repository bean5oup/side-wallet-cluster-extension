"""Bounded root-only Fomo capture for a frozen cohort; workers never spend credits."""
import argparse
import fcntl
import hashlib
import json
import os
from datetime import datetime
from pathlib import Path

from .config import DEFAULT_DATABASE, REPO_ROOT, load_api_key
from .provider import ApiResponse, FomoApiError, get_alerts, get_user_theses
from .store import Store, _alerts, _json, utc_now
from .parallel_theses import import_saved_theses
from .parallel_anchors import refresh_inventory


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temporary.chmod(0o600)
    temporary.replace(path)


def usage(manifest):
    requests = manifest['requests']
    value = {'fomo_http_attempts': len(requests),
             'fomo_credits_reported': sum(r.get('reported_cost') or 0 for r in requests),
             'fomo_credits_budget_charge': sum(r['budget_charge'] for r in requests),
             'cost_header_missing_attempts': sum(r.get('reported_cost') is None for r in requests)}
    manifest.setdefault('actual_usage', {}).update(value)
    return value


def integer_header(value):
    try:
        parsed = int(value)
        return parsed if parsed >= 0 else None
    except (ValueError, TypeError):
        return None


def validate(manifest, policy, store):
    if manifest.get('reservation_status') != 'closed' and manifest.get('policy_version') != policy['policy_version']:
        raise ValueError('An open batch must explicitly use the current policy version')
    if manifest['historical_window'] != policy['historical_window'] or manifest['cohort'] != policy['cohort']:
        raise ValueError('Manifest must use the fixed policy cohort and historical window')
    window = manifest['historical_window']
    start = datetime.fromisoformat(window['start_utc_inclusive'].replace('Z', '+00:00'))
    end = datetime.fromisoformat(window['end_utc_exclusive'].replace('Z', '+00:00'))
    if (end - start).total_seconds() != 5184000:
        raise ValueError('Historical window must be exactly 60 days')
    with store.connect() as connection:
        frozen = {r[0] for r in connection.execute(
            'SELECT fomo_user_id FROM leaderboard_snapshots WHERE raw_payload_id=? AND rank BETWEEN 1 AND 100',
            (manifest['cohort']['leaderboard_raw_payload_id'],))}
    selected = [user for worker in manifest['workers'] for user in worker['capture_user_ids']]
    if len(frozen) != 100 or len(selected) != len(set(selected)) or not set(selected).issubset(frozen):
        raise ValueError('Invalid explicit user IDs for the frozen Top100')
    limits = manifest['limits']
    policy_limits = policy['planned_global_batch_limits']
    for key in ('fomo_http_attempts_max', 'fomo_credits_max'):
        if limits[key] > policy_limits[key]:
            raise ValueError('Manifest exceeds the global policy limit')
    reservation = manifest['primary_network_reservation']
    if reservation['fomo_http_attempts'] > limits['fomo_http_attempts_max'] or reservation['fomo_credits'] > limits['fomo_credits_max']:
        raise ValueError('Primary reservation exceeds the batch limit')
    if any(w['reserved_limits'].get('fomo_http_attempts', 0) or w['reserved_limits'].get('fomo_credits', 0)
           for w in manifest['workers']):
        raise ValueError('This root collector requires all worker Fomo reservations to be zero')
    if manifest['campaign_fomo_credit_limit'] > policy['planned_fomo_foundation_campaign']['credits_max']:
        raise ValueError('Campaign credit limit exceeds the policy')
    return selected


def capture(manifest_path, manifest, policy, users):
    api_key = load_api_key()
    root = REPO_ROOT / 'data/raw/parallel' / manifest['batch_id'] / 'primary'
    start = manifest['historical_window']['start_utc_inclusive']
    reservation = manifest['primary_network_reservation']
    campaign_charge = 0
    for path in manifest_path.parent.parent.glob('*/manifest.json'):
        other = json.loads(path.read_text())
        if other.get('campaign_id') == manifest['campaign_id'] and path != manifest_path:
            campaign_charge += sum(r.get('budget_charge', 0) for r in other.get('requests', []))
    manifest['status'] = 'capturing'
    write_json(manifest_path, manifest)
    for user in users:
        for kind, estimate in (('theses', 1250), ('alerts', 125)):
            # A started request with unknown outcome remains charged and is not silently repeated.
            if any(r['user_id'] == user and r['kind'] == kind for r in manifest['requests']):
                continue
            used = usage(manifest)
            previous_balance = next((integer_header(r.get('credits_remaining')) for r in reversed(manifest['requests'])
                                     if integer_header(r.get('credits_remaining')) is not None), None)
            if (used['fomo_http_attempts'] >= reservation['fomo_http_attempts'] or
                used['fomo_credits_budget_charge'] + estimate > reservation['fomo_credits'] or
                campaign_charge + used['fomo_credits_budget_charge'] + estimate > manifest['campaign_fomo_credit_limit'] or
                (previous_balance is not None and previous_balance < estimate)):
                manifest['budget_stop'] = {'user_id': user, 'kind': kind, 'at_utc': utc_now()}
                write_json(manifest_path, manifest)
                return
            request = {'user_id': user, 'kind': kind, 'attempt': 1, 'started_at_utc': utc_now(),
                       'status': 'inflight_unknown', 'estimated_cost': estimate, 'budget_charge': estimate,
                       'reported_cost': None,
                       'params': {'limit': 100, 'sort': 'recent'} if kind == 'theses' else
                                 {'since': start, 'limit': 500, 'userId': user}}
            request['capture_path'] = str(root / ('{:02d}-{}-{}.json'.format(len(manifest['requests']) + 1, kind, user)))
            manifest['requests'].append(request)
            usage(manifest)
            write_json(manifest_path, manifest)  # Reservation survives process interruption.
            try:
                response = get_user_theses(api_key, user, limit=100, sort='recent') if kind == 'theses' else \
                           get_alerts(api_key, since=start, limit=500, user_id=user)
                at = utc_now()
                envelope = {'request': {'user_id': user, 'kind': kind, 'params': request['params']},
                            'captured_at_utc': at,
                            'response': {'route': response.route, 'status': response.status,
                                         'credits_cost': response.credits_cost,
                                         'credits_remaining': response.credits_remaining, 'payload': response.payload}}
                write_json(Path(request['capture_path']), envelope)
                request.update(status='captured', captured_at_utc=at, route=response.route,
                               reported_cost=integer_header(response.credits_cost),
                               credits_remaining=response.credits_remaining,
                               payload_sha256=hashlib.sha256(_json(response.payload).encode()).hexdigest())
                if request['reported_cost'] is not None:
                    request['budget_charge'] = request['reported_cost']
                payload = response.payload
                request['source_available'] = not (isinstance(payload, dict) and payload.get('available') is False)
                print(json.dumps({'user_id': user, 'kind': kind, 'status': 'captured',
                                  'available': request['source_available'], 'credits_cost': response.credits_cost,
                                  'credits_remaining': response.credits_remaining}), flush=True)
            except (FomoApiError, RuntimeError) as error:
                request.update(status='failed', failed_at_utc=utc_now(), error_type=type(error).__name__,
                               http_status=getattr(error, 'status', None), retry_status='queued_requires_new_reservation')
                # Provider exceptions are deliberately credential-free; do not retain arbitrary exception text.
                write_json(Path(request['capture_path']), {'request': {'user_id': user, 'kind': kind,
                           'params': request['params']}, 'failure': {'error_type': request['error_type'],
                           'http_status': request['http_status'], 'captured_at_utc': request['failed_at_utc']}})
                print(json.dumps({'user_id': user, 'kind': kind, 'status': 'failed',
                                  'http_status': request['http_status']}), flush=True)
            usage(manifest)
            write_json(manifest_path, manifest)


def ingest(manifest_path, manifest, store, users, policy):
    window = manifest['historical_window']
    thesis_ids = []
    for request in manifest['requests']:
        if request['status'] != 'captured':
            # Recover a fully written capture after an interruption without an external request.
            path = Path(request['capture_path'])
            if not path.exists() or 'response' not in json.loads(path.read_text()):
                continue
            envelope = json.loads(path.read_text())
            response = envelope['response']
            request.update(status='captured', captured_at_utc=envelope['captured_at_utc'],
                           route=response['route'], reported_cost=integer_header(response.get('credits_cost')),
                           credits_remaining=response.get('credits_remaining'),
                           payload_sha256=hashlib.sha256(_json(response['payload']).encode()).hexdigest())
            if request['reported_cost'] is not None:
                request['budget_charge'] = request['reported_cost']
        envelope = json.loads(Path(request['capture_path']).read_text())
        response_data = envelope['response']
        payload = response_data['payload']
        response = ApiResponse(response_data['route'], payload, response_data['status'],
                               response_data.get('credits_cost'), response_data.get('credits_remaining'))
        if 'raw_payload_id' not in request:
            with store.connect() as connection:
                prior = connection.execute('SELECT id FROM raw_payloads WHERE source=? AND route=? AND sha256=? AND captured_at_utc=?',
                    ('fomo', response.route, request['payload_sha256'], envelope['captured_at_utc'])).fetchone()
                request['raw_payload_id'] = prior[0] if prior else store.save_raw(connection, 'fomo', response.route,
                    payload, envelope['captured_at_utc'], response.status, response.credits_cost, response.credits_remaining)
            write_json(manifest_path, manifest)
        available = not (isinstance(payload, dict) and payload.get('available') is False)
        request['source_available'] = available
        if not available:
            request['retrieval_status'] = 'unavailable'
            request['source_reason'] = payload.get('reason')
        elif request['kind'] == 'alerts':
            try:
                _alerts(payload)
                request['ingestion'] = store.save_alerts(response, captured_at=envelope['captured_at_utc'],
                    existing_raw_payload_id=request['raw_payload_id'], authorized_user_ids=[request['user_id']],
                    start_at_utc=window['start_utc_inclusive'], end_at_utc=window['end_utc_exclusive'])
                request['retrieval_status'] = 'returned_page'
            except (ValueError, TypeError) as error:
                request['retrieval_status'] = 'invalid_schema'
                request['ingestion_error_type'] = type(error).__name__
        elif not isinstance(payload, dict) or not isinstance(payload.get('theses'), list):
            request['retrieval_status'] = 'invalid_schema'
        else:
            thesis_ids.append(request['raw_payload_id'])
            request['retrieval_status'] = 'returned_page'
        write_json(manifest_path, manifest)
    manifest['thesis_ingestion'] = import_saved_theses(store, thesis_ids,
        manifest['cohort']['leaderboard_raw_payload_id'], authorized_user_ids=users,
        start_at_utc=window['start_utc_inclusive'], end_at_utc=window['end_utc_exclusive'], strict=False)
    manifest['event_inventory'] = refresh_inventory(store, policy,
        manifest_path.parent / 'event-inventory-v2')
    usage(manifest)
    manifest['status'] = 'source_capture_and_ingestion_finished_review_pending'
    manifest['history_coverage'] = 'unknown_partial_not_60_day_complete'
    manifest['updated_at_utc'] = utc_now()
    write_json(manifest_path, manifest)
    store.set_state('top100_parallel_foundation_v1', _json({'campaign_id': manifest['campaign_id'],
        'batch_id': manifest['batch_id'], 'manifest_path': str(manifest_path),
        'status': manifest['status'], 'actual_usage': manifest['actual_usage'],
        'historical_window': window, 'history_coverage': manifest['history_coverage'],
        'event_inventory': manifest['event_inventory']}))
    print(json.dumps({'status': manifest['status'], 'actual_usage': manifest['actual_usage'],
                      'thesis_ingestion': {k: v for k, v in manifest['thesis_ingestion'].items()
                                          if k not in ('scope_user_ids', 'pages', 'rejected_rows')},
                      'rejected_thesis_rows': len(manifest['thesis_ingestion']['rejected_rows'])}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--ingest-only', action='store_true')
    args = parser.parse_args()
    path = args.manifest.resolve()
    policy = json.loads((REPO_ROOT / 'docs/agent-research-policy.json').read_text())
    store = Store(DEFAULT_DATABASE)
    lock_path = path.parent.parent / (json.loads(path.read_text())['campaign_id'] + '.primary.lock')
    with lock_path.open('a') as lock:
        os.chmod(lock_path, 0o600)
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        manifest = json.loads(path.read_text())
        users = validate(manifest, policy, store)
        if manifest.get('reservation_status') == 'closed':
            print(json.dumps({'status': 'reuse_closed_batch', 'batch_id': manifest['batch_id'],
                              'primary_review': manifest.get('primary_review'),
                              'actual_usage': manifest['actual_usage']}), flush=True)
            return
        if not args.ingest_only:
            capture(path, manifest, policy, users)
        ingest(path, manifest, store, users, policy)


if __name__ == '__main__':
    main()
