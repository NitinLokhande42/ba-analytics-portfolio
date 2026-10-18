"""Monte Carlo of cycle time and effort per request: as-is (email/paper) vs to-be (Power Platform)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir  # noqa: E402

rng = np.random.default_rng(2)
HOURS_PER_DAY = 24  # waits are elapsed (calendar) hours


def as_is(req):
    waits = [4, 18, 20, 16, 22, 18] + ([30] if req.amount > 500_000 or req.category == "capex" else []) + [14, 8]
    hours = sum(rng.gamma(2, w * 0.65) for w in waits)
    if rng.random() < 0.22:  # returned for missing info → restart part of the chain
        hours += rng.gamma(2, 12)
    effort_min = 9 * 3.2 + (15 if rng.random() < 0.22 else 0)  # 9 touches × ~3 min (open, check, forward, file)
    return hours, effort_min


def to_be(req, steps):
    hours = rng.gamma(2, 1)  # submit + validation
    for _ in range(steps):
        w = rng.gamma(2, 8.5)
        w = min(w, 24 + rng.gamma(2, 1)) if w > 24 else w  # 24h reminder
        w = min(w, 48) if not req.approver_on_leave else w + (0 if req.has_delegation else 4)
        hours += w
    effort_min = 2 * 2 + (5 if rng.random() < 0.03 else 0)  # submit + approve
    return hours, effort_min


def main():
    df = pd.read_csv(data_dir(__file__) / "requests.csv")
    from routing_engine import route  # noqa: E402
    steps = df.apply(lambda r: len(route(r)[1]), axis=1)
    a = np.array([as_is(r) for r in df.itertuples()])
    b = np.array([to_be(r, s) for r, s in zip(df.itertuples(), steps)])
    days_a, days_b = a[:, 0] / HOURS_PER_DAY, b[:, 0] / HOURS_PER_DAY
    print(f"Requests simulated: {len(df):,}")
    print(f"Cycle time (days) as-is: mean {days_a.mean():.1f}, p90 {np.percentile(days_a, 90):.1f}")
    print(f"Cycle time (days) to-be: mean {days_b.mean():.1f}, p90 {np.percentile(days_b, 90):.1f}")
    print("Manual touches: 9 -> 2")
    saved = (a[:, 1].sum() - b[:, 1].sum()) / 60
    print(f"Effort saved per year: {saved:,.0f} hours")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
