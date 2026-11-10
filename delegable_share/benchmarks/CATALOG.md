# Benchmark catalog for the delegable-share pipeline

Consolidated 2026-11-09 from the eight reports in `benchmarks/search/`. This file adds no new research. One conflict between reports was settled on the web; see "Conflicts between reports" at the end. Companion files: `stage3_catalog_draft.md` (the list the Stage 3 coder sees) and `ACQUISITION.md` (the to-do list).

## Bottom line

Seven benchmarks can be fitted now (Tier A): they have per-item or bucketed human times *and* item- or subset-level results for several models over time. Five are software (METR TH1.1, SWE-bench Verified, Multi-SWE-bench, Terminal-Bench 2.0, Cybench). One is analyst-style finance text (Vals Finance Agent), and one is long computer-use workflows (OSWorld 2.0, usable only in five time bins). Another 36 benchmarks (Tier B) become fittable after one feasible step: imputing times from action or step counts, getting times the authors already hold, or running dated models ourselves. The rest (Tier C, about 95 named benchmarks) are excluded or on watch. **No pilot occupation has a good match in Tier A.** Software QA, Computer User Support and Customer Service all have good matches only in Tier B: SWT-bench Verified for QA, WorkArena/WorkArena++ for user support, and the τ-bench family for customer service. Four BPO lines also lack a Tier A good match: voice/chat, data entry, insurance claims and medical records. As SPEC §4 predicted, per-item human times are the binding constraint. A few things would move the pilot most. For WorkArena, one author request plus a one-day timing study. For τ-bench, action counts from the public submissions plus a 20–30-task timed pilot. For QA, a join of SWE-bench Verified's time buckets onto SWT-bench. Two of the method flags below also change SPEC §2 and §9 before any fitting. First, METR's β is per doubling, not per ln-minute. Second, the "k_b = 7" for test-graded code rests on one model, out of a 2–20× range.

How to read the tables:

- **Domain** uses the Stage 2 tags: software / computer_use / text / mixed.
- **k_b class**: *test* = hidden unit or E2E tests; *state* = programmatic check of the final application or database state, or an exact answer; *LLM* = LLM judge or jury, usually on a rubric; *expert* = human experts grade against professional standards. SPEC §9 sets k_b only for *test* (7) and *expert* (1). The *state* and *LLM* classes need values; see method flag 7.
- **β** is quoted in the unit the source used. "/log2" means per doubling of human time, which is METR's unit. Multiply by 1.443 to get our per-ln unit (method flag 1).
- Release dates in "model series" come from the reports. Pull exact dates from Epoch's database before fitting.

---

## Tier A: usable now

| Benchmark | Domain | What one item is | Human times (status; range; median) | Model series (span; count) | Item-level results | Grading (k_b class) | Existing H, β | IT/BPO work it maps to | Next step |
|---|---|---|---|---|---|---|---|---|---|
| **METR Time Horizon 1.1** (HCAST + RE-Bench + SWAA) | software | Self-contained technical task in a container: ML-code bug fix, scripting, cyber, ML research; plus 1–30 s single actions. 228 tasks. | Per item, minutes. 162 timed baselines (geometric mean of successful contractor attempts) and 66 estimates. 0.02–1,800 min; median 12.6 (HCAST 44). Only 5 of 31 tasks over 8 h are baselined. | Mar 2023 – Apr 2026; 23 agents in the YAML, 21 in `runs.jsonl` (~24k runs) | Yes, per run. Task text mostly private. | Task-specific scoring functions (*test*) | Yes. H50/H80 with CIs per model. β median 0.58/log2 (0.41–0.69), i.e. 0.84/ln. Doubling ~129 days since 2023 (CI 104–158). | Anchor curve. App maintenance, scripting, data-pipeline fixes; low-context, "less messy" than client work. | Reproduce with `mle.py`; build a family→domain map for a SWE-only subset. Unreliable above 16 h. METR page frozen 2026-09-08: no H for Opus 4.7/5/5.5, GPT-5.5 or Gemini 4. |
| **SWE-bench Verified** | software | GitHub issue plus Python repo (12 OSS repos) → a patch that passes hidden tests. 500 items. | Bucketed annotator estimates (3 professional devs, "engineer familiar with the codebase"): <15 min 194; 15–60 min 261; 1–4 h 42; >4 h 3. Median in the 15–60 min bucket. | Oct 2023 – Sep 2026; 182 submissions; Epoch: 33 models with Inspect logs to mid-2026 | Yes, per instance (`swe-bench/experiments`; Epoch S3 logs) | FAIL_TO_PASS + PASS_TO_PASS tests (*test*) | METR cross-domain: β median 0.51/log2 (0.74/ln), all ≥ 0.25; H up to ~38 min (mid-2025). METR paper: doubling ~70 days. Whitfill: test vs merge T50 for 5 models. | L2/L3 application-maintenance bug-fix tickets (OSS Python, not enterprise apps) | Fit 2023–mid-2025 with interval-censored buckets. Saturated (90%+) and contaminated; OpenAI found flawed tests in 59.4% of 138 hard unsolved items. Since 2025-11-18 only academic teams can submit. |
| **Multi-SWE-bench** | software | Same format, 1,632 issues in Java, TS, JS, Go, Rust, C, C++ (e.g. Dubbo date-type serialisation fix). | Bucketed, **two independent annotators per item**, public xlsx (same 4 buckets, "after a few hours of familiarisation"): easy 374, medium 650, >1 h 608. 37% over 1 h. | Mar 2025 – Jul 2026; 9 models × 3 scaffolds in the paper, then community submissions; few closed frontier models after mid-2025 | Yes, per instance plus trajectories | Fail-to-pass tests (*test*) | None | **Enterprise AMS in Java/JS/TS**, the closest stacks to Indian IT | Fit per language. Fill 2025–26 with dated open-weight runs, or run the mini/flash subsets ourselves. |
| **Terminal-Bench 2.0** | software | Docker container plus instruction (e.g. install Nginx with logging, rate limiting and error pages); hidden pytest on the final state. 89 tasks. | Per item, **author estimates** (uncalibrated), 88/89. Expert 5–2,400 min, median 60. Junior 10–19,200 min, median 240. Sysadmin subset: expert 15–300 min. | Paper runs 2025, plus leaderboard runs 2025-11-13 → 2026-05-12; 73 usable of 75 submissions | Yes, per trial (HF `harborframework/terminal-bench-2-leaderboard`) | pytest on container state (*test*) | Researcher's fit: corr(ln time, success) −0.28. Pooled β 0.27/ln (= 0.19/log2, **below METR's 0.25 exclusion line**). Frontier slopes ~0, so H is not identified. "Think Fast" fits are no-CoT only. | Sysadmin/server config (9 tasks), debugging, log and data processing, DB recovery, security hygiene. About a third of items are everyday IT work; the rest are puzzles or research. | Subset by `category`. Test the exclusion rule per subset. Use Terminus-2 rows for a clean model comparison. Pool with TB1 and TB3 for date range. |
| **Vals Finance Agent** (v1.1; v2/v2.1) | text | Analyst research question answered with EDGAR and web search, parsing and a calculator ("difference in days inventory outstanding, HD vs Lowe's FY2024"). v1.1 537 items; v2 927. | Per-item `Expert time (mins)` on the **public split only**: v1.1 n=50, 2–60 min, median 10; v2 n=27, 15–120 min, median 40. Full set at **category level** (9 categories, medians 5–80 min). | v1.1 ~57 models (Claude 3.5/GPT-4o era → Feb 2026, dated snapshot pages); v2.1 39 models to Nov 2026 | Per category, for every model (leaderboard page JSON). Not per item. | LLM judge, a 3-model jury in v2.1 (*LLM*) | Researcher's rough category-level fit: H50 ~9 min (Claude 3.7 Sonnet Thinking, Feb 2025) → ~25 min (Opus 4.6 Thinking, Feb 2026). Slopes 0.32–0.66/log2. Illustrative only. | Equity research, financial-analyst KPO, parts of FP&A. **Not clerk work.** | Fit at category level now. Ask Vals for test-set per-item times and correctness. |
| **OSWorld 2.0** | computer_use | End-to-end office workflow on an Ubuntu VM with 31 self-hosted sites and desktop apps (e.g. "ExpenseFlow": follow a PDF tutorial, extract receipts, cross-check bank and email, file a reimbursement claim). 108 tasks, ~27 weighted checkpoints each. | Per item, but not public: two annotators each gave a range; t_i = geometric mean of the midpoints. Public at **bin level**: <45 min to 360 min; median ~1.6 h; 69.6% over 1 h. Ties are common. | Jun–Oct 2026 only. 7 author runs, Snorkel runs, vendor self-reports. Three task releases (06.24, 08.08, v2.1) that are not comparable. | Bin level public (5 bins × 4 models, App. G.2 Table 21). Per-task results sit in gated trajectory zips (3–17 GB each). | Final-state checkpoints, some model-judged; binary = all pass (*state*, part *LLM*) | None fitted. Authors: METR's pattern "transfers only partially". Success is flat at ~20% up to ~2 h, then 0 above 163 min. | F&A back office (expenses, reconciliation), document prep, admin and compliance; SOC-mapped per task | Bin-level fit now, at low confidence. Accept the HF gate and look for t_i, otherwise ask XLANG. |
| **Cybench** | software | Professional CTF challenge (crypto, web, pwn, reversing, forensics) in a Kali container; capture the flag. 40 tasks. | Per item, measured: first-solve time of the fastest competing team (biased low). ~2 min – 24 h 54 min. | 2024 paper models; later system-card reports (unverified) | Per-task tables and logs in the repo | Flag match (*test*-like) | None on Cybench itself; UK AISI fits its own private cyber suite. BRIDGE anchor: 92.3% of IRT-predicted times within 0.5–2× of first-solve time. | SOC and pentest work only. **Low relevance.** | Sensitivity check for security items only. |

