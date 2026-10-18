"""Power analysis and A/B read-out (two-proportion z-test)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir  # noqa: E402


def n_per_arm(p0, mde, alpha=0.05, power=0.8):
    p1 = p0 + mde
    za, zb = norm.ppf(1 - alpha / 2), norm.ppf(power)
    return int(np.ceil((za + zb) ** 2 * (p0 * (1 - p0) + p1 * (1 - p1)) / mde ** 2))


def main():
    print("Sample size per arm (α=0.05, power=80%)")
    for mde in (0.005, 0.01, 0.015):
        print(f"  baseline 8%, MDE +{mde * 100:.1f} pt -> {n_per_arm(0.08, mde):,}")

    df = pd.read_csv(data_dir(__file__) / "campaign.csv")
    g = df.groupby("treatment").converted.agg(["sum", "count", "mean"])
    pt, pc = g.loc[1, "mean"], g.loc[0, "mean"]
    nt, nc = g.loc[1, "count"], g.loc[0, "count"]
    pool = (g["sum"].sum()) / (nt + nc)
    z = (pt - pc) / np.sqrt(pool * (1 - pool) * (1 / nt + 1 / nc))
    se = np.sqrt(pt * (1 - pt) / nt + pc * (1 - pc) / nc)
    print(f"\nTreatment {pt:.2%} (n={nt:,}) vs holdout {pc:.2%} (n={nc:,})")
    print(f"Absolute lift {100 * (pt - pc):+.2f} pts, 95% CI [{100 * (pt - pc - 1.96 * se):+.2f}, "
          f"{100 * (pt - pc + 1.96 * se):+.2f}], relative lift {pt / pc - 1:+.1%}, p = {2 * (1 - norm.cdf(abs(z))):.2g}")
    inc = (pt - pc) * nt
    print(f"Incremental conversions in treatment arm: {inc:,.0f} of {g.loc[1, 'sum']:,} "
          f"({inc / g.loc[1, 'sum']:.0%} of conversions were caused by the campaign)")


if __name__ == "__main__":
    main()
