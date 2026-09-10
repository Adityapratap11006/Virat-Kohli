# KohliIQ — Cricsheet Data Dictionary (observed V1 scope)

Only fields actually observed in `data/raw/{odis,t20s,ipl}` are listed. Types as observed.

## Top level (per file = one match)

| Key | Type | Present | Notes |
|---|---|---|---|
| `meta.data_version` | string | always (sampled `1.2.0`) | format version |
| `meta.created` / `meta.revision` | string / int | always (sampled) | provenance |
| `info` | object | always | match metadata |
| `innings` | list | always (1–8 entries) | V1 uses first 2; index ≥ 2 = Super Over |

## `info`

| Key | Type | Present | Notes |
|---|---|---|---|
| `dates` | list[string] | always | match date(s); chronological sort key |
| `venue` | string | always | canonicalize via `venues` table; `city` may be null |
| `city` | string | ~90% | nullable |
| `season` | string or int | always | e.g. `2016/17`, `2026`; normalize to string |
| `match_type` | string | always | `ODI` or `T20` (T20I is `T20` + international) |
| `match_type_number` | int | usually | cross-check only |
| `team_type` | string | always | `international` (ODI/T20I) or `club` (IPL) |
| `teams` | list[string, 2] | always | variants exist (RCB rename) → canonicalize |
| `toss` | `{winner, decision}` | always | decision: `bat`/`field` |
| `outcome` | object | always | `winner+by` / `result: no result|tie` / `method` (DLS) |
| `overs` | int | always | 50 (ODI), 20 (T20/IPL); 8 anomalous 50s in t20s |
| `balls_per_over` | int | always | observed always 6 |
| `players` | map team → list[string] | always | squad incl. DNB; name strings, not order |
| `registry.people` | map name → hex id | ODI/IPL 100%, T20 ~53% | missing in older T20s → name-first resolution |
| `event` | `{name, match_number?}` | mostly | series/tournament; missing in 14 ODIs, 66 T20s |
| `gender` | string | always | V1 filter: `male` only |
| `officials`, `player_of_match` | misc | often | not used in V1 |

## `innings[i]`

| Key | Type | Present | Notes |
|---|---|---|---|
| `team` | string | always | batting team |
| `overs` | list | always | each `{over: int, deliveries: list}` |
| `target` | `{overs, runs}` | 2nd innings | chase target (DLS-revised where applicable) |
| `powerplays` | list | sometimes | not a V1 feature |

## Delivery (`innings[i].overs[j].deliveries[k]`)

| Key | Type | Present | Notes |
|---|---|---|---|
| `actual_delivery` | string | always | e.g. `8.5`; **duplicates on wides/noballs — not unique** |
| `batter` / `non_striker` / `bowler` | string | always | display names; resolve via registry/name map |
| `runs` | `{batter, extras, total}` | always | ints; `batter` observed 0–7 |
| `extras` | map | wides/noballs/byes/legbyes/penalty only | keys: `wides`, `noballs`, `byes`, `legbyes`, `penalty` |
| `wickets` | list of `{player_out, kind, fielders?}` | on dismissals | `player_out` may be non-striker; kinds enumerated in audit |
| `replacements.role` | list of `{in, out?, reason, role}` | rarely | subs; player identity follows delivery names |
| `review` | object | rarely | ignored in V1 |

## Derived (not in source — built by ETL)

- `batting_position` (nullable int) + `batting_position_reliable` (bool); excluded from V1 ML.
- Entry context per batter-innings: team score, wickets lost, balls remaining, chase target/required rate — replayed from deliveries strictly before the batter's first appearance.
- Target: `sum(runs.batter)` over the batter's deliveries in innings 0/1.
