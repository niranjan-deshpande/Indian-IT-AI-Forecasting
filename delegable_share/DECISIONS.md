# Decisions log

Changes to `SPEC.md` (v2) agreed since it was written. Newest first.

## Open

- **Pilot coverage.** No pilot occupation has a good match in Tier A. QA, user support and
  customer service depend on Tier B steps (SWT-bench time join; WorkArena times from authors or
  a timing study; τ-bench action counts or a timed pilot). See `benchmarks/ACQUISITION.md`.


## 2026-11-10 — Comparison set: hand-picked, with controls (user asked)

16 occupations outside the pilot and BPO set, chosen by hand (not an employment-weighted draw, so
not an economy average; it tests whether the measure separates controls and where BPO sits among
white-collar work). `data/comparison_tasks.csv` (`control_group` column), 313 rated statements.
- **Positive controls:** Interpreters and Translators, Proofreaders and Copy Markers, Technical
  Writers, Paralegals, Tax Preparers.
- **Negative controls:** Electricians, Registered Nurses, Childcare Workers, Janitors, Heavy Truck
  Drivers.
- **White-collar comparison:** Accountants and Auditors, Lawyers, Credit Analysts, Secondary School
  Teachers, Wholesale Sales Representatives, Management Analysts. (Financial and Investment
  Analysts dropped: no O*NET importance ratings.)
Same protocol as the BPO run, except Stages 2+3 batches ≤34 and Stage 1 groups of 3 occupations.
Run tags `comp_v1`.

**Result (2026-11-10, S at ρ = 1 / 0.5):** negative controls 3–8% (mean 5%); positive controls
18–30% (mean 23%); other white-collar 3–32% (mean 15%); IT/BPO 7–29% (mean 15%); pilot mean 23%.
The controls separate. Three white-collar results are driven by one benchmark each and should be
read with that in mind: Accountants 3% (APEX-Accounting, 56% of weight: all-criteria pass@1 of
24%, fitted on only 10 public items), Lawyers 7% (APEX-Agents, 71%), Wholesale Sales Reps 32%
(CRMArena-Pro, 37%: last scored March 2025, so moved forward 19 months on the pooled trend).
Stage 1: 313 statements → 448 parts; 127 disputes (41%; Opus chose Terra 67, Sonnet 51, revised 9);
duplicates 448 → 439. Stages 2+3: 255 coded items, 45 three-way splits adjudicated. Reasoning held
up at batches of 32 (median 114 → 78 words from first to last item). New benchmarks: JobBench,
APEX-Agents (public mirror; items not from the gated set), Online-Mind2Web. Pooled doubling 3.4
months with 34 benchmarks.

## 2026-11-10 — BPO run: set-up and usage cuts

- **Scope:** the 10 non-pilot BPO occupations, 204 rated statements (`data/bpo_tasks.csv`,
  `in_pilot` False). Run tags: Stage 1 `bpo_v1` (final table `bpo_v1_final/units_final.csv`), Stages 2+3 `bpo_v1`, item times `bench_times/bpo`.
- **Worked examples swapped** out of the BPO set (Stage 1 A–C, Stages 2+3 A–B). New sources:
  Executive Secretaries 2797, Market Research Analysts 5442, HR Specialists 18867. Their matches
  no longer point at BPO benchmarks (the old ones taught bookkeeping → APEX-Accounting and alerts
  → ITBench). **These three occupations, and Receptionists, must be left out of the comparison
  sample.**
- **Usage cuts (user asked):** Stage 1 coded by Sonnet, not Opus, with Terra as the cross-family
  check and Opus only for disputes. Several occupations per Stage 1 brief (instructions once;
  one output file per occupation).
- **No reconcile rounds** (Stage 1 and duplicates): disputes go straight to one Opus subagent
  (`reconcile_stage1.py` and `reconcile_dupes.py` now work without round files; `NOROUND=1`).
