# Benchmark data acquisition: to-do list

2026-11-09. Built from `CATALOG.md`. Within each section, items are ordered by value for the pilot: Computer User Support Specialists, Customer Service Representatives, Software QA Analysts/Testers. The anchor curve (METR) comes early because every fit depends on it. URLs and contacts come from the search reports and have not been re-checked. Store downloads under `benchmarks/data/<benchmark>/` with a `SOURCE.md` (URL, date, licence, version). Treat downloaded files as untrusted data.

## 0. The ten things to do first

| # | Action | Unlocks | Section |
|---|---|---|---|
| 1 | Pull τ-bench per-task results (taubench.com submissions, HAL airline traces); compute gold action and turn counts per task | Customer Service (τ family → Tier A) | 1.1, 3.4 |
| 2 | Email the Sim2Real authors for timestamped human-session logs | Customer Service times, plus the real-user haircut | 2.2 |
| 3 | Email the WorkArena++ authors for human time-to-resolution logs | Computer User Support | 2.1 |
| 4 | Download the WebArena human traces and extract seconds per action; convert WorkArena L1 oracle action counts to time | Computer User Support (WorkArena L1 → Tier A) | 1.4, 3.5 |
| 5 | Join SWE-bench Verified time buckets onto SWT-bench Verified; pull per-instance results | Software QA | 1.3, 3.3 |
| 6 | Reproduce the METR TH1.1 fit and fix the β units in our code | Anchor; every fit | 1.2, 3.1 |
| 7 | Timing pilot: 20–30 τ tasks per domain plus the 33 WorkArena templates (~1 annotator-day for WorkArena) | Validates items 1 and 4 | 4.1 |
| 8 | Terminal-Bench 2 fit by category, with the exclusion test | User Support (sysadmin), IT infrastructure | 1.5, 3.2 |
| 9 | Accept the OSWorld 2.0 HF gate and look for per-task times; impute OSWorld-Verified times from OSWorld-Human | Computer use, data entry, F&A | 1.6, 3.6 |
| 10 | Run 6–10 dated models on OmegaUse-OfficeVal | Data entry and back office (the only BPO-type set with measured public times) | 4.2 |

---

## 1. Datasets to download

### 1.1 Customer service (pilot: CSR; partly User Support via telecom)

- **τ²-bench / τ-bench 2.0 code and tasks:** https://github.com/sierra-research/tau2-bench (read `CHANGELOG.md` and `docs/leaderboard-submission.md`).
- **Official submissions, per task and trial:** taubench.com, repo path `web/leaderboard/public/submissions/*/benchmark-submission.json`. Record `model_release.release_date` where present.
- **Trajectories:** `s3://sierra-tau-bench-public/`. Public readability not yet confirmed; test with an anonymous `aws s3 ls`.
- **HAL τ-bench airline traces:** https://hal.cs.princeton.edu/taubench_airline. Encrypted; decrypt with `hal-decrypt`. Per HAL's 2026-10-05 notice, strip `taken_actions` using `task.actions`.
- **τ-Voice / voice-v2 packages:** check `interaction_metrics` and `benchmark-diagnostics.json` for per-call durations.
- **CRMArena-Pro:** HF `Salesforce/CRMArenaPro`; code at https://github.com/SalesforceAIResearch/CRMArena.
- **EVA-Bench:** https://github.com/ServiceNow/eva.
- **SOPBench** (24k trajectories): https://github.com/Leezekun/SOPBench.
- **Calibration:** Brynjolfsson, Li & Raymond (NBER w31161) topic-level handle times; ABCD turn counts (arXiv 2104.00783).

### 1.2 Anchor and cross-cutting

- **METR TH1.1:**
  - https://github.com/METR/eval-analysis-public, file `reports/time-horizon-1-1/data/raw/runs.jsonl`.
  - https://metr.org/assets/benchmark_results_1_1.yaml and https://metr.org/assets/task_results_1_1.yaml (these add Gemini 3.1, GPT-5.4 and Mythos).
