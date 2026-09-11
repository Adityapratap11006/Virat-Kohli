"""Build the leakage-safe Expected Runs feature dataset (v1).

Reads batter_innings (+ joins) from MySQL in chronological order, replays
one strictly-earlier-date history per batter, and writes data/ml/v1/:
features.csv (one row per batter-innings, split column included),
feature_schema.json, manifest.json. Deterministic; stdlib only.

Usage: python -m ml.features.build [--out data/ml/v1]   (repo root)
"""
import csv
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from db import config
from ml.features.history import BatterHistory

VERSION = "v1"
TRAIN_END = "2021-12-31"
VAL_END = "2022-12-31"
# train: match_date <= 2021; validation: 2022; test: >= 2023 (untouched).

COLUMNS = [
    # identity / traceability
    "batter_innings_id", "match_id", "source_match_id", "batter_code",
    "match_date", "year", "split",
    # entry context (known at prediction timestamp)
    "format", "innings_no", "is_chase", "chase_target",
    "entry_runs", "entry_wkts", "entry_balls", "entry_balls_remaining",
    "entry_overs_completed", "runs_required", "required_rr",
    "batting_position", "pos_reliable",
    "venue_key", "venue_name", "opposition",
    # history (strictly earlier dates only; NULL cold start)
    "prior_innings", "avg_5", "avg_10", "avg_20", "sr_10",
    "venue_n", "venue_avg", "venue_sr",
    "opp_n", "opp_avg", "opp_sr",
    "inn1_avg", "inn2_avg", "chase_avg", "setting_avg",
    # target
    "target_runs",
]

QUERY = """
SELECT bi.id, m.id, m.source_match_id, p.player_code,
       bi.match_date,
       bi.format, inn.innings_no,
       bi.entry_team_runs, bi.entry_wickets_lost, bi.entry_balls_bowled,
       bi.entry_balls_remaining, bi.chase_target,
       bi.batting_position, bi.batting_position_reliable,
       cv.canonical_key, cv.canonical_name,
       CASE WHEN bi.batting_team_id = m.team1_id THEN t2.canonical_name
            ELSE t1.canonical_name END,
       bi.runs, bi.balls_faced
FROM batter_innings bi
JOIN matches m ON m.id = bi.match_id
JOIN innings inn ON inn.id = bi.innings_id
JOIN players p ON p.id = bi.player_id
JOIN teams t1 ON t1.id = m.team1_id
JOIN teams t2 ON t2.id = m.team2_id
JOIN venues v ON v.id = m.venue_id
JOIN venue_aliases a ON a.raw_venue_id = v.id
JOIN canonical_venues cv ON cv.id = a.canonical_venue_id
ORDER BY bi.match_date, m.id, inn.id, bi.id
"""


def split_of(date: str) -> str:
    if date <= TRAIN_END:
        return "train"
    if date <= VAL_END:
        return "val"
    return "test"


def build_row(r: tuple, hist: dict) -> dict:
    (bid, mid, src, code, raw_date, fmt, ino, eruns, ewkts, eballs, ebrem,
     target, pos, posrel, vkey, vname, opp, runs, balls) = r
    date = raw_date.isoformat() if hasattr(raw_date, "isoformat") else raw_date
    is_chase = ino == 2
    runs_req = (target - eruns) if (is_chase and target is not None) else None
    rrr = round(runs_req * 6.0 / ebrem, 2) if (
        runs_req is not None and ebrem > 0) else None
    h = hist.setdefault(code, BatterHistory())
    snap = h.snapshot(date, vkey, opp)
    h.add(date, runs, balls, vkey, opp, ino, is_chase)
    return {
        "batter_innings_id": bid, "match_id": mid, "source_match_id": src,
        "batter_code": code, "match_date": date, "year": int(date[:4]),
        "split": split_of(date),
        "format": fmt, "innings_no": ino, "is_chase": int(is_chase),
        "chase_target": target,
        "entry_runs": eruns, "entry_wkts": ewkts, "entry_balls": eballs,
        "entry_balls_remaining": ebrem,
        "entry_overs_completed": eballs // 6,
        "runs_required": runs_req, "required_rr": rrr,
        "batting_position": pos, "pos_reliable": int(posrel),
        "venue_key": vkey, "venue_name": vname, "opposition": opp,
        **snap,
        "target_runs": runs,
    }


def main() -> None:
    outdir = Path(sys.argv[sys.argv.index("--out") + 1]
                  if "--out" in sys.argv else "data/ml/v1")
    outdir.mkdir(parents=True, exist_ok=True)
    conn = config.connect()
    cur = conn.cursor()
    cur.execute(QUERY)
    hist: dict = {}
    n = 0
    with open(outdir / "features.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        while True:
            batch = cur.fetchmany(5000)
            if not batch:
                break
            for r in batch:
                row = build_row(r, hist)
                w.writerow({k: ("" if row[k] is None else row[k])
                            for k in COLUMNS})
                n += 1
            print(f"  {n} rows ...", flush=True)
    cur.close()
    conn.close()
    (outdir / "feature_schema.json").write_text(json.dumps(
        {"version": VERSION, "columns": COLUMNS,
         "target": "target_runs",
         "target_definition": "Final runs scored by the batter in that innings.",
         "history_rule": "strictly earlier match_date only; NULL cold start.",
         "splits": {"train": f"match_date <= {TRAIN_END}",
                    "val": f"{TRAIN_END} < match_date <= {VAL_END}",
                    "test": f"match_date > {VAL_END}"}}, indent=2),
        encoding="utf-8")
    manifest = {
        "version": VERSION,
        "built_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "rows": n,
        "source": {"db": f"{config.HOST}:{config.PORT}/{config.NAME}"},
    }
    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2),
                                          encoding="utf-8")
    print(f"wrote {n} rows to {outdir}")


if __name__ == "__main__":
    main()
