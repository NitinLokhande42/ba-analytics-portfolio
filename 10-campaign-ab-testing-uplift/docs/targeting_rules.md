# Targeting Rules for Future Campaigns

Uplift score refreshed monthly; rules implemented in the campaign tool as audience filters.

| Segment | Definition | Action |
|---|---|---|
| Persuadables | Predicted uplift ≥ threshold | **Send offer** |
| Sure things | High baseline conversion, uplift < threshold | No discount; standard newsletter only |
| Lost causes | Low baseline, uplift ≈ 0 | Exclude from paid channels |
| Do-not-disturb | Negative uplift | Suppress |

**Threshold:** contact when `uplift × average margin per conversion > cost per contact` (incl. discount leakage).

**Always keep a 10% random holdout** in every campaign to keep measuring true incrementality and retrain the model.

| Rule ID | Audience filter (pseudo) |
|---|---|
| T-1 | `uplift_score >= :threshold AND email_opt_in = TRUE` |
| T-2 | `uplift_score < 0 → add to suppression list` |
| T-3 | `random_bucket < 10 → holdout (no offer)` |
