# Raw data schema (all files in `data/raw/`)

One CSV per firm: `data/raw/<firm>.csv` (firm ids: `tcs, infosys, hcltech, wipro, techm, ltim, cognizant, accenture`).
Long format, one row per (firm, fiscal quarter, metric, dimension, source document). UTF-8, comma-separated, quoted where needed.

| column | description |
|---|---|
| firm | firm id (see above) |
| fiscal_q | firm's own label, e.g. `Q1FY25` (Indian FY ends March; FY25 = Apr-2024..Mar-2025), `Q3FY24` for Accenture (FY ends Aug), `2024Q2` for Cognizant |
| period_end | quarter end date `YYYY-MM-DD` (e.g. 2024-06-30; Accenture 2024-11-30) |
| cal_q | calendar quarter the period is assigned to, `YYYYQn`. Indian & Cognizant: quarter containing period_end. Accenture: quarter containing period_end (Nov-30 → Q4, Feb-28 → Q1, May-31 → Q2, Aug-31 → Q3); the 1-month offset is logged in DECISIONS.md |
| metric | controlled vocabulary below |
| dimension | `total`, or the segment name exactly as the firm reports it (e.g. `BFSI`, `North America`, `Engineering and R&D Services`) |
| dim_type | `total`, `vertical`, `geography`, `service_line`, `client_bucket`, `other` |
| value | numeric. Leave EMPTY (and explain in notes) rather than guess. Never interpolate. |
| unit | `USD_mn`, `INR_cr`, `INR_mn`, `pct`, `count`, `USD_bn`, `ratio`, `text` |
| basis | `reported` (reported currency), `cc` (constant currency), `na` |
| period_type | `quarter` (default), `ltm`, `ytd`, `annual`, `point` (end-of-period stock, e.g. headcount) |
| source_url | direct URL of the primary document (PDF/HTML/EDGAR filing). REQUIRED on every row |
| source_doc | short human description, e.g. `TCS Q1FY25 fact sheet`, `Cognizant 10-Q Q2 2024` |
| source_loc | page / table name inside the document |
| doc_date | publication date of the source document (YYYY-MM-DD, approximate ok) — used to pick latest vintage when figures are restated |
| notes | definitional notes, restatement flags, anything odd |

## Metric vocabulary (use these names; add new ones only if needed and list them in your notes file)

Revenue
- `revenue` — total revenue (unit USD_mn or INR_cr/INR_mn; basis reported). Record USD where the firm reports USD. Indian firms reporting only INR (e.g. some periods), record INR.
- `revenue_growth_qoq` / `revenue_growth_yoy` — growth % (basis `cc` or `reported`) as reported by the firm (do not compute).
- `revenue_share` — % of total revenue by segment (dim_type vertical/geography/service_line).
- `segment_revenue` — segment revenue in currency, if reported in levels.
- `segment_growth_yoy` / `segment_growth_qoq` — segment growth % (basis cc or reported) as reported.

People
- `headcount` — total employees at period end (period_type point). Note in `notes` whether it includes subsidiaries/BPO/support staff and any definitional change.
- `net_additions` — as reported.
- `gross_additions`, `fresher_hires` (note whether quarterly/annual/campus offers).
- `attrition` — % ; note definition (LTM voluntary, annualized quarterly, IT services only, etc.).

Utilization / delivery
- `utilization_incl_trainees`, `utilization_excl_trainees` — % ; note definition (IT services only? offshore/onsite split?).
- `utilization_offshore`, `utilization_onsite` if reported separately.
- `effort_share_offshore` / `revenue_share_offshore` — onsite/offshore mix, if reported.
- `revenue_share_fixed_price` — fixed-price vs T&M mix, if reported.

Costs
- `subcontracting_cost` — currency level (quarterly) or `subcontracting_pct_rev` (% of revenue). Record whatever the primary doc reports.
- `employee_cost` — employee benefit expenses (currency), if easy.

Demand / deals
- `tcv` — total contract value of large deals / all deals as reported (note definition: "large deals", "total TCV", net new…).
- `bookings` — new bookings (Accenture), `book_to_bill` (Cognizant/others).
- `clients_bucket` — number of active clients by revenue bucket, dimension e.g. `USD100mn+`, `USD50mn+`, `USD20mn+`, `USD10mn+`, `USD5mn+`, `USD1mn+` (note whether LTM revenue).
- `active_clients` — total active clients.

AI
- `ai_disclosure` — any quantitative AI / GenAI revenue, bookings or deal disclosure (value numeric if possible, unit accordingly, text in notes).

## Notes file
Each agent also writes `data/raw/<firm>_NOTES.md`:
1. Sources used (URL patterns), and any source skipped because it needed a login/payment or blocked access (log it).
2. Coverage summary: for each metric, first and last quarter covered, and gaps.
3. Definitional breaks (segment reorganizations with the quarter they occurred, M&A, headcount-definition changes, attrition-definition changes, restatements).
4. Any judgment calls made.
