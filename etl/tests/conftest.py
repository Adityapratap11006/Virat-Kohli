"""Small synthetic Cricsheet-shaped fixtures (no full-dataset reads in unit tests)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


def dl(batter, bowler="B1", non_striker="N1", br=0, ex=0, extras=None,
       wickets=None, num="0.1", **kw):
    d = {"actual_delivery": num, "batter": batter, "bowler": bowler,
         "non_striker": non_striker,
         "runs": {"batter": br, "extras": ex, "total": br + ex}}
    if extras is not None:
        d["extras"] = extras
    if wickets is not None:
        d["wickets"] = wickets
    d.update(kw)
    return d


def match(info_over=None, innings=None):
    info = {"dates": ["2024-01-01"], "venue": "V", "city": "C",
            "season": "2024", "match_type": "ODI", "team_type": "international",
            "teams": ["A", "B"], "toss": {"winner": "A", "decision": "bat"},
            "outcome": {"winner": "A", "by": {"runs": 10}},
            "overs": 50, "balls_per_over": 6, "gender": "male",
            "players": {"A": ["A1", "A2"], "B": ["B1", "B2"]},
            "registry": {"people": {"A1": "id-a1", "A2": "id-a2",
                                    "B1": "id-b1", "B2": "id-b2"}}}
    info.update(info_over or {})
    return {"meta": {"data_version": "1.2.0"}, "info": info,
            "innings": innings if innings is not None else []}


def innings(team, overs, target=None):
    inn = {"team": team, "overs": overs}
    if target:
        inn["target"] = target
    return inn


def over(n, deliveries):
    return {"over": n, "deliveries": deliveries}
