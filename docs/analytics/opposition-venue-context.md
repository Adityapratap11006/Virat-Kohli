# KohliIQ — Opposition, Venue & Context Analytics (Phase 6)

All rows aggregate `batter_innings` (normal innings only, upstream).
Formulas match Phase 4 career summaries.

## Metric definitions

- **innings** — batter-innings rows in the group.
- **runs** — SUM(final runs).
- **average** — runs / dismissals, dismissals = innings − not-outs
  (`is_dismissed`). Null when never dismissed (no division by zero).
- **strikeRate** — 100 × runs / ballsFaced. Null when 0 balls.
  `balls_faced` excludes wides (ETL rule); no-balls faced count.
- **highestScore** — MAX(runs). **notOuts** — innings − dismissals.
- **fifties** — 50–99. **hundreds** — ≥100. **ducks** — exactly 0.

## Dimensions

- **opposition** — the side that did not bat in that innings:
  `CASE WHEN batting_team = team1 THEN team2 ELSE team1 END`.
  Actual DB names; no invented abbreviations.
- **venue** — match venue canonical name; `city` shown as-is, null stays
  null (“city not recorded”). Same-named grounds in different cities are
  separate rows (Phase 3 venue identity).
- **firstInnings / setting** — `innings_no = 1`.
- **secondInnings / chasing** — `innings_no = 2` (limited-overs structural
  truth; 3 Kohli chase rows lack a recorded target and are still chases).
- **positions** — `batting_position` where `batting_position_reliable`
  is true; unreliable/null positions never grouped. Kohli coverage:
  615/682 reliable, concentrated at No. 3.

## Ordering

Opposition and venue lists: runs DESC, innings ASC, name ASC (deterministic;
no “best/favourite” labels — neutral “Performance by Venue” etc.).
Positions: batting order ASC. Context blocks are fixed (first/second).

## Performance

Aggregations run in SQL (GROUP BY) over at most a few thousand rows per
player (Kohli: 682). Existing indexes used:
`batter_innings(player, format, date)`, match/venue joins via PK/FK.
No schema or index changes were needed.
