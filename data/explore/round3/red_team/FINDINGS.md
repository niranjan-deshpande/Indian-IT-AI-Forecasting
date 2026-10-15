# FINDINGS — red-teaming "reallocation, not shrinkage"

*Saved by the orchestrator from the subagent's report; subagents cannot write report files. Date: 2026-10-14. Two parallel sub-searches gathered the broader set of firms and the labour-market items; the probe spot-checked the NASSCOM and foundit figures. Growth rates are % changes unless marked log×100.*

> **Orchestrator note: the two probes disagree on the RBI census of foreign-owned companies.** This probe says foreign subsidiaries' exports grew about 22% in FY24. The GCC probe (`../gcc/FINDINGS.md`) gets +12.6% in INR for FY24 by comparing both years within the same census round. Census rounds are not comparable with each other, because the respondent set grew from 18.5k to 26.3k firms. So the ~22% probably compares across rounds and overstates growth. Use the within-round figures: FY24 +12.6%, FY25 +11.5% in INR. On those figures the FY25 deceleration this probe reports disappears. What remains is that volume growth is modest once wage-driven, cost-plus valuation is netted out.

## 1. Headline
- **Output is not shrinking, and the export growth is real IT work.** RBI survey IT-services exports were $125.5bn → $131.3bn → $147.0bn over FY24–26, about 8%/yr. BPO was flat in FY26 (+0.4%), so the rise is not a BPO artefact.
- **Measured in jobs, the listed firms are shrinking.**
  - Combined headcount at the top six plus the four mid-tier firms fell from 1,788k to 1,746k over FY23–26.
  - The mid-tier added 19.5k, against a 61k fall at the top six and a 384k shortfall against the top six's pre-COVID trend.
  - NASSCOM (industry body): tech employment +2.3% in FY26, against revenue +6.1%.
- **GCC export value overstates volume.** GCC exports are valued at cost plus a markup, so they grow with wages.
  - Private-limited exporters grew 14.1% and 14.2% in INR (FY25, FY26).
  - Net of GCC pay rises of about 9% (Aon), volume grew roughly 4.5%/yr.
  - The RBI census of foreign-owned companies gives +11.5% in INR for FY25, which implies only about 2% volume growth (see the note above on FY24).
- **The four mid-tier firms are a sample of winners.**
  - Eleven other listed mid/small IT firms grew about 5% in FY26, weighted by revenue: median 3.1%, about 2.2% excluding the two BPO-type firms.
  - Coforge's growth is partly acquired, and the Sabre deal is estimated to add about 9 points on its own.
- **The entry route is narrowing.**
  - All fresher hiring fell 10% y/y (July 2026). IT's share of it fell from 32% to 24%; GCCs' share rose from 8% to 11%.
  - Only 30% of GCC hires are early-career.
  - Large-firm fresher hires per $bn of revenue are about half their pre-COVID level at Infosys and HCLTech.

## 2. Angles

