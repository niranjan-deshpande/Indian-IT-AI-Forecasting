# Benchmark catalog: software testing/QA and IT operations

Researcher: testing & IT-ops slice. Compiled 2026-11-09. Everything below was checked against primary sources (papers, GitHub repos, HF datasets) unless marked **unverified**. Where I ran my own numbers, I say so and give the script logic.

**Bottom line.** Only one family in this area has per-item human times: **Terminal-Bench** (1.0, 2.0, and the continuous 3.0/4.x releases). Every task's metadata file holds author-assigned time estimates (expert and junior for TB1/TB2, expert-only in hours for TB3/4). TB2 also has public per-trial rewards for 73 leaderboard submissions. That makes it the only ready-to-use IT-ops/sysadmin benchmark for a time-horizon fit. The catch: in my own quick fit on those data, the author time estimates predict model failure only weakly. Correlation of log expert time with pooled task success is −0.28, and the common logistic slope is −0.27 per ln(minute). The frontier entries are near saturation (85–91%), so their 50% horizons are not identified. Testing benchmarks (SWT-bench and others) have no human times. SWT-bench Verified can borrow SWE-bench Verified's annotator time buckets because it is a subset of the same issues. SRE/AIOps, DBA, SQL, IaC and network benchmarks have no human times. The exception is DBA-Bench, which ran a Human DBA on all 106 scenarios but did not report durations, so a request to the authors could close that gap.

---

## 1. Terminal-Bench 2.0

- **Paper/URL:** Merrill, Shaw, Carlini et al., "Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces", arXiv 2601.11868 (17 Jan 2026). Tasks: github.com/harbor-framework/terminal-bench-2 (moved from laude-institute). Leaderboard: tbench.ai/leaderboard/terminal-bench/2.0.
- **Release date:** Benchmark released Nov 2025. Paper Jan 2026.
- **Maintainer:** Laude Institute / Stanford and others, now the "Harbor framework" org.
- **What one item looks like:** A Docker container plus a natural-language instruction. The agent works in a shell, and pytest checks the final container state. Example `nginx-request-logging` (category system-administration): "install and configure Nginx with advanced request logging, rate limiting, and custom error pages". Expert estimate 20 min, junior 120 min. Other IT-ops-like items: `configure-git-webserver`, `qemu-alpine-ssh`, `mailman`, `openssl-selfsigned-cert`, `sqlite-db-truncate`, `db-wal-recovery`, `log-summary-date-ranges`, `query-optimize`, `cobol-modernization`, `fix-git`.
- **Number of items:** 89, selected from 229 crowd-sourced tasks by 93 contributors.
- **Domain tag:** software (terminal/CLI).
- **Resembles:** sysadmin and server configuration (9 tasks tagged system-administration), debugging and build/maintenance (5 debugging, 26 software-engineering), data processing and log parsing (4), DB recovery and SQL optimization (a few), and security hygiene (8). Some items are puzzle-like or research-grade, such as `feal-differential-cryptanalysis`, `regex-chess`, `gpt2-codegolf` and `fix-ocaml-gc`. Only about a third of items resemble everyday IT-services work. Subset by `category` before using it as an IT-ops proxy.
- **Human times: per-item (author estimates).** Each `task.toml` has `expert_time_estimate_min` and `junior_time_estimate_min`. Task authors wrote these numbers when they submitted their tasks; nobody timed a baseline. I parsed all 89 files: 88 have both estimates (`caffe-cifar-10` has none).
  - Expert: median **60 min**, range 5–2,400 min (40 h).
  - Junior: median **240 min**, range 10–19,200 min (320 h).
  - Paper's bucket summary: about 49% of tasks under 1 h for experts and 8% for juniors; about 72% of junior estimates fall between 1 h and 1 day.
  - System-administration subset (9 tasks): expert 15–300 min, junior 60–600 min.
  - Caveat: no structured elicitation or calibration. A critique (miclchen Substack) argues these estimates are compressed and noisy. The paper reports that author difficulty labels correlate only r = 0.436 with empirical difficulty.
- **Model results over time:**
  - Paper: SOTA nearly doubled in the 8 months from Gemini 2.5 Pro to GPT-5.2. Codex CLI + GPT-5.2 scores about 62.9%, Terminus 2 + Claude Opus 4.5 57.8%, Terminus 2 + Gemini 3 Pro 56.9%, and the best open model, Kimi K2 Thinking, about 36%.
  - Leaderboard (my parse of the HF submissions repo): 73 usable submissions with runs dated 2025-11-13 to 2026-05-12. Models include GPT-5.x/5.5, Claude Opus 4.5/4.6/4.7, Gemini 3/3.1, GLM-4.7/5, Kimi K2.5, MiniMax, DeepSeek V3.2, Qwen and GPT-OSS.
  - Top pass rates I computed: vix + Claude Opus 4.7 0.91, Wecode + GPT-5.5 0.88, NexAU + GPT-5.5 0.85. Small open models fall to 0.09–0.24.
  - Many entries are scaffold-tuned. Use Terminus-2 entries (a fixed harness) for clean model comparisons.
