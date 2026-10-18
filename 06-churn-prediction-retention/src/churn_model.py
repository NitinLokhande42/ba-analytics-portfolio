"""Train a gradient-boosted churn model, evaluate it and produce the weekly risk-score feed."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir, output_dir  # noqa: E402

try:
    from xgboost import XGBClassifier
    MODEL = XGBClassifier(n_estimators=400, max_depth=4, learning_rate=0.05, subsample=0.8,
                          colsample_bytree=0.8, eval_metric="logloss")
    NAME = "XGBoost"
except ImportError:  # keeps the repo runnable without xgboost
    from sklearn.ensemble import HistGradientBoostingClassifier
    MODEL = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_depth=4, random_state=0)
    NAME = "scikit-learn HistGradientBoosting (install xgboost to use XGBoost)"

FEATS = ["tenure_months", "usage_trend", "sessions_30d", "tickets_90d", "csat_90d",
         "late_payments_6m", "modules_adopted", "plan_basic", "plan_enterprise"]
REASONS = {"usage_trend": "Usage declining", "tickets_90d": "High support contact", "csat_90d": "Low CSAT",
           "late_payments_6m": "Late payments", "modules_adopted": "Low product adoption",
           "tenure_months": "Short tenure", "plan_basic": "Entry plan", "sessions_30d": "Low activity"}
BAD_DIRECTION = {"usage_trend": -1, "tickets_90d": 1, "csat_90d": -1, "late_payments_6m": 1,
                 "modules_adopted": -1, "tenure_months": -1, "plan_basic": 1, "sessions_30d": -1}


def prep(df):
    d = df.copy()
    d["plan_basic"] = (d.plan == "basic").astype(int)
    d["plan_enterprise"] = (d.plan == "enterprise").astype(int)
    return d


def reasons(row, means, stds):
    """Simple, explainable reason codes: features most unfavourable vs. the base (z-score in the bad direction)."""
    z = {f: BAD_DIRECTION[f] * (row[f] - means[f]) / (stds[f] or 1) for f in BAD_DIRECTION}
    top = sorted(z, key=z.get, reverse=True)[:3]
    return [REASONS[f] for f in top]


def main():
    df = prep(pd.read_csv(data_dir(__file__) / "customers.csv"))
    tr, te = train_test_split(df, test_size=0.3, random_state=1, stratify=df.churned_90d)
    MODEL.fit(tr[FEATS], tr.churned_90d)
    p = MODEL.predict_proba(te[FEATS])[:, 1]
    print(f"Model: {NAME}")
    print(f"ROC AUC {roc_auc_score(te.churned_90d, p):.3f} | PR AUC {average_precision_score(te.churned_90d, p):.3f} "
          f"(base rate {te.churned_90d.mean():.1%})")

    te = te.assign(p=p).sort_values("p", ascending=False)
    te["decile"] = np.ceil(np.arange(1, len(te) + 1) / len(te) * 10).astype(int)
    lift = te.groupby("decile").agg(churn_rate=("churned_90d", "mean"), customers=("p", "size"))
    lift["capture"] = te.groupby("decile").churned_90d.sum().cumsum() / te.churned_90d.sum()
    print("\nLift by decile (1 = highest risk)")
    print(lift.round(3).to_string())

    # weekly feed for the whole base
    df["churn_probability"] = MODEL.predict_proba(df[FEATS])[:, 1]
    q90, q75 = df.churn_probability.quantile([0.90, 0.75])
    df["risk_tier"] = np.where(df.churn_probability >= q90, "HIGH", np.where(df.churn_probability >= q75, "MEDIUM", "LOW"))
    means, stds = df[list(BAD_DIRECTION)].mean(), df[list(BAD_DIRECTION)].std()
    feed = df[["customer_id", "churn_probability", "risk_tier", "annual_revenue"]].copy()
    rs = df.apply(lambda r: reasons(r, means, stds), axis=1)
    for i in range(3):
        feed[f"reason_{i + 1}"] = rs.str[i]
    feed["score_date"] = pd.Timestamp("2026-10-19").date()
    feed["model_version"] = "churn_gbm_v1"
    feed.to_csv(output_dir(__file__) / "risk_score_feed.csv", index=False)
    print("\nRisk tiers:", feed.risk_tier.value_counts().to_dict())
    print(feed.sort_values("churn_probability", ascending=False).head(5).round(3).to_string(index=False))


if __name__ == "__main__":
    main()
