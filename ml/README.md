# KohliIQ ML (Expected Runs at Batter Entry)

Authoritative contract: `docs/ml/feature-contract.md`. No exceptions.

- `common/` — shared helpers (chronological iteration, guards).
- `features/` — Phase 7 feature engineering (done): `build.py` replays
  strictly-earlier-date history into `data/ml/v1/` (local-only);
  `history.py` is the pure leakage-safe unit; `verify.py` reconciles
  against MySQL independently. History uses strictly pre-match rows.
- `tests/` — leakage tests A–I (`pytest ml/tests/`).
- `training/` — Phase 8. No random splits; expanding time-series CV.
- `evaluation/` — Phase 8 metrics on held-out recent period.
- `artifacts/` — trained model files (gitignored; never commit binaries).

No training in Phase 7. Contract: `docs/ml/feature-contract.md`;
dataset: `docs/ml/feature-dataset.md`.
