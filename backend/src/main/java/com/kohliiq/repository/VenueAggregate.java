package com.kohliiq.repository;

public record VenueAggregate(
        String venue,
        String city,
        String country,
        long sourceNames,
        long innings,
        long runs,
        Integer highestScore,
        long dismissals,
        long ballsFaced,
        long fifties,
        long hundreds,
        long ducks) {
}
