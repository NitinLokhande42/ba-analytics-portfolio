"""Synthetic doctors (with audit potential/share) and monthly territory sales for 4 regions."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir  # noqa: E402

rng = np.random.default_rng(5)
N = 12_000
doctors = pd.DataFrame({
    "doctor_id": [f"D{i:05d}" for i in range(N)],
    "territory_id": rng.integers(0, 60, N),
    "specialty": rng.choice(["CP", "CARDIO", "PULMO", "DIABETO", "GP"], N, p=[.3, .12, .1, .13, .35]),
    "monthly_rx_potential": np.round(rng.lognormal(3.2, 0.8, N)),
    "cipla_share": np.clip(rng.beta(2, 6, N), 0, 1).round(3),
    "current_calls_month": rng.choice([0, 1, 2, 3, 4], N, p=[.2, .3, .25, .15, .1]),
})
doctors["region"] = np.where(doctors.territory_id < 15, "R1_pilot", np.where(doctors.territory_id < 30, "R2_pilot",
                    np.where(doctors.territory_id < 45, "R3_control", "R4_control")))
doctors.to_csv(data_dir(__file__) / "doctors.csv", index=False)

# Monthly priority-segment sales per territory: 3 baseline months + 6 pilot months
rows = []
base = rng.normal(1.6, 0.25, 60)  # ₹ Cr per year in priority segments per territory -> monthly below
for t in range(60):
    pilot = t < 30
    for m in range(-3, 6):
        season = 1 + 0.04 * np.sin(m / 2)
        trend = 1 + 0.004 * (m + 3)
        uplift = 1.085 if (pilot and m >= 0) else 1.0
        ramp = min(1, (m + 1) / 2) if (pilot and m >= 0) else 1  # effect ramps in over 2 months
        eff = 1 + (uplift - 1) * ramp
        sales = base[t] / 12 * season * trend * eff * rng.normal(1, 0.03)
        rows.append({"territory_id": t, "pilot": int(pilot), "month": m, "post": int(m >= 0),
                     "priority_sales_cr": round(sales, 4)})
pd.DataFrame(rows).to_csv(data_dir(__file__) / "territory_sales.csv", index=False)
print(f"Wrote {N:,} doctors and {len(rows)} territory-months")
