# S&OP Dashboard Specification (Power BI)

| Page | Visuals | Filters | Audience |
|---|---|---|---|
| 1. Accuracy | Accuracy trend (lag 1, lag 3); accuracy by ABC-XYZ matrix; worst 20 SKUs | Therapy, brand, planner | Demand review |
| 2. Bias & FVA | Bias by brand (over/under); statistical vs. consensus accuracy | Month | Head of S&OP |
| 3. Demand vs. supply | Consensus demand, supply plan, gap by month (18 months) | Brand, plant | Supply review |
| 4. Inventory health | Days of cover vs. target; excess stock list; value by ABC class | Depot | Supply chain, finance |
| 5. Stockout risk | SKUs projected below safety stock in next 8 weeks, with action owner | Depot, brand | Weekly ops call |

## Measures (DAX)
```DAX
Abs Error = SUMX(Forecast, ABS(Forecast[Actual] - Forecast[Forecast]))
WMAPE = DIVIDE([Abs Error], SUM(Forecast[Actual]))
Accuracy = 1 - [WMAPE]
Bias % = DIVIDE(SUM(Forecast[Forecast]) - SUM(Forecast[Actual]), SUM(Forecast[Actual]))
Days of Cover = DIVIDE(SUM(Inventory[OnHandQty]), [Avg Daily Demand Next 30D])
```