- **Item/subset-level results:** **Yes.** HF dataset `harborframework/terminal-bench-2-leaderboard` (last updated 2026-05-15) holds, for each submission and job, a `result.json` with the per-trial reward lists. Each trial folder also has `agent/` and `verifier/` logs (trajectories). Paper-run configs are in github.com/laude-institute/terminal-bench-experiments. Its per-trial results appear to sit in a DB that is not obviously public (**unverified**).
- **Grading:** Binary. Hidden pytest checks the final container state. At least 5 trials per task are reported with 95% CIs.
- **Time horizon already computed?**
  - The "Think Fast" paper (Gould, Ward, Greenblatt, Stastny et al., arXiv 2606.07157, v4 Aug 2026) fits METR-style logistics on TB2 with the author estimates, but **only for no-CoT agents**. That is not the standard agentic horizon.
  - I found no METR or Epoch agentic time horizon on TB2.
  - **My own quick fit** (73 submissions, about 30,600 trials, success = reward ≥ 1):
    - Corr(ln expert time, pooled per-task success) = −0.28. With junior estimates it is −0.24.
    - Logistic fit with submission fixed effects and a common slope: β = −0.27 per ln(min) for expert estimates and −0.21 for junior.
    - Per-submission fits for frontier entries give slopes near zero, so H50 extrapolates far beyond the 40 h maximum (not identified). Mid-tier entries, e.g. Deep-Agents + GPT-5.2-Codex at 69% success, give H50 of about 15 h expert time. Weak small models give H50 under 5 min.
- **Verdict: INCLUDE**, with caveats.
  - It is the only IT-ops/sysadmin benchmark with per-item times plus per-trial multi-model results.
  - Use expert estimates, subset to sysadmin/debugging/data-processing/SE, and pool with TB1 for a longer date range.
  - The weak time–difficulty link means β will be shallow and H noisy. Treat any time-horizon number from TB2 alone as low-confidence.
  - The date span of leaderboard per-trial data is only about 6 months. For earlier models, use the paper's aggregate scores or TB1.
- **Sources:** arxiv.org/abs/2601.11868; arxiv.org/html/2601.11868v1; github.com/harbor-framework/terminal-bench-2 (all 89 task.toml parsed); huggingface.co/datasets/harborframework/terminal-bench-2-leaderboard; tbench.ai/leaderboard/terminal-bench/2.0; arxiv.org/abs/2606.07157 (Section D.38); miclchen.substack.com/p/how-could-benchmarks-collect-highly; github.com/laude-institute/terminal-bench-experiments.

## 2. Terminal-Bench 1.0 (terminal-bench-core v0.1.1)

