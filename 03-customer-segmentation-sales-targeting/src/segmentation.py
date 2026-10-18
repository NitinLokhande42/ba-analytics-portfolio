"""Apply segmentation rules, cross-check with k-means, and build a capacity-constrained call plan."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir, output_dir  # noqa: E402

CALLS = {"GROW": 4, "DEFEND": 3, "DEVELOP": 2, "MAINTAIN": 1, "DEPRIORITISE": 0}
ORDER = ["GROW", "DEFEND", "DEVELOP", "MAINTAIN", "DEPRIORITISE"]


def segment(row):
    p, s = row.potential_pct, row.cipla_share
    if p >= 0.8 and s < 0.30:
        return "GROW"
    if p >= 0.5 and s >= 0.30:
        return "DEFEND"
    if p >= 0.5 and s < 0.10:
        return "DEVELOP"
    if p >= 0.5 or s >= 0.30:
        return "MAINTAIN"
    return "DEPRIORITISE"


def build_call_plan(terr):
    terr = terr.copy()
    terr["seg_rank"] = terr.segment.map({s: i for i, s in enumerate(ORDER)})
    terr = terr.sort_values(["seg_rank", "monthly_rx_potential"], ascending=[True, False])
    cap, planned = terr.current_calls_month.sum(), []  # same capacity as today: no added headcount
    for c in terr.segment.map(CALLS):
        give = min(c, cap)
        planned.append(give)
        cap -= give
    terr["planned_calls"] = planned
    # leftover capacity: MAINTAIN doctors already got 1 call; give spare calls to DEVELOP (+1) in potential order
    spare = cap
    for i in terr.index[terr.segment == "DEVELOP"]:
        if spare <= 0:
            break
        terr.loc[i, "planned_calls"] += 1
        spare -= 1
    return terr


def main():
    df = pd.read_csv(data_dir(__file__) / "doctors.csv")
    df["potential_pct"] = df.groupby("territory_id")["monthly_rx_potential"].rank(pct=True)
    df["segment"] = df.apply(segment, axis=1)

    # validation: do natural clusters line up with the rule-based segments?
    X = StandardScaler().fit_transform(np.c_[np.log1p(df.monthly_rx_potential), df.cipla_share])
    df["cluster"] = KMeans(n_clusters=4, n_init=10, random_state=0).fit_predict(X)
    print("Rule segments vs k-means clusters (row %)")
    print((pd.crosstab(df.segment, df.cluster, normalize="index") * 100).round(0).to_string())

    plan = pd.concat([build_call_plan(g) for _, g in df.groupby("territory_id")])
    summary = plan.groupby("segment").agg(doctors=("doctor_id", "size"),
                                          rx_potential=("monthly_rx_potential", "sum"),
                                          calls_before=("current_calls_month", "sum"),
                                          calls_after=("planned_calls", "sum")).loc[ORDER]
    summary["potential_share"] = (summary.rx_potential / summary.rx_potential.sum()).round(3)
    summary["calls_share_before"] = (summary.calls_before / summary.calls_before.sum()).round(3)
    summary["calls_share_after"] = (summary.calls_after / summary.calls_after.sum()).round(3)
    print("\nCall allocation before vs after (same total capacity)")
    print(summary.to_string())
    pri = ["GROW", "DEFEND"]
    print(f"\nShare of calls on priority segments: {summary.loc[pri, 'calls_share_before'].sum():.0%} -> "
          f"{summary.loc[pri, 'calls_share_after'].sum():.0%}")
    print(f"Total calls: {summary.calls_before.sum():,} before vs {summary.calls_after.sum():,} after (no new reps)")
    plan.drop(columns=["seg_rank"]).to_csv(output_dir(__file__) / "call_plan.csv", index=False)


if __name__ == "__main__":
    main()
