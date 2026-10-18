# Business Requirements Document — Healthcare CRM Real-Time Analytics

| Item | Detail |
|---|---|
| Sponsor | VP Patient Access & Contact Centre |
| Stakeholders | Contact-centre ops, care management, clinic schedulers, compliance/HIPAA, IT (Salesforce, AWS, data) |
| Scale | ~25 hospitals, 300 clinics, 2.5M active patients, 400-seat contact centre, ~3.3M appointments/yr |

## 1. Problem statement
Operational data reaches decision makers ~24 hours late. Outreach is based on yesterday's list, so high-risk
appointments go unconfirmed and high-risk discharges are not called in time.

## 2. Objectives
| ID | Objective | Target (12 months) |
|---|---|---|
| BO-1 | Reduce appointment no-shows | 18% → ≤ 14% |
| BO-2 | Call high-risk discharged patients within 48h | 40% → ≥ 90% |
| BO-3 | Reduce average handle time | −15% |
| BO-4 | Reduce outreach cost (SMS + agent hours) | Measurable reduction vs. baseline |

## 3. Scope
**In:** outpatient appointments, inpatient discharges, contact-centre interactions, SMS/IVR reminders.
**Out:** clinical decision support, billing workflows, telehealth platform changes.

## 4. Functional requirements
| ID | Requirement | Priority |
|---|---|---|
| FR-1 | Publish appointment create/change/cancel and discharge events from Salesforce within 60 seconds | Must |
| FR-2 | Score no-show risk at booking, 72h and 24h before visit | Must |
| FR-3 | Route outreach by risk tier: Low = SMS, Medium = SMS + IVR, High = live agent call | Must |
| FR-4 | Create a discharge follow-up task due within 48h for high-risk discharges | Must |
| FR-5 | Escalate discharge tasks open > 36h to supervisor queue | Must |
| FR-6 | Show patient context panel (last visits, open tasks, preferred channel, language) on agent screen | Must |
| FR-7 | Power BI operational dashboard refreshed every 15 minutes | Must |
| FR-8 | Offer freed slots to wait-listed patients when a high-risk appointment cancels | Should |
| FR-9 | Weekly model performance report (AUC, calibration, drift) | Should |

## 5. Non-functional requirements
- **HIPAA:** PHI encrypted in transit and at rest; minimum-necessary fields in events; BAA with all vendors; audit logs retained 6 years.
- **Latency:** event to work-queue ≤ 5 minutes (p95).
- **Availability:** 99.5% during contact-centre hours.
- **Access:** row-level security by hospital/region in Power BI; agents see only assigned queues.

## 6. Assumptions & dependencies
- Salesforce Health Cloud is the system of engagement; EHR feeds Salesforce via existing HL7/FHIR integration.
- SMS vendor supports per-message API callbacks for delivery/response status.

## 7. Risks
| Risk | Mitigation |
|---|---|
| Model bias against certain patient groups | Fairness check by age, language, payer; human review of thresholds |
| Alert fatigue for agents | Tiered routing; cap high-risk queue size per agent; tuned with supervisors |
| PHI exposure in analytics layer | De-identified analytics schema; tokenised patient IDs |
