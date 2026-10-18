"""Executable version of the routing & escalation rules (mirrors the Power Automate flow)."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir, output_dir  # noqa: E402

MATRIX = [  # rule, category (None = any), min, max, approvers
    ("R4", "capex", 0, float("inf"), ["line_manager", "budget_owner", "cfo"]),
    ("R6", "contract", 0, float("inf"), ["line_manager", "legal", "budget_owner"]),
    ("R5", "it_purchase", 50_001, float("inf"), ["line_manager", ("budget_owner", "it_head")]),
    ("R1", None, 0, 50_000, ["line_manager"]),
    ("R2", "opex", 50_001, 500_000, ["line_manager", "budget_owner"]),
    ("R3", "opex", 500_001, float("inf"), ["line_manager", "budget_owner", "cfo"]),
]


def route(req):
    for rule, cat, lo, hi, approvers in MATRIX:
        if (cat is None or cat == req.category) and lo <= req.amount <= hi:
            chain = list(approvers)
            break
    else:
        raise ValueError(f"No rule for {req.request_id}")
    if req.over_budget and "cfo" not in chain:
        chain.append("cfo")
    if req.requester_is_manager:
        chain = ["managers_manager" if a == "line_manager" else a for a in chain]
    notes = []
    if req.approver_on_leave:
        notes.append("delegate" if req.has_delegation else "escalate_to_manager_after_4h")
    return rule, chain, notes


def main():
    df = pd.read_csv(data_dir(__file__) / "requests.csv")
    out = df.apply(lambda r: pd.Series(route(r), index=["rule", "chain", "notes"]), axis=1)
    df = pd.concat([df, out], axis=1)
    df["steps"] = df.chain.apply(len)
    print("Requests by rule:", df.rule.value_counts().sort_index().to_dict())
    print(f"Average approval steps (to-be): {df.steps.mean():.2f} (as-is up to 7)")
    print("\nSample routing decisions")
    print(df[["request_id", "category", "amount", "over_budget", "rule", "chain", "notes"]].head(8).to_string(index=False))
    df.to_csv(output_dir(__file__) / "routing_decisions.csv", index=False)


if __name__ == "__main__":
    main()
