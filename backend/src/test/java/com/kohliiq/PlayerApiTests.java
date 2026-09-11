package com.kohliiq;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.test.web.servlet.MockMvc;

@AutoConfigureMockMvc
class PlayerApiTests extends ContainerBase {
    @Autowired
    private MockMvc mvc;

    private long kohliId;

    @BeforeEach
    void fixture() {
        jdbc.execute("SET FOREIGN_KEY_CHECKS=0");
        for (String t : new String[]{"batter_innings", "wickets", "deliveries",
                "innings", "matches", "team_aliases", "venues", "teams", "players"}) {
            jdbc.execute("TRUNCATE TABLE " + t);
        }
        jdbc.execute("SET FOREIGN_KEY_CHECKS=1");

        jdbc.update("INSERT INTO teams (canonical_name) VALUES ('India'),('Australia')");
        jdbc.update("INSERT INTO venues (canonical_name, city, city_key, name_variants) "
                + "VALUES ('Test Ground','Test City','Test City','[]')");
        jdbc.update("INSERT INTO players (player_code, display_name, name_variants,"
                + " registry_ids, has_registry_id, ambiguous) VALUES "
                + "('REG:ba607b88','V Kohli','[]','[]',1,0),"
                + "('REG:40caa465','T Kohli','[]','[]',1,0)");
        kohliId = jdbc.queryForObject(
                "SELECT id FROM players WHERE player_code='REG:ba607b88'", Long.class);
        long india = jdbc.queryForObject(
                "SELECT id FROM teams WHERE canonical_name='India'", Long.class);
        long aus = jdbc.queryForObject(
                "SELECT id FROM teams WHERE canonical_name='Australia'", Long.class);
        long venue = jdbc.queryForObject("SELECT id FROM venues LIMIT 1", Long.class);

        addMatch("M100", "ODI", "2024-01-10", india, aus, venue, india);
        addMatch("M101", "ODI", "2024-01-20", india, aus, venue, aus);
        addMatch("M200", "T20I", "2024-02-10", india, aus, venue, india);
        addMatch("M300", "IPL", "2024-03-10", india, aus, venue, aus);

        // V Kohli: ODI 100(90) + 30(25); T20I 50*(40); IPL 0(2)
        addInnings(kohliId, "M100", 1, india, "ODI", "2024-01-10", 100, 90, true, "bowled");
        addInnings(kohliId, "M101", 1, india, "ODI", "2024-01-20", 30, 25, true, "caught");
        addInnings(kohliId, "M200", 1, india, "T20I", "2024-02-10", 50, 40, false, null);
        addInnings(kohliId, "M300", 1, india, "IPL", "2024-03-10", 0, 2, true, "bowled");
        // T Kohli: no innings (zero-state player)
    }

    private void addMatch(String sourceId, String format, String date, long t1,
                          long t2, long venue, long toss) {
        jdbc.update("INSERT INTO matches (source_match_id, source_file, format,"
                + " match_date, season, venue_id, team1_id, team2_id, team1_source,"
                + " team2_source, toss_winner_id, toss_decision, outcome) VALUES "
                + "(?,?,?,?,'2024',?,?,?,?,?,?,'bat','{}')",
                sourceId, sourceId + ".json", format, date, venue, t1, t2,
                "T1", "T2", toss);
        long mid = jdbc.queryForObject(
                "SELECT id FROM matches WHERE source_match_id=?", Long.class, sourceId);
        jdbc.update("INSERT INTO innings (match_id, innings_no, batting_team_id,"
                + " team_source, classification) VALUES (?,?,?,'T','normal')",
                mid, 1, t1);
        jdbc.update("INSERT INTO innings (match_id, innings_no, batting_team_id,"
                + " team_source, classification) VALUES (?,?,?,'T','normal')",
                mid, 2, t2);
    }

    private void addInnings(long player, String sourceId, int ino, long team,
                            String format, String date, int runs, int balls,
                            boolean dismissed, String kind) {
        long iid = jdbc.queryForObject(
                "SELECT i.id FROM innings i JOIN matches m ON m.id=i.match_id "
                        + "WHERE m.source_match_id=? AND i.innings_no=?",
                Long.class, sourceId, ino);
        long mid = jdbc.queryForObject(
                "SELECT id FROM matches WHERE source_match_id=?", Long.class, sourceId);
        jdbc.update("INSERT INTO batter_innings (player_id, match_id, innings_id,"
                + " batting_team_id, match_date, format, batting_position_reliable,"
                + " runs, balls_faced, dismissal_kind, is_dismissed, entry_team_runs,"
                + " entry_wickets_lost, entry_balls_bowled, entry_balls_remaining,"
                + " source_file) VALUES (?,?,?,?,?,?,0,?,?,?,?,0,0,120,120,?)",
                player, mid, iid, team, date, format, runs, balls, kind,
                dismissed ? 1 : 0, sourceId + ".json");
    }

