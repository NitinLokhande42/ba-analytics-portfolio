# Test Plan (pre-registered)

| Item | Specification |
|---|---|
| Hypothesis H1 | The offer increases 14-day conversion versus no offer |
| H0 | No difference in conversion between treatment and holdout |
| Unit | Customer (randomised by hash of customer_id) |
| Split | 50% treatment / 50% holdout |
| Primary metric | 14-day conversion rate |
| Secondary | Revenue per customer, discount cost, incremental margin |
| Guardrails | Unsubscribe rate ≤ +0.2 pts; complaint rate unchanged |
| Minimum detectable effect | +1.0 pt absolute on a ~8% baseline |
| α / power | 0.05 two-sided / 80% |
| Sample size | ~12,000 per arm (see `src/ab_test.py`) |
| Duration | Send + 14-day window; no early stopping |
| Decision rule | Scale if lift > 0 with p < 0.05 **and** incremental margin > campaign cost |

**Avoiding common errors:** no peeking before the window closes; one primary metric; segment results treated as
exploratory unless pre-specified.