---

## Tier B: fittable after a specific, feasible step

Sorted by domain, then by pilot priority. "Est." means the time is our rough guess from the report's evidence, not data.

### Software, testing, IT operations

| Benchmark | Domain | What one item is | Human times | Model series | Item-level results | Grading (k_b) | Existing H, β | IT/BPO work | Next step |
|---|---|---|---|---|---|---|---|---|---|
| **SWT-bench Verified** | software | Issue plus repo at the pre-fix commit → write tests that fail before and pass after the hidden fix. 433 items. | None of its own. **Borrow SWE-bench Verified buckets** by `instance_id`. These measure time to *fix*, so treat them as an upper bound. Almost none over 1 h. | Feb 2025 – Nov 2026 (Lite from May 2024); many bespoke systems | Partly: trajectory and eval links per entry | Fail-to-pass plus coverage (*test*) | None | **QA**: regression and bug-reproduction tests | Join buckets; pull per-instance results for fixed-scaffold entries (OpenHands, Claude Code). Near saturation (~90%). |
| **SWEeper-Bench** | software (+browser) | "Find and fix issues in feature X" on a real OSS web app (200 apps, 7 domains); a browser verifier checks the target behaviour and that nothing else broke. | None (bugs reproduced by hand, untimed) | One snapshot, Oct 2026 (15 agents) | Yes (HF traces) | Agentic browser verifier (*LLM*-like) | None | **Exploratory QA plus AMS fix** | Expert time estimates for 200 items; rerun 2025-era models for a trend. |
| **SWE-bench Pro** | software | Issue plus requirements plus interface spec in 41 repos (Python, Go, JS/TS); gold patches average 107 lines across 4.1 files. Public 642 / held-out / commercial 276. | None ("hours to days") | Sep 2025 – 2026, Scale leaderboard; harness changed (turn cap 50→250, SWE-Agent→mini-swe-agent) | Trajectories per entry | Tests, human-reviewed (*test*) | None | Feature work and multi-file fixes; commercial split ≈ client code | Impute times from patch size, files and language with a model calibrated on SWE-V and Multi-SWE buckets, or get ~50 expert estimates. Grading audits alleged (unverified). |
| **SWE-rebench / SWE-bench Live** | software | Fresh SWE-bench-style issues collected monthly | None | Monthly, ~30 models per month, fixed scaffold (2025–26) | Not confirmed (Harbor 860 tasks) | Tests (*test*) | None | AMS bug fixes, uncontaminated | Impute times as for Pro; get per-task results. Best clean 2026 trend. |
| **SWE-bench Multimodal** | software | JS front-end issue with screenshots; 619 items | Bucket shares only (13/43/38/6%); per-instance labels not released | 22 submissions, 2024 – Nov 2025 | Yes | Tests (+ pixel tests) (*test*) | None | Web/UI maintenance | Ask the SWE-bench team for per-instance labels. |
| **SWE-Lancer IC Diamond** | software | Real Upwork job on the Expensify app (React Native/TS); write the fix; E2E Playwright tests. 198 IC tasks (463 Diamond in total). | None. Per-item **price** $50–$32,000, median $500. | OpenAI-reported Feb 2025 – Feb 2026, plus paper models; no independent cross-lab series | Harness public (Inspect); no per-item results published | E2E tests, triple-verified (*test*) | None | Outsourced app dev and maintenance for a commercial product | Price is a weak proxy (method §M5). Time ~20 tasks and run the 198 IC tasks on 5–8 dated models. |
| **Terminal-Bench 3.0 / 4.x** | software (some back office via files) | Same container format, longer tasks, 8 h timeout: `medical-claims-processing`, `heat-pump-warranty`, `intrastat-meldung`, `live-database-cutover`, `wal-recovery-ordering`, `react-lead-form`. 66 tasks. | Per-item **expert-hour** author estimates (66/66): 0.75–60 h, median 4 h | Jul–Nov 2026 only | Unknown (Harbor Hub) | pytest (*test*) | None | DB ops, frontend, data engineering; plus 9 **operations** tasks (claims, compliance, finance) | Pull per-trial results from Harbor Hub, or `harbor run` ourselves. Each release drops saturated tasks, so the pool is biased toward hard items. |
| **Terminal-Bench 1.0** | software | As TB2 but easier (e.g. recover lost git changes and merge to master). 80 core tasks. | Author estimates for 42/80 core (198/241 pool); core expert 2–2,400 min, median 30 | ~mid-2025 | Not located | pytest (*test*) | None | Sysadmin, git, build | Check the repo's `leaderboard/` folder; rerun via Harbor's TB1 adapter; pool with TB2. |
| **ITBench-AA (SRE)** | software | Kubernetes incident snapshot (alerts, events, traces, logs) → JSON list of root-cause entities. 59 scenarios (40 public). | None. Production reference: ~52 min manual RCA. | Starts May 2026 (8 models); Artificial Analysis to add more | No | Average precision at full recall; binarisable (*state*) | None | **L2/L3 production support, SRE triage** | Elicit SRE times for 59 items; ask AA for per-item results or rerun with Stirrup. |
| **DBA-Bench** | software | Live PostgreSQL under load plus a symptom alert → diagnose and remediate (e.g. stale stats → `ANALYZE`). 106 scenarios. | **Human DBA ran all 106; durations not reported** | One snapshot, mid-2026 | Promised | Outcome verifier plus zero safety violations (*state*) | None | **DBA L2/L3** | Ask the authors for timestamps; rerun older models. Pass rates ≤18%, so only the easy end is informative. |
| **Spider 2.0** (Lite/Snow/DBT) | software | Business question over a large cloud warehouse → SQL; DBT data-transformation projects | None; SQL-length buckets only | Systems leaderboard, undated | Partial | Execution accuracy (*state*) | None | BI/MIS reporting, data engineering | Elicit times per bucket and run a fixed-scaffold model series. Low priority. |

