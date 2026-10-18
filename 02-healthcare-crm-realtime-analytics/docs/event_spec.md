# Real-Time Event Specification (minimum-necessary PHI)

## AppointmentEvent
| Field | Type | Notes |
|---|---|---|
| event_id | UUID | Idempotency key |
| event_type | ENUM | CREATED, RESCHEDULED, CANCELLED, CHECKED_IN, NO_SHOW |
| event_ts | TIMESTAMP (UTC) | |
| appointment_id | STRING | |
| patient_token | STRING | Tokenised MRN — no name/DOB in stream |
| clinic_id | STRING | |
| appointment_ts | TIMESTAMP | |
| lead_time_days | INT | Booking to appointment |
| specialty | STRING | |
| prior_no_shows_12m | INT | From patient summary |
| preferred_channel | ENUM | SMS, VOICE, EMAIL |

## DischargeEvent
| Field | Type | Notes |
|---|---|---|
| event_id | UUID | |
| discharge_ts | TIMESTAMP | |
| encounter_id | STRING | |
| patient_token | STRING | |
| hospital_id | STRING | |
| length_of_stay | INT | Days |
| acuity_admit | BOOLEAN | Emergency admission |
| comorbidity_index | INT | Charlson |
| ed_visits_6m | INT | |

**Delivery:** at-least-once; consumers de-duplicate on `event_id`. **Retention:** Kinesis 7 days, S3 raw 7 years.
