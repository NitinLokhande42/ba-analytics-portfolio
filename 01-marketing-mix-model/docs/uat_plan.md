# UAT Plan — MMM & Budget Simulator

**Testers:** 6 marketing managers, 2 FP&A analysts · **Duration:** 2 weeks · **Defect tracking:** JIRA

| ID | Scenario | Expected result | Status |
|---|---|---|---|
| UAT-01 | Open ROI page | All 5 channels shown with mean and interval | Pass |
| UAT-02 | Totals reconcile | Σ contribution + base = actual revenue (±2%) | Pass |
| UAT-03 | Optimise at current total budget | Expected revenue ≥ current plan | Pass |
| UAT-04 | Infeasible constraints | Clear error message, no crash | Pass after fix |
| UAT-05 | Save and compare 3 scenarios | Side-by-side deltas shown | Pass |
| UAT-06 | Export to Excel | File matches on-screen values | Pass |
| UAT-07 | Back-test last quarter | MAPE ≤ 10% | Pass |

**Exit criteria:** no open high-severity defects; all Must requirements passed.
**Sign-off:** Head of Marketing, FP&A Lead.