- **Paper/URL:** github.com/harbor-framework/terminal-bench-1 (formerly laude-institute/terminal-bench). Leaderboard on tbench.ai (1.0).
- **Release date:** May 2025 (core v0.1.0 had 71 tasks; v0.1.1 has 80).
- **Maintainer:** Laude Institute / Stanford.
- **What one item looks like:** Same container + test format as TB2. Example `fix-git`: "I just made some changes to my personal site and checked out master, but now I can't find those changes. Please help me find them and merge them into master." Expert estimate 5 min, junior 20 min.
- **Number of items:** 80 in core v0.1.1. The full pool in `original-tasks/` has 241 tasks.
- **Domain tag:** software.
- **Resembles:** sysadmin, git, build, and server setup. Easier and more everyday than TB2.
- **Human times: per-item author estimates, but incomplete.** `task.yaml` has `expert_time_estimate_min` and `junior_time_estimate_min`. I parsed all files: 198 of 241 tasks have estimates, but only **42 of the 80 core tasks** do. Core expert median 30 min, range 2–2,400 min.
- **Model results over time:** The 1.0 leaderboard covered models from roughly Claude 3.7 / GPT-4.1 through GPT-5 / Claude 4.x (mid-2025). **Unverified:** I could not load the 1.0 leaderboard table.
- **Item/subset-level results:** Not located. TB1 runs used the older `tb` harness. A leaderboard folder exists in the repo; I did not check whether it holds per-task data.
- **Grading:** Same as TB2 (pytest on container state).
- **Time horizon already computed?** None found.
- **Verdict: CANDIDATE.** It extends the TB date range back to early/mid 2025, but only 42 core tasks have times. Gap: per-task leaderboard results. Close it by checking the `leaderboard/` folder in harbor-framework/terminal-bench, or by rerunning older models via Harbor, which supports TB1 via adapter.
- **Sources:** github.com/harbor-framework/terminal-bench-1 (original-tasks/*/task.yaml and registry.json parsed).

## 3. Terminal-Bench 3.0 / 4.0 / 4.1 (continuous Terminal-Bench)

- **Paper/URL:** github.com/harbor-framework/terminal-bench (releases v3.0.0 on 2026-07-23, v4.0.0 on 2026-08-26, v4.1.0 on 2026-11-03). Blog: tbench.ai/news/terminal-bench-4-0. Leaderboard on Harbor Hub (hub.harborframework.com/datasets/terminal-bench/terminal-bench).
- **Release date:** Jul–Nov 2026.
- **Maintainer:** Harbor framework / Laude Institute. Some tasks are contributed by Scale AI and others.
- **What one item looks like:** The same container format, but tasks are longer and the agent timeout is a flat 8 h. Examples in categories relevant to us:
  - `medical-claims-processing` (Operations/Claims, 2 h)
  - `heat-pump-warranty` (Claims, 4 h)
  - `legacy-utility-triage` (Claims, 3.5 h)
  - `intrastat-meldung` (Compliance, 3 h)
  - `live-database-cutover` (Databases, 8 h)
  - `wal-recovery-ordering` (6 h)
  - `payments-pipeline-fix` (2 h)
  - `react-lead-form` (Frontend, 5 h)
  - `vba-userform-port` (4 h)
- **Number of items:** 66 task dirs on `main` as of today. v4.1 adds a 63-task CPU-only subset.
- **Domain tag:** software (some items are back-office-like computer work done via the terminal).
- **Resembles:** Operations (9 tasks: claims, logistics, compliance, finance, supply chain), Software (18: databases, frontend, systems, data engineering), and Security (5). Notably, it is the closest thing in my area to claims processing and back-office work. **Flag to the back-office researcher.**
- **Human times: per-item author estimates.** `expert_time_estimate_hours` is in every `task.toml`. I parsed all 66: median **4.0 h**, range 0.75–60 h. Expert only; there is no junior estimate. Elicitation is the same uncalibrated author estimate as TB2.
- **Model results over time:**
  - Official: per the 4.0 blog, results come from the Harbor Hub leaderboard, which did not render for me.
  - Aggregators (**unverified**, not mutually comparable): Claude Opus 5 at 51.8% on the Aug 2026 snapshot; Artificial Analysis Sept snapshot GPT-6 Astra 59.1%, Claude Fable 5.1 52.0%; Vals Sept snapshot Claude Opus 5.5 61.6%; one early-Nov aggregator has Claude Sonnet 5.5 at 70.6%.
  - The models span only about Jul–Nov 2026.
- **Item/subset-level results:** Unknown. If Harbor Hub exposes job and trial results the way the TB2 HF repo did, this is fixable. **Unverified.**
- **Grading:** pytest on container state. Version 4.1 hardened the verifiers against reward hacking.
- **Time horizon already computed?** None found.
- **Verdict: CANDIDATE.** It has per-item times, a long-task range (1–60 h) that fits a frontier horizon, and back-office Operations tasks. Gaps: (a) per-trial results, which may be obtainable from Harbor Hub or by running ourselves with `harbor run`; (b) a short model date range; (c) saturated tasks are removed each release, which biases the item pool against easy tasks. Pair it with TB2 to bridge.
- **Sources:** github.com/harbor-framework/terminal-bench (README, releases API, tasks/*/task.toml parsed); tbench.ai/news/terminal-bench-4-0; benchlm.ai/benchmarks/terminalBench4; capitalandcompute.net/blog/terminal-bench-4-0; artificialanalysis.ai/evaluations/terminalbench-v4-0.

## 4. SWT-bench (Lite / Verified): test generation for issue reproduction

- **Paper/URL:** Mündler, Müller, He, Vechev, "SWT-Bench: Testing and Validating Real-World Bug-Fixes with Code Agents", NeurIPS 2024, arXiv 2406.12952. Site: swtbench.com. Code: github.com/logic-star-ai/swt-bench.
- **Release date:** Jun 2024. The Verified split followed in early 2025.
- **Maintainer:** ETH Zurich SRI Lab / LogicStar AI.
- **What one item looks like:** A GitHub issue plus the repository at the pre-fix commit. The agent must write tests that fail on the original code and pass after the (hidden) gold patch. Example: a Django or SymPy issue describing wrong output, and the agent adds a unit test reproducing it.
- **Number of items:** Full 1,900+, Lite 276, Verified **433**. Verified is a subset of SWE-bench Verified.
- **Domain tag:** software.
- **Resembles:** QA and test engineers writing regression and bug-reproduction tests, and maintenance work (app maintenance, testing).
- **Human times: none native, but estimable.** SWT-bench Verified instances are SWE-bench Verified instances, so join on `instance_id` to the SWE-bench Verified `difficulty` column (annotator buckets: <15 min 194, 15 min–1 h 261, 1–4 h 42, >4 h 3, all 500 checked via the HF datasets-server). Caveat: those buckets estimate time to *fix* the issue, not to write the reproducing test. Writing the test is arguably a sub-step, so treat the bucket as an upper bound.
- **Model results over time (swtbench.com, Verified):**
  - Feb 2025: Zero-Shot+ GPT-4o 14.3%; OpenHands + Claude 3.5 Sonnet 27.7%.
  - Mar 2025: Otter++ GPT-4o 37.4%.
  - Apr 2025: Amazon Q 51.0%.
  - Aug 2025: OpenHands + GPT-5 79.8%.
  - Sep 2025: LogicStar L* 84.0%.
  - Dec 2025: TEX-T + Claude 4 Sonnet 87.0%.
  - Oct 2026: DPIAgent + GPT-5 87.5%.
  - Nov 2026: Claude Code + Claude Opus 5.5 87.8%; Bugstack (Sonnet 5.5 + Opus 5.5) **91.5%**.
  - Lite runs from 2024-05 (SWE-Agent GPT-4 15.9%) to 2026-03 (DevstralTestGen 89.1%).
  - Many entries are bespoke systems, not fixed-scaffold model comparisons.
