# f_j(h): task-length distributions by service line (touch-time hours)

Research note, 2026-11-07. Purpose: give count-weighted lognormal priors for the touch-time length of a "task" in each Indian IT/BPO service line. These priors feed the θ integral, where AI success falls steeply with task length (METR horizons). Every number below comes from a source I opened, or from my own computation on a dataset I downloaded. Guesses are labelled **[GUESS]**.

Notation: count-weighted task length h ~ LN(μ, σ), median m = e^μ. Hours-weighted distribution is LN(μ+σ², σ), so the hours-weighted median is m·e^{σ²}. Mean = m·e^{σ²/2}.

---

## 0. Headline proposal

| Line | Median h (low / **central** / high) | σ (low / **central** / high) | Implied mean h | Hours-wtd median h | Evidence weighting | Touch vs elapsed | Confidence |
|---|---|---|---|---|---|---|---|
| 1. AMS | 0.5 / **1.0** / 2.0 | 1.1 / **1.35** / 1.6 | 2.5 | 6.2 | count (Jira and SiP per-ticket logs); org-mean benchmarks | touch (worklogs) | medium |
| 2. App development | 4 / **8** / 16 | 1.3 / **1.5** / 1.8 | 25 | 76 | count (per-issue logs, story points) | touch (logs); SP are estimates | medium |
| 3. Testing / QA | 0.25 / **0.5** / 1.0 | 1.0 / **1.3** / 1.6 | 1.2 | 2.7 | mostly per-unit benchmarks, a few counts | touch | low |
| 4. Infra / IT ops | 0.25 / **0.5** / 1.0 | 1.0 / **1.2** / 1.5 | 1.0 | 2.1 | org-mean benchmarks (MetricNet), surveys | touch (work time); BPIC is elapsed | low-medium |
| 5. BPO | 0.08 / **0.15** / 0.3 | 0.95 / **1.1** / 1.4 | 0.27 | 0.50 | org-mean AHT; within-queue σ from call-level data | touch (AHT) | medium for voice/chat, low for back office |
| 6. Consulting / package impl. | 4 / **8** / 20 | 1.2 / **1.5** / 1.8 | 25 | 76 | count (SiP spec tasks); object-level estimates | mixed; mostly estimates | low (largely guess) |

What the central values imply:

| Line | p90 (h) | p99 (h) | Share of tasks > 8 h | Share of hours in tasks > 8 h |
|---|---|---|---|---|
| AMS (1.0, 1.35) | 5.6 | 23 | 6% | 43% |
| App dev (8, 1.5) | 55 | 260 | 50% | 93% |
| Testing (0.5, 1.3) | 2.7 | 10 | 2% | 20% |
| Infra (0.5, 1.2) | 2.3 | 8 | 1% | 13% |
| BPO (0.15, 1.1) | 0.6 | 1.9 | ~0% | ~1% |
| Consulting (8, 1.5) | 55 | 260 | 50% | 93% |

(App dev and consulting have the same central parameters but are derived separately.)

Three cross-cutting findings:

1. **σ is consistently 1.1 to 1.8 in every per-ticket software dataset.** Within one narrow queue (a call type, or bug fixes in one firm) σ ≈ 1.0 to 1.2. Pooling task types within a line adds dispersion, giving σ ≈ 1.4 to 1.9. The lognormal fits the upper tail well in the big datasets: for MariaDB bugs the predicted p99 is 99 h against an observed 98.5 h, and the predicted hours-weighted median is 29 h against 30.6 h observed.
2. **The hours-weighted median is 2 to 10 times the count median.** For development work it is about 10×. Most labor hours sit in tasks well above 8 h even when the typical ticket is 1 to 3 h. So the long tail drives θ more than the median does.
3. **Benchmarks mostly report org-level means, not within-org distributions.** MetricNet columns are average / min / median / max across organizations. The within-org dispersion therefore has to be borrowed from call-level data (Brown et al.) or ticket-level logs (Jira, SiP).

---

## 1. Datasets I downloaded and analysed

