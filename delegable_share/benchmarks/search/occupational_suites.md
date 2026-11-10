# Occupational / "economically valuable work" benchmark suites

Search date: 2026-11-09. Scope: suites built around paid occupational work (GDPval, RLI, TheAgentCompany, Mercor APEX, Upwork, office suites, O*NET-keyed suites). Everything below was checked on the web unless marked **[unverified]**. Many leaderboard numbers come from vendor pages that change often, so treat scores as snapshots.

## Summary table

| Benchmark | Items | Per-item human time? | Models over time? | Item-level results public? | Verdict |
|---|---|---|---|---|---|
| OmegaUse-OfficeVal (Baidu) | 100 | **Yes, measured and public** (5–501 min, median 122) | No (one snapshot, 5 open-weight models) | Tasks, rubrics and verifiers public; we can rerun | **CANDIDATE (high)**: run frontier models ourselves |
| APEX-Agents (Mercor) | 480 (v1), 240 (v1.1) | **Yes, expert estimates** in task metadata (mean 1.82 h); a baselining study found they run about 33% high | Yes (Jan–Nov 2026, many models) | Tasks public (gated, auto-approve); per-model item results not public except Qwen traces | **INCLUDE** (with caveats) |
| GDPval (OpenAI) | 1,320 (220 public gold) | Yes, but **private**; only aggregates published (gold median 5 h) | Yes (Sep 2025 → GPT-5.5, Apr 2026) | No | **CANDIDATE (high)**: request per-task times, or estimate them |
| GDPval-AA (Artificial Analysis) | 220 gold | No (the GDPval times are private) | Yes, more than 300 models with release dates | No | CANDIDATE (pairs with GDPval times) |
| Remote Labor Index (Scale/CAIS) | 240 (230 private) | Yes (self-reported, mean 28.9 h, median 11.5 h), private | Yes (Oct 2025 → Fable 5.2 at 41.3%) | No | CANDIDATE (low for IT/BPO); **CAIS says its time-horizon fit fails** |
| TheAgentCompany (CMU) | 175 | None (authors say 10 min to several hours) | Yes (Dec 2024–Nov 2025) | **Yes, per-task for about 19 agent runs on GitHub** | **CANDIDATE (high)**: human times need estimating |
| JobBench | 128 public (65 main + 63 easy) | None | One snapshot of 36 agent configs | Tasks public | CANDIDATE: per-item O*NET task mapping |
| APEX-Accounting (Mercor + Ramp) | 160 private + 10 dev | Not found | One snapshot of about 10 models (Jul 2026) | No | CANDIDATE (pass to back-office researcher) |
| $OneMillion-Bench | 400 | Per-task **dollar value** = senior-expert hours × wage (public table) | One snapshot of 35 models | Unclear | CANDIDATE (low): text Q&A |
| UpBench (Upwork) | 322 | None; has per-job **payouts** | 3 models (2025) | Not public | EXCLUDE for now (data not released) |
| Agents' Last Exam (Berkeley) | 1,490 (152 public) | None found | One snapshot of many harnesses | Partly | EXCLUDE for now |
| xbench-Profession, OfficeBench, WorkBench, PRBench, Vals Index | – | None | – | – | EXCLUDE |

---

## 1. OmegaUse-OfficeVal

