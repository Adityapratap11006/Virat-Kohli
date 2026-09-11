package com.kohliiq.entity;

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
@Table(name = "innings")
public class Innings {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "match_id", nullable = false)
    private Match match;

    @Column(name = "innings_no", nullable = false, columnDefinition = "TINYINT UNSIGNED")
    private Integer inningsNo;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "batting_team_id", nullable = false)
    private Team battingTeam;

    @Column(name = "classification", nullable = false,
            columnDefinition = "ENUM('normal','super_over','incomplete')")
    private String classification;

    @Column(name = "target_runs")
    private Integer targetRuns;

    @Column(name = "target_overs")
    private Integer targetOvers;

    protected Innings() {
    }

    public Long getId() {
        return id;
    }

    public Match getMatch() {
        return match;
    }

    public Integer getInningsNo() {
        return inningsNo;
    }

    public Team getBattingTeam() {
        return battingTeam;
    }

    public String getClassification() {
        return classification;
    }

    public Integer getTargetRuns() {
        return targetRuns;
    }

    public Integer getTargetOvers() {
        return targetOvers;
    }
}