- **METR cross-domain code and data:** https://github.com/METR/cross-domain-horizon (`mle.py`, `calculate_horizons.py`, `data/horizons/*.csv`, `data/benchmarks/*.toml`).
- **Epoch Benchmarking Hub:** https://epoch.ai/data/benchmark_data.zip (CC BY 4.0). Needed for model **release dates** and `metr_time_horizons_external.csv`. Inspect `.eval` logs on S3 give per-sample SWE-bench Verified results.
- **BRIDGE code** (IRT time imputation): https://github.com/McGill-NLP/BRIDGE.

### 1.3 Software QA and app maintenance (pilot: QA)

- **SWE-bench Verified:**
  - HF `princeton-nlp/SWE-bench_Verified` (`difficulty` field).
  - Annotation zip: https://cdn.openai.com/introducing-swe-bench-verified/swe-bench-annotation-results.zip.
  - Per-instance results: https://github.com/SWE-bench/experiments (`evaluation/verified/*/results/`).
- **SWT-bench:** https://swtbench.com and https://github.com/logic-star-ai/swt-bench. Follow each leaderboard entry's trajectory link (GitHub or files.sri.inf.ethz.ch) and check for per-instance pass/fail.
- **SWEeper-Bench:** HF `zlab-princeton/SWEeper-Bench` and `zlab-princeton/SWEeper-Bench-traces`.
- **Multi-SWE-bench:**
  - Per-item time labels: `docs/manual-verification/annotation-results/{java,js,ts,go,rust,c,c++}.xlsx` in https://github.com/multi-swe-bench/multi-swe-bench. Columns `问题 5.1-1` / `5.1-2` hold the two raters' buckets.
  - Results: https://github.com/multi-swe-bench/experiments.
- **SWE-bench Pro:** HF `ScaleAI/SWE-bench_Pro` (patch and category fields for imputation); trajectories via labs.scale.com.
- **SWE-Lancer:** `all_swelancer_tasks.csv` in https://github.com/openai/preparedness/tree/main/project/swelancer.

### 1.4 Service desk and enterprise web (pilot: User Support)

- **WorkArena / WorkArena++:** https://github.com/ServiceNow/WorkArena. Oracle action counts per task are in the paper, arXiv 2403.07718. BrowserGym leaderboard files are in HF Space `ServiceNow/browsergym-leaderboard` (`results/*/workarena-l1.json` etc.); check per-task granularity and submission dates.
- **WebArena human Playwright traces** (179 tasks): Google Drive link in https://github.com/web-arena-x/webarena/blob/main/resources/README.md. First check whether METR already extracted these times in `cross-domain-horizon`.
- **VisualWebArena traces** (233 tasks): https://github.com/web-arena-x/visualwebarena. Use them only to calibrate seconds per action.
- **StarShell:** https://github.com/ServiceNow/StarShell and HF collection `ServiceNow-AI/starshell`. Check whether per-task results for the 4 frontier models are published.
- **UI-CUBE:** https://github.com/UiPath/uipath_enterprise_benchmark (`DeterministicBenchmark/src/HumanEval.tsx` shows the timing set-up).
- **SCUBA:** https://github.com/SalesforceAIResearch/SCUBA (`data/test_demo_aug.json`).

### 1.5 IT operations

- **Terminal-Bench 2.0:**
  - Task metadata: https://github.com/harbor-framework/terminal-bench-2. Use `task.toml` for `expert_time_estimate_min`, `junior_time_estimate_min` and `category`.
  - Per-trial results: HF `harborframework/terminal-bench-2-leaderboard`.
- **Terminal-Bench 1.0:** https://github.com/harbor-framework/terminal-bench-1 (`original-tasks/*/task.yaml`; check the `leaderboard/` folder).
- **Terminal-Bench 3/4:** https://github.com/harbor-framework/terminal-bench (`tasks/*/task.toml`, `expert_time_estimate_hours`). Per-trial results via Harbor Hub (hub.harborframework.com).
- **ITBench-AA:** HF `ArtificialAnalysis/ITBench-AA`; https://github.com/itbench-hub/ITBench.
- **Cybench:** https://cybench.github.io (per-task first-solve times plus logs). Low priority.

### 1.6 Computer use, back office, finance, healthcare

- **OSWorld 2.0:**
  - Tasks: HF `xlangai/osworld_v2_tasks` (gated, auto-approve, Apache-2.0). After accepting, grep the task files for a time field.
  - Trajectories: HF `xlangai/osworld2.0-trajectory` (299 GB). Fetch only the per-task `result.json` if the layout allows.
