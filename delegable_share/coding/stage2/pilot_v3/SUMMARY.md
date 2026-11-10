# Stage 2 summary — pilot_v3

67 items × 3 coders (s1 = claude-sonnet (subagent), s2 = claude-sonnet (subagent), t = gpt-6.1-terra). Combined: median of numbers and ordered categories; domain by median κ.

## Spread between coders

- Median item length (p50), max/min across coders: median ratio 1.50, quartiles 1.25–1.60, 3 items above 3×.
- Stakes: all three agree on 33, within one step on 34, two steps apart on 0.
- Context: all agree 54, one step 13, two steps 0.
- Domain: all agree 51, two agree 16, three-way split 0.
- Coder tendency in p50 length (median ratio to combined): s1 ×1.00, s2 ×1.00, t ×1.00.
- Review line a + b·h (fit to the three median points): median b 0.159, quartiles 0.096–0.326; median a 1.7 min. Slope short→typical vs typical→long (medians): 0.200 vs 0.167.
- Unit flags: 9 items flagged by at least one coder; 12 items with two groups noted.

## Combined features by occupation (medians across items)

| Occupation | Items | p50 min | p90 min | review p10 | stakes (L/M/H) | context (L/M/H) | domain (sw/cu/tx) |
|---|---|---|---|---|---|---|---|
| Computer User Support Specialists | 16 | 30 | 90 | 3 | 5/9/2 | 2/11/3 | 1/10/5 |
| Customer Service Representatives | 20 | 8 | 19 | 2 | 3/13/4 | 0/19/1 | 0/17/3 |
| Software Quality Assurance Analysts and Testers | 31 | 180 | 480 | 10 | 2/27/2 | 0/20/11 | 7/11/13 |

## Widest disagreements on length (p50 ratio > 3)

- 14656a (Software Quality Assurance Analysts and Testers): one test environment built to mirror production — p50 by coder 1800;900;480 min
- 14663a (Software Quality Assurance Analysts and Testers): one tool evaluation with recommendation — p50 by coder 1800;1200;480 min
- 14658a (Software Quality Assurance Analysts and Testers): one standards-compliance review of a program with recommendations — p50 by coder 150;240;480 min

## Unit flags

- 1287b (1/3): A day's log aggregates many entries of different kinds over a whole shift, so it is a collection of many small writing tasks rather than one deliverable.
- 1288b (1/3): The item spans quick fixes and long diagnostic investigations that include escalation, so it mixes very different kinds of work.
- 1296a (1/3): Customizations range from a template tweak to a scripted macro, mixing very different kinds of work.
- 1297a (1/3): The study can combine workflow analysis, space design and cost comparison, which are very different kinds of work, and is an unusual task for support specialists.
- 15204a (1/3): One vacancy mixes screening, interviewing and deciding over days or weeks, and hiring is only loosely part of a support specialist's work.
- 18565b (1/3): Orders and account cancellations differ in kind and length (cancellations often involve retention talk), so the item mixes two types of work.
- 14644b (1/3): A curation pass covers many records of mixed kinds (merging, status updates, workarounds), so it mixes very different amounts and types of work.
- 14649a (1/3): A single standard and a full set of release-readiness criteria are very different in scope, so the item mixes light and heavy work.
- 14659a (2/3): A testing tool or framework component ranges from a small helper script to a substantial framework module, so the item mixes very different sizes of work. | Scope runs from a small helper script to a full framework component, mixing very different amounts and kinds of work.
