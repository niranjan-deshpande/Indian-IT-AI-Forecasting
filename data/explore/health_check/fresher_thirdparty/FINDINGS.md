# Third-party fresher hiring estimates for Indian IT

Compiled 15 Oct 2026. Data file: `fresher_thirdparty_long.csv` (565 rows, one row per number per source). 185 rows come from the publisher's own page or PDF ("primary") and 380 from press reports. 563 rows were checked against the page text. 2 rows (`verified=no`) were seen only in search-engine summaries. Each row records the series, value (with low/high for ranges), unit, period, publisher, report name, publication date, outlet, URL read, a short exact quote, a method note and caveats. `value_is_derived=TRUE` marks the few values that are arithmetic on a stated figure, e.g. "almost double 225K" or "2,000 a quarter".

**Bottom line.** No third-party source publishes a documented, reproducible count of sector-wide fresher intake. The numbers are estimates by staffing firms, quoted in the press with no method attached. They agree that the FY22 peak was 2–3× today's level. They do not agree on the size of the peak (400–600k), and the figures for a given year move between vintages. Our own firm-level numbers are better documented and tell the same story. The third-party figures are most useful for three things: scaling up from our firms to the whole sector, showing the FY24 trough, and the monthly opening counts.

## 1. What exists

### Xpheno (308 rows)

**Annual fresher intake.** No report from Xpheno itself is reachable: xpheno.com does not resolve and is not archived. All the annual figures are press quotes.

| FY | Value | As quoted in | Kind |
|--|--|--|--|
| 2010 | ~225k ("best year so far") | TOI, 21 Feb 2022 | estimate |
| pre-COVID | ~200k a year | Business Standard (BS), 16 Jun 2024 and 21 Sep 2024 | context; attribution to Xpheno ambiguous |
| FY22 | "almost double" 225k, so ~450k | TOI, 21 Feb 2022 | projection made in-year (derived) |
| FY22 | **600k** | Business Today (BT), 21 Mar 2026; ThePrint, 8 Oct 2026 | reported actual |
| FY23 | ~500k ("almost half a million") | TOI, Feb 2022 | projection; no actual ever quoted |
| FY24 | **60–70k**, "lowest in two decades" | BS, 16 Jun 2024; BS, 21 Sep 2024; Forbes India ("about 70,000"), 1 Oct 2024 | actual |
| FY25 | 150k ("moderate"); then 100–120k | Communications Today, Apr 2024; Jul 2024; Forbes India, Oct 2024 | projections |
| FY25 | 60–70k for *IT services companies only* | Forbes India, Oct 2024 | projection |
| FY25 | **~120k** (−80% from peak) | BT, 21 Mar 2026 | actual |
| FY26 | "only marginally higher" than FY25 | BT, 21 Mar 2026 | no number |
| FY23 to Mar 2026 | 595k cumulative | ThePrint student op-ed, 8 Oct 2026 | unclear start point |

