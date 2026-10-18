"""Synthetic appointments and discharges (sample of the network, de-identified)."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir  # noqa: E402

rng = np.random.default_rng(11)
N = 60_000

appt = pd.DataFrame({
    "appointment_id": [f"A{i:07d}" for i in range(N)],
    "patient_token": rng.integers(0, 40_000, N).astype(str),
    "clinic_id": rng.integers(1, 301, N),
    "lead_time_days": rng.gamma(1.6, 9, N).round().astype(int),
    "age": rng.integers(18, 90, N),
    "prior_no_shows_12m": rng.poisson(0.5, N),
    "specialty": rng.choice(["primary_care", "cardiology", "ortho", "derm", "behavioral", "ob_gyn"], N),
    "payer": rng.choice(["commercial", "medicare", "medicaid", "self_pay"], N, p=[0.5, 0.25, 0.2, 0.05]),
    "distance_miles": rng.gamma(2, 5, N).round(1),
    "monday_or_friday": rng.random(N) < 0.4,
    "sms_opt_in": rng.random(N) < 0.8,
})
logit = (-3.35 + 0.045 * appt.lead_time_days + 0.75 * appt.prior_no_shows_12m - 0.012 * (appt.age - 50)
         + 0.03 * appt.distance_miles + 0.2 * appt.monday_or_friday
         + appt.payer.map({"commercial": 0, "medicare": -0.1, "medicaid": 0.5, "self_pay": 0.7})
         + appt.specialty.map({"behavioral": 0.4, "derm": 0.2}).fillna(0))
appt["no_show"] = (rng.random(N) < 1 / (1 + np.exp(-logit))).astype(int)

M = 8_000
dis = pd.DataFrame({
    "encounter_id": [f"E{i:06d}" for i in range(M)],
    "hospital_id": rng.integers(1, 26, M),
    "length_of_stay": rng.gamma(2, 2.2, M).round().astype(int) + 1,
    "acute_admit": rng.random(M) < 0.55,
    "comorbidity_index": rng.poisson(1.8, M),
    "ed_visits_6m": rng.poisson(0.7, M),
})
dis.to_csv(data_dir(__file__) / "discharges.csv", index=False)
appt.to_csv(data_dir(__file__) / "appointments.csv", index=False)
print(f"Wrote {N:,} appointments (no-show rate {appt.no_show.mean():.1%}) and {M:,} discharges")
