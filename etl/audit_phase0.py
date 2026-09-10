"""Phase 0 dataset audit - scans real Cricsheet JSONs, no assumptions."""
import json, pathlib, collections, datetime

BASE = pathlib.Path("C:/Users/Lenovo/Desktop/Virat Kohli/data/raw")
OUT = pathlib.Path("C:/Users/Lenovo/Desktop/Virat Kohli/docs/data/audit_raw.json")
SOURCES = {"odis": BASE/"odis", "t20s": BASE/"t20s", "ipl": BASE/"ipl"}

def scan():
    report = {}
    for src_name, folder in SOURCES.items():
        files = sorted(folder.glob("*.json"))
        mt = collections.Counter(); gender = collections.Counter()
        team_type = collections.Counter(); season = collections.Counter()
        dates = []; venues = collections.Counter(); teams = collections.Counter()
        delivery_keys = collections.Counter(); runs_batter_vals = collections.Counter()
        extras_keys = collections.Counter(); wicket_kinds = collections.Counter()
        wicket_field_variants = collections.Counter()
        has_registry = 0; has_powerplays = 0; has_target = 0
        innings_counts = collections.Counter()
        overs_struct_variants = collections.Counter()
        missing_info_fields = collections.Counter()
        batter_order_check = {"can_reconstruct": True, "notes": []}
        errors = []
        n_deliveries = 0; n_wickets = 0; n_replacements = 0; n_reviews = 0
        kohli_files = []
        sample_delivery = None; sample_wicket = None; sample_info = None
        for i, f in enumerate(files):
            try:
                d = json.load(open(f, encoding="utf-8"))
            except Exception as e:
                errors.append(f"{f.name}: {e}"); continue
            info = d.get("info", {})
            if i == 0:
                sample_info = info
            for k in ["dates","venue","city","teams","toss","outcome","match_type","season","gender","team_type","overs","balls_per_over","players","registry","event"]:
                if k not in info:
                    missing_info_fields[k] += 1
            mt[info.get("match_type", "MISSING")] += 1
            gender[info.get("gender", "MISSING")] += 1
            team_type[info.get("team_type", "MISSING")] += 1
            s = info.get("season", "MISSING"); season[s] += 1
            try:
                for dt in info.get("dates", []):
                    dates.append(dt)
            except: pass
            venues[info.get("venue", "MISSING")] += 1
            for t in info.get("teams", []):
                teams[t] += 1
            if "registry" in info and info["registry"].get("people"):
                has_registry += 1
            # Kohli presence (name string match)
            try:
                pls = info.get("players", {})
                for squad in pls.values():
                    if any("Kohli" in x for x in squad):
                        kohli_files.append(f.name); break
            except: pass
            innings = d.get("innings", [])
            innings_counts[len(innings)] += 1
            for inn in innings:
                if "powerplays" in inn: has_powerplays += 1
                if "target" in inn: has_target += 1
                if "overs" not in inn:
                    overs_struct_variants["no_overs_key"] += 1; continue
                overs = inn["overs"]
                overs_struct_variants[type(overs).__name__] += 1
                for ov in overs:
                    for dl in ov.get("deliveries", []):
                        n_deliveries += 1
                        for k in dl.keys():
                            delivery_keys[k] += 1
                        if sample_delivery is None:
                            sample_delivery = dl
                        r = dl.get("runs", {})
                        runs_batter_vals[r.get("batter", "MISSING")] += 1
                        for ek in (dl.get("extras") or {}).keys():
                            extras_keys[ek] += 1
                        if "wickets" in dl or "wicket" in dl:
                            w = dl.get("wickets") or dl.get("wicket")
                            wicket_field_variants["wickets" if "wickets" in dl else "wicket"] += 1
                            n_wickets += 1
                            items = w if isinstance(w, list) else [w]
                            for wi in items:
                                if isinstance(wi, dict):
                                    wicket_kinds[wi.get("kind", "MISSING")] += 1
                                    if sample_wicket is None:
                                        sample_wicket = dl
                        if "replacements" in dl: n_replacements += 1
                        if "review" in dl or "reviews" in dl: n_reviews += 1
        dates_sorted = sorted(dates)
        report[src_name] = {
            "files": len(files),
            "match_type": dict(mt), "gender": dict(gender),
            "team_type": dict(team_type), "season_min": min(map(str, season)) if season else None,
            "season_max": max(map(str, season)) if season else None, "n_seasons": len(season),
            "date_min": dates_sorted[0] if dates_sorted else None,
            "date_max": dates_sorted[-1] if dates_sorted else None,
            "n_venues": len(venues), "n_teams": len(teams),
            "top_teams": teams.most_common(15),
            "innings_counts": dict(innings_counts),
            "has_registry": has_registry, "has_powerplays_innings": has_powerplays,
            "has_target_innings": has_target,
            "overs_struct": dict(overs_struct_variants),
            "delivery_keys": dict(delivery_keys),
            "runs_batter_distinct": sorted([str(x) for x in runs_batter_vals.keys()])[:30],
            "runs_batter_gt6": sum(c for k, c in runs_batter_vals.items() if isinstance(k, int) and k > 6),
            "extras_keys": dict(extras_keys),
            "wicket_field_variants": dict(wicket_field_variants),
            "wicket_kinds": dict(wicket_kinds),
            "n_deliveries": n_deliveries, "n_wickets": n_wickets,
            "n_replacements": n_replacements, "n_reviews": n_reviews,
            "missing_info_fields": dict(missing_info_fields),
            "kohli_files": len(kohli_files),
            "errors": errors[:10],
            "sample_delivery": sample_delivery, "sample_wicket": sample_wicket,
            "sample_info_keys": sorted(sample_info.keys()) if sample_info else None,
        }
    OUT.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(f"wrote {OUT}")
    for k, v in report.items():
        print(f"\n== {k}: files={v['files']} dates={v['date_min']}..{v['date_max']} ==")
        print(" match_type:", v["match_type"])
        print(" gender:", v["gender"])
        print(" team_type:", v["team_type"])
        print(" seasons:", v["n_seasons"], v["season_min"], "->", v["season_max"])
        print(" innings_counts:", v["innings_counts"])
        print(" delivery_keys:", v["delivery_keys"])
        print(" extras:", v["extras_keys"])
        print(" wickets:", v["wicket_kinds"], v["wicket_field_variants"])
        print(" runs_batter values:", v["runs_batter_distinct"], "gt6:", v["runs_batter_gt6"])
        print(" n_deliveries:", v["n_deliveries"], "n_wickets:", v["n_wickets"])
        print(" missing_info:", v["missing_info_fields"])
        print(" kohli_files:", v["kohli_files"])

if __name__ == "__main__":
    scan()
