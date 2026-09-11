package com.kohliiq.repository;

import java.time.LocalDate;

public record CareerAggregate(
        long innings,
        long runs,
        Integer highestScore,
        long dismissals,
        long ballsFaced,
        long fifties,
        long hundreds,
        long ducks,
        LocalDate firstMatchDate,
        LocalDate lastMatchDate) {
}
