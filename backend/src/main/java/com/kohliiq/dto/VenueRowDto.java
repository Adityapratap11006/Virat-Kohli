package com.kohliiq.dto;

public record VenueRowDto(
        String venue,
        String city,
        String country,
        long sourceNames,
        long innings,
        long runs,
        Double average,
        Double strikeRate,
        Integer highestScore,
        long fifties,
        long hundreds,
        long notOuts) {
}
