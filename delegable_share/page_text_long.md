---
title: Which work would a firm hand to an AI agent? A pilot
short: Delegable share (pilot)
description: A pilot estimate, for three occupations, of the hours a firm saves by handing work to an AI agent instead of having a person do it with AI help, using benchmark success-versus-length curves.
byline: Niranjan Deshpande · November 2026 · Pilot
thanks: Written as part of SPAR (Fall 2026), supervised by Andrei Potlogea. Three occupations only; a run on ten Indian IT and BPO occupations is under way. Data and code: {{repo}}.
---

<!--
HOW THIS FILE WORKS
`python3 delegable_share/scripts/build_page.py pilot_v4c [bpo_run]` turns this file into docs/delegable-share.html.
  - {{name}} is a number computed by the build script from the run's CSVs (list in tokens() there). Don't type numbers that
    come from the data; use a token, so the page can't drift from the results. The build stops on an unknown token.
  - [^key] marks a footnote; define it on its own line at the end as "[^key]: text". Footnotes show on hover.
  - $...$ and $$...$$ are math (KaTeX). Keep display math on its own line.
  - "::: figure NAME" ... ":::" holds a caption; the chart is drawn by the build script.
  - "::: gentable NAME" ... ":::" is a table built by the script (caption, then optional "---" and a note).
  - "::: table" ... ":::" is a hand-written pipe table (caption, rows, optional "---" and a note).
  - "::: details Title" ... ":::" is a collapsible block.
  - "::: if-bpo" / "::: if-no-bpo" ... ":::" show only when the BPO run is present / absent.
  - "### " headings under "## Appendix" become collapsible.
-->

## Summary
Here, I investigate how **automatable** certain professions are. Like we discussed, this is intended to be an update to Eloundou et al.'s framework. 

The goal is roughly to replace Eloundou's binary metric with a continuous measure of how much of an occupation's tasks are delegatable. I try to bring in insights from my model 


Existing exposure measures ask whether AI could help with a task. We ask a narrower question: how many hours a firm would save by handing a piece of work to an AI agent and having a person check the result, instead of having the person do the work with AI help. This page reports a pilot on three occupations: Computer User Support Specialists, Customer Service Representatives, and Software Quality Assurance (QA) Analysts and Testers.

- Our headline measure, **S**, is the net hours a firm saves by delegating instead of assisting, as a share of the hours the work takes without AI.
- Alongside it we report **D**, the share of those hours a cost-minimising firm would hand to an agent at all. D is much larger than S. A failed attempt costs the firm only the reviewer's time, so it tries the agent even on work the agent usually gets wrong.
- We don't know how strict a firm's reviewer is compared with a benchmark's grader, so we report two cases. With ρ = 1, the reviewer accepts everything that passes the benchmark. With ρ = 0.5, they accept half of what passes benchmarks graded by tests or state checks.[^rho] With ρ = 1, S is {{us_S}} for user support, {{cs_S}} for customer service and {{qa_S}} for QA. With ρ = 0.5, it is {{us_S5}}, {{cs_S5}} and {{qa_S5}}.
- Three choices move the results most. The first is ρ. The second is how we line up benchmarks scored at different dates: we move each one's latest result forward to today at a doubling time of {{pooled}} months, and without that step S is {{us_S_noalign}}, {{cs_S_noalign}} and {{qa_S_noalign}}. The third is our time estimates. The LLM coders who estimate how long tasks take squeeze their answers toward the middle. If we stretch the estimates back out, for both the work and the benchmark items, S falls to {{us_S_decomp}}, {{cs_S_decomp}} and {{qa_S_decomp}}, though this probably overcorrects.
- Benchmarks cover nearly all of the work: no occupation has more than {{unc_max}} of its weight without a usable match. But almost every match is "partial". In each occupation, {{partial_lo}}–{{partial_hi}} of the weight is matched to a benchmark whose items differ from the real work in some way that matters.

