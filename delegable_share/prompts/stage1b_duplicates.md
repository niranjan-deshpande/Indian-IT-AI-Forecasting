# Stage 1b prompt: duplicate work items — v1 (2026-11-09)

Why a separate pass: in Stage 1 each coder sees one target at a time, and neither Claude nor
GPT-6.1 Terra flagged a single duplicate, even where an umbrella statement (43-4051 task 18565,
"…take or enter orders, cancel accounts…") contains another statement's work (2584,
"…issue service discontinuance orders…"). Comparing all parts of an occupation side by side is
an easier judgment. Two models run this independently, and a pair is collapsed only when both
flag it (rule in `../DECISIONS.md`); pairs flagged by one model go to the hand-check.

## Prompt

```
You are checking a list of work items for duplicates. All items come from
one occupation. Each item has an ID, a type, a description, and where it
starts and ends.

Two items are DUPLICATES if a worker doing one of them has thereby done the
other: the same inputs, the same actions, the same output, in the same
setting (live with a waiting customer, or afterwards). If both stayed in the
list, the same work would be counted twice.

They are NOT duplicates if:
  - one is a step that comes before or after the other (taking a complaint
    vs. resolving it vs. recording it);
  - they produce different outputs (a test plan vs. a test procedure
    document), even if the same person often does both;
  - one is done live and the other afterwards;
  - one is a narrower case that is only a small part of the other, unless
    the narrower item covers most of the broader one's work.

Be conservative. Only list a pair when one item is clearly redundant
given the other. Most lists have few or no duplicates.

For each pair, write one sentence of reasoning first.

Output JSON only:
{"pairs": [{"reasoning": "...", "a": "<item id>", "b": "<item id>"}]}
```
