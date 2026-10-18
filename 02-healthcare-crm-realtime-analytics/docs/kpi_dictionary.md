# KPI Dictionary

| KPI | Definition | Formula | Grain | Target |
|---|---|---|---|---|
| No-show rate | Share of scheduled appointments where patient did not arrive and did not cancel ≥ 24h ahead | no_shows / (completed + no_shows) | Day × clinic | ≤ 14% |
| Confirmation rate | Appointments confirmed by patient before visit | confirmed / scheduled | Day × clinic | ≥ 70% |
| 48h discharge-call compliance | High-risk discharges with a completed call within 48h | calls ≤ 48h / high-risk discharges | Day × hospital | ≥ 90% |
| Average handle time (AHT) | Talk + hold + after-call work per handled call | Σ(talk+hold+acw) / handled calls | Interval × queue | −15% vs. baseline |
| Queue backlog | Open tasks past due time | COUNT(open AND due < now) | 15-min × queue | 0 for discharge queue |
| SMS spend | Cost of reminder messages sent | messages × unit cost | Day | ↓ vs. baseline |
| Recovered visits | Completed visits above baseline no-show rate | appts × (baseline NS − current NS) | Month | — |
| 30-day readmission rate | Discharges readmitted within 30 days | readmits / discharges | Month × hospital | ↓ |
| Model AUC | Discrimination of no-show score | ROC AUC on last 30 days | Week | ≥ 0.70 |
