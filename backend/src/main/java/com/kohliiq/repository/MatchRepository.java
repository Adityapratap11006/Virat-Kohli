package com.kohliiq.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.kohliiq.entity.Match;

public interface MatchRepository extends JpaRepository<Match, Long> {
    Optional<Match> findBySourceMatchId(String sourceMatchId);
}
