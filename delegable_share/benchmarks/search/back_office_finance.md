# Benchmark search: back office, finance & accounting, documents, spreadsheets, healthcare admin

Searched 2026-11-09. Everything below was checked against a primary page (paper, official leaderboard, or GitHub repo) unless marked **[unverified]**. Model names are copied as the sources print them. Aggregator sites (benchlm, benchmarklist, llm-stats) disagree with each other, so I used them only as leads.

**Headline.** One benchmark in this area already supports a METR-style fit without new data collection: the **Vals Finance Agent Benchmark**. Its public CSVs carry an `Expert time (mins)` field for every item (v1.1: 50 items, 2–60 min, median 10; v2: 27 items, 15–120 min, median 40). The Vals leaderboard HTML embeds per-category accuracy for every model (57 models on v1.1, 39 on v2.1). A rough bucketed fit I ran (described in section 1) gives 50% horizons rising from about 9 min (Claude 3.7 Sonnet Thinking, Feb 2025) to about 25 min (Claude Opus 4.6 Thinking, Feb 2026). Treat these numbers as illustrative only.

Nothing in this area has been time-horizon-analysed by METR. The Kwa & Cheng cross-domain post (metr.org, 2025-07-14) covers METR-HRS, SWE-bench Verified, OSWorld, WebArena, Mock AIME, MATH, LiveCodeBench, GPQA, Video-MME, Tesla FSD and RLBench. It includes no finance, spreadsheet, accounting, medical or document benchmark. I found no Epoch horizon estimate for this area either.

---

## 1. Vals AI Finance Agent Benchmark (FAB v1.1; v2 / v2.1)
- **Paper/URL:** arXiv 2508.00828; https://www.vals.ai/benchmarks/finance_agent_v1 (archived v1.1); https://www.vals.ai/benchmarks/fabv2-1; data: github.com/vals-ai/finance-agent and github.com/vals-ai/finance-agent-v2
- **Release:** v1 in spring 2025 (paper Aug 2025). v1.1 is archived as saturated. v2 came in 2026, and the v2.1 leaderboard is dated 2026-11-09.
- **Maintainer:** Vals AI. Questions written by ex-bulge-bracket analysts.
- **Item:** An analyst-style research question answered with EDGAR search, web search, HTML parsing, retrieval and calculator tools. Example: "Compare Home Depot and Lowe's FY2024 inventory efficiency and calculate the difference in days inventory outstanding."
  - v1.1: 537 questions in 9 categories (Simple retrieval quant/qual, Numerical reasoning, Complex retrieval, Adjustments, Beat-or-miss, Trends, Financial modelling, Market analysis); 50 are public.
  - v2: 927 questions (27 public, 450 private validation, 449 test) in 9 categories (General qualitative/quantitative, Market analysis, Comparables, Precedents, Adjustments, Earnings, Disclosure, Financial modelling).
- **Domain tag:** text (agentic tool use)
- **Resembles:** Equity research and financial analyst KPO work (a large Indian KPO segment), plus parts of FP&A. Not clerical bookkeeping.
- **Human times:** **Per-item expert estimates in the public CSVs.** I downloaded both files.
  - v1.1 public (n=50): min 2, median 10, mean 12.6, max 60 min. Category medians: retrieval and numerical reasoning 5; adjustments and beat-or-miss 10; trends 15; complex retrieval 20; financial modelling 22.5; market analysis 30.
  - v2 public (n=27, 3 per category): min 15, median 40, mean 43.5, max 120 min. Category medians: General quantitative 20; Earnings and Precedents 30; Adjustments, Comparables and General qualitative 40; Market 45; Disclosure 60; Financial modelling 80.
  - Measurement: the paper reports experts averaged 16.8 min per v1 question (1010.5 s, "time spent directly answering"), which suggests the times were measured or logged. The CSV column may still be a self-estimate. I couldn't confirm which.
  - Test-set per-item times are not public.
- **Model results over time:**
  - v1.1: 59 models covering roughly the Claude 3.5/GPT-4o era through Feb 2026. Top: Claude Opus 4.6 Thinking 60.65%, GPT 5.1 56.55%, Claude Sonnet 4.5 Thinking 55.3%. The paper version had o3 at 46.8%.
  - Dated snapshot pages exist (e.g. /finance_agent-05-30-2025, -07-17-2025, -09-29-2025).
  - v2.1 (39 models, 2026-11-09): Claude Fable 5.2 69.47%, Claude Opus 5.5 67.85%, Gemini 4 Argon 67.66%, GPT-6.1 Sol 61.82%.
