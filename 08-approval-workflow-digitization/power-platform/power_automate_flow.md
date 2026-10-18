# Power Automate Flow — `Request Approval Router` (logic outline)

```
Trigger: When an item is created in Requests
1. Get ApprovalMatrix items where Category = trigger.Category AND Min ≤ Amount ≤ Max AND Active
2. Compose effectiveAmount = Amount + sum(Requests same Requester+Vendor last 7 days)   # split detection
3. If effectiveAmount > Budgets.Remaining → append CFO to approver list
4. For each stage in ApproverRoles:
     a. Resolve role → user (Office 365 Users: Manager / lookup table)
     b. If user = Requester → use user's manager
     c. If active Delegation → use delegate
     d. Start and wait for approval (adaptive card in Teams + Outlook)
        - Parallel branch: reminder after 24h, escalate after 48h (Do Until with timeout)
     e. Write ApprovalHistory row
     f. If Rejected → update Status = Rejected, notify requester, terminate
5. Update Requests.Status = Approved; notify Procurement; set CompletedOn
Error handling: Scope "Try/Catch" → on failure notify process owner with run URL
```

Power Apps form: `Patch()` to `Requests`, mandatory fields enforced with `DisplayMode` and `IsBlank()` checks,
status gallery filtered by `User().Email`.
