# Which tasks can be handed to AI? A plan for a reliability-adjusted exposure measure

Niranjan Deshpande · November 2026 · Working draft (v2)

## 1. What we're measuring and why

Existing exposure measures ask whether AI *could* help with a task. The best known, Eloundou et al. ("GPTs are GPTs"), labels each O\*NET task by whether an LLM could cut the time it takes by at least half. That label ignores reliability. A task where the AI succeeds 60% of the time and one where it succeeds 99% of the time can get the same label, but a firm would treat them very differently.

We want a measure that answers a narrower question: **what share of the hours spent on a task would a cost-minimizing firm hand to an AI agent, rather than have a person do with AI help?** We call this the task's *delegable share*.

Why this question:

- **It's where the large savings are.** Assisting a worker saves a modest share of their time (roughly 5–25% in the studies we have). Handing the whole task to an agent saves most of it.
- **It's a step up from Eloundou, not a replacement.** It uses the same task list, so the two measures can be compared task by task. This is the framing Andrei suggested: a quality-adjusted version of exposure, where the adjustment is for reliability.
- **It's one rung of the full model.** The full model estimates the share of labor AI saves per service line (θ). That needs more inputs than we can pin down now. The delegable share needs fewer, and θ can be built on it later.

For India, the question we care about is relative: is the work Indian IT/BPO firms do *more or less* delegable than the average task in the economy? An absolute answer ("BPO will be disrupted") says little, since most sectors will be affected to some degree.

## 2. The model

### One work item, two options

Take one *work item*: one ticket, one email reply, one report (Section 6 defines this). A trained worker takes $h$ hours to do it without AI. The firm has two options.

**Assist.** The worker does it with AI help and saves a share $\kappa$ of the time. Cost: $(1-\kappa)h$.

**Delegate.** An agent does it and a person reviews the output. If the reviewer accepts it, we're done. If not, the worker does it with AI help, as they would have anyway. With $\pi(h)$ the chance the output is accepted, the firm delegates when

$$
\underbrace{\pi(h)\,(1-\kappa)\,h}_{\text{expected hours saved}} \;>\; \underbrace{a + b\,h}_{\text{review hours}} .
$$

In words: delegate when the expected time saved by a successful attempt exceeds the time spent reviewing.

Why this setup: it's the simplest version that keeps the trade-off we care about. A failed attempt costs review time and nothing else, because the fallback is the assisted work the firm would have done anyway. Section 11 lists what we leave out.

### Review time

Review takes $a + b\,h$ hours. $a$ is a fixed time to check any item, however small: open it, read the context, confirm the result. $b$ is review time that grows with the size of the item.

Why both parts: with only the proportional part, the model would delegate very short items too readily. A two-minute reply can take a minute to check. This matters for BPO, where many items are short. With only the fixed part, long items would cost no more to review than short ones.

A consequence: delegation happens in a *band* of item lengths. Very short items aren't worth it because the fixed review cost eats the saving. Very long items aren't worth it because the agent rarely succeeds.

### Reliability: the chance the output is accepted

Each work item is matched to the benchmark $b$ it most resembles (Section 8). The chance of acceptance follows that benchmark's success-versus-length curve:

$$
\pi(h) = \sigma\!\Big(\beta_b\,\big[\ln\big(H_b(t)/k_b\big) - \ln(m\,h)\big]\Big), \qquad \sigma(x) = \frac{1}{1+e^{-x}} .
$$

| Symbol | Meaning | Source |
|---|---|---|
| $H_b(t)$ | Task length at which the best agent at date $t$ succeeds half the time on benchmark $b$ | Fit to benchmark data (Section 4) |
| $\beta_b$ | How fast success falls as items get longer on benchmark $b$ | Same fit |
| $k_b$ | How much stricter a real reviewer is than benchmark $b$'s grader, as a stretch in task length | Set per benchmark from its grading method (Section 9) |
| $m$ | How much firm-specific context the item needs, as a stretch in task length | Coded per task (Section 7) |

Why match each task to a benchmark:

