# BRD — Commercial Performance Cockpit

## Objectives
| ID | Objective | KPI |
|---|---|---|
| BO-1 | One agreed set of commercial KPIs | KPI dictionary signed by CCO and CFO |
| BO-2 | Same-day reporting | Data available by 07:00 daily; month-end pack D+0 |
| BO-3 | Reduce report production effort | ≥ 4,000 analyst hours/yr; ≥ 35 reports retired |
| BO-4 | Secure access by role | RLS tested for 100% of roles |

## Functional requirements (summary)
| ID | Requirement | Release |
|---|---|---|
| FR-01 | Revenue, volume and target by day/month/quarter, region, territory, product, customer | R1 |
| FR-02 | Executive summary with variance to target and prior year | R1 |
| FR-03 | RLS by geography; margin visible only to finance/leadership roles | R1 |
| FR-04 | Margin bridge: price, volume, mix, cost | R2 |
| FR-05 | Customer and product profitability ranking | R2 |
| FR-06 | Pipeline by stage, ageing, conversion, coverage vs. target | R3 |
| FR-07 | Forecast vs. actual by region | R3 |
| FR-08 | Drill-through to account detail and invoice lines | R1–R3 |
| FR-09 | Export to Excel respecting RLS | R1 |

## Non-functional
Refresh complete by 07:00 IST; page load < 5 s; 99% availability in business hours; audit log of access.

## Out of scope
Incentive calculation (separate project), real-time order tracking.

## Transition
Two-month parallel run; legacy report retired only after three consecutive matched month-ends and owner sign-off.
