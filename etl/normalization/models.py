"""Normalized record shapes. Every record carries source provenance."""
from dataclasses import asdict, dataclass


@dataclass
class MatchRecord:
    match_id: str
    source_file: str
    format: str  # ODI | T20I | IPL
    date: str
    season: str
    venue: str
    venue_canonical: str
    city: str | None
    team1: str
    team2: str
    team1_source: str
    team2_source: str
    toss_winner: str
    toss_decision: str
    outcome: dict
    dls_method: str | None
    event: str | None


@dataclass
class InningsRecord:
    match_id: str
    innings_no: int  # 1-based, file order
    team: str
    opposition: str
    team_source: str
    classification: str  # normal | super_over | incomplete
    target_runs: int | None
    target_overs: int | None
    had_replacement: bool = False


@dataclass
class DeliveryRecord:
    match_id: str
    innings_no: int
    over: int
    seq_in_over: int  # 0-based; disambiguates duplicated actual_delivery
    actual_delivery: str
    global_seq: int  # 0-based within innings
    batter_id: str
    non_striker_id: str
    bowler_id: str
    runs_batter: int
    runs_extras: int
    runs_total: int
    extras: dict
    wickets: list  # [{player_out_id, kind}]
    is_legal_ball: bool
    batter_ambiguous: bool = False


@dataclass
class BatterInningsRecord:
    match_id: str
    format: str
    date: str
    innings_no: int
    batter_id: str
    team: str
    opposition: str
    venue_canonical: str
    runs: int
    balls_faced: int
    dismissal_kind: str | None
    is_dismissed: bool
    # entry context: state immediately before the first delivery faced
    entry_team_runs: int
    entry_wickets_lost: int
    entry_balls_bowled: int
    entry_balls_remaining: int
    chase_target: int | None
    batting_position: int | None
    batting_position_reliable: bool
    dls_method: str | None
    source_file: str


def to_json(rec) -> dict:
    return asdict(rec)
