# workarena_pp (WorkArena++ L2 + L3)
Accessed 2026-11-09. Licence: WorkArena Apache-2.0.

## URLs
- github.com/ServiceNow/WorkArena src/browsergym/workarena/tasks/compositional/ (curriculum in utils/curriculum.py; saved under raw/). Paper arXiv 2407.05291 (raw/wapp.pdf).
- Scores: HF Space ServiceNow/browsergym-leaderboard results/*/workarena-l2.json and workarena-l3.json (copies in ../workarena_l1/raw/lb/), plus paper Table 2.

## Population and sampling
Headline for the pooled benchmark = 470 task slots = 235 per level (L2, L3) in the agent curriculum: 5 skill categories (planning 44, information retrieval 56, data-driven decision making 55, sophisticated memory 48, infeasible tasks 32) built from num_seeds x bucket weights in curriculum.py. (The WA++ paper's "682" counts 341 workflows x 2 presentation styles but the evaluated agent curriculum is 235 per level; the A3 leaderboard comment says 341, inconsistent.) I enumerated all 470 slots as ids `<level>/<category>/<bucket>/<slot>` (slot is just an index), sorted, and took random.Random(2026).sample(ids, 24). Items are template buckets, not exact instances: instances are generated at run time from a seed, so each text is a composed example paraphrasing the source template's goal/ticket with invented placeholders (flagged in meta.note). L2 = explicit numbered steps from the home page; L3 = ticket in "My Work" that points to a company protocol in the knowledge base.

## Grading method
`state`: programmatic validators check every resulting record (and the chat answer where one is needed). Infeasible tasks are graded on the agent reporting infeasibility.

## Description for time estimators
A multi-step service-desk job in ServiceNow (given as numbered steps, or as a ticket that points to a company protocol), for example offboard a user, clean up duplicate problems, allocate a budget over expense lines, or order items for agents chosen from a report; done when all resulting records are correct.

## Human times
None published. Human study (15 participants, 98-instance human curriculum, 93.9% success) recorded time to resolution but it is not released; ACQUISITION.md plans to email the authors.

## Problems
- scores.csv uses the mean of L2 and L3 success (equal n). Only 12 models have both levels; models with only an L2 entry are in scores_l2_only.csv.
- Pooled scores are floor-dominated: L3 is 0% for all but GPT-5 (11.5%, with max_steps raised to 100) and Claude-3.5-Sonnet (0.4%).
- Mixed scaffolds and dates (paper Jul 2024; leaderboard 2024-10 to 2025-08). Release date of AgentTrek not verified. No frontier rows after Aug 2025.
- Sampled texts are composed examples, not verbatim instances; gold step counts and the L2/L3 task times are unknown (meta.gold_steps null).
- Public benchmark; instances require a ServiceNow instance to generate.
