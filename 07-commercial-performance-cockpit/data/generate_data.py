"""Synthetic legacy report inventory and parallel-run figures (legacy vs cockpit)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir  # noqa: E402

rng = np.random.default_rng(4)
areas = ["revenue", "target", "margin", "pipeline", "customer", "product", "forecast"]
pages = {"revenue": "Executive summary", "target": "Sales vs target", "margin": "Margin bridge",
         "pipeline": "Pipeline health", "customer": "Customer drill-down", "product": "Product performance",
         "forecast": None}
rows = []
for i in range(62):
    area = rng.choice(areas, p=[.22, .18, .14, .12, .14, .12, .08])
    freq = rng.choice(["daily", "weekly", "monthly"], p=[.15, .40, .45])
    runs = {"daily": 250, "weekly": 52, "monthly": 12}[freq]
    rows.append({"report_id": f"RPT{i + 1:03d}", "area": area, "owner_team": rng.choice(["sales_ops", "finance", "regional", "IT"]),
                 "frequency": freq, "hours_per_run": round(rng.uniform(0.5, 6) if freq != "daily" else rng.uniform(0.3, 1.2), 1),
                 "runs_per_year": runs, "users": int(rng.integers(1, 40)),
                 "cockpit_page": pages[area] if rng.random() > 0.3 else None})
pd.DataFrame(rows).to_csv(data_dir(__file__) / "report_inventory.csv", index=False)

regions = ["North", "South", "East", "West"]
pr = []
for m in pd.date_range("2025-04-01", periods=2, freq="MS"):
    for d in pd.date_range(m, periods=20, freq="B"):
        for r in regions:
            cockpit = rng.uniform(2, 5) * 1e7
            diff = rng.normal(0, 0.001)
            if r == "East" and d.month == 4 and d.day < 15:
                diff += 0.021  # legacy includes intercompany sales until fixed
            if r == "West" and d.day in (1, 2):
                diff -= 0.012  # credit-note timing
            pr.append({"date": d.date(), "region": r, "cockpit_nr": round(cockpit), "legacy_nr": round(cockpit * (1 + diff))})
pd.DataFrame(pr).to_csv(data_dir(__file__) / "parallel_run.csv", index=False)
print(f"Wrote {len(rows)} legacy reports and {len(pr)} parallel-run checks")
