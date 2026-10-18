-- Snowflake DDL for the MMM data mart
CREATE SCHEMA IF NOT EXISTS MKT_MMM;

CREATE OR REPLACE TABLE MKT_MMM.FACT_MEDIA_SPEND (
    week_start   DATE          NOT NULL,
    channel      VARCHAR(20)   NOT NULL,
    spend_inr    NUMBER(18,2)  NOT NULL,
    source_file  VARCHAR(200),
    loaded_at    TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    CONSTRAINT pk_spend PRIMARY KEY (week_start, channel)
);

CREATE OR REPLACE TABLE MKT_MMM.FACT_REVENUE (
    week_start       DATE NOT NULL PRIMARY KEY,
    net_revenue_inr  NUMBER(18,2) NOT NULL
);

CREATE OR REPLACE TABLE MKT_MMM.DIM_CONTROLS (
    week_start   DATE NOT NULL PRIMARY KEY,
    price_index  NUMBER(6,3),
    promo_flag   BOOLEAN
);

CREATE OR REPLACE TABLE MKT_MMM.SIM_SCENARIO (
    scenario_id          NUMBER AUTOINCREMENT PRIMARY KEY,
    scenario_name        VARCHAR(100),
    created_by           VARCHAR(100),
    created_at           TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    channel              VARCHAR(20),
    spend_inr            NUMBER(18,2),
    expected_revenue_inr NUMBER(18,2)
);
