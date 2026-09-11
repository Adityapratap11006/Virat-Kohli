package com.kohliiq.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "venues")
public class Venue {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "canonical_name", nullable = false, length = 256)
    private String canonicalName;

    @Column(name = "city", length = 128)
    private String city;

    protected Venue() {
    }

    public Venue(String canonicalName, String city) {
        this.canonicalName = canonicalName;
        this.city = city;
    }

    public Long getId() {
        return id;
    }

    public String getCanonicalName() {
        return canonicalName;
    }

    public String getCity() {
        return city;
    }
}
