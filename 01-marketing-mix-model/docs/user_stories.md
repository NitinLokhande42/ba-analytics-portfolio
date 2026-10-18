# User Stories — Budget Simulator

### US-01 View channel ROI
**As a** marketing manager **I want** to see ROI per channel with a range **so that** I know which channels are most efficient and how certain we are.
- **Given** the latest model run **when** I open the ROI page **then** I see mean ROI and 90% credible interval for every channel.
- Channels are sorted by mean ROI, highest first.

### US-02 See response curves
**As a** brand manager **I want** to see how revenue responds to more spend in my channel **so that** I know where saturation starts.
- Curve shows expected incremental revenue from 0% to 200% of current spend.
- Current spend point is marked on the curve.

### US-03 Run a budget scenario
**As a** marketing director **I want** to enter a total budget and min/max per channel **so that** I get the revenue-maximising split.
- **Given** a total budget and constraints **when** I click *Optimise* **then** I get recommended spend per channel and expected revenue within 10 seconds.
- If constraints are infeasible (sum of minimums exceeds total) a clear error message is shown.

### US-04 Compare scenarios
**As an** FP&A analyst **I want** to save scenarios and compare them side by side **so that** I can present options to leadership.
- Up to 5 named scenarios saved per user.
- Comparison shows spend, revenue and ROI deltas versus the current plan.

### US-05 Export plan
**As a** marketing director **I want** to export the chosen scenario to Excel **so that** it can go into the annual planning pack.
- Exported values match on-screen values to the rupee.

### US-06 Model refresh
**As a** marketing analytics lead **I want** the model refreshed each quarter **so that** recommendations stay current.
- Refresh log shows date, data range and hold-out MAPE.
