# Software-engineering agent benchmarks: catalog for the time-horizon method

Researcher: software-engineering area. Compiled 2026-11-09 from web search plus direct checks of the datasets and repos. "Verified" means I opened the primary file or page. "Secondary" means the claim comes from an aggregator or news story only.

**Top-line findings**

1. **Whitfill et al. (METR, 10 Mar 2026), verified.** The "about 7x" figure holds, but only for one model and one comparison. On SWE-bench Verified, Claude Sonnet 4.5 has a 50% horizon of 50 min when graded by tests and 8 min when graded by whether maintainers would merge. The same comparison for other models: GPT-5 39 vs 2 min, Opus 4 35 vs 4, Sonnet 3.7 31 vs 6, Sonnet 3.5 4 vs 2. So the gap ranges from 2x to about 20x and is very noisy. The headline is about 50% of test-passing PRs would be merged. After normalising to the golden-patch merge rate (68%), the grader overstates merges by 24.2 pp (SE 2.7).
2. **Benchmarks with per-item human times.** Three have them:
   - METR TH1.1: 228 tasks; minutes per task; 162 timed baselines plus 66 estimates.
   - SWE-bench Verified: 500 items in 4 time buckets, with a `difficulty` field on Hugging Face.
   - Multi-SWE-bench: 1,632 items in 7 non-Python languages. Two annotators per item each picked one of the same 4 buckets. The labels are public as xlsx files on GitHub. Before this search I didn't know these per-item labels were public.

   SWE-Lancer has per-item **real dollar payouts** (price list verified, 463 tasks) but no hours.
3. **Most 2025–26 SWE benchmarks have no human times.** This includes SWE-bench Pro, SWE-rebench, SWE-bench Live, SWE-PolyBench, Vibe Code Bench, FeatBench, Commit0, the code-review benchmarks and the migration benchmarks. All of these would need times imputed, for example with a model calibrated on the Verified / Multi-SWE-bench buckets using patch size, files touched and language.

---

## 1. METR Time Horizon suite (TH1.1 = HCAST + RE-Bench + SWAA)

- **Paper/URL:** Kwa et al. 2025, "Measuring AI Ability to Complete Long Tasks" (arXiv 2503.14499). TH1.1 post: https://metr.org/blog/2026-01-29-time-horizon-1-1/. Live page: https://metr.org/time-horizons/
- **Release:** TH1 Mar 2025; TH1.1 29 Jan 2026. Maintainer: METR.
- **Items:** 228 tasks in 79 families: HCAST 157, SWAA 66, RE-Bench 5. I verified these counts from `reports/time-horizon-1-1/data/raw/runs.jsonl`. TH1 had 170 tasks; TH1.1 added 73 HCAST tasks.
  - HCAST tasks are software, ML-engineering, cybersecurity and general reasoning tasks in a container. Example: `acdc_bug/fix_checkpointing`, a bug fix in an ML codebase with a baselined human time of 877 min.
  - SWAA tasks are 1-to-30-second single actions, such as picking which file to open.
  - RE-Bench tasks are 8-hour ML research-engineering optimisation tasks.
- **Domain:** software (mostly), with ML and cyber.
- **Resembles:** app maintenance and debugging, sysadmin and scripting, data-pipeline fixes. It is research-flavoured: well-specified, auto-scorable, and with low context needed. The tasks are "less messy" than client work.
- **Human times: per-item, in minutes.**
  - Of 228 tasks, 162 have timed human baselines (contract professionals, geometric mean of successful baselines) and 66 have estimates. HCAST: 94 baseline, 63 estimate.
  - Range 0.02 min to 1,800 min; median 12.6 min. HCAST median is 44 min.
  - Distribution: <1 min 67; 1–15 min 52; 15–60 min 36; 1–4 h 18; 4–8 h 24; 8 h+ 31. Only 5 of the 31 tasks over 8 h are baselined.
- **Model results over time:** 20 public models in the runs file, from GPT-4 0314 (Mar 2023) to GPT-5.3-Codex and Claude Opus 4.6 (Feb 2026).
  - Examples (TH1.1 50% horizons): GPT-4 0314 3.5 min; Sonnet 3.7 60 min; o3 121 min; GPT-5 214 min; Opus 4.5 320 min.
  - Opus 4.6 is about 12 h after a 3 Mar 2026 bug fix (Cotra blog, secondary).
  - Claude Mythos Preview is estimated at 16 h or more (95% CI 8.5–55 h). METR says the suite is unreliable above 16 h. Mythos is not in the public runs file.
  - Doubling time about 197 days overall; 131 days since 2023.
