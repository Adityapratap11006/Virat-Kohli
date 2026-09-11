"""Independent reconciliation of data/ml/v1 against MySQL (not the builder).

Checks: row counts, splits, date ranges, formats, target sums, entry-field
spot agreement, NULL rates, history-count distributions, Kohli anchors.
Exit nonzero on mismatch. Usage: python -m ml.features.verify (repo root).
"""
import csv
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from db import config

V1 = Path("data/ml/v1/features.csv")
ERRORS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    print(f"{'OK ' if cond else 'FAIL'}  {name} {detail}")
    if not cond:
        ERRORS.append(name)


def main() -> None:
    rows = list(csv.DictReader(open(V1, encoding="utf-8", newline="")))
    check("row_count", len(rows) == 119619, f"n={len(rows)}")
    splits = Counter(r["split"] for r in rows)
    print("splits:", dict(splits))
    check("split_counts", sum(splits.values()) == len(rows))
    dates = [r["match_date"] for r in rows]
    check("date_range", min(dates) == "2002-06-27" and max(dates) == "2026-09-09",
          f"{min(dates)}..{max(dates)}")
    fmts = Counter(r["format"] for r in rows)
    print("formats:", dict(fmts))
    check("formats", set(fmts) == {"ODI", "T20I", "IPL"})

    conn = config.connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*), COALESCE(SUM(runs),0) FROM batter_innings")
    n_db, runs_db = cur.fetchone()
    check("count_vs_db", n_db == len(rows), f"db={n_db}")
    check("target_sum_vs_db", sum(int(r["target_runs"]) for r in rows) == runs_db,
          f"db_runs={runs_db}")
    cur.execute("SELECT COUNT(*), COALESCE(SUM(runs),0) FROM batter_innings bi "
                "JOIN players p ON p.id=bi.player_id "
                "WHERE p.player_code='REG:ba607b88'")
    kn, kr = cur.fetchone()
    k = [r for r in rows if r["batter_code"] == "REG:ba607b88"]
    check("kohli_rows", len(k) == kn == 682, f"db={kn} csv={len(k)}")
    check("kohli_runs", sum(int(r["target_runs"]) for r in k) == kr == 28078,
          f"db={kr}")
    # entry-field spot agreement on 2000 deterministic rows
    cur.execute("SELECT bi.id, bi.entry_team_runs, bi.entry_wickets_lost,"
                " bi.entry_balls_bowled, bi.entry_balls_remaining, bi.runs "
                "FROM batter_innings bi ORDER BY bi.id LIMIT 2000")
    by_id = {str(r["batter_innings_id"]): r for r in rows}
    bad = 0
    for bid, er, ew, eb, ebr, runs in cur.fetchall():
        r = by_id.get(str(bid))
        if (r is None or int(r["entry_runs"]) != er
                or int(r["entry_wkts"]) != ew or int(r["entry_balls"]) != eb
                or int(r["entry_balls_remaining"]) != ebr
                or int(r["target_runs"]) != runs):
            bad += 1
    check("entry_spot_2000", bad == 0, f"mismatches={bad}")
    # chase consistency: runs_required/RRR recompute
    bad = 0
    for r in rows:
        if r["is_chase"] == "1" and r["chase_target"] not in ("", None):
            exp_req = int(r["chase_target"]) - int(r["entry_runs"])
            if int(r["runs_required"]) != exp_req:
                bad += 1
            ebrem = int(r["entry_balls_remaining"])
            exp_rrr = round(exp_req * 6.0 / ebrem, 2) if ebrem > 0 else None
            got = None if r["required_rr"] == "" else float(r["required_rr"])
            if exp_rrr != got:
                bad += 1
    check("chase_math", bad == 0, f"mismatches={bad}")
    cur.close()
    conn.close()

    def null_rate(col):
        return sum(1 for r in rows if r[col] == "") / len(rows)

    for col in ["avg_5", "avg_10", "avg_20", "sr_10", "venue_avg", "opp_avg",
                "inn1_avg", "inn2_avg", "chase_avg", "setting_avg",
                "batting_position", "runs_required", "required_rr"]:
        print(f"null {col}: {null_rate(col):.3f}")
    pc = Counter(r["prior_innings"] for r in rows)
    print("prior_innings==0 rows:", pc.get("0", 0))
    check("cold_start_present", pc.get("0", 0) > 0)
    print("ERRORS:", ERRORS if ERRORS else "none")
    sys.exit(1 if ERRORS else 0)


if __name__ == "__main__":
    main()
