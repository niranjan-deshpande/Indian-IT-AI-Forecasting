## FINDINGS_jobs.md

### Bottom line

1. **Nasscom, ICRIER and Goldman/World Bank vs PLFS: mostly different measures; where they overlap, they agree within sampling error.**
   - PLFS NIC 62+63, 2022-23 → CY2025 (about 2.5 years): +4.1% (90% CI −7.0% to +15.2%), or +1.6% a year (−2.8 to +6.1).
   - Nasscom's chained +6.1% over FY23–26 is about +4.9% over the same 2.5 years, almost exactly the PLFS point estimate.
   - Neither "sector employment is flat" nor "sector employment grows about 2% a year" is established. The honest claim is "slow growth at most".
2. **ICRIER's "employment continued to grow" is right, but for 2021-22 → 2023-24.** It comes from ICRIER's own PLFS tabulation, not its survey, and reproduces our numbers. It stops before our flat stretch.
3. **The Goldman figures (via the World Bank) are not like-for-like.** The −64k is right. The +700k most likely mixes two Nasscom vintages; about 0.24m of it is Nasscom adding GCCs to its count. Like-for-like the rest of the sector grew about +0.39m. Even at face value, +700k is inside the PLFS CI (z ≈ 0.8).
4. **The big-firm claim holds, with a recent uptick.**
   - Top six at end-March: 1,679,489 (FY23), 1,605,986 (FY24), 1,621,361 (FY25), 1,618,023 (FY26).
   - Q2 FY27 for the four firms that have reported: +9,438 (TCS +4,258, HCLTech +6,450, TechM +5,446, Wipro −6,716).
   - The IANS and Computerworld tallies match our panel to within 0.03% of headcount.

### 1. Sector employment: Nasscom, ICRIER and Goldman vs PLFS

#### 1a. What each source measures

