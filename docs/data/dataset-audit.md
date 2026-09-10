# KohliIQ — Phase 0 Dataset Audit (observed, not assumed)

Audit script: `etl/audit_phase0.py` (+ `etl/probe2.py`). Output: `docs/data/audit_raw.json`.
All counts below are from real files on disk. No fields invented.

## 1. Source & version

- Source: official Cricsheet downloads:
  - `https://cricsheet.org/downloads/odis_json.zip` (3183 entries, 3182 `.json` on disk)
  - `https://cricsheet.org/downloads/t20s_json.zip` (5701 entries, 5700 `.json` on disk)
  - `https://cricsheet.org/downloads/ipl_json.zip` (1244 entries, 1243 `.json` on disk)
- Downloaded: 2026-09-10. Cricsheet is a rolling release (no frozen version number);
  observed `meta.data_version: 1.2.0` in sampled files.
- Reproduce: re-download the three zips, extract to `data/raw/{odis,t20s,ipl}`, run the audit script.

## 2. V1 coverage (male only)

| Dataset | Files on disk | V1 filter | V1 matches | Coverage dates |
|---|---|---|---|---|
| odis | 3182 | gender=male, match_type=ODI | **2571** | 2002-06-27 → 2026-09-09 |
| t20s | 5700 | gender=male, match_type=T20, team_type=international (= T20I) | **3539** | 2005-02-17 → 2026-09-09 |
| ipl | 1243 | all (male, team_type=club) | **1243** | 2008-04-18 → 2026-05-31 |
| **Total V1** | | | **7353** | |

- Excluded from V1: 611 women's ODIs, 2161 women's T20Is.
- Kohli squad-presence (name match on `info.players`, includes DNB): ODI 311, T20 159, IPL 286.
- Seasons observed (all genders): ODI 52 labels (2002→2026), T20 46 labels (2004/05→2026), IPL 24 labels (2007/08→2026).

## 3. Schema findings (observed)

- Top-level keys: `meta`, `info`, `innings`. Deliveries are nested: `innings[i].overs[j].deliveries[k]` (list, file order = chronological).
- `info.match_type` values: odis=`ODI`; t20s=`T20` (**not** `T20I` — T20I = `match_type:T20` + `team_type:international` + `gender:male`); ipl=`T20` + `team_type:club`.
- `balls_per_over` always 6 (all files). `info.overs`: ODI=50, T20/IPL=20, **except 8 files in t20s with `overs: 50` (anomaly, see §6)**.
- Innings counts: overwhelmingly 2; 1-innings files are `no result`/abandoned (exclude from ML); 4/6/8-innings files are Super Overs and must be excluded from batter-innings construction (observed super-over innings: ODI 20, T20 54, IPL 34).
- Delivery keys (always): `actual_delivery` (string, e.g. `8.5`), `batter`, `bowler`, `non_striker`, `runs`. Optional: `extras`, `wickets` (list), `review`, `replacements`.
- `runs`: `{batter: 0-7, extras, total}`. `runs.batter = 7` observed once (ODI) and twice (T20) — overthrows, legitimate.
- `extras` keys observed: `wides`, `noballs`, `byes`, `legbyes`, `penalty`. No other keys.
- `wickets` is a **list** with `{player_out, kind, fielders?}`. `player_out != batter` in ~3–4% of wickets (ODI 1723, T20 1778, IPL 571) — run-outs of the non-striker, etc. Never assume the batter is out.
- Wicket `kind` values observed (union): bowled, caught, caught and bowled, run out, lbw, stumped, hit wicket, retired hurt, retired out, retired not out, obstructing the field, timed out, hit the ball twice (T20 once).
- `replacements.role`: list of `{in, out?, reason, role}` — mid-match injury subs. Observed in all formats (ODI 342, T20 247, IPL 585 delivery-events).
- `review`: `{by, batter, decision, umpire?, umpires_call?}` — informational only, excluded from V1 features.
- 2nd innings has `innings[i].target: {overs, runs}`; some innings have `powerplays`. No ball-tracking, weather, or pitch data anywhere.
- Identifiers: `info.registry.people` maps display name → hex ID. Coverage: **ODI 100%, IPL 100%, T20 only 3000/5700 (~53%)** — older T20s have no IDs. `player_of_match`, officials also present but unused in V1.
- Team renames observed in `info.teams`/`outcome.winner`: `Royal Challengers Bangalore` → `Royal Challengers Bengaluru` (old + new names coexist). Canonical team mapping required (also watch Kings XI Punjab / Punjab Kings, Delhi Daredevils / Delhi Capitals).
- Venue: `info.venue` always present; `info.city` missing in ~10% (ODI 281/2571, T20 123, IPL 51). Toss, dates, outcome, teams always present in V1 scope.
- Toss/outcome: `toss: {winner, decision}`; `outcome` is `winner+by` / `result: no result|tie` / `method` (DLS). Outcome strings vary in key order — parse as structured, not string.