- **The FY22 figure has drifted up from 450k to 600k.** In Feb 2022, Karanth projected FY22 at "almost double" the 2010 peak of 225k, which is about 450k. From 2026 the same peak is quoted as 600k. That is 33% higher, and no revision was explained. Only BT and ThePrint give 600k, and ThePrint is a student column. No source gives a FY22 actual between those dates. Treat 450–600k as Xpheno's range.
- **FY24 at 60–70k and FY25 at about 120k imply a trough in FY24 followed by a near-doubling.** This matches what Xpheno projected in Jul 2024 ("100% YoY growth", 100–120k). The FY24 value is very low against our firm data. Infosys (11.9k) plus HCL (12.1k) already make 24k. If TCS did anything near its reported ~40k FY24 plan, three firms alone would cover the whole Xpheno total. Either the FY24 estimate is too low, or TCS's FY24 intake was far below 40k. We have no TCS FY24 figure.
- **The cumulative figure checks out roughly.** If 595k covers FY23 to FY26, then with FY24 ≈ 65k, FY25 ≈ 120k and FY26 ≈ 130–140k, FY23 comes to about 250–280k. That is close to TeamLease Digital's 230k for FY23 (below). This is a rough check on a weak source.
- **The "600k to 140k" quote is a conflation.** ET (23 Aug 2026) wrote that Xpheno estimates "net hiring in the IT sector fell from around 600,000 in FY22 to 140,000 in FY26", and our literature note repeats it. The 600k matches Xpheno's *fresher-intake* peak, not net hiring. Nasscom's FY22 net addition was about 230k, and BS (20 May 2026) quotes Xpheno's own IT net headcount addition for FY26 as 110k. So 600k → 140k is best read as gross fresher intake, wrongly labelled "net hiring". On that reading, 140k is the only explicit Xpheno-attributed FY26 number. It is consistent with "marginally higher than ~120k". It is still second-hand, so don't use it as a net-hiring series.
- **Net headcount additions, IT vs GCC (BS, 20 May 2026).** IT: 50k (FY24), 100k (FY25), 110k (FY26). GCC: 60k, 110k, 200k. The GCC FY25 figure was quoted as 140k in BS articles of Mar and Dec 2025, then as 110k in May 2026: a silent revision. The FY26 GCC projection was 180k; the actual came in at 200k. Separately, the top-8 IT firms' headcount was −75k year on year to Dec 2023 (ET, Feb 2024).

**Monthly Active Tech Jobs Outlook.** These are counts of openings that employers post themselves (career pages, official social pages, direct postings on job boards), active in a 4-week window, excluding postings by agencies. They are openings, not hires.

- Total: 262k (Jan 2022) → 102–107k (early 2024) → 136k (Jan 2025) → 102–105k (Sep–Dec 2025) → 93k (Jun 2026, a 28-month low) → 117k (Sep 2026) → 120–123k (Oct 2026, an 18-month high, +17% YoY).
- Entry-level (0–2 years): 18k (Jun 2025), 14–15k for most of 2025–26, 10k (Jun 2026, −44% YoY), 15k (Oct 2026, +15% YoY).
- **Entry-level share of openings (my calc): 16.1% (Jun 2025) → 13–14% → 10.8% (Jun 2026) → 12.2% (Oct 2026).** Xpheno itself said "barely 14%" in Apr 2026.
- IT services openings: 52k (Jun 2025) → 36k (Jun 2026) → 66k (Oct 2026, +57% YoY). GCC openings: 11–19k.
- The levels agree across outlets within each month. The only clash is Oct 2026 total, quoted as 120k and 123k (early-month vs full-month snapshot), plus one Sep 2026 GCC conflict (13k vs 18k).

### TeamLease (108 rows; 66 primary, mostly the report PDFs)

**EdTech Career Outlook, half-yearly.** The metric is the % of surveyed employers intending to hire freshers (0–1 year) in the next six months. Sample sizes are 377–1,097 employers in about 18 sectors and 14 cities.

| Half-year | IT intent | All sectors | n |
|--|--|--|--|
| Feb–Apr 2021 | 24 | 15 | 815 |
| 2021 H2 | 31 | 17 | 661 |
| 2022 H1 | 57 | 47 | 829 |
| 2022 H2 | 65 | 59 | 865 |
| 2023 H1 | 67 | 62 | 874 |
| 2023 H2 | 49 | 65 | 737 |
| 2024 H1 | 42 | 68 | 377 |
| 2024 H2 | 45 | 72 | 603 |
| 2025 H1 | 59 | 74 | 649 |
| 2025 H2 | 75 | 70 | 1,065 |
| 2026 H1 | 81 | 73 | 1,051 |
| 2026 H2 | 76 | 75 | 1,097 |

- IT ran above the all-sector average through 2023 H1. It then fell below it (42–45% in 2024), and rebounded to 75–81% in 2025–26.
- **There is a series break at the 2025 H2 edition.** The sample jumps from about 650 to about 1,065. Sector values leap (Marketing 11% → 67%, Retail 50% → 87%) while the headline value falls. The report puts this down to more small organisations in the sample. The IT jump from 59 to 75 therefore cannot be read as a change in demand. Only within-regime comparisons are safe:
  - 2021–2025 H1: IT fell from 67 to 42 and then recovered to 59.
  - 2025 H2 to 2026 H2: IT went 75 → 81 → 76, and IT dropped out of the top-3 sectors.
