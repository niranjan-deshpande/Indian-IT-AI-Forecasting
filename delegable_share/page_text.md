---
title: Which work would a firm hand to an AI agent?
short: Delegable share
description: A measure of how many of an occupation's work hours a firm would save by handing work to an AI agent instead of having a person do it with AI help, for Indian IT and BPO occupations.
byline: Niranjan Deshpande · November 2026 · Working draft
thanks: Written as part of SPAR (Fall 2026), supervised by Andrei Potlogea. Data and code: {{repo}}.
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

Here, I investigate how **delegable** different occupations are to AI. Like we discussed last time, I mean this as an update to Eloundou et al.'s exposure measure, which labels each O\*NET task by whether an LLM could cut the time it takes in half. The issue with that label is that it ignores **reliability**: a task the AI gets right 60% of the time and one it gets right 99% of the time are very different, but they get the same label under Eloundou et al.'s framework. 

I replace their metric with a continuous measure: the share of an occupation's work hours that a cost-minimising firm would save by handing work to an AI agent, instead of having a person do it with AI help.

Importantly, I don't try to calibrate all my parameters from data. I use public benchmark data to estimate reliability; but I use LLMs to estiamte every other parameter (how a task breaks into units of work, how long those take, how long checking them takes, and which benchmark they resemble) using O\*NET task statements. 

So far, I have results for {{bpo_n_occ}} Indian IT and BPO occupations and three pilot occupations (will edit this as more results come online overnight; my agents are still running!). Preliminary findings:
- Across the IT and BPO occupations, delegation would save between {{bpo_S_lo}} and {{bpo_S_hi}} of work hours today, most for {{bpo_top}} and least for {{bpo_bottom}}.
- If a firm's reviewer accepts only half of what passes the automatically graded benchmarks, that range drops to {{bpo_S5_lo}}–{{bpo_S5_hi}}.
- A few choices, listed at the end, move these numbers a lot, so treat them as a first pass.

## The model

Here, I walk through the model I use at a high level of abstraction. Consider one piece of work, like a support ticket, an email reply or a test plan. Suppose a worker takes $h$ hours to do it without AI. Thefirm has two options.

- **Assist.** The worker can do it with AI help, which saves a share $\kappa$ of the time.
- **Delegate.** An agent can do it with a person checking the result. If the check passes, the work is done. If not, the worker does it with AI help, as they would have anyway (i.e., they go down the usual assist path). 

These two save very different amounts of time! Relatively old (2025; this is ancient in AI land!) studies of AI assistance find time savings of roughly 5–25%. Meanwhile, delegating saves most of the work, but only when the agent is reliable enough that checking its output is worth the time. A failed attempt costs only the check, so the firm delegates when

$$\pi(h)\,(1-\kappa)\,h \;>\; a + b\,h,$$

where $\pi(h)$ is the chance the output is accepted and $a + bh$ is the checking time. The checking time is defined in this way because every check costs a few fixed minutes, plus time that grows with the size of the work.

I calibrate the acceptance chance comes from benchmarks. LLMs match each piece of work is matched to the benchmark whose items it most resembles. On every benchmark, agents succeed less often on items that take people longer, so we can use the latest scores to observe roughly how often the best current agent would succeed on work of a given length.

Different instances of one task type can have very different lengths (e.g. a "support ticket" can be a few minutes or a few hours), so I compute the saving at each length and take the average. We calculate two metrics: 

- **S**, the hours saved by delegating instead of assisting, as a share of the hours the work takes without AI.
- **D**, the share of hours where delegating pays at all. D is generally much higher than S, because when checking is cheap it is worth trying the agent even where it usually fails (e.g. for very long tasks, even if success probability is close to zero, the upside of the agent succesfully doing the task is much higher than the cost of a check, since check-time grows less than one-for-one with $h$. Live calls and chats follow a slightly different rule.[^live]

## Calibrating parameters

For {{n_bench}} benchmarks I collected dated scores for every model I could find. For each benchmark I then estimate its horizon: the length of item at which the best agent succeeds half the time.[^fit]

::: figure trend
**Figure 1.** Each point is a model that beat every earlier model on that benchmark, for the eight benchmarks the work is most often matched to.
:::

Everything else comes from LLMs reading O\*NET. Two Claude models and one GPT model each split every task statement into units of work, estimate how long these take and how long they take to check, and pick the closest benchmark. I use the median answer. The same models also estimate how long people take on the benchmark items, so we measure the work and benchmarks on the same scale.

## Results

::: gentable bpo_summary
**Table 1.** S and D for the IT and BPO occupations as of {{today_long}}, for both reviewer cases. Averages over each occupation's work, weighted by O\*NET task importance.
:::

::: figure bpo_headline
**Figure 2.** S by occupation, IT and BPO set, as of {{today_long}}.
:::

::: figure timeline
**Figure 3.** S over time. Every benchmark's horizon moves along the pooled trend, so the lines before and after today are extrapolations, not refits.
:::

::: gentable summary
**Table 2.** The same for the three pilot occupations, as of {{today_long}}.
:::

## What moves the numbers

- **How strict the reviewer is.** Benchmarks graded by tests or state checks pass some work a real reviewer would reject. If the reviewer accepts only half of it, S for customer service falls from {{cs_S}} to {{cs_S5}}, since all of its benchmarks are graded that way.
- **Lining up dates.** Benchmarks were last scored between early 2025 and this month. I move each one's best result forward to today at a doubling time of {{pooled}} months.[^pooled] Without that step, S for the pilot occupations is {{us_S_noalign}}, {{cs_S_noalign}} and {{qa_S_noalign}}, instead of {{us_S}}, {{cs_S}} and {{qa_S}}.
- **Squeezed time estimates.** The LLMs rank items by length well, but squeeze their estimates toward an hour or two. Using the same LLMs on both sides cancels much of this, but not all.

::: figure scenarios
**Figure 4.** S and D for the pilot occupations as one setting changes at a time, as of {{today_long}}.
:::

## Comparison occupations

To check the measure, I also ran sixteen occupations picked by hand: five that should come out high (translators, proofreaders, technical writers, paralegals, tax preparers), five that should come out near zero (electricians, nurses, childcare workers, janitors, truck drivers), and six other white-collar jobs. The controls separate, and the IT and BPO occupations sit between them.

::: figure groups
**Figure 5.** S for every occupation, as of {{today_long}}.
:::

::: figure group_timeline
**Figure 6.** S over time, averaged within each group, on the same pooled trend as Figure 3.
:::

[^live]: Nobody checks a call before the customer hears it. So for live work the firm reviews a sample of contacts, and a failed contact adds a cost for the customer's bad experience, set to {{lam}} times the contact's length.
[^fit]: The slope of success against log length is fixed at METR's estimate. Only the horizon is fitted, so that the predicted success over a sample of 24 items matches each model's overall score.
[^pooled]: The median of the benchmarks' own doubling times, over benchmarks with at least four successive record-setting models.
