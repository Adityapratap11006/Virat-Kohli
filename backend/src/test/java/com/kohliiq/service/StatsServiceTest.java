package com.kohliiq.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

import org.junit.jupiter.api.Test;

import com.kohliiq.dto.CareerSummaryDto;
import com.kohliiq.dto.PlayerDto;
import com.kohliiq.entity.Player;
import com.kohliiq.repository.BatterInningsRepository;
import com.kohliiq.repository.CareerAggregate;

class StatsServiceTest {
    private final PlayerService playerService = mock(PlayerService.class);
    private final BatterInningsRepository innings = mock(BatterInningsRepository.class);
    private final StatsService stats = new StatsService(playerService, innings);

    private Player player() {
        return new Player("REG:ba607b88", "V Kohli", true, false);
    }

    @Test
    void careerMathUsesDismissalsForAverage() {
        when(playerService.requirePlayer(1L)).thenReturn(player());
        when(innings.careerAggregate(eq(1L), any())).thenReturn(Optional.of(
                new CareerAggregate(3, 150, 100, 2, 120, 1, 1, 1,
                        LocalDate.of(2024, 1, 1), LocalDate.of(2024, 3, 1))));
        CareerSummaryDto dto = stats.careerSummary(1L, "ODI");
        assertEquals(3, dto.innings());
        assertEquals(150, dto.runs());
        assertEquals(100, dto.highestScore());
        assertEquals(75.0, dto.average());
        assertEquals(125.0, dto.strikeRate());
        assertEquals(1, dto.notOuts());
        assertEquals(new PlayerDto(1L, "V Kohli", "ba607b88", false).name(), dto.player().name());
    }

    @Test
    void averageNullWhenNeverDismissed() {
        when(playerService.requirePlayer(1L)).thenReturn(player());
        when(innings.careerAggregate(eq(1L), any())).thenReturn(Optional.of(
                new CareerAggregate(2, 60, 40, 0, 50, 0, 0, 0, null, null)));
        CareerSummaryDto dto = stats.careerSummary(1L, null);
        assertNull(dto.average());
        assertEquals(2, dto.notOuts());
        assertNull(dto.firstMatchDate());
    }
}
