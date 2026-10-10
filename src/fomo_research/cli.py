import argparse
import json
import sys

from .collector import collect_alerts, collect_snapshot, sync_alerts
from .config import DEFAULT_DATABASE
from .solana import match_top_solana_event
from .research import build_top10_wallet_inventory, build_top_solana_timeline
from .store import Store


def _database_arg(parser):
    parser.add_argument("--database", default=str(DEFAULT_DATABASE),
                        help="SQLite path (default: local ignored research database)")


def make_parser():
    parser = argparse.ArgumentParser(description="Collect Fomo leaderboard snapshots and public alerts locally.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init-db", help="Create the local SQLite schema")
    _database_arg(init)

    snapshot = subparsers.add_parser("snapshot", help="Capture a Fomo leaderboard snapshot")
    snapshot.add_argument("--period", choices=("24h", "7d", "30d", "all"), default="30d")
    snapshot.add_argument("--limit", type=int, default=50)
    _database_arg(snapshot)

    alerts = subparsers.add_parser("alerts", help="Recover a bounded alert interval using REST")
    alerts.add_argument("--since", required=True, help="ISO-8601 UTC timestamp")
    alerts.add_argument("--limit", type=int, default=100)
    alerts.add_argument("--type", choices=("buy", "sell", "thesis"))
    alerts.add_argument("--user-id", help="Limit to one Fomo trader userId")
    _database_arg(alerts)

    sync = subparsers.add_parser(
        "sync-alerts",
        help="Poll one Top 10 trader's Fomo REST alerts from a saved timestamp/cursor",
    )
    target = sync.add_mutually_exclusive_group(required=True)
    target.add_argument("--user-id", help="Fomo trader userId from a stored leaderboard")
    target.add_argument("--rank", type=int, help="Rank 1-10 in the latest stored 30d snapshot")
    sync.add_argument("--since", help="Initial ISO-8601 UTC starting time; required on first run")
    sync.add_argument("--overlap-seconds", type=int, default=300,
                      help="Re-read this much time before the previous poll checkpoint")
    sync.add_argument("--limit", type=int, default=500)
    sync.add_argument("--max-pages", type=int, default=1,
                      help="Maximum REST pages to fetch in this run; each costs credits")
    sync.add_argument("--type", choices=("buy", "sell", "thesis"))
    _database_arg(sync)

    status = subparsers.add_parser("status", help="Show local collection counts")
    _database_arg(status)

    match = subparsers.add_parser("match-solana", help="Independently match one stored Fomo event against Solana RPC")
    match.add_argument("--window-seconds", type=int, default=120)
    match.add_argument("--max-pages", type=int, default=10)
    match.add_argument("--page-size", type=int, default=100)
    match.add_argument("--rank", type=int, choices=range(1, 11),
                       help="Limit event matching to one rank in the latest stored 30d Top 10")
    _database_arg(match)

    timeline = subparsers.add_parser(
        "build-timeline",
        help="Normalize stored verified Solana history into SQLite and export research CSVs",
    )
    timeline.add_argument("--rank-limit", type=int, default=10)
    _database_arg(timeline)

    inventory = subparsers.add_parser(
        "build-inventory",
        help="Rebuild the latest Top-N wallet inventory from SQLite source tables",
    )
    inventory.add_argument("--rank-limit", type=int, default=10)
    _database_arg(inventory)
    return parser


def main(argv=None):
    parser = make_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "init-db":
            Store(args.database).initialize()
            result = {"database": args.database, "initialized": True}
        elif args.command == "snapshot":
            result = collect_snapshot(args.database, args.period, args.limit)
        elif args.command == "alerts":
            result = collect_alerts(args.database, args.since, args.limit, args.type, args.user_id)
        elif args.command == "sync-alerts":
            result = sync_alerts(args.database, args.user_id, args.rank, args.since,
                                 args.overlap_seconds, args.limit, args.max_pages, args.type)
        elif args.command == "match-solana":
            result = match_top_solana_event(args.database, args.window_seconds, args.max_pages,
                                            args.page_size, args.rank)
        elif args.command == "build-timeline":
            result = build_top_solana_timeline(args.database, args.rank_limit)
        elif args.command == "build-inventory":
            result = build_top10_wallet_inventory(args.database, args.rank_limit)
        else:
            result = Store(args.database).status()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (RuntimeError, ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Stopped.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
