package com.kohliiq.dto;

import java.util.List;

public record ContextSummaryDto(
        PlayerDto player,
        String format,
        StatsBlockDto firstInnings,
        StatsBlockDto secondInnings,
        List<PositionRowDto> positions) {
    public record StatsBlockDto(
            String label,
            boolean chase,
            long innings,
            long runs,
            Double average,
            Double strikeRate,
            Integer highestScore,
            long fifties,
            long hundreds,
            long ducks,
            long notOuts) {
    }

    public record PositionRowDto(
            int position,
            long innings,
            long runs,
            Double average,
            Double strikeRate) {
    }
}
