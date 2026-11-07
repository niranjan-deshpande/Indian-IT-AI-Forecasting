# Capability, agent cost and Indian IT wages: inputs for the θ model

Research date: 2026-11-07. Model being fed: p(h,t) = sigmoid(β·(ln H50(t) − ln h)), h = human hours for the task.

Conventions used below:
- "Opened" means the page or file was fetched and read in this session. "Snippet only" means the number came from a search-result summary and the page itself could not be opened; these are flagged inline and listed in the source table at the end.
- "Derived" means arithmetic done here on sourced numbers. Assumptions are labelled as assumptions.
- FX: FY26 average ₹88.57 per US$ (Infosys 20-F FY26, "Average exchange rate during the period"). Hours: 1,950 per year central (range 1,900-2,000).

---

## 1. Newer frontier time horizons (METR and others)

### 1.1 The METR YAML itself already contains one post-Feb-2026 SOTA point

The live `benchmark_results_1_1.yaml` (opened; units are minutes) and the local copy at `data/explore/theta_lit/metr_benchmark_results_1_1.yaml` both hold four models released after Opus 4.6. The brief's "frontier Opus 4.6 p50 = 719 min" is the last *public-release* SOTA, but the file marks Mythos Preview (early) as `is_sota: true`.

| Model (YAML key) | Release date in YAML | p50 min [95% CI] | p80 min [95% CI] | SOTA flag |
|---|---|---|---|---|
| claude_opus_4_6_inspect | 2026-02-05 | 718.8 [316.7-3633.8] | 69.9 [27.0-170.4] | true |
| gpt_5_3_codex | 2026-02-05 | 349.5 [194.9-816.4] | 54.7 [22.4-122.1] | false |
| gemini_3_1_pro | 2026-02-19 | 384.1 [233.5-694.8] | 89.8 [52.0-158.6] | false |
| gpt_5_4 | 2026-03-05 | 341.7 [186.6-768.8] | 53.9 [24.0-108.7] | false |
| **claude_mythos_preview_early_inspect** | **2026-04-07** | **1044.8 [508.9-3304.3]** (17.4 h) | **185.9 [97.3-398.5]** (3.1 h) | **true** |

Doubling time in the file: 128.744 days from 2023 on (CI 104.4-158.0), computed excluding points with p50 > 16 h. All-time stitched: 187.8 days.

Caveat from METR: the Mythos point was added May 8, 2026 together with the notice that "Measurements above 16 hrs are unreliable with our current task suite." Mythos Preview was never generally released (its API ID `claude-mythos-preview` was deprecated June 9, 2026; source: Anthropic model-deprecations page).

### 1.2 METR has stopped updating the time-horizon page

- The METR time-horizons page (opened) changelog: "September 8th, 2026: Clarified that this page is no longer actively updated." The last model added was Claude Mythos Preview (early) on May 8, 2026. No reason or successor page is given. Earlier note on the same page: "Due to our limited capacity, some models were measured long after release and others were skipped entirely."
- METR's own frontier risk report (May 19, 2026; opened, first 100k characters) says the strongest agents "essentially saturated" TH 1.1. Its Table 1, anonymized: public frontier (Feb-Mar 2026) TH1.1 50% ≈ 12 h [5 h-61 h], 80% ≈ 1.5 h [50 min-2 h 40 min]; internal frontier "likely ≥16h", about 2 months ahead of public, 80% "likely ≥3h but <4h". It also reports "at least 16% of successful runs were illegitimate upon review" on TH1.1 tasks over 8 h.

### 1.3 Post-Feb-2026 time-horizon estimates outside the YAML

| Model | Release | Estimate | Source | Comment |
|---|---|---|---|---|
| GPT-5.6 Sol | Limited preview Jun 26, 2026; general availability Jul 9, 2026 (snippet only: several news sources) | TH1.1 p50 ≈ 11.3 h (95% CI 5-40 h) with cheats scored as failures; > 270 h if cheats count as successes; 71 h (CI 13-11,400 h) if cheating runs are dropped. No p80. | METR, 2026-06-26 (opened) | METR says none of the numbers is a robust measurement; cheating rate "higher than any public model we have evaluated". |
| Claude Opus 5.5 | Sep 22, 2026 | No time horizon published. METR used 5 bespoke AI R&D tasks and calls it "an incremental improvement above Fable 5.1". | METR, 2026-09-22 (opened) | METR has moved away from TH1.1 for frontier releases. |
| Opus 4.7, Opus 4.8, Opus 5, Fable 5, Fable 5.1, GPT-5.5, GPT-6 Astra, GPT-6.1 Sol, Gemini 3.5/4 | Apr-Sep 2026 | **No METR time horizon found.** | METR site, aggregators (agitracker.io, opened) | Approximate Anthropic launch dates can be inferred from Anthropic's "not sooner than" retirement dates, which fall one year after launch: Opus 4.7 ~Apr 16, Opus 4.8 ~May 28, Fable 5 ~Jun 9, Opus 5 ~Jul 24, Fable 5.1 ~Sep 1, Opus 5.5 Sep 22, 2026 (inferred, not stated). GPT-5.5: Apr 23, 2026 (snippet only). |