- **Item/subset-level results:** Each leaderboard entry links to trajectories and eval results (GitHub or files.sri.inf.ethz.ch). I did not open them to confirm per-instance pass/fail, but SWE-bench-style harness output normally includes it. **Partly verified.**
- **Grading:** Execution-based fail-to-pass, plus change coverage of the gold patch (ΔC).
- **Time horizon already computed?** None found.
- **Verdict: CANDIDATE.** It is the best testing benchmark: real QA work and about 2.5 years of results. Gaps: (a) human times are borrowed buckets for a different task (fixing), and almost no items exceed 1 h, so the range is short; (b) it is near saturation (about 90%); (c) the scaffold confound. Close by joining SWE-bench Verified buckets, pulling per-instance logs for entries with a fixed scaffold (OpenHands, Claude Code), and dating by model release.
- **Sources:** swtbench.com; arxiv.org/abs/2406.12952; github.com/logic-star-ai/swt-bench; datasets-server.huggingface.co (princeton-nlp/SWE-bench_Verified difficulty stats); agentmarketcap.ai/blog/2026/04/10/swt-bench-software-testing-agent-benchmark-logicstar.

## 5. TDD-Bench Verified

- **Paper/URL:** Ahmed et al. (IBM Research), arXiv 2412.02883. Code: github.com/IBM/TDD-Bench-Verified.
- **Release date:** Dec 2024.
- **Maintainer:** IBM Research.
- **What one item looks like:** Same as SWT-bench: write a fail-to-pass test from the issue *before* the fix exists (test-driven development).
- **Number of items:** 449, a subset of SWE-bench Verified.
- **Domain tag:** software.
- **Resembles:** test automation and QA.
- **Human times:** None native. Estimable the same way as SWT-bench, via the SWE-bench Verified buckets.
- **Model results over time:** Only the paper (GPT-4o 23.6% F→P, Llama-3.1-70B, Mistral-Large). The README leaderboard says "TBA".
- **Item/subset-level results:** Harness only.
- **Grading:** Fail-to-pass plus coverage.
- **Time horizon already computed?** No.
- **Verdict: EXCLUDE.** It duplicates SWT-bench Verified with almost no multi-model results.
- **Sources:** arxiv.org/abs/2412.02883; alphaxiv.org/benchmarks/ibm-research/tdd-bench-verified.

## 6. TestGenEval (and TestEval)

- **Paper/URL:** Jain et al. (Meta), "TestGenEval: A Real World Unit Test Generation and Test Completion Benchmark", ICLR 2025, arXiv 2410.00752.
- **Release date:** Oct 2024.
- **Maintainer:** Meta FAIR / CMU.
- **What one item looks like:** Given a Python source file from a SWE-bench repo, write the full unit-test file (or complete a partial one). Scoring is pass rate, coverage and mutation score.
- **Number of items:** 1,210 file pairs (68,647 tests) from 11 repos. Lite: 160.
- **Domain tag:** software.
- **Resembles:** writing unit tests (test automation).
- **Human times:** None. Possibly estimable from test-file length or the git history of the original test commits, but that would be crude.
- **Model results over time:** Paper (2024 models, mostly non-agentic). Agentic follow-up TestForge (arXiv 2503.14713) reports 84.3% pass@1 and 44.4% line coverage. No maintained leaderboard found.
- **Item/subset-level results:** Not found.
- **Grading:** Execution: pass@k, line coverage, mutation score (a continuous metric, not binary acceptance).
- **Time horizon already computed?** No.
- **Verdict: EXCLUDE.** No times, sparse results over time, and a continuous metric. **TestEval** (LeetCode programs) is excluded as puzzle-like.
- **Sources:** arxiv.org/abs/2410.00752; arxiv.org/abs/2503.14713.

## 7. SWEeper-Bench: bug discovery and repair in interactive web apps

- **Paper/URL:** Yao, Chen, Kang, Narasimhan, Liu (Princeton), arXiv 2610.14096 (8 Oct 2026). sweeperbench.com. Code: github.com/zlab-princeton/sweeper-bench. Data: HF `zlab-princeton/SWEeper-Bench`. Traces: HF `zlab-princeton/SWEeper-Bench-traces`.
- **Release date:** Oct 2026.
- **Maintainer:** Princeton (Zhuang Liu lab).
- **What one item looks like:** An open-ended QA-plus-fix request on a real open-source web app. Example (Focalboard): "Find and fix issues in Focalboard's board sharing and membership". The bug, a shared board never appearing in the member's sidebar, shows up only after 9 steps across 2 accounts.
- **Number of items:** 200 tasks, each from a different web app, in 7 domains.
- **Domain tag:** software (with browser interaction).
- **Resembles:** manual or exploratory QA of web apps plus maintenance bug-fixing. This is very close to Indian IT "testing + AMS" work.
- **Human times:** **None.** Authors reproduced every bug by hand but did not time it. Agent wall-clock is reported (e.g. 12–100 min average). Estimable via expert elicitation or by timing a sample.
- **Model results over time:** Single snapshot (Oct 2026) of 15 agents: Grok 4.6 (Cursor) 59.0%, Qwen 3.8 Flash 57.5%, Claude Fable 5.1 / Opus 5 / GPT-6 Astra 56.5%, down to Qwen 3.8 Max 28.0%. All frontier models are from 2026.
- **Item/subset-level results:** **Yes**, the traces dataset on HF.
- **Grading:** An agentic browser verifier runs a target-behaviour test plus a preservation test, without source access. Both must pass.
- **Time horizon already computed?** No.
- **Verdict: CANDIDATE.** Strong task realism and public traces. Gaps: no human times and a single time point. Close by expert time estimates for 200 items (cheap) and by rerunning 2025-era models to get a trend.
- **Sources:** arxiv.org/html/2610.14096.