- **Stage 1 result:** 204 statements → 288 parts; Sonnet and Terra disagreed on 61 statements
  (30%, pilot 32%); Opus chose Terra's coding 32 times, Sonnet's 26, and revised 3 (no sign of the
  pilot's self-preference).
- **Duplicates:** both models flagged 3 pairs; Opus confirmed 6 of 8 one-model pairs; 288 → 280
  parts. Chained pairs are merged as a group (one kept, weight = mean over the group); the old
  pairwise merge would have double-averaged a three-way group.
- **Stages 2+3:** 230 coded items, batches of 46 (5 per Sonnet coder), up from 34. Every coder
  reported thinning reasoning in the second half (median reasoning words per item fall from ~100
  to ~30; pilot batches of 34 fell to ~60), and some wrote late items from a script. Checked
  before deciding: agreement between the two Sonnet coders does not fall with position (length
  |Δln| 0.27–0.30 early vs 0.20–0.29 late; same best match 50–59% early vs 57–73% late; pilot 0.28
  and 69%), and early and late answers have the same distributions (median length 30 min, p90/p10
  12, review/length 0.25, GDPval share 20%, "none" 2–4%). Codings kept; only the written reasoning
  is thin. **Future runs: batches of ≤34.**
- **Benchmarks added for the BPO matches** (same brief, Sonnet agents): APEX-Accounting (only the
  10 public dev items; scores on the private set), DualEntry (8 illustrative items, one per
  category, not random; two scoring rounds the vendor calls non-comparable), Vals Finance Agent,
  HealthAdminBench (5 models, one month), UI-CUBE, TheAgentCompany, SWE-Lancer, Spider 2 (top rows
  are third-party systems; kept, as everywhere: best reported system per model), Terminal-Bench 4,
  DBA-Bench (6 models), SWE-bench Verified. **Excluded:** OfficeVal (score is mean partial credit,
  not share solved) and OSWorld 2 (tasks gated). Benchmarks under ~0.8% of weight (SCUBA,
  Online-Mind2Web, APEX-Agents, JobBench, Cybench, SWE-bench Multimodal, WebArena) not gathered.
  Items in these cases count as uncovered; the "fill from 2nd match" scenario covers them.
- **Pooled doubling time stays 3.5 months** in the base case with 31 benchmarks (2.2–4.0 across
  the β and decompression variants). Pilot results barely move (QA uncovered 6% → 4%).
- **BPO result (base, ρ = 1 / ρ = 0.5 for tests/state):** S — Web Developers 28/20%, Insurance
  Claims 24/10%, Network Admins 19/8%, Billing 14/6%, DBAs 14/11%, Systems Analysts 13/10%, Software
  Developers 12/11%, Medical Records 11/5%, Bookkeeping 9/5%, Data Entry 6/0% (39% uncovered).
  Pilot: User Support 20/8%, Customer Service 33/10%, QA 15/11%.

## 2026-11-10 — Second half (curves and D): built; choices made while building (user may revisit)

Pipeline: `benchmarks/data/<b>/` (24 sampled items, dated scores, SOURCE.md; gathered by Sonnet
subagents per `benchmarks/data/BRIEF.md`) → `bench_times.py` run `main` (480 items, 2 Sonnet +
Terra, same prompt as validation; Terra $0.28) → `horizons.py` → `delegable.py`. Results:
`benchmarks/HORIZONS.md`, `coding/stage2/pilot_v4c/delegable/RESULTS.md`.

- **Horizons from overall scores for every benchmark** (one method everywhere): H solves
  mean_i σ(β(ln H − ln t_i)) = score over the 24 items, t_i = coders' median time.
- **Common date.** Benchmarks' latest scores range from Mar 2025 (CRMArena-Pro) to Nov 2026, so
  each benchmark's best observed H is moved forward to today at the pooled doubling time (median
  over benchmarks with ≥4 frontier points: **3.5 months**). Sensitivity: latest observed H, no
  alignment. Release date missing → evaluation date. One-year projection uses the same pooled rate.
- **Item lengths:** coded p10/p50/p90 are across items, so hours-weighted g(h) is
  lognormal(ln p50 + σ², σ).
