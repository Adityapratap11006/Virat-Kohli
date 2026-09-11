package com.kohliiq.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "teams")
public class Team {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "canonical_name", nullable = false, unique = true, length = 128)
    private String canonicalName;

    protected Team() {
    }

    public Team(String canonicalName) {
        this.canonicalName = canonicalName;
    }

    public Long getId() {
        return id;
    }

    public String getCanonicalName() {
        return canonicalName;
    }
}
