package com.kohliiq.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.kohliiq.dto.MatchDto;
import com.kohliiq.exception.BadRequestException;
import com.kohliiq.exception.ResourceNotFoundException;
import com.kohliiq.repository.MatchRepository;

@Service
@Transactional(readOnly = true)
public class MatchService {
    private final MatchRepository matches;

    public MatchService(MatchRepository matches) {
        this.matches = matches;
    }

    public MatchDto bySourceId(String matchId) {
        if (matchId == null || matchId.isBlank() || matchId.length() > 32) {
            throw new BadRequestException("Invalid match id.");
        }
        return matches.findBySourceMatchId(matchId.trim())
                .map(MatchDto::from)
                .orElseThrow(() -> new ResourceNotFoundException(
                        "Match " + matchId + " not found."));
    }
}
