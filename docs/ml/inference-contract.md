# KohliIQ — Expected Runs Inference Contract (Phase 8 → Phase 9)

Future FastAPI request (built by Spring Boot from MySQL, never by the
browser; FastAPI never touches MySQL):

```json
{
  "model_version": "v1",
  "format": "ODI",
  "innings_no": 2,
  "is_chase": true,
  "chase_target": 250,
  "entry_runs": 30,
  "entry_wkts": 1,
  "entry_balls": 60,
  "entry_balls_remaining": 240,
  "runs_required": 220,
  "required_rr": 5.5,
  "batting_position": 4,
  "pos_reliable": true,
  "venue_key": "m-chinnaswamy-stadium__bengaluru",
  "venue_name": "M Chinnaswamy Stadium",
  "opposition": "Australia",
  "prior_innings": 12,
  "avg_5": 41.2, "avg_10": 38.0, "avg_20": 44.5, "sr_10": 92.1,
  "venue_n": 3, "venue_avg": 55.0, "venue_sr": 98.0,
  "opp_n": 5, "opp_avg": 47.0, "opp_sr": 90.0,
  "inn1_avg": 40.0, "inn2_avg": 52.0, "chase_avg": 55.0, "setting_avg": 38.0
}
```

Response:

```json
{
  "expected_runs": 42.7,
  "model_name": "xgboost",
  "model_version": "v1",
  "entry_context": {"entry_runs": 30, "entry_wkts": 1, "entry_balls": 60}
}
```

Rules: every historical field must be computed from strictly pre-match
rows (same builder semantics as `ml/features`); NULL history stays NULL
(median/target-encoding fallbacks live in the persisted preprocessor);
no confidence percentages (unjustified); RAE (`actual − expected`) is a
post-match metric, never an input.
