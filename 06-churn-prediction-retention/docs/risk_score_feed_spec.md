# Risk-Score Feed Specification

| Item | Detail |
|---|---|
| Source | `CHURN.RISK_SCORE_WEEKLY` (Snowflake) |
| Target | CRM custom object `Churn_Risk__c`, upsert on `customer_id` |
| Refresh | Weekly, Monday 06:00 IST; CRM sync by 08:00 |
| Population | Active customers, excluding the exclusions in the churn definition |

| Field | Type | Description |
|---|---|---|
| customer_id | VARCHAR | Key |
| score_date | DATE | Scoring date |
| churn_probability | FLOAT (0–1) | Calibrated 90-day churn probability |
| risk_tier | VARCHAR | HIGH / MEDIUM / LOW |
| reason_1..3 | VARCHAR | Top drivers (from feature contributions), business-friendly text |
| annual_revenue | NUMBER | For prioritising within tier |
| experiment_group | VARCHAR | TREATMENT / CONTROL during the test |
| model_version | VARCHAR | For audit |

**Quality checks:** row count within ±5% of last week; no nulls in key fields; tier distribution 10/15/75 ±2 pts.
**Control-group rule:** CONTROL customers are visible to analytics but **not** pushed to agent queues during the test.
