package com.kohliiq.dto;

import java.time.LocalDate;

public record InningsEntryDto(
        LocalDate matchDate,
        String format,
        String opposition,
        String venue,
        int runs,
        int ballsFaced,
        Double strikeRate,
        int inningsNo,
        String dismissalKind,
        boolean dismissed,
        String matchId) {
    public static Double strikeRate(int runs, int ballsFaced) {
        if (ballsFaced <= 0) {
            return null;
        }
        return Math.round(runs * 10000.0 / ballsFaced) / 100.0;
    }
}
