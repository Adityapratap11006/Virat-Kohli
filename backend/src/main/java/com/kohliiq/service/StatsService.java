package com.kohliiq.service;

import java.util.List;

import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.kohliiq.dto.CareerSummaryDto;
import com.kohliiq.dto.FormatSummaryDto;
import com.kohliiq.dto.InningsEntryDto;
import com.kohliiq.dto.PlayerDto;
import com.kohliiq.entity.BatterInnings;
import com.kohliiq.entity.Match;
import com.kohliiq.repository.BatterInningsRepository;
import com.kohliiq.repository.CareerAggregate;

@Service
@Transactional(readOnly = true)
public class StatsService {
    private final PlayerService playerService;
    private final BatterInningsRepository innings;

    public StatsService(PlayerService playerService,
                        BatterInningsRepository innings) {
        this.playerService = playerService;
        this.innings = innings;
    }

    public CareerSummaryDto careerSummary(Long playerId, String format) {
        var player = playerService.requirePlayer(playerId);
        String fmt = QueryParams.formatOrNull(format);
        CareerAggregate agg = innings.careerAggregate(playerId, fmt)
                .orElseThrow(() -> new IllegalStateException("Aggregate query failed"));
        return new CareerSummaryDto(PlayerDto.from(player), fmt, agg.innings(),
                agg.runs(), agg.highestScore(), average(agg.runs(), agg.dismissals()),
                strikeRate(agg.runs(), agg.ballsFaced()),
                agg.innings() - agg.dismissals(), agg.fifties(), agg.hundreds(),
                agg.ducks(), agg.firstMatchDate(), agg.lastMatchDate());
    }

    public FormatSummaryDto formatSummary(Long playerId) {
        var player = playerService.requirePlayer(playerId);
        List<FormatSummaryDto.PerFormatDto> rows = innings.formatAggregate(playerId)
                .stream()
                .map(r -> new FormatSummaryDto.PerFormatDto((String) r[0],
                        (Long) r[1], (Long) r[2], (Integer) r[3],
                        average((Long) r[2], (Long) r[4])))
                .toList();
        return new FormatSummaryDto(PlayerDto.from(player), rows);
    }

    public List<InningsEntryDto> recentForm(Long playerId, String format, Integer limit) {
        playerService.requirePlayer(playerId);
        String fmt = QueryParams.formatOrNull(format);
        int n = QueryParams.limitOrDefault(limit, 10, 100);
        return innings.recentForm(playerId, fmt, PageRequest.of(0, n)).stream()
                .map(this::toEntry).toList();
    }

    public List<InningsEntryDto> topInnings(Long playerId, String format, Integer limit) {
        playerService.requirePlayer(playerId);
        String fmt = QueryParams.formatOrNull(format);
        int n = QueryParams.limitOrDefault(limit, 10, 100);
        return innings.topInnings(playerId, fmt, PageRequest.of(0, n)).stream()
                .map(this::toEntry).toList();
    }

    private InningsEntryDto toEntry(BatterInnings b) {
        Match m = b.getMatch();
        String opposition = b.getBattingTeam().getId().equals(m.getTeam1().getId())
                ? m.getTeam2().getCanonicalName()
                : m.getTeam1().getCanonicalName();
        return new InningsEntryDto(b.getMatchDate(), b.getFormat(), opposition,
                m.getVenue().getCanonicalName(), b.getRuns(), b.getBallsFaced(),
                InningsEntryDto.strikeRate(b.getRuns(), b.getBallsFaced()),
                b.getInnings().getInningsNo(), b.getDismissalKind(),
                Boolean.TRUE.equals(b.getDismissed()), m.getSourceMatchId());
    }

    static Double average(long runs, long dismissals) {
        if (dismissals <= 0) {
            return null;
        }
        return Math.round(runs * 100.0 / dismissals) / 100.0;
    }

    static Double strikeRate(long runs, long balls) {
        if (balls <= 0) {
            return null;
        }
        return Math.round(runs * 10000.0 / balls) / 100.0;
    }
}
