# Acceptance Testing with 100 Real User Questions

## Collection
1. Pulled 6 months of ad-hoc request tickets, emails and Teams messages to the analytics team (~1,400 items).
2. De-duplicated and clustered by intent; picked **100 representative questions** keeping users' own wording.
3. Category mix: simple totals, breakdowns, top-N, filtered, time comparisons, and questions that **should be refused** (PII, out of scope, write operations).

## Labelling
- For each question an analyst wrote the **gold SQL**; a second analyst reviewed it.
- Expected result stored as a snapshot so tests are deterministic.

## Scoring
- **Execution accuracy:** assistant's result set equals gold result set (order-insensitive unless the question asks for a ranking; numeric tolerance 0.01%).
- Refusal questions pass only if the assistant refuses.
- Reported overall and by category; failures reviewed weekly → fixes go into synonyms, examples or the semantic layer, never into hard-coded answers.

## Results (production rollout)
| Category | Accuracy |
|---|---|
| Overall | **85%** |
| Security/refusal cases | 100% blocked |

This repository reproduces the method with a synthetic warehouse and generated benchmark (`data/generate_data.py`).
