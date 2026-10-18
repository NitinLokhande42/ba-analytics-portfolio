"""Synthetic randomised campaign: customer features, treatment flag and 14-day conversion with heterogeneous effects."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir  # noqa: E402

rng = np.random.default_rng(13)
N = 60_000
df = pd.DataFrame({
    "customer_id": np.arange(N),
    "recency_days": rng.gamma(2, 30, N).round(),
    "frequency_12m": rng.poisson(3, N),
    "monetary_12m": rng.gamma(2, 120, N).round(2),
    "email_engagement": rng.beta(2, 5, N).round(3),
    "discount_user": (rng.random(N) < 0.35).astype(int),
})
df["treatment"] = (rng.random(N) < 0.5).astype(int)
base = -2.9 - 0.008 * df.recency_days + 0.18 * df.frequency_12m + 1.5 * df.email_engagement
# heterogeneous treatment effect: discount users and lapsing-but-engaged customers respond; very frequent buyers don't
tau = (0.65 * df.discount_user + 1.2 * df.email_engagement * (df.recency_days > 45)
       - 0.12 * np.maximum(df.frequency_12m - 5, 0) - 0.02)
p = 1 / (1 + np.exp(-(base + df.treatment * tau)))
df["converted"] = (rng.random(N) < p).astype(int)
df.to_csv(data_dir(__file__) / "campaign.csv", index=False)
print(f"Wrote {N:,} customers | conversion treatment {df[df.treatment == 1].converted.mean():.2%} "
      f"vs holdout {df[df.treatment == 0].converted.mean():.2%}")
