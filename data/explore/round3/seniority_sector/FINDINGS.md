# FINDINGS — entry-level vs experienced IT employment, sector-wide and at GCCs

*Saved by the orchestrator from the subagent's report; subagents cannot write report files. Probe date: 14 Oct 2026. Extends `data/explore/workforce/FINDINGS.md` (top-6 ESG tables; JobSpeak experience bands to 2024). "Confirmed" means the page or file was fetched and the data seen.*

## 1. Headline

**(a) Entry-level hiring is falling sector-wide.** The evidence is modest and recent.
- **NIRF (official; institutions self-report).** Same institutions, same edition:
  - UG engineering graduates placed fell 1.8 log points for the class of 2023-24, while graduates rose 3.3.
  - The placement rate fell from 73.8% to 70.1%.
  - This is the first fall since 2016-17; earlier classes grew 2.5 to 10.5 log points.
  - NIRF counts placements with every employer, GCCs included.
- **foundit (job portal), July 2026.**
  - Fresher postings fell 10% YoY.
  - IT firms' share of fresher postings fell from 32% to 24%, which implies IT fresher postings fell about 33%.
- **Naukri JobSpeak (job portal), September 2026, all industries.** Postings for 0–3 years of experience rose 1%, against +5% to +7% for the senior bands.

**(b) GCCs hire freshers, but less intensively than IT-services firms and not enough to fill the gap.**
- foundit: GCCs' share of fresher postings rose from 8% to 11% (implied about +24%). That offsets only about a fifth of the IT loss.
- Taggd survey (industry): freshers are 16% of GCCs' planned FY27 hires. At the top-6 firms, freshers have been about 20–38% of hires (global denominators).
- So "rising GCC employment means rising non-senior employment" holds for 0–5 years' experience (about 30–46% of GCC hiring), but not for the fresher rung.

**Data access**
- **PLFS unit-level data** is free but needs a login (free registration). Its metadata show 4,797 NIC-62 person-visit records for Apr–Dec 2025, which is enough to build a series for graduates aged 21–30.
- **NIRF 2026** (class of 2024-25) is not yet online: `Rankings/2026/` returns 404.

## 2. Sources

| name | publisher | measures | disaggregation | period/freq | lag | access | confirmed? | URL |
|--|--|--|--|--|--|--|--|--|
| NIRF institution data (Engineering) | MoE/NIRF (official, self-reported) | UG 4-year graduates, placed, median salary, higher studies | institution × graduating year | classes 2015-16 to 2023-24; annual | ~1.5 yr | free PDFs, ranked institutions only | yes (1,313 PDFs parsed) | https://www.nirfindia.org/Rankings/2025/EngineeringRanking.html |
| PLFS unit-level data | MoSPI (official) | employment by NIC 5-digit, age, education, wages | person | 2017-18 to 2023-24; CY24; CY25; Apr–Dec 2025 quarterly | 3–5 months | free, login required | metadata only | https://microdata.gov.in/NADA/index.php/catalog/292 |
| PLFS reports | MoSPI | broad industry sections only | no NIC 62 × age × education | annual | — | free | no (inferred) | mospi.gov.in |
| EPFO payroll | EPFO (official, administrative) | new subscribers | age bands from under 18 to over 35; "top industries" (expert services ~40%) | monthly from Sep 2017 | ~2 months | 403/404 to scripts | no (snippets and press only) | https://www.epfo.gov.in/site_en/Estimate_of_Payroll.php |
| AICTE dashboard | AICTE (official, self-reported) | intake, enrolment, passed, placed | institution / state | to 2021-22 (seen in press) | ? | connection reset | no; press gives 3.97, 6.45, 5.78, 6.19 lakh placed, 2018-19 to 2021-22 | facilities.aicte-india.org/dashboard |
| Naukri JobSpeak | Info Edge (job portal) | postings | experience bands (all industries); GCC tile | GCC series from Jul 2024 (levels Oct 2023 to Oct 2024); monthly | ~7 days | free PDF | yes | https://www.infoedge.in/pdfs/News_Events_pdfs/Naukri-Jobspeak-September-2026.pdf |
| foundit Insights Tracker | foundit (job portal) | postings | experience band; fresher share by employer type (incl. GCC) and industry | monthly | ~1 week | free web | yes (Jul 2026) | https://www.foundit.in/career-advice/foundit-insights-tracker-july-2026/ |
| Taggd GCC Talent Lab 2026 | Taggd (industry) | planned hiring mix | freshers / 1–5 years | FY27 intentions | — | press page | yes | https://taggd.in/news-and-media/finding-right-talent-biggest-challenge-for-gccs-eyeing-workforce-expansion-report/ |
| Zinnov–Nasscom GCC Landscape 2026 | consultancy | GCC employment, 2.36m (FY26) | not seen | annual | — | gated | landing page only | https://zinnov.com/centers-of-excellence/zinnov-nasscom-india-gcc-landscape-2026-report/ |
| Indeed Hiring Lab; LinkedIn Grad's Guide | platforms | postings; entry-level hiring | no IT × experience split found | — | — | — | no (press only) | — |

