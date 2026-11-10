# terminal_bench_4 (Terminal-Bench 3.0 / 4.x; headline = 4.1)
Accessed 2026-11-10.
- Tasks: github.com/harbor-framework/terminal-bench, tasks/*/task.toml + instruction.md, main @ 9a318be656d4 (2026-11-09). Apache-2.0 (GitHub licence field). 66 task dirs = the 66 tasks of TB 4.0/4.1 (BenchLM; the 3.0 launch had 74). Raw in raw/.
- Scores: BenchLM snapshot 2026-11-09 (https://benchlm.ai/md/benchmarks/terminal-bench-3.md), TB 4.1 leaderboard mirror; tbench.ai leaderboard is JS-rendered and returned no rows. Launch table (tbench.ai/news/terminal-bench-3-0, 3.0 era, 74 tasks) not used.
## Population and sample
- All 66 tasks minus the 5 category=Security tasks (formal-crypto, html-js-filter, interleaved-vigenere, shadow-relay, uefi-bootkit), excluded as for terminal_bench_2 (safety-filter scope). Population = 61.
- Sample: random.Random(2026).sample(sorted 61 task names, 24). Text = instruction.md, truncated at 300 words.
## Grading method
tests: hidden verifier scripts check outputs and final machine state (some tasks all-or-nothing over many sub-checks; a few drive web services).
## Description for time estimators
A Linux machine plus a written instruction describing a long, realistic job (infrastructure, data pipelines, operations/claims/compliance processing, science or ML engineering) done at the command line. Done means hidden tests on the outputs and final machine state pass.
## Human times
meta.expert_time_estimate_hours (and _min) from task.toml [metadata]: author estimates, not measurements. Population median 4.0 h, range 0.75 to 60 h.
## Problems
- Scores are over all 66 tasks (incl. the 5 security tasks), not the 61. 5 trials per task; 4.1 re-scored saved 4.0 trials with looser verifiers (162/11,550 trials changed).
- Scaffolds differ (Claude Code, Codex, Grok Build, mini-SWE-agent, ...); best reasoning config per model kept. Secondary source; per-row dates absent so eval_date = snapshot. Several release dates blank (GPT-6 Sol/6.1 Sol/6 Luna, GLM-5.3, Grok 4.7, Qwen3.8-Max, Gemini 3.7/3.8 Flash, Sonnet 5).
- Vendor-agnostic official leaderboard not retrievable; tbench.ai figures could differ. Tasks are continuously updated (task versions 1.1.0 to 4.2.1 in toml).
