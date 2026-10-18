# UAT & Parallel Run

## UAT
- 22 testers across all roles, 3 cycles (one per release), 146 test cases.
- Defects: 58 raised (7 critical, 19 major, 32 minor); all critical/major fixed before go-live.

## Parallel run (2 months)
| Check | Tolerance | Frequency |
|---|---|---|
| Net revenue by region vs. legacy month-end pack | ±0.5% | Daily and month-end |
| Net revenue vs. general ledger | ±0.1% | Month-end |
| Volume by product | Exact | Weekly |
| Target attainment % | ±0.2 pts | Weekly |

**Root causes of differences found:** legacy reports included intercompany sales (2 regions), different credit-note
timing, a stale exchange rate in one file. Each resolved by applying the KPI dictionary rule and documenting it.

**Retirement rule:** a legacy report is switched off after **3 consecutive matched checks** and owner sign-off.