- **Item/subset-level:** **Per-category accuracy, stderr, latency and cost for every model** is embedded in the leaderboard page HTML (found in the `"tasks"` / `"<category>":{"<model>":{"accuracy":…}}` JSON). I parsed 57 models on v1.1 and 39 on v2.1. Per-item results are not public, except for sample transcripts on the page.
- **Grading:** Rubric checks scored by an LLM judge. v2.1 uses a 3-model jury, dealbreaker-gated partial credit plus an all-pass metric, and a 2-hour cap per task.
- **Horizon computed already?** Not by METR or Epoch. **My rough pass:** a weighted logistic of category accuracy on log2(category median public expert minutes), per model, using v1.1 category counts as weights.

  | Model | H50 | Slope (per doubling) |
  |---|---|---|
  | Claude 3.7 Sonnet Thinking | ~9 min | −0.66 |
  | o3 | ~10 min | −0.39 |
  | Claude Sonnet 4.5 | ~11 min | −0.44 |
  | GPT-5.2 | ~15 min | −0.41 |
  | Claude Opus 4.5 Thinking | ~17 min | −0.39 |
  | GPT-5.1 | ~20 min | −0.32 |
  | Claude Opus 4.6 Thinking | ~25 min | −0.41 |

  Caveats: category medians come from only 3–9 public items each; category is confounded with difficulty; and the slopes are shallow next to METR's.
- **Verdict: INCLUDE.** It is the best-instrumented benchmark in this area. Two gaps remain:
  1. The times are category-level, with per-item times only on the public split. To close: email Vals for test-set `Expert time (mins)` and per-item scores, since they clearly hold both.
  2. It measures analyst work, not clerk work.
- **Sources:** https://arxiv.org/abs/2508.00828 ; https://arxiv.org/html/2508.00828 ; https://www.vals.ai/benchmarks/finance_agent_v1 ; https://www.vals.ai/benchmarks/fabv2-1 ; https://raw.githubusercontent.com/vals-ai/finance-agent/main/data/public.csv ; https://raw.githubusercontent.com/vals-ai/finance-agent-v2/main/data/public.csv

## 2. FrontierFinance
- **Paper/URL:** arXiv 2604.05912, "A Long-Horizon Computer-Use Benchmark of Real-World Financial Tasks". Krumdick, Reddy, … Tanner (Kensho/S&P authors, the FinanceBench/DocFinQA lineage; affiliation **[unverified]**).
- **Release:** 2026-04-07
- **Item:** Build a client-ready financial model in Excel plus a PPT memo, e.g. an LBO of Electronic Arts (sources and uses, debt schedule, returns, sensitivities). 25 tasks across 5 model types (M&A, three-statement, LBO, lender, DCF).
- **Domain tag:** computer_use (Excel + PowerPoint)
- **Resembles:** Financial modelling and IB/PE analyst work (KPO). Too long to stand in for back-office transactions, but useful as the long-task anchor.
- **Human times:** **Per-task measured times for 10 tasks** (Table 3): 6.5–35 h, mean 18.3 h, median about 19 h. Experts had estimated 12.5 h; observed times ran about 31% higher. Estimated hours by model type: DCF 8–10, lender 10–12, LBO 11–15, M&A 12–16, three-statement 13–16. Humans were asked not to use plug-ins or automation.
- **Model results:** GPT-5.4, Opus 4.6, Sonnet 4.6 and Gemini 3.1 Pro, all at one date (spring 2026).
  - Human-graded on 10 tasks: experts 77.2, GPT-5.4 70.9, Opus 4.6 61.8.
  - LLM-judge on 25 tasks: GPT-5.4 87.5, Sonnet 4.6 84.0, Opus 4.6 83.0, Gemini 3.1 Pro 63.5.
- **Item-level:** Per-task human-graded scores for 10 tasks are in Table 3.
- **Grading:** Expert rubrics with human graders (r=0.965 against the expert); an LLM judge as secondary.
- **Horizon computed?** No.
- **Verdict: CANDIDATE.** It has per-task measured times, but only 4 models at one date, scores are continuous rubric percentages rather than pass/fail, and the code and data are "forthcoming". To close: wait for the release and rerun older models. Its per-type hour estimates could also calibrate EMB task families (section 3).
- **Sources:** https://arxiv.org/abs/2604.05912 ; https://arxiv.org/html/2604.05912v1

