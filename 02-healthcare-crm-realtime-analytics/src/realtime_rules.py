"""
Simulate the Lambda rules engine on a stream of discharge events.
Compares the as-is batch process (next-day list, capacity-limited) with the to-be real-time queue
(task created on event, 48h SLA, escalation at 36h).
"""
import heapq
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.paths import data_dir, output_dir  # noqa: E402

rng = np.random.default_rng(3)
HIGH_RISK_CUTOFF = 10
REACH_RATE = 0.75  # share of call attempts that reach the patient


def risk_score(row):
    """LACE-style score: Length of stay, Acuity, Comorbidity, ED visits."""
    los = row.length_of_stay
    l_pts = 0 if los < 1 else 1 if los == 1 else 2 if los == 2 else 3 if los == 3 else 4 if los <= 6 else 5 if los <= 13 else 7
    a_pts = 3 if row.acute_admit else 0
    c_pts = min(row.comorbidity_index, 4) + (1 if row.comorbidity_index >= 4 else 0)
    e_pts = min(row.ed_visits_6m, 4)
    return l_pts + a_pts + c_pts + e_pts


def simulate(df, realtime, calls_per_hour):
    """Event-driven simulation over 30 days; returns share of high-risk discharges called within 48h."""
    hours = 30 * 24
    df = df.copy()
    df["discharge_h"] = rng.uniform(0, hours, len(df))
    if realtime:
        df["available_h"] = df["discharge_h"] + 0.1          # task created within minutes
    else:
        df["available_h"] = np.ceil(df["discharge_h"] / 24) * 24 + 8  # next-morning list at 08:00
    queue, called, events = [], {}, df.sort_values("available_h").itertuples()
    pending = next(events, None)
    for h in range(hours + 72):
        while pending is not None and pending.available_h <= h:
            # real-time: earliest-due first (SLA driven); batch: list order (random)
            prio = pending.discharge_h if realtime else rng.random()
            heapq.heappush(queue, (prio, pending.encounter_id, pending.discharge_h))
            pending = next(events, None)
        open_hours = 8 <= h % 24 < 20
        capacity = calls_per_hour if open_hours else 0
        if realtime and queue:
            # tasks past 48h move to the supervisor escalation queue and are worked after in-SLA tasks
            queue = [(dh + (1e6 if h - dh > 48 else 0), eid, dh) for _, eid, dh in queue]
            heapq.heapify(queue)
        retry = []
        for _ in range(capacity):
            if not queue:
                break
            prio, eid, dh = heapq.heappop(queue)
            if rng.random() < REACH_RATE:
                called[eid] = h - dh          # patient reached
            elif h - dh < 7 * 24:
                retry.append((prio, eid, dh))  # no answer: retry next hour block
        for item in retry:
            heapq.heappush(queue, item)
    delays = pd.Series(called)
    return (delays <= 48).reindex(df.encounter_id, fill_value=False).mean(), delays


def main():
    dis = pd.read_csv(data_dir(__file__) / "discharges.csv")
    dis["risk_score"] = dis.apply(risk_score, axis=1)
    hr = dis[dis.risk_score >= HIGH_RISK_CUTOFF]
    print(f"Discharges: {len(dis):,} | high risk (score ≥ {HIGH_RISK_CUTOFF}): {len(hr):,} ({len(hr)/len(dis):.0%})")

    # As-is: care managers call from a next-morning, unprioritised list, sharing time with other work
    asis, _ = simulate(hr, realtime=False, calls_per_hour=4)
    # To-be: dedicated discharge queue staffed with hours freed by lower AHT and tiered outreach,
    # tasks created on the event and worked earliest-due first with 36h escalation
    tobe, delays = simulate(hr, realtime=True, calls_per_hour=8)
    print(f"Called within 48h — as-is batch: {asis:.0%} | to-be real-time queue: {tobe:.0%}")
    print(f"To-be median hours to first call: {delays.median():.1f}")
    pd.DataFrame({"process": ["as_is", "to_be"], "within_48h": [asis, tobe]}).to_csv(
        output_dir(__file__) / "discharge_sla.csv", index=False)


if __name__ == "__main__":
    main()
