-- Flatten raw appointment events (latest event per appointment)
CREATE OR REPLACE VIEW HC_RT.V_APPT_LATEST AS
SELECT payload:appointment_id::VARCHAR  AS appointment_id,
       payload:event_type::VARCHAR      AS event_type,
       payload:event_ts::TIMESTAMP_NTZ  AS event_ts,
       payload:clinic_id::VARCHAR       AS clinic_id
FROM HC_RT.RAW_EVENTS
WHERE payload:event_type IS NOT NULL
QUALIFY ROW_NUMBER() OVER (PARTITION BY payload:appointment_id ORDER BY payload:event_ts DESC) = 1;

-- No-show rate by day and clinic
CREATE OR REPLACE VIEW HC_RT.V_NO_SHOW_DAILY AS
SELECT DATE(appointment_ts) AS appt_date, clinic_id,
       COUNT_IF(status = 'NO_SHOW')                                         AS no_shows,
       COUNT_IF(status IN ('NO_SHOW', 'COMPLETED'))                         AS kept_or_missed,
       DIV0(no_shows, kept_or_missed)                                       AS no_show_rate
FROM HC_RT.FACT_APPOINTMENT
GROUP BY 1, 2;

-- 48-hour discharge call compliance
CREATE OR REPLACE VIEW HC_RT.V_DISCHARGE_SLA AS
SELECT DATE(discharge_ts) AS discharge_date, hospital_id,
       COUNT(*)                                                                         AS high_risk_discharges,
       COUNT_IF(first_call_ts <= DATEADD(hour, 48, discharge_ts))                       AS called_within_48h,
       DIV0(called_within_48h, high_risk_discharges)                                    AS compliance_48h
FROM HC_RT.FACT_DISCHARGE
WHERE high_risk_flag
GROUP BY 1, 2;

-- Average handle time by queue, 15-minute interval
CREATE OR REPLACE VIEW HC_RT.V_AHT_15MIN AS
SELECT TIME_SLICE(start_ts, 15, 'MINUTE') AS interval_start, queue,
       COUNT(*)                            AS handled_calls,
       AVG(talk_sec + hold_sec + acw_sec)  AS aht_sec
FROM HC_RT.FACT_CALL
GROUP BY 1, 2;

-- Open discharge tasks approaching breach (feeds supervisor escalation tile)
SELECT encounter_id, hospital_id, discharge_ts,
       DATEDIFF(hour, discharge_ts, CURRENT_TIMESTAMP()) AS hours_open
FROM HC_RT.FACT_DISCHARGE
WHERE high_risk_flag AND first_call_ts IS NULL
  AND DATEDIFF(hour, discharge_ts, CURRENT_TIMESTAMP()) >= 36
ORDER BY hours_open DESC;
