# apex_accounting (Mercor APEX-Accounting) - source notes

- Accessed 2026-11-10. Items: HF mercor/apex-accounting-harbor (ungated, CC-BY-4.0, sha 1662b7e4, lastModified 2026-09-17); only instruction.md/mercor.json/task.toml/agent.json/grading_config
  and per-task input file NAMES fetched (raw/tasks). No images, solutions or golden answers used. `mercor/apex-accounting` (tabular source) returned HTTP 401 to anonymous API/page requests; not accessed, no terms accepted, no login.
  Scores: https://www.mercor.com/apex/apex-accounting-leaderboard/ (raw/lb.html, parsed from the embedded __NEXT_DATA__ JSON). Paper: arXiv 2607.27189 (page saved, not read in depth).
- Population: the public dev set is only 10 tasks (World 9, a law firm's Dec-2024 close), all included (n<24, no sampling). The headline leaderboard is on 100 held-out tasks (10 private worlds, 1,475 criteria);
  the HF README says 160 tasks across 10 worlds - the two Mercor sources disagree (leaderboard says 100). The 10 dev tasks are NOT the headline-scored items; they are a sample of the same task family.
- Grading method: `llm_judge`. Each rubric criterion (expert-written, binary, ~9 per task, 89 total on dev set) is judged Met/Not Met by an LM judge from the task prompt and final console answer; the judge penalises hedging.
- Description for time estimators: A month-end accounting task for a small firm, given in plain words with a handful of spreadsheets, PDFs, ledger exports and accounting-system (QuickBooks) records; the worker reconciles an account, books or checks accruals/journal entries, analyses a variance or builds a schedule, and reports specific figures; done when every expert checklist figure and judgment is right.
- Published human times: none confirmed. Task metadata has an unlabelled numeric field (custom_field c70bed5d, values 0.75-4.0 across the 10 tasks; kept in meta, possibly expert-hour estimates - UNVERIFIED) plus an author difficulty label (Moderate/Hard/Very Hard/Extreme).
- scores.csv: 49 models (2026-04-16 to 2026-11-09). `score` = Pass@1 (share of tasks where all rubric criteria are met, from 8 runs/task), 0-1. The leaderboard's canonical metric is mean criteria % passed
  (e.g. top 71.5%); pass@1 is much lower (top 23.8%, floor 0.8%), so score here is on the strict "task fully solved" scale. Mean criteria score is in notes. Passing = all criteria, so horizons fit to pass@1 will be shorter than ones fit to mean score.
- Problems: dev items are 10 of a private set (small n, one world); one model per effort setting only (highest available, `effort` in model name); eval dates not shown (access date used);
  6 release dates were missing on the Mercor page, 5 filled from vals.ai model pages, Nemotron 3.5 Bolt blank; all models released Apr-Nov 2026 (narrow window); Mercor is the benchmark author; dev results are explicitly "not comparable to leaderboard results";
  task review notes in mercor.json contain model outputs/scores and were excluded from item text.
