---
title: How much labor can AI save? A model for θ<sub>j</sub> in Indian IT and BPO
byline: Niranjan Deshpande · October 2026 · Working draft
thanks: Written as part of SPAR (Fall 2026), supervised by Andrei Potlogea. Literature summaries below come from our 26 October literature review; anything marked “unverified” there is marked here too.
---

<!--
HOW THIS FILE WORKS
`python3 scripts/final/build_theta_model.py` turns this file into docs/theta-model.html.
  - $...$ is inline math and $$...$$ (on its own line) is display math; both are rendered with KaTeX.
  - Write a literal dollar sign as \$.
  - ## headings are numbered automatically, except "Sources"; ## and ### headings go in the contents.
-->

## The question

Our health check found that employment in Indian IT and BPO is roughly flat so far. To forecast what happens next, we use

$$g_L = d - s\,(1 - \varepsilon\varphi),$$

where $s$ is the share of labor AI removes at fixed output. So the forecast is only as good as our estimate of $s$, and $s$ depends on how much labor AI can save on the work these firms actually do.

We want to estimate that saving for each service line $j$ (application maintenance, testing, infrastructure, BPO, and so on):

- $\theta_j(t)$ is the fraction of labor hours saved on service line $j$ at full adoption, with the AI available at date $t$, net of failures and human review.
- $S(t) = \sum_j w_j\,\theta_j(t)$ is the sector-wide version, where $w_j$ is line $j$'s share of labor hours.

The existing literature doesn't give us this number. Exposure indices (e.g. Eloundou et al.) label whether AI *could* cut a task's time by at least 50%; those labels are beliefs, never checked against measured times, and nothing is netted out for review or failure. Macro estimates (e.g. Acemoglu) multiply an exposure share by a cost saving of ~27%, taken from a few 2023 experiments and held constant. That saving doesn't move when models get better, which is the thing we most want to forecast.

So the goal is a θ_j that (1) is tied to measured AI capability, so it moves with $t$, (2) counts the human time spent reviewing and fixing AI output, and (3) depends on how long tasks are, since AI succeeds much more often on short tasks than on long ones.

## The model

### One task

Assume a task takes a firm employee $h$ hours. There are two ways AI can help: it can *assist* (the human does the task with AI help), or it can do the *whole task* (the human delegates and then reviews).

**Assist.** The task takes $(1-\kappa)h$ hours, so the saving is $\kappa$.

**Delegate.** The AI produces output, which costs no human time. Then one of three things happens:

| Outcome | Probability | Review time (share of $h$) | Work left (share of $h$) |
|---|---|---|---|
| Fails automated checks | $1 - p_j$ | $\rho_F \approx 0$ | $R_F \approx 1$ |
| Passes checks, reviewer rejects | $p_j - \pi_j$ | $\rho_R$ | $R_R$ |
| Accepted | $\pi_j$ | $\rho_A$ | $R_A \approx 0$ |

Here $p_j$ is the chance the output passes automated checks and $\pi_j$ is the chance it's accepted. A few things are worth saying about the rows:

- If the output fails its tests, nobody needs to read it; the human just does the task.
- If a reviewer rejects it, they can often stop at the first fatal flaw, so $\rho_R$ can be below full review. But a subtly wrong output can take *longer* to diagnose than a correct one takes to approve.
- A rejected attempt usually gives some head start, so $R_R$ can be well below 1. It can also be above 1, if the AI's approach sends the human down the wrong path.

Whatever work is left, the human does with AI assistance, so it costs $(1-\kappa)$ per unit. Averaging over the three outcomes:

$$\bar\rho = \pi_j\,\rho_A + (p_j - \pi_j)\,\rho_R + (1 - p_j)\,\rho_F$$

$$\bar R = \pi_j\,R_A + (p_j - \pi_j)\,R_R + (1 - p_j)\,R_F$$

$$\text{saving}_D = 1 - \bar\rho - \bar R\,(1-\kappa)$$

