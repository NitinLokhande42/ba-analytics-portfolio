"""Payout test pack (TC-01 … TC-13). Runs with pytest or directly with python."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from incentive_engine import net_credit, payout_pct, prorated_target, quarterly_payout, split_credit  # noqa: E402


def close(a, b, tol=1e-6):
    return abs(a - b) < tol


def test_threshold():
    assert payout_pct(0.799) == 0.0                      # TC-01
    assert close(payout_pct(0.80), 0.50)                 # TC-02


def test_curve():
    assert close(payout_pct(0.90), 0.75)                 # TC-03
    assert close(payout_pct(1.00), 1.00)                 # TC-04
    assert close(payout_pct(1.10), 1.20)                 # TC-05
    assert close(payout_pct(1.20), 1.40)                 # TC-06
    assert close(payout_pct(1.50), 1.40)                 # TC-07 cap


def test_split():
    c = split_credit(1_000_000, {"A": 0.6, "B": 0.4})    # TC-08
    assert close(c["A"], 600_000) and close(c["B"], 400_000)
    try:                                                  # TC-09
        split_credit(1_000_000, {"A": 0.6, "B": 0.5})
        raise AssertionError("invalid split accepted")
    except ValueError:
        pass


def test_transfer_and_returns():
    assert close(prorated_target(3_000_000, 45, 90), 1_500_000)  # TC-10
    assert close(net_credit([500_000, 0, 0], [0, 200_000, 0]), 300_000)  # TC-11


def test_new_hire_and_leaver():
    assert quarterly_payout(1_200_000, 0.60, new_hire_first_q=True) == 60_000   # TC-12: 12L × 20% / 4
    assert quarterly_payout(1_200_000, 1.10, resigned_before_qe=True) == 0     # TC-13


if __name__ == "__main__":
    tests = [v for k, v in dict(globals()).items() if k.startswith("test_")]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"{len(tests)} test groups passed (13 test cases)")
