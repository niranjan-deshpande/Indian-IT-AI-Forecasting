# India IT pilot: summary of follow-up tasks

*Date: 2026-10-05. Detailed files: `audit_report.md`, `price_data.md`, `price_calls_timeline.md`, `discriminating_data.md`, `figures/task2/README.md`.*

The repo's data are clean apart from a few errors, and none of those errors change the pilot's main numbers. No public source measures sector-level price growth (g_p) directly. The pilot's conclusion that S1 and S3 cannot be separated therefore stands.

## How the work was done

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
  - The agents couldn't write `.md` files, so I saved their reports myself: `audit/findings_1a.md` and `audit/findings_1b.md`.
  - The session hit its 200-query web-search limit. Some searches were left undone; they are listed under Open questions.

## Task 1: Data audit (`audit_report.md`)

### Spot-check (`audit/spotcheck_1a.csv`)

- 30 values were drawn at random (seed 20261005), spread across all firms, 2007–2026 and six metric types. **All 30 match the source documents.**
- 18 were checked against freshly downloaded copies. These were identical to the repo's cached files, so the cache really is the primary documents.
- The values flow unchanged into the tidy data, except one deliberate Cognizant series choice.
- TCS documents from 2015 on could be checked only against the cache, because tcs.com blocks downloads.

### Errors found outside the sample

- **Sign errors.** Mindtree and LTI print negatives as "(3.7)%", and the parser dropped the minus sign. This affects 22 cells (16 Mindtree, 6 LTI). Two reach a core column: Mindtree's reported-currency growth in 2020Q3 and 2020Q4. The cause is a bug in `scripts/extract/ltim_parse_tables.py`.
- **Cognizant attrition.** The build script picks between two attrition definitions arbitrarily. In 2021Q2 and 2021Q3 it took the quarterly-annualized rate (29, 33), where neighbouring quarters use the trailing-12-month rate (18, 24).
- **Accenture FY18.** The FY18 quarters come from figures restated under ASC 606, while FY17 is on the old basis. This inflated FY18 USD growth by about 3.5 pp.
- **GFC-era bases.**
  - TCS's 2007Q1 USD revenue is a currency conversion, not a reported figure.
  - Wipro's 2007Q1 headcount is on an older, narrower perimeter.

### Currency and units

- Revenue is reported in USD for every firm from 2015 on.
- Constant-currency (cc) growth is never mixed with reported growth. The cc series has no fallback to reported growth.
- Accenture's "local currency" growth is the same concept as the Indian firms' cc. It is printed in whole percents, which adds ±0.5 pp of rounding.
- Some GFC-era "reported" growth for TCS and Tech Mahindra is actually INR growth. It is flagged and not used in the analysis.
- TCS's subcontracting cost is in USD, while the other firms' is in INR. The share-of-revenue calculation is still consistent.

### Fiscal-year alignment

- **Fiscal year ends**, confirmed from filings:
  - Indian firms: March.
  - Accenture: August.
  - Cognizant: December.
  - HCLTech: June until FY15, then a 9-month FY16.
- **Calendar mapping.** Every calendar-quarter assignment matches its period-end date, with no exceptions. Mapping Accenture's November quarter to calendar Q4 gives the maximum possible overlap (two of three months).
- **The pilot's correlations reproduce exactly:** revenue 0.90 before 2023 and 0.58 after; headcount 0.83 and 0.33.
  - Across 11 variants they move by about ±0.1–0.2. The variants are other Accenture mappings, mean or revenue-weighted averages, annual data, and removing double counting.
  - The cleanest variant gives 0.91 / 0.60 / 0.81 / 0.32. **The periods were not misaligned.**
- **What the correlations mean is the real problem.**
  - Over 2016Q1–2020Q1 they are only 0.13 (revenue) and −0.09 (headcount). The high pre-2023 figure comes from the single 2021–22 boom and bust.
  - With only about five independent observations, 0.90 and 0.58 cannot be told apart statistically.
  - Within FY25–27 alone, the correlations are near zero.
- **The FY25–27 growth gap.** Indian firms grew about 2.4–2.9 pp less revenue than Accenture. This overlaps with Accenture's guided acquisition-driven growth: "a bit more than 3%" for FY25 and about 1.5% for FY26. These are guidance figures, not realized ones.

### The "missing" 2023

