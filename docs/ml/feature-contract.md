# KohliIQ — Feature Contract: Expected Runs at Batter Entry (V1)

## 1. Prediction unit & timestamp & target

- **Unit:** one batter-innings (one batter × one team-innings, innings index 0–1 only; Super Overs excluded).
- **Timestamp:** immediately after the previous delivery/wicket completes, before the batter faces their first delivery. Entry causes: start of innings, wicket, retirement, replacement/sub.
- **Target:** `sum(runs.batter)` over that batter's deliveries in that innings (retired-hurt returns merged; retired-out ends the innings; DNB = no row).

## 2. Allowed features (all must be knowable at the timestamp)

- **Match context:** format (ODI/T20I/IPL), venue (canonical id; city nullable), opposition, home/away/neutral (if derivable), innings number (1/2), bat-first vs chase, chase `target` (2nd innings only, DLS-revised value where present), toss outcome/decision.
- **Entry context (replayed from prior deliveries in this innings only):** team runs, wickets lost, balls bowled/remaining, runs required + balls remaining (chase only). Openers: defined as 0/0/full-overs.
- **History (completed prior matches only, strictly before this match date):** rolling average over prior 5/10/20 batter-innings, prior-10 strike rate, venue/opposition history, phase history — computed by chronological iteration, never from current innings/match. Minimum-innings guards required (early-career thin history).

## 3. FORBIDDEN (leakage)

Final innings score, current-innings result, any delivery/ball from this batter-innings at or after the timestamp, future matches, post-match stats (incl. this innings' strike rate), reviews/replacements occurring after entry, Super Over data, `batting_position` (excluded from V1 — nullable/unreliable per audit).

## 4. Leakage-prevention algorithm

1. Sort matches chronologically by `info.dates[0]` (tie-break: match file ID).
2. For each batter-innings row in order: compute history from strictly-earlier rows only → attach entry context → attach target → append. No global aggregates, no `train_test_split` shuffle.

## 5. Temporal validation (provisional — finalize exact cut years in Phase 7 after row counts)

- Train: historical seasons through ~2021; Validation: ~2022 (tuning); Test: most recent period (~2023–2026). Expanding time-series CV inside train. No random splits.
- Sensitivity: DLS-method matches and thin-history rows reported separately, not silently dropped.
