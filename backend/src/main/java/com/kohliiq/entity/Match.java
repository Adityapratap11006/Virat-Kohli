package com.kohliiq.entity;

import java.time.LocalDate;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "matches")
public class Match {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "source_match_id", nullable = false, unique = true, length = 32)
    private String sourceMatchId;

    @Column(name = "source_file", nullable = false, length = 64)
    private String sourceFile;

    @Column(name = "format", nullable = false,
            columnDefinition = "ENUM('ODI','T20I','IPL')")
    private String format;

    @Column(name = "match_date", nullable = false)
    private LocalDate matchDate;

    @Column(name = "season", nullable = false, length = 16)
    private String season;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "venue_id", nullable = false)
    private Venue venue;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "team1_id", nullable = false)
    private Team team1;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "team2_id", nullable = false)
    private Team team2;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "toss_winner_id", nullable = false)
    private Team tossWinner;

    @Column(name = "toss_decision", nullable = false,
            columnDefinition = "ENUM('bat','field')")
    private String tossDecision;

    @Column(name = "dls_method", length = 16)
    private String dlsMethod;

    @Column(name = "event", length = 256)
    private String event;

    protected Match() {
    }

    public Long getId() {
        return id;
    }

    public String getSourceMatchId() {
        return sourceMatchId;
    }

    public String getSourceFile() {
        return sourceFile;
    }

    public String getFormat() {
        return format;
    }

    public LocalDate getMatchDate() {
        return matchDate;
    }

    public String getSeason() {
        return season;
    }

    public Venue getVenue() {
        return venue;
    }

    public Team getTeam1() {
        return team1;
    }

    public Team getTeam2() {
        return team2;
    }

    public Team getTossWinner() {
        return tossWinner;
    }

    public String getTossDecision() {
        return tossDecision;
    }

    public String getDlsMethod() {
        return dlsMethod;
    }

    public String getEvent() {
        return event;
    }
}
