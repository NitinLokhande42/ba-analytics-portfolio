"""
NL-to-SQL assistant.

Retrieval step: pull matching metric/dimension definitions from the semantic layer (the "RAG context").
Generation step: either
  * offline parser — deterministic mapping using semantic-layer synonyms (default, no API needed), or
  * LLM — prompt with retrieved context + few-shot examples (set ANTHROPIC_API_KEY and use --llm).
Every SQL goes through guardrails before execution.
"""
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from guardrails import GuardrailError, check_question, enforce  # noqa: E402

SL = json.loads((ROOT / "semantic_layer" / "semantic_layer.json").read_text())
DB = ROOT / "data" / "warehouse.db"
TIME_PHRASES = {
    "last quarter": "s.order_date BETWEEN '2026-04-01' AND '2026-06-30'",
    "this year": "s.order_date BETWEEN '2026-01-01' AND '2026-07-15'",
    "in march 2026": "s.order_date BETWEEN '2026-03-01' AND '2026-03-31'",
    "in 2025": "s.order_date BETWEEN '2025-01-01' AND '2025-12-31'",
    "in 2024": "s.order_date BETWEEN '2024-01-01' AND '2024-12-31'",
}


class NeedsClarification(Exception):
    pass


def retrieve(question):
    """Return the semantic-layer entries mentioned in the question (longest synonym wins)."""
    q = question.lower()
    def find(items):
        hits = []
        for key, spec in items.items():
            for syn in spec.get("synonyms", []):
                m = re.search(rf"\b{re.escape(syn.lower())}\b", q)
                if m:
                    hits.append((m.start(), -len(syn), key))
        return [k for _, _, k in sorted(hits)]
    metrics = find(SL["metrics"])
    dims = find({k: v for k, v in SL["dimensions"].items()})
    values = [(d, v) for d, spec in SL["dimensions"].items() for v in spec.get("values", [])
              if re.search(rf"\b{re.escape(v.lower())}\b", q)]
    return metrics, dims, values


def offline_sql(question):
    q = question.lower()
    metrics, dims, values = retrieve(question)
    if not metrics:
        raise NeedsClarification("I couldn't match a governed metric. Did you mean revenue, units, orders, AOV or active customers?")
    metric = metrics[0]
    time = next((v for k, v in TIME_PHRASES.items() if k in q), None)
    if time is None:
        raise NeedsClarification("Which period? (e.g. 'in 2025', 'last quarter')")
    group_by = [d for d in dims if d not in {v[0] for v in values}]
    by = re.search(r"\b(by|split|break down|top|which|per)\b", q)
    dim = group_by[0] if group_by and by else None
    top = re.search(r"\b(?:top|which)\s+(\d+)", q)
    needs_join = "segment" in ([dim] + [v[0] for v in values])
    join = " " + SL["joins"]["customers"] if needs_join else ""
    where = [time] + [f"{SL['dimensions'][d]['sql']} = '{v}'" for d, v in values]
    dim_sql = SL["dimensions"][dim]["sql"] if dim else None
    sel = (f"{dim_sql} AS {dim}, " if dim else "") + f"{SL['metrics'][metric]['sql']} AS value"
    sql = f"SELECT {sel} FROM sales s{join} WHERE {' AND '.join(where)}"
    if dim:
        sql += f" GROUP BY {dim_sql}"
        if top:
            sql += f" ORDER BY value DESC LIMIT {top.group(1)}"
    return sql, metric


def llm_sql(question):
    """Generate SQL with an LLM using retrieved semantic-layer context (requires ANTHROPIC_API_KEY)."""
    import urllib.request
    metrics, dims, _ = retrieve(question)
    context = {"metrics": {k: SL["metrics"][k] for k in (metrics or SL["metrics"])},
               "dimensions": SL["dimensions"], "joins": SL["joins"], "time": SL["time"]}
    prompt = (f"You write SQLite SQL for a sales warehouse. Use ONLY these governed definitions:\n{json.dumps(context)}\n"
              "Table alias s for sales, c for customers. Output the metric as `value`. "
              "If the question cannot be answered with these definitions reply exactly REFUSE.\n"
              f"Question: {question}\nSQL:")
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", method="POST", data=json.dumps({
        "model": os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6"), "max_tokens": 400,
        "messages": [{"role": "user", "content": prompt}]}).encode(),
        headers={"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01",
                 "content-type": "application/json"})
    text = json.loads(urllib.request.urlopen(req).read())["content"][0]["text"].strip()
    text = re.sub(r"^```(sql)?|```$", "", text, flags=re.M).strip()
    if text.upper().startswith("REFUSE"):
        raise NeedsClarification("Out of scope for governed data.")
    return text, metrics[0] if metrics else None


def answer(question, use_llm=False, row_filter=None):
    check_question(question)
    sql, metric = llm_sql(question) if use_llm else offline_sql(question)
    safe = enforce(sql, row_filter=row_filter)
    with sqlite3.connect(DB) as con:
        rows = con.execute(safe).fetchall()
    return {"sql": safe, "rows": rows, "metric_definition": SL["metrics"].get(metric, {}).get("definition")}


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--llm"]
    question = " ".join(args) or "Top 3 regions by revenue in 2025"
    try:
        res = answer(question, use_llm="--llm" in sys.argv)
        print("SQL:", res["sql"])
        print("Definition used:", res["metric_definition"])
        for r in res["rows"]:
            print("  ", r)
    except (GuardrailError, NeedsClarification) as e:
        print("Assistant:", e)