::: gentable summary
**Table 1.** S and D by occupation, pilot. Averages over each occupation's work items, weighted by O\*NET task importance; each item's S and D are shares of that item's hours without AI.
---
"Uncovered" is the share of weight whose work items have no matched benchmark with a horizon. It is left out of the averages, not filled. Interpersonal, physical and no-deliverable work counts as zero.
:::

## 1. What we measure

### Assist or delegate

Take one *work item*: one support ticket, one email reply, one test plan. An experienced worker takes $h$ hours to do it without AI. The firm can do one of two things.

- **Assist.** The worker does it with AI help, which saves a share $\kappa$ of the time.[^kappa]
- **Delegate.** An agent does it and a person reviews the output. If the reviewer accepts it, the item is done. If not, the worker does it with AI help, as they would have anyway.

So a failed attempt wastes only the review. The firm delegates when the time it expects to save is larger than the time it spends reviewing. Review takes a few fixed minutes for any item (open it, read the context, check the result), plus time that grows with the item's size.[^review]

The chance that the reviewer accepts the agent's output comes from benchmarks. We match each work item to the benchmark whose items it most resembles. On each benchmark, agents succeed less often on items that take people longer, so we can read off how often the best current agent would succeed on an item of a given length. The coders who describe the work never judge what AI can do. That comes only from benchmark scores.

For example, a written answer to a support ticket typically takes {{ex1_h}}. It is matched to {{ex1_bm}}, and at that length the chance of acceptance is {{ex1_pi}}.[^ex1] Compared with an assisted worker, delegating saves {{ex1_pi}} × (1 − {{ex1_kappa}}) × {{ex1_hmin}} = {{ex1_gain}} minutes in expectation. Review takes {{ex1_rev}} minutes. The net saving is {{ex1_net}} minutes, or {{ex1_netpct}} of the time the item takes without AI.

### From one item to S and D

Items of one kind vary in length: some tickets take a few minutes and some take most of an hour. We compute the saving at every length and average, weighting each length by its share of the item's hours. That average is the item's S. Lengths where delegating would lose time count as zero, since the firm wouldn't delegate them. D is the share of the item's hours where delegating pays at all. Figure 1 shows both for two items.

::: figure mechanism
**Figure 1.** The delegation rule for two pilot items, baseline case (ρ = 1). The blue line is the expected saving from delegating at each item length, per hour of work; the orange line is review time per hour. Where blue is above orange the firm delegates, and the shaded gap is the net saving. The grey hump shows where the item's hours are. S averages the gap over the hump; D is the share of the hump where the firm delegates.
:::

Formally, the chance of acceptance at length $h$ is

$$\pi(h) = \rho_b\,\sigma\big(\beta\,[\ln H_b - \ln(m\,h)]\big), \qquad \sigma(x) = \frac{1}{1+e^{-x}}.$$

$H_b$ is the *horizon* of benchmark $b$: the item length at which the best agent today succeeds half the time. $\beta$ sets how fast success falls as items get longer. $m$ stretches the length of items that need knowledge of the client or employer ({{m_low}}, {{m_med}} or {{m_high}} for low, medium or high context). $\rho_b$ is the share of outputs passing the benchmark's grader that a real reviewer would accept. The saving per hour of unassisted work at length $h$ is

$$s(h) = \max\Big\{0,\; \frac{\pi(h)\,(1-\kappa)\,h \;-\; (a + b\,h)}{h}\Big\},$$

where $a + b\,h$ is review time. With $g(h)$ the share of the item's hours at length $h$ (a lognormal fitted to the coders' 10th, 50th and 90th percentile lengths),[^hours]

$$S = \int s(h)\,g(h)\,dh, \qquad D = \int \mathbb{1}\{s(h) > 0\}\,g(h)\,dh.$$

An occupation's S and D are averages over its work items, weighted by O\*NET's importance rating.[^weights]