### Computer use and web

| Benchmark | Domain | What one item is | Human times | Model series | Item-level results | Grading (k_b) | Existing H, β | IT/BPO work | Next step |
|---|---|---|---|---|---|---|---|---|---|
| **WorkArena++ (L2/L3)** | computer_use | Multi-step ServiceNow workflow. L3 gives only a ticket (onboard a user and order their hardware; assign a new problem to the least-loaded agent). 682 tasks. | **Recorded but unpublished**: 15 people, 98 instances, time to resolution | L2 14 models, L3 8 (2024–25) | Leaderboard JSON per model; rerun gives per-task results | Programmatic DB-state validators (*state*) | None | **Service desk L1/L2 end to end** | Ask the authors (top request); run 2026 models via AgentLab. |
| **WorkArena L1** | computer_use | One atomic ServiceNow action: create an incident or change request, filter or sort a list, order a catalog item, search the KB, read a dashboard. 33 templates. | None. Oracle action counts 1–47 per task → est. ~20 s – 3 min. | 16 models on the fixed GenericAgent harness (2024–25) | Per task in papers; leaderboard JSON | Programmatic validators (*state*) | None | **IT service desk L1 / ITSM** | Convert action counts to time at a rate calibrated on WebArena traces, or run a 1-day timing study (33 templates, free dev instance). Use StarShell for 2026 points. |
| **StarShell** | computer_use / software | The same enterprise task via web, terminal/API or MCP: ServiceNow 330 (WorkArena), GitLab 192, ERPNext 207 (invoices, sales orders) | None (ServiceNow part inherits WorkArena action counts) | One generation, 2026 (4 frontier models) | Per category; per-task logs unconfirmed | Programmatic state (*state*) | None | ITSM; **ERP/F&A back office** | Use as the 2026 endpoint of the WorkArena series; impute ERPNext times. |
| **OSWorld-Verified** | computer_use | Single-goal desktop task on Ubuntu (Chrome setting, Calc formula, file operation, Thunderbird). 369 (361 used). | Measured per item, **only the aggregate published**: median 112 s; <60 s 28.7%, 60–180 s 40.1%, >180 s 30.2%; many ~900 s | 2024–26, ~50 dated runs; step budgets differ | Yes (`all_result.json`, per-task 0/1) | Per-task evaluator (*state*) | METR score-only H on synthetic times, β fixed 0.6/log2: o3-CUA 1.79 min, Claude 3.7 Sonnet 1.08, GPT-4o 0.31 (to mid-2025) | Desktop support micro-tasks, spreadsheet operations: one *step* of a BPO workflow | Impute from OSWorld-Human step counts, checked against the known median and bucket shares, or request XLANG's timing log. Saturated (>72% human baseline), so fit 2024 – mid-2025 only. |
| **WebArena (+ Verified)** | computer_use | NL intent on self-hosted Magento admin, GitLab, CMS, forum, map ("update price and mark out of stock"). 812 tasks. | **Extractable** from 179 human Playwright traces (one per template); mean 110 s; 5 s – 9 min | 2023–26, 50+ entries; scaffold-dominated (14–74%) | Scattered per system; BrowserGym per task | Answer/state checks; Verified is deterministic (*state*) | METR score-only H up to 2.5 min (β 0.6) | E-commerce back-office admin, GitLab admin | Extract trace durations. These also give the seconds-per-action rate for WorkArena, Online-Mind2Web and SCUBA. Use fixed-harness rows. |
| **UI-CUBE** | computer_use | Enterprise UI task in replicas of Salesforce, SAP, Concur, Workday (enter an expense report, update stock, move records between apps), plus 136 single-widget tasks. 226 tasks. | **Category means only**: widgets ~11 s; enterprise 43–267 s (3 s – 4.5 min overall). Per-task logs exist at UiPath. | 5 configs, 2025 | No | State-diff `test()` (*state*) | None | **RPA/BPO data entry and transfer**, expense, ERP, HR records | Ask UiPath for per-task human and model results; rerun 3–4 models. |
| **HealthAdminBench** | computer_use | Across an Epic-like EHR, two payer portals and fax: prior authorisation, appeal a denial, DME order. 135 tasks, ~12.6 subtasks each. | None. Industry norms 6–45 min (est.). | 7 configs, spring 2026 | Per type and subtask; tasks public | 1,177 deterministic state checks plus 521 LLM rubric checks (*state*, part *LLM*) | None | **Healthcare RCM / medical-records BPO** | Time a stratified sample, or ask the authors for the 100+ h shadowing data; run older models. |
| **SCUBA** | computer_use | Task in a live Salesforce sandbox as admin, sales rep or service agent (report with a filter; formula field). 300 instances from 60 templates. | None. Human demo plans public (`data/test_demo_aug.json`); annotation trajectories with step counts not public. | 9 agents, 2025 only | Samples only | Rule-based org state plus milestones (*state*) | None | CRM admin, service-agent case handling, sales ops | Ask Salesforce for step counts or timestamps; rerun newer models (free dev org). |
| **Online-Mind2Web** | computer_use | Task on a live consumer site (cheapest flight plus an add-on). 300 tasks, 136 sites. | Per-item **human step counts** (`reference_length`: ≤5 / 6–10 / ≥11) | HAL fixed scaffolds Jan–Aug 2025 (~20 combinations); vendor self-reports to Mar 2026 | Yes (HAL traces; OSU per-task labels) | WebJudge (*LLM*) | None | Consumer transactions; weak for BPO | Convert steps to time. Low priority. |

### Customer service (text and voice)

