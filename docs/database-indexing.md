# KohliIQ — Indexing (Phase 3)

One secondary index per documented query pattern; no blanket indexing.

| Index | Serves |
|---|---|
| `matches(match_date)` | date-range scans |
| `matches(format, match_date)` | format + chronological (ML splits, career views) |
| `matches(venue_id)` | venue + format joins |
| `players(display_name)` | name lookup |
| `venues(city)` | city filtering |
| `deliveries(innings_id, global_seq)` | innings replay in order (entry-state verification) |
| `deliveries(batter_id)` / `(bowler_id)` | player delivery retrieval |
| `batter_innings(player_id, match_date)` | career innings chronological |
| `batter_innings(player_id, format, match_date)` | player + format |
| `batter_innings(match_id, innings_id)` | match/innings drill-down |

UNIQUE keys double as indexes (`uq_matches_source`, `uq_innings`,
`uq_delivery`, `uq_batter_innings`, `uq_players_code`, `uq_teams_canonical`,
`uq_venues_name_city`, `uq_wicket`). `wickets` has an explicit delivery-triple
key for the composite FK. No full-text or covering indexes in V1.
