# Stage 2 summary — comp_v1

255 items × 3 coders (s1 = claude-sonnet (subagent), s2 = claude-sonnet (subagent), t = gpt-6.1-terra). Combined: median of numbers and ordered categories; domain by median κ.

## Spread between coders

- Median item length (p50), max/min across coders: median ratio 1.50, quartiles 1.33–2.00, 6 items above 3×.
- Stakes: all three agree on 104, within one step on 142, two steps apart on 9.
- Context: all agree 152, one step 101, two steps 2.
- Domain: all agree 202, two agree 53, three-way split 0.
- Coder tendency in p50 length (median ratio to combined): s1 ×1.00, s2 ×1.00, t ×1.00.
- Review line a + b·h (fit to the three median points): median b 0.177, quartiles 0.115–0.296; median a 1.1 min. Slope short→typical vs typical→long (medians): 0.200 vs 0.167.
- Unit flags: 16 items flagged by at least one coder; 16 items with two groups noted.

## Combined features by occupation (medians across items)

| Occupation | Items | p50 min | p90 min | review p10 | stakes (L/M/H) | context (L/M/H) | domain (sw/cu/tx) |
|---|---|---|---|---|---|---|---|
| Interpreters and Translators | 14 | 75 | 270 | 8 | 2/12/0 | 8/6/0 | 0/0/14 |
| Proofreaders and Copy Markers | 12 | 20 | 82.5 | 2.5 | 9/3/0 | 5/7/0 | 0/5/7 |
| Technical Writers | 11 | 75 | 300 | 5 | 6/5/0 | 0/11/0 | 0/5/6 |
| Paralegals and Legal Assistants | 12 | 120 | 420 | 7.5 | 1/3/8 | 3/8/1 | 0/6/6 |
| Tax Preparers | 21 | 25 | 75 | 5 | 5/10/6 | 17/4/0 | 0/12/9 |
| Electricians | 8 | 30 | 105 | 3 | 2/4/2 | 4/3/1 | 0/5/3 |
| Registered Nurses | 25 | 20 | 60 | 3 | 2/11/12 | 0/21/4 | 1/14/10 |
| Childcare Workers | 11 | 15 | 30 | 1 | 5/6/0 | 1/10/0 | 0/3/8 |
| Janitors and Cleaners, Except Maids and Housekeeping Cleaners | 2 | 7.5 | 22.5 | 1 | 1/1/0 | 0/2/0 | 0/1/1 |
| Heavy and Tractor-Trailer Truck Drivers | 9 | 8 | 20 | 1 | 2/5/2 | 4/5/0 | 0/6/3 |
| Accountants and Auditors | 32 | 240 | 930 | 15 | 0/11/21 | 2/16/14 | 0/22/10 |
| Lawyers | 28 | 240 | 810 | 15 | 0/4/24 | 7/15/6 | 0/7/21 |
| Credit Analysts | 12 | 57.5 | 180 | 4.5 | 0/8/4 | 0/12/0 | 0/11/1 |
| Secondary School Teachers, Except Special and Career/Technical Education | 20 | 47.5 | 150 | 3 | 13/7/0 | 2/17/1 | 0/4/16 |
| Sales Representatives, Wholesale and Manufacturing, Except Technical and Scientific Products | 25 | 25 | 60 | 2 | 9/14/2 | 1/23/1 | 0/19/6 |
| Management Analysts | 13 | 480 | 1800 | 15 | 2/11/0 | 0/10/3 | 0/3/10 |

## Widest disagreements on length (p50 ratio > 3)

- 9339b (Interpreters and Translators): one technical document or section localized — p50 by coder 480;150;120 min
- 3773b (Lawyers): one written client advice response — p50 by coder 90;180;300 min
- 21527a (Accountants and Auditors): one advice memo — p50 by coder 150;180;480 min
- 3793d (Lawyers): one enforcement procedure or procedure set — p50 by coder 900;300;960 min
- 1861c (Registered Nurses): one unit operating or long-range plan — p50 by coder 480;1500;720 min
- 21525b (Accountants and Auditors): one taxpayer audit case — p50 by coder 480;1500;900 min

## Unit flags

- 9336a (1/3): The item starts with a query about the original and ends when the answer is applied, so it covers a single question not the whole translation check.
- 18496b (1/3): The item mixes reviewing a title search with preparing closing items, which are different kinds of work.
- 1850b (2/3): A health program plan and a set of education materials are very different in size and kind of work. | A health improvement program plan and a set of education materials can involve substantially different scopes of program design and content production.
- 1859a (1/3): Recommending a treatment and prescribing a drug are very different kinds of work, and a nurse can normally only recommend.
- 1860a (1/3): A single case review and a periodic surveillance report are very different in size and content.
- 1865a (1/3): The item ends at plan agreed, which mixes meetings with community groups and the writing of the plan.
- 18757b (1/3): The item combines asynchronous written updates with live callbacks while defining all cases as discrete work ending when a message is sent.
- 10637b (1/3): The work item includes pre-trip reports even though the specified part is post-trip reporting and its start is at the end of driving or after inspection.
- 21514a (1/3): A set of financial statements covers work from a simple monthly pack to a full audited annual set, which is very different.
- 21534a (1/3): A financial position review ranges from a small client's balance sheet check to a large entity analysis, which mixes very different scopes.
- 3790c (1/3): The item includes closing a matter but specifies a new matter as its start, which does not fit the closing workflow.
- 3791a (2/3): A fiduciary transaction covers very different work such as paying a bill, selling property or distributing an estate. | A fiduciary transaction covers very different work, from paying a bill to selling property, so one item mixes unlike kinds of work.
- 3793a (2/3): A program proposal and a single design component are very different in size and kind of work. | A program proposal or design component covers very different kinds and sizes of work.
- 6662b (2/3): A proposal, an evaluation and a revision are different kinds of work with very different scale. | A program proposal, an evaluation and a revision are very different in size and kind of work.
- 7279a (1/3): A records management program mixes policy writing, retention schedules, systems and training, which are very different kinds of work.
- 7279b (2/3): A unit rollout mixes training sessions, meetings, physical filing work and system setup over weeks, which are very different kinds of work. | Rolling out a program in a unit mixes training, filing set-up, labelling, process change and compliance checking over weeks, so it is a project rather than one deliverable.
