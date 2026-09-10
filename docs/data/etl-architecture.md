# KohliIQ — ETL Architecture (Phase 2)

## Stages

```text
data/raw/{odis,t20s,ipl}  (immutable)
  → etl/pipeline/run.py -- scan + pass 1
  → etl/validation/validate.py -- fail-loud vs flag-and-continue
  → etl/resolution/{players,teams,venues}.py -- entity resolution
  → pass 2: etl/normalization/normalize.py -- matches/innings/deliveries
  → etl/derived/batter_innings.py -- batter-innings + entry context
  → etl/quality/report.py -- etl_report.json + manifest.json
  → data/processed/  (local-only, gitignored)
```

Two deterministic passes: pass 1 validates every file and collects
registries/venue spellings; pass 2 re-reads only usable V1 files and writes
outputs. No randomness, no in-memory world model, per-file streaming.

## Outputs (`data/processed/`)

| File | Content |
|---|---|
| `matches.jsonl` | one row per V1 match (canonical + source team names, venue, toss, outcome, DLS method) |
| `innings.jsonl` | classification `normal` / `super_over` / `incomplete`; chase `target_*`; `had_replacement` |
| `deliveries.jsonl` | identity `(innings_no, over, seq_in_over, global_seq)`; resolved ids; extras/wickets verbatim |
| `batter_innings.jsonl` | one row per batter per normal innings; entry context; aggregates; nullable position + reliability |
| `players.json` / `teams.json` / `venues.json` | resolution maps (every REG id has a meta entry) |
| `etl_report.json` / `manifest.json` | quality stats + run provenance |

## Key rules

- V1 scope: male ODI (`odis`), male T20+international (`t20s`), club (`ipl`).
  Women, 1-innings/no-result matches, Super Over deliveries, and eight
  anomalous 50-over `t20s` files are excluded from normalized rows (raw kept).
- `actual_delivery` is preserved, never a key. `runs.batter > 6` is allowed.
- `player_out` is independent of `batter`. Retired hurt/not-out are not
  dismissals; retired out ends the innings without a dismissal.
- Entry context = state before the first delivery FACED (score, wickets lost
  excl. retired hurt/not-out, legal balls).
- `data/processed/` is local-only and never committed.
