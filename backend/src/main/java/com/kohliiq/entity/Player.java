package com.kohliiq.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "players")
public class Player {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "player_code", nullable = false, unique = true, length = 64)
    private String playerCode;

    @Column(name = "display_name", nullable = false, length = 128)
    private String displayName;

    @Column(name = "has_registry_id", nullable = false)
    private Boolean hasRegistryId;

    @Column(name = "ambiguous", nullable = false)
    private Boolean ambiguous;

    protected Player() {
    }

    public Player(String playerCode, String displayName, Boolean hasRegistryId,
                  Boolean ambiguous) {
        this.playerCode = playerCode;
        this.displayName = displayName;
        this.hasRegistryId = hasRegistryId;
        this.ambiguous = ambiguous;
    }

    public Long getId() {
        return id;
    }

    public String getPlayerCode() {
        return playerCode;
    }

    public String getDisplayName() {
        return displayName;
    }

    public Boolean getHasRegistryId() {
        return hasRegistryId;
    }

    public Boolean getAmbiguous() {
        return ambiguous;
    }
}