## 3. Vals Excel Modeling Benchmark (EMB v1.0 / v1.1)
- **URL:** https://vals.ai/benchmarks/emb ; public sample at github.com/vals-ai/emb-public-dataset
- **Release:** 2026-07-01 (per letsdatascience **[unverified]**); page updated 2026-10-20.
- **Maintainer:** Vals AI
- **Item:** Build a full IB/PE Excel model from a prompt plus source files. Example: a SaaS customer-retention cohort model with 4 tabs and IB formatting, checked on cells such as Q1-2018 cohort ARR at Dec-19 = $24,640. 103 questions (51 test). Families: LBO, DCF, M&A, Operating, Comps, Dataroom, Misc.
- **Domain tag:** software (spreadsheet generation)
- **Resembles:** Financial modelling and spreadsheet-heavy KPO.
- **Human times:** Aggregate only: each task is "expected to take human experts a minimum of 5 hours".
- **Model results:** 71–77 models. Top: Claude Fable 5.1 76.67%, Claude Opus 5.5 75.94%, Claude Sonnet 5.5 75.71%, GPT-5.6 Sol 72.34%. Lowest: Gemini 3.1 Flash Lite Preview 8.63%. Covers roughly early 2026 to now.
- **Subset-level:** Per-family accuracy (LBO, DCF, M&A, …) and template-vs-scratch mode for every model is embedded in the page JSON.
- **Grading:** Template mode scores the share of cells matching the gold model; scratch mode uses rubric checks judged by an agentic LLM. Workbooks are recalculated in Excel; 3.5 h cap per run.
- **Horizon computed?** No.
- **Verdict: CANDIDATE.** Its family-level results could be paired with FrontierFinance per-type hour estimates to give family-level lengths. The gap is that all items are long (≥5 h), so the curve has no short end. Pool it with FAB.
- **Sources:** https://vals.ai/benchmarks/emb ; https://www.vals.ai/benchmarks/finance_index

