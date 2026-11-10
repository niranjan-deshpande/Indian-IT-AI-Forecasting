# workarena_l1 (WorkArena L1)
Accessed 2026-11-09. Licence: WorkArena code Apache-2.0; ServiceNow-AI task datasets Apache-2.0.

## URLs
- Task goals: HF dataset ServiceNow-AI/servicenow-tasks (330 rows, 33 templates x 10 seeds; derived from WorkArena L1), file saved at ../starshell/raw/servicenow-tasks.parquet
- Template list and curriculum: github.com/ServiceNow/WorkArena (browsergym-workarena 0.5.3) src/browsergym/workarena/__init__.py (raw/wa_init.py)
- Paper arXiv 2403.07718 (v5, Jul 2024), Table 6 oracle action counts (raw/wa1.pdf)
- Scores: HF Space ServiceNow/browsergym-leaderboard results/*/workarena-l1.json (raw/lb/), plus paper Table 2 and the StarShell paper (arXiv 2604.00073)

## Population and sampling
Headline score = mean success over 330 tasks = 33 templates x 10 seeds, so every template has equal weight. Sampled 24 of the 33 template names with random.Random(2026).sample(sorted names, 24). Each item text is the real goal of the lowest-seed instance of that template in the HF dataset (seeds may differ from the leaderboard's seeds; goals are template-typical). Gold steps = mean oracle Playwright actions per template from the paper (meta.gold_steps_mean_oracle_playwright_actions).

## Grading method
`state`: programmatic validators check the ServiceNow record, list view state or the chat answer against the goal.

## Description for time estimators
One explicit instruction in a ServiceNow IT-service-management web UI (for example create a record with given field values, filter or sort a list, order a catalog item, find a knowledge-base answer, read a value off a chart); done when the record, list state or answer matches the goal.

## Human times
None published. Oracle action counts (1 to 47 Playwright actions per template) are the only effort proxy.

## Problems
- Headline for 2025-26 leaderboard rows is near saturation (Gemini-3-Flash 90.3%).
- Scaffolds differ: older rows use AgentLab GenericAgent (15 max steps); GPT-5 and Gemini-3-Flash rows raised max_steps to 30 and are flagged as not following protocol.
- Leaderboard date_time is a 2021-01-01 placeholder for several rows; eval_date in scores.csv comes from study_id.
- Claude-3.5-Sonnet snapshot unspecified. Gemini-3-Flash release date from memory (not verified).
- StarShell (2026) rows re-grade the same 330 goals with a different harness and grader; keep them separate or flag them in fits.
- Items are a public, fixed 330-task curriculum, not a subset of a larger private set. Instances need a ServiceNow developer instance to run; not needed here.