- FY23 isn't missing; it is split. Three quarters sit in "2015–22" and one in "FY24 slowdown". The table also mixes calendar-year and fiscal-year labels.
- **"FY25–27" has 9 quarters:** four in FY25, four in FY26 and one in FY27 (Q1FY27).
- 2021Q1–Q2 belong to no row, and "2015–19" actually runs to 2020Q1.
- No saved script produces the baseline rows. They reproduce only if the LTI business is counted up to three times (LTI, Mindtree and LTIMindtree).
  - With one LTI entity, baseline headcount growth is 9.9%, not 11.8%.
- **Recomputed by Indian fiscal year:**

| Year | Revenue growth | Headcount growth | Revenue per employee |
|---|---|---|---|
| FY23 | +13.7% | +14.3% | −0.6% |
| FY24 | +0.7% | −3.6% | +4.4% |
| FY25 | +2.6% | +0.1% | +2.6% |
| FY26 | +1.4% | +1.2% | +0.2% |

  - FY23 is the tail of the boom.
  - FY24 on its own is sharper than the pilot's 5-quarter window, which showed headcount at −1.8%.

### Headcount definitions

These were checked against the firms' sustainability reports (BRSR), annual reports and 20-Fs.

| Firm | What the headcount covers | Trainees |
|---|---|---|
| TCS, Infosys, HCLTech, LTIMindtree | Permanent staff only; contractors excluded. The fact-sheet figure equals the BRSR "Permanent" row | Included at Infosys (stated); not stated for the other three |
| Tech Mahindra | Also includes directly contracted staff and non-integrated subsidiaries | Not stated |
| Wipro, before FY18 | "Head Count" included contractors and retainers (181,482 vs 165,481 employees in March 2017). The repo correctly uses only the later series | Not stated |
| Wipro, now | The count doesn't reconcile with Wipro's own sustainability report | Not stated |

### Structural breaks

- **Handled correctly:**
  - the LTI–Mindtree merger (no splice);
  - HCLTech's fiscal-year change;
  - the HCLTech divestiture adjustment to headcount;
  - Wipro's FY17 definition change.
- **Weak:**
  - The LTI business is triple counted in the baseline row.
  - Inorganic growth is adjusted nowhere: Cognizant's Belcan (about 4 pp), Accenture's acquisitions, HCLTech–IBM in 2019, Wipro's Capco.
  - The HCLTech divestiture is removed from headcount but not from revenue.
- **Not logged before:**
  - A Wipro perimeter restatement that biases FY17 headcount growth by about −3 pp.
  - About 9,000 staff transferred to Wipro in Q2FY19 (the Alight deal).

### Corrected data

A new script, `scripts/audit/build_corrected.py`, applies every verified correction. It checks each old value before changing it and logs each change. With no corrections, its output is byte-identical to the original data.

## Task 2: Graphs (`figures/task2/`)

- `scripts/08_task2_graphs.py` regenerates all eight figures with one command: `cd scripts && python 08_task2_graphs.py`.
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

## Task 3: Price data (`price_data.md`, `price_calls_timeline.md`)

**Main conclusion: no public source measures g_p for Indian IT services in any period since 2015.**

### Official price indices

- **US.**
  - BLS has never published a producer price index for computer systems design services.
  - BEA's software price index is modelled from input costs plus an assumed productivity rate.
  - BEA's import price for computer services is built from US domestic indices.
- **UK, EU and Japan.** Their indices price hourly rates or revenue per person-month. That measures price per unit of *labor*, not per unit of *work*, and covers domestic sellers only.
- **India.** No IT services price index exists. The national accounts deflate IT output with goods or consumer price indices.

### Firm disclosures (`audit/price_firm_disclosures.csv`, 434 rows, each read from a document)

- **Infosys reported billed person-months and revenue per person-month in its 20-F every year from FY2003 to FY2020.** This gives billed effort directly, but not price.
  - The figures suggest Infosys's price growth was at most about −1% to −2% a year in FY15–17, and about 0% in FY18–20.
  - That holds only *if* labor per unit of work didn't rise. The bound is the agent's inference, not a sourced figure.
- Wipro disclosed volume vs price only for FY09–FY12.
- LTI disclosed billed person-months until 2022.
- TCS never disclosed pricing.
- Accenture's "pricing" means contract margin, not price.

