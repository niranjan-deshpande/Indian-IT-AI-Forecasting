# Running the coders as Claude subagents (not API calls)

Decision 2026-11-09: every coding stage runs as Claude Code subagents launched from a
session, which costs nothing extra under the enterprise plan, rather than as API calls.
This file describes how, and what that changes in the design.

## What changes

| Spec assumes (API) | With subagents | How we handle it |
|---|---|---|
| One call per statement, fresh context each time | One agent codes a **batch** in one context, so earlier items can anchor later ones | Small batches (~15–20 items). Each of the three coders gets the items in a **different random order**, so anchoring doesn't line up across coders. Stage 2/3 batches mix occupations. |
| Coders independent by construction | Agents can read the file system, including other coders' output | Brief each agent with only the prompt text and its inputs, embedded inline. Tell it to read nothing else and write only to its own directory. Launch the three coders at the same time. |
| Coders see only the prompt | Agents could open SPEC.md (model, parameter values, framing) | Same as above. The coders never see the spec, so knowing what the numbers feed can't bias them. |
| Temperature/seed fixed, exact model pinned | No control over temperature or seed; the model is whatever the session runs | Record model ID, date and batch ID in every output. Keep all raw outputs. Reproducibility means "same prompt, same model", not identical bytes. |
| Structured output enforced by the API | Agent writes JSON files by hand | `scripts/validate_stage{1,2,3}.py` checks schema, shares sum to 1, p10 ≤ p50 ≤ p90, categories valid. Failed items get re-queued to a fresh agent. |
| Model knowledge only | Agents have web search | Forbidden in the brief for Stages 1–2 (they should describe work from general knowledge, consistently). Revisit later as a variant. |

## Models

- Stage 1 (one pass that everything downstream inherits): Opus.
- Stages 2–3 (three coders, many batches): Sonnet.
- Never Fable.
- Optional cross-family check: an OpenAI model (Terra or Sol, never Astra), with the key in
  the repo-root `.env` (gitignored) and a per-run spend cap (`OPENAI_MAX_USD`).

## Batching plan

| Stage | Unit of work | Pilot (56 statements) | BPO set (~269) |
|---|---|---|---|
| 1 Unit schema | one agent per occupation (it needs the full task list anyway) | 3 agents | 13 agents |
| 2 Features | ~20 work items per agent, × 3 coders | ~80 items → ~12 agents | ~400 items → ~60 agents |
| 3 Benchmark match | ~20 work items per agent, × 3 coders; catalog given once per batch | ~12 agents | ~60 agents |

The comparison sample (600–1,000 statements) would mean a few hundred agents, so it would
run in waves. For that scale, the Workflow tool can run the fan-out and validation as a
script, but it needs your explicit go-ahead each time.

## Files

```
prompts/stage{1,2,3}_*.md       the coder instructions (what goes in the brief)
coding/stage1/<onetsoc>.json    one file per occupation, list of statement schemas
coding/stage2/coder_{1,2,3}/<batch>.json
coding/stage3/coder_{1,2,3}/<batch>.json
coding/batches/                 batch manifests: item IDs, order, coder, model, date
scripts/make_batches.py         builds manifests (random orders per coder)
scripts/validate_stage*.py      checks outputs, lists items to re-run
scripts/combine.py              medians/modes across coders, spread, flags
```

## Brief template (wraps each stage prompt)

```
You are a coder in a research pipeline. Follow the instructions below exactly.
Use only the information in this message: do not read any files, and do not
search the web. Code each item independently, in the order given. Do not
compare items or adjust earlier answers.

Write one JSON array to <output path>, one element per item, each element
being the output object described in the instructions plus "item_id". Write
nothing else. Then reply "done <n> items".

=== INSTRUCTIONS ===
<stage prompt, incl. worked examples>
=== ITEMS ===
<items>
```