- **OSWorld-Verified:** HF `xlangai/ubuntu_osworld_verified_trajs` (`all_result.json`, per-task 0/1).
- **OSWorld-Human:** https://github.com/WukLab/osworld-human (per-task human action sequences).
- **OmegaUse-OfficeVal:** HF `baidu-frontier-research/OmegaUse-OfficeVal`; code at https://github.com/baidu-frontier-research/OmegaUse-OfficeVal.
- **Vals Finance Agent:**
  - Public CSVs: https://raw.githubusercontent.com/vals-ai/finance-agent/main/data/public.csv and https://raw.githubusercontent.com/vals-ai/finance-agent-v2/main/data/public.csv.
  - Leaderboard JSON: scrape and save page snapshots of https://www.vals.ai/benchmarks/finance_agent_v1 (and the dated snapshot pages) and https://www.vals.ai/benchmarks/fabv2-1.
- **HealthAdminBench:** https://github.com/som-shahlab/health-admin-bench.
- **TheAgentCompany:** https://github.com/TheAgentCompany/TheAgentCompany and https://github.com/TheAgentCompany/experiments. Also Wang et al. 2025 (arXiv 2510.22780), with 48 timed workers on TAC-style tasks, for calibration.
- **Finch:** HF `FinWorkBench/Finch`. **SpreadsheetBench 2:** https://github.com/RUCKBReasoning/SpreadsheetBench-2. **APEX-Accounting public world:** HF `mercor/apex-accounting`, `mercor/apex-accounting-harbor`.
- **APEX-Agents:** HF `mercor/apex-agents` (gated, CC-BY-4.0; per-task expert time estimates). **Do not** use `mercor/ApexAgentsRecipe-ApexAgents480-EvalTraces` for fitting: its licence forbids parameter fitting.
- **GDPval:** HF `openai/gdpval` (220 gold tasks; no times). Digitise Fig. 13 of arXiv 2510.04374 (win rate by task length).
- **Calibration standards:** APQC invoices per AP FTE; AHIMA/himagine coding charts per hour; HFMA RCM follow-up norms (sources listed in `search/back_office_finance.md`).

---

## 2. Author requests

Ordered by pilot value. Each request should say what we'll use the data for: aggregate fits only, with a citation and a copy of the results.

