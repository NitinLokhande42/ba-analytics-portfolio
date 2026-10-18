-- Territory workload and imbalance
WITH acct AS (
    SELECT a.account_id, a.territory_id, a.tier,
           CASE a.tier WHEN 'A' THEN 24 WHEN 'B' THEN 12 ELSE 4 END AS visits,
           CASE a.tier WHEN 'A' THEN 60 WHEN 'B' THEN 45 ELSE 30 END AS mins,
           a.travel_minutes
    FROM accounts a
), wl AS (
    SELECT territory_id,
           SUM(visits * (mins + travel_minutes) / 60.0 + 2) AS workload_hours
    FROM acct GROUP BY territory_id
)
SELECT territory_id, workload_hours,
       workload_hours / AVG(workload_hours) OVER () - 1 AS imbalance_pct
FROM wl
ORDER BY imbalance_pct DESC;

-- Quarterly attainment with split credit and returns
SELECT c.rep_id, DATE_TRUNC('quarter', s.invoice_date) AS qtr,
       SUM(s.net_amount * c.split_pct)                  AS credited_revenue,
       MAX(t.prorated_target)                           AS target,
       DIV0(credited_revenue, target)                   AS attainment
FROM sales s
JOIN account_credit_split c ON c.account_id = s.account_id
JOIN rep_targets t          ON t.rep_id = c.rep_id AND t.qtr = DATE_TRUNC('quarter', s.invoice_date)
GROUP BY 1, 2;
