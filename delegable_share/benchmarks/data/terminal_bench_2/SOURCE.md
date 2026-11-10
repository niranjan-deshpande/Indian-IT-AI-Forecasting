# terminal_bench_2 (Terminal-Bench 2.0)
Accessed 2026-11-09/10.
- Tasks: reused earlier clone, benchmarks/timing_validation/raw/tb/repo (laude-institute/terminal-bench-2, commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6, 2026-04-29; 89 task dirs). Licence Apache-2.0 per HF dataset card (repo licence not re-checked).
- Scores: HF harborframework/terminal-bench-2-leaderboard (apache-2.0), submissions/terminal-bench/2.0/*/<job>/result.json. Raw saved in raw/tb2_leaderboard_raw.json (75 submissions, 245 job result files). Also VentureBeat launch article for two 2025-11 rows (secondary). tbench.ai pages are JS-rendered; not usable.
## Population and sample
- All 89 tasks, minus 10 excluded by caller instruction (safety-filter scope): the 6 named (crack-7z-hash, qemu-alpine-ssh, filter-js-from-html, password-recovery, fix-code-vulnerability, feal-differential-cryptanalysis) plus every category=security task (also break-filter-js-from-html, openssl-selfsigned-cert, sanitize-git-repo, vulnerable-secret). Population = 79.
- Sample: random.Random(2026).sample(sorted 79 task names, 24). Text = instruction.md (truncated at 300 words, one task). caffe-cifar-10 is in the population (no time estimate in toml, not sampled).
## Grading method
tests: hidden pytest verifier inspects the final container state.
## Description for time estimators
A Linux machine plus a written instruction; the worker does it at the command line (build, configure, debug, analyse data, small research/programming puzzles). Done means hidden tests on the final machine state pass.
## Human times
meta.expert_time_estimate_min and junior_time_estimate_min from task.toml [metadata]: task authors' estimates (not measurements). Range 5 to 2400 min expert, many ties.
## Problems
- Headline scores in scores.csv are over ALL 89 tasks (pooled trials, ~5 per task). Our sample population excludes 10 tasks; the 79-task score per row is in notes (differs by about 0 to 3 points). Use that column for fits if the population should match.
- Scaffolds differ widely (Terminus 2, Codex, Droid, many custom harnesses); best scaffold per model kept. Scores can reflect harness work, not just the model.
- Multi-model, fine-tune and partial rows skipped (JJAgent, Polaris, OB-1, Junie, AfterQuery, TermiGen; 0error-Ledger had 241 trials; Crux and WozCode result files unparseable).
- Leaderboard is mostly 2026; only 2 launch-era rows (VentureBeat, not recomputed). Submissions closed May 2026 (integrity update). Several release dates are from memory (marked in notes).
- Leaderboard integrity concerns exist (see tbench.ai integrity blog); top scores near 0.9 are approaching saturation.
