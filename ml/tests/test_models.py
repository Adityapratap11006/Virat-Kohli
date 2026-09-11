"""Phase 8 model tests: baselines, split integrity, train-only fitting,
determinism, shapes, Kohli selection. No test-set tuning anywhere."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from ml.models import baselines, data
from ml.models.preprocess import FittedPreprocessor

V1 = Path("data/ml/v1/features.csv")


def _toy(n=40, seed=0):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "target_runs": rng.integers(0, 100, n).astype(float),
        "avg_20": rng.uniform(5, 60, n),
        "avg_10": rng.uniform(5, 60, n),
        "avg_5": rng.uniform(5, 60, n),
        "format": rng.choice(["ODI", "T20I"], n),
        "opposition": rng.choice(["Aus", "Eng"], n),
        "venue_key": rng.choice(["v1", "v2"], n),
        "split": ["train"] * (n // 2) + ["val"] * (n - n // 2),
    })


def test_baseline_shapes_and_cold_start():
    df = _toy()
    tr = df.iloc[:20]
    df.loc[20, ["avg_20", "avg_10", "avg_5"]] = np.nan
    outs = [baselines.predict_global_mean(tr, [df.iloc[20:]])[0],
            baselines.predict_hist_avg(tr, [df.iloc[20:]])[0],
            baselines.predict_format_mean(tr, [df.iloc[20:]])[0]]
    for o in outs:
        assert o.shape == (20,) and np.all(np.isfinite(o))


def test_target_never_a_feature():
    for _, (num, low, high) in data.GROUPS.items():
        assert data.TARGET not in num + low + high


def test_split_integrity_on_frozen_csv():
    if not V1.exists():
        return
    df = pd.read_csv(V1, usecols=["split", "match_date"])
    assert (df.loc[df["split"] == "train", "match_date"] <= "2021-12-31").all()
    assert ((df.loc[df["split"] == "val", "match_date"] >= "2022-01-01")
            & (df.loc[df["split"] == "val", "match_date"] <= "2022-12-31")).all()
    assert (df.loc[df["split"] == "test", "match_date"] >= "2023-01-01").all()


def test_preprocessor_train_only_and_unseen_category():
    df = _toy(60)
    tr, va = df.iloc[:30], df.iloc[30:]
    pre = FittedPreprocessor(["avg_20"], ["format"], ["opposition"]).fit(tr)
    va2 = va.copy()
    va2.loc[va2.index[0], "opposition"] = "NeverSeen"
    Xt, _ = pre.transform(tr), None
    Xv = pre.transform(va2)
    assert list(Xv.columns) == list(Xt.columns)
    assert np.all(np.isfinite(Xv.to_numpy()))
    row0 = Xv.iloc[0]
    assert row0["opposition__te"] == pre.encoder_.global_mean_


def test_ridge_deterministic():
    from sklearn.linear_model import Ridge
    df = _toy(60)
    tr, va = df.iloc[:30], df.iloc[30:]
    pre = FittedPreprocessor(["avg_20"], ["format"], ["opposition"]).fit(tr)
    Xtr = pre.transform(tr).to_numpy()
    Xva = pre.transform(va).to_numpy()
    ytr = tr["target_runs"].to_numpy()
    p1 = Ridge(alpha=1.0, random_state=7).fit(Xtr, ytr).predict(Xva)
    p2 = Ridge(alpha=1.0, random_state=7).fit(Xtr, ytr).predict(Xva)
    assert np.array_equal(p1, p2)


def test_kohli_selection_from_csv():
    if not V1.exists():
        return
    df = pd.read_csv(V1, usecols=["batter_code", "target_runs", "format", "split"])
    k = df[df["batter_code"] == "REG:ba607b88"]
    assert len(k) == 682 and int(k["target_runs"].sum()) == 28078
    assert set(k["format"]) == {"ODI", "T20I", "IPL"}