| angle | source | confirmed? | what it shows | dent | URL |
|--|--|--|--|--|--|
| Cost-plus valuation of GCC exports | RBI survey FY26 (private-limited, INR); Aon pay survey (consultancy) | data yes; the volume figure is the probe's calculation | Private-limited exports +14.1% and +14.2% in INR. GCC pay rose 9.2% in 2025, so volume grew about 4.5%/yr (+3.4% to +6.5% for pay growth of 10.4% to 7%) | **serious**: cuts the 9–12% headline to about 4–5% volume growth | rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63625 ; aon.com/apac/in-the-press/asia-newsroom/2026/aon-survey-projects-slight-uptick-in-salaries-in-india-2026 |
| Same, from the RBI census of foreign-owned companies | RBI census 2024-25, Table 9C | yes for FY24–25 | Foreign subsidiaries' I&C exports ₹10.40 → 11.60 lakh crore (+11.5%). FY24 "about +22%" is probably a cross-round comparison (see the note above) | some, after correction | rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=61524 |
| INR vs USD and real terms | RBI survey (implied ₹/$) | yes | Implied ₹/$ 82.8, 84.6, 88.3. Exports grew 9.7% and 13.0% in INR but 7.3% and 8.2% in USD. The headline 7–8% is already in USD | some | prid=63625, prid=61562 |
| Change in transfer-pricing rules | Budget 2026-27: a single 15.5% safe-harbour margin (was 17–24%); threshold ₹300cr → ₹2,000cr | PIB search snippet; the notified rules were not seen | Captive export values for firms that opt in will step down from FY27. A series break, not a fall in volume | some, for future readings | pib.gov.in/PressReleasePage.aspx?PRID=2221428 |
| Non-IT components | RBI survey, by activity | yes | FY25 growth was led by BPO (+11%) and engineering services (+13%). In FY26, IT services +12% and BPO flat. Over two years IT services grew in line with the total | **none** | prid=63625 |
| Delivery abroad | RBI survey Mode 3 (affiliates abroad) and Mode 4 (on-site) | yes | Mode 3 $13.9bn → $17.9bn (+29%); Mode 4 $19.1bn → $18.4bn. Indian firms book more of their growth abroad | some | prid=63625 |
| Selection of mid-tier firms | Company releases, broker notes, news | mostly yes; a few figures only from snippets | 11 other firms: about 5% revenue-weighted, median 3.1%. Birlasoft −6%; Tata Elxsi −5.5% cc (unverified); Cyient's engineering segment −0.7%; Sonata −2.1%; KPIT +1.3% cc | **serious** for "the mid-tier is booming" | `broader_listed_it_growth_fy26.csv` |
| Mid-tier acquisitions and deal concentration | repo; broker note on Coforge | repo yes; broker figure is an estimate | Coforge +31% in FY25 includes Cigniti; Sabre estimated at ~9 points of FY26. Persistent (~17–19%) is the clean organic case; Mphasis and Hexaware grew 7–9% | some | barodaetrade.com/Reports/Coforge-Q4FY26ResultReview6May26-Research.pdf |
| Employment vs output | repo headcounts; NASSCOM via news | yes | Ten-firm headcount −42k over FY23–26; the mid-tier covers ~5% of the top six's trend shortfall. NASSCOM: +1.35 lakh jobs (+2.3%) against revenue +6.1%, an elasticity of about 0.3–0.4 | **serious** | `listed_headcount_absorption.csv` ; etvbharat.com/en/business/india-fy26-tech-revenues-hit-usd-315-billion-enn26022404879 |
| GCC count inconsistent with industry total | Nasscom–Zinnov (consultancy): 2.36m in FY26; 1.9m in FY24 | partly | +460k at GCCs would exceed NASSCOM's total net additions (~2.7 lakh), if NASSCOM's total includes GCCs (inferred) | some: the GCC count is unusable as evidence | freepressjournal.in/business/indias-gcc-industry-records-984-billion-revenue-in-fy26-report-says |
| Job postings (GCC +4% vs IT −4%) | Naukri JobSpeak via news; repo noise estimate | yes | August 2026: GCC +10%, IT +11%. The repo's 2022 data show a monthly y/y s.d. of 23 points, so ±4% in one month is noise | **serious**, as evidence it is worthless | angelone.in/news/stocks/india-s-white-collar-hiring-rise-2-in-september-as-ai-ml-hiring-jumps-20 ; `data/explore/workforce/FINDINGS.md` |
| Fresher and campus hiring | foundit via news; repo fresher counts; news on TCS | yes | Fresher hiring −10% y/y; IT share 32% → 24%; GCC share 8% → 11%. By inference, IT fresher hiring fell ~33% and GCC fresher hiring rose ~24%, so GCCs offset about a fifth. TCS plans ~25k freshers in FY27 (was ~42k; news). Infosys fresher hires per $bn: 640–990 in FY24–26 against 1,200–1,800 in FY16–19 | **serious** for the mobility ladder | businesstoday.in/amp/jobs/story/...-547654-2026-08-06 ; `workforce/fresher_hires_annual_best.csv` |
| Fresher pay and onboarding | news | yes, weakly sourced | TCS trainee pay ₹3.16 LPA in 2007 and ₹3.36 LPA in 2026. Wipro has left more than 250 freshers holding offer letters without onboarding since 2025 (union complaint). TCS cut 12,261 jobs in 2025 | some | `labour_market_signals.csv` |
| Graduate and youth unemployment | PLFS (MoSPI, official) | 2025 annual yes; graduate 2023-24 figure inferred | Youth unemployment 9.9% in 2025 (10.3% in 2024); educated youth 6.5% (7.0%). Quarterly youth unemployment 15.9% in Apr–Jun 2026, up from 14.6% (via news). Graduates about 13% in 2023-24. No IT-specific series | some: mixed, recently worse | mospi.gov.in press notes (see CSV) |
| Engineering seats | AICTE via news | yes, via news | About 25% of BTech seats empty (enrolment/intake 75% in 2024-25); CS seats expanded heavily. Graduate supply rises while IT intake shrinks | some | news.careers360.com/... |
| Startup layoffs | Inc42 (news) | yes | More than 9,500 layoffs at 44 startups in 2025 (about 9,000 in 2024), much of it gaming | minimal | inc42.com/buzz/a-year-of-pink-slips-9500-layoffs-among-indian-startups-in-2025/ |
| Office market | Knight Frank, JLL (consultancies) | yes | GCCs took 38% of 2025 leasing and 41.7% in H1 2026 (+14%). IT-services leasing +94% in 2025. Bengaluru gross leasing −20.5% in H1 2026 | none; mildly supportive | jll.com/en-in/newsroom/india-office-leasing-dips-3-point-9-percent-to-379m-sf-gccs-strong |
| AI adoption in GCCs | news, source unnamed | weak | GCC hiring +11% in H1 2026, but only 30% early-career and about two-thirds of roles need AI or data skills. A story that GCC hiring is slowing because of AI was not verified (spam sites only) | some, speculative | swarajyamag.com/amp/story/economy/ai-data-skills-now-drive-two-in-three-new-gcc-jobs-... |
| Large foreign IT employers | repo (SEC filings) | yes | Cognizant 336k → 357k (Q1 2025 to latest); Accenture 779k → 814k. The private-limited vendors have not collapsed | none | `core_quarterly_final.csv` |
| Latest quarter | IMF BOP (repo) | yes | Computer-services exports +8.6% y/y in Apr–Jun 2026, down from 12–14% | some: slowing | `trade/imf_bop_india_services_quarterly.csv` |