| # | To | Ask for | Why it matters |
|---|---|---|---|
| 2.1 | **WorkArena++**: Léo Boisvert, Alexandre Drouin, Maxime Gasse (ServiceNow Research) | Per-instance human time-to-resolution for the 98-instance human curriculum (L2 and L3), with instance IDs. Also per-task leaderboard results with run dates. | The most job-relevant benchmark for Computer User Support; the times already exist. Moves WorkArena++ to Tier A. |
| 2.2 | **Sim2Real study** (arXiv 2603.11245): Zhou, Sap, Neubig et al. (CMU) | Timestamped chat logs for the 495 real-user sessions on 165 τ-bench retail/airline tasks, with per-session outcomes | The only human-paced conversation lengths for τ items (CSR times), plus the per-task real-vs-simulated success gap |
| 2.3 | **OSWorld / OSWorld 2.0**: XLANG Lab (Tianbao Xie, Tao Yu; leaderboard contacts in the OSWorld-V2 README) | (a) Per-task t_i (the two annotator ranges) for OSWorld 2.0, if not in the gated files. (b) The original per-task human timing log behind Fig. 4 of the OSWorld paper. | Per-item computer-use times. (b) also lets ChainWorld inherit times and replaces METR's synthetic lognormal. |
| 2.4 | **DBA-Bench**: Chen, Jiang et al. (UESTC; GitHub TanJI-C/DBA-Bench) | Per-scenario durations or timestamps from the human DBA runs (106 scenarios), and the promised per-item evaluation artifacts | The only DBA benchmark with matched human runs; DBA is a core infrastructure line |
| 2.5 | **Sierra** (τ-bench team: Barres, Narasimhan) | Per-call durations for τ-Voice / voice-v2 runs; confirm public access to `s3://sierra-tau-bench-public/` | Free duration proxy for voice CS items |
| 2.6 | **UiPath** (UI-CUBE: Cristescu et al.) | Per-task human times from the HumanEval runs, and per-task model results | Enterprise data-entry tasks (SAP/Concur/Workday) with times already recorded |
| 2.7 | **Vals AI** | Test-set per-item `Expert time (mins)` and per-item correctness for Finance Agent v1.1 and v2.x | Makes Vals FAB a full per-item dataset with 57+ dated models |
| 2.8 | **Mercor** (apex@mercor.com) | APEX-Accounting per-task expert time estimates and per-task pass rates; per-task times from the CPA baseline study; APEX-Agents per-model item results with written permission to fit curves | F&A clerk work (reconciliation, accruals, data entry) has no timed benchmark |
| 2.9 | **HealthAdminBench**: Shah lab, Stanford | Minute-level data from the 100+ h staff shadowing, or per-task time estimates; the released "model outputs" | Medical-records / RCM line |
| 2.10 | **Salesforce AI Research** (SCUBA) | Human annotation trajectories with timestamps or step counts per task | CRM admin and service-agent work |
| 2.11 | **OpenAI** (GDPval) | Per-task expert times and per-task win/tie outcomes for the 220 gold tasks (ideally all 1,320) | Best O*NET link; includes CSRs, accountants, order clerks |
| 2.12 | **SWE-bench team** (John Yang et al.) | Per-instance time buckets for SWE-bench Multimodal | Front-end maintenance with a longer time range |
| 2.13 | **Harbor / Terminal-Bench**: Merrill, Shaw | TB 3/4 per-trial results (Harbor Hub API); TB1 per-task leaderboard results | TB3/4 includes claims-processing operations tasks with expert-hour times |
| 2.14 | **Artificial Analysis** | ITBench-AA per-item results by model | SRE/production-support line |
| 2.15 | **METR** | Item-level data from the 18-issue algorithmic-vs-holistic study (Rein) and the Whitfill per-PR reviews; whether extracted WebArena trace times exist | Acceptance adjustment (k_b) for code, with fix-up times |
| 2.16 | Low priority: Scale/CAIS (RLI per-project times and outcomes by category); Alibaba (CirrusBench ticket handle times); Upwork (UpBench data) | — | Caution or watch-list items |

---

## 3. Fits we can run ourselves now

Code: start from METR's `mle.py`. One logistic per model; frontier models only; then a trend in ln H against release date. **Use β per ln-minute** (METR's per-log2 β × 1.443) and record the unit.

| # | Fit | Inputs | Notes |
|---|---|---|---|
| 3.1 | **METR TH1.1 reproduction** | `runs.jsonl` plus YAMLs | Check that H50 matches METR (the infra researcher matched to within 1%). Build a SWE-only family subset. Stop at 16 h. |
| 3.2 | **Terminal-Bench 2.0** by category (sysadmin, debugging, data processing, SE) | `task.toml` times plus HF per-trial results | Expert times as primary, junior as sensitivity. Test β against the 0.36/ln exclusion line per subset. Terminus-2 rows for the trend. |
| 3.3 | **SWE-bench Verified, 2023–mid-2025**, and **SWT-bench Verified** on the same buckets | experiments `results/` plus Epoch logs; bucket join on `instance_id` | Interval-censored buckets, or geometric midpoints 3.9/30/120/480 min. Run with and without a Whitfill haircut. Treat SWT times as an upper bound. |
| 3.4 | **τ-bench** per task, with imputed times | Submissions plus HAL traces; gold action and turn counts | minutes_i = handle time for the call type × actions_i / mean actions. Validate against the 4.1 pilot and the Sim2Real logs once they arrive. Run once with the 0.82 real-user haircut. |
| 3.5 | **WorkArena L1** with action-count times; WebArena with trace times | WebArena traces → seconds per action; oracle action counts; BrowserGym GenericAgent overall scores | Overall scores only, so use the score-only method with a pooled β. Add StarShell's 2026 per-category points. |
| 3.6 | **OSWorld 2.0, bin level** (5 bins × 4 models); **OSWorld-Verified** with OSWorld-Human-imputed times | Table 21; `all_result.json`; OSWorld-Human | Expect a poor logistic fit. Compare a free β with a pooled β. Check imputed OSWorld times against the 112 s median and the bucket shares. |
| 3.7 | **Multi-SWE-bench** per language | xlsx buckets plus experiments results | Java/JS/TS first (AMS stacks). Thin 2026 coverage. |
| 3.8 | **Vals Finance Agent**, category level | Category medians from public CSVs; per-category accuracy from page JSON | Redo the researcher's rough fit with uncertainty; pool v1.1 and v2.1 only through models scored on both. |
| 3.9 | **Score-only H** for APEX-Agents (domain-level times) and τ³ | Leaderboards plus pooled β | Treat as ±2×. |
| 3.10 | **Pooled-β check**: fit one β per domain across Tier A benchmarks | All of the above | Gives the fallback β for weak-slope benchmarks (TB2, OSWorld 2.0). |
| 3.11 | **BRIDGE-style IRT imputation** as a cross-check (not for β) | Item × model matrices (HAL, TAC, SWE-Pro) | The circularity caveat applies (CATALOG, methods rank 5). |

