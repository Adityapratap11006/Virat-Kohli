package com.kohliiq.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "venue_aliases")
public class VenueAlias {
    @Id
    @Column(name = "raw_venue_id", nullable = false)
    private Long rawVenueId;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "canonical_venue_id", nullable = false)
    private CanonicalVenue canonicalVenue;

    @Column(name = "mapping_type", nullable = false,
            columnDefinition = "ENUM('EXACT','NORMALIZED_ALIAS','HISTORICAL_RENAME','CURATED_ALIAS','UNRESOLVED')")
    private String mappingType;

    protected VenueAlias() {
    }

    public Long getRawVenueId() {
        return rawVenueId;
    }

    public CanonicalVenue getCanonicalVenue() {
        return canonicalVenue;
    }

    public String getMappingType() {
        return mappingType;
    }
}
