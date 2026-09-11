package com.kohliiq.repository;

public record ContextAggregate(
        Integer inningsNo,
        long innings,
        long runs,
        Integer highestScore,
        long dismissals,
        long ballsFaced,
        long fifties,
        long hundreds,
        long ducks) {
}