- **LIVE_SERVICE:** q = 0.03 (barely matters), **λ = 1** (sensitivity 0.25, 3), κ as coded.
- **Unmatched / no horizon:** excluded and reported as uncovered (≤6% of weight in the pilot);
  sensitivity fills from the second match. SCUBA and TheAgentCompany (<1% each) not gathered.
- **Decompression = spread only**, around each benchmark's median and each item's p50 (levels as
  coded). Stretching around a fixed 60 minutes was dropped: it turned an 8-minute call into 16
  seconds. Widening the work items' own p10–p90 by 1/0.37 makes p90/p10 ≈ 470 and pushes hours into
  the far tail; treat that case as a loose bound.
- **New output S** (alongside D): expected net hours saved by delegating, as a share of unassisted
  hours. Needed because with failures costing only review, and coded review slopes of 5–8% for long
  items, the firm "tries the agent" whenever π > b/(1−κ) ≈ 0.06–0.09. D then counts hours where an
  attempt is made, not hours saved (e.g. a 6-hour QA evaluation with π ≈ 0.23 gets D = 0.91).
- **Headline measure is S, with D alongside** (user, 2026-11-10).
- **ρ: report both cases as the headline** (user, 2026-11-10): ρ = 1 and ρ = 0.5 for test- or
  state-graded benchmarks, side by side. Doubling-time alignment accepted (user).
- **Rows kept as reported:** best scaffold per model, custom scaffolds included (e.g. τ-banking's
  top row); WorkArena L1 includes StarShell's re-run of the same goals.

## 2026-11-09 — ρ: baseline 1, sensitivity 0.5 for test-graded benchmarks (supersedes the class values below)

ρ_b = the share of outputs that pass benchmark b's own grader that a competent reviewer at a firm
would accept as they are. It is about the benchmark's grader, not the firm's reviewer (review
effort is in b via stakes; client knowledge is in m). Evidence exists only for test-graded code
(Whitfill et al.: maintainers would merge about half of test-passing PRs), so class-specific
values would build an unmeasured cross-domain difference into the BPO-vs-economy comparison.
**Baseline ρ = 1 for every benchmark. One sensitivity case: ρ = 0.5 for benchmarks graded by
tests or programmatic state checks.** The projection scenario becomes "ρ for test-graded
benchmarks rises from 0.5 to 1."

## 2026-11-09 — Coder disagreements: reconcile, then adjudicate

