"""Synthetic candidate projects with triangular assumption ranges (₹ Cr)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir  # noqa: E402

rng = np.random.default_rng(8)
therapies = ["respiratory", "cardio", "diabetes", "oncology", "anti_infective", "dermatology"]
rows = []
for i in range(18):
    peak_ml = rng.uniform(8, 60)
    rows.append({
        "project_id": f"P{i + 1:02d}",
        "name": f"Project {chr(65 + i)}",
        "therapy": rng.choice(therapies),
        "type": rng.choice(["new_launch", "line_extension", "in_licensing"]),
        "peak_sales_low": round(peak_ml * rng.uniform(0.4, 0.7), 1),
        "peak_sales_ml": round(peak_ml, 1),
        "peak_sales_high": round(peak_ml * rng.uniform(1.2, 1.8), 1),
        "cogs_pct": round(rng.uniform(0.30, 0.55), 2),
        "capex_low": round(rng.uniform(3, 15), 1),
        "launch_cost": round(rng.uniform(2, 10), 1),
        "p_success": round(rng.uniform(0.55, 0.95), 2),
        "strategic_fit": int(rng.integers(1, 6)),
        "capability_fit": int(rng.integers(1, 6)),
        "competition_score": int(rng.integers(1, 6)),
    })
df = pd.DataFrame(rows)
df["capex_ml"] = (df.capex_low * rng.uniform(1.1, 1.3, len(df))).round(1)
df["capex_high"] = (df.capex_ml * rng.uniform(1.2, 1.6, len(df))).round(1)
df.to_csv(data_dir(__file__) / "projects.csv", index=False)
print(f"Wrote {len(df)} candidate projects")
