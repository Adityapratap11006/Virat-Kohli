# KohliIQ — Backend API (Phase 4)

Base URL (dev): `http://localhost:8080`. All responses JSON. Errors use a
stable shape: `{timestamp, status, error, message, path}` — no stack traces,
no SQL leakage. IDs below are database surrogate keys (`players.id`).

## Players

### `GET /api/players?search=&size=`

- `search` optional (case-insensitive substring on display name; blank/missing
  returns first page). Max 128 chars.
- `size` default 20, max 50.
- `200 [{id, name, registryId, ambiguous}]` — `registryId` is the Cricsheet
  hex id without the `REG:` prefix (null when name-resolved); `ambiguous`
  marks shared display names kept as separate entities.

### `GET /api/players/{playerId}`

- `200 {id, name, registryId, ambiguous}`; unknown id → `404`.

### `GET /api/players/{playerId}/career-summary?format=`

- `format` optional; `ODI`/`T20I`/`IPL` (case-insensitive), else `400`.
- Aggregated in SQL from `batter_innings` (normal innings only, upstream):
  `innings` = rows; `runs` = SUM; `highestScore` = MAX; `average` =
  runs/dismissals (`is_dismissed` count, null when never dismissed);
  `strikeRate` = 100·runs/balls (null when 0 balls); `notOuts` =
  innings − dismissals; `fifties` = 50–99; `hundreds` = ≥100; `ducks` = 0;
  `firstMatchDate`/`lastMatchDate` = MIN/MAX date. `format` echoes the filter
  (null = all formats). A player with no rows gets zeros/nulls (`200`).

### `GET /api/players/{playerId}/format-summary`

- One row per played format (DB ENUM order: ODI, T20I, IPL):
  `[{format, innings, runs, highestScore, average}]`.

### `GET /api/players/{playerId}/recent-form?format=&limit=`

- `limit` default 10, 1–100. Newest first (`match_date DESC`).
- Rows: `{matchDate, format, opposition, venue, runs, ballsFaced,
  strikeRate, inningsNo, dismissalKind, dismissed, matchId}` where
  `opposition` is the non-batting side and `matchId` is the Cricsheet source id.

### `GET /api/players/{playerId}/top-innings?format=&limit=`

- “Top Knocks by Runs” — sorted `runs DESC, ballsFaced ASC, matchDate DESC`.
  Same row shape as recent-form.

## Matches

### `GET /api/matches/{matchId}`

- `{matchId}` is the Cricsheet source id (e.g. `1000887`).
- `200 {matchId, format, date, season, venue, city, team1, team2,
  tossWinner, tossDecision, event, dlsMethod}`; unknown → `404`.
- Minimal by design; full match analytics is a later slice.

## Validation summary

Bad format value → `400`; limit/size out of range → `400`; unknown player or
match → `404`; non-numeric player id → `400`.

## Deferred (later slices)

Opposition/venue/phase analytics, rolling ML features, prediction endpoints,
RAE/Impact Index, comparison/similarity, auth. CORS allows `GET` from
`http://localhost:5173` (configurable via `kohliiq.cors.allowed-origins`).
