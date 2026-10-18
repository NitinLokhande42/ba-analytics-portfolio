# 07 · Commercial Performance Cockpit

**Company:** Genpact · **Stack:** Snowflake, Power BI (row-level security), JIRA · **Role:** Business Analyst

## Business problem
Sales, finance and regional leadership relied on **60+ Excel and legacy reports** built by different teams, each with
its own definitions of revenue, margin and pipeline. Month-end numbers took **3 days** to assemble, meetings started
with "whose number is right?", and analysts spent thousands of hours a year copying data between files.

## My BA role
- Ran **15 stakeholder interviews** (CCO, regional heads, finance controllers, sales ops, key account managers).
- Wrote the **BRD**, a single **KPI dictionary** with agreed owners, and **user stories across 3 releases** in JIRA.
- Ran a **report rationalisation**: inventoried every existing report, mapped them to cockpit pages, and agreed retirement dates.
- Led **UAT** and a **two-month parallel run**, reconciling cockpit numbers against legacy reports until sign-off.

## Solution
- **Snowflake** star schema: sales, orders, pipeline and targets facts; customer, product, geography, date and employee dimensions.
- **Power BI** cockpit: executive summary, sales vs. target, margin bridge, pipeline health, customer drill-down.
- **Row-level security**: users see only their region/territory; leadership sees all; finance sees margin.
- Daily refresh by 07:00 → **same-day reporting**.

## Releases
| Release | Scope | Weeks |
|---|---|---|
| R1 | Revenue & target tracking, executive summary, RLS | 8 |
| R2 | Margin bridge, product & customer profitability | 6 |
| R3 | Pipeline health, forecast vs. actual, KAM account view | 6 |

## Impact
| Metric | Before | After |
|---|---|---|
| Reports | 60+ legacy | **40+ retired** |
| Reporting cycle | 3 days | **Same day** |
| Analyst effort | — | **~4,500 hours / year saved** |

## What the code reproduces (synthetic data)
- 44 of 62 legacy reports mapped to cockpit pages → retire; ≈ 4,900 analyst hours/yr
- Parallel run flags intercompany and credit-note timing differences; retirement rule applied per region

> Synthetic data is calibrated to the shape of the real problem; exact figures will differ slightly from the engagement results above.

## Run it
```bash
python data/generate_data.py            # report inventory + legacy vs cockpit figures for the parallel run
python src/report_rationalization.py    # which reports to retire, hours saved
python src/parallel_run_reconciliation.py
```

## Contents
`docs/stakeholder_interviews.md` · `docs/BRD.md` · `docs/kpi_dictionary.md` · `docs/user_stories_releases.md` · `docs/rls_design.md` · `docs/uat_parallel_run.md` · `powerbi/measures.dax` · `sql/` · `src/`