::: details Live calls and chats
In a live call or chat, nobody reviews the agent's reply before the customer hears it, so for these items (the "live service" type in Section 3) the rule changes. The agent handles the conversation. The firm checks a share $q$ = {{q}} of conversations at the usual review time. When the agent fails, a worker takes over and redoes the work with AI help, and the firm also pays a penalty $\lambda h$ for the customer's bad experience. The saving is then

$$\pi(h)(1-\kappa)h \;-\; q\,(a+b\,h) \;-\; \big(1-\pi(h)\big)\,\lambda h .$$

Unlike the standard rule, failure now costs something, so items the agent often gets wrong stop being delegated. We set $\lambda$ = {{lam}}: a failed conversation costs the firm as much again as the conversation itself. This is a judgment call, and Section 2 varies it from 0.25 to 3.
:::

### Why S is the headline and not D

We first planned to report D, but it says little about how many hours are saved. Since a failed attempt costs only review time, the firm tries the agent whenever its chance of success clears a low bar. Take a beta-site performance evaluation in QA, which typically takes {{ex2_h}} and is matched to {{ex2_bm}}. The chance of acceptance at that length is {{ex2_pi}}. Review takes a few fixed minutes plus about {{ex2_b}} of the item's length, so the firm should try the agent whenever its chance of acceptance is above {{ex2_thresh}}. The item gets D = {{ex2_D}}, although about three in four attempts fail. Its S is {{ex2_S}}.

In other words, D counts the hours where the firm makes an attempt, and S counts the hours it saves. Figure 2 shows the gap for every item.

::: figure dvs
**Figure 2.** D and S for each coded work item in the pilot. Most items are near D = 100%, with S anywhere from 0 to {{S_item_max}}. S can't exceed D (dotted line).
:::

## 2. Results

### By occupation

::: figure headline
**Figure 3.** S and D by occupation in both reliability cases. Other settings at baseline: horizons moved to today, β = {{beta}}, λ = {{lam}}.
:::

Customer service has the highest S with ρ = 1 ({{cs_S}}). Its items are short (the median typical item takes {{cs_p50}} minutes), and most are matched to benchmarks of customer-service conversations such as τ-Voice, where the best agent's horizon today is about {{hz_tau_voice_today}}. So agents usually succeed.

Customer service also falls furthest when ρ = 0.5, to {{cs_S5}}. Of its coded weight, {{cs_rhoshare}} is matched to benchmarks graded by state checks, where the chance of acceptance can now never exceed one half. And {{cs_live}} of its weight is live calls. For a live call to be worth handing over, the agent has to succeed more than about {{live_thresh_lo}}–{{live_thresh_hi}} of the time,[^thresh] so with ρ = 0.5 {{live_r5_zero}} live item drops to zero.

QA has the lowest S ({{qa_S}}). Its items are long (median typical item {{qa_p50}} minutes, against {{us_p50}} for user support), and many are matched to software benchmarks whose horizons are a few hours, such as SWEeper-Bench ({{hz_sweeper_bench_today}}) and ITBench SRE ({{hz_itbench_sre_today}}). QA moves least under ρ = 0.5, because only {{qa_rhoshare}} of its coded weight is on benchmarks graded by tests or state checks.

User support is in between ({{us_S}}). Interpersonal, physical and no-deliverable work make up {{us_zero}} of its weight, and these count as zero.

### Which items

::: figure items
**Figure 4.** S and D for every pilot work item. Hover for the item, its benchmark and the chance of acceptance at its typical length. Hollow grey markers are interpersonal, physical or no-deliverable items, which count as zero. Items whose matched benchmark has no horizon are left out.
:::

