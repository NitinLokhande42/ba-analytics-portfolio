# JIRA Epics & User Stories

## EPIC HC-1 Real-time event pipeline
- **HC-11** As an integration engineer I want appointment events published to Kinesis within 60 s so downstream rules act on current data.
  - AC: p95 publish latency ≤ 60 s measured over 7 days; events contain only fields listed in the event spec.
- **HC-12** As a data engineer I want events landed in S3 and Snowflake via Snowpipe so analytics has full history.
  - AC: row counts reconcile S3 vs. Snowflake daily (difference = 0).

## EPIC HC-2 No-show risk scoring
- **HC-21** As a scheduler I want every appointment to carry a no-show risk tier so I know which ones need attention.
  - AC: tier visible on the appointment record within 5 min of booking; tiers Low/Medium/High.
- **HC-22** As an operations manager I want risk recalculated at 72h and 24h so late changes are captured.
- **HC-23** As a compliance officer I want the model checked for bias by age band, language and payer.
  - AC: no group's false-negative rate exceeds the overall rate by more than 5 points.

## EPIC HC-3 Outreach routing
- **HC-31** As a contact-centre supervisor I want high-risk appointments routed to the live-agent queue ordered by visit time.
- **HC-32** As a marketing ops lead I want low-risk patients to receive SMS only so we cut SMS and call cost.
- **HC-33** As an agent I want a disposition picklist (confirmed, rescheduled, cancelled, no answer, wrong number) so outcomes are measurable.

## EPIC HC-4 Discharge follow-up
- **HC-41** As a care manager I want a call task created for each high-risk discharge with a 48h due time.
  - AC: task created ≤ 5 min after discharge event; due = discharge time + 48h.
- **HC-42** As a supervisor I want tasks open > 36h escalated to me so none breach the 48h SLA.

## EPIC HC-5 Agent productivity
- **HC-51** As an agent I want one patient context panel so I don't search multiple screens.
  - AC: panel shows last 3 visits, open tasks, preferred language and channel; loads < 2 s.

## EPIC HC-6 Operational dashboard
- **HC-61** As a VP Patient Access I want no-show rate, 48h discharge compliance, AHT and SMS spend refreshed every 15 min.
- **HC-62** As a hospital director I want to see only my facility's data (RLS).
