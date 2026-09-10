# KohliIQ — Database Schema (Phase 3)

MySQL 8.x, InnoDB, `utf8mb4_0900_ai_ci`, strict mode. Migration `V1`
(`db/migrations/V1__initial_schema.sql`), tracked in `schema_version`.
Mirrors Phase 2 processed output 1:1 — no invented fields.

## Tables

- **players** — `player_code` UNIQUE (`REG:<hex>` or `NAME:<norm>`),
  `display_name`, `name_variants`/`registry_ids` (JSON), `ambiguous` flag.
  Ambiguous shared-name identities stay separate rows.
- **teams** — `canonical_name` UNIQUE. **team_aliases** — source spelling →
  team (4 approved renames; Deccan/SRH unmerged).
- **venues** — UNIQUE (`canonical_name`, `city_key`); `city` nullable
  (legitimately missing upstream); multi-city generic names (e.g. National
  Stadium Karachi vs Hamilton) stored as separate rows. 486 rows.
- **matches** — UNIQUE `source_match_id` (Cricsheet stem); `source_file`;
  format ENUM; date/season; FKs to venue, both teams, toss winner
  (canonicalized, validated); `outcome` JSON; `dls_method`; `event`.
- **innings** — UNIQUE (`match_id`, `innings_no`); batting-team FK + source
  spelling; `classification` ENUM (`normal`/`super_over`/`incomplete`);
  chase `target_*`; `had_replacement`.
- **deliveries** — UNIQUE (`innings_id`, `over_number`, `seq_in_over`)
  (never over+ball alone); `global_seq`; `actual_delivery` preserved;
  batter/non-striker/bowler FKs; runs columns with
  `CHECK (runs_total = runs_batter + runs_extras)` and non-negativity —
  no `runs_batter <= 6` rule; `extras` JSON; `batter_ambiguous`.
- **wickets** — one row per wicket event; composite FK to the delivery
  triple; `player_out_id` FK (independent of batter); UNIQUE on
  (delivery triple, player_out, kind).
- **batter_innings** — UNIQUE (`player_id`, `match_id`, `innings_id`);
  nullable `batting_position` + reliability flag; runs/balls/dismissal;
  entry context (`entry_team_runs/wickets_lost/balls_bowled/balls_remaining`,
  `chase_target`); `match_date` + `format` intentionally denormalized for
  chronological ML retrieval; `source_file` provenance.

## Nullability

`venues.city`, `batting_position`, `dismissal_kind`, `chase_target`,
`target_*`, `dls_method`, `event` are nullable by design (upstream
missingness). Everything else required is NOT NULL + FK/UNIQUE/CHECK.
