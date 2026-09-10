# KohliIQ — Architecture (Phase 1)

## Request flow

```text
Raw Cricsheet JSON (local, data/raw/)
  → ETL (Python: validation → entity resolution → normalization → derived → quality)
  → MySQL (normalized schema + rollups, Phase 3)
  → Spring Boot (frontend-facing REST API, Phase 4+)
  → React (dashboard, Phase 6)
```

ML prediction flow (Phase 9/10):

```text
React → Spring Boot → FastAPI → ML model → FastAPI → Spring Boot → React
```

## Ownership (mandatory)

- **Spring Boot** owns business logic, MySQL access, request validation,
  and ML prediction-context construction from `player_match_stats`/aggregates.
- **FastAPI** (`inference/`) owns model loading, inference, and model metadata.
  It never touches MySQL and never duplicates Spring Boot logic.
- **React** talks only to Spring Boot, never to FastAPI or MySQL directly.

## ML invariants (from `docs/ml/feature-contract.md`)

- Unit: one batter-innings. Timestamp: just before the batter's first delivery.
- Target: final `runs.batter` in that innings. Features knowable at the
  timestamp only; history from strictly pre-match rows; chronological splits.

## Service ports (local dev)

| Service | Port |
|---|---|
| Spring Boot | 8080 |
| FastAPI | 8000 |
| Vite | 5173 |
| MySQL (Phase 3) | 3306 |
