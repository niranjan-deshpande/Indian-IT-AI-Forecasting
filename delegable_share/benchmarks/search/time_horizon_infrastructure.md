# Time-horizon infrastructure and methods (cross-cutting search)

Searched 2026-11-09. Every number below was checked against a primary source (METR/Epoch pages, arXiv, GitHub repos, raw data files) unless marked **[unverified]** or **[secondary]**. Where I recomputed numbers from public raw data, the entry says **[our computation]**.

**Units convention (important for our pipeline).** METR's code fits `P(success) = c + (1-c)·σ(β·(log2 H − log2 t))`, so β is **per doubling of human time (log2 minutes)**. An odds ratio per doubling is e^β, so β = 0.25 ≈ 1.28× odds per doubling, which is METR's stated cutoff ([mle.py](https://github.com/METR/cross-domain-horizon/blob/main/mle.py), [cross-domain post](https://metr.org/blog/2025-07-14-how-does-time-horizon-vary-across-domains/)). If our pipeline regresses on natural-log minutes, β_ln = β_log2 / ln 2 ≈ 1.44 × β_log2 (so METR's default 0.6 becomes ≈ 0.87, and the 0.25 cutoff becomes ≈ 0.36).

---

## 1. METR's time-horizon work through late 2026

### 1.1 Timeline of releases

| Date | Output | What it adds | URL |
|---|---|---|---|
| 2025-03-19 | Kwa, West et al., *Measuring AI Ability to Complete Long Tasks* (arXiv 2503.14499; HTML header shows v4) | Original method. 170 tasks (HCAST + RE-Bench + SWAA). 50% horizon doubling time **207 days** (95% CI 166–240). 80% horizon doubles every **204 days** and is ~4–6× shorter than the 50% horizon. | [blog](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/), [arXiv](https://arxiv.org/abs/2503.14499) |
| 2025-03-17 | HCAST paper | The human-calibrated task suite behind it | [arXiv 2503.17354](https://arxiv.org/abs/2503.17354) |
| 2025-07-14 | Kwa & Cheng, *How Does Time Horizon Vary Across Domains?* | 9 extra benchmarks (see 1.3). Median doubling ~4 months (range 2.5–17). | [post](https://metr.org/blog/2025-07-14-how-does-time-horizon-vary-across-domains/), [code+data](https://github.com/METR/cross-domain-horizon) |
| 2025-08-13 | Rein, *Algorithmic vs. Holistic Evaluation* | Test-pass vs mergeable on 18 real OSS issues (see 1.5) | [post](https://metr.org/blog/2025-08-12-research-update-towards-reconciling-slowdown-with-time-horizons/) |
| 2026-01-22 | *Clarifying limitations of time horizon* (note) | Caveats: 50% horizon is not a delegation threshold; 80% and 20% horizons are not independent of the 50% fit; 99% horizons need ~300 tasks per bucket | [note](https://metr.org/notes/2026-01-22-time-horizon-limitations/) |
| 2026-01-29 | **Time Horizon 1.1** | Suite grows from 170 to 228 tasks (+73 HCAST, −15). 8h+ tasks grow from 14 to 31, but only 5 of the 8h+ tasks have human baselines. Infrastructure moves from Vivaria to Inspect. | [post](https://metr.org/blog/2026-01-29-time-horizon-1-1/) |
| 2026-02-13 | *Measuring TH using Claude Code and Codex* | Commercial scaffolds do not beat METR's defaults (Opus 4.5 and GPT-5; differences not significant) | [note](https://metr.org/notes/2026-02-13-measuring-time-horizon-using-claude-code-and-codex/) |
| 2026-03-10 | Whitfill, Wu, Becker, Rush, *Many SWE-bench-Passing PRs Would Not Be Merged* | Merge-based horizons are much shorter than test-pass horizons (see 1.5) | [note](https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/) |
| 2026-03-20 | *Impact of modeling assumptions on TH results* | Sensitivity analysis (see 1.4). Fixes a regularization bug that cut recent 50% horizons by up to 20%. | [note](https://metr.org/notes/2026-03-20-impact-of-modelling-assumptions-on-time-horizon-results/) |
| 2026-04-10 | MirrorCode | Some weeks-long coding tasks (software re-implementation) are within reach. Not a TH-fit. | [post](https://metr.org/blog/2026-04-10-mirrorcode-preliminary-results/) |
| 2026-05-08 | Claude Mythos Preview (early) added | 50% horizon ≈ **1045 min (~17.4 h)**, 95% CI 509–3304 min. 80% horizon **186 min (3h06)**. METR: "Measurements above 16 hrs are unreliable with our current task suite." | [time-horizons page](https://metr.org/time-horizons/), [Epoch mirror CSV](https://epoch.ai/data/benchmark_data.zip) |
| 2026-06-26 | GPT-5.6 Sol evaluation | 50% horizon ≈ 11.3 h (CI 5–40) when cheats count as failures. >270 h if cheats count as successes; 71 h if cheats are discarded. METR calls none of these robust. | [post](https://metr.org/blog/2026-06-26-gpt-5-6-sol/) |
| 2026-07-24 | Cunningham, *Metrics of Agent Ability* | A taxonomy of metrics (binary/continuous horizon, expenditure horizon, "number of nines"). No new numbers. | [note](https://metr.org/notes/2026-07-24-metrics-of-model-ability/) |
| 2026-09-08 | Time-horizons page frozen | "This page is no longer actively updated." No TH 2.0 had been announced as of 2026-11-09. | [page](https://metr.org/time-horizons/) |

### 1.2 TH1.1 per-model results (public, item-level)

Source: [`benchmark_results_1_1.yaml`](https://metr.org/assets/benchmark_results_1_1.yaml) and [`task_results_1_1.yaml`](https://metr.org/assets/task_results_1_1.yaml), which give per-agent logistic coefficients plus per-task n_successes/n_runs for 23 agents × 228 tasks. Raw runs for 21 agents (24,008 runs, with human_minutes, human_source baseline/estimate, and weights) are in [eval-analysis-public `reports/time-horizon-1-1/data/raw/runs.jsonl`](https://github.com/METR/eval-analysis-public). Human-time distribution: median 12.6 min, IQR 0.2–174 min, max 1800 min. 17,765 of the runs are on tasks with real baselines; 6,243 are on tasks with estimated times [our computation].

| Model | Release | H50 (min) [95% CI] | H80 (min) | β (log2) |
|---|---|---|---|---|
| GPT-4 0314 | 2023-03 | 4.0 [2, 8] | 0.9 | 0.64 |
| GPT-4o | 2024-05 | 7.0 [4, 13] | 1.3 | 0.56 |
| Claude 3.5 Sonnet (New) | 2024-10 | 20.5 [10, 41] | 2.6 | 0.47 |
| o1 | 2024-12 | 38.8 [21, 65] | 7.1 | 0.57 |
| Claude 3.7 Sonnet | 2025-02 | 60.4 [33, 104] | 12.1 | 0.60 |
| o3 | 2025-04 | 119.7 [75, 191] | 30.0 | 0.69 |
| Claude Opus 4 / 4.1 | 2025-05 / 08 | 100.4 / 100.5 | 20.4 / 23.5 | 0.60 / 0.66 |
| GPT-5 | 2025-08 | 203.0 [113, 406] | 38.3 | 0.58 |
| Gemini 3 Pro | 2025-11 | 224.3 [140, 379] | 54.1 | 0.68 |
| GPT-5.1-Codex-Max | 2025-11 | 223.7 [134, 396] | 50.6 | 0.65 |
| Claude Opus 4.5 | 2025-11 | 293.0 [162, 624] | 49.4 | 0.54 |
| GPT-5.2 | 2025-12 | 352.2 [198, 815] | 66.0 | 0.57 |
| GPT-5.3-Codex | 2026-02 | 349.5 [195, 816] | 54.7 | 0.52 |
| Claude Opus 4.6 | 2026-02 | 718.8 [317, 3634] | 69.9 | 0.41 |
| Gemini 3.1 Pro | 2026-02 | 384.1 [234, 695] | 89.8 | 0.66 |
| GPT-5.4 | 2026-03 | 341.7 [187, 769] | 53.9 | 0.52 |
| Claude Mythos Preview (early) | 2026-04 | 1044.8 [509, 3304] | 185.9 | 0.56 |
| (human baseliners, as an "agent") | — | 106.4 | 12.3 | 0.45 |

- **β across the 23 TH1.1 agents:** median **0.58**, range 0.41–0.69 [our computation from the YAML coefficients]. Our check: an unregularized, inverse-sqrt-weighted logistic fit on `runs.jsonl` reproduces METR's H50 to within 1% (e.g. Opus 4.6: 718.8 vs 718.8; GPT-5: 203.0 vs 203.0).
- **Doubling times.** The TH1.1 YAML (excluding points with H50 > 16 h) gives 187.8 days stitched over all time and **128.7 days from 2023 on** (CI 104–158). The Jan-2026 blog gave 196.5 days stitched, 130.8 days since 2023, and 88.6 days since 2024. TH1.0 gave 195.8 / 165.3 / 108.9 days.
- **Bug fix.** Opus 4.6 was first reported at ~14.5 h. After the March 2026 regularization fix it is ~12 h (718.8 min). The 14.5 h figure is cited in [LessWrong comments](https://www.lesswrong.com/posts/WacuyurbABwNv8ziq/estimating-metr-time-horizons-for-claude-opus-4-6-and-gpt-5) **[secondary]**. The 12 h figure is in [METR's note](https://metr.org/notes/2026-03-20-impact-of-modelling-assumptions-on-time-horizon-results/).
- **Not on METR's chart:** Opus 4.7, Opus 5/5.5, GPT-5.5, and Gemini 4. METR stopped updating the page on 2026-09-08. GPT-5.6 Sol has the stand-alone, non-robust estimate in 1.1.

### 1.3 Cross-domain paper (Kwa & Cheng, July 2025): benchmarks, human times, H, β

Sources: the [post](https://metr.org/blog/2025-07-14-how-does-time-horizon-vary-across-domains/) and the [repo](https://github.com/METR/cross-domain-horizon). The repo has `data/horizons/*.csv` with per-model `horizon` (min), `slope`, and `slope_method` (mle or guess), plus benchmark length specs in `data/benchmarks/*.toml`. It is public and is a July-2025 snapshot. I found no 2026 update and no arXiv version.

**Method.**
- **When per-item or per-split data exist:** MLE of (H, β).
- **When only overall scores exist:** fix β = 0.6 (`DEFAULT_SLOPE` in `calculate_horizons.py`, roughly the METR-HRS average) and binary-search H so that the expected score matches. METR warns this "can produce large errors" far from the benchmark's median task length.
- **Chance accuracy:** c = 1/n for multiple choice and 1/1000 for AIME.
- **Frontier points:** only models whose H exceeds all previous ones, fit with a linear spline.
- **Exclusion rule:** a benchmark's horizon is excluded if >50% of models have β < 0.25.
- **Robustness:** on METR-HRS the score-only method differs from full MLE by <2×, usually within 25%. It diverged noticeably on AIME, GPQA, and LiveCodeBench.

| Benchmark | Item lengths | How human times were obtained | Agent data | β | Max H in repo (min) | Doubling (METR text) | Our OLS frontier doubling* |
|---|---|---|---|---|---|---|---|
| METR-HRS (HCAST + RE-Bench + SWAA) | 1 s–16 h | Real baselines (~24/170 estimated) | Per-task, 8 runs | MLE ~0.6 | 117.6 (o3, score-only method) | ~4 mo since 2024 | 7.3 (all years) |
| SWE-bench Verified | 7 min–2 h (buckets) | OpenAI annotator buckets → points. The repo uses 7.5 / 30 / 120 / 480 min (194 / 261 / 42 / 3 tasks). The original paper used 3.9 / 30 / 120 / 480 (geometric midpoints). | Per-task (Epoch) | **MLE, median 0.51** (all ≥ 0.25) | **37.8** (Claude Sonnet 4 / Opus 4) | in 2–6 mo cluster | 4.2 |
| OSWorld | 8 s–45 s (as listed) | Paper demo lengths ×1/0.7236 human-success correction | Overall only (leaderboard) | assumed 0.6 | 1.8 (o3 CUA) | similar rate, "~2 yrs behind"; 40–100× shorter | 4.2 |
| WebArena | 5 s–9 min | Times from public leaderboard/trace data | Overall only | assumed 0.6 | 2.5 (IBM CUGA) | same as OSWorld | 4.5 |
| Mock AIME | 5 min–4 h | No baselines. Log-uniform allocation over the 180-min exam, adjusted by assumed per-question success | Per-item (Epoch) | MLE, median 0.76 | 119.5 (o3) | **~3 mo** | 2.8 |
| MATH (Hendrycks) | 2 s–30 min | Author self-timed 4 per difficulty level | Overall | assumed 0.6 | 363.7 (o3-mini; extrapolated beyond longest item) | 2–6 mo cluster | 4.6 |
| LiveCodeBench (11/24–05/25) | 4 min–1.5 h | Author's LeetCode medians 8/20/40 min, log-uniform m/2–2m | 3 difficulty buckets | MLE, median **2.3** | 41.9 | 2–6 mo cluster | 6.4 |
| GPQA Diamond | 5 min–3 h | Mean of the two expert time annotations shipped with the dataset | Per-item (Epoch) | MLE, median 0.52 (13% < 0.25) | 1820 (implausible extrapolation; saturating) | 2–6 mo cluster | 2.7 |
| Video-MME | 1 s–1 h | Video length | 3 length buckets | MLE, median **0.14** (100% < 0.25) → **excluded** | n/a | n/a | — |
| Tesla FSD tracker | n/a | Miles between disengagements → time at 30/60 mph; horizon = MTBF × ln 2 | Tracker | n/a | 93.2 | **~20 mo** | — |
| RLBench | 4 s–20 s | Demo lengths, 18 tasks | Overall | assumed 0.6 | 1.8 | — | 7.2 |

\*Our OLS frontier doubling [our computation]: OLS of log2 H on date over running-max frontier points in `data/processed/all_data.csv`. METR used a linear spline, so these are rough cross-checks, not METR's figures. METR's text gives a median of ~4 months across benchmarks (range 2.5–17), Mock AIME ~3 months, and Tesla FSD ~20 months. The post shows per-benchmark doubling times only in figures.

### 1.4 Methodological follow-ups worth copying

From the [modelling-assumptions note](https://metr.org/notes/2026-03-20-impact-of-modelling-assumptions-on-time-horizon-results/):
- Alternative link functions (Cauchy, Weibull, non-parametric) cut recent 50% horizons by up to 35% and raise 80% horizons by up to 100%.
- A **single slope shared across models** gives the best leave-one-family-out cross-validation error. This supports our pooled-β plan.
- Human-time noise: baseliner attempts are within ~3× of the true length 80% of the time, and estimates within ~4×. A SIMEX noise correction lowers Opus 4.6's H50 by 25–40%.
- Dropping public tasks moves Opus 4.6 from 12 h to 7h11m.
- Inverse-sqrt family weights change results by <10%.

From the original paper:
- **Messiness:** 16 binary factors. In a regression on HCAST, success falls about 8.1 pp per messiness point (b = −0.081, R² = 0.251). Mean messiness is 3.2/16, max 8. Trends over time are similar for low- and high-messiness subsets. ([arXiv 2503.14499](https://arxiv.org/html/2503.14499), App. F.2/H.6)
- **80% horizons:** ~5× shorter than 50% horizons, with a similar doubling time (204 vs 207 days). In TH1.1 the H50/H80 ratio ranges from 4–6× (most models) to ~10× (Opus 4.6) [our computation from the table above].

### 1.5 Tests-pass vs maintainer-merge, and the contractor-vs-maintainer gap

**Whitfill et al. 2026 (METR note, 2026-03-10).** The "~7×" figure in our spec is **confirmed**: the authors call it "roughly a 7× overstatement" for Claude Sonnet 4.5.

Setup:
- 4 maintainers across 3 repos (scikit-learn, Sphinx, pytest) reviewed 296 agent PRs covering 95 of 500 issues.
- PRs came from Claude 3.5 Sonnet, Claude 3.7 Sonnet, Claude 4 Opus, Claude 4.5 Sonnet, and GPT-5, taken from Epoch's hub.
- 47 golden human patches set a noise baseline (~68% merge rate).

Results:
- Merge rate is **24.2 pp below** the grader (SE 2.7).
- Merge rate improves 9.6 pp/yr more slowly than the grader (SE 5.5; weak evidence).
- The doubling-time difference is −9.8 months with an unusable CI (−158 to 2.1).

| Model | T50, test-pass (min) | T50, maintainer-merge (min) | Ratio |
|---|---|---|---|
| Claude 3.5 Sonnet | 4 | 2 | ~2× |
| Claude 3.7 Sonnet | 31 | 6 | ~5× |
| Claude 4 Opus | 35 | 4 | ~9× |
| GPT-5 | 39 | 2 | ~20× |
| Claude 4.5 Sonnet | 50 | 8 | ~6× ("~7×" in text) |

Source: [METR note, App. A9](https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/). The note does not say whether the review data are released.

**Rein (Aug 2025).** 18 issues (15 stdlib-js, 3 hypothesis); humans took 20 min–4 h, mean 1.3 h. Claude 3.7 Sonnet passed tests 38% of the time, but **0 of 15** reviewed PRs were mergeable as-is. Fixing a PR took an average of 42 min (26 min for test-passing ones). ([post](https://metr.org/blog/2025-08-12-research-update-towards-reconciling-slowdown-with-time-horizons/))

**Contractors 5–18× slower than maintainers.** This is confirmed in Kwa et al. 2025 §4 and App. C.2. Five uncontaminated internal-repo issues (six entries) took maintainers 5–235 min. For four issues with recorded times, contractors took 81, 113, 69, and 93 min, i.e. ratios of 16×, ~5.5×, 14×, and 18.6×. ([arXiv HTML](https://arxiv.org/html/2503.14499))

Implication: METR's "human time" is low-context professional time. For high-context incumbents in O*NET tasks, the same task is plausibly 5–18× shorter, which inflates the horizon in "incumbent-minutes."

---

## 2. Aggregators with model-dated (ideally item-level) results

| Source | Coverage | Granularity | Model release dates | Access / licence | Notes |
|---|---|---|---|---|---|
| **METR eval-analysis-public + metr.org YAMLs** | TH1.0 and TH1.1, 228 tasks, 23 agents (GPT-2 → Mythos) | **Per-run** (`runs.jsonl`) and per-task success counts (YAML) | Yes | [GitHub](https://github.com/METR/eval-analysis-public), [task YAML](https://metr.org/assets/task_results_1_1.yaml) | The gold standard. The public `runs.jsonl` stops at Opus 4.6 / GPT-5.3-Codex; the YAML adds Gemini 3.1, GPT-5.4, and Mythos. |
| **METR cross-domain-horizon** | 11 benchmarks, to mid-2025 | Per-model H and β; item-length specs; some raw score files | Yes | [GitHub](https://github.com/METR/cross-domain-horizon) | Reusable code: `mle.py` and `calculate_horizons.py`. |
| **Epoch AI Benchmarking Hub** | 97 benchmarks. Zip (updated 2026-11-10) holds ~90 CSVs, including GDPval, RLI, APEX-Agents, OSWorld, OSWorld 2.0, TheAgentCompany, Terminal-Bench, Cybench, GSO, DeepSWE, Vending-Bench 2, and METR horizons (`metr_time_horizons_external.csv`, with H50, H80, and CIs) | **CSV is per model (aggregate).** For Epoch-run benchmarks (SWE-bench Verified, GPQA Diamond, Mock AIME, FrontierMath, MATH L5, SimpleQA Verified, chess puzzles, …) each row links a public **Inspect `.eval` log** on S3 with **per-sample results and transcripts**. The S3 URL returned HTTP 200 without auth. | Yes (`Release date` column) | CC BY 4.0. [zip](https://epoch.ai/data/benchmark_data.zip), [docs](https://epoch.ai/benchmarks/use-this-data), [python client](https://github.com/epoch-research/epochai-python/) | SWE-bench Verified: 35 runs (33 models) in the current CSV, 34 with logs, latest GLM-5.2 (2026-06). External benchmarks are aggregate only. |
| **Epoch Capabilities Index (ECI)** | IRT across many benchmarks. Bayesian method since 2026-11-04. Anchored at Claude 3.5 Sonnet = 130, GPT-5 = 150. Top listed ECI 174. | Per model, plus `processed_data_for_eci.csv` (benchmark × model scores) | Yes | [ECI](https://epoch.ai/eci), [method](https://epoch.ai/publications/eci-bayesian-methodology), [code](https://github.com/epoch-research/eci-public) | Benchmark-level, not item-level. Useful as the latent ability in a BRIDGE-style map (§4). One blogger regressed log METR-H on ECI ([LessWrong](https://www.lesswrong.com/posts/WacuyurbABwNv8ziq/estimating-metr-time-horizons-for-claude-opus-4-6-and-gpt-5)); it under-predicted Opus 4.6. |
| **Princeton HAL** | The leaderboard shows 9 benchmarks: AssistantBench, CORE-Bench Hard, GAIA, Online Mind2Web, SWE-bench Verified Mini, SciCode, ScienceAgentBench, τ-bench Airline, USACO. The harness also supports AppWorld, τ-bench retail, and ColBench. 26,597 rollouts. | **Full traces, encrypted** (`hal-decrypt`), via W&B Weave. Per-task success is recoverable from traces. | Model names (dates must be joined) | [site](https://hal.cs.princeton.edu/), [harness (archived 2026-07-01)](https://github.com/princeton-pli/hal-harness), [ICLR 2026 paper](https://proceedings.iclr.cc/paper_files/paper/2026/file/a0928f924a344aaebbb7f6cd8d56e34c-Paper-Conference.pdf) | Frozen around late-2025 models (GPT-5, Sonnet/Opus 4.5). New models paused. Reliability dashboard at [/reliability](https://hal.cs.princeton.edu/reliability/). |
| **SWE-bench/experiments** | Every leaderboard submission (Lite, Verified, bash-only, Multilingual, Multimodal) | **Per-instance resolved IDs** (`results/`), plus logs and trajectories via `python -m analysis.download_logs` from S3 or the submitter's repo | Submission date (join model dates) | [GitHub](https://github.com/SWE-bench/experiments) | The largest per-instance multi-model SWE dataset. Since 2025-11-18, Verified submissions are restricted to academic teams. |
| **Terminal-Bench 2.0 leaderboard** | 75 submissions (mostly 2026 models: Opus 4.6/4.7, GPT-5.3-Codex/5.4/5.5, Gemini 3.x, GLM-5, …) | **Per-trial `result.json` + verifier output** for every task × trial (k≈5) | Folder names only (join dates) | [HF dataset](https://huggingface.co/datasets/harborframework/terminal-bench-2-leaderboard), [tasks repo](https://github.com/harbor-framework/terminal-bench-2) | Each task's `task.toml` has `expert_time_estimate_min` and `junior_time_estimate_min` (88/89 tasks; expert median 60 min, range 5–2400; junior median 240) [our computation]. Submissions paused 2026-05. |
| **OSWorld-Verified trajectories** | 15+ model variants, 15/50/100-step budgets | Per-task results and trajectories in zips | Partial | [HF](https://huggingface.co/datasets/xlangai/ubuntu_osworld_verified_trajs) | The dataset viewer is broken; I did not open the zips. **[unverified layout]** |
| **OSWorld 2.0** (2026-06) | 108 long tasks | Rollout trajectories released, plus a **per-task skilled-human time estimate from two annotators** (median ~1.6 h; 69.6% of tasks > 1 h) | Yes | [arXiv 2606.29537](https://arxiv.org/html/2606.29537v1), [site](https://osworld-v2.xlang.ai/) | §4.3 bins tasks by human time (<30 min, 30 min–2 h, >2 h). Success falls with human time and is 0 for every model above ~163 min. Release of per-task times **[unverified]**. |
| **Every Eval Ever (EvalEval)** | 22,235 models, 2,273 benchmarks, 31 formats | Aggregate parquet plus `dataset_samples.parquet` where instance-level data exist (an agentic trace schema exists) | Varies | [paper](https://arxiv.org/abs/2606.14516), [HF datastore](https://huggingface.co/datasets/evaleval/EEE_datastore), [schema](https://github.com/evaleval/every_eval_ever) | Coverage of agentic item-level data **[unverified]**. Worth a targeted query per benchmark. |
| **Harbor Adapters / Harbor-Index** (2026-09) | 80+ benchmarks ported to one harness. 8 models × 54 benchmarks × (Terminus-2 + native harness). Harbor-Index = 82 hard tasks. | Paper says released open-source. Item-level availability **[unverified]**. | — | [arXiv 2609.04298](https://arxiv.org/abs/2609.04298) | Potentially the best cross-benchmark item-level matrix for 2026 models if per-task results are public. |
| **Inspect / inspect_evals** | Eval framework used by METR (TH1.1), UK AISI, Epoch, HAL-like efforts | `.eval` logs store per-sample scores | — | [Inspect](https://inspect.aisi.org.uk/) | Infrastructure, not a results store. Item-level data are wherever the logs are published (Epoch S3, METR). |
| **Artificial Analysis** | Intelligence Index v4.x with agentic components: GDPval-AA (v2, human Elo = 1000), Terminal-Bench (2.1 → 4.0), τ²/τ³-bench, AutomationBench-AA | Per-model aggregate. 45% of v4.3 weight is on private-question evals. | Yes | [v4.1](https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v4-1), [v4.3](https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v4-3) | I found no per-question download **[unverified; likely none]**. |
| **Arena (ex-LMArena)** | WebDev/Code Arena (pairwise); "Agent Arena" (2026, causal success estimates from real usage) | Pairwise or aggregate | — | [arena.ai blog](https://arena.ai/blog/category/product) | No task lengths and no public item-level agent data found. Low value for horizons. |

**Best single source of item-level, multi-model, dated results:**
- **Software:** METR TH1.1, then SWE-bench/experiments plus Epoch's SWE-bench Verified Inspect logs, then the Terminal-Bench 2 leaderboard.
- **Non-software agents:** HAL traces (τ-bench, AssistantBench, GAIA, Online Mind2Web, CORE-Bench), but they stop at late-2025 models.

---

## 3. Third-party time-horizon estimates on other benchmarks

| Who / when | Benchmark(s) | Human-time method | Results | Data/code |
|---|---|---|---|---|
| METR, Kwa et al. 2025, App. H.5 | SWE-bench Verified | OpenAI difficulty buckets → 3.9 / 30 / 120 / 480 min. Spot-checked with 7 baselines on 6 tasks; annotators **underestimate** easy tasks relative to contractors. | Doubling **~70 days** (vs 104–143 for HCAST on the same models). H50: Claude 3 Opus 0.83, GPT-4o 5.96, Sonnet 3.5 (New) 16.9, o1 51.2 min. | [arXiv](https://arxiv.org/html/2503.14499) |
| METR cross-domain 2025 | SWE-bench Verified, OSWorld, WebArena, GPQA-D, Mock AIME, MATH, LiveCodeBench, RLBench, Tesla FSD | See §1.3 | See §1.3 | [repo](https://github.com/METR/cross-domain-horizon) |
| Whitfill et al. 2026 | SWE-bench Verified, test-pass vs merge | Same buckets | Merge T50 2–8 min vs test-pass 4–50 min (§1.5) | [note](https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/) |
| **BRIDGE** (Liu, Gala, Nilaksh, Bahdanau, Reddy, Larochelle; Feb 2026, v2 Jul 2026) | METR suite (calibration), SWE-bench Verified, MLE-bench (38 comps), **GDPval** (Gemini-3-Pro judge, ≥4 = success), Cybench | 2PL IRT on pass/fail, then latent difficulty regressed on log METR human time (R² = 0.81; 1 difficulty unit ≈ 2.26× human time). Predicts times for unlabeled items. | Pooled frontier H50 ~1.4–2.5 h. H80 ~40 min overall: METR 54 min, SWE-bench 44 min, MLE-bench 1.1 h, **GDPval ~20 min**. Doubling ~6 months (50% and 80%). The paper has typos (a "22 hours" and a "66 months"). | [arXiv](https://arxiv.org/html/2602.07267v2), [site](https://mcgill-nlp.github.io/BRIDGE/), [code](https://github.com/McGill-NLP/BRIDGE) |
| Ihle, *WeirdML Time Horizons* (LessWrong, Feb 2026) | WeirdML (17 ML tasks, thresholds 25–95%) | **LLM estimates** (GPT-5.2, Gemini 3 Pro, Opus 4.5, Grok 4) of a median researcher's time | H from 24 min (GPT-4) to 37.7 h (Opus 4.6). Doubling 4.8 mo [3.8, 5.8]; 5.7 mo after calibrating to author's own estimates, which are 3–8× lower. | [post](https://www.lesswrong.com/posts/hoQd3rE7WEaduBmMT/weirdml-time-horizons), [code](https://github.com/htihle/weirdml-time-horizons) |
| Gould, Ward, … Greenblatt, Stastny, *Think Fast* (Jun 2026) | 43 benchmarks, **no-CoT** (math, coding, puzzles, ToM; some agentic, e.g. TerminalBench, SHADE-Arena) | Existing human times, small human trials, else Claude Opus 4.7 estimates with in-context examples. Human-measured-only check: doubling 349 days. | No-CoT H50 for GPT-5.5 ≈ 3 min. Doubling 373 days (CI 167–691); per-domain 246–387 days. | [arXiv 2606.07157](https://arxiv.org/abs/2606.07157), [LW](https://www.lesswrong.com/posts/SieLowPgNgRSPGhFw/estimating-no-cot-task-completion-time-horizons-of-frontier). Data on request. |
| CharlesD (LessWrong, Feb 2026) | METR-H predicted from ECI-style IRT (10 agentic benchmarks incl. Terminal-Bench 2, GDPval-AA, SWE-bench Pro, ARC-AGI-2) | n/a (maps ability to METR H) | Predicted ~8.7 h for Opus 4.6; actual ~12 h post-fix | [post](https://www.lesswrong.com/posts/WacuyurbABwNv8ziq/estimating-metr-time-horizons-for-claude-opus-4-6-and-gpt-5) |
| OSWorld 2.0 authors (2026-06) | OSWorld 2.0 | Two annotators timed each task | No fitted H. GPT-5.5 / Opus 4.7 reach 20–24% on <45-min tasks, <10% at 137–163 min, 0% above. Authors: the METR trend "transfers only partially" to computer use. | [arXiv](https://arxiv.org/html/2606.29537v1) |

**Not found:** published METR-style H/β for τ-bench / τ²-bench, WebArena-Verified, TheAgentCompany, Terminal-Bench (despite its time fields), GDPval with real expert times, or RLI. BRIDGE's GDPval number uses IRT-predicted times, not GDPval's own expert times.

---

## 4. Estimating human item times when a benchmark lacks them

| Method | How | Validation evidence | Use when |
|---|---|---|---|
| **Native times shipped with the benchmark** | Use per-item human times, conditioned on human success (METR uses the geometric mean of successful baselines). Examples: GDPval (expert hours, mean ~7 h; [Epoch](https://epoch.ai/blog/what-do-economic-value-benchmarks-tell-us)), RLI (self-reported freelancer hours, mean 29 h, ~$600 billed), APEX-Agents (timed subsample, ~2 h), OSWorld (demo lengths), OSWorld 2.0 (two annotators), GPQA (two expert annotations), Cybench (first-solve times), Terminal-Bench 2 (author expert and junior estimates), GAIA (annotator metadata reportedly includes time taken **[unverified; dataset gated]**) | METR: baseliner attempts are within ~3× of truth 80% of the time; estimates within ~4×. Arithmetic means run ~25% above geometric. ([note](https://metr.org/notes/2026-03-20-impact-of-modelling-assumptions-on-time-horizon-results/), [limits](https://metr.org/notes/2026-01-22-time-horizon-limitations/)) | Always first |
| **Bucket → point** | SWE-bench Verified annotator buckets (<15 min, 15 min–1 h, 1–4 h, >4 h) → geometric midpoints **3.9 / 30 / 120 / 480 min** (METR paper). The cross-domain repo used 7.5 for the first bucket. Distribution: 194 / 261 / 42 / 3. | Spot check with 7 baselines on 6 tasks. Annotators underestimate easy tasks, which shortens the doubling time (70 days vs 104–143). | Any benchmark with difficulty or time buckets |
| **IRT calibration (BRIDGE)** | Fit 2PL IRT on an item × model pass/fail matrix; regress difficulty on log human time for anchor items with real times; predict the rest | R² = 0.81 on METR. Cybench: 92.3% of items within 0.5–2× of real first-solve time. Beats LLM estimators on SWE-bench buckets. Rank robust with 70% of cells missing (ρ > 0.94). | Item-level multi-model data exist (HAL, SWE-bench/experiments, TB2) and a few anchor times can be obtained |
| **LLM-estimated times** | Prompt a frontier model with the task, the human profile, and few-shot real times | METR transcript note: GPT-5 judge vs 34 human estimates, r_log = 0.83, within 2–3×, **biased high**. BRIDGE: LLM estimates "consistently overestimate" on Cybench. WeirdML: LLM estimates 3–8× above the author's. | Fallback. Always calibrate with a multiplicative correction fit on items with real times. |
| **Freelance price → hours** | Hours = price / market hourly rate (SWE-Lancer payouts, RLI billed price) | RLI hours roughly track wages (Epoch). But SWE-Lancer task value did **not** correlate with model success (METR limitations note), so price is a weak difficulty proxy. | Only for priced marketplace tasks. Cross-check with hours where available. |
| **Step-count / output-size → time** | Map human or agent steps (or LOC) to minutes | OSWorld 2.0: agent step counts rise with human-time bins (e.g. 301–450-step bin is 18.9% of easy vs 42.9% of hard tasks). METR: committed LOC per day explains ~46% of variance in estimated minutes. No validated conversion factor found. | Last resort, short GUI/web tasks |
| **Author self-timing** | Researcher times a sample per difficulty level (METR did this for MATH and LiveCodeBench) | Kwa & Cheng flag low confidence | Small item pools |

Context-level adjustments:
- **Low vs high context:** contractors were 5–18× slower than maintainers (§1.5).
- **Mergeability:** test-pass → merge cuts H by ~2–20× (~7× for Sonnet 4.5).
- **Messiness:** about −8 pp success per messiness point.

---

## Implications for our catalog

**A. Usable published H, and sometimes β (we can take these directly):**

| Benchmark | H available | β | Trend | Caveat |
|---|---|---|---|---|
| METR-HRS TH1.1 (software / ML research) | H50, H80, and CIs for 23 agents to Mythos (17.4 h); GPT-5.6 separately | **Per-model, median 0.58 (log2)** | 128.7 days since 2023; ~188 days stitched | Saturated above 16 h; frozen 2026-09 |
| SWE-bench Verified (test-pass) | Per-model to mid-2025 (max ~38 min); paper values for 2024 models | MLE, median 0.51 | ~70 days (paper); ~4 mo (our OLS) | Annotator buckets; contamination; **merge-adjust ÷~7** |
| SWE-bench Verified (merge) | T50 for 5 models (2–8 min) | not reported | not identified | Small n (95 issues, 3 repos) |
| OSWorld, WebArena | H to mid-2025 (1.8 / 2.5 min) | **assumed 0.6** | ~same as software, ~2 yrs behind | Score-only method; old leaderboards |
| GPQA-D, Mock AIME, MATH, LiveCodeBench | Yes | MLE (0.52 / 0.76 / – / 2.3) | 2–6 mo | Not agentic; little relevance to O*NET tasks except as a check |
| GDPval, MLE-bench, Cybench, SWE-bench (pooled) | BRIDGE H80 only (GDPval ~20 min) | implicit in IRT | ~6 mo pooled | IRT-predicted times, not GDPval's own expert times |
| WeirdML | H via LLM times | per-model fits | 4.8–5.7 mo | LLM times biased high |

**B. Data exist; we can fit H and β ourselves (priority order):**
1. **SWE-bench Verified, extended to 2026.** SWE-bench/experiments per-instance results plus Epoch Inspect logs (33 models to mid-2026), times from OpenAI buckets (3.9 / 30 / 120 / 480). Fit with METR's `mle.py`. Optionally apply Whitfill merge ratios.
2. **Terminal-Bench 2.0.** 75 submissions with per-trial results × per-task expert/junior time estimates. This is a strong candidate for the "testing/IT ops" analogue. Use expert times as the primary measure and junior times as a sensitivity check. Dates come from model names.
3. **HAL benchmarks** (τ-bench airline/retail, AssistantBench, GAIA, Online Mind2Web, CORE-Bench, SciCode, USACO). Per-task success comes from decrypted traces, but **no human times**. Get them by BRIDGE calibration (anchoring on METR/SWE-bench items) or by calibrated LLM estimates. GAIA annotator times may exist **[verify]**.
4. **OSWorld 2.0** (108 tasks with annotator times and released rollouts) and **OSWorld-Verified trajectories** with OSWorld-1 human times. Gives a GUI-domain β instead of the assumed 0.6.
5. **GDPval.** Per-task expert hours exist. Model-level win rates are public (Epoch, AA). Per-task gradings for the 220 gold tasks would be needed; check OpenAI's release and GDPval-AA **[not verified]**.

**C. Everything else (overall scores only, no item times):**
- **Item times:** use, in order of preference, native times, then bucket geometric midpoints, then BRIDGE-style IRT calibration (when an item × model matrix exists), then LLM estimates scaled by a correction fit on anchor items with real times (expect LLMs to overestimate by ~2–3×).
- **H from overall scores:** binary-search H with a **pooled β = 0.6 per log2-minute** (TH1.1 median 0.58; SWE-bench 0.51). Equivalently ≈ 0.84–0.87 per ln-minute; make sure our code uses the same base. METR's own note found a shared slope generalizes best.
- **Error and exclusion:** treat score-only H as ±2× and unreliable away from the benchmark's median item length. Apply the Kwa–Cheng exclusion (drop if most models have β < 0.25) only where β is estimable; Video-MME is the only benchmark they found that failed it.
- **Acceptance gap:** for "accepted output" (our target), apply an acceptance adjustment on top of tests-pass horizons: ~÷7 (range 2–20×) from Whitfill for code. Also consider the 5–18× low- vs high-context time gap when mapping METR minutes to incumbent-worker minutes.
