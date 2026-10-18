# SharePoint Lists

| List | Key columns |
|---|---|
| `Requests` | RequestID, Requester, Category, Amount, Vendor, CostCentre, Justification, Attachments, Status, CurrentApprover, RuleID, SubmittedOn, CompletedOn |
| `ApprovalMatrix` | RuleID, Category, MinAmount, MaxAmount, ApproverRoles (JSON array), Mode (Sequential/Parallel), Active |
| `ApprovalHistory` | RequestID, Step, Approver, Delegate, Decision, Comment, ActionOn, SLAHours |
| `Delegations` | Approver, Delegate, StartDate, EndDate |
| `Budgets` | CostCentre, FiscalYear, Budget, Committed, Remaining |