    @Test
    void kohliResolvesThroughDatabase() throws Exception {
        mvc.perform(get("/api/players").param("search", "V Kohli"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(1))
                .andExpect(jsonPath("$[0].name").value("V Kohli"))
                .andExpect(jsonPath("$[0].registryId").value("ba607b88"));
    }

    @Test
    void careerSummaryAllFormats() throws Exception {
        mvc.perform(get("/api/players/" + kohliId + "/career-summary"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.innings").value(4))
                .andExpect(jsonPath("$.runs").value(180))
                .andExpect(jsonPath("$.highestScore").value(100))
                .andExpect(jsonPath("$.average").value(60.0))
                .andExpect(jsonPath("$.fifties").value(1))
                .andExpect(jsonPath("$.hundreds").value(1))
                .andExpect(jsonPath("$.ducks").value(1));
    }

    @Test
    void careerSummaryOdiOnly() throws Exception {
        mvc.perform(get("/api/players/" + kohliId + "/career-summary")
                        .param("format", "ODI"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.format").value("ODI"))
                .andExpect(jsonPath("$.innings").value(2))
                .andExpect(jsonPath("$.runs").value(130))
                .andExpect(jsonPath("$.average").value(65.0));
    }

    @Test
    void careerSummaryUndefeatedAverageIsNull() throws Exception {
        mvc.perform(get("/api/players/" + kohliId + "/career-summary")
                        .param("format", "T20I"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.innings").value(1))
                .andExpect(jsonPath("$.average").value(org.hamcrest.Matchers.nullValue()))
                .andExpect(jsonPath("$.notOuts").value(1));
    }

    @Test
    void formatSummaryListsOnlyPlayedFormats() throws Exception {
        mvc.perform(get("/api/players/" + kohliId + "/format-summary"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.formats.length()").value(3))
                .andExpect(jsonPath("$.formats[0].format").value("ODI"))
                .andExpect(jsonPath("$.formats[1].format").value("T20I"))
                .andExpect(jsonPath("$.formats[2].format").value("IPL"));
    }

    @Test
    void recentFormIsChronologicalAndLimited() throws Exception {
        mvc.perform(get("/api/players/" + kohliId + "/recent-form")
                        .param("limit", "2"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.length()").value(2))
                .andExpect(jsonPath("$[0].matchDate").value("2024-03-10"))
                .andExpect(jsonPath("$[0].runs").value(0))
                .andExpect(jsonPath("$[1].matchDate").value("2024-02-10"))
                .andExpect(jsonPath("$[1].strikeRate").value(125.0));
    }

    @Test
    void topInningsSortedByRuns() throws Exception {
        mvc.perform(get("/api/players/" + kohliId + "/top-innings")
                        .param("limit", "3"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].runs").value(100))
                .andExpect(jsonPath("$[0].opposition").value("Australia"))
                .andExpect(jsonPath("$[1].runs").value(50))
                .andExpect(jsonPath("$[2].runs").value(30));
    }

    @Test
    void playerWithoutInningsReturnsZeros() throws Exception {
        long tId = jdbc.queryForObject(
                "SELECT id FROM players WHERE player_code='REG:40caa465'", Long.class);
        mvc.perform(get("/api/players/" + tId + "/career-summary"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.innings").value(0))
                .andExpect(jsonPath("$.runs").value(0));
    }

    @Test
    void unknownPlayerIs404() throws Exception {
        mvc.perform(get("/api/players/999999/career-summary"))
                .andExpect(status().isNotFound());
    }

    @Test
    void unknownFormatIs400() throws Exception {
        mvc.perform(get("/api/players/" + kohliId + "/recent-form")
                        .param("format", "TEST"))
                .andExpect(status().isBadRequest());
    }

    @Test
    void limitAboveMaxIs400() throws Exception {
        mvc.perform(get("/api/players/" + kohliId + "/top-innings")
                        .param("limit", "500"))
                .andExpect(status().isBadRequest());
    }

    @Test
    void matchDetailBySourceId() throws Exception {
        mvc.perform(get("/api/matches/M100"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.format").value("ODI"))
                .andExpect(jsonPath("$.venue").value("Test Ground"))
                .andExpect(jsonPath("$.team1").value("India"));
        mvc.perform(get("/api/matches/NOPE"))
                .andExpect(status().isNotFound());
    }
}
