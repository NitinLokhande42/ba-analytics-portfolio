# Gap Analysis — Spreadsheet Demand Planning

| Area | Current state (as-is) | Desired state (to-be) | Gap | Recommendation |
|---|---|---|---|---|
| Data | Sales exported manually from ERP each month; 3 days to consolidate | Automated daily load into Snowflake | Manual, slow, error-prone | Scheduled ERP extract, data-quality checks |
| Method | Last year × growth % per brand, judgment per SKU | Statistical baseline per SKU, judgment only as overrides | No baseline, no seasonality handling | Holt-Winters + ML baseline |
| Version control | 12+ emailed files, "final_v7.xlsx" | Single forecast of record with history | No audit trail | Forecast table with version and user stamp |
| Accuracy tracking | Not measured | WMAPE and bias by SKU, brand, planner | Cannot tell if forecasts improve | Accuracy dashboard |
| Overrides | Untracked | Reason-coded, FVA measured | Bias invisible | Override workflow |
| Segmentation | Same effort on all 1,200 SKUs | ABC-XYZ drives effort | Effort misallocated | Review only A/X-flagged exceptions |
| Inventory link | Safety stock = fixed 45 days cover | Safety stock from forecast error and lead time | Excess stock on stable SKUs, shortages on volatile ones | Dynamic safety stock |
| Review meeting | Debates numbers | Decides on exceptions and supply constraints | Low-value meeting | New agenda, pre-read dashboard |

**Quantified pain:** ~3 planner-days per month of consolidation; accuracy ~65%; 45-day blanket cover → ₹100 Cr inventory.
