# KohliIQ — Implementation Plan & Architecture Specification (Final)

This document represents the formal architecture, data strategy, and implementation roadmap for the KohliIQ platform.

## 1. Scope Definition
To ensure the project remains finishable while accurately representing Virat Kohli's career, the scope is defined as follows:

*   **V1 (Core System & White-ball Focus):** ODI, T20I, and IPL data. Includes full ETL, Spring Boot backend, React dashboard, and core Expected Runs ML pipeline (XGBoost/Linear Regression).
*   **V2 (Extensions):** Addition of Test matches, Player Comparison, Player Similarity engine, and Milestone Models (30+, 50+, 100+).
*   **V3 (Optional/Productionization):** AI Assistant ("Ask KohliIQ"), comprehensive Dockerization, CI/CD, and User Authentication.

## 2. Actual Data Strategy
*   **Source:** Cricsheet ball-by-ball datasets (JSON/CSV).
*   **Batting Position Rule:** Batting position must remain **nullable**.
    1. It will be derived only when reliably reconstructable from the source data.
    2. A `batting_position_reliable` flag will be stored.
    3. It will **not** be a mandatory ML feature.
    4. If coverage/reliability across the dataset is insufficient, it will be entirely excluded from the V1 ML model rather than forcing an inference.

## 3. Detailed ML Target Definition
**Target Name:** Expected Runs at Batter Entry
*   **Definition:** The number of runs the batter is expected to score from the moment they enter the crease until the end of their innings.
*   **Prediction Unit:** One batter-innings.
*   **Exact Prediction Timestamp:** **Immediately after the previous delivery/wicket has completed and before the batter faces their first delivery.**
    *   *Constraint:* Only information available at that exact moment may be used. This includes handling the context accurately whether the batter enters because of a wicket, a retirement, or at the start of a new innings.
*   **Calculation:** `Target = Final Runs for the innings`.

## 4. ML Feature Contract
To be documented in `docs/ml/feature-contract.md`.

*   **Match Context (Allowed):** Format, venue, opposition, innings number, chase/defend, target (if chasing).
*   **Current Innings Context (Allowed exactly at Prediction Timestamp):** Team score, wickets lost, overs remaining, and required run rate (if chasing) immediately before the batter faces their first delivery.
*   **Historical Context (Allowed - Must be pre-match):** Previous 5/10/20 innings average, previous 10 innings strike rate, historical venue/opposition performance, historical phase strike rate.
*   **Features that MUST NOT be used (Leakage):** Final innings score, current innings result, future matches/innings, post-match statistics, batter's final strike rate for the current innings.

## 5. Leakage-Prevention Strategy
Rolling features will be generated dynamically using strict chronological iteration.
*   **Algorithm:**
    1. Sort the entire dataset chronologically by match date.
    2. For each match/innings row:
        a. Calculate historical features using *only* rows that appear before the current row.
        b. Attach current context features (known at the Prediction Timestamp).
        c. Attach the target (Final Runs).
        d. Append the constructed feature row.

## 6. Temporal Validation Strategy
No random shuffling (`train_test_split`).
1. Inspect actual dataset coverage (e.g., 2008–2024).
2. Split chronologically based on real data distributions.
    *   **Training:** Historical seasons (e.g., 2008–2021).
    *   **Validation:** Later unseen season(s) (e.g., 2022) for hyperparameter tuning.
    *   **Testing:** Most recent unseen period (e.g., 2023–2024) for final evaluation.
3. We will utilize expanding time-series cross-validation during the training phase.

## 7. Revised MySQL Schema (With Strict Constraints)
A normalized schema supporting analytical rollups:

*   **`players`**:
    *   `id` (PK, NOT NULL)
    *   `name` (NOT NULL, Idx)
    *   `unique_identifier` (Cricsheet ID, UNIQUE, NOT NULL)
*   **`teams`**: `id` (PK), `name` (UNIQUE, NOT NULL, Idx).
*   **`venues`**: `id` (PK), `name` (NOT NULL, Idx), `city`.
*   **`matches`**:
    *   `id` (PK, NOT NULL)
    *   `date` (NOT NULL, Idx)
    *   `format` (NOT NULL, Idx)
    *   `venue_id` (FK -> venues.id, NOT NULL, Idx)
*   **`innings`**:
    *   `id` (PK, NOT NULL)
    *   `match_id` (FK -> matches.id, NOT NULL, Idx)
    *   `batting_team_id` (FK -> teams.id, NOT NULL)
    *   `innings_number` (NOT NULL)
    *   *Constraint:* `UNIQUE(match_id, innings_number)`