- **Item-level results:** yes. https://github.com/METR/eval-analysis-public `reports/time-horizon-1-1/data/raw/runs.jsonl` has about 24,000 runs. Fields include `task_id`, `task_family`, `alias`, `score_binarized`, `score_cont`, `human_minutes`, `human_source`, `task_source`, `human_cost` and weights. TH1.0 runs are there too. Task text is mostly private; some example tasks are public.
- **Grading:** automatic task-specific scoring functions, binarised.
- **Time horizon already computed?** Yes, METR. This is the canonical reference.
- **Verdict: INCLUDE.** It is the anchor curve and the only suite with timed baselines across 4 orders of magnitude.
  - Caveat 1: tasks are cleaner than real IT work. Use the merge-rate and holistic adjustments (§3, §4).
  - Caveat 2: the ceiling is near 16 h.
  - Caveat 3: per-task domain tags (SWE vs cyber vs ML) are only available at family level. A SWE-only subset needs a manual family-to-domain map. METR's paper describes the HCAST domains.
- **Sources:** https://metr.org/blog/2026-01-29-time-horizon-1-1/ ; https://github.com/METR/eval-analysis-public (runs.jsonl downloaded and parsed) ; https://metr.org/time-horizons/ ; https://www.planned-obsolescence.org/p/i-underestimated-ai-capabilities (secondary, for the Opus 4.6 correction) ; https://the-decoder.com/metr-says-it-can-barely-measure-claude-mythos-palo-alto-networks-warns-of-autonomous-ai-attackers/

## 2. SWE-bench Verified (and the bash-only / mini-SWE-agent leaderboard)

- **Paper/URL:** Jimenez et al. 2023 (SWE-bench); OpenAI "Introducing SWE-bench Verified" (Aug 2024). https://www.swebench.com ; HF `princeton-nlp/SWE-bench_Verified`
- **Release:** Aug 2024. Maintainers: Princeton/Stanford SWE-bench team, with the OpenAI annotations.
- **Items:** 500 GitHub issues from 12 Python repos (django, sympy, scikit-learn, sphinx, ...). The agent gets the repo and the issue text and must produce a patch that passes the hidden FAIL_TO_PASS tests and keeps PASS_TO_PASS tests passing. Example: fix a Django ORM bug described in an issue.
- **Domain:** software.
- **Resembles:** application maintenance and bug-fix tickets (L2/L3 app support). This is the bread-and-butter of Indian AMS contracts, though these are OSS Python libraries rather than enterprise apps.
- **Human times: per-item buckets.** HF field `difficulty`, which I verified: `<15 min fix` 194, `15 min - 1 hour` 261, `1-4 hours` 42, `>4 hours` 3. The median item is in the 15–60 min bucket.
  - How measured: OpenAI annotators (professional developers) estimated "how long it would take an experienced engineer familiar with the codebase". Three labels were ensembled.
  - These are estimates, not timed attempts. METR notes they may understate time for easy tasks because they exclude familiarisation time.
  - The full annotation zip is at https://cdn.openai.com/introducing-swe-bench-verified/swe-bench-annotation-results.zip (HTTP 200, 2.4 MB).
