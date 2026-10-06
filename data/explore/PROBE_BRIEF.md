PROJECT ROOT: /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/0. Exploratory Analysis  (quote the path)

CONTEXT: A completed pilot (read REPORT.md §1 and §6 in the project root, ~2 min) found that public firm data on Indian IT-services
firms cannot separate S1 (client demand/volume Q falls) from S3 (labor per unit a falls AND price per unit of output p falls).
Key identity: R = p·Q, billed effort = u·L = a·Q. So revenue per billed hour = p/a: rate cards and hours do NOT separate S1 from S3.
What CAN: (i) prices per unit of OUTPUT (fixed-price/managed-service pricing, output-based price indices), (ii) incidence of cuts
across tasks/occupations with different AI exposure, (iii) client-side output volumes, (iv) for S4 (work moving to clients'
captive centres/GCCs in India): affiliated vs unaffiliated trade, GCC headcount.
You are a FEASIBILITY PROBE for one candidate data source. Not a full collection. Be fast and precise.

RULES
- Primary/official sources only (statistical agencies, regulators, company filings). Consultancy/analyst estimates are not data
  (you may note they exist). If something needs login or payment, do not pay; record price/terms if visible and move on.
- Record a source URL for every number you save. Save small extracts only (CSV) under data/explore/<your topic>/.
  Save any script under data/explore/<your topic>/ too. Large raw downloads: keep only filtered extracts; delete the rest.
- Do not use the in-app browser or Chrome. Use curl (UA "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36
  (KHTML, like Gecko) Chrome/128.0 Safari/537.36"; for SEC/BLS/BEA APIs a UA with contact "ndeshpande research
  ndeshpande@college.harvard.edu"), WebFetch/WebSearch (load via ToolSearch), Python (pandas, requests, pdfplumber, openpyxl).
- The pilot's quarterly firm panel is data/tidy/yoy_metrics.csv and core_quarterly.csv (firm, cal_q, gR=YoY cc revenue growth
  log×100, gL=YoY headcount log×100, du, ...). Use it for validation where asked.

EVERY PROBE MUST REPORT (in data/explore/<topic>/FINDINGS.md, ≤450 words, plus your final reply ≤350 words):
 1. Access: URL(s), free/paid/login, format, frequency, first & last period available, publication lag.
 2. Level: firm / occupation / industry / country; which of the 8 firms (TCS, Infosys, HCLTech, Wipro, TechM, LTIMindtree,
    Cognizant, Accenture) are identifiable.
 3. Measurement: what exactly is measured, and does it map to p (per output), p/a (per hour), Q, a·Q, task incidence, or GCC share?
    Quote the methodology line that settles it.
 4. Noise (if a time series is obtained): YoY log-change ×100 series; over 2015–2022 excluding 2020Q2–2021Q2: residual s.d. about
    the mean, AR(1) coefficient, number of observations. And the 2023–2026 path (mean YoY vs pre-2023 mean).
 5. Predicted sign under S1, S2, S3, S4 (be explicit about assumptions), and the main confound.
 6. Verdict: worth including in a full project? (yes / conditional / no) and cost in RA-days.
