package com.kohliiq.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "deliveries")
public class Delivery {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "innings_id", nullable = false)
    private Long inningsId;

    @Column(name = "over_number", nullable = false, columnDefinition = "SMALLINT")
    private Integer overNumber;

    @Column(name = "seq_in_over", nullable = false, columnDefinition = "SMALLINT")
    private Integer seqInOver;

    @Column(name = "global_seq", nullable = false)
    private Integer globalSeq;

    @Column(name = "actual_delivery", nullable = false, length = 16)
    private String actualDelivery;

    @Column(name = "batter_id", nullable = false)
    private Long batterId;

    @Column(name = "non_striker_id", nullable = false)
    private Long nonStrikerId;

    @Column(name = "bowler_id", nullable = false)
    private Long bowlerId;

    @Column(name = "runs_batter", nullable = false, columnDefinition = "TINYINT")
    private Integer runsBatter;

    @Column(name = "runs_extras", nullable = false, columnDefinition = "TINYINT")
    private Integer runsExtras;

    @Column(name = "runs_total", nullable = false, columnDefinition = "TINYINT")
    private Integer runsTotal;

    @Column(name = "is_legal_ball", nullable = false)
    private Boolean legalBall;

    protected Delivery() {
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

    public Integer getGlobalSeq() {
        return globalSeq;
    }

    public String getActualDelivery() {
        return actualDelivery;
    }

    public Long getBatterId() {
        return batterId;
    }

    public Long getNonStrikerId() {
        return nonStrikerId;
    }

    public Long getBowlerId() {
        return bowlerId;
    }

    public Integer getRunsBatter() {
        return runsBatter;
    }

    public Integer getRunsExtras() {
        return runsExtras;
    }

    public Integer getRunsTotal() {
        return runsTotal;
    }

    public Boolean getLegalBall() {
        return legalBall;
    }
}
