# Requirements — GenAI Analytics Assistant

## Functional
| ID | Requirement | Priority |
|---|---|---|
| F-1 | Answer questions about governed metrics (revenue, units, orders, AOV, active customers) by governed dimensions | Must |
| F-2 | Show the answer, the result table, the SQL and the metric definition used | Must |
| F-3 | Understand business synonyms defined in the semantic layer (e.g. "sales" = revenue) | Must |
| F-4 | Resolve relative dates ("last quarter", "YTD") using the fiscal calendar | Must |
| F-5 | Ask a clarifying question or refuse when the question is ambiguous or out of scope | Must |
| F-6 | Thumbs up/down feedback stored with question, SQL and result | Should |
| F-7 | Suggested follow-up questions | Could |

## Semantic layer
- Every metric has: name, business definition, SQL expression, owner, allowed dimensions, synonyms.
- Joins are pre-defined; the LLM may not invent joins.
- Default time grain month; default period = last 12 months if none given (and stated in the answer).

## Security
| ID | Requirement |
|---|---|
| S-1 | Queries run under the user's Snowflake role; row-access policies apply (region managers see own region) |
| S-2 | PII columns (email, phone, name) are never selectable; masked at Snowflake level as defence-in-depth |
| S-3 | Service account is read-only; no DDL/DML grants |
| S-4 | Prompts and results logged for 90 days for audit; no customer data sent to model provider for training |

## Guardrails
| ID | Rule | Behaviour on breach |
|---|---|---|
| G-1 | SQL must be a single SELECT statement | Block |
| G-2 | Only allow-listed tables/views | Block |
| G-3 | No PII columns | Block, explain |
| G-4 | Add `LIMIT 1000` if missing | Auto-fix |
| G-5 | Inject user's row-level predicate | Auto-fix |
| G-6 | Confidence below threshold or no metric matched | Clarify / refuse |
| G-7 | Prompt-injection text in question ("ignore previous instructions") | Refuse |

## Acceptance
- ≥ 80% execution accuracy on the 100-question benchmark; 100% of security test cases blocked.
- No question in the "should refuse" category answered with data.