The {{gdpval_n}} written items matched to GDPval (ticket answers, test procedures, evaluations) have S between {{gdpval_S_lo}} and {{gdpval_S_hi}}, higher for the short ones. Investigations matched to ITBench SRE (following up a performance alert, finding a defect's root cause) are at {{itbench_sre_S_hi}} or below. The highest values rest on the least certain horizons: a live diagnosis with field staff matched to τ-bench telecom, which agents have nearly saturated (best score {{hz_tau_telecom_score}}), and a coverage question answered during a call, matched to SOPBench, whose latest score is from {{hz_sopbench_date}}.

### What moves the numbers

::: figure scenarios
**Figure 5.** S and D under other settings, changed one at a time from the baseline. Dotted lines mark the baseline values.
:::

- Reliability (ρ), discussed above. This is the case we report next to the baseline.
- Compressed time estimates. Our coders squeeze their time estimates toward the middle (Section 3), and the work-item lengths come from the same coders. Widening the spread of lengths on both sides lowers S to {{us_S_decomp}}, {{cs_S_decomp}} and {{qa_S_decomp}}, because it moves hours into very long items that agents rarely finish. This case probably overshoots: the median work item's 90th-percentile length becomes about {{decomp_ratio}} times its 10th. Widening only the benchmark side raises S, to {{us_S_decompb}}, {{cs_S_decompb}} and {{qa_S_decompb}}.
- Date alignment. Benchmarks were last scored at different times, from {{hz_crmarena_pro_date}} (CRMArena-Pro) to this month. We move each benchmark's latest horizon forward to today at a pooled doubling time of {{pooled}} months.[^pooled] For old benchmarks this is a big step: CRMArena-Pro's horizon goes from {{hz_crmarena_pro_latest}} to {{hz_crmarena_pro_today}}. Without alignment, S is {{us_S_noalign}}, {{cs_S_noalign}} and {{qa_S_noalign}}. The aligned numbers assume each kind of work kept improving at the pooled rate after its benchmark was last scored; the unaligned ones assume it stopped.
- The slope β. A flatter success curve (β = 0.6) helps long items most, and QA's S rises to {{qa_S_b06}}.
- The failure penalty λ. With λ = 3, customer service's S falls to {{cs_S_lam3}}. The other two occupations have little live work and barely move.
- Filling uncovered items from the coders' second-choice benchmark changes no occupation's S.
- One year from now, if every horizon keeps growing at the pooled rate, S would be {{us_S_12m}}, {{cs_S_12m}} and {{qa_S_12m}}.

### BPO occupations

::: if-no-bpo
In progress. The same pipeline is running on ten occupations matched to Indian IT and BPO service lines: software and web developers, network and systems administrators, database administrators, systems analysts, and bookkeeping, billing, data-entry, insurance-claims and medical-records clerks. Their S and D will appear here when the run finishes.
:::

::: if-bpo
::: gentable bpo_summary
**Table B1.** S and D by occupation, BPO run. Same definitions as Table 1.
:::

::: figure bpo_headline
**Figure B1.** S and D by occupation for the BPO run, in both reliability cases.
:::

::: figure bpo_items
**Figure B2.** S and D for every work item in the BPO run. Hollow grey markers count as zero; items without a horizon are left out.
:::
:::

## 3. How the inputs are built

### From task statements to work items

We start from O\*NET's task statements: {{n_statements}} rated statements across the three pilot occupations. Claude Opus reads each one and names its unit of work: one deliverable that a worker finishes and that someone else would check or rely on as a whole. It splits statements that join different activities, gives each part a share of the statement's time, and types each part. GPT-6.1 Terra codes the same statements as a check.[^stage1] The five types are:

- discrete: produces something a person can check, such as a written ticket answer or a test plan;
- live service: done while a customer waits, such as a call or chat;
- interpersonal: the output is a conversation with colleagues, such as training users or a design review;
- physical: can't be done at a computer, such as replacing a drive;
- no deliverable: nothing anyone checks, such as reading trade magazines to keep up.

Only discrete and live-service items can be delegated in our setup. The pilot has {{n_items}} work items, and {{n_coded}} of them are of these two types.

::: figure types
**Figure 6.** Types of work item, as a share of each occupation's importance weight. Customer service is {{cs_live}} live service; about a third of user support is work we count as zero.
:::

### Features and benchmark matches

Three coders read each work item independently: two Claude Sonnet subagents and GPT-6.1 Terra. Each describes the work as people do it today, without AI: its domain (software, computer use or text, which sets κ), the 10th, 50th and 90th percentile length of one item, review minutes for a short, a typical and a long item, the stakes of an error that slips through, and how much the item depends on knowledge of the client. Each coder then picks the closest and second-closest benchmark from a catalog of 44 and rates the match as good, partial or none. Coders see no benchmark scores or human times, so they match on what the work involves. We take the median of the numbers and the most common benchmark.[^combine]

::: figure coverage
**Figure 7.** Where the pilot's coded weight (discrete and live-service items) is matched. GDPval takes {{w_gdpval}}.
:::

::: gentable match
**Table 2.** Match quality, as a share of each occupation's coded weight.
---
"Partial" means the coders judged that the benchmark shares the main actions but differs in an important way. "Matched, but no horizon" covers two small benchmarks we didn't gather data for.
:::

Coverage is high, but the matches are loose. GDPval is the clearest case. It holds written work from many occupations, so the coders send most written deliverables there, but its items are multi-hour documents built from a brief (median {{hz_gdpval_med}} by our estimate), while many of the items matched to it are short replies or notes. The coders flag this themselves when they rate these matches "partial".

### Benchmark horizons

For each of the {{n_bench}} benchmarks matched in the pilot, we sampled 24 items and collected dated scores for as many models as we could find, from leaderboards and papers. Most benchmarks don't publish how long their items take people, so the same three coders estimated it for all {{n_bench_items}} sampled items, with the same kind of question they answered about work-item lengths.[^sametimes]

We don't fit the slope β per benchmark, since with estimated times the fitted slope would mostly measure how compressed the estimates are. Instead we fix β at {{beta}} per natural log of time (METR's median, {{beta_doubling}} per doubling) and estimate only each benchmark's horizon. For each model, that is the length at which a success curve with this slope, applied to the 24 items' estimated times, reproduces the model's overall score.[^fit] We keep the best model released by today.