- **Quality:** a stated-intent survey, an unweighted share of firms (a 50-person firm counts the same as TCS), changing samples, and no volumes. It is useful for direction within a regime only.

**TeamLease Digital, absolute fresher hires (all press).**
- FY23: 230k (actual). FY24: 155k (projection, BT Dec 2023). FY25: 85–95k ("tech services", Outlook Business Mar 2025).
- 800k cumulative over FY22–23 (BT). If FY23 was 230k, that implies FY22 ≈ 570k, close to Xpheno's 600k.
- A blog table credited to TeamLease Digital (390k, 230k, 155k, 90k, 150k for FY22–FY26) mixes projections with actuals, and its FY22 contradicts the 800k figure. It is kept in the file but flagged low quality.
- The FY25 range of 85–95k is about equal to the top-6 firms' own reported fresher hires (86k, below). As a sector total it is implausible; it probably means large tech-services firms only.

### Other HR firms and Nasscom

- **HAN Digital (ET, 14 Oct 2026; IT-BPM including GCCs and BPO).** About 400k (FY22) → 175k (FY26, estimate), and "up to" 210k in FY27 (+20%). IT services would make up about 60% of FY27 hires and GCCs 28%. This is the most recent sector estimate and the only one with an FY27 projection. Its FY22 figure (400k) sits a third below Xpheno's 600k, and its scope is wider.
- **UnearthInsight (press).**
  - FY26: global IT services firms (Accenture, Capgemini, Cognizant) hiring 160–180k freshers in India; GCCs 25–30% of fresher hiring.
  - BS, Dec 2025: IT services net additions of "up to 35k" in FY26 and GCC net additions of 130–150k. This clashes with Xpheno's IT net figure of 110k for the same year.
- **Nasscom.** Publishes net additions only, never a fresher count:
  - FY22: 230k. FY23: 60k (Forbes India) or 270k (NDTV Profit via Communications Today); the sources conflict. FY24: 60k.
  - FY25: 126k, revised to 133k. FY26: 135k (+2.3%; "a large portion driven by GCCs").
  - Nasscom officials said campus hiring "has come down significantly" without giving a number.
- **CIEL HR and Quess:** no IT fresher numbers found. **Careernet:** campus hiring 30–35% below historical averages (mid-2026).

### Portals (all industries unless stated)

- **foundit fresher (0–3 years) postings, YoY:**
  - 2025: +26 (Feb), +13 to +17 (Oct–Dec).
  - 2026: +13 (Jan), +5 (Feb), then **negative from March**: −2, −2, −2, −6, −10 (Jul).
  - IT-industry share of fresher postings: 32% (Jul 2025) → 24% (Jul 2026). The CEO said "one in four entry-level IT jobs has disappeared".
  - GCC share of fresher postings: 8% → 11%. AI roles: 4% of fresher postings.
- **Naukri JobSpeak 0–3 years, YoY:** +16 (Mar 2026), +11, +7, +8, +15 (Aug), +1 (Sep). It stays positive throughout.
- **The two portals diverge from March 2026.** foundit's fresher postings turned negative while Naukri's 0–3 band stayed at +7 to +16 until September. The gap is about 15–25 points a month. Both cover all industries, both count postings, and neither covers campus hiring. Naukri is larger, and foundit's figures are rounded. The September Naukri reading (+1, with IT-Software −4) is the first sign of convergence.
- Most Naukri values are already in `workforce/jobspeak_expband_yoy_2025_26_chart.csv`. The new values here are the press-reported months that confirm them.

### Company-announced targets (42 rows)

