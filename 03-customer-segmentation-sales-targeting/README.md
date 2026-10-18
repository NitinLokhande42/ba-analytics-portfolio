# 03 · Customer Segmentation & Sales Force Targeting

**Company:** Cipla · **Stack:** SQL, Python, Power BI, CRM · **Role:** Business Analyst

## Business problem
Medical representatives visited doctors largely by habit and relationship. High-potential prescribers in fast-growing
therapy areas were under-covered while low-potential doctors got frequent visits. Sales leadership wanted to grow
priority segments **without adding headcount**.

## My BA role
- Defined **segmentation rules** with sales leadership: prescriber potential (therapy-area patient volume) × current Cipla share.
- Designed **call-plan logic**: visit frequency per segment, per-rep capacity limits, and priority products by segment.
- Designed a **2-region pilot vs. control** test with matched regions and a pre/post difference-in-differences read-out.
- Wrote the CRM change requirements (segment field, call-plan targets, compliance tracking) and the Power BI tracker spec.
- **Trained managers** on the rollout: segment meaning, call-plan adherence reports, coaching conversations.

## Approach
1. **Data** — doctor master, prescription audit data (potential), Cipla secondary sales, CRM call history (`sql/`).
2. **Segmentation** — rule-based 3×3 grid (potential tier × share tier) mapped to 4 actionable segments, validated with k-means.
3. **Call plan** — frequency by segment (e.g. *Grow* 4 calls/month, *Defend* 3, *Maintain* 1, *Deprioritise* 0–1), constrained by rep capacity of ~200 calls/month.
4. **Pilot** — 2 pilot regions vs. 2 matched control regions for 6 months; difference-in-differences on priority-segment sales.
5. **Scale-up** — national rollout with manager dashboards for call-plan adherence.

## Impact
| Metric | Result |
|---|---|
| Sales in priority segments | **+8%** vs. control |
| Annual value | **~₹6.4 Cr / year** |
| Headcount | **No change** — calls re-allocated, not added |

## What the code reproduces (synthetic data)
- Share of calls on GROW/DEFEND doctors 30% → 69% with the same total call capacity
- Difference-in-differences: steady-state uplift ≈ 8% → ≈ ₹6.4 Cr/yr at national scale

> Synthetic data is calibrated to the shape of the real problem; exact figures will differ slightly from the engagement results above.

## Run it
```bash
python data/generate_data.py
python src/segmentation.py     # segment doctors, build call plan
python src/pilot_analysis.py   # difference-in-differences on pilot vs control
```

## Contents
`docs/segmentation_rules.md` · `docs/call_plan_logic.md` · `docs/pilot_design.md` · `docs/training_plan.md` · `sql/` · `src/`
