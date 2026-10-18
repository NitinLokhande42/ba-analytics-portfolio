"""Rebalance territory workload by moving unlocked accounts to adjacent territories (local search)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir, output_dir  # noqa: E402

VISITS = {"A": 24, "B": 12, "C": 4}
MINS = {"A": 60, "B": 45, "C": 30}
MAX_MOVE_SHARE = 0.20
ADJ_DIST = 30  # centroid distance defining "adjacent"


def workload(df):
    return df.tier.map(VISITS) * (df.tier.map(MINS) + df.travel_minutes) / 60 + 2


def imbalance(wl_by_terr):
    return (wl_by_terr / wl_by_terr.mean() - 1)


def main():
    acc = pd.read_csv(data_dir(__file__) / "accounts.csv")
    ter = pd.read_csv(data_dir(__file__) / "territories.csv").set_index("territory_id")
    acc["wl"] = workload(acc)
    acc["orig"] = acc.territory_id
    acc["locked"] = acc.groupby("territory_id").revenue_lakh.rank(ascending=False) <= 10  # TR-2
    cent = ter[["cx", "cy"]].values
    dist = np.linalg.norm(cent[:, None] - cent[None], axis=2)
    adj = {t: [u for u in ter.index if u != t and dist[t, u] < ADJ_DIST] for t in ter.index}
    max_moves = (acc.groupby("orig").size() * MAX_MOVE_SHARE).astype(int)

    before = imbalance(acc.groupby("territory_id").wl.sum())
    pairs = {(a, b) for a in adj for b in adj[a]}
    exhausted = set()
    for _ in range(20_000):  # safety cap
        wl = acc.groupby("territory_id").wl.sum()
        live = [(wl[a] - wl[b], a, b) for a, b in pairs if (a, b) not in exhausted and wl[a] > wl[b]]
        if not live:
            break
        gap, src, dst = max(live)
        if gap / wl.mean() < 0.05:          # good enough: remaining gaps under 5% of average
            break
        moved_out = ((acc.orig == src) & (acc.territory_id != src)).sum()
        cand = acc[(acc.territory_id == src) & (~acc.locked) & (acc.wl < gap)].copy()
        if moved_out >= max_moves[src]:      # TR-4: only accounts that came in from elsewhere may leave
            cand = cand[cand.orig != src]
        if cand.empty:
            exhausted.add((src, dst))
            continue
        cand["d"] = np.hypot(cand.x - ter.loc[dst, "cx"], cand.y - ter.loc[dst, "cy"])  # TR-3: nearest to neighbour
        acc.loc[cand.d.idxmin(), "territory_id"] = dst
        exhausted.clear() if len(exhausted) > 200 else None

    after = imbalance(acc.groupby("territory_id").wl.sum())
    moved = (acc.territory_id != acc.orig).mean()
    print(f"Territories: {len(ter)} | accounts: {len(acc):,} | accounts moved: {moved:.1%}")
    print(f"Workload imbalance before: {before.min():+.0%} to {before.max():+.0%}")
    print(f"Workload imbalance after:  {after.min():+.0%} to {after.max():+.0%}")
    print(f"Territories within ±15%: {(before.abs() <= .15).sum()} -> {(after.abs() <= .15).sum()} of {len(ter)}")
    acc.drop(columns=["wl"]).to_csv(output_dir(__file__) / "realigned_accounts.csv", index=False)


if __name__ == "__main__":
    main()