## 8. WebTestBench: end-to-end web app testing

- **Paper/URL:** Kong et al. (Northeastern Univ. China / Kuaishou), arXiv 2603.25226 (26 Mar 2026). github.com/friedrichor/WebTestBench.
- **Release date:** Mar 2026.
- **Maintainer:** Kuaishou / NEU.
- **What one item looks like:** A locally runnable web app plus its development requirements. The agent must (a) generate a test checklist and (b) execute it in a browser to detect seeded defects. Example latent constraint: a meeting-room booking app must not allow double booking of overlapping slots.
- **Number of items:** 100 apps, 1,750 gold test items.
- **Domain tag:** computer_use (browser) and software.
- **Resembles:** manual QA and test-case writing for web apps.
- **Human times:** None.
- **Model results over time:** Single snapshot of about 10 models (GPT-5.1, GPT-5.2, Claude Sonnet/Opus 4.5, GLM-4.7/5, …). Best F1 is about 26%; coverage is below 70% for all models.
- **Item/subset-level results:** Code and data are public. Per-item results are not confirmed.
- **Grading:** An LLM judge (Qwen3.5-27B) matches checklist items to gold, plus precision/recall/F1 on defects. Not binary.
- **Time horizon already computed?** No.
- **Verdict: EXCLUDE** for now. Continuous F1 scoring, no times, one time point. It is useful only as a qualitative QA-capability signal.
- **Sources:** arxiv.org/html/2603.25226.

## 9. ITBench / ITBench-AA (IBM): SRE, CISO, FinOps

- **Paper/URL:** Jha et al. (IBM / UIUC), "ITBench: Evaluating AI Agents across Diverse Real-World IT Automation Tasks", ICML 2025, arXiv 2502.05352. github.com/itbench-hub/ITBench. **ITBench-AA:** Artificial Analysis + IBM, launched 27 May 2026 (huggingface.co/blog/ibm-research/itbench-aa; HF dataset `ArtificialAnalysis/ITBench-AA`; leaderboard on artificialanalysis.ai).
- **Release date:** Feb 2025 (ITBench); May 2026 (ITBench-AA).
- **Maintainer:** IBM Research; Artificial Analysis for AA.
- **What one item looks like:** A Kubernetes incident snapshot (alerts, events, traces, metrics, logs, topology). The agent investigates with shell commands and submits a JSON list of root-cause entities. Example: frontend errors traced to `otel-demo/NetworkPolicy/frontend-block-all-ports`.
- **Number of items:** Original ITBench has 94 scenarios across SRE, CISO and FinOps. ITBench-AA SRE has 59 (40 public, 19 held out). The public `data.jsonl` has 40 rows with fields `id_aa, scenario_id, category, source_split, scenario_root, ground_truth_yaml`; I checked, and there is **no time or difficulty field**.
- **Domain tag:** software (IT ops).
- **Resembles:** L2/L3 production support and SRE incident triage (RCA), and compliance checks (CISO). This is core Indian IT infrastructure-management work.
- **Human times:** **None.** Estimable by having SREs estimate or time diagnosis per scenario. As a production reference, Kuaishou's KRCA paper (arXiv 2607.01788) cites about 52 min average manual root-cause localization.
- **Model results over time:**
  - Original paper: SRE 13.8%, CISO 25.2%, FinOps 0% (early-2025 models; an earlier version says 11.4% SRE).
  - ITBench-AA (May 2026): Claude Opus 4.7 47%, GPT-5.5 46%, Qwen3.7 Max 42%, GLM-5.1 40%, Gemini 3.5 Flash about 40%, DeepSeek V4 Pro 38%, Gemma 4 31B 37%, Gemini 3.1 Pro 30%.
  - Artificial Analysis will presumably add models over time (FinOps and CISO are "coming").
- **Item/subset-level results:** Not confirmed public. Scenario snapshots and ground truth are public.
- **Grading:** Average precision at full recall. A miss of any root cause scores 0. The score averages 59 tasks × 3 repeats. Can be binarized (full recall plus precision = 1).
- **Time horizon already computed?** No.
- **Verdict: CANDIDATE.** It is the most realistic IT-ops incident benchmark with a maintained multi-model leaderboard. Gaps: human times (needs elicitation; 59 items is feasible) and per-item results (ask Artificial Analysis, or rerun with their Stirrup harness).
- **Sources:** arxiv.org/abs/2502.05352; huggingface.co/blog/ibm-research/itbench-aa; artificialanalysis.ai/articles/itbench-aa-launch; HF API for ArtificialAnalysis/ITBench-AA (data.jsonl inspected); github.com/itbench-hub/ITBench.

