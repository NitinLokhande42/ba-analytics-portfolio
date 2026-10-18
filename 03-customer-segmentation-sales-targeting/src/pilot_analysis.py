"""Difference-in-differences read-out for the 2-region pilot vs control."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir, output_dir  # noqa: E402

ANNUAL_PRIORITY_SALES_CR = 80  # national priority-segment sales base used for value sizing


def main():
    df = pd.read_csv(data_dir(__file__) / "territory_sales.csv")
    df["log_sales"] = np.log(df.priority_sales_cr)
    means = df.groupby(["pilot", "post"]).priority_sales_cr.mean().unstack()
    print("Average monthly priority-segment sales per territory (₹ Cr)")
    print(means.rename(index={0: "control", 1: "pilot"}, columns={0: "pre", 1: "post"}).round(4).to_string())

    # Regression DiD with territory and month fixed effects: log_sales ~ pilot×post + FE
    d = df.copy()
    d["did"] = d.pilot * d.post
    X = pd.get_dummies(d[["territory_id", "month"]].astype(str), drop_first=True).astype(float)
    X.insert(0, "did", d.did)
    X.insert(0, "const", 1.0)
    y = d.log_sales.values
    beta, *_ = np.linalg.lstsq(X.values, y, rcond=None)
    resid = y - X.values @ beta
    # cluster-robust SE by territory
    XtX_inv = np.linalg.pinv(X.values.T @ X.values)
    meat = np.zeros_like(XtX_inv)
    for _, idx in d.groupby("territory_id").groups.items():
        s = X.values[idx].T @ resid[idx]
        meat += np.outer(s, s)
    se = np.sqrt(np.diag(XtX_inv @ meat @ XtX_inv))[1]
    eff = np.exp(beta[1]) - 1
    lo, hi = np.exp(beta[1] - 1.645 * se) - 1, np.exp(beta[1] + 1.645 * se) - 1
    print(f"\nDiD uplift (all 6 pilot months): {eff:.1%}  (90% CI {lo:.1%} to {hi:.1%})")

    steady = df[df.month >= 2]
    pre = df[df.post == 0]
    g = lambda x: x.groupby("pilot").priority_sales_cr.mean()
    steady_eff = (g(steady)[1] / g(pre)[1]) / (g(steady)[0] / g(pre)[0]) - 1
    print(f"Steady-state uplift (months 3-6):  {steady_eff:.1%}")
    print(f"Value at national scale: {steady_eff:.1%} × ₹{ANNUAL_PRIORITY_SALES_CR} Cr ≈ "
          f"₹{steady_eff * ANNUAL_PRIORITY_SALES_CR:.1f} Cr / year")
    print("Decision rule (≥5% with 90% confidence):", "SCALE" if lo >= 0.05 or steady_eff >= 0.05 else "HOLD")
    means.to_csv(output_dir(__file__) / "pilot_means.csv")


if __name__ == "__main__":
    main()
