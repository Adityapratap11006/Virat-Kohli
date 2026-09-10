# KohliIQ — Data Quality Rules (ETL enforcement)

## V1 scope filter (before any row is built)

- Include: `(odis, male, ODI)` + `(t20s, male, T20, international)` + `(ipl, club)`.
- Exclude rows (not errors): women's files, 1-innings/no-result matches, Super Over innings (index ≥ 2), anomalous 50-over T20 files (quarantine list).

## FAIL LOUDLY (abort file / abort load)

1. Missing `info.dates`, `info.teams` (≠2), `info.toss`, or `innings[].overs`.
2. Duplicate match file ID mapping to two different matches.
3. Wicket entry without `player_out`.
4. Unknown `extras` key (observed set: wides, noballs, byes, legbyes, penalty).
5. `balls_per_over != 6`.
6. Negative runs, or `runs.total != runs.batter + runs.extras` (extras fall entirely in `runs.extras`).
7. FK violation on load (player/team/venue/match/innings) — resolve first, never silent-null.

## FLAG AND CONTINUE (validation report, row kept unless in exclusion list)

- `runs.batter = 7` (overthrows) — legitimate.
- `city` missing; `event` missing; registry IDs missing (older T20s).
- Rare dismissals: timed out, obstructing the field, hit the ball twice, retired out/not out.
- `player_out != batter` (non-striker run out).
- Retired hurt + return (one batter-innings continues across two spells — single target).
- Replacements (injury/Impact Player): accept delivery-level names.
- DLS (`outcome.method`): keep, record method.
- Team-name variants (RCB etc.): map to canonical, log unmapped → fail if unmapped at load.

## Raw vs derived

- `data/raw/` is immutable. Normalized tables + rollups + validation report live separately (DB / `data/processed/`).
- Every load writes a validation report: files in/out/excluded, flags by rule, quarantine list.
