# Excel NPV Template (structure)

The production model was an Excel workbook; `src/monte_carlo_npv.py` reproduces its logic in Python.

| Sheet | Contents |
|---|---|
| `Inputs` | One row per assumption: low / most likely / high, owner function, source, date agreed |
| `Revenue` | Year 0–10: uptake curve to peak sales, price erosion after year 4 |
| `Costs` | COGS %, launch marketing, sustaining marketing, capex phasing |
| `CashFlow` | EBITDA → tax → free cash flow; NPV at WACC; payback year |
| `MonteCarlo` | Data table driving 10,000 RAND()-based draws via inverse triangular CDF |
| `Scorecard` | Strategic criteria (1–5) and weighted total |
| `Summary` | Expected NPV, P10/P90, P(NPV<0) — feeds Power BI |

Inverse triangular formula used in Excel:
`=IF(U<(c-a)/(b-a), a+SQRT(U*(b-a)*(c-a)), b-SQRT((1-U)*(b-a)*(b-c)))` where a=low, c=most likely, b=high, U=RAND().