## 3. Overall assessment
"The sector isn't shrinking" holds for output: India-delivered IT-services exports really did grow about 8%/yr in USD.

It does not hold for jobs, which is the policymaker's question:
- Correcting for cost-plus valuation cuts GCC-type volume growth to roughly 2–5%/yr.
- The mid-tier winners are a selected sample.
- Headcount at the ten listed firms fell.
- Industry employment grows at about a third of the rate of revenue.
- The fresher channel is narrowing; GCCs replace only a fraction of it and hire mostly experienced staff.

The defensible framing: work is reallocating toward GCCs and some mid-tier firms, but the number of jobs the sector creates for young graduates has stalled. That fits S4a plus a labour-saving component (S2 or S3), not benign reallocation alone. "Relatively benign" is not supported for the mobility question.

**Most decisive test.** Use PLFS unit-level microdata to measure employment in IT (NIC 62–63, possibly plus 82 for BPO) for urban graduates aged 21–30, from 2022-23 to CY2025. If it grew at or above trend, reallocation survives the jobs question; if it is flat or falling, reallocation fails.

## 4. Could not check
- PLFS microdata (registration needed); PLFS figures for technical-degree holders.
- EPFO by industry (no IT series; 403 errors).
- AICTE dashboard (would not load); national CS seat-vacancy figures.
- Firm-level GCC headcount, and whether NASSCOM's total includes GCCs.
- Organic-growth splits for Persistent, Hexaware and Happiest Minds; headcount for the broader set of firms; Datamatics, Nucleus, R Systems, 3i Infotech.
- Whether the new safe-harbour rules have been notified.
- Tata Elxsi −5.5% cc (snippet only).
- S4d (work moving abroad) was left to `../offshore_competitors/`.

## Addendum from the probe's final report
- **Export mix by year.** In FY25 the mix was the reverse of FY26: IT services grew +4.6% in USD and BPO +11.4%.
- **Fresher hires per $bn of revenue.**
  - HCL: about 570–900 in FY24–26, against about 2,000 before COVID.
  - Infosys: about 640–990, against 800–1,800.
- **Other mid/small firms.** Excluding eClerx and Firstsource, which are BPO-type, the other mid/small firms grew about 2.2%. The four chosen firms grew about 16%.
- **The PLFS test should include BPO.** It should cover NIC 82 (BPO) as well as 62–63, and count regular salaried graduates aged 21–29.
- **Second-best test.** Get GCC employment from the RBI census of foreign-owned companies, or build a ratio of export value to employment from its FY26 round.

## Files
- `rbi_exports_by_activity_type.csv`
- `rbi_fla_foreign_subsidiary_exports.csv`
- `listed_headcount_absorption.csv`
- `broader_listed_it_growth_fy26.csv`
- `labour_market_signals.csv`
