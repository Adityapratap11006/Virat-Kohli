package com.kohliiq.service;

import java.util.List;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.kohliiq.dto.ContextSummaryDto;
import com.kohliiq.dto.OppositionRowDto;
import com.kohliiq.dto.VenueRowDto;
import com.kohliiq.repository.AnalyticsRepository;
import com.kohliiq.repository.ContextAggregate;

@Service
@Transactional(readOnly = true)
public class AnalyticsService {
    private final PlayerService playerService;
    private final AnalyticsRepository analytics;

    public AnalyticsService(PlayerService playerService,
                            AnalyticsRepository analytics) {
        this.playerService = playerService;
        this.analytics = analytics;
    }

    public List<OppositionRowDto> opposition(Long playerId, String format) {
        playerService.requirePlayer(playerId);
        String fmt = QueryParams.formatOrNull(format);
        return analytics.opposition(playerId, fmt).stream()
                .map(a -> new OppositionRowDto(a.opposition(), a.innings(), a.runs(),
                        StatsService.average(a.runs(), a.dismissals()),
                        StatsService.strikeRate(a.runs(), a.ballsFaced()),
                        a.highestScore(), a.fifties(), a.hundreds(), a.ducks(),
                        a.innings() - a.dismissals()))
                .toList();
    }

    public List<VenueRowDto> venues(Long playerId, String format) {
        playerService.requirePlayer(playerId);
        String fmt = QueryParams.formatOrNull(format);
        return analytics.venues(playerId, fmt).stream()
                .map(a -> new VenueRowDto(a.venue(), a.city(), a.innings(), a.runs(),
                        StatsService.average(a.runs(), a.dismissals()),
                        StatsService.strikeRate(a.runs(), a.ballsFaced()),
                        a.highestScore(), a.fifties(), a.hundreds(),
                        a.innings() - a.dismissals()))
                .toList();
    }

    public ContextSummaryDto context(Long playerId, String format) {
        var player = playerService.requirePlayer(playerId);
        String fmt = QueryParams.formatOrNull(format);
        ContextSummaryDto.StatsBlockDto first = null;
        ContextSummaryDto.StatsBlockDto second = null;
        for (ContextAggregate a : analytics.byInningsNo(playerId, fmt)) {
            var block = new ContextSummaryDto.StatsBlockDto(
                    a.inningsNo() == 1 ? "First innings" : "Second innings",
                    a.inningsNo() == 2, a.innings(), a.runs(),
                    StatsService.average(a.runs(), a.dismissals()),
                    StatsService.strikeRate(a.runs(), a.ballsFaced()),
                    a.highestScore(), a.fifties(), a.hundreds(), a.ducks(),
                    a.innings() - a.dismissals());
            if (a.inningsNo() == 1) {
                first = block;
            } else if (a.inningsNo() == 2) {
                second = block;
            }
        }
        List<ContextSummaryDto.PositionRowDto> positions = analytics
                .byPosition(playerId, fmt).stream()
                .map(p -> new ContextSummaryDto.PositionRowDto(p.position(), p.innings(),
                        p.runs(), StatsService.average(p.runs(), p.dismissals()),
                        StatsService.strikeRate(p.runs(), p.ballsFaced())))
                .toList();
        return new ContextSummaryDto(
                com.kohliiq.dto.PlayerDto.from(player), fmt, first, second, positions);
    }
}
