# KPI Dictionary (signed off by CCO and CFO)

| KPI | Business definition | Calculation | Source | Owner |
|---|---|---|---|---|
| Gross sales | Invoiced value before discounts and returns | Σ invoice_line.gross_amount | ERP billing | Finance |
| Net revenue | Gross sales − discounts − returns − rebates | Σ net_amount | ERP billing | Finance |
| Volume | Units invoiced net of returns | Σ qty | ERP billing | Sales ops |
| Target attainment % | Net revenue ÷ target for the period | net_revenue / target | Targets table | Sales ops |
| YoY growth % | Change vs. same period last year | (NR − NR_LY) / NR_LY | ERP | Finance |
| Gross margin % | (Net revenue − standard COGS) ÷ net revenue | (NR − COGS) / NR | ERP + costing | Finance |
| Price effect | Change in average price × current volume | (P₁ − P₀) × Q₁ | Derived | Finance |
| Volume effect | Change in volume × prior price | (Q₁ − Q₀) × P₀ | Derived | Finance |
| Pipeline value | Open opportunities × amount | Σ amount where stage open | CRM | Sales ops |
| Weighted pipeline | Σ amount × stage probability | Σ amount × p_stage | CRM | Sales ops |
| Pipeline coverage | Weighted pipeline ÷ remaining target | WP / (target − NR) | CRM + targets | Sales ops |
| Win rate | Won ÷ (won + lost) opportunities closed in period | count ratio | CRM | Sales ops |
| Forecast accuracy | 1 − abs(forecast − actual) ÷ actual | — | FP&A | FP&A |

**Rules:** fiscal calendar April–March; currency INR at monthly average rate; intercompany sales excluded.
