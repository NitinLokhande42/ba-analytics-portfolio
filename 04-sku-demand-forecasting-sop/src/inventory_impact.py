"""
Link forecast accuracy to inventory and stockouts.

Both policies: monthly review, 1-month lead time, order up to (next month's forecast + safety stock).
Before: spreadsheet forecast, blanket safety stock of 15 days (45 days total cover) for every SKU.
After:  statistical forecast, safety stock = z × σ(out-of-sample forecast error) × √lead time.
Simulated month by month on the back-test months for every SKU.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import output_dir  # noqa: E402

LEAD_TIME_M = 1.0
SERVICE = 0.99
FIXED_COVER_M = 1.5  # 45 days


def simulate(bt, fcst_col, dynamic, sigma=None):
    """Periodic review, monthly: receive last month's order, serve demand, order up to target."""
    stock_val, short, demand, events, months = [], 0.0, 0.0, 0, 0
    for sku, g in bt.groupby("sku_id"):
        g = g.sort_values("month").reset_index(drop=True)
        err_sd = sigma[sku] if dynamic else 0.0
        on_hand, pipeline = g[fcst_col].iloc[0] * 1.5, g[fcst_col].iloc[0]
        for _, r in g.iterrows():
            on_hand += pipeline                      # order placed last month arrives (lead time = 1 month)
            sold = min(on_hand, r.actual)
            short += r.actual - sold
            events += int(sold < r.actual)
            months += 1
            demand += r.actual
            stock_val.append((on_hand - sold / 2) * r.unit_cost)  # average stock held during the month
            on_hand -= sold
            if dynamic:
                safety = norm.ppf(SERVICE) * err_sd * np.sqrt(LEAD_TIME_M)
            else:
                safety = r[fcst_col] * (FIXED_COVER_M - 1)  # blanket 45 days of cover = 1 month + 15 days buffer
            target = r[fcst_col] * LEAD_TIME_M + safety  # covers next month's demand + safety stock
            pipeline = max(0.0, target - on_hand)
    return np.mean(stock_val) * bt.sku_id.nunique(), short / demand, events / months



def main():
    full = pd.read_csv(output_dir(__file__) / "backtest.csv", parse_dates=["month"])
    # out-of-sample error σ: from the first back-test months (before the evaluation window)
    calib = full[full.best_of.isna()]
    sigma = calib.groupby("sku_id").apply(lambda g: np.std(g.actual - g.ensemble))
    bt = full.dropna(subset=["best_of"])
    inv0, so0, ev0 = simulate(bt, "spreadsheet", dynamic=False)
    inv1, so1, ev1 = simulate(bt, "best_of", dynamic=True, sigma=sigma)
    scale = 100 / inv0  # express as index where today's inventory = ₹100 Cr
    print(f"Inventory (indexed to ₹100 Cr today): spreadsheet + 45-day cover = ₹{inv0 * scale:.0f} Cr | "
          f"statistical + dynamic safety stock = ₹{inv1 * scale:.0f} Cr")
    print(f"Stockout events (SKU-months short): {ev0:.1%} -> {ev1:.1%}  ({ev1 / ev0 - 1:+.0%})")
    print(f"Units short / demand:               {so0:.2%} -> {so1:.2%}")


if __name__ == "__main__":
    main()
