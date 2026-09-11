"""Load data/reference/venue_aliases.csv into canonical_venues + venue_aliases.

Every raw venue row must map to exactly one canonical venue; unknown mapping
types, unresolvable raw keys, or duplicate raw keys fail loudly. Idempotent
via natural-key upserts.
"""
import csv
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db import config

REGISTRY = Path(__file__).resolve().parent.parent / "data" / "reference" / "venue_aliases.csv"
VALID_TYPES = {"EXACT", "NORMALIZED_ALIAS", "HISTORICAL_RENAME", "CURATED_ALIAS", "UNRESOLVED"}
VALID_CONF = {"high", "medium", "low"}


def canonical_key(name: str, city: str) -> str:
    slug = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", slug.lower()).strip("-")
    cslug = re.sub(r"[^a-z0-9]+", "-", city.lower()).strip("-") if city else "no-city"
    return f"{slug}__{cslug}"


def load_rows() -> list:
    if not REGISTRY.exists():
        raise RuntimeError(f"missing registry: {REGISTRY}")
    with open(REGISTRY, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    required = {"raw_venue_name", "raw_city", "canonical_venue_name", "canonical_city",
                "canonical_country", "mapping_type", "confidence", "source"}
    if set(rows[0]) != required:
        raise RuntimeError(f"bad registry columns: {list(rows[0])}")
    seen = set()
    for r in rows:
        if r["mapping_type"] not in VALID_TYPES:
            raise RuntimeError(f"bad mapping_type: {r}")
        if r["confidence"] not in VALID_CONF:
            raise RuntimeError(f"bad confidence: {r}")
        if not r["canonical_venue_name"] or not r["source"]:
            raise RuntimeError(f"missing canonical/source: {r}")
        key = (r["raw_venue_name"], r["raw_city"])
        if key in seen:
            raise RuntimeError(f"duplicate raw key: {key}")
        seen.add(key)
    return rows


def load_canonical(conn, rows: list) -> dict:
    cur = conn.cursor()
    cur.execute("SELECT canonical_name, city_key, id FROM venues")
    raw_ids = {(c, k): i for c, k, i in cur.fetchall()}
    canon_rows = {}
    for r in rows:
        key = (r["raw_venue_name"], r["raw_city"])
        if key not in raw_ids:
            raise RuntimeError(f"registry raw key has no venue row: {key}")
        ck = canonical_key(r["canonical_venue_name"], r["canonical_city"])
        val = (r["canonical_venue_name"],
               r["canonical_city"] or None,
               r["canonical_country"] or None)
        if ck in canon_rows and canon_rows[ck] != val:
            raise RuntimeError(f"canonical key collision: {ck}: "
                               f"{canon_rows[ck]} vs {val}")
        canon_rows[ck] = val
    from db.ingest import _executemany_batched, UPSERT
    _executemany_batched(
        conn,
        "INSERT INTO canonical_venues (canonical_key, canonical_name, city, country)"
        " VALUES (%s,%s,%s,%s)" + UPSERT +
        "canonical_name=new.canonical_name, city=new.city, country=new.country",
        [(k, n, c, co) for k, (n, c, co) in sorted(canon_rows.items())],
        "canonical_venues")
    cur.execute("SELECT canonical_key, id FROM canonical_venues")
    canon_ids = {k: i for k, i in cur.fetchall()}
    alias_rows = []
    for r in rows:
        ck = canonical_key(r["canonical_venue_name"], r["canonical_city"])
        alias_rows.append((raw_ids[(r["raw_venue_name"], r["raw_city"])],
                           canon_ids[ck], r["mapping_type"], r["confidence"],
                           r["source"][:512]))
    _executemany_batched(
        conn,
        "INSERT INTO venue_aliases (raw_venue_id, canonical_venue_id, mapping_type,"
        " confidence, source) VALUES (%s,%s,%s,%s,%s)" + UPSERT +
        "canonical_venue_id=new.canonical_venue_id, mapping_type=new.mapping_type,"
        " confidence=new.confidence, source=new.source",
        alias_rows, "venue_aliases")
    cur.execute("SELECT COUNT(*) FROM venues v LEFT JOIN venue_aliases a "
                "ON a.raw_venue_id = v.id WHERE a.raw_venue_id IS NULL")
    orphan = cur.fetchone()[0]
    cur.close()
    if orphan:
        raise RuntimeError(f"{orphan} raw venues without canonical mapping")
    return canon_ids
