# 02 · Healthcare CRM Real-Time Analytics

**Company:** Neutrino · **Stack:** Salesforce Health Cloud, AWS (Kinesis, Lambda, S3), SQL, Snowflake, Power BI, JIRA · **Role:** Business Analyst / Data Science

## Business problem
A large US healthcare network — **~25 hospitals, 300 outpatient clinics, 2.5 million active patients and a 400-seat
patient contact centre** — learned about problems **a day late**. No-show risk, unconfirmed appointments and high-risk
discharges only appeared in next-morning batch reports, so the contact centre called the wrong patients at the wrong
time. The network was losing revenue (empty slots, readmission penalties) and patient trust.

## My BA / data science role
- Mapped the as-is patient-contact process and the latency in each data hop (EHR → Salesforce → nightly batch → reports).
- Led requirement sessions with contact-centre operations, care management, clinic schedulers, compliance (HIPAA) and IT.
- Wrote the BRD, event specification, KPI dictionary and **JIRA epics/user stories** for real-time work queues.
- Built and validated the **no-show risk score** and the **discharge risk prioritisation rules**; defined alert thresholds with clinicians.
- Designed Power BI operational dashboards (15-minute refresh) and ran UAT with supervisors.

## Solution
```
EHR / Scheduling ──► Salesforce Health Cloud ──(Platform Events)──► AWS Kinesis ──► Lambda (scoring + rules)
                                                                           │              │
                                                                           ▼              ▼
                                                                   S3 raw zone    Salesforce work queues
                                                                           │        (agent next-best-call)
                                                                           ▼
                                                                Snowflake (Snowpipe) ──► Power BI (15-min)
```
1. **No-show risk model** scores every appointment at booking and again 72h / 24h before the visit.
2. **Outreach rules** route high-risk appointments to SMS → IVR → live agent based on risk tier, saving SMS and agent time.
3. **Discharge work queue**: high-risk discharges (LACE-style score) create a call task due within 48 hours.
4. **Agent desktop context** (recent visits, open tasks, preferred channel) shown in Salesforce to reduce handle time.
5. **Operational dashboard**: no-show trend, queue backlog, 48h discharge-call compliance, AHT, SMS spend.

## Impact (12 months)
| Metric | Before | After |
|---|---|---|
| No-show rate | 18% | **13.8%** |
| High-risk discharge calls within 48h | 40% | **91%** |
| Average handle time | baseline | **−17%** |
| Extra completed visits | — | **~130,000 / yr** (≈4-pt drop × ~3.3M yearly appointments) |

Further value: avoided readmission penalties, fewer agent hours, lower SMS spend (risk-tiered outreach).
See `src/impact_model.py` for the value calculation.

## What the code reproduces (synthetic data)
- No-show model ROC AUC ≈ 0.73 (acceptance target ≥ 0.70); fairness check by payer printed
- Discharge simulation: high-risk calls within 48h 42% (batch list) → 96% (real-time SLA queue with escalation)
- Impact model: 4.2-pt no-show drop × 3.3M appointments ≈ 138,600 recovered visits

> Synthetic data is calibrated to the shape of the real problem; exact figures will differ slightly from the engagement results above.

## Run it
```bash
python data/generate_data.py      # synthetic appointments, discharges, contact-centre calls
python src/no_show_model.py       # train/evaluate no-show risk score, assign outreach tiers
python src/realtime_rules.py      # simulate streaming events through the alerting rules
python src/impact_model.py        # business-value calculation
```

## Contents
| Path | What it is |
|---|---|
| `docs/BRD.md` | Business requirements |
| `docs/as_is_to_be.md` | Process and latency mapping |
| `docs/jira_epics_user_stories.md` | Epics and stories with acceptance criteria |
| `docs/kpi_dictionary.md` | Operational KPI definitions |
| `docs/event_spec.md` | Real-time event payloads |
| `docs/uat_plan.md` | UAT scenarios |
| `sql/` | Snowflake DDL, Snowpipe, KPI views |
| `src/` | Risk model, streaming rules simulator, impact model |
