"""Dev probe: team names per format (male V1), match-id collisions, DLS methods."""
import json, pathlib, collections

base = pathlib.Path("C:/Users/Lenovo/Desktop/Virat Kohli/data/raw")

def v1_ok(src, info):
    g = info.get("gender"); tt = info.get("team_type"); mt = info.get("match_type")
    if g != "male":
        return False
    if src == "odis":
        return mt == "ODI"
    if src == "t20s":
        return mt == "T20" and tt == "international"
    return tt == "club"

ids = collections.Counter()
for src in ["odis", "t20s", "ipl"]:
    teams = collections.Counter(); methods = collections.Counter(); n = 0
    for p in (base/src).glob("*.json"):
        ids[p.stem] += 1
        d = json.load(open(p, encoding="utf-8"))
        info = d.get("info", {})
        if not v1_ok(src, info):
            continue
        n += 1
        for t in info.get("teams", []):
            teams[t] += 1
        out = info.get("outcome", {})
        if "method" in out:
            methods[out["method"]] += 1
    print(f"== {src} V1 files: {n}")
    print("  teams:", sorted(teams))
    print("  DLS methods:", dict(methods))

dups = {k: v for k, v in ids.items() if v > 1}
print("duplicate match ids across formats:", dups if dups else "NONE")
