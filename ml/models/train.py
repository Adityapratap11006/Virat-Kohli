"""Phase 8 training + evaluation. Chronological splits only; test is scored
once, after model selection on validation.

Usage: python -m ml.models.train [--out ml/models/v1]   (repo root)
Deterministic (SEED=7). Saves metrics.json + config.json (tracked) and
model/preprocessor pickles (gitignored binaries, regenerable).
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from ml.models import baselines, data, evaluate
from ml.models.preprocess import FittedPreprocessor, design_matrix

SEED = 7
RIDGE_ALPHAS = [0.1, 1.0, 10.0, 100.0]
XGB_GRID = [
    {"max_depth": 3, "learning_rate": 0.05, "n_estimators": 500},
    {"max_depth": 3, "learning_rate": 0.1, "n_estimators": 300},
    {"max_depth": 4, "learning_rate": 0.05, "n_estimators": 500},
    {"max_depth": 4, "learning_rate": 0.1, "n_estimators": 300},
    {"max_depth": 5, "learning_rate": 0.05, "n_estimators": 300},
    {"max_depth": 3, "learning_rate": 0.05, "n_estimators": 300,
     "subsample": 0.8, "colsample_bytree": 0.8},
    {"max_depth": 4, "learning_rate": 0.05, "n_estimators": 500,
     "subsample": 0.8, "colsample_bytree": 0.8},
    {"max_depth": 3, "learning_rate": 0.05, "n_estimators": 500,
     "reg_alpha": 1.0, "reg_lambda": 2.0},
    {"max_depth": 6, "learning_rate": 0.03, "n_estimators": 500},
    {"max_depth": 2, "learning_rate": 0.1, "n_estimators": 300,
     "min_child_weight": 5},
]
WINDOWS = [("2018", "2019"), ("2019", "2020"), ("2020", "2021"), ("2021", "2022")]


def fit_ridge(Xtr, ytr, alpha):
    from sklearn.linear_model import Ridge
    m = Ridge(alpha=alpha, random_state=SEED)
    m.fit(Xtr, ytr)
    return m


def fit_xgb(Xtr, ytr, Xva, yva, params):
    from xgboost import XGBRegressor
    m = XGBRegressor(tree_method="hist", random_state=SEED, n_jobs=4,
                     early_stopping_rounds=50, eval_metric="mae", **params)
    m.fit(Xtr, ytr, eval_set=[(Xva, yva)], verbose=False)
    return m


def bucket(prior):
    if prior == 0:
        return "debut(0)"
    if prior <= 4:
        return "low(1-4)"
    if prior <= 19:
        return "med(5-19)"
    return "strong(20+)"


def main() -> None:
    t0 = time.time()
    outdir = Path(sys.argv[sys.argv.index("--out") + 1]
                  if "--out" in sys.argv else "ml/models/v1")
    outdir.mkdir(parents=True, exist_ok=True)
    df = data.load()
    tr, va, te = data.splits(df)
    ytr, yva, yte = tr[data.TARGET].to_numpy(), va[data.TARGET].to_numpy(), \
        te[data.TARGET].to_numpy()
    report: dict = {"seed": SEED, "ridge_alphas": RIDGE_ALPHAS,
                    "xgb_grid": XGB_GRID, "validation": {}, "ablation": {},
                    "expanding": {}, "test": {}, "kohli": {}, "error": {}}

    # ---- baselines (val) ----
    base_val = {
        "global_mean": baselines.predict_global_mean(tr, [va])[0],
        "hist_avg": baselines.predict_hist_avg(tr, [va])[0],
        "format_mean": baselines.predict_format_mean(tr, [va])[0],
    }
    for name, p in base_val.items():
        report["validation"][name] = evaluate.metrics(yva, p)
        print(f"val {name}: MAE {report['validation'][name]['mae']}", flush=True)

    # ---- ridge grid (full group, val) ----
    num, low, high = data.GROUPS["full"]
    pre_full = FittedPreprocessor(num, low, high).fit(tr)
    Xtr, ytr2 = design_matrix(pre_full, tr)
    Xva, _ = design_matrix(pre_full, va)
    best_alpha, best_mae = None, 1e9
    for a in RIDGE_ALPHAS:
        m = fit_ridge(Xtr, ytr2, a)
        mae = evaluate.metrics(yva, m.predict(Xva))["mae"]
        report["validation"][f"ridge_a{a}"] = {"mae": mae}
        print(f"val ridge_a{a}: MAE {mae}", flush=True)
        if mae < best_mae:
            best_alpha, best_mae = a, mae
    ridge = fit_ridge(Xtr, ytr2, best_alpha)
    report["validation"]["ridge"] = evaluate.metrics(yva, ridge.predict(Xva))

    # ---- xgb grid (full group, val, early stopping) ----
    best_cfg, best_xgb, best_xmae = None, None, 1e9
    for i, cfg in enumerate(XGB_GRID):
        m = fit_xgb(Xtr, ytr2, Xva, yva, cfg)
        mae = evaluate.metrics(yva, m.predict(Xva))["mae"]
        report["validation"][f"xgb_{i}"] = {"mae": mae, "cfg": cfg,
                                            "best_iter": int(m.best_iteration)}
        print(f"val xgb_{i}: MAE {mae} iters={m.best_iteration}", flush=True)
        if mae < best_xmae:
            best_cfg, best_xgb, best_xmae = cfg, m, mae
    report["validation"]["xgboost"] = evaluate.metrics(yva, best_xgb.predict(Xva))
    report["best"] = {"ridge_alpha": best_alpha, "xgb_cfg": best_cfg}

    # ---- ablation on val (ridge variants + xgb full/nopos) ----
    for gname in ["history", "context", "combined", "full", "full_nopos"]:
        num, low, high = data.GROUPS[gname]
        pre = FittedPreprocessor(num, low, high).fit(tr)
        Xa, _ = design_matrix(pre, tr)
        Xb, _ = design_matrix(pre, va)
        m = fit_ridge(Xa, ytr2, best_alpha)
        report["ablation"][f"ridge_{gname}"] = evaluate.metrics(yva, m.predict(Xb))
    num, low, high = data.GROUPS["full_nopos"]
    pre_np = FittedPreprocessor(num, low, high).fit(tr)
    Xn_tr, _ = design_matrix(pre_np, tr)
    Xn_va, _ = design_matrix(pre_np, va)
    m_np = fit_xgb(Xn_tr, ytr2, Xn_va, yva, best_cfg)
    report["ablation"]["xgb_full_nopos"] = evaluate.metrics(
        yva, m_np.predict(Xn_va))
    report["ablation"]["xgb_full"] = report["validation"]["xgboost"]
    for k, v in report["ablation"].items():
        print(f"abl {k}: MAE {v['mae']} R2 {v['r2']}", flush=True)

    # ---- expanding windows (val years 2019..2022) ----
    for train_end, val_year in WINDOWS:
        wtr = df[df["year"] <= int(train_end)].reset_index(drop=True)
        wva = df[df["year"] == int(val_year)].reset_index(drop=True)
        wyva = wva[data.TARGET].to_numpy()
        prow = {"window": f"train<={train_end} val={val_year}",
                "n_train": len(wtr), "n_val": len(wva)}
        for name, fn in [("global_mean", baselines.predict_global_mean),
                         ("hist_avg", baselines.predict_hist_avg),
                         ("format_mean", baselines.predict_format_mean)]:
            prow[name] = evaluate.metrics(wyva, fn(wtr, [wva])[0])["mae"]
        prew = FittedPreprocessor(*data.GROUPS["full"]).fit(wtr)
        Xwtr, ywtr = design_matrix(prew, wtr)
        Xwva, _ = design_matrix(prew, wva)
        prow["ridge"] = evaluate.metrics(
            wyva, fit_ridge(Xwtr, ywtr, best_alpha).predict(Xwva))["mae"]
        prow["xgboost"] = evaluate.metrics(
            wyva, fit_xgb(Xwtr, ywtr, Xwva, wyva, best_cfg).predict(Xwva))["mae"]
        report["expanding"][val_year] = prow
        print(f"window {val_year}: {prow}", flush=True)

    # ---- TEST (once, after selection) ----
    Xte, _ = design_matrix(pre_full, te)
    test_preds = {
        "global_mean": baselines.predict_global_mean(tr, [te])[0],
        "hist_avg": baselines.predict_hist_avg(tr, [te])[0],
        "format_mean": baselines.predict_format_mean(tr, [te])[0],
        "ridge": ridge.predict(Xte),
        "xgboost": best_xgb.predict(Xte),
    }
    for name, p in test_preds.items():
        report["test"][name] = evaluate.metrics(yte, p)
        print(f"test {name}: {report['test'][name]}", flush=True)

    # ---- error analysis on test (winner = best val MAE exc. test) ----
    winner = min(
        [(k, v["mae"]) for k, v in report["validation"].items()
         if k in ("global_mean", "hist_avg", "format_mean", "ridge", "xgboost")],
        key=lambda kv: kv[1])[0]
    report["winner_val"] = winner
    pw = test_preds[winner]
    te_r = te.reset_index(drop=True)
    err = {}
    for col in ["format", "innings_no"]:
        err[col] = {str(k): evaluate.metrics(
            te_r[data.TARGET][te_r[col] == k].to_numpy(),
            pw[(te_r[col] == k).to_numpy()])["mae"]
            for k in sorted(te_r[col].unique())}
    te_r["__bucket"] = te_r["prior_innings"].map(bucket)
    err["history"] = {k: evaluate.metrics(
        te_r[data.TARGET][te_r["__bucket"] == k].to_numpy(),
        pw[(te_r["__bucket"] == k).to_numpy()])["mae"]
        for k in ["debut(0)", "low(1-4)", "med(5-19)", "strong(20+)"]}
    rel = te_r[te_r["pos_reliable"] == 1]
    err["reliable_pos"] = {}
    for k in sorted(rel["batting_position"].dropna().unique()):
        m = (te_r["pos_reliable"] == 1) & (te_r["batting_position"] == k)
        err["reliable_pos"][str(int(k))] = evaluate.metrics(
            te_r[data.TARGET][m].to_numpy(), pw[m.to_numpy()])["mae"]
    for col, topn in [("opposition", 8), ("venue_name", 8)]:
        top = te_r.groupby(col)[data.TARGET].sum().nlargest(topn).index
        err[col] = {str(k): evaluate.metrics(
            te_r[data.TARGET][te_r[col] == k].to_numpy(),
            pw[(te_r[col] == k).to_numpy()])["mae"] for k in top}
    report["error"] = err

    # ---- Kohli slice (test; general model, no Kohli-only training) ----
    koh = te_r[te_r["batter_code"] == "REG:ba607b88"]
    koh_all = df[df["batter_code"] == "REG:ba607b88"]
    report["kohli"] = {
        "n_test": int(len(koh)), "n_total": int(len(koh_all)),
        "models": {name: evaluate.metrics(
            koh[data.TARGET].to_numpy(), p[(te_r["batter_code"] ==
                                            "REG:ba607b88").to_numpy()])
            for name, p in test_preds.items()},
        "by_format": {str(f): evaluate.metrics(
            koh[data.TARGET][koh["format"] == f].to_numpy(),
            test_preds[winner][(te_r["batter_code"] == "REG:ba607b88").to_numpy()]
            [koh["format"].to_numpy() == f])
            for f in sorted(koh["format"].unique())},
    }
    print(f"kohli test: {report['kohli']}", flush=True)

    # ---- artifacts ----
    (outdir / "metrics.json").write_text(json.dumps(report, indent=2,
                                                    default=str),
                                         encoding="utf-8")
    (outdir / "config.json").write_text(json.dumps(
        {"seed": SEED, "group": "full", "ridge_alpha": best_alpha,
         "xgb": best_cfg, "winner_val": winner,
         "features": pre_full.feature_names_}, indent=2), encoding="utf-8")
    pre_full.save(outdir / "preprocessor.pkl")
    import pickle
    with open(outdir / "ridge.pkl", "wb") as f:
        pickle.dump(ridge, f)
    best_xgb.save_model(outdir / "xgb.ubj")
    print(f"done in {time.time() - t0:.0f}s -> {outdir}")


if __name__ == "__main__":
    main()