*   **`deliveries`**:
    *   `id` (PK, NOT NULL)
    *   `innings_id` (FK -> innings.id, NOT NULL, Idx)
    *   `over_number` (NOT NULL)
    *   `ball_number` (NOT NULL)
    *   *Constraint:* Identity within an innings is logically unique, e.g., `UNIQUE(innings_id, over_number, ball_number)` unless re-bowled balls necessitate a sub-ball sequence identifier.
    *   `batter_id`, `bowler_id` (FK -> players.id, NOT NULL, Idx)
*   **`player_match_stats` (Rollup)**:
    *   `id` (PK, NOT NULL)
    *   `player_id` (FK -> players.id, NOT NULL, Idx)
    *   `match_id` (FK -> matches.id, NOT NULL, Idx)
    *   `batting_position` (Nullable)
    *   `batting_position_reliable` (Boolean, NOT NULL)
    *   *Constraint:* `UNIQUE(player_id, match_id)`

## 8. Cricsheet-Aware ETL Validation
The ETL pipeline will fail loudly for critical structural errors (e.g., missing match metadata, duplicate `match_id` mapping).
However, it will **not** treat unusual but legitimate cricket events (e.g., `runs_batter > 6` via overthrows) as automatically invalid. Unusual events will be flagged for inspection in a validation report rather than incorrectly rejected.

## 9. API Request Flow Strategy (Spring Boot -> FastAPI)
**Architecture Flow:** `React -> Spring Boot -> FastAPI -> ML Model -> FastAPI -> Spring Boot -> React`

*   **Spring Boot (Java):** Acts as the frontend-facing API. It validates the prediction request, aggregates the necessary match/player context from MySQL, constructs the final prediction context payload, and handles all business logic.
*   **FastAPI (Python):** Pure ML Inference service. Receives the strictly prepared ML context, loads the trained model, performs inference, and returns prediction results + model metadata. **FastAPI does NOT directly access MySQL or duplicate Spring Boot business logic.**

## 10. RAE and Kohli Impact Index Methodology
Implementation sequence:
`Expected Runs -> Model Validation -> RAE -> Contextual Analysis -> Impact Index Design -> Normalization/Weights -> Sensitivity Testing -> UI`

*   **Runs Above Expected (RAE):** `Actual Runs - Expected Runs at Batter Entry`. Calculated purely post-performance.
*   **Kohli Impact Index:** Delayed until RAE is fully validated. Will be clearly labeled as a project-defined metric (not an official statistic), documented in `docs/metrics/kohli-impact-index.md`.

## 11. Implementation Roadmap

*   **Phase 0 — Dataset Audit & Data Contract:** Inspect Cricsheet data, verify available fields, define `docs/ml/feature-contract.md`.
*   **Phase 1 — Architecture & Repository Setup:** Init Git, Python ETL skeleton, Spring Boot (Maven), React (Vite).
*   **Phase 2 — ETL & Entity Resolution:** Script raw data parsing, Cricsheet-aware validation, and canonical mapping.
*   **Phase 3 — MySQL Schema & Ingestion:** Stand up MySQL, run DDL scripts with strict constraints, load normalized data + rollups.
*   **Phase 4 — Spring Boot Backend:** JPA Entities, DTOs, Controllers for basic fetching and context preparation.
*   **Phase 5 — Core Analytics APIs:** Implement form, opposition, and venue aggregations.
*   **Phase 6 — React Dashboard:** Build UI components, integrate Spring Boot APIs.
*   **Phase 7 — ML Feature Engineering:** Python script to generate chronological feature rows from the Prediction Timestamp and validate no leakage.
*   **Phase 8 — Baseline + Advanced ML Models:** Train Linear Regression (Baseline) and XGBoost (Expected Runs at Batter Entry). Evaluate & save.
*   **Phase 9 — FastAPI Inference:** Expose loaded models via REST endpoints.
*   **Phase 10 — ML Integration & Predictor UI:** Connect React -> Spring Boot -> FastAPI.
*   **Phase 11 — Impact Index + RAE:** Implement RAE post-match calculations and UI visualizations, followed by Impact Index design.
*   **Phase 12 — Comparison & Similarity (V2):** PCA/Clustering implementation.
*   **Phase 13 — Testing:** JUnit, PyTest, Frontend tests.
*   **Phase 14 — Docker & Deployment:** `Dockerfile`s and `docker-compose.yml`.
*   **Phase 15 — Documentation:** Comprehensive README, ER diagrams.
*   **Phase 16 — Optional AI Assistant (V3):** LLM integration.
