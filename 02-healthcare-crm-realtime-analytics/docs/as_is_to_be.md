# As-Is vs. To-Be Process

## As-is (latency ≈ 24h)
1. Appointment booked in EHR → synced to Salesforce overnight.
2. Nightly batch builds reminder list (all appointments in next 2 days, no prioritisation).
3. Blanket SMS to everyone; agents work a static spreadsheet of unconfirmed appointments next morning.
4. Discharges reported in next-day census; care management calls when capacity allows → **40%** reached within 48h.
5. Agent searches 3–4 screens for patient history → long handle times.

**Pain points:** late data, no prioritisation, duplicate outreach, manual lists, no visibility for supervisors during the day.

## To-be (latency ≈ minutes)
1. Booking/change event published from Salesforce in real time → Kinesis.
2. Lambda scores no-show risk and applies routing rules → task written back to Salesforce queue.
3. Low-risk: SMS only. Medium: SMS + IVR. High: live agent call, prioritised by appointment time.
4. Discharge event → risk score → high-risk task due in 48h; escalation at 36h.
5. Agent sees one context panel; disposition codes captured in a standard picklist.
6. Supervisors watch 15-minute dashboard and rebalance agents across queues.

| Step | As-is | To-be |
|---|---|---|
| Data latency | ~24 h | < 5 min |
| Outreach targeting | Everyone, same channel | Risk-tiered channel |
| Discharge follow-up | Ad hoc | SLA-driven queue with escalation |
| Agent screens per call | 3–4 | 1 |
