# Finch (FinWorkBench) - source notes

- Accessed 2026-11-09. Data: https://huggingface.co/datasets/FinWorkBench/Finch (ungated, CC-BY-3.0, HF sha 530700c2, lastModified 2026-04-17), file finch_workflows_test.jsonl.
  Paper: https://arxiv.org/abs/2512.13168 (raw/paper.pdf). Eval code: https://github.com/FinWorkBench/Finch (not used).
- Population: all 172 workflows in the single "test" split (headline pass rates are over all 172). Sample: random.Random(2026).sample(sorted(ids as strings), 24).
  Note sorted() is lexicographic on string ids ("0","1","10",...). Source xlsx/pdf/ref files were NOT downloaded; text = instruction + list of attached file names.
- Grading method: `human_expert` for the two headline human-eval rows (GPT-5.1 Pro, Claude Sonnet 4.5); all other rows are `llm_judge`
  (GPT-5-mini multimodal judge comparing input/output/reference; overestimates human pass by ~3-4 pts, 82-90% agreement).
- Description for time estimators: A messy real-world finance/accounting spreadsheet workflow (often several linked workbooks, sometimes PDFs/images) with a written
  instruction of 1-5 sub-tasks (data entry, formulas, cross-sheet retrieval, modelling, validation, formatting, charts, translation); done when the returned workbook matches an expert reference.
- Published human times per item: none. The paper reports only agent run time (GPT-5.1 Pro avg 16.8 min) and tool-call counts for 20 tasks with Claude Coworker (Opus 4.6); not human time.
  Task-type tags and # tasks per workflow are in meta (task_type) as a proxy.
- Problems:
  - Only 8 score rows, from one paper (Dec 2025); no public leaderboard found. Scores mix human-eval and LLM-judge and product agents vs single-call API harnesses.
  - Opus 4.5 has only an automated score (read from figure bar label).
  - GPT-5.1 Pro and Opus 4.5 release dates are from memory - flagged in notes.
  - Small time window (all models released Jul-Nov 2025), so little trend information. Score at n=172 has SE ~3.7 pts.
  - Annotations "should not appear in training corpora"; public full set (no private holdout noted).
