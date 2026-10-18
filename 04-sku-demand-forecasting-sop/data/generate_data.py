"""Synthetic monthly SKU demand: trend, seasonality (monsoon respiratory peak), promotions and noise."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir  # noqa: E402

rng = np.random.default_rng(21)
N_SKU, MONTHS = 150, 48
months = pd.date_range("2021-01-01", periods=MONTHS, freq="MS")
rows = []
for k in range(N_SKU):
    therapy = rng.choice(["respiratory", "cardio", "anti_infective", "diabetes"])
    level = rng.lognormal(7, 1.0)
    trend = rng.normal(0.006, 0.008)
    amp = {"respiratory": 0.30, "anti_infective": 0.25, "cardio": 0.05, "diabetes": 0.05}[therapy] * rng.uniform(.6, 1.4)
    phase = 7 if therapy in ("respiratory", "anti_infective") else rng.integers(0, 12)
    noise = rng.uniform(0.06, 0.30)
    price = rng.uniform(40, 400)
    promo = rng.random(MONTHS) < 0.08
    t = np.arange(MONTHS)
    demand = level * (1 + trend) ** t * (1 + amp * np.cos(2 * np.pi * (t % 12 - phase) / 12))
    demand *= np.where(promo, 1.25, 1.0) * rng.lognormal(0, noise, MONTHS)
    for i in range(MONTHS):
        rows.append({"month_start": months[i], "sku_id": f"SKU{k:04d}", "therapy": therapy,
                     "qty": round(demand[i]), "unit_cost_inr": round(price, 2), "promo_flag": int(promo[i])})
df = pd.DataFrame(rows)
df.to_csv(data_dir(__file__) / "sku_monthly.csv", index=False)
print(f"Wrote {len(df):,} SKU-months for {N_SKU} SKUs")
