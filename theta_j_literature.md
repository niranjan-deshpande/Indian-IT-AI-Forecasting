# Estimating θ_j: what the literature gives you, what it doesn't, and what to do next

*Literature report for the SPAR project on AI and employment in Indian IT services and BPO. Written 26 Oct 2026. It is built only from the verified literature digest, three gap reviews (measurement, skeptic, context), the idea list and the judge's scores. No new research was done for this report.*

**How to read this.** Section 1 gives the answer in one paragraph and a table of where each parameter currently comes from. Sections 2–7 go through the literature, and each ends with a "For θ_j" line. Section 8 ranks the gaps. Section 9 ranks what you could do and gives a draft "dataset requirement and recipe" for Andrei. Section 10 lists sources.

**Notation (reader-facing).**
- θ_j: the fraction of labour time saved on service line j at full adoption with current AI. It is net of failures, human review and AI running cost.
- p(h,t): the chance AI output passes checks on a task that takes a human h hours, with models available at date t.
- q: the share of passing output a reviewer would actually accept.
- ρ: review time as a share of h.
- κ: the speedup when AI is used as an assistant rather than given the task outright.
- f_j(h): the hours-weighted distribution of task lengths in service line j.
- w_j: service line j's share of labour time.
- Draft formula: θ_j(t) = ∫ max{ q·p(h,t)·(1−κ) + κ − ρ, κ } f_j(h) dh, and S(t) = Σ_j w_j θ_j(t).