- **Model results over time:**
  - 182 submissions in `swe-bench/experiments/evaluation/verified`, from Oct 2023 (RAG + Claude 2) to Sep 2026 (`20260901_mini-v2.4.2_gemini-3-5-flash`).
  - Includes a controlled-scaffold series (mini-SWE-agent v2, Feb 2026) for Sonnet 4.5, Opus 4.6, GPT-5.2, Gemini 3 Pro / Flash, GLM-5, Kimi K2.5, DeepSeek 3.2 and MiniMax 2.5.
  - Frontier self-reported scores: Opus 4.7 87.6%; GPT-5.5 88.7% (Vals' independent run: 82.6%); Mythos Preview 93.9%; aggregators list Claude Opus 5 at 96–97% in Sep–Oct 2026 (secondary).
  - Epoch AI Benchmarking Hub runs a 484-item subset with a log viewer: https://epoch.ai/benchmarks/swe-bench-verified
- **Item-level results:** yes. Per-instance `results/` and logs for every submission in https://github.com/swe-bench/experiments; full trajectories via AWS download. Epoch logs are viewable.
- **Grading:** unit tests (FAIL_TO_PASS + PASS_TO_PASS) in Docker.
- **Time horizon already computed?** Yes, three times:
  - METR 2025 paper (validation appendix; the trend holds with a faster doubling time).
  - Kwa & Cheng cross-domain post, Jul 2025: range 7 min–2 h, Epoch agent data. Code: https://github.com/METR/cross-domain-horizon
  - Whitfill et al. 2026, test-graded vs merge-graded horizons (§3).
- **Verdict: INCLUDE**, as the best-matched public benchmark for app-maintenance tickets with per-item time and dense per-item results over three years. Caveats:
  - (a) It is saturated (90%+) and contaminated. OpenAI stopped reporting it on 23 Feb 2026 after finding 59.4% of 138 hard, unsolved items had flawed tests.
  - (b) It has almost no items over 1 h.
  - (c) Times are bucketed. Use geometric bucket midpoints (as METR and Whitfill did), or treat them as interval-censored.
  - Usable for the 2023–mid-2025 part of the trend; weak for 2026 models.
- **Sources:** https://datasets-server.huggingface.co (difficulty field statistics) ; https://openai.com/index/introducing-swe-bench-verified/ ; https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ ; https://github.com/swe-bench/experiments (API listing) ; https://metr.org/blog/2025-07-14-how-does-time-horizon-vary-across-domains ; https://epoch.ai/blog/what-skills-does-swe-bench-verified-evaluate ; https://www.vals.ai/benchmarks/swebench-2025-09-24 (secondary)

## 3. METR maintainer-merge study, "Many SWE-bench-Passing PRs Would Not Be Merged into Main" (Whitfill, Wu, Becker, Rush)

- **URL:** https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/ (research note, 10 Mar 2026). Maintainer: METR.
- **Items:** 296 agent PRs that passed the SWE-bench Verified grader, on 95 of 500 issues from 3 repos (scikit-learn, Sphinx, pytest). They were reviewed blind by 4 active maintainers, with 47 golden human patches as a control.
  - Models: Claude 3.5 Sonnet, 3.7 Sonnet, Opus 4, Sonnet 4.5, GPT-5. The runs came from Epoch's hub.
- **Domain:** software. It is an acceptance-adjustment study, not a benchmark.
- **Human times:** inherited from the SWE-bench Verified buckets (geometric means).
- **Key numbers (verified):**
  - Maintainers merged 68% of golden patches.
  - Golden-normalised, the grader exceeds the maintainer merge rate by 24.2 pp (SE 2.7). Unnormalised, the gap is 34.9 pp.
  - The merge rate improves about 9.6 pp/yr slower than the grader (SE 5.5, weak; not significant on SOTA models alone).
  - Rejection reasons: code quality, breaking other code, core functionality failure, other.
  - 50% horizons, grader vs merge: Sonnet 3.5 4 vs 2 min; Sonnet 3.7 31 vs 6; Opus 4 35 vs 4; GPT-5 39 vs 2; **Sonnet 4.5 50 vs 8 (the "about 7x")**. The merge-based doubling-time difference is uninterpretably noisy (95% CI –158 to +2 months).
- **Item-level data:** not public. Patches were reviewed on private repo copies.
- **Verdict: INCLUDE as an adjustment factor.** It is the direct evidence for "accepted by a paying client" versus "passes tests". Recommended use is a multiplicative acceptance haircut, about 0.5–0.7 of the test-pass probability, rather than a fixed 7x horizon divisor. The ratio varies 2x–20x across models.
- **Sources:** the METR note (fetched) ; https://x.com/whitfill_parker/status/2031408266660503743 ; https://x.com/joel_bkr/status/2031423528608952541

## 4. METR "Algorithmic vs. Holistic Evaluation" (RCT-repo issues)

- **URL:** https://metr.org/blog/2025-08-12-research-update-towards-reconciling-slowdown-with-time-horizons (Aug 2025). Maintainer: METR.
- **Items:** 18 real issues (15 stdlib-js, 3 hypothesis) drawn from METR's developer-productivity RCT.
- **Human times: actual developer implementation times** logged in the RCT: 20 min to 4 h, mean 1.3 h.
- **Results:** Claude 3.7 Sonnet only. It passed maintainer-written tests on 38% (±19%) but **0 of 15 reviewed PRs were mergeable as-is**. An average of 42 min of extra human work was needed (26 min for the test-passing ones), about one third of the task time.
- **Grading:** tests plus manual holistic review.
- **Verdict: CANDIDATE (supporting evidence, n=18, one model).** It is the only SWE item set with real logged work times. It gives a "fix-up time" quantity useful for a partial-credit or acceptance model. Gap: the data is not released. Ask METR for the item-level file.
- **Sources:** the METR post (fetched) ; https://www.lesswrong.com/posts/25JGNnT9Kg4aN5N5s/metr-research-update-algorithmic-vs-holistic-evaluation

## 5. Multi-SWE-bench (ByteDance Seed)

- **Paper/URL:** arXiv 2504.02605 (Apr 2025). https://multi-swe-bench.github.io ; HF `bytedance-research/Multi-SWE-bench` ; https://github.com/multi-swe-bench/multi-swe-bench. Maintainer: ByteDance Seed. There are also "mini" and "flash" subsets in the experiments repo.
- **Items:** 1,632 issues in Java 128, TypeScript 224, JavaScript 356, Go 428, Rust 239, C 128, C++ 129, plus a 500-item Python split borrowed from Verified. Example: `apache/dubbo-10638`, where PojoUtils fails to serialise LocalDate, LocalTime and LocalDateTime in generic calls; the fix adds conversion logic.
- **Domain:** software.
- **Resembles:** enterprise application maintenance in **Java/JS/TS/Go**. This is closer to Indian IT AMS stacks (Java/Spring, JS front ends) than Python-only Verified.
- **Human times: per-item buckets from two independent annotators**, with the same 4 buckets as Verified. Question 5.1 asks: "assuming an experienced engineer has a few hours to get familiar with the codebase, how long to understand, design and code?"
  - **Public per item:** `docs/manual-verification/annotation-results/{java,js,ts,go,rust,c,c++}.xlsx`. The sheets are in Chinese; columns `问题 5.1-1` / `5.1-2` hold the two raters' buckets. I verified this in java.xlsx.
  - 68 annotators with at least 2 years' experience in the language, cross-reviewed. Paper totals: easy (<15 min) 374, medium (15–60 min) 650, hard (>1 h) 608.
  - Harder than Verified: 37% of items are over 1 h, versus 9% in Verified.
- **Model results over time:**
  - Mar 2025 paper: 9 models × 3 scaffolds (MagentLess, MSWE-agent, MopenHands). Examples: Claude 3.7 Sonnet + MopenHands, Java 21.9%, TS 2.2%, Go 7.5%; o1, o3-mini, DeepSeek-R1/V3, Qwen2.5, Doubao.
  - Apr 2025 adds Gemini 2.5 Pro and Llama 4.
  - Later community submissions (Java dir): iSWE (Oct/Dec 2025), InfCode + GPT-5.2 (Jan 2026), CodeArts + MiniMax-M2.5 (Mar 2026), CodeArts + GLM-5.1 (Jun–Jul 2026).
  - Chinese open-weight labs (MiniMax, GLM, Kimi, Qwen) also self-report Multi-SWE-bench in model cards. I could not load the leaderboard page (JS-rendered).
  - Gap: few closed frontier models after mid-2025.
- **Item-level results:** yes, per-instance evaluation results and trajectories in https://github.com/multi-swe-bench/experiments (`evaluation/<lang>/verified/<date_scaffold_model>`).
- **Grading:** unit tests (fail-to-pass, no pass-to-fail) in Docker.
- **Time horizon already computed?** Not that I found.
- **Verdict: INCLUDE**, with gap-filling. It has per-item human-time labels and per-item results, in the languages Indian IT actually maintains. Gap: sparse frontier coverage in 2025–26. Close it by:
  - (a) harvesting model-card scores from open-weight labs (aggregate only), and
  - (b) running the "mini"/"flash" subsets ourselves on a few dated models via its Docker harness.
- **Sources:** https://arxiv.org/html/2504.02605 ; https://huggingface.co/datasets/bytedance-research/Multi-SWE-bench ; GitHub API listings of multi-swe-bench/multi-swe-bench and multi-swe-bench/experiments (java.xlsx downloaded and inspected)

## 6. SWE-Lancer (OpenAI)

- **Paper/URL:** arXiv 2502.12115 (Feb 2025). https://openai.com/index/swe-lancer/ ; code and tasks: https://github.com/openai/preparedness/tree/main/project/swelancer. Maintainer: OpenAI.
- **Items:** real Upwork freelance jobs on the Expensify app (React Native / TypeScript), of two kinds:
  - **IC SWE:** write the fix, graded by end-to-end Playwright tests. Example `16912_4`: "[$1000] Inconsistency hint text for zipcode on home address page vs the connect bank account page".
  - **SWE Manager:** choose the best of several freelancer proposals, graded against the actual manager's choice.
  - Counts: the paper had 1,488 tasks in total, of which Diamond is 502 tasks / $500,800. The **current repo CSV has 463 Diamond tasks (198 IC, 265 Manager), $453,800 total**. On 2025-07-17, 39 IC tasks were dropped so the rest run offline. I verified this by downloading `all_swelancer_tasks.csv`.
- **Domain:** software (web/mobile app).
- **Resembles:** **outsourced app development and maintenance tickets for a commercial product**. It is the closest public match to Indian IT/BPO app work, including the "tech lead reviews proposals" role.
- **Human times: none, but per-item real prices.** IC prices run $50–$32,000, median $500 (84 tasks at $250, 62 at $500, 27 at $1,000). Manager tasks run $125–$32,000, median $500. Diamond issues averaged about 26 days open on GitHub and 47 comments.
  - Estimable by price ÷ a freelance hourly rate (e.g. $25–50/h gives a median of 10–20 h). That is likely an overestimate.
  - Caveat: **prices rise when issues go unsolved** (e.g. one rose to $8,000 over 4 weeks). So price mixes difficulty with market and timing. Use log-price as an ordinal difficulty, calibrated against a small timed sample.
- **Model results over time:**
  - Paper (Diamond): Claude 3.5 Sonnet 26.2% IC, 44.9% Manager, about $208K of $501K; GPT-4o and o1 lower.
  - OpenAI-reported IC Diamond pass rates: GPT-4.5 32.6% (Feb 2025); GPT-5.1 69.7% (Nov 2025); GPT-5.2 74.6% (Dec 2025); GPT-5.3-Codex 81.4% (Feb 2026). These figures are from the llmlearner aggregator citing OpenAI announcements; I didn't confirm each in the original system cards.
  - The OpenAI-only series means there are no independent cross-lab results after 2025.
- **Item-level results:** a per-task harness is public (Inspect port at https://ukgovernmentbeis.github.io/inspect_evals/evals/coding/swe_lancer). I didn't find published per-item results.
- **Grading:** E2E Playwright tests, triple-verified by engineers (IC); match to the manager's choice (Manager).
- **Time horizon already computed?** Not found. A "dollar horizon" is possible.
- **Verdict: CANDIDATE.** It has the best task realism for IT services. Gap: no human times, and an OpenAI-only result series after 2025. To close it:
  - (a) map price to hours (log-linear, anchored by a timed sample of about 20 tasks or by Upwork rate data);
  - (b) run IC Diamond (198 tasks, Inspect) on 5–8 dated models from several labs.
- **Sources:** https://arxiv.org/html/2502.12115 ; https://github.com/openai/preparedness/tree/main/project/swelancer ; raw CSV (parsed) ; https://llmlearner.com/rankings/ic-swe-lancer-diamond (secondary)

## 7. SWE-bench Pro (Scale AI)

- **Paper/URL:** arXiv 2509.16941 (Sep 2025). Leaderboard: https://labs.scale.com/leaderboard/swe_bench_pro_public ; repo https://scaleapi.github.io/SWE-bench_Pro-os ; HF `ScaleAI/SWE-bench_Pro`. Maintainer: Scale AI.
- **Items:** 1,865 issues from 41 repos. Splits:
  - public: 731 in the paper; the HF default config now has **642**, with `v1` and `hard` (51) configs;
  - held-out: 12 repos;
  - commercial: 18 private startup repos, 276 items.
  - Each task has a problem statement plus requirements plus an interface spec. Gold patches average 107 lines across 4.1 files, all over 10 lines. Languages: Python, Go, JS/TS.
- **Domain:** software.
- **Resembles:** feature work and multi-file bug fixes in product codebases. The commercial split is the closest to client work.
- **Human times: none.** The paper only says tasks may take "hours to days". Estimable from patch size and files (HF has `patch`, `issue_categories`, `issue_specificity`) via a model calibrated on Verified / Multi-SWE-bench buckets.
- **Model results over time:** Scale leaderboard (public), with mixed harnesses:
  - GPT-4o-era models <5% (capped runs); Claude Sonnet 4 42.7; GPT-5 41.8; Sonnet 4.5 43.6; Opus 4.5 45.9; Gemini 3 Pro 43.3; Gemini 3.1 Pro 46.1; Opus 4.6 51.9; GPT-5.4 xHigh 59.1; **Muse Spark 1.1 61.5** (latest, mini-swe-agent harness).
  - Commercial set (paper): Opus 4.1 17.8%, GPT-5 15.7%.
  - The harness changed (50 to 250 turns; SWE-Agent to mini-swe-agent), so cross-time comparisons are confounded.
  - Unverified: OpenAI (Jul 2026) and Datacurve (May 2026) audits reportedly found broken tasks or mis-grading in the public split.
- **Item-level results:** trajectories linked per leaderboard entry (scaleapi GitHub).
- **Grading:** fail2pass + pass2pass unit tests, human-reviewed.
- **Time horizon already computed?** Not found.
- **Verdict: CANDIDATE.** It has the right difficulty range for 2026 models and is now the de facto replacement for Verified. Gap: no human times. Close it by imputing times from patch statistics, or by commissioning about 50 expert time estimates on public items.
- **Sources:** https://arxiv.org/html/2509.16941 ; https://labs.scale.com/leaderboard/swe_bench_pro_public ; https://scaleapi.github.io/SWE-bench_Pro-os ; HF datasets-server (fields and counts) ; https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/

## 8. SWE-bench Multimodal and SWE-bench Multilingual (SWE-bench team)

- **Paper/URL:**
  - Multimodal: arXiv 2410.03859 (Oct 2024); 619 JS front-end issues (510 test + 102 dev on HF), 17 repos, with screenshots.
  - Multilingual: 300 tasks in 9 languages (2025), on HF `SWE-bench/SWE-bench_Multilingual`.
- **Domain:** software. Multimodal covers UI and front-end bug fixing (e.g. a grommet Tab component bug), which resembles web-app maintenance.
- **Human times:** Multimodal annotators bucketed each task: <15 min 13%, 15–60 min 43%, 1–4 h 38%, >4 h 6%. That is much longer than Verified. **Per-instance labels are not in the HF dataset, and I could not find them released.** Multilingual: none.
- **Model results:**
  - Multimodal: 22 submissions in swe-bench/experiments (2024 to Nov 2025; GPT-4o 12% at launch, later GUIRepair, Refact).
  - Multilingual: 14 submissions to Sep 2026 (mini-SWE-agent: GPT-5.2, Kimi K2.5, Gemini 3.5 Flash ...).
- **Item-level results:** yes (swe-bench/experiments).
- **Grading:** unit tests, plus pixel tests for 69 Multimodal items.
- **Verdict: CANDIDATE (Multimodal).** It has per-item results and a longer time distribution. Gap: ask the SWE-bench team (Yang et al.) for the per-instance time labels. **Multilingual: EXCLUDE** (no times; subsumed by Multi-SWE-bench).
- **Sources:** https://arxiv.org/html/2410.03859 ; HF datasets-server ; GitHub API for swe-bench/experiments

## 9. MirrorCode (Epoch AI + METR)

- **URL:** https://epoch.ai/blog/mirrorcode (preliminary, 10 Apr 2026) ; https://epoch.ai/MirrorCode ; paper arXiv 2606.30182 ; https://github.com/epoch-research/MirrorCode. Maintainers: Epoch AI, co-developed and funded by METR.
- **Items:** 25 target CLI programs (22 open, 132 task instances across 6 languages). The agent must reimplement the program from execute-only access to the binary, with hidden end-to-end tests. Example: gotree, a 16.9k-line Go phylogenetics toolkit with 2,001 tests. The leaderboard uses 30 tasks (15 programs × 2 languages).
- **Domain:** software.
- **Resembles:** greenfield rebuilds and legacy reimplementation and migration ("rewrite this system"), at weeks-to-months scale.
- **Human times: rough expert estimates only.** For gotree, 4 people guessed between 1.5 and 17 weeks. One human baseline on a 2k-LoC task was unfinished after 20 h. Extrapolated lower bounds: over 6 days for gotree, over 25 days for Pkl.
- **Results:** gotree tests passed by Opus 4 (May 2025) 15%; Opus 4.1 24%; Opus 4.5 63%; Opus 4.6 99.95%. Opus 4.7 solved gotree in 14 h for $251. A leaderboard exists at epoch.ai/benchmarks/mirrorcode; I didn't extract its scores.
- **Item-level:** transcripts and code in epoch-research/MirrorCode-data.
- **Grading:** hidden end-to-end output-equivalence tests.
- **Time horizon:** none computed. The authors say horizons look much longer than METR's 12 h for Opus 4.6.
- **Verdict: CANDIDATE (long-tail anchor only).** It is the only SWE evidence above 16 h. Gaps: human times are guesses with wide spread; contamination (the original code is likely in pretraining); and the task type (black-box cloning) is atypical of client work.
- **Sources:** https://epoch.ai/blog/mirrorcode ; https://epoch.ai/MirrorCode ; https://metr.org/blog/2026-04-10-mirrorcode-preliminary-results/ ; https://jack-clark.net/2026/07/27/ (secondary)

## 10. SWE-Marathon

- **URL:** arXiv 2606.07682 (5 Jun 2026; NeurIPS 2026 poster). First author Rishi Desai; about 26 authors.
- **Items:** 20 project-scale tasks. Examples: Slack, Mastodon and Excel clones; a C compiler; a Java to Rust rewrite; JAX to PyTorch; a VLIW kernel optimisation.
- **Domain:** software.
- **Human times:** a secondary summary says expert estimates of **40–400 h**. I could not confirm the method in the abstract page.
- **Results:** 13 agent configurations. Best: Claude Opus 4.8 + Claude Code, then GPT-5.5 + Codex. All under 30% resolved.
- **Grading:** multi-layer verification (behavioural parity, performance gates, hidden-seed replay, integrity audits, agentic UI verifiers).
- **Item-level:** the authors say the benchmark, evaluation code and trajectories are released (URL not extracted).
- **Verdict: CANDIDATE.** It gives long-horizon anchors in product development. Gaps: confirm the per-task human-hour estimates in the PDF; only 20 items; a single time snapshot (no model-over-time series).
- **Sources:** https://www.alphaxiv.org/abs/2606.07682

## 11. Vibe Code Bench (Vals AI)

- **URL:** arXiv 2603.04601 (Mar 2026) ; https://vals.ai/benchmarks/vibe-code. Maintainer: Vals AI.
- **Items:** 100 web-app specifications written from a non-technical perspective (50 public, 50 held-out), checked by 964 browser workflows (10,131 substeps). Example: build a habit-tracker or parking-reservation app with Supabase, Stripe test mode and email.
- **Domain:** software (web development).
- **Resembles:** small-business app builds and agency web development. This is a common Indian IT/freelance gig.
- **Human times: none.** Only model wall-clock (up to 5 h) and API cost.
- **Results:**
  - v1 (Feb–Mar 2026): GPT-5.3-Codex 61.8% top; GPT-5.2 41.3%; Opus 4.6 36.1%.
  - v1.1 (2026): Opus 4.8 + Claude Code 77.5%; GLM-5.3 78.1% (BenchLM mirror, secondary).
  - Vals says v1 is saturated and archived.
- **Item-level:** trajectories and generated apps on GitHub (partial). Not all specs are confirmed public.
- **Grading:** a browser-use agent (Sonnet 4.5) plus an LLM judge per substep. A workflow passes if at least 90% of its substeps pass.
- **Verdict: CANDIDATE.** Strong realism for web development. Gaps: no human times (the specs could be priced by freelancers or estimated by experts), a short model series, and an LLM-judge grader.
- **Sources:** https://arxiv.org/html/2603.04601v1 ; https://vals.ai/benchmarks/vibe-code ; https://benchlm.ai/benchmarks/vibecodebench (secondary)

## 12. SWE-rebench (Nebius) and SWE-bench Live (Microsoft): contamination-free rolling issue sets

- **URL:** https://swe-rebench.com ; SWE-rebench V2 arXiv 2602.23866 ; HF `SWE-bench-Live/SWE-bench-Live`.
- **Items:** SWE-bench-style Python issues (and multilingual in V2) taken from recent PRs. SWE-rebench adds a monthly batch and evaluated about 30 models per month; it moved to larger batches in May 2026 (110 tasks covering Mar–May). There are 860 curated tasks on Harbor.
- **Human times: none.**
- **Results:** dated monthly leaderboards with a fixed scaffold. Ideal for a clean trend. Opus 4.6 reportedly 65.3% (Jul 2026); GPT-5.5 reportedly first in a later update (secondary).
- **Grading:** unit tests.
- **Verdict: CANDIDATE.** These are the best source of uncontaminated, harness-controlled scores over time. Gap: no human times. Impute with a time model trained on the Verified + Multi-SWE-bench buckets (same task format), or ask annotators to bucket one monthly batch.
- **Sources:** https://hub.harborframework.com/datasets/swe-rebench/swe-rebench-leaderboard/latest ; https://ai.engineer/talks/swe-rebench-lessons-from-evaluating-coding-agents-on-real-software-engineering-tasks-ibragim-bad ; https://aiweekly.co/alerts/swe-rebench-puts-gpt-55-first-on-clean-coding-leaderboard (secondary)

## 13. Code-review benchmarks: SWE-PRBench, c-CRAB, GitHub ReviewBench, LangChain ReviewBench, Martian Code Review Bench

- **What they are (2026):**
  - SWE-PRBench (arXiv 2603.26130, Mar 2026): 350 PRs with human review comments. Frontier models detect 15–31% of human-flagged issues.
  - c-CRAB (arXiv 2603.23448): test-based review tasks; existing agents solve about 40% combined.
  - GitHub/Microsoft ReviewBench (Oct 2026): 219 PRs, 187 repos, 19 languages. Copilot leads at 40.1% grounded F1.
  - LangChain ReviewBench (Jul 2026).
  - Martian Code Review Bench (Feb 2026): offline set plus an online developer-response tracker.
- **Domain:** software.
- **Resembles:** code review and QA. This is part of testing/QA work, and the PR-reviewer role is common in offshore delivery.
- **Human times:** none found.
- **Grading:** matching to human review comments (precision/recall/F1, LLM-matched) or tests.
- **Verdict: EXCLUDE for now.** No human times, mostly single-snapshot results, and F1-style scores rather than per-item pass/fail. Keep as a lead if code review becomes a separate O*NET task cluster.
- **Sources:** https://arxiv.org/html/2603.26130v1 ; https://arxiv.org/html/2603.23448v3 ; https://thenewstack.io/github-reviewbench-code-review/ ; https://langchain.com/blog/evaluating-code-review-agents-with-reviewbench

## 14. Feature/library generation and migration: FeatBench, Commit0, MigrationBench, FreshBrew, SWE-PolyBench

- **FeatBench** (arXiv 2509.22237, Sep 2025; Nanjing University): natural-language feature requests. Best was GPT-5 + Trae-agent at 29.9%, with frequent regressions.
- **Commit0** (ICLR 2025): build a Python library from spec plus tests. o1-preview reached 21% on lite. I found no 2026 updates.
- **MigrationBench** (AWS, KDD 2026): 5,102 Java 8 Maven repos (300 selected) to migrate to Java 17/21.
- **FreshBrew** (Oct 2025): 228 Java-migration projects with coverage-preservation guards.
- **SWE-PolyBench** (Amazon): 2,110 tasks in Java/JS/TS/Python with AST-complexity fields (`num_nodes`, `task_category`).
- **Human times:** none for any of them. SWE-PolyBench's AST fields could feed a time-imputation model.
- **Resemblance:** migration (Java upgrades) is very close to Indian IT modernisation contracts. Feature work is close to development.
- **Verdict: EXCLUDE** (no human times; thin model-over-time series). **MigrationBench/FreshBrew are the strongest leads if we ever impute times**, because "Java 8 to 17 upgrade" is a priced line item in IT services.
- **Sources:** https://arxiv.org/html/2509.22237v1 ; https://arxiv.org/html/2412.01769v1 ; https://arxiv.org/pdf/2505.09569 ; https://www.alphaxiv.org/overview/2510.04852 ; HF datasets-server for SWE-PolyBench fields

---

## Recommendation for the pipeline

1. **Anchor curve:** METR TH1.1 runs.jsonl (per-task minutes, 20 models, 2023–26).
2. **Ticket-style SWE curve:** SWE-bench Verified (500 items, 4 buckets, 182 dated submissions) plus Multi-SWE-bench (1,632 items, 2-rater buckets, Java/JS/TS/Go). Treat buckets as interval-censored times. Verified covers models up to about mid-2025. For 2026 models, use SWE-bench Pro or SWE-rebench with imputed times.
3. **Acceptance adjustment:** apply the Whitfill et al. merge-rate haircut (merge ≈ 0.5× of test-pass, golden-normalised gap 24 pp). Don't divide horizons by a constant 7. The 7x is Sonnet 4.5 alone; the ratio ranges from 2x to 20x.
4. **Realism check for IT services:** SWE-Lancer IC Diamond, with price as an ordinal time proxy.

## Leads I didn't chase

- METR's 2026 developer-productivity RCT follow-up. An Oct 2026 news headline says METR's latest trial "cannot show how much time agents save" (tuput.com, secondary). It might contain logged task times on real issues.
- arXiv 2610.12466, "On the estimation and validity of AI time horizons" (Oct 2026). Cross-cutting; for the time-horizon-infrastructure researcher.
- METR "Frontier Risk Report (Feb–Mar 2026)": https://metr.org/blog/2026-05-19-frontier-risk-report/ (Mythos 50% horizon 16–20 h; 80% horizon 3–4 h).
- Upwork **UpBench** (arXiv 2511.12306) and the **HAPI** index (322 jobs under $500, rubric-graded by freelancers). These are real jobs with prices; they belong to the occupational-suites researcher, but they include coding jobs.
- GSO / SWE-fficiency (performance-optimisation tasks, human expert commits as reference), SWE-Dev, NL2Repo, SWE-Compass, SWE-Evo, ABC-Bench: not checked.
- RE-Bench as a standalone ML-engineering curve: it is in TH1.1 with 8 h baselines; not re-researched.
- SWE-bench Multimodal per-instance time labels: email the SWE-bench team.
- The Datacurve audit of SWE-bench Pro grading (May 2026) is unverified. It matters if we use Pro.
- Terminal-Bench 2.0, OSWorld 2.0 (median 1.6 h human per task, Jun 2026) and BixBench3 are for the other researchers.
