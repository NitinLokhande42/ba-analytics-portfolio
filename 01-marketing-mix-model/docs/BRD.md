# Business Requirements Document — Marketing Mix Model & Budget Simulator

| Item | Detail |
|---|---|
| Sponsor | CMO and Head of FP&A |
| Stakeholders | Brand managers, digital lead, media agency, FP&A, data engineering |
| Version | 1.2 (signed off) |

## 1. Background
Annual marketing budget of ₹50 Cr is allocated by precedent. There is no shared, evidence-based view of channel
effectiveness, and finance challenges every increase.

## 2. Business objectives
| ID | Objective | Measure |
|---|---|---|
| BO-1 | Quantify revenue contribution of each channel | Contribution % with credible interval |
| BO-2 | Improve marketing ROI | ROI from 2.1x to ≥ 2.4x within one planning cycle |
| BO-3 | Enable evidence-based budget planning | Scenario simulator used in annual plan |

## 3. Scope
**In scope:** TV, digital (search, social, programmatic), print, radio, field activations; weekly national data; 3 years of history.
**Out of scope:** Creative quality scoring, regional models (phase 2), real-time bid optimisation.

## 4. Functional requirements
| ID | Requirement | Priority |
|---|---|---|
| FR-1 | Ingest weekly spend per channel from agency files and ad platforms into Snowflake | Must |
| FR-2 | Ingest weekly net revenue from ERP | Must |
| FR-3 | Model carry-over (adstock) and diminishing returns (saturation) per channel | Must |
| FR-4 | Report channel ROI and contribution with uncertainty bands | Must |
| FR-5 | Simulator: user sets total budget and per-channel min/max; tool returns optimal split and expected revenue | Must |
| FR-6 | Save, name and compare up to 5 scenarios | Should |
| FR-7 | Export scenario to Excel for the planning pack | Should |
| FR-8 | Refresh model quarterly with new data | Should |

## 5. Non-functional requirements
- Model fit: MAPE on hold-out ≤ 10%.
- Simulator returns a result in < 10 seconds.
- Access restricted to marketing leadership and FP&A (Power BI workspace security).

## 6. Assumptions & constraints
- Spend is reported consistently by agencies (excluding GST).
- No channel can move more than ±30% in one cycle (contract commitments).
- Price and promotion calendar provided by the category team.

## 7. Risks
| Risk | Mitigation |
|---|---|
| Correlated channel spend makes effects hard to separate | Informative priors agreed with marketing; sensitivity analysis |
| Stakeholders distrust a "black box" | Walk-through sessions, response curves shown, back-test vs. actuals |

## 8. Sign-off
CMO · Head of FP&A · Marketing Analytics Lead
