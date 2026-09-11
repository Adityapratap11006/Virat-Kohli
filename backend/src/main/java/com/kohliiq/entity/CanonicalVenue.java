package com.kohliiq.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "canonical_venues")
public class CanonicalVenue {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "canonical_key", nullable = false, unique = true, length = 256)
    private String canonicalKey;

    @Column(name = "canonical_name", nullable = false, length = 256)
    private String canonicalName;

    @Column(name = "city", length = 128)
    private String city;

    @Column(name = "country", length = 128)
    private String country;

    protected CanonicalVenue() {
    }

    public Long getId() {
        return id;
    }

    public String getCanonicalKey() {
        return canonicalKey;
    }

    public String getCanonicalName() {
        return canonicalName;
    }

    public String getCity() {
        return city;
    }

    public String getCountry() {
        return country;
    }
}
