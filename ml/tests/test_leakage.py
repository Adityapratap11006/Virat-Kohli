"""Leakage tests A–H for the Expected Runs feature layer.

Tests A–F run against the pure history unit (no DB); G–I run against the
built dataset in data/ml/v1 (skipped when absent).
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from ml.features.history import BatterHistory

REPO = Path(__file__).resolve().parent.parent.parent
V1 = REPO / "data" / "ml" / "v1" / "features.csv"


def _hist():
    h = BatterHistory()
    h.add("2020-01-01", 10, 8, "v1", "Aus", 1, False)
    h.add("2020-02-01", 50, 40, "v1", "Aus", 2, True)
    h.add("2020-03-01", 0, 2, "v2", "Eng", 1, False)
    return h


def test_A_history_excludes_same_and_later_dates():
    h = _hist()
    s = h.snapshot("2020-02-01", "v1", "Aus")
    assert s["prior_innings"] == 1  # only 2020-01-01; same-day excluded
    assert s["avg_5"] == 10.0
    s2 = h.snapshot("2020-01-01", "v1", "Aus")
    assert s2["prior_innings"] == 0
    assert s2["avg_5"] is None and s2["venue_n"] == 0


def test_B_target_change_does_not_move_features():
    h1, h2 = _hist(), _hist()
    a = h1.snapshot("2020-04-01", "v1", "Aus")
    b = h2.snapshot("2020-04-01", "v1", "Aus")
    assert a == b  # final runs of the target row never enter history


def test_C_entry_state_independent_of_future():
    from ml.features import build as B
    base = (1, 1, "M", "P", "2020-05-01", "ODI", 2, 30, 1, 60, 240,
            250, 4, 1, "v1", "V", "Aus", 99, 80)
    r1 = B.build_row(base, {})
    changed = list(base)
    changed[17] = 5  # target final runs differ...
    changed[18] = 3  # ...as do balls faced
    r2 = B.build_row(tuple(changed), {})
    for k in ("entry_runs", "entry_wkts", "entry_balls", "entry_balls_remaining",
              "runs_required", "required_rr", "avg_5", "venue_avg", "opp_avg"):
        assert r1[k] == r2[k]
    assert r1["runs_required"] == 220
    assert r1["required_rr"] == round(220 * 6.0 / 240, 2)


def test_D_future_match_leaves_earlier_rows_unchanged():
    h = BatterHistory()
    h.add("2020-01-01", 10, 8, "v1", "Aus", 1, False)
    before = h.snapshot("2020-06-01", "v1", "Aus")
    h.add("2021-01-01", 100, 90, "v1", "Aus", 1, False)
    after = h.snapshot("2020-06-01", "v1", "Aus")
    assert before == after


def test_EF_venue_opp_history_strictly_before():
    h = _hist()
    s = h.snapshot("2020-04-01", "v2", "Eng")
    assert s["venue_n"] == 1 and s["venue_avg"] == 0.0
    assert s["opp_n"] == 1 and s["opp_avg"] == 0.0
    s0 = h.snapshot("2020-02-15", "v2", "Eng")
    assert s0["venue_n"] == 0 and s0["opp_n"] == 0


def _dataset():
    if not V1.exists():
        return None
    with open(V1, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_G_temporal_split_no_overlap():
    rows = _dataset()
    if rows is None:
        return
    train = {r["match_date"] for r in rows if r["split"] == "train"}
    val = {r["match_date"] for r in rows if r["split"] == "val"}
    test = {r["match_date"] for r in rows if r["split"] == "test"}
    assert train and val and test
    assert max(train) <= "2021-12-31" and min(val) >= "2022-01-01"
    assert max(val) <= "2022-12-31" and min(test) >= "2023-01-01"


def test_H_unique_batter_innings():
    rows = _dataset()
    if rows is None:
        return
    keys = [(r["match_id"], r["batter_innings_id"]) for r in rows]
    assert len(set(keys)) == len(keys)


def test_I_kohli_anchor():
    rows = _dataset()
    if rows is None:
        return
    k = [r for r in rows if r["batter_code"] == "REG:ba607b88"]
    assert len(k) == 682
    assert sum(int(r["target_runs"]) for r in k) == 28078
    assert {r["format"] for r in k} == {"ODI", "T20I", "IPL"}
    keys = [(r["match_id"], r["batter_innings_id"]) for r in k]
    assert len(set(keys)) == len(keys)
