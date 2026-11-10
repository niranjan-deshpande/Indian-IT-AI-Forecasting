# Stage 3 prompt: benchmark match — v1 draft (2026-11-09)

Each DISCRETE or LIVE_SERVICE work item is matched to the benchmark whose items are most like it.
The match decides which success-vs-length curve (H_b(t), β_b) sets the item's acceptance
probability. Changes from the spec appendix are listed at the bottom.

## Inputs (per item)

Occupation, task statement, and from Stage 1–2: type, work item, start, end, checked_by, domain.
**Not** item length (see change 2). Catalog: `benchmarks/stage3_catalog_draft.md` with the human-time
lines removed, groups and entries shuffled per coder.

## Run plan

- Three coders (two Sonnet subagents, Terra), batches of ~17, random item order per coder; each
  coder sees the catalog in its own random order (groups shuffled, entries shuffled within groups).
- Combine: plurality on `best`. Its rating = the lower rating among coders who chose it (if two
  agreed) or their shared rating (if three). Three-way split → Opus adjudicator (only case).
- `second` is combined the same way and used as a fallback when the best match has no usable
  curve yet, and as a robustness check.

## Prompt

```
You are matching work items to benchmarks. Each benchmark in the list below
is a set of tasks used to test how well software agents can do a kind of
work. For each work item, find the benchmark whose items are most like it in
what the worker has to do: the inputs, the actions, and what counts as a
correct result.

Describe and compare the work only. Do not consider how well AI performs on
any benchmark, how hard the benchmark is, or how long its items take.

Rate each match:
  - good: the benchmark's items are the same kind of work
  - partial: they share the main actions but differ in an important way
    (say how)
  - none: no benchmark is close. Do not force a match.

Give your best match and your second-best match (another benchmark, or
"none"). Write two sentences of reasoning before choosing.

Output, per item:
{
  "item_id": "...",
  "reasoning": "...",
  "best": "<benchmark id or none>", "best_match": "good | partial | none",
  "best_difference": "if partial: the important difference",
  "second": "<benchmark id or none>", "second_match": "good | partial | none"
}
```

## Worked examples

To write once the catalog is final: the three Stage 2 example items (bookkeeping batch check;
network alert investigated; appointment booked during a call) with their matches, including at
least one "none" or "partial".

## Changes from the spec appendix, and why

1. **Best and second-best.** Many matched benchmarks will have no fitted curve yet (Tier B). The
   second choice gives a documented fallback instead of an ad-hoc one, and agreement between
   first and second choices shows how sharp the match is.
2. **No human times in the catalog, and no item length in the input.** The spec says similar length
   isn't enough. Showing times invites matching on length. Whether the item's length falls
   inside the benchmark's tested range is checked in code afterwards: items far outside it are
   extrapolations and get flagged.
3. **Catalog order shuffled per coder,** so position in the list can't drive the match.
4. **Domain from Stage 2 given as context,** not as a filter: a computer-use item can match a
   text benchmark if the actions are the same.

## Open decisions

- **Show human times or not** (change 2).
- **Partial matches in the baseline?** Proposal: baseline uses good and partial; sensitivity uses
  good only; "none" is reported separately (as in the spec).
- **Catalog scope.** Tier A and B only (44 entries). Tier C is excluded or on watch, so matching
  to it couldn't produce a curve.
