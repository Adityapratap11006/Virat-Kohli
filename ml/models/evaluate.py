"""Regression metrics + run-range breakdowns."""
import numpy as np
from sklearn.metrics import (mean_absolute_error, mean_squared_error, r2_score,
                             median_absolute_error)

RANGES = [(0, 9, "0-9"), (10, 29, "10-29"), (30, 49, "30-49"), (50, 10**9, "50+")]  # noqa: E501


def metrics(y: np.ndarray, p: np.ndarray) -> dict:
    y = np.asarray(y, dtype=float)
    p = np.asarray(p, dtype=float)
    resid = y - p
    out = {
        "n": int(len(y)),
        "mae": round(float(mean_absolute_error(y, p)), 4),
        "rmse": round(float(np.sqrt(mean_squared_error(y, p))), 4),
        "r2": round(float(r2_score(y, p)), 4),
        "medae": round(float(median_absolute_error(y, p)), 4),
        "mean_actual": round(float(y.mean()), 4),
        "mean_pred": round(float(p.mean()), 4),
        "resid_mean": round(float(resid.mean()), 4),
        "resid_std": round(float(resid.std()), 4),
    }
    by_range = {}
    for lo, hi, name in RANGES:
        m = (y >= lo) & (y <= hi)
        by_range[name] = {"n": int(m.sum()),
                          "mae": round(float(mean_absolute_error(y[m], p[m])), 4)
                          if m.sum() else None}
    out["mae_by_range"] = by_range
    return out