| Benchmark | Domain | What one item is | Human times | Model series | Item-level results | Grading (k_b) | Existing H, β | IT/BPO work | Next step |
|---|---|---|---|---|---|---|---|---|---|
| **τ-bench / τ²-bench** (retail, airline, telecom) | text | A simulated customer chats with the agent, which has a policy document and tools; success = final DB matches gold plus required statements. Telecom: guide the user through fixes on their own phone. Retail ~115, airline 50, telecom 114. | None. Gold actions (telecom means 2.3–6.0, range 1–12) and turn counts. Handle-time anchors: retail 4–8 min, telecom technical 8–12 min. | 2024 – Oct 2026. HAL airline 15 models (Jan–Aug 2025); official board; AA telecom 440 models with release dates | Yes: HAL encrypted traces; taubench.com `benchmark-submission.json` per task and trial | DB state plus required outputs; 2.0 adds LLM-judged assertions (*state*) | None | **Chat/voice CS** (returns, rebooking); tier-1 telecom troubleshooting ≈ help-desk scripts | Impute minutes from actions and turns; validate with a timed 20–30-task pilot and Sim2Real timestamps. Saturated (telecom ~99% on AA, overall 85–88%): pair with τ³ and τ-Voice. Scores not comparable across 1.x/2.0 or user simulators. |
| **τ³-Banking (τ-Knowledge)** | text | Fintech support: find the policy among ~700 documents, then make a verifiable, compliant account change (e.g. correct a refund). 97 tasks. | None (as τ², plus retrieval steps) | Mar–Nov 2026; grading break 2026-07-15 | Submission packages | DB-state hash plus actions (*state*) | None | **Banking BPO**: disputes, refunds, fee queries | As τ². Unsaturated. |
| **τ-Voice** (+ τ-bench 2.0 voice-v2, i18n incl. Hindi) | text (audio) | τ² tasks as live full-duplex calls with accents, noise and interruptions. 278 tasks; 2.0 adds 50 per domain per language. | None. A simulated call duration exists per call (example retail call ~3 min); publication unconfirmed. | Dec 2025 – 2026 | voice-v2 packages per task | Same as τ² (*state*) | None | **Inbound voice contact centre**, Hindi | Check `interaction_metrics` for durations; otherwise run it and log them. |
| **CRMArena-Pro** | software / text | Query or action against a Salesforce org via API: route a case, check a quote against discount policy, qualify a lead; single- and multi-turn. 19 task types, 4,280 queries. | None. ~9 min per query was the experts' time *budget*. | Jul 2024 – Apr 2025 models | Skill-level only | Exact match (+ LLM extractor/judge) (*state*) | None | CS case routing, sales ops, CRM back office | Time 3–5 admins on ~95 items (~15 h); rerun 2025–26 models (open harness). |
| **EVA-Bench** | text (audio) | Bot-to-bot voice call: a caller with a goal; the agent queries and modifies a DB. Airline, HR services, **enterprise IT service desk**. 213 scenarios. | None | 12 systems, 2026 | Local runs write per-record results | DB state plus faithfulness (*state*, part *LLM*) | None | Voice IT help desk (password reset, access), HR shared services | Log call durations from our own runs. ~70 items per domain limits the fit. |
| **SOPBench** | text | Customer request in 7 service domains with a coded SOP; verifiers check SOP compliance and outcome. ~830–900 cases. | None; SOP step counts | 18 models, 2024 – mid-2025 | Yes (24k trajectories) | Rule-based (*state*) | None | SOP-driven process work (banking, records) | Convert steps to time; rerun newer models. Low priority (toy-like). |

### Occupational suites and back office

