package com.kohliiq.controller;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import com.kohliiq.dto.PlayerDto;
import com.kohliiq.exception.BadRequestException;
import com.kohliiq.exception.ResourceNotFoundException;
import com.kohliiq.service.PlayerService;
import com.kohliiq.service.StatsService;

@WebMvcTest(PlayerController.class)
class PlayerControllerTest {
    @Autowired
    private MockMvc mvc;

    @MockitoBean
    private PlayerService players;

    @MockitoBean
    private StatsService stats;

    @MockitoBean
    private com.kohliiq.service.AnalyticsService analytics;

    @Test
    void searchReturnsPlayers() throws Exception {
        when(players.search(any(), any())).thenReturn(
                List.of(new PlayerDto(1L, "V Kohli", "ba607b88", false)));
        mvc.perform(get("/api/players").param("search", "kohli"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].name").value("V Kohli"))
                .andExpect(jsonPath("$[0].registryId").value("ba607b88"));
    }

    @Test
    void missingPlayerIs404WithStableShape() throws Exception {
        when(players.profile(999L))
                .thenThrow(new ResourceNotFoundException("Player 999 not found."));
        mvc.perform(get("/api/players/999"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status").value(404))
                .andExpect(jsonPath("$.error").value("Not Found"))
                .andExpect(jsonPath("$.message").value("Player 999 not found."))
                .andExpect(jsonPath("$.stackTrace").doesNotExist());
    }

    @Test
    void invalidFormatIs400() throws Exception {
        when(stats.careerSummary(eq(1L), eq("TEST")))
                .thenThrow(new BadRequestException("Invalid format 'TEST'."));
        mvc.perform(get("/api/players/1/career-summary").param("format", "TEST"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400));
    }

    @Test
    void nonNumericIdIs400() throws Exception {
        mvc.perform(get("/api/players/abc"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400));
    }
}
