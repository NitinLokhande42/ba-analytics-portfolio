-- Feature table for churn scoring (as of :score_date)
CREATE OR REPLACE TABLE CHURN.FEATURES AS
WITH usage AS (
    SELECT customer_id,
           SUM(IFF(event_date >= DATEADD(day, -30, :score_date), sessions, 0))                    AS sessions_30d,
           SUM(IFF(event_date BETWEEN DATEADD(day, -90, :score_date) AND DATEADD(day, -31, :score_date), sessions, 0)) / 2 AS sessions_prior_30d_avg
    FROM usage_daily
    WHERE event_date >= DATEADD(day, -90, :score_date)
    GROUP BY 1
), tickets AS (
    SELECT customer_id, COUNT(*) AS tickets_90d, AVG(csat) AS csat_90d
    FROM support_tickets
    WHERE created_at >= DATEADD(day, -90, :score_date)
    GROUP BY 1
), billing AS (
    SELECT customer_id, COUNT_IF(days_late > 15) AS late_payments_6m
    FROM invoices
    WHERE invoice_date >= DATEADD(month, -6, :score_date)
    GROUP BY 1
)
SELECT c.customer_id,
       DATEDIFF(month, c.start_date, :score_date)                         AS tenure_months,
       c.plan, c.annual_revenue,
       COALESCE(u.sessions_30d, 0)                                        AS sessions_30d,
       DIV0(u.sessions_30d, u.sessions_prior_30d_avg) - 1                 AS usage_trend,
       COALESCE(t.tickets_90d, 0)                                         AS tickets_90d,
       t.csat_90d,
       COALESCE(b.late_payments_6m, 0)                                    AS late_payments_6m
FROM customers c
LEFT JOIN usage u   USING (customer_id)
LEFT JOIN tickets t USING (customer_id)
LEFT JOIN billing b USING (customer_id)
WHERE c.status = 'ACTIVE'
  AND DATEDIFF(day, c.start_date, :score_date) > 60;

-- Experiment read-out
SELECT experiment_group, risk_tier,
       COUNT(*)                                AS customers,
       1 - AVG(IFF(churned_90d, 1, 0))         AS retention_rate,
       SUM(IFF(churned_90d, 0, annual_revenue)) AS revenue_retained
FROM CHURN.EXPERIMENT_OUTCOMES
GROUP BY 1, 2
ORDER BY 2, 1;
