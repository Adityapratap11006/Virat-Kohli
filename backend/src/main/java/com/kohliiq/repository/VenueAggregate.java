package com.kohliiq.repository;

public record VenueAggregate(
        String venue,
        String city,
        long innings,
        long runs,
        Integer highestScore,
        long dismissals,
        long ballsFaced,
        long fifties,
        long hundreds,
        long ducks) {
}
