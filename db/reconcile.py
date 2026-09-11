"""Post-ingestion reconciliation: Phase 2 processed output vs MySQL.

Compares matches/innings/deliveries/batter-innings/players/teams/venues/
wickets counts exactly, plus Kohli integrity anchors (1 entity, 685 rows,
max 183, no dup (player,match,innings), all formats present).
Exits nonzero on any mismatch.

Usage: python -m db.reconcile   (run from repo root)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db import config
from db.ingest import PROCESSED, _lines

KOHLI_CODE = "REG:ba607b88"
KOHLI_ROWS = 682  # V Kohli only; T Kohli has 3 separate rows (Phase 2 note)
KOHLI_MAX = 183


def _count(conn, table: str) -> int:
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    n = cur.fetchone()[0]
    cur.close()
    return n


def _lines_count(path: Path) -> int:
    return sum(1 for _ in _lines(path))


def reconcile() -> dict:
    conn = config.connect()
    errors: list[str] = []
    report: dict = {}
    try:
        players = json.load(open(PROCESSED / "players.json", encoding="utf-8"))
        expected_teams: set[str] = set()
        for m in _lines(PROCESSED / "matches.jsonl"):
            expected_teams.add(m["team1"])
            expected_teams.add(m["team2"])
        expected_venues: set[tuple] = set()
        for m in _lines(PROCESSED / "matches.jsonl"):
            expected_venues.add((m["venue_canonical"], m["city"] or ""))
        expected_wickets = 0
        for d in _lines(PROCESSED / "deliveries.jsonl"):
            expected_wickets += len(d["wickets"])

        checks = [
            ("matches", _lines_count(PROCESSED / "matches.jsonl")),
            ("innings", _lines_count(PROCESSED / "innings.jsonl")),
            ("deliveries", _lines_count(PROCESSED / "deliveries.jsonl")),
            ("batter_innings", _lines_count(PROCESSED / "batter_innings.jsonl")),
            ("players", len(players)),
            ("teams", len(expected_teams)),
            ("team_aliases", len(json.load(
                open(PROCESSED / "teams.json", encoding="utf-8"))["aliases"])),
            ("venues", len(expected_venues)),
            ("wickets", expected_wickets),
        ]
        for table, expected in checks:
            actual = _count(conn, table)
            report[table] = {"expected": expected, "actual": actual,
                             "diff": actual - expected}
            if actual != expected:
                errors.append(f"{table}: expected {expected}, got {actual}")

        cur = conn.cursor()
        cur.execute("SELECT id, display_name, ambiguous FROM players "
                    "WHERE JSON_CONTAINS(name_variants, '\"V Kohli\"')")
        kohli = cur.fetchall()
        if len(kohli) != 1:
            errors.append(f"kohli entities: expected 1, got {len(kohli)}")
        else:
            kid = kohli[0][0]
            cur.execute("SELECT player_code FROM players WHERE id = %s", (kid,))
            code = cur.fetchone()[0]
            if code != KOHLI_CODE:
                errors.append(f"kohli code: expected {KOHLI_CODE}, got {code}")
            cur.execute("SELECT COUNT(*), MAX(runs) FROM batter_innings "
                        "WHERE player_id = %s", (kid,))
            n, mx = cur.fetchone()
            report["kohli"] = {"rows": n, "max_runs": mx}
            if n != KOHLI_ROWS:
                errors.append(f"kohli rows: expected {KOHLI_ROWS}, got {n}")
            if mx != KOHLI_MAX:
                errors.append(f"kohli max: expected {KOHLI_MAX}, got {mx}")
            cur.execute("SELECT DISTINCT format FROM batter_innings WHERE player_id=%s",
                        (kid,))
            fmts = sorted(r[0] for r in cur.fetchall())
            report["kohli"]["formats"] = fmts
            if fmts != ["IPL", "ODI", "T20I"]:
                errors.append(f"kohli formats: {fmts}")
        cur.execute("SELECT COUNT(*) FROM (SELECT player_id, match_id, innings_id "
                    "FROM batter_innings GROUP BY 1,2,3 HAVING COUNT(*) > 1) d")
        if cur.fetchone()[0]:
            errors.append("duplicate (player,match,innings) rows")
        cur.execute("SELECT COUNT(*) FROM batter_innings bi JOIN innings i "
                    "ON i.id = bi.innings_id WHERE i.classification != 'normal'")
        if cur.fetchone()[0]:
            errors.append("non-normal batter-innings rows present")
        cur.execute("SELECT COUNT(*) FROM deliveries WHERE runs_batter > 6")
        report["seven_run_deliveries"] = cur.fetchone()[0]
        if report["seven_run_deliveries"] != 2:
            errors.append("7-run deliveries changed")
        cur.execute("SELECT COUNT(*), COUNT(DISTINCT canonical_key) FROM canonical_venues")
        ncv, distinct_cv = cur.fetchone()
        cur.execute("SELECT COUNT(*) FROM venue_aliases")
        nal = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM venues")
        nvenues = cur.fetchone()[0]
        report["canonical_venues"] = {"rows": ncv, "distinct_keys": distinct_cv,
                                      "aliases": nal, "raw_venues": nvenues}
        if nal != nvenues:
            errors.append(f"venue alias coverage: {nal} aliases for {nvenues} raw venues")
        # canonical grouping must preserve exact totals (grouping only, no row changes)
        cur.execute("SELECT COUNT(*), COALESCE(SUM(bi.runs),0), "
                    "COALESCE(SUM(bi.balls_faced),0) FROM batter_innings bi "
                    "JOIN matches m ON m.id=bi.match_id "
                    "JOIN venue_aliases a ON a.raw_venue_id=m.venue_id")
        canon_totals = cur.fetchone()
        cur.execute("SELECT COUNT(*), COALESCE(SUM(runs),0), "
                    "COALESCE(SUM(balls_faced),0) FROM batter_innings")
        raw_totals = cur.fetchone()
        report["venue_totals"] = {"canonical": list(canon_totals),
                                  "raw": list(raw_totals)}
        if tuple(canon_totals) != tuple(raw_totals):
            errors.append(f"canonical totals diverged: {canon_totals} vs {raw_totals}")
        cur.execute("SELECT COUNT(*), COALESCE(SUM(bi.runs),0) FROM batter_innings bi "
                    "JOIN players p ON p.id=bi.player_id "
                    "JOIN matches m ON m.id=bi.match_id "
                    "JOIN venue_aliases a ON a.raw_venue_id=m.venue_id "
                    "WHERE p.player_code=%s", (KOHLI_CODE,))
        kn, kr = cur.fetchone()
        report["kohli_canonical"] = {"rows": kn, "runs": kr}
        cur.execute("SELECT COALESCE(SUM(bi.runs),0) FROM batter_innings bi "
                    "JOIN players p ON p.id=bi.player_id WHERE p.player_code=%s",
                    (KOHLI_CODE,))
        kohli_raw_runs = cur.fetchone()[0]
        if kr != kohli_raw_runs:
            errors.append(f"kohli canonical runs {kr} != raw {kohli_raw_runs}")
        if kn != KOHLI_ROWS:
            errors.append(f"kohli canonical rows {kn} != {KOHLI_ROWS}")
        cur.close()
    finally:
        conn.close()
    report["errors"] = errors
    print(json.dumps(report, indent=2, default=str))
    return report


if __name__ == "__main__":
    rep = reconcile()
    sys.exit(1 if rep["errors"] else 0)
