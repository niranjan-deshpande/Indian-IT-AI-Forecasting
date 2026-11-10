# osworld_2 (OSWorld 2.0)
Accessed 2026-11-10. NO items.jsonl written: task items are not public.
- Task classes (task_*.py) are only in HF xlangai/osworld_v2_tasks, which is GATED; I did not accept the terms. Full assets are in gated xlangai/osworld_v2_assets_gated. GitHub xlang-ai/OSWorld-V2 (Apache-2.0, latest release osworld-v2.1, 2026-09-16) has code and release manifests but no task list/instructions. osworld-v2.xlang.ai/task-showcase/ is JS-rendered (no text retrievable); the site shows 3 failure-case walkthroughs (Task035, Task103, Task008) only as summaries. arXiv 2606.29537 not read (could carry a few example tasks).
- Next-best substitute for items: osworld_verified (v1, public) for GUI tasks, or hand-write items from the paper's appendix examples if the paper lists some.
- Scores: Steel leaderboard https://leaderboard.steel.dev/leaderboards/osworld-2.md (page dated 2026-09-30), mixing author runs, vendor self-reports and co-author (Snorkel/Simular) runs. Rows with a published binary score only (12 models); partial scores are in notes.
## Population
108 tasks, 31 self-hosted websites, 7 professional domains, 21 sub-categories (osworld-v2.xlang.ai).
## Grading method
state: programmatic execution-based checkers on final state, average 27.25 checkpoints per task; binary = all checkpoints pass, partial = fraction passed.
## Description for time estimators
A long end-to-end office workflow on a desktop with real input files, desktop applications and internal websites (email, banking, team chat, portals, GitLab). Example: follow a PDF guide, extract receipt data, cross-check bank and email records, and file an expense claim. Done means every checkpoint on the final state passes.
## Human times
Median about 1.6 h; 69.6% of tasks over 1 hour (project site); per-task times not public.
## Problems
- No items: gated. No per-row run dates (eval_date = page date); mixed step budgets (500 default), effort levels and tool modes; Fable 5.1 row ran modified tasks/grading; OpenAI/Google rows use an "offline subset" and report only partial scores (omitted). Benchmark releases (06.24, 08.08, v2.1) changed tasks/grading, so scores across dates are not strictly comparable. Simular Sai is an agent system, not listed.
