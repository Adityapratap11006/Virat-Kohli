"""Phase 2 processed JSONL -> MySQL. Streaming, batched, idempotent.

Idempotency: every table has a natural UNIQUE key; all writes are
INSERT ... ON DUPLICATE KEY UPDATE, so re-running never duplicates.
Order: players -> teams/aliases -> venues -> matches -> innings
-> deliveries+wickets -> batter_innings. FKs enforced by InnoDB.

Usage: python -m db.ingest   (run from repo root; requires migrated DB)
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from etl.config import TEAM_ALIASES

from db import config

PROCESSED = Path(__file__).resolve().parent.parent / "data" / "processed"


def _lines(path: Path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def _executemany_batched(conn, sql: str, rows: list, label: str) -> int:
    cur = conn.cursor()
    total = 0
    for i in range(0, len(rows), config.BATCH_SIZE):
        cur.executemany(sql, rows[i:i + config.BATCH_SIZE])
        conn.commit()
        total += cur.rowcount
        if i % (config.BATCH_SIZE * 10) == 0:
            print(f"  {label}: {min(i + config.BATCH_SIZE, len(rows))}/{len(rows)}",
                  flush=True)
    cur.close()
    return total


def _id_map(conn, table: str, key_col: str) -> dict:
    cur = conn.cursor()
    cur.execute(f"SELECT {key_col}, id FROM {table}")
    out = {k: v for k, v in cur.fetchall()}
    cur.close()
    return out


UPSERT = " AS new ON DUPLICATE KEY UPDATE "


def load_players(conn) -> dict:
    pmap = json.load(open(PROCESSED / "players.json", encoding="utf-8"))
    rows = [(pid, sorted(m["variants"])[0], json.dumps(sorted(m["variants"])),
             json.dumps(m["registry_ids"]), int(m["has_registry_id"]),
             int(m["ambiguous"]))
            for pid, m in pmap.items() if m["variants"]]
    if len(rows) != len(pmap):
        raise RuntimeError("player without variants cannot be named")
    sql = ("INSERT INTO players (player_code, display_name, name_variants,"
           " registry_ids, has_registry_id, ambiguous) VALUES "
           "(%s,%s,%s,%s,%s,%s)" + UPSERT +
           "display_name=new.display_name, name_variants=new.name_variants,"
           " registry_ids=new.registry_ids, has_registry_id=new.has_registry_id,"
           " ambiguous=new.ambiguous")
    _executemany_batched(conn, sql, rows, "players")
    return _id_map(conn, "players", "player_code")


def load_teams(conn, matches_path: Path) -> dict:
    canonical: set[str] = set()
    for m in _lines(matches_path):
        canonical.add(m["team1"])
        canonical.add(m["team2"])
    sql = ("INSERT INTO teams (canonical_name) VALUES (%s)" + UPSERT +
           "canonical_name=new.canonical_name")
    _executemany_batched(conn, sql, [(t,) for t in sorted(canonical)], "teams")
    team_ids = _id_map(conn, "teams", "canonical_name")
    aliases = json.load(open(PROCESSED / "teams.json", encoding="utf-8"))["aliases"]
    for src, canon in aliases.items():
        if canon not in team_ids:
            raise RuntimeError(f"alias target missing: {canon}")
    sql = ("INSERT INTO team_aliases (alias, team_id) VALUES (%s,%s)" + UPSERT +
           "team_id=new.team_id")
    _executemany_batched(conn, sql,
                         [(s, team_ids[c]) for s, c in sorted(aliases.items())],
                         "team_aliases")
    for src, canon in TEAM_ALIASES.items():
        if src in aliases and aliases[src] != canon:
            raise RuntimeError(f"approved alias contradicted: {src}")
    return team_ids


def load_venues(conn, matches_path: Path) -> dict:
    vmap = json.load(open(PROCESSED / "venues.json", encoding="utf-8"))
    groups: set[tuple] = set()
    for m in _lines(matches_path):
        groups.add((m["venue_canonical"], m["city"] or ""))
    rows = []
    for canon, city_key in sorted(groups):
        if canon not in vmap:
            raise RuntimeError(f"venue without resolution entry: {canon}")
        rows.append((canon, city_key or None, city_key,
                     json.dumps(sorted(vmap[canon]["variants"]))))
    sql = ("INSERT INTO venues (canonical_name, city, city_key, name_variants)"
           " VALUES (%s,%s,%s,%s)" + UPSERT +
           "city=new.city, name_variants=new.name_variants")
    _executemany_batched(conn, sql, rows, "venues")
    cur = conn.cursor()
    cur.execute("SELECT canonical_name, city_key, id FROM venues")
    out = {(c, k): i for c, k, i in cur.fetchall()}
    cur.close()
    return out


def _canon_team(name: str) -> str:
    return TEAM_ALIASES.get(name, name)


def load_matches(conn, team_ids: dict, venue_ids: dict) -> dict:
    seen: set[str] = set()
    rows = []
    for m in _lines(PROCESSED / "matches.jsonl"):
        if m["match_id"] in seen:
            raise RuntimeError(f"duplicate source match_id in input: {m['match_id']}")
        seen.add(m["match_id"])
        t1, t2 = m["team1"], m["team2"]
        if _canon_team(m["toss_winner"]) not in (t1, t2):
            raise RuntimeError(f"toss winner not playing: {m['match_id']}")
        try:
            venue_id = venue_ids[(m["venue_canonical"], m["city"] or "")]
            t1_id, t2_id = team_ids[t1], team_ids[t2]
            toss_id = team_ids[_canon_team(m["toss_winner"])]
        except KeyError as e:
            raise RuntimeError(f"unresolved FK in {m['match_id']}: {e}")
        rows.append((m["match_id"], m["source_file"], m["format"], m["date"],
                     m["season"], venue_id, t1_id, t2_id, m["team1_source"],
                     m["team2_source"], toss_id, m["toss_decision"],
                     json.dumps(m["outcome"]), m["dls_method"], m["event"]))
    sql = ("INSERT INTO matches (source_match_id, source_file, format, match_date,"
           " season, venue_id, team1_id, team2_id, team1_source, team2_source,"
           " toss_winner_id, toss_decision, outcome, dls_method, event) VALUES "
           "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" + UPSERT +
           "source_file=new.source_file, venue_id=new.venue_id,"
           " outcome=new.outcome, dls_method=new.dls_method, event=new.event")
    _executemany_batched(conn, sql, rows, "matches")
    return _id_map(conn, "matches", "source_match_id")


def load_innings(conn, match_ids: dict, team_ids: dict) -> dict:
    per_match: dict[str, set] = {}
    rows = []
    for inn in _lines(PROCESSED / "innings.jsonl"):
        if inn["match_id"] not in match_ids:
            raise RuntimeError(f"innings for unknown match: {inn['match_id']}")
        if inn["team"] not in team_ids:
            raise RuntimeError(f"innings unknown team: {inn}")
        per_match.setdefault(inn["match_id"], set()).add(inn["innings_no"])
        rows.append((match_ids[inn["match_id"]], inn["innings_no"],
                     team_ids[inn["team"]], inn["team_source"],
                     inn["classification"], inn["target_runs"],
                     inn["target_overs"], int(inn["had_replacement"])))
    for mid, nos in per_match.items():
        if nos != set(range(1, len(nos) + 1)):
            raise RuntimeError(f"non-contiguous innings numbering: {mid} {sorted(nos)}")
    sql = ("INSERT INTO innings (match_id, innings_no, batting_team_id, team_source,"
           " classification, target_runs, target_overs, had_replacement) VALUES "
           "(%s,%s,%s,%s,%s,%s,%s,%s)" + UPSERT +
           "classification=new.classification, target_runs=new.target_runs,"
           " target_overs=new.target_overs, had_replacement=new.had_replacement")
    _executemany_batched(conn, sql, rows, "innings")
    return _remap_innings(conn, match_ids)


def _remap_innings(conn, match_ids: dict) -> dict:
    cur = conn.cursor()
    cur.execute("SELECT m.source_match_id, i.innings_no, i.id FROM innings i "
                "JOIN matches m ON m.id = i.match_id")
    out = {(mid, no): i for mid, no, i in cur.fetchall()}
    cur.close()
    return out


def load_deliveries(conn, match_ids: dict, player_ids: dict) -> None:
    inn_ids = _remap_innings(conn, match_ids)
    d_rows, w_rows = [], []
    n = 0
    cur = conn.cursor()
    for d in _lines(PROCESSED / "deliveries.jsonl"):
        key = (d["match_id"], d["innings_no"])
        if key not in inn_ids:
            raise RuntimeError(f"delivery for unknown innings: {key}")
        try:
            b = player_ids[d["batter_id"]]
            ns = player_ids[d["non_striker_id"]]
            bo = player_ids[d["bowler_id"]]
        except KeyError as e:
            raise RuntimeError(f"delivery unknown player: {e}")
        iid = inn_ids[key]
        d_rows.append((iid, d["over"], d["seq_in_over"], d["global_seq"],
                       d["actual_delivery"], b, ns, bo, d["runs_batter"],
                       d["runs_extras"], d["runs_total"],
                       json.dumps(d["extras"]), int(d["is_legal_ball"]),
                       int(d["batter_ambiguous"])))
        for w in d["wickets"]:
            if w["player_out_id"] not in player_ids:
                raise RuntimeError(f"wicket unknown player: {w}")
            w_rows.append((iid, d["over"], d["seq_in_over"],
                           player_ids[w["player_out_id"]], w["kind"]))
        n += 1
        if len(d_rows) >= config.BATCH_SIZE * 5:
            _flush_deliveries(conn, cur, d_rows, w_rows)
            d_rows, w_rows = [], []
            print(f"  deliveries: {n} ...", flush=True)
    if d_rows:
        _flush_deliveries(conn, cur, d_rows, w_rows)
    cur.close()
    print(f"  deliveries: {n} done", flush=True)


def _flush_deliveries(conn, cur, d_rows: list, w_rows: list) -> None:
    cur.executemany(
        "INSERT INTO deliveries (innings_id, over_number, seq_in_over, global_seq,"
        " actual_delivery, batter_id, non_striker_id, bowler_id, runs_batter,"
        " runs_extras, runs_total, extras, is_legal_ball, batter_ambiguous) VALUES "
        "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" + UPSERT +
        "global_seq=new.global_seq, actual_delivery=new.actual_delivery,"
        " runs_batter=new.runs_batter, runs_extras=new.runs_extras,"
        " runs_total=new.runs_total, extras=new.extras,"
        " is_legal_ball=new.is_legal_ball, batter_ambiguous=new.batter_ambiguous",
        d_rows)
    cur.executemany(
        "INSERT INTO wickets (innings_id, over_number, seq_in_over, player_out_id,"
        " kind) VALUES (%s,%s,%s,%s,%s)" + UPSERT + "kind=new.kind",
        w_rows)
    conn.commit()


def load_batter_innings(conn, match_ids: dict, player_ids: dict,
                        team_ids: dict) -> None:
    inn_ids = _remap_innings(conn, match_ids)
    cur = conn.cursor()
    cur.execute("SELECT source_match_id, match_date, format FROM matches")
    match_meta = {mid: (str(dt), fmt) for mid, dt, fmt in cur.fetchall()}
    rows = []
    n = 0
    for r in _lines(PROCESSED / "batter_innings.jsonl"):
        key = (r["match_id"], r["innings_no"])
        if key not in inn_ids:
            raise RuntimeError(f"batter-innings for unknown innings: {key}")
        try:
            pid = player_ids[r["batter_id"]]
            tid = team_ids[r["team"]]
        except KeyError as e:
            raise RuntimeError(f"batter-innings unknown ref: {e}")
        mdate, fmt = match_meta[r["match_id"]]
        if fmt != r["format"] or mdate != r["date"]:
            raise RuntimeError(f"batter-innings match mismatch: {r['match_id']}")
        rows.append((pid, match_ids[r["match_id"]], inn_ids[key], tid, mdate, fmt,
                     r["batting_position"], int(r["batting_position_reliable"]),
                     r["runs"], r["balls_faced"], r["dismissal_kind"],
                     int(r["is_dismissed"]), r["entry_team_runs"],
                     r["entry_wickets_lost"], r["entry_balls_bowled"],
                     r["entry_balls_remaining"], r["chase_target"],
                     r["dls_method"], r["source_file"]))
        n += 1
        if len(rows) >= config.BATCH_SIZE * 5:
            _flush_bi(conn, cur, rows)
            rows = []
            print(f"  batter_innings: {n} ...", flush=True)
    if rows:
        _flush_bi(conn, cur, rows)
    cur.close()
    print(f"  batter_innings: {n} done", flush=True)


def _flush_bi(conn, cur, rows: list) -> None:
    cur.executemany(
        "INSERT INTO batter_innings (player_id, match_id, innings_id, batting_team_id,"
        " match_date, format, batting_position, batting_position_reliable, runs,"
        " balls_faced, dismissal_kind, is_dismissed, entry_team_runs,"
        " entry_wickets_lost, entry_balls_bowled, entry_balls_remaining,"
        " chase_target, dls_method, source_file) VALUES "
        "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" + UPSERT +
        "batting_position=new.batting_position,"
        " batting_position_reliable=new.batting_position_reliable, runs=new.runs,"
        " balls_faced=new.balls_faced, dismissal_kind=new.dismissal_kind,"
        " is_dismissed=new.is_dismissed, entry_team_runs=new.entry_team_runs,"
        " entry_wickets_lost=new.entry_wickets_lost,"
        " entry_balls_bowled=new.entry_balls_bowled,"
        " entry_balls_remaining=new.entry_balls_remaining,"
        " chase_target=new.chase_target, dls_method=new.dls_method",
        rows)
    conn.commit()


def ingest() -> None:
    from db.migrate import migrate
    migrate()
    t0 = time.time()
    conn = config.connect()
    try:
        print("players ...", flush=True)
        player_ids = load_players(conn)
        print("teams ...", flush=True)
        team_ids = load_teams(conn, PROCESSED / "matches.jsonl")
        print("venues ...", flush=True)
        venue_ids = load_venues(conn, PROCESSED / "matches.jsonl")
        print("matches ...", flush=True)
        match_ids = load_matches(conn, team_ids, venue_ids)
        print("innings ...", flush=True)
        load_innings(conn, match_ids, team_ids)
        print("deliveries ...", flush=True)
        load_deliveries(conn, match_ids, player_ids)
        print("batter_innings ...", flush=True)
        load_batter_innings(conn, match_ids, player_ids, team_ids)
    finally:
        conn.close()
    print(f"ingest done in {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    ingest()
