# OSWorld-Verified - source notes

- Accessed 2026-11-09. Tasks: https://github.com/xlang-ai/OSWorld evaluation_examples/test_nogdrive.json + examples/<domain>/<id>.json (main branch, Apache-2.0). Task json only for the 24 sampled ids (raw/tasks/).
  Leaderboard: https://os-world.github.io/ static/data/osworld_verified_results.xlsx (raw/, also self_reported_results.xlsx, not used). Human steps: https://github.com/WukLab/osworld-human (raw/human/; arXiv 2506.16042; no licence file checked).
- Population: test_nogdrive.json = 360 tasks on main today (leaderboard rows report ~361, 356-369 completed, because of infra failures and the 8 Google-Drive tasks excluded; headline "369" includes them).
  test_all.json has 368. Sample: random.Random(2026).sample(sorted(ids), 24) over the 360 no-gdrive ids. Includes infeasible tasks (flagged in meta); ~10-15% of tasks are infeasible.
- Grading method: `state`. Per-task execution-based evaluator scripts check final app/file/OS state; 1/0 (a few tasks give fractional scores).
- Description for time estimators: One desktop task on an Ubuntu machine, stated in a sentence or two (e.g. edit a spreadsheet, change an app setting, export a file, multi-app workflow); done when the final file or
  application state matches what the instruction asks.
- Published human times per item: none (OSWorld paper has only aggregate timing). OSWorld-Human gives per-task human reference action sequences: meta.human_steps_single_action and human_steps_grouped_action
  (manually annotated GUI actions; sampled items 1-255 single steps). Step counts are a proxy for time, not times. Note: osworld-human instructions are the pre-Verified wording; text uses the current Verified wording.
- Scores: scores.csv has the best row per distinct system (66 systems, leaderboard dates 2025-07-28 to 2026-08-01). Rows are models (general/specialized) AND agent frameworks around a base model
  (notes say which; release_date for frameworks = base model's). Best-of-max-steps selection (15/50/100/150 steps; N-rollout bBoN rows flagged) gives a small upward bias. Fraction = leaderboard success rate/100.
- Problems:
  - Mixed harnesses/scaffolds, step budgets and coding-action use; several frameworks' scores far exceed the plain-model scaffold. A same-scaffold model series is only the "General model" rows.
  - Release dates: from memory for most older models (flagged "verify"); Opus 5, Fable 5, Kimi K2.6 from web press coverage; blank for Seed-1.8, Qwen 3.7 Plus, MiniMax M3, Muse Spark 1.1, EvoCUA, Coasty, and small open GUI models.
  - Benchmark is near saturation at the top (85-90%); leaderboard is partly self-submitted though "verified" by the OSWorld team.
  - Leaderboard denominator differs from the sampled 360 set slightly; task wording was revised in Verified, and the public set is all of the benchmark (no private split).
