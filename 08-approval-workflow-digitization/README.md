# 08 · Approval Workflow Digitization

**Company:** Neutrino · **Stack:** Power Apps, Power Automate, SharePoint · **Role:** Business Analyst

## Business problem
Purchase, expense-exception and contract approvals ran on email and printed forms. A request passed through
**9 manual touches** and up to **7 approval steps**, some duplicated, taking **~7 days** on average. Nobody could see
where a request was stuck, and approvers on leave silently stalled everything.

## My BA role
- Mapped the **as-is process** with requesters, approvers, finance and procurement; measured touches and waiting time per step.
- Designed the **to-be process**; got agreement to **remove 3 redundant approvals** (duplicate department sign-off, finance pre-check that repeated the budget check, and a post-approval acknowledgement).
- Wrote the **routing and escalation rules** (amount thresholds, category, delegation, SLA reminders and auto-escalation).
- Owned **UAT** and the **phased rollout** (pilot department → finance & procurement → company-wide).

## Solution
- **Power Apps** request form with validation, attachments and live status.
- **SharePoint** lists for requests, approval history, delegation and the approval matrix (business-maintained, no code changes for threshold updates).
- **Power Automate** flow: reads the matrix, routes approvals (sequential/parallel), sends Teams/Outlook adaptive cards, reminders at 24h, escalation at 48h, auto-delegation when approver is out of office.

## Impact
| Metric | Before | After |
|---|---|---|
| Cycle time | 7 days | **1.5 days** |
| Manual touches | 9 | **2** |
| Effort saved | — | **~2,800 hours / year** |

## What the code reproduces (synthetic data)
- Cycle time ≈ 6.9 → 1.3 days (simulated), touches 9 → 2, ≈ 2,800 hours/yr effort saved
- Routing engine reproduces matrix rules R1–R6 plus delegation, over-budget and self-approval rules

> Synthetic data is calibrated to the shape of the real problem; exact figures will differ slightly from the engagement results above.

## Run it
```bash
python data/generate_data.py      # synthetic request history
python src/routing_engine.py      # apply routing & escalation rules to sample requests
python src/process_simulation.py  # as-is vs to-be cycle time and effort
```

## Contents
`docs/as_is_process.md` · `docs/to_be_process.md` · `docs/routing_escalation_rules.md` · `docs/uat_plan.md` · `docs/rollout_plan.md` · `power-platform/` · `src/`