All raw files are in their own directories under the session scratchpad (`.../scratchpad/{jira_raw,redhat_raw,rubin_raw,sip_raw,bpic14_raw}`). Scripts are in `.../scratchpad/scripts/`, and every script was run with `python3 -I`. "σ" is the SD of log hours. "σ_IQR" is the log-IQR divided by 1.349, a robust check. "HW-med" is the empirical hours-weighted median.

### 1a. SiP effort dataset: commercial software house, actual hours per task
- Source: https://github.com/Derek-Jones/SiP_dataset (file `Sip-task-info.csv`). The README describes the data in Jones & Cullum, arXiv:1901.01621. Software in Partnership Ltd is a UK firm building insurance/financial software for clients. Each task has `HoursEstimate` and `HoursActual`.
- 10,266 distinct tasks (I took the first row per TaskNumber, since `HoursActual` is task level). **Count-weighted, touch time** (developer-logged actual hours).

| Subcategory | n | median | p10 | p25 | p75 | p90 | p99 | σ | σ_IQR | HW-med |
|---|---|---|---|---|---|---|---|---|---|---|
| Bug | 2075 | 1.5 | 0.5 | 0.75 | 3.5 | 7.5 | 36 | 1.15 | 1.14 | 7.8 |
| Support (Development) | 1045 | 0.8 | 0.25 | 0.33 | 2.5 | 7.0 | 47 | 1.27 | 1.50 | 12 |
| Client Support | 616 | 1.0 | 0.25 | 0.5 | 3.5 | 10.8 | 107 | 1.45 | 1.44 | 81 |
| In-house Support | 1137 | 2.5 | 0.7 | 1.25 | 6.0 | 14 | 62 | 1.22 | 1.16 | 31 |
| Enhancement | 2592 | 4.2 | 0.65 | 1.5 | 12.5 | 33.5 | 170 | 1.52 | 1.57 | 53 |
| Testing | 200 | 4.5 | 0.75 | 1.5 | 13.5 | 37.7 | 111 | 1.47 | 1.63 | 100 |
| Release | 457 | 3.0 | 0.5 | 1.0 | 7.25 | 16 | 48 | 1.36 | 1.47 | 16 |
| Business Specification | 95 | 2.5 | 0.5 | 1.0 | 7.0 | 12 | — | 1.41 | 1.44 | 36 |
| Technical Specification | 61 | 2.25 | 0.75 | 1.0 | 5.1 | 13 | — | 1.18 | — | — |
| Consultancy (Operational) | 50 | 1.75 | 0.48 | 0.75 | 4.9 | 11.8 | — | 1.41 | — | — |
| Conversion | 75 | 9.3 | 2.0 | 4.0 | 30 | 88 | — | 1.49 | — | — |
| All Development | 6918 | 2.5 | 0.5 | 1.0 | 7.0 | 19 | 122 | 1.47 | 1.44 | 43 |
| All Operational | 1787 | 2.0 | 0.5 | 1.0 | 5.0 | 13 | 86 | 1.34 | 1.19 | 39 |

- Estimates against actuals: SD of log(actual/estimate) = 0.77 (bugs), 0.88 (enhancements), 0.85 (all). The median ratio is 1.0. σ of estimates (1.05 / 1.42) is about 0.1 below σ of actuals (1.15 / 1.52), so estimate-based distributions such as story points understate σ by roughly 0.1.

