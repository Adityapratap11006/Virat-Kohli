package com.kohliiq.dto;

import java.time.LocalDate;

import com.kohliiq.entity.Match;

public record MatchDto(
        String matchId,
        String format,
        LocalDate date,
        String season,
        String venue,
        String city,
        String team1,
        String team2,
        String tossWinner,
        String tossDecision,
        String event,
        String dlsMethod) {
    public static MatchDto from(Match m) {
        return new MatchDto(
                m.getSourceMatchId(), m.getFormat(), m.getMatchDate(), m.getSeason(),
                m.getVenue().getCanonicalName(), m.getVenue().getCity(),
                m.getTeam1().getCanonicalName(), m.getTeam2().getCanonicalName(),
                m.getTossWinner().getCanonicalName(), m.getTossDecision(),
                m.getEvent(), m.getDlsMethod());
    }
}
