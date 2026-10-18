# Business Rules

## Workload
| Account tier | Visits / year | Minutes / visit |
|---|---|---|
| A | 24 | 60 |
| B | 12 | 45 |
| C | 4 | 30 |

`workload_hours = visits × minutes / 60 + visits × travel_minutes / 60 + 2h admin per account`

## Territory rules
- TR-1 Imbalance = (territory workload − average) ÷ average; target band ±15%.
- TR-2 Top-10 revenue accounts of each rep are locked.
- TR-3 Moves only between adjacent territories (centroid distance below threshold).
- TR-4 Maximum 20% of a territory's accounts move in one realignment.

## Incentive plan
| Rule | Definition |
|---|---|
| IP-1 Target incentive | 20% of base salary at 100% attainment |
| IP-2 Threshold | No payout below 80% attainment |
| IP-3 Payout curve | 80–100%: linear 50% → 100% of target incentive; 100–120%: accelerator 2× slope; above 120%: capped at 140% of target incentive |
| IP-4 Split accounts | Revenue credited by agreed split %, must sum to 100% |
| IP-5 Mid-period transfer | Attainment calculated on pro-rated target for days in territory |
| IP-6 Returns | Credit reversed in the month of return; can make monthly credit negative, quarter floored at 0 payout |
| IP-7 New hires | Guaranteed 100% of target incentive for first full quarter |
| IP-8 Leavers | No payout for quarter if resigned before quarter end (per HR policy) |
| IP-9 Rounding | Payout rounded to nearest ₹ at quarter level only |
