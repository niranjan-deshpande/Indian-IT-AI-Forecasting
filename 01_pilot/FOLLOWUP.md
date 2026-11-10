# Pilot follow-up and final pass (2026-10-05)

*Working record of the two rounds between the pilot report (`01_pilot/REPORT.md`) and the research note (`01_pilot/note_text.md` → `docs/index.html`). Merged on 2026-11-09 from four files:*
- *Part 1. Summary of the follow-up tasks (formerly `FOLLOWUP_SUMMARY.md`).*
- *Part 2. Data audit, follow-up Task 1 (formerly `audit_report.md`).*
- *Part 3. Final pass before the write-up (formerly `FINAL_PASS_SUMMARY.md`).*
- *Part 4. Inputs for the research note (formerly `note_inputs.md`).*

*Date of all four parts: 2026-10-05. The repo paths quoted inside them were updated when the repo was reorganised.*

The repo's data are clean apart from a few errors, and none of those errors change the pilot's main numbers. No public source measures sector-level price growth (g_p) directly. The pilot's conclusion that S1 and S3 cannot be separated therefore stands.

---

## Part 1. Summary of the follow-up tasks

### How the work was done

- **Setup.** I read the pilot's write-ups, data schema, build scripts and earlier probe folders first, and confirmed web access.
- **Parallel work.** Tasks 1, 3 and 4 ran in parallel across five agents. Task 1 and Task 3 were each split in two. Task 2 ran after Task 1, on the corrected data.
- **Rules followed.**
  - No existing data file, script or write-up was edited. The simulation code was not touched. All outputs are new files.
  - Every outside number carries a citation and a label: measured, estimated or commentary.
- **My own checks.** I re-checked a sample of the agents' claims against the sources myself:
  - three earnings-call quotes;
  - Infosys's FY2020 billed person-months (live 20-F);
  - TCS's subcontracting figures (fact sheet);
  - the ISG unit-price statement (live page).
- **Problems along the way.**
  - The agents couldn't write `.md` files, so I saved their reports myself: `01_pilot/audit/findings_1a.md` and `01_pilot/audit/findings_1b.md`.
  - The session hit its 200-query web-search limit. Some searches were left undone; they are listed under Open questions.

### Task 1: Data audit

See Part 2, which is the full audit write-up (spot-check, errors found, currency and units, fiscal-year alignment, the "missing" 2023, headcount definitions, structural breaks, corrections).

### Task 2: Graphs (`01_pilot/figures/task2/`)

- `01_pilot/scripts/08_task2_graphs.py` regenerates all eight figures with one command: `cd 01_pilot/scripts && python 08_task2_graphs.py`.
- **Figures:**
  - revenue growth in USD;
  - constant-currency revenue growth;
  - headcount growth;
  - revenue per employee;
  - utilization change;
  - the residual g(R/L) − g(u);
  - the Indian-minus-Accenture gap;
  - the 8-quarter rolling correlation.

  The first six each have an annual and a quarterly panel.
- **What each figure shows:** the six firms, both comparators, and both a simple and a revenue-weighted Indian average.
  - **Weighting barely matters after 2023:** the two averages are within ±0.35 pp. Single quarters can differ by up to about 7 pp.
- **Markers:**
  - vertical lines at 2022 and 2023Q1;
  - shading for 2008–09 and COVID;
  - the points where TCS (2015Q4) and HCLTech (2019Q1) stop reporting utilization.
- Each plotted line is also saved as a CSV.
- **One choice differs from the pilot:** pre-merger LTI and Mindtree count as one entity in the average, not two.
- **New result.** The rolling correlation with Accenture is high only in windows covering 2020–24. For revenue it is −0.08 in 2019Q4, 0.96 in 2022Q4 and −0.05 in 2026Q2. This supports the audit's point that the pre-2023 correlation reflects one episode.

### Task 3: Price data (`01_pilot/evidence/price_data.md`, `01_pilot/evidence/price_calls_timeline.md`)

**Main conclusion: no public source measures g_p for Indian IT services in any period since 2015.**

#### Official price indices

- **US.**
  - BLS has never published a producer price index for computer systems design services.
  - BEA's software price index is modelled from input costs plus an assumed productivity rate.
  - BEA's import price for computer services is built from US domestic indices.
- **UK, EU and Japan.** Their indices price hourly rates or revenue per person-month. That measures price per unit of *labor*, not per unit of *work*, and covers domestic sellers only.
- **India.** No IT services price index exists. The national accounts deflate IT output with goods or consumer price indices.

#### Firm disclosures (`01_pilot/audit/price_firm_disclosures.csv`, 434 rows, each read from a document)

- **Infosys reported billed person-months and revenue per person-month in its 20-F every year from FY2003 to FY2020.** This gives billed effort directly, but not price.
  - The figures suggest Infosys's price growth was at most about −1% to −2% a year in FY15–17, and about 0% in FY18–20.
  - That holds only *if* labor per unit of work didn't rise. The bound is the agent's inference, not a sourced figure.
- Wipro disclosed volume vs price only for FY09–FY12.
- LTI disclosed billed person-months until 2022.
- TCS never disclosed pricing.
- Accenture's "pricing" means contract margin, not price.

#### Analyst estimates

These are labelled estimated; some are secondhand via news reports.

- **Kotak:** about 3–3.5% a year of AI-led revenue deflation through FY28.
- **Jefferies:** about 20% over 2025–30.
- These figures *assume* clients get the savings, so they can't be used to test S3.

#### Advisory firms

- **ISG** reports that contracted unit prices in managed-services deals historically fell 10–20% by year two of a contract. It says this has recently "doubled or even tripled". This is real price data, but it covers a narrow, mostly infrastructure slice. I verified the quote.
- **Everest Group, Gartner and HfS:** what is public is mostly per-FTE rates or paywalled.

#### Earnings calls

- **Coverage:** 389 verbatim management statements from 183 transcripts, all eight firms, 2021–2026. Only TCS's Q4FY23 call is missing.
- **Timeline:**
  - 2021–22: rate-card increases.
  - Mid-2023: "no price expansion".
  - 2023–24: pricing "stable".
  - 2025: explicit pass-through of AI savings (LTIMindtree, TCS, Wipro, Infosys).
  - 2026: quantified. HCLTech cites 2–3% a year of portfolio deflation and "$100 million deal … maybe 80 million"; LTIMindtree cites about 15% less for the same scope.
- **How much weight to give it.** This is commentary, not measured prices, and many numbers are illustrative or forward-looking.
- **Reading.** Taken literally, it fits demand weakness (S1) in 2023–24, with S3-type pass-through starting only in 2025.

### Task 4: Other data that could separate the scenarios (`01_pilot/evidence/discriminating_data.md`)

#### Subcontracting

Computed from the firms' filings by `01_pilot/scripts/audit/subcontracting_series.py`.

- Subcontracting cost as a share of revenue **fell at all six Indian firms in FY24**, by 1.3–2.9 pp. TCS went from 9.5% to 6.6%; I checked TCS against its fact sheet.
- It was flat to down in FY25 and rose slightly in FY26, but stays below FY22–23 levels.
- So work did not shift from employees to contractors (the subcontractor version of S4).

#### What exists, and how far it helps

| Source | Helps with | What it shows |
|---|---|---|
| RBI census of foreign-owned companies' exports | S1 vs S4 | Exports rose from ₹6.54 to ₹8.45 lakh crore (FY22 → FY23). Foreign-owned vendors are included too |
| BEA data on US-owned affiliates in India | S1 vs S4 | 893k employed in professional services in 2023 |
| Naukri JobSpeak | S1 vs S4 | Now reports GCC postings next to IT services (Sep 2026: GCC +4%, IT −4%) |
| Firm client counts; onsite/offshore mix | Weak | The offshore share is rising, which leans weakly against S4 |
| Fresher hiring | Weak | Fell sharply after FY23; confounded by the earlier hiring boom |
| Anything public | S1 vs S3 | Nothing separates them |

#### Not as described

- Nasscom-Zinnov GCC headcounts are restated consultancy estimates. They can't be chained into a trend.
- EPFO payroll data has only a coarse IT category and no ownership split.
- The RBI software-exports survey has no foreign-owned or GCC category.
- USCIS L-1 data by employer stops at FY2019.
- Cognizant and Accenture don't disclose a usable subcontracting figure.
- The repo's RBI file is missing FY2017-18, which does exist.

#### Not collected publicly anywhere

Each item is listed in `01_pilot/evidence/discriminating_data.md` with the scenario pair it would separate.

- output-based prices per unit of scope;
- role-level headcount by firm;
- client-side work volumes;
- GCC headcount by parent company.

### Every change to the data

