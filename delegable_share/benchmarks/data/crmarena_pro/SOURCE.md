# crmarena_pro (Salesforce CRMArena-Pro)
Accessed 2026-11-09. Dataset: HF Salesforce/CRMArenaPro (ungated, licence CC BY-NC 4.0), sha 8c055f5b (last modified 2025-07-09). Code: github.com/SalesforceAIResearch/CRMArena (CC BY-NC 4.0).
Paper: arXiv 2505.18878 (submitted 2025-05-24; TMLR 2026-02). Scores from the paper's Table 2 (read via arxiv.org/html/2505.18878). The repo `results/` folder holds only tiny stub files.

## Population and sampling
Variant: SINGLE-TURN (`tasks_b2b.json`, `tasks_b2c.json`), the paper's headline setting. Multi-turn (`*_interactive.json`) not sampled; its scores are in `notes`.
Pooled B2B + B2C, 19 task-completion task types x 100 x 2 orgs = 3800 items. The 3 confidentiality-awareness types (240 per org) are excluded, as in Table 2.
Ids `<org>:<idx>`, sorted as strings; `random.Random(2026).sample(ids, 24)` (19 B2C, 5 B2B by chance). Build script: eva_bench/scripts/build_crm.py.
Text = task type, request, supplied policy/guide text. The long "Domain details" glossary is dropped.

## Grading method: `exact_answer`
Exact match on the returned id/value for most types; F1 word overlap for knowledge QA. (Multi-turn uses a gpt-4o answer extractor.)

## One-line description for time estimators
A request handled in a company's Salesforce CRM through query and search tools; for example route a new case to the best agent, check whether a quote breaks policy, qualify a lead, or answer from knowledge articles; done when the returned record id or answer is the correct one.

## Published human times
None. About 9 minutes per query was the experts' time budget, not a measurement.

## Problems
- Only 9 models, all from Nov 2024-May 2025 (series stopped); no newer scores found, including the TMLR version if it added any.
- Score = mean of the paper's B2B and B2C "All" (each the average of 4 skill averages: workflow, policy, text, database), not an item-weighted mean; the two differ slightly. Item-weighted would need per-task numbers.
- Paper's abstract quotes about 58% for Gemini 2.5 Pro (this is B2C only).
- Release dates for Gemini 2.5 Pro and Flash are preview dates; eval date approximated by paper date.
- Task types differ hugely in difficulty (workflow tasks near 80-90% for the best model); an item sample of 24 covers 19 task types thinly.
- Public set of the same environment; the Salesforce orgs are shared and live (GUI access removed).
