# Pilot vs. Control Design

| Element | Design |
|---|---|
| Unit | Region (all territories in it) |
| Pilot | 2 regions using the new segmentation and call plan |
| Control | 2 regions matched on sales size, growth trend, specialty mix, rep tenure |
| Duration | 3 months baseline + 6 months pilot |
| Primary metric | Secondary sales to priority-segment doctors' catchment (₹) |
| Secondary metrics | Call-plan adherence, calls per rep, share in GROW doctors |
| Analysis | Difference-in-differences: (pilot post − pilot pre) − (control post − control pre); territory-level regression with region and month fixed effects |
| Guardrails | Total region sales must not fall; no change to incentive plan during pilot |
| Decision rule | Scale nationally if uplift ≥ 5% with 90% confidence |

**Threats to validity and mitigations:** regional seasonality (matched control), new launches (excluded from metric), rep attrition (tracked, sensitivity analysis excluding vacant territories).
