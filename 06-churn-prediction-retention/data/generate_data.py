"""Synthetic customer base (~20,000) with behavioural features and 90-day churn outcome."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir  # noqa: E402

rng = np.random.default_rng(31)
N = 20_000
df = pd.DataFrame({
    "customer_id": [f"C{i:05d}" for i in range(N)],
    "tenure_months": rng.integers(3, 96, N),
    "plan": rng.choice(["basic", "pro", "enterprise"], N, p=[.5, .35, .15]),
    "usage_trend": np.clip(rng.normal(0, 0.3, N), -1, 1.5).round(3),
    "sessions_30d": rng.poisson(40, N),
    "tickets_90d": rng.poisson(1.2, N),
    "csat_90d": np.clip(rng.normal(4.0, 0.8, N), 1, 5).round(1),
    "late_payments_6m": rng.poisson(0.3, N),
    "modules_adopted": rng.integers(1, 6, N),
})
df["annual_revenue"] = (df.plan.map({"basic": 3000, "pro": 7000, "enterprise": 16000})
                        * rng.lognormal(0, 0.25, N)).round(0)
logit = (-1.75 - 0.015 * df.tenure_months - 2.2 * df.usage_trend + 0.25 * df.tickets_90d
         - 0.5 * (df.csat_90d - 4) + 0.45 * df.late_payments_6m - 0.25 * (df.modules_adopted - 3)
         + 0.4 * (df.plan == "basic"))
df["churned_90d"] = (rng.random(N) < 1 / (1 + np.exp(-logit))).astype(int)
df.to_csv(data_dir(__file__) / "customers.csv", index=False)
print(f"Wrote {N:,} customers, 90-day churn {df.churned_90d.mean():.1%}, avg revenue ${df.annual_revenue.mean():,.0f}")