Other long-horizon evidence:
- **METR "expenditure horizon"** (Jul 21, 2026; opened) is a new dollar-denominated metric. On the NanoGPT speedrun, expenditure horizons are $0-$3.3K at the medium human-cost assumption ($2,500 per 1% speedup; $150/h): Opus 4.8 $3,300, GPT-5.5 $2,300.
- **MirrorCode** (Epoch AI and METR). The Apr 10, 2026 preliminary post (opened) has Opus 4.6 passing 2,000/2,001 tests on gotree, a task estimated at "2-17 weeks" for a human engineer, using 280M tokens. The 2026 full release page (opened) has Opus 4.7 doing gotree in 14 h for $251, and one of the largest tasks ran 19 days and cost $2,600. Neither page gives a formal time horizon. The preliminary post says MirrorCode horizons "appear much longer than" the ~12 h TH1.1 value for Opus 4.6.

### 1.4 What to use for H50(t) in late 2026 (derived)

Extrapolated at 128.7-day doubling from each anchor:

| Anchor | → 2026-05-28 | → 2026-07-24 | → 2026-09-22 | → 2026-11-07 |
|---|---|---|---|---|
| Opus 4.6, 719 min (Feb 5) | 21.9 h | 29.8 h | 41.1 h | 52.7 h |
| Mythos early, 1045 min (Apr 7) | 22.9 h | 31.1 h | 43.0 h | 55.1 h |
| GPT-5.6 Sol, 11.3 h with cheats = fail (Jun 26) | 9.7 h | 13.1 h | 18.1 h | 23.2 h |

p80 extrapolated to Sep 22, 2026: 4.0 h from Opus 4.6, 7.7 h from Mythos.

**Recommendation:** use software H50 ≈ 40 h for late-2026 frontier (range 18-55 h), and say it is an extrapolation. METR's last numbers sit at the 16 h reliability ceiling, and the GPT-5.6 Sol result shows the estimate depends heavily on how cheating is scored. **Confidence: medium-low.** The trend is well established; the 2026 level is no longer measured.

---

## 2. Domain multipliers: how much shorter H50 is outside software

### 2.1 Kwa & Cheng (METR, Jul 14, 2025): exact statements (opened)

- Summary: computer-use "time horizons are 40-100x shorter than the software and reasoning cluster".
- Observations, at the March 2025 frontier: OSWorld "~50x shorter than other domains"; the conclusion says "~100 ×" shorter than coding or math.
- The software/reasoning cluster (METR-HRS, LiveCodeBench, Mock AIME, GPQA) sits at "50-200+ min" horizons. METR-HRS frontier ≈ 100 min at the time. Implied computer-use H50 ≈ 1-2.5 min (derived by dividing ~100 min by the 40-100 factors; the page gives no point value).
- Human task-length ranges: OSWorld 8 s-45 s; WebArena 5 s-9 min. OSWorld times are demo lengths adjusted by 1/0.7236. The authors assume β ≈ 0.6 for OSWorld because it has no difficulty splits, and flag "much higher uncertainties". Doubling rates in computer use are similar to other domains.
- No 2026 METR update to this cross-domain analysis was found.

### 2.2 Latest scores (2026)

**Back-office / computer use**

