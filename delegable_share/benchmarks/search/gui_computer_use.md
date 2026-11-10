# GUI / desktop / OS computer-use benchmarks: catalog for the time-horizon method

Researcher: GUI/computer-use slot. Searched 2026-11-09. Everything below was checked against primary sources (arXiv full text, GitHub repo trees, HF dataset listings) unless marked **[unverified]**. Model scores marked "self-reported" come from vendor launch posts as collected by leaderboard aggregators (steel.dev, Yutori, BenchLM). I did not cross-check those against the vendor posts. I also did not verify release dates for models released after mid-2025. Pull them from Epoch's model database.

## Bottom line

- **The key fact for this domain: no GUI benchmark has public per-item human times today, but two are one step away.**
  - *OSWorld 2.0* (XLANG, Jun 2026): every one of its 108 tasks has a human time from two annotators who timed it. Median ≈ 1.6 h; 69.6% of tasks take over 1 h. The paper publishes success by five time bins for four models (App. G.2, Table 21). The per-task values t_i are probably in the gated HF task repo or available from the authors.
  - *OSWorld 1.0/Verified*: the authors timed every task with human testers (median 112 s) but released only the distribution. METR's cross-domain horizon for OSWorld therefore used a **synthetic lognormal** of 369 times fitted to the median and the Easy/Medium/Hard shares, with the slope fixed at β = 0.6 (`METR/cross-domain-horizon/osworld.py`). Any OSWorld horizon published so far is not an item-level fit.
- **Saturation splits the domain.** OSWorld-Verified (frontier ≈ 85–86%, above the 72% human baseline) and AndroidWorld (100%) are saturated. They are useful only for the 2024–25 part of the trend. OSWorld 2.0 is the unsaturated frontier benchmark: 20.6% binary completion in the authors' best run, and 41.7% in a self-reported vendor run on a modified version.
- **Enterprise-application GUI benchmarks** (UiPath UI-CUBE with SAP/Salesforce/Concur/Workday mocks, Salesforce SCUBA, Accenture ERPBench on ERPNext, Stanford HealthAdminBench on Epic-like EHR and payer portals) match Indian IT/BPO work best. Each has at most category- or tier-level human durations and only 1–7 model configurations at a single point in time. None supports a trend over time yet.
- **OSWorld 2.0's binned data argue against a clean logistic.** Opus 4.7 scores 20.0 / 19.0 / 16.7 / 5.0 / 0.0% across bins of <45, 45–90, 90–137, 137–163 and >163 min. Success is flat at about 20% up to about 2 h, then collapses. The authors say outright that the METR time-horizon pattern "transfer[s] only partially" to computer use. Read literally, the 50% horizon lies below the shortest bin, and β fitted on log-time would be very shallow. Treat any GUI horizon as poorly identified.

---

## 1. OSWorld 2.0

- **Paper/URL:** "OSWorld 2.0: Benchmarking Computer Use Agents on Long-Horizon Real-World Tasks", arXiv:2606.29537 (v1 28 Jun 2026, v2 13 Jul 2026). https://osworld-v2.xlang.ai/ · https://github.com/xlang-ai/OSWorld-V2 · tasks at HF `xlangai/osworld_v2_tasks` (gated, auto-approve, Apache-2.0) · trajectories at HF `xlangai/osworld2.0-trajectory` (gated, 299 GB).
- **Maintainer:** XLANG Lab (HKU; Tianbao Xie, Tao Yu) and collaborators. Leaderboard contacts are named in the README.
- **What one item looks like:** an end-to-end professional workflow on an Ubuntu VM with real input files, 31 self-hosted websites (email, banking, team chat, application portals, GitLab…) and desktop apps (LibreOffice/WPS, FreeCAD…). Some tasks include a simulated user and dynamic or streaming UI.
  - *Example (Task 008, "ExpenseFlow"):* follow a tutorial PDF, extract receipt data, cross-check it against bank and email records, then file an expense reimbursement claim in a portal.