| Benchmark | Domain | What one item is | Human times | Model series | Item-level results | Grading (k_b) | Existing H, β | IT/BPO work | Next step |
|---|---|---|---|---|---|---|---|---|---|
| **OmegaUse-OfficeVal** | mixed | Practitioner's office request with 1–N Word/Excel/PPT/PDF inputs → reformat, restructure, extract into a table, annotate. 100 items. | **Per item, measured, public** (≥2 annotators, mean of the two shortest valid times): 5–501 min, median 122 | One snapshot, 5 open-weight models (Jul 2026) | Tasks, rubrics and verifiers public; rerunnable | Code verifiers from expert-revised rubrics; continuous score needs a threshold (*state*) | None | **Back-office document processing, data extraction/entry**, report formatting | Run 6–10 dated models ($0.2–1.8 per task) and fit directly. |
| **TheAgentCompany** | mixed | Task in a simulated software company (GitLab, Plane, ownCloud, RocketChat with simulated colleagues), e.g. collect equipment requests, price them, message the requester. 175 tasks. | None ("10 min to several hours") | Dec 2024 – Nov 2025, ~19 runs | **Yes**, per task (experiments repo) | Checkpoint evaluators, some LLM (*state*) | None | IT-services roles: dev, PM, HR/admin, finance back office | 2–3 annotators estimate all 175; time 20–30. Calibrate with Wang et al. 2025 (48 workers, 16 TAC-style tasks). |
| **GDPval** (+ GDPval-AA) | mixed | Professional request with reference files → an Office-style deliverable. 44 O*NET occupations incl. CSRs, software developers, accountants, order clerks. 220 public gold of 1,320. | Per item, self-reported by the writer, **private**. Gold median 5 h, IQR 2.4–10 h, 0.5–100 h. | Sep 2025 – Apr 2026 (OpenAI); GDPval-AA: 300+ models with release dates (Elo, no human comparison) | No. Fig. 13: win rate falls with task length. | Blinded expert pairwise vs the human deliverable (*expert*); AA uses LLM judges | BRIDGE H80 ~20 min (IRT-predicted times, not GDPval's own) | Best O*NET link; several BPO occupations | Ask OpenAI for per-task times and outcomes. Otherwise LLM-estimate gold-set times calibrated to the published quantiles, and digitise Fig. 13. |
| **APEX-Agents** | mixed | Long cross-app task in a simulated firm (files, mail, chat, spreadsheets) for IB, consulting or law; returns a message or file. v1 480 / v1.1 240. | Per-item **expert estimates** (gated metadata; mean 1.82 h, roughly 1–3 h). Baselining on 96 tasks: estimate 1.70 h vs actual 1.37 h. | Jan–Nov 2026, many models; v1 and v1.1 not comparable | No. Qwen traces only, and their licence bars parameter fitting. | LLM judge on binary expert rubric (*LLM*) | None | KPO analyst work; not core IT/BPO | Score-only H now (pooled β, domain-level times); own runs for β. Narrow time range limits β. |
| **APEX-Accounting** | mixed | Synthetic company at month-end close: reconcile, accrue, post, enter data, explain variances. 160 private tasks plus 10 public. | None. CPA baseline on 4 simplified tasks: 30–180 min. | One date (Jul 2026), 9 models | No (private) | LLM judge on expert binary rubrics (*LLM*) | None | **F&A**: GL posting, reconciliations, accruals, AP/AR entry, close | Ask Mercor for per-task times and pass rates, or time humans on the public world and run models on it. |
| **DualEntry (DualBench100)** | text | Short accounting case: classify a bank transaction, write a JE, AP/AR, bank rec, report, MCQ. 101 cases. | None. Standards ~0.5–10 min per item (APQC ~9 min per invoice). | Mar–Oct 2026 rounds; 23 models in Oct | Category × difficulty per model | Deterministic (*state*) | None | **Bookkeeping clerks** | Assign standard minutes per category; fit at category level. Vendor-run, near saturation; short-end anchor. |
| **Finch (FinWorkBench)** | mixed | Real F&A workflow rebuilt from Enron emails and spreadsheets: import, cross-file lookup, calculation, validation, chart, report. 172 workflows / 384 tasks. | None. Tasks per workflow (1 to ≥4) is a length proxy. | One date, late 2025 | By length proxy | Binary expert judgement (+ LLM) (*expert*) | None | Spreadsheet back office, consolidation, reporting | Expert minute estimates; rerun dated models with the released harness. |
| **SpreadsheetBench 2** | software | End-to-end workbook task: debug formulas, build a financial model (~1,164 changed cells), fill a template, chart. 321 tasks. | None | 8 frontier LLMs, 2026 | Per category | Deterministic cell check (+ VLM for charts) (*state*) | None | Spreadsheet clerk and analyst work | Estimate minutes; rerun dated models. |
| **JobBench** | mixed | Workspace of public-record files plus a professional request; **each item keyed to one O*NET task statement**. 128 public. | None | One snapshot, 36 configs spanning release dates | Tasks public; item scores not | LLM judge on binary rubric chain (*LLM*) | None | Mixed professional work (35 occupations) | Estimate times; rerun. Low priority. |
| **Vals Excel Modeling (EMB)** | software | Build a full IB/PE Excel model from a prompt plus source files. 103 questions. | Aggregate only: ≥5 h. FrontierFinance per-type estimates 8–16 h. | 71–77 models, 2026 | Per family per model | Cell match / agentic LLM rubric (*state* / *LLM*) | None | Financial-modelling KPO | Long-end anchor only; pool with Vals Finance Agent. Low priority. |

---

## Tier C: watch or excluded

| Benchmark(s) | Domain | Reason | Would move up if |
|---|---|---|---|
| MirrorCode | software | Human times are guesses (1.5–17 weeks for one program); contaminated; black-box cloning is atypical | Never as a fit; long-tail anchor only |
| SWE-Marathon | software | 20 items, single snapshot; 40–400 h estimates unconfirmed | Repeated runs over time |
| Vibe Code Bench | software | No times; LLM-judge grader; v1 saturated and archived | Freelancer pricing or timing of specs |
| Code-review benches (SWE-PRBench, c-CRAB, GitHub/LangChain ReviewBench, Martian) | software | No times; F1-style scores; single snapshots | Code review becomes its own O*NET cluster |
| FeatBench, Commit0, MigrationBench, FreshBrew, SWE-PolyBench, SWE-bench Multilingual | software | No times; thin series. MigrationBench/FreshBrew are the leads (Java upgrades are priced IT-services work). | Time imputation from AST/patch fields |
| TDD-Bench Verified, TestGenEval/TestEval, WebTestBench | software | Duplicate of SWT-bench / no series / continuous metrics / no times | WebTestBench gets binary scoring and times (manual-QA gap) |
| AIOpsLab, SREGym, SRE-Marathon; DevOps-Gym, IaC-Eval, Multi-IaC-Eval, TerraFormer, NetConfEval, NetArena, CORNETTO, EnvBench, SetupBench; LHTB | software | No human times; few models; scaffold-dominated or partial-credit scores | Timing studies; TB2/TB3 sysadmin subsets cover these jobs for now |
| METR algorithmic-vs-holistic (Rein, 18 issues) | software | n=18, one model; data not released | Used as method evidence (flag 2) |
| Whitfill et al. merge study | software | Adjustment study, not a benchmark | Used as method evidence (flag 2) |
| ERPBench (Accenture) | computer_use | ~30 tasks, unreleased, one frontier model at ceiling; tier-mean times only | Release plus a model series. Qualitative point: 1–7 min ERP form entry is near-solved. |
| Windows Agent Arena, macOSWorld, AndroidWorld, MobileWorld | computer_use | Aggregate or plotted times only; sparse series, or saturated consumer mobile | macOSWorld Fig. 3c data plus reruns |
| OpenComputer, WeaveBench, MyPCBench, DeskCraft, OSExpert-Eval, OSUniverse, VideoGUI | computer_use | No human times | Timing studies |
| ChainWorld | computer_use | Inherits OSWorld times by summing, once per-item OSWorld times exist | OSWorld per-item times obtained → Tier B |
| VisualWebArena | computer_use | Thin recent model series; low job relevance | Use its 233 human traces only to calibrate seconds per action |
| WebChoreArena | computer_use | No times (back-office "chore" content is relevant) | A timing study on a sample, reusing WebArena's Docker sites |
| ST-WebAgentBench | computer_use | Old agents only; no times | Used as acceptance evidence (flag 7) |
| Mind2Web 2, REAL, WebVoyager, AssistantBench, BrowseComp, BearCubs, WebBench, WoW-bench, CAP, Odysseys | computer_use / text | Consumer or search-puzzle tasks; no times or single snapshots. WoW-bench is ITSM via API but has no times. | — |
| τᶜ-Bench | text | Synthetic harder τ² tasks with LLM-judged validity | Needed to extend the τ curve to longer items |
| CRMArena | text | Superseded by CRMArena-Pro; stale series | — |
| CRM-Agent-Bench | text | Single snapshot, near-saturated, no times (but has ITSM and payments domains) | We rerun older models |
| CirrusBench | text | Data release uncertain; LLM judge; no times (but real cloud-support tickets) | Release plus Alibaba handle times |
| ECom-Bench, JourneyBench, ServiceBench | text | 53 items / synthetic / non-binary scores | — |
| CXBench | text | Small, single snapshot | Used as acceptance evidence (flag 7) |
| ABCD; Sim2Real study | text | Not benchmarks: a calibration dataset (22.1 turns per human chat) and a real-user data source | Sim2Real timestamps feed τ-bench (ACQUISITION) |
| Remote Labor Index | mixed | Times and outcomes private; creative/multimedia mix; **CAIS found no negative slope** | Per-category times and outcomes from Scale/CAIS |
| UpBench, Agents' Last Exam, $OneMillion-Bench, xbench-Profession, OfficeBench, WorkBench, PRBench, Vals Index, OdysseyBench | mixed / text | Data not public, no times, not IT/BPO, or non-binary scores | UpBench data release (has O*NET tags and payouts) |
| FrontierFinance | computer_use | 4 models at one date; continuous scores; code and data "forthcoming" (has 10 measured task times, 6.5–35 h) | Release → long-end F&A anchor |
| MedAgentBench (+ PhysicianBench, MedHELM) | software | Saturated; clinical rather than BPO | — |
| Medical coding (ICD-10/CPT papers) | text | No multi-model, multi-date benchmark | **Build target**: MIMIC-IV/MDACE plus AHIMA charts-per-hour standards (ACQUISITION §4) |
| TaxCalcBench, Vals Tax Agent | text | Stale models, no times / tax research rather than clerical | Cheap rerun if tax prep becomes a priority line |
| DABstep, KYBench, FinSpread-Bench, Vals MortgageTax, BlueFin, FormFactory, FormGym | text / software | No per-item times, or all items one length (KYBench ~30 min), or not agentic | KYBench could supply one ~30 min point on a pooled curve |
| InsClaimBench (+ UNDERWRITE, InsLogicBench) | text | Release unclear, unnamed models, not agentic. **The only claims-adjudication content found.** | Release plus named, dated models; times from claims-per-day standards |
| Penrose AccountingBench | mixed | Effectively one long task; no updates since Jul 2025 | Cite qualitatively for error compounding |
| FinanceBench, SpreadsheetBench v1, SheetCopilot | text / software | Saturated or old | — |

**Counts:** Tier A 7; Tier B 36; Tier C about 95 named benchmarks in the 34 rows above. Several rows group related benchmarks, and four entries are evidence sources rather than benchmarks (Rein, Whitfill, ABCD, Sim2Real).

---

## Coverage map

Match quality is our reading of the benchmark descriptions against the occupation's core tasks. It is not yet a Stage 3 result. "Tier" is the best tier among the listed benchmarks.

### Pilot occupations

| Occupation | Best benchmark(s) | Tier | Match | Gaps |
|---|---|---|---|---|
| **Software QA Analysts and Testers (15-1253)** | SWT-bench Verified (regression and repro tests); SWEeper-Bench (exploratory QA plus fix); SWE-bench Verified / Multi-SWE-bench (bug fixing found in testing); TB2 (build/debug) | B for good matches; A only for partial | Good (B) for writing automated tests; partial (A) via bug fixing | **Manual test design and execution, test plans and defect reports have no usable benchmark.** WebTestBench and TestGenEval are excluded. SWT-bench's times are borrowed from fixing. |
| **Computer User Support Specialists (15-1232)** | WorkArena L1/++ (ServiceNow tickets, provisioning, catalog, KB); τ²-telecom (guided troubleshooting); EVA-Bench IT desk (voice); OSWorld-Verified (desktop settings); TB2 sysadmin subset | B for good matches; A (TB2, OSWorld 2.0) partial only | Good (B) for ticket handling in an ITSM tool and scripted troubleshooting; partial (A) for hands-on configuration | **Remote troubleshooting on a user's own Windows machine** (WAA is excluded, OSWorld is Linux). Hardware and in-person work is outside scope. |
| **Customer Service Representatives (43-4051)** | τ-bench retail/airline (chat); τ-Voice (voice); τ³-Banking; CRMArena-Pro (case routing, policy checks); GDPval CSR tasks | B | Good (B) for policy-bound transactional contacts | Complaint handling and de-escalation (ServiceBench has no binary score); outbound and sales calls; real-customer behaviour (Sim2Real). **All voice CS is Tier B with short series.** |

### BPO service lines (SPEC §5)

| Service line | Best benchmark(s) | Tier | Match | Gaps |
|---|---|---|---|---|
| App development and maintenance (15-1252, 15-1254) | SWE-bench Verified, Multi-SWE-bench, METR TH1.1; SWE-Lancer, SWE-bench Pro, SWE-rebench | A | Good (bug-fix tickets) | Greenfield feature builds and web-app builds (Vibe Code and SWE-Marathon are C); migration and modernisation (MigrationBench is C); enterprise stacks beyond Java/JS/Go (SAP ABAP, .NET, COBOL: one TB2 item). |
| Testing (15-1253) | as in the pilot table | B (good) / A (partial) | Partial at Tier A | Manual QA |
| Infrastructure and support: user support (15-1232) | as in the pilot table | B (good) / A (partial) | Partial at Tier A | Windows endpoint support |
| Infrastructure: sysadmin (15-1244) | Terminal-Bench 2 sysadmin subset; TB1/TB3; ITBench-AA | A | Partial: the TB2 time–success link is weak and only 9 items are tagged sysadmin | Cloud/IaC and network configuration (all C); incident RCA is Tier B only |
| Infrastructure: DBA (15-1242) | DBA-Bench; TB2/TB3 DB items (`db-wal-recovery`, `query-optimize`, `live-database-cutover`) | B (A for a handful of TB2 items) | Good (B) | DBA-Bench durations are the missing piece |
| Consulting and analysis (15-1211) | GDPval (Computer & Info Systems Managers, Project Management Specialists); TheAgentCompany PM tasks; APEX-Agents consulting | B | Partial | **Requirements analysis and system design have no benchmark**, and many of these tasks are interpersonal |
| Voice and chat support (43-4051) | τ family, τ-Voice, EVA-Bench, CRMArena-Pro | B | Good (B) | No Tier A. Real-user discount needed (flag 6). DECISIONS.md LIVE_SERVICE rule makes failure costly, so β and the real-user haircut matter more here. |
| Finance and accounting (43-3031, 43-3021) | Vals Finance Agent (A, analyst); OSWorld 2.0 (A, expense claims); APEX-Accounting, DualEntry, Finch, StarShell-ERPNext, UI-CUBE Concur/SAP (B) | A partial; B good | **Clerk work has good matches only in Tier B** | Billing and posting clerks (invoice posting in an ERP) rely on imputed times; no timed AP/AR benchmark |
| Data entry (43-9021) | UI-CUBE (copy-paste, enterprise forms); OmegaUse-OfficeVal (extract, reformat); WorkArena forms; OSWorld 2.0 (partial) | B (A partial) | Good (B) | Keying from scanned documents (MortgageTax and FormGym are C); per-item times only in OfficeVal |
| Insurance claims and policy processing (43-9041) | TB3/4 operations tasks (`medical-claims-processing`, `heat-pump-warranty`, `legacy-utility-triage`); HealthAdminBench appeals/denials | B | Partial (a handful of TB3 tasks; payer-side only) | **Effectively a gap.** InsClaimBench (adjudication) is C; no benchmark of policy servicing or endorsements. |
| Medical records (29-2072) | HealthAdminBench (EHR documentation, prior auth) | B | Partial (revenue cycle rather than records) | **Medical coding has no benchmark** (build target); no chart-abstraction or release-of-information benchmark |

**What this means for the comparison (SPEC §10).** Tier A today covers software and two narrow slices of finance and computer use. Fitted on Tier A alone, BPO would be measured almost entirely by software curves, and the BPO-vs-economy comparison would mostly compare software horizons with whatever the random sample matches. The pilot needs at least the τ family, WorkArena and SWT-bench in Tier A before Stage 3 coverage numbers mean much.

---

## Method flags

Each flag gives the evidence and what it means for our model.

1. **β units.** METR fits `σ(β·(log2 H − log2 t))`, so its β is per *doubling* of human time. SPEC §2 writes `σ(β[ln(H/k) − ln(mh)])`, which needs β per *ln-minute*. Convert with **β_ln = β_log2 / ln 2 ≈ 1.443 β_log2**. METR's default 0.6 becomes 0.87; the TH1.1 median 0.58 becomes 0.84; SWE-bench Verified's 0.51 becomes 0.74; the Kwa–Cheng exclusion line 0.25 becomes **0.36 per ln**. H itself does not depend on the base. Check each source's unit:
   - The Terminal-Bench researcher reported 0.27 *per ln* (= 0.19/log2), which is below the exclusion line.
   - The Vals Finance Agent slopes were reported *per doubling* (0.32–0.66, i.e. 0.46–0.95/ln).
   - METR also includes a chance floor c. It is irrelevant for agentic tasks (c ≈ 0), but our formula omits it, so don't port fits from multiple-choice benchmarks.
   - **Consequence:** fix the units in code before fitting, and state the unit in every table.

2. **k_b for test-graded code (SPEC §9 "7") rests on one model.** Whitfill et al. report a test-pass vs merge T50 ratio of ~2× (Sonnet 3.5), ~5× (3.7), ~9× (Opus 4), **~20× (GPT-5)** and ~6× (Sonnet 4.5, the "~7×"). The merge-based doubling-time difference is uninterpretable (95% CI −158 to +2 months). The robust result: **about half of test-passing PRs would be merged**. Golden patches were merged 68% of the time, and normalised to that, the grader overstates merges by 24.2 pp (SE 2.7). Rein (Aug 2025) found 0 of 15 test-passing PRs mergeable as-is, with ~42 min of fix-up. Consequences:
   - (a) The SPEC sensitivity range 3.5–14 doesn't span the evidence (2–20). Widen it.
   - (b) A **probability haircut** (π_accept = ρ·π_test with ρ ≈ 0.5–0.7) is the better-supported form. It behaves differently from a horizon divisor. Under the haircut, even trivial items are accepted at most ρ of the time, so the delegation condition for short items becomes ρ(1−κ) > b + a/h. With ρ = 0.5 and κ = 0.2, high-stakes items (b = 0.33) are **never** delegated (0.40 vs 0.33 + a/h). A divisor never blocks short items. Run both forms.
   - (c) Merge rates improved ~9.6 pp/yr more slowly than test-pass rates (weak). That points to k_b *rising* over time, the opposite of SPEC §10's "k_b halves" scenario. Add the opposite scenario.
   - (d) The fix-up time (~one third of task time) is evidence for the "partial use of rejected output" term SPEC §11 leaves out.

3. **Saturated benchmarks.** These have frontier scores at or above the human baseline, or at the ceiling:
   - SWE-bench Verified (90%+; contaminated; flawed tests on many hard items)
   - OSWorld-Verified (85–86% vs 72% human)
   - AndroidWorld (100%)
   - τ²-bench (telecom ~99% on AA; overall 85–88%)
   - SWT-bench (~90%)
   - Vals Finance Agent v1.1 (archived)
   - GDPval win-or-tie (80–85%)
   - WorkArena L1 (GPT-5 79%; custom agent 90%)
   - ERPBench, DualEntry, MedAgentBench, Vibe Code v1, Spider2-Snow
   - METR TH1.1 itself above 16 h

   **Consequence:** H is unidentified for frontier models on these. Fit H only on models clearly below the ceiling, and splice each benchmark to a harder successor of the same kind for 2026: Verified → Pro/rebench; OSWorld → OSWorld 2.0; τ² → τ³/τ-Voice; FAB v1.1 → v2.1; TB2 → TB3/4. Splicing assumes the two benchmarks share a curve, which needs a check on models run on both.

4. **Benchmarks where the logistic in log time fits poorly.**
   - *OSWorld 2.0:* success is flat at ~20% up to ~2 h, then collapses to 0 above 163 min. Read literally, H50 sits below the shortest bin and β is very shallow up to 2 h.
   - *Remote Labor Index:* CAIS found the relation "flat to slightly rising".
   - *Terminal-Bench 2:* corr −0.28; pooled β below the exclusion line; frontier slopes ~0. Author difficulty labels correlate only r = 0.436 with empirical difficulty.
   - *GDPval* is the counter-example: Fig. 13 shows win rate falling steadily with length.

   **Consequences:** For OSWorld 2.0, TB2 and any RLI-like suite, use a pooled β (METR's 0.58/log2, or a pooled fit across benchmarks in the same domain) with a benchmark-specific H. Alternatively, report D for those matches with and without length dependence. Apply the exclusion rule per benchmark or subset, not just per suite. Suites mixing very different work (RLI) should be fitted within category or not at all. Two further points:
   - METR's own sensitivity note found other link functions cut recent H50 by up to 35%. It also found a **single slope shared across models** cross-validates best, which supports fitting one β_b per benchmark across models.
   - Time noise flattens β. Baseliner times are within ~3× of truth 80% of the time, estimates within ~4×, and a SIMEX correction cut Opus 4.6's H50 by 25–40%. Benchmarks with author-estimated times (TB, OSWorld 2.0, APEX) will show shallower slopes partly for this reason.

5. **Agent-framework (scaffold) dependence.**
   - WebArena ranges 14–74% across systems, many on non-frontier models.
   - OSWorld and AndroidWorld leaderboards mix base models with frameworks.
   - SWE-bench Pro changed harness mid-series.
   - SWT-bench and Spider 2.0 are dominated by bespoke systems.
   - TB2 entries are scaffold-tuned.
   - StarShell found terminal/API agents match or beat web agents on the same tasks at 3–8× lower cost.

   METR found Claude Code and Codex don't beat its default scaffold on its suite, but that was software, not web. **Consequence:** fit trends on fixed-harness rows only (BrowserGym GenericAgent, HAL, Terminus-2, mini-SWE-agent). Treat best-system results as an upper-envelope scenario. For web and GUI matches, the measured horizon may *understate* what a firm gets from an API-connected agent on the same work. Record the harness per data point.

6. **Simulated vs real users (τ family).** Sim2Real had 451 real participants play the τ-bench customer against one agent. Success was 63.6% with real humans, vs up to 77.8% with LLM simulators. The binary reward was largely orthogonal to human-perceived quality. **Consequence:** apply a real-user haircut of about 0.82 (63.6/77.8) to π for τ-matched items, or treat it as a k_b > 1 for this family. Under the DECISIONS.md LIVE_SERVICE rule, failures cost (1−π)λh, so this haircut moves D more than it would under the standard review rule. Real customers also lengthen conversations, which matters for item times imputed from simulated runs.

7. **Grading strictness by k_b class.** SPEC §9 gives k_b only for *test* (7) and *expert* (1). Evidence for the other classes:
   - Outcome-only state checks overstate acceptability in regulated work. CXBench: 55.5% of runs are "false passes" (correct outcome, failed process checks); only 13.8% pass both. ST-WebAgentBench: completion under policy is ~38% below raw completion.
   - LLM judges can be lenient. RLI's LLM judge overstated newer models' automation rates 2–3× against experts; the GDPval autograder agrees with experts 66% of the time vs 71% between experts.
   - **Consequence:** set *state*-graded k_b between 1 and the test value, with a wider band for regulated BPO (claims, banking, KYC). Treat *LLM*-judge benchmarks as needing k_b > 1 unless validated against human graders (Vals, APEX and HealthAdminBench report such validation). Expert-pairwise benchmarks (GDPval) keep k_b ≈ 1, but "win or tie vs a professional" is our acceptance outcome only if ties count.

8. **Licence and access limits.**
   - Mercor's APEX-Agents Qwen trace card forbids "training, fine-tuning, or parameter fitting", so we cannot fit curves on those traces. Our own runs avoid the problem. Check the APEX task-data licence (CC-BY-4.0 per HF) separately from the trace licence.
   - Gated but auto-approved (licence acceptance needed): OSWorld 2.0 tasks and trajectories (Apache-2.0), APEX data, WorkArena ServiceNow instances.
   - HAL traces are encrypted (`hal-decrypt`).
   - Epoch data are CC BY 4.0.
   - SWE-bench Verified submissions are restricted to academic teams since 2025-11-18, which ends the clean public series.
   - Spider2-Snow access has been disrupted since Aug 2026.
   - GDPval and RLI per-task data are private.
   - **Consequence:** prefer our own runs wherever a source's terms are unclear, and record licence status per data file.

9. **Whose minutes?** METR's human times are low-context contractor times. Contractors took 5–18× longer than maintainers on the same issues. SWE-bench annotators assumed familiarity with the codebase; Multi-SWE assumed a few hours of familiarisation; GDPval used the task writer's own estimate; OSWorld timed students new to the tasks. **Consequence:** benchmark time scales are not on a common footing. SPEC's m multiplies item length by context, which assumes the benchmark's H is in low-context minutes. That holds for METR but not for SWE-bench Verified ("familiar with the codebase"). Record each benchmark's time definition, and consider a per-benchmark time-scale correction fitted on items timed both ways (METR spot checks; APEX baselining).

10. **Estimated vs measured times are biased, in both directions.**
    - APEX-Agents estimates ran high (1.70 h vs 1.37 h actual). The report calls this "~33% high", but those numbers give ~24%; use the factor 0.81.
    - FrontierFinance estimates ran low (12.5 h estimated; the observed times run 6.5–35 h, mean 18.3 h).
    - SWE-bench annotators underestimate easy tasks, which makes the doubling time look faster (70 vs 104–143 days).
    - LLM time estimates run high by 2–3×.

    **Consequence:** never mix measured and estimated times within one fit without a correction term. Report which benchmarks rest on estimates.

11. **Version breaks.** Each of these needs a version field per data point, and no fit should span a break:
    - τ 1.x vs 2.0, and τ³'s v1.0.1 regrade
    - OSWorld 2.0's three releases
    - APEX-Agents v1 vs v1.1
    - GDPval-AA v1 vs v2
    - Vals FAB v1.1 vs v2.x
    - Terminal-Bench pools that drop saturated tasks
    - OSWorld step budgets 15/50/100

12. **Model dates.** Many leaderboards record submission dates, not model release dates (SWE-bench/experiments, Spider 2.0, SpreadsheetBench). **Consequence:** join to Epoch's `Release date` column. Use frontier points only (models that beat every earlier H), as SPEC §4 says.

13. **Continuous scores need a threshold.** OfficeVal, FrontierFinance, SpreadsheetBench, ITBench (AP), APEX-Accounting (mean criteria) and Vals FAB v2.1 (partial credit) all report graded scores. **Consequence:** pick the binarisation per benchmark to match acceptance: all criteria pass, or score ≥ the human's score on that task. H depends on the choice, so report the sensitivity.

---

## Methods for missing human times (ranked)

| Rank | Method | Validation evidence | Where we'd use it |
|---|---|---|---|
| 1 | **Native per-item times, timed baselines first** (METR: geometric mean of successful attempts) | METR: baseline attempts are within ~3× of the true length 80% of the time; arithmetic means run ~25% above geometric. | METR TH1.1, OfficeVal, Cybench (fastest team, biased low), FrontierFinance (10 tasks) |
| 2 | **Times the authors already hold** (recorded but unpublished) | Same quality as rank 1 once released | WorkArena++ (98 instances), OSWorld-1 timing log, OSWorld 2.0 t_i, DBA-Bench human runs, Sim2Real chat logs, UI-CUBE HumanEval logs, Vals test-set times, GDPval |
| 3 | **Native estimates or buckets** (annotator or author estimates; buckets → geometric midpoints 3.9/30/120/480 min, or interval-censored) | METR: estimates within ~4× 80% of the time. SWE-V buckets were spot-checked with 7 baselines on 6 tasks; easy tasks are underestimated, which shortens the doubling time. APEX estimates ran ~24% high on a 96-task baseline. TB author labels r = 0.436 with empirical difficulty. | SWE-V, Multi-SWE, TB1–4, APEX-Agents, Vals FAB |
| 4 | **Our own timing study on a stratified sample** (20–30 items per benchmark, or one item per template) | The only route that gives measured times for Tier B; also calibrates ranks 5–7. Costs from the reports: WorkArena ~1 annotator-day (33 templates); CRMArena-Pro ~15 h (95 items); τ pilot a few contractor-days; TAC 20–30 tasks. | WorkArena, τ family, CRMArena-Pro, HealthAdminBench, SWEeper, TheAgentCompany, UI-CUBE |
| 5 | **IRT calibration (BRIDGE)**: 2PL IRT on the item × model matrix; regress difficulty on log time for anchor items; predict the rest | R² = 0.81 on METR. Cybench: 92.3% of items within 0.5–2× of first-solve time. Beats LLM estimators on SWE-V buckets; ranks stable with 70% of cells missing (ρ > 0.94). **Caveat for us:** difficulty comes from model success, so imputed times are partly circular. Fitting β on IRT-imputed times overstates how well length predicts success. Use them for H with an externally set β, or only where real anchors dominate. | Benchmarks with item × model matrices but no times: τ (HAL), TheAgentCompany, SWE-bench Pro/rebench, Online-Mind2Web |
| 6 | **Step, action or turn counts × calibrated seconds per step** | Weak. OSWorld 2.0 agent step counts rise with human-time bins. METR: committed LOC per day explains ~46% of variance in estimated minutes. No validated conversion factor found. OSWorld-Human comes with a built-in check (the imputed distribution must match the 112 s median and 28.7/40.1/30.2% bucket shares). WebArena/VisualWebArena traces give a seconds-per-action rate. | WorkArena L1 (oracle actions), OSWorld-Verified (OSWorld-Human), Online-Mind2Web, SCUBA, SOPBench, τ (gold actions plus turns) |
| 7 | **Industry throughput standards** (APQC invoices per FTE, AHIMA charts per hour, claims per examiner-day, contact-centre AHT) | None at item level. Definitions vary: after-call work included or not; concurrent chats inflate Brynjolfsson et al.'s 43 min. Gives category-level times only. | DualEntry, medical coding, InsClaimBench, τ (as anchor), HealthAdminBench |
| 8 | **LLM-estimated times with a multiplicative correction** fitted on anchor items | METR transcript note: GPT-5 vs 34 human estimates, r_log = 0.83, within 2–3×, **biased high**. BRIDGE: overestimates on Cybench. WeirdML: 3–8× above the author's estimates. One argument in favour: our Stage 2 coders already LLM-estimate O*NET item lengths, so a common multiplicative bias would partly cancel in ln(H/h). That holds only if the bias is the same across work types, which is untested. | Fallback for GDPval gold set, JobBench, Finch, SpreadsheetBench 2 |
| 9 | **Freelance price → hours** | Weakest. SWE-Lancer task value did not correlate with model success, and prices rise when issues go unsolved. RLI hours roughly track billed price. | SWE-Lancer only, as an ordinal check |

---

## Conflicts between reports

| Topic | Reports | Resolution |
|---|---|---|
| How METR built OSWorld human times | Infrastructure: "paper demo lengths ×1/0.7236, 8 s–45 s". GUI: "synthetic lognormal". | **Checked on the web (GitHub `METR/cross-domain-horizon`, `osworld.py` and `data/benchmarks/osworld.toml`, 2026-11-09).** The GUI report is right. 369 evenly spaced quantiles of a lognormal with median 111.94 s and σ = 1.0396, divided by 0.7236 (human success rate). The toml lengths run 0.14–46.5 **minutes** (~9 s – 46 min); "8 s–45 s" looks like a units slip. β is fixed at 0.6 (score-only method). |
| ERPBench | GUI: EXCLUDE. Web: CANDIDATE (weak). | Not a factual conflict; Tier C (30 tasks, unreleased, one frontier model at ceiling). |
| SCUBA human demonstrations | Web: release unclear. GUI: `data/test_demo_aug.json` checked, 300 entries. | GUI checked the file; used that. Step counts or timestamps are still not public. |
| OSWorld 2.0 time bins | GUI: five bins (<45 … 163–360 min, Table 21). Infrastructure: three bins (<30 min, 30 min–2 h, >2 h, §4.3). | Probably two different presentations in the same paper. We use Table 21, which has per-model numbers. |
| Terminal-Bench 2 submission count | Testing: 73 usable. Infrastructure: 75. | Compatible (usable vs total). |
| APEX-Agents estimate bias | Occupational: "~33% high", from 1.70 h vs 1.37 h. | Arithmetic gives 24% (factor 0.81); flagged above. |