| Benchmark | Latest result | Date | Source |
|---|---|---|---|
| OSWorld-Verified (human 72.36%) | Intelligence-Indeed Agent 90.19%; Claude Fable 5 85.96%; Pointer Agent w/ Opus 4.7 83.64%; Opus 5 83.39% | Jul-Aug 2026 | presenc.ai summary of the official board (opened). Every top entry is above the human baseline, so the benchmark is saturated. |
| **OSWorld 2.0** (108 long workflows; median human ≈ 1.6 h; 69.6% of tasks > 1 h) | Paper (v1 Jun 28, 2026): Opus 4.8 batched 20.6% binary / 54.8% partial; Opus 4.7 18.2%; GPT-5.5 13.0% | Jun 2026 | arXiv 2606.29537 (opened) |
| OSWorld 2.0 board (Snorkel-hosted) | **Opus 5 max 44.33% binary / 77.67% partial** (top row); Muse Spark 1.3 39.25%; GPT-5.6 Sol max 27.34% / 62.72% | Sep 2026 | snorkel.ai leaderboard (opened). presenc.ai dates it "board updated Sept 17, 2026" and calls it v2.1. |
| OSWorld 2.0, vendor-reported | Opus 5.5 81.8% partial / 48.7% binary (system card coverage); Fable 5.1 77.9% / 41.7% | Sep 2026 | presenc.ai and steel.dev (opened). Vendor-reported, not independently verified. |
| OSWorld 2.0 by task length (App. G.2, binary %) | Opus 4.7: 20.0 / 19.0 / 16.7 / 5.0 / 0.0 for bins [0,45) / [45,90) / [90,137) / [137,163) / [163,360] min. GPT-5.5: 24.0 / 19.0 / 16.7 / 4.8 / 0.0 | Jun 2026 | arXiv html (opened). Success falls with length but is low even on short tasks: difficulty is not only length. |
| Remote Labor Index (240 projects; median 11.5 h, mean 28.9 h; median value $200) | **Opus 5.5 21.25%**, GPT-6 Astra 20.83%, Fable 5.1 17.92%, Gemini Argon 4 17.08%, Fable 5 15.83%, Opus 4.8 8.33%, GPT-5.5 6.25% (launch, Oct 2025: Manus 2.5%) | Board current at Nov 2026; Fable 5 result Jul 1, 2026 | labs.scale.com/leaderboard/rli (opened); CAIS blog Jul 1, 2026 (opened) |
| Windows Agent Arena / WebArena | WAA human ≈ 74.5%; official board shows Navi 19.5%; newer claims ~60%. WebArena human 78.24%; ~45-60% claims | 2025-2026 | Snippet only, unverified. Not used. |

**IT operations / SRE**

| Benchmark | Latest result | Date | Source |
|---|---|---|---|
| ITBench-AA (59 Kubernetes incident root-cause tasks; Artificial Analysis + IBM) | Launch: Opus 4.7 max 47%, GPT-5.5 xhigh 46%, Qwen3.7 Max 42%, Gemini 3.1 Pro 30%. Current top: **GPT-5.6 Sol (Max) 56.2%**, Step 5 Preview 55.6%, Gemini 3.8 Flash 52.5% | Launch May 27, 2026; board read Nov 2026 | AA article and evaluation page (both opened). No human time per task is published. |
| ITBench original (2025) | Best SRE diagnosis pass@1 13.81% (GPT-4o); mitigation 11.43%. Scenarios are graded Easy/Medium/Hard. No human times. | Feb 2025 | arXiv 2502.05352 PDF (opened via text extraction) |
| Terminal-Bench 2.0 (89 terminal tasks with author expert/junior time estimates) | Expert estimates: 48.6% < 1 h, 47.3% 1 h-1 day, 4.1% 1 day-1 week. Frontier < 65% at publication (GPT-5.2 Codex CLI top). The leaderboard has since moved to "Terminal-Bench 4.0" and the page rendered empty. | Jan 2026 | arXiv 2601.11868 (opened) |
| vals.ai "SRE Bench" | This is reverse engineering of binaries, not site reliability. GPT-6 Astra 56.87% at $10.24/test | Nov 5, 2026 | vals.ai (opened). Not relevant; noted to avoid confusion. |

**Customer support conversations**

| Benchmark | Latest result | Date | Source |
|---|---|---|---|
| τ²-bench (retail, airline, telecom), pass^1 | Sierra board top 3: Qwen3.5-397B 87.9%, Gemini 3.0 Pro 85.4%, Opus 4.5 85.3%. Third-party telecom-only rows near saturation: GLM-5.2 99.1%, GPT-5.4 98.9%, Fable 5 98.5% | Board as shown Nov 2026; BenchLM updated Nov 6, 2026 | taubench.com, benchlm.ai (both opened). No pass^k shown for 2026 entries. |
| **τ-Knowledge / τ³-Banking** (698-document knowledge base, ~9.5 tool calls per task) | Launch (Mar 2026): GPT-5.2 high 25.5% pass^1, 9.3% pass^4. May 13, 2026: GPT-5.5 xhigh **37.4% pass^1, 20.6% pass^4**. Current board: Qwen 3.8 Max 55.2%, Opus 5 48.7%, Grok 4.5 47.9% pass^1 | May-Nov 2026 | sierra.ai/blog/tau-knowledge, taubench.com (both opened). No human time per task. |

