-- V2: canonical venue layer. Raw `venues` rows stay immutable; each maps to
-- exactly one canonical physical venue. See docs/analytics/venue-canonicalization.md.

CREATE TABLE IF NOT EXISTS canonical_venues (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  canonical_key   VARCHAR(256) NOT NULL COMMENT 'slug of canonical name + city',
  canonical_name  VARCHAR(256) NOT NULL,
  city            VARCHAR(128) NULL,
  country         VARCHAR(128) NULL COMMENT 'null where not reliably known',
  PRIMARY KEY (id),
  UNIQUE KEY uq_canonical_key (canonical_key),
  KEY idx_canonical_name (canonical_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS venue_aliases (
  raw_venue_id        BIGINT UNSIGNED NOT NULL,
  canonical_venue_id  BIGINT UNSIGNED NOT NULL,
  mapping_type        ENUM('EXACT','NORMALIZED_ALIAS','HISTORICAL_RENAME','CURATED_ALIAS','UNRESOLVED') NOT NULL,
  confidence          VARCHAR(16) NOT NULL,
  source              VARCHAR(512) NOT NULL,
  PRIMARY KEY (raw_venue_id),
  KEY idx_alias_canonical (canonical_venue_id),
  CONSTRAINT fk_alias_raw FOREIGN KEY (raw_venue_id) REFERENCES venues (id),
  CONSTRAINT fk_alias_canonical FOREIGN KEY (canonical_venue_id) REFERENCES canonical_venues (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
