# 06 · Customer Churn Prediction & Retention Program

**Company:** Genpact · **Stack:** SQL, XGBoost, Snowflake · **Role:** Business Analyst

## Business problem
A subscription business with **~20,000 customers** lost customers without warning. The support team only learned a
customer was unhappy when the cancellation request arrived. Retention offers were given to whoever complained loudest,
not to customers who were actually at risk and worth saving.

## My BA role
- Defined **churn rules** with the customer support team (what counts as churn, observation and prediction windows, exclusions).
- Designed the **retention workflow**: who gets contacted, by which team, with which offer, within what SLA.
- Specified the **risk-score feed** from Snowflake to the support CRM (fields, refresh, thresholds, reason codes).
- Designed the **randomized controlled test** to prove the program's causal impact before full rollout.

## Approach
1. **Churn definition** — customer cancels or does not renew within 30 days of contract end; involuntary churn (payment failure) handled separately.
2. **Features** — tenure, usage trend (last 30 vs. prior 60 days), support tickets, CSAT, late payments, plan changes, product adoption.
3. **Model** — gradient boosted trees (XGBoost; scikit-learn fallback) predicting 90-day churn; calibrated probabilities; top reasons per customer.
4. **Feed** — weekly table in Snowflake with score, tier and top-3 reasons, synced to CRM work queues.
5. **Test** — high-risk customers randomly split 50/50 into treatment (retention workflow) and control (business as usual).

## Impact
| Metric | Result |
|---|---|
| Retention uplift | **+3 points** across ~20,000 customers |
| Revenue protected | **~$3.6M / year** (≈600 customers × ~$6K annual revenue) |

## What the code reproduces (synthetic data)
- Churn model ROC AUC ≈ 0.73 with decile lift table and reason codes in the risk-score feed
- Randomised test: +11 pts retention in targeted tiers → ≈ +2.8 pts across 20,000 customers ≈ $3.2M protected

> Synthetic data is calibrated to the shape of the real problem; exact figures will differ slightly from the engagement results above.

## Run it
```bash
python data/generate_data.py
python src/churn_model.py          # train, evaluate, build risk-score feed
python src/retention_experiment.py # analyse the randomized test
```

## Contents
`docs/churn_definition.md` · `docs/retention_workflow.md` · `docs/risk_score_feed_spec.md` · `docs/experiment_design.md` · `sql/` · `src/`
