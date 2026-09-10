"""Structural + cricket validation per docs/data/data-quality-rules.md.

Fail loudly (fatal) on structural corruption; flag-and-continue (warning)
on legitimate unusual events. Never rejects runs.batter > 6.
"""
from dataclasses import dataclass, field

from etl.config import EXTRAS_KEYS, in_v1_scope

REQUIRED_DELIVERY_KEYS = {"actual_delivery", "batter", "bowler", "non_striker", "runs"}


@dataclass
class ValidationResult:
    match_id: str
    source: str
    fatal: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    # ok | excluded_non_v1 | excluded_incomplete | excluded_anomaly | invalid
    disposition: str = "ok"

    @property
    def usable(self) -> bool:
        return self.disposition == "ok"


def validate_match(match_id: str, source: str, data: dict) -> ValidationResult:
    r = ValidationResult(match_id=match_id, source=source)
    if not isinstance(data, dict) or not {"meta", "info", "innings"} <= set(data):
        r.fatal.append("missing top-level meta/info/innings")
        r.disposition = "invalid"
        return r
    info = data["info"]
    if not info.get("dates"):
        r.fatal.append("missing info.dates")
    if len(info.get("teams", [])) != 2:
        r.fatal.append(f"info.teams != 2: {info.get('teams')}")
    if "toss" not in info:
        r.fatal.append("missing info.toss")
    if r.fatal:
        r.disposition = "invalid"
        return r

    if not in_v1_scope(source, info):
        r.disposition = "excluded_non_v1"
        return r
    if info.get("balls_per_over", 6) != 6:
        r.fatal.append(f"balls_per_over={info.get('balls_per_over')}")
        r.disposition = "invalid"
        return r
    # Phase 0 anomaly: a few t20s files declare 50 overs -> quarantine
    if source == "t20s" and info.get("overs") == 50:
        r.warnings.append("t20s file declares overs=50; quarantined")
        r.disposition = "excluded_anomaly"
        return r

    innings = data["innings"]
    if len(innings) < 1:
        r.fatal.append("no innings")
        r.disposition = "invalid"
        return r
    if len(innings) == 1:
        r.warnings.append("single-innings (no-result/abandoned) match")
        r.disposition = "excluded_incomplete"
        # still validate structure below before returning
    if len(innings) > 2:
        r.warnings.append(f"{len(innings)} innings entries; index>=2 treated as super-over")

    for i, inn in enumerate(innings):
        if "overs" not in inn or "team" not in inn:
            r.fatal.append(f"innings[{i}] missing overs/team")
            continue
        for ov in inn["overs"]:
            for dl in ov.get("deliveries", []):
                _validate_delivery(r, i, dl)
    if r.fatal:
        r.disposition = "invalid"
    return r


def _validate_delivery(r: ValidationResult, inn_idx: int, dl: dict) -> None:
    missing = REQUIRED_DELIVERY_KEYS - set(dl)
    if missing:
        r.fatal.append(f"innings[{inn_idx}] delivery missing {sorted(missing)}")
        return
    runs = dl["runs"]
    try:
        b, e, t = runs["batter"], runs["extras"], runs["total"]
    except KeyError:
        r.fatal.append(f"innings[{inn_idx}] runs missing batter/extras/total")
        return
    if not all(isinstance(v, int) for v in (b, e, t)):
        r.fatal.append(f"innings[{inn_idx}] non-int runs: {runs}")
        return
    if min(b, e, t) < 0:
        r.fatal.append(f"innings[{inn_idx}] negative runs: {runs}")
        return
    if t != b + e:
        r.fatal.append(f"innings[{inn_idx}] total != batter+extras: {runs}")
        return
    if b > 6:
        r.warnings.append(f"innings[{inn_idx}] runs.batter={b} (overthrows; allowed)")
    extras = dl.get("extras") or {}
    unknown = set(extras) - EXTRAS_KEYS
    if unknown:
        r.fatal.append(f"innings[{inn_idx}] unknown extras keys: {sorted(unknown)}")
    for w in dl.get("wickets") or []:
        if not isinstance(w, dict) or "player_out" not in w or "kind" not in w:
            r.fatal.append(f"innings[{inn_idx}] malformed wicket: {w}")
