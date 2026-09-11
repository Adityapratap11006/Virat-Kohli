"""Registry validity + coverage for data/reference/venue_aliases.csv."""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from db.canonical_venues import REGISTRY, VALID_CONF, VALID_TYPES, canonical_key

REPO = Path(__file__).resolve().parent.parent.parent


def _rows():
    with open(REGISTRY, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_registry_columns_and_enums():
    rows = _rows()
    assert len(rows) == 486
    for r in rows:
        assert r["mapping_type"] in VALID_TYPES
        assert r["confidence"] in VALID_CONF
        assert r["canonical_venue_name"] and r["source"]
    keys = [(r["raw_venue_name"], r["raw_city"]) for r in rows]
    assert len(set(keys)) == len(keys)
    ckeys = [canonical_key(r["canonical_venue_name"], r["canonical_city"])
             for r in rows]
    assert all(ckeys)


def test_historical_renames_present():
    rows = _rows()
    by_raw = {(r["raw_venue_name"], r["raw_city"]): r for r in rows}
    feroz = by_raw[("Feroz Shah Kotla", "Delhi")]
    assert feroz["mapping_type"] == "HISTORICAL_RENAME"
    assert (feroz["canonical_venue_name"], feroz["canonical_city"]) == \
        ("Arun Jaitley Stadium", "Delhi")
    motera = by_raw[("Sardar Patel Stadium, Motera", "Ahmedabad")]
    assert motera["mapping_type"] == "HISTORICAL_RENAME"
    assert motera["canonical_venue_name"] == "Narendra Modi Stadium"


def test_chinnaswamy_collapses():
    rows = _rows()
    chin = [r for r in rows if "hinnaswamy" in r["raw_venue_name"]]
    assert len(chin) == 3
    assert {(r["canonical_venue_name"], r["canonical_city"]) for r in chin} == \
        {("M Chinnaswamy Stadium", "Bengaluru")}


def test_distinct_grounds_stay_split():
    rows = _rows()
    by_raw = {(r["raw_venue_name"], r["raw_city"]): r for r in rows}
    county = {by_raw[("County Ground", "Bristol")]["canonical_city"],
              by_raw[("County Ground", "Taunton")]["canonical_city"],
              by_raw[("County Ground, Chelmsford", "Chelmsford")]["canonical_city"]}
    assert county == {"Bristol", "Taunton", "Chelmsford"}
    assert by_raw[("National Stadium", "Karachi")]["canonical_city"] == "Karachi"
    assert by_raw[("National Stadium", "Hamilton")]["canonical_city"] == "Hamilton"


def test_null_city_never_invented_raw():
    processed = REPO / "data" / "processed" / "matches.jsonl"
    if not processed.exists():
        return
    import json
    null_raw = set()
    for line in open(processed, encoding="utf-8"):
        m = json.loads(line)
        if not m["city"]:
            null_raw.add((m["venue_canonical"], ""))
    rows = _rows()
    by_raw_name = {}
    for r in rows:
        by_raw_name.setdefault(r["raw_venue_name"], set()).add(r["raw_city"])
    for name, _ in null_raw:
        assert "" in by_raw_name[name], f"raw null city overwritten for {name}"


def test_coverage_of_processed_venues():
    processed = REPO / "data" / "processed" / "matches.jsonl"
    if not processed.exists():
        return
    import json
    needed = set()
    for line in open(processed, encoding="utf-8"):
        m = json.loads(line)
        needed.add((m["venue_canonical"], m["city"] or ""))
    rows = _rows()
    raw_keys = {(r["raw_venue_name"], r["raw_city"]) for r in rows}
    assert needed <= raw_keys
