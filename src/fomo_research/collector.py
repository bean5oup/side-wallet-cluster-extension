from datetime import datetime, timedelta, timezone

from .config import load_api_key
from .provider import get_alerts, get_leaderboard
from .store import Store, utc_now


def collect_snapshot(database, period="30d", limit=50):
    key = load_api_key()
    response = get_leaderboard(key, period, limit)
    store = Store(database)
    store.initialize()
    received, inserted = store.save_leaderboard(response, period)
    return {"received": received, "inserted": inserted, "captured_at_utc": utc_now(),
            "credits_cost": response.credits_cost, "credits_remaining": response.credits_remaining}


def collect_alerts(database, since, limit=100, alert_type=None, user_id=None, cursor=None,
                   include_cursor=False):
    key = load_api_key()
    response = get_alerts(key, since, limit, alert_type, user_id, cursor)
    store = Store(database)
    store.initialize()
    result = store.save_alerts(response)
    payload = response.payload
    has_more = payload.get("hasMore") if isinstance(payload, dict) else None
    result.update({"credits_cost": response.credits_cost,
                   "credits_remaining": response.credits_remaining,
                   "has_more": has_more,
                   "next_cursor_present": bool(payload.get("nextCursor")) if isinstance(payload, dict) else False,
                   "possible_truncation": result["received"] >= limit if has_more is None else bool(has_more)})
    if include_cursor:
        result["_next_cursor"] = payload.get("nextCursor") if isinstance(payload, dict) else None
    return result


def _parse_utc(value):
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        raise ValueError("timestamp must be ISO-8601") from None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def sync_alerts(database, user_id=None, rank=None, since=None, overlap_seconds=300,
                limit=500, max_pages=1, alert_type=None):
    store = Store(database)
    store.initialize()
    if user_id and rank is not None:
        raise ValueError("choose either user-id or rank")
    if rank is not None:
        if rank < 1 or rank > 10:
            raise ValueError("rank must be between 1 and 10")
        with store.connect() as connection:
            row = connection.execute(
                """SELECT fomo_user_id FROM leaderboard_snapshots
                   WHERE period='30d' AND captured_at_utc=(
                     SELECT MAX(captured_at_utc) FROM leaderboard_snapshots WHERE period='30d'
                   ) AND rank=?""",
                (rank,),
            ).fetchone()
        if not row:
            raise ValueError("no stored 30d leaderboard trader found for rank {}".format(rank))
        user_id = row[0]
    if not user_id:
        raise ValueError("choose --rank 1-10 or --user-id")
    if overlap_seconds < 0:
        raise ValueError("overlap-seconds must be zero or greater")
    if max_pages < 1:
        raise ValueError("max-pages must be at least one")
    state_prefix = "rest_alerts_user_{}".format(user_id)
    cursor_key = state_prefix + "_cursor"
    cursor_since_key = state_prefix + "_cursor_since_at_utc"
    through_key = state_prefix + "_sync_through_at_utc"
    cursor = store.get_state(cursor_key)
    cursor_since = store.get_state(cursor_since_key)
    previous = store.get_state(through_key)
    if cursor:
        if since is not None:
            raise ValueError("an unfinished cursor is active; omit --since to resume it")
        start = _parse_utc(cursor_since) if cursor_since else None
        if start is None:
            raise ValueError("saved REST cursor has no starting timestamp")
    elif previous:
        if since is not None:
            raise ValueError("--since is only used for the first REST sync")
        start = _parse_utc(previous) - timedelta(seconds=overlap_seconds)
    elif since:
        start = _parse_utc(since)
    else:
        raise ValueError("first REST sync requires --since")
    start_text = start.isoformat(timespec="milliseconds").replace("+00:00", "Z")
    totals = {"received": 0, "inserted": 0, "duplicates": 0, "ignored": 0,
              "synthetic_ids": 0, "credits_cost": 0}
    pages = 0
    has_more = None
    latest_credit_balance = None
    complete = False
    while pages < max_pages:
        result = collect_alerts(database, start_text, limit, alert_type, user_id, cursor,
                                include_cursor=True)
        pages += 1
        for key in ("received", "inserted", "duplicates", "ignored", "synthetic_ids"):
            totals[key] += result[key]
        try:
            totals["credits_cost"] += int(result["credits_cost"])
        except (TypeError, ValueError):
            pass
        latest_credit_balance = result["credits_remaining"]
        has_more = result["has_more"]
        payload_cursor = result.pop("_next_cursor", None)
        if has_more is True and payload_cursor:
            store.set_state(cursor_since_key, start_text)
            store.set_state(cursor_key, payload_cursor)
            cursor = payload_cursor
            continue
        if has_more is False:
            store.delete_state(cursor_key)
            store.delete_state(cursor_since_key)
            store.set_state(through_key, utc_now())
            complete = True
            break
        # Missing pagination metadata or a missing next cursor is an unknown boundary.
        break

    checked_through = None
    if complete:
        checked_through = store.get_state(through_key)
    totals.update({"pages": pages, "sync_since_at_utc": start_text,
                   "user_filter_applied": True,
                   "cohort_rank": rank,
                   "checked_through_at_utc": checked_through,
                   "checkpoint_advanced": complete,
                   "has_more": has_more,
                   "cursor_saved": bool(store.get_state(cursor_key)),
                   "credits_remaining": latest_credit_balance,
                   "possible_truncation": not complete,
                   "note": "provider returned no more pages" if complete else
                           "page boundary remains; rerun to resume the saved cursor"})
    return totals