| Firm | FY26 target → actual | FY27 target | FY27 so far |
|--|--|--|--|
| TCS | — → 44k | **25k offers** made (CEO to PTI, Apr 2026) | H1 ≈ 24k onboarded (14k Q1 + 10k Q2; low-tier outlets) |
| Infosys | 20k → 20k+ | **20k**, repeated on the Q4 FY26 and Q1 FY27 calls (primary SEC 6-K transcripts) | >4k in Q1 |
| Wipro | 10–12k, cut to 7.5–8k in Jan 2026 → 7.5k | **none** ("completely on demand") | Q1: reportedly 0 (single weak source) |
| HCLTech | ~8k (2k a quarter; derived) → 11.7k | **none disclosed** | H1 7.2k, flat vs H1 FY26 |
| Cognizant (calendar year) | CY25 20k → ~20k | CY26 24–25k (Feb), **cut to 20k** (Jul) | — |
| LTIMindtree | 5k → 6.7k | none found | — |
| TechM | 6k/yr (FY25) → 950 (FY26) | none found | — |

- All management-stated actuals match `fresher_hires_annual_best.csv`: TCS 44k, Infosys 20k, HCL 11,744, LTIM above target, TCS FY25 42k vs a 40k target.
- **Newly found:** Wipro FY25 about 10k and FY26 7.5k. Our file has Wipro only for FY23.
- The TCS "~20,000" figure in circulation is Q2 FY23 joiners, not an annual target.
- The Wipro guidance cut was announced 16–17 Jan 2026, not in March.
- **The FY27 targets that are stated sum to about 65k** (TCS 25k + Infosys 20k + Cognizant 20k). FY26 actuals for the same three firms were about 84k.

## 2. Comparison with our firm-level data

Top-6 sum = TCS + Infosys + HCL + Wipro + TechM + LTIM. It uses `fresher_hires_annual_best.csv` plus the Wipro FY25 and FY26 figures found here (10k and 7.5k).

| FY | TCS+Infy+HCL | Top-6 | Sector estimate | Top-6 as % of sector |
|--|--|--|--|--|
| FY22 | 218k | 238k (no Wipro) | Xpheno 600k (450k in 2022); HAN 400k; TeamLease Digital ≈570k implied | 40% (Xpheno), 59% (HAN) |
| FY23 | 121k | 143k | TeamLease Digital 230k | 62% |
| FY24 | (TCS missing) | ≥24k | Xpheno 60–70k | ≥37%; ~100% if TCS hit 40k |
| FY25 | 65k | 86k | Xpheno ~120k; TeamLease Digital 85–95k | 72% (Xpheno) |
| FY26 | 76k | 91k | HAN 175k (IT-BPM); Xpheno ~"marginally above 120k" / 140k (ET) | 52% (HAN), 65% (Xpheno 140k) |

- **Direction agrees.** From peak to FY25/26:
  - Our top-3: −70% to FY25 and −65% to FY26.
  - Xpheno: −80% to FY25.
  - HAN: −56% to FY26.
  - All sources put FY24 or FY25 as the trough and show a partial rebound after it.
- **The big firms' share of sector intake roughly rose from FY22 to FY25** (40–59% to about 65–72%). Smaller firms cut freshers proportionally more after the boom, or the third-party peak figures are inflated. Either way, our firm data probably *understates* the sector-wide fall from peak and *overstates* the rebound.
- **Sector scaling factor:** sector intake ≈ 1.5–2.0× the top-6 in FY25–26, and 1.7–2.5× in FY22. A sector line can be drawn as top-6 × ~1.7 with a band. The third-party points can serve as the check.

## 3. What contradicts or qualifies the working claim

Working claim: output still growing, big firms stopped adding jobs, sector job growth slow, entry-level rung narrowing.

**These sources support it:**
- The level of fresher intake is 55–80% below FY22 on every source.
- The entry-level share of tech openings fell from 16% (mid-2025) to 11–12% (mid-to-late 2026).
- foundit's fresher postings have been negative since March 2026, and IT's share of fresher postings fell from 32% to 24%.
- FY27 targets are lower or withdrawn: TCS 25k offers vs 44k hired in FY26; Wipro and HCL have none; Cognizant cut to 20k; Infosys is flat at 20k.
- Nasscom's FY26 net addition was +2.3%, mostly at GCCs.

