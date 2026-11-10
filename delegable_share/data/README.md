# Task data for the delegable-share measure

Task lists for the pilot and BPO occupations (SPEC.md Section 5), with O\*NET ratings and Eloundou et al. exposure labels attached to each task statement.

## Files

| File | What it is |
|---|---|
| `pilot_tasks.csv` | 59 task statements: Computer User Support Specialists (15-1232.00), Customer Service Representatives (43-4051.00), Software QA Analysts and Testers (15-1253.00). |
| `bpo_tasks.csv` | 269 task statements for the 13 BPO occupations. Includes the three pilot occupations; `in_pilot` marks them. |
| `occupation_summary.csv` | One row per occupation per set: code check, task counts, ratings coverage, suppression flags, Eloundou match counts, notes. |
| `eloundou_match_stats.json` | Match statistics over the whole O\*NET 31.0 task file, for context. |
| `raw/` | Downloads (git-ignored). `raw/manifest.json` has the URL, download time, size and SHA-256 of every file. |

Rebuild everything (from the repo root):

```
python3 -I delegable_share/scripts/pull_tasks.py                 # download if missing, then build
python3 -I delegable_share/scripts/pull_tasks.py --force         # re-download, then build
python3 -I delegable_share/scripts/pull_tasks.py --skip-download # build from raw/ only
```

The downloads are untrusted data. The script only writes bytes, unzips with a path check, and parses tables. It lives outside `raw/` and is run with `-I` so nothing in `raw/` can be imported.

## Sources

### O\*NET 31.0 Database

