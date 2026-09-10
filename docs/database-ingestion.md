# KohliIQ — Ingestion & Local Setup (Phase 3)

## Reproduce (one command)

```bash
python -m db.run   # migrate -> ingest -> reconcile; fails loudly on mismatch
```

Granular: `python -m db.migrate`, `python -m db.ingest`, `python -m db.reconcile`.
Tests: `python -m pytest db/tests/ -q` (uses throwaway `kohliiq_test`).

## Strategy

- **No staging tables.** Input is already validated Phase 2 output; Python
  re-validates (duplicate source IDs, FK resolvability, contiguous innings
  numbering, toss-winner membership, batter-innings match consistency) and
  InnoDB constraints enforce the rest. A staging layer would add machinery
  without a second writer or untrusted source to isolate.
- **Idempotent upserts.** Every table has a natural UNIQUE key; all writes
  are `INSERT ... ON DUPLICATE KEY UPDATE`. Re-running changes zero rows
  (verified on full data + in tests).
- **Streaming + batching.** JSONL streamed line-by-line (never the 760 MB
  deliveries file in memory); batches of 2,000 (deliveries/batter-innings
  flushed every 10,000); commit per batch. Full ingest ~6 min.
- **FK chaining without round-trips.** Small id-maps (players/teams/venues/
  matches/innings) loaded once; wickets reference the delivery triple via a
  composite FK, so no per-row id lookups (2.4 M rows).
- **Unusual events preserved.** 7-run balls, duplicate delivery numbers,
  non-striker dismissals, DLS, replacements all load; CHECKs only enforce
  `total = batter + extras` and non-negativity.

## Failure behavior

Structural violations (dup source IDs, unresolvable FKs, bad numbering)
abort with `RuntimeError` before commit of that batch. DB errors roll back
the batch. `reconcile.py` exits nonzero on any count/anchor mismatch.

## Local database

Project MySQL 8 runs in Docker (`kohliiq-mysql`, host port 3307, named
volume `kohliiq-mysql-data`) so the pre-existing host instance is untouched:

```bash
docker run -d --name kohliiq-mysql -p 3307:3306 \
  -v kohliiq-mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=kohliiq-dev -e MYSQL_DATABASE=kohliiq mysql:8.0
```

Config via `KOHLIIQ_DB_HOST/PORT/USER/PASSWORD/NAME` (defaults target the
container; placeholders in root `.env.example`). Dev password is local-only,
never committed outside `.env.example` placeholders.
