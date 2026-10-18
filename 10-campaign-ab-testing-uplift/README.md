# 10 · Digital Campaign A/B Testing & Uplift Targeting

**Company:** Genpact · **Stack:** SQL, statistical testing, uplift modelling · **Role:** Business Analyst

## Business problem
Marketing sent digital offers (email, paid social retargeting, discount codes) to almost the whole customer base,
spending **~$2M a year**. Many recipients would have bought anyway, and some were never going to buy. Nobody could
say which part of the spend actually *caused* conversions.

## My BA role
- Set **hypotheses, success metrics and sample sizes** with marketing before each test (no "peeking", pre-registered decision rules).
- Wrote the test specification: randomisation unit, holdout share, duration, guardrail metrics.
- Translated results and the uplift model into **targeting rules** marketing could run in their campaign tool.
- Built the read-out template so every future campaign reports incremental conversions, not just response rate.

## Approach
1. **Randomised test** — 50/50 treatment vs. holdout on a large audience; primary metric = conversion within 14 days.
2. **Statistical test** — two-proportion z-test, confidence interval for lift; sample size from power analysis.
3. **Uplift model** — two-model (T-learner) gradient boosting estimates each customer's *incremental* conversion probability.
4. **Segments** — Persuadables (high uplift), Sure things (convert anyway), Lost causes, Do-not-disturb (negative uplift).
5. **Targeting rule** — only send to customers whose predicted uplift × margin > contact cost; validated on held-out data with a Qini curve.

## Impact
| Metric | Result |
|---|---|
| Campaign spend | **−25% (~$500K / year)** |
| Conversions | **Held flat** |

## What the code reproduces (synthetic data)
- Power analysis: ~12,200 per arm to detect +1 pt on an 8% baseline
- Uplift targeting of the top ~70–75% keeps total conversions within ±2% while cutting contacts by 25–30%

> Synthetic data is calibrated to the shape of the real problem; exact figures will differ slightly from the engagement results above.

## Run it
```bash
python data/generate_data.py
python src/ab_test.py         # power analysis + test read-out
python src/uplift_model.py    # T-learner, Qini, targeting rule and spend impact
```

## Contents
`docs/test_plan.md` · `docs/targeting_rules.md` · `sql/` · `src/`
