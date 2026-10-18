"""Train and evaluate the no-show risk score; assign outreach tiers and check fairness."""
import sys
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir, output_dir  # noqa: E402

NUM = ["lead_time_days", "age", "prior_no_shows_12m", "distance_miles"]
CAT = ["specialty", "payer", "monday_or_friday"]
TIERS = [(0.30, "High", "live_agent_call"), (0.15, "Medium", "sms_plus_ivr"), (0.0, "Low", "sms_only")]


def tier(p):
    for cut, name, _ in TIERS:
        if p >= cut:
            return name


def main():
    df = pd.read_csv(data_dir(__file__) / "appointments.csv")
    X, y = df[NUM + CAT], df["no_show"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
    model = Pipeline([
        ("prep", ColumnTransformer([("num", StandardScaler(), NUM),
                                    ("cat", OneHotEncoder(handle_unknown="ignore"), CAT)])),
        ("clf", LogisticRegression(max_iter=1000)),
    ]).fit(Xtr, ytr)
    p = model.predict_proba(Xte)[:, 1]
    print(f"No-show model ROC AUC: {roc_auc_score(yte, p):.3f}  (acceptance target ≥ 0.70)")

    res = Xte.copy()
    res["no_show"], res["risk"] = yte.values, p
    res["tier"] = res["risk"].apply(tier)
    summary = res.groupby("tier").agg(appointments=("risk", "size"), avg_risk=("risk", "mean"),
                                      actual_no_show=("no_show", "mean"))
    summary["share_of_no_shows"] = res.groupby("tier")["no_show"].sum() / res["no_show"].sum()
    print("\nOutreach tiers")
    print(summary.loc[["High", "Medium", "Low"]].round(3).to_string())

    # Fairness check (HC-23): recall of High+Medium tiers by payer
    res["flagged"] = res["tier"].isin(["High", "Medium"])
    ns = res[res.no_show == 1]
    recall = ns.groupby("payer")["flagged"].mean()
    print("\nShare of actual no-shows flagged (High/Medium) by payer")
    print(recall.round(3).to_string())
    print(f"Overall: {ns['flagged'].mean():.3f}")

    summary.to_csv(output_dir(__file__) / "tier_summary.csv")


if __name__ == "__main__":
    main()
