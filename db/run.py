"""One-command database rebuild from Phase 2 processed output:
migrate -> ingest -> integrity/reconciliation checks.

Usage: python -m db.run   (run from repo root)
Requires: project MySQL (see docs/database-ingestion.md) and data/processed/.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db import config
from db.ingest import PROCESSED, ingest
from db.migrate import migrate
from db.reconcile import reconcile


def main() -> None:
    missing = [f for f in ("matches.jsonl", "innings.jsonl", "deliveries.jsonl",
                           "batter_innings.jsonl", "players.json",
                           "teams.json", "venues.json")
               if not (PROCESSED / f).exists()]
    if missing:
        raise SystemExit(f"missing processed inputs: {missing} "
                         f"(run: python -m etl.pipeline.run)")
    try:
        conn = config.connect(database=None)
        conn.close()
    except Exception as e:
        raise SystemExit(f"cannot reach MySQL at {config.HOST}:{config.PORT}: {e}")
    migrate()
    ingest()
    report = reconcile()
    if report["errors"]:
        raise SystemExit(f"RECONCILIATION FAILED: {report['errors']}")
    print("database rebuild complete: schema + ingest + reconciliation all green")


if __name__ == "__main__":
    main()
