# User Stories by Release (JIRA)

## Release 1 — Revenue & Target (8 weeks)
| Key | Story | Acceptance criteria | Points |
|---|---|---|---|
| CPC-101 | As the CCO I want an executive summary of net revenue vs. target and LY so I see performance at a glance | Tiles for NR, target %, YoY; matches finance ledger ±0.5% | 8 |
| CPC-102 | As a regional head I want revenue by territory and customer so I can act on gaps | Drill region → territory → customer → invoice | 5 |
| CPC-103 | As a regional head I want to see only my region | RLS tested with 4 regional users | 5 |
| CPC-104 | As sales ops I want daily refresh by 07:00 | Refresh log shows success by 07:00 on 20 consecutive days | 3 |
| CPC-105 | As a user I want to export a visual to Excel with my security applied | Export contains only permitted rows | 2 |

## Release 2 — Margin (6 weeks)
| Key | Story | Acceptance criteria | Points |
|---|---|---|---|
| CPC-201 | As a finance controller I want a price-volume-mix-cost bridge vs. LY | Bridge sums exactly to total margin change | 8 |
| CPC-202 | As the CFO I want product and customer profitability rankings | Top/bottom 20 by margin % and value | 5 |
| CPC-203 | As a regional head I must not see margin | Margin pages hidden for non-finance roles | 3 |

## Release 3 — Pipeline & Forecast (6 weeks)
| Key | Story | Acceptance criteria | Points |
|---|---|---|---|
| CPC-301 | As a sales director I want pipeline by stage and age | Ageing buckets 0–30/31–60/61–90/90+ | 5 |
| CPC-302 | As FP&A I want forecast vs. actual by region | Variance % with RAG thresholds ±5/10% | 5 |
| CPC-303 | As a KAM I want an account page with orders, pipeline and history | All on one page; loads < 5 s | 8 |