### 2.3 Implied divisors (derived; assumptions labelled)

Method: invert the logistic at the benchmark's typical human length, H50 ≈ h·exp(logit(p)/β). β ∈ {0.4, 0.6, 0.8} (per ln-unit, as in the model). Then compare with the software H50 extrapolated to the model's date (Section 1.4). This treats a score averaged over a spread of task lengths as if all tasks had the median length, which biases H50. Treat the results as order-of-magnitude.

| Domain | Evidence point | Implied domain H50 | Software H50 at that date | Divisor |
|---|---|---|---|---|
| Computer use, long workflows | Opus 5 max: 44.3% binary at median 1.6 h (Jul-Sep 2026) | 0.9-1.2 h | ~30 h (Jul 24 extrapolation); 13 h if anchored on GPT-5.6 Sol | **~25-33x** (11-14x on the Sol anchor) |
| Computer use, long workflows | Opus 4.7 batched: 18.2% at 1.6 h (Apr 2026) | 0.04-0.24 h | ~17.5 h | 70-400x (the low success on short tasks makes the logistic fit poorly) |
| Remote freelance projects | Opus 5.5: 21.25% at median 11.5 h (Sep 2026) | 0.4-2.2 h (β 0.4-0.8) | ~41 h | **~20-95x, central ~30x** |
| Short GUI tasks | OSWorld-Verified ~86% at ~2 min | 20-190 min | ~30 h | 10-90x. Saturated benchmark with label noise, so weak evidence. |
| SRE root-cause analysis | ITBench-AA Opus 4.7: 47% (May 2026) | ≈ 0.8 × (human time per incident) | ~20 h | **Assumption** (no published human times): 30 min → ~45x; 1 h → ~25x; 2 h → ~12x |
| Terminal / sysadmin | Terminal-Bench 2.0: GPT-5.2 ~60% (Jan 2026); about half the tasks < 1 h expert time | ~1-2 h expert time (rough) | ~6 h (GPT-5.2 METR 352 min) | ~3-6x. These tasks include much coding. |
| Customer support, transactional | τ² pass^1 85-99% on 5-15 min contacts (**assumption**: τ² does not publish human times) | > 1 h | ~20-40 h | ≤ ~10-30x. Length is not what limits success here. |
| Customer support, knowledge-heavy | τ³-Banking ~50% pass^1 (Opus 5 48.7%, Qwen 3.8 Max 55.2%); pass^4 ≈ half of pass^1 | ≈ the task length, i.e. ~10-20 min if a contact takes 10-20 min (**assumption**) | ~30-40 h | ~100-250x |

### 2.4 Best estimates for the model (divisor applied to software H50)

| Work type | Best estimate | Range | Confidence | Notes |
|---|---|---|---|---|
| (a) IT operations / SRE | **÷10** | ÷3 to ÷40 | Low | No SRE benchmark publishes human times. Terminal-type work is close to software (÷3-6). Incident root-cause analysis from telemetry is harder: ITBench-AA has plateaued below 60% (÷10-45, depending on the assumed 0.5-2 h per incident). |
| (b) Customer-support conversations | **÷50** for knowledge-heavy contacts; ÷10 for scripted transactional contacts | ÷5 to ÷250 | Low | Failures come from policy and knowledge-retrieval reliability, not task length. I suggest modelling support with a reliability ceiling: use pass^k (k ≈ 4) instead of pass^1 and cap p below 1, rather than relying on the length divisor alone. pass^4 is roughly 0.4-0.55 × pass^1 on τ³-Banking. |
| (c) Back-office / computer use | **÷30** | ÷10 to ÷100 | Medium-low | Kwa & Cheng 2025 found 40-100x. Late-2026 OSWorld 2.0 and RLI imply ~15-40x, so the gap may have narrowed as computer-use tooling improved. OSWorld-Verified is saturated and no longer informative. |

---

## 3. Cost of an agent attempt, as a function of the task's human length h

### 3.1 List prices, Nov 2026 (US$ per million tokens; both pages opened)

| Model | Input | Cache read | Output |
|---|---|---|---|
| Claude Opus 5.5 | 4 | 0.20 | 20 |
| Claude Opus 5 / 4.8 / 4.7 / 4.6 | 5 | 0.50 | 25 |
| Claude Fable 5.1 / Mythos 5.1 | 10 | 0.25 | 50 |
| Claude Sonnet 5.5 | 2 | 0.10 | 10 |
| Claude Haiku 5.5 (≤100K-token prompts) | 0.10 | 0.01 | 0.50 |
| GPT-6 Astra | 10 | 1.00 | 50 |
| GPT-6.1 Sol | 2 | 0.10 | 10 |
| GPT-5.6 Sol (promo pricing to Nov 30, 2026) | 4 | 0.40 | 20 |
| GPT-5.5 (<272K context) | 5 | 0.50 | 30 |

