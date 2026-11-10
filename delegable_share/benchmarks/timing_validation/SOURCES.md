# Sources and provenance (assembled 2026-11-09; no estimates made by the assembler)

Script: `build_items.py` (run `python3 -I build_items.py`). Seed 20261109 for both benchmarks. Raw downloads in `raw/` (git-ignored).

## SWE-bench Verified (48 items)
- Data: https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified, repo commit sha c104f840cc67f8b6eec6f759ebc8b2693d585d4a (lastModified 2025-02-18). File `data/test-00000-of-00001.parquet`, sha256 a45b1fe4e2f0c8390b2b2938ac83e92ed5979000856808f3679c07812e9e6dcd.
- Text = `problem_statement` prefixed by repo and instance_id. Hints, patches and tests excluded.
- Time = `difficulty` field in that dataset. Bucket counts in full set: <15 min 194; 15 min-1 hour 261; 1-4 hours 42; >4 hours 3.
- How produced: OpenAI's human annotation campaign for SWE-bench Verified (https://openai.com/index/introducing-swe-bench-verified/; could not be fetched directly, 403). Per secondary sources: 93 Python-experienced developers; each annotator ESTIMATED how long a developer would need to decide on and implement the fix, assuming the sample is non-problematic. METR (https://arxiv.org/abs/2503.14499, Sec 4.1) describes the wording as an "engineer who has had a few hours to familiarize themselves with the codebase" (wording from the original SWE-bench paper). Annotators saw the issue/PR/tests in OpenAI's annotation tool; I did not verify exactly what they saw. These are estimates, not measurements.
- Not verified: that the HF `difficulty` field is identical to OpenAI's separate public annotation release (I did not download that release; I believe the HF field is copied from it).
- Caveat: METR (same paper) found annotator estimates underestimate contract-baseliner times on the easiest tasks (their 4 "<15 min" tasks took 8-84 min).
- Sampling: 15 random (random.Random(seed).sample over sorted instance_ids) from each of the first three buckets; all 3 in ">4 hours". Buckets in minutes [0,15], [15,60], [60,240], [240,null]. No issue exceeded 1,500 words; none truncated (truncation rule implemented: first 1,500 words + " [truncated]").

## Terminal-Bench 2.0 (40 items)
- Repo: https://github.com/laude-institute/terminal-bench-2 , commit 2fd12b88aafdd04a52c298e3940bcb189f9766d6 (2026-04-29), cloned shallow. 89 task dirs.
- Text = `<task>/instruction.md` (not solution, not tests).
- Time = `[metadata] expert_time_estimate_min` (time_min) and `junior_time_estimate_min` (in time_note), from each task's `task.toml`. These are task authors' ESTIMATES, not measurements. category and author difficulty are also in time_note.
- Oddity: `caffe-cifar-10` has no time estimates in task.toml, excluded, leaving 88 eligible. Expert times range 5-2400 min with heavy ties (e.g. 14 tasks at 30, 13 at 60).
- Sampling: eligible tasks sorted by (expert time, name), split by rank into 4 equal groups of 22 (quartiles; ties may straddle boundaries), 10 random per group.
- Sampled expert-time range: 5 to 1440 min (the 2400 min task was not drawn).

## Optional third benchmark
Skipped (not pursued; no time spent on METR task subset).