**These sources cut against it:**
1. **The sector fresher series is not still narrowing. It bottomed in FY24 and has risen since.** Xpheno: 65k → 120k → "marginally higher". HAN projects up to +20% for FY27. TeamLease IT intent recovered within both survey regimes up to 2026 H1. Infosys and HCL H1 FY27 intake is flat year on year. "Narrowing" is accurate for FY22 → FY24. For FY24 → FY26 the honest wording is "partial recovery, to well below the peak".
2. **Xpheno puts IT-sector net headcount additions rising, from 50k (FY24) to 100k (FY25) to 110k (FY26).** IANS has the top-5 firms at −7.4k in FY26. If both hold, the non-top-5 IT firms added more than 100k. That fits "big firms stopped adding jobs", but it weakens "sector job growth slow" if "sector" means IT services broadly. UnearthInsight's "up to 35k" contradicts Xpheno here, so the size of IT-services net adds in FY26 is genuinely uncertain (35–110k).
3. **The Naukri 0–3 band has been positive every month of 2026** (to +1 in September), and Xpheno's Oct 2026 tech openings were at an 18-month high, with IT services +57% YoY and entry-level +15% YoY. The narrowing shows up as a *share* (entry-level share of openings, IT share of fresher postings), not as a falling count.

## 4. Candidate charts

1. **Sector fresher intake vs our big-firm fresher hires, FY19–FY27.**
   - Bars: TCS + Infosys + HCL and the top-6 (`workforce/fresher_hires_annual_best.csv`, plus the Wipro FY25/26 rows here).
   - Dots: `xpheno_it_fresher_intake` (FY22 shown at both 450k and 600k with a connector, FY24 range bar, FY25), `han_digital_it_bpm_fresher_hiring` (FY22, FY26, FY27 "up to" as a hollow dot), and `teamlease_digital_it_fresher_hires` (FY23 and the FY25 range; projections hollow).
   - Message: everyone agrees on the collapse, the FY22 peak itself is uncertain, and there has been a partial rebound since FY24.
2. **Entry-level share of active tech openings, monthly, Jun 2025–Oct 2026.**
   - Use `xpheno_entry_level_tech_openings_0_2y` ÷ `xpheno_active_tech_openings`, with total openings on a second panel.
   - Message: total openings recovered to an 18-month high while the entry share slid from 16% to 12%. The rung is narrowing in share, not count.
3. **Two portals and one survey disagree (small multiples).**
   - (a) foundit fresher postings YoY vs Naukri 0–3 YoY, Jan 2025–Sep 2026, showing the divergence from March 2026.
   - (b) TeamLease IT vs all-sector fresher intent, 2021–2026 half-years, with a break marker at 2025 H2.
   - Message: high-frequency fresher indicators are noisy and conflicting. Lean on the annual firm data.

An alternative to chart 3 is a **FY27 targets vs FY26 actuals** dumbbell for TCS, Infosys, Wipro, HCL and Cognizant, with "no target" shown as an open marker.

## 5. Caveats on using these sources

- **Staffing-firm figures (Xpheno, TeamLease Digital, HAN, UnearthInsight)** have no published method or scope (IT services vs IT-BPM vs "tech"), and are quoted second-hand. Use them as order-of-magnitude checks, cite as "Xpheno, as reported in …", and show ranges.
- **Vintages move:** Xpheno FY22 450k → 600k; GCC FY25 140k → 110k; Nasscom FY25 126k → 133k. Always cite the date of the article.
- **Openings and postings are not hires,** and none of these sources includes campus offers. Portal series are all-industry unless the series name says IT.
- **Gaps:**
  - No Xpheno FY19–FY21 or FY23 actuals, and no explicit FY26 number other than the ET "140k".
  - No FY27 projection from Xpheno.
  - No CIEL HR or Quess IT fresher figures.
  - TCS FY24 and Wipro FY24 actuals are still missing. One source says Wipro onboarded 10k in FY24, but this is probably a mislabel of FY25.
  - Wipro's Q2 FY27 results (due today) and Infosys's Q2 FY27 (23 Oct) are not captured.
