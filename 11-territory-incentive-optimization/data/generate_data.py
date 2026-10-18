"""Synthetic accounts across 30 territories with deliberately uneven workload."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir  # noqa: E402

rng = np.random.default_rng(27)
T = 30
cent = rng.uniform(0, 100, (T, 2))
size = rng.uniform(0.62, 1.45, T)  # historical sprawl -> uneven account counts
rows = []
aid = 0
for t in range(T):
    n = int(70 * size[t])
    for _ in range(n):
        x, y = cent[t] + rng.normal(0, 6, 2)
        tier = rng.choice(["A", "B", "C"], p=[.12, .33, .55])
        rows.append({"account_id": f"AC{aid:05d}", "territory_id": t, "x": round(x, 2), "y": round(y, 2), "tier": tier,
                     "revenue_lakh": round(rng.lognormal({"A": 3.5, "B": 2.6, "C": 1.6}[tier], 0.4), 2),
                     "travel_minutes": int(rng.integers(15, 60))})
        aid += 1
pd.DataFrame(rows).to_csv(data_dir(__file__) / "accounts.csv", index=False)
pd.DataFrame({"territory_id": range(T), "cx": cent[:, 0].round(2), "cy": cent[:, 1].round(2)}).to_csv(
    data_dir(__file__) / "territories.csv", index=False)

reps = pd.DataFrame({"rep_id": [f"R{t:02d}" for t in range(T)], "territory_id": range(T),
                     "base_salary_lakh": rng.uniform(8, 14, T).round(2),
                     "attainment": np.clip(rng.normal(1.0, 0.18, T), 0.5, 1.6).round(3),
                     "new_hire_first_q": rng.random(T) < 0.07, "resigned_before_qe": rng.random(T) < 0.03})
reps.to_csv(data_dir(__file__) / "reps.csv", index=False)
print(f"Wrote {len(rows):,} accounts across {T} territories")