## 10. SRE/AIOps live benchmarks: AIOpsLab, SREGym, SRE-Marathon (grouped)

- **Paper/URL:**
  - AIOpsLab: Microsoft, arXiv 2501.06706; leaderboard microsoft.github.io/AIOpsLab.
  - SREGym: Clark, … Xu (UIUC), arXiv 2605.07161.
  - SRE-Marathon: Tian … Jacobsen (Toronto), arXiv 2609.33023 (26 Sep 2026).
- **Release date:** Jan 2025 / May 2026 / Sep 2026.
- **What one item looks like:** A fault is injected into a live microservice app on Kubernetes (Online Boutique, Astronomy Shop, Train Ticket). The agent must detect, localize, find the root cause and mitigate. SRE-Marathon injects about 60 faults over 60 min from a 700-fault catalog and scores correlation, localization and repair.
- **Number of items:** AIOpsLab 48 problems (four task levels); SRE-Marathon 700 faults.
- **Domain tag:** software (IT ops).
- **Resembles:** NOC/SRE on-call, incident management.
- **Human times:** **None** in any of them. I checked the SRE-Marathon text.
- **Model results:**
  - AIOpsLab: paper-era models (GPT-4, GPT-3.5, Llama-3); the leaderboard is sparse.
  - SRE-Marathon: Kimi K2.5 and GPT-5.6 Luna with 10 scaffolds; best Marathon-Score is 41.3 (Keep-agent + Kimi K2.5).
  - SREGym: PDF not parseable; **unverified**.
- **Item/subset-level results:** Not confirmed.
- **Grading:** Deterministic state probes with partial credit.
- **Time horizon already computed?** No.
- **Verdict: EXCLUDE.** No human times, few models, scaffold-dominated, continuous scores. Keep ITBench-AA as the SRE representative.
- **Sources:** arxiv.org/abs/2501.06706; microsoft.github.io/AIOpsLab/pages/leaderboard; arxiv.org/html/2609.33023v1; arxiv.org/abs/2605.07161.

## 11. DBA-Bench: database operations agents

- **Paper/URL:** Chen, Jiang, Chen, Liang, Zheng (UESTC), arXiv 2607.22165 (24 Jul 2026). github.com/TanJI-C/DBA-Bench (full release "upon publication").
- **Release date:** Jul 2026.
- **Maintainer:** UESTC.
- **What one item looks like:** A live PostgreSQL instance under workload, a symptom alert and a dirty snapshot. The agent diagnoses and remediates through metric, SQL and instance tools. Example: a 1.2M-row hot-key insert with autovacuum disabled leaves stale statistics, so a bad plan holds locks and checkout writes time out. The fix is `ANALYZE` on the table (4-hop diagnosis).
- **Number of items:** 106 PostgreSQL scenarios (42 Easy, 64 Hard) across query tuning, system failure, health check, business change (schema), resource governance, composite faults and misleading alerts. The abstract also mentions TiDB.
- **Domain tag:** software (DBA).
- **Resembles:** DBA L2/L3 support, a core Indian IT infrastructure-services role.
- **Human times:** **Human DBA runs exist for all 106 scenarios** (93.4% Safe Pass) using the same tools and verifier, **but no durations are reported.** I grepped the full HTML for minute/duration/wall-clock and found none. Estimable: the authors likely have timestamps in the human traces, so ask them.
- **Model results over time:** Single snapshot (mid-2026): GPT-5.5 and Claude Opus 4.8 17.9% Safe Pass; GLM-5.1, Qwen3.7-Max and DBAIOps 14–15%; DeepSeek V4 Pro 10.4%; D-Bot <6%.
- **Item/subset-level results:** Promised ("evaluation artifacts"). Not yet verified.
- **Grading:** Outcome verifier plus a zero-safety-violation rule = "Safe Pass" (binary). Diagnosis and Outcome pass are also reported.
- **Time horizon already computed?** No.
- **Verdict: CANDIDATE.** It is the one IT-ops benchmark here with matched human runs. Gaps: human durations (email the authors for per-scenario human timestamps), per-item model results, and more model vintages. Low pass rates (≤18%) mean only the easy end is informative today.
- **Sources:** arxiv.org/abs/2607.22165; arxiv.org/html/2607.22165v1 (full text grepped).

## 12. Spider 2.0 (Lite / Snow / DBT): enterprise text-to-SQL and data workflows