## 4. Batting-position feasibility

- No batting-position field exists. Reconstruction = order of first appearance (batter or non_striker) per innings.
- Works in clean innings (verified: Kohli file `1022353.json`, India innings order RG Sharma, S Dhawan, V Kohli …).
- **Unreliable when**: retired hurt + return, retired out/not out, replacement subs, DNB players (never appear), 1-innings/no-result files, Super Overs.
- Decision (per plan): `batting_position` **nullable** + `batting_position_reliable` flag; **excluded from V1 ML features** entirely.

## 5. Cricket edge cases affecting ETL/ML

1. Wides/noballs share `actual_delivery` numbers (e.g. two `0.5`s) — file order is the truth; never dedupe on over+ball alone.
2. `runs.batter > 6` (7s) legitimate via overthrows — flag, never reject.
3. Non-striker dismissals (`player_out != batter`) — batter's innings continues.
4. Retired hurt (may return), retired out (innings over), retired not out — distinct target-accounting from wickets.
5. Super Overs (innings index ≥ 2) — excluded from ML rows.
6. No-result / 1-innings matches — excluded from ML rows.
7. DLS-affected matches (`outcome.method`, revised `target`) — include but record method; entry-context overs-remaining uses revised target/overs where present.
8. `timed out`, `obstructing the field`, `hit the ball twice` — vanishingly rare but valid dismissals.
9. Replacements (injury/Impact Player era) — new batters can appear mid-innings; player identity follows the delivery-level name, not the squad list.
10. T20 `overs: 50` anomalies (8 files) — quarantine for inspection, excluded from V1 until verified.

## 6. Data-quality findings

- Critical (fail loudly): missing `info.dates/teams/toss`, missing `innings[].overs`, duplicate match file IDs, `player_out` missing on a wicket, unknown `extras` key, `balls_per_over != 6`.
- Flag-and-continue: `runs.batter = 7`, city missing, registry IDs missing (T20), 1-innings matches, super overs, 50-over T20 anomalies, team-name variants.
- No duplicate filenames observed; counts match zip entries minus one non-JSON entry each.

## 7. Assumptions changed

- `match_type: T20I` does not exist — filter is `match_type=T20 AND team_type=international AND gender=male`.
- T20 registry coverage is ~53%, not universal — entity resolution must be name-first with ID where available.
- `t20s_json.zip` is men+women T20I combined; `odis_json.zip` likewise. Gender filter is mandatory for V1.

## 8. Limitations for the Expected-Runs-at-Entry model

- No ball-tracking/pitch/weather; context features limited to score/wickets/overs/chase-state + history.
- Openers enter at 0/0 — model must handle degenerate entry state.
- City missing ~10% — venue features must tolerate null city (venue name always present).
- History for early-career batters is thin — rolling averages need minimum-innings guards.
- DLS matches add noise to required-rate features — record `outcome.method`, consider sensitivity exclusion later.
- Super-over, no-result, and anomalous 50-over-T20 rows are out of scope for training rows.
