# 09 · GenAI Analytics Assistant

**Company:** Neutrino · **Stack:** LLM, RAG, NL-to-SQL, Snowflake · **Role:** Business Analyst

## Business problem
The analytics team was flooded with ad-hoc questions ("what were West region sales last quarter?") that took hours to
queue, answer and check. Business users wanted to ask questions in plain English and get trustworthy answers — but
leadership would only approve a GenAI tool if it was **accurate, secure and governed**.

## My BA role
- **Collected 100 real user questions** from tickets, emails and Teams threads and turned them into **acceptance tests** with expected answers (gold SQL + result).
- Defined the **semantic layer** requirements: governed metrics, dimensions, synonyms, joins and default time logic, so the LLM never guesses business definitions.
- Wrote **security requirements**: user-level row access inherited from Snowflake roles, PII masking, read-only service account.
- Wrote **guardrail requirements**: SELECT-only, table allow-list, row limits, refusal for out-of-scope or ambiguous questions, citation of the metric definition used.

## Architecture
```
User question ─► Retrieval (RAG over semantic layer + KPI docs + example Q→SQL pairs)
             ─► LLM generates SQL against semantic layer
             ─► Guardrails (parse, SELECT-only, allow-list, PII, LIMIT, RLS predicate injection)
             ─► Snowflake (user's role) ─► Answer + table + "metric definition used" + SQL shown
```

## Impact
| Metric | Result |
|---|---|
| Benchmark accuracy (100 acceptance questions) | **85%** |
| Ad-hoc requests to analytics team | **−40% (~1,800 hours / year)** |

## What the code reproduces (synthetic data)
- Offline semantic-layer parser scores 84/100 on the benchmark; all 10 should-refuse questions refused
- All guardrail security tests blocked; RLS predicate injection demonstrated
- Failures are unseen synonyms (e.g. 'takings', 'basket size') — exactly the backlog that feeds semantic-layer updates

> Synthetic data is calibrated to the shape of the real problem; exact figures will differ slightly from the engagement results above.

## Run it (no API key needed)
```bash
python data/generate_data.py           # builds a SQLite "warehouse" + the 100-question benchmark with gold SQL
python src/evaluate.py                 # runs the assistant on the benchmark, scores execution accuracy
python src/assistant.py "top 3 regions by revenue in 2025"
```
By default the assistant uses an offline **semantic-layer parser** so the repo runs anywhere. Set `ANTHROPIC_API_KEY`
and pass `--llm` to `evaluate.py` / `assistant.py` to generate SQL with an LLM instead; both paths go through the same guardrails.

## Contents
| Path | What it is |
|---|---|
| `docs/requirements.md` | Functional, security and guardrail requirements |
| `docs/acceptance_testing.md` | How the 100 questions were collected, labelled and scored |
| `semantic_layer/semantic_layer.json` | Governed metrics, dimensions, synonyms, joins |
| `benchmark/` | Generated benchmark (`questions.csv`) |
| `src/guardrails.py` | SQL safety checks and RLS injection |
| `src/assistant.py` | Retrieval + NL-to-SQL (offline parser or LLM) |
| `src/evaluate.py` | Execution-accuracy scoring by question category |
