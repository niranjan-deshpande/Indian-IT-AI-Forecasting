---
title: Estimating θ<sub>j</sub>: model and data requirements
byline: Niranjan Deshpande · October 2026 · Working draft (internal)
thanks: Memo for Andrei. Sources and details for every number are in our 26 October literature review (theta_j_literature.md in the repo); anything marked “unverified” there is marked here too.
---

<!--
HOW THIS FILE WORKS
`python3 scripts/final/build_theta_model.py` turns this file into docs/theta-model.html.
  - $...$ is inline math and $$...$$ (on its own line) is display math; both are rendered with KaTeX.
  - Write a literal dollar sign as \$.
  - ## headings are numbered automatically, except "Sources"; ## and ### headings go in the contents.
-->

This is my idea for how to model $\theta_j$, the share of labor hours AI saves on service line $j$ at full adoption. A "service line" is a type of work that a BPO firm does: application maintenance, software testing, customer support, etc. Importantly, this does NOT include adoption frictions. But it DOES include the cost of failures and human review (because AI inputs are unreliable).

The rough idea is that a human worker can either *delegate* each task to AI, or complete it with *AI assistance.* We model the firm as choosing the more profitable option for each task. If a human tries to delegate the task to an AI and it fails, the human then completes it with AI assistance.

The biggest data gaps are task-length distributions $f_j(h)$ for Indian service lines, review time as a function of task length, and the work left after a rejection.

## Overview of the Model

**Why it's structured this way.** The idea is that assisting saves a modest, fairly predictable share of a task's time, while delegating saves almost all of it when the AI's output is good enough to accept. But when the AI's output is insufficient, delegation wastes the review time. Thus, delegating is much less valuable when outputs are likely to not be accepted, which depends heavily on how long the task is. This is why we work task by task, sorting them by length, then adding up and integrating.

I have two contributions here to the existing literature:

- While capability scores and general savings indices already exist, as far as I know this is the first treatment of the **costs of delegation**, like review time, rejected attempts leaving unfinished work, and agent inference costing money.
- I also construct a mapping from METR capability scores to the Indian BPO context. The difficulty is that METR measures agent pass rate in a controlled setting timed by external contractors; but we care about reviewers *in a firm* accepting changes *to their own codebases.* For reasons I discuss later, I model this as a shift to METR's frontier.

Here's the full model (will explain parameters below):

$$\theta_j(t) = \int \big[\kappa + \delta_j(h,t)\,\Delta_j(h,t)\big]\, f_j(h)\,dh$$

$$\Delta_j(h,t) = (1-\kappa) - \bar\rho(h,t) - \bar R(h,t)\,(1-\kappa)$$

$$\delta_j(h,t) = \mathbb{1}\{\omega h\,\Delta_j(h,t) > c_D(h)\}$$

$$\bar\rho = \pi_j\,\rho_A + (p_j - \pi_j)\,\rho_R + (1 - p_j)\,\rho_F$$

$$\bar R = \pi_j\,R_A + (p_j - \pi_j)\,R_R + (1 - p_j)\,R_F$$

$$p_j(h,t) = p_{\text{METR}}(m_j h,\,t), \qquad \pi_j(h,t) = q_0\,p_{\text{METR}}(m_j k_j h,\,t)$$

$$p_{\text{METR}}(h,t) = \sigma\big(\beta\,[\ln H_{50}(t) - \ln h]\big)$$

$$S(t) = \sum_{j \ge 0} w_j\,\theta_j(t), \qquad g_L = d - s + \varepsilon\varphi\,(s - \bar c), \quad s = S \text{ at full adoption}$$

In words:

- A task takes a firm employee $h$ hours, in service line $j$, with the AI available at date $t$.
- $\kappa$ is the share of time saved by assisting. $\Delta_j$ is the *extra* share saved by delegating instead, and $\delta_j = 1$ when the firm delegates.
- $p_j$ is the chance the AI's output passes automated checks, and $\pi_j$ the chance a reviewer accepts it. $\bar\rho$ is the expected review time and $\bar R$ the expected work left after the attempt, both as shares of $h$.
- $p_{\text{METR}}$ is METR's success curve; $m_j$ (missing context) and $k_j$ (reviewer standards) rescale task length, and $q_0$ covers rejections unrelated to length.
- $\omega$ is the loaded wage and $c_D(h)$ the cost of an agent run. $f_j(h)$ is the hours-weighted distribution of task lengths, $w_j$ is line $j$'s share of labor hours, and $\bar c$ is AI spend as a share of the labor bill.

