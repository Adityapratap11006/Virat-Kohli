"""Non-ML baselines. All statistics fitted on TRAIN only.

A: global train mean. B: row's historical average (avg_20 ?? avg_10 ??
avg_5, else train global mean for cold-start rows). C: train mean per
format (fallback global mean). No current-innings information anywhere.
"""
import numpy as np
import pandas as pd

TARGET = "target_runs"


def _hist_avg_row(r) -> float | None:
    for c in ("avg_20", "avg_10", "avg_5"):
        v = r[c]
        if v is not None and not (isinstance(v, float) and np.isnan(v)):
            return float(v)
    return None


def predict_global_mean(tr: pd.DataFrame, frames: list) -> list:
    mu = float(tr[TARGET].mean())
    return [np.full(len(f), mu) for f in frames]


def predict_hist_avg(tr: pd.DataFrame, frames: list) -> list:
    mu = float(tr[TARGET].mean())
    out = []
    for f in frames:
        preds = [(_hist_avg_row(r) if _hist_avg_row(r) is not None else mu)
                 for _, r in f.iterrows()]
        out.append(np.array(preds))
    return out


def predict_format_mean(tr: pd.DataFrame, frames: list) -> list:
    mu = float(tr[TARGET].mean())
    per_format = tr.groupby("format")[TARGET].mean().to_dict()
    out = []
    for f in frames:
        preds = [float(per_format.get(fmt, mu)) for fmt in f["format"]]
        out.append(np.array(preds))
    return out
