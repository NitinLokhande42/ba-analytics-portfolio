# As-Is Process (email & paper)

```mermaid
flowchart LR
  A[Requester fills Excel form] --> B[Email to line manager]
  B --> C[Department head sign-off]
  C --> D[Second department sign-off]:::redundant
  D --> E[Finance pre-check]:::redundant
  E --> F[Budget owner check]
  F --> G{Amount > 5L?}
  G -- yes --> H[CFO approval]
  G -- no --> I[Procurement]
  H --> I
  I --> J[Requester acknowledgement email]:::redundant
  J --> K[Admin files PDF]
  classDef redundant fill:#fdd,stroke:#c00
```

| Step | Touches | Avg wait (h) | Issue |
|---|---|---|---|
| Form + email | 2 | 4 | Wrong template, missing attachments (22% returned) |
| Line manager | 1 | 18 | Lost in inbox |
| Department head | 1 | 20 | |
| Second department sign-off | 1 | 16 | Duplicate of department head for cross-charged costs |
| Finance pre-check | 1 | 22 | Repeats budget owner check |
| Budget owner | 1 | 18 | |
| CFO (if > ₹5 L) | 1 | 30 | Travel, no delegation |
| Procurement + acknowledgement | 1 | 14 | Acknowledgement adds no control |
| Filing | — | 8 | Manual |
| **Total** | **9** | **~7 days** | No visibility of status |