Listed in Part 2, "Corrections" (7 corrections applied in `data/corrected/`, 57 issues flagged but not changed; only 6 growth values differ and the pilot's outputs are unchanged).

### Open questions

1. **LTI counting.** Should the pilot's baseline row and averages count the LTI business once? That changes baseline headcount growth from 11.8% to 9.9%.
2. **Acquisitions.** Should inorganic growth be adjusted for, or kept as a caveat? Accenture's acquisitions could explain much of the recent gap between it and the Indian firms.
3. **HCLTech divestiture.** Adjust revenue as well as headcount, or adjust neither?
4. **Wipro.** Should the quarters distorted by the FY17 perimeter change and the Q2FY19 staff transfer be dropped?
5. **Script bugs.** Should the parser and attrition bugs be fixed in the original extraction and build scripts? So far they are corrected only downstream.
6. **Accenture Q4FY26.** It was released 1 Oct and isn't in the data yet. Should it be added?
7. **Unfinished searches,** stopped by the search limit:
   - Mphasis, Hexaware and Persistent filings;
   - an RBI price index;
   - later rounds of the RBI foreign-subsidiary census.

   These can be continued by direct fetch.

One figure was verified only by an agent: Kotak's 3–3.5% via ANI. The page returned 403 when I re-fetched it.

---

## Part 2. Data audit (follow-up Task 1)

*Date: 2026-10-05. Detailed findings: `01_pilot/audit/findings_1a.md` (items 1, 2, 5) and `01_pilot/audit/findings_1b.md` (items 3, 4, 6, pipeline). Row-level evidence: `01_pilot/audit/*.csv`. No existing file was modified. Corrected data are written to new files in `data/corrected/`.*

### Summary

1. **Spot-check: 30 of 30 values match the primary documents.** 18 were checked against freshly downloaded copies, which were byte- or text-identical to the cached files.
   - Targeted tests outside the sample found **two parser bugs**:
     - Mindtree and LTI negatives printed as "(x.x)%" were stored as positive: 22 cells, 2 of which reach a core column.
     - Cognizant attrition definitions were picked arbitrarily in 2 quarters.
   - None of the errors touch `gR` (cc revenue growth), `gL` or `du` in 2015–2026. **The pilot's Part 2–4 numbers are unchanged by the corrections.**
2. **Currency and units are consistent from 2015 on.** Revenue is reported USD throughout. cc growth is never mixed with reported growth: `gR` has no fallback. Three problems:
   - Accenture FY18 `gR_usd` was inflated by about 3.5 pp by an ASC 606 basis mix. Corrected.
   - Two GFC-era base values were not comparable. Set to missing.
   - Some GFC-era "reported" growth is INR growth. Flagged.
3. **Fiscal-year alignment was not wrong.** Every `cal_q` matches its `period_end`. Mapping Accenture's quarter ending Nov-30 to calendar Q4 is the best alignment available (2 of 3 months overlap).
   - The comparator correlations reproduce exactly (0.90 / 0.58 revenue, 0.83 / 0.33 headcount). Across 11 alignment and aggregation variants they move by about ±0.1–0.2; the cleanest variant gives 0.91 / 0.60 / 0.81 / 0.32.
   - **The bigger issue is interpretation.** Over 2016Q1–2020Q1 the correlations are only 0.13 (revenue) and −0.09 (headcount). The pre-2023 figure comes from the 2021–22 boom. With an effective n of about 5, 0.90 and 0.58 cannot be told apart statistically.
4. **2023 is not missing; it is split across rows and mislabelled.** Q1–Q3FY23 sit in "2015–22" and Q4FY23 in "FY24 slowdown". The labels mix calendar and fiscal years. **"FY25–27" contains 9 quarters: FY25 ×4, FY26 ×4, FY27 ×1 (Q1FY27).**
   - The "2015–22" row also counts the LTI business up to three times (LTI, Mindtree, LTIMindtree). With one LTI entity, baseline headcount growth is 9.9%, not 11.8%.
5. **Headcount excludes contractors at TCS, Infosys, HCLTech and LTIMindtree.** At these four, the fact-sheet figure equals the BRSR "Permanent" row.
   - Tech Mahindra includes directly contracted staff and non-integrated subsidiaries.
   - Wipro's pre-FY18 "Head Count" included contractors and retainers. The repo correctly uses only the later "Employee Count" series. Wipro's current count is not reconciled to its own BRSR.
   - Trainees are explicitly included only at Infosys; at the other firms it is not stated.
6. **Structural-break handling is adequate for headcount but incomplete elsewhere:**
   - The LTI business is counted multiple times in the REPORT's baseline row.
   - Inorganic growth is adjusted nowhere (Belcan, Accenture acquisitions, HCLTech–IBM, Wipro–Alight).
   - The HCLTech divestiture is removed from headcount but not from revenue.
   - Two Wipro breaks were not logged: the ISRE perimeter (FY17 base) and the Alight transfer (Q2FY19, about 9,000 staff).

### 1. Spot-check (`01_pilot/audit/spotcheck_1a.csv`)

**Design.** Seed 20261005. 26 cells were drawn from the vintages actually used (`panel_long.csv`, 2015Q2 onward), stratified across all 8 firms plus LTI and Mindtree, and across six metric groups: revenue USD, headcount, utilization, attrition, vertical share and cc growth. 4 more cells came from the GFC file.

**Results.**

| metric group | n | match | checked against live or Wayback copy |
|--|--|--|--|
| revenue USD | 6 | 6 | 5 |
| headcount | 7 | 7 | 4 |
| utilization | 7 | 7 | 3 |
| attrition | 5 | 5 | 2 |
| vertical share | 3 | 3 | 0 |
| cc YoY growth | 3 | 3 | 3 |
| **total** | **30** | **30** | **18** |

- Each value was read from the document itself, not from the CSV. The table with value in repo, value in source, source location and result is `01_pilot/audit/spotcheck_1a.csv`.
- **Propagation:** 27 of the cells feed `core_quarterly.csv`, and all arrive unchanged. The one exception is a deliberate preference for Cognizant's Tech Services attrition series.
- **Coverage gap:** TCS 2015+ fact sheets could be checked only against the local cache, because tcs.com returns 403 and Wayback rate-limited.

**Systematic problems found by targeted tests** (rows T01–T08):
- **Sign loss for negatives printed as "(x.x)%".**
  - Mindtree: 16 cells. Two of them are total YoY growth in Q2FY21 and Q3FY21, which feed core `rev_rep_yoy`.
  - LTI: 6 cells (Q1FY18 segment growth), found by Task 1b's scan of 1,980 positive rows against the PDFs.
  - Cause: `parse_num` in `scripts/extract/ltim_parse_tables.py`. LTIM rows are unaffected.
  - Because Mindtree has only one cc-growth quarter, `gR` is unaffected.
- **Cognizant attrition 2021Q2–Q3.** `pick()` chose quarterly-annualized rates (29, 33) where the neighbouring quarters use TTM (18, 24). It is the only ambiguous pick in any core column.

### 2. Currency and units (`01_pilot/audit/findings_1a.md` §2)

- **Revenue USD:**
  - Reported USD for every firm-quarter from 2015.
  - Wipro is the IT Services segment only, and 2007–12 is missing.
  - TCS 2007Q1 is an INR convenience translation at Rs 43.47 per USD: set to missing.
  - Accenture FY18 quarters come from the ASC 606 restated vintage, while FY17 is on the old net-revenue basis. That inflates `gR_usd` for 2017Q4–2018Q3 by 3.3–3.7 pp. Corrected using the like-for-like growth printed in the FY18 releases.
- **Constant currency:**
  - Every `rev_cc_yoy` value comes from a `basis=cc` row. `gR` is cc only and missing elsewhere: it never falls back to USD growth (DECISIONS D18).
  - Infosys, Wipro, Cognizant and Accenture all define cc as current-period revenue at prior-period FX rates. Accenture calls it "local currency" and prints whole percents, so there is ±0.5 pp of rounding.
  - TCS, HCLTech, TechM and LTIM print no definition in the documents checked.
- **Mislabelled basis:** GFC-era `rev_rep_yoy` for TCS (2007Q1–2010Q2) and TechM (2007–12) is INR growth. Flagged; it is not used in Parts 2–4.
- **Units:**
  - Revenue, headcount, utilization and TCV are consistent once the build script's conversions are applied (INR crore→mn, USD bn→mn).
  - TCS `subcon` is USD, unlike the other firms (INR). Its share uses a USD denominator, so the ratio is still correct.
- **Utilization definitions differ by firm** (including vs excluding trainees, offshore vs blended). The audit confirms that only within-firm changes (`du`) are used.

### 3. Fiscal-year alignment (`01_pilot/audit/findings_1b.md` §3; `01_pilot/audit/fiscal_calendar.csv`, `comparator_corr_variants.csv`)

| firm | FY end | quarter ends |
|--|--|--|
| TCS, Infosys, Wipro, TechM, LTIM/LTI/Mindtree | 31 Mar | Jun, Sep, Dec, Mar |
| HCLTech | 30 Jun to FY15; FY16 = 9 months (Jul-15 to Mar-16); 31 Mar from FY17 | — |
| Accenture | 31 Aug | Nov, Feb, May, Aug |
| Cognizant | 31 Dec | Mar, Jun, Sep, Dec |

Each row is cited to a primary filing in `fiscal_calendar.csv`.

**Mapping checks.**
- `cal_q` is the calendar quarter containing `period_end` for every firm. Checks found 0 inconsistencies, 0 duplicates, and no holes at HCLTech's transition year.
- The pilot uses the firm-reported same-fiscal-quarter cc growth, and computes other growth as 4 calendar quarters back. The two coincide.

**Comparator correlations, Indian aggregate vs Accenture** (pre = 2016Q1–2022Q4 excluding COVID quarters; post = 2023Q1–2026Q2).

| variant | revenue pre | revenue post | headcount pre | headcount post |
|--|--|--|--|--|
| pilot (median; Nov→Q4) | 0.90 | 0.58 | 0.83 | 0.33 |
| Accenture Nov→next Q1 (0 months overlap) | 0.87 | 0.60 | 0.79 | 0.41 |
| Accenture Nov→Q3 (1 month overlap) | 0.84 | 0.42 | 0.69 | 0.12 |
| month-weighted Indian (⅔ t + ⅓ t−1) | 0.91 | 0.60 | 0.80 | 0.32 |
| mean instead of median | 0.94 | 0.64 | 0.83 | 0.36 |
| revenue-weighted mean | 0.90 | 0.54 | 0.79 | 0.44 |
| annual, calendar year (n = 5 / 3) | 0.94 | −0.51 | 0.88 | −0.24 |
| clean (no triple count, month-weighted) | 0.91 | 0.60 | 0.81 | 0.32 |
| *pilot set, 2016Q1–2020Q1 only* | *0.13* | — | *−0.09* | — |

**Verdict.**
- The periods were **not misaligned**, so the headline figures do not need to change.
- They are fragile, however:
  - The pre-2023 correlation is driven by the single 2021–22 boom-and-bust.
  - Within FY25–27 alone the correlations are 0.05 (revenue) and −0.10 (headcount).
  - The 95% confidence intervals overlap almost completely.
  - Task 2's 8-quarter rolling correlation shows the same thing: it is high only in windows that span 2020–24 (−0.08 in 2019Q4, 0.96 in 2022Q4, −0.05 in 2026Q2 for revenue).
- **The FY25–27 growth gap** (Indian minus Accenture, −2.4 to −2.9 pp for revenue) overlaps with Accenture's guided inorganic growth of "a bit more than 3%" in FY25 and about 1.5% in FY26. That is guidance, not realized growth; it comes from the Q4FY24, Q1FY25 and Q4FY25 calls. Growth is not adjusted for acquisitions in any series.

### 4. The "missing" 2023 (`01_pilot/audit/findings_1b.md` §4; `episodes_relabelled.csv`, `episodes_fiscal.csv`)

| REPORT row | calendar quarters | Indian FY quarters | quarters per FY |
|--|--|--|--|
| 2015–22 (ex-COVID) | 2015Q2–2022Q4, excl. 2020Q2–21Q2 | Q1FY16–Q3FY23 | FY23: 3 |
| pre-COVID "2015–19" | 2015Q2–**2020Q1** | Q1FY16–Q4FY20 | — |
| COVID | 2020Q2–Q4 | Q1–Q3FY21 | — |
| "FY24 slowdown" | 2023Q1–2024Q1 | **Q4FY23**–Q4FY24 | FY23: 1, FY24: 4 |
| "FY25–27" | 2024Q2–2026Q2 | Q1FY25–Q1FY27 | FY25: 4, FY26: 4, **FY27: 1** |

- **FY23 is split 3 + 1.** Calendar-year labels ("2015–22") and fiscal-year labels ("FY24") are mixed in one table.
- **Gaps and labels:** 2021Q1–Q2 fall in no row. The "2015–19" row actually runs to 2020Q1.
- **Latest quarter:** every firm ends at 2026Q2. Accenture's Q4FY26, released 1 Oct 2026, is not yet in the data.
- **Indian fiscal-year windows** (one LTI entity):
  - **FY23 on its own is the tail of the boom:** revenue +13.7%, headcount +14.3%.
  - **FY24 is sharper than the REPORT row:** headcount −3.6% against −1.8%, and revenue per employee +4.4%.
  - **Later years:** FY25 revenue +2.6% and headcount +0.1%; FY26 +1.4% and +1.2%.
- **No saved script produces the REPORT's 2015–22 and pre-COVID rows.** They reproduce only as a mean of firm-means over 8 Indian entities, which counts the LTI business up to three times. That is why revenue per employee (0.9) ≠ revenue − headcount (12.2 − 11.8).
- **Rows recomputed with one LTI entity:**
  - 2015–22: revenue 11.7, headcount 9.9, revenue per employee 1.0, Δutilization 0.3, residual 2.1.
  - pre-COVID: 9.5 / 6.7 / 1.8 / 0.9 / 1.8.
  - The FY24 and FY25–27 rows are unchanged.

### 5. Headcount definitions (`01_pilot/audit/findings_1a.md` §5)

| firm | trainees | contractors / subcontractors | changes over sample |
|--|--|--|--|
| TCS | not stated | **excluded**. Fact sheet 607,979 = BRSR permanent; 28,854 "other than permanent" (IAR 2024-25, p.131) | 2009Q1: e-Serve and Diligenta added (GFC window). None 2015–26 |
| Infosys | **included**. 20-F FY2016 and FY2026: "…including trainees" | **excluded**. 317,240 = BRSR permanent; 23,447 contractors excluded (IAR 2023-24, p.159) | wording only; trainee sub-line dropped after Q4FY18 |
| HCLTech | not stated | **excluded**. 223,420 = BRSR permanent = 167,316 company + 56,104 subsidiaries (AR 2024-25, pp.130, 187) | Q1FY25 divestiture of 7,398, correctly adjusted in `gL` |
| Wipro | not stated | pre-FY18 "Head Count" **included** contractors and retainers (181,482 vs 165,481 employees at Q4FY17; AR 2016-17, p.52). Current employee count 233,346 lies between BRSR permanent 225,306 and BRSR total 235,415: **unreconciled** | Q4FY17 switch (handled: the repo uses the employee count from Q4FY16). **Unlogged:** ISRE perimeter restated only back to Q1FY18 (biases `gL` 2017Q2–18Q1 by about −3 pp); Alight transfer of about 9,000 staff in Q2FY19. Q2FY25 restatement of Q3'24–Q1'25 (corrected values are in use) |
| TechM | not stated | **included** if contracted directly. 148,731 = BRSR 139,271 (incl. 7,827 contractors) + 9,460 non-integrated subsidiaries (IAR FY25, p.125) | label changes only |
| LTIMindtree | not stated | **excluded**. 84,307 permanent; 3,782 "Non-FTE Subcontractors" excluded (FY25 BRSR p.3) | merger restatement 1,858–2,335 below LTI + Mindtree, unexplained (no splice used) |
| Cognizant | not stated | excluded implicitly: "subcontractor usage has been immaterial" (10-K FY2025) | TriZetto (2014Q4), Belcan (2024Q3) |
| Accenture | not stated | not stated | none found |

**Implication.** The Indian headcount series measure permanent employees, so a shift from employees to contractors would show up as falling L. Task 4's subcontracting-cost series rules that out for FY24–FY26: subcontracting as a share of revenue *fell* at all six firms in FY24 (`01_pilot/evidence/discriminating_data.md` §b).

### 6. Structural breaks (`01_pilot/audit/findings_1b.md` §6)

| break | handling in pilot | verdict |
|--|--|--|
| LTI–Mindtree merger | no splice; LTI and Mindtree until 2022Q3, LTIM after; Parts 3–4 drop LTIM before 2022Q4 | correct in the model. **REPORT baseline row counts the LTI business up to three times.** The comparator median includes all three in 2022Q3 (no material effect) |
| HCLTech FY change | mapped through `period_end` | correct |
| HCLTech divestiture (Q1FY25) | headcount base reduced by 7,398 for 4 quarters | correct for `gL`. **Revenue not adjusted**, so `gRPE` is biased down 2024Q3–2025Q2 |
| Wipro Q4FY17 definition | new series only | correct |
| Wipro ISRE perimeter; Alight transfer | not logged | flagged |
| Inorganic growth (Belcan ~4 pp; Accenture acquisitions; HCLTech–IBM 2019; Capco; TriZetto) | not adjusted (D12) | biases the comparator gap and the baseline. Flagged, not corrected |
| Accenture ASC 606 | cc growth as reported | `gR` fine; `gR_usd` FY18 corrected |

### Corrections

Applied by `01_pilot/scripts/audit/build_corrected.py`. Every row is logged in `data/corrected/CHANGELOG.csv`, and every change was verified against a primary document.

| # | firm | quarters | field | old → new | reason |
|--|--|--|--|--|--|
| 1 | Mindtree | 16 cells: Q2–Q3FY17 QoQ, Q2–Q3FY21 YoY, 12 segment cells FY22–23 | raw growth rates | +x → −x | parser lost "(x.x)%" sign |
| 2 | Mindtree | 2020Q3, 2020Q4 | core `rev_rep_yoy` | 3.7 → −3.7; 0.4 → −0.4 | same bug, propagated to core |
| 3 | LTI | Q1FY18, 6 segment cells | raw growth rates | +x → −x | same bug |
| 4 | Cognizant | 2021Q2, 2021Q3 | core `attrition` | 29 → 18; 33 → 24 | definition mix (quarterly-annualized vs TTM) |
| 5 | TCS | 2007Q1 | core `rev_usd` | 1,183.9 → missing | INR convenience translation; removes the 2008Q1 `gR_usd` (24.8) |
| 6 | Wipro | 2007Q1 | core `headcount` | 67,818 → missing | old perimeter; removes the 2008Q1 `gL` (+34.3) |
| 7 | Accenture | 2017Q4–2018Q3 | yoy `gR_usd` | 14.91 / 17.51 / 18.74 / 13.80 → 11.18 / 14.19 / 15.13 / 10.37 | ASC 606 vintage mix; like-for-like net revenue growth from the FY18 releases |

**Flagged, not changed (57 rows):**
- Wipro ISRE perimeter (2017Q2–2018Q1)
- Wipro Alight (2018Q3)
- TCS e-Serve (2009Q1)
- GFC-era INR growth labelled "reported" (TCS, TechM)
- HCLTech divestiture effect on revenue
- Cognizant Belcan
- Accenture `rev_usd` FY18 levels

There are 18 duplicate rows, where 1a and 1b found the same error.

**Effect on pilot outputs.**
- Corrected `yoy_metrics` differs from the original in only 6 cells: 5 `gR_usd`, 1 `gL`. No `gR`, `du` or `resid` value changes.
- The Part 2 episode table and the comparator correlations are unchanged. The simulation inputs (`gR`, `gL`, `du`, `gTCV`, `dsub`) are also unchanged; the simulation was not re-run.

**Alternative, not a correction.** `data/corrected/yoy_metrics_corrected_alt_ltimchain.csv` adds a single LTI-group entity (`ltim_chain`), built from growth rates with no level splice.

### Files

- `data/corrected/core_quarterly_corrected.csv`, `yoy_metrics_corrected.csv`, `CHANGELOG.csv`, `yoy_metrics_corrected_alt_ltimchain.csv`
- Regenerate: `python 01_pilot/scripts/audit/build_corrected.py`. It asserts each `old_value` before changing it. With no corrections, its output is byte-identical to `data/tidy`.
- Evidence: `01_pilot/audit/spotcheck_1a.csv`, `corrections_1a.csv`, `corrections_1b.csv`, `fiscal_calendar.csv`, `calq_mapping_check.csv`, `comparator_corr_variants.csv`, `episode_row_quarter_map.csv`, `episodes_relabelled.csv`, `episodes_fiscal.csv`, `structural_breaks_jumps.csv`, `ltim_sign_scan.csv`, `hcl_divestiture_check.csv`
- Scripts: `01_pilot/scripts/audit/*.py`

### Not fixed at source (outside the brief)

The parser bug in `scripts/extract/ltim_parse_tables.py` (`parse_num`) and the attrition ranking in `01_pilot/scripts/01_build_tidy.py` (`pick()`) are both corrected downstream here. The original scripts were left unchanged.

---

## Part 3. Final pass before the write-up

*Date: 2026-10-05. Detailed inputs for the note are in Part 4.*

To regenerate the data, tables and figures with one command, run `python3 01_pilot/scripts/note/make_all.py`. Add `--ltim` to re-extract the LTIM raw file with the fixed parser first.

The run includes a reproduction check: the source-fixed pipeline reproduces the previous round's `data/corrected/*_corrected.csv` exactly.

### How the work was split

- **Done directly:** Tasks 1, 3 and 5.
- **Task 2 used two agents.** The first re-scanned the transcripts and coded the statements as coder 1. The second coded the same statements independently, as coder 2.
  - The first agent split the full read across 32 parallel readers, despite the request to limit subagents. The second agent worked alone.
- **Task 4 used one agent,** working alone.
- **Spot checks done by hand:**
  - all six note quotes, verbatim against the transcripts;
  - the Accenture Q4FY26 figures;
  - the TCS subcontracting figures;
  - Persistent FY24 revenue and headcount;
  - both BLS results.

---

### Task 1: Audit decisions and rebuilt data

#### Decisions applied

1. **LTI counted once.** LTI + Mindtree are combined through FY22, and LTIMindtree is used from FY23. LTIMindtree's restated history covers FY22, so FY23 growth uses one entity in both years. No period includes both.
2. **HCLTech divestiture: adjust neither revenue nor headcount.**
   - No revenue figure for the divested State Street JV was disclosed. The only number is a forward-looking "80-bps impact" on FY25 guidance (Q1FY25 call); none appears in the investor releases.
   - The 7,398 headcount-base adjustment (D10) is therefore removed. HCLTech's FY25 headcount growth becomes −1.6%, against +1.7% when adjusted. This moves the six-firm simple average by about 0.6 pp.
3. **Wipro.** Growth observations spanning a level break are set to missing; levels are kept.
   - ISRE perimeter change: YoY windows 2017Q2–2018Q1, for headcount growth and USD revenue growth.
   - Alight staff transfer (Q2FY19): headcount growth for 2018Q3–2019Q2.
   - Firm-reported cc growth is kept, because each figure is like-for-like within its own release.
4. **Script bugs fixed at source.**
   - `scripts/extract/ltim_parse_tables.py`: `parse_num` now reads "(3.7)%" as negative.
   - `01_pilot/scripts/01_build_tidy.py`: `pick()` ranks period types in the order listed (trailing-twelve-month before quarterly) and uses a stable sort.
   - `scripts/extract/ltim_build.py`: a `LTIM_OUT` environment variable now lets the output go elsewhere, so `data/raw/` is not overwritten. The default path is unchanged.
   - Checks:
     - The unfixed builder reproduces `data/raw/ltim.csv` byte for byte.
     - The fixed parser changes exactly the 22 audited cells and nothing else.
     - The fixed `pick()` changes exactly the 2 Cognizant attrition cells.
     - The full fixed pipeline reproduces `data/corrected/` exactly.
5. **Accenture Q4FY26 added** from the 1 Oct 2026 8-K (`01_pilot/audit/new_raw_accenture_q4fy26.csv`).
   - Its quarter ends in August, so it maps to calendar 2026Q3, which is Indian Q2FY27. It therefore does not enter Table A.
6. **Acquisitions:** not adjusted.

#### Tables and figures

Built by `01_pilot/scripts/note/tables_figures.py`; nothing was hand-computed.

- **Table A** (`01_pilot/output/final/table_A.md`, `.csv`; firm-level inputs in `table_A_firms.csv`).
  - Rows: FY16–FY26, plus FY27 Q1 labelled as one quarter.
  - Columns: revenue growth in USD and in constant currency (cc); headcount growth (average-based, plus a year-end version); revenue per employee (USD and cc); utilization change; residual.
  - Shown for: the Indian simple average, the Indian revenue-weighted average, Accenture and Cognizant.
  - Comparators are aggregated to Indian fiscal years. Accenture's year runs Mar–Feb, so 11 of 12 months overlap.
  - Firm lists are given for each year.
- **Table B** (`01_pilot/output/final/table_B.md`): mean residual and mean utilization change, FY16–FY23 against FY24–FY26. Variants: excluding FY21, and same firms in both windows.
- **Figure 1** (`01_pilot/figures/final/fig1_india_vs_comparators.png`, `.svg`): the Indian revenue-weighted average against Accenture and Cognizant, FY16–FY26. Three panels (revenue cc, headcount, revenue per employee cc), with FY24 marked.
- **Figure 2** (`01_pilot/figures/final/fig2_subcontracting_share.png`, `.svg`): subcontracting cost as a share of revenue for the six Indian firms, FY20–FY26. LTIMindtree starts at FY22.

#### Definitions

- **Growth:** log change × 100.
- **Fiscal-year revenue growth:** quarterly YoY growth aggregated with prior-year revenue weights. For USD revenue, this equals the log change of fiscal-year revenue.
- **Headcount growth:** the mean of the four quarterly YoY changes, which approximates growth of average headcount.
- **Utilization change:** the mean of quarterly YoY changes within each firm's own series.
- **Residual:** revenue-per-employee growth (cc) minus utilization change.
- **Completeness:** a fiscal-year value requires all four quarters.

#### Key numbers (`note_numbers.csv`)

| Indian six | FY16–20 mean | FY22 | FY23 | FY24 | FY25 | FY26 |
|---|---|---|---|---|---|---|
| Headcount, simple | +7.4 | +18.5 | +14.3 | **−3.6** | −0.5 | +1.2 |
| Headcount, revenue-weighted | +7.2 | +17.2 | +13.9 | **−2.8** | −0.8 | +0.6 |
| Revenue cc, simple | +8.7 | +16.7 | +12.8 | +0.7 | +2.6 | +1.4 |
| Revenue per employee cc, simple | +2.5 | +0.0 | −0.8 | +4.4 | +3.1 | +0.2 |

**Table B** (mean residual, by window):

| firm set | FY16–23 | FY16–23 excl. FY21 | FY24–26 |
|---|---|---|---|
| All firms with data | +1.1 | +2.1 | +1.3 |
| Same firms (Infosys, Tech Mahindra, Wipro) | +0.5 | +1.7 | +0.9 |

**Subcontracting share fell FY23 → FY24 at all six firms:**

| | TCS | Infosys | HCLTech | Wipro | Tech Mahindra | LTIMindtree |
|---|---|---|---|---|---|---|
| FY23 | 9.5 | 9.6 | 14.7 | 12.7 | 15.0 | 8.5 |
| FY24 | 6.6 | 8.0 | 13.3 | 11.5 | 12.9 | 7.2 |

---

### Task 2: Earnings-call statements

#### Extraction

The method is documented in `01_pilot/audit/calls_codebook.md`.

- **Transcripts:** the same 183 transcripts as the pricing pass, listed in `01_pilot/audit/calls_transcripts.csv`. TCS Q4FY23 is still missing.
- **Demand re-scan:**
  - 1,711 statements (`01_pilot/audit/demand_calls_quotes.csv`; dictionary in `01_pilot/audit/calls_demand_dictionary.json`).
  - Every transcript was effectively read in full; about 9.3 statements were kept per call.
  - Rules were the same as the pricing pass: verbatim (machine-checked), management only, speaker confirmed, page re-derived.
- **Merged total:** 389 + 1,711 − 13 cross-pass duplicates = **2,087 statements** (`01_pilot/audit/calls_statements.csv`; duplicates logged in `01_pilot/audit/calls_merge_log.csv`).
- **Scripts:** `01_pilot/scripts/audit/calls_*.py`.

#### Codebook and reliability

- **Codebook** (`01_pilot/audit/calls_codebook.md`): categories A–E, 7 decision rules, and one verbatim example per category.
- **Coder 2** was a separate agent. It received only the codebook and a shuffled file of quotes with context notes. It did not see coder 1's codes or which pass each statement came from.
- **Agreement on the primary category:** **92.1%**, Cohen's κ = **0.87** (`01_pilot/output/final/calls_agreement.csv`, `calls_confusion.csv`).

| category | coder 1 count | coder 2 count | coder 1's codes matched by coder 2 | positive agreement | κ |
|---|---|---|---|---|---|
| A | 796 | 743 | 91.0% | 94.1% | 0.91 |
| B | 47 | 54 | 87.2% | 81.2% | 0.81 |
| C | 72 | 83 | 76.4% | 71.0% | 0.70 |
| D | 117 | 91 | 70.1% | 78.8% | 0.78 |
| E | 1,055 | 1,116 | 96.8% | 94.1% | 0.88 |

- **Agreement by pass:** 81.5% on pricing-pass statements, 94.6% on demand-pass statements.
- **Main disagreements:**
  - 71 statements coded A by coder 1 and E by coder 2. These are mostly mixed strength/weakness statements.
  - 22 statements coded D by coder 1 and C by coder 2. In these the AI link is implied but not named.
- **Disagreements:** all 164 are in **`01_pilot/audit/calls_disagreements.csv`**, unresolved, with a `resolved_primary` column to fill in.
- **Spot-check:** 30 statements drawn with seed 20261006, showing both codings, in `01_pilot/audit/calls_spotcheck.csv`.

#### Figure 3

- **Files:** `01_pilot/figures/final/fig3_call_categories.png` and `.svg` (coder 1 codes); `fig3_call_categories_coder2.png` (coder 2 codes); data in `01_pilot/output/final/fig3_data.csv`.
- **What it shows:** statements per transcript by category and half-year, 2021H1–2026H2. Transcript counts appear under the axis. Panels are split by scale.

Statements per transcript (coder 1):

| category | 2021–22 | 2023 | 2024H2–2026H1 | 2026H2 |
|---|---|---|---|---|
| A, demand weakness | 0.4–1.4 (3.0 in 2022H2) | 7.5–7.9 | 4.7–5.7 | 5.9 |
| D, AI pass-through | 0–0.1 | 0.3 | 0.6–1.6 | 3.0 (8 transcripts) |

- **Robustness:** coder 2's codes give the same pattern.
- **Caveat:** A comes mostly from the broader demand pass (about 9 statements per call), and D from the pricing pass (about 2). Compare trends within a category, not levels across categories.

#### Quotes (`01_pilot/evidence/note_quotes.md`)

All six were re-verified verbatim on the cited page (`01_pilot/scripts/note/verify_note_quotes.py` → `01_pilot/output/final/note_quotes_check.csv`). Both coders agree on every one.

| # | category | firm, call, date | speaker | quote |
|---|---|---|---|---|
| 1 | A | Infosys Q2FY24, 12 Oct 2023 | Salil Parekh | "We continue to see the overall environment where digital transformation program and discretionary spends are low and decision-making is slow. This is impacting our volumes." |
| 2 | A | TCS Q2FY24, 11 Oct 2023 | K Krithivasan | "Our growth was affected by the holding back of discretionary spends by clients." |
| 3 | B | TCS Q3FY24, 11 Jan 2024 | Samir Seksaria | "…Pricing environment is stable…" |
| 4 | D | TCS Q4FY25, 10 Apr 2025 | K Krithivasan | "…we will try to share those gains with our customers… what we did with $100 if we are able to do with $95 or $90." |
| 5 | D | HCLTech Q4FY26, 21 Apr 2026 | C. Vijayakumar | "…would translate to 2% to 3% for our portfolio." |
| 6 | D | HCLTech Q4FY26, 21 Apr 2026 | C. Vijayakumar | "$100 million deal would be much lesser today - maybe 80 million…" |

The full quotes, URLs and page numbers are in `01_pilot/evidence/note_quotes.md`.

---

### Task 3: Price index check

Added to `01_pilot/evidence/price_data.md` §A2b; files are in `01_pilot/explore/prices/final_bls/`.

- **NAICS 5415 / 541511 / 541512: no BLS producer price index exists.**
  - The BLS API returns "Series does not exist" for PCU5415--5415--, PCU541511541511 and PCU541512541512.
  - The current and discontinued industry lists have no 5415 code.
  - BLS's [Areas of Noncoverage](https://www.bls.gov/ppi/fd-id/areas-of-noncoverage-in-the-ppi-system.htm) page (last modified March 4, 2026) lists 541511, 541512, 541513 and 541519 as not covered.
- **NAICS 518210, PCU518210518210** (data processing, hosting and related services; base Dec 2000 = 100).
  - According to the [BLS fact sheet](https://www.bls.gov/ppi/factsheets/producer-price-index-for-the-data-processing-and-related-services-industry-naics-518210.htm) (last modified Nov 7, 2008), it was introduced in January 2002 with history from December 2000. It is priced by repricing actual contracts with fixed characteristics.
  - Annual-average growth:

| 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (Jan–Aug YoY) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| +0.3 | +1.2 | +1.5 | +0.3 | +0.5 | +2.9 | +1.0 | +1.0 | +1.5 | +1.3 | +3.3 | +0.5 |

  - May–Aug 2026 values are preliminary.
  - **Label:** a US domestic producer price, used as a proxy for offshore Indian vendors' prices, not as a measure of them.

---

### Task 4 (optional): Mid-tier Indian firms

Files are in `01_pilot/explore/midtier/` (raw rows with citations, annual file, comparison file); source documents are in `data/sources/midtier/`. These firms are not in the main tables.

**Coverage, FY20–FY26:**
- **Persistent:** complete.
- **Mphasis:** complete. FY20 comes from the FY21 report, because the FY20 report link returns 404.
- **Coforge:** complete, except FY20 USD revenue (INR only).
- **Hexaware:** reports calendar years (CY2019–CY2025). Each is aligned to the Indian fiscal year ending three months later.

| | FY24 | FY25 | FY26 |
|---|---|---|---|
| Top-six revenue growth (USD) | +2.0 | +2.7 | +2.2 |
| Mid-tier four revenue growth (USD) | +5.0 | +14.7 | +13.9 |
| Top-six year-end headcount growth | −4.5 | +1.0 | −0.2 |
| Mid-tier four year-end headcount growth | +0.7 | +10.7 | +5.6 |

- **Share gain.** The mid-tier share of combined revenue rose from 5.1% (FY21) to 7.3% (FY26); its share of headcount rose from 5.5% to 7.3%. The mid-tier firms gained share while the top six stalled.
- **Acquisitions are included:** Coforge–Cigniti (FY25), Mphasis–Silverline (FY24), Persistent (FY22) and Hexaware's deals. Excluding Coforge, FY25 revenue growth for the other three is still +10.9.
- **Headcount definitions differ:** Mphasis and Hexaware include contractors.

---

### Task 5: Note inputs

Written to `note_inputs.md` (now Part 4 of this file), organised by the note's eight sections plus a 1b subsection on the mid-tier firms. Every number traces to a repo file (mostly `01_pilot/output/final/note_numbers.csv`, `table_A.*`, `table_B.*`, `fig2_data.csv`, `fig3_data.csv`, `calls_agreement.csv`) or to a cited external source. There are 16 limitations, one line each.

---

### Every data change in this pass

All are logged in `data/corrected/CHANGELOG.csv`, which now has 193 rows: 105 from the audit round (also kept in `CHANGELOG_v1_audit.csv`) and 88 from this pass. The final files are `data/corrected/core_quarterly_final.csv` and `yoy_metrics_final.csv`; the previous `*_corrected.csv` files are untouched.

1. **Source fixes (decision 4).**
   - The 22 LTI/Mindtree sign cells and the 2 Cognizant attrition cells (2021Q2: 29 → 18; 2021Q3: 33 → 24) are now produced by the fixed code instead of applied as corrections. Values are the same as before.
   - The fixed LTIM raw file is `data/rebuilt/raw/ltim.csv`; `data/raw/ltim.csv` is unchanged.
2. **HCLTech (decision 2).** The divestiture adjustment is removed. Headcount growth for 2024Q2 / Q3 / Q4 / 2025Q1:

| | 2024Q2 | 2024Q3 | 2024Q4 | 2025Q1 |
|---|---|---|---|---|
| Before | +1.54 | +2.26 | +1.55 | +1.50 |
| After | −1.82 | −1.15 | −1.80 | −1.80 |

   Revenue-per-employee growth for those quarters changes accordingly.
3. **Wipro (decision 3).**
   - Headcount growth set to missing for 2017Q2–2018Q1 (ISRE) and 2018Q3–2019Q2 (Alight).
   - USD revenue growth set to missing for 2017Q2–2018Q1.
   - The derived revenue-per-employee growth and residual are missing for the same quarters.
4. **Accenture Q4FY26 (decision 5).** New raw rows, all from the 1 Oct 2026 8-K Ex.99:
   - revenue $18,679.11M;
   - growth +6% in USD, +7% in local currency;
   - new bookings $22,170M;
   - headcount 814,000. This is a rounded figure: the release says "approximately 814,000 people".
   - Utilization and attrition are not available: the presentation returns 403 and is not archived, and the 10-K is not yet filed.
   - Derived 2026Q3 values: cc revenue growth +6.77, USD revenue growth +5.97, headcount growth +4.36.
5. **LTI counted once (decision 1):** done at aggregation in the tables script; no data change.

**Files modified in place:** the three scripts in decision 4 (as instructed) and `01_pilot/evidence/price_data.md` (Task 3). No original data file, simulation code or existing write-up was modified.

---

### What contradicts or qualifies the note's five claims

1. **"Headcount growth collapsed after FY23": supported, with qualifiers.**
   - The six-firm average fell from +14.3% (FY23) to −3.6% (FY24), against a +7.4% FY16–20 mean. Headcount fell at 5 of 6 entities in FY24; HCLTech was the exception at +2.1%.
   - The comparators slowed too: Accenture +1.5% (FY24); Cognizant −0.9% (FY24) and −2.6% (FY25).
   - The mid-tier Indian firms grew strongly, so this is not a sector-wide collapse.
   - FY23 itself is the end of the FY22 hiring boom, not a normal year.
2. **"The identity rules out S2": weaker than stated.**
   - After FY23 the residual changes by −0.8 to +0.4 pp, depending on the firm set and on whether FY21 is included. S2 predicts a rise of several points.
   - But the test covers only Infosys, Wipro, Tech Mahindra and the LTI group. TCS and HCLTech, the two largest, report no utilization.
   - TCS's revenue per employee accelerated in FY24–25 (+4.2 and +3.9, against +1.7 in FY16–20) and cannot be decomposed.
   - Infosys's residual reached +6.6 in FY24. That may be mechanical: utilization excludes trainees while headcount includes them, and fresher intake collapsed.
   - So the data rule out a large S2 effect at those four firms, not at all six. The second half of the claim (S1 and S3 are equivalent under full pass-through) follows from the identity and is unaffected.
3. **"Subcontracting share fell in FY24, ruling out the subcontractor version of S4": holds for FY24–25.**
   - The share fell at all six firms in FY24.
   - It rose again at 5 of 6 in FY26, though all six remain below FY23.
   - It is a cost ratio, not contractor FTEs.
4. **"No public source measures output prices for Indian IT services": holds for Indian vendors specifically.**
   - ISG publishes measured unit-price declines for a narrow slice of managed-services contracts, across all vendors.
   - The BLS 518210 index is a contract output price for US domestic firms.
5. **"Explanations shifted from demand weakness to AI pass-through": partly.**
   - Pass-through (D) statements rose from about 0.1–0.3 per transcript before mid-2024 to 0.6–1.6 from 2024H2 to 2026H1.
   - Demand-weakness (A) statements stayed high: 4.7–5.9 per transcript in 2024H2–2026H2, down from 7.5–7.9 in 2023.
   - Pass-through talk was added to demand talk, not substituted for it. The pattern holds under both coders.

---

### Judgment calls you may want to revisit

- **HCLTech:** I treated the "80-bps" guidance remark as not a disclosure of divested revenue. If you count it as disclosed, adjusting both revenue and headcount takes one small change.
- **Wipro:** firm-reported cc revenue growth is kept across the ISRE and Alight windows, because each figure is like-for-like within its own release. Only level-based growth is excluded.
- **Accenture Q4FY26 headcount:** a rounded boilerplate figure. Replace it with the exact count when the 10-K or presentation is available.

---

### New files in this pass

**Note documents:** `01_pilot/FOLLOWUP.md (Part 4)`, `01_pilot/evidence/note_quotes.md`, `01_pilot/audit/calls_codebook.md`, `01_pilot/audit/calls_disagreements.csv`, `01_pilot/audit/calls_spotcheck.csv`, `01_pilot/FOLLOWUP.md (Part 3)`.

**Data:**
- `data/corrected/core_quarterly_final.csv`, `yoy_metrics_final.csv`, `CHANGELOG.csv`, `CHANGELOG_v1_audit.csv`
- `data/rebuilt/raw/ltim.csv`
- `01_pilot/explore/midtier/`
- `01_pilot/explore/prices/final_bls/`
- `data/sources/accenture/final_q4fy26/`, `data/sources/midtier/`

**Tables:** `01_pilot/output/final/` — `table_A.*`, `table_B.*`, `table_A_firms.csv`, `note_numbers.csv`, `calls_agreement.csv`, `calls_confusion.csv`, `fig2_data.csv`, `fig3_data*.csv`, `note_quotes_check.csv`.

**Figures:** `01_pilot/figures/final/` — `fig1_india_vs_comparators`, `fig2_subcontracting_share`, `fig3_call_categories`, `fig3_call_categories_coder2` (PNG and SVG each).

**Audit files:** `01_pilot/audit/calls_transcripts.csv`, `calls_statements.csv`, `calls_statements_for_coder2.csv`, `demand_calls_quotes.csv`, `calls_demand_dictionary.json`, `calls_merge_log.csv`, `calls_coding_coder1.csv`, `calls_coding_coder2.csv`, `new_raw_accenture_q4fy26.csv`.

**Scripts:** `01_pilot/scripts/note/` — `make_all.py`, `build_final_data.py`, `tables_figures.py`, `calls_analysis.py`, `verify_note_quotes.py`, `note_numbers.py`; and `01_pilot/scripts/audit/calls_*.py`.

---

## Part 4. Inputs for the research note

*Built 2026-10-05. Every number below comes from a repo file (path given) or from a cited external source. To regenerate everything, run `python3 01_pilot/scripts/note/make_all.py`.*

Conventions used throughout:
- **Growth** is a log change × 100, which is close to a % change.
- **Years** are Indian fiscal years, April–March. "Indian six" means TCS, Infosys, HCLTech, Wipro, Tech Mahindra and the LTI business. The LTI business is counted once: LTI + Mindtree up to FY22, LTIMindtree from FY23.
- **Headcount growth** is the growth of average headcount: the mean of the four quarterly year-on-year changes.

---

### 1. The fact: headcount growth collapsed after FY23

Sources: `01_pilot/output/final/table_A.md` and `table_A.csv`, with summaries in `01_pilot/output/final/note_numbers.csv`. Figure 1: `01_pilot/figures/final/fig1_india_vs_comparators.png` (.svg).

| Indian six | FY16–FY20 mean | FY22 | FY23 | FY24 | FY25 | FY26 | FY27 Q1 (one quarter) |
|---|---|---|---|---|---|---|---|
| Headcount, simple average | +7.4 | +18.5 | +14.3 | **−3.6** | −0.5 | +1.2 | +1.0 |
| Headcount, revenue-weighted | +7.2 | +17.2 | +13.9 | **−2.8** | −0.8 | +0.6 | −0.1 |
| Revenue cc, simple | +8.7 | +16.7 | +12.8 | +0.7 | +2.6 | +1.4 | +3.6 |
| Revenue cc, revenue-weighted | +8.7 | +16.3 | +12.9 | +1.5 | +3.2 | +0.6 | +3.0 |
| Revenue per employee (cc), simple | +2.5 | +0.0 | −0.8 | +4.4 | +3.1 | +0.2 | +2.6 |
| Revenue per employee (cc), revenue-weighted | +2.2 | −0.4 | −0.7 | +4.4 | +4.0 | +0.0 | +3.1 |

- **Breadth of the fall.** Headcount fell in FY24 at 5 of the 6 entities. HCLTech is the exception at +2.1 (`note_numbers.csv`). Year-end headcount (March 2024 vs March 2023) fell 4.7% on the simple average.
- **The comparators slowed too.**
  - Accenture: headcount +1.5 (FY24), +5.7 (FY25), +0.5 (FY26) against a +8.1 FY17–FY20 mean; revenue cc +2.5, +5.4, +5.0.
  - Cognizant: headcount −0.9 (FY24), −2.6 (FY25), +3.9 (FY26) against a +7.1 FY16–FY20 mean; revenue cc −1.0, +4.1, +5.2. Cognizant's FY25–26 revenue includes Belcan; acquisitions are not adjusted.
  - Accenture's year is shifted by one month (its fiscal quarters end Nov/Feb/May/Aug).
- **What FY23 actually shows.** FY23 is the end of the FY22 hiring boom, not a normal year. The collapse is measured against both FY16–FY20 and FY22–23.
- **How many firms are in each average.** The cc revenue average covers 4 firms in FY16–FY20, 5 in FY21–FY23 and 6 from FY24. The LTI group lacks cc revenue before FY24, and Tech Mahindra lacks it before FY21. Firm lists by year are in `table_A.md`.

#### 1b. Context: mid-tier firms (kept separate from the main tables)

Source: `01_pilot/explore/midtier/midtier_vs_top6.csv`, built from primary filings in `01_pilot/explore/midtier/midtier_raw.csv`. The four firms are Persistent, Coforge, Mphasis and Hexaware.

| | FY24 | FY25 | FY26 |
|---|---|---|---|
| Top-six revenue growth (USD, from levels) | +2.0 | +2.7 | +2.2 |
| Mid-tier four revenue growth (USD, from levels) | +5.0 | +14.7 | +13.9 |
| Top-six year-end headcount growth | −4.5 | +1.0 | −0.2 |
| Mid-tier four year-end headcount growth | +0.7 | +10.7 | +5.6 |

- **Share of the combined total (top six plus mid-tier four).** The mid-tier share of revenue rose from 5.1% (FY21) to 7.3% (FY26). Its share of headcount rose from 5.5% to 7.3% over the same years.
- **Acquisitions are included.** Examples: Coforge–Cigniti (FY25), Mphasis–Silverline (FY24), and Hexaware's deals. Excluding Coforge in FY25, the other three still grew revenue +10.9.
- **Hexaware reports calendar years.** Each one is aligned to the Indian fiscal year ending three months later, a 9-month overlap.
- **Headcount definitions differ.** Mphasis and Hexaware include contractors.
- **What it implies.** Demand for Indian-delivered IT services did not fall uniformly. Some work went to smaller Indian vendors. This bears on S1 (demand) versus a vendor-share shift (an S4-like reallocation among vendors). It is not GCC evidence.

### 2. The identity: what the residual says

Source: `01_pilot/output/final/table_B.md` and `table_B.csv`.

The residual is revenue-per-employee growth (cc) minus utilization change. It equals g_p − g_a, and can be computed only for firms that report utilization.

| window | firm set | mean residual | mean utilization change | firm-years | firms |
|---|---|---|---|---|---|
| FY16–FY23 | all with data | +1.1 | +0.8 (33 firm-years) | 18 | HCLTech, Infosys, Tech Mahindra, Wipro |
| FY16–FY23 excl. FY21 | all with data | +2.1 | +0.5 (29) | 15 | same |
| FY24–FY26 | all with data | +1.3 | +1.0 | 12 | Infosys, LTI group, Tech Mahindra, Wipro |
| FY16–FY23 | same firms in both windows | +0.5 | +0.3 | 14 | Infosys, Tech Mahindra, Wipro |
| FY16–FY23 excl. FY21 | same firms | +1.7 | −0.4 | 11 | same |
| FY24–FY26 | same firms | +0.9 | +0.7 | 9 | same |

- **Change in the residual.** After FY23 it moves by between −0.8 and +0.4 pp, depending on the firm set and on whether COVID-hit FY21 is included. S2 predicts a rise equal to the labor-saving effect, e.g. the pilot's prior of about 4 pp a year. No specification shows a rise of more than 0.4 pp.
- **Which firms are not covered.** TCS stopped reporting utilization after Q3FY16 and HCLTech after Q4FY19, so neither is in FY24–26. Wipro is also excluded in FY18–FY20 under decision 3.

### 3. Subcontracting

Sources: Figure 2 `01_pilot/figures/final/fig2_subcontracting_share.png` (.svg); data in `01_pilot/output/final/fig2_data.csv`, from `01_pilot/audit/subcontracting_series.csv`.

Subcontracting cost as a % of revenue, firm-reported, same currency:

| firm | FY23 | FY24 | change | FY26 |
|---|---|---|---|---|
| TCS | 9.5 | 6.6 | −2.9 | 5.5 |
| Infosys | 9.6 | 8.0 | −1.6 | 8.6 |
| HCLTech | 14.7 | 13.3 | −1.5 | 14.2 |
| Wipro | 12.7 | 11.5 | −1.3 | 11.6 |
| Tech Mahindra | 15.0 | 12.9 | −2.2 | 10.7 |
| LTIMindtree | 8.5 | 7.2 | −1.3 | 7.7 |

- **Direction.** The share fell at all 6 firms from FY23 to FY24. In FY26 all 6 remain below their FY23 level, but 5 of 6 rose from FY25 to FY26; Tech Mahindra is the exception.
- **Definitions.**
  - TCS's line is "fees to external consultants" (cost of revenue + SG&A), with a definition break at Q1FY27 (not shown).
  - LTIMindtree's comes from annual reports, from FY22 only.

### 4. S1 vs S4: did the work go to clients' own centres (GCCs)?

Detail and citations: `01_pilot/evidence/discriminating_data.md` §(a), rows 1i, 11b and 2a. All three are labelled *measured*.

- **RBI Census on Foreign Liabilities and Assets, Table 9C.**
  - Information-and-communication exports by 22,395 foreign subsidiaries in India: ₹6,53,856 cr (2021-22) and ₹8,45,021 cr (2022-23).
  - Coverage includes foreign-owned vendors as well as captives, and includes telecom and publishing.
  - Source: RBI press release, 12 Sep 2023, https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=56359
- **BEA, employment of US multinationals' majority-owned foreign affiliates (AMNE/MOFA).**
  - India, professional, scientific and technical services, thousands: 598.4 (2019), 877.0 (2022), 893.2 (2023, preliminary).
  - Coverage includes US-headquartered vendors.
  - Source: BEA `mofas-employment.xls`, released 22 Aug 2025; 2024 data due Nov 2026.
- **Naukri JobSpeak, Sep 2026.**
  - Year-on-year hiring index: IT/Software Services −4%, GCC +4% (p.4 tiles).
  - IT-software index 3,432 (Sep 2026) vs 3,585 (Sep 2025).
  - These are job postings, not hires. The GCC series is shown only as a year-on-year change.
  - Source: Info Edge, `Naukri-Jobspeak-September-2026.pdf`, infoedge.in/InvestorRelations/NaukriJobSpeak

### 5. Earnings calls

**Material.** 2,087 verbatim management statements from 183 transcripts, Jan 2021–Oct 2026, eight firms (`01_pilot/audit/calls_statements.csv`). Codebook, extraction methods and reliability: `01_pilot/audit/calls_codebook.md`.

**Agreement between the two coders.**
- Primary category: **92.1%**, κ = 0.87 (`01_pilot/output/final/calls_agreement.csv`).
- By category (share of coder 1's codes matched by coder 2):

| A | B | C | D | E |
|---|---|---|---|---|
| 91.0% | 87.2% | 76.4% | 70.1% | 96.8% |

- 164 disagreements are listed in `01_pilot/audit/calls_disagreements.csv`, unresolved. A 30-statement spot-check sample is in `01_pilot/audit/calls_spotcheck.csv`.

**Figure 3.** `01_pilot/figures/final/fig3_call_categories.png` (coder 1). The coder-2 version is `fig3_call_categories_coder2.png`; data in `01_pilot/output/final/fig3_data.csv`.

Statements per transcript (coder 1):

| category | 2021–22 | 2023 | 2024H2–2026H1 | 2026H2 |
|---|---|---|---|---|
| A, demand weakness | 0.4–1.4 (3.0 in 2022H2) | 7.5–7.9 | 4.7–5.7 | 5.9 |
| D, AI productivity passed to clients | 0–0.1 | 0.3 | 0.6–1.6 | 3.0 (8 transcripts) |

- Coder 2's codes give the same pattern.
- **Caveat on levels.** A comes mainly from a broader extraction pass than D: about 9 vs 2 statements per call. Compare trends within a category, not levels across categories.

**Quotes.** Six, all re-verified verbatim: `01_pilot/evidence/note_quotes.md`.
- Two are A (TCS and Infosys, Oct 2023).
- One is B (TCS, Jan 2024).
- Three are D (TCS, Apr 2025; HCLTech ×2, Apr 2026).

### 6. Price data

**What was searched and found.** Searched:
- official producer and services price indices: US BLS/BEA, UK ONS, Eurostat, Bank of Japan, India's WPI and new Services PPI, India's national-accounts deflators;
- the firms' own disclosures, 2003–2026;
- sourcing advisors: ISG, Everest, Gartner, HfS;
- broker research;
- 183 earnings calls.

What was found:
- **No public source measures output prices for Indian IT services in any period.**
- Official indices cover domestic producers and mostly price hourly or person-month rates, which measure price per unit of labor (p/a), not per unit of work.
- India has no IT services price index.
- Firm disclosures measure p/a and stopped by FY2020.
- Analysts' 2025–28 "deflation" estimates assume pass-through rather than measure it.
- The only measured output price found is ISG's contracted resource-unit prices in managed-services deals. It covers all vendors and a narrow, mostly infrastructure, slice.

Details: `01_pilot/evidence/price_data.md`.

**Infosys person-month bound.**
- Infosys's 20-F reported revenue per billed person-month (p/a) every year FY2003–FY2020. Growth, USD reported: FY15 −2.8%, FY16 −4.7%, FY17 −2.7%, FY18 +1.5%, FY19 −0.8%, FY20 −1.5% (`01_pilot/evidence/price_data.md` §A3; values in `01_pilot/audit/price_firm_disclosures.csv`).
- Adjusted to constant currency, this is about −1% to −2% a year in FY15–FY17 and about 0% in FY18–FY20. The adjustment is our own calculation, labelled derived (`01_pilot/evidence/price_data.md` §b).
- Since g_p = g_{p/a} + g_a, this is an *upper* bound on Infosys's g_p **only if labor per unit (a) did not rise**. That is an assumption, not an observation.
- It is a single firm, not the sector, and it ends in FY20.

**BLS check (Task 3; `01_pilot/evidence/price_data.md` §A2b).**
- **NAICS 5415 / 541511 / 541512:** BLS publishes no producer price index for these. The BLS API returns "Series does not exist" for PCU5415--5415--, PCU541511541511 and PCU541512541512. BLS lists 541511–541519 as non-covered industries (https://www.bls.gov/ppi/fd-id/areas-of-noncoverage-in-the-ppi-system.htm, last modified March 4, 2026).
- **NAICS 518210, data processing and hosting (PCU518210518210):** introduced January 2002 with history from December 2000. It is priced by repricing actual contracts with fixed characteristics (BLS fact sheet, last modified Nov 7, 2008).
  - Annual-average growth: 2015 +0.3, 2016 +1.2, 2017 +1.5, 2018 +0.3, 2019 +0.5, 2020 +2.9, 2021 +1.0, 2022 +1.0, 2023 +1.5, 2024 +1.3, 2025 +3.3; 2026 Jan–Aug +0.5 year-on-year.
  - Files: `01_pilot/explore/prices/final_bls/`.
  - This is a US domestic producer price: a proxy for offshore Indian vendors' prices, not a measure of them.

### 7. What would settle it

From `01_pilot/evidence/discriminating_data.md` §(c), condensed.

| data item | who could collect it | pair it separates | exists publicly? |
|---|---|---|---|
| Price per unit of output in managed-service and fixed-price contracts; renewal value vs prior value for the same scope | Vendors, client procurement teams, sourcing advisors (ISG, Everest, Avasant) | **S1 vs S3** | No. Held in contracts and paid advisory benchmarks |
| Revenue and headcount by service line, split by AI exposure (testing, application maintenance, infrastructure, BPO vs consulting/engineering) | The six firms (disclosure choice) | S1 vs S3 | Discontinued: TCS after FY17, Infosys after FY18, Wipro after FY23 |
| Headcount by role or job level | The firms. Paid proxy: Revelio Labs / LinkedIn | S1 vs S3 | Infosys job bands only; otherwise paid |
| GCC headcount by parent company and function, measured | MCA filings compiled per entity (₹100 per company inspection); Nasscom | **S1 vs S4** | No. Industry estimates only, with no parent detail |
| Affiliated vs unaffiliated computer-services imports from India | BEA (BE-125 survey) | S1 vs S4 | Collected, not published by country |
| RBI software-exports survey: employees and billing to subsidiaries abroad | RBI | S1 vs S4 | Collected, not published |
| Subcontractor headcount (FTEs) | The firms | S2 vs S4 (subcontractor version) | No. Cost lines only |
| Utilization for all six firms on a consistent definition | The firms | S1 vs S2 (the utilization term) | Discontinued at TCS (FY16) and HCLTech (FY19) |

### 8. Limitations

1. The S2 test rests on 4 of 6 firms. TCS and HCLTech, the two largest, report no utilization in FY24–26.
2. TCS's revenue per employee rose faster in FY24–25 (+4.2, +3.9 vs +1.7 in FY16–20), but without utilization data it cannot be decomposed (`01_pilot/output/final/table_A_firms.csv`).
3. Infosys's residual jumped to +6.6 in FY24. Its utilization excludes trainees but its headcount includes them, so the collapse in fresher intake can raise the residual mechanically.
4. Before FY24, constant-currency revenue covers only 4–5 of the six entities. The averages change composition over time.
5. The HCLTech divestiture is not adjusted (decision 2). HCLTech's FY25 headcount growth is −1.6% unadjusted against +1.7% adjusted (`data/corrected/CHANGELOG.csv`), which moves the six-firm simple average by about 0.6 pp.
6. Acquisitions are not adjusted: Cognizant–Belcan, Wipro–Capco, Accenture's programme, HCLTech–IBM products.
7. Accenture's fiscal year is offset from the Indian year by one month. Its Q4FY26 (added in this pass) falls outside Table A.
8. Accenture Q4FY26 headcount is a rounded "approximately 814,000". Its utilization and attrition were not available on 2026-10-05.
9. Wipro growth observations spanning the ISRE perimeter change (FY18) and the Alight transfer (FY19–FY20) are excluded, so Wipro is missing from several FY18–FY20 averages.
10. Fiscal-year cc growth aggregates quarterly firm-reported cc growth using prior-year revenue weights. Accenture's cc is printed in whole percents (±0.5 pp).
11. Headcount excludes contractors at TCS, Infosys, HCLTech and LTIMindtree but includes direct contractors at Tech Mahindra. Trainee treatment is stated only by Infosys.
12. Subcontracting share is a cost ratio: it mixes contractor rates with volume. Contractor FTEs are not reported.
13. The S4 evidence (RBI FLA, BEA affiliates, Naukri) includes foreign-owned vendors, is annual or postings-based, and lags 1–3 years.
14. Call statements are management commentary (cheap talk), selected through keyword screens. The two passes differ in intensity, coder agreement on D is 70–79%, and 164 disagreements are unresolved.
15. The pilot's S1-vs-S3 argument relies on the full pass-through assumption, under which revenue, headcount and utilization can't separate the two.
16. The demand re-scan used 32 parallel readers. Their per-call yields may differ somewhat.
