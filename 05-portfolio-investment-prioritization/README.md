# 05 · Product Portfolio Investment Prioritization

**Company:** Cipla · **Stack:** Excel NPV model, Monte Carlo simulation, Power BI · **Role:** Business Analyst

## Business problem
Every year R&D, marketing, manufacturing and finance proposed new products, line extensions and in-licensing deals.
Each function used its own assumptions and template, so comparing projects took **~6 weeks** of back-and-forth, and
decisions leaned toward whoever presented best. Some projects with poor risk-adjusted returns were funded.

## My BA role
- **Aligned four functions** (R&D, marketing, manufacturing, finance) on a single set of evaluation criteria, weights and assumption ranges.
- Built the standard **NPV template** (Excel) with uncertainty ranges and a Monte Carlo layer.
- **Documented the decision process**: intake form, gates, who approves, what evidence is required at each gate.
- Built the **leadership dashboard** in Power BI: risk-return bubble chart, NPV distributions, ranked portfolio within budget.

## Approach
1. **Common assumptions** — peak sales, time to peak, price erosion, COGS %, capex, launch probability, discount rate (WACC).
2. **Monte Carlo NPV** — 10,000 simulations per project using triangular distributions agreed with each function owner.
3. **Scorecard** — 60% financial (expected NPV, P(NPV<0), payback) + 40% strategic (therapy fit, capability fit, competitive intensity).
4. **Portfolio selection** — rank by score and expected NPV per ₹ invested; fund within the capex budget; flag projects with P(NPV<0) > 40% for rework or stop.

## Impact
| Metric | Before | After |
|---|---|---|
| Evaluation cycle | 6 weeks | **1 week** |
| Low-return spend avoided | — | **~₹8 Cr** |

## What the code reproduces (synthetic data)
- 10,000-run Monte Carlo per project; P10/P90 and P(NPV<0) reported
- Risk-adjusted selection raises portfolio eNPV vs. the old 'rank by peak sales' approach at the same capex budget and avoids a low-return project

> Synthetic data is calibrated to the shape of the real problem; exact figures will differ slightly from the engagement results above.

## Run it
```bash
python data/generate_data.py   # candidate projects with assumption ranges
python src/monte_carlo_npv.py  # simulate NPVs, score and select the portfolio
```

## Contents
`docs/evaluation_criteria.md` · `docs/decision_process.md` · `docs/assumptions_register.md` · `docs/dashboard_spec.md` · `excel/README.md` · `src/`
