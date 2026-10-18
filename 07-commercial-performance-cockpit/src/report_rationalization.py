"""Decide which legacy reports the cockpit replaces and estimate analyst hours saved."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir, output_dir  # noqa: E402

RESIDUAL_EFFORT = 0.10  # retired reports still need ~10% effort (checks, commentary)


def main():
    inv = pd.read_csv(data_dir(__file__) / "report_inventory.csv")
    inv["annual_hours"] = inv.hours_per_run * inv.runs_per_year
    inv["decision"] = inv.cockpit_page.notna().map({True: "RETIRE", False: "KEEP / REVIEW"})
    retire = inv[inv.decision == "RETIRE"]
    saved = retire.annual_hours.sum() * (1 - RESIDUAL_EFFORT)
    print(f"Legacy reports inventoried: {len(inv)}")
    print(f"Retire (covered by a cockpit page): {len(retire)} | keep/review: {len(inv) - len(retire)}")
    print("\nRetired reports by cockpit page")
    print(retire.groupby("cockpit_page").agg(reports=("report_id", "size"), annual_hours=("annual_hours", "sum"))
          .sort_values("annual_hours", ascending=False).round(0).to_string())
    print(f"\nAnalyst hours saved per year ≈ {saved:,.0f}")
    inv.to_csv(output_dir(__file__) / "report_decisions.csv", index=False)


if __name__ == "__main__":
    main()
