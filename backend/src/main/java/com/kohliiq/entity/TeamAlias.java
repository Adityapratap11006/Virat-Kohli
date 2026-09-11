package com.kohliiq.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "team_aliases")
public class TeamAlias {
    @Id
    @Column(name = "alias", nullable = false, length = 128)
    private String alias;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "team_id", nullable = false)
    private Team team;

    protected TeamAlias() {
    }

    public String getAlias() {
        return alias;
    }

    public Team getTeam() {
        return team;
    }
}