- **Paper/URL:** Lei et al. (HKU XLANG, Salesforce, Google, …), ICLR 2025 Oral, arXiv 2411.07763. spider2-sql.github.io; github.com/xlang-ai/Spider2.
- **Release date:** Nov 2024.
- **Maintainer:** XLANG Lab (HKU).
- **What one item looks like:** A business question over a large cloud warehouse (BigQuery/Snowflake, often 1,000+ columns). The agent explores the schema and docs and writes SQL; gold SQL averages 144 tokens. DBT tasks are full data-transformation projects.
- **Number of items:** Spider 2.0 has 632; Lite 547; Snow 547; DBT 68.
- **Domain tag:** software (data/SQL).
- **Resembles:** BI/reporting analysts, data engineers, MIS/report-writing in back offices.
- **Human times:** **None.** Difficulty is bucketed by gold-SQL length: Easy <80 tokens (25%), Medium 80–159 (44%), Hard ≥160 (31%). Times are estimable by expert elicitation per bucket. ELT-Bench's "3–5 h per pipeline" annotation effort is a loose analogue for DBT.
- **Model results over time:** The paper's Spider-Agent runs: o1-preview 17.1%, GPT-4o 10.1% (late 2024). The leaderboard is now dominated by bespoke systems: Snow top 96.7 (Genloop Sentinel v2 Pro); Lite 76.2 (Tianqiong + GLM 5.2); DBT 65.6 (SignalPilot). Entries are undated on the page, and Snow access has been disrupted since Aug 2026. Annotation-error critiques exist (ddkang Substack; Emergence "Spider2-E").
- **Item/subset-level results:** Some submitters publish predictions; no central per-item log.
- **Grading:** Execution accuracy against gold result tables.
- **Time horizon already computed?** No.
- **Verdict: CANDIDATE (weak).** Very relevant work content (SQL/reporting), but no human times, and the leaderboard measures systems, not models. Close by eliciting time per item (or per difficulty bucket) and running fixed-scaffold Spider-Agent across model vintages. **BIRD-Interact** (ICLR 2026; 600 tasks; GPT-5 8.7% c-Interact / 17% a-Interact) and **BIRD-Critic** (SQL debugging, 530 PG + 570 multi-dialect; o3-mini 38.9%) have the same gap. BIRD's simple/moderate/challenging labels are not times.
- **Sources:** arxiv.org/abs/2411.07763; arxiv.org/html/2411.07763v2 (difficulty definition); spider2-sql.github.io; github.com/xlang-ai/Spider2; arxiv.org/html/2510.05318; ddkang.substack.com/p/pervasive-annotation-errors-break.

## 13. Cybench: security CTFs (IT-ops/security proxy only)

- **Paper/URL:** Zhang et al. (Stanford), ICLR 2025 Oral, arXiv 2408.08926. cybench.github.io.
- **Release date:** Aug 2024 (v4 Apr 2025).
- **Maintainer:** Stanford (Percy Liang / Dan Boneh groups).
- **What one item looks like:** A professional CTF challenge (crypto, web, pwn, reversing, forensics) in a Kali container. The agent must capture the flag.
- **Number of items:** 40 (from 4 CTF competitions).
- **Domain tag:** software (security).
- **Resembles:** SOC/pentest work, at best partially. Mostly puzzle-like and far from IT-services work.
- **Human times: per-item, measured.** First Solve Time (FST) is the time the fastest competing human team took in the real competition. Range about 2 min to 24 h 54 min. FST is a fastest-team time, not a typical worker's time, so it is biased low.
- **Model results over time:** Paper (GPT-4o, o1-preview, Claude 3/3.5, Llama 3.1 …). Cybench is reported in frontier system cards through 2025–2026 (**unverified** specifics). UK AISI reports cyber time horizons on its own suite, with 80% horizon doubling about every 4.7–5 months (early 2026). That is a different suite.
- **Item/subset-level results:** Paper per-task tables; logs in repo.
- **Grading:** Binary flag match (plus subtask-guided mode).
- **Time horizon already computed?** Not on Cybench specifically that I could find. AISI has done it on its private cyber suite.
- **Verdict: CANDIDATE (low relevance).** It has per-item measured times and multi-year results, but the content is CTF puzzles, not paid IT work. Use only as a security-ops sensitivity check.
- **Sources:** arxiv.org/abs/2408.08926; aisi.gov.uk/blog/how-fast-is-autonomous-ai-cyber-capability-advancing; emergentmind.com/topics/cybench.

## 14. DevOps / IaC / network / env-setup benchmarks (grouped)

- **DevOps-Gym** (Tang … Song, Guo; arXiv 2601.20882, ICLR 2026). 700+ tasks from 30+ Java/Go projects covering build/config, monitoring, issue resolving and test generation. Explicitly excludes CI/CD and IaC. No human times. Few models.
- **IaC-Eval v2** (arXiv 2607.20478, 186 AWS Terraform tasks), **Multi-IaC-Eval** (arXiv 2509.05303), and **TerraFormer** (arXiv 2601.08734, 458 NL→Terraform). Single-shot generation checked with Terraform plan and OPA/Rego. No human times, and mostly non-agentic.
- **NetConfEval** (2024, static), **NetArena** (ICLR 2026, dynamic: routing, Kubernetes networking, host-unreachable fixes), and **CORNETTO** (2026, 231 misconfiguration repairs). None have human times.
- **EnvBench** (JetBrains; arXiv 2503.14443; 329 Python + 665 JVM repos) and **SetupBench** (Microsoft; arXiv 2507.09063; 93 bare-Linux bootstrap tasks). SetupBench compares agent action counts to "optimal human" actions (38–89% unnecessary), but has no times.
- **Domain tag:** software.
- **Resembles:** DevOps/cloud engineers, network admins, build/release engineers.
- **Verdict: EXCLUDE** as standalone sources (no human times, few model vintages, often continuous or partial scores). The best path to cover these job tasks is TB2/TB3 sysadmin-category items, which have times.
- **Sources:** arxiv.org/abs/2601.20882; arxiv.org/html/2607.20478; arxiv.org/pdf/2601.08734; arxiv.org/html/2509.05303v1; github.com/NetConfEval/NetConfEval; en.papernotes.org (NetArena ICLR 2026 notes); arxiv.org/pdf/2503.14443; arxiv.org/abs/2507.09063v1.

