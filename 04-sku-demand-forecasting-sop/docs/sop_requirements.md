# S&OP Requirements

## Functional
| ID | Requirement | Priority |
|---|---|---|
| SOP-1 | Monthly statistical forecast per SKU × depot, 18-month horizon | Must |
| SOP-2 | Forecast hierarchy SKU → brand → therapy → national with reconciliation | Must |
| SOP-3 | Planner overrides at brand or SKU level with mandatory reason code | Must |
| SOP-4 | Lock consensus forecast after demand review (D+8 of month) | Must |
| SOP-5 | Accuracy (1 − WMAPE) and bias at lag 1 and lag 3, by ABC-XYZ class | Must |
| SOP-6 | Forecast value-add: statistical vs. consensus accuracy | Should |
| SOP-7 | Safety stock recommendation per SKU from forecast error and lead time | Must |
| SOP-8 | Stockout-risk list: SKUs with projected cover < safety stock in next 8 weeks | Must |
| SOP-9 | Promotion and launch calendar as model inputs | Should |

## Monthly cycle
| Day | Step | Owner |
|---|---|---|
| D+1 | Actuals loaded, accuracy computed | Data team |
| D+3 | Statistical forecast refreshed | Demand planning |
| D+5 | Brand team overrides with reason codes | Marketing / brand |
| D+8 | Demand review: consensus sign-off | Head of S&OP |
| D+10 | Supply review: capacity and constraints | Supply chain |
| D+12 | Executive S&OP: decisions and escalations | COO |

## Non-functional
Forecast run completes in < 2 hours; Power BI refresh daily; history retained for 5 years.