- **Name / URL / date / maintainer:** OmegaUse-OfficeVal: Benchmarking LLM Agents on Long-Horizon Office-Suite Tasks with Economic Grounding. arXiv 2607.27155 (Jul 2026). https://omegause-officeval.github.io ; data at https://huggingface.co/datasets/baidu-frontier-research/OmegaUse-OfficeVal ; code at https://github.com/baidu-frontier-research/OmegaUse-OfficeVal . Maintained by Baidu (Agent Frontier Team).
- **Item:** An office-suite request proposed by a practitioner and adapted for privacy, with 1–N input files (Word, Excel, PPT, PDF). The agent must produce a deliverable. Example kinds of task: restructure a report, reformat a spreadsheet, extract data into a table, annotate a document. Operation intents: Reformat 29, Restructure 14, Extract 6, Beautify 4, Annotate 3, Compute 1, Other 43. Domains: Education 25, Business Ops 20, Academic 14, Engineering 10, Admin 9, Financial Data 4, Other 18. 100 items, 220 input files, about 20 rubric items per task.
- **Domain tag:** computer_use / mixed (office documents)
- **Resembles:** junior office or back-office work: document processing, data entry/extraction, report formatting, admin support. This is the **closest match among these suites to Indian BPO back-office and data-entry work**. No O*NET mapping.
- **Human times: per-item, measured** (the best in this survey). 20 screened annotators; at least 2 per task, and a 3rd if the two times differ by more than 30%. A senior expert gates quality (revision time counts), and there are speed incentives. The task time is the mean of the two shortest valid times. Public field `human_labor_time` (minutes): **min 5, median 122, mean 139, max 501** (from HF dataset statistics). Each task also has a `task_price_proxy` (USD; 20% explicit outsourcing prices, 80% expert estimates; median $35).
- **Model results:** One snapshot (paper, Jul 2026). GLM-5.2 17.9, Qwen3.7-Plus 17.5, Kimi K2.6 17.0, DeepSeek-V4-Pro 14.5, MiniMax M3 13.8. Best human 27.8. Scores are 0–100 rubric/verifier scores, and the human ceiling is low because the scoring penalises collateral damage. No US frontier models, and no time series.
- **Item-level public?** Tasks, rubrics and verifier code are public. I did not find per-model per-task scores, but the paper has heatmaps by time bucket ("time-score-heatmap.png" on the project page).
- **Grading:** Code verifiers generated from expert-revised rubrics; human–code discrepancies were resolved by hand. Continuous score. Acceptance would need a threshold (e.g. full pass, or score ≥ that task's human score).
- **Time horizon computed?** No. The paper reports time-weighted scores only.
- **Verdict: CANDIDATE (high priority).** Gap: no models over time. Fix: it is fully open and cheap ($0.2–1.8 per task in the paper), so run about 6–10 models with spread-out release dates (e.g. GPT-4o, o3, GPT-5, GPT-5.5, Claude 3.7/4.5/Opus 4.8, Gemini 2.5/3) and fit H and β directly. Define success as a binary threshold on the verifier score.
- **Sources:** https://arxiv.org/html/2607.27155 ; https://omegause-officeval.github.io ; HF datasets-server info/statistics for baidu-frontier-research/OmegaUse-OfficeVal

## 2. APEX-Agents (Mercor)

- **Name / URL / date / maintainer:** APEX-Agents, arXiv 2601.14242 (v1 20 Jan 2026, v3 23 Feb 2026). v1.1 released 8 Sep 2026 (https://mercor.com/blog/introducing-apex-agents-1-1/). Leaderboard at https://www.mercor.com/apex/apex-agents-leaderboard/ . Data: HF `mercor/apex-agents` (480 tasks, CC-BY-4.0, gated with auto-approve) and `mercor/apex-agents-v1.1` (Harbor tasks). Infrastructure: "Archipelago". Maintained by Mercor (Vidgen et al.).
- **Item:** A long-horizon, cross-application task inside a simulated "world" (files, mail, chat, spreadsheets, presentations, PDFs, plus EDGAR and market data in some worlds; no web). The agent returns a message or a file. Examples from the gold-file names: update an LBO model, build comps and precedents, prepare an accretion/dilution model, draft an estoppel certificate, identify class members in a spreadsheet. v1 has 480 tasks across 33 worlds (160 each in investment banking, management consulting and corporate law). v1.1 has 240 tasks (80 per domain), re-audited.
- **Domain tag:** mixed (knowledge work with tools and files)
- **Resembles:** high-end analyst and associate work (IB analyst, consultant, corporate lawyer). It is close to KPO/finance analytics in Indian IT-BPM, but not core IT/BPO. **O*NET:** the survey that shaped it covered financial and investment analysts (13-2051), management consultants (13-1111) and lawyers (23-1011).
- **Human times: per-item expert estimates.** Experts tagged each task with the "expected time for an industry professional to complete the task" (paper §3.3). Average estimated hours by domain: IB 1.36; Law 2.40; consulting (not captured cleanly in my extract); overall **1.82 h**. **Baselining study:** on 96 tasks (20%), independent experts actually did the work. Estimated 1.70 h vs. actual 1.37 h, so the estimates run **about 33% high**. That gives a usable calibration factor. I could not open the gated file, so I have **not verified** the exact metadata field name or the per-item spread. The range looks narrow (roughly 1–3 h), which limits how well β can be identified.
- **Model results over time:** v1 (Jan 2026) tested 8 agents; Pass@1 leaders were Gemini 3 Flash 24.0%, GPT-5.2, Opus 4.5, Gemini 3 Pro. Epoch (Feb 2026) reports Opus 4.6 at about 30%. v1.1 (Sep 2026): Claude Fable 5.1 68.6% Pass@1; GPT-6 Astra had the best Pass^4 (56.3%). Current leaderboard (Nov 2026, metric probably mean score): Gemini 4 Carbon 84.2%, Gemini 4 Argon 82.4%, Fable 5.2 80.1%, Hy4 77.6%, Sonnet 5.5 75.5%. Per-domain top-3 figures are shown. Third-party mirror: https://benchlm.ai/benchmarks/mercorapexagents11 . Release dates of the models are mostly public.
- **Item-level public?** Tasks, rubrics, gold outputs and metadata are public for v1 (gated). Per-model per-task results are **not** public, except `mercor/ApexAgentsRecipe-ApexAgents480-EvalTraces` (Qwen3.5/3.6 traces, gated). That card says use is "exclusively for model evaluation" and forbids "training, fine-tuning, or parameter fitting". **Check the licence before fitting curves on Mercor traces**; our own runs avoid the issue.
- **Grading:** Binary rubric criteria (several per task) graded by an LLM judge, validated against human labels (confusion matrix in paper Table 2). Pass@1 means all criteria met. v1.1 zeroes "scattergun" answers.
- **Time horizon computed?** None found.
- **Verdict: INCLUDE.** It is the only suite here with per-item expert times plus a public task set plus a multi-model time series plus binary pass/fail. Gaps: (a) per-model item results. Fix by re-running a few models via Archipelago/Harbor, or by asking Mercor (apex@mercor.com). Fallback: METR-style fit from aggregate Pass@1 with an assumed β. (b) Narrow time range. (c) Versions 1.0 and 1.1 are not comparable, so pick one.
- **Sources:** https://arxiv.org/abs/2601.14242 ; https://arxiv.org/html/2601.14242 ; https://mercor.com/blog/introducing-apex-agents-1-1/ ; https://www.mercor.com/apex/apex-agents-leaderboard/ ; HF API `mercor/*` listings ; https://epoch.ai/blog/what-do-economic-value-benchmarks-tell-us

## 3. GDPval (OpenAI)

- **Name / URL / date / maintainer:** GDPval: Evaluating AI Model Performance on Real-World Economically Valuable Tasks. arXiv 2510.04374 (Oct 2025; the benchmark was announced Sep 2025; ICLR 2026). Data: https://huggingface.co/datasets/openai/gdpval (220-task gold set; last modified 2026-02-10, when rubric fields were added). Automated grader at evals.openai.com. Maintained by OpenAI.
- **Item:** A realistic work request from an industry professional (average 14 years' experience), with reference files. The deliverable is usually an Office-style file (doc, slides, spreadsheet, PDF, sometimes CAD/video). Examples from the gold deliverables: "Receiving Parts Order Procedures", "Black Friday 8 Week Plan", "DMAIC – Analyze Tollgate" deck, "Bulk Form – Canyon Pathology" spreadsheet. 1,320 tasks (30 per occupation); 220 public gold tasks (5 per occupation).
- **Domain tag:** mixed
- **Resembles / O*NET: explicitly O*NET-keyed.** Occupations were chosen as the top 5 by wages in each of the 9 sectors that each make up more than 5% of US GDP, keeping only occupations that are "predominantly digital" (at least 60% of O*NET tasks, weighted by importance, labelled digital). The gold set covers 208 unique O*NET tasks. The 44 occupations include several relevant to us: **Software Developers; Accountants & Auditors; Customer Service Representatives; Medical Secretaries & Admin Assistants; Computer & Info Systems Managers; Order Clerks; Shipping/Receiving/Inventory Clerks; First-Line Supervisors of Office/Admin Support; Financial & Investment Analysts; Compliance Officers; Project Management Specialists.** The full list is in the paper's Table 1.
- **Human times: exist per item, but private.** Times were self-reported by the task writer ("how long it would take in the real world") and validated by occupational reviewers. Gold set: mean 9.49 h, **median 5.0 h**, IQR 2.38–10 h, min 0.5, max 100 (paper Table 3; another passage gives mean 404 min). Full set: median 4.0 h, max 605 h. Cost = hours × BLS OEWS median wage. **The public HF schema has no time or cost field** (verified via the HF API: task_id, sector, occupation, prompt, files, rubric_pretty, rubric_json).
- **Model results over time:** Paper (strict win rate vs. expert): GPT-4o 12.5%, o4-mini 29.1%, o3 35.2%, GPT-5 39.0%. Claude Opus 4.1 had 47.6% wins or ties; Gemini 2.5 Pro and Grok 4 are in Fig. 5. Later, vendor-reported "wins or ties": GPT-5.2 70.9% (Dec 2025), GPT-5.2 Pro 74%, GPT-5.4 83.0% (5 Mar 2026), GPT-5.5 84.9% (Apr 2026), GPT-5.5 Pro 82.3%, Claude Opus 4.7 80.3%, Gemini 3.1 Pro 67.3% (OpenAI GPT-5.5 launch table). The benchmark is near saturation on win-or-tie.
- **Item-level public?** No. The paper shows win rate by occupation and a **win-rate-vs-task-length plot (Fig. 13): highest win rates for 0–2 h tasks, declining steadily as length grows.** That is evidence that human time does predict difficulty here, unlike RLI.
- **Grading:** Blinded pairwise comparison by occupational experts: model deliverable vs. human deliverable, scored better/tie/worse. 3 samples × 3 graders per task; each comparison took over an hour. Human inter-rater agreement 71%; the GPT-5-based autograder agrees 66% with humans.
- **Time horizon computed?** Not officially. A LessWrong post ("bira", 30 Sep 2025) fit only a logit-of-win-rate vs. release-date trend (3 points). An unofficial LessWrong post estimating METR horizons for Opus 4.6/GPT-5.3 used GDPval-AA as an input.
- **Verdict: CANDIDATE (high).** It has the best O*NET mapping and covers several IT/BPO occupations, but per-task times and per-task outcomes are private. Ways to close the gap: (1) ask OpenAI for per-task times and per-task win/tie outcomes for the gold set (and, ideally, the full set); (2) otherwise estimate gold-set times with an LLM or expert panel from prompt + deliverable, calibrated to the published quantiles (0.5 / 2.38 / 5 / 10 / 100 h), and pair them with GDPval-AA or our own runs; (3) digitise Fig. 13 to get bucketed success by length for the paper's models. Treat "win or tie" as the acceptance outcome.
- **Sources:** https://arxiv.org/html/2510.04374v1 ; https://huggingface.co/datasets/openai/gdpval (and the HF API/datasets-server) ; https://openai.com/index/introducing-gpt-5-5/ ; https://openai.com/index/introducing-gpt-5-4 ; https://epoch.ai/blog/what-do-economic-value-benchmarks-tell-us ; https://www.lesswrong.com/posts/P43ck9FX3ztLNv5xv/gdpval-models-could-automate-the-u-s-economy-by-2027 ; https://www.testmuai.com/learning-hub/gdpval/ (confirms that times are not in the public set)

## 4. GDPval-AA (Artificial Analysis)

- **URL / date / maintainer:** https://artificialanalysis.ai/evaluations/gdpval-aa . v1 was part of Intelligence Index v4 (early 2026). v2 launched 15 Jun 2026, replacing the single judge with a rotating panel of 3 judges [secondary source]. v2.1 is current. Maintained by Artificial Analysis.
- **Item:** The 220 GDPval gold tasks, run in the agentic "Stirrup" harness with shell and web access.
- **Human times:** none (they inherit GDPval's private times).
- **Model results over time:** More than 300 models, each with a release date, and an "Elo vs release date" chart. Top (Nov 2026): Claude Opus 5.5 (max) 1866, Kimi K3.1 Pro 1858, Muse Wonder 1857, Sonnet 5.5 1838. Elo is anchored at DeepSeek V4.1 Flash = 1600. Scores drift between versions.
- **Item-level public?** Per-task deliverables can be browsed; judgments and per-task scores are not published.
- **Grading:** LLM judge(s) compare pairs of model outputs, aggregated to Elo. There is **no direct comparison to the human deliverable in v2.1**, so it does not give an acceptance probability.
- **Time horizon computed?** No.
- **Verdict: CANDIDATE.** Its value is the long model time series on GDPval items. To be usable, it needs GDPval per-task times and per-task outcomes against the human reference, which we would have to run ourselves (Stirrup is open, per AA).
- **Sources:** https://artificialanalysis.ai/evaluations/gdpval-aa ; https://capitalandcompute.net/ai-benchmarks/gdpval/ ; https://systems-analysis.ru/eng/GDPval-AA_v2 (secondary)

## 5. Remote Labor Index (RLI)

- **Name / URL / date / maintainer:** Remote Labor Index: Measuring AI Automation of Remote Work, arXiv 2510.26787 (Oct 2025). Leaderboard at https://labs.scale.com/leaderboard/rli and dashboard.safe.ai. Update post: https://safe.ai/blog/significant-increase-in-digital-labor-automation (1 Jul 2026). Maintained by Scale AI + CAIS.
- **Item:** A real, previously completed Upwork project: the brief, input files, and the freelancer's deliverable. Public examples include an earbud 3D model and animation (60 h), a music arrangement (30 h), and apartment interior renders (22 h). 240 projects (230 private test, 10 public) from 23 Upwork subcategories. Mostly multimedia, design, 3D/CAD, architecture, video, audio, games, plus some coding and data.
- **Domain tag:** mixed (heavily creative/multimedia)
- **Resembles:** freelance creative/design work. **Poor match to IT/BPO.** No O*NET mapping: the authors judged O*NET DWAs too generic and used the Upwork taxonomy instead.
- **Human times: per project, private.** Self-reported by the freelancer (midpoints of ranges); available for 84% of projects. **Mean 28.9 h, median 11.5 h**, log-normal. Cost is also per project (mean $633, median $200, total about $144k).
- **Model results over time (automation rate):** Oct 2025: Manus 2.5%, Grok 4 2.1%, Sonnet 4.5 2.1%, GPT-5 1.7%, ChatGPT agent 1.3%, Gemini 2.5 Pro 0.8%. Then Opus 4.5 3.75%, Opus 4.6 (CoWork) 4.17%, GPT-5.2 2.5%, Gemini 3 Pro 1.25%. Jul 2026: Fable 5 15.8%, Opus 4.8 8.3%, GPT-5.5 6.25%. Current leaderboard: **Fable 5.2 41.3%**, Opus 5.5 21.25%, GPT-6 Astra 20.8%, Fable 5.1 17.9%, Gemini Argon 4 17.1%. Scaffolds changed in Jul 2026 (Claude Code/Codex plus computer use, worker–critic loop, $50–150 budget), so the series is not methodologically constant.
- **Item-level public?** No.
- **Grading:** Trained experts judge whether the AI deliverable would be accepted as commissioned work, with the human deliverable as reference (3-point scale; "automation rate" = share at 2 or above; 94.4% agreement). Elo comes from pairwise comparisons. An LLM judge overstated the newer models' rates by 2–3×.
- **Time horizon computed? Yes, by CAIS (Jul 2026), and it failed.** "The relationship is flat to slightly rising, not the downward slope a time-horizon model would assume"; the model "fits the data poorly". They conclude that the assumption "that work taking humans longer is harder for AIs" does not hold across RLI's diverse work, and they keep the automation rate as the metric.
- **Verdict: CANDIDATE (low priority for mapping; high importance as a caution).** Gaps: private times and outcomes, and a creative-work domain mix. Use it as (a) an aggregate acceptance-rate trend for "freelance project" work, and (b) evidence that, across heterogeneous occupations, human time is a weak difficulty index. Fitting within category, or adding modality/category covariates, may be needed. A request to Scale/CAIS for per-project outcomes and times by category would be needed for anything more.
- **Sources:** https://arxiv.org/html/2510.26787v1 ; https://safe.ai/blog/significant-increase-in-digital-labor-automation ; https://labs.scale.com/leaderboard/rli ; https://epoch.ai/blog/what-do-economic-value-benchmarks-tell-us

## 6. TheAgentCompany (CMU)

- **Name / URL / date / maintainer:** TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks, arXiv 2412.14161 (Dec 2024). https://the-agent-company.com ; code at https://github.com/TheAgentCompany/TheAgentCompany ; per-run results at https://github.com/TheAgentCompany/experiments . Maintained by CMU (Xu, Neubig et al.).
- **Item:** A task inside a simulated software company (GitLab, Plane, ownCloud, RocketChat with simulated colleagues). Each task has an instruction, an environment state, and checkpoints scored by an evaluator script. Example: "Collect equipment requests from colleagues on RocketChat, check prices in the ownCloud spreadsheet, compute the total, and message the requester." 175 tasks across SDE, PM, HR, Admin, Finance, DS and other categories.
- **Domain tag:** mixed (software + office/computer use)
- **Resembles:** **IT-services company roles**: developer, project manager, HR/admin, finance back office, data scientist. This is very relevant to Indian IT/BPO. **O*NET:** tasks were built by referencing O*NET 29.1 (job categories chosen by headcount and median wage). There is no per-item O*NET code [I did not find one].
- **Human times: none.** The authors say they "did not collect human performance data" and that tasks take "anywhere from 10 minutes to several hours". Ways to estimate: (a) LLM or expert estimates per task; (b) calibrate with Wang et al. 2025 (arXiv 2510.22780), which measured 48 human workers on 16 TAC-style tasks.
- **Model results over time:** The experiments repo has runs dated 20241217 (Claude 3.5 Sonnet, GPT-4o, Gemini 1.5 Pro / 2.0 Flash, Llama 3.1/3.3, Qwen 2/2.5, Nova Pro), 20250510 (Gemini 2.5 Pro, Claude 3.7 Sonnet, OWL), 20250614 (OpenHands-Versa with Claude 3.7 / Sonnet 4), 20250729, 20251013 (MUSE Gemini 2.5 Flash) and 20251110 (DeepSeek-V3.2). Paper headline: Claude 3.5 Sonnet 24% full completion. Secondary aggregators give later tops of about 40–52% but conflict [unverified]. Updates look sparse in 2026.
- **Item-level public?** **Yes.** Per-task eval outputs for each run are in the experiments repo.
- **Grading:** Deterministic checkpoint evaluators (some LLM-judged checkpoints). Full-completion score plus partial-credit score.
- **Time horizon computed?** None found (not in METR's Jul 2025 cross-domain post).
- **Verdict: CANDIDATE (high).** Item-level results across about 2 years of models already exist, and the task mix matches IT services. The only gap is human times. Fix: have 2–3 annotators estimate times for all 175 tasks, and baseline a stratified subset of about 20–30 by actually timing people.
- **Sources:** https://arxiv.org/html/2412.14161 ; GitHub API listing of TheAgentCompany/experiments/evaluation/1.0.0 ; https://arxiv.org/html/2510.22780 ; https://benchmarklist.com/benchmarks/the_agent_company/ (secondary)

## 7. JobBench

- **Name / URL / date / maintainer:** JobBench: Aligning Agent Work With Human Will, arXiv 2605.26329 (May 2026). https://job-bench.github.io ; HF `JobBench/job-bench` ; GitHub Job-Bench/job-bench-eval. Multi-institution (MIT-IBM, UChicago and others).
- **Item:** A workspace of real public-record files (about 3.9 per task) plus a professional request. Example (biostatisticians): validate a Phase III SAP against Framingham cohort data, recompute sample size under a group-sequential design, and stratify baseline characteristics. The deliverable is graded by a chain of rubrics (35.6 binary criteria per task). 65 main + 63 easy tasks on HF (the paper says 130).
- **Domain tag:** mixed
- **Resembles / O*NET: every item is keyed to one O*NET task statement** plus a WorkBank automation-desire score. It covers 35 O*NET occupations in 10 SOC groups, chosen for high desire (above 3/5) and high OEWS wage bill.
- **Human times:** none.
- **Model results:** One snapshot of 36 agent configs. Claude Opus 4.7 / Claude Code 45.9, GPT-5.5 / Codex 42.7, GPT-5.4 / Codex 38.9; all others 19 or below. The configs span several release dates, so a cross-sectional fit is possible.
- **Item-level public?** Tasks are public; per-model item scores were not found.
- **Grading:** Binary rubric criteria graded by LLM, reported as a score.
- **Time horizon computed?** No.
- **Verdict: CANDIDATE.** Its value is the clean O*NET-task-per-item link. Gaps: human times (estimate them) and per-item results (rerun or request).
- **Sources:** https://arxiv.org/html/2605.26329v1 ; HF datasets-server rows for JobBench/job-bench

## 8. APEX-Accounting (Mercor + Ramp)

- arXiv 2607.27189 (Jul 2026). Blog: https://www.mercor.com/blog/introducing-the-ai-productivity-index-for-accounting/ . 160 closed tasks in 10 held-out "worlds" (synthetic companies at month-end close), plus a 10-task public dev set (HF `mercor/apex-accounting`, `mercor/apex-accounting-harbor`). Task types: **Reconciliation, Data Entry, Variance Analysis, Schedules & Accruals**. These are direct analogues of F&A back-office work. Grading: binary rubric criteria (about 9 per task) judged by DeepSeek-v4-Flash, validated against majority human votes (n=1,687). Results (Jul 2026, mean criteria@3 / Pass@1): Claude Fable 5 56.4 / 9.5; Muse Spark 1.1 52.6 / 7.7; GPT-5.6 Sol 51.5; Opus 4.8 48.0; Gemini 3.1 Pro 34.6; Qwen3.5-397B 28.5. **Human times: none found** in the paper text I searched. Verdict: **CANDIDATE**; pass it to the back-office/finance researcher. Gaps: times, and closed items.

## 9. $OneMillion-Bench

- arXiv 2603.07980 (9 Mar 2026), https://github.com/humanlaya/OneMillion-Bench . 400 expert tasks (Finance, Law, Healthcare, Natural Science, Industry; Global and CN subsets). These are open-ended text problems, optionally with web search. **Each task's dollar value = senior-expert time to complete × market hourly wage** (BLS / tier-1 Chinese city wage guides, ×1.3 overhead when the source is wage-only). The per-task value table is published (Appendix Table 5), so hours can be backed out if the wage per domain is recovered. 35 models in one snapshot (e.g. Opus 4.6 first, then GPT-5.4-High, Qwen3.5-Plus). Rubric scoring with a 0.7 "cliff" threshold for pass. Domain: text, mostly professional Q&A. **Not IT/BPO.** Verdict: **CANDIDATE (low)**.

## 10. UpBench (Upwork)

- arXiv 2511.12306 (Nov 2025). 322 real fixed-price, single-milestone Upwork jobs with verified client payouts, expert-written rubrics, and `onet_tasks` references per job (dataset schema in the paper). Human expert freelancers grade the deliverables; there is also a human-in-the-loop re-attempt arm. Results: Claude Sonnet 4 P1 = 0.398, Gemini 2.5 Pro 0.199, GPT-5 0.196. Related public page: Upwork Human+Agent Productivity Index (https://www.upwork.com/human-agent-productivity-index). **No human times** (only payouts; hours could be guessed from payout ÷ category rate). **The data does not appear to be public**: no HF dataset found. Verdict: **EXCLUDE for now.** It would become valuable if Upwork shared per-job payout, O*NET and outcome data.

## 11. Agents' Last Exam (ALE)

- arXiv 2606.05405 (Jun 2026), UC Berkeley-led, 250+ experts. HF org `agents-last-exam` (ale-tasks-152 and others). 1,490 task instances (152 public), 55 subfields in 13 industry clusters **anchored to SOC 2018 / O*NET**. Graded by deterministic scripts. Three tiers: Near-Term, Full-Spectrum, Last-Exam. Best overall pass is about 23% (GPT-5.5 / Codex CLI); the hardest tier is near 0%. Domains lean towards science, engineering, chip and manufacturing, with some finance, legal and health. **No per-task human times found** (described only as "hours–weeks"). Verdict: **EXCLUDE for now** (no times, poor IT/BPO fit). Re-check if the living leaderboard adds times.

## 12. Excluded briefly

- **xbench-Profession** (arXiv 2506.13651, Jun 2025; https://xbench.org): Recruitment (50 headhunting search tasks) and Marketing (50 influencer-matching tasks). LLM-judge 1–5 scores; no human times. EXCLUDE.
- **OfficeBench** (arXiv 2407.19056, Jul 2024): 300 synthetic Word/Excel/calendar/email tasks across 1–3 apps; exact/fuzzy/execution checks; no human times; old models only. EXCLUDE (OfficeVal supersedes it).
- **WorkBench** (arXiv 2405.00823, May 2024): 690 sandbox tasks over 5 databases and 26 tools (email, calendar, CRM, analytics); GPT-4 43%. Very short tasks, no times. EXCLUDE.
- **PRBench (Scale)** (arXiv 2511.11562): 1,100 single-turn finance and legal questions with expert rubrics; leaderboard at https://scale.com/leaderboard/prbench-legal . No times; not agentic. EXCLUDE.
- **Vals Index** (https://www.vals.ai/benchmarks/vals_index): a GDP-weighted composite (Finance Agent, EMB Excel modelling, Terminal-Bench 2.1, legal, tax); mostly private; no times. Components belong to other researchers' areas. EXCLUDE.
- **OdysseyBench** (arXiv 2508.09124, Microsoft): 300 + 302 long-horizon Word/Excel/PDF/email/calendar tasks; o3 56%, GPT-5 54% (secondary source). No times found. EXCLUDE unless times appear (not deeply checked).

## Has anyone computed a time horizon on these suites?

- **METR cross-domain (Kwa, Jul 2025):** covered OSWorld, WebArena, SWE-bench, math and others, not the occupational suites.
- **CAIS on RLI (Jul 2026):** tried it and found **no negative slope**, so the fit is poor.
- **GDPval paper:** qualitative decline of win rate with task length (Fig. 13); no logistic fit.
- **LessWrong:** logit-trend extrapolations on GDPval win rates only.
- **OfficeVal:** time-weighted scores only.
- Nothing found for APEX-Agents, TheAgentCompany or JobBench.

## Leads I didn't chase

- **OSWorld 2.0** (Yuan et al. 2026): 108 tasks, median about 1.6 h of skilled human time (cited by the OfficeVal paper). For the desktop-GUI researcher.
- **Workspace-Bench 1.0** (arXiv 2605.03596): workspace tasks with large file dependencies; ">3 h expert annotation per task" (annotation time, not completion time).
- **"How Do AI Agents Do Human Work?"** (Wang et al., arXiv 2510.22780): measured human times on 16 O*NET-representative tasks (48 workers); could calibrate TAC time estimates.
- **Rio-Chanona & Einsiedler, "Self-building benchmarks"** (Brookings, Nov 2025): LLM-generated exams for 149 text-only O*NET tasks, 13 models; no times.
- **arXiv 2603.01203:** maps 43 agent benchmarks (72k tasks) onto O*NET; useful for the cross-cutting researcher.
- **Mercor ACE** (consumer tasks) and **APEX-SWE** (Dec 2025): not checked.
- **CRMArena-Pro, WorkArena++, SOP-Bench, FinanceBench, Finance Agent:** belong to other researchers.
- **Ask directly:** OpenAI (GDPval per-task times and outcomes), Scale/CAIS (RLI per-project times and outcomes by category), Mercor (APEX-Agents per-model item results), Upwork (UpBench data).