- Version: **O\*NET 31.0**, August 2026 release, the current production database on 2026-11-09.
- URL: <https://www.onetcenter.org/dl_files/database/db_31_0_text.zip> (tab-delimited text release; listed at <https://www.onetcenter.org/database.html>). Server `Last-Modified: 2026-08-30`.
- Downloaded: 2026-11-10 02:37 UTC (2026-11-09 local). SHA-256 `6883548adf5fde64cf6f801b35d15519c9225f2732c3cab0e281c652d16b23a9`.
- Files used: `Occupation Data.txt`, `Task Statements.txt`, `Task Ratings.txt`, `Task Categories.txt`, `Tasks to DWAs.txt`, `GWAs to IWAs to DWAs.txt` (for DWA titles). The whole release is extracted in `raw/onet/db_31_0_text/`.
- Documentation: data dictionary at <https://www.onetcenter.org/dictionary/31.0/excel/> (Task Statements, Task Ratings, Appendix 2 for rating statistics).
- License: Creative Commons Attribution 4.0 International (CC BY 4.0), <https://www.onetcenter.org/license_db.html>. Required attribution. We derive new fields from the data, so use the "modified" form:

  > This page includes information from the [O\*NET 31.0 Database](https://www.onetcenter.org/database.html) by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license. O\*NET® is a trademark of USDOL/ETA. [Our names] have modified all or some of this information. USDOL/ETA has not approved, endorsed, or tested these modifications.

  The license page also asks that the version number be named ("O\*NET 31.0 Database", not "O\*NET Database"), that changes be indicated (the derived columns are listed below), and that "O\*NET" be used as an adjective ("O\*NET data"), never as a noun, plural or possessive.

### Eloundou, Manning, Mishkin and Rock, "GPTs are GPTs"

- Repo: <https://github.com/openai/GPTs-are-GPTs>, pinned to commit `0471612fef3cc22b74fb884d27bff9dbd3770582` (2025-10-04). Raw files come from `https://raw.githubusercontent.com/openai/GPTs-are-GPTs/<commit>/data/...`.
- Files: `full_labelset.tsv` (the task-level label set, 19,265 tasks; the main input), `automation_gpt4_human_labels.tsv`, `full_onet_data.tsv`, `occ_level.csv`, plus `README.md` and `LICENSE`.
- Paper: arXiv 2303.10130v5, <https://arxiv.org/abs/2303.10130> (PDF saved in `raw/eloundou/`). Published as Eloundou, T., Manning, S., Mishkin, P., & Rock, D. (2024), "GPTs are GPTs: Labor market impact potential of LLMs," *Science* 384(6702), 1306–1308.
- License: MIT, Copyright (c) 2024 OpenAI. Keep the copyright and permission notice with any copy of the data.
- **O\*NET version of their tasks: 27.2** (paper Section 3.1: "We use the O\*NET 27.2 database", 1,016 occupations, 19,265 tasks, 2,087 DWAs). Their notebook links 27.1 Task Statements and 27.2 Task Ratings; the task lists are the same for our purposes.

What the label columns are (from the repo README, the paper, and checks in the build script):

| Column in `full_labelset.tsv` | Meaning |
|---|---|
| `human_exposure_agg` | Human label, E0/E1/E2. Annotators labelled every DWA and a subset of tasks; DWA labels were aggregated to the task (paper footnote 5). `human_labels` is an exact duplicate (asserted in the script). |
| `gpt4_exposure` | GPT-4 label, rubric 1 (the paper's main GPT-4 measure). |
| `gpt4_exposure_alt_rubric` | GPT-4 label, rubric 2 (paper Table 2). |
| `alpha`, `beta`, `gamma` | **GPT-4 rubric 1 only**: E1, E1 + 0.5·E2, E1 + E2 as 0/0.5/1 scores per task (asserted). The paper (v5) calls the third one ζ. |
| `gpt4_automation`, `automation` | GPT-4 automation label T0–T4 and its score (0, .25, .5, .75, 1). Not described in paper v5. |
| `gpt_3_relevant` | Boolean; not documented in the paper or README. Carried for completeness. |

E0 = no exposure; E1 = direct exposure (an LLM via ChatGPT/Playground cuts task time by at least half at equal quality); E2 = exposure via additional LLM-powered software (including image tools, their E3, which they merge into E2). The paper's headline measure is β = E1 + 0.5·E2.

## Column definitions (`pilot_tasks.csv`, `bpo_tasks.csv`)

One row per O\*NET 31.0 task statement. Sorted by the occupation order in the spec, then `task_id`. Blank means missing.

**Occupation and task (O\*NET, verbatim)**

| Column | Definition |
|---|---|
| `in_pilot` | (`bpo_tasks.csv` only) True for the three pilot occupations. |
| `onetsoc_code`, `occupation_title`, `occupation_description` | From Occupation Data. |
| `task_id`, `task_statement` | From Task Statements. |
| `task_type` | `Core` (relevance ≥ 67% and mean importance ≥ 3.0) or `Supplemental` (relevance ≥ 67% but importance < 3.0, or relevance < 67%). Blank for tasks without ratings. |
| `task_incumbents_responding`, `task_date`, `task_domain_source` | Task Statements metadata. `Analyst` tasks dated 11/2020 were added at the 2019 O\*NET-SOC taxonomy transition and have no ratings. |

**Ratings (O\*NET Task Ratings)**

| Column | Definition |
|---|---|
| `has_ratings` | True if the task has an IM rating. |
| `im`, `im_n`, `im_se`, `im_ci_lower`, `im_ci_upper`, `im_suppress` | Importance (scale 1–5): mean, sample size, standard error, 95% CI, Recommend Suppress (Y/N). |
| `rt`, `rt_n`, `rt_se`, `rt_ci_lower`, `rt_ci_upper`, `rt_suppress` | Relevance (0–100): percent of respondents who say they perform the task, with the same statistics. |
| `ft_pct_1` … `ft_pct_7` | Frequency: percent of respondents in each category: 1 yearly or less, 2 more than yearly, 3 more than monthly, 4 more than weekly, 5 daily, 6 several times daily, 7 hourly or more. |
| `ft_n` | Sample size for the frequency item. |
| `ft_suppress_n` | Number of the 7 frequency categories flagged Recommend Suppress = Y. |
| `ratings_date`, `ratings_domain_source` | Date and source of the ratings (`Incumbent` survey or `Occupational Expert`). |

Recommend Suppress = Y means low precision: N < 10, or zero variance with N < 15, or relative standard error > 0.5 (data dictionary, Appendix 2). **Ratings from Occupational Experts carry no standard errors and no suppress flag**: the `*_se`, `*_ci_*` and `*_suppress` columns are blank for those occupations (15-1253, 15-1254, 15-1244), not "N".

**Derived (our additions; these are the "modifications" for the license notice)**

| Column | Definition |
|---|---|
| `freq_mean_cat` | Mean frequency category, Σ p_k·k for k = 1…7, where p_k = `ft_pct_k` normalised to sum to 1 (the raw sums are 100 ± 0.02). Use this as the default frequency measure: it needs no assumptions about the open-ended end categories. |
| `freq_per_year` | Expected occurrences per year, Σ p_k·r_k, with r_k the geometric midpoint of each band at 260 working days and 8 hours a day: r = 1, 3.5, 25, 116, 260, 1040, 2080. Categories 1 and 7 are open-ended, so r_1 = 1 is an upper bound and r_7 = 8/day a lower bound. Sensitive to those choices; treat as indicative. |
| `freq_pct_daily_plus` | Percent of respondents reporting daily or more often (categories 5–7). |
| `dwa_ids`, `dwa_titles` | Linked Detailed Work Activities from Tasks to DWAs ("; " and " \| " separated). |

**Eloundou match and labels**

| Column | Definition |
|---|---|
| `eloundou_match` | `task_id`: same O\*NET Task ID in `full_labelset.tsv`. `text`: no ID match but the statement is identical after trimming and collapsing whitespace (same occupation preferred). `none`: no match. |
| `el_task_id`, `el_onetsoc_code`, `el_task_type` | The matched Eloundou row. `el_task_type` is the Core/Supplemental type in O\*NET 27.2, which can differ from `task_type` in 31.0. |
| `el_text_identical`, `el_text_similarity` | Whether the matched statement text is identical to the 31.0 statement, and a difflib similarity ratio (0–1). |
| `el_task_text` | Eloundou's statement, filled only when it differs from the 31.0 text. |
| `el_human_exposure`, `el_gpt4_exposure`, `el_gpt4_exposure_alt_rubric` | E0/E1/E2 labels (human; GPT-4 rubric 1; GPT-4 rubric 2). |
| `el_human_alpha`, `el_human_beta`, `el_human_gamma` | Computed by us from `el_human_exposure`: α = E1, β = E1 + 0.5·E2, γ (ζ) = E1 + E2, scored 0/0.5/1. |
| `el_gpt4_alpha`, `el_gpt4_beta`, `el_gpt4_gamma` | Eloundou's `alpha`/`beta`/`gamma` columns (GPT-4 rubric 1). |
| `el_gpt3_relevant`, `el_gpt4_automation`, `el_gpt4_automation_score` | As in the source; see above. |
| `el_human_automation` | Human automation label. Only about 100 of 19,265 tasks have one; blank for every task in our sets. |
| `el_nearest_task_id`, `el_nearest_similarity`, `el_nearest_task_text` | For `none` rows only: the most similar Eloundou statement in the same occupation. Empty in both sets, since everything matched. |

**The clean exposure fields are `el_human_beta` and `el_gpt4_beta`** (E1 + 0.5·E2, the paper's main measure). The paper reports human labels as its primary results and GPT-4 rubric 1 as its main model measure.

## Match statistics

**Pilot and BPO sets: 100% matched by Task ID** (59/59 and 269/269). No text fallback was needed. In 3 BPO tasks the matched text differs trivially, by a singular/plural (`databases` vs `database` in 15-1242 tasks 1306 and 1311; `systems` vs `system` in 15-1211 task 3472). All pilot matches are text-identical.

Whole O\*NET 31.0 task file (`eloundou_match_stats.json`): of 18,838 statements, 18,735 match by Task ID (18,677 of them with identical text), 3 match by exact text, and 100 do not match. All 100 unmatched statements are new tasks written in O\*NET updates after 27.2 (dated 08/2023 to 08/2026). Their nearest Eloundou statement in the same occupation has a median similarity of only 0.44, so they are new tasks, not rewordings. In the other direction, 530 of Eloundou's 19,265 tasks are no longer in 31.0.

What has drifted for our occupations is not the matching but the context around it:

- **Tasks dropped since 27.2.** 15 Eloundou tasks for our codes are gone from 31.0: 2 in 43-4051, 2 in 15-1252, 2 in 43-3031, 4 in 43-3021, 2 in 43-9041, 1 in 29-2072. Eloundou's occupation averages for those codes include them; ours won't.
- **Core/Supplemental changed.** 64 of 269 BPO tasks have a different type in 31.0 than in 27.2, mostly where O\*NET re-surveyed the occupation after 27.2. Software Developers (17 of 17) and Medical Records Specialists (16 of 16) had no ratings or type in 27.2 (both are 2019-taxonomy codes) and are now rated. Others: Billing and Posting Clerks (12), Database Administrators (8), Computer Systems Analysts (6), Network Administrators (3), Computer User Support Specialists (2). Eloundou's occupation scores use 27.2 types; ours use 31.0 ratings.
- **Ratings updated since 27.2**: 15-1252 (08/2025), 15-1244, 43-3021, 29-2072 (08/2026), 15-1232, 15-1242, 15-1211 (08/2023). The labels apply to statement text, so they are unaffected.

## Pilot occupations

| Occupation | Statements | Core | Supplemental | No type | With IM | Ratings |
|---|---|---|---|---|---|---|
| 15-1232.00 Computer User Support Specialists | 16 | 13 | 3 | 0 | 16 | Incumbent, 08/2023 |
| 43-4051.00 Customer Service Representatives | 13 | 7 | 6 | 0 | 13 | Incumbent, 08/2022 |
| 15-1253.00 Software QA Analysts and Testers | 30 | 27 | 0 | 3 | 27 | Occupational Expert, 08/2022 |

The 3 unrated QA tasks (21680–21682) are `Analyst` additions from the 11/2020 taxonomy transition. One of them, "Recommend purchase of equipment to control dust, temperature, or humidity…", looks inherited from an older occupation. Decide whether to keep them; they have Eloundou labels but no weight. Suppression: no IM flags; one RT flag (43-4051 task 2586); FT categories flagged on 1 task in 15-1232 and 3 in 43-4051.

## BPO code check

All 13 codes exist in O\*NET 31.0 with the same `.00` code and title, and all have task statements and ratings. No code has changed. Points to note:

- **Tasks without ratings**: 15-1253 (3), 15-1254 (2), 43-9041 (4), all 11/2020 analyst additions without Core/Supplemental type. 260 of 269 BPO tasks have IM.
- **Expert-rated occupations** (no SE or suppress flags): 15-1253, 15-1254 (ratings from 07/2017), 15-1244.
- **Old data**: 15-1254 ratings date from 07/2017, 43-3031 from 07/2017, 43-9021 from 08/2018.
- **Sibling code**: 15-1211 has a detailed occupation 15-1211.01 (Health Informatics Specialists) that is not in the set. We use only the `.00` code, as specified.
- Suppression: no IM flags in any BPO occupation; RT flags on 1 task each in 43-4051 and 15-1252; FT flags are most common in 43-3021 (7 tasks).

Per-occupation detail is in `occupation_summary.csv`.
