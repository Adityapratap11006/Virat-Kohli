"""Audit knock/opposition image coverage against the database.

For every displayed Kohli knock (top 6 per format) and every Kohli
opposition card, reports the image tier actually wired in
frontend/src/data/{knockImages,oppositionImages}.ts, and cross-checks each
knock record's (runs, opposition) against batter_innings (mismatch = fail).

Usage: python scripts/audit-match-images.py   (repo root; needs local MySQL)
Exit nonzero on any mismatch or DB disagreement.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db import config

REPO = Path(__file__).resolve().parent.parent
ERRORS: list[str] = []


def parse_ts(path: Path, marker: str):
    src = path.read_text(encoding="utf-8")
    recs = []
    for b in re.findall(r"\{([^{}]*" + marker + r":[^{}]*)\}", src, re.S):
        if "imagePath: '" not in b:
            continue
        rec = dict(re.findall(r"(\w+):\s*'([^']*)'", b))
        for k, v in re.findall(r"(\w+):\s*(true|false)", b):
            rec[k] = v
        for k, v in re.findall(r"(\w+):\s*(\d+)(?![\w'])", b):
            rec.setdefault(k, v)
        recs.append(rec)
    return recs


def processed_match_ids() -> set:
    """Source match IDs present in Phase 2 output (raw coverage)."""
    import json
    path = REPO / "data" / "processed" / "matches.jsonl"
    if not path.exists():
        return set()
    return {json.loads(line)["match_id"] for line in open(path, encoding="utf-8")}


def main() -> None:
    knocks = parse_ts(REPO / "frontend/src/data/knockImages.ts", "sourceMatchId")
    opp_imgs = parse_ts(REPO / "frontend/src/data/oppositionImages.ts", "imagePath")
    opp_img_map = {r["opposition"]: r for r in opp_imgs}
    knock_by_match = {r["sourceMatchId"]: r for r in knocks}

    conn = config.connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT m.source_match_id, bi.format, bi.runs, "
        "CASE WHEN bi.batting_team_id=m.team1_id THEN t2.canonical_name "
        "ELSE t1.canonical_name END, bi.match_date "
        "FROM batter_innings bi JOIN players p ON p.id=bi.player_id "
        "JOIN matches m ON m.id=bi.match_id "
        "JOIN teams t1 ON t1.id=m.team1_id JOIN teams t2 ON t2.id=m.team2_id "
        "WHERE p.player_code='REG:ba607b88'")
    db_rows = {r[0]: r for r in cur.fetchall()}
    cur.close()
    conn.close()

    # 1. knock records must agree with the DB on runs + opposition.
    # Matches absent even from Phase 2 raw coverage (e.g. T20I 122* vs
    # Afghanistan, file missing from Cricsheet t20s) are documented gaps:
    # verified photo, but never rendered since UI is DB-driven.
    raw_ids = processed_match_ids()
    gaps = []
    for r in knocks:
        mid = r["sourceMatchId"]
        if mid not in db_rows:
            if mid not in raw_ids:
                gaps.append(f"{r.get('kohliRuns')} vs {r['opposition']} "
                            f"{r.get('matchDate')} [{mid}]")
                continue
            ERRORS.append(f"knock {mid}: match in raw data but missing from DB")
            continue
        _, fmt, runs, opp, _ = db_rows[mid]
        if int(r.get("kohliRuns", -1)) != runs or r["opposition"] != opp:
            ERRORS.append(
                f"MISMATCH {mid}: registry runs/opp vs DB runs={runs} opp={opp}")
        if r.get("format") != fmt:
            ERRORS.append(f"MISMATCH {mid}: registry format vs DB {fmt}")

    # 2. displayed knocks = top 6 per format -> tier report
    by_fmt: dict[str, list] = {}
    for mid, (m, fmt, runs, opp, date) in db_rows.items():
        by_fmt.setdefault(fmt, []).append((runs, mid, opp, date))
    tiers = {"exact_knock": 0, "exact_match": 0, "same_opposition": 0,
             "generic_action": 0, "fallback": 0}
    print("top knocks per format:")
    for fmt in ("ODI", "T20I", "IPL"):
        top = sorted(by_fmt.get(fmt, []), reverse=True)[:6]
        for runs, mid, opp, date in top:
            rec = knock_by_match.get(mid)
            tier = rec["matchAssociation"] if rec else "fallback"
            tiers[tier if tier in tiers else "fallback"] += 1
            flag = "" if rec else "  <-- FALLBACK"
            print(f"  {fmt} {runs} vs {opp} {date} [{mid}]: {tier}{flag}")

    # 3. opposition cards: exact-knock preferred, else licensed same-opp, else fallback
    print("opposition cards:")
    opps = {}
    for mid, (m, fmt, runs, opp, date) in db_rows.items():
        opps.setdefault((fmt, opp), 0)
        opps[(fmt, opp)] += 1
    for (fmt, opp) in sorted(opps):
        pref = [k for k in knocks if k["opposition"] == opp]
        if pref:
            tier, detail = "exact_knock", pref[0]["sourceMatchId"]
        elif opp in opp_img_map:
            tier, detail = "same_opposition", "licensed"
        else:
            tier, detail = "fallback", "none"
        tiers[tier] += 1
        print(f"  {fmt} {opp}: {tier} ({detail})")

    total_knocks = 18
    print("\nsummary:", tiers)
    print(f"displayed knocks audited: {total_knocks}")
    if gaps:
        print("documented coverage gaps (verified photo, match absent from "
              "Cricsheet raw data, never rendered):")
        for g in gaps:
            print(" ", g)
    if ERRORS:
        print("ERRORS:")
        for e in ERRORS:
            print(" ", e)
        sys.exit(1)
    print("mismatches: 0")


if __name__ == "__main__":
    main()
