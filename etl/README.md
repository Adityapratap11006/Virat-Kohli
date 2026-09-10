# KohliIQ ETL

Pipeline: raw Cricsheet JSON → validation → entity resolution →
normalization → derived data → quality checks → MySQL (Phase 2/3).

- `audit_phase0.py` / `probe2.py` — Phase 0 audit tooling (authoritative results
  in `docs/data/`). The Cricsheet schema in `docs/data/data-dictionary.md`
  is authoritative; never invent fields.
- `validation/` `resolution/` `normalization/` `derived/` `quality/` arrive in Phase 2.
- `data/raw/` is local-only and never committed.
