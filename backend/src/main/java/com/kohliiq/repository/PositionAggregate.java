package com.kohliiq.repository;

public record PositionAggregate(
        Integer position,
        long innings,
        long runs,
        long dismissals,
        long ballsFaced) {
}
