# KohliIQ Database (MySQL 8)

Authoritative persistent store for Phase 2 normalized output.
Spring Boot reads it in Phase 4+; only this layer writes it.

- `migrations/` — versioned SQL (`V1__initial_schema.sql`).
- `migrate.py` — applies pending migrations, tracks `schema_version`.
- `ingest.py` — streaming batched upserts (`INSERT ... ON DUPLICATE KEY
  UPDATE`); re-runnable without duplication.
- `reconcile.py` — exact count reconciliation + Kohli anchors; nonzero exit
  on mismatch.
- `run.py` — one-command rebuild: `python -m db.run` (repo root).
- `tests/` — needs a running MySQL; uses throwaway `kohliiq_test` database.

No staging tables (documented in `docs/database-ingestion.md`).
Config via `KOHLIIQ_DB_*` env; see root `.env.example`.
