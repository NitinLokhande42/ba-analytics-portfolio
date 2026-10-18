"""Monte Carlo NPV, scorecard and capex-constrained portfolio selection."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir, output_dir  # noqa: E402

rng = np.random.default_rng(123)
SIMS, YEARS, WACC, TAX = 10_000, 10, 0.12, 0.252
CAPEX_BUDGET = 90.0  # ₹ Cr available this cycle
WEIGHTS = {"enpv_per_inv": .30, "downside": .20, "payback": .10, "strategic_fit": .15,
           "capability_fit": .15, "competition_score": .10}


def tri(lo, ml, hi, n):
    return rng.triangular(lo, ml, max(hi, ml + 1e-9), n)


def simulate(p):
    peak = tri(p.peak_sales_low, p.peak_sales_ml, p.peak_sales_high, SIMS)
    t_peak = tri(3, 4, 6, SIMS)
    erosion = tri(0.03, 0.06, 0.12, SIMS)
    mkt = tri(0.08, 0.10, 0.14, SIMS)
    capex = tri(p.capex_low, p.capex_ml, p.capex_high, SIMS)
    success = rng.random(SIMS) < p.p_success
    years = np.arange(1, YEARS + 1)
    uptake = np.minimum(years[None, :] / t_peak[:, None], 1.0)
    decline = np.where(years[None, :] > 4, (1 - erosion[:, None]) ** (years[None, :] - 4), 1.0)
    sales = peak[:, None] * uptake * decline * success[:, None]
    ebitda = sales * (1 - p.cogs_pct - mkt[:, None])
    ebitda[:, 0] -= p.launch_cost * success
    fcf = ebitda * (1 - TAX)
    disc = (1 + WACC) ** -years
    npv = -capex + (fcf * disc).sum(axis=1)
    cum = np.cumsum(fcf, axis=1) - capex[:, None]
    payback = np.where((cum > 0).any(axis=1), (cum > 0).argmax(axis=1) + 1, YEARS + 1)
    return npv, payback, capex.mean() + p.launch_cost


def minmax(s, invert=False):
    r = (s - s.min()) / (s.max() - s.min())
    return 1 - r if invert else r


def main():
    projects = pd.read_csv(data_dir(__file__) / "projects.csv")
    res = []
    for _, p in projects.iterrows():
        npv, pb, inv = simulate(p)
        res.append({"project_id": p.project_id, "enpv": npv.mean(), "p10": np.percentile(npv, 10),
                    "p90": np.percentile(npv, 90), "p_loss": (npv < 0).mean(),
                    "payback_median": np.median(pb), "investment": inv})
    df = projects.merge(pd.DataFrame(res), on="project_id")
    df["enpv_per_inv"] = df.enpv / df.investment

    score = (WEIGHTS["enpv_per_inv"] * minmax(df.enpv_per_inv) + WEIGHTS["downside"] * minmax(df.p_loss, True)
             + WEIGHTS["payback"] * minmax(df.payback_median, True)
             + sum(WEIGHTS[c] * (df[c] - 1) / 4 for c in ["strategic_fit", "capability_fit", "competition_score"]))
    df["score"] = (100 * score).round(1)
    df["hard_rule"] = np.where(df.p_loss > 0.40, "REWORK/STOP (P(NPV<0) > 40%)", "")

    ranked = df.sort_values("score", ascending=False).copy()
    funded, spent = [], 0.0
    for _, r in ranked.iterrows():
        ok = not r.hard_rule and spent + r.investment <= CAPEX_BUDGET
        funded.append("FUND" if ok else ("STOP" if r.hard_rule else "DEFER"))
        spent += r.investment if ok else 0
    ranked["decision"] = funded

    cols = ["project_id", "therapy", "score", "enpv", "p10", "p90", "p_loss", "payback_median", "investment", "decision"]
    print(ranked[cols].round(2).to_string(index=False))
    print(f"\nCapex budget ₹{CAPEX_BUDGET} Cr | committed ₹{spent:.1f} Cr | "
          f"portfolio eNPV ₹{ranked[ranked.decision == 'FUND'].enpv.sum():.1f} Cr")

    # Old process: fund by headline (most-likely) peak sales, no risk adjustment, same budget
    old, spent_old = [], 0.0
    for _, r in df.sort_values("peak_sales_ml", ascending=False).iterrows():
        if spent_old + r.investment <= CAPEX_BUDGET:
            old.append(r.project_id)
            spent_old += r.investment
    new = set(ranked[ranked.decision == "FUND"].project_id)
    median_eff = df.enpv_per_inv.median()
    avoided = df[df.project_id.isin(set(old) - new) & (df.enpv_per_inv < median_eff)]
    print(f"\nOld process (rank by headline peak sales) would fund: {sorted(old)}")
    print(f"Low-return projects it funded that the new process does not: {avoided.project_id.tolist()}")
    print(f"Low-return spend avoided ≈ ₹{avoided.investment.sum():.1f} Cr | eNPV of old portfolio "
          f"₹{df[df.project_id.isin(old)].enpv.sum():.1f} Cr vs new ₹{ranked[ranked.decision == 'FUND'].enpv.sum():.1f} Cr")
    ranked.to_csv(output_dir(__file__) / "portfolio_ranking.csv", index=False)


if __name__ == "__main__":
    main()
