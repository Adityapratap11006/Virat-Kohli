package com.kohliiq.dto;

public record OppositionRowDto(
        String opposition,
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
