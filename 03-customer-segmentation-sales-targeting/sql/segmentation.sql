-- Doctor potential and Cipla share (last 6 months)
WITH rx AS (
    SELECT doctor_id,
           SUM(rx_count)                                      AS total_rx,
           SUM(IFF(company = 'CIPLA', rx_count, 0))           AS cipla_rx
    FROM rx_audit
    WHERE month >= DATEADD(month, -6, CURRENT_DATE())
      AND therapy_area IN ('RESPIRATORY', 'CARDIO', 'DIABETES')
    GROUP BY doctor_id
), ranked AS (
    SELECT d.doctor_id, d.territory_id, d.specialty, rx.total_rx,
           DIV0(rx.cipla_rx, rx.total_rx)                                         AS cipla_share,
           PERCENT_RANK() OVER (PARTITION BY d.territory_id ORDER BY rx.total_rx) AS potential_pct
    FROM doctor_master d
    JOIN rx USING (doctor_id)
)
SELECT *,
       CASE WHEN potential_pct >= 0.8 THEN 'HIGH' WHEN potential_pct >= 0.5 THEN 'MEDIUM' ELSE 'LOW' END AS potential_tier,
       CASE WHEN cipla_share >= 0.30 THEN 'HIGH' WHEN cipla_share >= 0.10 THEN 'MEDIUM' ELSE 'LOW' END   AS share_tier,
       CASE
         WHEN potential_pct >= 0.8 AND cipla_share <  0.30 THEN 'GROW'
         WHEN potential_pct >= 0.5 AND cipla_share >= 0.30 THEN 'DEFEND'
         WHEN potential_pct >= 0.5 AND cipla_share <  0.10 THEN 'DEVELOP'
         WHEN potential_pct >= 0.5                          THEN 'MAINTAIN'
         WHEN cipla_share >= 0.30                           THEN 'MAINTAIN'
         ELSE 'DEPRIORITISE'
       END AS segment
FROM ranked;

-- Call-plan adherence by rep (month to date)
SELECT c.rep_id,
       COUNT_IF(c.doctor_id IN (SELECT doctor_id FROM call_plan p WHERE p.rep_id = c.rep_id))  AS on_plan_calls,
       (SELECT SUM(planned_calls) FROM call_plan p WHERE p.rep_id = c.rep_id)                  AS planned_calls,
       DIV0(on_plan_calls, planned_calls)                                                      AS adherence
FROM crm_calls c
WHERE c.call_date >= DATE_TRUNC('month', CURRENT_DATE())
GROUP BY c.rep_id;
