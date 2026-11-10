# Pilot lessons (2026-11-09)

Pilot: 3 occupations (15-1232 User Support, 43-4051 Customer Service, 15-1253 Software QA), 56
statements → 79 work items, 67 coded. Full decision log with dates and numbers: `DECISIONS.md`.
This file is the condensed version: the pipeline as it should now run, what we learned, and
what's still missing.

## 1. Pipeline as it should run at scale

| Step | What | Who | Prompt / script |
|---|---|---|---|
| 1 Units | Split, type, name work item per statement | Opus subagent per occupation; Terra cross-check on same brief | `prompts/stage1_unit_schema.md` (v2); `scripts/stage1_briefs.py`, `openai_stage1.py`, `validate_stage1.py` |
| 1 disputes | Type mix differs ≥0.25 or part count differs | Opus adjudicates directly (no reconcile round) | `scripts/reconcile_stage1.py` (build/adjudicate/finalize; skip the `terra` round) |
| 1b Duplicates | Side-by-side pass over all parts in an occupation | Sonnet + Terra; collapse if both flag; one-model flags → Opus | `prompts/stage1b_duplicates.md`; `scripts/stage1b_duplicates.py`, `reconcile_dupes.py` |
| 2+3 Features + match | Domain, length p10/50/90, review p10/50/90, stakes, context; best + second benchmark | 2 Sonnet + Terra, batches ~34, own random order and catalog order | `prompts/stage23_combined.md`; `scripts/stage23.py` + `stage2.py validate/combine` |
| 2+3 combine | Median numbers/ordered categories; median κ for domain; plurality match, rating = lowest of agreeing coders | script; Opus only for three-way match splits | `stage23.py matches/adjudicate/apply_adj` |
| Benchmark times | Same coders estimate human time per benchmark item (no anchors) | same mix as 2+3 | `prompts/benchmark_times.md`; `scripts/bench_times.py` |
| Benchmark data | 24 random items + dated scores + grading per matched benchmark | Sonnet subagent per family | `benchmarks/data/BRIEF.md` |
| Curves | Fixed β = 0.84/ln; H per model from overall score; align to today at pooled doubling | script | `scripts/horizons.py` → `benchmarks/HORIZONS.md` |
| D, S | Delegation rule over hours-weighted lognormal; D and net saving S; scenarios | script | `scripts/delegable.py` → `coding/stage2/<run>/delegable/` |

Model parameters now: ρ = 1 (sensitivity 0.5 for test-graded); review line a + b·h fitted per
item to its three review points (stakes not used); context m as coded (almost all medium = 3);
LIVE_SERVICE rule π(1−κ)h > q(a+bh) + (1−π)λh with q, λ still to source.

## 2. What we learned about the method

**Units (Stage 1)**
- O*NET often splits one workflow into several statements (talk to customer / record it / check
  the fix / refer it). Each statement's work item must be its own step's output, or everything
  collapses into "one call" and importance is double-counted.
- Where a step happens matters: steps done while the customer waits are live service. v1 coded
  them as back-office items and gave Customer Service 9% live; the "where is it done" rule gave 40%.
- Importance weights are not time. 40% live for Customer Service understates time on calls. Always
  report equal weights alongside.
- Duplicates are never flagged while coding one statement at a time (0 in both models). A separate
  side-by-side pass finds them; even then a single model is inconsistent across runs.
- ~9 items were flagged by ≥2 coders as containing "two groups" of work: candidates to re-split.
- Final pilot shares (weight): User Support 62% discrete / 4% live / 15% interpersonal / 13%
  physical / 6% no deliverable; Customer Service 50 / 40 / 7 / 2 / 0; QA 92 / 2 / 7 / 0 / 0.

**Features (Stage 2)**
- Coders agree well on numbers: max/min across three coders ≈1.4–1.5× on typical length;
  independent re-runs differ by ×1.17 (90th pct ×1.5). Categories agree ~60/67 across runs.
- Review time does not depend on stakes (slope ≈0.2 at every level) but does depend on size and
  occupation: Customer Service b ≈0.5 (listening to a call), QA ≈0.11, User Support ≈0.15; mildly
  concave. Hence per-item lines, not a stakes lookup.
- "Trivially small item" is a bad question; ask about concrete items the coder already described.
- The context rubric doesn't discriminate (57/67 "medium" for all coders).
- Typical lengths: User Support 30 min, Customer Service 8 min, QA 120–180 min.

