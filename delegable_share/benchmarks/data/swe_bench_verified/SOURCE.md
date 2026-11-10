# swe_bench_verified (SWE-bench Verified)
Accessed 2026-11-10.
- Items: HF princeton-nlp/SWE-bench_Verified, data/test-00000-of-00001.parquet (500 rows, saved in raw/). Licence: not re-checked (dataset card says MIT, from memory).
- Scores: official leaderboard data github.com/SWE-bench/swe-bench.github.io data/leaderboards.json ("Verified" tab, 180 entries, saved raw/leaderboards.json), i.e. swebench.com. Six newer rows (Opus 5, Fable 5, Opus 4.8, Opus 4.7, Sonnet 5, GPT-5.3 Codex) from BenchLM https://benchlm.ai/md/benchmarks/swe-bench-verified.md (2026-11-10, provider-reported, secondary).
## Population and sample
All 500 instances. random.Random(2026).sample(sorted instance_ids, 24). Text = "Repository: X. GitHub issue to resolve: <problem_statement>" truncated at 300 words. meta.difficulty = dataset time bucket (sample: 8 "<15 min fix", 15 "15 min - 1 hour", 1 "1-4 hours"; population 194/261/42/3 for <15m, 15m-1h, 1-4h, >4h).
## Grading method
tests: FAIL_TO_PASS tests must pass and PASS_TO_PASS tests must still pass.
## Description for time estimators
A GitHub issue (bug report or feature request) for an open-source Python library plus the full repository. The worker edits the code to fix the problem. Done means hidden unit tests for the fix pass and existing tests still pass.
## Human times
`difficulty` field: annotators' estimate of time for an engineer familiar with the codebase (OpenAI annotation of the 500 Verified items); buckets only.
## Problems
- Scores mix scaffolds (mini-SWE-agent, SWE-agent, OpenHands, many vendor agents); best entry per model kept, agent named in notes. Some entries unchecked. Leaderboard stops 2026-02-26; later models are only in the 6 aggregator rows (no scaffold or date given).
- Excluded: fine-tuned small models, multi-model or "Undisclosed" systems, tiny/older RAG baselines kept (Claude 2, GPT-3.5). Name aliases merged by hand (e.g. Claude 4 Sonnet = Claude Sonnet 4).
- Leaderboard "date" is the submission folder date, not a model release date; RAG baselines dated 2023-10 were run on Verified later. Release dates for pre-2025-07 rows are from memory (flagged); the leaderboard model_release_date field was used when present.
- Saturated (~90%+) and contaminated per BenchLM; Python-only, 12 repos.
