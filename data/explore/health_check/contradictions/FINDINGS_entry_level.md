# FINDINGS_entry_level.md

*2026-10-15. PLFS figures are our own survey-weighted aggregates from PLFS unit-level data (MoSPI, NSO), used under the Data Access Agreement. Only aggregates are reported. Scripts and CSVs are in `contradictions/plfs/`.*

## 1. Future of India Substack (2 Oct 2026)

**Their method.**
- PLFS 2017-18, 2022-23, 2023-24 and 2025.
- IT means NIC 62–63.
- "Salaried graduates" means graduates in regular salaried jobs.
- Real earnings are medians of all IT workers with recorded earnings, deflated by CPI-Combined to 2025 prices.
- They don't state the activity status, NCO codes or any code. ([post](https://foifaction.substack.com/p/it-sector-helped-build-the-indian))

**Reproduction.** "Ours" means our PLFS figures (MoSPI): usual principal status (UPS), NIC 62+63, graduates = education codes 12–13. Every number here can be rebuilt from the CSVs.

| Their number | Their value | Ours | Match |
|--|--|--|--|
| IT share of salaried graduates (17-18 / 22-23 / 2025) | 6.9 / 13.7 / 11.2% | 6.9 / 13.8 / 11.2% (weekly-status version 13.7) | Exact |
| IT share of salaried graduates aged 21–25 (22-23 → 2025) | 20.0 → 15.8% | 20.4 → 16.0% (SE 1.5 / 1.0) | Yes |
| IT share of graduates in the labour force | 3.9 / 7.4 / 6.0% | 3.9 / 7.6 / 6.2% | Yes |
| Share of IT workers who are salaried graduates | 82% | 82.4% | Yes |
| IT workers (17-18 / 23-24 / 2025) | 28.8 / 69.3 / 68.2 lakh | 23.5 / 59.8 / 57.0 lakh | Their figure ÷ ours = 1.22 / 1.16 / 1.20 |
| Software developers and analysts inside IT (23-24 → 2025) | 42.5 → 36.7 lakh | 36.8 → 30.7 lakh (×1.16 / ×1.20 gives theirs) | Yes, after rescaling |
| Keyboard operators, share of IT | 6.1 → 10.3% | 6.1 → 10.1% | Yes |
| ICT support technicians, share of IT | 2.7 → 5.9% | 2.6 → 6.0% | Yes |
| Real median pay, all IT workers (2025 ₹) | 35.7k → 40.0k | 36.1k → 40.0k (2023-24: 47.7k) | Yes |
| Median pay, 2025: age 21–25 / 30+ | ₹28k / ₹45k | ₹28k / ₹45k | Exact |

**Why their levels are higher.**
- Changing the definition doesn't close the gap. Other employment measures (weekly status, ps+ss) land within 2% of our numbers. Adding NIC 58 or 61 doesn't match either.
- The ratio varies by round: 1.22, about 1.13 (2022-23), 1.16 and 1.20. That pattern fits rescaling to population projections: PLFS's own weights sum to only 1.07–1.22bn people. This is my inference.
- Over 2023-24→2025 the rescaling adds about +3pp to every change they report.

**How robust each of their claims is.** Our numbers, without their rescaling:
- **Share of young salaried graduates in IT: robust, but it's about the denominator.**
  - Salaried graduates aged 21–25 in IT are flat: 9.5 → 11.5 → 10.9 → 9.95 lakh (2022-23 to CY2025).
  - All salaried graduates aged 21–25 rose from 46.8 to 62.0 lakh, +26% of that before the redesign.
  - So IT stopped absorbing the growing supply; it did not cut young graduates.
- **"IT employment peaked in 2023-24": not robust.** Without the high-weight cluster, 2023-24 is 56.7 lakh, below CY2025's 57.0. The series is flat since 2022-23.
- **"Salaried-graduate IT jobs peaked": not robust.**
  - All ages: 47.9 lakh (2023-24, without the cluster) vs 47.0 (CY2025).
  - Ages 21–25: 10.3 vs 9.95 lakh, about −3%.
- **"Developers fell about 14%": fragile.**
  - The drop has z ≈ 1.5, and 2023-24 includes the cluster.
  - The shift toward keyboard operators and support technicians lands on the 2025 redesign.
