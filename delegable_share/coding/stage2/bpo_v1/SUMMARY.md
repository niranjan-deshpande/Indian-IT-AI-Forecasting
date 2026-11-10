# Stage 2 summary — bpo_v1

230 items × 3 coders (s1 = claude-sonnet (subagent), s2 = claude-sonnet (subagent), t = gpt-6.1-terra). Combined: median of numbers and ordered categories; domain by median κ.

## Spread between coders

- Median item length (p50), max/min across coders: median ratio 1.50, quartiles 1.32–2.00, 12 items above 3×.
- Stakes: all three agree on 88, within one step on 135, two steps apart on 7.
- Context: all agree 137, one step 93, two steps 0.
- Domain: all agree 186, two agree 43, three-way split 1.
- Coder tendency in p50 length (median ratio to combined): s1 ×1.00, s2 ×1.00, t ×1.00.
- Review line a + b·h (fit to the three median points): median b 0.192, quartiles 0.114–0.272; median a 1.6 min. Slope short→typical vs typical→long (medians): 0.233 vs 0.189.
- Unit flags: 5 items flagged by at least one coder; 40 items with two groups noted.

## Combined features by occupation (medians across items)

| Occupation | Items | p50 min | p90 min | review p10 | stakes (L/M/H) | context (L/M/H) | domain (sw/cu/tx) |
|---|---|---|---|---|---|---|---|
| Software Developers | 15 | 240 | 960 | 10 | 2/12/1 | 0/7/8 | 4/2/9 |
| Web Developers | 30 | 105 | 480 | 6.5 | 5/19/6 | 1/26/3 | 12/3/15 |
| Network and Computer Systems Administrators | 29 | 40 | 180 | 3 | 6/16/7 | 2/14/13 | 4/20/5 |
| Database Administrators | 18 | 105 | 480 | 6.5 | 1/10/7 | 0/7/11 | 9/3/6 |
| Computer Systems Analysts | 23 | 240 | 960 | 10 | 2/15/6 | 0/10/13 | 8/5/10 |
| Bookkeeping, Accounting, and Auditing Clerks | 35 | 30 | 90 | 3 | 3/22/10 | 6/29/0 | 0/33/2 |
| Billing and Posting Clerks | 31 | 15 | 40 | 2 | 6/15/10 | 8/22/1 | 0/24/7 |
| Data Entry Keyers | 6 | 30 | 120 | 3 | 2/4/0 | 4/2/0 | 0/4/2 |
| Insurance Claims and Policy Processing Clerks | 25 | 15 | 40 | 2 | 2/13/10 | 0/25/0 | 0/18/7 |
| Medical Records Specialists | 18 | 20 | 60 | 3 | 1/5/12 | 1/17/0 | 0/16/2 |

## Widest disagreements on length (p50 ratio > 3)

- 1312b (Database Administrators): one trend briefing — p50 by coder 480;180;60 min
- 21649a (Database Administrators): one DBMS upgrade planned and installed — p50 by coder 2400;960;480 min
- 3475a (Computer Systems Analysts): one package evaluation — p50 by coder 480;1200;240 min
- 14719a (Web Developers): one performance improvement recommendation — p50 by coder 240;90;60 min
- 3482a (Computer Systems Analysts): one business problem analyzed and solved — p50 by coder 600;960;2400 min
- 11406a (Data Entry Keyers): one shift's work log — p50 by coder 40;25;10 min
- 11409a (Data Entry Keyers): one message resolved — p50 by coder 15;30;60 min
- 2505a (Bookkeeping, Accounting, and Auditing Clerks): one account status review — p50 by coder 30;45;12 min
- 21670a (Software Developers): one change request or bug fix to existing software — p50 by coder 240;150;480 min
- 14694b (Web Developers): one implemented website feature or component — p50 by coder 150;240;480 min
- 14725a (Web Developers): one server hardware or software recommendation — p50 by coder 240;480;150 min
- 3468a (Computer Systems Analysts): one system-to-system integration or interface — p50 by coder 1500;4800;2400 min

## Unit flags

- 14724a (1/3): The item combines interface prototyping with physical, logical and data modeling, which can require substantially different work.
- 1319a (1/3): Item mixes planning a policy with technical configuration, which are very different kinds of work.
- 3470a (1/3): Mixes quick tweaks and multi-week projects; the item is too broad.
- 3482a (3/3): The work item is open-ended and mixes very different kinds of business problem (a quick spreadsheet analysis versus building a production or inventory system). | Item is a very broad problem that mixes analysis and building a system. | The item combines broad business analysis with potentially building and delivering an entire production, inventory or cost system.
- 11409a (1/3): Cryptographic decoding does not match a data entry keyer's usual work and mixes very different cases.
