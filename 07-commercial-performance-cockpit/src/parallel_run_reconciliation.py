"""Reconcile cockpit vs legacy figures during the parallel run and apply the retirement rule."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir, output_dir  # noqa: E402

TOL = 0.005
CONSECUTIVE = 3


def main():
    pr = pd.read_csv(data_dir(__file__) / "parallel_run.csv", parse_dates=["date"])
    pr["diff_pct"] = (pr.cockpit_nr - pr.legacy_nr) / pr.legacy_nr
    pr["status"] = (pr.diff_pct.abs() <= TOL).map({True: "MATCH", False: "INVESTIGATE"})
    print(f"Checks: {len(pr)} | match rate {(pr.status == 'MATCH').mean():.1%}")
    print("\nExceptions by region")
    print(pr[pr.status != "MATCH"].groupby("region").agg(checks=("date", "size"), avg_diff=("diff_pct", "mean"),
                                                         first=("date", "min"), last=("date", "max")).to_string())
    print("\nRetirement readiness (last 3 checks matched per region)")
    for r, g in pr.sort_values("date").groupby("region"):
        ready = (g.status.tail(CONSECUTIVE) == "MATCH").all()
        print(f"  {r:<6} {'READY' if ready else 'NOT READY'}")
    pr.to_csv(output_dir(__file__) / "reconciliation.csv", index=False)


if __name__ == "__main__":
    main()
