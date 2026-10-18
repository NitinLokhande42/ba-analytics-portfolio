"""Generate 3 years of synthetic weekly marketing data (spend and revenue in ₹ lakh)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir  # noqa: E402

rng = np.random.default_rng(42)
WEEKS = 156
ANNUAL_BUDGET_LAKH = 5000  # ₹50 Cr
# share of budget, true adstock decay, half-saturation point, max weekly effect (lakh)
CHANNELS = {
    "tv":      dict(share=0.40, decay=0.6, half=1.0, beta=95.0),
    "digital": dict(share=0.25, decay=0.3, half=1.8, beta=115.0),
    "print":   dict(share=0.12, decay=0.2, half=0.6, beta=14.0),
    "radio":   dict(share=0.08, decay=0.3, half=0.9, beta=12.0),
    "field":   dict(share=0.15, decay=0.4, half=1.5, beta=60.0),
}


def adstock(x, decay):
    out = np.zeros_like(x)
    for t in range(len(x)):
        out[t] = x[t] + (decay * out[t - 1] if t else 0)
    return out


weeks = pd.date_range("2022-01-03", periods=WEEKS, freq="W-MON")
season = 1 + 0.15 * np.sin(2 * np.pi * np.arange(WEEKS) / 52 + 1.2)
df = pd.DataFrame({"week_start": weeks})
df["price_index"] = np.round(1 + rng.normal(0, 0.03, WEEKS), 3)
df["promo_flag"] = (rng.random(WEEKS) < 0.12).astype(int)
revenue = 120 * season + 0.08 * np.arange(WEEKS) - 60 * (df["price_index"] - 1) + 10 * df["promo_flag"]

for ch, p in CHANNELS.items():
    weekly_mean = ANNUAL_BUDGET_LAKH * p["share"] / 52
    flighting = rng.gamma(2.0, 0.5, WEEKS) * (rng.random(WEEKS) > 0.15) / 0.85
    spend = weekly_mean * flighting * season
    df[f"spend_{ch}"] = np.round(spend, 2)
    a = adstock(spend, p["decay"]) / (weekly_mean / (1 - p["decay"]))
    revenue += p["beta"] * a / (a + p["half"])

df["net_revenue"] = np.round(revenue + rng.normal(0, 10, WEEKS), 2)
out = data_dir(__file__) / "mmm_weekly.csv"
df.to_csv(out, index=False)
print(f"Wrote {len(df)} weeks to {out}")
