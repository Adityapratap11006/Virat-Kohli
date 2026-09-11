package com.kohliiq.repository;

public record OppositionAggregate(
        String opposition,
        long innings,
        long runs,
        Integer highestScore,
        long dismissals,
        long ballsFaced,
        long fifties,
        long hundreds,
        long ducks) {
}
