package com.kohliiq.service;

import java.util.List;

import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.kohliiq.dto.PlayerDto;
import com.kohliiq.entity.Player;
import com.kohliiq.exception.BadRequestException;
import com.kohliiq.exception.ResourceNotFoundException;
import com.kohliiq.repository.PlayerRepository;

@Service
@Transactional(readOnly = true)
public class PlayerService {
    private final PlayerRepository players;

    public PlayerService(PlayerRepository players) {
        this.players = players;
    }

    public List<PlayerDto> search(String query, Integer size) {
        int pageSize = QueryParams.limitOrDefault(size, 20, 50);
        String q = query == null ? "" : query.trim();
        if (q.isEmpty()) {
            return players.findAll(PageRequest.of(0, pageSize)).stream()
                    .map(PlayerDto::from).toList();
        }
        if (q.length() > 128) {
            throw new BadRequestException("Search text too long.");
        }
        return players.searchByName(q, PageRequest.of(0, pageSize)).stream()
                .map(PlayerDto::from).toList();
    }

    public Player requirePlayer(Long playerId) {
        if (playerId == null || playerId < 1) {
            throw new BadRequestException("Invalid player id.");
        }
        return players.findById(playerId).orElseThrow(
                () -> new ResourceNotFoundException("Player " + playerId + " not found."));
    }

    public PlayerDto profile(Long playerId) {
        return PlayerDto.from(requirePlayer(playerId));
    }
}
