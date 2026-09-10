"""Phase 2 pipeline: scan -> validate -> resolve -> normalize -> report.

Deterministic two-pass batch processing over data/raw/{odis,t20s,ipl}.
Pass 1 parses each file once (validation + registry/venue collection);
pass 2 re-reads only usable V1 files. Raw data is never modified.
Outputs (data/processed/, local-only): matches/innings/deliveries/
batter_innings JSONL + players/teams/venues maps + etl_report.json + manifest.

Usage:  python -m etl.pipeline.run [--limit N]   (run from repo root)
"""
import argparse
import datetime
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from etl.config import FORMAT_BY_SOURCE, PROCESSED_DIR, RAW_DIR, TEAM_ALIASES
from etl.derived.batter_innings import build_batter_innings
from etl.normalization.models import to_json
from etl.normalization.normalize import normalize_match
from etl.quality.report import QualityReport
from etl.resolution.players import build_player_map, collect_registry, normalize_name
from etl.resolution.teams import canonical_team
from etl.resolution.venues import VenueMap
from etl.validation.validate import validate_match


def iter_source_files(limit: int | None = None):
    files = []
    for source in ("odis", "t20s", "ipl"):
        files += [(source, p) for p in sorted((RAW_DIR / source).glob("*.json"))]
    return files[:limit] if limit else files


def write_jsonl(path: Path, records: list) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(to_json(rec), separators=(",", ":")) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    t0 = time.time()
    report = QualityReport()
    files = iter_source_files(args.limit)

    # ---- Pass 1: parse, validate, collect registries ----
    parsed, results = [], []
    for i, (source, path) in enumerate(files):
        if i % 500 == 0:
            print(f"pass1 {i}/{len(files)} ...", flush=True)
        report.files_seen += 1
        try:
            data = json.load(open(path, encoding="utf-8"))
        except Exception as e:
            report.parse_failures.append(f"{path.name}: {e}")
            report.dispositions["parse_failure"] += 1
            continue
        r = validate_match(path.stem, source, data)
        results.append((source, path, r))
        report.dispositions[r.disposition] += 1
        for m in r.fatal:
            report.fatal[m.split(":")[0][:80]] += 1
        for w in r.warnings:
            report.warnings[w.split(";")[0][:80]] += 1
        if r.disposition in ("ok", "excluded_incomplete"):
            parsed.append((path.stem, data))
            info = data["info"]
            if not info.get("city"):
                report.missing_city += 1
        if r.disposition == "excluded_anomaly":
            report.quarantined.append(path.name)

    name_to_ids, _ = collect_registry(parsed)
    pmap = build_player_map(name_to_ids)
    venues = VenueMap()
    for _, data in parsed:
        info = data["info"]
        venues.observe(info.get("venue", ""), info.get("city"))
    venues.finalize()

    # ---- Pass 2: normalize usable V1 files ----
    matches, innings_all, deliveries_all, bi_all = [], [], [], []
    seen_ids: set[str] = set()
    for i, (source, path, r) in enumerate(results):
        if i % 500 == 0:
            print(f"pass2 {i}/{len(results)} ...", flush=True)
        if r.disposition != "ok":
            continue
        if path.stem in seen_ids:
            report.fatal["duplicate match_id"] += 1
            continue
        seen_ids.add(path.stem)
        data = json.load(open(path, encoding="utf-8"))
        fmt = FORMAT_BY_SOURCE[source]
        match, inn_recs, del_recs = normalize_match(
            path.stem, path.name, fmt, data, pmap, venues)
        for w in del_recs:
            if w.batter_ambiguous:
                report.ambiguous_hits += 1
        matches.append(match)
        innings_all.extend(inn_recs)
        deliveries_all.extend(del_recs)
        by_inn: dict[int, list] = {}
        for d in del_recs:
            by_inn.setdefault(d.innings_no, []).append(d)
        for inn in inn_recs:
            bi_all.extend(build_batter_innings(
                match, inn, by_inn.get(inn.innings_no, [])))

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(PROCESSED_DIR / "matches.jsonl", matches)
    write_jsonl(PROCESSED_DIR / "innings.jsonl", innings_all)
    write_jsonl(PROCESSED_DIR / "deliveries.jsonl", deliveries_all)
    write_jsonl(PROCESSED_DIR / "batter_innings.jsonl", bi_all)
    (PROCESSED_DIR / "players.json").write_text(json.dumps(
        {pid: m for pid, m in pmap.meta.items()}, indent=1), encoding="utf-8")
    (PROCESSED_DIR / "teams.json").write_text(json.dumps(
        {"aliases": TEAM_ALIASES}, indent=1), encoding="utf-8")
    (PROCESSED_DIR / "venues.json").write_text(json.dumps(
        venues.report(), indent=1), encoding="utf-8")

    for _, d in parsed:
        for t in d["info"].get("teams", []):
            canon, variant = canonical_team(t)
            if variant:
                report.team_variants[f"{t} -> {canon}"] += 1
    report.n_matches = len(matches)
    report.n_innings = len(innings_all)
    report.n_deliveries = len(deliveries_all)
    report.n_batter_innings = len(bi_all)
    report.write(PROCESSED_DIR / "etl_report.json")
    manifest = {
        "processed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "sources": {s: len(list((RAW_DIR / s).glob("*.json"))) for s in FORMAT_BY_SOURCE},
        "records": report.summary()["records"],
    }
    (PROCESSED_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"done in {time.time() - t0:.0f}s")
    report.print_human()


if __name__ == "__main__":
    main()
