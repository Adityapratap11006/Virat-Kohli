package com.kohliiq.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "wickets")
public class Wicket {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "innings_id", nullable = false)
    private Long inningsId;

    @Column(name = "over_number", nullable = false, columnDefinition = "SMALLINT")
    private Integer overNumber;

    @Column(name = "seq_in_over", nullable = false, columnDefinition = "SMALLINT")
    private Integer seqInOver;

    @Column(name = "player_out_id", nullable = false)
    private Long playerOutId;

    @Column(name = "kind", nullable = false, length = 32)
    private String kind;

    protected Wicket() {
    }

    public Long getId() {
        return id;
    }

    public Long getInningsId() {
        return inningsId;
    }

    public Integer getOverNumber() {
        return overNumber;
    }

    public Integer getSeqInOver() {
        return seqInOver;
    }

    public Long getPlayerOutId() {
        return playerOutId;
    }

    public String getKind() {
        return kind;
    }
}
