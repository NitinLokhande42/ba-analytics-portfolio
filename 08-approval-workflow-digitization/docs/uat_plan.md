# UAT Plan

| ID | Scenario | Expected | Result |
|---|---|---|---|
| UAT-01 | ₹30,000 opex | Line manager only (R1) | Pass |
| UAT-02 | ₹2,00,000 opex | Line manager → budget owner | Pass |
| UAT-03 | ₹8,00,000 opex | Adds CFO | Pass |
| UAT-04 | Capex ₹40,000 | CFO included (R4) | Pass |
| UAT-05 | IT ₹1,00,000 | Parallel budget owner + IT head | Pass after fix |
| UAT-06 | Approver has delegation | Routed to delegate; both names logged | Pass |
| UAT-07 | No action 48h | Escalated to manager | Pass |
| UAT-08 | Requester is line manager | Routed to their manager | Pass |
| UAT-09 | Two ₹30,000 requests same vendor in 3 days | Combined → R2 | Pass after fix |
| UAT-10 | Over-budget ₹20,000 | Routed to CFO | Pass |
| UAT-11 | Mobile approval via Teams card | Works on iOS/Android | Pass |

**Participants:** 14 users (requesters, approvers, finance, procurement) · **Defects:** 17 (2 high) · all closed.
