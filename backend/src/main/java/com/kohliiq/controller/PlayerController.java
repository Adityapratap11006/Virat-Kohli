package com.kohliiq.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.kohliiq.dto.CareerSummaryDto;
import com.kohliiq.dto.FormatSummaryDto;
import com.kohliiq.dto.InningsEntryDto;
import com.kohliiq.dto.ContextSummaryDto;
import com.kohliiq.dto.OppositionRowDto;
import com.kohliiq.dto.PlayerDto;
import com.kohliiq.dto.VenueRowDto;
import com.kohliiq.service.AnalyticsService;
import com.kohliiq.service.PlayerService;
import com.kohliiq.service.StatsService;

@RestController
@RequestMapping("/api/players")
public class PlayerController {
    private final PlayerService players;
    private final StatsService stats;
    private final AnalyticsService analytics;

    public PlayerController(PlayerService players, StatsService stats,
                            AnalyticsService analytics) {
        this.players = players;
        this.stats = stats;
        this.analytics = analytics;
    }

    @GetMapping
    public List<PlayerDto> search(@RequestParam(required = false) String search,
                                  @RequestParam(required = false) Integer size) {
        return players.search(search, size);
    }

    @GetMapping("/{playerId}")
    public PlayerDto profile(@PathVariable Long playerId) {
        return players.profile(playerId);
    }

    @GetMapping("/{playerId}/career-summary")
    public CareerSummaryDto careerSummary(@PathVariable Long playerId,
                                          @RequestParam(required = false) String format) {
        return stats.careerSummary(playerId, format);
    }

    @GetMapping("/{playerId}/format-summary")
    public FormatSummaryDto formatSummary(@PathVariable Long playerId) {
        return stats.formatSummary(playerId);
    }

    @GetMapping("/{playerId}/recent-form")
    public List<InningsEntryDto> recentForm(@PathVariable Long playerId,
                                            @RequestParam(required = false) String format,
                                            @RequestParam(required = false) Integer limit) {
        return stats.recentForm(playerId, format, limit);
    }

    @GetMapping("/{playerId}/top-innings")
    public List<InningsEntryDto> topInnings(@PathVariable Long playerId,
                                            @RequestParam(required = false) String format,
                                            @RequestParam(required = false) Integer limit) {
        return stats.topInnings(playerId, format, limit);
    }

    @GetMapping("/{playerId}/opposition-summary")
    public List<OppositionRowDto> opposition(@PathVariable Long playerId,
                                             @RequestParam(required = false) String format) {
        return analytics.opposition(playerId, format);
    }

    @GetMapping("/{playerId}/venue-summary")
    public List<VenueRowDto> venues(@PathVariable Long playerId,
                                    @RequestParam(required = false) String format) {
        return analytics.venues(playerId, format);
    }

    @GetMapping("/{playerId}/context-summary")
    public ContextSummaryDto context(@PathVariable Long playerId,
                                     @RequestParam(required = false) String format) {
        return analytics.context(playerId, format);
    }
}
