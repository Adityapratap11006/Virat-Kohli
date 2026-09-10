"""Ingestion behavior: idempotency, constraints, edge-case preservation."""
import mysql.connector
import pytest

from db import ingest


def _count(conn, table):
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    n = cur.fetchone()[0]
    cur.close()
    return n


def test_full_mini_load_counts(conn, loaded):
    assert _count(conn, "matches") == 2
    assert _count(conn, "innings") == 5
    assert _count(conn, "deliveries") == 5
    assert _count(conn, "wickets") == 2
    assert _count(conn, "batter_innings") == 2
    assert _count(conn, "players") == 5
    assert _count(conn, "team_aliases") == 1


def test_reingest_is_idempotent(conn, loaded, mini_processed, monkeypatch):
    monkeypatch.setattr(ingest, "PROCESSED", mini_processed)
    before = {t: _count(conn, t) for t in
              ("matches", "innings", "deliveries", "wickets",
               "batter_innings", "players", "teams", "venues")}
    p = ingest.load_players(conn)
    t = ingest.load_teams(conn, mini_processed / "matches.jsonl")
    v = ingest.load_venues(conn, mini_processed / "matches.jsonl")
    m = ingest.load_matches(conn, t, v)
    ingest.load_innings(conn, m, t)
    ingest.load_deliveries(conn, m, p)
    ingest.load_batter_innings(conn, m, p, t)
    after = {t: _count(conn, t) for t in before}
    assert before == after


def test_duplicate_delivery_seq_upserts(conn, loaded):
    cur = conn.cursor()
    cur.execute("SELECT id FROM innings LIMIT 1")
    iid = cur.fetchone()[0]
    cur.execute("SELECT id FROM players LIMIT 1")
    pid = cur.fetchone()[0]
    cur.executemany(
        "INSERT INTO deliveries (innings_id, over_number, seq_in_over, global_seq,"
        " actual_delivery, batter_id, non_striker_id, bowler_id, runs_batter,"
        " runs_extras, runs_total, extras, is_legal_ball) VALUES "
        "(%s,9,0,99,'9.1',%s,%s,%s,1,0,1,'{}',1) AS new "
        "ON DUPLICATE KEY UPDATE global_seq=new.global_seq",
        [(iid, pid, pid, pid), (iid, pid, pid, pid)])
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM deliveries WHERE over_number=9")
    assert cur.fetchone()[0] == 1
    cur.close()


def test_fk_enforcement(conn, loaded):
    cur = conn.cursor()
    with pytest.raises(mysql.connector.errors.IntegrityError):
        cur.execute("INSERT INTO deliveries (innings_id, over_number, seq_in_over,"
                    " global_seq, actual_delivery, batter_id, non_striker_id,"
                    " bowler_id, runs_batter, runs_extras, runs_total, extras,"
                    " is_legal_ball) VALUES (999999,0,0,0,'0.1',1,1,1,0,0,0,'{}',1)")
    with pytest.raises(mysql.connector.errors.IntegrityError):
        cur.execute("INSERT INTO wickets (innings_id, over_number, seq_in_over,"
                    " player_out_id, kind) VALUES (999999,0,0,1,'bowled')")
    cur.close()


def test_check_constraint_runs_total(conn, loaded):
    cur = conn.cursor()
    cur.execute("SELECT innings_id, batter_id FROM deliveries LIMIT 1")
    iid, pid = cur.fetchone()
    with pytest.raises(mysql.connector.errors.DatabaseError):  # CHECK -> 3819
        cur.execute("INSERT INTO deliveries (innings_id, over_number, seq_in_over,"
                    " global_seq, actual_delivery, batter_id, non_striker_id,"
                    " bowler_id, runs_batter, runs_extras, runs_total, extras,"
                    " is_legal_ball) VALUES (%s,8,0,98,'8.1',%s,%s,%s,4,0,5,'{}',1)",
                    (iid, pid, pid, pid))
    cur.close()


def test_seven_run_and_nonstriker_preserved(conn, loaded):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM deliveries WHERE runs_batter = 7")
    assert cur.fetchone()[0] == 1
    cur.execute("SELECT COUNT(*) FROM wickets w JOIN deliveries d ON "
                "d.innings_id=w.innings_id AND d.over_number=w.over_number "
                "AND d.seq_in_over=w.seq_in_over "
                "WHERE w.player_out_id != d.batter_id")
    assert cur.fetchone()[0] == 1
    cur.close()


def test_ambiguous_players_stay_separate(conn, loaded):
    cur = conn.cursor()
    cur.execute("SELECT player_code, ambiguous FROM players "
                "WHERE player_code IN ('REG:x1','REG:x2') ORDER BY 1")
    rows = cur.fetchall()
    assert rows == [("REG:x1", 1), ("REG:x2", 1)]
    cur.close()


def test_team_alias_and_null_city(conn, loaded):
    cur = conn.cursor()
    cur.execute("SELECT t.canonical_name FROM team_aliases a JOIN teams t "
                "ON t.id=a.team_id WHERE a.alias='Royal Challengers Bangalore'")
    assert cur.fetchone()[0] == "Royal Challengers Bengaluru"
    cur.execute("SELECT COUNT(*) FROM venues WHERE city IS NULL")
    assert cur.fetchone()[0] == 1
    cur.close()


def test_nullable_unreliable_position(conn, loaded):
    cur = conn.cursor()
    cur.execute("SELECT batting_position, batting_position_reliable FROM "
                "batter_innings WHERE dismissal_kind IS NULL AND runs = 0")
    assert cur.fetchone() == (None, 0)
    cur.close()


def test_super_over_excluded_from_batter_innings(conn, loaded):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM innings WHERE classification='super_over'")
    assert cur.fetchone()[0] == 1
    cur.execute("SELECT COUNT(*) FROM batter_innings bi JOIN innings i "
                "ON i.id=bi.innings_id WHERE i.classification != 'normal'")
    assert cur.fetchone()[0] == 0
    cur.close()
