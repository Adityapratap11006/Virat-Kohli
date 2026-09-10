# KohliIQ — ETL Runbook (Phase 2)

## Reproduce

```bash
# from repo root, raw zips extracted to data/raw/{odis,t20s,ipl}
python -m etl.pipeline.run            # full V1 run (~3 min)
python -m etl.pipeline.run --limit 5  # smoke test
python -m pytest etl/tests/ -q        # 30 unit/smoke tests
```

## Outputs & provenance

- Normalized data: `data/processed/*.jsonl` + maps (local-only).
- Run provenance: `data/processed/manifest.json` (timestamp, source counts).
- Quality: `data/processed/etl_report.json`; committed summary:
  `docs/data/etl-summary.json`.

## Known limitations

- Thin-history/early-career guards belong to Phase 7, not ETL.
- `batting_position` is derived and excluded from V1 ML features.
- DLS matches keep the recorded (revised) target; `dls_method` is carried
  on every batter-innings row for later sensitivity analysis.
- No Phase 0 contradictions found; 50-over `t20s` anomalies quarantined
  (8 files) pending Phase 3+ decision.
