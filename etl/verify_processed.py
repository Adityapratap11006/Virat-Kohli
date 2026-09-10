"""Ad-hoc verification of processed outputs (not part of test suite)."""
import json
from collections import Counter
from pathlib import Path

P = Path("C:/Users/Lenovo/Desktop/Virat Kohli/data/processed")

players = json.load(open(P / "players.json", encoding="utf-8"))
name_only = [p for p in players if p.startswith("NAME:")]
amb = [p for p, m in players.items() if m["ambiguous"]]
print(f"players={len(players)} name_only={len(name_only)} ambiguous={len(amb)}")
print("ambiguous sample:", amb[:10])

kohli = [p for p, m in players.items()
         if any("kohli" in v.lower() for v in m["variants"])]
print("kohli entities:", [(p, players[p]["variants"]) for p in kohli])

n_bi = runs = balls = dismiss = 0
kohli_bi = 0
kohli_ids = set(kohli)
pos_rel = Counter()
entry_openers = 0
sevens = 0
nonstriker_outs = 0
super_bi = 0
for line in open(P / "batter_innings.jsonl", encoding="utf-8"):
    r = json.loads(line)
    n_bi += 1
    runs += r["runs"]
    balls += r["balls_faced"]
    dismiss += r["is_dismissed"]
    pos_rel[r["batting_position_reliable"]] += 1
    if r["entry_team_runs"] == 0 and r["entry_wickets_lost"] == 0:
        entry_openers += 1
    if r["batter_id"] in kohli_ids:
        kohli_bi += 1
    if r["innings_no"] > 2:
        super_bi += 1
print(f"batter_innings={n_bi} total_runs={runs} balls={balls} dismissed={dismiss}")
print(f"pos_reliable={dict(pos_rel)} openers={entry_openers} kohli_rows~{kohli_bi} super={super_bi}")

# Kohli rows via players map
n = 0
max_runs = 0
for line in open(P / "batter_innings.jsonl", encoding="utf-8"):
    r = json.loads(line)
    if r["batter_id"] in kohli_ids:
        n += 1
        max_runs = max(max_runs, r["runs"])
print(f"kohli batter-innings={n} max_runs={max_runs}")

for line in open(P / "deliveries.jsonl", encoding="utf-8"):
    d = json.loads(line)
    if d["runs_batter"] == 7:
        sevens += 1
    for w in d["wickets"]:
        if w["player_out_id"] != d["batter_id"]:
            nonstriker_outs += 1
print(f"7-run events={sevens} nonstriker_dismissals={nonstriker_outs}")

import os
for f in ["matches.jsonl", "innings.jsonl", "deliveries.jsonl",
          "batter_innings.jsonl", "players.json"]:
    print(f, round(os.path.getsize(P / f) / 1e6, 1), "MB")
