package com.kohliiq.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import com.kohliiq.entity.BatterInnings;

public interface BatterInningsRepository extends JpaRepository<BatterInnings, Long> {
    String AGG_SELECT = "SELECT new com.kohliiq.repository.CareerAggregate("
            + "COUNT(b), COALESCE(SUM(b.runs), 0), MAX(b.runs), "
            + "COALESCE(SUM(CASE WHEN b.dismissed = true THEN 1 ELSE 0 END), 0), "
            + "COALESCE(SUM(b.ballsFaced), 0), "
            + "COALESCE(SUM(CASE WHEN b.runs >= 50 AND b.runs < 100 THEN 1 ELSE 0 END), 0), "
            + "COALESCE(SUM(CASE WHEN b.runs >= 100 THEN 1 ELSE 0 END), 0), "
            + "COALESCE(SUM(CASE WHEN b.runs = 0 THEN 1 ELSE 0 END), 0), "
            + "MIN(b.matchDate), MAX(b.matchDate)) "
            + "FROM BatterInnings b WHERE b.player.id = :playerId";

    @Query(AGG_SELECT + " AND (:format IS NULL OR b.format = :format)")
    Optional<CareerAggregate> careerAggregate(@Param("playerId") Long playerId,
                                              @Param("format") String format);

    @Query("SELECT b.format, COUNT(b), COALESCE(SUM(b.runs), 0), MAX(b.runs), "
            + "SUM(CASE WHEN b.dismissed = true THEN 1 ELSE 0 END) "
            + "FROM BatterInnings b WHERE b.player.id = :playerId "
            + "GROUP BY b.format ORDER BY b.format")
    List<Object[]> formatAggregate(@Param("playerId") Long playerId);

    @Query("SELECT b FROM BatterInnings b "
            + "JOIN FETCH b.match m JOIN FETCH m.venue JOIN FETCH m.team1 "
            + "JOIN FETCH m.team2 JOIN FETCH b.battingTeam "
            + "WHERE b.player.id = :playerId "
            + "AND (:format IS NULL OR b.format = :format) "
            + "ORDER BY b.matchDate DESC, b.id DESC")
    List<BatterInnings> recentForm(@Param("playerId") Long playerId,
                                   @Param("format") String format,
                                   Pageable pageable);

    @Query("SELECT b FROM BatterInnings b "
            + "JOIN FETCH b.match m JOIN FETCH m.venue JOIN FETCH m.team1 "
            + "JOIN FETCH m.team2 JOIN FETCH b.battingTeam "
            + "WHERE b.player.id = :playerId "
            + "AND (:format IS NULL OR b.format = :format) "
            + "ORDER BY b.runs DESC, b.ballsFaced ASC, b.matchDate DESC")
    List<BatterInnings> topInnings(@Param("playerId") Long playerId,
                                   @Param("format") String format,
                                   Pageable pageable);
}
