"""Score the assistant on the 100-question acceptance benchmark (execution accuracy)."""
import sqlite3
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT.parent))
from assistant import DB, NeedsClarification, answer  # noqa: E402
from guardrails import GuardrailError, enforce  # noqa: E402
from common.paths import output_dir  # noqa: E402


def norm(rows, ordered):
    r = [tuple(round(x, 2) if isinstance(x, float) else x for x in row) for row in rows]
    return r if ordered else sorted(r, key=str)


def main(use_llm=False):
    bench = pd.read_csv(ROOT / "benchmark" / "questions.csv")
    results = []
    with sqlite3.connect(DB) as con:
        for q in bench.itertuples():
            try:
                res = answer(q.question, use_llm=use_llm)
                if q.gold_sql == "REFUSE":
                    ok, note = False, "answered a should-refuse question"
                else:
                    gold = con.execute(enforce(q.gold_sql)).fetchall()
                    ok = norm(res["rows"], q.ordered) == norm(gold, q.ordered)
                    note = "" if ok else "result mismatch"
            except (GuardrailError, NeedsClarification) as e:
                ok, note = q.gold_sql == "REFUSE", str(e)
            results.append({"qid": q.qid, "category": q.category, "question": q.question, "correct": ok, "note": note})
    r = pd.DataFrame(results)
    print(f"Benchmark accuracy: {r.correct.mean():.0%} ({r.correct.sum()}/{len(r)})  [{'LLM' if use_llm else 'offline parser'}]")
    print(r.groupby("category").correct.agg(["mean", "sum", "count"]).rename(columns={"mean": "accuracy"}).round(2).to_string())
    print("\nSample failures (feed into synonym / semantic-layer backlog):")
    print(r[~r.correct].head(8)[["qid", "question", "note"]].to_string(index=False))
    r.to_csv(output_dir(__file__) / "benchmark_results.csv", index=False)

    # Security tests: guardrails must block these
    attacks = ["SELECT email FROM customers", "DELETE FROM sales", "SELECT * FROM sqlite_master",
               "SELECT 1; DROP TABLE sales"]
    blocked = sum(1 for a in attacks if _blocked(a))
    print(f"\nSecurity test cases blocked: {blocked}/{len(attacks)}")
    print("RLS example:", enforce("SELECT SUM(s.revenue) FROM sales s WHERE s.order_date >= '2026-01-01'",
                                  row_filter="s.region = 'West'"))


def _blocked(sql):
    try:
        enforce(sql)
        return False
    except GuardrailError:
        return True


if __name__ == "__main__":
    main(use_llm="--llm" in sys.argv)