The intuition: you pay for review ($\bar\rho$), and whatever work is left you do in assist mode ($\bar R(1-\kappa)$). Importantly, θ depends on the outcome table only through these two averages. Our first draft, $\kappa + qp(1-\kappa) - \rho$, is the special case where review costs the same in every row, $R_A = 0$, and every rejection means a full redo. (Every time cost here is proportional to $h$, so $h$ cancels when we write savings as a share of $h$. It comes back in two places: $p_j$ and $\pi_j$ depend on $h$, and review cost doesn't scale one-for-one with $h$; see below.)

**Choosing a mode.** The firm delegates when that's cheaper, counting inference cost. Let $\omega$ be the loaded wage (what an hour of an employee costs the firm: salary plus benefits, payroll contributions and per-head overhead), $c_{\text{agent}}(h)$ the cost of the agent run (tokens, tool calls, retries), and $c_A(h)$ the cost of assistance when a human does the task. If the AI's output is rejected, the human finishes the remaining work with assistance, so delegating costs $c_{\text{agent}}(h) + \bar R\,c_A(h)$ in AI spend. So the firm delegates if

$$\omega h\,\big[(1-\kappa) - \bar\rho - \bar R(1-\kappa)\big] > c_{\text{agent}}(h) - (1 - \bar R)\,c_A(h).$$

The left side is the labor cost saved by delegating instead of assisting; the right side is the extra AI spend.

θ then counts the *hours* saved under whichever mode wins. Inference cost changes which mode is chosen, but it isn't itself hours, so it doesn't go inside θ (more on where it does go below). With no inference cost, this is just $\max\{\text{saving}_D, \kappa\}$.

### Where $p_j$ and $\pi_j$ come from

We take the capability curve from METR's time-horizon work. For a task that takes METR's baseliners $h$ hours, the chance an AI agent passes is a logistic in log task length:

$$p_{\text{METR}}(h,t) = \sigma\big(\beta\,[\ln H_{50}(t) - \ln h]\big),$$

where $H_{50}(t)$ is the length at which the best model at $t$ succeeds half the time, and $\beta$ is how steeply success falls with length.

Two adjustments get us from METR's setting to ours, and both turn out to be rescalings of $h$.

**Context ($m_j$).** METR's baseliners are outside contractors with no context on the codebase; they took 5–18× longer than the repositories' own maintainers. A firm engineer on a long-running client account is somewhere in between. So a ticket logged at $h$ hours is roughly an $m_j h$-hour task in METR's units:

$$p_j(h,t) = p_{\text{METR}}(m_j h,\ t).$$

**Reviewer standards ($k_j$, $q_0$).** Passing tests isn't the same as being accepted. Our first draft modeled this with a flat multiplier, $\pi = q\,p$. We think a *horizon shift* is closer to the truth:

$$\pi_j(h,t) = q_0\; p_{\text{METR}}(m_j k_j\, h,\ t),$$

where $k_j$ is how much longer reviewer standards make a task effectively, and $q_0$ (close to 1) covers rejections unrelated to task length (e.g. "we don't want this feature").

### Why a horizon shift and not a multiplier

The two forms disagree about *where* review bites. A flat $q = 0.5$ says half of all agent output gets rejected even on 10-minute tasks, and that acceptance can never exceed 50% however good models get. A shift says short tasks are almost always accepted and long tasks are rejected much more often. We think the shift is more plausible, for three reasons.

**1. A simple mechanism produces it exactly.** Suppose each hour of work carries a constant chance $\lambda$ of failing the tests (Ord's constant-hazard model), and a reviewer checks things tests don't (conventions, edge cases, design choices), so each hour also carries a chance $\mu$ of an objection. Then

$$\pi(h) = e^{-(\lambda + \mu)h} = e^{-\lambda (k h)} = p(kh), \qquad k = 1 + \frac{\mu}{\lambda}.$$

A reviewer whose objections pile up with the amount of work *is* a horizon shift. (Under the logistic curve this holds approximately rather than exactly.) A flat multiplier needs rejections that have nothing to do with the work, like a coin flip; some rejections are like that, which is what $q_0$ is for, but it's hard to see why most would be.

**2. The one direct measurement looks like a shift.** Whitfill et al. (METR, Mar 2026) had maintainers review agent PRs that had passed SWE-bench Verified's tests. Refitting Sonnet 4.5's horizon on maintainer verdicts gives about 8 minutes instead of about 50, i.e. $k \approx 7$. (We don't know whether the slope $\beta$ was the same under both scorings; if it wasn't, the effect isn't a pure shift.)

**3. Short tasks get accepted at high rates in practice.** In deployment, Claude Code PRs were merged 83.8% of the time vs 91.0% for matched human PRs (Watanabe et al.). That's far from the ~50% a flat $q$ predicts. This is weak evidence, though: those PRs weren't conditioned on passing tests, and people choose what to delegate.

A clean test would be to take agent PRs that pass their tests and check whether the acceptance rate falls with task size. Under a multiplier it stays flat; under a shift it falls.

### Frictions as a lag

Because the curve is a logistic in $\ln h$, rescaling $h$ by a constant just divides the horizon: with $D_j = m_j k_j$, the effective horizon for accepted work is $H_{50}(t)/D_j$. And since horizons have doubled every $T_d \approx 129$ days since 2023, dividing by $D_j$ is the same as using the frontier from $L_j$ days earlier:

$$\pi_j(h,t) = q_0\; p_{\text{METR}}(h,\ t - L_j), \qquad L_j = T_d \log_2 D_j.$$

| $D_j$ | Lag $L_j$ |
|---|---|
| 7 (reviewer standards only) | ≈ 1.0 year |
| 20 | ≈ 1.5 years |
| 126 ($m_j = 18$, $k_j = 7$) | ≈ 2.5 years |

That is, "Indian AMS work runs about $L_j$ years behind the METR frontier." The same logic gives a shorter lag for passing checks, $T_d \log_2 m_j$.

This has two useful consequences:

- **Frictions delay savings; they don't cap them.** If the trend continues, $\pi_j \to q_0$ for any fixed task length, so the delegate saving approaches roughly $1 - \rho_A$. Under the flat multiplier it's stuck below $q(1-\kappa) + \kappa - \rho \approx 0.28$ at central values, forever. So for the long run, the parameters that matter most are review cost and whether the trend continues, not $m_j$ or $k_j$.
- **It matches what the data can identify.** Our top-down series (realized replacement of roughly 2.3 pp/yr over FY24–26) gives about one equation, so it can pin down roughly one composite parameter, and $L_j$ is that parameter. Separating $m_j$ from $k_j$ needs ticket-level data that records whether automated checks passed.

Of course, this all leans on the doubling trend. If horizons stop doubling, $D_j$ is still a discount but no longer a fixed delay. And $D_j$ may not be constant: if reviewers get stricter with AI output, or context matters more on long tasks, a single lag is too simple.

### Review cost

Review time probably isn't proportional to task length. At Google, a median 24-line change takes a reviewer roughly 45–50 minutes, which suggests a large fixed cost per change. So

$$\rho_A(h) = \frac{a}{h} + b,$$

with a fixed part $a$ (in hours) and a proportional part $b$. We'll report the $a = 0$ and $b = 0$ corners. For rejections, $\rho_R = \tau\,\rho_A$ with $\tau \in (0, 1]$, and $\rho_F \approx 0$.

### Putting it together

For a task of length $h$ in line $j$ at date $t$, the extra hours saved by delegating instead of assisting, as a share of $h$, are

$$\Delta_j(h,t) = (1-\kappa) - \bar\rho(h,t) - \bar R(h,t)\,(1-\kappa),$$

and the firm delegates ($\delta_j = 1$) when that saving beats the extra AI spend:

$$\delta_j(h,t) = \mathbb{1}\Big\{\, \omega h\,\Delta_j(h,t) > c_{\text{agent}}(h) - \big(1-\bar R(h,t)\big)\,c_A(h) \Big\}.$$

Integrating over the hours-weighted distribution of task lengths in each line gives the share of hours saved:

$$\theta_j(t) = \int \big[\,\kappa + \delta_j(h,t)\,\Delta_j(h,t)\,\big]\, f_j(h)\, dh.$$

That is, every task gets the assist saving, and delegated tasks get the extra saving on top. (With no inference cost, $\delta_j = 1$ exactly when $\Delta_j > 0$, and this is just $\int \max\{1 - \bar\rho - \bar R(1-\kappa),\ \kappa\}\, f_j(h)\, dh$.)

θ is pure hours, which is what $s$ measures; mixing dollars in would break the units. But the price channel depends on the *cost* saving: labor cost saved, net of AI spend.

$$\theta^c_j(t) = \theta_j(t) - \int \frac{c_A(h) + \delta_j(h,t)\,\big[c_{\text{agent}}(h) - (1-\bar R)\,c_A(h)\big]}{\omega h}\, f_j(h)\, dh$$

The second term is AI spend as a share of the labor cost the task would have had: $c_A$ if assisted, $c_{\text{agent}} + \bar R\,c_A$ if delegated.

Summing over lines,

$$S(t) = \sum_j w_j\,\theta_j(t), \qquad S^c(t) = \sum_j w^c_j\,\theta^c_j(t),$$

where $w_j$ are hours shares and $w^c_j$ are labor-cost shares (they coincide if wages are the same across lines). There's also a non-task bucket (bench, training, sales, coordination) with weight $w_0$ and $\theta_0 = \theta^c_0 = 0$; leaving it out overstates $S$.

### How this feeds the rest of the project

As agreed, adoption is set to 1, so $S$ and $S^c$ are full-adoption ceilings, and $s = S$. Adoption only comes back in when we validate against realized data, through $s(t) = \sum_j w_j A_j(t)\,\theta_j(t)$.

Inference cost enters the forecast through prices. If $\varphi$ is defined relative to labor cost saved, the forecasting equation becomes

$$g_L = d - S + \varepsilon\varphi\, S^c.$$

Since $S^c \approx S - \bar c$, where $\bar c$ is AI spend as a share of the labor bill, this is the same as $g_L = d - s + \varepsilon\varphi\,(s - \bar c)$. (We still need to check this against how the CES micro-foundation defines $\varphi$.)

### Parameters at a glance

| Parameter | Meaning | Current best value | Main gap |
|---|---|---|---|
| $p_{\text{METR}}(h,t)$ | Chance AI passes checks on a task of METR length $h$ | Frontier $H_{50}$ ≈ 6–12 h; doubling ≈ 129 days | Software only; unreliable above 16 h |
| $m_j$ | Context gap: METR hours per firm hour | Prior 1–18 | No direct measurement |
| $k_j$ | Reviewer standards as a horizon shift | ≈ 7 | One model, three repos, four reviewers |
| $q_0$ | Length-independent rejections | Close to 1 (prior) | No direct estimate |
| $\rho_A(h)$ | Review time on accepted output | 0.1–0.33; GDPval 0.27 | Not measured against $h$ |
| $\rho_R, \rho_F$ | Review time on rejected / check-failing output | $\rho_F \approx 0$; $\rho_R$ unknown | Nothing measures time to rejection |
| $R_A, R_R, R_F$ | Work left after each outcome | $R_R$ ≈ 1/3–1/2 (Rein, n = 4) | Almost no data; sign of the head start uncertain |
| $\kappa$ | Assist speedup | ≈ 0.15–0.25 for 2022–24 coding tools | Current tools unmeasured |
| $f_j(h)$ | Hours-weighted task-length distribution | None for India | The biggest data gap |
| $w_j, w_0, w^c_j$ | Hours shares (and labor-cost shares) | From revenue splits | Revenue ≠ hours |
| $\omega$ | Loaded wage | ≈ \$16/h, blended onsite and offshore | Unverified; offshore probably lower |
| $c_{\text{agent}}(h)$ | AI cost of a delegated attempt | ≈ \$4 for a 1-hour task | A single point; growth with $h$ unknown |
| $c_A(h)$ | AI cost of assistance | Small at the margin (per-seat pricing) | No direct estimate |

### What the model leaves out

- **Routing ticket by ticket.** We assume firms choose a mode based on $h$ alone. If they can predict which tickets the AI will get right, they do better; if weak reviewers over-delegate, they do worse.
- **Task splitting.** We treat $f_j(h)$ as fixed, but firms can split a long task into chunks that fit the horizon, paying review per chunk (Demirer et al. 2026). This biases θ down for long tasks.
- **Time saved vs. labor removed.** Danish survey data suggest about 80% of saved time goes to other tasks (Humlum & Vestergaard). Some of that is the demand response, which $\varepsilon\varphi$ handles; some is reallocation inside the firm, which it doesn't.
- **Downstream rework.** AI-written code may cost more to maintain later (the CMU Cursor study finds velocity gains fade within two months while complexity rises). This matters for AMS, which inherits other people's code.
- **Whose hours.** Juniors save the most time and seniors do the review, so hours-weighted and cost-weighted θ can differ.
- **Large shocks.** $S = \sum w_j \theta_j$ is first-order (Hulten). With large savings, the weights themselves shift (Baqaee & Farhi), so we should also report a reweighted $S$.


## Getting to each parameter

### $p(h,t)$: the capability curve

**Best source: METR's Time Horizon 1.1 (Jan 2026), with public task-level data.** 228 software, ML and cyber tasks, each timed by human baselines, with agents run several times per task. Frontier 50% / 80% horizons: Claude Opus 4.6 719 / 70 min, Gemini 3.1 Pro 384 / 90 min, GPT-5.2 352 / 66 min. The doubling time since 2023 is 128.7 days (95% CI 104–158). The ratio of the 50% and 80% horizons implies a shallow slope, roughly 0.6–0.95 per natural-log unit of $h$ (the literature review's derivation): even with a 12-hour $H_{50}$, a model fails roughly 9–18% of 1-hour tasks. The dashboard was frozen in September 2026.

**Kwa et al. (2025)** is the original method: fit success against log human time for each model and read off the 50% length.

**Caveats that matter for us:**

- **Barry (METR, Mar 2026):** reasonable alternative fits cut recent 50% horizons by up to 35% and raise 80% horizons by up to 100%. A single slope shared across models cross-validated best. On private tasks only, Opus 4.6's $H_{50}$ falls from 12 h to 7.2 h.
- **Ord (2025):** a constant-hazard curve fits too, and curve shape changes the high-reliability tail by about 3×. Delegation needs 90%+ success, so we should report both shapes.
- **Kwa & Cheng (METR, 2025):** computer-use horizons (OSWorld, WebArena) are 40–100× shorter than software horizons. That's the closest proxy for BPO and IT-ops work, and borrowing coding curves for those lines could be off by one to two orders of magnitude.
- **Kwa (METR, Jan 2026)** is explicit that a 50% horizon of X hours doesn't mean we can delegate tasks under X hours. That's exactly the gap the rest of this model fills.

**Cross-check:** Anthropic's January 2026 Economic Index report finds API task success falls from about 60% on sub-hour tasks to about 45% at 5+ hours, crossing 50% near 3.5 h. Both success and time are judged by Claude, and users chose which tasks to bring, so it's a check, not a substitute.

**Plan:** fit a shared-slope logistic to `task_results_1_1.yaml`, bootstrap over tasks, and report a constant-hazard alternative.

### $m_j$, $k_j$, $q_0$: the discount $D_j$

**Context, $m_j$.** The only anchor is METR's own finding that contractor baseliners took 5–18× longer than repository maintainers on internal PRs. We'll use a prior of 1–18 and report $m_j = 1, 3, 10$. Nobody has measured where vendor staff on long-running accounts sit.

**Reviewer standards, $k_j$. Best source: Whitfill, Wu, Becker, Rush (METR, Mar 2026).** Four maintainers (scikit-learn, Sphinx, pytest) reviewed 296 agent PRs that had passed SWE-bench Verified's tests:

- They re-approved only 68% of the *real* merged human patches, which sets the noise floor.
- Relative to that floor, test pass rates exceed maintainer acceptance by 24.2 pp (SE 2.7); roughly half of passing PRs wouldn't be merged.
- Sonnet 4.5's horizon is ~50 min under the tests and ~8 min under maintainers, giving $k \approx 7$.
- Agents couldn't respond to feedback, so this is pessimistic for real workflows with iteration.
- Maintainer acceptance improved 9.6 pp/yr more slowly than test scores (SE 5.5, significant only at 10%). If real, the gap is widening, which neither a pure shift nor a flat multiplier captures.

**Deployment merge rates** bracket this from the other side, though they aren't conditioned on passing tests and are shaped by what people choose to delegate. Watanabe et al.: 83.8% for Claude Code PRs vs 91.0% for matched human PRs; about 45% of merged agent PRs were revised before merge, but so were ~41.5% of human PRs. Nakashima et al.: agent PRs merged 55–86% vs 82.6% for humans. **AIDev** (7.69M agent PRs, public) makes it possible to estimate acceptance by PR size and month, which is the test of shift vs multiplier above.

**Length-independent rejections, $q_0$.** No direct estimate. The deployment numbers suggest it's close to 1, but they're confounded.

**For Indian delivery,** there's a second review layer: client acceptance (UAT, change boards). Nothing in the literature measures it, and it plausibly raises $k_j$.

### $\rho$: review cost

**Best single figure: GDPval (OpenAI, 2025).** Expert graders took 109 minutes against 404 minutes of expert completion time, so $\rho \approx 0.27$ (0.19–0.27 depending on which reported task length is the denominator). This is grading time in an evaluation, not production review.

**Other anchors:**

- **Rein (METR, Aug 2025):** estimated fix time of ~26 minutes for 4 test-passing agent PRs and ~42 minutes across all reviewed PRs, against tasks averaging 1.3 hours.
- **METR's 2025 RCT (screen recordings):** about 9% of AI-allowed time went to reviewing and cleaning AI output, plus 4% waiting.
- **CUPS (Mozannar et al., 2024):** Copilot users spent 22.4% of session time verifying suggestions (34.3% including editing). Verification per suggestion was about 5× the naive estimate, because people accept first and check later.

**Evidence for a fixed cost per change.** At Google (Sadowski et al. 2018), reviewers spend about 3.2 hours a week on about 4 changes, with a median change of 24 lines: roughly 45–50 minutes per change. That's far slower per line than inspection norms of 200–500 lines/hour, which suggests a fixed cost dominates for small changes. Hence $\rho_A(h) = a/h + b$.

**Review and acceptance are chosen together.** Reviewers can trade checking time for false acceptances. Over-reliance rises with task difficulty and falls with higher stakes and cheaper verification (Vasconcelos et al.); AI users wrote less secure code while believing it more secure (Perry et al.). Also, only 14–15% of human review comments concern defects (Bacchelli & Bird; Czerwonka et al.), so passing review is a weak test of correctness.

**Gap:** nothing measures review time against task length in production, and nothing measures how fast reviewers reject. METR collected maintainer review times in its 2026 study but hasn't published them.

### $R$: the head start after a rejection

**Best (and nearly only) source: Rein (METR, Aug 2025).** Zero of 15 agent PRs on real repos were mergeable as-is, but estimated fix times were about 1/3 to 1/2 of task length rather than a full redo. That suggests $R_R$ well below 1. It's 4 test-passing PRs, the fix times are estimated rather than timed, and we only see fixes for PRs someone chose to fix.

**Bounds:** GDPval's workflow redoes every failure from scratch ($R = 1$, and without assistance). Demirer et al. (2026) model retrying and re-verifying instead.

**The sign could be negative.** In METR's 2025 RCT, experienced developers on their own repos were 19% *slower* with AI tools. That's at least consistent with AI output sending people down wrong paths, though it mixes assisting and delegating.

**Gap:** the fallback after a failed attempt has never been timed against the alternatives. With $p$ near 0.5, this choice alone moves θ a lot.

### $\kappa$: the assist speedup

**Best field estimate for coding: Cui et al. (2025/2026).** Field RCTs at Microsoft, Accenture (Southeast Asia) and a Fortune 100 firm, 4,867 developers, 2022–23 autocomplete: completed tasks +26% (SE 10.3%), so about 21% of labor saved per task. Juniors gained more.

**Others:**

- **Google RCT (Paradis et al., 2024):** ~21% faster on an "extend existing code" task; the CI includes zero.
- **METR early-2025 RCT:** experts on their own code were 19% slower (CI +2% to +39%), while *believing* they were 20% faster.
- **METR Feb 2026 update:** estimated speedups of 18% and 4% for two groups, both CIs including zero. METR calls the data unreliable, partly because 30–50% of developers withheld tasks they wouldn't do without AI.
- **BPO chat:** Brynjolfsson, Li & Raymond find handle time −8.5% (resolutions/hour +15%) for 5,172 support agents; Ni et al. (Alibaba) find a 32% cut on one diagnostic step became a 4.2% cut on the whole chat.
- **Trend:** Merali finds roughly 8% less task time per year of model progress for consultants and analysts, which gives a slope for indexing κ by tool vintage.

**Plan:** use κ ≈ 0.15–0.25 for development and ≈ 0.04–0.13 for BPO chat, index it by tool vintage ($\kappa_v$), and re-estimate κ by task length from METR's public RCT data. Don't use self-reports: they get even the sign wrong.

### $f_j(h)$: task lengths

**There is no hours-weighted task-length distribution for any Indian service line.** This is probably the single biggest gap, since METR's slope is shallow and where hours sit along $h$, especially the long tail, largely sets θ_j.

**Public proxies:**

- **JOSSE and the Public Jira Dataset (Zenodo):** effort logs from open-source projects. Sparse, and we need to check JOSSE's units before trusting it.
- **SWE-bench Verified (via Epoch):** 39% of tasks under 15 minutes, 52% at 15–60 minutes, 8% at 1–4 hours. These are annotator guesses, count-weighted, for open-source bug fixes, so they're optimistic.
- **Anthropic Economic Index:** per-task means of human time, estimated by Claude. Validated on 1,000 open-source Jira tickets, Claude's estimates correlate 0.44 (Spearman) with actual times, vs 0.50 for developers' own estimates, and they compress the range.
- **Remote Labor Index:** real freelance projects with median 11.5 h and mean 28.9 h, but a mostly creative task mix.

**Why weighting matters:** Hatgis-Kessell et al. (2026) find that weighting by time spent rather than task count reshuffles 11 of the 25 occupations usually reported as most exposed.

**The real fix is firm data:** one row per ticket with logged effort hours, released only as aggregates by line and length bin.

### $w_j$ and $w_0$: hours weights

**Best source: firm service-line disclosures, already in the project repo** (`data/tidy/panel_long.csv`). The problem is that these are revenue shares, and revenue isn't hours: Infosys onsite hours bill at roughly 3× offshore (offshore was 71.3% of effort but 45.4% of revenue at Q4 FY18). We convert using the onsite premium and report intervals. Detailed splits end in 2017–19, so FY26 figures are extrapolated.

**For $w_0$,** Infosys person-month data (2010–18) are the best public source for bench, training and other non-task time.

**Context:** HCLTech said on its Q4 FY26 call that about 40% of industry spend (application development and support, traditional infrastructure, customer support) "can shrink 3% to 5% CAGR for a few years." ICRIER's survey of 620 Indian IT firms reports which divisions are most affected (software development 72%, infrastructure/cloud 48%), but direction only, no magnitudes.

### $c_{\text{agent}}$, $c_A$ and $\omega$: inference cost and the loaded wage

**Best available figure:** the literature review's derivation of ~\$16/h loaded labor cost from Infosys's FY26 20-F, under which a \$4 agent run on a 1-hour task is 25% of that task's labor cost. This is unverified, and the derivation isn't shown, so we don't know whether it includes subcontractors or overhead, or what hours per year it assumes. It's also a blended average: onsite hours cost several times more than offshore ones, and offshore was 76.8% of Infosys effort in FY26. So the offshore loaded wage is probably below \$16/h, and inference cost is a bigger share of the saving for offshore work.

**Which wage.** For the delegation decision, the right wage is the marginal cost of an hour of labor: the costs that fall when the firm needs fewer hours (salary, benefits, per-head overhead), not the ones that don't (headquarters, sales):

$$\omega = \frac{\text{employee costs} + \text{per-head overhead}}{\text{headcount} \times \text{hours worked per employee per year}}.$$

**How the two costs behave.** $c_A$ is probably small at the margin: assistant tools are often flat per-seat subscriptions, so once the seat is paid for, one more assisted task costs close to nothing. $c_{\text{agent}}$ is billed by usage and grows with $h$, possibly faster than linearly, since context accumulates over long runs and failed attempts get retried. We don't have good numbers on how fast; the \$4 figure is a single point.

Cost comparisons elsewhere use US wages (GDPval) or computer vision (Svanberg et al.), where only 23% of exposed wages were cost-effective to automate at the time.

**Why it matters for India specifically:** lower wages make inference cost a bigger share of the saving, most of all for long, retry-heavy tasks.

### Cross-checks on the result

- **Ordering across lines.** Exposure measures don't give θ, but they can check the *ordering* of θ_j. ILO Working Paper 140 (Gmyrek et al., 2025) scores 29,753 tasks from 0 to 1 for "could be done without a human operator" (software developers 0.53, applications programmers 0.57, systems administrators 0.57). It's perceived automatability with nothing netted out, so at best a loose upper bound on gross θ. Eisfeldt, Schubert & Zhang separate exposure through core vs supplemental tasks, which roughly tracks the delegate vs assist distinction.
- **A reality check for multi-hour work.** GDPval's try-and-review workflow cuts GPT-5's 90× raw speedup to 1.12–1.39×, i.e. about 11–28% of time saved, mostly because ~61% of failures had to be redone.
- **Validation against realized data.** Realized cumulative replacement over FY24–26 (≈ 7 pp, range 4.5–11) should roughly match the change in $\sum_j w_j A_j(t)\,\theta_j(t)$, with adoption $A_j(t)$ built from disclosed tool head-counts. This mostly identifies κ × adoption and the lag $L_j$; it has little power over review cost.


## Sources

- Acemoglu (2024/2025), "The Simple Macroeconomics of AI". <https://www.nber.org/papers/w32487>
- Bacchelli & Bird (2013). <https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ICSE202013-codereview.pdf>
- Barry (METR, 2026), modelling assumptions and time horizons. <https://metr.org/notes/2026-03-20-impact-of-modelling-assumptions-on-time-horizon-results/>
- Baqaee & Farhi (2019). <https://econometricsociety.org/publications/econometrica/browse/2019/07/01/macroeconomic-impact-microeconomic-shocks-beyond-hultens>
- Becker, Rush, Barnes, Rein (METR, 2025), developer RCT. <https://arxiv.org/abs/2507.09089> ; data: <https://github.com/METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs>
- Becker et al. (METR, Feb 2026), uplift update. <https://metr.org/blog/2026-02-24-uplift-update/>
- Brynjolfsson, Li, Raymond (2025). <https://www.nber.org/papers/w31161>
- Cui et al. (2025/2026), Copilot field experiments. <https://economics.mit.edu/sites/default/files/inline-files/draft_copilot_experiments.pdf>
- Czerwonka, Greiler, Tilford (2015). <https://www.microsoft.com/en-us/research/wp-content/uploads/2015/05/PID3556473.pdf>
- Demirer, Horton, Immorlica, Lucier, Shahidi (2026), "Chaining Tasks". <https://www.nber.org/papers/w34859>
- Eisfeldt, Schubert, Zhang (rev. 2026). <https://www.nber.org/papers/w31222>
- Eloundou, Manning, Mishkin, Rock (2023/2024). <https://arxiv.org/abs/2303.10130>
- Gmyrek et al. (2025), ILO WP 140. <https://www.ilo.org/publications/generative-ai-and-jobs-refined-global-index-occupational-exposure>
- Hatgis-Kessell, Aguirre, Wan, Bommasani (2026). <https://arxiv.org/abs/2608.05172>
- HCLTech Q4 FY26 call. <https://nsearchives.nseindia.com/corporate/HCLTECH_24042026174011_TranscriptEarningsCall.pdf>
- He et al. (2026), Cursor study. <https://arxiv.org/html/2511.04427v3>
- Humlum & Vestergaard (2025/2026). <https://www.nber.org/papers/w33777>
- Kwa et al. (2025). <https://arxiv.org/abs/2503.14499>
- Kwa (METR, 2026), time-horizon limitations. <https://metr.org/notes/2026-01-22-time-horizon-limitations/>
- Kwa & Cheng (METR, 2025), horizons across domains. <https://metr.org/blog/2025-07-14-how-does-time-horizon-vary-across-domains/>
- Li, Zhang, Hassan (2025), AIDev. <https://huggingface.co/datasets/hao-li/AIDev>
- Merali (2024). <https://arxiv.org/abs/2409.02391>
- METR (2026), Time Horizon 1.1. <https://metr.org/blog/2026-1-29-time-horizon-1-1/> ; data: <https://metr.org/assets/task_results_1_1.yaml>
- Mishra et al. (2026), ICRIER. <https://icrier.org/pdf/AI-and-Jobs.pdf>
- Montgomery et al. (2022), Public Jira Dataset; Alhamed & Storer (2022), JOSSE. <https://zenodo.org/doi/10.5281/zenodo.5882881> ; <https://zenodo.org/records/7022735>
- Mozannar, Bansal, Fourney, Horvitz (2024), CUPS. <https://arxiv.org/abs/2210.14306>
- Nakashima et al. (2026). <https://arxiv.org/html/2602.04226v1>
- Ni et al. (2026), Alibaba. <https://arxiv.org/pdf/2603.29888>
- Ord (2025). <https://arxiv.org/abs/2505.05115>
- Paradis et al. (2024), Google RCT. <https://arxiv.org/html/2410.12944v2>
- Patwardhan et al. (2025), GDPval. <https://arxiv.org/abs/2510.04374>
- Perry et al. (2023). <https://arxiv.org/abs/2211.03622>
- Rein (METR, 2025), algorithmic vs holistic evaluation. <https://metr.org/blog/2025-08-12-research-update-towards-reconciling-slowdown-with-time-horizons>
- Remote Labor Index (Mazeika et al., 2025). <https://arxiv.org/abs/2510.26787>
- Sadowski et al. (2018), code review at Google. <https://sback.it/publications/icse2018seip.pdf>
- Svanberg et al. (2024). <https://futuretech.mit.edu/2024-01-18+Beyond_AI_Exposure.pdf>
- Tamkin & McCrory (2025); Anthropic Economic Index (Jan 2026). <https://www.anthropic.com/research/estimating-productivity-gains> ; <https://www.anthropic.com/research/anthropic-economic-index-january-2026-report>
- Vasconcelos et al. (2023). <https://arxiv.org/abs/2212.06823>
- Watanabe et al. (2025). <https://arxiv.org/html/2509.14745v3>
- Whitfill, Wu, Becker, Rush (METR, 2026). <https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/>