---

## 4. Running models and people ourselves

### 4.1 Human timing studies (cheap, high value)

| # | Benchmark | Sample | Cost (from reports) | Unlocks |
|---|---|---|---|---|
| a | τ-bench retail, airline, telecom, τ³ banking | 20–30 tasks per domain; a contractor plays the agent through the tool API, with a human or LLM customer | A few contractor-days | CSR times; validates the action-count imputation |
| b | WorkArena L1 | All 33 templates on a free ServiceNow developer instance | ~1 annotator-day | User Support; validates the seconds-per-action rate |
| c | SWEeper-Bench / SWT-bench | 20–30 items, timed or expert-estimated | 1–2 QA-engineer-days | QA times on QA tasks rather than borrowed fix times |
| d | CRMArena-Pro | ~5 items per task type (~95), 3–5 Salesforce admins | ~15 h | CS case handling, CRM back office |
| e | HealthAdminBench | Stratified 20–30 tasks | RCM specialist, 2–3 days | Medical-records line |
| f | TheAgentCompany | Estimates for all 175 by 2–3 annotators; time 20–30 | 2–4 days | IT-services mixed roles |
| g | UI-CUBE (if UiPath doesn't share) | Enterprise subset (40 scenarios plus 50 business-process tasks) | ~1 day (tasks are short) | Data entry |

### 4.2 Running dated models (needs API access to older models)

Many older models are deprecated on vendor APIs. Plan around models that are still served, plus open-weight models with known release dates (Llama, Qwen, DeepSeek, GLM). Fix the harness across models, and record model ID, harness and date.

| # | Benchmark | Why us | Cost and feasibility |
|---|---|---|---|
| a | **OmegaUse-OfficeVal** | Measured public times; only one snapshot of open models | $0.2–1.8 per task × 100 × 6–10 models. Binarise the verifier score (full pass, or ≥ the human score on that task). |
| b | **WorkArena++ / L1** (AgentLab) | No 2026 frontier rows on the fixed harness | Needs a gated ServiceNow instance from the HF pool |
| c | **τ² / τ³** (if submissions are thin for older models) | Fixed user simulator across dates | Open harness, cheap |
| d | **HealthAdminBench** | One date only; public environments | Moderate (computer-use runs) |
| e | **SWEeper-Bench** | Single 2026 snapshot; adds a trend | Moderate; browser verifier |
| f | **CRMArena-Pro** | Series stops Apr 2025 | Open data and code; cheap |
| g | **Multi-SWE-bench mini/flash** | Few closed frontier models after mid-2025 | Docker harness |
| h | **SWE-Lancer IC Diamond** (198 tasks, Inspect) | OpenAI-only series | Moderate; offline-runnable since Jul 2025 |
| i | **UI-CUBE** | 2025 only | Open harness |
| j | **Terminal-Bench 3/4** (`harbor run`) | Only if Harbor Hub results are not available | 8 h timeouts make this expensive |
| k | **Medical coding (build)**: MIMIC-IV / MDACE discharge summaries, per-chart exact match, times from AHIMA charts-per-hour by chart type | No multi-model benchmark exists for a major BPO line | Needs credentialed PhysioNet access and its data-use agreement |
| l | Finch, SpreadsheetBench 2, DualEntry-style cases, TaxCalcBench | Back-office coverage | Low priority until the pilot shows matches there |
