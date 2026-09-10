"""Batter-innings construction (feeds Phase 7 feature engineering, not the model).

One row per batter per normal innings (index 0/1). Entry context = innings
state immediately before the FIRST DELIVERY FACED (per feature contract).
Batting position = first-appearance order; reliable only in clean innings
(no replacements, no retired-*. DNB players never appear, so they get no row).
"""
from etl.config import NON_DISMISSAL_WICKET_KINDS, RETIRED_KINDS
from etl.normalization.models import BatterInningsRecord, DeliveryRecord, InningsRecord, MatchRecord
from etl.normalization.normalize import expected_balls, is_wicket_lost_event


def build_batter_innings(match: MatchRecord, inn: InningsRecord,
                         deliveries: list) -> list:
    if inn.classification != "normal":
        return []
    total_balls = expected_balls(match.format)
    # batting order: first appearance as batter OR non-striker
    order: list[str] = []
    for dl in deliveries:
        for pid in (dl.batter_id, dl.non_striker_id):
            if pid not in order:
                order.append(pid)
    messy = inn.had_replacement or any(
        w["kind"] in RETIRED_KINDS
        for dl in deliveries for w in dl.wickets)
    rows: list[BatterInningsRecord] = []
    by_batter: dict[str, BatterInningsRecord] = {}
    order_idx = {pid: i + 1 for i, pid in enumerate(order)}
    runs = wkts = legal = 0
    for dl in deliveries:
        b = dl.batter_id
        if b not in by_batter:
            pos = order_idx.get(b)
            row = BatterInningsRecord(
                match_id=match.match_id, format=match.format, date=match.date,
                innings_no=inn.innings_no, batter_id=b, team=inn.team,
                opposition=inn.opposition, venue_canonical=match.venue_canonical,
                runs=0, balls_faced=0, dismissal_kind=None, is_dismissed=False,
                entry_team_runs=runs, entry_wickets_lost=wkts,
                entry_balls_bowled=legal,
                entry_balls_remaining=max(0, total_balls - legal),
                chase_target=inn.target_runs,
                batting_position=pos,
                batting_position_reliable=pos is not None and not messy,
                dls_method=match.dls_method, source_file=match.source_file,
            )
            rows.append(row)
            by_batter[b] = row
        row = by_batter[b]
        row.runs += dl.runs_batter
        if "wides" not in dl.extras:
            row.balls_faced += 1
        for w in dl.wickets:
            if w["player_out_id"] != b:
                continue
            if w["kind"] in NON_DISMISSAL_WICKET_KINDS:
                row.dismissal_kind = w["kind"]
            elif w["kind"] in RETIRED_KINDS:
                row.dismissal_kind = w["kind"]
                row.is_dismissed = w["kind"] == "retired out"
            else:
                row.dismissal_kind = w["kind"]
                row.is_dismissed = True
        runs += dl.runs_total
        if is_wicket_lost_event(dl.wickets):
            wkts += 1
        if dl.is_legal_ball:
            legal += 1
    return rows
