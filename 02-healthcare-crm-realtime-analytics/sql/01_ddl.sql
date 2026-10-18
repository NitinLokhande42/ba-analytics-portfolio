-- Snowflake: de-identified analytics schema for the real-time CRM program
CREATE SCHEMA IF NOT EXISTS HC_RT;

CREATE OR REPLACE TABLE HC_RT.RAW_EVENTS (
    payload     VARIANT,
    file_name   VARCHAR,
    loaded_at   TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Snowpipe from S3 raw zone (Kinesis Firehose writes JSON)
CREATE OR REPLACE STAGE HC_RT.S3_EVENTS_STAGE
  URL = 's3://hc-crm-raw/events/'
  STORAGE_INTEGRATION = HC_S3_INT
  FILE_FORMAT = (TYPE = JSON);

CREATE OR REPLACE PIPE HC_RT.EVENTS_PIPE AUTO_INGEST = TRUE AS
  COPY INTO HC_RT.RAW_EVENTS (payload, file_name)
  FROM (SELECT $1, METADATA$FILENAME FROM @HC_RT.S3_EVENTS_STAGE);

CREATE OR REPLACE TABLE HC_RT.FACT_APPOINTMENT (
    appointment_id      VARCHAR PRIMARY KEY,
    patient_token       VARCHAR,
    clinic_id           VARCHAR,
    appointment_ts      TIMESTAMP_NTZ,
    booked_ts           TIMESTAMP_NTZ,
    specialty           VARCHAR,
    risk_score          FLOAT,
    risk_tier           VARCHAR(10),
    outreach_channel    VARCHAR(20),
    status              VARCHAR(20)   -- COMPLETED, NO_SHOW, CANCELLED
);

CREATE OR REPLACE TABLE HC_RT.FACT_DISCHARGE (
    encounter_id        VARCHAR PRIMARY KEY,
    patient_token       VARCHAR,
    hospital_id         VARCHAR,
    discharge_ts        TIMESTAMP_NTZ,
    risk_score          INT,
    high_risk_flag      BOOLEAN,
    first_call_ts       TIMESTAMP_NTZ,
    readmit_30d_flag    BOOLEAN
);

CREATE OR REPLACE TABLE HC_RT.FACT_CALL (
    call_id             VARCHAR PRIMARY KEY,
    agent_id            VARCHAR,
    queue               VARCHAR,
    start_ts            TIMESTAMP_NTZ,
    talk_sec            INT,
    hold_sec            INT,
    acw_sec             INT,
    disposition         VARCHAR
);