Whenever two coders (or two model families) disagree, each is shown both codings and both sets of
reasoning, labelled X/Y in random order, and asked to pick one or write a revision. Agreement after
this round settles the item. Anything still unsettled goes to one Opus subagent, which sees
everything and makes the final call. All rounds are logged. (User's protocol, 2026-11-09.)

## 2026-11-09 — Horizons: fixed slope, location from estimated item times

Adopted (user). β is fixed at 0.84 per natural log (METR's median from timed baselines; 0.58 per
doubling), sensitivity 0.6 and 1.0. Only each benchmark's horizon H_b(t) is estimated, per model
and date, from per-item results where available, overall scores otherwise. Benchmark item times
come from the same coders, prompt style and coder mix as the work-item lengths, so compression
affects both sides alike; it distorts h/H mainly when the matched lengths are far apart (e.g.
GDPval multi-hour tasks vs ~30-minute written items). Sensitivity: "de-compressed" times,
stretching log times on both sides by ~1/0.37 around their centre. Anchors are dropped: they fixed
level bias only, and leaving them out keeps the benchmark-item prompt matched to the unanchored
Stage 2 length question.

## 2026-11-09 — Benchmark item times estimated by our coders: validation result

Plan (user agreed): instead of waiting on authors, have the same coders estimate human times for
benchmark items, so one estimator sits on both sides of h/H; first validated blind against
benchmarks that publish times. Run: `coding/bench_times/validation/` (SCORE.md, estimates.csv);
items: `benchmarks/timing_validation/`. 48 SWE-bench Verified items (annotator buckets) and 34
Terminal-Bench 2 tasks (author expert estimates). Note: both "published" times are themselves
human estimates, not measurements. Six security/CTF-style Terminal-Bench tasks were dropped for
every coder: irrelevant to IT/BPO, and one tripped a safety classifier mid-run.

- **Ordering is decent:** rank correlation 0.71 (SWE-bench buckets), 0.64 (Terminal-Bench).
- **Level bias is small for Sonnet** (Terminal-Bench median ratio ×0.75–0.83) but Terra estimates
  run ~2.4× Sonnet's on the same items, so the coder mix matters.
- **Strong compression — the main problem.** Estimates squeeze toward 1–2 hours: slope of
  log(estimate) on log(published) is 0.29 (Terminal-Bench) and 0.33 (SWE-bench buckets).
  Published 5–1,440 min became estimated 15–180 min; SWE-bench "<15 min" items got 20 min,
  ">4 hours" items 120 min. Only 12 of 34 Terminal-Bench items within 2×.
- **Consequence:** fitting curves on these times would distort β (the slope against length) and
  pull horizons toward the middle. The same compression may affect Stage 2's work-item lengths.

**Anchored re-run** (`coding/bench_times/validation_anchored/`; 11 held-out reference items with
known times, 5–960 min, in each brief): bias fixed for Sonnet (Terminal-Bench median ratio ×1.00;
Terra ×1.67), estimate range widened (15–360 min), but compression barely moved: slope 0.29 → 0.37
(Terminal-Bench), 0.33 → 0.37 (SWE-bench). Rank correlation unchanged (0.67–0.69). One Sonnet coder
skipped one item.

Reading: the compression is not mainly a scale-use problem that anchors fix. Part of it is
probably a real information limit (a short instruction can hide an eight-hour task), and part is
noise in the "published" times themselves, which are estimates too: noise in the yardstick
flattens the measured slope even for a perfect estimator, and METR found SWE-bench's "<15 min"
items actually took 8–84 min. Without measured times we can't separate the two.

## 2026-11-09 — Pilot Stage 2+3 result: folding confirmed; almost every match is "partial"

Run: `coding/stage2/pilot_v4c/` (features.csv, matches_final.csv, PRIMING.md, MATCHES.md). Four
Sonnet subagents (~87k tokens each) + Terra ($0.13; project total $0.51). These are the pilot's
Stage 2 and Stage 3 results.

- **Priming check passed; the stages stay folded.** The combined run's features show no shift
  against either separate-stage run (×1.00 on every length and review number) and the same
  spread as between the two separate runs (×1.17–1.20); stakes/context/domain agreement within
  the same range (55–65 of 67).
- **Match agreement:** all three coders 33 items, two 26, three-way split 8 (Opus adjudicated;
  one went to "none"). Four second choices were internally inconsistent and treated as none.
- **Coverage (share of coded weight):** User Support 0% good / 98% partial / 2% none; Customer
  Service 9 / 91 / 0; QA 0 / 96 / 4. Matched to Tier A (fittable now): User Support 18%
  (Terminal-Bench 2), QA 5%, Customer Service 0%.
- **Where the weight goes:** GDPval 23% (written deliverables: test plans, evaluations, reports,
  written replies), SWEeper-Bench 12%, τ-Voice 9%, WorkArena L1 9%, SWT-bench 6%, Terminal-Bench 2
  6%, ITBench 6%, WorkArena++ 4%. The τ family together is ~16%.
- **Implication:** pilot delegable shares need curves for Tier B benchmarks, led by GDPval. GDPval
  items are long (expert median ~5 h) relative to the written items matched to it, so the range
  check will matter. This order sets the acquisition priority (`benchmarks/ACQUISITION.md`).

## 2026-11-09 — Stages 2 and 3 folded into one pass (pending the priming check); Stage 3 settled

Folded at the user's suggestion: one read of instructions and items per item instead of two, and
half the subagents (Claude usage, not OpenAI spend, is the binding constraint). Prompt:
`prompts/stage23_combined.md`. Feature questions unchanged (Stage 2 v3); the match comes last in
each item's output. Batches of ~34 items (2 per Claude coder) to cut fixed subagent overhead.

**Check before relying on it:** the pilot run (`coding/stage2/pilot_v4c/`) is compared with the two
separate-stage runs (v2, v3). If its features stay within the v2-vs-v3 noise (typical length
×1.17; categories ~60 of 67 identical), folding stays. If they shift systematically, the stages
are split again and v3 features are kept. Caveat: batch size also changed (17 → 34), so a shift
could come from either.

Stage 3 decisions (user agreed): coders see **no benchmark human times** (range overlap is checked
in code); best and second-best match; catalog order shuffled per coder; baseline counts **good and
partial** matches (sensitivity: good only; "none" reported separately); catalog = the 44 Tier A
and B benchmarks. Combine: plurality on best; rating = lowest among coders who chose the winner;
Opus adjudicates three-way splits only.

## 2026-11-09 — Stage 2 v3 coded; this is the Stage 2 pilot result

`coding/stage2/pilot_v3/features.csv` (supersedes `pilot/`). 67 items × 3 coders, no validation
problems; Terra $0.10 (project total ~$0.37).

- **Review line per item** (fit to median p10/p50/p90 review points): median b = 0.16 (middle
  half 0.10–0.33); median a = 1.7 min. By occupation: Customer Service b ≈ 0.51 (reviewing a call
  means listening to most of it), User Support 0.15, QA 0.11. Mildly concave: in 47 of 67 items
  the slope falls from the short→typical to the typical→long segment (medians 0.20 vs 0.17), so a
  straight line is an acceptable approximation. Still no stakes gradient (low 0.31, medium 0.15,
  high 0.19). Half of items fall outside the literature range 0.10–0.33 (18 below, 15 above).
- **Run-to-run stability** (v2 vs v3, independent runs of the same coders): median item p50
  differs by a factor of 1.17 (90th percentile 1.5); stakes, context and domain identical for
  59–61 of 67 items. Within-run spread across the three coders is similar (median max/min 1.5).
- Lengths: User Support p50 30 min, Customer Service 8, QA 180 (v2: 120).

## 2026-11-09 — Review slope b from each item's own coded review times; context as coded

**Review slope.** Replaces the stakes → b lookup in SPEC §9. Stage 2 v3 asks review minutes for
the coder's p10, p50 and p90 items; each item's line a + b·h is fitted to the three points
(median across the three coders at each point; a ≥ 0). Why: in v2 the implied slope didn't vary
with stakes (low 0.28, medium 0.20, high 0.21) but did fall with item size (0.60 → 0.12), and a
constant would throw away information we can collect cheaply. The literature range 0.10–0.33
becomes a sanity check and a sensitivity case. Stakes no longer enters the standard rule; it is
still coded, reported, and available for the live-service penalty λ.

**Context.** No rubric change. Coded values are used as they are (almost all medium, m = 3);
the m levels are varied in sensitivity cases. (User: biased toward simplicity; defensible.)

## 2026-11-09 — Stage 2 pilot coded (67 items × 3 coders)

Output: `coding/stage2/pilot/features.csv`, summary `coding/stage2/pilot/SUMMARY.md`. No validation
problems. Terra cost $0.10 (project total $0.27).

- **Coders agree well.** Median item length: max/min across the three coders is 1.43 at the
  median item; one item above 3×. Terra differs from each Sonnet coder about as much as the two
  Sonnet coders differ from each other (median |log ratio| 0.22–0.29). Stakes never two steps
  apart; domain three-way split on 1 item.
- **Lengths (median across items of the combined p50):** User Support 30 min, Customer Service
  9 min, QA 120 min.
- **Open: context barely varies.** 57 of 67 items are "medium" for all three coders, and almost no
  item is "low". So m is nearly constant (3) across the pilot. Either firm work really is
  medium-context, or the rubric doesn't discriminate.
- **Open: review time doesn't rise with stakes.** The slope implied by each item's p10 and p50
  review answers is ~0.2 whatever the stakes (low 0.28, medium 0.20, high 0.21; spec: 0.10 / 0.20 /
  0.33). Caveat: a slope from two short items is noisy and inflated where fixed costs dominate.
- **Possible Stage 1 misses:** 9 items flagged "two groups" by at least two coders (3 by all
  three); 1297a flagged by two coders as mixing different work.

## 2026-11-09 — From Stage 2 on: best of three, no reconcile round

Stage 1 showed each model sides with its own coding when shown both, so the reconcile round adds
cost and little information. From Stage 2 on, three independent coders (two Claude subagents, one
Terra) are combined directly: median for numbers and ordered categories, median κ for domain;
plurality for Stage 3 benchmark matches (rule for three-way splits to be set then). An Opus
adjudicator is used only where no majority exists.

## 2026-11-09 — Stage 2 review time: two concrete items instead of a "trivially small" one

Coders give review minutes for their own p10 and p50 items. a = max(0, R10 − b·h10) with b from
stakes; R50 checks the stakes-based b. See `prompts/stage2_features.md`, change 6.

## 2026-11-09 — Stage 1 pilot schema final (79 parts)

Final table: `coding/stage1/v2_final/units_final.csv`, review file `v2_final/REVIEW.md`.
Shares of weight — User Support: discrete 62%, interpersonal 15%, physical 13%, no deliverable
6%, live 4%. Customer Service: discrete 50%, live 40%, interpersonal 7%, physical 2%. QA:
discrete 92%, interpersonal 7%, live 2%.

How it got there: 18 of 56 statements disputed between Claude (Opus) and Terra. After each saw
both codings, they agreed on 5; in the other 13, **each model picked its own coding**
(self-preference, despite random X/Y labels). The Opus adjudicator then picked Claude's coding
in 10 of 13, Terra's in 2, and revised 1, which is consistent with self-preference but can't be
told apart from Claude's codings being better. It barely matters at occupation level (all shares
within 3 points of Terra's) except User Support live service: 7% before duplicates (Terra: 15%).
Duplicates: 3 pairs collapsed (1282a=1288a, both models; 1283b=1285b and 14641a=14642a,
adjudicated; the adjudicator sided with Terra on a fourth, 1282b≠1288b). Terra was inconsistent
across runs on 14641a=14642a. OpenAI spend to date: $0.17.

**Lesson for later stages:** both model families favour their own output when shown both, so
the reconcile round settles little, and an adjudicator from one of the two coding families may
lean its own way. For Stage 2, numbers are combined by median across three coders (two Claude,
one Terra), which needs no adjudication; only category features with wide spread go through
the protocol.

## 2026-11-09 — Stage 1 pilot schema: v2 adopted

v1 coded steps done during a live call as DISCRETE (Customer Service Reps 9% LIVE_SERVICE). Prompt
v2 types each step by where it is done (customer waiting → LIVE_SERVICE) and splits when both
happen; Customer Service Reps are now 40% LIVE_SERVICE. Cross-check with GPT-6.1 Terra on the same
v2 briefs: occupation-level type shares agree within a few points (Customer Service 40% vs 42%
live; QA 91% vs 95% discrete); 38 of 56 statements agree statement by statement. The largest gap
is how much of User Support's verification, record-keeping and referral work is done live
(Claude: none; Terra: 25–40% of those statements). Final table:
`coding/stage1/v2/units_final.csv` (83 parts), review file `coding/stage1/v2/REVIEW.md`.
OpenAI spend so far: $0.12.

## 2026-11-09 — Exact duplicate statements are collapsed, symmetrically

Stage 1 v2 records `duplicates` separately from `overlaps_with`, but in practice neither Claude nor
Terra flagged any duplicates while coding one statement at a time. So duplicates come from a
separate pass, Stage 1b (`prompts/stage1b_duplicates.md`): Claude (Sonnet subagent) and GPT-6.1
Terra each compare all coded parts within an occupation. A pair is collapsed only when **both**
models flag it; pairs flagged by one model go to the hand-check. A collapsed pair becomes one part, with weight equal to the **mean** of the two weights (importance × time share). Taking the
mean rather than keeping either copy avoids choosing which statement survives, so collapsing
introduces no direction of its own; it only removes the double count. Partial overlaps are
recorded and left alone.

## 2026-11-09 — Pilot drops the three unrated Software QA statements

Three 15-1253 statements have no O*NET importance rating: they were carried over from an older
occupation in the 2020 taxonomy change, and one is about dust and humidity control. With no
weight they can't enter the weighted average, so the pilot codes 56 statements (16 + 13 + 27),
and the dropped ones are left out of the coder's context list too.

## 2026-11-09 — Reviewer strictness is a cut in acceptance probability, not a horizon divisor (form kept; values superseded above)

Replaces $k_b$ in SPEC §2 and §9. Acceptance becomes

$$
\pi(h) = \rho_b\;\sigma\!\big(\beta_b\,[\ln H_b(t) - \ln(m\,h)]\big),
$$

where $\rho_b \le 1$ is the share of outputs that pass benchmark $b$'s grader that a real
reviewer would also accept.

Why: the robust finding in Whitfill et al. (METR, Mar 2026) is that maintainers would merge
about half of test-passing PRs. The "≈7×" horizon ratio holds for one model only (five models
span ~2–20×). A probability cut matches the robust finding, is one number per grading class,
and is easier to explain ("half of what passes the tests would pass review").

Pilot values by grading class: programmatic (tests or state checks) $\rho = 0.5$, sensitivity
0.35–0.75; LLM judge $\rho = 0.75$, sensitivity 0.5–1; human experts against professional
standards $\rho = 1$, sensitivity 0.75–1. The projection scenario "$k_b$ halves" becomes
"$\rho_b$ rises halfway to 1."

What changes: unlike a divisor, $\rho_b$ caps acceptance below 1 even for very short items.
That's intended (a short patch can pass tests and still fail review), but it means programmatic
benchmarks never reach $\pi > 0.5$. This matters most under the LIVE_SERVICE rule, where
failures cost $\lambda h$.

## 2026-11-09 — β is per natural log of time

SPEC §2 uses natural logs. METR and most sources report β per doubling of human time, so
multiply their β by $1/\ln 2 \approx 1.443$ (METR median 0.58 → 0.84). The exclusion rule
(Kwa & Cheng: β < 0.25) is in METR's per-doubling unit, i.e. 0.36 per ln; Terminal-Bench 2
(0.19 per doubling) falls below it.

## 2026-11-09 — Live customer service: sampled QA plus a failure cost

Live chats and calls (Stage 1 type LIVE_SERVICE) get no per-item review before the customer
sees the output, so the spec's rule ("review, then accept or redo") doesn't apply. For these
items:

- The agent handles the conversation.
- The firm QA-reviews a share $q$ of conversations at the usual review time $a + bh$.
- A failed conversation (probability $1-\pi$) escalates to a worker, who redoes it with AI help,
  $(1-\kappa)h$, plus a penalty $\lambda h$ for the customer's bad experience.

Assist costs $(1-\kappa)h$. Delegation costs $q(a+bh) + (1-\pi)\big[(1-\kappa)h + \lambda h\big]$.
So the firm delegates when

$$
\pi(h)\,(1-\kappa)\,h \;>\; q\,(a + b\,h) \;+\; (1-\pi(h))\,\lambda\,h .
$$

New parameters: $q$ (contact-centre QA sampling, roughly 0.02–0.05; to be sourced) and
$\lambda$ (a judgment call, needing wide sensitivity; it could vary by stakes). Unlike the
standard rule, failures now cost something, so items with low reliability stop being
delegated.

Rejected: D = 0 (likely understates BPO); splitting conversation from fulfilment (no model
change, but assumes customers keep talking to people; could be combined with this later);
splitting by channel (needs chat-vs-voice shares).

## 2026-11-09 — Coders run as Claude subagents, not API calls

Free under the enterprise plan. Consequences and safeguards (batching, independence,
random order per coder, no file or web access, validation scripts) are in `prompts/RUNNING.md`.

## 2026-11-09 — Stage 1 prompt changes

Full task list given as context; split and classify are separate steps; new types
LIVE_SERVICE and NO_DELIVERABLE; `checked_by` field; a rule for choosing the unit level; a
rule against splitting on lists of alternative methods; a rule for statements that describe
one step of a workflow. Details are in `prompts/stage1_unit_schema.md`.
