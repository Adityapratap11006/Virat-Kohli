"""Phase 2 ETL configuration. Paths, V1 scope, canonical maps, rule constants."""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "data" / "raw"
PROCESSED_DIR = REPO_ROOT / "data" / "processed"

# source dir -> canonical V1 format label
FORMAT_BY_SOURCE = {"odis": "ODI", "t20s": "T20I", "ipl": "IPL"}

# --- V1 scope filter (Phase 0 finding: T20I == match_type T20 + international) ---
def in_v1_scope(source: str, info: dict) -> bool:
    if info.get("gender") != "male":
        return False
    mt, tt = info.get("match_type"), info.get("team_type")
    if source == "odis":
        return mt == "ODI"
    if source == "t20s":
        return mt == "T20" and tt == "international"
    if source == "ipl":
        return tt == "club"
    return False

# --- Verified same-franchise renames (observed in data, Phase 2 probe) ---
# Deccan Chargers / Sunrisers Hyderabad intentionally NOT merged (different franchises).
# Defunct sides (Kochi, Pune Warriors, Gujarat Lions) stay separate.
TEAM_ALIASES = {
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Kings XI Punjab": "Punjab Kings",
    "Delhi Daredevils": "Delhi Capitals",
    "Rising Pune Supergiants": "Rising Pune Supergiant",
}

# --- Cricsheet value domains (observed, Phase 0) ---
EXTRAS_KEYS = {"wides", "noballs", "byes", "legbyes", "penalty"}
# player_out events that do NOT count as wickets lost / dismissal
NON_DISMISSAL_WICKET_KINDS = {"retired hurt", "retired not out"}
# kinds that end a batter-innings without a dismissal
RETIRED_KINDS = {"retired hurt", "retired out", "retired not out"}
EXPECTED_BALLS = {"ODI": 300, "T20I": 120, "IPL": 120}