- **"Real pay peaked in 2023-24": true for juniors only.**
  - Medians bunch at round numbers (₹40k, ₹45k, ₹50k), so they jump between them.
  - The real mean for all IT workers is flat: 51.0k → 49.5k.
  - For ages 21–25 the real mean fell 35.2k → 30.9k (−12%, z ≈ 2). This is the robust part.

**Use:** cite them as corroboration, but use our unscaled numbers. Their age 21–25 share chart is worth adopting, with the CY2025 design break marked.

## 2. State of Working India 2026

**What it says.** "Nearly 40% among the 15- to 25-year-olds, and 20% among the 25- to 29-year-olds." Coverage gives 39.33% for 2023. The data are PLFS 2023-24, and the extract I could read doesn't name the activity status. The "about 7% get permanent salaried jobs within a year" figure is from CMIE CPHS. ([press release](https://azimpremjiuniversity.edu.in/media/resources/SWI/SWI-2026/SWI-2026-Press-Release-15Mar.pdf), [appendix](https://azimpremjiuniversity.edu.in/media/resources/SWI/SWI-2026/SWI-2026-Appendix.pdf), [Business Today](https://www.businesstoday.in/jobs/story/youth-in-labour-market-graduate-unemployment-remains-high-in-india-520932-2026-03-17))

**Graduate unemployment rates from our PLFS (MoSPI), %.** SE is about 1.1pp for 2023-24 and 0.6pp for CY2025.

| Group | Measure | 17-18 | 21-22 | 23-24 | CY24 | CY25 |
|--|--|--|--|--|--|--|
| 15–25 | Principal status | 47.9 | 42.2 | 41.2 | 41.6 | 32.6 |
| 15–25 | Weekly status | 47.7 | 40.5 | 38.2 | 38.8 | 39.8 |
| 15–25 | Official ps+ss | 45.8 | 37.4 | 34.5 | 35.2 | 28.9 |
| 21–25 | Principal status | 46.9 | 41.9 | 40.1 | 41.1 | 31.8 |
| 21–25 | Weekly status | 46.8 | 40.2 | 37.3 | 38.5 | 39.2 |
| 21–25 | Official ps+ss (our figure) | 45.0 | 37.1 | 33.7 | 35.0 | 28.3 |
| 25–29 | Principal / weekly / ps+ss | 27.6 / 28.0 / 26.4 | – | 21.8 / 20.5 / 18.9 | – | 17.8 / 22.1 / 16.0 |
| Engineering degree, 21–25 | Weekly / ps+ss | 53.3 / 53.3 | 41.9 / 39.5 | 37.5 / 35.9 | – | 41.0 / 36.6 |

**Reconciliation.** Their ~40% and our 28.3% measure different things:
- Measure: about 6pp. Theirs most likely uses principal status. Their 2023 report's 42.3% for 2021-22 matches our 42.2%, but that 42.3% is recalled and I couldn't verify it.
- Survey year: about 5pp (2023-24 vs CY2025).
- Age band: about 1pp.
- Their "1.1 of 6.3 crore graduates aged 20–29 unemployed": the ratio matches ours (17.2% vs 17.5%). The levels don't; theirs look rescaled too.

**Key finding.** From 2017-18 to 2023-24, unemployment fell on every measure. The further fall in CY2025 appears only on usual status. On weekly status it is flat or slightly up, and the same holds for engineering graduates. The redesign is the likely cause.

**Use:** cite SWI's ~40% (PLFS 2023-24) for the level, next to our concept-matched 37–41%. Show the trend on two measures, ending at CY2024 within the old design. Cite the 7% figure as SWI/CMIE only.

## 3. Job portals

**Naukri.**
- What it counts: postings, not hires, and no campus hiring. The 0–3-year experience band covers all industries.
- January 2026: freshers +8%, IT flat, BPO/ITES +21% (freshers there +39%).
- February 2026: freshers +17%, IT +6%.
- Against 2022, chained from our files:
  - Fresher (0–3 year) postings in 2026: −0.1% (Jan), +1.0% (Feb), +6.1% (Aug). That is a return to the 2022 level after a 12% fall from 2022 to 2024.
  - Senior (16+ year) postings: +73% to +97%.
  - IT-Software index: −29% to −42%.
- Values for 2025–26 were read off charts and are rough to about ±2pp.