::: figure horizons
**Figure 8.** Benchmark horizons. Hollow markers are the best model's horizon at its latest score; filled markers are the same horizon moved forward to today at the pooled doubling time. Grey ticks are the median item time (our estimate). The right-hand column is the share of the pilot's coded weight matched to each benchmark. Blue benchmarks are graded by tests or state checks, so ρ = 0.5 applies to them.
:::

Several horizons sit far beyond the benchmark's own items. This happens when the best model scores near the ceiling: τ-bench telecom's best score is {{hz_tau_telecom_score}}, which gives a horizon of {{hz_tau_telecom_latest}} on items that take people about {{hz_tau_telecom_med}}. A horizon like that comes from the tail of the assumed curve, not from data. The step to today is also large for benchmarks last scored in 2025.

### Time estimates

We tested the coders blind on two benchmarks that publish human times:[^pubtimes] {{swe_n}} SWE-bench Verified items, published as four time buckets, and {{tb_n}} Terminal-Bench 2 tasks, published as the authors' estimates. The coders rank items reasonably well. Their rank correlation with the published times is {{swe_rho}} on SWE-bench and {{tb_rho}} on Terminal-Bench. But their estimates are strongly compressed. On Terminal-Bench, published times of {{tb_pub_range}} became estimates of {{tb_est_range}}, and the slope of log estimate on log published time is {{tb_slope}}. Only {{tb_within2}} of the {{tb_n}} estimates are within a factor of 2.

::: figure timing
**Figure 9.** Blind time estimates (median of three coders) against published times. A perfect estimator would sit on the dashed line. Left: Terminal-Bench 2. Right: SWE-bench Verified, where each item's published time is a bucket (shaded).
:::

