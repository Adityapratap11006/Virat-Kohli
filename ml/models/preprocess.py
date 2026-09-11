"""Train-only fitted preprocessing. Encoders see training data exclusively;
validation/test rows are transformed with frozen statistics.

Numerics: median imputation (medians from train). Low-cardinality cats:
one-hot (unknown -> all zeros). High-cardinality cats (opposition,
venue_key): smoothed target encoding
  enc = (n * mean + m * global) / (n + m), m = 20,
unseen -> global train mean. All state lives in FittedPreprocessor,
persisted with the model.
"""
import pickle

import numpy as np
import pandas as pd

TARGET = "target_runs"
SMOOTH_M = 20.0


class TargetEncoder:
    def __init__(self, cols: list, m: float = SMOOTH_M):
        self.cols = cols
        self.m = m
        self.global_mean_: float = 0.0
        self.maps_: dict = {}

    def fit(self, X: pd.DataFrame, y: pd.Series):
        self.global_mean_ = float(y.mean())
        for c in self.cols:
            g = y.groupby(X[c]).agg(["mean", "count"])
            self.maps_[c] = ((g["count"] * g["mean"] + self.m * self.global_mean_)
                             / (g["count"] + self.m)).to_dict()
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=X.index)
        for c in self.cols:
            out[c + "__te"] = X[c].map(self.maps_[c]).fillna(self.global_mean_)
        return out


class FittedPreprocessor:
    def __init__(self, num_cols: list, low_cols: list, high_cols: list):
        self.num_cols = num_cols
        self.low_cols = low_cols
        self.high_cols = high_cols
        self.medians_: dict = {}
        self.low_levels_: dict = {}
        self.encoder_: TargetEncoder | None = None
        self.feature_names_: list = []

    def fit(self, df: pd.DataFrame):
        y = df[TARGET]
        for c in self.num_cols:
            self.medians_[c] = float(df[c].median())
        for c in self.low_cols:
            self.low_levels_[c] = sorted(str(v) for v in df[c].dropna().unique())
        if self.high_cols:
            self.encoder_ = TargetEncoder(self.high_cols).fit(df, y)
        self.feature_names_ = (
            list(self.num_cols)
            + [f"{c}={v}" for c in self.low_cols for v in self.low_levels_[c]]
            + ([c + "__te" for c in self.high_cols] if self.high_cols else []))
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        parts = []
        num = pd.DataFrame(index=df.index)
        for c in self.num_cols:
            num[c] = pd.to_numeric(df[c], errors="coerce").fillna(self.medians_[c])
        parts.append(num)
        for c in self.low_cols:
            s = df[c].astype(str)
            for v in self.low_levels_[c]:
                parts.append(pd.DataFrame({f"{c}={v}": (s == v).astype(float)},
                                          index=df.index))
        if self.high_cols:
            assert self.encoder_ is not None
            parts.append(self.encoder_.transform(df))
        return pd.concat(parts, axis=1)[self.feature_names_]

    def save(self, path) -> None:
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path):
        with open(path, "rb") as f:
            return pickle.load(f)


def design_matrix(pre: FittedPreprocessor, df: pd.DataFrame):
    return pre.transform(df).to_numpy(dtype=np.float64), \
        df[TARGET].to_numpy(dtype=np.float64)