## 3. Caveats

**NIRF**
- Covers all employers; it does not split IT or GCC hiring.
- Ranked top-100/200 institutions only. 49 unranked IDs were tested and all returned 404.
- An upper-tier sample: about 175k of 1.2m+ B.Tech graduates.
- 35% of overlapping cells are revised in later editions (−2% to −4%), so compare within one edition.

**PLFS**
- The right official denominator, but GCCs can't be identified (they fall under NIC 62/63/70 or the parent's industry).
- Survey design break in 2025.
- Annual NIC-62 sample is roughly 1,000–1,500 workers per round. This is the probe's estimate, not a count.

**JobSpeak**
- No GCC × experience split in any month checked: Jul 2024, Oct 2024, Jan/Apr/Jul 2025, Jan/Jul/Aug/Sep 2026.
- Postings only; campus hiring isn't covered.

**foundit**
- A single portal, with rounded shares, so implied growth rates are ±5 points.
- The GCC (employer type) and IT (industry) categories can overlap.
- Its figures for the 0–3-year share of GCC hiring conflict: 42% (Jul 2025, via HRKatha) against 30% (2026, via Business Today).

**Surveys** report intentions only. Unverified press figures were not used, e.g. "1.33 lakh GCC freshers FY25" and "IT freshers 6 lakh → 1.2 lakh".

## 4. Numbers
The full list, with URLs, is in `key_numbers.csv`.

**NIRF, within-edition YoY change in UG graduates placed (log points)**

| classes | all | elite | other |
|--|--|--|--|
| 16-17 → 17-18 | +2.5 | +2.4 | +2.5 |
| 17-18 → 18-19 | +10.5 | +5.7 | +11.6 |
| 18-19 → 19-20 | +4.0 | −4.5 | +5.8 |
| 19-20 → 20-21 | +6.9 | +5.8 | +7.1 |
| 20-21 → 21-22 | +7.7 | +19.9 | +4.8 |
| 21-22 → 22-23 | +9.5 | +10.8 | +9.1 |
| **22-23 → 23-24** | **−1.8** | **+0.1** | **−2.4** |

For the class of 2023-24:
- Median salary at elite institutions fell 11 log points.
- Graduates going on to higher studies rose 20%.

## 5. Not checked
- PLFS microdata (login needed).
- NIRF 2026 (not yet published).
- EPFO and AICTE portals (blocked to scripts).
- Full Zinnov–Nasscom and Nasscom "Next Generation" reports (gated / HTTP 406).
- Original Xpheno, Quess, ANSR and TeamLease reports.
- Earlier foundit months, which would give a time series of GCCs' fresher share.

## Files
- **Scripts:**
  - `01_fetch_nirf.sh`
  - `02_parse_nirf.py`
  - `03_aggregate_nirf.py`
  - `04_within_edition_yoy.py`
  - `05_plfs_nic_cellcounts.py`
- **NIRF data:**
  - `nirf_ug4_placement_long.csv`
  - `nirf_ug4_placement_by_gradyear.csv`
  - `nirf_within_edition_yoy.csv`
- **Other data:**
  - `plfs_nic62_63_case_counts.csv`
  - `key_numbers.csv`
- **`raw/`:** NIRF PDFs (15 MB), 4 JobSpeak PDFs, foundit extract.
