"""Incentive payout engine implementing business rules IP-1 … IP-9."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir, output_dir  # noqa: E402

TARGET_INCENTIVE_PCT = 0.20


def payout_pct(attainment: float) -> float:
    """IP-2/IP-3: share of target incentive earned for an attainment ratio."""
    if attainment < 0.80:
        return 0.0
    if attainment <= 1.00:
        return 0.50 + (attainment - 0.80) * 2.5          # 80%→50%, 100%→100%
    if attainment <= 1.20:
        return 1.00 + (attainment - 1.00) * 2.0          # accelerator: 120%→140%
    return 1.40                                           # cap


def split_credit(amount: float, splits: dict) -> dict:
    """IP-4: revenue credited by split %, which must sum to 100%."""
    if abs(sum(splits.values()) - 1.0) > 1e-9:
        raise ValueError("Split percentages must sum to 100%")
    return {rep: amount * pct for rep, pct in splits.items()}


def prorated_target(target: float, days_in_territory: int, days_in_period: int) -> float:
    """IP-5: mid-period transfer."""
    return target * days_in_territory / days_in_period


def net_credit(monthly_sales: list, monthly_returns: list) -> float:
    """IP-6: returns reverse credit; quarterly credit floored at zero."""
    return max(0.0, sum(monthly_sales) - sum(monthly_returns))


def quarterly_payout(base_salary: float, attainment: float, new_hire_first_q=False, resigned_before_qe=False) -> int:
    if resigned_before_qe:                       # IP-8
        return 0
    pct = 1.0 if new_hire_first_q else payout_pct(attainment)   # IP-7
    return round(base_salary * TARGET_INCENTIVE_PCT / 4 * pct)  # IP-1, IP-9 (annual base → quarter)


def main():
    reps = pd.read_csv(data_dir(__file__) / "reps.csv")
    reps["payout_pct"] = reps.apply(lambda r: 1.0 if r.new_hire_first_q else payout_pct(r.attainment), axis=1)
    reps["payout_inr"] = reps.apply(lambda r: quarterly_payout(r.base_salary_lakh * 1e5, r.attainment,
                                                               r.new_hire_first_q, r.resigned_before_qe), axis=1)
    print(reps[["rep_id", "attainment", "payout_pct", "new_hire_first_q", "resigned_before_qe", "payout_inr"]]
          .head(12).to_string(index=False))
    print(f"\nQuarterly payout total: ₹{reps.payout_inr.sum():,.0f} | reps at cap: {(reps.payout_pct == 1.4).sum()} | "
          f"below threshold: {(reps.payout_pct == 0).sum()}")
    reps.to_csv(output_dir(__file__) / "payout_statements.csv", index=False)


if __name__ == "__main__":
    main()
