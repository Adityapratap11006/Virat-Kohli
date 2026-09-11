# KohliIQ — Expected Runs Model Evaluation v1 (Phase 8)

## Dataset

Frozen `data/ml/v1` (119,619 rows, 38 feature columns, target
`target_runs` = final batter runs). Chronological splits, never random:
train ≤2021 (65,143), validation 2022 (10,808), test ≥2023 (43,668,
scored once after selection). Full definition:
`docs/ml/feature-dataset.md`.

## Leakage controls

Prediction timestamp = before the batter's first faced ball. History uses
strictly earlier match dates; target/balls/future deliveries never enter
features; preprocessing (medians, one-hot levels, target-encoding maps
with smoothing m=20) fitted on train only. Tests: `ml/tests/test_leakage.py`
(A–I) + `ml/tests/test_models.py` (target exclusion, split integrity,
train-only fitting, determinism). No test tuning.

## Preprocessing

Numerics → train-median imputation. `format, innings_no, is_chase,
pos_reliable` → one-hot. `opposition, venue_key` → smoothed target
encoding (train only; unseen → train global mean). `year` excluded
(time identifier). Same matrix feeds Ridge and XGBoost (documented
simplification; XGB's native NaN handling unused).

## Models

- **global_mean**: train mean. **hist_avg**: row's avg_20→avg_10→avg_5,
  else train mean. **format_mean**: train mean per format.
- **Ridge** (α ∈ {0.1, 1, 10, 100} → 100.0): regularized linear baseline.
- **XGBoost** (10-config restrained grid, early stopping on 2022):
  winner = depth 3, lr 0.05, 500 trees, α 1.0, λ 2.0 (seed 7).

## Results

| Model | Val MAE | Val RMSE | Val R² | Test MAE | Test RMSE | Test R² |
|---|---|---|---|---|---|---|
| Global Mean | 17.02 | 21.91 | -0.02 | 16.98 | 21.70 | -0.03 |
| Hist Avg | 15.26 | 21.09 | 0.05 | 14.51 | 20.42 | 0.09 |
| Format Mean | 16.02 | 21.50 | 0.02 | 15.72 | 21.12 | 0.02 |
| Ridge | 14.27 | 20.05 | 0.15 | 13.78 | 19.49 | 0.17 |
| XGBoost | 14.00 | 19.73 | 0.17 | 13.60 | 19.26 | 0.19 |

**Does ML add value? Yes, modestly:** XGBoost beats the historical
average by ~0.9 test MAE (~6% relative) and doubles R² (0.19 vs 0.09),
consistently across all four expanding windows (2019–2022). Absolute
skill is limited — cricket scores are heavy-tailed; 50+ innings dominate
error (test MAE 44.1 there vs 7.0 in 10–29).

## Ablation (validation MAE)

history-only 14.84 · context-only 14.57 · combined 14.27 ·
full 14.27 (Ridge) / 14.00 (XGB). Batting position adds nothing
measurable (Ridge full 14.2715 vs no-pos 14.2656; XGB full 13.9984 vs
no-pos 14.0158) — kept in the schema, not relied upon.

## Error analysis (test, XGBoost)

Formats: T20I 12.06, IPL 15.34, ODI 18.48 (higher scores → higher MAE).
Innings: 1st 14.02, chase 13.12. History buckets rise with scoring level
(debut 8.78 → strong 16.09), as do tail-vs-top positions (No. 11: 2.84,
No. 3: 17.86) — error follows run variance, not model bias against
newcomers. Residual mean −0.39 (near-zero bias).

## Kohli slice (test, 111 rows, mean actual 47.3)

| Model | MAE | RMSE | R² |
|---|---|---|---|
| Hist Avg | 32.38 | 38.65 | -0.07 |
| Ridge | 30.93 | 37.03 | 0.01 |
| XGBoost | 30.62 | 36.45 | 0.04 |

General model applied unchanged; Kohli's test era is big-score heavy
(53/111 are 50+), hence larger absolute errors. By format (XGB):
IPL 25.48 (n=60), ODI 38.16 (n=44), T20I 27.36 (n=7).

## Artifacts (`ml/models/v1/`)

`metrics.json` + `config.json` (tracked); `preprocessor.pkl`,
`ridge.pkl`, `xgb.ubj` (gitignored binaries; regenerate with
`python -m ml.models.train`, ~1 min, seed 7).

## Limitations

- R² ≈ 0.19: context + history explain part of innings variance; the
  rest is cricket (match situation evolution, bowling, luck).
- High-score innings dominate MAE; cold-start rows lean on train means.
- Date-strict history sacrifices same-day information by design.
- Expanding windows reuse the val-selected Ridge α/XGB config (diagnostic).
- No uncertainty estimates — none are statistically justified yet.