Giving the coders reference items with known times fixed the level of their estimates but barely changed the compression.[^anchors] Part of the compression is probably a real limit, since a short instruction can hide a day's work. Part is probably noise in the published times, which are estimates too. We can't separate the two without measured times. This is why β is fixed and the same coders estimate both the work items and the benchmark items: whatever squeezes one side squeezes the other.

## 4. What we don't trust yet

- Most matches are partial. A benchmark's progress may not carry over to work that differs from it in an important way, and we have no test of how well it does.
- ρ is a guess outside code. The one study behind ρ = 0.5 is about pull requests that pass tests.[^rho] We have no evidence for benchmarks graded by state checks, which carry most of customer service's weight.
- Score data are uneven. Some benchmarks were last scored in early 2025. For a few, scores came from third-party copies of the leaderboard because the official page wasn't reachable, and some release dates come from secondary sources.
- Scaffolds are mixed. We kept the best reported result per model, including custom agent systems (τ-bench banking's top entry is one). Horizons therefore partly reflect how much effort went into scaffolding each benchmark, which differs across benchmarks.
- λ is a judgment call. It only affects live service, but that is {{cs_live}} of customer service's weight.
- The coders' time estimates are compressed, and we don't know whether the work-item lengths are compressed by the same amount. The two widened cases in Figure 5 bracket a wide range.
- Context barely varies. {{n_medium}} of the {{n_coded}} coded items are rated medium and {{n_high}} high, so $m$ is close to a constant. Either most firm work really does need some client knowledge, or the question doesn't separate items well.
- The model leaves out the cost of running the agent, partial use of rejected output, errors found after acceptance, and firms splitting long tasks into shorter ones. Leaving out the first and third makes S too high; leaving out the other two makes it too low.

## Appendix

### Parameter values

::: table
**Table A1.** Parameter values in the baseline.
| Parameter | Value | Source |
|---|---|---|
| β, how fast success falls with length | {{beta}} per natural log (also 0.6 and 1.0) | METR's median slope from timed tasks |
| ρ, share of grader passes a reviewer accepts | 1; also 0.5 for test- and state-graded benchmarks | Whitfill et al. (METR, 2026), code only |
| κ, time saved by assisting | software {{kappa_sw}}, computer use {{kappa_cu}}, text {{kappa_text}} | Assist studies on 2023–25 models |
| a + bh, review time | Fitted per item to coders' review minutes (median b {{review_b_med}}, median a {{review_a_med}} min) | Coders |
| m, context stretch | low {{m_low}}, medium {{m_med}}, high {{m_high}} | METR: outside contractors took 5–18 times longer than maintainers |
| q, share of live conversations checked | {{q}} | Placeholder, still to source |
| λ, failure penalty for live items | {{lam}} × item length (also 0.25 and 3) | Judgment |
| Doubling time for date alignment | {{pooled}} months | Median over benchmarks with at least four frontier models |
| Item lengths | Lognormal through the coded p10, p50 and p90 | Coders |
:::

### Decisions so far

- 10 November 2026. S is the headline, with D alongside. Both reliability cases are reported side by side. Horizons are moved to today at the pooled doubling time.
- 10 November. Horizons come from overall scores for every benchmark, so one method is used throughout. Items without a horizon are left out and reported, not filled. Live service uses q = {{q}} and λ = {{lam}}. We keep the best reported result per model, custom scaffolds included.
- 9 November. ρ = 1 for every benchmark in the baseline, with 0.5 for test- and state-graded benchmarks as the second case. An earlier draft set ρ by grading method, but that would have built an unmeasured difference between kinds of work into the comparison.
- 9 November. β is fixed and only horizons are estimated. Benchmark item times come from the same coders as the work-item lengths. Reference items in the prompt were dropped, since they fixed the level but not the compression.
- 9 November. Review time is a line fitted to each item's own coded review minutes. A lookup by stakes was dropped because review time didn't rise with stakes in the coded data.
- 9 November. Features and benchmark matches are coded in one pass, after a check that this doesn't shift the features.
- 9 November. Three coders are combined by median, with no round in which coders see each other's answers. In Stage 1, each model family sided with its own coding when shown both.
- 9 November. Live service gets its own rule (sampled checks and a failure penalty) instead of D = 0.
- 9 November. Exact duplicate statements are collapsed when both models flag them. Three QA statements with no importance rating are dropped.

### Every work item

::: gentable items
**Table A2.** Every coded work item in the pilot, baseline. "π, typical item" is the chance of acceptance at the item's median length, with ρ = 1.
:::

[^rho]: Whitfill et al. (METR, 2026) found that repository maintainers would merge about half of the AI-written pull requests that pass the tests. We know of no comparable evidence for other kinds of grading.
[^kappa]: κ is set by domain: {{kappa_sw}} for software, {{kappa_cu}} for computer use, {{kappa_text}} for text. These come from studies of workers using 2023–25 models, so current values may differ in either direction. S is the saving from delegating on top of what assisting already saves.
[^review]: Coders give review minutes for a short, a typical and a long item. We fit a line $a + b\,h$ through the three points (medians across coders). Across items, the median slope $b$ is {{review_b_med}} of the item's length and the median fixed part $a$ is {{review_a_med}} minutes. Review time didn't rise with the coded stakes, so stakes don't enter.
[^ex1]: GDPval's horizon today is {{hz_gdpval_today}}. The item needs medium client knowledge, which multiplies its effective length by {{m_med}}, so the {{ex1_hmin}}-minute ticket counts as a {{ex1_eff}}-minute GDPval item.
[^hours]: The coders' percentiles describe items by count. Long items take up more of the hours than their count suggests, so we weight by hours. For a lognormal with log-mean $\mu$ and log-spread $\sigma$, that moves the log-mean to $\mu + \sigma^2$.
[^weights]: O\*NET rates each task's importance from 1 to 5. Where a statement is split into parts, each part gets the statement's rating times its share of the statement's time. Importance isn't time, so these averages are not shares of an occupation's working hours, which O\*NET doesn't report.
[^thresh]: A live item pays only if $\pi(1-\kappa) > (1-\pi)\lambda$, ignoring the small sampled review, which means $\pi > \lambda/(1-\kappa+\lambda)$. With λ = {{lam}} and κ = {{kappa_cu}} or {{kappa_text}}, that is {{live_thresh_lo}}–{{live_thresh_hi}}.
[^pooled]: The median of the benchmarks' own doubling times, over the benchmarks with at least four models that each set a new best horizon. Most benchmarks' own trends rest on too few points to use alone.
[^stage1]: Where the two models disagreed, an Opus adjudicator decided. Shown both codings, each model mostly kept its own, and the adjudicator sided with Claude more often than with Terra, which may be self-preference. At the occupation level the type shares are within 3 points of Terra's, except user support's live share, which Terra puts higher.
[^combine]: Medians for numbers and ordered categories; for domain, the median κ. For the benchmark, the most common first choice, rated with the lowest rating among the coders who chose it. Where all three coders picked different benchmarks, an Opus adjudicator chose.
[^sametimes]: Using the same coders on both sides matters. Terra's estimates of benchmark item times run 1.7–2.4 times Sonnet's, so a different mix on the two sides would shift every ratio of item length to horizon.
[^fit]: That is, $H$ solves $\tfrac{1}{24}\sum_i \sigma\big(\beta[\ln H - \ln t_i]\big) = \text{score}$, where $t_i$ is the coders' median time for item $i$.
[^pubtimes]: Both sets of "published" times are human judgments, not measurements. SWE-bench Verified's annotators assigned buckets, and Terminal-Bench's authors estimated times. Six security-style Terminal-Bench tasks were left out.
[^anchors]: With 11 reference items of known time in the prompt, the median ratio of estimate to published time on Terminal-Bench moved from {{tb_ratio}} to {{anch_ratio}}, but the slope rose only from {{tb_slope}} to {{anch_slope}}.
