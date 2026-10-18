"""
Rolling-origin back-test (last 12 months, 1-month-ahead):
  * Spreadsheet method: last year's same month × brand growth % with planner-style rounding/bias
  * Holt-Winters (damped additive trend, multiplicative seasonality) per SKU
  * Global gradient boosting on lags, seasonality and promo flag
  * Best-of: model chosen per SKU on the first 6 back-test months, scored on the last 6
"""
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from statsmodels.tsa.holtwinters import ExponentialSmoothing

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir, output_dir  # noqa: E402

warnings.filterwarnings("ignore")
rng = np.random.default_rng(0)
TEST = 12


def accuracy(actual, fcst):
    return 1 - np.sum(np.abs(actual - fcst)) / np.sum(actual)


def spreadsheet(hist):
    """Last year same month × trailing-12 growth, plus judgmental adjustment (~±20%, slight over-forecast bias)."""
    growth = hist[-12:].sum() / hist[-24:-12].sum()
    return hist[-12] * growth * rng.normal(1.06, 0.26)


def holt_winters(hist):
    m = ExponentialSmoothing(hist, trend="add", damped_trend=True, seasonal="mul", seasonal_periods=12,
                             initialization_method="estimated").fit()
    return float(m.forecast(1)[0])


def features(df):
    df = df.sort_values(["sku_id", "month_start"]).copy()
    df["log_qty"] = np.log1p(df.qty)
    g = df.groupby("sku_id")["log_qty"]
    for lag in (1, 2, 3, 12):
        df[f"lag{lag}"] = g.shift(lag)
    df["roll3"] = g.transform(lambda s: s.shift(1).rolling(3).mean())
    df["moy"] = df.month_start.dt.month
    df["sin"], df["cos"] = np.sin(2 * np.pi * df.moy / 12), np.cos(2 * np.pi * df.moy / 12)
    df["therapy_code"] = df.therapy.astype("category").cat.codes
    return df


FEATS = ["lag1", "lag2", "lag3", "lag12", "roll3", "sin", "cos", "promo_flag", "therapy_code"]


def main():
    df = pd.read_csv(data_dir(__file__) / "sku_monthly.csv", parse_dates=["month_start"])
    months = sorted(df.month_start.unique())
    test_months = months[-TEST:]
    fe = features(df)
    out = []
    for tm in test_months:
        train = fe[(fe.month_start < tm)].dropna(subset=FEATS)
        gbm = HistGradientBoostingRegressor(max_iter=200, learning_rate=0.05, random_state=0)
        gbm.fit(train[FEATS], train.log_qty)
        cur = fe[fe.month_start == tm]
        gbm_pred = dict(zip(cur.sku_id, np.expm1(gbm.predict(cur[FEATS]))))
        for sku, g in df[df.month_start <= tm].groupby("sku_id"):
            hist = g.qty.values[:-1].astype(float)
            out.append({"month": tm, "sku_id": sku, "actual": g.qty.values[-1],
                        "unit_cost": g.unit_cost_inr.values[-1],
                        "spreadsheet": spreadsheet(hist), "holt_winters": holt_winters(hist), "gbm": gbm_pred[sku]})
    bt = pd.DataFrame(out)
    bt["ensemble"] = (bt.holt_winters + bt.gbm) / 2

    # ABC classification on value
    val = bt.groupby("sku_id").apply(lambda g: (g.actual * g.unit_cost).sum()).sort_values(ascending=False)
    cum = val.cumsum() / val.sum()
    abc = pd.Series(np.where(cum <= 0.8, "A", np.where(cum <= 0.95, "B", "C")), index=val.index)
    bt["abc"] = bt.sku_id.map(abc)

    # best-of selection: choose per SKU on first half, evaluate on second half
    first, second = bt[bt.month < test_months[6]], bt[bt.month >= test_months[6]]
    cands = ["holt_winters", "gbm", "ensemble"]
    choice = first.groupby("sku_id").apply(
        lambda g: min(cands, key=lambda c: np.abs(g.actual - g[c]).sum()))
    second = second.assign(best_of=[r[choice[r.sku_id]] for _, r in second.iterrows()])

    print("Forecast accuracy (1 − WMAPE), 1-month ahead, last 6 months")
    res = {m: accuracy(second.actual, second[m]) for m in ["spreadsheet", "holt_winters", "gbm", "ensemble", "best_of"]}
    for m, a in res.items():
        print(f"  {m:<13} {a:.1%}")
    print("\nBy ABC class (spreadsheet vs best-of)")
    for c, g in second.groupby("abc"):
        print(f"  {c}: {accuracy(g.actual, g.spreadsheet):.1%} -> {accuracy(g.actual, g.best_of):.1%}  ({g.sku_id.nunique()} SKUs)")
    print("\nModel chosen per SKU:", choice.value_counts().to_dict())
    bias = (second.spreadsheet.sum() - second.actual.sum()) / second.actual.sum()
    print(f"Spreadsheet bias: {bias:+.1%}  |  best-of bias: "
          f"{(second.best_of.sum() - second.actual.sum()) / second.actual.sum():+.1%}")
    bt.merge(second[["month", "sku_id", "best_of"]], on=["month", "sku_id"], how="left").to_csv(
        output_dir(__file__) / "backtest.csv", index=False)


if __name__ == "__main__":
    main()
