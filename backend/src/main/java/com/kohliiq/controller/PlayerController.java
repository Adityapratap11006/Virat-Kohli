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
import com.kohliiq.dto.PlayerDto;
import com.kohliiq.service.PlayerService;
import com.kohliiq.service.StatsService;

@RestController
@RequestMapping("/api/players")
public class PlayerController {
    private final PlayerService players;
    private final StatsService stats;

    public PlayerController(PlayerService players, StatsService stats) {
        this.players = players;
        this.stats = stats;
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
}
