CREATE SCHEMA IF NOT EXISTS SOP;

CREATE OR REPLACE TABLE SOP.FACT_SALES_MONTHLY (
    month_start DATE, sku_id VARCHAR, depot_id VARCHAR,
    qty NUMBER(14,2), value_inr NUMBER(18,2), stockout_days INT, promo_flag BOOLEAN
);

CREATE OR REPLACE TABLE SOP.FACT_FORECAST (
    forecast_run_month DATE,       -- month the forecast was produced
    target_month       DATE,       -- month being forecast
    sku_id             VARCHAR,
    forecast_type      VARCHAR,    -- STATISTICAL | CONSENSUS
    qty                NUMBER(14,2),
    model_name         VARCHAR,
    override_reason    VARCHAR,
    created_by         VARCHAR,
    created_at         TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Accuracy at lag 1 by SKU class
WITH f AS (
    SELECT f.sku_id, f.target_month, f.forecast_type, f.qty AS fcst, s.qty AS actual
    FROM SOP.FACT_FORECAST f
    JOIN (SELECT sku_id, month_start, SUM(qty) qty FROM SOP.FACT_SALES_MONTHLY GROUP BY 1, 2) s
      ON s.sku_id = f.sku_id AND s.month_start = f.target_month
    WHERE DATEDIFF(month, f.forecast_run_month, f.target_month) = 1
)
SELECT c.abc_class, c.xyz_class, f.forecast_type,
       1 - SUM(ABS(actual - fcst)) / NULLIF(SUM(actual), 0) AS accuracy,
       SUM(fcst - actual) / NULLIF(SUM(actual), 0)          AS bias
FROM f JOIN SOP.DIM_SKU_CLASS c USING (sku_id)
GROUP BY 1, 2, 3
ORDER BY 1, 2, 3;

-- ABC (value) × XYZ (coefficient of variation) classification, last 12 months
CREATE OR REPLACE TABLE SOP.DIM_SKU_CLASS AS
WITH m AS (
    SELECT sku_id, month_start, SUM(qty) qty, SUM(value_inr) val
    FROM SOP.FACT_SALES_MONTHLY
    WHERE month_start >= DATEADD(month, -12, CURRENT_DATE())
    GROUP BY 1, 2
), s AS (
    SELECT sku_id, SUM(val) val, STDDEV(qty) / NULLIF(AVG(qty), 0) cv FROM m GROUP BY 1
)
SELECT sku_id,
       CASE WHEN SUM(val) OVER (ORDER BY val DESC) / SUM(val) OVER () <= 0.8 THEN 'A'
            WHEN SUM(val) OVER (ORDER BY val DESC) / SUM(val) OVER () <= 0.95 THEN 'B' ELSE 'C' END AS abc_class,
       CASE WHEN cv < 0.25 THEN 'X' WHEN cv < 0.6 THEN 'Y' ELSE 'Z' END                          AS xyz_class
FROM s;
