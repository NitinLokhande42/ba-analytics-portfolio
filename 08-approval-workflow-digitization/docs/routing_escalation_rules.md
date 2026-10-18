# Routing & Escalation Rules

## Approval matrix (SharePoint list `ApprovalMatrix`)
| Rule | Category | Amount (₹) | Approvers (in order) | Mode |
|---|---|---|---|---|
| R1 | Any | ≤ 50,000 | Line manager | Single |
| R2 | Opex | 50,001 – 5,00,000 | Line manager → Budget owner | Sequential |
| R3 | Opex | > 5,00,000 | Line manager → Budget owner → CFO | Sequential |
| R4 | Capex | Any | Line manager → Budget owner → CFO | Sequential |
| R5 | IT purchase | > 50,000 | Line manager → (Budget owner ∥ IT head) | Parallel second stage |
| R6 | Contract | Any | Line manager → Legal → Budget owner | Sequential |

## Business rules
1. Requester cannot approve own request; if requester is the line manager, route to their manager.
2. Budget check: if amount > remaining budget for cost centre, flag and route to CFO regardless of amount.
3. Delegation: if approver has an active delegation in `Delegations` list, route to delegate and record both names.
4. Out-of-office: if no delegation and OOO detected, route to approver's manager after 4 hours.
5. Split-request detection: same requester, same vendor, total > threshold within 7 days → treat as combined amount.

## SLA & escalation
| Event | Action |
|---|---|
| 24h pending | Reminder to approver (Teams + email) |
| 48h pending | Escalate to approver's manager; requester notified |
| 72h pending | Escalate to process owner; listed on weekly exceptions report |
| Rejected | Mandatory reason; requester may edit and resubmit once |

## Audit
Every action stored in `ApprovalHistory` (who, when, decision, comment, delegate, rule ID) — retained 8 years.
