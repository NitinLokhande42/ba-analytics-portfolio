"""Synthetic approval requests for one year."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir  # noqa: E402

rng = np.random.default_rng(17)
N = 6_000
df = pd.DataFrame({
    "request_id": [f"REQ{i:05d}" for i in range(N)],
    "category": rng.choice(["opex", "capex", "it_purchase", "contract"], N, p=[.6, .1, .2, .1]),
    "amount": np.round(rng.lognormal(11.3, 1.2, N), -2),
    "requester_is_manager": rng.random(N) < 0.08,
    "approver_on_leave": rng.random(N) < 0.10,
    "has_delegation": rng.random(N) < 0.6,
    "over_budget": rng.random(N) < 0.05,
})
df.to_csv(data_dir(__file__) / "requests.csv", index=False)
print(f"Wrote {N:,} requests; median amount ₹{df.amount.median():,.0f}")
