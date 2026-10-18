-- Wide weekly table consumed by the model (one row per week)
CREATE OR REPLACE VIEW MKT_MMM.V_MODEL_INPUT AS
SELECT
    r.week_start,
    r.net_revenue_inr,
    c.price_index,
    IFF(c.promo_flag, 1, 0)                         AS promo_flag,
    SUM(IFF(s.channel = 'TV',      s.spend_inr, 0)) AS spend_tv,
    SUM(IFF(s.channel = 'DIGITAL', s.spend_inr, 0)) AS spend_digital,
    SUM(IFF(s.channel = 'PRINT',   s.spend_inr, 0)) AS spend_print,
    SUM(IFF(s.channel = 'RADIO',   s.spend_inr, 0)) AS spend_radio,
    SUM(IFF(s.channel = 'FIELD',   s.spend_inr, 0)) AS spend_field
FROM MKT_MMM.FACT_REVENUE r
JOIN MKT_MMM.DIM_CONTROLS c USING (week_start)
LEFT JOIN MKT_MMM.FACT_MEDIA_SPEND s USING (week_start)
GROUP BY 1, 2, 3, 4;

-- Data-quality check: weeks missing from revenue feed
SELECT DATEADD(week, SEQ4(), (SELECT MIN(week_start) FROM MKT_MMM.FACT_REVENUE)) AS expected_week
FROM TABLE(GENERATOR(ROWCOUNT => 156))
MINUS
SELECT week_start FROM MKT_MMM.FACT_REVENUE;

-- Channel spend share by year (feeds Power BI)
SELECT YEAR(week_start) AS yr, channel,
       SUM(spend_inr) AS spend_inr,
       RATIO_TO_REPORT(SUM(spend_inr)) OVER (PARTITION BY YEAR(week_start)) AS share
FROM MKT_MMM.FACT_MEDIA_SPEND
GROUP BY 1, 2
ORDER BY 1, 3 DESC;
