import json, pathlib
base = pathlib.Path("C:/Users/Lenovo/Desktop/Virat Kohli/data/raw")
for src in ["odis", "t20s", "ipl"]:
    found_rep = None; found_rev = None
    for p in (base/src).glob("*.json"):
        dd = json.load(open(p, encoding="utf-8"))
        for inn in dd.get("innings", []):
            for ov in inn.get("overs", []):
                for dl in ov.get("deliveries", []):
                    if found_rep is None and "replacements" in dl:
                        found_rep = (p.name, dl)
                    if found_rev is None and "review" in dl:
                        found_rev = (p.name, dl)
                    if found_rep and found_rev:
                        break
                if found_rep and found_rev:
                    break
            if found_rep and found_rev:
                break
        if found_rep and found_rev:
            break
    print(src, "REPL:", str(found_rep)[:500])
    print(src, "REVIEW:", str(found_rev)[:600])

kohli = None
for p in (base/"odis").glob("*.json"):
    dd = json.load(open(p, encoding="utf-8"))
    pls = dd.get("info", {}).get("players", {})
    hit = False
    for sq in pls.values():
        for x in sq:
            if "Kohli" in x:
                hit = True
    if hit:
        kohli = p
        break
dd = json.load(open(kohli, encoding="utf-8"))
print("kohli demo file:", kohli.name, dd["info"]["dates"], dd["info"]["teams"])
for i, inn in enumerate(dd["innings"]):
    order = []
    for ov in inn["overs"]:
        for dl in ov["deliveries"]:
            for b in [dl["batter"], dl.get("non_striker")]:
                if b and b not in order:
                    order.append(b)
    print("inn", i, "team=", inn["team"], "order=", order)
