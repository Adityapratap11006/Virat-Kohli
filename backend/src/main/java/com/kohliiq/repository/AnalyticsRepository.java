package com.kohliiq.repository;

import java.util.List;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.Repository;
import org.springframework.data.repository.query.Param;

import com.kohliiq.entity.BatterInnings;

public interface AnalyticsRepository extends Repository<BatterInnings, Long> {
    String OPP = "CASE WHEN b.battingTeam.id = m.team1.id "
            + "THEN m.team2.canonicalName ELSE m.team1.canonicalName END";

    String STATS = "COUNT(b), COALESCE(SUM(b.runs), 0), MAX(b.runs), "
            + "COALESCE(SUM(CASE WHEN b.dismissed = true THEN 1 ELSE 0 END), 0), "
            + "COALESCE(SUM(b.ballsFaced), 0), "
            + "COALESCE(SUM(CASE WHEN b.runs >= 50 AND b.runs < 100 THEN 1 ELSE 0 END), 0), "
            + "COALESCE(SUM(CASE WHEN b.runs >= 100 THEN 1 ELSE 0 END), 0), "
            + "COALESCE(SUM(CASE WHEN b.runs = 0 THEN 1 ELSE 0 END), 0)";

    @Query("SELECT new com.kohliiq.repository.OppositionAggregate(" + OPP + ", " + STATS + ") "
            + "FROM BatterInnings b JOIN b.match m "
            + "WHERE b.player.id = :playerId AND (:format IS NULL OR b.format = :format) "
            + "GROUP BY " + OPP + " "
            + "ORDER BY SUM(b.runs) DESC, COUNT(b) ASC, " + OPP + " ASC")
    List<OppositionAggregate> opposition(@Param("playerId") Long playerId,
                                         @Param("format") String format);

    @Query("SELECT new com.kohliiq.repository.VenueAggregate("
            + "v.canonicalName, v.city, " + STATS + ") "
            + "FROM BatterInnings b JOIN b.match m JOIN m.venue v "
            + "WHERE b.player.id = :playerId AND (:format IS NULL OR b.format = :format) "
            + "GROUP BY v.canonicalName, v.city "
            + "ORDER BY SUM(b.runs) DESC, COUNT(b) ASC, v.canonicalName ASC")
    List<VenueAggregate> venues(@Param("playerId") Long playerId,
                                @Param("format") String format);

    @Query("SELECT new com.kohliiq.repository.ContextAggregate("
            + "inn.inningsNo, " + STATS + ") "
            + "FROM BatterInnings b JOIN b.innings inn "
            + "WHERE b.player.id = :playerId AND (:format IS NULL OR b.format = :format) "
            + "GROUP BY inn.inningsNo")
    List<ContextAggregate> byInningsNo(@Param("playerId") Long playerId,
                                       @Param("format") String format);

    @Query("SELECT new com.kohliiq.repository.PositionAggregate("
            + "b.battingPosition, COUNT(b), COALESCE(SUM(b.runs), 0), "
            + "COALESCE(SUM(CASE WHEN b.dismissed = true THEN 1 ELSE 0 END), 0), "
            + "COALESCE(SUM(b.ballsFaced), 0)) "
            + "FROM BatterInnings b "
            + "WHERE b.player.id = :playerId AND (:format IS NULL OR b.format = :format) "
            + "AND b.battingPositionReliable = true AND b.battingPosition IS NOT NULL "
            + "GROUP BY b.battingPosition ORDER BY b.battingPosition ASC")
    List<PositionAggregate> byPosition(@Param("playerId") Long playerId,
                                       @Param("format") String format);
}