- **Number of items:** 108. Each task has on average 27.25 weighted checkpoints and needs about 318 tool calls for Opus 4.7.
- **Domain tag:** computer_use (mixed GUI, CLI and web).
- **Resembles:** finance and accounting back office (expense claims, reconciliation), document preparation (23.8% of tasks by the authors' SOC mapping), software and databases (17.8%), finance and operations analysis (16.3%), plus administrative and compliance work. Of all the benchmarks here, it is the closest to "a day's chunk of real office work". The authors map each task to a SOC major group and an O*NET-style activity (App. G.1).
- **Human times: per item, as annotator estimates, not yet public.**
  - Two annotators each timed every task. Each gave a time range (e.g. "10–30 min", "2–5 h").
  - The authors combine them per task: t_i = geometric mean of the two range midpoints.
  - Median ≈ 1.6 h of active operation. 69.6% of tasks exceed 1 h. Range runs up to 360 min. The shortest bin is <45 min; the exact minimum is not stated.
  - Times are discrete (many ties), because annotators picked from fixed ranges.
  - Per-task t_i is not in the public GitHub `BaseTask` schema. It may be in the gated task files or implementation notes; I did not authenticate to check. Otherwise, ask the maintainers.
  - **Public now:** success by bin (App. G.2, Table 21):

    | Model | [0,45) n=25 | [45,90) n=21 | [90,137) n=24 | [137,163) n=21 | [163,360] n=17 |
    |---|---|---|---|---|---|
    | Opus 4.7 (max) | 20.0 | 19.0 | 16.7 | 5.0 | 0.0 |
    | Sonnet 4.6 (max) | 12.0 | 14.3 | 8.3 | 9.5 | 0.0 |
    | GPT-5.5 (xhigh) | 24.0 | 19.0 | 16.7 | 4.8 | 0.0 |
    | MiniMax M3 | 8.0 | 9.5 | 4.2 | 0.0 | 0.0 |

- **Model results over time:** all results come from Jun–Oct 2026 releases, which is only about 4–5 months of model releases. Metrics are binary (all checkpoints pass) and partial; all at 500 steps.
  - Authors' runs (paper Table 3):

    | Model | Binary | Partial |
    |---|---|---|
    | Qwen 3.7-Plus | 2.8 | 21.5 |
    | Kimi 2.6 | 4.6 | 22.1 |
    | MiniMax M3 | 4.6 | 22.3 |
    | Sonnet 4.6 | 8.3 | 41.5 |
    | GPT-5.5 | 13.0 | 49.5 |
    | Opus 4.7 | 13.9 | 49.1 |
    | Opus 4.8 (batched tools) | 20.6 | 54.8 |

  - Snorkel independent runs: Opus 5 31.4% binary / 68.3% partial; GPT-5.6 Sol 27.3% / 62.7%.
  - Self-reported: Muse Spark 1.3 32.0 / 66.9; Claude Fable 5.1 41.7 binary / 77.9 partial (on the 08.08 release, vendor-modified tasks and grading); GPT-6 Astra 72.6 partial (offline subset).
  - The frontier labs now report this benchmark in launch posts (OpenAI GPT-5.6/6.x, Anthropic Opus 5/Fable 5.x, Google Gemini 4 Argon, Meta Muse Spark).
  - **Caveat:** three task releases exist (06.24, 08.08, v2.1). Scores across releases are not comparable.
- **Item-level results public?** Yes, in the gated trajectories dataset: per-run zips for Sonnet 4.6, Opus 4.7, GPT-5.5, GPT-5.6 Sol, GPT-6 Astra, MiniMax M3, Qwen 3.7-Plus, GLM-5V-Turbo, Muse Spark 1.2/1.3. Each zip is 3–17 GB; per-task `result.json` is written by the runner. There is also a trajectory viewer at osworld-v2-monitor.xlang.ai.
- **Grading:** execution-based checks of the final state, with weighted checkpoints. Some checkpoints use a model-based judge, which the authors validated in App. E.1. The primary metric is binary (score = 1.00); partial score is also reported. Separate safety side-effect checks run on a subset.
- **Time horizon computed already?** No fit. The authors bin success by human time (Fig. 7, Table 21) and cite Kwa et al. They conclude horizon trends "transfer only partially to general computer-use settings": agent effort (steps) scales with human time, but success does not track it on the human-easy tasks.
- **Verdict: INCLUDE.** It is the only unsaturated GUI benchmark with human time on every item and economically real tasks. It can be used now at bin level, as five bins × four models plus partial scores. **To close the per-item gap:** accept the HF gate and grep the task files for a time field, or email the maintainers listed in the README for t_i. Then join t_i to the per-task results in the trajectory zips. **Weakness:** the time span is short, and the flat-then-collapse pattern makes a logistic in log-time a poor fit.
- **Sources:** arxiv.org/abs/2606.29537; arxiv.org/html/2606.29537 (§2.2.1, §4.3, App. G.1–G.2, Table 21); github.com/xlang-ai/OSWorld-V2 (README, `desktop_env/task_base.py`, `benchmark_releases/`); HF API listings for `xlangai/osworld_v2_tasks` and `xlangai/osworld2.0-trajectory`; leaderboard.steel.dev/leaderboards/osworld-2.md; epoch.ai/benchmarks/osworld-2; snorkel.ai/blog/osworld-2-0-why-computer-use-agents-fail-most-tasks/

## 2. OSWorld (1.0) / OSWorld-Verified

- **Paper/URL:** Xie et al., "OSWorld", arXiv:2404.07972 (Apr 2024; NeurIPS 2024). OSWorld-Verified upgrade 2025-07-28. https://osworld-v1.xlang.ai/ · github.com/xlang-ai/OSWorld · per-run trajectories at HF `xlangai/ubuntu_osworld_verified_trajs` (public, not gated).
- **Maintainer:** XLANG Lab, HKU.
- **What one item looks like:** a single-goal task on an Ubuntu VM in Chrome, LibreOffice Calc/Writer/Impress, GIMP, Thunderbird, VLC, VS Code, the OS itself, or multi-app combinations.
  - *Example:* "Can you enable the 'Do Not Track' feature in Chrome to enhance my online privacy?"
  - *Calc example:* fill a column with formulas, or convert a sheet to a chart.
- **Number of items:** 369. Most Verified results use 361, excluding 8 Google Drive tasks. There are also 43 supplementary Windows tasks.
- **Domain tag:** computer_use.
- **Resembles:** desktop IT support micro-tasks (settings, file management), spreadsheet and data-entry operations, and light office work. Tasks are short (a median of about 2 minutes), so each resembles a *step* of a BPO workflow rather than a whole ticket.
- **Human times: measured per item, but only the aggregate is published.**
  - CS undergraduates with no prior exposure to the tasks attempted every task. Each was timed and graded (paper §3.4, Fig. 4).
  - Median 111.94 s. Many tasks sit at about 900 s or more.
  - Buckets: Easy <60 s (28.7% of tasks), Medium 60–180 s (40.1%), Hard >180 s (30.2%).
  - Human success by bucket: 84.9 / 81.1 / 49.6%; overall 72.36%.
  - I found no per-task time file in the repo or HF. METR did not find one either and synthesized times.
  - **Estimable:** OSWorld-Human (github.com/WukLab/osworld-human, arXiv:2506.16042, MLSys 2026) publishes per-task human ground-truth action sequences for all 369 tasks, in single-action and grouped-action form (`human-ground-truth` field in each task JSON). Multiplying these step counts by a seconds-per-step rate calibrated to the 112 s median and the bucket shares gives per-item time estimates.
- **Model results over time (OSWorld-Verified unless noted):** about 50 dated runs from 2024 to 2026.
  - Earlier models: GPT-4V 2024 (12.2% on original OSWorld) · OpenAI CUA/Operator Jan 2025 (32.6% at 50 steps) · Claude 3.7 Sonnet Feb 2025 (Agent S2 34.5%) · o3 · Claude Sonnet 4 (May 2025) · Claude Sonnet 4.5 (Sep 2025, 61.4%).
  - Later models: Claude Haiku 4.5 50.7 · Claude Opus 4.5 66.3 · Kimi K2.5 63.3 · Claude Opus 4.6 72.7 · GPT-5.4 75.0 · Claude Sonnet 4.6 78.5 · Claude Sonnet 5 81.2 · Claude Opus 4.8 83.4 · Claude Fable 5 / Mythos 5 85.0 · Qwen3.8-Max 86.1 (self-reported).
  - An agent-framework entry ("Intelligence-Indeed") claims 90.2% **[unverified]**.
  - **Saturated:** the frontier exceeds the 72% human baseline.
  - **Caveat:** step budgets (15/50/100) and harness revisions differ across rows.
- **Item-level results public?** Yes, for many runs. The HF repo `xlangai/ubuntu_osworld_verified_trajs` holds about 100 files: per-model zips (Claude 3.7/4/4.5/4.6, o3, UI-TARS, OpenCUA, Kimi K2.5/K2.6, Qwen 3.5–3.7, Holo3, a Fable 5 run, …) and an `all_result.json` mapping domain → task-id → score. I checked that file; it holds per-task 0/1 scores.
- **Grading:** execution-based checks of the final state, with one hand-written evaluator function per task. It also includes "infeasible" tasks, where saying FAIL counts as success.
- **Time horizon computed already?** Yes: METR, "How Does Time Horizon Vary Across Domains?" (2025-07-14).
  - Human times are synthetic: a lognormal with median 111.94 s / 0.7236 and σ = 1.04, chosen to match the bucket shares.
  - The slope is fixed at 0.6 ("guess").
  - Horizons in `data/horizons/osworld.csv`: o3-CUA 1.79 min, UI-TARS-1.5 1.79, Gemini 2.5 Pro 1.58, OpenAI CUA 1.39, Claude 3.7 Sonnet 1.08, GPT-4o 0.31, GPT-4V 0.11.
  - Conclusion: computer-use horizons are about 40–100× shorter than the software/reasoning cluster, with a similar doubling time.
- **Verdict: INCLUDE**, for the 2024–mid-2025 part of the trend: a long model series with public item-level results. **Gaps:** (a) per-item human times. Either request the original timing log from XLANG, or impute from OSWorld-Human step counts. (b) Saturation after late 2025: the top models solve nearly everything feasible, so H is unidentified at the top. Use OSWorld 2.0 for the frontier.
- **Sources:** arXiv 2404.07972 PDF (§3.4, Fig. 4, Table 6); osworld-v1.xlang.ai; HF API listing of `xlangai/ubuntu_osworld_verified_trajs` and its `all_result.json`; github.com/METR/cross-domain-horizon (`osworld.py`, `data/benchmarks/osworld.toml`, `data/horizons/osworld.csv`); metr.org/blog/2025-07-14-how-does-time-horizon-vary-across-domains; arxiv.org/html/2506.16042v1; github.com/WukLab/osworld-human; leaderboard.steel.dev/leaderboards/osworld.md

## 3. UI-CUBE (UiPath)

- **Paper/URL:** "UI-CUBE: Enterprise-Grade Computer Use Agent Benchmarking Beyond Task Accuracy to Operational Reliability", arXiv:2511.17131 (21 Nov 2025). github.com/UiPath/uipath_enterprise_benchmark · uipath.com/ai/research/ui-cube-benchmark
- **Maintainer:** UiPath (Cristescu et al.).
- **What one item looks like:**
  - Tier 1 (136 tasks): single UI-control tasks, such as a combo box, date or time picker, input box, list or table navigation, or a kanban board.
  - Tier 2 (90 tasks): 50 copy-paste / business-process tasks (e.g. moving records between apps) and 40 scenarios in replicas of **Salesforce (CRM), SAP (stock/ERP), Concur (expense) and Workday (HR)**.
  - Every task is checked by a programmatic state-diff `test()`. Each runs at XGA, 1080p and 4K.
  - *Example:* in the Concur-like app, enter an expense report from given data.
- **Number of items:** 226.
- **Domain tag:** computer_use.
- **Resembles:** squarely the RPA/BPO target — data entry and transfer between enterprise systems, expense processing, ERP stock updates, HR record changes.
- **Human times: average duration per collection, not per item.** Human evaluators new to the apps completed every task, with times recorded through `DeterministicBenchmark/src/HumanEval.tsx` in the repo.

  | Collection | Avg. human time | Human accuracy |
  |---|---|---|
  | Simple tasks (various widgets) | 2.9–20.6 s (mean 10.7 s) | 97.9% |
  | Business process | 267 s | 50% |
  | Copy-paste | 178 s | 53% |
  | Salesforce | 123 s | 62.5% |
  | Concur | 130 s | 50% |
  | SAP | 183 s | 50% |
  | Workday | 43 s | 62.5% |
  | Complex tasks overall | mean 149 s | 61.2% |

  The paper also gives average human steps per collection. Range of category means: 3 s to 4.5 min.
- **Model results over time:** five configurations, all from 2025 (simple / complex success):

  | Configuration | Simple | Complex |
  |---|---|---|
  | Claude Computer Use 4.0 | 66.7% | 9.5% |
  | OpenAI computer-use-preview | 70.3% | 10.5% |
  | UiPath ScreenAgent + Gemini 2.5 Flash | 68.6% | 11.9% |
  | UiPath ScreenAgent + GPT-5 mini | 77.0% | 18.4% |
  | UiPath ScreenAgent + GPT-5 | 84.8% | 19.4% |

  I found no 2026 updates.
- **Item-level results public?** Not found: no results files in the repo. The harness is public, so tasks can be re-run.
- **Grading:** programmatic postcondition and state-diff validation.
- **Time horizon computed already?** No.
- **Verdict: CANDIDATE.** It has the best fit to IT/BPO and real human timing infrastructure. **Gaps:** per-item human times (UiPath has them from HumanEval runs, so request them, or time the tasks yourself — they are short); only one generation of models; human accuracy on complex tasks is only 61%. **To close:** ask UiPath for per-task human logs and per-task model results, or re-run 3–4 current models with the open harness.
- **Sources:** arxiv.org/html/2511.17131v1 (§6.1 Tables 5–6, §6.2 Tables 7–8); repo tree github.com/UiPath/uipath_enterprise_benchmark

## 4. SCUBA (Salesforce Computer Use Benchmark)

- **Paper/URL:** arXiv:2509.26506 (Sep 2025; ICLR 2026). https://sfrcua.github.io/SCUBA/ · github.com/SalesforceAIResearch/SCUBA
- **Maintainer:** Salesforce AI Research.
- **What one item looks like:** a CRM task in a real Salesforce developer-org sandbox, for one of three personas: platform admin, sales rep, or service agent.
  - *Example (admin_001_001):* "Create a report with Leads type with name MyLeadRPT … add a standard filter to select records whose Lead Status equals Open – Not Contacted."
- **Number of items:** 300 instances from 60 templates.
- **Domain tag:** computer_use (it can also be run by browser-use/DOM agents).
- **Resembles:** CRM administration, sales operations, customer-service back office (case handling, record updates, report and dashboard building) — common Indian IT/BPO Salesforce-support work.
- **Human times: none published. Estimable.**
  - All 300 instances were completed by a trained internal annotation team using a primitive-action tool, giving human trajectories. The 50-step budget was "justified by the average steps used from the human annotation".
  - Human demonstration plans are public in `data/test_demo_aug.json` (I checked it: 300 entries).
  - Per-task human step counts would need the annotation trajectories (not public as far as I can tell). These could be converted to time.
- **Model results over time:** nine agents (2025), zero-shot. Computer-use agents: Claude 4 Sonnet ≈ 27%, OpenAI CUA ≈ 16%, open-source CUAs < 5%. Browser-use agents: GPT-5 / o3 / Gemini 2.5 Pro / Claude 4 Sonnet; the best is about 39–51% depending on paper version.
  - Per-agent wall-clock time is reported (e.g. about 19 min per task for GPT-5 browser-use) **[from aggregator summaries; not checked in the paper table]**.
  - The project-site leaderboard did not render for me.
- **Item-level results public?** Only sample outputs in the repo.
- **Grading:** rule-based evaluator of the org's final state, plus milestone (process) rubric scores.
- **Time horizon computed already?** No.
- **Verdict: CANDIDATE.** Real enterprise SaaS and high BPO relevance. **Gaps:** human times (ask Salesforce for the annotation trajectories with timestamps or step counts) and models over time (only 2025 models).
- **Sources:** arxiv.org/html/2509.26506 (§3.2.2 Phase 4, App. E, §4.2); salesforce.com/blog/scuba-benchmark/; repo tree and `data/test_demo_aug.json`

## 5. HealthAdminBench (Stanford)

- **Paper/URL:** arXiv:2604.09937 (Apr 2026; ICLR 2026, NeurIPS 2026 listings). healthadminbench.stanford.edu (redirects to som-shahlab.github.io/health-admin-bench-website/) · github.com/som-shahlab/health-admin-bench
- **Maintainer:** Stanford (Shah lab, SOM).
- **What one item looks like:** a computer-use agent works across four simulated GUIs — an Epic-like EHR, two payer portals (Anthem- and Availity-like), and a RightFax-like fax system — to complete **prior authorization, appeals/denials, or DME order processing**.
  - *Example:* pull the clinical documents for a worklist patient, submit a prior-auth request on the right payer portal, and record the result in the EHR.
- **Number of items:** 135 tasks, 1,698 subtask checkpoints, three difficulty levels.
- **Domain tag:** computer_use (web-app GUIs operated by screenshot CUAs).
- **Resembles:** medical-records and revenue-cycle BPO — claims, prior auth, denials management. This is a core Indian healthcare-BPO line.
- **Human times: none.** Environments were designed from more than 100 h of observing real staff. Two revenue-cycle experts reviewed the tasks but were not timed. **Estimable** from subtask counts per task (≈ 12.6 on average) times per-subtask time, or by timing a sample.
- **Model results:** seven configurations on five models (2026): Claude Opus 4.6, GPT-5.4, Gemini 3.1 Pro, Kimi K2.5, Qwen-3.5-27B.
  - Best task success: Opus 4.6 CUA, 36.3%.
  - Best subtask success: GPT-5.4 CUA, 82.8%.
  - The leaderboard shows Score / Subtask score / Avg. steps / Avg. time per model (values did not load for me).
- **Item-level results public?** The authors say they release "model outputs"; I did not locate the files.
- **Grading:** 1,177 checkpoints are deterministic JMESPath checks on portal state; 521 are judged by GPT-5.4 against rubrics.
- **Time horizon computed already?** No.
- **Verdict: CANDIDATE.** Closest match to healthcare-BPO work. **Gaps:** no human times; one time point. **To close:** time a stratified sample, or use subtask counts as a length proxy. Note the overlap with the web-agent researcher's area.
- **Sources:** arxiv.org/html/2604.09937; Stanford site; repo link from the paper

## 6. ERPBench (Accenture)

- **Paper/URL:** "ERPBench: A State-Grounded Evaluation Paradigm for Computer-Use Agents in Enterprise Software", arXiv:2609.17885 (v2 23 Sep 2026). There is a separate, unrelated "ERPBench" at arXiv:2609.04667 (decision-making).
- **Maintainer:** Accenture Agentic AI CoE.
- **What one item looks like:** screenshot-only work in a live ERPNext instance.
  - T1 (20 tasks): edit one field or create a simple record (e.g. set a customer's tax ID).
  - T2: create a full 6–9-field Customer or Supplier record.
  - T3: chain 2–4 linked documents (Lead → Opportunity → status, or Project → Task → Timesheet), sometimes ending with an irreversible "submit".
- **Number of items:** about 30 (T1 20; T1+T2 = 24; plus T3). Each was run five times.
- **Domain tag:** computer_use.
- **Resembles:** ERP data entry and master-data maintenance — finance and accounting / procurement back office.
- **Human times: tier means from three annotators** (two expert ERPNext users and one first-time user):
  - T1: about 41–89 s
  - T2: about 86–150 s
  - T3: about 100–396 s
  - Per-run durations clearly exist internally.
- **Model results:**
  - Claude Sonnet 4.6: 94 / 100 / 100% on T1 / T2 / T3. This is near saturation for the frontier.
  - Open models: Holo3-35B, Qwen3-VL-32B, OpenCUA-32B/7B, UI-TARS-1.5-7B, all at 0–34%.
- **Item-level results public?** No.
- **Grading:** database field values compared with ground truth (field-weighted partial credit; chain depth for T3).
- **Time horizon computed already?** No.
- **Verdict: EXCLUDE** for horizon fitting. It is too small, has a single frontier model, and that model is saturated. It is still a useful qualitative datapoint: ERP form entry of 1–7 minutes is essentially solved by frontier CUAs in 2026.
- **Sources:** arxiv.org/html/2609.17885 (§3.1, §3.4, Table 2)

## 7. Windows Agent Arena (WAA)

- **Paper/URL:** Bonatti et al., arXiv:2409.08264 (Sep 2024; ICML 2025). github.com/microsoft/WindowsAgentArena
- **Maintainer:** Microsoft (with CMU and Columbia co-authors).
- **What one item looks like:** an OSWorld-style task on a Windows 11 VM: Edge/Chrome, File Explorer, Settings, LibreOffice, VS Code, VLC, Notepad/Clock/Paint.
  - *Example:* "open the autosave feature of VS Code and delay AutoSave operations for 500 milliseconds".
- **Number of items:** 154.
- **Domain tag:** computer_use.
- **Resembles:** Windows desktop IT support and office micro-tasks.
- **Human times: aggregate only.**
  - One "casual Windows user" did all 154 tasks in about 1.5 h over five sittings, i.e. roughly 35 s per task on average. Human success 74.5%.
  - Per-task human step counts and difficulty ratings were recorded (App. A.5) but are not in the repo. Task JSONs have no step or difficulty field (I checked).
- **Model results over time:** Navi + GPT-4V 19.5% (2024). Later agent frameworks are self-reported: UI-TARS-2 about 50%; Agent S3 about 56%; VLAA-GUI (Gemini 3 Flash) 60–61%, Apr 2026 **[aggregator figures, unverified]**. Frontier labs rarely report WAA.
- **Item-level results public?** Not systematically.
- **Grading:** execution-based evaluators (OSWorld-derived).
- **Time horizon computed already?** No.
- **Verdict: EXCLUDE** (low priority). Times are aggregate only, it was benchmarked by one person, results are sparse, and the tasks largely duplicate OSWorld.
- **Sources:** arxiv.org/html/2409.08264 (§3.2, App. A.5); repo tree and a sample task JSON

## 8. macOSWorld

- **Paper/URL:** arXiv:2506.04135 (Jun 2025; NeurIPS 2025). github.com/showlab/macosworld
- **Maintainer:** Show Lab, NUS.
- **What one item looks like:** a task on a macOS VM (System Settings, Finder, Pages/Numbers/Keynote, media apps, multi-app), offered in five languages. There is also a safety subset with deceptive pop-ups.
- **Number of items:** 202 English tasks, of which 183 also exist in other languages.
- **Domain tag:** computer_use.
- **Resembles:** desktop IT support and office tasks on Mac. Low relevance to Indian BPO, which is Windows- and web-heavy.
- **Human times: per item, but only plotted.** Annotators re-performed every task a month after writing it. Total time versus steps per task is plotted in Fig. 3c, and the per-step time histogram (ex-Gaussian) in Fig. 3d. All tasks take 20 human steps or fewer. No data file is in the repo.
- **Model results:** 2025 only. OpenAI CUA and Claude CUA above 30%; Gemini 2.5 Pro 18.5%; GPT-4o, UI-TARS-7B and ShowUI below 10%. There is no sustained series.
- **Item-level results public?** Not found.
- **Grading:** scripted checks of the final state.
- **Time horizon computed already?** No.
- **Verdict: CANDIDATE (low priority).** It has per-item human times; ask the authors for the Fig. 3c data. **Gap:** almost no model series. Only worth it if someone re-runs current models.
- **Sources:** arxiv.org/html/2506.04135 (§4.2, §5.2); repo tree

## 9. AndroidWorld

- **Paper/URL:** Rawles et al., arXiv:2405.14573 (May 2024; ICLR 2025). github.com/google-research/android_world · community leaderboard (Google Sheet linked from the README).
- **Maintainer:** Google DeepMind / Google Research.
- **What one item looks like:** a parameterized task in 20 Android apps on an emulator, with randomized parameters.
  - *Example:* "Create a timer with {h} hours, {m} minutes … Do not start the timer"; also adding contacts, recording expenses, or editing notes in Markor.
- **Number of items:** 116 templates.
- **Domain tag:** computer_use (mobile).
- **Resembles:** consumer phone use. A weak match for IT/BPO, apart from expense entry.
- **Human times: per item, as step counts. Public.**
  - `android_world/task_metadata.json` gives each task's `difficulty` (61 easy, 36 medium, 19 hard) and `optimal_steps` as estimated by human annotators.
  - Step budgets were reset in Nov 2024 to about twice "the human average completion time" (per-task table in a linked sheet; I downloaded it).
  - Two software engineers attempted every task once (80% success); per-task wall time is not published.
  - **Estimable:** steps × seconds-per-step.
- **Model results over time:** a long series from 2024 to 2026: M3A/GPT-4 Turbo 30.6% (2024) → many agent frameworks → 100% (several entries, Aug–Oct 2026, e.g. GPT-6 Astra-based MobileRun). About 70 leaderboard rows with dates. **Saturated.**
- **Item-level results public?** Partly: many leaderboard rows link trajectory files.
- **Grading:** programmatic checks of app state.
- **Time horizon computed already?** Not that I found. METR's cross-domain post did not include it.
- **Verdict: EXCLUDE** for this project. The tasks are consumer mobile, it is saturated, and the frontier entries are mostly self-reported agent scaffolds rather than base models. It could serve as a secondary 2024–25 trend check, because per-task step counts are public.
- **Sources:** arxiv.org/pdf/2405.14573 (Fig. 2, App. D.4); repo README and `task_metadata.json`; Google Sheets exports of the leaderboard and step-budget table

## 10. MobileWorld (Tongyi)

- **Paper/URL:** arXiv:2512.19432 (Dec 2025). tongyi-mai.github.io/MobileWorld/
- **Maintainer:** Alibaba Tongyi.
- **What one item looks like:** an Android task. 62% need several apps; some need clarifying questions to a simulated user; some use MCP tools.
- **Number of items:** 201: 117 GUI-only, 44 user-interaction, 40 MCP.
- **Domain tag:** computer_use (mobile).
- **Resembles:** consumer and personal-assistant phone work. Low BPO relevance.
- **Human times:** none found. The average of 27.8 steps per task (versus 14.3 for AndroidWorld) suggests step counts per task exist.
- **Model results:** best about 51.7% (GPT-5 + UI-Ins-7B), per search summary **[unverified]**.
- **Grading:** programmatic.
- **Time horizon computed already?** No.
- **Verdict: EXCLUDE** (low BPO relevance, no human times).
- **Sources:** search results and the project page (not read in full)

## 11. Long-horizon 2026 desktop benchmarks without human times

These are grouped because they share the same gap. All are 2026, unsaturated, and frontier-relevant.

- **OpenComputer** (arXiv:2605.19769, Yale/Cohan lab, May 2026)
  - 1,000 tasks across 33 desktop apps, each with an app-state verifier.
  - GPT-5.4 about 68% **[aggregator]**.
  - No human times (I checked the paper text).
- **WeaveBench** (arXiv:2606.09426, Microsoft-affiliated, Jun 2026)
  - 114 tasks in 8 work domains, mixing GUI and CLI actions; median 76 tool calls.
  - Best PassRate 41.2%. A trajectory-aware judge cuts GPT-5.5 from 53.5% to 33.3%.
  - No human times.
- **MyPCBench** (arXiv:2606.16748, CMU, Jun 2026)
  - 184 personal-assistant tasks over 17 simulated web apps, all seeded for one persona.
  - Opus 4.8 62% (per Yutori).
  - No human times; graded by an LLM judge.
- **ChainWorld** (Scale Labs, arXiv:2606.21654, Jun 2026)
  - 347 chains, each 2–4 OSWorld tasks long.
  - Best chain completion 31%.
  - **Could inherit OSWorld per-task human times by summing them**, which makes it a natural longer-horizon extension once OSWorld per-item times are obtained.
- **DeskCraft** (arXiv:2606.03103) and **OSExpert-Eval** (arXiv:2603.07978): professional desktop workflows. No human times in the text.
- **Verdict:** EXCLUDE for now; ChainWorld is a CANDIDATE if OSWorld per-item times are obtained.
- **Sources:** arXiv HTML for each, grepped for human timing; yutori.com/leaderboards/mypcbench.md; labs.scale.com/papers/chainworld

## 12. OSUniverse and VideoGUI

- **OSUniverse** (arXiv:2505.03570, Kentauros AI, May 2025)
  - GUI tasks in tiers from Paper to Gold, validated by a Gemini judge.
  - No human times; few models.
  - **EXCLUDE.**
- **VideoGUI** (arXiv:2406.10227, Show Lab, NeurIPS 2024 D&B)
  - 86 full tasks and 463 subtasks in Photoshop, Premiere, After Effects, PowerPoint, etc., built from instructional videos.
  - Has human *recording time per subtask* (mean 55 s).
  - But evaluation is mostly offline (planning and action prediction), GPT-4o completes no full task, and there is no model series. The work is creative software, not BPO.
  - **EXCLUDE.**
- **Sources:** arxiv.org/html/2505.03570; arxiv.org/html/2406.10227 (App., Fig. 11)

---

## Cross-cutting notes for the time-horizon pipeline

- **How to get per-item OSWorld times, in order of preference:**
  1. Ask XLANG for the original human-evaluation timing log behind Fig. 4 of the paper.
  2. Impute from OSWorld-Human step counts. Fit seconds per step so that the imputed distribution matches the 112 s median and the 28.7/40.1/30.2% bucket shares. Divide by 0.7236, as METR did, only if a success adjustment is wanted.
- **OSWorld 2.0 times are annotator estimates (ranges), not stopwatch logs.** They behave more like METR "estimated" lengths than "baseline" lengths. Because of the ties, a per-item fit will look like a five-to-eight-bin fit anyway.
- **Saturation:** OSWorld-Verified, AndroidWorld and ERPBench T1–T3 are at or above human level for 2026 frontier models. Fit H only on models whose success is clearly below ceiling.
- **Scaffold versus model:** GUI leaderboards mix base models with agent frameworks (e.g. GPT-5 + grounding model). For a model-release-date trend, keep base-model or vendor-harness rows only.

## Things in other researchers' areas (one line each, not researched)

- **Agents' Last Exam** (Sun et al. 2026): 1K+ expert professional tasks, a small GUI share → occupational suites.
- **Odysseys** (Jang et al. 2026): long-horizon multi-site web → browser/web.
- **CRMArena-Pro, WorkArena/WorkArena++, REAL**: cited as enterprise CUA comparators → web / customer service.
- **Argo-Bench** (arXiv:2610.02122): data agents on an ERP warehouse → back office / finance.
- **"How Benchmarks Mis-Score Computer-Use Agents"** (arXiv:2607.28367): an audit of CUA evaluator reliability → time-horizon infrastructure.

## Leads I didn't chase

- The gated HF `xlangai/osworld_v2_tasks` files and implementation notes may contain the per-task human-time ranges. This needs an HF login and accepting the gate (auto-approved).
- OSWorld 2.0 v2.1 release notes and the Snorkel independent leaderboard (snorkel.ai/leaderboard/os-world-2-0/), for more independent per-model runs.
- WindowsAgentArena-V2 and OSWorld-MCP (2025 variants).
- MedCUA-Bench (clinical software rebuilt from manuals): possible EHR GUI benchmark; not opened.
- Desktop-Delta Bench (arXiv:2607.26041) and GUI-360: mostly transition and grounding; likely excluded.
- AndroidLab, SPA-Bench, AndroidDaily (mobile): low BPO relevance.
- A SAP-GUI-specific benchmark: none found in two searches. UI-CUBE's SAP-like app is the closest.
- UiPath Screen Agent results on UI-CUBE with 2026 models (UiPath blog), if any.