| | PLFS NIC 62+63 (our series) | Nasscom "direct employment" | Top-6 headcount |
|--|--|--|--|
| Unit | Persons in Indian households whose usual principal activity is in NIC 62 (programming, consultancy) or 63 (data processing, hosting, portals) | Industry-body estimate of India-based technology-industry employees | Global employees of six firms |
| BPM | Mostly not: call centres are NIC 822, other BPO is NIC 82 | Yes | Partly (the firms' BPS arms) |
| ER&D | Only if coded to 62; engineering services are NIC 71 or the manufacturer's industry | Yes | Yes |
| GCCs | Only if the respondent names the activity as IT; a bank's GCC employee can be coded to NIC 64 | Yes. The FY24 restatement from 5.43m to about 5.68m equals Nasscom-Zinnov's +0.24m GCC revision | No |
| Self-employed, small domestic firms | Yes (about 10% are not regular salaried) | Partly | No |
| Timing | Jul–Jun rounds to 2023-24, then calendar years; CY2025 is centred on mid-2025 | End-March stock. FY26 was published 24 Feb 2026, so it is partly a projection | Quarter-end stock |
| Method | Probability sample, about 4,470 respondents in CY2025; CY2025 is a new survey design | Member surveys, filings and Zinnov GCC counts; method not public; levels revised each edition | Company filings |

The levels (PLFS 5.70m in CY2025, Nasscom 5.95m in FY26) are similar largely by coincidence. Compare growth rates, not levels.

#### 1b. Is ~2% a year compatible with PLFS? Yes. So is zero.

Changes are log changes, with 90% CIs; the two rounds are treated as independent samples. Full table in `plfs_change_ci.csv`.

| PLFS series | window | change | 90% CI |
|--|--|--|--|
| NIC 62+63 | 2022-23 → CY2025 | +227k (+4.1%); +1.6%/yr | −389k to +843k; −2.8 to +6.1%/yr |
| NIC 62+63 | 2023-24 → CY2025 | −274k (−4.7%) | −1,090k to +543k |
| NIC 62+63 | 2021-22 → 2023-24 | +1,393k (+26.5%) | +600k to +2,185k |
| NIC 62 | 2022-23 → CY2025 | +17k (+0.4%) | −581k to +615k |
| NIC 63 | 2022-23 → CY2025 | +210k (+24.1%) | +67k to +354k (crosses the CY2025 design break) |
| ICT occupations outside NIC 62–63 | 2022-23 → CY2025 | +188k (326k → 515k) | +80k to +297k |
| 62+63 plus ICT occupations outside | 2022-23 → CY2025 | +415k (+6.9%); +2.8%/yr | −210k to +1,041k |

| Benchmark, scaled to the 2.5-year window | z vs PLFS +4.1% |
|--|--|
| Flat (0%) | −0.61 |
| Nasscom +6.1% FY23–26 (+4.9%) | +0.12 |
| Goldman/World Bank net +636k on 5.4m (+9.3%) | +0.77 |

None is rejected.
- The CY2025 design break means these CIs understate the true uncertainty.
- 2023-24 is inflated by one high-weight sampling unit, so start comparisons from 2022-23.
- **ICT workers outside NIC 62/63 rose significantly (about +190k).** Host industries are software publishing (58), telecom (61), finance (64), engineering (71) and manufacturing. That fits GCC staff being coded to their parent's industry. On the broader definition, PLFS grows about 2.8% a year, close to Nasscom.

#### 1c. ICRIER (Feb 2026), confirmed

- The claim rests on Section 7 (pp.32–33), ICRIER's own PLFS tabulation, not the 651-firm survey. The survey gives only shares of firms; its entry-level result is 55% of firms down vs 35% up.

| | ICRIER | ours |
|--|--|--|
| NIC 62, 2021-22 | 3.8m | 3.818m |
| NIC 62, 2023-24 | 5.2m | 5.179m |
| NIC 63, 2021-22 | 731k | 766k |
| NIC 63, 2023-24 | 809,761 | 797k |
| 62+63, 2021-22 | about 4.53m | 4.583m |
| 62+63, 2023-24 | about 5.99m | 5.976m |

- Levels reconcile within about 1%. The NIC 63 gaps are probably a different weighting or status convention; I didn't test this.
- Their window is the boom tail, where we also find a significant +26.5%. It ends at the inflated 2023-24 peak.
- **Verdict:** not a contradiction. The change since 2022-23 is not significant.

#### 1d. Nasscom FY26 (+135k, +2.3%, 5.95m)

- Plausible as a statement about the whole industry including GCCs and BPM.
- With the top six at −3.3k in FY26, the rest added about +138k (+3.3%). That fits our evidence: GCC tech jobs about +260k over FY23–26 (+385k all functions), and the 21 other listed firms +18.6% (+13.9% excluding acquisitions).
- Weaknesses: published before year-end, revised every year, no sampling error, and not independent of the Zinnov GCC count.
- **Verdict:** compatible with PLFS; treat as "about 2% a year, unverified". Nasscom itself reports revenue +6.1% against jobs +2.3%, which supports "jobs lag output".

#### 1e. Goldman via the World Bank: −64k / +700k / 4.4m

- **Source:** World Bank India Development Update, 13 Oct 2026, p.41, citing Goldman Sachs, "Gen-AI in India: Jobs Crosswinds, Productivity Tailwinds" (July 2026, client-only).
  - The World Bank text: the six largest firms "reduced employment by approximately 64,000 workers from a combined workforce of 1.7 million"; the rest of the sector, including GCCs, "added around 700,000 workers over the past three years, bringing employment to approximately 4.4 million".
  - Goldman's press coverage gives no numbers. Cite the World Bank, attributing the figures to Goldman.
- **−64k:** our panel gives −63,557 for Dec 2022 → Dec 2025 (exactly three years). FY23 → FY26 gives −61,466; peak → Mar 2026 gives −76,165. **Correct.**
- **+700k to 4.4m:** this needs a start of about 3.7m. My reconstruction (inference; Goldman's workings aren't public):
  - Nasscom FY23 in its old vintage (about 5.37m) minus the top six (1.68m) = 3.69m.
  - Nasscom FY26 in its 2026 vintage (5.95m) minus the top six (1.62m) = 4.33m, roughly 4.4m.
  - About 0.24m of that gap is Nasscom's FY24 GCC coverage restatement, not hiring.
  - Chained within vintages, the rest of the sector rose about **+0.39m (+10.6%, ~3.4% a year)**.
  - Top-six headcount is global while Nasscom is India-only. That understates the residual's level, but barely its change.
- **Against our GCC reconciliation:** +0.39m fits GCCs (+0.26m tech, +0.385m all functions) plus mid-tier firms. +0.70m would need about +0.3m more from other firms; our 21-firm listed panel added only about +63k.
- **Against PLFS:** +9.3% over 2.5 years vs +4.1% (CI −7.0 to +15.2), z = 0.77. Compatible, but well above the point estimate. Much of it would be BPM and ER&D jobs that PLFS puts outside 62+63 anyway.
- **Verdict:** −64k correct; +700k overstated as hiring; about +0.4m is the like-for-like figure. The World Bank's conclusion ("headcount rationalization within some large firms rather than a generalized contraction") fits our claim if we say "stopped adding", not "shrinking sector".

### 2. Firm update: Q2 FY27 (quarter to 30 Sep 2026)

- **Reported:** TCS (8 Oct), HCLTech (12 Oct), Wipro (15 Oct), TechM (15 Oct).
- **Pending:** LTM (16 Oct), Infosys (23 Oct), Cognizant (late Oct).
- Accenture's Jun–Aug 2026 quarter (814k, cc +7%) is already in the canonical file.

| firm | headcount | QoQ net | YoY net | USD rev ($m) | USD YoY | cc YoY | LTM attrition | utilization |
|--|--|--|--|--|--|--|--|--|
| TCS* | 598,056 | +4,258 | +4,742 | 7,642 | +2.4% | +2.8% | 13.3% | n/a |
| HCLTech | 230,339 | +6,450 (6,136 freshers) | +3,699 | 3,724 | +2.2% | +2.6% (services +4.0%) | 12.8% | n/a |
| Wipro | 236,328 | −6,716 | +836 | 2,611.5 (IT Services) | +0.3% | +0.6% | 13.8% | 83.4% excl. trainees |
| TechM | 152,206 | +5,446 | −508 | 1,693.4 | +6.8% | +7.2% | 11.7% | 88.9% incl. trainees |
| **Four firms** | 1,216,929 | **+9,438** | **+8,769 (+0.7%)** | | | | | |

\* TCS is from the fact sheet as shown in search results, not downloaded (tcs.com blocks scripts). Its figures are internally consistent: 593,798 + 4,258 = 598,056, and USD revenue matches +0.2% QoQ and +2.4% YoY against the panel.

- With Infosys and LTM held at June levels, the top six are about 1.633m at Sep 2026. That is the highest since mid-2023, but −46.6k (−2.8%) against March 2023.
- **Correction to our literature note:** TCS is +4.7k year on year, not "15k below a year earlier". The −15k compares with June 2025 (613,069).

#### 2a. Press tallies vs our panel

- **IANS: top five −7,389 in FY26, +12,718 in FY25.**
  - We get −6,981 for FY26 and exactly +12,718 for FY25.
  - All five Q4 FY26 firm figures match: TCS +2,356, Infosys −8,440, HCLTech +802, Wipro +135, TechM −1,993.
  - Our per-firm FY26 changes: TCS −23,460, Infosys +5,016, HCLTech +3,761, Wipro +8,810, TechM −1,108. I couldn't pin the 408 gap to one firm; it sits somewhere in Q1–Q3.
  - **Verdict:** matches.
- **Computerworld / Constellation: +17 in 9M FY26, +17,764 in 9M FY25.**
  - We get +159 for Apr–Dec 2025.
  - For 9M FY25 we get +10,372, or +17,770 with HCLTech's 7,398 divested staff added back. So Constellation adjusted for the divestiture and we do not; both are defensible.
  - **Verdict:** matches in substance. Cite it as "roughly zero".

#### 2b. Does TCS change "big firms stopped adding jobs"?

No, but acknowledge it.
- TCS's three straight additions (+2,356, +9,279, +4,258) follow a −30,906 drop over Jun–Dec 2025. It is +0.8% year on year and −18.1k (−2.9%) below its Sep 2022 peak.
- The Q2 pickup is led by freshers (HCLTech onboarded 6,136), and Wipro shrank by 6.7k, so this is not broad-based hiring.
- Two quarters of about +0.5% each is too short to call a turn. Revenue growth is 0.6–7% cc, and HCLTech guides 2.5–4% for FY27.
- **Wording:** "have not added jobs in net terms since FY23 (FY23 → FY26: −3.7%), with a small pickup in H1 FY27."

### 3. Recommended wording

Long form:
> Output is still growing, but jobs are not keeping pace. The six largest IT firms employ fewer people than in March 2023 (1.62m vs 1.68m in March 2026, −3.7%) and have been roughly flat since early 2024; the first half of FY27 brought a small pickup (about +1%, mainly freshers at TCS and HCLTech), not a return to the pre-2022 pace. Employment in the wider industry is growing slowly at best. Industry estimates put it at about 2% a year in FY24–26, mostly in GCCs and mid-sized firms, against revenue growth of about 6%. The official labour-force survey shows no statistically significant change in IT-industry employment since 2022-23 (5.5m to 5.7m in NIC 62–63; 90% CI −0.4m to +0.8m), which is consistent with either zero or about 2% a year. The entry rung is where hiring has fallen most.

Short form:
> Revenue up, big-firm headcount down 4% from FY23 and only now edging up; sector-wide jobs growing at most about 2% a year, much more slowly than output.

Do not say:
- "Sector employment is flat." PLFS can't show it, and can't rule out about 2–3% a year.
- "The sector stopped adding jobs."
- "Goldman: the rest of the sector added 700k." It is probably inflated by Nasscom's GCC restatement.

### Sources

- **TCS:** fact sheet https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2026-27/q2/Presentations/Q2%202026-27%20Fact%20Sheet.pdf; cross-check https://www.businesstoday.in/markets/stocks/story/tcs-adds-4258-employees-in-q2-marks-third-quarter-of-headcount-addition-560460-2026-10-08
- **HCLTech:** https://nsearchives.nseindia.com/corporate/HCLTECH_12102026170757_InvestorRelease_5.pdf
- **Wipro:** https://www.wipro.com/content/dam/nexus/en/investor/quarterly-results/2026-2027/q2fy27/datasheet-q2fy27.pdf
- **TechM:** https://insights.techmahindra.com/investors/tml-q2-fy-27-press-release.pdf and datasheet
- **Report dates:** NSE announcement data in `raw/nse/`
- **IANS:** https://ianslive.in/top-it-firms-hiring-turns-negative-as-headcount-falls-over-7000-in-fy26--20260425104000
- **Computerworld:** https://www.computerworld.com/article/4119064/ai-boom-hiring-bust-indian-it-firms-add-just-17-net-employees-in-nine-months.html
- **Nasscom:** https://www.businesstoday.in/amp/latest/corporate/story/it-industry-likely-to-hire-135000-employees-in-fy26-projects-nasscom-517760-2026-02-24
- **ICRIER:** https://www.icrier.org/pdf/AI-and-Jobs.pdf (Section 7)
- **World Bank:** https://documents.worldbank.org/curated/en/099455510022634209/pdf/IDU-26df18db-fc2b-4e0b-91ed-be8ced3d9bce.pdf (p.41)
- **Goldman press (qualitative only):** https://www.businesstoday.in/markets/stocks/story/goldman-sachs-pushes-back-on-short-ai-india-narrative-says-report-42-stocks-in-focus-559148-2026-10-01
- **PLFS (MoSPI) unit data**, aggregate only, in `data/explore/round3/plfs/`. Cite MoSPI and send it a copy of any publication.

### Open

- Fetch the TCS fact sheet by hand: tcs.com blocks scripts and the NSE copy of the press release truncates at 128 KB.
- Nasscom's estimation method: the search budget ran out before I found a methodology note.
- The IANS 408-person gap can't be pinned to one firm.
- Add Infosys, LTM and Cognizant rows once they report.

---

Files are in `/Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/0. Exploratory Analysis/data/explore/health_check/contradictions/`:
- `q2fy27_update.csv`
- `plfs_change_ci.csv`
- `raw/` (NSE filings, Wipro, TechM, World Bank and ICRIER downloads)
