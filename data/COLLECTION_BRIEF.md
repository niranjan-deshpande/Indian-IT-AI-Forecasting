PROJECT ROOT: /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/0. Exploratory Analysis   (quote the path — it has spaces)

CONTEXT: We are running a feasibility pilot on whether public data can distinguish causes of recent headcount declines at large Indian IT-services firms (demand drop vs. lower labor needs from AI with/without price pass-through vs. work moving to client captive centers/subcontractors). Your job is ONLY data collection for one firm (or one period), from PRIMARY sources, with a source URL on every data point. Someone else does the analysis.

READ FIRST: data/SCHEMA.md in the project root. Follow it exactly (columns, metric vocabulary, cal_q mapping).

HARD RULES
- Primary sources only: company investor-relations fact sheets / data sheets / press releases / earnings releases / investor presentations / annual reports, SEC filings (10-K, 10-Q, 8-K, 20-F, 6-K via EDGAR), and stock-exchange filings of the company's own documents (BSE/NSE). Company-published earnings-call transcripts are acceptable for metrics only disclosed on calls (mark source_doc accordingly). News/aggregator sites (Moneycontrol, Screener, Macrotrends, etc.) are NOT data — you may use them only to cross-check, never as the source of a row.
- Never fill, interpolate, or compute missing values. If a value isn't disclosed, it's simply absent (or an empty-value row with a note if useful). Do not derive shares from levels or vice versa — record only what is reported. (Exception: none.)
- If a source needs a login or payment, skip it and log it in the NOTES file.
- Every row must have a working source_url that points to the specific document (PDF/HTML/EDGAR filing URL), not just a landing page, whenever possible.
- Do not treat LLM-generated summaries or analyst estimates as data.

HOW TO WORK
- Tools: curl (use a browser-like User-Agent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"), WebFetch/WebSearch (load via ToolSearch if deferred), pdftotext -layout (installed), Python 3 with pandas, pdfplumber, requests, bs4, openpyxl.
- For SEC EDGAR use UA "ndeshpande research ndeshpande@college.harvard.edu" and the JSON APIs (https://data.sec.gov/submissions/CIK##########.json, full-text search https://efts.sec.gov/LATEST/search-index?q=...). Stay under 10 requests/second.
- Do NOT use the in-app browser (mcp__Claude_Browser__*) or Claude in Chrome unless your firm-specific instructions explicitly allow it (other agents share it).
- Save downloaded source documents under data/sources/<firm>/ (keep original filenames or descriptive names). Save any extraction/parsing scripts under scripts/extract/<firm>_*.py so the extraction is reproducible (the script can read the local copies in data/sources/). Hand-transcribed values are acceptable when parsing is impractical, but then note `hand-entered` in notes.
- Multi-quarter tables (fact sheets often show 5 quarters) are efficient — but prefer to collect every quarterly document where feasible because restatements matter. Keep all vintages as separate rows (doc_date differs); the analyst will pick vintages.
- Sanity-check your output: headcount should move smoothly; segment shares should sum to ~100 per quarter; revenue should match across sources. Fix parsing errors. Spot-check at least 10 random values against the PDF text.
- Write your output to data/raw/<firm>.csv (schema) and data/raw/<firm>_NOTES.md (sources, skipped sources, coverage by metric with first/last quarter and gaps, definitional breaks with the quarter they occurred, judgment calls).
- Work efficiently but thoroughly. Priority order if time runs short: (1) revenue total USD + cc growth, headcount, utilization, attrition; (2) revenue shares/growth by vertical, geography, service line; (3) subcontracting cost, TCV/bookings, client buckets, fresher hiring, net additions; (4) AI disclosures, onsite/offshore mix, fixed-price mix.

FINAL REPLY (keep it under ~300 words): rows written, coverage by metric (first–last quarter, notable gaps), definitional breaks, blocked/paywalled sources, and any concerns about data quality.
