# sopbench (SOPBench)
Accessed 2026-11-09. Code MIT; data (data/ folder) CC BY 4.0. Repo github.com/Leezekun/SOPBench HEAD 8790ed7 (2026-09-13). Paper arXiv 2503.08669 (v1 2025-03-11, v2 2025-06-17; EMNLP 2026).
Items: `data/<domain>_tasks.json`. Scores: README results table (updated beyond the paper, with Qwen3.5 / Gemma-4 / GPT-5 rows).

## Population and sampling
All 830 tasks across 7 domains (bank 134, dmv 97, healthcare 124, hotel 195, library 66, online_market 172, university 42), which matches the per-domain denominators implied by the README percentages.
Ids `<domain>:<action>:<index>`, sorted; `random.Random(2026).sample(ids, 24)` (hotel 5, market 5, library 5, bank 3, univ 3, healthcare 2, dmv 1). Build script: eva_bench/scripts/build_sop.py.
Text: customer's first message, the SOP's numeric parameters, the SOP conditions to check (from `constraints_original`, function names made readable), should-succeed vs should-decline, and gold tool names. The natural-language SOP wording lives in generated system prompts (reference/prompts) and was not copied in.

## Grading method: `state`
Programmatic: the target action must be performed in the database if and only if all SOP constraints hold (an environment check over the final state/action log, with dependency checking of required verification calls).

## One-line description for time estimators
A customer request in a service setting (banking, DMV, healthcare, hotel, library, online market, university) with a written standard operating procedure and system tools; the worker checks the required conditions in the required order and either performs the requested action or declines it with the reason; done when the action was taken exactly when the SOP allows it and every required check was made.

## Published human times
None.

## Problems
- Prompt-based "act only if SOP allows" tasks are synthetic and templated (numbers and names are generated); about 65% (542 of 830) of tasks should end in refusal.
- Scores come from the README, one setting per model (mostly function calling, ReAct for open models), not unified scaffolds. Only the overall (830-task) figure is used; per-domain in notes.
- No eval dates in the repo; eval_date blank. Release dates from memory/web for older models; Qwen3.5 and Gemma-4 dates approximate and unverified. Gemini 2.5 release dates are preview dates.
- Several rows are small open models; saturated nowhere (best 75%).
- Public data; no private split. Output folder also holds many raw trajectory files (not downloaded).
