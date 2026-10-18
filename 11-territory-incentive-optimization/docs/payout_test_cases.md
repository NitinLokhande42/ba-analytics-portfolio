# Payout Test Pack (executed before launch)

| TC | Scenario | Input | Expected payout (% of target incentive) |
|---|---|---|---|
| TC-01 | Below threshold | 79.9% attainment | 0% |
| TC-02 | At threshold | 80% | 50% |
| TC-03 | Mid band | 90% | 75% |
| TC-04 | On target | 100% | 100% |
| TC-05 | Accelerator | 110% | 120% |
| TC-06 | Accelerator top | 120% | 140% |
| TC-07 | Cap | 150% | 140% |
| TC-08 | Split account 60/40 | ₹10L sale | Rep A credited ₹6L, rep B ₹4L |
| TC-09 | Invalid split | 60/50 | Error raised |
| TC-10 | Mid-quarter transfer | 45 of 90 days, ₹30L target | Pro-rated target ₹15L |
| TC-11 | Return | Sale ₹5L month 1, return ₹2L month 2 | Net credit ₹3L |
| TC-12 | New hire | First quarter, 60% attainment | 100% (guarantee) |
| TC-13 | Leaver | Resigned before quarter end | 0 |

**Parallel check:** all reps' Q1 payouts recalculated independently by finance; 100% matched within ₹1 before launch.
**Dispute reduction drivers:** written rules (IP-1…IP-9), monthly statements showing every credit line, test pack evidence.
