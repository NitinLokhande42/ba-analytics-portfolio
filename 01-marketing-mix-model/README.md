# 01 · Marketing Mix Model & Budget Simulator

**Company:** Genpact · **Stack:** Bayesian MMM, Snowflake, Power BI · **Role:** Business Analyst

## Business problem
The marketing team spent **₹50 Cr a year** across TV, digital, print, radio and field activations, but budgets were set
by last year's split plus negotiation. Finance could not see which channels actually drove revenue, and marketing could
not defend its plan. Leadership wanted a model to explain channel contribution and a **what-if simulator** to test
re-allocations before committing money.

## My BA role
- Ran **requirement workshops** with marketing (brand, digital, media) and finance (FP&A) to agree the questions the model must answer.
- Wrote the **KPI and data specification**: weekly grain, spend/GRP sources, revenue definition, control variables (seasonality, price, promotions).
- Wrote **user stories** for the budget simulator (scenario creation, constraints, saving and comparing plans).
- Planned and ran **UAT** with marketing managers; logged defects in JIRA; signed off release.

## Approach
1. **Data** — 3 years of weekly spend by channel, revenue, price index and promotion flags loaded into Snowflake (`sql/`).
2. **Transformations** — geometric **adstock** (carry-over) and **Hill saturation** (diminishing returns) per channel.
3. **Model** — Bayesian linear regression with informative priors (spend effects positive), giving posterior distributions of channel ROI rather than single point estimates.
4. **Simulator** — constrained optimiser re-allocates budget (each channel within ±30% of current) to maximise expected revenue at a fixed total budget.
5. **Power BI** — contribution waterfall, ROI by channel with credible intervals, response curves and the scenario simulator.

## Impact
| Metric | Before | After |
|---|---|---|
| Budget re-allocated | — | **15% of ₹50 Cr (₹7.5 Cr)** |
| Marketing ROI | 2.1x | **2.5x** |
| Incremental revenue | — | **~₹20 Cr** |

## What the code reproduces (synthetic data)
- Hold-out MAPE (last 26 weeks): ~3%
- Optimiser moves ~12% of budget between channels (each within ±30%) at the same total spend
- Media-driven revenue +5.3% at the same budget
- Channel ROI shown with 90% credible intervals (ROI here is incremental media ROI, i.e. excludes base sales)

> Synthetic data is calibrated to the shape of the real problem; exact figures will differ slightly from the engagement results above.

## Run it
```bash
python data/generate_data.py   # synthetic weekly data
python src/mmm_model.py        # fit model, print ROI by channel, run optimiser
```

## Repository contents
| Path | What it is |
|---|---|
| `docs/BRD.md` | Business requirements document |
| `docs/user_stories.md` | Simulator user stories with acceptance criteria |
| `docs/kpi_data_spec.md` | KPI definitions and data specification |
| `docs/uat_plan.md` | UAT scenarios and sign-off |
| `sql/` | Snowflake DDL and the model-input view |
| `src/mmm_model.py` | Adstock, saturation, Bayesian regression and budget optimiser |
