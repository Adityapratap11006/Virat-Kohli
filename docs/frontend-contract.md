# KohliIQ — Frontend Contract (Phase 4 → Phase 5)

Base: `VITE_API_BASE_URL` (dev proxied to `http://localhost:8080/api`).
Resolve Kohli at runtime: `GET /api/players?search=V Kohli`, pick the row
with `name == "V Kohli"` (registry `ba607b88`); never hard-code the numeric id.

## Shapes (all `200` unless noted)

Player: `{id: number, name: string, registryId: string | null,
ambiguous: boolean}`

Career summary: `{player, format: "ODI"|"T20I"|"IPL"|null, innings: number,
runs: number, highestScore: number|null, average: number|null,
strikeRate: number|null, notOuts: number, fifties: number, hundreds: number,
ducks: number, firstMatchDate: "YYYY-MM-DD"|null,
lastMatchDate: "YYYY-MM-DD"|null}`

Format summary: `{player, formats: [{format, innings, runs,
highestScore: number|null, average: number|null}]}` (ENUM order ODI, T20I, IPL)

Innings row (recent-form, top-innings): `{matchDate, format, opposition,
venue, runs, ballsFaced, strikeRate: number|null, inningsNo,
dismissalKind: string|null, dismissed: boolean, matchId: string}`

Match: `{matchId, format, date, season, venue, city: string|null, team1,
team2, tossWinner, tossDecision: "bat"|"field", event: string|null,
dlsMethod: string|null}`

Errors: `{timestamp, status, error, message, path}` (`400` bad format/limit,
`404` unknown player/match). Averages/rates are `null` when undefined
(never 0/NaN) — render as "–".

## Phase 6 shapes

Opposition row: `{opposition, innings, runs, average, strikeRate,
highestScore, fifties, hundreds, ducks, notOuts}` — ranked runs DESC.

Venue row: `{venue, city: string|null, innings, runs, average, strikeRate,
highestScore, fifties, hundreds, notOuts}` — ranked runs DESC; null city
renders as “city not recorded”.

Context: `{player, format, firstInnings, secondInnings, positions}` with
blocks `{label, chase, innings, runs, average, strikeRate, highestScore,
fifties, hundreds, ducks, notOuts}` (a block may be `null`) and
`positions: [{position, innings, runs, average, strikeRate}]`.

## Example

```json
{
  "player": {"id": 214, "name": "V Kohli", "registryId": "ba607b88",
             "ambiguous": false},
  "format": "ODI",
  "innings": 296,
  "runs": 14780,
  "highestScore": 183,
  "average": 59.36,
  "strikeRate": 94.01,
  "notOuts": 47,
  "fifties": 77,
  "hundreds": 54,
  "ducks": 17,
  "firstMatchDate": "2008-08-18",
  "lastMatchDate": "2026-07-19"
}
```

(Real values from the verified database; numeric ids vary per load.)
