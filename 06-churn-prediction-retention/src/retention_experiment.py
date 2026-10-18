"""
Randomized test of the retention workflow.
Simulates outcomes for HIGH + MEDIUM risk customers split 50/50, then analyses them as we would the real test:
two-proportion z-test, confidence interval, revenue protected and portfolio-level retention points.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import output_dir  # noqa: E402

rng = np.random.default_rng(99)
TREATMENT_EFFECT = 0.40  # assumed: workflow prevents ~40% of would-be churn among those contacted
CONTACT_RATE = 0.75      # share of treatment customers actually reached


def sample_size(p1, p2, alpha=0.05, power=0.8):
    z_a, z_b = norm.ppf(1 - alpha / 2), norm.ppf(power)
    pbar = (p1 + p2) / 2
    return int(np.ceil((z_a * np.sqrt(2 * pbar * (1 - pbar)) + z_b * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
                       / (p1 - p2) ** 2))


def main():
    feed = pd.read_csv(output_dir(__file__) / "risk_score_feed.csv")
    total = len(feed)
    tgt = feed[feed.risk_tier.isin(["HIGH", "MEDIUM"])].copy()
    tgt["group"] = np.where(rng.random(len(tgt)) < 0.5, "TREATMENT", "CONTROL")
    churn_p = tgt.churn_probability.values
    reached = (tgt.group == "TREATMENT") & (rng.random(len(tgt)) < CONTACT_RATE)
    churn_p = np.where(reached, churn_p * (1 - TREATMENT_EFFECT), churn_p)
    tgt["churned"] = (rng.random(len(tgt)) < churn_p).astype(int)

    g = tgt.groupby("group").agg(n=("churned", "size"), churn=("churned", "mean"))
    g["retention"] = 1 - g.churn
    print("Sample size needed per arm to detect +5 pts from 75% retention:", sample_size(0.75, 0.80))
    print(g.round(4).to_string())
    pt, pc = g.loc["TREATMENT", "retention"], g.loc["CONTROL", "retention"]
    nt, nc = g.loc["TREATMENT", "n"], g.loc["CONTROL", "n"]
    se = np.sqrt(pt * (1 - pt) / nt + pc * (1 - pc) / nc)
    diff = pt - pc
    z = diff / se
    print(f"\nUplift in targeted tiers: {diff * 100:+.1f} pts (95% CI {100 * (diff - 1.96 * se):+.1f} to "
          f"{100 * (diff + 1.96 * se):+.1f}), p = {2 * (1 - norm.cdf(abs(z))):.4f}")

    portfolio_pts = diff * len(tgt) / total
    saved = diff * len(tgt)
    rev = saved * tgt.annual_revenue.mean()
    print(f"At full rollout (all {len(tgt):,} high/medium-risk customers treated):")
    print(f"  portfolio retention +{portfolio_pts * 100:.1f} pts across {total:,} customers")
    print(f"  ≈{saved:,.0f} customers saved/yr × ${tgt.annual_revenue.mean():,.0f} ≈ ${rev / 1e6:.1f}M revenue protected")


if __name__ == "__main__":
    main()
