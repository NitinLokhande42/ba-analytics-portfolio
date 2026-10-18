# To-Be Process (Power Platform)

```mermaid
flowchart LR
  A[Requester submits Power App form] --> V{Validation}
  V -- fail --> A
  V -- pass --> R[Flow reads approval matrix]
  R --> M[Line manager - adaptive card]
  M --> B[Budget owner]
  B --> T{Amount > 5L or category = Capex?}
  T -- yes --> C[CFO / delegate]
  T -- no --> P[Procurement auto-notified]
  C --> P
  P --> Z[Status = Approved, record archived in SharePoint]
```

**Removed:** second department sign-off (covered by cost-centre owner in matrix), finance pre-check (budget check now automated against budget list), acknowledgement email (status visible in app).

| Metric | As-is | To-be |
|---|---|---|
| Approval steps (max) | 7 | 4 |
| Manual touches | 9 | 2 (submit, approve) |
| Visibility | None | Live status, approver and SLA timer |
| Returned for missing info | 22% | < 3% (mandatory fields) |
