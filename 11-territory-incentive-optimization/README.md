# 11 · Sales Territory & Incentive Optimization

**Company:** Genpact · **Stack:** SQL, optimization, Power BI · **Role:** Business Analyst

## Business problem
Territories had grown by history: some reps carried nearly double the workload of others (**±45% imbalance**),
targets did not reflect territory potential, and the incentive plan had grey areas (split accounts, mid-year transfers,
returns). The result was burnout in overloaded territories, missed opportunities, and a steady stream of **payout disputes**.

## My BA role
- Gathered **workload, target and incentive requirements** from sales ops, sales leadership, finance and HR.
- Documented every **business rule** (workload formula, territory constraints, target setting, payout tiers, caps, edge cases).
- Built the **payout test pack** and **tested payouts before launch** against finance's independent calculation.
- Specified the Power BI views: workload balance map, rep payout statements, dispute log.

## Approach
1. **Workload index** per account = visits/year × minutes per visit + travel time + admin, by account tier.
2. **Territory optimisation** — re-assign accounts between neighbouring territories to minimise workload imbalance, while keeping each rep's top accounts (relationship continuity) and limiting disruption.
3. **Target setting** — targets proportional to territory potential (60%) and history (40%).
4. **Incentive engine** — tiered payout curve with threshold, accelerator and cap; explicit rules for splits, transfers and returns.
5. **Payout testing** — automated test cases for every rule and edge case; parallel calculation with finance.

## Impact
| Metric | Before | After |
|---|---|---|
| Workload imbalance | ±45% | **±15%** |
| Payout disputes | baseline | **−60%** |

## What the code reproduces (synthetic data)
- Workload imbalance −43%/+39% → −11%/+17% moving ~10% of accounts (top-10 accounts locked, adjacency respected)
- Payout test pack: 13 test cases pass (`tests/test_incentive_rules.py`)

> Synthetic data is calibrated to the shape of the real problem; exact figures will differ slightly from the engagement results above.

## Run it
```bash
python data/generate_data.py
python src/territory_optimizer.py   # rebalance accounts, report imbalance before/after
python src/incentive_engine.py      # calculate payouts for all reps
python tests/test_incentive_rules.py  # payout test pack (also runs with pytest)
```

## Contents
`docs/business_rules.md` · `docs/requirements.md` · `docs/payout_test_cases.md` · `sql/` · `src/` · `tests/`
