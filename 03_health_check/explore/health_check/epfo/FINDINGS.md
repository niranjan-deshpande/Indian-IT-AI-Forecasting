# FINDINGS.md

## 1. What exists and what we have

**The source.** EPFO publishes a monthly PDF called "Net Payroll Data EPFO" on the 20th of each month (an xlsx too from April 2025). Each report covers the month about two months earlier: the report released on 20 Aug 2025 covers data to June 2025.

Each report contains:
- **Page 1:** net payroll for six age bands (<18, 18-21, 22-25, 26-28, 29-35, >35) and a total. It gives one figure per closed financial year from FY2017-18 (Sep-Mar only), then monthly figures for the current year only. It also counts establishments filing their first monthly contribution return.
- **Components table:** by age and period:
  - (a) new subscribers
  - (b) members who exited
  - (c) members who exited and later rejoined
  - (d) net payroll = a − b + c
- **State × age, gender × age, and industry × age tables.** The industry tables show only the **top 10 industries within each age band**.

**IT is only partly separable.** EPFO uses its own industry headings, not NIC codes. The IT one is "Establishment engaged in manufacture, marketing, servicing, usage of computers" ("computers/IT" below).
- It is in the top 10 for ages 18-21 and 22-25 in every report, and for 26-28 in most.
- It never appears for <18 or >35, and for 29-35 in only one report (Oct 2022).
- So we have **IT × age for 18-28 only, with no all-ages IT total.**
- We don't know how EPFO classifies big IT firms. Some may sit under "Expert services" (the largest heading, which also covers manpower suppliers). Others may sit under "Others", a residual that grew from 0.32m to 0.60m in 18-25 net additions between FY22 and FY25.

**Access.** epfindia.gov.in and epfo.gov.in return HTTP 403 from outside India. Every report came from its Wayback Machine capture, byte for byte, and every CSV row carries the original and archive links.
- 66 reports, released 20 Jul 2019 to 20 Aug 2025. A few releases are missing (Aug and Nov 2019; Mar, Jun, Jul and Sep 2020; Jul 2024); none of these gaps affect the "best" files.
- The 20 Sep 2025 release (data to July 2025) could not be retrieved, so July 2025 uses the PIB release headline (PRID 2169975).

**EPFO appears to have stopped publishing.** The archived EPFO listing page (23 Jan 2026) shows the Sep 2025 release as the newest. That release named 20 Oct 2025 as the next release date. The last PIB payroll release is dated 23 Sep 2025. No reason has been given; it coincides with the launch of the Employment Linked Incentive (ELI) scheme. There is no FY2025-26 annual figure.

**Aggregators.** None was usable here:
- data.gov.in and RBI DBIE did not respond from this machine.
- The labour.gov.in mirror of the same PDFs now returns 404.
- MoSPI's "Payroll Reporting in India" page is a JavaScript app and could not be scraped.
- Dataful and CEIC were not checked (the search limit ran out). As far as I know they only re-host EPFO headline series.

## 2. Files

| File | Content |
|--|--|
| `01_download.sh`, `wayback_captures.txt` | Re-download all raw PDFs from their archive copies |
| `02_parse.py` | Parses the PDFs (needs `pdftotext`) into the three `*_vintages.csv` files. Run with `python3 -I` |
| `03_build.py` | Builds the "best" and like-for-like files below. Run with `python3 -I` |
| `epfo_age_net_payroll_vintages.csv` | Page-1 net payroll by age, every period in every vintage |
| `epfo_age_components_vintages.csv` | New subscribers, exits, rejoins and net, by age, period and vintage |
| `epfo_industry_age_vintages.csv` | Top-10 industry × age × period, every vintage (16 MB) |
| `epfo_fy_age_best.csv` | FY2017-18 to FY2024-25 by age, plus FY2025-26 Apr-Jun, from the 20 Aug 2025 release |
| `epfo_monthly_age_best.csv` | Apr 2019 to Jun 2025 by age, each month at its last print; July 2025 from PIB |
| `epfo_monthly_first_print.csv` | Every month at its first print (about a 2-month lag): total, ages, IT 18-28 |
| `epfo_q1_aug_release.csv` | Apr-Jun of each year as printed in that year's August release (FY21 to FY26). The only fair way to compare FY26 |
| `epfo_it_age_best.csv` | IT heading: 18-21, 22-25 and 26-28, with the all-industry figure and IT's share; annual and monthly |
| `epfo_industry_age_best.csv` | All top-10 headings × age; annual from the latest vintage, months at their last print |
| `epfo_revisions.csv` | First print vs last print for each month |

## 3. Definitions

- **Net payroll** = new subscribers + rejoiners − exits. It is a flow, not a headcount, and people are de-duplicated by their Aadhaar-linked account number (UAN).
- **New subscribers** means a person's first-ever EPF contribution. This is the cleanest measure of entry into formal payroll, and the closest EPFO gets to the entry-level rung.
- **Exits** are recorded when contributions stop, often months later. This is why the data are revised so heavily.
- **FY2017-18** covers Sep 2017 to Mar 2018 only.

## 4. Caveats

1. **Coverage.** EPFO covers the formal and semi-formal sector only.
   - EPF is compulsory for establishments with 20 or more employees.
   - Membership is compulsory only for employees whose basic pay is at or below ₹15,000 a month at joining. Higher-paid first-time joiners can be "excluded employees".
   - Firms that run their own provident fund trusts (several large IT firms do) manage their own funds. The reports don't say whether their members are counted. **This is the biggest open question for using EPFO on big-firm IT.**
