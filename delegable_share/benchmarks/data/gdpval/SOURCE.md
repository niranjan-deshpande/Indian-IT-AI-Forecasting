# gdpval (OpenAI GDPval), accessed 2026-11-09
URLs: https://huggingface.co/datasets/openai/gdpval (parquet data/train-00000-of-00001.parquet, ungated, HF sha 11e7900c, lastModified 2026-02-10);
paper arXiv 2510.04374; scores via benchmarklist.com/benchmarks/openai_gdpval, digitalapplied.com GPT-5.2 guide, techmeme. openai.com and evals.openai.com returned 403, so launch posts were NOT read directly.
Licence: HF card lists none in metadata that I saw; check card before redistribution. Dataset carries a canary string; keep out of training data.
Population: all 220 public gold tasks (44 occupations, 9 sectors). The headline wins-or-ties score is computed on this gold subset (the full private set is 1,320 tasks).
Sample: random.Random(2026).sample(sorted task_ids, 24) over the 220 ids (pooled across occupations). Prompt truncated to 230 words if longer; reference files listed by name and type; rubrics and deliverable contents excluded.
Grading method: human_expert (blinded pairwise comparison of model deliverable vs an industry professional's deliverable by occupational experts; win/tie/loss).
Benchmark description for time estimators: A realistic work request written by an experienced professional in one of 44 occupations, with reference files attached; the deliverable is a document, spreadsheet, slide deck, or similar file. Done means an expert reviewer judges the deliverable at least as good as a professional's.
Human times: the HF dataset ships NO time or cost field (columns: task_id, sector, occupation, prompt, reference files, deliverable files, rubric). The paper reports expert completion time per task (about 30 min to 100+ h range; median approx 5 h per the catalog) but not per-task in the public data. Paper Fig 13 (win rate by task length) could be digitised.
Problems:
- Scores are mostly from secondary sources (aggregator and blogs); primary launch posts were inaccessible. Treat later-model numbers as needing verification.
- Metric drift: original paper used wins-or-ties by GPT-5-era graders; later numbers come from OpenAI leaderboard/launch tables, probably with a newer automated or updated grading setup, and some are reported on different effort settings. GPT-5 has 38.8% and 40.6% in different sources.
- Opus 4.5 (59.6) and Opus 4.6 (78.0) come from single secondary sources; Gemini 3 Pro 53.5 likewise.
- Release dates for post-2025 models come from secondary sources, not provider posts.
- Older model scores (o3, o4-mini, GPT-4o, Gemini 2.5 Pro, Grok 4) wins-or-ties not found; win-only values are in scores_wins_only_extra.csv. Gemini 2.5 Pro and Grok 4 have no numbers found.
- Artificial Analysis GDPval-AA (Elo, different task set/harness) is a different metric and not included.
- Saturation: top models above 80%, so horizon fits near the top are poorly determined.
