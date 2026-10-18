# Churn Definition (agreed with Customer Support & Finance)

| Item | Rule |
|---|---|
| Churn event | Customer cancels, or contract ends and is not renewed within 30 days |
| Voluntary vs. involuntary | Payment-failure churn is *involuntary* and routed to billing, not the retention team |
| Prediction target | Voluntary churn in the next 90 days |
| Observation window | Last 180 days of behaviour as of the scoring date |
| Exclusions | Customers in first 60 days (onboarding program), internal/test accounts, customers already in cancellation process |
| Reactivation | Return within 90 days = not churned (save) |
| Retention rate | 1 − churned customers in period ÷ customers active at period start |