### Analyst estimates

These are labelled estimated; some are secondhand via news reports.

- **Kotak:** about 3–3.5% a year of AI-led revenue deflation through FY28.
- **Jefferies:** about 20% over 2025–30.
- These figures *assume* clients get the savings, so they can't be used to test S3.

### Advisory firms

- **ISG** reports that contracted unit prices in managed-services deals historically fell 10–20% by year two of a contract. It says this has recently "doubled or even tripled". This is real price data, but it covers a narrow, mostly infrastructure slice. I verified the quote.
- **Everest Group, Gartner and HfS:** what is public is mostly per-FTE rates or paywalled.

### Earnings calls

- **Coverage:** 389 verbatim management statements from 183 transcripts, all eight firms, 2021–2026. Only TCS's Q4FY23 call is missing.
- **Timeline:**
  - 2021–22: rate-card increases.
  - Mid-2023: "no price expansion".
  - 2023–24: pricing "stable".
  - 2025: explicit pass-through of AI savings (LTIMindtree, TCS, Wipro, Infosys).
  - 2026: quantified. HCLTech cites 2–3% a year of portfolio deflation and "$100 million deal … maybe 80 million"; LTIMindtree cites about 15% less for the same scope.
- **How much weight to give it.** This is commentary, not measured prices, and many numbers are illustrative or forward-looking.
- **Reading.** Taken literally, it fits demand weakness (S1) in 2023–24, with S3-type pass-through starting only in 2025.

## Task 4: Other data that could separate the scenarios (`discriminating_data.md`)

### Subcontracting

Computed from the firms' filings by `scripts/audit/subcontracting_series.py`.

- Subcontracting cost as a share of revenue **fell at all six Indian firms in FY24**, by 1.3–2.9 pp. TCS went from 9.5% to 6.6%; I checked TCS against its fact sheet.
- It was flat to down in FY25 and rose slightly in FY26, but stays below FY22–23 levels.
- So work did not shift from employees to contractors (the subcontractor version of S4).

### What exists, and how far it helps

| Source | Helps with | What it shows |
|---|---|---|
| RBI census of foreign-owned companies' exports | S1 vs S4 | Exports rose from ₹6.54 to ₹8.45 lakh crore (FY22 → FY23). Foreign-owned vendors are included too |
| BEA data on US-owned affiliates in India | S1 vs S4 | 893k employed in professional services in 2023 |
| Naukri JobSpeak | S1 vs S4 | Now reports GCC postings next to IT services (Sep 2026: GCC +4%, IT −4%) |
| Firm client counts; onsite/offshore mix | Weak | The offshore share is rising, which leans weakly against S4 |
| Fresher hiring | Weak | Fell sharply after FY23; confounded by the earlier hiring boom |
| Anything public | S1 vs S3 | Nothing separates them |

### Not as described

- Nasscom-Zinnov GCC headcounts are restated consultancy estimates. They can't be chained into a trend.
- EPFO payroll data has only a coarse IT category and no ownership split.
- The RBI software-exports survey has no foreign-owned or GCC category.
- USCIS L-1 data by employer stops at FY2019.
- Cognizant and Accenture don't disclose a usable subcontracting figure.
- The repo's RBI file is missing FY2017-18, which does exist.

### Not collected publicly anywhere

Each item is listed in `discriminating_data.md` with the scenario pair it would separate.

- output-based prices per unit of scope;
- role-level headcount by firm;
- client-side work volumes;
- GCC headcount by parent company.

## Every change to the data

All changes are in new files under `data/corrected/` and logged in `CHANGELOG.csv`.

1. **Sign restored** on negative growth rates for Mindtree (16 cells) and LTI (6 cells).
2. **Cognizant attrition:** 29 → 18 (2021Q2) and 33 → 24 (2021Q3).
3. **Set to missing:** TCS 2007Q1 USD revenue and Wipro 2007Q1 headcount.
4. **Accenture USD revenue growth, 2017Q4–2018Q3:** 14.9 / 17.5 / 18.7 / 13.8 → 11.2 / 14.2 / 15.1 / 10.4.

Another 57 issues are flagged but not changed.

**Net effect:**
- Only 6 growth values differ.
- The pilot's episode table, correlations and simulation inputs are unchanged.
- I did not re-run the simulation.

## Open questions

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
