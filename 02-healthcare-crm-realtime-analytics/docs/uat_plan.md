# UAT Plan

**Testers:** 8 contact-centre supervisors, 4 care managers, 2 schedulers · **Environment:** Salesforce full-copy sandbox + AWS staging

| ID | Scenario | Expected | Result |
|---|---|---|---|
| UAT-01 | Book appointment with 3 prior no-shows | High tier, live-agent task within 5 min | Pass |
| UAT-02 | Reschedule high-risk appointment | Task updated, not duplicated | Pass after fix |
| UAT-03 | Discharge with high risk score | Call task due in 48h | Pass |
| UAT-04 | Leave discharge task open 36h | Escalation to supervisor queue | Pass |
| UAT-05 | Duplicate event delivered | Single task (idempotent) | Pass |
| UAT-06 | Hospital director logs into Power BI | Sees own hospital only | Pass |
| UAT-07 | Agent opens patient | Context panel < 2 s | Pass |
| UAT-08 | Dashboard refresh | Data ≤ 15 min old | Pass |
