# KohliIQ ETL

Pipeline: raw Cricsheet JSON → validation → entity resolution →
normalization → derived data → quality checks → `data/processed/`
(local-only, never committed). Details: `docs/data/etl-architecture.md`.

- `config.py` — paths, V1 scope, team aliases, rule constants.
- `pipeline/run.py` — two-pass batch runner (`python -m etl.pipeline.run`).
- `validation/` — fail-loud vs flag-and-continue (`data-quality-rules.md`).
- `resolution/` — players (registry-first, ambiguous flagged), teams
  (verified renames only), venues (variant grouping).
- `normalization/` — match/innings/delivery records; delivery identity is
  `(innings_no, over, seq_in_over)`, never `actual_delivery` alone.
- `derived/` — batter-innings rows + entry context (feeds Phase 7, not a model).
- `quality/` — report + manifest.
- `tests/` — `pytest etl/tests/` (fixtures + real-file smoke test).
- `audit_phase0.py` / `probe*.py` / `verify_processed.py` — Phase 0/2 audit tooling.

The Cricsheet schema in `docs/data/data-dictionary.md` is authoritative;
never invent fields. MySQL ingestion belongs to Phase 3.