### 1b. Public Jira instances: logged `timespent` per issue (live REST API, pulled 2026-11-07)
These are three of the 16 instances in the Montgomery et al. (2022) Public Jira Dataset (https://arxiv.org/abs/2201.08368: 16 instances, 1,822 projects, about 2.7M issues). I queried the live instances directly rather than downloading the MongoDB dump. JQL used: `timespent > 0`. **Count-weighted, touch time** (sum of all worklogs on the issue, which may include several people).

- **MariaDB** (https://jira.mariadb.org/rest/api/2/search; all 25,839 issues with logged time). I spot-checked worklogs: they are human entries, for example "Filing this bug, devising fix." Engineers at MariaDB plc / Foundation.

| Type | n | median | p10 | p25 | p75 | p90 | p99 | σ | σ_IQR | HW-med |
|---|---|---|---|---|---|---|---|---|---|---|
| Bug | 19,876 | 2.9 | 0.5 | 1.0 | 8.0 | 20.5 | 98.5 | 1.52 | 1.54 | 30.6 |
| Task | 4,096 | 8.0 | 1.0 | 2.0 | 22.5 | 60 | 306 | 1.69 | 1.79 | 94 |
| New Feature | 1,176 | 14 | 1.0 | 3.5 | 45 | 137 | 494 | 1.84 | 1.90 | 176 |
| New Feature (resolved) | 952 | 16 | 1.5 | 4.0 | 46 | 128 | 352 | 1.70 | 1.81 | 140 |
| Technical task | 396 | 3.0 | 0.5 | 1.0 | 9.1 | 40 | 246 | 1.75 | 1.64 | 96 |

- **Atlassian public tracker** (https://jira.atlassian.com/rest/api/2/search; all 5,226 issues with logged time; mostly Crucible, Jira Server, FishEye and Bamboo).
  Bug: n=2,411, median 1.75, p90 8.0, p99 20, σ 1.43, HW-med 6.0. Suggestion: n=2,412, median 4.0, p90 18, σ 1.54. Sub-task: n=397, median 4.0, σ 1.56.
- **Red Hat** (https://redhat.atlassian.net/rest/api/3/search/jql; anonymous access shows only 2,885 issues with logged time, mostly JBoss/middleware).
  Bug: n=914, median 2.0, p90 18, σ 1.84. Task: n=862, median 8.0, p90 38, σ 1.54. Story: n=406, median 16, p75 40, p90 90, σ 1.92. A few absurd entries (e.g. an Epic at 200k h) distort the mean, so I use quantiles only.
- **Apache** (https://issues.apache.org/jira/rest/api/2/search) is **not usable**. Of 107,597 issues with `timespent>0`, 104,605 have worklogs by `githubbot`, which auto-logs 10 min per PR event. Anyone using Montgomery's Apache subset for effort must drop bot worklogs.
- Caveats for all Jira logs:
  1. Selection: only issues where someone chose to log time. Trivial issues are probably under-represented, which pushes the median up.
  2. Rounding heaps at 0.5/1/2/4/8 h.
  3. These are product-company engineers fixing their own code, not a services vendor on a client's code. A vendor adds handover, environment access and client communication, but also takes on many trivial service requests.

### 1c. Rubin Observatory (LSST) Data Management Jira: story points
- https://rubinobs.atlassian.net/rest/api/3/search/jql, project DM, status Done, Story Points not empty. I pulled the 30,000 most recent (2017-07 to 2026-11); 28,640 have SP > 0.
- Definition (https://developer.lsst.io/work/flow.html): "One story point is an idealized half day of uninterrupted work by a competent developer". "A common velocity in DM is 0.7". So 1 SP ≈ 4 h of touch time (≈ 5.7 h of paid time).
- Story: n=23,268, SP median 2.0 (≈ 8 h), p25 1, p75 4, p90 8, p99 21, σ 0.98. Bug: n=2,046, median 1 SP (≈ 4 h), σ 0.85. Improvement: median 2 SP, σ 0.96.
- **Count-weighted, but these are estimates.** Following SiP (§1a), the σ of actuals is likely about 0.1 higher, plus extra spread from the SP-to-hours conversion. The Fibonacci-like grid also compresses the tails.

### 1d. BPI Challenge 2014 (Rabobank ICT, HP Service Manager): ITIL incidents
- Dataset page https://data.4tu.nl/datasets/a752c1b5-9732-4bbc-8949-bf24581f9034; file `Detail_Incident.csv` (MD5 verified b0608464...). 46,605 incidents and requests-for-information.
- The field `Handle Time (Hours)` has median 3.9 h (p25 0.9, p75 16.5, p90 48). Open-to-resolved elapsed time has median 18.4 h. The median ratio of handle time to elapsed time is 0.32, about the business-hours fraction of a calendar day, and for many tickets handle time equals elapsed time. **This is elapsed (business-hours) time, not touch time.** Use it only as an upper bound for infra/AMS incident touch time. I did not find a definition of the field.

---

## 2. Benchmarks and literature (opened)

### ITSM / service desk / desktop support. MetricNet 2023 benchmark roundups
- MetricNet "Benchmarking roundup: summary of 2023 service and support benchmarks" (https://www.brighttalk.com/resource/core/447335/benchmarking-roundup---summary-of-2023-service-and-support-benchmarks-v3_954461.pdf). Columns are Average / Min / Median / Max **across peer organizations**, so these are org-level means, not task distributions.
  - Service desk handle time (min): inbound voice 10.78 / 3.30 / 10.50 / 19.86. Chat 13.42 / 3.72 / 13.69 / 26.93. Web ticket/email 13.70 / 3.80 / 13.77 / 24.91.
  - Desktop support: **average incident work time 31 min** (min 14, median 25, max 75). **Average service-request work time 98 min** (21 / 92 / 274). Travel time per ticket 34 min. Tickets per technician per month 74 (median 68). Technician utilization 53.6%.
  - Desktop support **elapsed** times: MTTR for incidents 16.9 business hours (median 13.4). Mean time to fulfil SRs 7.6 business days. Touch time is therefore about 3% of elapsed time for incidents.
- HDI / Rumburg, "Metric of the month: ticket handle time" (https://thinkhdi.com/library/supportworld/2019/metric-of-month-ticket-handle-time): industry-average handle time of 8.6 min across all service desks. Password resets take 1 to 3 min. Complex business-application tickets (Oracle/SAP) take "15 minutes or more". Handle time = talk + after-call work. It also notes that handle time ≠ MTTR.

### Contact centre / BPO
- MetricNet 2023 contact-center roundup (https://www.brighttalk.com/resource/core/444634/benchmarking-roundup---summary-of-2023-contact-center-benchmarks-v2_949577.pdf). Columns are Avg / Min / Median / Max across centres. Voice handle time 8.03 / 3.65 / 6.99 / 16.51 min. Chat 11.21 / 3.41 / 9.81 / 37.05. Web/email 8.01 / 3.32 / 7.07 / 19.07.
- **Brown, Gans, Mandelbaum et al. (2005, JASA), "Statistical Analysis of a Telephone Call Center"** (https://faculty.wharton.upenn.edu/wp-content/uploads/2012/04/Brown-etal-CCdata.pdf). Service times are close to lognormal, and lognormality also holds within service type, priority and individual agent (§4.3). Table 1, Nov–Dec, truncated at 1 h:
  - Overall: mean 201 s, SD 248 s, median 124 s.
  - By type: regular service mean/median 179/121 s; Internet consulting 401/221 s; stock trading 270/175 s.
  - Implied σ: from mean/median, σ² = 2 ln(201/124) → **σ = 0.98**; from the CV, σ² = ln(1 + 1.234²) → **σ = 0.96**. This is the best available anchor for **within-queue** σ of BPO contacts. It is count-weighted touch time (service time = agent talk time).
- Umbrex AHT page (https://umbrex.com/resources/company-analysis/customer-service-support/average-handle-time/). Unsourced practitioner ranges: voice 4–6 min (Tier 2/3 8–15+). Chat 6–10 min active. **Email/ticket 15–30 min cumulative agent work per case, with complex cases "45–90 minutes across multiple touches"**. B2B SaaS email 20–40 min.
- Back office:
  - APQC via Procurify (https://www.procurify.com/blog/the-4-kpis-your-accounts-payable-team-should-be-tracking-immediately/): invoices per AP FTE per year are 24,284 (top), **9,483 (median)** and about 5,000 (bottom). At about 1,700 productive h/FTE-year that is **≈ 11 min per invoice** at the median and 20 min at the bottom (my arithmetic; it includes all AP overhead).
  - IBM / Salient case (https://www.ibm.com/case-studies/salient): staff were "processing only 15 claims per day" manually, i.e. about 30 min per claim (claim type unspecified; vendor case).
  - Docketry TPA case (https://www.casestudies.com/company/docketry/case-study/insurance-tpa-improves-operational-efficiency-and-customer-satisfaction-with-docketry): about 20 min per claim of manual document handling (vendor).
  - KYC remediation, AML Intelligence sponsored piece on Steward (https://www.amlintelligence.com/2026/07/insight-stewards-ai-agents-cuts-kyc-remediation-to-under-5-minutes-a-file/): manual review "takes an analyst between 30 minutes and three hours", baseline 45 min per file.
  - Encompass (https://www.encompasscorporation.com/encompass-customers/kyc-corporate-banking/): "13 hours saved per analyst per case" for corporate/investment-bank KYC, which implies manual CIB KYC cases of 13+ h (vendor marketing).
  - These form the back-office long tail: data entry and AP run minutes, claims tens of minutes, KYC files 0.5–3 h, and CIB KYC 10+ h.

### Security / NOC alerts (infra)
- Prophet Security, State of AI in the SOC 2026 (https://www.prophetsecurity.ai/blog/state-of-ai-in-the-soc-2026), survey of 250 respondents: "A thorough investigation averages about 75 minutes, with a median near 45." Dwell before pickup averages 55 min (median 23); that is elapsed time and should not be used. Self-reported, vendor survey.

### Testing / QA
- Dwarakanath et al. (Accenture Labs Bangalore), ICST 2017, "Accelerating Test Automation through a Domain Specific Language" (https://arxiv.org/pdf/1809.08100), Table 2, a real client project. Estimated Selenium authoring time per test scenario: **8–15 h** (low-complexity 8, high 11–15). Actual times for project automation engineers using the DSL were 6–10 h.
- Alégroth et al., visual GUI testing industrial case (https://arxiv.org/pdf/2005.09303), Tables 5–6. Script development effort per suite of 5–42 test cases was 10–187 min, i.e. **a few minutes per automated test case** for converting existing manual cases on simple apps.
- QA Wolf (https://www.qawolf.com/lifecycle-of-a-test), from "3.5 million automated test runs" and 100k+ tests (vendor): average test creation **95 min**, maintenance 45 min, failure investigation 17 min, bug reporting 30 min, test run 9 min.
- Inflectra whitepaper (https://inflectra.com/Ideas/Whitepaper/Incorporating-Automated-and-Manual-Testing-In-An-Effective-Test-Plan.aspx): "the normal 15-20 minutes" to write a manual test case by hand.
- ESPRET (Tahvili et al., JSS 2018; https://www.es.mdu.se/pdf_publications/5223.pdf): a Bombardier dataset of 1,187 test steps/cases with highly right-skewed execution times (skewness 3.8–5.2). The values are seconds-scale machine-timed steps, so not directly usable for human touch time.
- SiP "Testing" tasks (§1a): median 4.5 h, σ 1.47. These are bundled testing work items, not individual test cases.

### Consulting / package implementation
- QSM / Beckett, "Parametric Estimation for ERP Implementations" (https://ndia.dtic.mil/wp-content/uploads/2011/CMMI/Thursday12962.pdf). RICEF gearing factors in implementation units, not hours:
  - Reports: simple / average / complex = 100 / 200 / 300.
  - Interfaces: 320 / 620 / 1520.
  - Conversions: 100 / 200 / 300.
  - Enhancements: 100 / 500 / 1000.
  - Forms: 100 / 200 / 300.
  - A configured "average table" is 43 units.
  - Useful for **relative** spread: the simple-to-complex ratio is 3–10× within an object type, and the range across types is about 15×. Treating simple/complex as roughly p15/p85, within-type σ ≈ ln(3 to 10)/2 ≈ 0.55–1.15. Pooling types adds more.
- Kilgore et al., ICEAA 2019, ERP estimation (https://www.iceaaonline.com/wp-content/uploads/2019/06/SW05-The-Journey-to-Better-ERP-Estimation-Kilgore.pdf): RICEFW complexity is "typically simply defined (e.g. Low, Medium, High) and not always consistent". No hour table.
- SAP Community threads on ABAP/RICEF estimates returned HTTP 403, so **not opened**. Search snippets claimed "simple 5–6 days, medium 8–9, complex 15–18 days" and "4 / 7 / 10 man-days" per object, including spec, build and unit test. **Unverified, do not cite.**

### AMS-specific
- CGI, ICEAA 2024, "Power of ML for Application Maintenance" (https://iceaaonline.com/wp-content/uploads/2024/09/ITS24-vanderVliet-Power-of-ML-for-Application-Maintenance-ppt.pdf). Qualitative only: AM ticket effort data are "extremely right-skewed". Some logged values are "over 10 – 100 times the median", which CGI treats as registration errors. Effort is predicted per engagement × ticket type × priority.
- IBM Research (Li & Katircioglu, IEEE SCC 2013; IJBPIM 2014, "Estimating and applying service request effort data in application management services"). This is the closest match to Indian-delivered AMS ticket effort. Full text is on ResearchGate (403), so **not opened**; its distribution is unknown.
- Indian-firm disclosures: none found with per-ticket effort. HCLTech and Wipro case studies report aggregate savings only. **Gap.**

---

## 3. Derivations, line by line

### 1. AMS (incidents, bug fixes, minor enhancements, service requests)
- Touch-time anchors for software bug fixes: SiP bugs median 1.5 h (σ 1.15); Atlassian bugs 1.75 h (σ 1.43); Red Hat bugs 2.0 h (σ 1.84); MariaDB bugs 2.9 h (σ 1.52).
- Support/SR-like tasks: SiP Support 0.8 h, Client Support 1.0 h (σ 1.27–1.45).
- Desktop-support analogue: MetricNet incident work time averages 0.5 h and SR work time 1.6 h. These are org means; within-org medians would be lower.
- Real AMS queues hold many short SRs (data fixes, job reruns, access, reports) that the logged-time Jira samples under-represent, alongside minor enhancements of several days.
- **Central median 1.0 h, σ 1.35.** Low (0.5, 1.1) is a queue dominated by L1.5 service requests. High (2.0, 1.6) is a queue dominated by L3 bug fixes, the MariaDB-like case.
- Implied hours-weighted median is about 6 h, and about 43% of hours sit in tickets over 8 h. **The minor-enhancement tail matters for θ.**

### 2. Application development (stories, features, integration)
- SiP Enhancement median 4.2 h (σ 1.52). Rubin DM story median 2 SP ≈ 8 h (σ_est 0.98, so ≈ 1.1 for actuals). MariaDB Task 8 h (σ 1.69). Red Hat Task 8 h (σ 1.54) and Story 16 h (σ 1.92). MariaDB New Feature 14–16 h (σ 1.7–1.84).
- Granularity matters a lot. A sub-task or technical task has a median of about 3–4 h; a user story about 8–16 h; a "feature" about 15+ h.
- **Central: median 8 h at story/task level, σ 1.5. Low (4, 1.3) is sub-task granularity; high (16, 1.8) is story/feature granularity.**
- The hours-weighted median is about 76 h, i.e. most dev hours sit in multi-day items. This is the line where the METR horizon bites hardest.

### 3. Testing / QA
- The unit of work is mixed:
  - manual test-case writing: 15–20 min (Inflectra);
  - test execution: minutes to tens of minutes, mostly unsourced blogs (not used);
  - defect investigation and reporting: 17 + 30 min (QA Wolf);
  - automated test creation: 95 min average (QA Wolf, Playwright), up to 8–15 h for complex enterprise Selenium scenarios (Accenture);
  - bundled testing tasks: SiP median 4.5 h, σ 1.47.
- At per-test-case granularity, executions and design dominate the count. **[GUESS]: central median 0.5 h, σ 1.3. Low (0.25, 1.0), high (1.0, 1.6).**
- If the model instead treats a testing "task" as a work item like the SiP Testing tasks, use median ≈ 4 h, σ ≈ 1.5. **The choice of unit matters more than the evidence does.** Pick the unit that matches how θ_j's AI-success curve is defined (one autonomous agent run).

### 4. Infrastructure / IT operations
- MetricNet desktop support: incident work time averages 31 min (org median 25); SR work time 98 min (org median 92). Service desk handle time is 8.6–14 min. SOC alert investigation: median about 45 min, mean 75 (survey).
- Changes and patching: no measured benchmark found. One hypothetical example said "two hours" for a standard change (GIVA blog, seen only in search; not used as data).
- BPIC 2014 "handle time" median 3.9 h is elapsed business-hours time, so it is only an upper bound. SiP In-house Support median 2.5 h (σ 1.22) is a mixed bag.
- **Central median 0.5 h, σ 1.2**, which gives mean ≈ 1.0 h, consistent with the 31/98-min MetricNet means for an incident/SR mix. Low (0.25, 1.0) is alert- and incident-heavy; high (1.0, 1.5) is change/project-heavy L2/L3 data-centre work. The σ is a **[GUESS]**: within-queue σ ≈ 1.0 (Brown analogue), plus extra for mixing.

### 5. BPO / business process services
- Voice: org-median AHT 7.0 min (contact centres), 10.5 min (service desks). Chat 9.8–13.7. Email 7.1–13.8, or 15–30 min per case per Umbrex. Within queue σ ≈ 0.97 (Brown et al.).
- Back office: AP about 11 min per invoice, claims 20–30 min, KYC files 0.5–3 h, CIB KYC 13+ h.
- Count-weighted pooling for a typical Indian BPO mix (contact-heavy plus F&A/insurance back office): **central median 0.15 h (9 min), σ 1.1.** Low (0.08 h ≈ 5 min, 0.95) is a voice-heavy book. High (0.3 h, 1.4) is a back-office/KYC-heavy book.
- The hours-weighted median is about 30 min. Essentially no hours are in tasks over 8 h, except CIB KYC / complex claims, which a high σ partly captures. **Medium confidence for contact centres, low for back office.**

### 6. Consulting / package implementation (SAP/Oracle/Salesforce)
- Small work items: SiP spec/consultancy tasks have medians of 1.75–2.5 h (σ 1.2–1.4).
- Object level: SAP RICEF objects are multi-day builds. QSM gearing factors show a 3–10× simple-to-complex spread within a type and about 15× across types. The day counts in SAP forums are unverified.
- Configuration items (tables, org structures) are probably hours each. Solution design and workshops are days.
- **[GUESS]: central median 8 h, σ 1.5. Low (4, 1.2) is configuration-item granularity; high (20, 1.8) is RICEF-object / design-document granularity.** This is the weakest line. A per-object effort sample from an SI (e.g. a WRICEF tracker with actuals) would be the single most valuable addition.

---

## 4. Caveats that apply across lines
1. **Touch vs elapsed time.** All the "central" numbers are touch/work time: worklogs, AHT, MetricNet work time. Elapsed resolution times run 5–30× longer (MetricNet MTTR 16.9 business hours vs 31 min of work; BPIC elapsed median 18 h). Never mix them.
2. **Count vs hours weighting.** Every dataset and benchmark here is count-weighted, i.e. per task or per contact. Hours-weighted medians are given for reference only. The empirical values match the lognormal m·e^{σ²} formula well for MariaDB (30.6 vs 29) and SiP Enhancement (53 vs 42).
3. **Org-level vs task-level.** MetricNet and APQC give dispersion of org means, not of tasks. Task-level σ came from SiP, Jira, Rubin and Brown et al.
4. **Selection.** Logged-time Jira subsets omit unlogged (often trivial) issues, which biases medians up. Vendor case studies favour slow manual baselines.
5. **Granularity is a modelling choice.** The median moves by 2–4× between sub-task, story and feature, or between test case and testing work item. σ is more stable (1.1–1.9 across all software samples).
6. **No India-specific task-level data found.** Indian firms do not disclose per-ticket effort. The closest is Accenture Bangalore's test-automation case and IBM AMS research (not opened).
