# dba_bench (DBA-Bench)
Accessed 2026-11-10.
- Items: github.com/TanJI-C/DBA-Bench @ main (Apache-2.0 per README); docs/catalogs/postgresql-scenarios.catalog.md (case list) and docs/scenarios/postgresql/*/*.contract.md (alerts). Paper arXiv:2607.22165 (v1 2026-07-24, v2 2026-10-10), html at arxiv.org/html/2607.22165 (first 100k chars read).
- Scores: paper Table 2, Safe Pass by Easy/Hard on PostgreSQL.
## Population and sample
- Population = the 107 formal PostgreSQL ScenarioCases (51 scenarios), matching our catalog text (PostgreSQL). Excluded: 124 TiDB cases (catalog format partial, different system), 3 "basic" demo scenarios and 10 persistent episodes. Item id = <scenario_id>:<case_id>.
- Sample: random.Random(2026).sample(sorted 107 ids, 24). Text = fixed framing sentence plus the case's registered alert (exact agent-visible text from the contract); scenario titles were left out because they name the root cause.
## Grading method
state: system-verified outcome check (business-query result snapshots and live DB state) plus safety rules (no unsafe/protected-object changes); diagnosis is scored separately by an LLM but is NOT part of the headline.
## Description for time estimators
A live PostgreSQL database under application load plus a symptom alert (for example checkout writes timing out). The worker diagnoses the cause with metrics, SQL, logs and admin tools, then fixes it without unsafe actions. Done means the business check passes and no safety constraint was broken.
## Human times
None reported (paper: no completion times for the human DBA reference). Human DBA Safe Pass 99/107 on PG (92.5%).
## Problems
- Headline = Safe Pass (paper's primary endpoint), computed by us as (57*easy% + 50*hard%)/107 from Table 2 percentages (rounded to 0.1, so +-0.1pt). Opus 4.8 and GPT-5.5 ReAct 26.2/22.4 match the text, so the weights are right.
- Only 6 models (GPT-5.5 row is the best scaffold, DBAIOps; ReAct 22.4). Single run, pass@1; all within 2026-04 to 2026-05 releases (narrow date range, low scores 2-27%). Eval date = paper v2 date; run dates unknown. Releases for DeepSeek V4 Pro, GLM-4.7-Flash, Qwen3-Coder-Next not found.
- Case attribute yaml in the repo covers only 50 cases (provisional); the catalog was used instead. Dataset is public in full; labels are Easy/Hard from the authors' calibration.
