-- A/B read-out: conversion by arm
SELECT arm,
       COUNT(*)                                   AS customers,
       SUM(converted_14d)                         AS conversions,
       AVG(converted_14d)                         AS conversion_rate,
       SUM(revenue_14d) / COUNT(*)                AS revenue_per_customer
FROM campaign_test_results
WHERE campaign_id = :campaign_id
GROUP BY arm;

-- Lift by pre-specified segment (exploratory)
SELECT segment,
       AVG(IFF(arm = 'TREATMENT', converted_14d, NULL)) - AVG(IFF(arm = 'HOLDOUT', converted_14d, NULL)) AS abs_lift,
       COUNT(*) AS n
FROM campaign_test_results
WHERE campaign_id = :campaign_id
GROUP BY segment
ORDER BY abs_lift DESC;

-- Audience for next campaign using uplift scores
SELECT customer_id
FROM customer_uplift_scores
WHERE score_month = DATE_TRUNC('month', CURRENT_DATE())
  AND uplift_score >= :threshold
  AND email_opt_in
  AND MOD(ABS(HASH(customer_id)), 100) >= 10;   -- 10% holdout kept out
