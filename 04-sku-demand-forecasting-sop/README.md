# 04 · SKU Demand Forecasting & S&OP

**Company:** Cipla · **Stack:** SQL, forecasting models (Holt-Winters, gradient boosting), Power BI · **Role:** Business Analyst

## Business problem
Demand planning ran on a chain of spreadsheets: each brand team adjusted last year's numbers by gut feel, files were
emailed around, and the monthly demand review argued about which version was right. Forecast accuracy was **~65%**,
inventory sat at **₹100 Cr**, and stockouts of fast-moving SKUs still happened.

## My BA role
- **Gap analysis** of the spreadsheet process: data sources, manual steps, version control, bias, missing metrics.
- Wrote **S&OP requirements**: forecast hierarchy (SKU → brand → therapy → national), monthly cycle calendar, override workflow and audit trail.
- Specified the **S&OP dashboards** in Power BI: accuracy and bias by SKU class, demand vs. supply plan, inventory cover, stockout risk list.
- Drove **adoption in the monthly demand review**: new agenda, consensus forecast sign-off, forecast value-add (FVA) tracking.

## Approach
1. **Data** — 4 years of monthly SKU × depot secondary sales, promotions, price changes, stockout flags (`sql/`).
2. **ABC-XYZ classification** — value (ABC) × volatility (XYZ) to decide model and review effort per SKU.
3. **Statistical forecasts** — Holt-Winters (damped trend, seasonal) per SKU and a global gradient-boosting model on lag/seasonality features; best model chosen by back-test per SKU.
4. **Consensus layer** — planners override only with a reason code; FVA measures whether overrides help.
5. **Inventory policy** — safety stock from forecast error (σ) and lead time, so better accuracy directly lowers stock.

## Impact
| Metric | Before | After |
|---|---|---|
| Forecast accuracy (1 − WMAPE) | 65% | **82%** |
| Inventory value | ₹100 Cr | **₹85 Cr** |
| Stockouts | baseline | **−28%** |

## What the code reproduces (synthetic data)
- Accuracy (1 − WMAPE): spreadsheet ≈ 67% → statistical best-of ≈ 83%
- Inventory indexed ₹100 Cr → ≈ ₹77–80 Cr with dynamic safety stock; stockout events ≈ −30%
- Trade-off between service level and inventory is configurable (`SERVICE` in `src/inventory_impact.py`)

> Synthetic data is calibrated to the shape of the real problem; exact figures will differ slightly from the engagement results above.

## Run it
```bash
python data/generate_data.py
python src/forecasting.py      # back-test spreadsheet method vs statistical models
python src/inventory_impact.py # safety stock and stockout simulation using the forecast errors
```

## Contents
`docs/gap_analysis.md` · `docs/sop_requirements.md` · `docs/dashboard_spec.md` · `docs/demand_review_process.md` · `sql/` · `src/`
