package com.kohliiq.dto;

import java.time.LocalDate;

public record CareerSummaryDto(
        PlayerDto player,
        String format,
        long innings,
        long runs,
        Integer highestScore,
        Double average,
        Double strikeRate,
        long notOuts,
        long fifties,
        long hundreds,
        long ducks,
        LocalDate firstMatchDate,
        LocalDate lastMatchDate) {
}
