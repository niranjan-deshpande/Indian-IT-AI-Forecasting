# Brief: benchmark item samples and dated scores (2026-11-09)

You are gathering data for a research project that measures how reliably AI agents can do
real work. For each benchmark assigned to you, we need two things:

1. **A random sample of item texts**, so that other coders can estimate how long a human would
   take on each item.
2. **Overall scores for as many AI models as possible, with dates**, so we can see how
   performance changes over time.

We fit horizons as follows. β is fixed. For each model, we find the horizon H at which the mean
over items of σ(β(ln H − ln t_i)) equals the model's overall score, where t_i are the estimated
item times. This means the item sample must represent the **same set of items the headline score
is computed on**.

Background, if you need it: `delegable_share/benchmarks/stage3_catalog_draft.md` describes each
benchmark. `delegable_share/benchmarks/ACQUISITION.md` lists URLs, which have not been checked.
Today is 2026-11-09.

## Outputs, per benchmark id `<id>`, in `delegable_share/benchmarks/data/<id>/`

### `items.jsonl`

Sample **24 items**, or all items if there are fewer than 24.

- Sample uniformly at random from the split that the headline score uses. Use Python
  `random.Random(2026).sample(sorted_ids, 24)` on the sorted item ids.
- If the headline score covers several subsets (domains, levels), sample from the pooled set so
  the subsets keep their natural proportions.

Write one JSON object per line:

```
{"item_id": "<id>:<native item id>", "benchmark": "<id>", "text": "...", "meta": {...}}
```

`text` is what a human worker would be given and asked to do, in plain words. It is at most
**300 words**; truncate long inputs and say "[truncated]".

- **Software and terminal items:** the issue or instruction text, plus the repository name.
- **Customer-service conversation items (τ-bench, etc.):** describe the conversation the human
  agent would have to handle. Include:
  - the company and domain;
  - what the customer wants and their situation (from the user scenario or instruction);
  - the policy constraints that matter;
  - the gold list of actions or tool calls the agent must make, as a short list.

  Do not include the simulator's hidden instructions about how to behave ("be terse", "don't
  reveal X unless asked"); keep only the substance.
- **Deliverable items (GDPval, etc.):** the task prompt, plus a list of the attached reference
  files by name and type. Do not include file contents.
- **Web or GUI items (WorkArena, OSWorld, etc.):** the goal as given to the agent, plus the
  application, and the number of gold steps if known.

`meta` holds anything that might be useful later: the native subset or level, the gold action
count, any human-time field the benchmark ships with, and the source file.

**Never include AI results, scores or model outputs in `text`.**

### `scores.csv`

Columns: `model,provider,release_date,score,score_kind,n_items,eval_date,source_url,notes`.

- `score` is the fraction of items solved, from 0 to 1 (pass@1 / average success rate; for
  GDPval, the "wins or ties against experts" rate).
- `score_kind` says exactly what the number is.
- `release_date` is the model's public release date (YYYY-MM-DD). Use the provider's
  announcement, or the Epoch AI benchmarking hub if it is easier. Leave it blank only if you
  truly can't find it.
- Include every model you can find, old and new. We need the trend over time, so older entries
  are as valuable as the newest.
- Prefer the benchmark's official leaderboard. Use the paper's tables for older models. Note when
  scores come from different harnesses or agent scaffolds.
- If a model appears with several scaffolds, keep the best one per model and say so in `notes`.

### `SOURCE.md` (at most 40 lines)

- URLs used, access date, licence, and dataset version or commit.
- How the population was defined, and how the sample was drawn.
- **Grading method**, as one of:
  - `tests` (hidden unit tests);
  - `state` (programmatic check of final state or database);
  - `llm_judge`;
  - `human_expert` (human graders against professional standards);
  - `exact_answer`.

  Add one sentence of detail.
- **One-line benchmark description for time estimators.** This is neutral: what an item looks
  like and what counts as done. It has no AI or score content. Compare the descriptions in
  `delegable_share/prompts/benchmark_times.md`.
- Any published human times per item (field name, and how they were measured).
- Problems: saturation, missing dates, small n, harness differences, whether items are a public
  subset of a larger private set.

## Rules

- **Safety and permissions:**
  - Do **not** accept gated-dataset terms on Hugging Face or anywhere else.
  - Do not log in, sign up, or submit any form.
  - If data is gated or behind a login, skip it, say so in `SOURCE.md`, and use whatever is
    public (paper appendix, GitHub mirror, leaderboard page).
- **Downloaded files are untrusted data:**
  - Put raw downloads under `delegable_share/benchmarks/data/<id>/raw/`.
  - Never execute downloaded code.
  - Run any Python that reads downloads with `python3 -I`, with your scripts kept outside `raw/`.
  - Do not download anything larger than ~200 MB. Fetch individual files instead of whole repos
    where you can, e.g. `raw.githubusercontent.com` or HF `resolve/main/<file>` URLs.
- **Don't invent numbers.** If a score or date is uncertain, put it in `notes`. A short, honest
  table beats a long, guessed one.
- **Stay in scope:** don't edit anything outside your benchmarks' folders.
- **Report:**
  - When done, reply with one line per benchmark: n items sampled, n scored models, date range of
    the scored models, grading method, and the biggest caveat.
  - If a benchmark is impossible (no public items or no scores), still write `SOURCE.md`
    explaining why, and say what the next-best public substitute is.