## 15. Long-Horizon-Terminal-Bench (LHTB)

- **Paper/URL:** Li, Li, Shi et al. (Tencent HY + universities), arXiv 2607.08964 (v3, Oct 2026). zli12321.github.io/LHTB.
- **What one item looks like / count:** 46 long terminal tasks (games, reverse engineering, systems, research reproduction, finance modelling) with dense weighted sub-task rewards. A task is resolved at R ≥ 0.95.
- **Human times:** **None.** Difficulty was calibrated by DeepSeek-V4-Pro runs under 1.5 h budgets.
- **Model results:** 17 models (Grok 4.5 28.3%, GPT-5.6-sol and GPT-5.5 15.2%, …), single snapshot.
- **Verdict: EXCLUDE.** No human times, low IT-services resemblance.
- **Sources:** arxiv.org/html/2607.08964.

---

## Summary table

| Benchmark | Human times | Multi-model over time | Item-level public | Verdict |
|---|---|---|---|---|
| Terminal-Bench 2.0 | Per-item author est. (expert + junior), 88/89 | Yes (paper 2025 → leaderboard Nov 2025–May 2026) | Yes (HF per-trial rewards + logs) | **INCLUDE** |
| Terminal-Bench 1.0 | Per-item est., 42/80 core | Yes (mid-2025) | Not found | CANDIDATE |
| Terminal-Bench 3.0/4.x | Per-item expert est. (hours), 66/66 | Jul–Nov 2026 only | Unverified (Harbor Hub) | CANDIDATE |
| SWT-bench Verified | Borrowed SWE-bench Verified buckets | Yes (2024–Nov 2026) | Partly (trajectory links) | CANDIDATE |
| SWEeper-Bench | None | One snapshot | Yes (HF traces) | CANDIDATE |
| ITBench-AA | None | Starting (May 2026) | No | CANDIDATE |
| DBA-Bench | Human runs, durations unreported | One snapshot | Promised | CANDIDATE |
| Spider 2.0 / BIRD | SQL-length buckets only | Systems leaderboard | Partial | CANDIDATE (weak) |
| Cybench | Per-item FST (measured) | Yes | Yes | CANDIDATE (low relevance) |
| TDD-Bench V., TestGenEval, WebTestBench, AIOpsLab/SREGym/SRE-Marathon, DevOps-Gym/IaC/Net/Env, LHTB | None | Sparse | Varies | EXCLUDE |

## Leads I didn't chase

- **Harbor Hub API** for TB 3.0/4.x per-trial results (the leaderboard page didn't render through fetch). Worth a direct try or an email to the maintainers (Merrill, Shaw).
- **TB1 `leaderboard/` folder** in github.com/harbor-framework/terminal-bench, which may hold per-task TB1 results from 2025.
- **SREGym** (arXiv 2605.07161): the PDF was unreadable via fetch. Check the problem count, models and any difficulty labels.
- **"Why Do AI Agents Systematically Fail at Cloud Root Cause Analysis?"** (arXiv 2602.09937) and **OpenRCA** (Microsoft, ICLR 2025): RCA datasets, likely without human times.
- **DiagDBench** (arXiv 2611.07339): interactive DB diagnosis, top score 56.24/100. Not opened.
- **ELT-Bench-Verified** (arXiv 2603.29399): data-pipeline benchmark; annotation took 3–5 h per pipeline (construction effort, not solve time).
- **Think Fast** (arXiv 2606.07157) has *estimated* per-item human times for **NL2Bash** and **CyBashBench** (seconds-to-minutes bash one-liners). That could be a short-task anchor for sysadmin, like METR's SWAA.
- **LinuxArena** (control setting; human time-to-complete 5–12 h per main task per Think Fast D.23). It is an AI-control benchmark, but its main tasks are real SWE PRs with human times. Worth a look by the SWE/time-horizon researchers.
- **Out of my scope, noted in passing:**
  - TB 3.0/4.x *Operations* tasks (`medical-claims-processing`, `heat-pump-warranty`, `intrastat-meldung`, `fin-saccr-rwa`) are claims and back-office work with expert-hour estimates (back-office researcher).
  - SWE-bench Verified's `difficulty` buckets are the time source for any SWE-bench-derived benchmark (SWE researcher).
  - METR TH1.1 (Jan 2026) and UK AISI cyber time horizons (cross-cutting researcher).
  - A critique of uncalibrated author time estimates: miclchen.substack.com/p/how-could-benchmarks-collect-highly (cross-cutting).
