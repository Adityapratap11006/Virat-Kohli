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
@Table(name = "batter_innings")
public class BatterInnings {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "player_id", nullable = false)
    private Player player;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "match_id", nullable = false)
    private Match match;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "innings_id", nullable = false)
    private Innings innings;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "batting_team_id", nullable = false)
    private Team battingTeam;

    @Column(name = "match_date", nullable = false)
    private LocalDate matchDate;

    @Column(name = "format", nullable = false, columnDefinition = "ENUM('ODI','T20I','IPL')")
    private String format;

    @Column(name = "batting_position", columnDefinition = "SMALLINT")
    private Integer battingPosition;

    @Column(name = "batting_position_reliable", nullable = false)
    private Boolean battingPositionReliable;

    @Column(name = "runs", nullable = false, columnDefinition = "SMALLINT")
    private Integer runs;

    @Column(name = "balls_faced", nullable = false, columnDefinition = "SMALLINT")
    private Integer ballsFaced;

    @Column(name = "dismissal_kind", length = 32)
    private String dismissalKind;

    @Column(name = "is_dismissed", nullable = false)
    private Boolean dismissed;

    @Column(name = "entry_team_runs", nullable = false)
    private Integer entryTeamRuns;

    @Column(name = "entry_wickets_lost", nullable = false, columnDefinition = "SMALLINT")
    private Integer entryWicketsLost;

    @Column(name = "entry_balls_bowled", nullable = false, columnDefinition = "SMALLINT")
    private Integer entryBallsBowled;

    @Column(name = "entry_balls_remaining", nullable = false, columnDefinition = "SMALLINT")
    private Integer entryBallsRemaining;

    @Column(name = "chase_target")
    private Integer chaseTarget;

    @Column(name = "dls_method", length = 16)
    private String dlsMethod;

    protected BatterInnings() {
    }

    public BatterInnings(Player player, Match match, Innings innings, Team battingTeam,
                         LocalDate matchDate, String format, Integer runs,
                         Integer ballsFaced, Boolean dismissed) {
        this.player = player;
        this.match = match;
        this.innings = innings;
        this.battingTeam = battingTeam;
        this.matchDate = matchDate;
        this.format = format;
        this.runs = runs;
        this.ballsFaced = ballsFaced;
        this.dismissed = dismissed;
        this.battingPositionReliable = false;
        this.entryTeamRuns = 0;
        this.entryWicketsLost = 0;
        this.entryBallsBowled = 0;
        this.entryBallsRemaining = 0;
    }

    public Long getId() {
        return id;
    }

    public Player getPlayer() {
        return player;
    }

    public Match getMatch() {
        return match;
    }

    public Innings getInnings() {
        return innings;
    }

    public Team getBattingTeam() {
        return battingTeam;
    }

    public LocalDate getMatchDate() {
        return matchDate;
    }

    public String getFormat() {
        return format;
    }

    public Integer getBattingPosition() {
        return battingPosition;
    }

    public Boolean getBattingPositionReliable() {
        return battingPositionReliable;
    }

    public Integer getRuns() {
        return runs;
    }

    public Integer getBallsFaced() {
        return ballsFaced;
    }

    public String getDismissalKind() {
        return dismissalKind;
    }

    public void setDismissalKind(String dismissalKind) {
        this.dismissalKind = dismissalKind;
    }

    public Boolean getDismissed() {
        return dismissed;
    }

    public Integer getEntryTeamRuns() {
        return entryTeamRuns;
    }

    public Integer getEntryWicketsLost() {
        return entryWicketsLost;
    }

    public Integer getEntryBallsBowled() {
        return entryBallsBowled;
    }

    public Integer getEntryBallsRemaining() {
        return entryBallsRemaining;
    }

    public Integer getChaseTarget() {
        return chaseTarget;
    }

    public String getDlsMethod() {
        return dlsMethod;
    }
}