In the rest of this memo, I build up each piece of this.

## One task

Assume a task takes a firm employee $h$ hours. AI can help in two ways.

**Assist.** The human does the task with AI help, taking $(1-\kappa)h$ hours, where $\kappa$ is the fraction of time the assistant saves per unit of $h$. So the saving is $\kappa$.

**Delegate.** The AI produces output, which we assume costs no human time. Let $p_j$ be the chance the output passes automated checks (tests, linters), and $\pi_j \le p_j$ the chance it passes *and* a human reviewer accepts it. Then one of three things happens:

| Outcome | Probability | Review time (share of $h$) | Work left (share of $h$) |
|---|---|---|---|
| Fails automated checks | $1 - p_j$ | $\rho_F \approx 0$ | $R_F \approx 1$ |
| Passes checks, reviewer rejects | $p_j - \pi_j$ | $\rho_R$ | $R_R$ |
| Accepted | $\pi_j$ | $\rho_A$ | $R_A \approx 0$ |

- If it fails the checks, nobody needs to read it, but nearly all the work is left.
- If it passes and the reviewer rejects it, the reviewer can often stop at the first fatal flaw, so $\rho_R$ may be below full review. (But a subtly wrong output can take longer to review than a correct one.) A rejected attempt usually gives a head start, so $R_R$ can be well below 1. It can also be above 1, if the AI's approach sends the human down the wrong path.
- If it's accepted, review is full and only small fixes are left.

Whatever work is left, the human does with assistance, at $(1-\kappa)$ per unit. Averaging over the three outcomes:

$$\bar\rho = \pi_j\,\rho_A + (p_j - \pi_j)\,\rho_R + (1 - p_j)\,\rho_F$$

$$\bar R = \pi_j\,R_A + (p_j - \pi_j)\,R_R + (1 - p_j)\,R_F$$

$$\text{saving}_D = 1 - \bar\rho - \bar R\,(1-\kappa)$$

That is, we always pay for review, and whatever is left we do in assist mode. θ depends on the outcome table only through $\bar\rho$ and $\bar R$; the three-way split matters for what data we ask firms for. Our first draft, $\kappa + qp(1-\kappa) - \rho$, is the special case where review costs the same in every outcome, $R_A = 0$, and $R_R = R_F = 1$.

**Delegate or assist?** For each task, the firm chooses between delegating it and having the human do it with assistance. Delegating saves an extra share of $h$ over assisting of

$$\Delta_j(h,t) = (1-\kappa) - \bar\rho - \bar R\,(1-\kappa).$$

But delegating also costs money: the agent run itself (tokens, tool calls, retries), $c_D(h)$. Let $\omega$ be the loaded wage (salary plus benefits and per-head overhead, per hour). The firm delegates when the labor it saves is worth more than the agent run:

$$\omega h\,\Delta_j(h,t) > c_D(h).$$

