"""Dataset loading for Phase 8. Frozen v1 CSV in, split frames out.

Feature groups (documented in docs/ml/model-evaluation.md):
HIST = history-derived (incl. target-encoded venue/opposition);
CTX  = entry context known at the timestamp; POS = batting position fields.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

V1 = Path("data/ml/v1/features.csv")
TARGET = "target_runs"

NUM_ALL = [
    "prior_innings", "avg_5", "avg_10", "avg_20", "sr_10",
    "venue_n", "venue_avg", "venue_sr", "opp_n", "opp_avg", "opp_sr",
    "inn1_avg", "inn2_avg", "chase_avg", "setting_avg",
    "entry_runs", "entry_wkts", "entry_balls", "entry_balls_remaining",
    "entry_overs_completed", "runs_required", "required_rr",
    "batting_position",
]
CAT_LOW = ["format", "innings_no", "is_chase", "pos_reliable"]
CAT_HIGH = ["opposition", "venue_key"]

HIST_NUM = [c for c in NUM_ALL if c not in (
    "entry_runs", "entry_wkts", "entry_balls", "entry_balls_remaining",
    "entry_overs_completed", "runs_required", "required_rr",
    "batting_position")]
CTX_NUM = ["entry_runs", "entry_wkts", "entry_balls", "entry_balls_remaining",
           "entry_overs_completed", "runs_required", "required_rr"]
POS_NUM = ["batting_position"]
POS_CAT = ["pos_reliable"]
CTX_CAT = ["format", "innings_no", "is_chase"]

GROUPS = {
    "history": (HIST_NUM, [], CAT_HIGH),
    "context": (CTX_NUM, CTX_CAT, []),
    "combined": (HIST_NUM + CTX_NUM, CTX_CAT, CAT_HIGH),
    "full": (HIST_NUM + CTX_NUM + POS_NUM, CTX_CAT + POS_CAT, CAT_HIGH),
    "full_nopos": (HIST_NUM + CTX_NUM, CTX_CAT, CAT_HIGH),
}


def load() -> pd.DataFrame:
    df = pd.read_csv(V1)
    assert len(df) == 119619, len(df)
    return df


def splits(df: pd.DataFrame):
    tr = df[df["split"] == "train"].reset_index(drop=True)
    va = df[df["split"] == "val"].reset_index(drop=True)
    te = df[df["split"] == "test"].reset_index(drop=True)
    assert len(tr) == 65143 and len(va) == 10808 and len(te) == 43668
    return tr, va, te