## 4. APEX-Accounting (Mercor × Ramp)
- **Paper/URL:** arXiv 2607.27189; https://www.mercor.com/blog/introducing-the-ai-productivity-index-for-accounting/ ; human-baseline study at https://www.mercor.com/blog/human-baselines-for-benchmarks-ai-now-outperforms-junior-accountants/
- **Release:** 2026-07-30/31. Human-baseline post 2026-10-01.
- **Maintainer:** Mercor (Vidgen, Foody et al.) with Ramp
- **Item:** A synthetic company "world" frozen at month-end close, with an accounting system, spreadsheets and PDFs. The agent reconciles accounts, accrues expenses, posts transactions and produces reports. 160 private tasks across 10 worlds, in 4 categories: Reconciliation, Data Entry, Variance Analysis, Schedules & Accruals. A public sample of 10 tasks from 1 world is on Hugging Face.
- **Domain tag:** mixed (agent in software tools and files)
- **Resembles:** **The closest match to the BPO accounting list:** GL posting, bank and account reconciliation, accruals, month-end close, AP/AR data entry.
- **Human times:** None on the main set. The baseline study gave simplified versions of 4 month-end-close tasks to 12 licensed CPAs (about 5.5 years' experience). Most attempts took **30–180 min**; humans averaged about 37% while Claude Opus 5 scored 100% in under 10 min. No per-task times in the blog; the linked paper **[not read]**.
- **Model results:** 9 frontier models at one date (July 2026), Mean Criteria@3: Claude Fable 5 56.4%, Muse Spark 1.1 52.6%, GPT-5.6 Sol 51.5%, Qwen 3.5 24.4%. Best Pass^8 is 2.6%; 93/160 tasks were never fully solved by any model.
- **Item-level:** No, the test set is hidden. Category-level results are in the paper **[not checked in detail]**.
- **Grading:** Expert binary rubrics (mean 13.7 criteria per task); an open-source LLM judge with 97% agreement against experts.
- **Horizon computed?** No.
- **Verdict: CANDIDATE (high priority).** Its task content is exactly right. Gaps: no per-task times, a single date, a private set. To close: ask Mercor (they run on request) for per-task expert time estimates (APEX-Agents had them) and per-task pass rates. Alternatively, time humans on the public 10-task world.
- **Sources:** https://www.alphaxiv.org/abs/2607.27189 ; Mercor pages above

## 5. DualEntry Accounting AI Benchmark ("DualBench100")
- **URL:** https://www.dualentry.com/accounting-ai-benchmark ; https://www.dualentry.com/benchmark
- **Release:** Earlier rounds in March and April 2026 (press: GPT-5.4 led at 77.3%, then Claude Opus 4.7 at 79.2%). v1.0 methodology Oct 2026 (eval release 2026-10-13).
- **Maintainer:** DualEntry, an ERP vendor.
- **Item:** 101 synthetic cases (37 easy, 36 medium, 28 hard) in 8 categories of 12–13 each: transaction classification, journal entries, AP, AR, bank reconciliation, financial reporting, month-end close, and accounting-knowledge MCQ. Example: "What account should this bank transaction be classified under? $450.00 payment to Staples on 2025-03-15" → Office Supplies.
- **Domain tag:** text (no environment)
- **Resembles:** **Bookkeeping clerk work directly:** coding transactions, JEs, AP/AR, reconciliation.
- **Human times:** None. Estimable from industry throughput. APQC's median is 12,000 invoices per AP FTE per year (about 9 min per invoice at 1,800 h); the top quartile is about 24k (about 4.5 min). Transaction coding is plausibly 0.5–2 min per item. All items are short, so the benchmark would anchor only the low end of the curve.
- **Model results:** 23 models in the Oct 2026 table: Gemini 4 Argon 91.1%, GLM-5.3 Flash 88.1%, Claude Fable 5.1 85.1%, GPT-6.1 Sol 81.2%, down to GPT-6 Luna 66.3%. The earlier 2026 rounds give a short time series.
- **Item/subset-level:** Category heatmap and difficulty-level scores per model are on the site; no per-item results.
- **Grading:** Deterministic (exact, tolerance, classification); pass if ≥2 of 3 runs pass.
- **Horizon computed?** No.
- **Verdict: CANDIDATE.** Task content fits well, but it is vendor-run and short-QA rather than agentic, the items are nearly saturated, and there are no times. To close: assign APQC/industry standard minutes per category and fit at category level. Mainly useful as the short-task anchor.
- **Sources:** pages above; https://itbrief.co.uk/story/gpt-5-4-tops-ai-accounting-test-but-errors-remain-high ; https://dualentry.com/blog/claude-opus-4-7-accounting-ai-benchmark-results

## 6. Finch (FinWorkBench)
- **Paper/URL:** arXiv 2512.13168 (v5 Apr 2026; ICLR 2026 / ACL Findings listing); data at huggingface.co/datasets/FinWorkBench/Finch
- **Release:** 2025-12
- **Maintainer:** Dong et al. (Shuxin Zheng's group, per ACL listing)
- **Item:** A real enterprise F&A workflow reconstructed from Enron email threads and attachments. Example: an analyst predictive-modelling flow (web search → import → cross-sheet retrieval → calculation → chart → report). 172 workflows / 384 tasks over 1,710 spreadsheets plus PDFs and docs. Task types include data entry/import, formatting, cross-file retrieval, calculation, validation, translation, visualisation and reporting.
- **Domain tag:** mixed (spreadsheet/file agent)
- **Resembles:** Spreadsheet back-office work, consolidation, reporting and data entry. A good match to "spreadsheet work".
- **Human times:** None. The 700+ h of expert annotation and QC covers construction (about 4 h per workflow), not completion time. Estimable via expert time estimates on the public data.
- **Model results:** Human-graded pass rates: GPT 5.1 Pro 38.4%, Claude Sonnet 4.5 25.0%. Automated pass rates: GPT 5.1 Pro 41.9%, Sonnet 4.5 29.1%, GPT-5.1 API 32.0%. Opus 4.5, Gemini 3 Pro, Grok 4 and Qwen 3 Max appear in a figure only. One date, late 2025.
- **Subset-level:** Pass rate by tasks-per-workflow (1: 48.6%, 2: 42.4%, 3: 33.3%, ≥4: 5.6%). This is a natural length proxy.
- **Grading:** Binary human expert judgement; GPT-5-mini judge as secondary (82–90% agreement).
- **Horizon computed?** No.
- **Verdict: CANDIDATE.** The data is public and the tasks are realistic. Gaps: no times and a single date. To close: get expert minute estimates per workflow (or run timed baselines on about 40) and rerun older and newer models with the released harness.
- **Sources:** https://arxiv.org/html/2512.13168v5 ; https://huggingface.co/datasets/FinWorkBench/Finch

## 7. SpreadsheetBench (v1 full/verified) and SpreadsheetBench 2 (SheetCopilot noted)
- **Paper/URL:** v1: NeurIPS 2024 D&B (Ma et al., Renmin/Tsinghua/Zhipu); https://spreadsheetbench.github.io. v2: arXiv 2606.29955 (2026-06-29, revised 2026-11-07), github.com/RUCKBReasoning/SpreadsheetBench-2, NeurIPS 2026 poster.
- **Item:**
  - v1: 912 real Excel-forum questions over 2,729 test-case spreadsheets, judged online-judge style. Example: extract part of a text string from a headerless column into B3:B14. "Verified" is a 400-item subset.
  - v2: 321 end-to-end business workflows in four categories: Debugging, Financial_Model (100 tasks, about 15 sheets and 1,164 modified cells each), Template, Visualization. Example: audit and fix a workbook for formula errors and hard-codes.
- **Domain tag:** software (spreadsheet manipulation)
- **Resembles:** Spreadsheet clerk and analyst work: formulas, lookups, cleaning, templates.
- **Human times:** None in either version; the dataset fields have no time column. Estimable by expert estimates or by timing a stratified sample. v1 items are probably 5–30 min; v2 items probably hours.
- **Model results:** v1 top overall 70.48% (Gemini in Google Sheets, May 2026 per benchmarklist **[unverified]**). Verified top about 91–95% by mid-2026 (product agents, e.g. Qingqiu Agent 94.75% **[unverified]**). v2 best of 8 frontier LLMs 34.89%; debugging as low as 12%. The leaderboard is dominated by products and scaffolds rather than bare models, and its dates are submission dates.
- **Item-level:** Not public. Per-category figures are in the v2 paper.
- **Grading:** Deterministic cell comparison after LibreOffice recalculation; a VLM checklist for visualisation.
- **Horizon computed?** No (the EA Forum "Excel time horizon" post of 2026-07 is satire).
- **SheetCopilot** (NeurIPS 2023): 221 superuser.com tasks; GPT-4 best at 44.3% pass@1. Old, no times. **EXCLUDE.**
- **Verdict: CANDIDATE** for v2 (realistic, public data, deterministic grading), with the gap being times plus a clean bare-model series. To close: estimate per-item minutes and rerun dated models with the released harness. v1 is near saturation for the short end.
- **Sources:** https://spreadsheetbench.github.io ; https://arxiv.org/abs/2606.29955 ; https://github.com/RUCKBReasoning/SpreadsheetBench-2 ; https://benchmarklist.com/benchmarks/spreadsheetbench_v1_verified/ ; https://arxiv.org/abs/2305.19308

## 8. HealthAdminBench (Stanford Shah lab)
- **Paper/URL:** arXiv 2604.09937; code and tasks at github.com/som-shahlab/health-admin-bench (task JSON under benchmark/v2/tasks); site at healthadminbench.stanford.edu (leaderboard did not render for me)
- **Release:** 2026-04-10
- **Item:** A computer-use task across a simulated EHR, two payer portals and a fax system. 135 tasks: 60 prior authorisation, 60 appeals and denials, 15 DME orders, at 3 difficulty levels with 1,698 subtasks. Example (hard): "Identify a high-value denial, file an appeal with supporting documentation, and document the investigation."
- **Domain tag:** computer_use
- **Resembles:** **Healthcare revenue-cycle BPO** (prior auth, denial management, appeals, order processing), a core Indian RCM back-office line.
- **Human times:** None. The authors logged 100+ h observing Stanford admin staff, but published no per-task times. Estimable from RCM throughput norms: an HFMA CFO cites 50–63 follow-up accounts per day (about 8–10 min each); a posting cites 75 insurance verifications per day (about 6 min). Prior-auth submission is plausibly 15–45 min.
- **Model results:** 7 configurations at one date (spring 2026). Task success: Claude Opus 4.6 CUA 36.3% (51.9% with portal guidance and a11y tree), GPT-5.4 CUA 26.7%, Kimi K2.5 15.6%; GPT-5.4 has the best subtask success at 82.8%.
- **Subset-level:** Results by task type and subtask type (Tables 3–4), plus difficulty tiers. Tasks are public, so per-task runs are reproducible.
- **Grading:** 1,177 deterministic state checks plus 521 GPT-5.4 rubric checks; task success requires every subtask to pass.
- **Horizon computed?** No.
- **Verdict: CANDIDATE (high priority for BPO relevance).** To close: get expert minute estimates per task (the authors have the shadowing data, so ask them) and run older models on the public environments.
- **Sources:** https://arxiv.org/abs/2604.09937 ; https://arxiv.org/html/2604.09937 ; https://som-shahlab.github.io/health-admin-bench-website/ ; https://hai.stanford.edu/news/measuring-what-medical-ai-can-actually-do ; https://www.hfma.org/topics/q_a/42618.html ; https://www.physicianspractice.com/view/verifications-day

## 9. MedAgentBench (v1, v2)
- **Paper/URL:** arXiv 2501.14654 (NEJM AI); github.com/stanfordmlgroup/MedAgentBench; v2: Chen et al., PSB 2026
- **Release:** 2025-01 (v1); late 2025 (v2)
- **Item:** A FHIR-API task in a virtual EHR (100 patients). Example: "check the last HbA1c and order a new one if >1 year old". v1 has 300 tasks; v2 adds 300.
- **Domain tag:** software (API agent)
- **Resembles:** Clinical order entry, chart lookup and recording vitals. Partly medical-records clerk work, mostly clinician work.
- **Human times:** None.
- **Model results:** v1: Claude 3.5 Sonnet v2 69.67%, GPT-4o 64.0%, DeepSeek-V3 62.7%, … Mistral 7B 4.0%. v2 paper: 91% without memory and 98% with memory for an improved agent. Stanford HAI says frontier models exceed 90% by 2026.
- **Item-level:** Code and environment are public, so runs are reproducible; by query/action split.
- **Grading:** Exact answer match and rule-based checks on POST payloads.
- **Verdict: EXCLUDE.** Saturated, no times, short clinical lookups. Note **PhysicianBench** (arXiv 2605.02240; 100 long EHR tasks, GPT-5.5 46%) and **MedHELM** (admin & workflow category win-rates 0.53–0.63) as clinical, not BPO.
- **Sources:** https://arxiv.org/html/2501.14654v2 ; https://hai.stanford.edu/news/measuring-what-medical-ai-can-actually-do ; https://d2ygbh7lwzeoju.cloudfront.net/psb-online/proceedings/psb26/chen_eric.pdf

## 10. Medical coding (ICD-10-CM / PCS / CPT): no maintained agent benchmark
- **What exists:**
  - "Understanding the Limits of Agentic ICD Coding" (EMNLP 2026; NTU / ASUS): 150 MIMIC-IV discharge summaries stratified by code rarity, plus a 153-note multi-step subset. Compares PLM-ICD, CodeSeeker and an agentic framework, each with Claude Opus 4.6 and GPT-5.2; micro-F1, best about 0.56 on rare codes.
  - Code Like Humans / Corti Symphony (vendor; ICD-10-PCS F1 37.3%).
  - MIMIC-CPT from CPTCoder (ACL 2026 demo; 7,735 test pairs).
  - MDACE.
  - Mount Sinai NEJM AI 2024 (GPT-4 exact match ICD-10-CM 33.9%, CPT 49.8%).
- **Domain tag:** text
- **Resembles:** Medical coders (a major Indian BPO line).
- **Human times:** **Strong external calibration exists.** Inpatient coding averages about 2.0 charts/h (himagine data at AHIMA 2018), i.e. about 30 min per chart. A 1996 AHIMA survey found most inpatient coders at 4–7/h and outpatient at 11–20/h (3–5 min). ED is 8–11/h **[secondary]**.
- **Model results over time:** Only 2–3 models per paper; no shared leaderboard.
- **Grading:** Micro/macro-F1 against gold codes. This is not pass/fail, but per-chart exact match can be derived.
- **Verdict: EXCLUDE as is, but a strong build target.** The data (MIMIC-IV), graders and per-chart time standards all exist. What's missing is a multi-model, multi-date run. To close: run 6–10 dated models on a fixed MIMIC-IV / MDACE set and assign time from chart type (ED / outpatient / inpatient).
- **Sources:** https://aclanthology.org/2026.emnlp-main.1583.pdf ; https://aclanthology.org/2026.acl-demo.60.pdf ; https://www.corti.ai/stories/introducing-symphony-for-medical-coding ; https://work.chron.com/medical-coding-productivity-standards-29187.html ; https://journal.ahima.org/AMP_EDN/383/AHIMA-Seeks-More-Coders-for-Participation-in-Productivity-Survey-2092.amp.html

## 11. TaxCalcBench (Column Tax)
- **Paper/URL:** arXiv 2507.16126; github.com/column-tax/tax-calc-bench
- **Release:** 2025-07
- **Item:** A JSON of a taxpayer's facts (W-2 boxes etc.) → a complete TY2024 federal 1040 in MeF-style output. 51 cases, e.g. "hoh-multiple-w2-box12-codes".
- **Domain tag:** text
- **Resembles:** Tax preparers and tax/billing clerks (US 1040 prep is a real Indian outsourcing line).
- **Human times:** None. Estimable from IRS burden estimates by return complexity, or from preparer norms (simple 1040 about 30–60 min) **[not verified this session]**.
- **Model results:** Gemini 2.5 Pro 32.35% strict / 51.96% lenient; Claude Opus 4 27.45%; Gemini 2.5 Flash 25.98%; Claude Sonnet 4 23.04%. Mid-2025 only. A yearly TY2025 release was promised but I found none.
- **Item-level:** Per-run outputs and evals in the repo.
- **Grading:** Deterministic line-by-line against a tax engine (strict, or ±$5).
- **Verdict: CANDIDATE (low).** Public, deterministic and per-case, but the models are stale and there are no times. Cheap to rerun on new models.
- **Related:** **Vals Tax Agent Bench** (193 private corporate-tax research questions; 6 categories; 77 models; top Gemini 4 Carbon 51.78%; public JSON has no time field). That one is tax research, not clerical; CANDIDATE only via expert estimates.
- **Sources:** https://arxiv.org/html/2507.16126v1 ; https://vals.ai/benchmarks/tax_agent_bench ; https://raw.githubusercontent.com/vals-ai/tax-agent-bench/main/data/public.json

## 12. DABstep (Adyen × Hugging Face)
- **URL:** arXiv 2506.23719; https://huggingface.co/blog/dabstep ; leaderboard at adyen-dabstep.hf.space
- **Release:** 2025-02-04. Validation is now closed and "DABStep-v2" was announced as coming **[date unverified]**.
- **Item:** 450+ multi-step data-analysis questions over 138k payment transactions, a fee-rules JSON and a business manual. Hard example: which ACI gives the lowest fees for merchant "Crossfit Hanna", answered as `E:346.49`.
- **Domain tag:** software (code-writing data agent)
- **Resembles:** Payments operations analyst, fee reconciliation, merchant billing.
- **Human times:** Aggregate only: humans averaged 62% on Easy after "3+ hours" (presumably the whole Easy set).
- **Model results:** At release on Hard: o3-mini 16%, DeepSeek R1 13%, Claude Sonnet 12%. Many agent submissions since, with dates on the leaderboard (did not render for me). Vendor claims of 94% are **[unverified]**.
- **Item-level:** Submissions include per-task answers (I believe, since the leaderboard dataset stores them) **[unverified]**.
- **Grading:** Exact match with tolerance; no LLM judge.
- **Verdict: CANDIDATE (low).** Many dated submissions, but no per-item times, and tasks are analytic rather than clerical.
- **Sources:** https://huggingface.co/blog/dabstep ; https://arxiv.org/html/2506.23719v1 ; https://adyen-dabstep.hf.space/

## 13. KYBench (Taktile Labs): KYB / adverse-media investigation
- **URL:** https://labs.taktile.com/benchmarks/kybench
- **Release:** 2026-04; updated 2026-09-07
- **Item:** Investigate a real business for adverse media across 9 categories (fraud, sanctions, …) and write an evidence-cited report. Example: Ozy Media → FRAUD and SEC_VIOLATIONS, escalate to EDD. 47 businesses (46 in the update).
- **Domain tag:** text (web-research agent, Parallel retrieval)
- **Resembles:** **KYC/KYB/AML analyst checks**, a large Indian compliance-BPO line.
- **Human times:** **Aggregate human baseline 30.0 min per investigation** (range 25–35), excluding QA. The intro cites 30–90 min per KYB review. Per-case times not published.
- **Model results:** The original board has 8 models (Claude Sonnet 4.6, Opus 4.6, Haiku 4.5, GPT-5.2 Pro, GPT-5, Gemini 3.1 Pro, …) with Adjusted F1 72–90%. The update ranks 21–25 models by economic cost; the human analyst Elo is 913.
- **Item-level:** No; the paper is promised.
- **Grading:** Category F1, an evidence-quality score (RAIS), a 20-point blind rubric and pairwise Elo.
- **Verdict: CANDIDATE.** It has a real human time baseline and the content fits, but only 46 cases, vendor-run, with all items about the same length (no length variation to fit a slope). It would supply one point (≈30 min) on a pooled curve.
- **Related:** **FinSpread-Bench** (Taktile, 2026-03): financial-statement spreading of 1,312 fields across 84 real underwriting documents (a classic Indian credit-KPO task). Human field-match 89% vs GPT-5.2 96.5%; no human time. CANDIDATE (low).
- **Sources:** https://labs.taktile.com/benchmarks/kybench ; https://labs.taktile.com/benchmarks/finspread

## 14. InsClaimBench (insurance claim adjudication)
- **URL:** arXiv 2610.09671 (seen via emergentmind; I did not reach arXiv directly)
- **Release:** 2026-10-07
- **Item:** An auto, property or health claim adjudicated from atomic policy rules → module decisions → payout decision and amount. 3,780 cases in 375 families; 86,656 atomic rule judgements.
- **Domain tag:** text
- **Resembles:** **Claims examiners and adjudicators** (health and P&C claims BPO).
- **Human times:** None. Estimable from production standards: a job posting sets minimums of 90 CMS-1500 or 50 UB-04 claims per day (about 5–10 min each).
- **Model results:** 6 unnamed LLMs at one date. Payout-decision accuracy 74–80%; joint decision and amount 48–73%.
- **Grading:** Exact match at each level; counterfactual variants test propagation.
- **Verdict: CANDIDATE (low).** Data release unclear, single date, not agentic. Also noted: **UNDERWRITE** (Snorkel, arXiv 2602.00456, commercial underwriting) and **InsLogicBench** (ACL 2026).
- **Sources:** https://www.emergentmind.com/papers/2610.09671 ; https://aclanthology.org/2026.acl-long.1035/ ; https://arxiv.org/abs/2602.00456

## 15. Penrose AccountingBench
- **URL:** accounting.penrose.com (the page body did not load for me; details are from secondary coverage)
- **Release:** 2025-07
- **Item:** Close the books monthly for a real SaaS company over a year, using Stripe, Ramp, Mercury and Rippling data. Errors carry forward. The CPA's books are the reference.
- **Domain tag:** mixed
- **Resembles:** Bookkeeping and month-end close, exactly.
- **Human times:** None published.
- **Model results:** Claude 4 Opus/Sonnet held above 95% for the early months, then fell below 85%. Grok 4 dropped in month 5. Gemini 2.5 Pro, o3 and o4-mini failed to finish month 1. No update found since July 2025.
- **Verdict: EXCLUDE.** It is effectively one long task on one company with no newer models, so no curve can be fitted. Cite it qualitatively for error compounding.
- **Sources:** https://gigazine.net/gsc_news/en/20250724-accountingbench ; https://publicaccountant.com.au/features/ai-accounting-future-accuracy-challenge/

## Also checked, short verdicts
- **FinanceBench** (Patronus, Nov 2023): 10,231 filing QA items, 150 public. Retrieval QA, no times, near-saturated (about 89% on the open set per benchmarklist **[unverified]**). **EXCLUDE.**
- **Vals MortgageTax:** extraction from county tax-certificate images (numerical and semantic), 92 models over time, Claude Opus 5 at 72.06% **[aggregator]**. Document data entry is BPO-relevant, but it isn't agentic and has no times; per-field keying time could be estimated. **CANDIDATE (low).**
- **BlueFin** (arXiv 2605.30907, NeurIPS 2026): 131 finance-spreadsheet tasks (10 synthesis, 82 manipulation, 39 interrogation); 3,225 rubric criteria; frontier models below 50%. No times. **CANDIDATE (low).**
- **FormFactory** (arXiv 2506.01520) and **FormGym** (2506.14079): form-filling and paperwork agents, mid-2025, few models, no times. **EXCLUDE** (lead for data-entry calibration only).
- **OfficeQA** (Databricks), **ExtractBench** (LlamaIndex): seen in passing, not researched.

## Calibration sources for imputing item length (for the "estimable" route)
- **AP invoices:** APQC median 12,000 invoices per AP FTE per year (n≈3,665 orgs), i.e. about 9 min per invoice; top performers about 23–24k. https://www.apqc.org/what-we-do/benchmarking/open-standards-benchmarking/measures/number-invoices-processed-fte-1
- **Medical coding:** inpatient about 2 charts/h (≈30 min); outpatient 11–20/h (3–5 min); ED 8–11/h **[secondary]**. AHIMA sources above.
- **Claims:** 50–90 claims per examiner-day (about 5–10 min) **[job posting]**. APQC also has a "healthcare claims settled per FTE" measure (not retrieved).
- **RCM follow-up:** 50–63 accounts per day (HFMA Q&A); 75 eligibility verifications per day.
- **KYB review:** 30 min (KYBench measured baseline); 30–90 min (industry cite).
- **Analyst research:** 16.8 min mean per FAB v1 question (measured).
- **Spreadsheet modelling:** 6.5–35 h per FrontierFinance task (measured); EMB ≥5 h.

## Noticed outside my area (one line each, not researched)
- **APEX-Agents** (Mercor, arXiv 2601.14242): 160 investment-banking tasks with **per-task expert hour estimates (mean 1.36 h; estimate 1.70 h vs measured 1.37 h on a sample)**. It is in the broad-occupational agent's area but highly relevant to finance.
- **GDPval:** includes accountants and auditors and financial analysts, with per-task times; broad-suite agent.
- **Mercor ACE / APEX leaderboard pages** show 2026 scores for newer models.
- **"METR Time Horizon 2.0"** EA Forum post (2026-07): satire about Excel's horizon; ignore.

## Leads I didn't chase
1. Email Vals for test-set per-item `Expert time (mins)` and per-item correctness on FAB v1.1 and v2.x. This would make FAB a full per-item METR dataset with 57+ models.
2. Ask Mercor for APEX-Accounting per-task expert time estimates and the human-baseline paper's per-task times. The paper linked from the Oct-2026 blog post was not read.
3. Ask the HealthAdminBench authors for the minute-level shadowing data; they observed 100+ h of admin work.
4. Check whether DABstep leaderboard submissions expose per-task answers and dates (for pass/fail by item over time), and the status of DABstep-v2.
5. The APQC "healthcare claims settled per FTE" and "invoice line items per FTE" measures, and the AKASA 2021 RCM productivity benchmarks, as length calibrators.
6. A TaxCalcBench TY2025 release and the HN thread's updated leaderboard.
7. The FinanceBenchmark "Financial AI Leaderboard" (Aug 2026), the Tencent HY FinAgentBench (internal), and ZenML's claims-appeals benchmark (800 appeals).
8. Accounting-specific subsets inside OSWorld, TheAgentCompany or GDPval: the finance/admin items could be pooled with the above if their times are per item.
