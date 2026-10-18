CREATE SCHEMA IF NOT EXISTS CPC;

CREATE OR REPLACE TABLE CPC.DIM_DATE (date DATE PRIMARY KEY, fiscal_year INT, fiscal_quarter INT, fiscal_month INT);
CREATE OR REPLACE TABLE CPC.DIM_GEOGRAPHY (territory_id VARCHAR PRIMARY KEY, territory VARCHAR, region VARCHAR, zone VARCHAR);
CREATE OR REPLACE TABLE CPC.DIM_PRODUCT (product_id VARCHAR PRIMARY KEY, product VARCHAR, brand VARCHAR, category VARCHAR);
CREATE OR REPLACE TABLE CPC.DIM_CUSTOMER (customer_id VARCHAR PRIMARY KEY, customer VARCHAR, segment VARCHAR,
                                          territory_id VARCHAR, is_intercompany BOOLEAN);

CREATE OR REPLACE TABLE CPC.FACT_SALES (
    invoice_line_id VARCHAR PRIMARY KEY, invoice_date DATE, customer_id VARCHAR, product_id VARCHAR,
    territory_id VARCHAR, qty NUMBER(14,2), gross_amount NUMBER(18,2), discount NUMBER(18,2),
    returns NUMBER(18,2), net_amount NUMBER(18,2), std_cogs NUMBER(18,2)
);
CREATE OR REPLACE TABLE CPC.FACT_TARGET (month_start DATE, territory_id VARCHAR, product_id VARCHAR, target_amount NUMBER(18,2));
CREATE OR REPLACE TABLE CPC.FACT_PIPELINE (opportunity_id VARCHAR, snapshot_date DATE, customer_id VARCHAR,
                                           stage VARCHAR, amount NUMBER(18,2), expected_close DATE);

-- RLS mapping
CREATE OR REPLACE TABLE CPC.SEC_USER_GEO (user_email VARCHAR, territory_id VARCHAR, role VARCHAR);

-- Reporting view applying KPI dictionary rules (exclude intercompany)
CREATE OR REPLACE VIEW CPC.V_SALES_REPORTING AS
SELECT s.*
FROM CPC.FACT_SALES s
JOIN CPC.DIM_CUSTOMER c USING (customer_id)
WHERE NOT c.is_intercompany;

-- Parallel-run reconciliation: cockpit vs legacy month-end pack
SELECT l.month_start, l.region,
       l.net_revenue                                         AS legacy_nr,
       SUM(v.net_amount)                                     AS cockpit_nr,
       DIV0(SUM(v.net_amount) - l.net_revenue, l.net_revenue) AS diff_pct,
       IFF(ABS(diff_pct) <= 0.005, 'MATCH', 'INVESTIGATE')    AS status
FROM CPC.LEGACY_MONTH_END l
JOIN CPC.DIM_GEOGRAPHY g ON g.region = l.region
JOIN CPC.V_SALES_REPORTING v ON v.territory_id = g.territory_id
                            AND DATE_TRUNC('month', v.invoice_date) = l.month_start
GROUP BY 1, 2, 3;
