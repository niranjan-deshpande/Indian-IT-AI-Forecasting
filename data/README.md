# Shared firm data

The quarterly firm panel used by every stage of the project. Eight firms (TCS, Infosys, HCLTech, Wipro, Tech Mahindra, LTIMindtree, Cognizant, Accenture), 2015–2026 plus the GFC window 2007–2012, every value from a primary document with its URL.

| folder | what | built by |
|--|--|--|
| `raw/` | One long CSV per firm (`<firm>.csv`), every vintage kept, plus `<firm>_NOTES.md` on sources, coverage and definitional breaks. Schema below. | `scripts/extract/` (one set of scripts per firm) |
| `tidy/` | `panel_long.csv` (latest vintage), `core_quarterly.csv`, `yoy_metrics.csv` | `01_pilot/scripts/01_build_tidy.py` |
| `corrected/` | Audit-corrected panel (`*_corrected.csv`) and the final panel used by the note and later pages (`*_final.csv`), with `CHANGELOG.csv` | `01_pilot/scripts/audit/build_corrected.py`, `01_pilot/scripts/note/build_final_data.py` |
| `rebuilt/raw/` | LTIM raw file re-extracted with the fixed sign parser | `01_pilot/scripts/note/make_all.py --ltim` |
| `sources/` | Downloaded filings, transcripts and PDFs (≈7 GB). **Gitignored**; URLs are recorded in the data. Includes PLFS unit-level microdata in `sources/plfs/` (MoSPI data-access agreement: only aggregates may leave this folder). | collection agents, `scripts/extract/` |

Stage-specific data (probes, measurement rounds, chart inputs) live in each stage's `explore/` folder, not here.

The collection was done on 2026-09-27 by one agent per firm. The schema and rules those agents followed are kept below (formerly `SCHEMA.md` and `COLLECTION_BRIEF.md`).

## How the raw data were collected

**Hard rules**
- Primary sources only: company investor-relations fact sheets / data sheets / press releases / earnings releases / investor presentations / annual reports, SEC filings (10-K, 10-Q, 8-K, 20-F, 6-K via EDGAR), and stock-exchange filings of the company's own documents (BSE/NSE). Company-published earnings-call transcripts are acceptable for metrics only disclosed on calls (mark source_doc accordingly). News/aggregator sites (Moneycontrol, Screener, Macrotrends, etc.) are NOT data — you may use them only to cross-check, never as the source of a row.
- Never fill, interpolate, or compute missing values. If a value isn't disclosed, it's simply absent (or an empty-value row with a note if useful). Do not derive shares from levels or vice versa — record only what is reported. (Exception: none.)
- If a source needs a login or payment, skip it and log it in the NOTES file.
- Every row must have a working source_url that points to the specific document (PDF/HTML/EDGAR filing URL), not just a landing page, whenever possible.
- Do not treat LLM-generated summaries or analyst estimates as data.

**How to work**
- Tools: curl (use a browser-like User-Agent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"), WebFetch/WebSearch (load via ToolSearch if deferred), pdftotext -layout (installed), Python 3 with pandas, pdfplumber, requests, bs4, openpyxl.
- For SEC EDGAR use UA "ndeshpande research ndeshpande@college.harvard.edu" and the JSON APIs (https://data.sec.gov/submissions/CIK##########.json, full-text search https://efts.sec.gov/LATEST/search-index?q=...). Stay under 10 requests/second.
- Do NOT use the in-app browser (mcp__Claude_Browser__*) or Claude in Chrome unless your firm-specific instructions explicitly allow it (other agents share it).
- Save downloaded source documents under data/sources/<firm>/ (keep original filenames or descriptive names). Save any extraction/parsing scripts under scripts/extract/<firm>_*.py so the extraction is reproducible (the script can read the local copies in data/sources/). Hand-transcribed values are acceptable when parsing is impractical, but then note `hand-entered` in notes.
- Multi-quarter tables (fact sheets often show 5 quarters) are efficient — but prefer to collect every quarterly document where feasible because restatements matter. Keep all vintages as separate rows (doc_date differs); the analyst will pick vintages.
- Sanity-check your output: headcount should move smoothly; segment shares should sum to ~100 per quarter; revenue should match across sources. Fix parsing errors. Spot-check at least 10 random values against the PDF text.
- Write your output to data/raw/<firm>.csv (schema) and data/raw/<firm>_NOTES.md (sources, skipped sources, coverage by metric with first/last quarter and gaps, definitional breaks with the quarter they occurred, judgment calls).
- Work efficiently but thoroughly. Priority order if time runs short: (1) revenue total USD + cc growth, headcount, utilization, attrition; (2) revenue shares/growth by vertical, geography, service line; (3) subcontracting cost, TCV/bookings, client buckets, fresher hiring, net additions; (4) AI disclosures, onsite/offshore mix, fixed-price mix.

### Raw data schema (all files in `data/raw/`)

One CSV per firm: `data/raw/<firm>.csv` (firm ids: `tcs, infosys, hcltech, wipro, techm, ltim, cognizant, accenture`).
Long format, one row per (firm, fiscal quarter, metric, dimension, source document). UTF-8, comma-separated, quoted where needed.

| column | description |
|---|---|
| firm | firm id (see above) |
| fiscal_q | firm's own label, e.g. `Q1FY25` (Indian FY ends March; FY25 = Apr-2024..Mar-2025), `Q3FY24` for Accenture (FY ends Aug), `2024Q2` for Cognizant |
| period_end | quarter end date `YYYY-MM-DD` (e.g. 2024-06-30; Accenture 2024-11-30) |
| cal_q | calendar quarter the period is assigned to, `YYYYQn`. Indian & Cognizant: quarter containing period_end. Accenture: quarter containing period_end (Nov-30 → Q4, Feb-28 → Q1, May-31 → Q2, Aug-31 → Q3); the 1-month offset is logged in 01_pilot/REPORT.md (Appendix B) |
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

### Metric vocabulary (use these names; add new ones only if needed and list them in your notes file)

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

### Notes file
Each agent also writes `data/raw/<firm>_NOTES.md`:
1. Sources used (URL patterns), and any source skipped because it needed a login/payment or blocked access (log it).
2. Coverage summary: for each metric, first and last quarter covered, and gaps.
3. Definitional breaks (segment reorganizations with the quarter they occurred, M&A, headcount-definition changes, attrition-definition changes, restatements).
4. Any judgment calls made.