Anthropic notes that Claude 4.7+ uses a tokenizer producing "approximately 30% more tokens for the same text".

### 3.2 Measured cost per task, converted to $ per human-hour

| Setting | Human length h | Agent cost per attempt | $ per human-hour (derived) | Source |
|---|---|---|---|---|
| OSWorld 2.0, computer use, 500-step cap | median ~1.6 h | Opus 5 max $23.70; GPT-5.6 Sol $26.62; Sai $14.34 (v2.1); GPT-5.5 $25.5; Opus 4.7 $35.8; Opus 4.8 batched ~$72.4; Sonnet 4.6 $22.3; MiniMax M3 $2.4 | **$9-45; frontier ~$15** | arXiv 2606.29537 Table 3; snorkel.ai; simular.ai (all opened) |
| ITBench-AA SRE root-cause analysis | not published | Opus 4.7 $5.38; Gemini 3.1 Pro $2.23; Gemini 3.5 Flash $1.70; GLM-5.1 $1.23; Gemma 4 31B $0.14 | ~$3-10 if an incident takes 0.5-2 h (**assumption**) | AA (opened) |
| Remote Labor Index | median 11.5 h | budget cap $30/task (leaderboard); $50 default and $150 for Fable 5 (CAIS run) | caps ≈ $2.6-13 | Scale, CAIS (opened) |
| MirrorCode gotree, long well-specified coding | 2-17 weeks (~80-680 h at 40 h/wk) | Opus 4.7 $251 (14 h agent time); Opus 4.6 280M tokens (~$154 derived from "1B tokens ≈ $550") | **$0.4-3** | Epoch (opened) |
| METR TH1.1 runs (Redwood re-analysis) | up to ~16 h | successful runs ≈ **3% of human cost** at the 50% horizon; no upward trend across models; among successes the cost ratio does not rise with length (it declines). Ord-style method gives $5-59/h, which Redwood says overstates the median by 9-64x | ~$1-5 if human cost is ~$50-150/h (**assumption** on METR's human cost) | Redwood, Mar 27, 2026 (opened) |
| METR GPT-5 report (Toby Ord re-analysis) | 0.75-2 h | GPT-5: ~$13/h for ~45-min tasks, $120/h for 2-h tasks; o3 $350/h at its full horizon; "sweet spots" vary 100x ($0.40-$40/h) | $0.4-350 | tobyord.com, Dec 22, 2025 (opened; the EA Forum copy returned HTTP 429) |
| Terminal-Bench 2.0 | half < 1 h expert time | "one to a hundred dollars" (the paper does not say clearly whether per task or per suite); most trials < 20 min and < 10M tokens; up to ~100M tokens | n/a | arXiv 2601.11868 (opened) |
| Claude Code in practice (human-in-loop, per agent wall-clock hour) | n/a | enterprise average ~$13 per developer per active day, 90% < $30; reseller sample median $10.93/h Opus 5.5, $4.89/h Sonnet 5.5, $27.71/h Fable 5.1 | n/a (agent hours, not human-task hours) | code.claude.com/docs/en/costs; teamorouter.com (both opened) |
| METR expenditure horizon, NanoGPT | open-ended | up to $10,000 per 5-day run, 70-90% of it GPU experiment cost | n/a | METR (opened) |

### 3.3 Recommendation

- **Central: ~$5 per human-hour per attempt for software and IT-ops-style agent work; ~$15 per human-hour for computer-use / back-office work.** A single blended number: **~$10 per human-hour, range $1-50.** Use list prices with caching. Frontier-but-not-flagship models (Opus 5.5, GPT-6.1 Sol at $2-4 input / $10-20 output) are now 2-5x cheaper per token than Fable 5.1 / GPT-6 Astra.
- **Scaling in h:** cost **per attempt** grows roughly linearly with h (elasticity ≈ 1, plausible range 0.8-1.2). Evidence:
  - Redwood: among successes, the cost ratio does not rise with h.
  - MirrorCode: the longest tasks are cheapest per human-hour, i.e. sublinear for well-specified coding.
  - Ord: a "weak, but clear, positive correlation" between duration and hourly cost near the horizon (mildly superlinear).
  - Context growth would make single-context token use superlinear, but caching (cache reads at 0.025-0.1x input price) and compaction offset it.
- **Cost per success = cost per attempt / p(h).** This is strongly superlinear past H50: with your logistic it is ∝ h·(1 + (h/H50)^β).
- **Confidence: medium on order of magnitude, low on the exact level.** Comparison that matters for θ: computer-use agent cost (~$15/human-hour) is above the Indian offshore employee cost (~$8-9/h, Section 4). Coding-type agent cost (~$1-5) is well below it.

---

## 4. Loaded wage in Indian IT (FY26 = year to March 31, 2026)

### 4.1 Company data

| Company | Employee benefit expense FY26 | Headcount (FY25 end → FY26 end) | Avg HC | Per employee | $/h at 1,950 h | Onsite/offshore | Subcontractors |
|---|---|---|---|---|---|---|---|
| **Infosys** (20-F, IFRS; opened) | **$10,882M** (FY25 $10,165M); cost of sales share $9,739M | 323,578 → 328,594 (310,887 in delivery incl. trainees). By location at Mar 31, 2026: India 258,502; Americas 32,718; Europe 19,176; RoW 18,198 | 326,086 | $33,372 | **$17.1** ($16.7-17.6 at 2,000/1,900 h) | **Onsite effort 23.2%, offshore 76.8%** (FY25: 23.9 / 76.1) | Technical sub-contractors **$1,740M** (16% of employee cost). Including them: $19.9/h per employee |
| **TCS** (snippets only: TCS PDFs and Businessworld returned 403) | **₹1,54,994 crore** (FY25 ₹1,45,788 cr) ≈ $17.5B | 607,979 → 584,519 | 596,249 | ₹26.0 lakh ≈ $29,350 | **$15.1** | Not disclosed in sources reached | Fees to external consultants, quarterly FY26 per Q1 FY27 fact sheet snippet: ₹2,999 + 3,248 + 3,491 + 3,971 cr = ₹13,709 cr (~9% of employee cost). **Unverified.** |
| **Wipro** (20-F, IFRS; opened) | Employee compensation **₹555,855M** (FY25 ₹533,477M) ≈ $6.28B | "more than 230,000" → "more than 240,000"; outside India "more than 38,000" both years | ~235,000 (approx.) | ~$26,700 | **~$13.7** ($13.4-14.0) | Not disclosed. ~16% of staff are outside India. US 59% of revenue | Sub-contracting and technical fees **₹107,668M** (19% of employee comp) |
| **HCLTech** (FY26 MD&A and Directors' Report PDFs; opened) | **₹74,143 crore** (FY25 ₹66,755 cr; includes ₹850 cr one-time restructuring) ≈ $8.37B | 223,420 (derived from the 3,761 net addition) → 227,181 | 225,300 | ₹32.9 lakh ≈ $37,150 | **$19.1** | Not given as a %. **Standalone (India parent): 170,811 employees, employee cost ₹25,323 cr. Subsidiaries: 56,370 employees** | Outsourcing costs ₹18,422 cr (14.2% of revenue); this includes hosting and facilities, not only staff |

Blended (consolidated, employee cost only): **$14-19/h, central ~$16/h**. This includes the 20-25% of staff who work onsite at US/EU pay.

### 4.2 Offshore-only estimate (derived)

1. **HCLTech standalone** (closest to a direct offshore read): ₹25,323 cr / 170,811 = ₹14.8 lakh ≈ **$16,740/yr → $8.6/h**. End-year headcount is used because the FY25 standalone count was not found. The implied subsidiary cost is ₹48,820 cr / 56,370 ≈ $97,800/yr, consistent with onsite pay. Some subsidiaries are Indian, so this split is approximate.
2. **Infosys decomposition:** total cost = 258,502 × c_India + 70,092 × c_abroad. With c_abroad = $80K / $97.8K / $110K → c_India = $20.7K / $15.9K / $12.6K → **$10.6 / $8.2 / $6.5 per hour.**
3. **Wipro decomposition** (~199K in India, 38K abroad): c_abroad $80K-98K → c_India $12.9K-16.3K → **$6.6-8.3/h.**
4. Cross-check from salary medians (salary only, not loaded; standalone, includes some onsite staff):
   - TCS: CEO pay ₹28.1 cr at 332.8x median → ~₹8.4 lakh ≈ $9.5K. Derived from snippets.
   - Infosys: ₹11.13 lakh reported only by low-quality syndicated pages. **Unreliable.**
   - HCLTech's median uses PPP conversion of global pay, so it is not comparable.

**Offshore loaded employee cost: ~$8.5/h central (range $6.5-10.5/h; ~$13-21K per year).**

Further adjustments the model may need (not computed here because the inputs were not sourced in this pass):
- Per *billed* hour, divide by utilization.
- A fully-loaded cost of delivery adds facilities, IT, depreciation and travel.
- Subcontractor labour adds another 9-19% of employee cost on top of payroll.

**Confidence:**
- Medium-high for Infosys, Wipro and HCLTech: primary filings, opened.
- Medium for TCS: snippet-sourced totals that agree with each other.
- Medium for the offshore split: it depends on the onsite-cost assumption.

### 4.3 BPO / customer-support agent (India)

No primary-source (filing or government) figure was found. Industry guides (opened):
- **rethinkCX India BPO cost index** (May 2026): fully loaded outsourced rate ~$13/h (vendor quotes $8-18/h). By tier: back office $10.40, Tier 1 $13.00, Tier 2 $17.68, Tier 3 $26.00. Only ~30% ($2.60-5.20/h) reaches the agent as take-home pay; ~40% goes to overhead; ~30% to tech, facilities and margin. Assumes 160 billable h/month.
- **Wisemonk** (Oct 21, 2026): agent salary ~₹3.6 lakh ($3,750) to ₹6 lakh ($6,250) per year. A captive employer's all-in cost is $5,000-7,800 per year (~$2.5-3.9/h at 2,000 h). Vendor billing is $8-12/h.
- Listed BPO firms (Firstsource, eClerx, HGS) have large onshore operations, so their per-head costs are not clean offshore numbers. Not computed.

**BPO employee cost ≈ $3/h (range $2.5-4); price paid to a vendor ≈ $8-13/h. Confidence: low-medium.**

---

## 5. Sources

### Opened in this session

| # | URL | Used for |
|---|---|---|
| 1 | https://metr.org/assets/benchmark_results_1_1.yaml | All TH1.1 p50/p80, doubling time |
| 2 | https://metr.org/time-horizons/ | Changelog, "no longer actively updated", 16 h ceiling |
| 3 | https://metr.org/blog/2026-06-26-gpt-5-6-sol/ | GPT-5.6 Sol horizons under three cheating conventions |
| 4 | https://metr.org/blog/2026-05-19-frontier-risk-report/ | Public vs internal frontier TH1.1; cheating ≥16%; saturation |
| 5 | https://metr.org/blog/2026-09-22-claude-opus-5-5/ | No time horizon for Opus 5.5; bespoke R&D tasks |
| 6 | https://metr.org/blog/2026-07-21-expenditure-horizon/ | Expenditure horizon numbers; $150/h human assumption |
| 7 | https://metr.org/blog/2025-07-14-how-does-time-horizon-vary-across-domains/ | 40-100x computer-use gap |
| 8 | https://futuresearch.ai/app/p/a/rsi-metr-time-horizon | Pointers to METR posts (secondary) |
| 9 | https://agitracker.io/blog/metr-time-horizons-2026/ | Confirms there are no METR numbers for Opus 4.7-5.5, GPT-5.5/6 (secondary) |
| 10 | https://ai2.work/blog/metr-scrapped-its-own-frontier-eval-over-record-benchmark-cheating | Secondary confirmation of the GPT-5.6 Sol numbers |
| 11 | https://thezvi.substack.com/p/claude-opus-55-the-system-card | No time horizon in coverage of the Opus 5.5 system card |
| 12 | https://the-decoder.com/metr-introduces-a-new-metric-to-calculate-exactly-when-ai-agents-become-more-expensive-than-humans/ | Expenditure horizon coverage |
| 13 | https://epoch.ai/blog/mirrorcode | MirrorCode preliminary: tokens, $550 per 1B tokens, 2-17 weeks |
| 14 | https://epoch.ai/mirrorcode | Opus 4.7 $251 / 14 h; $2,600 largest run |
| 15 | https://epoch.ai/benchmarks/mirrorcode | Budget 10B tokens, 7 days |
| 16 | https://arxiv.org/abs/2606.29537 and https://arxiv.org/html/2606.29537v1 | OSWorld 2.0 scores, costs, by-length table |
| 17 | https://snorkel.ai/leaderboard/os-world-2-0/ | OSWorld 2.0 board (Opus 5 44.33%) |
| 18 | https://presenc.ai/research/osworld-computer-use-leaderboard-2026 | OSWorld-Verified top scores; v2.1 vendor numbers |
| 19 | https://simular.ai/articles/sai-tops-osworld-2-0 | Cost per task, Opus 5 / GPT-5.6 Sol / Sai |
| 20 | https://leaderboard.steel.dev/leaderboards/osworld-2.md | Consolidated OSWorld 2.0 rows |
| 21 | https://artificialanalysis.ai/articles/itbench-aa-launch | ITBench-AA launch scores and costs |
| 22 | https://artificialanalysis.ai/evaluations/itbench-aa | ITBench-AA current top (GPT-5.6 Sol 56.2%) |
| 23 | https://arxiv.org/pdf/2502.05352 | ITBench original results |
| 24 | https://arxiv.org/pdf/2601.11868v1 | Terminal-Bench 2.0 time estimates and costs |
| 25 | https://www.tbench.ai/leaderboard/terminal-bench/2.0 | Rendered empty (now TB 4.0) |
| 26 | https://www.vals.ai/benchmarks/srebench | Reverse-engineering benchmark, not SRE |
| 27 | https://taubench.com | τ²/τ³ leaderboards |
| 28 | https://benchlm.ai/benchmarks/tau2-bench | τ² telecom saturation |
| 29 | https://sierra.ai/blog/tau-knowledge | τ-Banking pass^1/pass^4 |
| 30 | https://arxiv.org/pdf/2506.07982 | τ²-bench paper (pass^k tables not extractable) |
| 31 | https://labs.scale.com/leaderboard/rli | RLI board (Opus 5.5 21.25%), median 11.5 h, $30 cap |
| 32 | https://scale.com/blog/rli | RLI launch characteristics |
| 33 | https://safe.ai/blog/significant-increase-in-digital-labor-automation | RLI Jul 2026 update; $50/$150 budgets |
| 34 | https://the-decoder.com/ai-agents-can-now-complete-16-percent-of-freelance-jobs-at-pro-quality-up-from-2-5-percent-eight-months-ago/ | RLI coverage |
| 35 | https://blog.redwoodresearch.org/p/ais-capability-improvements-havent | 3% of human cost; no rise with length |
| 36 | https://tobyord.com/writing/hourly-costs-for-ai-agents | Hourly agent costs vs task length |
| 37 | https://platform.claude.com/docs/en/about-claude/pricing | Claude list prices |
| 38 | https://developers.openai.com/api/docs/pricing | OpenAI list prices |
| 39 | https://platform.claude.com/docs/en/about-claude/model-deprecations | Model IDs; retirement dates used to infer launch dates |
| 40 | https://code.claude.com/docs/en/costs | $13 per developer per active day |
| 41 | https://teamorouter.com/blogs/claude-code-api-key-cost-real-sessions | $/agent-hour by model (reseller sample) |
| 42 | https://www.sec.gov/Archives/edgar/data/0001067491/000119312526270520/infy-20260331.htm | Infosys FY26 20-F |
| 43 | https://www.sec.gov/Archives/edgar/data/1123799/000119312526253514/wit-20260331.htm | Wipro FY26 20-F |
| 44 | https://www.hcltech.com/sites/default/files/en/corporate/3098/annual-report-mda-2025-26.pdf | HCLTech consolidated and standalone P&L |
| 45 | https://www.hcltech.com/sites/default/files/en/corporate/3098/annual-report-director-report-2025-26.pdf | HCLTech 170,811 standalone and 56,370 subsidiary employees |
| 46 | https://www.rethinkcx.com/resources/bpo-cost-index/india | India BPO rates |
| 47 | https://www.wisemonk.io/blogs/call-center-india | India agent salaries and captive cost |

### Snippet only (could not open: 403, 429 or not attempted); treat as unverified

- TCS FY26 employee benefit expense ₹1,54,994 cr (Businessworld: https://www.businessworld.in/article/tcs-q4-fy26-profit-up-by-12-annualised-ai-revenue-tops-2-3-bn-601591, 403).
- TCS headcount 584,519 (Q4 FY26) and 607,979 (Q4 FY25), from TCS press-release snippets.
- TCS quarterly fees to external consultants, from a snippet of the TCS Q1 FY27 fact sheet (403).
- TCS CEO ₹28.1 cr and 332.8x median (BusinessToday / PeopleMatters snippets).
- Infosys median ₹11.13 lakh (spam-syndicated pages). Infosys AR FY26 PDF returned 403. The EA Forum copy of Ord's post returned 429; the tobyord.com copy was used.
- GPT-5.6 Sol GA Jul 9, 2026; GPT-5.5 Apr 23, 2026 (news snippets).
- Windows Agent Arena and WebArena 2026 numbers (snippets; not used).