2. **Net payroll is not employment.**
   - A job-switcher whose contributions lapse and resume shows up as an exit and a rejoin.
   - Temporary workers are included.
   - Annual sums are not the number of people on payrolls.
3. **Revisions are large and one-directional.**
   - A month's first print falls by a median of 32% by its last print (range −19% to −61%, FY22-FY25).
   - The 12 first prints for FY25 sum to 20.5m; the final annual total is 13.0m.
   - Once a year closes (in the June release) its annual figures are frozen; no annual total changed in any later report.
   - So press headlines are first prints and are not comparable with annual figures. Annual totals are consistent with each other.
   - Jan-Mar months get less downward revision than Apr-Sep months, so the last-print monthly series has a sawtooth pattern. For comparisons, use annual totals, first prints, or the August-release Apr-Jun file.
4. **FY2023-24 has thinner monthly detail.** The Mar, Apr and May 2024 releases printed one month each, so Jan-Mar 2024 exist only as first prints.
5. **Industry figures.**
   - Top-10 only, so a blank does not mean zero.
   - The heading belongs to the establishment, not the worker.
   - Headings occasionally get reclassified: IT 18-21 in FY19 was 96,016 in 2019-20 reports and is 92,658 now.
   - The "Others" residual is growing.
6. **Misprints in the reports.**
   - Page 1 shows FY2019-20 age 22-25 as 1,771,707, a repeat of the FY19 value. The components table gives 2,196,926, which makes the row add up; the best files use that.
   - In the Aug 2025 report the FY2024-25 column is labelled "Sep-05" in one table; this was corrected in parsing.
7. **Parsing checks.** Every page-1 row adds up to its printed total, and annual totals match across all reports. Some industry rows that wrap across lines in a few 2019-21 reports are misparsed; no "best" file uses those reports.

## 5. Headline numbers

Net payroll unless stated. Annual figures are the frozen totals from the 20 Aug 2025 release.

| | FY22 | FY23 | FY24 | FY25 | FY22→FY25 |
|--|--|--|--|--|--|
| All ages, all industries | 12.23m | 13.85m | 13.15m | 12.98m | +6% (−6% from FY23 peak) |
| Age 18-25, all industries | 6.37m | 6.85m | 6.53m | 6.37m | 0% |
| New subscribers aged 18-25 | 6.03m | 6.41m | 6.21m | 6.53m | +8% (18-21 +19%; 22-25 −3%) |
| **IT, 18-25** | **366k** | **289k** | **210k** | **251k** | **−31%** |
| IT, 22-25 | 238k | 170k | 118k | 152k | −36% |
| IT, 26-28 | 70k | 41k | 22k | 24k | −66% |
| IT share of all 18-25 net additions | 5.8% | 4.2% | 3.2% | 3.9% | −1.8 pp |

- **IT falls the most of the top-10 industries** for ages 18-25, FY22→FY25:
  - Expert services −3%
  - Trading −17%
  - Electrical/mechanical engineering products +4%
  - Construction +15%
  - "Others" +88%
- **Before COVID, IT 18-25 was 205k (FY19) and 240k (FY20).** FY25 (251k) is about back to that level, while all-industry 18-25 is about 35% above FY20 (4.74m).
- **FY26 so far** (Apr-Jun, each year as printed in its August report, so revision stages match):

  | Apr-Jun | FY22 | FY23 | FY24 | FY25 | FY26 |
  |--|--|--|--|--|--|
  | IT, 18-25 | 84k | 101k | 59k | 72k | 75k |
  | All industries, 18-25 | 1.44m | 2.16m | 2.05m | 2.28m | 2.37m |

  IT is up 3% on a year earlier but 26% below FY23. IT's share of 18-25 is about 3.2%, against 5.8% in FY22.
- **July 2025 first print (PIB):** 2.10m net in total, 0.91m aged 18-25, 0.98m new subscribers.

## 6. Bearing on the working claim

- **Supports "entry rung narrowing" in IT.** Net additions of 18-25 year-olds under the IT heading are down 31% from FY22 and down more at 26-28. IT's share of young formal entrants fell from 5.8% to about 3-4%, while young formal entry overall was flat to rising.
- **Supports "sector job growth slow".** IT net additions are still positive, at about 250k a year at ages 18-25, but well below the FY22 peak.
- **What EPFO cannot show:** big firms on their own, or an all-ages IT total. Coverage of firms with their own provident fund trusts is unclear.
- **Early FY26 shows stabilisation, not further decline.** This matches the small FY25 rebound in big-firm fresher hiring.

## 7. Candidate charts

1. **IT's falling share of young formal entrants.** Bars for IT net additions FY19-FY25, stacked 18-21 / 22-25 / 26-28, with a line for IT's share of all 18-25 additions (5.8% → 3.9%). Source: `epfo_it_age_best.csv`.
2. **Index, FY22 = 100, ages 18-25:** IT, all industries, expert services, trading, construction and engineering products. IT falls furthest. Source: `epfo_industry_age_best.csv` and `epfo_fy_age_best.csv`.
3. **Like-for-like Apr-Jun, FY21-FY26:** IT 18-25 against all-industry 18-25. This is the only fair way to show FY26. Source: `epfo_q1_aug_release.csv`.
4. **Why the headlines mislead:** first print vs final for each month, FY20-FY25, annotated with FY25's 20.5m of first prints against a 13.0m final. Source: `epfo_revisions.csv` and `epfo_monthly_first_print.csv`. Best as a methods collapsible.
5. **Entry vs churn, ages 18-25, FY19-FY25:** new subscribers against net payroll. New entrants are flat to rising, so the IT weakness is not a shortage of young people entering formal work. Source: `epfo_fy_age_best.csv`.
