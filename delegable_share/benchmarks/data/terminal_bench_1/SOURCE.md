# terminal_bench_1 (Terminal-Bench 1.0, terminal-bench-core 0.1.1)
Accessed 2026-11-09/10.
- Task list: registry.json of github.com/harbor-framework/terminal-bench-1 (entry terminal-bench-core 0.1.1, 80 task ids incl. .easy/.hard variants, commit 91e10457b5410f16c44364da1a34cb6de8c488a5 of laude-institute/terminal-bench branch dataset/terminal-bench-core/v0.1.x). Task text from tasks/<id>/task.yaml at that commit (saved in raw/tasks/). Repo licence Apache-2.0 (not re-checked).
- Scores: github.com/laude-institute/terminal-bench-leaderboard results/terminal-bench-core@0.1.1/*/<run>/results.json (raw/tb1_leaderboard_raw.json).
## Population and sample
- 80 tasks minus 13 excluded by analogy to the TB2 caller instruction: all 12 category=security tasks plus qemu-alpine-ssh. Population 67 (variants counted separately as in the leaderboard). Sample random.Random(2026).sample(sorted 67, 24). One task (blind-maze-explorer-5x5) truncated.
## Grading method
tests: pytest on final machine state.
## Description for time estimators
Same format as Terminal-Bench 2.0 with shorter everyday items: Linux machine, written instruction, done at the command line (git, builds, servers, small data/ML tasks). Done means hidden tests pass.
## Human times
core 0.1.1 task.yaml has no time fields. meta.expert/junior_time_estimate_min were back-filled from main-branch original-tasks/<id>/task.yaml of terminal-bench-1 where the id (or base id for variants) exists; null for 9 of 24 sampled items. Author estimates, not measurements.
## Problems
- Only 6 models; only submissions with parseable run results (6 skipped: goose x2, orchestrator x3, camel-agent use a different layout). Official Terminus/Codex baseline rows were not retrievable (leaderboard page JS-rendered).
- Score is mean accuracy over ~5 runs of the best submission for each model, over all 80 tasks; 67-task value in notes. Scaffolds differ (Droid, Ante, Apex, iflow).
- Older models (GPT-4o, o3, Claude 3.x) absent. Release dates from memory.
- Time fields missing for many items; items overlap with TB2 (same task names, different versions).
