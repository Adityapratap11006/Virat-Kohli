"""Team canonicalization. Only verified same-franchise renames are merged;
everything else (incl. Deccan Chargers vs Sunrisers Hyderabad) stays separate.
Original source value is always preserved on the match record."""
from etl.config import TEAM_ALIASES


def canonical_team(name: str) -> tuple[str, bool]:
    """Returns (canonical_name, was_variant)."""
    if name in TEAM_ALIASES:
        return TEAM_ALIASES[name], True
    return name, False
