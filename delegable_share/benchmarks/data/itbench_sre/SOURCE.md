# itbench_sre (ITBench SRE, Artificial Analysis release)
Accessed 2026-11-09/10.
- Items: HF ArtificialAnalysis/ITBench-AA (not gated, CC-BY-4.0), repo sha 76df38a82288f75ba9e41dc8c515033332497473 (modified 2026-05-27), sre/data.jsonl (40 public scenarios, saved raw/data.jsonl). Upstream: github.com/itbench-hub/ITBench (original ITBench paper arXiv 2502.05352).
- Scores: benchmarklist.com/benchmarks/itbench_aa (third-party copy of the Artificial Analysis leaderboard, sampled 2026-06-10). artificialanalysis.ai page and HF blog URL returned 404 to fetch, so not checked against the official page.
## Population and sample
- 40 public scenarios (AA's leaderboard is computed on its 59 scenarios; the other 19 are private and not available). Sample random.Random(2026).sample(sorted 40 scenario ids, 24).
- text is synthesised: environment, firing alerts (from ground_truth_yaml alerts) and the task. Ground truth fault, root cause and remediation are NOT in text. The agent in the benchmark also sees events, logs, traces and topology, which are not available here. meta has counts of alerts, root-cause entities and propagation edges.
## Grading method
state/exact_answer hybrid: programmatic comparison of named root-cause entities to ground-truth entities (pass = all true entities named, no wrong ones). Closest label: exact_answer.
## Description for time estimators
A snapshot of a failing Kubernetes application: alerts, events, logs, traces, metrics and service topology. The worker investigates with command-line tools and reports which components caused the incident. Correct means every true root-cause component is named, with no wrong ones.
## Human times
None shipped. Original ITBench paper has no per-item times. Catalog estimate 15 min to 2 h.
## Problems
- Score used is the "Pass Rate" column; AA's headline is avg precision at full recall (in notes). Pass rate is over repeated samples on 59 scenarios (public+private), so the 40-item sample is only a subset of the scored population.
- Single date (2026-06-10) for all rows: eval_date is the sample date, not a trend; use release_date for trend. Many release dates approximate or blank (MiMo-V2.5-Pro, Gemma 4, Grok 4.3, Qwen3.5 small); several from secondary or memory.
- Llama 3.3 70B row looks inconsistent on the aggregator (precision 60% vs pass 0.581%).
- Third-party copy; some reasoning-effort settings are baked into model names. No pre-2026 models except Haiku 4.5 and Llama 3.3. The original ITBench paper reports ~13.8% (GPT-4o) on a different harness and scenario set, not included.
