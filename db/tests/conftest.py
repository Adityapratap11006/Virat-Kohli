"""DB tests use a throwaway kohliiq_test database (dropped + recreated
per session). Requires the project MySQL running (see docs/database-ingestion.md).
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from db import config, ingest
from db.migrate import migrate


@pytest.fixture(scope="session", autouse=True)
def _use_test_db():
    import mysql.connector
    admin = mysql.connector.connect(host=config.HOST, port=config.PORT,
                                    user=config.USER, password=config.PASSWORD,
                                    charset="utf8mb4", autocommit=True)
    cur = admin.cursor()
    cur.execute("DROP DATABASE IF EXISTS kohliiq_test")
    cur.execute("CREATE DATABASE kohliiq_test CHARACTER SET utf8mb4 "
                "COLLATE utf8mb4_0900_ai_ci")
    cur.close()
    admin.close()
    config.NAME = "kohliiq_test"
    migrate()
    yield
    config.NAME = "kohliiq"


@pytest.fixture()
def conn():
    c = config.connect()
    yield c
    c.rollback()
    c.close()


@pytest.fixture(autouse=True)
def _clean(conn):
    cur = conn.cursor()
    cur.execute("SET FOREIGN_KEY_CHECKS=0")
    for t in ("batter_innings", "wickets", "deliveries", "innings", "matches",
              "team_aliases", "venues", "teams", "players"):
        cur.execute(f"TRUNCATE TABLE {t}")
    cur.execute("SET FOREIGN_KEY_CHECKS=1")
    conn.commit()
    cur.close()


def _dl(batter, num="0.1", br=0, ex=0, extras=None, wickets=None, **kw):
    d = {"match_id": "M1", "innings_no": 1, "over": 0, "seq_in_over": 0,
         "actual_delivery": num, "global_seq": 0, "batter_id": kw.get("b", "REG:p1"),
         "non_striker_id": "REG:p2", "bowler_id": "REG:p3",
         "runs_batter": br, "runs_extras": ex, "runs_total": br + ex,
         "extras": extras or {}, "wickets": wickets or [],
         "is_legal_ball": True, "batter_ambiguous": False}
    d["batter_id"] = batter
    return d


@pytest.fixture()
def mini_processed(tmp_path):
    """Two matches: M1 (ODI, 2 normal innings, edge-case deliveries),
    M2 (super-over header, null city, alias team)."""
    players = {
        "REG:p1": {"registry_ids": ["p1"], "variants": ["A One"],
                   "ambiguous": False, "has_registry_id": True},
        "REG:p2": {"registry_ids": ["p2"], "variants": ["B Two"],
                   "ambiguous": False, "has_registry_id": True},
        "REG:p3": {"registry_ids": ["p3"], "variants": ["C Three"],
                   "ambiguous": False, "has_registry_id": True},
        "REG:x1": {"registry_ids": ["x1", "x2"], "variants": ["X Khan"],
                   "ambiguous": True, "has_registry_id": True},
        "REG:x2": {"registry_ids": ["x1", "x2"], "variants": ["X Khan"],
                   "ambiguous": True, "has_registry_id": True},
    }
    matches = [
        {"match_id": "M1", "source_file": "M1.json", "format": "ODI",
         "date": "2024-01-01", "season": "2024", "venue": "Ground",
         "venue_canonical": "Ground", "city": "City",
         "team1": "Alpha", "team2": "Beta",
         "team1_source": "Alpha", "team2_source": "Beta",
         "toss_winner": "Alpha", "toss_decision": "bat",
         "outcome": {"winner": "Alpha"}, "dls_method": None, "event": None},
        {"match_id": "M2", "source_file": "M2.json", "format": "T20I",
         "date": "2024-02-01", "season": "2024", "venue": "Ground",
         "venue_canonical": "Ground", "city": None,
         "team1": "Royal Challengers Bengaluru", "team2": "Beta",
         "team1_source": "Royal Challengers Bangalore",
         "team2_source": "Beta",
         "toss_winner": "Beta", "toss_decision": "field",
         "outcome": {"winner": "Beta"}, "dls_method": "D/L", "event": "Cup"},
    ]
    innings = [
        {"match_id": "M1", "innings_no": 1, "team": "Alpha",
         "opposition": "Beta", "team_source": "Alpha",
         "classification": "normal", "target_runs": None,
         "target_overs": None, "had_replacement": False},
        {"match_id": "M1", "innings_no": 2, "team": "Beta",
         "opposition": "Alpha", "team_source": "Beta",
         "classification": "normal", "target_runs": 50,
         "target_overs": 50, "had_replacement": True},
        {"match_id": "M2", "innings_no": 1, "team": "Royal Challengers Bengaluru",
         "opposition": "Beta", "team_source": "Royal Challengers Bangalore",
         "classification": "normal", "target_runs": None,
         "target_overs": None, "had_replacement": False},
        {"match_id": "M2", "innings_no": 2, "team": "Beta",
         "opposition": "Royal Challengers Bengaluru", "team_source": "Beta",
         "classification": "normal", "target_runs": 30,
         "target_overs": 20, "had_replacement": False},
        {"match_id": "M2", "innings_no": 3, "team": "Royal Challengers Bengaluru",
         "opposition": "Beta", "team_source": "Royal Challengers Bangalore",
         "classification": "super_over", "target_runs": 10,
         "target_overs": 1, "had_replacement": False},
    ]
    deliveries = [
        _dl("REG:p1", num="0.5", ex=1, extras={"wides": 1}),
        dict(_dl("REG:p1", num="0.5", br=2), **{"seq_in_over": 1, "global_seq": 1}),
        dict(_dl("REG:p1", num="0.6", br=7), **{"seq_in_over": 2, "global_seq": 2}),
        dict(_dl("REG:p1", num="0.7",
                 wickets=[{"player_out_id": "REG:p2", "kind": "run out"}]),
             **{"seq_in_over": 3, "global_seq": 3}),
        dict(_dl("REG:x1", num="0.8",
                 wickets=[{"player_out_id": "REG:x1", "kind": "retired hurt"}]),
             **{"seq_in_over": 4, "global_seq": 4, "batter_ambiguous": True}),
    ]
    bi = [
        {"match_id": "M1", "format": "ODI", "date": "2024-01-01",
         "innings_no": 1, "batter_id": "REG:p1", "team": "Alpha",
         "opposition": "Beta", "venue_canonical": "Ground", "runs": 9,
         "balls_faced": 4, "dismissal_kind": None, "is_dismissed": False,
         "entry_team_runs": 0, "entry_wickets_lost": 0,
         "entry_balls_bowled": 0, "entry_balls_remaining": 300,
         "chase_target": None, "batting_position": 1,
         "batting_position_reliable": True, "dls_method": None,
         "source_file": "M1.json"},
        {"match_id": "M2", "format": "T20I", "date": "2024-02-01",
         "innings_no": 1, "batter_id": "REG:x2",
         "team": "Royal Challengers Bengaluru", "opposition": "Beta",
         "venue_canonical": "Ground", "runs": 0, "balls_faced": 0,
         "dismissal_kind": None, "is_dismissed": False,
         "entry_team_runs": 0, "entry_wickets_lost": 0,
         "entry_balls_bowled": 0, "entry_balls_remaining": 120,
         "chase_target": None, "batting_position": None,
         "batting_position_reliable": False, "dls_method": "D/L",
         "source_file": "M2.json"},
    ]
    (tmp_path / "players.json").write_text(json.dumps(players), encoding="utf-8")
    (tmp_path / "teams.json").write_text(json.dumps(
        {"aliases": {"Royal Challengers Bangalore":
                     "Royal Challengers Bengaluru"}}), encoding="utf-8")
    (tmp_path / "venues.json").write_text(json.dumps(
        {"Ground": {"variants": ["Ground"], "cities": ["City"]}}),
        encoding="utf-8")
    for name, rows in (("matches", matches), ("innings", innings),
                       ("deliveries", deliveries), ("batter_innings", bi)):
        with open(tmp_path / f"{name}.jsonl", "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
    return tmp_path


@pytest.fixture()
def loaded(conn, mini_processed, monkeypatch):
    monkeypatch.setattr(ingest, "PROCESSED", mini_processed)
    player_ids = ingest.load_players(conn)
    team_ids = ingest.load_teams(conn, mini_processed / "matches.jsonl")
    venue_ids = ingest.load_venues(conn, mini_processed / "matches.jsonl")
    match_ids = ingest.load_matches(conn, team_ids, venue_ids)
    ingest.load_innings(conn, match_ids, team_ids)
    ingest.load_deliveries(conn, match_ids, player_ids)
    ingest.load_batter_innings(conn, match_ids, player_ids, team_ids)
    return {"players": player_ids, "teams": team_ids, "venues": venue_ids,
            "matches": match_ids}