**LinkedIn.**
- The source wording: for bachelor's holders, hiring into firms with 1–10 employees "grew 64% between 2023 and 2025, while for the broader entry-level cohort, it grew 168%."
- So the 168% is about micro-firm hiring. The metric is also based on LinkedIn members, it can't be reproduced, and it has no IT figure.
- Don't cite it as total entry-level hiring.

**Not a contradiction.** Our evidence is about IT services, hires and pay:
- Fresher hires at TCS, Infosys and HCLTech: 218k → 76k (−65%).
- Infosys junior grades (JL3 and below): 46% → 30% of headcount.
- NIRF class of 2023-24: number placed fell 1.8 log points while graduates rose 3.3.
- Junior pay relative to seniors is falling.
- IT-specific portal data agree: Xpheno entry-level tech openings −44%; foundit's IT share of fresher hiring 32% → 24%; TeamLease IT fresher hiring intent 81% → 76%.

**Concede:** the squeeze is in IT, not graduate hiring overall, and big-firm fresher intake has partly recovered (Infosys 11.9k → 20k; TCS offering 25k for FY27).

## 4. Recommended wording

**Entry level:**
> "India's IT firms have pulled up the bottom rung. Fresher intake at TCS, Infosys and HCLTech is about 65% below its FY22 peak. Across the sector, the number of salaried graduates aged 21–25 working in IT has been flat at about 1.0–1.15m since 2022-23, while salaried jobs for that age group grew by about a third. So IT's share fell from about 20% to about 16% (PLFS, MoSPI; the 2025 redesign makes the last step uncertain). Real pay for 21–25-year-olds in IT fell about 12% in 2025, while pay for over-30s held. Economy-wide fresher postings are back at their 2022 level, but that recovery is outside IT; IT postings remain about 30% below 2022."

**Graduate unemployment:**
> "Unemployment among young graduates is high but not rising. In PLFS 2023-24 (MoSPI), 37–41% of graduates aged 15–25 in the labour force were unemployed on the principal-status and weekly measures (34% on the official ps+ss measure); State of Working India 2026 puts it near 40%. The rate has fallen since 2017-18 (from 46–48%). The further 2025 fall shows up only on usual status (28% for ages 21–25), not on the weekly measure (39%), so we don't rely on it."

## 5. Which numbers we can reproduce

- **We reproduce, so use our numbers:** all of Future of India's shares and earnings figures; their levels, but only after their rescaling, so use our unscaled levels instead; State of Working India's 40% and 20%, within a range; their 20–29 unemployed ratio.
- **We must cite:** Future of India's labour share of value added; State of Working India's CMIE transition figures, including the 7%; Naukri's fresher figures, labelled as postings across all industries.
- **Don't cite:** LinkedIn's +168% as an entry-level hiring figure.

PLFS source for all of the above: Periodic Labour Force Survey unit-level data, 2017-18 to CY2025, NSO, MoSPI. The data agreement requires sending MoSPI a copy of any publication.

Sources: [Future of India](https://foifaction.substack.com/p/it-sector-helped-build-the-indian), [SWI 2026 page](https://azimpremjiuniversity.edu.in/publications/2026/report/swi-2026), [The Wire](https://m.thewire.in/article/economy/nearly-40-of-indian-graduates-under-the-age-of-25-are-unemployed-azim-premji-report), [Naukri Jan 2026](https://www.naukri.com/blog/naukri-jobspeak-white-collar-hiring-opens-2026-with-3-yoy-growth-driven-by-non-it-sectors-and-fresher-hiring/amp), [Naukri Feb 2026](https://naukri.com/blog/naukri-jobspeak-it-hiring-shows-meaningful-recovery-and-ai-momentum-continues-white-collar-market-posts-12-yoy-growth-in-february-2026/), [Storyboard18](https://www.storyboard18.com/how-it-works/indias-white-collar-hiring-up-3-yoy-in-january-bpo-ites-leads-with-21-growth-naukri-88655.htm), [People Matters/LinkedIn](https://peoplematters.in/news/strategic-hr/entry-level-hiring-climbs-168percent-as-ai-roles-and-internships-gain-ground-linkedin-49290), [Tripura Star News/LinkedIn](https://www.tripurastarnews.com/ai-specialist-content-creator-among-fastest-growing-roles-for-fresh-graduates-in-india-linkedin/), [RBI Handbook CPI table](https://rbi.org.in/scripts/PublicationsView.aspx?id=23859).
