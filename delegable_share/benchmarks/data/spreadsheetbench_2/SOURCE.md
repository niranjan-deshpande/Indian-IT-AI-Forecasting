# SpreadsheetBench 2 - source notes

- Accessed 2026-11-09. Data: https://huggingface.co/datasets/KAKA22/SpreadsheetBench-v2 (ungated, MIT, HF sha 5a2215ed), file spreadsheetbench-v2.zip (134 MB; only the four
  dataset.json files were extracted to raw/x/, zip deleted afterwards). Code: https://github.com/RUCKBReasoning/SpreadsheetBench-2 (README only). Site: https://spreadsheetbench.github.io/.
  Paper: arXiv 2606.29955 (v2, 7 Nov 2026), raw/paper.pdf.
- Population: all 321 tasks = Debugging 100 + Financial_Model 100 + Template 97 + Visualization 24 (the "Overall" column of Table 3 pools all four).
  Native ids repeat across categories, so item ids are "<Category>:<id>" (spaces to underscores). Sample: random.Random(2026).sample(sorted(ids), 24) -> 9 Template, 7 Debugging, 4 Fin. Model, 4 Visualization.
  Input/golden xlsx files were not extracted; text = instruction + attached file name.
- Grading method: `state`. Debugging/Financial_Model/Template: programmatic cell-by-cell comparison of output vs golden workbook (task passes only if every cell matches). Visualization (24 tasks): `llm_judge`
  (GLM-4.6V VLM rubric pass rate per task; the headline pools this fractional score with the binary ones).
- Description for time estimators: A business spreadsheet workflow on a large multi-sheet workbook (avg ~12 sheets, ~590 cells to change): complete a financial model or template schedule from
  stated assumptions, audit and repair a workbook with injected errors, or build a specified chart; done when the edited workbook matches an expert golden file (charts: meets a rubric).
- Published human times per item: none found in the dataset or paper. meta has answer_position (target cell ranges) as a size proxy.
- Problems:
  - 8 models only, all one paper, one scaffold (SWE-agent); no dated leaderboard page found (site table is an image). Models released Dec 2025 - Feb 2026; eval dates not stated per model.
  - Release dates are from memory (not verified against announcements).
  - Debugging instructions are generic ("audit and fix this file"), so item text carries little information about work size; Debugging/Financial_Model golden-file targets are huge.
  - "Accuracy" is strict full-match; the paper also gives a lenient cell-level "Modification" score (e.g. Opus 4.6 77.2% overall) which is not used here.
  - Public release includes full 321 tasks (no private holdout mentioned).