This ignores the cost of assistance itself. Assistant tools are mostly per-seat subscriptions, so one more assisted task costs close to nothing. (If it didn't, the right side would be $c_D - (1-\bar R)\,c_A$.)

So θ counts the hours saved under whichever option is cheaper for the firm, which isn't always the one that saves more hours. With no inference cost the two coincide, and the saving is $\max\{\text{saving}_D, \kappa\}$.

## Capability and acceptance

### Passing checks

We take $p$ from METR's time horizons. For a task that takes METR's baseliners $h$ hours, the chance an agent passes is a logistic in log task length:

$$p_{\text{METR}}(h,t) = \sigma\big(\beta\,[\ln H_{50}(t) - \ln h]\big),$$

where $H_{50}(t)$ is the length at which the frontier model at $t$ succeeds half the time, and $\beta$ is how steeply success falls with length.

Two things separate METR's setting from ours. Both turn out to be rescalings of $h$.

- **Context ($m_j$).** METR's baseliners are outside contractors; they took 5–18× longer than the repositories' own maintainers. A firm engineer on a long-running account is somewhere in between, so a ticket logged at $h$ hours is roughly an $m_j h$-hour task in METR's units: $p_j(h,t) = p_{\text{METR}}(m_j h,\,t)$.
- **Reviewer standards ($k_j$, $q_0$).** Passing tests isn't the same as being accepted. We write $\pi_j(h,t) = q_0\,p_{\text{METR}}(m_j k_j h,\,t)$, where $k_j$ is how much longer reviewer standards effectively make the task, and $q_0$ (close to 1) covers rejections unrelated to length, like "we don't want this feature".

### Why a horizon shift, not a flat q

A flat $q = 0.5$ says half of agent output gets rejected even on 10-minute tasks. It also caps the delegate saving at $q(1-\kappa) + \kappa - \rho \approx 0.28$ (at $\kappa = 0.1$, $\rho = 0.27$), however good models get. A shift says short tasks are almost always accepted and long ones often aren't. We think the shift is closer to the truth, for three reasons:

1. **A simple mechanism produces it.** If each hour of work carries a constant chance $\lambda$ of failing the tests (Ord's constant-hazard model) and a chance $\mu$ of a reviewer objection, then $\pi(h) = e^{-(\lambda+\mu)h} = p(kh)$ with $k = 1 + \mu/\lambda$. Objections that pile up with the amount of work *are* a horizon shift. (Under the logistic this holds only approximately.)
2. **The one direct measurement looks like a shift.** In Whitfill et al. (METR, Mar 2026), maintainers reviewed SWE-bench-passing PRs. Sonnet 4.5's horizon falls from about 50 minutes under the tests to about 8 under maintainers, so $k \approx 7$. We don't know whether the slope changed too.
3. **Short agent PRs get merged at high rates.** Claude Code PRs were merged 83.8% of the time vs 91.0% for matched human PRs (Watanabe et al.), far above 50%. This is weak evidence: those PRs weren't conditioned on passing tests, and people choose what to delegate.

The clean test is whether acceptance falls with PR size among agent PRs that pass their tests. Under a multiplier it stays flat; under a shift it falls. AIDev (7.69M agent PRs, public) can probably answer this.

### Frictions as a lag

Because $p$ is a logistic in $\ln h$, rescaling $h$ by $D_j = m_j k_j$ just divides the horizon by $D_j$. Horizons have doubled every $T_d \approx 129$ days since 2023, so dividing by $D_j$ is the same as using the frontier from $L_j$ earlier:

$$\pi_j(h,t) = q_0\,p_{\text{METR}}(h,\,t - L_j), \qquad L_j = T_d \log_2 D_j.$$

$D_j = 7$ (reviewer standards only) gives a lag of about 1 year; $D_j = 20$ about 1.5 years; $D_j = 126$ ($m_j = 18$, $k_j = 7$) about 2.5 years.

Two consequences:

- **Frictions delay savings; they don't cap them.** If the trend continues, $\pi_j \to q_0$ at any fixed $h$, so the delegate saving approaches roughly $1 - \rho_A$. For the long run, review cost and the trend matter most, not $m_j$ or $k_j$.
- **It matches what the data can identify.** The top-down series (about 2.3 pp/yr over FY24–26) is roughly one equation, so it can pin down roughly one composite parameter, and $L_j$ is that parameter. Separating $m_j$ from $k_j$ needs ticket data that records whether checks passed.

This leans on the doubling trend continuing and on $D_j$ being constant. If reviewers get stricter with AI output, or context matters more on long tasks, a single lag is too simple.

## Adding up

To get $\theta_j$, we integrate the per-task saving over $f_j(h)$, the hours-weighted distribution of task lengths in line $j$ (the first equation in the model above). Every task gets the assist saving, and delegated tasks get $\Delta_j$ on top. With no inference cost this is $\int \max\{1 - \bar\rho - \bar R(1-\kappa),\ \kappa\}\,f_j(h)\,dh$.

To get the sector-wide $S = \sum_{j \ge 0} w_j\,\theta_j$, we weight by $w_j$, line $j$'s share of labor hours. The bucket $w_0$ is non-task time (bench, training, sales, coordination), with $\theta_0 = 0$. Leaving $w_0$ out overstates $S$.

**Where inference cost goes.** θ is a share of hours, so dollars can't go inside it. Inference cost enters through prices instead: what the firm can pass on is the labor cost saved net of AI spend. With $\bar c$ the AI spend as a share of the labor bill,

$$g_L = d - s + \varepsilon\varphi\,(s - \bar c).$$

With adoption set to 1, $s = S$. (We still need to check this against how the CES setup defines $\varphi$.) Adoption comes back only for validation, through realized $s(t) = \sum_j w_j A_j(t)\,\theta_j(t)$.

## Parameters

### $p(h,t)$

- METR Time Horizon 1.1 (Jan 2026; task-level data public). Frontier 50% horizons are about 6–12 hours (Opus 4.6: 719 min, with an 80% horizon of 70 min). Doubling time about 129 days (95% CI 104–158).
- The slope is shallow: even with a 12-hour $H_{50}$, models fail roughly 9–18% of 1-hour tasks. Delegation needs 90%+ success, and the curve's shape changes that tail by about 3× (Ord), so we should report a constant-hazard fit too.
- Software only. Computer-use horizons, the closest proxy for BPO and IT ops, are 40–100× shorter (Kwa & Cheng).
- Plan: fit a shared-slope logistic to the task-level data and bootstrap over tasks.

### $m_j$

- The only anchor is METR's 5–18× gap between contractors and maintainers. We use a prior of 1–18 and report $m_j = 1, 3, 10$. Nobody has measured where vendor staff sit.

### $k_j$ and $q_0$

- $k \approx 7$ from Whitfill et al.: 4 maintainers, 3 Python repos, 296 PRs. The agents couldn't respond to feedback, so this is pessimistic for real workflows.
- Maintainer acceptance improved about 9.6 pp/yr more slowly than test scores (significant only at 10%). If real, the gap is widening, which neither form captures.
- $q_0$: no direct estimate. Deployment merge rates suggest it's close to 1, but they're confounded.
- Indian delivery adds a second review layer (client UAT, change boards), which plausibly raises $k_j$. Nothing measures it.

### $\rho_A$, $\rho_R$, $\rho_F$

- Estimates range from 0.1 to 0.33: GDPval grading time (about 0.27; 109 minutes against 404 minutes of expert time), METR's RCT screen recordings (about 9% of time), and Copilot users' verification time (22% of session time; CUPS). None is production review of delegated work.
- Review probably has a fixed cost per change: at Google, a median 24-line change takes about 45–50 reviewer-minutes. So $\rho_A(h) = a/h + b$, and we'll report the $a = 0$ and $b = 0$ corners.
- $\rho_R = \tau\rho_A$ with $\tau \in (0, 1]$, and $\rho_F \approx 0$. Nothing measures how fast reviewers reject.
- Nothing measures review time against task length in production. METR collected maintainer review times in its 2026 study but hasn't published them.

### $R_A$, $R_R$, $R_F$

- The only anchor is Rein (METR, Aug 2025): estimated fix times of about 1/3 to 1/2 of task length for test-passing agent PRs. That's 4 PRs, the fix times are estimated rather than timed, and we only see fixes for PRs someone chose to fix.
- The sign could flip. Experienced developers in METR's 2025 RCT were 19% slower with AI, which is consistent with AI output sending people down wrong paths (though it mixes assisting and delegating).
- With $p$ near 0.5, $R_R$ alone moves θ a lot.

### $\kappa$

- Development: about 0.15–0.25, from 2022–24 tools. The best field estimate is Cui et al.: +26% completed tasks across 4,867 developers, i.e. about 21% of labor saved per task.
- Experts on their own code: 19% *slower* in early 2025 (METR). The 2026 follow-up points to a speedup, but METR calls the data unreliable.
- BPO chat: about 0.04–0.13. Brynjolfsson, Li & Raymond find handle time down 8.5%; at Alibaba, a 32% cut on one step became a 4.2% cut on the whole chat (Ni et al.).
- Current tools are unmeasured. We'd index κ by tool vintage; Merali finds about 8% less task time per year of model progress.

### $f_j(h)$

- None exists for any Indian service line. This is probably the biggest gap: the slope is shallow, so where hours sit along $h$ (especially the long tail) largely sets $\theta_j$.
- Proxies: SWE-bench Verified (39% of tasks under 15 min, 52% at 15–60 min, 8% at 1–4 h; annotator guesses, count-weighted); JOSSE and the Public Jira Dataset (sparse open-source effort logs); Anthropic Economic Index task times (estimated by Claude).
- We treat $f_j$ as fixed, but firms can split long tasks into chunks the AI can handle, paying review per chunk (Demirer et al. 2026). This biases θ down for long tasks.
- What we'd ask firms for: one row per ticket with logged effort hours, released only as aggregates by line and length bin.

### $w_j$ and $w_0$

- Firm service-line splits are already in the repo, but they're revenue shares, and revenue isn't hours: Infosys onsite hours bill at about 3× offshore. We convert using the onsite premium and report intervals. Detailed splits end in 2017–19.
- For $w_0$, Infosys person-month data (2010–18) are the best public source.

### $\omega$ and $c_D$

- $\omega \approx$ \$16/h loaded (unverified; derived from Infosys's FY26 20-F, blending onsite and offshore). The offshore wage is probably lower. At \$16/h, a \$4 agent run on a 1-hour task is 25% of its labor cost, so inference cost matters more for India than in US-based estimates.
- $c_D$ is billed by usage and probably grows faster than linearly in $h$, since context accumulates and failures get retried. The \$4 is a single data point.

## What the model leaves out

- **Routing ticket by ticket.** We assume firms pick a mode on $h$ alone. If they can predict which tickets the AI will get right, they do better; if weak reviewers over-delegate, they do worse.
- **Time saved vs. labor removed.** Danish survey data suggest about 80% of saved time goes to other tasks (Humlum & Vestergaard). Some of that is the demand response, which $\varepsilon\varphi$ handles; some is reallocation inside the firm, which it doesn't.
- **Downstream rework.** AI-written code may cost more to maintain later: in He et al., velocity gains fade within two months while complexity rises. This matters for application maintenance, which inherits other people's code.
- **Whose hours.** Juniors save the most time and seniors do the review, so hours-weighted and cost-weighted θ can differ.
- **Large savings.** $S = \sum_j w_j\theta_j$ is a first-order (Hulten) approximation. With large savings the weights themselves shift (Baqaee & Farhi), so we should also report a reweighted $S$.

## Validation

Realized cumulative replacement over FY24–26 (about 7 pp, range 4.5–11) should roughly match the change in $\sum_j w_j A_j(t)\,\theta_j(t)$, with adoption $A_j(t)$ built from disclosed tool head-counts. This mostly identifies κ × adoption and the lag $L_j$. It has little power over review cost.

## Sources

- Baqaee & Farhi (2019). <https://econometricsociety.org/publications/econometrica/browse/2019/07/01/macroeconomic-impact-microeconomic-shocks-beyond-hultens>
- Becker, Rush, Barnes, Rein (METR, 2025), developer RCT. <https://arxiv.org/abs/2507.09089>
- Becker et al. (METR, Feb 2026), uplift update. <https://metr.org/blog/2026-02-24-uplift-update/>
- Brynjolfsson, Li, Raymond (2025). <https://www.nber.org/papers/w31161>
- Cui et al. (2025/2026), Copilot field experiments. <https://economics.mit.edu/sites/default/files/inline-files/draft_copilot_experiments.pdf>
- Demirer, Horton, Immorlica, Lucier, Shahidi (2026), "Chaining Tasks". <https://www.nber.org/papers/w34859>
- He et al. (2026), Cursor study. <https://arxiv.org/html/2511.04427v3>
- Humlum & Vestergaard (2025/2026). <https://www.nber.org/papers/w33777>
- Kwa & Cheng (METR, 2025), horizons across domains. <https://metr.org/blog/2025-07-14-how-does-time-horizon-vary-across-domains/>
- Li, Zhang, Hassan (2025), AIDev. <https://huggingface.co/datasets/hao-li/AIDev>
- Merali (2024). <https://arxiv.org/abs/2409.02391>
- METR (2026), Time Horizon 1.1. <https://metr.org/blog/2026-1-29-time-horizon-1-1/> ; data: <https://metr.org/assets/task_results_1_1.yaml>
- Montgomery et al. (2022), Public Jira Dataset; Alhamed & Storer (2022), JOSSE. <https://zenodo.org/doi/10.5281/zenodo.5882881> ; <https://zenodo.org/records/7022735>
- Mozannar, Bansal, Fourney, Horvitz (2024), CUPS. <https://arxiv.org/abs/2210.14306>
- Ni et al. (2026), Alibaba. <https://arxiv.org/pdf/2603.29888>
- Ord (2025). <https://arxiv.org/abs/2505.05115>
- Patwardhan et al. (2025), GDPval. <https://arxiv.org/abs/2510.04374>
- Rein (METR, 2025), algorithmic vs holistic evaluation. <https://metr.org/blog/2025-08-12-research-update-towards-reconciling-slowdown-with-time-horizons>
- Sadowski et al. (2018), code review at Google. <https://sback.it/publications/icse2018seip.pdf>
- Tamkin & McCrory (2025); Anthropic Economic Index (Jan 2026). <https://www.anthropic.com/research/estimating-productivity-gains> ; <https://www.anthropic.com/research/anthropic-economic-index-january-2026-report>
- Watanabe et al. (2025). <https://arxiv.org/html/2509.14745v3>
- Whitfill, Wu, Becker, Rush (METR, 2026). <https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/>
