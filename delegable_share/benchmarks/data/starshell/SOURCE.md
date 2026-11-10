# starshell (StarShell enterprise tasks)
Accessed 2026-11-09. Licence: code Apache-2.0 (github.com/ServiceNow/StarShell, commit c54ec90, 2026-08-05); datasets Apache-2.0, not gated.

## URLs
- Paper "Terminal Agents Suffice for Enterprise Automation", arXiv 2604.00073 (TMLR 10/2026) (raw/starshell.pdf)
- HF collection ServiceNow-AI/starshell: datasets servicenow-tasks (330 rows), gitlab-tasks (192), erpnext-tasks (207), plus docs sets. Parquet files in raw/ (not executed; validation code columns not run).

## Population and sampling
Headline = overall success over all 729 tasks (330 ServiceNow = WorkArena L1 goals, 192 GitLab, 207 ERPNext). Ids `<domain>:<task_name>:<task_seed>` sorted; random.Random(2026).sample(ids, 24) gave 14 ServiceNow, 4 GitLab, 6 ERPNext. Text is the dataset's `goal` field verbatim (some GitLab goals contain unresolved {{placeholders}}). The dataset README says 155 GitLab samples but the parquet and paper have 192.

## Grading method
`state`: per-task Python validators query the live platform (ServiceNow REST API, GitLab API, ERPNext SQL) to check the resulting records.

## Description for time estimators
One record-keeping instruction in a business system (ServiceNow incidents, catalog orders, list views, dashboards; GitLab groups, projects, issues, invitations; ERPNext sales or purchase orders, invoices, users, projects, sometimes chained); done when the records in the system match the goal.

## Human times
None published.

## Scores
Paper Tables 2, 3, 5, 6: four frontier models and two open-weight models, each with several scaffolds (web, terminal, tool-use, API-call, hybrid). scores.csv keeps the best overall scaffold per model and lists others in notes. No per-task results are published (only a local viewer). Single date window (2026-03 to 2026-05): no trend, only 6 models.

## Problems
- Narrow date range and a ceiling near 80%.
- Release dates from web search (not provider pages); Qwen3.6-27B date approximate.
- ServiceNow subset duplicates workarena_l1 goals; do not treat as independent.
- Some tasks are infeasible for tool-use scaffolds, which affects the per-scaffold comparison but not the best-scaffold score.