- **Different kinds of work improve at different rates, and the rates change.** Computer use started far behind software and may now be catching up faster. A fixed ratio to one headline horizon can't represent that. Each benchmark's own trend can.
- **Matching is a judgment an LLM can make and we can check.** "Which of these benchmarks is this task most like?" is a classification. We can read the answers. "How good is AI at this task?" is a judgment about AI capability, which an LLM makes poorly and nobody can check.
- **Levels and rates come from data.** The coder never states how capable AI is.

Why $k_b$ is simple to handle: it appears only in the ratio $H_b/k_b$, the *effective horizon*. For tasks matched to the same benchmark, $k_b$ shifts the capability axis but doesn't change which tasks are delegable before others. It matters for comparisons across benchmarks and for dates.

### From one item to one task

A task (an O\*NET statement) covers many items of different lengths. Item lengths follow a lognormal. Let $g(h)$ be the share of the task's *hours* at each item length. The task's delegable share is the share of hours that pass the test:

$$
D = \int \mathbb{1}\big\{\pi(h)(1-\kappa)h > a + b\,h\big\}\; g(h)\,dh .
$$

$D$ is between 0 and 1 and depends on the date through $H_b(t)$. We compute it numerically. Tasks coded as interpersonal or physical get $D = 0$.

### From tasks to occupations

$$
\bar D = \frac{\sum_i w_i D_i}{\sum_i w_i},
$$

with $w_i$ the O\*NET importance rating. Where a statement is split into parts, each part gets the original weight times its time share. We also report equal weights. Neither is a share of hours, which O\*NET doesn't provide.

## 3. Where each input comes from

| Input | Source |
|---|---|
| $H_b(t)$, $\beta_b$ | Benchmark data, fit per benchmark |
| $k_b$ | Our judgment per benchmark, from its grading method |
| $\kappa$ | Assist studies, by domain |
| $b$ | Measured review shares, assigned by stakes |
| Work item, length percentiles, fixed review minutes ($a$), stakes, context ($m$), domain, benchmark match | LLM-coded per task |

Alternatives we rejected:

- **An LLM grades "delegability" directly with a rubric.** One grade would mix reliability, review cost, and failure cost, so we couldn't tell which drove a result or check it. It would reflect the grading model's beliefs at its training date. And a close version exists: Shao et al. (2025, WORKBank) had AI experts rate 844 O\*NET tasks on a scale from full automation to essential human involvement.
- **An LLM maps a headline capability score to each task's capability.** The LLM would give each task a fixed ratio to the headline score, which is the same fixed-ratio problem moved to the task level. It can't know future rates of progress.
- **A single capability index (e.g. the Epoch Capabilities Index).** It fits every benchmark to one latent capability, so each benchmark's progress is a fixed function of one number. If one kind of work speeds up relative to the rest, a one-index model can't show it.

## 4. The benchmark catalog

The coder picks the closest benchmark from a list we supply. Benchmarks have multiplied over the past year, and many relevant ones postdate the coding model's training data, so the coder can't be relied on to know them. The list has to come from a fresh search.

**A benchmark goes in the catalog if:**

