# KohliIQ — Expected Runs Feature Dataset v1 (Phase 7)

## Prediction contract

- **Unit:** one batter-innings (normal innings only; Super Overs excluded upstream).
- **Timestamp:** immediately after the previous delivery/wicket, before the
  batter's first faced delivery.
- **Target `target_runs`:** final runs by that batter in that innings.

## Construction (`ml/features/build.py`, stdlib only)

1. Read all 119,619 `batter_innings` rows (+ team/venue/canonical joins)
   from MySQL ordered by (match_date, match_id, innings_id, id).
2. Per batter, replay history: a row dated D uses only completed rows with
   match_date strictly before D (day-granular dates; same-day matches
   excluded as a conservative leakage guard).
3. Entry features are copied from persisted entry state (team runs, wickets
   lost excl. retired hurt/not-out, legal balls bowled/remaining, chase
   target); `runs_required`/`required_rr` derived arithmetically.
4. Write `data/ml/v1/features.csv` (local-only) + `feature_schema.json` +
   `manifest.json`. Deterministic; re-running reproduces it.

## Feature list (38 columns)

Identity/traceability: `batter_innings_id, match_id, source_match_id,
batter_code, match_date, year, split`. Entry: `format, innings_no,
is_chase, chase_target, entry_runs, entry_wkts, entry_balls,
entry_balls_remaining, entry_overs_completed, runs_required, required_rr,
batting_position, pos_reliable, venue_key, venue_name, opposition`.
History (NULL cold start): `prior_innings, avg_5/10/20, sr_10, venue_n,
venue_avg, venue_sr, opp_n, opp_avg, opp_sr, inn1_avg, inn2_avg,
chase_avg, setting_avg`. Target: `target_runs`.

Windows use available history even when shorter than N; counts expose
sample size. `batting_position` is always present (appeared batters);
`pos_reliable` marks the 93% clean reconstructions — Phase 8 decides its
use; it was excluded from V1 candidacy in Phase 0.

## Splits (chronological, never random)

Train ≤2021 (65,143) · Validation 2022 (10,808) · Test ≥2023 (43,668,
untouched). `year` column supports expanding-window CV in Phase 8.

## Leakage stance

`ml/tests/test_leakage.py` (A–I): same-day exclusion, target/future
isolation, venue/opp strict-prior, split non-overlap, row uniqueness,
Kohli anchor (682 rows, 28,078 runs). `ml/features/verify.py`
reconciles counts, sums, entry fields, and chase math against MySQL
independently of the builder.

## Limitations

- Date-strict history drops same-day prior matches (conservative).
- No ball-tracking/pitch/weather; venue/city gaps persist from upstream.
- Thin-history rows (4.6% debuts; venue 38% / opp 30% cold) need
  minimum-history guards in Phase 8.
- Model training itself is Phase 8; no model artifacts exist yet.
