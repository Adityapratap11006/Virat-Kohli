-- V1: KohliIQ initial schema (MySQL 8.x, InnoDB, utf8mb4).
-- Mirrors Phase 2 processed output; see docs/database-schema.md.

CREATE TABLE IF NOT EXISTS schema_version (
  version     INT NOT NULL PRIMARY KEY,
  applied_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS players (
  id               BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  player_code      VARCHAR(64) NOT NULL COMMENT 'REG:<hex> or NAME:<normalized>',
  display_name     VARCHAR(128) NOT NULL,
  name_variants    JSON NOT NULL,
  registry_ids     JSON NOT NULL,
  has_registry_id  TINYINT(1) NOT NULL DEFAULT 0,
  ambiguous        TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'shared display name, kept separate',
  PRIMARY KEY (id),
  UNIQUE KEY uq_players_code (player_code),
  KEY idx_players_name (display_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS teams (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  canonical_name  VARCHAR(128) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_teams_canonical (canonical_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS team_aliases (
  alias    VARCHAR(128) NOT NULL COMMENT 'source spelling, e.g. Royal Challengers Bangalore',
  team_id  BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (alias),
  CONSTRAINT fk_alias_team FOREIGN KEY (team_id) REFERENCES teams (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS venues (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  canonical_name  VARCHAR(256) NOT NULL,
  city            VARCHAR(128) NULL COMMENT 'nullable: legitimately missing upstream',
  city_key        VARCHAR(128) NOT NULL DEFAULT '' COMMENT 'COALESCE(city) for uniqueness',
  name_variants   JSON NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_venues_name_city (canonical_name, city_key),
  KEY idx_venues_city (city)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS matches (
  id               BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  source_match_id  VARCHAR(32) NOT NULL COMMENT 'Cricsheet file stem',
  source_file      VARCHAR(64) NOT NULL,
  format           ENUM('ODI','T20I','IPL') NOT NULL,
  match_date       DATE NOT NULL,
  season           VARCHAR(16) NOT NULL,
  venue_id         BIGINT UNSIGNED NOT NULL,
  team1_id         BIGINT UNSIGNED NOT NULL,
  team2_id         BIGINT UNSIGNED NOT NULL,
  team1_source     VARCHAR(128) NOT NULL,
  team2_source     VARCHAR(128) NOT NULL,
  toss_winner_id   BIGINT UNSIGNED NOT NULL,
  toss_decision    ENUM('bat','field') NOT NULL,
  outcome          JSON NOT NULL,
  dls_method       VARCHAR(16) NULL,
  event            VARCHAR(256) NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_matches_source (source_match_id),
  KEY idx_matches_date (match_date),
  KEY idx_matches_format_date (format, match_date),
  KEY idx_matches_venue (venue_id),
  CONSTRAINT fk_matches_venue FOREIGN KEY (venue_id) REFERENCES venues (id),
  CONSTRAINT fk_matches_team1 FOREIGN KEY (team1_id) REFERENCES teams (id),
  CONSTRAINT fk_matches_team2 FOREIGN KEY (team2_id) REFERENCES teams (id),
  CONSTRAINT fk_matches_toss FOREIGN KEY (toss_winner_id) REFERENCES teams (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS innings (
  id               BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  match_id         BIGINT UNSIGNED NOT NULL,
  innings_no       TINYINT UNSIGNED NOT NULL,
  batting_team_id  BIGINT UNSIGNED NOT NULL,
  team_source      VARCHAR(128) NOT NULL,
  classification   ENUM('normal','super_over','incomplete') NOT NULL,
  target_runs      INT NULL,
  target_overs     INT NULL,
  had_replacement  TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uq_innings (match_id, innings_no),
  CONSTRAINT fk_innings_match FOREIGN KEY (match_id) REFERENCES matches (id),
  CONSTRAINT fk_innings_team FOREIGN KEY (batting_team_id) REFERENCES teams (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS deliveries (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  innings_id      BIGINT UNSIGNED NOT NULL,
  over_number     SMALLINT NOT NULL,
  seq_in_over     SMALLINT NOT NULL COMMENT 'disambiguates duplicated actual_delivery',
  global_seq      INT NOT NULL,
  actual_delivery VARCHAR(16) NOT NULL,
  batter_id       BIGINT UNSIGNED NOT NULL,
  non_striker_id  BIGINT UNSIGNED NOT NULL,
  bowler_id       BIGINT UNSIGNED NOT NULL,
  runs_batter     TINYINT NOT NULL COMMENT 'may exceed 6 (overthrows); never rejected',
  runs_extras     TINYINT NOT NULL,
  runs_total      TINYINT NOT NULL,
  extras          JSON NOT NULL,
  is_legal_ball   TINYINT(1) NOT NULL,
  batter_ambiguous TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY uq_delivery (innings_id, over_number, seq_in_over),
  KEY idx_deliveries_innings_seq (innings_id, global_seq),
  KEY idx_deliveries_batter (batter_id),
  KEY idx_deliveries_bowler (bowler_id),
  CONSTRAINT fk_del_innings FOREIGN KEY (innings_id) REFERENCES innings (id),
  CONSTRAINT fk_del_batter FOREIGN KEY (batter_id) REFERENCES players (id),
  CONSTRAINT fk_del_nonstriker FOREIGN KEY (non_striker_id) REFERENCES players (id),
  CONSTRAINT fk_del_bowler FOREIGN KEY (bowler_id) REFERENCES players (id),
  CONSTRAINT chk_runs_total CHECK (runs_total = runs_batter + runs_extras),
  CONSTRAINT chk_runs_nonneg CHECK (runs_batter >= 0 AND runs_extras >= 0 AND runs_total >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS wickets (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  innings_id     BIGINT UNSIGNED NOT NULL,
  over_number    SMALLINT NOT NULL,
  seq_in_over    SMALLINT NOT NULL,
  player_out_id  BIGINT UNSIGNED NOT NULL COMMENT 'independent of batter',
  kind           VARCHAR(32) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_wicket (innings_id, over_number, seq_in_over, player_out_id, kind),
  CONSTRAINT fk_wicket_delivery FOREIGN KEY (innings_id, over_number, seq_in_over)
    REFERENCES deliveries (innings_id, over_number, seq_in_over),
  CONSTRAINT fk_wicket_player FOREIGN KEY (player_out_id) REFERENCES players (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS batter_innings (
  id                        BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  player_id                 BIGINT UNSIGNED NOT NULL,
  match_id                  BIGINT UNSIGNED NOT NULL,
  innings_id                BIGINT UNSIGNED NOT NULL,
  batting_team_id           BIGINT UNSIGNED NOT NULL,
  match_date                DATE NOT NULL COMMENT 'denormalized for chronological ML retrieval',
  format                    ENUM('ODI','T20I','IPL') NOT NULL COMMENT 'denormalized for filtering',
  batting_position          SMALLINT NULL COMMENT 'nullable: unreliable positions not forced',
  batting_position_reliable TINYINT(1) NOT NULL DEFAULT 0,
  runs                      SMALLINT NOT NULL COMMENT 'target: final runs at entry prediction',
  balls_faced               SMALLINT NOT NULL,
  dismissal_kind            VARCHAR(32) NULL,
  is_dismissed              TINYINT(1) NOT NULL,
  entry_team_runs           INT NOT NULL,
  entry_wickets_lost        SMALLINT NOT NULL,
  entry_balls_bowled        SMALLINT NOT NULL,
  entry_balls_remaining     SMALLINT NOT NULL,
  chase_target              INT NULL,
  dls_method                VARCHAR(16) NULL,
  source_file               VARCHAR(64) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_batter_innings (player_id, match_id, innings_id),
  KEY idx_bi_player_date (player_id, match_date),
  KEY idx_bi_player_format_date (player_id, format, match_date),
  KEY idx_bi_match_innings (match_id, innings_id),
  CONSTRAINT fk_bi_player FOREIGN KEY (player_id) REFERENCES players (id),
  CONSTRAINT fk_bi_match FOREIGN KEY (match_id) REFERENCES matches (id),
  CONSTRAINT fk_bi_innings FOREIGN KEY (innings_id) REFERENCES innings (id),
  CONSTRAINT fk_bi_team FOREIGN KEY (batting_team_id) REFERENCES teams (id),
  CONSTRAINT chk_bi_nonneg CHECK (runs >= 0 AND balls_faced >= 0 AND entry_team_runs >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