**Matching (Stage 3)**
- Folding Stages 2 and 3 doesn't prime the feature answers (no shift, same spread) and halves the
  subagents.
- Almost every match is "partial" (91–98% of weight). Matched to benchmarks fittable today: User
  Support 18%, QA 5%, Customer Service 0%.
- GDPval absorbs written deliverables (23% of pilot weight) but its tasks are multi-hour; the
  written items are ~30 min, the worst case for length mismatch.
- Weight by benchmark: GDPval 23%, SWEeper 12%, τ-Voice 9%, WorkArena L1 9%, SWT 6%,
  Terminal-Bench 2 6%, ITBench 6%; the τ family ~16% in total.

**Benchmarks and horizons**
- Human times per benchmark item are the binding constraint; most IT/BPO-like benchmarks lack them.
  Even "published" times are often estimates (SWE-bench annotators, Terminal-Bench authors).
- Our coders' blind time estimates rank items decently (Spearman ≈0.67–0.71) but compress hard
  (slope of log estimate on log published ≈0.3–0.37). Reference items (anchors) fixed level bias,
  not compression. Hence: fixed β, estimate only the horizon's location, same estimator both sides.
- Terra estimates benchmark item times 1.7–2.4× Sonnet's (but not work-item lengths), so the
  coder mix must be identical on both sides.
- Reviewer strictness: the "≈7×" (Whitfill) is one model (2–20× across five); the robust result is
  ~half of test-passing PRs merged. Evidence exists only for code, so ρ = 1 baseline.
- β is reported per doubling by METR; ours is per natural log (×1.443).
- Some benchmarks fit the logistic poorly (OSWorld 2.0, Remote Labor Index, Terminal-Bench 2 weak
  time–success link); several are saturated (τ²-telecom, OSWorld-Verified, MedAgentBench).

**Coders and adjudication**
- Both model families pick their own coding when shown both (13 of 18 disputes). A reconcile round
  settles little; skip it. An Opus adjudicator then sided with Claude's codings 10 of 12, which
  may be self-preference. Best of three by median avoids adjudication for numbers.

## 3. Operational lessons

- Claude usage, not OpenAI spend, is the constraint. A subagent costs ~65–70k tokens of fixed
  overhead; larger batches (~34 items, briefs ~6–7k words) cost ~85–110k per agent. Fewer, larger
  batches are the main lever.
- OpenAI (GPT-6.1 Terra, $1/$5 per M tokens) cost ~$0.70 for the whole pilot. Every call goes
  through `scripts/openai_client.py` with a ledger (`coding/openai_ledger.jsonl`) and an $80 cap.
- Briefs must be self-contained ("read only this file", outputs to one path). Agents' "done n items"
  is not proof: one miscounted, one skipped an item, four gave inconsistent second choices. Always
  validate with the scripts.
- Security/CTF-style benchmark items can trip a safety classifier mid-run; exclude them (they're
  irrelevant to IT/BPO anyway).
- Small parsing traps cost time: wrapped bullets in prompt files, hyphen vs underscore ids.

**Second half (2026-11-10)**
- Pilot snapshot (importance-weighted; D = share of hours delegated, S = net hours saved):
  User Support D 58% / S 20%; Customer Service 85% / 33%; QA 66% / 15%.
- Biggest levers, in order: date alignment (no alignment: D 42/58/47%); ρ = 0.5 for
  test/state-graded benchmarks (Customer Service D 85% → 22%); λ (λ = 3: CS 68%); β moves QA
  54–82%. Coverage is no longer the issue (≤6% uncovered), but most matches are "partial".
- Score data is uneven: some benchmarks stop in 2025, scaffolds and harnesses are mixed, and dates
  partly come from secondary sources. Sonnet coders' times for 480 benchmark items agree within
  ~1.25×; Terra barely moves the medians.
- With failures costing only review, cheap review makes D large even at low π; report S alongside.

## 4. Still missing before results

1. **Check the levers above with the user:** date alignment rule, ρ, λ, and whether D or S is the
   headline.
2. **BPO run:** Stages 1–3, then gather data for any newly matched benchmarks (same brief).
3. **Parameters to source:** q, λ (QA sampling share, failure penalty) for live service.
4. **Comparison sample not drawn** (30–50 occupations, employment-weighted).
5. **Nothing is committed** (including the repo reorganisation).
