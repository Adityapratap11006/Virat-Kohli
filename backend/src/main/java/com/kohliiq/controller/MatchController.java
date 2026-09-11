package com.kohliiq.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.kohliiq.dto.MatchDto;
import com.kohliiq.service.MatchService;

@RestController
@RequestMapping("/api/matches")
public class MatchController {
    private final MatchService matches;

    public MatchController(MatchService matches) {
        this.matches = matches;
    }

    @GetMapping("/{matchId}")
    public MatchDto byId(@PathVariable String matchId) {
        return matches.bySourceId(matchId);
    }
}
