# Randomized Retention Test

| Element | Design |
|---|---|
| Population | Customers scored HIGH or MEDIUM risk at test start |
| Randomisation | Customer-level, 50/50, stratified by tier and revenue band (seeded hash of customer_id) |
| Treatment | Retention workflow |
| Control | Business as usual (reactive only) |
| Primary metric | 90-day retention |
| Secondary | Revenue retained, offer cost, CSAT |
| Sample size | Baseline retention in risk tiers ≈ 75%; to detect +5 pts with 80% power at α = 0.05 needs ~1,100 per arm |
| Duration | 90-day outcome window after contact |
| Guardrails | Discount cost per save ≤ 20% of annual revenue; CSAT not lower than control |

**Scaling the result:** uplift in the targeted tiers × tier size ÷ total base = portfolio-level retention points.