1. **Its items resemble real work.** Tasks a person is paid to do, not puzzles.
2. **It has human completion times per item, or they can be estimated.** Without times, there's no length axis.
3. **It has scores for several models released over time.** This gives the trend $H_b(t)$.
4. **It has item-level or subset-level results**, ideally. These let us fit $\beta_b$. With overall scores only, we can still estimate $H_b$ using a pooled $\beta$, with larger error (Kwa & Cheng's method).
5. **Its grading method is documented.** This sets $k_b$.

**For each benchmark we record:** a short description of what an item looks like, the range of human item times, $H_b$ for each frontier model and date, the fitted $\beta_b$, $k_b$, and the domain (software, computer use, text).

**Fitting.** Following METR, fit a logistic in log human time to each model's per-item success, giving $H_b$ and $\beta_b$ for that model. Keep only frontier models (those that beat every earlier horizon). Fit a trend to $\ln H_b$ against release date. Drop benchmarks where success barely depends on item length; Kwa & Cheng excluded those with $\beta < 0.25$.

**Starting points to check:** METR's software task suite, SWE-bench Verified, OSWorld, WebArena, τ²-bench (customer service with policies), GDPval (occupational tasks with expert times), and the Remote Labor Index (freelance projects). Several of these lack human times, which is likely to be the binding constraint.

**Coverage.** Report the share of task importance, for BPO and for the comparison sample, that has a good match, a partial match, or none. Tasks with no match are reported separately, not filled with a guess.

## 5. Tasks and occupations

### Task list: O\*NET

We use O\*NET task statements, with Indian data for the weights.

- **The comparison needs the whole economy.** India's IT-ITeS job standards (the NASSCOM Sector Skills Council qualification packs) cover only that sector.
- **It matches existing work.** Eloundou, WORKBank, and the Anthropic Economic Index use O\*NET, so results can be compared task by task.
- **What's Indian is the mix, not the task.** A help-desk ticket is much the same task in Pune and Ohio. What differs is the hours going to each kind of work, which the weights capture.

We use the NASSCOM standards as a check that O\*NET's task lists cover what Indian workers do.

### Which occupations

O\*NET has over 19,000 task statements. We don't need all of them.

**Pilot (about 50 statements).** Computer User Support Specialists, Customer Service Representatives, and Software QA Analysts and Testers. These cover computer use, text, and software, so the pilot tests every part of the pipeline.

**BPO set (about 250–300 statements).** Occupations matching Indian IT/BPO service lines (codes to check):

| Service line | O\*NET occupations |
|---|---|
| Application development and maintenance | Software Developers (15-1252), Web Developers (15-1254) |
| Testing | Software QA Analysts and Testers (15-1253) |
| Infrastructure and support | Computer User Support Specialists (15-1232), Network and Computer Systems Administrators (15-1244), Database Administrators (15-1242) |
| Consulting and analysis | Computer Systems Analysts (15-1211) |
| Voice and chat support | Customer Service Representatives (43-4051) |
| Finance and accounting | Bookkeeping, Accounting, and Auditing Clerks (43-3031); Billing and Posting Clerks (43-3021) |
| Data and back office | Data Entry Keyers (43-9021); Insurance Claims and Policy Processing Clerks (43-9041); Medical Records Specialists (29-2072) |

**Comparison sample (about 600–1,000 statements).** 30–50 occupations drawn at random, weighted by employment, spread across the major occupation groups.

Why a random sample rather than hand-picked "representative" occupations: any reader can ask why we chose the ones we did. A random sample estimates the economy-wide average without bias and comes with a margin of error. The pilot will show how much delegable shares vary across occupations, which sets the sample size.

A free check: Eloundou's labels exist for all 19,000 statements. If the sample's average Eloundou exposure is close to the full average, the sample is probably representative on the dimension that matters most.

## 6. Work items

The length $h$ needs a unit. "Answer user questions" is clear: one ticket. "Monitor system performance" is not.

**Rule:** a work item is one deliverable in the *current* human workflow that a worker finishes and that someone else would check or rely on as a whole.

Why fixed to today's workflow: if the unit were "what a firm would hand to an agent," it would change as agents improve, and it would depend on the delegation decision it feeds. Firms will split long tasks into smaller pieces for agents. We treat that as a separate effect. Leaving it out biases the delegable share down for long tasks.

**One pass sets the units (Stage 1).** One model reads every statement once and writes a *unit schema*. It classifies each statement (discrete, compound, ongoing, interpersonal, physical), splits compound statements, recasts ongoing activities as the discrete items they produce, and names the work item in one line. Every later coder uses this schema.

Why one pass: if coders picked their own units, their numbers would describe different things and couldn't be combined. A shared schema means disagreement between coders reflects only the features. It also leaves one short list we can read by hand. Interpersonal tasks get $D = 0$ because delegation here means an agent produces an output a person can review, and a live meeting doesn't produce one.

The cost: a bad unit passes silently to every coder. Section 12 covers the safeguards.

## 7. Coding the features (Stage 2)

Three coders (separate LLM runs) code each work item independently. We take the median of each number and the middle value of each category, and report the spread.

Why three and the median: three runs show whether a feature is stable, and the median ignores one outlier. Combining features is valid because all coders use the same unit.

| Feature | What the coder gives | Feeds |
|---|---|---|
| Domain | Software, computer use, or text | $\kappa$ |
| Item length | 10th, 50th, 90th percentile minutes for one item, experienced worker, no AI | $g(h)$ |
| Fixed review minutes | Minutes to check a trivially small item | $a$ |
| Stakes | Cost of an error that slips past review: low, medium, high | $b$ |
| Context | Dependence on knowledge of this client or employer: low, medium, high | $m$ |

Choices worth justifying:

- **Coders describe the work as it's done today, without AI.** Every feature here is a fact about the work. Judgments about AI come only from benchmark data.
- **Percentiles, not a distribution.** Percentiles are easier to judge than parameters. Three of them give a check: if one smooth curve can't fit them, the statement probably holds two kinds of item and should be split.
- **Lognormal lengths.** Item length plausibly comes from many factors multiplied together (number of steps, difficulty, unfamiliarity), which produces this shape. It's positive and skewed right: most items are short, a few long ones take a large share of the hours. It also fits the reliability curve, which is in log length. Some effort data have longer tails than a lognormal; we'll check against software effort logs.
- **Counts to hours.** Coders think about a typical item, which weights items by count. For a lognormal with log-mean $\mu$ and log-spread $\tau$, the hours-weighted version has log-mean $\mu+\tau^2$ and the same spread, where $\mu = \ln h_{50}$ and $\tau = (\ln h_{90} - \ln h_{10})/2.56$.
- **Stakes set review thoroughness.** When an undetected error is costly, reviewers check more carefully. Mapping stakes to $b$ captures this without a separate outcome for errors found later.
- **Categories for context.** Nobody has measured $m$ for firm workers. Coarse categories are as precise as the evidence allows.

## 8. Matching to benchmarks (Stage 3)

Three coders independently match each work item to the closest benchmark in the catalog and rate the match as good, partial, or none. We take the most common choice and record disagreement.

Why a separate stage: the catalog descriptions are long, and keeping them out of Stage 2 keeps that prompt focused. It also lets us rerun matching when the catalog grows without recoding everything else.

Why "none" is allowed: forcing a match on a task unlike every benchmark would assign it a horizon with no basis. Unmatched tasks are reported separately, and their share of importance is itself a result: it shows where the evidence runs out.

## 9. Global parameters and calibration

| Parameter | Pilot value | Sensitivity | How we set it |
|---|---|---|---|
| $H_b(t)$, $\beta_b$ | Fit per benchmark | Trend fit uncertainty | Section 4 |
| $k_b$ | 7 for test-graded software benchmarks; 1 for benchmarks graded by human experts against professional standards | Test-graded: 3.5, 14. Others: 1 to 7 | Whitfill et al. (METR, 2026) estimated about 7 for code that passes tests versus what maintainers merge. That rests on few PRs and may suffer from selection. Benchmarks graded the way a reviewer would grade should need little stretch. |
| $\kappa$ | Software 0.20; computer use 0.12; text 0.25 | Software 0 to 0.30; computer use 0.05 to 0.20; text 0.15 to 0.40 | See below |
| $b$ | Low stakes 0.10; medium 0.20; high 0.33 | All ± 0.05 | Measured review shares run roughly 0.1 to 0.33. Assigning them by stakes is a judgment call. |
| $m$ | Low 1; medium 3; high 10 | High: 5, 18 | METR's outside contractors took 5–18 times longer than maintainers who knew the code. That's the high-context case. Medium is roughly the geometric middle of 1 and 10. |

**$\kappa$ sources (from memory; check each).** A study reporting $x\%$ more output per hour implies $\kappa = x/(100+x)$; one reporting $y\%$ less time implies $\kappa = y/100$.

| Domain | Studies |
|---|---|
| Software | Cui et al. 2024 (~26% more completed PRs); METR 2025 (19% slower for experienced developers on their own repos) |
| Computer use / support | Brynjolfsson, Li & Raymond 2023 (~14% more issues resolved per hour) |
| Text | Noy & Zhang 2023 (~40% less time on short writing tasks); Dell'Acqua et al. 2023 (~25% faster for consultants) |

These used 2023–2025 models, so current values may differ in either direction.

**Why $k_b$ only affects dates within a benchmark.** $k_b$ appears only in $H_b(t)/k_b$. If $k_b$ falls over time (agents learn to meet reviewers' standards), the effective horizon grows faster than the benchmark trend. We treat that as a scenario in the projections, not something to estimate now.

## 10. Reporting

**Snapshot.** Delegable shares at today's benchmark horizons. This needs no forecast.

**Projections.** Delegable shares at future dates, extending each benchmark's own trend. Different kinds of work then move at their own measured rates. We show a second scenario in which $k_b$ halves over the projection period.

**The comparison.** BPO occupations and service lines against the random-sample average, at each date. Service lines are weighted by their hour shares from firm filings. The comparison group uses US employment weights, and Indian weights from PLFS if the crosswalk from Indian occupation codes to O\*NET works.

**Against Eloundou.** Both measures for every task, and where they disagree. If they rank tasks the same way, our adjustment adds little. Where they differ is the contribution.

## 11. What we leave out for now, and why

| Left out | Effect | Why |
|---|---|---|
| Cost of running the agent | Too much delegation, mostly for long items | Needs wages and per-run costs; the measure is in hours. Easy to add as one term. |
| Partial use of rejected output | Too little delegation | No measurement beyond a handful of PRs. |
| Errors found after acceptance | Too much delegation | Partly handled through stakes. |
| Automatic checks before human review | Too little delegation for testable work | Mostly relevant to software, where benchmark success already reflects tests. |
| Firms splitting long tasks | Too little delegation for long tasks | A separate mechanism; including it would make the unit change over time. |
| Saved time reused on other work | Overstates labor saved | A labor-demand question, outside this measure. |

One thing to watch: because a failed attempt costs only review time, the model will delegate items the agent gets right less than half the time. That's correct if errors are caught at review. If many are caught later (client testing, production failures), failure costs more and the model delegates too much.

## 12. Checks

1. **Pilot first.** Run all three stages on the ~50 pilot statements. Measure coder disagreement, the share of importance in each statement type, and benchmark coverage.
2. **Read the unit schema.** Hand-check a sample before Stage 2, weighted toward high-importance BPO tasks. Unit errors don't show up as disagreement, so this is the main safeguard.
3. **Read the benchmark matches.** Hand-check a sample of matches, especially partial ones.
4. **Let coders flag bad units.** Flags show where to fix the schema.
5. **Test sensitivity to the unit.** For 20–30 tasks, write an alternative unit (e.g. an email thread instead of one email), recode, and see how much $D$ moves.
6. **Check lengths against logs.** Compare coded lengths for software items with effort logs (the Public Jira Dataset, JOSSE). We know of no public timed data for BPO items.
7. **Compare with other measures.** On overlapping tasks, compare with the Anthropic Economic Index split between automation and augmentation, and with WORKBank expert ratings. Neither is ground truth, but large disagreements are worth investigating.

## 13. Open questions

- **How many benchmarks have human times?** This decides coverage.
- **Does a benchmark's trend transfer to the tasks matched to it?** Matching assumes progress on the benchmark tracks progress on similar real work.
- **How strict are real reviewers relative to each benchmark's grader?** We have one estimate, for software.
- **How much BPO work is ongoing or interpersonal?** The pilot will tell us.

---

## Appendix: draft coder instructions

These are starting points to edit. Each prompt should include two or three fully coded worked examples. Without them, coders will use different scales.

### Stage 1: unit schema (one run)

Input: occupation title, occupation description, one task statement.

```
You are building a coding schema for an occupational task.

Describe the task as people do it today, without AI. Do not consider what AI
could or could not do.

1. Classify the statement as one of:
   - DISCRETE: produces a distinct deliverable.
     Example: answer a user's question about software.
   - COMPOUND: joins two or more different activities, often with "or"/"and".
     Example: write training materials, or train users.
   - ONGOING: a continuing activity with no single deliverable.
     Example: monitor system performance.
   - INTERPERSONAL: the output is a live interaction with people.
     Example: meet with staff to set requirements.
   - PHYSICAL: cannot be done at a computer.
     Example: install cables.

2. If COMPOUND: split into separate statements. Give each part a share of the
   original task's working time (shares sum to 1). Classify each part again.

3. If ONGOING: name the discrete items the activity produces
   (e.g. "one alert investigated", "one daily status report").
   If there are several kinds, list each with a share of working time.

4. For every discrete item, name the work item in one line: one deliverable
   that a worker finishes and that someone else would check or rely on as a
   whole. State where it starts and where it ends
   (e.g. "one support ticket: from the customer's first message to
   confirmed resolution").

5. If one statement covers very different kinds of item (e.g. quick replies
   and long investigations), split it as in step 2.

Before each decision, give one sentence of reasoning.

Output JSON: {type, reasoning, parts: [{statement, time_share, type,
work_item, start, end, reasoning}]}
```

### Stage 2: features (three independent runs)

Input: occupation, task statement, work item with start and end (from Stage 1).

```
You are coding features of one work item.

Use the work item exactly as defined. If it does not fit the task, set
unit_flag to true, explain in one sentence, and code it anyway.

Describe the work as experienced people do it today, without AI. Do not
consider what AI could do; that comes from other data.

For each field, write one sentence of reasoning, then the value.

DOMAIN: what would someone mainly have to do to produce this item?
  - software: write, change, or test code or configuration
  - computer_use: operate applications or websites (ticketing tools, ERP
    systems, forms, web portals)
  - text: read and write documents or messages, where the output is text
    and producing it does not require operating other software
  Pick the one that takes most of the time.

LENGTH: active working minutes for one item, start to end, for an
experienced worker in this occupation, without AI. Exclude waiting time.
Give the 10th, 50th, and 90th percentile across the items this worker
meets. If the items fall into two distinct groups, say so.

FIXED_REVIEW_MINUTES: minutes a competent colleague needs to check a
trivially small instance of this item well enough to accept it: open it,
read the context, verify the result. Exclude time to fix errors.

STAKES: cost of an error that slips past review, for a typical item.
  - low: cheap to fix and noticed soon (wrong ticket category; typo in an
    internal note)
  - medium: reaches a client or user and causes rework or a complaint, but
    can be reversed (wrong instructions to a user; a bug caught in testing)
  - high: financial loss, legal or regulatory exposure, data loss, or an
    outage, or hard to reverse (wrong payment; compliance filing;
    production deployment)
  If the 90th-percentile item is in a higher category, note it.

CONTEXT: how much does the item depend on knowledge specific to this
client or employer?
  - low: a skilled outsider with the item in front of them could do it
    about as fast as an insider
  - medium: needs familiarity with the client's tools, processes, or
    conventions that takes weeks to learn
  - high: needs deep knowledge of the client's systems, history, or people
    that takes months to build

Output JSON: {unit_flag, unit_flag_reason, domain, length_p10, length_p50,
length_p90, two_groups, fixed_review_minutes, stakes, stakes_p90,
context, reasoning: {...}}
```

### Stage 3: benchmark match (three independent runs)

Input: work item with start and end, domain from Stage 2, the benchmark catalog (name, what an item looks like, range of human item times).

```
You are matching a work item to the most similar benchmark.

Below is a list of benchmarks. Each entry says what a benchmark item looks
like and how long items take people.

Choose the benchmark whose items are most like this work item in what the
worker has to do: the inputs, the actions, and what counts as a correct
result. Similar length is not enough. Do not consider how well AI performs
on any benchmark.

Rate the match:
  - good: the benchmark's items are the same kind of work
  - partial: they share the main actions but differ in an important way
    (say how)
  - none: no benchmark is close. Do not force a match.

Give two sentences of reasoning, then your choice.

Output JSON: {benchmark, match, difference_if_partial, reasoning}
```
