# Round 3 synthesis: is the sector shrinking, or is work reallocating? (2026-10-14)

This round gathered evidence for the S4-first structure agreed with Andrei. S4 is now split:
- **S4a:** work moves to GCCs (foreign firms' captive centres in India)
- **S4b:** work moves to mid-tier or small Indian firms
- **S4c:** work moves to contractors (already ruled out)
- **S4d:** work leaves India

Each folder has a FINDINGS.md with sources and URLs:

| folder | question |
|--|--|
| `sector_aggregates/` | Is the whole sector shrinking? |
| `gcc/` | How large are GCCs, and did they absorb the slowdown? |
| `gcc_reconcile/` | Why do Nasscom's GCC and industry numbers conflict? |
| `offshore_competitors/` | Did work leave India (S4d)? |
| `listed_panel/` | 21 other listed IT, ER&D and BPM firms, FY23–FY26 |
| `seniority_firms/` | Age, level and trainee data at the 10 firms |
| `seniority_sector/` | Entry-level hiring across the sector and at GCCs |
| `red_team/` | The case against "benign reallocation" |

## Output: not shrinking

- **Exports grew.** RBI's software-exports survey shows India's exports rose 19% in USD from FY23 to FY26 ($185.5bn → $221.4bn). Growth was 7.3% in FY25 and 8.2% in FY26. FY26 growth came from IT services, not BPO.
- **The growth was at private-limited exporters.** These are GCCs, foreign-owned vendors and unlisted Indian firms. They grew 29%, against 6% for public-limited exporters (close to the top six's 7%).
- **Foreign subsidiaries grew faster than the vendors.** In RBI's census of foreign-owned firms, their exports of information and communication services grew 12.6% (FY24) and 11.5% (FY25) in INR, comparing within each census round. The FY26 round is due around late October 2026.
- **Work did not leave India (S4d is unlikely in aggregate).**
  - India's share of world computer-services exports was flat: 29.3% → 30.1% excluding Ireland, 2022–25.
  - Its share among 25 emerging delivery countries held at about 66.6% in H1 every year from 2023 to 2026.
  - Its share of US computer-services imports was flat at about 24–25%.
  - Cognizant's India share of headcount stayed at about 73%.
  - US computer-systems-design employment fell, so there was no onshoring.
- **Caveat: GCC export values track wages, not volume.** GCCs are paid cost plus a markup, so export value moves with their wage bill. Netting out about 9% wage growth leaves roughly 2–5% a year of volume growth.

## Jobs: growth stalled, but no collapse

- **Industry employment grew about 2% a year.** Nasscom's figure for FY23→FY26 is +6% (about +325k), while revenue grew 5–6% a year. Nasscom's total includes GCC staff.
- **GCCs added roughly 260k tech jobs.** Our central estimate is about +385k GCC jobs in all functions, of which about +260k are tech roles. The plausible range is +155k to +430k tech.
  - Nasscom–Zinnov's +460k (FY24–26) is overstated: it mixes report editions and adds newly counted GCCs.
- **The rest of the industry was roughly flat** on the central estimate.
- **Top six:** −61k against the FY23 level, and −384k against their pre-COVID trend. GCC tech hiring more than offsets the first and covers about two-thirds of the second.
- **Other listed firms (21 firms):** they added 62.7k staff, offsetting the top six's loss.
  - Most of the gain was at BPM firms (+36k) and through acquisitions (at least 15.7k).
  - The 12 IT and ER&D firms outside the four mid-tier firms grew only about 2.3% organically over three years, and five of them shrank.
  - So S4b is weak for IT services. Persistent is the exception.
- **Job postings tell us nothing here.** The note's "GCC postings +4% vs IT −4%" (Naukri, one month) is within noise: the monthly year-on-year standard deviation is about 23 points. Drop it from the note.

## The entry rung: narrowing

- **Graduate placements fell.** NIRF data for the same engineering institutions show graduates placed fell 1.8 log points for the class of 2023-24, the first fall since 2016-17. The placement rate fell from 73.8% to 70.1%. These counts cover all employers, including GCCs.
- **Fresher postings fell.** foundit shows fresher postings down 10% year on year in July 2026.
  - IT's share of them fell from 32% to 24%.
  - GCCs' share rose from 8% to 11%, which offsets only about a fifth of the IT loss.
- **GCCs hire fewer freshers.** Freshers are about 16–22% of GCC hiring, against 20–38% at the top six. GCCs do hire heavily at 0–5 years of experience.
- **Firms' own age data.**
  - The under-30 share of headcount fell from FY23 at 8 of the 10 firms.
  - Persistent's under-30 headcount fell 31% while its total headcount rose 20%.
  - Junior hiring at the large firms has partly recovered in FY25–26: Infosys's under-30 share of hires rose from 60% to 73%, and its trainee share recovered from 1.2% to 3–5%.

## Can headcount be split by seniority?

- **At the 10 firms: yes, by age.**
  - Under-30 share of headcount: FY22–25 for 9 firms, FY20–26 for about 6.
  - Under-30 share of new hires: 8 firms.
  - BRSR filings have no age fields, so these come from GRI annexes.
  - High-frequency proxies: an Infosys trainee proxy (quarterly since FY11), and median pay compared with wage hikes.
- **At GCCs: no official split.** Only job-portal and consultancy shares exist.
- **Sector-wide: PLFS unit-level data**, by age × education × NIC industry. It is free but needs a login. Apr–Dec 2025 alone has 4,797 records in NIC 62. GCCs cannot be identified separately.

## Most decisive next test

Use PLFS to count employed graduates aged 21–30 in NIC 62/63 (and 82) each year, 2017-18 to 2025. This needs the user to register at microdata.gov.in.

## Fixes to the note (on hold)

- Drop or caveat the one-month Naukri comparison.
- §5b uses RBI's foreign-owned-firms census across rounds (₹6.5 → 8.5 lakh crore). Use within-round growth instead.
