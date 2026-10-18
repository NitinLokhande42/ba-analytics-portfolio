# KPI Dictionary & Data Specification

## KPIs
| KPI | Definition | Formula | Owner |
|---|---|---|---|
| Net revenue | Invoiced revenue net of returns and discounts | SUM(net_revenue) | Finance |
| Marketing spend | Media + production + agency fees, excl. GST | SUM(spend) | Marketing |
| Channel contribution | Revenue attributed to a channel by the model | Σ β_c · sat(adstock(spend_c)) | Analytics |
| Channel ROI | Revenue attributed per ₹ spent | contribution_c / spend_c | Analytics |
| Marketing ROI | Total attributed revenue per ₹ spent | Σ contribution / Σ spend | Analytics |
| Base revenue | Revenue not explained by marketing (trend, seasonality, price) | intercept + controls | Analytics |
| Marginal ROI | Revenue from the next ₹1 in a channel | ∂contribution / ∂spend | Analytics |

## Data specification
| Field | Type | Grain | Source | Rule |
|---|---|---|---|---|
| week_start | DATE | Week (Mon) | Calendar | ISO week |
| channel | VARCHAR | Week × channel | Agency files / ad platforms | One of TV, DIGITAL, PRINT, RADIO, FIELD |
| spend_inr | NUMBER(18,2) | Week × channel | Agency / finance | Excl. GST; ≥ 0 |
| net_revenue_inr | NUMBER(18,2) | Week | ERP | Net of returns |
| price_index | NUMBER(6,3) | Week | Category team | 1.0 = base price |
| promo_flag | BOOLEAN | Week | Trade marketing | 1 if a national promotion ran |

**Data quality checks:** no missing weeks; spend non-negative; weekly revenue within ±3σ of rolling mean (flag, do not drop).
