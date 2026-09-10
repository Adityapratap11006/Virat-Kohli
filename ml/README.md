# KohliIQ ML (Expected Runs at Batter Entry)

Authoritative contract: `docs/ml/feature-contract.md`. No exceptions.

- `common/` — shared helpers (chronological iteration, guards).
- `features/` — feature engineering, Phase 7. History uses strictly pre-match rows.
- `training/` — Phase 8. No random splits; expanding time-series CV.
- `evaluation/` — Phase 8 metrics on held-out recent period.
- `artifacts/` — trained model files (gitignored; never commit binaries).

No training in Phase 1.
