"""File -> normalized match/innings/delivery records.

Delivery identity: (innings_no, over, seq_in_over) plus global_seq per innings.
actual_delivery is preserved but never used as a unique key (wides/noballs
duplicate it — Phase 0 finding).
"""
from etl.config import EXPECTED_BALLS, NON_DISMISSAL_WICKET_KINDS
from etl.normalization.models import DeliveryRecord, InningsRecord, MatchRecord
from etl.resolution.players import PlayerMap
from etl.resolution.teams import canonical_team
from etl.resolution.venues import VenueMap


def normalize_match(match_id: str, source_file: str, fmt: str, data: dict,
                    pmap: PlayerMap, venues: VenueMap) -> tuple[MatchRecord, list, list]:
    info = data["info"]
    venue = info.get("venue", "")
    canon_venue, _ = venues.resolve(venue)
    s1, s2 = info["teams"][0], info["teams"][1]
    t1, _ = canonical_team(s1)
    t2, _ = canonical_team(s2)
    outcome = info.get("outcome", {})
    match = MatchRecord(
        match_id=match_id, source_file=source_file, format=fmt,
        date=info["dates"][0], season=str(info.get("season", "")),
        venue=venue, venue_canonical=canon_venue, city=info.get("city"),
        team1=t1, team2=t2, team1_source=s1, team2_source=s2,
        toss_winner=info["toss"]["winner"], toss_decision=info["toss"]["decision"],
        outcome=outcome, dls_method=outcome.get("method"),
        event=(info.get("event") or {}).get("name"),
    )
    innings_recs, delivery_recs = [], []
    n_innings = len(data["innings"])
    for idx, inn in enumerate(data["innings"]):
        ino = idx + 1
        classification = "normal"
        if idx >= 2:
            classification = "super_over"
        elif n_innings == 1:
            classification = "incomplete"
        steam = inn["team"]
        team, _ = canonical_team(steam)
        target = inn.get("target") or {}
        had_repl = any("replacements" in dl for ov in inn["overs"]
                       for dl in ov.get("deliveries", []))
        innings_recs.append(InningsRecord(
            match_id=match_id, innings_no=ino, team=team,
            opposition=t2 if team == t1 else t1, team_source=steam,
            had_replacement=had_repl,
            classification=classification,
            target_runs=target.get("runs"), target_overs=target.get("overs"),
        ))
        if classification == "super_over":
            continue  # normalized at header level only; excluded from deliveries/ML
        people = (info.get("registry") or {}).get("people") or {}
        gseq = 0
        for ov in inn["overs"]:
            for seq, dl in enumerate(ov.get("deliveries", [])):
                extras = dl.get("extras") or {}
                w_norm = []
                for w in dl.get("wickets") or []:
                    po = w["player_out"]
                    pid, _, _ = pmap.resolve(po, people.get(po))
                    w_norm.append({"player_out_id": pid, "kind": w["kind"]})
                b_id, b_amb, _ = pmap.resolve(
                    dl["batter"], people.get(dl["batter"]))
                ns_id, _, _ = pmap.resolve(dl["non_striker"], people.get(dl["non_striker"]))
                bo_id, _, _ = pmap.resolve(dl["bowler"], people.get(dl["bowler"]))
                runs = dl["runs"]
                delivery_recs.append(DeliveryRecord(
                    match_id=match_id, innings_no=ino, over=ov.get("over", -1),
                    seq_in_over=seq, actual_delivery=dl["actual_delivery"],
                    global_seq=gseq, batter_id=b_id, non_striker_id=ns_id,
                    bowler_id=bo_id, runs_batter=runs["batter"],
                    runs_extras=runs["extras"], runs_total=runs["total"],
                    extras=dict(extras), wickets=w_norm,
                    is_legal_ball="wides" not in extras and "noballs" not in extras,
                    batter_ambiguous=b_amb,
                ))
                gseq += 1
    return match, innings_recs, delivery_recs


def is_wicket_lost_event(wickets: list) -> bool:
    return any(w["kind"] not in NON_DISMISSAL_WICKET_KINDS for w in wickets)


def expected_balls(fmt: str) -> int:
    return EXPECTED_BALLS[fmt]
