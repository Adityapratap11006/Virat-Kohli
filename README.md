# KohliIQ

Career analytics for Virat Kohli across ODI, T20I, and IPL (V1 scope):
ball-by-ball ETL from Cricsheet data, a Spring Boot API, a React dashboard,
and an Expected Runs at Batter Entry model (baseline + XGBoost).

## V1 scope

- Formats: ODI, T20I, IPL (men's; Tests deferred to V2).
- Core: ETL → MySQL → Spring Boot → React + Expected Runs pipeline + RAE.
- Out of V1: Tests, player comparison/similarity, milestone models (V2);
  AI assistant, Docker, CI/CD, auth (V3).

## Technologies

| Layer | Stack |
|---|---|
| ETL | Python (pandas in Phase 2+) |
| Database | MySQL (Phase 3) |
| Backend | Java 21, Spring Boot 3.5, Spring Data JPA (Phase 4), Maven |
| ML | Python, pandas, NumPy, scikit-learn, XGBoost (Phase 7/8) |
| Inference | FastAPI (Phase 9) |
| Frontend | React 19, TypeScript, Tailwind CSS 4, Vite |

## Architecture

```text
React → Spring Boot → FastAPI → ML model → FastAPI → Spring Boot → React
```

Details and ownership rules: `docs/architecture.md`.
Spring Boot owns business logic + DB + prediction context; FastAPI owns only
model loading/inference; React talks only to Spring Boot.

## Repository structure

```text
etl/          Cricsheet parsing, validation, entity resolution, normalization
backend/      Spring Boot API (Java 21, Maven)
frontend/     React + TypeScript + Tailwind (Vite)
ml/           feature engineering, training, evaluation (contract first)
inference/    FastAPI inference service (no DB access)
docs/         data audit + dictionary + quality rules, ML contract, architecture
data/raw/     local-only Cricsheet JSON (never committed)
```

## Data source

Cricsheet ball-by-ball JSON (`odis_json`, `t20s_json`, `ipl_json` zips),
audited in Phase 0: `docs/data/dataset-audit.md`. 7353 men's
ODI/T20I/IPL matches (2002→2026). Place extracted JSON in `data/raw/`.

## Status

Phase 1 (foundations) done. Each service builds independently; no domain
functionality yet. See `implementation_plan.md` for the phase roadmap.