**Economics terms used below, in plain words.**
- **Extensive vs intensive margin.** Extensive: *can* AI touch this task at all (yes/no). Intensive: *how much* labour it removes when it does. ML analogy: extensive is "is this task in the model's distribution?", intensive is "what is the net score once you count the human's time?"
- **Pass-through (φ) and price elasticity of demand (ε).** φ is how much of a cost saving the vendor passes to the client as lower prices. ε is how much more work clients buy when prices fall. Together they decide whether time saved becomes fewer jobs.
- **Reduced form.** An outcome that mixes several mechanisms. For example, a fall in employment mixes θ, adoption and demand response, with no way to separate them without more assumptions.
- **Difference-in-differences (DiD), event study, synthetic control.** Ways of comparing treated and untreated groups before and after a change. Think of them as A/B tests where nature, not you, assigned treatment, so you have to argue the groups would otherwise have moved together.
- **ITT vs LATE (or IV/2SLS).** ITT (intent-to-treat) is the effect of being *offered* the tool, including people who never use it. LATE is the effect on people who actually use it. Random assignment is used as an "instrument" to back this out.
- **Hulten's theorem.** To first order, the economy-wide productivity gain equals the sum over tasks of (the task's share of GDP) × (its cost saving). This is the macro version of S = Σ w_j θ_j.
- **TFP vs labour productivity.** TFP is output per unit of *all* inputs. Labour productivity is output per hour. They differ by a factor of roughly 1/(labour share), so check units before comparing.
- **CES and elasticity of substitution.** How easily one task can stand in for another. If tasks are complements (low elasticity), making one cheap mostly makes the others the bottleneck (the "Baumol" effect).
- **Throughput to labour saved.** If output per hour rises by g, labour per unit of output falls by 1 − 1/(1+g). So +26% completed tasks is about 21% labour saved, not 26%.
- **Statistical shorthand.** pp = percentage points. SD = standard deviation; SE = standard error; CI = 95% confidence interval; n.s. = not statistically significant. "g" (Hedges' g) is a difference in means divided by the pooled SD. "Log points": a change of −0.349 in a log outcome is about a 30% fall (e^−0.349 − 1).
- **Industry shorthand.** PR = pull request (a proposed code change). AMS = application maintenance and support. UAT = user acceptance testing (the client's sign-off). GCC = a client's own offshore "global capability centre". Lightcast and Revelio are commercial job-postings and LinkedIn-based workforce datasets.

---

## 1. Bottom line

The literature gives you most of the *ingredients* for θ_j but no finished *dish*. You get the following:
- A well-measured capability curve p(h,t) for software tasks. METR's time horizons are a logistic in log task length. Frontier 50% horizons are about 6–12 hours as of spring 2026, doubling roughly every 129 days since 2023.
- One rough number for q: about 0.5. Maintainers would not merge about half of SWE-bench-passing PRs.
- A handful of anchors for ρ, roughly 0.1–0.33 of task time. They come from GDPval grading time, a 4-PR fix-time estimate, and screen-recording shares.
- κ estimates that are almost all from 2020–24 assistant tools. They range from −19% for experts on their own code to about +20% for development work.
- Worked examples of net savings. The clearest is GDPval, where GPT-5's 90× raw speedup falls to 1.12–1.39× (about 11–28% of time saved) once review and redo are counted.

It does *not* give you:
- hours-weighted task-length distributions f_j(h), or hours weights w_j, for any Indian service line;
- ρ as a function of task length;
- q for agents that iterate on enterprise or client code;
- any capability curve for testing, IT operations or BPO work with human time baselines;
- any study that measures p, q, ρ and κ together on one set of tasks, by length, as capability rises.

On the working hypothesis, the honest verdict is "half right". It is right about the *exposure* literature. Eloundou et al. and its descendants label whether AI can cut a task's time by ≥50%. Those labels are beliefs that were never checked against measured times, and no exposure index nets out review or failure. But the skeptic review refuted the broad version, "nobody measures the intensive margin". Many studies measure it, with different degrees of netting:
- RCTs, from Noy-Zhang's 37–40% saving on writing to METR's 19% slowdown;
- Anthropic's usage data, about 80% saved gross, with success adjustment cutting the implied gain by about a third to 45% (1.8 to 1.2 or 1.0 pp/yr);
- GDPval's review-and-redo workflow;
- surveys, about 3% of hours saved in Denmark and about 0.35 hours saved per AI-assisted hour in the US.

What survives is narrower and still important: no one measures labour saved *net of review and failure, by task length, indexed to capability, for IT-services or BPO task mixes*. The judge also found a structural point that may matter more than any missing number. If q is a flat multiplier, the delegate branch can never exceed q(1−κ)+κ−ρ. That is about 0.28 at q = 0.5, κ = 0.1, ρ = 0.27, however capable models get. If instead q is a "horizon shift" (reviewer standards make tasks effectively ~7× longer), the cap rises to 1−ρ. So how you model q is a first-order decision for Andrei, not a detail.

**Where each parameter comes from today**

| Parameter | Plain meaning | Best current source | Best number to use now | Main weakness |
|---|---|---|---|---|
| p(h,t) | Chance AI output passes checks on a task of human length h | METR time horizons (Kwa et al. 2025; Time Horizon 1.1 data files) | Logistic in log h. Frontier p50 ≈ 6–12 h (Opus 4.6: 719 min; Gemini 3.1 Pro: 384 min); p80 ≈ 1–3 h. Doubling ≈ 129 days (95% CI 104–158) since 2023. Slope ≈ 0.6–0.95 per log unit (our derivation) | Software only; h is low-context contractor time; the 80%+ tail is poorly identified; unreliable above 16 h; computer-use horizons are 40–100× shorter |
| q | Share of passing output a reviewer accepts | Whitfill, Wu, Becker, Rush (METR, Mar 2026) | ≈ 0.5 (one-shot). Alternatively, treat it as shifting the horizon down ~7× (Sonnet 4.5: 50 min under the grader vs 8 min under maintainers) | 3 Python repos, 4 reviewers, no iteration, models up to Sonnet 4.5/GPT-5 |
| ρ | Review time as a share of h | GDPval (109 of 404 min); Rein (METR 2025); METR RCT; CUPS | Range 0.1–0.33; GDPval's 0.27 is the best single figure | No ρ-vs-h curve; GDPval is grading time; Rein is n = 4 estimated fixes |
| κ | Speedup from AI as assistant | Cui et al. (field RCTs), Google RCT, METR RCTs, Brynjolfsson-Li-Raymond | Development ≈ 0.15–0.25 (2022–24 tools); experts on familiar code −0.19 in early 2025, now uncertain; chat support ≈ 0.08–0.13 | Old tools or mixed modes; late-2025 RCT broken by selection |
| f_j(h) | Hours-weighted task-length distribution per service line | No Indian data. Proxies: SWE-bench Verified buckets, JOSSE/public Jira effort logs, Anthropic Economic Index task times, RLI | SWE-bench Verified: 39% < 15 min, 52% 15–60 min, 8% 1–4 h (count-weighted, optimistic) | Open-source/US/freelance; counts not hours; often LLM- or annotator-estimated |
| w_j | Service line's share of labour hours | Firm service-line revenue splits already in the project repo | Use intervals from revenue shares converted to hours; add a non-task bucket w_0 | Revenue ≠ hours (onsite rates ≈ 3× offshore at Infosys); detailed splits end 2017–19 |

---

## 2. Exposure measures

**What these measure.** Exposure indices score tasks or occupations on whether AI is *relevant* to them. They are the economics equivalent of asking "is this task in-distribution?", not "what is the net score?". Almost all are single snapshots built on the US O*NET task list.

**Eloundou, Manning, Mishkin, Rock (arXiv 2023; Science 384:1306–1308, 2024).** This is the canonical measure. Each of 19,265 O*NET tasks gets a label:
- **E0:** no meaningful time saving.
- **E1:** ChatGPT access could cut time by at least 50% at quality the recipient would not notice or care about.
- **E2:** it would take software built on the LLM to get there.

The labellers were OpenAI alignment reviewers, not workers in those occupations, plus an early GPT-4 using a tuned rubric. GPT-4 agreed with humans 66–82% of the time depending on the measure. Occupation-level means (Table 3):
- α (E1 share): 0.14;
- β (E1 + ½E2): 0.30 human / 0.34 GPT-4;
- ζ (E1 + E2): 0.46 human / 0.55 GPT-4.

The text rounds these up to "over 30%" and "surpasses 50%", but the human ζ is below 0.50. Headline: 80% of US workers are in occupations with ≥10% of tasks exposed, and 19% with >50%. These are shares of *tasks*, not time saved or jobs lost.

Why this is not θ:
- E1 is a threshold: 1{believed saving ≥ 50%}. If the labels were accurate, E1 tasks would have θ ≥ 0.5. But the labels are beliefs about *potential, gross* savings and were never checked against measured times.
- The authors chose a high threshold because they expected real-world savings to be lower.
- Task weights are core/supplemental counts, not hours. There is no task-length dimension.
- Nothing is netted out for review, rejection or AI cost.

**Other exposure indices, all ordinal.**
- **Felten, Raj, Seamans (AIOE; SMJ 2021, and a 2023 language-model version).** Crowd ratings link 10 AI applications to 52 O*NET abilities. The language-model reweighting correlates 0.979 with the original, so the index hardly moves when capabilities change.
- **Webb (2019).** Text overlap between patents and task descriptions. Its useful feature is method: it *validates* exposure against historical employment changes, which is the same kind of check as comparing a bottom-up S(t) with the top-down 2.3 pp/yr.
- **Brynjolfsson, Mitchell, Rock (AEA P&P 2018, "suitability for machine learning").** About 2,059 work activities rated on a 5-point scale by about 10 raters each (from the author's 2020 slides; the rating platform and the rubric item count, 21 vs 23, could not be confirmed from the paper). Some rubric items (tolerance for error, verifiability of output) are close in spirit to q and ρ.

**Continuous scores: closer, but still not θ.**
- **ILO Working Paper 140 (Gmyrek et al., May 2025).** Scores 29,753 tasks from 0 to 1 for "could be done without a human operator", using three LLMs, a survey of 1,640 Polish workers and expert rounds. Selected ISCO-08 means: software developers (2512) 0.53; web and multimedia developers (2513) 0.60; applications programmers (2514) 0.57; database designers (2521) 0.57; systems administrators (2522) 0.57. The ILO calls these an "upper threshold" of exposure. They are perceived automatability, with nothing netted for review. India's NCO-2015 classification is aligned with ISCO-08. But public PLFS microdata appear to record occupation at only 3 digits, so these occupations cannot be separated in PLFS (from search results, not opened; unverified).
- **Eisfeldt, Schubert, Zhang ("Generative AI and Firm Values", NBER WP 31222, revised Jan 2026).** Re-applies the Eloundou rubric with GPT-3.5 (14% of tasks directly exposed) and rolls it up to firms by their occupation mix. It separates exposure through *core* tasks (likely substitution) from *supplemental* tasks (likely complementarity). A long-short "artificial-minus-human" portfolio earned about 5% in the two weeks after ChatGPT's release.
- **Tomlinson et al. (Microsoft, "Working with AI", arXiv 2507.07935).** 200k US Bing Copilot conversations from 2024, mapped to O*NET activities. Completion rates range from 0.55 to 0.99 across occupations. Applicability correlates 0.73 with Eloundou at the occupation level. All programming falls into one activity, so it cannot separate maintenance from testing from development. The repo says the metrics "should not be misconstrued … as measuring the ability of AI to replace jobs."
- **Massenkoff & McCrory (Anthropic, "observed exposure", Mar 2026).** Combine Eloundou's β with actual Claude usage. For computer and math tasks, observed coverage is 33% against a theoretical 94%. The gap is mostly adoption, which θ deliberately excludes. Automated use gets weight 1 and augmented use 0.5, but those weights are assumed, not estimated.

**Two papers that show the gap between "exposed" and "worth automating".**
- **Svanberg et al. (MIT FutureTech, Jan 2024).** For computer-vision tasks, only 23% of the wages paid for exposed tasks would be cost-effective to automate at today's costs. A bare-bones firm-level implementation reaches 49%. A single national "AI-as-a-service" system would reach 88%.
- **Hatgis-Kessell, Aguirre, Wan, Bommasani (arXiv 2608.05172, 2026).** Weighting exposure by *time spent* rather than *number of tasks* reshuffles 11 of the 25 occupations commonly reported as most exposed, moving the top of the list from clerical toward analytical roles. This is a lesson about w_j: the choice of weights changes the answer.

**The offshoring precedent.** The 2005–13 offshoring literature asked "which jobs could a cheaper remote supplier do?", which has the same structure as asking which jobs AI could do.
- **Blinder (2007)** hand-ranked 284 US occupations (533 others were placed as a block in the least-offshorable category). He found 22–29% of 2004 US employment "potentially offshorable". He warned that the index is ordinal, not a probability, and not a forecast. Software engineers score 74 of 100, not the top.
- **Blinder & Krueger (2009/2013)** found about a quarter of US jobs offshorable. Their three preferred measures agree only 70–80% of the time, and offshorability is unrelated to wages or layoff risk.
- **Jensen & Kletzer (2005)** classed 100% of US computer and mathematical employment as tradable.
- **van Welsum and Reif**, as summarised by Reinsdorf & Slaughter (2009), put 18–20% of OECD employment as potentially offshorable.

The lesson carries over: in Blinder & Krueger's survey, offshorability was not related to layoff risk, and Blinder himself warned his index was not a forecast. That is consistent with, though it does not prove, the view that exposure scores do not identify θ now. The completeness critic also flagged Autor, Levy & Murnane (2003, QJE), the founding paper of the task approach (NBER WP 8337, https://www.nber.org/papers/w8337), as a classic missing from the streams.

**For θ_j:** exposure measures can give you an extensive-margin mask (which tasks have θ > 0 at all) and a rough ordering across occupations. ILO's continuous scores are at most a loose upper bound on *gross* θ. None of them gives p, q, ρ or κ, and none gives hours weights. Best use: a cross-check on the ordering of θ_j across service lines.

---

## 3. Experiments

A note on units before the numbers. Some studies report *time per task*. Others report *output per worker* (pull requests, resolutions per hour). Convert output gains with θ = 1 − 1/(1+g) before comparing. Most of these experiments test AI as an **assistant**, which is the κ branch of the formula, not delegation.

### 3a. Outside coding

| Study | Setting | Result | What it means for θ |
|---|---|---|---|
| Noy & Zhang (2023; Science) | ~27-min professional writing tasks, ChatGPT (GPT-3.5 era) | Time −37% (working paper; Science version −40%), quality +0.45 SD | Near-delegation on short, low-stakes tasks: 68% *said* they submitted the first output unedited. Graders could not fact-check, so ρ is understated. Treat as an upper anchor for short tasks |
| Brynjolfsson, Li, Raymond (QJE 2025) | 5,172 chat-support agents, mostly in the Philippines, 2020–21 GPT assistant, staggered rollout | Resolutions/hour +15%; handle time −8.5%; less-skilled and less-experienced agents +30% (the 2023 NBER version says 14% and 34%); top agents ≈ 0 | Assistant-mode θ for BPO chat ≈ 8–13%. Agents followed suggestions 35–38% of the time |
| Ni et al. (Alibaba, arXiv 2603.29888) | 5,940 *new* agents (<1 yr tenure), randomised, Qwen assistant at chat opening | At full use: diagnosis step −32%, whole chat only −4.2% | Saving on a sub-step × that step's share of task time. Small κ for short (~8-min) chats |
| Dell'Acqua et al. (BCG, Org. Science 2026) | 758 consultants, GPT-4 | Inside the AI's "frontier": 22.5–27.6% less time, >40% higher quality. Outside it: correctness −19 pp | θ varies sharply between tasks of similar apparent difficulty. Errors become harder to spot |
| Dell'Acqua et al. (P&G "Cybernetic Teammate", NBER 2025) | 776 professionals, product innovation | Time −13 to −16%; one person with AI matched a two-person team's quality | The headcount reading is an inference; staffing was not measured |
| Schwarcz et al. ("AI-Powered Lawyering", 2025) | 153 law students enrolled, 127 completed; six legal tasks, o1-preview and a retrieval tool | Average time −19 to −21%; the NDA drafting task (with a template) showed no saving | Similar time savings to an earlier GPT-4 study, with higher quality. Weak cross-study hint that better models may buy quality rather than time |
| Merali (arXiv 2409.02391; 2512.21316) | 300 translators and 13 LLMs; >500 consultants/analysts and 13 LLMs | +12.3% speed per 10× training compute; about −8% task time per year of model progress; agentic tasks gain less | Among the works checked, the only within-design randomisation over model capability (the 2025 follow-up was read at abstract level only). Gives an empirical slope for θ(t) |
| Lukac et al. (NEJM AI 2025) | 238 UCLA physicians, AI scribes | Nabla: time in notes −9.5% ITT (DAX −1.7%, n.s.), but scribes used in only ~30% of visits | The saving *per use* is likely much larger. Not θ at full adoption |
| Dillon et al. (Microsoft 365 Copilot, 66 firms) | 7,137 workers | Email time −12% ITT, −17% among users (~2 h/week of an 11.7 h baseline); no change in meetings or Word | Shows how w_j × θ_j shrinks a big task-level number to ~5% of the week |
| Otis et al. (Kenya, Mgmt Sci 2026) | 640 small-business owners, GPT-4 advisor | Zero average effect cannot be ruled out; low performers did ~10% worse | Value depends on which suggestions users pick, a q-type problem |
| Agarwal, Moehring, Rajpurkar, Salz (NBER 31422) | 227 radiologists | AI predictions: no average accuracy gain even though AI beat ~¾ of radiologists; active time +4% | κ can be ≤ 0. Given biased updating, optimal routing is AI alone *or* human alone |
| Vaccaro, Almaatouq, Malone (Nat. Hum. Behav. 2024) | Meta-analysis, 106 experiments | Human+AI vs the better of the two alone: g = −0.23; worse (g = −0.54) when AI is the stronger party; creation tasks g = +0.19 (n.s.) | Adding a human in the loop often hurts when AI is better. Outcomes are quality, not time |

### 3b. Coding

| Study | Setting | Result | What it means for θ |
|---|---|---|---|
| Peng et al. (2023) | Upwork freelancers, mostly India/Pakistan; one greenfield task with tests (2022 Copilot) | 55.8% less time (95% CI 21–89%) | Upper-bound κ for a short, test-checked new-code task. Self-estimates (35%) were *below* the measured gain |
| Cui et al. (Mgmt Sci) | Field RCTs at Microsoft, Accenture (SE Asia, n = 320) and a Fortune 100 firm; 4,867 developers | Completed tasks +26% (SE 10.3%) ⇒ ~21% labour saved per task; juniors gain more | Best field κ for 2022–23 autocomplete. Coding is only part of the job (the w_j point) |
| Paradis et al. (Google RCT, ICSE 2025) | 96 engineers, "extend existing code" task (mid-2024) | ~21% faster, CI includes zero | κ ≈ 0.2 for modification work |
| Becker, Rush, Barnes, Rein (METR, 2025) | 16 expert maintainers, 246 tasks of ~2 h on their own large repos; Cursor + Claude 3.5/3.7 | Time **+19%** (CI +2 to +39%); developers *believed* −20% | Net effect of allowing AI can be negative for experts on familiar code. Mixes assist and delegate. Self-reports can get the sign wrong |
| METR update (Feb 2026) | 57 developers, 800+ tasks, late-2025 tools | Speedups of 18% (returning developers, CI −9% to 38%) and 4% (new recruits, CI −9% to 15%). METR writes these as −18% and −4%, where negative means faster. Both intervals include zero, and METR calls the data unreliable and a lower bound | Probably positive now, size unknown. 30–50% of developers withheld tasks they would not do without AI, so per-task RCTs are breaking down |
| Murphy-Hill et al. (Microsoft, arXiv 2607.01418) | Tens of thousands of engineers, Claude Code and Copilot CLI, Jan–Apr 2026; synthetic control | Merged PRs per engineer +24% (CI 14.5–33.7%) ⇒ ~19% labour per PR; heavy-use weeks +50% (association only) | The largest agentic field evidence. Not randomised; no quality measures |
| He et al. (CMU Cursor study, MSR '26) | 806 adopting open-source repos | Velocity gains fade after two months; complexity about +9% beyond what codebase growth explains (headline +42%) | Gross speedups are partly repaid later as maintenance cost |
| Denisov-Blanch (Stanford talk, 2025; not peer-reviewed) | 136 teams | Greenfield-simple +31%, brownfield-complex +7%; niche languages (COBOL) ≈ 0–5% | Prior ordering: θ_maintenance < θ_development. Thin support for the legacy-stack result |
| Huang et al. (Anthropic internal, Dec 2025) | 132 staff survey, 200k transcripts | Claude used in ~59% of work; more than half can *fully delegate* only 0–20%; 27% of AI-assisted work would not otherwise exist | Rough split of the assist share vs the delegate share. "New work" means throughput gains are not all labour saved |
| Mozannar et al. (RealHumanEval, arXiv 2404.02806) | 243 mostly students, short Python tasks | Stronger benchmark models save more time, but far less than one-for-one; acceptance rates do not track productivity | The mapping from capability to κ is real but noisy |
| DORA 2024/2025 (Google's DevOps Research and Assessment survey) | ~5,000 respondents (2025) | AI adoption is positively related to throughput but negatively to stability | System bottlenecks (testing, review) limit flow-through. Correlational |

**For θ_j:** this section mainly informs **κ**.
- Development, assistant mode, 2022–24 tools: κ ≈ 0.15–0.25.
- Maintenance by experts on familiar code: −0.19 in early 2025, sign now uncertain.
- BPO chat with an assistant: ≈ 0.04–0.13.
- Short writing: ≈ 0.37–0.40.

The best *field* number for agentic delegation is about 19% labour saved per merged PR (Microsoft 2026), which is not randomised. Do not use self-reports for any parameter.

---

## 4. From benchmarks to labour saved

This is the section closest to the draft formula. It goes parameter by parameter, then looks at studies that combine them.

### 4.1 p(h,t): the capability curve

- **Kwa et al. (METR, arXiv 2503.14499).** For 170 software/ML/cyber tasks, METR times skilled humans and runs agents several times. It then fits success against log(human time) for each model and reads off the length at which success is 50% (and 80%). The 50% horizon doubled about every 7 months over 2019–25 (207 days). For Claude 3.7 Sonnet, "around 50 minutes".
- **Caveat on h.** Contractor baseliners took 5–18× longer than repository maintainers on internal PRs. METR's h is *low-context outsider time*.
- **Time Horizon 1.1 (METR, Jan 2026; public YAML files).**
  - A bigger suite: 228 tasks, 31 of them ≥ 8 h, but only 5 of those human-baselined.
  - Doubling since 2023: 128.7 days (CI 104–158).
  - Frontier p50 / p80: Claude Opus 4.6 719 / 70 min; Gemini 3.1 Pro 384 / 90 min; GPT-5.2 352 / 66 min.
  - Claude Mythos Preview: 1,045 min, above METR's 16-hour reliability limit, and excluded from the trend fit.
  - The ratio of p50 to p80 is 4–6× for 18 of 26 models (full range 2.3–10.3×). That implies a shallow slope of roughly 0.6–0.95 per natural-log unit of h (our own derivation). With a 12 h p50, a model still fails roughly 9–18% of 1 h tasks.
  - The dashboard was frozen in September 2026.
- **Barry (METR, Mar 2026).** Reasonable alternative fits cut recent 50% horizons by up to 35% and raise 80% horizons by up to 100%. Noise in task lengths makes curves look shallower. A single slope shared across models cross-validated best. On private tasks only, Opus 4.6's p50 falls 40%, from 12 h to 7.2 h.
- **Ord (arXiv 2505.05115).** An alternative "constant hazard" curve (each minute of work carries a fixed chance of failure). It implies T99 ≈ T50/70. A logistic with typical slopes implies about T50/200 (our derivation). Curve shape changes the reliability tail by about 3×.
- **Kwa (METR, Jan 2026).** "A 50% time horizon of X hours does not mean we can delegate tasks under X hours to AIs." Converting horizons into speedups needs data on time spent "prompting AIs, waiting for generations, checking AI output", which METR does not have.
- **Kwa & Cheng (METR, Jul 2025).** Visual computer-use horizons (OSWorld, WebArena) are 40–100× shorter than software horizons. That is the nearest proxy for BPO and IT-operations work.
- **Other benchmarks.**
  - HCAST: 189 tasks, 563 human baselines.
  - SWE-bench Verified: per Epoch, 39% of tasks < 15 min, 52% 15–60 min, 8% 1–4 h (annotator estimates).
  - TheAgentCompany: best agent 30% full completion on 175 simulated company tasks. No human times.
  - AI 2027 / AI Futures forecasts: full distributions over future horizon paths, useful as a template for scenario bands.
- **Usage-based analogue.** The January 2026 Anthropic report finds that API success falls from about 60% on sub-hour tasks to about 45% at 5+ hours, crossing 50% near 3.5 h. Both success and time are judged by Claude, and the tasks are ones users chose to bring.

### 4.2 q: does a reviewer accept passing output?

- **Whitfill, Wu, Becker, Rush (METR, Mar 2026).** Four maintainers (scikit-learn, Sphinx, pytest) reviewed 296 agent PRs that passed SWE-bench Verified tests. Models ranged from Claude 3.5 Sonnet to GPT-5 and Sonnet 4.5.
  - The maintainers re-approved only 68% of the *real merged human* patches, which is the noise baseline.
  - After normalising to that baseline, grader pass rates exceed merge rates by 24.2 pp (SE 2.7). Raw gap: 34.9 pp.
  - Headline: roughly half of passing PRs would not be merged.
  - Sonnet 4.5's horizon is about 50 min under the grader and about 8 min under maintainers, roughly 7×. This suggests q is better modelled as a horizon shift (q depends on h) than as a flat multiplier.
  - Merge rates improve 9.6 pp/yr more slowly than grader scores (SE 5.5, only 10% significant). With state-of-the-art models only, the gap is 4.1 pp/yr (SE 12.1), not significant.
  - Agents could not iterate on feedback, so 0.5 is pessimistic for real workflows.
- **Deployment merge rates** (not conditioned on passing tests, and shaped by what people choose to delegate):
  - Nakashima et al. (arXiv 2602.04226): agent PRs merged 55–86% vs 82.6% for humans.
  - Pinna et al.: docs 82.1%, features 66.1%.
  - Watanabe et al.: Claude Code PRs merged 83.8% vs 91.0% for matched human PRs. Agent PRs add twice the lines (median 48 vs 24). About 45% of merged agent PRs were revised before merge, *but so were ~41.5% of human PRs*, with similar effort.
  - The public AIDev dataset (Li, Zhang, Hassan; v5 has 7.69M agent PRs) makes q(size, month) estimable.
- **Assistant-mode acceptance:** Copilot suggestions about 34% (CUPS); Cursor generations under 44% (METR RCT). These mix p and q.

### 4.3 ρ: what does review cost?

- **GDPval (OpenAI, arXiv 2510.04374).** On 220 open "gold" tasks, expert graders took 109 min (monitored) against 404 min of expert completion time, so ρ ≈ 0.27. The paper reports two different task-length statistics (404 min average expert time in Appendix A.2.1; a 9.49 h mean, 5.0 h median, in Table 3), so depending on which denominator you use ρ is about 0.19–0.27. This is grading time in an evaluation, not production review.
- **Rein (METR, Aug 2025).** 0 of 15 agent PRs on real repos were mergeable as-is. Estimated fix time was about 26 min for the 4 test-passing PRs and about 42 min for all reviewed PRs, against tasks averaging 1.3 h. So fixes cost roughly 1/3 to 1/2 of h. Tiny sample, estimated rather than timed. This argues for replacing a binary q with a "fix-up fraction", since passing-but-unmergeable work still saves time.
- **METR 2025 RCT screen recordings.** About 9% of AI-allowed time went to reviewing and cleaning AI output and about 4% to waiting, on 44 issues. 75% of developers say they read every line.
- **CUPS (Mozannar, Bansal, Fourney, Horvitz, CHI 2024).** 21 Microsoft programmers in ~12-min Copilot sessions spent 22.4% of session time verifying suggestions and 34.3% verifying plus editing. True verification time per suggestion is about 5× the naive estimate, because people accept first and check later.
- **Human code-review baselines.**
  - Google (Sadowski et al. 2018), from logs: reviewers spend a mean of 3.2 h/week reviewing about 4 changes/week, with a median change of 24 lines. That is roughly 45–50 reviewer-minutes per change, or about 30 lines/hour.
  - Inspection norms of 200–500 lines/hour (Kemerer & Paulk on classroom self-review; SmartBear, a vendor) are far faster. So for small changes, a *fixed cost per change* probably dominates. Model ρ as fixed-per-change plus per-line, not as a constant share of h.
  - Google's ML review-edit blog adds about 60 min of author "shepherding" time per change.
  - Czerwonka et al.'s often-quoted "6 h/week" is a cited self-report survey, not a Microsoft measurement.
  - Only 14–15% of review comments concern defects (Bacchelli & Bird 2013; Czerwonka et al. 2015). Passing review is a weak test of correctness.
- **Elapsed-time evidence (latency, not effort).** Faros telemetry: review time per PR +91% on high-adoption teams in 2025, and no significant company-level improvement. Cihan et al.: adding an AI *reviewer* raised average PR closure time from 5.9 h to 8.3 h (before/after, no control).
- **Non-code work.** The only evidence is a self-report survey on "workslop" (BetterUp/Stanford, HBR 2025): 40% of 1,150 US desk workers received low-quality AI work in the past month, costing about 2 h per incident.

### 4.4 Reviewer behaviour and routing

- **Over-reliance.**
  - Buçinca et al.: on the key sub-decision, 48–64% of wrong AI answers were followed.
  - Vasconcelos et al.: over-reliance rises with task difficulty and falls with higher stakes and cheaper verification.
  - Bansal et al.: explanations raise acceptance whether or not the AI is right.
  - Perry et al. (CCS '23): AI users wrote less secure code while believing it more secure (3% vs 21% secure signing solutions).
  - Lee et al. (CHI '25): higher confidence in AI is associated with less self-reported critical thinking (cross-sectional).
  - Implication: q and ρ are chosen together. A reviewer can trade checking time for false acceptances.
- **Theory of verification.**
  - Huang, Xiao, Vishnoi (ICML 2026): workers choose how much to delegate and how hard to verify. There are three regimes (manual; pure delegation; verified delegation), and weak verifiers over-delegate. Missed errors cost *quality*, not time.
  - Catalini, Hui, Wu (arXiv 2602.20946): a falling cost of automating races against a cost of verifying that is bounded by human time.
- **Routing per task instance.** The formula averages p over all tasks of length h before taking the max. If success is *predictable* task by task, routing each instance separately does better, because the average of a max is at least the max of the averages. Raghu et al. (2019) found a zero-error slice of 35–44% of cases on an adjudicated eye-disease set, but only 10–24% on a noisier holdout. That is an oracle bound, and nobody has measured this predictability for coding or IT tickets. Relevant estimators include learning to defer (Mozannar & Sontag, ICML 2020), selective classification (Geifman & El-Yaniv, NIPS 2017), and LLM routers (RouteLLM, ICLR 2025; confidence tokens, Chuang et al., ICML 2025). Lykouris & Weng model review as a congestible queue.

### 4.5 Putting it together: worked net-savings examples

- **GDPval's workflow** is the closest published analogue to the delegate branch. Try the model, have an expert review it, accept with probability equal to the win rate (a q·p stand-in), and otherwise redo by hand.
  - GPT-5 (39% strict win rate): 90× faster naively, 1.12× trying once, 1.39× trying up to n times. That is about 11% and 28% time saved.
  - GPT-4o: 0.46× under try-n, i.e. slower than doing the task yourself.
  - The collapse comes mostly from redoing the ~61% of failures, not from review alone.
  - There is no assistant (κ) branch, and figures are for OpenAI models only.
- **SWE-Lancer (OpenAI 2025).** 1,488 real Upwork tasks worth $1M; Claude 3.5 Sonnet earned $403k. A model-first, freelancer-fallback scheme saves 9–34%, but it assumes verification is free; the authors note it "can take over 24 hours".
- **Remote Labor Index (CAIS/Scale).** 240 real freelance projects (median 11.5 h, mean 28.9 h). The best agent's client-acceptance rate was 2.5% at publication in Oct 2025. The live leaderboard shows about 21% for the best model in Oct 2026, with no confidence intervals and a mostly creative/media task mix.

**For θ_j:** use **p** from METR TH1.1 with a single shared slope, and report at least two curve shapes. Set **q ≈ 0.5**, or model it as a ~7× horizon shift; this choice drives the result. Set **ρ ≈ 0.1–0.33**, preferably as fixed-per-change plus a per-line part. Report the fallback rule (redo with assistance / full redo / retry) as an explicit choice. Use GDPval's try-n result, about 28% saved, as a reality check for multi-hour knowledge tasks.

---

## 5. Usage and adoption data

**Anthropic Economic Index (data on Hugging Face, Anthropic/EconomicIndex; releases from Feb 2025 to Jun 2026).**
- **Handa et al. (Feb 2025).** Pure extensive margin: which O*NET tasks show up in Claude.ai chats. Computer and math tasks were 37.2% of queries. 57% of conversations were augmentation, 43% automation.
- **Software development (Apr 2025).** 79% of Claude Code conversations are automation vs 49% on Claude.ai. Agentic tools shift work from assisting toward delegating.
- **Sept 2025.** First-party API traffic is 77% automation. "Context" is offered as a *possible* bottleneck for enterprise deployment.
- **Tamkin & McCrory (Nov 2025).** Claude estimates, for 100,000 conversations, how long a professional would take without AI and how long the task took with it. The median time saving is "about 80%" (84% in the text, 81% in a figure caption) on tasks averaging about 90 min (1.4 h elsewhere). Implied US labour productivity growth is +1.8%/yr at universal adoption; the authors say this is not a forecast. This is **gross**: it excludes validation outside the chat, failures and rejection. It is also selected on tasks people chose to bring to AI. Validated on 1,000 open-source JIRA tickets: Claude's Spearman correlation with actual times is 0.44, against 0.50 for developers' own estimates, and its estimates are compressed (short tasks too long, long tasks too short).
- **"Economic primitives" (Jan 2026).** Claude-judged task success is 67% on Claude.ai and 49% on the API. API success falls with human task length, crossing 50% near 3.5 h. Weighting time savings by success cuts the implied gain from 1.8 to 1.2 pp/yr (Claude.ai) or 1.0 pp/yr (API). With tasks as complements (CES elasticity 0.5), it falls further, to 0.6–0.8 pp/yr. This is the closest usage-based analogue to multiplying by p. There is still no ρ or q term.
- **Mar 2026 ("learning curves").** Users with 6+ months' tenure succeed about 3–5 pp more often, so q and p partly depend on the user, not only the model. Success and time fields are still in the data.
- **Jun 2026 ("Cadences").** Monthly time means continue (human-alone time in hours, with-AI time in minutes), but task success is dropped. Claude Code is 0.37 points more autonomous (on a 1–5 scale) than chat.
- **Data caveat.** Per-task files give means, medians and confidence intervals for human-alone and with-AI time. They are *not* task-level histograms, and units are unstated in the Jan 2026 documentation. So f_j(h) cannot be read off directly.

**OpenAI, "How People Use ChatGPT" (Chatterji et al., NBER 34255).** On consumer plans, non-work use grew to over 70%. Messages split into Asking 49%, Doing 40%, Expressing 11%. Programming is 4.2% of messages. No time or success measures.

**Surveys of time saved.**
- **Bick, Blandin, Deming** (Real-Time Population Survey; Mgmt Sci 2026; FRED series RPSGENAITSALL).
  - Time saved as a share of *all* US work hours (non-users count as zero) rose from 1.41% (2024Q4) to 2.17% (2026Q2), then 2.08% (2026Q3).
  - Hours assisted rose from 4.1% to 6.3%, then fell to 5.3%.
  - Hours saved per assisted hour, using matched quarters, stayed around **0.31–0.39** (0.34 in 2024Q4, 0.35 in 2026Q2), roughly flat (our arithmetic from the FRED series). The St. Louis Fed's own point figure, "33% more productive in each hour" of use, is consistent with this.
  - In Nov 2024, previous-week users saved 5.4% of their hours, and computer/math occupations saved 2.5% of all their hours.
  - The answers are bracketed and top-coded at 4+ hours, and gross of review, so the flat ratio is suggestive only.
- **Humlum & Vestergaard** (Denmark, about 25,000 workers per survey round in 11 occupations including software developers and IT support).
  - Users save 2.8% of hours (6–7% on days they use chatbots).
  - Effects on earnings and recorded hours are precisely zero (ruling out more than 1% in the 2025 version, more than 2% in the 2026 revision).
  - About 80% of saved time is reallocated to other tasks, and only 3–7% passes through to earnings.
  - This is the clearest bridge between RCT-sized task effects and small realised effects. The gaps are infrequent use, limited applicability within jobs, and weak employer coordination.
- **Adoption measures disagree.** About 18% of US *firms* use AI (Census BTOS), versus 78% of the labour force working at adopting firms (Atlanta Fed survey), per Allen's FEDS Note (Apr 2026). Any top-down back-out of θ (θ ≈ realised replacement ÷ adoption) is very sensitive to which adoption measure is used. For large Indian IT firms, employment-weighted measures are the relevant ones.

**For θ_j:** usage data give a *gross* intensive margin (~80% within the chat) and a usage-based p(h) curve (50% near 3.5 h on the API) for cross-checking METR. They supply no ρ or q. Surveys give realised, adoption-weighted savings (~3% of hours; ~0.35 saved per assisted hour), which bound realised savings, not θ. They are needed later to reconcile θ with the 2.3 pp/yr, through an adoption term.

---

## 6. Aggregation models (and task theory)

**The Hulten skeleton.** Most macro estimates compute (share of the economy's tasks AI affects) × (average cost saving on those tasks) (Hulten 1978). The spread across papers comes mostly from the first factor. The second factor, the intensive margin, is **plugged in from a few early experiments, held constant, and not derived from capability**.
- **Acemoglu ("The Simple Macroeconomics of AI", Economic Policy 2025).** Exposure 20% (wage-bill-weighted, from Eloundou) × 23% profitable to automate (borrowed from Svanberg's computer-vision study) = 4.6% of tasks affected. Labour cost saving 27% (the average of Noy-Zhang and Brynjolfsson et al.) × labour share 0.535 = 14.4% total cost saving. TFP gain ≤ 0.66% over 10 years (≈ 0.064%/yr), or < 0.53% with "hard" tasks at a 7% saving. Adding Peng et al. raises the saving to 36% and TFP to 0.89%. (The April 2024 draft gives 0.71%.) Structurally this is S = Σ w_j × 1{exposed} × feasibility × saving, exactly the product the recipe wants to replace with a capability-based θ_j(t).
- **Aghion & Bunel (2024).** Same formula with wider inputs: exposure 18.5–68%, profitable share 0.23–0.8 tied to falling compute costs, saving 27–40%. Range 0.07–1.24 pp/yr; median 0.68 pp/yr of TFP. The intensive input moves the result by under 1.5×, while exposure and profitability move it by more than 10×.
- **OECD (Filippucci et al., IPM 2025).** A flat 30% micro gain that *explicitly excludes coding studies*. US TFP +0.3 to 0.7 pp/yr.
- **Penn Wharton (Arnon 2025).** Saving of 25%, *assumed* to rise to 40%. TFP level +1.5% by 2035.
- **Goldman Sachs (Briggs, Kodnani; Briggs, Dong).** "Just under 1.5 pp/yr" of *labour* productivity growth, about 1 pp of TFP, and 6–7% of workers displaced (unverified: primary reports not opened, figures from press coverage).
- **Anthropic (Tamkin-McCrory; Jan 2026).** Among the macro estimates reviewed, the only one that estimates per-task savings from (model-estimated) usage data, and then adjusts for success. Still no ρ or q.

**Caveats for a simple sum.**
- **Baqaee & Farhi (Econometrica 2019).** Hulten is only first-order. With large shocks, the weights w_j themselves shift (the Baumol effect), so S computed with today's w_j can mislead. Report a first-order S and a reweighted S.
- **Gans & Goldfarb ("O-Ring Automation", NBER 2026).** When tasks are quality complements, freed time goes to bottleneck tasks. Exposure indices that add task-level risk linearly overstate displacement.
- **Demirer, Horton, Immorlica, Lucier, Shahidi ("Chaining Tasks", NBER 2026).** AI succeeds on step i with probability α^{d_i} (α = AI quality, d_i = step difficulty). Chains of steps are verified once at the end, with retry until success. Neighbouring steps matter: an AI-executed adjacent step raises a step's chance of being executed by AI by 4–11 pp. The theory stream judged it the most usable 2026 model. It derives expected labour time as a function of a capability index *net of verification*, with review cost **per verified chunk**, not proportional to h. Its failure rule (retry and re-verify) differs from the draft's (human redoes with κ assistance), which gives different θ for the same p. It has not been calibrated to METR horizons or IT data.

**Growth models (all-or-nothing automation per task).**
- **GATE (Erdil, Potlogea, Besiroglu et al., arXiv 2503.04941).** Andrei co-wrote this. The automated share of tasks rises log-linearly with effective compute between two thresholds, and a CES across tasks creates bottlenecks.
- **Erdil & Besiroglu** and **Korinek & Suh** are related growth models. Korinek & Suh's spread of task complexity is the analogue of f_j(h), with an automation frontier moving through it.
- The project's integral is effectively a *partial-automation* version of GATE's automation function.

**Task-based labour theory.**
- **Acemoglu & Restrepo (AER 2018; JEP 2019; Econometrica 2022).** Three forces: displacement, productivity (cheaper output raises demand, the ε·φ channel) and reinstatement (new tasks). θ is binary per task there. Their 2022 paper finds 50–70% of changes in the US wage structure since 1980 are explained by task displacement.
- **Autor, Chin, Salomons, Seegmiller (QJE 2024).** Most current US jobs are in job titles introduced after 1940, so w_j cannot be held fixed over long horizons.
- **Autor & Thompson ("Expertise", JEEA 2025).** Removing *inexpert* tasks raises wages and cuts employment; removing *expert* tasks does the reverse. The same θ_j can have opposite employment effects depending on which tasks inside j go.
- **Grossman & Rossi-Hansberg (AER 2008).** A structural template: tasks ordered by handoff cost, a threshold, and a saving that integrates a per-task penalty. Its "productivity effect" warns that savings can *raise* demand for the workers who remain.
- **Garicano (JPE 2000) and Ide & Talamas (JPE 2025).** Knowledge hierarchies. Juniors solve common problems, and seniors spend "helping time" on referrals, the analogue of ρ. In Ide & Talamas, basic AI pushes humans out of routine work, and advanced AI pushes solvers down into routine work. Autonomous AI corresponds to the q·p branch, copilot AI to κ. The application to Indian delivery pyramids is our reading; neither paper studies IT services.
- **Agrawal, Gans, Goldfarb (JEP 2019).** AI as cheap prediction plus human judgment. Tasks where judgment cannot be codified should have high ρ or low q.

**Hidden assumptions in the draft that theory exposes.**
- (i) Time saved equals labour removed. O-ring, the GRH productivity effect, and Humlum's 80% reallocation all cut against this.
- (ii) Additivity across j. Chaining and complementarity cut against this.
- (iii) Hours-weighted vs cost-weighted aggregation. Saved junior hours and added senior review hours carry different prices.
- (iv) Fixed task boundaries and fixed w_j.

**For θ_j:** this section informs the *aggregation* step (w_j, and whether S = Σ w_j θ_j is valid) and the *functional form* (fallback rule; ρ fixed vs proportional). It supplies no numbers for p, q, ρ or κ. Best practice: report S both first-order and reweighted, and test at least two fallback rules.

---

## 7. IT services and BPO evidence

**Exposure and job postings in South Asia and beyond.**
- **World Bank South Asia Development Update (Oct 2025, ch. 2; Kirby, Rexer, Sharma)**, using Lightcast postings:
  - After ChatGPT, postings for the most exposed, least complementary white-collar jobs fell about 20%.
  - Call-centre agents fell 24% relative to machine operators.
  - Business-services postings were −0.349 log points (about 30% lower; the text says "35 percent slower"), with posted wages −8% relative to other jobs.
  - Entry-level jobs with a software developer's exposure grew 21% more slowly than those with an electrician's exposure.
  - These are relative effects on postings, not hours.
- **WDR 2026.** 4.5% of jobs in low- and middle-income countries are amenable to automation by GenAI, vs 14.2% in high-income countries. Its "39% fall in jobs outsourced to developing countries in 2025" cannot be traced to the cited slides, whose data end Dec 2024. Do not use it.
- **IMF (Cucio & Hennig 2025).** About a third of Philippine workers are highly exposed, and BPO has the highest share at risk.
- **Huang, Liu, Wang, Yu (World Bank WP, 2026; 84 countries).** In high-income countries, postings for more substitutable occupations fell 5.8%. In middle- and low-income countries the effect was smaller and insignificant (only the seminar abstract was read; full text unverified). Adoption gaps keep realised substitution below the ceiling.

**Platform and market evidence.**
- **Betai & Chen (Jan 2026 conference slides).** On a global freelance platform, for developing-country sellers at mean exposure: contracts −34%, workers −35%, value −43% to −53% (the slides disagree). Value per surviving contract is higher. This mixes labour saved, buyers doing the work in-house, and demand.
- **Hui, Reshef, Zhou (Org. Sci. 2024):** Upwork freelancers in exposed occupations saw jobs −2% and earnings −5.2%.
- **Demirci, Hannane, Zhu (Mgmt Sci 2025):** automation-prone writing and coding posts fell 21% within 8 months, and the remaining jobs were more complex. That fits AI taking short tasks first, though this was not tested.

**Firm and labour-market studies.** These give *reduced forms*, roughly s(1 − εφ) × an exposure difference, not θ.
- **Canaries (Brynjolfsson, Chandar, Chen, Aug 2026; US ADP payroll):** employment of 22–25-year-olds in exposed occupations is 19% below the kept-pace path. The authors call this descriptive, and the gap attenuates with education controls.
- **Hampole et al. (NBER 33509):** one SD more task exposure cuts an occupation's within-firm employment share by about 14.5% over 5 years (IV), offset by firm growth. US, 2010–23, mostly pre-generative-AI.
- **Hosseini & Lichtinger (2026):** junior employment at adopting firms about 9% lower after six quarters, with no break for seniors.
- **Chandar & Klein Teeselink (41 countries, including India):** the junior share at affiliates of adopting firms is −1.9 pp; senior employment +6.7%; total +3.3% (marginally significant). India ranks first in the AI share of LinkedIn postings, but Revelio covers only about 8% of Indian employment.
- **Acemoglu, Autor, Hazell, Restrepo (JOLE 2022):** substitution showed up in establishment hiring but washed out in aggregates. Their hiring regressions exclude IT and professional services.
- **Eisfeldt et al. and Borri, Liu, Tsyvinski (arXiv 2606.30583):** templates for an event study of stock prices around frontier model releases. Converting returns into an implied s is our proposal, and the sign is ambiguous for vendors whose clients capture the savings.

**India-specific surveys.**
- **ICRIER (Mishra et al., Feb 2026; acknowledges OpenAI support).** 651 respondents from 620 IT firms, about a 10% response rate.
  - 65% report lower hiring after AI. Entry level: 55% declines; mid-level: 25%; senior: 82% no change.
  - Most affected divisions: software development 72%, infrastructure/cloud 48%, project management 37%.
  - Roles seen as declining *in the industry*: data entry/back-office 32%, manual testing 15%, entry-level programming 13%.
  - It asks about "time per unit of work" but reports **direction only, no magnitudes**. Its microdata would be the closest thing to a direct θ_j check.
- **EY India (2025).** IT productivity +43–45% over 5 years, by function development ~60%, BPO 52%, consulting 47% (press coverage only; method undisclosed). Use only as an upper-bound prior on the *ordering*.

**Firm disclosures (selected cases and targets, not averages).**
- **HCLTech (Q4 FY26 call).** About 40% of industry spend (application development and support, traditional infrastructure, customer support) "can shrink 3% to 5% CAGR for a few years". The ability to run production fixes without a human is "very limited". "Very little has really played out in already reported numbers."
- **Infosys (Q4 FY26, Q1 FY27).**
  - Hertz COBOL-to-microservices migration: 60% lower cost and 60% faster.
  - BP: 18% better IT-operations efficiency.
  - 30,000+ developers on Copilot; "over 80,000 employees" on tools like Claude Code or Codex, out of ~328,000 staff.
  - CFO: productivity "will get passed back to the client largely", so φ is near 1.
  - The context reviewer also read Infosys's FY26 20-F: 54% of revenue is fixed-price, 76.8% of effort is offshore, and there is a shift toward outcome and transaction pricing attributed to "AI disruptions". Their derived ~$16/h average loaded labour cost was not re-checked.
- **TCS (Q1 FY27, 9 Jul 2026).** CEO K. Krithivasan reportedly said productivity gains passed on to clients at renewal are around 10–15% "in most places". This bears on pass-through φ, not θ directly. (Unverified: seen only in search snippets of the transcript PDF, which blocked automated access. Open it in a browser before citing: https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2026-27/q1/Management%20Commentary/Transcript%20of%20the%20Q1%202026-27%20Earnings%20Conference%20Call%20held%20on%20Jul%209,%202026.pdf)
- None of TCS, Infosys or HCLTech gave a company-wide AI effort-reduction percentage on their Q2 FY27 calls (Oct 2026). Infosys said it could not give a number; HCLTech said it is "in the early phases of deflation".
- **TCS (Q2 FY27).** AI revenue $3.1 bn annualised. Target of 25–30% faster S/4HANA implementation; aiming to double HR-operations efficiency. "There is a deflation because of the productivity benefit."
- **Cognizant (Feb 2025).** About 20% of code written with AI; +34% productivity for bottom-quartile developers and +17% for the top half.

**Broker estimates (press summaries; all mix θ with pass-through, demand and contract timing).**
- Kotak: about 7% gross / 3.5% net AI-led deflation, period unstated.
- Jefferies: an assumed 5–35% productivity boost; application managed services 22–45% of revenue (5paisa narration).
- ICICI: about 30% of the industry at risk; base case applies 50% revenue deflation to that segment.

**Older India literature.**
- Banerjee & Duflo (QJE 2000): reputation and contracting in Indian software.
- Arora & Asundi (1999): ISO certification, mostly as a marketing signal.
- Eichengreen & Gupta (2011): services-led growth.
- Jensen (QJE 2012): BPO recruiting changed young rural women's schooling, work and marriage decisions. This bears on who bears the losses.

**For θ_j:** this section informs **w_j** (revenue splits; HCLTech's ~40% "disrupted" share), the **ordering** of θ_j (development and testing faster than unattended production operations; legacy COBOL maintenance low except for one-off migrations), and **φ** (near 1 per Infosys). It gives outside checks on s·φ, but **no ρ, q or f_j for Indian delivery work**. The ICRIER microdata, if obtainable, are the most promising direct check.

---

## 8. Gaps

**First, what is *not* a gap.** The skeptic and measurement reviews refuted several tempting claims:
- "Nobody measures the intensive margin": many RCTs, Anthropic usage data and surveys do.
- "Nobody nets out failure": Anthropic's January 2026 report does.
- "Nothing ties success to task length outside benchmarks": the same report does.
- "ρ is only in GDPval": there are also the METR RCT, Rein's fix-time note and CUPS.
- "q is only on SWE-bench": there are also AIDev deployment merge rates, GDPval win rates and RLI client acceptance.
- "No IT-ops or customer-service agent benchmarks exist": ITBench (arXiv 2502.05352: SRE 13.8%, CISO 25.2%, FinOps 0%) and τ-bench exist. They just lack human time baselines.
- "No public task-length data": the Public Jira Dataset, JOSSE and SWE-bench difficulty labels exist.
- "No India evidence": ICRIER, the World Bank and Chandar & Klein Teeselink exist. They give outcomes, not parameters.

The real gaps, merged across the three lenses and ranked by how much they matter for θ_j:

**1. No joint measurement of the whole formula on one set of tasks, by task length.** *(Skeptic G1; measurement M9.)*
- *Plain:* p, q, ρ and κ are each measured somewhere, but always on different tasks, models and people, and almost never broken down by h. Multiplying them assumes they are independent and comparable. The fallback rule after failure (redo with assistance, full redo, or retry) has never been timed against the alternatives.
- *Closest:* GDPval (win rate × review × full redo). It has no breakdown by h, no κ branch, uses grading time, and covers OpenAI models only.
- *Why it matters:* the GDPval-style collapse (90× → 1.4×) probably depends on h, and the fallback rule alone can shift θ a lot when p ≈ 0.5.
- *Confidence:* high.

**2. No hours-weighted task-length distributions f_j(h) for Indian service lines.** *(M1; C2; G6.)*
- *Plain:* nobody has published how long an AMS ticket, a test task or a claims transaction takes in an Indian delivery centre, weighted by hours.
- *Closest:* SWE-bench Verified buckets (annotator guesses, open-source bug fixes); JOSSE and the Public Jira Dataset (sparse open-source effort logs); Anthropic task-time means (conversations, Claude-estimated, selected); RLI (freelance, creative-heavy).
- *Why it matters:* METR's slope is shallow, so where hours sit along h, especially the long tail, largely sets θ_j. Alibaba shows a 32% cut on one sub-step becoming 4% of the whole chat.
- *Confidence:* high.

**3. Review cost ρ as a function of task length, in production review.** *(M6; G2.)*
- *Plain:* we do not know whether review time is a fixed cost per change, proportional to length, or something else.
- *Closest:* GDPval 0.27 (grading); Rein ~0.33 (n = 4, estimated); METR RCT 9%; CUPS 22.4%; Google's baseline (~45–50 min per 24-line change, implying a fixed cost). METR collected maintainer review times in its 2026 study but did not publish them.
- *Why it matters:* ρ is subtracted one-for-one. Moving it from 0.1 to 0.3 can erase the delegate branch at mid-range p. A fixed per-change cost penalises short tasks most.
- *Confidence:* high.

**4. q for agents that iterate, on client-style code, and its dependence on h.** *(M5; G3; C6.)*
- *Plain:* q ≈ 0.5 comes from one-shot agents on three strict Python projects. Indian delivery adds a second review layer: client acceptance (UAT, change boards).
- *Closest:* Whitfill et al.; AIDev deployment merge rates (not conditioned on passing tests or on h).
- *Why it matters:* q multiplies the whole delegate branch, and as a flat multiplier it caps θ (Section 1). Values from 0.5 to 0.9 move delegated θ by up to ~2×.
- *Confidence:* high for importance, medium for the claim that q depends on h, which is inferred from the 50 → 8 min horizon refit.

**5. No capability curve p(h,t) for testing, IT operations, BPO, legacy stacks or non-English work.** *(M3; C7; C9; C8; G5.)*
- *Plain:* METR's curves are software, ML and cyber. Computer-use horizons are 40–100× shorter. IT-ops and customer-service benchmarks report success but not human time. Legacy stacks (COBOL, SAP) have almost no evidence. Hindi or code-mixed work is untested.
- *Closest:* Kwa & Cheng domain multipliers; ITBench; τ-bench; TheAgentCompany; OSWorld; the Stanford talk on niche languages.
- *Why it matters:* testing, infrastructure and BPO are probably most of Indian IT/BPO hours. Borrowing coding curves could be off by 1–2 orders of magnitude in horizon.
- *Confidence:* high.

**6. The task length h is measured on the wrong human.** *(M2; C6.)*
- *Plain:* METR's h is outside contractors, who took 5–18× longer than maintainers. Vendor staff on long-running client accounts are somewhere in between, and nobody has estimated where.
- *Why it matters:* the same task can look like a 4-hour task (low success) or a 20-minute one (high success). At the frontier, that is equivalent to moving t by more than a year.
- *Confidence:* high.

**7. Labour-hours weights w_j by service line, including non-task time.** *(M10; C1.)*
- *Plain:* only revenue shares exist, and revenue ≠ hours (Infosys onsite hours bill at roughly 3× offshore). Bench, training, sales and coordination time (θ ≈ 0) is usually ignored, which overstates S.
- *Closest:* firm service-line splits (end 2017–19); Infosys person-months (2010–18); ICRIER (direction only); Hatgis-Kessell (US O*NET).
- *Why it matters:* S is linear in w_j.
- *Confidence:* high.

**8. No net, service-line θ for Indian IT/BPO to validate against, and no model of how contracts turn θ into observed numbers.** *(M12; C4.)*
- *Plain:* every direct θ number is gross (Anthropic), from a benchmark (GDPval), self-reported, or a firm showcase. Under time-and-materials contracts, savings become fewer billed hours. Under fixed-price contracts (54% of Infosys revenue), the vendor keeps them until renewal. HCLTech says AI has barely shown up in reported numbers.
- *Why it matters:* without an anchor, errors in p, q, ρ and κ cannot be told apart. The 2.3 pp/yr also contains adoption, contract timing and εφ.
- *Confidence:* high.

**9. κ for current tools, in the right population.** *(M8.)*
- *Plain:* clean κ estimates are 2020–24 tools, or early-2025 tools with mixed modes. The late-2025 RCT broke down because of selection. There is no Indian delivery sample; Accenture's offices in the Cui study are in Southeast Asia.
- *Why it matters:* κ is the floor of the max{}, which applies across most of h today.
- *Confidence:* high.

**10. The high-reliability tail of p.** *(M4.)*
- *Plain:* delegation needs 90–99% success. The 80% horizon moves by up to 2× across reasonable fits, the 99% horizon cannot be measured (it would need ~300 tasks per time bucket), and curve shape changes the tail by ~3×.
- *Confidence:* high.

**11. No net θ tracked across model generations on a fixed task set.** *(M11; G4.)*
- *Plain:* θ_j(t) is extrapolated from p(h,t). If q and ρ lag p (as Merali's agentic result and METR's weak q trend hint), the bottom-up S(t) overshoots. The US self-reported ratio of hours saved per assisted hour is flat at ~0.35.
- *Closest:* Merali; GDPval across model generations.
- *Confidence:* medium.

**12. Downstream rework never converted into hours.** *(M13; G7.)*
- *Plain:* complexity, warnings, incidents and insecure code all rise with AI output, but nobody turns this into later maintenance hours. This matters for Indian AMS, which inherits other people's code.
- *Closest:* the CMU Cursor study, Faros, Perry et al., DORA.
- *Confidence:* medium.

**13. AI running cost relative to Indian wages.** *(M14; C3.)*
- *Plain:* cost comparisons use US wages (GDPval) or computer vision (Svanberg). At ~$16/h loaded cost (context reviewer's derivation; unverified), a $4 agent run on a 1-hour task removes about a quarter of the saving.
- *Why it matters:* θ for India is biased upward without this term, most for long, retry-heavy tasks.
- *Confidence:* medium.

**14. The staffing pyramid: whose hours are saved and who reviews.** *(M15; C5.)*
- *Plain:* gains are largest for juniors, and seniors do the review. Hours-weighted and cost-weighted θ can differ. Weak verifiers over-delegate (Huang et al.).
- *Closest:* ICRIER entry-level hiring; Garicano / Ide-Talamas theory.
- *Confidence:* medium.

**15. How predictable success is for an individual task.** *(M16.)*
- *Plain:* if a firm can tell in advance which tickets the AI will get right, routing per ticket beats the h-average. This has never been measured for code or IT tickets. METR's task-level data could give an upper bound.
- *Confidence:* medium.

**16. Time zones and offshore latency.** *(C10.)*
- *Plain:* slow feedback across time zones may add review rounds and coordination hours and change q. It may also push clients to do AI-assisted work in-house or in captive centres (GCCs), which contaminates the top-down estimate.
- *Confidence:* low.

---

## 9. What you could do

### 9.1 Ranked ideas (judge's scores, each out of 10; total out of 40)

| Rank | Idea | Feas. | Gap | Fit to recipe | Career | Total | One-line verdict |
|---|---|---|---|---|---|---|---|
| 1 | **feasible-1** θ_j calculator plus a value-of-information ranking that becomes the dataset requirement | 8 | 6 | 9 | 6 | **29** | Closest to what Andrei asked for; shows the q form and the fallback rule are first-order |
| 2 | **firmdata-2** Bottom-up ceiling vs the realised 2.3 pp/yr | 6 | 7 | 8 | 7 | **28** | Makes θ falsifiable; FY24–26 mainly identifies κ × adoption |
| 3 | **firmdata-1** Hours weights w_j (and non-task w_0) from firm service-line disclosures | 8 | 6 | 8 | 4 | **26** | Data already in the repo; fixes the upward bias from ignoring non-task time |
| 4 | **feasible-2** Refit METR task-level data: tail, curve shape, per-task predictability, q form | 7 | 5 | 6 | 8 | **26** | Most evals-native; do only the depth needed for bootstrap bands on p |
| 5 | **feasible-3** Re-analyse METR's public RCTs for κ(h) and post-review rework | 8 | 5 | 6 | 7 | **26** | Cheap; gives κ an honest length gradient; check the paper's subgroup figures first |
| 6 | **lab-1** Umbrella: horizons → net labour saved with a Sobol (variance-based sensitivity) ranking | 4 | 6 | 8 | 7 | **25** | Right table of contents, too big as a separate project |
| 7 | **lab-4** Fixed-task mini-panel: delegate vs assist vs manual across two model generations | 3 | 8 | 7 | 7 | **25** | Truest gap, infeasible in 5 weeks; write the protocol only |
| 8 | **lab-2** q(h,t) in deployment from AIDev agent PRs | 5 | 7 | 5 | 8 | **25** | Estimates q·p at the self-selected mix; one week of descriptive work as a band on q |
| 9 | **feasible-4** f_j(h) from public Jira effort logs plus a calibrated LLM duration labeller | 5 | 7 | 7 | 5 | **24** | Check JOSSE units first; scope to JOSSE only |
| 10 | **firmdata-3** Code management claims into per-line θ checks | 7 | 4 | 5 | 4 | **20** | Do a one-day keyword filter; skip the full codebook |
| 11 | **lab-3** Review-cost primitive from agentic coding logs (local transcript pilot; full version needs lab data) | 4 | 5 | 4 | 7 | **20** | Park as a post-fellowship proposal |
| 12 | **firmdata-4** Cross-firm test of whether firms with more high-θ work show bigger effects | 7 | 3 | 3 | 3 | **16** | Underpowered (firm residual SD ≈ 2.2–3.4 pp); keep only an FY27–28 pre-registration |

### 9.2 Before the next mentor meeting (~6–8 hours)

Goal: show Andrei a working recipe skeleton plus one surprising structural result, not a plan.

1. **θ function and the two-form plot (~2.5 h).**
   - Code θ_j(t) with p(h) as a logistic in log h. Back out each model's slope as β = ln4 / ln(p50/p80) from the TH1.1 YAML already downloaded to `data/explore/theta_lit/metr_benchmark_results_1_1.yaml (from https://metr.org/assets/benchmark_results_1_1.yaml)`.
   - Plot θ against model release date for one maintenance-like f(h): hours-weighted lognormal with a 1 h or 4 h median.
   - Use two q forms (flat 0.5 vs a 7× horizon shift) and three fallback rules (redo with assistance / full redo / retry).
   - The judge's illustrative check (own assumptions: q = 0.5, κ = 0.1, ρ = 0.27): Opus 4.6 at a 1 h median gives θ ≈ 0.19 with the multiplier vs 0.35 with the shift; at a 4 h median, ≈ 0.14 vs 0.20.
2. **w_j table (~1.5 h).**
   - Pull all `dim_type=='service_line'` rows from `data/tidy/panel_long.csv` into one CSV, with a hand crosswalk to the six j.
   - Compute the Infosys offshore effort/revenue ratio by quarter (71.3 vs 45.4 at Q4 FY18) to check whether the ~3× onsite premium is stable.
   - Resolve the TCS ADM figure (37.7 in the panel vs 37.9 quoted).
3. **RCT reproduction (~1.5 h).** Clone `github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs`, run `regression.py`, and confirm the time units. Skim arXiv 2507.09089's subgroup figures for an existing breakdown by task length before claiming novelty.
4. **Recipe one-pager (~1 h).** See 9.5.

**Questions for Andrei:**
- (a) Is the deliverable a ranked data specification plus an identified set (a range of parameter values consistent with the data), or does he want a point estimate?
- (b) Should q be a multiplier or a horizon shift? Should κ be indexed by tool generation?
- (c) Should validation target the *level* of S or its *change* times adoption? The judge recommends the change.
- (d) Where does ER&D go? It is not one of the six j.

Do not start the AIDev, JOSSE or 5.8 GB Jira downloads this week.

### 9.3 The remaining weeks (~5 weeks × 5–8 h)

Rule: every week ends with a figure or table that goes into the final note.

- **Week 2: recipe core (feasible-1 + firmdata-1).** Set prior ranges on q, ρ, κ, the context multiplier m (1–18) and the curve shape. Run a Monte Carlo and a simple variance decomposition (binned correlation ratios are enough), under two prior sets. Finish the revenue-to-hours conversion and estimate w_0 from Infosys person-months. *Output: the parameter ranking.*
- **Week 3: p(h,t) module (trimmed feasible-2).** Parse `task_results_1_1.yaml`, replicate METR's p50 for 2–3 models, fit a shared-slope logistic, and bootstrap bands on p(h). Optionally compute one per-task predictability number per h-bin, as a bound on the routing gain.
- **Week 4: validation (firmdata-2).** Build an adoption series A(t) from `audit/calls_statements.csv` and a map of which models were actually in use when. Compute the change in S_ceiling over FY24–26. Find the region of (q, ρ, κ, m, curve) consistent with ~7 pp cumulative (4.5–11), with breakdown points and implied adoption. If time allows, run the feasible-3 κ(h) regression in parallel.
- **Week 5: one data module, chosen by the week-2 ranking.** If f_j or m dominates: JOSSE only (check units; compare count- vs hours-weighted effort; fit lognormals). If q dominates: an AIDev-pop descriptive analysis of merge rate by agent × size decile × month, excluding self-merges.
- **Week 6: write-up.** A 5–7 page note with the formal recipe and the identified set; a one-page firm data request; a pre-registered FY27–28 prediction table; a half-page "ideal experiment" appendix (the lab-4 protocol and power calculation).

**Dropped:** lab-3, running lab-4, firmdata-4 estimation, the Montgomery 5.8 GB dump, LLM-labeller calibration, and the firmdata-3 full codebook.

**Contingency:** if week 2 shows the q form and the fallback rule swamp every data-driven parameter, make that the headline result and spend week 5 on AIDev.

### 9.4 Combinations the judge recommends

1. **Recipe + validation spine: feasible-1 + firmdata-2 + firmdata-1.** One shared θ function. feasible-1 ranks the unknowns, firmdata-1 supplies the weights, firmdata-2 checks against 2.3 pp/yr. Use lab-1 as the table of contents.
2. **q module: the q-form step of feasible-2 + one week of lab-2.** METR's one-shot horizon shift and AIDev's iterating-agent merge curves bracket q from two sides.
3. **κ and ρ priors: feasible-3 + a lab-4 protocol (written, not run).** Use feasible-3's variance to size the power calculation.
4. **f_j bridge: JOSSE-only feasible-4 + the firm data request.** A public prior, plus a labelling protocol a firm could run on its own tickets and release only as aggregates.
5. **Cheap add-ons in the write-up:** the firmdata-3 one-day filter, and the firmdata-4 FY27–28 pre-registration.

**Measurement agendas and funding (context for the ask).**
- Brynjolfsson, Korinek & Agrawal's NBER research agenda (w34256) proposes finer task taxonomies. That is an extensive-margin refinement, not time-saved measurement.
- Coyle & Poquiz (NBER w34330) call for task-time and time-use-at-work data in labour surveys. That is close to a data requirement for f_j and w_j.
- BLS (Machovec, Rieley, Rolen, MLR Feb 2025) uses analyst judgment, not any θ-type parameter. It projects software developers +17.9% and customer service representatives −5.0% for 2023–33.
- Funding:
  - Anthropic Economic Futures awards are $10–50k plus $5k API credits, and are currently closed.
  - The OpenAI Foundation's $250M programme (May 2026) promises open calls with no dates yet and names low- and middle-income countries as a priority.
  - OpenAI's Economic Research Exchange deadline, the Stripe and UChicago fellowships, and the Anthropic Fellows economics track could not be confirmed from primary pages (unverified).

### 9.5 Draft "dataset requirement and recipe" for Andrei

**Target.** θ_j(t) is the share of labour hours in service line j removed at full adoption with the AI available at t, net of failure, review, assisted redo and AI running cost. The aggregate is S(t) = Σ_j w_j θ_j(t), plus a non-task bucket w_0 with θ_0 = 0.

**Core formula, with the choices made explicit:**

θ_j(t) = ∫ max{ q(h,t)·p(h/m, t)·(1 − κ_v) + κ_v − ρ(h) − c(h,t)/wage , κ_v } f_j(h) dh

- m converts firm-staff hours into METR contractor hours.
- κ_v is the assistant speedup for tool vintage v.
- c/wage is AI running cost as a share of labour cost.

**Three structural choices, always reported as alternatives:**
1. q as a flat multiplier vs a horizon shift (q = 1, with h50 divided by ~7). A flat q caps θ at q(1−κ)+κ−ρ ≈ 0.28 at central values. A shift caps it at 1 − ρ.
2. Fallback after failure: redo with assistance (draft), full human redo (GDPval), or retry-and-reverify (Demirer et al.).
3. Curve shape: logistic in log h with a shared slope, vs constant hazard.

**A. Public data available now**

| Parameter | Dataset | Access | What it gives you / how to estimate |
|---|---|---|---|
| p(h,t) | METR TH1.1 `task_results_1_1.yaml`, `benchmark_results_1_1.yaml` (metr.org/time-horizons) | Public; frozen Sep 2026 | Per-task human minutes, successes, runs. Weighted logistic on log h, shared slope, bootstrap over tasks. Check p50/p80 (e.g. Claude 3.7 Sonnet 60.4/12.1 min) |
| m (context) | None | — | Prior range 1–18 from METR's contractor-vs-maintainer gap; report m = 1, 3, 10 |
| q | Whitfill et al. (METR note); AIDev v5 (HF `hao-li/AIDev`) | Note public; AIDev public, CC-BY-4.0 | Anchor 0.5 / 7× shift. AIDev: logistic of merge (excluding self-merges) on log diff size by agent × month, giving a band on q·p |
| ρ(h) | GDPval paper; Rein note; METR RCT repo (`post_review_implementation_time`); CUPS | Public | Model ρ(h) = a/h + b; report the a = 0 and b = 0 corners |
| κ_v | METR early-2025 RCT `data_complete.csv`; published Cui, Google, BLR estimates | Public (no licence stated on repo) | log(time) on AI × log(predicted_time_no_ai), developer fixed effects ⇒ κ(h) for 2025 tools |
| f_j(h) | JOSSE (Zenodo 7022735); Public Jira Dataset (Zenodo 5882881); SWE-bench Verified `difficulty` | Public, CC BY 4.0 | Hours-weighted histograms and lognormal fits for maintenance vs development. Check JOSSE effort units first |
| w_j, w_0 | Project repo `data/tidy/panel_long.csv` (service-line splits, onsite/offshore effort and revenue, Infosys person-months 2010–18) | Public firm disclosures | Revenue → hours via the onsite premium; intervals; FY26 roll-forward flagged as extrapolated |
| c/wage | Token prices × retries; loaded wage from filings | Public | Include only in the long-task, many-retry scenario |
| Cross-check p | Anthropic Economic Index (HF, Jan/Mar 2026) | Public, CC-BY | Success-by-length means; gross time ratios |

**B. Estimation.**
1. Monte Carlo over priors and the three structural choices.
2. Variance decomposition of θ_j and S under two prior sets, which gives a ranked list of which missing measurement most narrows S.
3. Report S(t) at each model release date as a band.

**C. Validation against the top-down estimate (≈ 2.3 pp/yr, range 1.5–3.6, FY24–26).**
- (a) Compare *changes*. Realised cumulative replacement (≈ 7 pp, range 4.5–11) should roughly equal the change in Σ_j w_j A_j(t) θ_j(t), where A(t) is adoption from disclosed tool head-counts, lagged from model release.
- (b) Ceiling test: realised ≤ the change in S_ceiling. Report breakdown points (the smallest q, or largest ρ, at which the ceiling falls below the realised figure).
- (c) Implied adoption = realised ÷ change in S. Check it against disclosures, e.g. Infosys's Copilot and Claude Code head-counts relative to ~328k staff.
- (d) On time-and-materials work, savings show up as fewer billed hours, so the measured rate is closer to a lower bound.
- (e) Per-line sanity checks from realised, portfolio-wide firm claims.
- (f) Pre-register FY27–28 predictions.

State plainly that FY24–26 mostly identifies κ × adoption and has little power over q and ρ.

**D. The ask: ideal firm or partner dataset (one row per ticket or task).**
- Service line and task type; client and account (hashed).
- Logged effort hours, plus an estimate made before the work started.
- AI mode (none / assist / delegate), tool and model version, date.
- Whether automated checks passed.
- Reviewer seniority band and reviewer minutes.
- Accept/reject at vendor review and at client UAT.
- Rework hours before and after acceptance; reopen or incident within 30 days.
- AI cost (tokens or $).
- Onsite/offshore flag; contract type (fixed-price, T&M, outcome).
- Plus timesheet hours by service line and non-task category, for w_j and w_0.

Rough sample size: if the per-ticket net saving has an SD of about 0.4 (an assumption), pinning θ_j within ±5 pp at 95% confidence needs ~250 tickets per line per mode, and ~500 per arm for an AI-vs-no-AI difference, in each of about 4 h-bins. Only aggregates by line × h-bin × mode need to leave the firm. That fits firm confidentiality and MoSPI-style aggregate-only norms.

---

## 10. Sources

Works with status "verified" or "corrected" in the digest are listed. A few works were not in the stream digests but were opened directly by the completeness critic or a gap reviewer; they are listed with that note. Where a work appears in several sections, it is listed under its main use.

### Section 2: Exposure measures
- Eloundou, Manning, Mishkin, Rock (2023/2024), "GPTs are GPTs". https://arxiv.org/abs/2303.10130 ; https://arxiv.org/pdf/2303.10130v5 ; data: https://github.com/openai/GPTs-are-GPTs
- Felten, Raj, Seamans (2021; 2023), AIOE and LM-AIOE. https://arxiv.org/pdf/2303.01157 ; https://github.com/AIOE-Data/AIOE
- Webb (2019), "The Impact of Artificial Intelligence on the Labor Market". https://conference.nber.org/confer/2020/YSAIf20/Required%2011.pdf
- Brynjolfsson, Mitchell, Rock (2018), "What Can Machines Learn…". https://www.aeaweb.org/articles?id=10.1257/pandp.20181019 ; https://www.openicpsr.org/openicpsr/project/114436/version/V1/view
- Svanberg, Li, Fleming, Goehring, Thompson (2024), "Beyond AI Exposure". https://futuretech.mit.edu/2024-01-18+Beyond_AI_Exposure.pdf
- Gmyrek et al. (2025), ILO Working Paper 140. https://www.developmentaid.org/api/frontend/cms/file/2025/05/WP140_web.pdf ; https://www.ilo.org/publications/generative-ai-and-jobs-refined-global-index-occupational-exposure
- Eisfeldt, Schubert, Zhang (2023, rev. 2026), "Generative AI and Firm Values". https://www.nber.org/papers/w31222
- Tomlinson, Jaffe, Wang, Counts, Suri (2025), "Working with AI". https://arxiv.org/abs/2507.07935 ; https://github.com/microsoft/working-with-ai
- Massenkoff, McCrory (2026), "Labor market impacts of AI". https://www.anthropic.com/research/labor-market-impacts
- Hatgis-Kessell, Aguirre, Wan, Bommasani (2026), "Estimating time spent on work tasks". https://arxiv.org/abs/2608.05172
- Blinder (2007), "How Many U.S. Jobs Might Be Offshorable?". https://gceps.princeton.edu/wp-content/uploads/2017/01/142blinder.pdf
- Blinder, Krueger (2009/2013), "Alternative Measures of Offshorability". https://www.nber.org/papers/w15287
- Jensen, Kletzer (2005), "Tradable Services". https://www.piie.com/sites/default/files/publications/wp/wp05-9.pdf
- Reinsdorf, Slaughter (2009), introduction summarising van Welsum and Reif. https://www.nber.org/system/files/chapters/c11604/c11604.pdf
- Autor, Levy, Murnane (2003), "The Skill Content of Recent Technological Change", QJE 118(4) (NBER WP 8337). Landing page opened by the completeness critic only; not reviewed in a stream. https://www.nber.org/papers/w8337

### Section 3: Experiments
- Noy, Zhang (2023). https://economics.mit.edu/sites/default/files/inline-files/Noy_Zhang_1.pdf
- Brynjolfsson, Li, Raymond (2025), "Generative AI at Work". https://arxiv.org/pdf/2304.11771v2 ; https://www.nber.org/papers/w31161
- Ni et al. (2026), Alibaba field experiment. https://arxiv.org/pdf/2603.29888
- Dell'Acqua et al. (2023/2026), "Navigating the Jagged Technological Frontier". https://mitsloan.mit.edu/sites/default/files/2023-10/SSRN-id4573321.pdf
- Dell'Acqua et al. (2025), "The Cybernetic Teammate". https://www.nber.org/system/files/working_papers/w33641/w33641.pdf
- Schwarcz et al. (2025), "AI-Powered Lawyering". https://www.law.berkeley.edu/wp-content/uploads/archive/2025/12/AI-Powered-Lawyering.pdf
- Otis, Clarke, Delecourt, Holtz, Koning (2026), Kenya field experiment. https://escholarship.org/content/qt0fb001r8/qt0fb001r8.pdf
- Merali (2024), "Scaling Laws for Economic Productivity". https://arxiv.org/abs/2409.02391
- Lukac et al. (2025), AI scribes RCT. https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=41497288&rettype=abstract&retmode=text
- Dillon, Jaffe, Immorlica, Stanton (2025), "Shifting Work Patterns with Generative AI". https://arxiv.org/pdf/2504.11436v4
- Agarwal, Moehring, Rajpurkar, Salz (2023, rev. 2026), radiology experiment. https://www.nber.org/papers/w31422
- Vaccaro, Almaatouq, Malone (2024), meta-analysis. https://arxiv.org/abs/2405.06087
- Peng, Kalliamvakou, Cihon, Demirer (2023), Copilot experiment. https://arxiv.org/pdf/2302.06590
- Cui, Demirer, Jaffe, Musolff, Peng, Salz (2025), three field experiments (Management Science, published online 27 Feb 2026, doi:10.1287/mnsc.2025.00535, confirmed via Crossref; volume/issue not yet assigned). https://economics.mit.edu/sites/default/files/inline-files/draft_copilot_experiments.pdf
- Becker, Rush, Barnes, Rein (2025), METR developer RCT. https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ ; https://arxiv.org/abs/2507.09089 ; data: https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs
- Becker, Rush, Cunningham, Rein, Mahamud (2026), "We are Changing our Developer Productivity Experiment Design". https://metr.org/blog/2026-02-24-uplift-update/
- Paradis et al. (2024), Google enterprise RCT. https://arxiv.org/html/2410.12944v2
- Murphy-Hill, Butler, Savelieva (2026), Microsoft CLI agents rollout. https://arxiv.org/html/2607.01418v1
- He, Miller, Agarwal, Kästner, Vasilescu (2026), Cursor study. https://arxiv.org/html/2511.04427v3
- Denisov-Blanch (2025), Stanford talk. https://www.ai.engineer/talks/tbDDYKRFjhk-ai-developer-productivity
- Huang et al. (2025), "How AI is transforming work at Anthropic". https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic
- DORA reports (2024/2025). https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report
- Mozannar et al. (2024), "The RealHumanEval". https://arxiv.org/abs/2404.02806

### Section 4: From benchmarks to labour saved
- Kwa et al. (2025), "Measuring AI Ability to Complete Long Software Tasks". https://arxiv.org/abs/2503.14499
- METR (2026), Time Horizon 1.1 and data files. https://metr.org/blog/2026-1-29-time-horizon-1-1/ ; https://metr.org/time-horizons/ ; https://metr.org/assets/benchmark_results_1_1.yaml ; https://metr.org/assets/task_results_1_1.yaml
- Barry (2026), "Impact of modelling assumptions on time horizon results". https://metr.org/notes/2026-03-20-impact-of-modelling-assumptions-on-time-horizon-results/
- Kwa (2026), "Clarifying limitations of time horizon". https://metr.org/notes/2026-01-22-time-horizon-limitations/
- Kwa, Cheng (2025), "How Does Time Horizon Vary Across Domains?". https://metr.org/blog/2025-07-14-how-does-time-horizon-vary-across-domains/
- Ord (2025), "Is there a half-life for the success rates of AI agents?". https://arxiv.org/abs/2505.05115
- Rein et al. (2025), HCAST. https://arxiv.org/abs/2503.17354
- Brand, Denain (2025), "What skills does SWE-bench Verified evaluate?". https://epoch.ai/blog/what-skills-does-swe-bench-verified-evaluate
- Whitfill, Wu, Becker, Rush (2026), "Many SWE-bench-Passing PRs Would Not Be Merged into Main". https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/
- Rein (2025), "Research Update: Algorithmic vs. Holistic Evaluation". https://metr.org/blog/2025-08-12-research-update-towards-reconciling-slowdown-with-time-horizons
- Patwardhan et al. (2025), GDPval. https://arxiv.org/abs/2510.04374 ; https://arxiv.org/html/2510.04374
- Miserendino, Wang, Patwardhan, Heidecke (2025), SWE-Lancer. https://arxiv.org/abs/2502.12115
- Mazeika et al. (2025), Remote Labor Index. https://arxiv.org/abs/2510.26787 ; https://labs.scale.com/leaderboard/rli
- Xu et al. (2024), TheAgentCompany. https://arxiv.org/abs/2412.14161
- ITBench (IBM/UIUC, 2025). Abstract opened by the measurement gap reviewer only. https://arxiv.org/abs/2502.05352
- Yao et al. (2024), τ-bench. Abstract opened by the measurement gap reviewer only. https://arxiv.org/abs/2406.12045
- OSWorld (2024): abstract numbers (369 tasks; humans 72.36%, best model 12.24%) confirmed by a verifier, but the URL was not recorded in the digest (unverified citation details).
- Lifland, Jurkovic; Kokotajlo et al. (2025), AI 2027 / AI Futures model. https://ai-2027.com/research/timelines-forecast ; https://blog.aifutures.org/p/ai-futures-model-dec-2025-update
- Montgomery, Lüders, Maalej (2022), Public Jira Dataset; Alhamed, Storer (2022), JOSSE. https://arxiv.org/abs/2201.08368 ; https://zenodo.org/doi/10.5281/zenodo.5882881 ; https://zenodo.org/records/7022735
- Li, Zhang, Hassan (2025), AIDev. https://arxiv.org/abs/2507.15003 ; https://huggingface.co/datasets/hao-li/AIDev
- Nakashima et al. (2026), "Why Agentic-PRs Get Rejected". https://arxiv.org/html/2602.04226v1
- Pinna, Gong, Williams, Sarro (2026), task-stratified PR acceptance. https://arxiv.org/abs/2602.08915
- Watanabe et al. (2025), "On the Use of Agentic Coding". https://arxiv.org/html/2509.14745v3
- Mozannar, Bansal, Fourney, Horvitz (2024), CUPS. https://arxiv.org/abs/2210.14306
- Sadowski et al. (2018), "Modern Code Review: A Case Study at Google". https://sback.it/publications/icse2018seip.pdf
- Bacchelli, Bird (2013), "Expectations, Outcomes, and Challenges of Modern Code Review". https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ICSE202013-codereview.pdf
- Czerwonka, Greiler, Tilford (2015), "Code Reviews Do Not Find Bugs". https://www.microsoft.com/en-us/research/wp-content/uploads/2015/05/PID3556473.pdf
- Kemerer, Paulk (2009), PSP review data. https://doi.org/10.1109/TSE.2009.27
- SmartBear, "Best Practices for Code Review". https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/
- Frömmgen, Kharatyan (2023), "Resolving code review comments with ML". https://research.google/blog/resolving-code-review-comments-with-ml/
- Cihan et al. (2024/2025), "Automated Code Review In Practice". https://arxiv.org/abs/2412.18531
- Faros AI (2025; Q2 2026). https://www.faros.ai/blog/ai-software-engineering ; https://www.faros.ai/research/ai-acceleration-whiplash
- Niederhoffer et al. (2025), "AI-Generated 'Workslop'". https://hbr.org/2025/09/ai-generated-workslop-is-destroying-productivity ; https://www.betterup.com/workslop
- Perry, Srivastava, Kumar, Boneh (2023), "Do Users Write More Insecure Code with AI Assistants?". https://arxiv.org/abs/2211.03622
- Buçinca, Malaya, Gajos (2021), "To Trust or to Think". https://arxiv.org/abs/2102.09692
- Vasconcelos et al. (2023), "Explanations Can Reduce Overreliance". https://arxiv.org/abs/2212.06823
- Bansal et al. (2021), "Does the Whole Exceed its Parts?". https://arxiv.org/abs/2006.14779
- Lee et al. (2025), "The Impact of Generative AI on Critical Thinking". https://www.microsoft.com/en-us/research/wp-content/uploads/2025/01/lee_2025_ai_critical_thinking_survey.pdf
- Barke, James, Polikarpova (2023), "Grounded Copilot". https://arxiv.org/abs/2206.15000
- Huang, Xiao, Vishnoi (2026), "Delegation and Verification under AI". https://arxiv.org/html/2603.02961
- Catalini, Hui, Wu (2026), "Some Simple Economics of AGI". https://arxiv.org/abs/2602.20946
- Raghu et al. (2019), "The Algorithmic Automation Problem". https://arxiv.org/abs/1903.12220
- Mozannar, Sontag (2020), "Consistent Estimators for Learning to Defer". https://arxiv.org/abs/2006.01862
- Geifman, El-Yaniv (2017), "Selective Classification for Deep Neural Networks". https://arxiv.org/abs/1705.08500
- Lykouris, Weng (2024), "Learning to Defer in Congested Systems". https://arxiv.org/abs/2402.12237
- Ong et al. (2025), RouteLLM. https://arxiv.org/abs/2406.18665
- Chuang et al. (2025), "Learning to Route LLMs with Confidence Tokens". https://arxiv.org/abs/2410.13284

### Section 5: Usage and adoption data
- Handa et al. (2025), Anthropic Economic Index report 1. https://arxiv.org/abs/2503.04761
- Anthropic (2025), "AI's impact on software development". https://www.anthropic.com/research/impact-software-development
- Appel, McCrory, Tamkin et al. (2025), September 2025 report. https://www.anthropic.com/research/anthropic-economic-index-september-2025-report
- Tamkin, McCrory (2025), "Estimating AI productivity gains from Claude conversations". https://www.anthropic.com/research/estimating-productivity-gains
- Appel, Massenkoff, McCrory et al. (2026), "Economic primitives". https://www.anthropic.com/research/anthropic-economic-index-january-2026-report ; https://www.anthropic.com/research/economic-index-primitives
- Massenkoff, Lyubich, McCrory et al. (2026), "Learning curves". https://www.anthropic.com/research/economic-index-march-2026-report
- Massenkoff et al. (2026), "Cadences". https://www.anthropic.com/research/economic-index-june-2026-report
- Anthropic Economic Index data. https://huggingface.co/datasets/Anthropic/EconomicIndex
- Chatterji et al. (2025), "How People Use ChatGPT". https://www.nber.org/papers/w34255
- Bick, Blandin, Deming (2024/2026), "The Rapid Adoption of Generative AI". https://www.nber.org/papers/w32966
- Bick, Blandin, Deming (2025), St. Louis Fed posts; FRED series and blog. https://www.stlouisfed.org/on-the-economy/2025/feb/impact-generative-ai-work-productivity ; https://www.stlouisfed.org/on-the-economy/2025/nov/state-generative-ai-adoption-2025 ; https://fred.stlouisfed.org/data/RPSGENAITSALL ; https://fred.stlouisfed.org/data/RPSGENAIASSISTWRKHRSALL ; https://fred.stlouisfed.org/blog/2026/08/does-generative-ai-save-time-at-work/
- Humlum, Vestergaard (2025/2026), "Large Language Models, Small Labor Market Effects" / "Still Waters, Rapid Currents". https://bfi.uchicago.edu/wp-content/uploads/2025/04/BFI_WP_2025-56-3.pdf ; https://www.nber.org/papers/w33777
- Grundy, Breaux, Khatiwoda (2026), Census BTOS story. https://census.gov/library/stories/2026/05/ai-use-businesses.html
- Allen (2026), "Monitoring AI Adoption in the U.S. Economy". https://www.federalreserve.gov/econres/notes/feds-notes/monitoring-ai-adoption-in-the-u-s-economy-20260403.html

### Section 6: Aggregation models and task theory
- Hulten (1978), "Growth Accounting with Intermediate Inputs". https://ideas.repec.org/a/oup/restud/v45y1978i3p511-518..html
- Baqaee, Farhi (2019), "The Macroeconomic Impact of Microeconomic Shocks". https://econometricsociety.org/publications/econometrica/browse/2019/07/01/macroeconomic-impact-microeconomic-shocks-beyond-hultens
- Acemoglu (2024/2025), "The Simple Macroeconomics of AI". https://www.nber.org/papers/w32487 ; https://economics.mit.edu/sites/default/files/2024-05/The%20Simple%20Macroeconomics%20of%20AI.pdf
- Aghion, Bunel (2024), "AI and Growth: Where Do We Stand?". https://www.frbsf.org/wp-content/uploads/AI-and-Growth-Aghion-Bunel.pdf
- Filippucci, Gal, Laengle, Schief, Unsal (2025), IPM No. 48. https://csls.ca/wp-content/uploads/ipm-archive/IPM48.pdf
- Briggs, Kodnani (2023); Briggs, Dong (2025–26), Goldman Sachs (press coverage; primary not opened). https://sg.news.yahoo.com/generative-ai-could-hit-300-205539542.html
- Arnon (2025), Penn Wharton Budget Model. https://budgetmodel.wharton.upenn.edu/issues/2025/9/8/projected-impact-of-generative-ai-on-future-productivity-growth
- Erdil, Potlogea, Besiroglu et al. (2025), GATE. https://arxiv.org/abs/2503.04941
- Erdil, Besiroglu (2023), "Explosive growth from AI automation". https://arxiv.org/abs/2309.11690v3
- Korinek, Suh (2024), "Scenarios for the Transition to AGI". https://arxiv.org/abs/2403.12107
- Acemoglu, Restrepo (2018), "The Race between Man and Machine". https://www.aeaweb.org/articles?id=10.1257/aer.20160696
- Acemoglu, Restrepo (2022), "Tasks, Automation, and the Rise in US Wage Inequality". https://www.nber.org/papers/w28920
- Autor, Chin, Salomons, Seegmiller (2024), "New Frontiers". https://www.nber.org/papers/w30389
- Grossman, Rossi-Hansberg (2008), "Trading Tasks". https://www.aeaweb.org/articles?id=10.1257/aer.98.5.1978
- Agrawal, Gans, Goldfarb (2019), "Artificial Intelligence: The Ambiguous Labor Market Impact of Automating Prediction". https://www.aeaweb.org/articles?id=10.1257/jep.33.2.31
- Garicano (2000), "Hierarchies and the Organization of Knowledge in Production". https://ideas.repec.org/a/ucp/jpolec/v108y2000i5p874-904.html
- Ide, Talamas (2025), "Artificial Intelligence in the Knowledge Economy". https://arxiv.org/abs/2312.05481
- Autor, Thompson (2025), "Expertise". https://www.nber.org/papers/w33941
- Gans, Goldfarb (2026), "O-Ring Automation". https://www.nber.org/papers/w34639
- Demirer, Horton, Immorlica, Lucier, Shahidi (2026), "Chaining Tasks, Redefining Work". https://www.nber.org/papers/w34859 ; https://arxiv.org/abs/2606.15960

### Section 7: IT services and BPO evidence
- World Bank (2025), South Asia Development Update, Oct 2025. https://thedocs.worldbank.org/en/doc/e59d0c80ed5c4a928630c9d2295ea0ad-0360012025/original/SADU25b-Full-Version-10-3-2025.pdf
- Betai, Chen (2026), "Automation without Borders" (slides). https://thedocs.worldbank.org/en/doc/2770aa5def57e42a6d2449c90d6cf974-0070062026/original/10-Chen.pdf
- World Bank (2026), World Development Report 2026 (doi 10.1596/978-1-4648-2331-2). https://www.donorplatform.org/wp-content/uploads/2026/08/World-Development-Report-2026-The-Promise-of-Artificial-Intelligence-1.pdf
- Cucio, Hennig (2025), IMF WP on the Philippines. https://www.imf.org/en/publications/wp/issues/2025/02/21/artificial-intelligence-and-the-philippine-labor-market-mapping-occupational-exposure-and-562171
- Huang, Liu, Wang, Yu (2026), "Who Takes the Hit?" (seminar abstract only). https://amro-asia.org/amro-cafe-seminar-who-takes-the-hit-the-uneven-impacts-of-generative-ai-on-labor-demand-across-countries
- Hui, Reshef, Zhou (2024), Upwork freelancers. https://www.ifo.de/DocDL/cesifo1_wp10601.pdf
- Demirci, Hannane, Zhu (2025), "Who Is AI Replacing?". https://spiral.imperial.ac.uk/entities/publication/88113a91-b994-4717-8526-dadac657f1cb
- Brynjolfsson, Chandar, Chen (2026), "Canaries in the Coal Mine?". https://digitaleconomy.stanford.edu/app/uploads/2026/08/Canaries_August2026.pdf
- Hampole, Papanikolaou, Schmidt, Seegmiller (2025), "Artificial Intelligence and the Labor Market". https://www.nber.org/system/files/working_papers/w33509/w33509.pdf
- Hosseini, Lichtinger (2026), "Generative AI as Seniority-Biased Technological Change" (SSRN 5425555). https://raw.githack.com/s-mahdihosseini/Website/b99fa2962dcc4c165bbc3c41dd283afa99c5ccfb/GenAI_SenBTC_May_2026.pdf
- Chandar, Klein Teeselink (2026), "How Does AI Change Labor Demand?". https://digitaleconomy.stanford.edu/app/uploads/2026/09/HowDoesAIChangeLaborDemand.pdf
- Acemoglu, Autor, Hazell, Restrepo (2022), "Artificial Intelligence and Jobs: Evidence from Online Vacancies". https://www.nber.org/papers/w28257
- Borri, Liu, Tsyvinski (2026), "The Cross-Section of Stock Returns and AI Exposure". https://arxiv.org/pdf/2606.30583
- Mishra, Kedia, Reddy, Fernandez, Khanduri (2026), ICRIER "AI and Jobs". https://icrier.org/pdf/AI-and-Jobs.pdf
- EY India (2025), "The AIdea of India 2025" and IT survey (press). https://www.ey.com/content/dam/ey-unified-site/ey-com/en-in/newsroom/2025/ey-the-aidea-of-india-2025-how-much-productivity-can-genai-unlock-in-india.pdf ; https://tele.net.in/genai-to-boost-indias-it-industry-productivity-by-43-45-per-cent-over-next-five-years-says-ey-indias-survey/
- HCLTech (2026), Q4 FY26 earnings call transcript. https://nsearchives.nseindia.com/corporate/HCLTECH_24042026174011_TranscriptEarningsCall.pdf
- Infosys (2026), Q4 FY26 call transcript (SEC 6-K exhibit). https://www.sec.gov/Archives/edgar/data/0001067491/000106749126000018/exv99w05.htm
- TCS (2026), Q2 FY27 earnings call transcript. https://nsearchives.nseindia.com/corporate/TCS_CORPCS_14102026155941_SEInt14102026_signed.pdf
- Kotak Institutional Equities (2026), via ANI. https://www.newkerala.com/news/a/ai-deflation-weak-demand-keep-large-it-growth-314.htm
- Jefferies (2025–26), via press. https://www.wionews.com/business-economy/ai-to-impact-20-of-existing-it-services-revenues-by-fy30-report-1757680298162/amp
- ICICI Securities (2026), "Indian IT Sector Analysis 2026". https://www.icicidirect.com/research/equity/finace/indian-it-sector-analysis-2026-valuation-growth-ai-risks-and-top-picks
- Cognizant CEO (2025), via Outlook Business. https://www.outlookbusiness.com/amp/story/news/newscognizant-ceo-says-ai-now-writes-20-of-code-boosts-developer-productivity-by-34
- Banerjee, Duflo (2000), "Reputation Effects and the Limits of Contracting". https://academic.oup.com/qje/article-lookup/doi/10.1162/003355300554962
- Arora, Asundi (1999), "Quality Certification and the Economics of Contract Software Development". https://www.nber.org/papers/w7260
- Eichengreen, Gupta (2011), "The Service Sector as India's Road to Economic Growth". https://www.nber.org/papers/w16757
- Jensen (2012), "Do Labor Market Opportunities Affect Young Women's Work and Family Decisions?". https://academic.oup.com/qje/article-lookup/doi/10.1093/qje/qjs002

### Section 9: Measurement agendas
- Brynjolfsson, Korinek, Agrawal (2025), "A Research Agenda for the Economics of Transformative AI". https://www.nber.org/system/files/working_papers/w34256/w34256.pdf
- Coyle, Poquiz (2025), "Making AI Count". https://www.nber.org/system/files/working_papers/w34330/w34330.pdf
- Machovec, Rieley, Rolen (2025), "Incorporating AI impacts in BLS employment projections". https://www.bls.gov/opub/mlr/2025/article/incorporating-ai-impacts-in-bls-employment-projections.htm
