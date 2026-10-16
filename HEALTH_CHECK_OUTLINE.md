# Health check of Indian IT services: outline (draft, 2026-10-15)

This is a tour of the evidence, not an argument.
- **Length:** about 1,700 words of prose (2,000 at most), not counting chart captions and collapsibles.
- **Charts:** about 24, plus one scorecard and one table.
- **Style:** the two-questions page. Left table of contents, hover footnotes, collapsible appendix, Plotly charts built from repo CSVs, and a number-check script.
- **Data:** chart sources sit under `data/explore/` unless the path says otherwise.
- **Checks:** every number gets checked against the data before publishing.

---

## The synthesis (what the piece should leave a reader believing)

1. **Bigger, but no longer broader.**
   - The sector still grows its output.
     - RBI software exports: $221bn in FY26, +19% since FY23, about 6% a year in dollars.
     - India holds a steady ~30% of world computer-services exports.
   - The growth has left the six giants: their revenue grows 1–3% a year in constant currency, against ~9% before COVID.
   - It has gone to GCCs, mid-tier firms (+14% a year) and BPM.
2. **Jobs lag output.**
   - Top-six headcount is ~4% below FY23 and flat since FY24. H1 FY27 shows only a small uptick.
   - Sector-wide jobs grow at most ~2% a year. Nasscom +2.3% in FY26; PLFS shows no significant change since 2022-23.
   - Revenue per employee is rising.
3. **The bottom rung is a smaller share of a flat total.**
   - Fresher intake is 55–80% below the FY22 boom peak. It bottomed in FY24 and has partly recovered.
   - On every measure we have, IT's share of young entrants is falling: young salaried graduates, young EPFO entrants, entry-level openings, fresher postings.
   - Junior real pay fell in 2025.
4. **No sign of distress among those already employed.**
   - Attrition and utilisation are back to normal.
   - The labour share of value added is stable at ~0.7, and pay per head is rising.
   - Deal pipelines are steady and prices have not fallen.
5. **AI is mostly still ahead of us in the data.**
   - Measured AI price give-backs: ~0.4% in FY26, with ~1.5% expected in FY27.
   - AI talk on earnings calls has exploded.
   - Every outcome series predates the summer-2026 jump in coding agents. This is a baseline, not a verdict.

One-line frame: **"Still growing, no longer hiring like it used to, and the entry ramp is narrowing."**

---

## Structure

### 0. Title, dek, scorecard

- **Title (options):** "India's IT services in 2026: a health check" / "Growing, but not hiring" / "The ladder and the escalator".
- **Dek:** "Output keeps growing, jobs have stalled, and the bottom rung is getting narrower. A tour of 25-odd datasets."
- **Scorecard (table, colour-coded arrows).** Each row: indicator, latest value, change vs FY22/23, direction, source.

| Indicator | Latest | Change | Source |
|--|--|--|--|
| Software exports | $221bn FY26 | +8.2% y/y; +19% vs FY23 | RBI |
| India's share of world computer-services exports | ~30% ex-Ireland | flat | IMF |
| Top-6 constant-currency revenue growth | FY26 +0.6% | pre-COVID ~9% | — |
| Mid-tier revenue growth | FY26 +14% | — | — |
| Top-6 headcount | 1.62m | −4% vs FY23 | — |
| Sector employment, PLFS NIC 62–63 | 5.7m | flat since 2022-23, ±CI | — |
| Sector employment, Nasscom | 5.95m | +2.3% | Nasscom |
| Fresher hires at TCS + Infosys + HCL | 76k FY26 | vs 218k FY22 | — |
| IT share of young salaried graduates (21–25) | 16% | from 20% | PLFS |
| IT net payroll additions, ages 18–25 | — | −31% FY22–25 | EPFO |
| Real pay, IT, ages 21–25 | — | −12% in 2025 | PLFS |
| Attrition | 12–14% | normal | — |
| Labour share of value added | ~0.7 | flat | — |
| AI price give-back | 0.4% FY26 → ~1.5% FY27e | — | — |

### 1. Introduction (~180 words)

- **Why now:**
  - IT stocks sold off in Feb and May–Jun 2026.
  - Headlines contradict each other: "AI is killing Indian IT" vs "exports are booming".
  - The sector matters as a job ladder for educated Indians.
- **What we did:**
  - Assembled firm filings, RBI/BoP trade data, PLFS microdata, EPFO payroll, college placements, job postings, earnings calls and price data.
  - Checked the headline numbers others circulate.
- **The frame in three sentences** (from the synthesis).
- **A caveat up front:** nearly all data end in FY26/CY2025, before the mid-2026 step change in coding agents.
- Footnotes: scope (IT services incl. BPM and GCCs where stated), and PLFS/MoSPI attribution.

### 2. Output: still growing (~250 words, 5 charts)

Prose:
- Exports grew 7–8% a year in FY25–26, in dollars.
- FY26 growth came from IT services, not BPO.
- India is not losing work abroad.
- The six giants grew far more slowly than peers and smaller Indian firms. Accenture is back on its pre-COVID trend; the top six are ~18% below theirs.
- Footnotes:
  - Balance-of-payments data grow about twice as fast as the RBI survey.
  - Baldwin's "+27% above trend" and ING reproduce, but ~15 of Baldwin's 27 points predate ChatGPT.
  - The Economic Survey's 39.5% is a relative difference-in-differences estimate, not a growth rate.

Charts:
- **2.1 Software exports, FY19–FY26** (stacked public-limited vs private-limited exporters).
  - Data: `round3/sector_aggregates/exports_recomputed.csv`, `trade/rbi_survey_orgtype.csv`.
- **2.2 Revenue growth (cc), FY16–FY26 + Q1FY27:** top-6 (weighted), mid-tier four, Accenture, Cognizant.
  - Data: `output/final/table_A.csv`, `midtier/midtier_vs_top6.csv`.
- **2.3 Revenue level vs pre-COVID trend, top-6 vs Accenture** (index; shaded gap).
  - Data: `round4/robustness/baseline/r1_comparators_levels.csv`.
- **2.4 India's share of world computer-services exports, 2015–25** (ex-Ireland and delivery-country group), with an inset of H1 growth India vs 24 others.
  - Data: `round3/offshore_competitors/india_share_summary.csv`, `imf_h1_india_vs_delivery_group.csv`.
- **2.5 What grew in FY25 vs FY26:** IT services, BPO, engineering, products (grouped bars).
  - Data: `round3/red_team/rbi_exports_by_activity_type.csv`.

### 3. Who is growing (~150 words, 3 charts)

Prose:
- Growth has moved from the giants to GCCs, the mid-tier and BPM.
- The rest of the listed IT mid-market did *not* absorb the slack: 5 of 12 shrank.
- GCC hiring is real but continued at its pre-2023 pace; it did not accelerate.
- Firm weakness is firm-specific, not concentrated in a vertical or region (footnote: variance shares).

Charts:
- **3.1 FY23→FY26 change in headcount and revenue by segment.**
  - Segments: top-6, mid-tier four, other IT, ER&D, BPM, GCCs (range bar, tech roles +155k to +430k, central +260k).
  - Data: `round3/listed_panel/listed_panel_summary.csv`, `round3/gcc_reconcile/gcc_scenarios.csv`.
- **3.2 Public-limited share of software exports, FY12–FY26** (a proxy for "big Indian firms"), with a break marker at FY23.
  - Data: `trade/rbi_survey_orgtype.csv`.
- **3.3 Firm small multiples, quarterly cc growth, 2022–Q2FY27.**
  - TCS negative through 2025 then recovering; LTIM and TechM leading.
  - Data: `data/corrected/yoy_metrics_final.csv` plus `health_check/contradictions/q2fy27_update.csv`.

### 4. Jobs: output up, headcount flat (~250 words, 3 charts + box)

Prose:
- The six giants peaked at 1.69m in Sep 2022. They are ~1.62–1.63m now: down ~4%, flat since FY24, and +9k in Q2FY27 across four reporters.
- Revenue per employee rose from $48.6k to $53.8k.
- Sector-wide, the honest statement is "growing at most ~2% a year". PLFS can't distinguish that from zero.
- About 190k software workers sit outside the IT industry codes, consistent with GCC staff being coded to their parent's industry.

Charts:
- **4.1 Top-6 headcount, quarterly 2015–Q2FY27,** with peak marker; the last point is partial (Infosys and LTIM pending).
  - Data: `core_quarterly_final.csv`, `q2fy27_update.csv`.
- **4.2 Revenue vs headcount, top-6, indexed FY19 = 100.** The widening wedge is revenue per employee.
  - Data: `core_quarterly_final.csv`.
- **4.3 Sector employment: PLFS NIC 62–63 with 90% CI vs Nasscom.**
  - Add a stacked sliver for ICT occupations outside NIC 62–63.
  - Mark the CY2025 design break.
  - Data: `round3/plfs/employment_levels_long.csv`, `health_check/contradictions/plfs_change_ci.csv`, `round3/sector_aggregates/sector_series_pulled.csv`.

**Box: "How many jobs did the sector add?"** A one-line reconciliation for each:
- Nasscom: +135k in FY26.
- Goldman (via the World Bank): "+700k" in three years, about +390k like-for-like.
- ICRIER: "still growing", but that runs to 2023-24 only.
- PLFS: +4% ± 11%.
- Conclusion: all are compatible with ≤2%/yr.

### 5. The bottom rung (~350 words, 7 charts + counterpoint box). The heart of the piece.

Prose:
- The FY22 fresher boom (TCS + Infosys + HCL: 218k) collapsed to 65k by FY25. Sector-wide estimates show the same shape: 55–80% below peak.
- Since FY24 the count has partly recovered, but FY27 targets are lower or withdrawn.
- The more telling signal is *shares*. Each young-entrant measure shows IT's share falling, while young graduates' jobs elsewhere grew:
  - PLFS: IT share of salaried graduates aged 21–25, 20% → 16%.
  - EPFO: IT share of net payroll additions aged 18–25, 5.8% → 3.9%.
  - Xpheno: entry-level share of tech openings, 16% → 12%.
  - foundit: IT share of fresher postings, 32% → 24%.
- Firms got older: the under-30 share fell at 8 of 10 large firms. Infosys's junior grade fell from 46% to 30% of staff.
- Engineering placements fell for the class of 2023-24, the first fall in the NIRF series.
- Junior real pay in IT fell ~12% in 2025 while senior pay held.
- Postings data (World Bank/Lightcast): in AI-exposed jobs, postings for 0–5 years' experience fell most after ChatGPT.
- Footnote: boom-era hires turning 30 around FY30–31 will mechanically depress under-30 shares later; don't read that as AI.

Charts:
- **5.1 Fresher intake, FY16–FY27.**
  - Bars: TCS + Infosys + HCL and the top-6.
  - Hollow bars: FY27 stated targets.
  - Dots: third-party sector estimates (Xpheno, HAN Digital, TeamLease Digital), with FY22 shown as a 450–600k range.
  - Data: `workforce/fresher_hires_annual_best.csv`, `health_check/fresher_thirdparty/fresher_thirdparty_long.csv`.
- **5.2 "Four shares, one direction"** (2×2 small multiples).
  - IT share of salaried graduates 21–25: `contradictions/plfs/it_shares_of_grad_groups.csv`.
  - IT share of EPFO 18–25 net additions: `epfo/epfo_it_age_best.csv`.
  - Entry-level share of tech openings (Xpheno): `fresher_thirdparty_long.csv`.
  - IT share of fresher postings (foundit): same file.
- **5.3 Under-30 share of headcount, FY23 vs latest, 10 firms** (slope chart).
  - Data: `round3/seniority_firms/under30_panel.csv`.
- **5.4 Infosys staff by grade, FY14–FY26** (stacked: junior / middle / senior).
  - Data: `workforce/workforce_firm_tidy.csv`.
- **5.5 NIRF engineering placement rate and median salary by graduating class, elite vs other.**
  - Data: `round3/seniority_sector/nirf_ug4_placement_by_gradyear.csv`.
- **5.6 Real monthly pay in IT by age band (21–25, 26–30, 31–40) vs all graduates 21–25,** 2017-18 to CY2025, with a design-break marker.
  - Data: `health_check/labour_share/chart3_real_earnings_juniors.csv`.
- **5.7 Postings by experience band in AI-exposed jobs** (World Bank/Lightcast effect estimates, dot-and-whisker).
  - Data: `health_check/postings/wb_lightcast_point_estimates.csv`.

**Counterpoint box: "Not a collapse".** Optional mini-chart: graduate unemployment on two measures, from `contradictions/plfs/grad_unemployment_variants.csv`.
- Sector fresher counts bottomed in FY24: Xpheno ~65k → ~120k.
- TeamLease IT hiring intent rebounded (series break flagged).
- All-industry fresher postings on Naukri are back to their 2022 level. The rebound is outside IT; IT postings are still ~30% below 2022.
- Graduate unemployment is high (~40% for under-25s) but not rising.
- India's tech postings fell about half as much as the US/UK ones.

### 6. Health of the business (~200 words, 3 charts)

Prose:
- No signs of financial stress.
- Attrition is back to 12–14% and utilisation is near normal.
- The labour share of value added has held at ~0.7, so pay per head has risen in line with value added per head: a smaller, more senior, costlier workforce.
- Prices have not fallen yet. Firms' own statements put the AI give-back at ~0.4% in FY26, expected ~1.5% in FY27. Broker "2–3.5% deflation" figures are gross forecasts.
- Footnote: the Substack labour-share chart is a methodological artefact.

Charts:
- **6.1 Stress gauges** (small multiples: attrition and utilisation by firm vs 2016–19 mean; trailing-12-month deal value).
  - Data: `core_quarterly_final.csv`, `q2fy27_update.csv`.
- **6.2 Labour share of value added, FY16–FY26:** top-6, RBI listed IT, mid-tier.
  - Data: `health_check/labour_share/chart1_labour_share_measures.csv`.
- **6.3 AI price give-back, measured and expected, FY24–FY27** (fan), with the broker range as a shaded band.
  - Data: `round4/price_statements/m2_aggregate.csv`, `contradictions/output_side/broker_deflation_vs_m2.csv`.

### 7. Demand signals (~100 words, 2 charts)

Prose:
- Clients are doing more IT in-house: the US in-house share of computer jobs rose from 64–65% to 67.5%, and US vendor employment is shrinking.
- On earnings calls, talk of weak demand peaked in 2023. Talk of passing AI savings to clients, and AI mentions generally, have surged since 2025.

Charts:
- **7.1 US computer jobs: in-house share (2015–25) and IT-vendor employment (CES 5415, monthly to 2026).**
  - Data: `round4/demand_shift/oews_computer_occ_by_bucket.csv`, `round3/offshore_competitors/bls_ces_monthly.csv`.
- **7.2 What managers talk about, per earnings call, 2021–2026H2:** demand weakness, AI pass-through, and AI mentions per 10k words.
  - Data: `output/final/fig3_data.csv`. **AI-mention counts must be added to the repo**; computed earlier but not saved.

### 8. What others say, and how it squares (~100 words + table)

Short intro, then a table with columns *claim / source / what we find / reproducible?*:

| Claim | Source | What we find | Reproducible? |
|--|--|--|--|
| Sector added +135k jobs in FY26 | Nasscom | Plausible, unverified | No |
| Rest of sector added "+700k" | Goldman via World Bank | ~+390k like-for-like | Partly |
| Employment still growing | ICRIER | True to 2023-24 | Yes |
| IT share of young graduates 20% → 15.8% | Future of India | Yes; levels are rescaled; labour-share chart is an artefact | Yes / no |
| Graduate unemployment ~40% | State of Working India | Yes, on principal status | Yes |
| Entry-level hiring "+168%" | LinkedIn | Micro-firm hiring only | No |
| Exports 27% above trend | Baldwin | Yes, but half pre-ChatGPT | Yes |
| "600k → 140k" | Xpheno via ET | Mislabel | No |
| "2–3.5% AI deflation" | Brokers | Forecast, gross | No |
| "Top-5 added 17 jobs in nine months" | Computerworld | ~0 confirmed | Yes |

Link to the full citation catalogue.

### 9. What to watch (~120 words, bullets)

- Infosys Q2FY27 (23 Oct) and the rest of the FY27 results: is the headcount uptick broad?
- AI price pass-through in FY27 contracts.
- Whether the post-summer-2026 coding-agent jump shows up in FY27 hiring.
- RBI census of foreign-owned firms (late Oct 2026) for GCCs.
- PLFS 2026.
- Whether EPFO resumes publishing (it has been silent since Sep 2025).
- NIRF 2026 placement data.

### Appendix (collapsibles, outside the word budget)

- **Sources and methods,** one short entry per chart.
- **Metrics we cite but cannot reproduce** (from `health_check/literature/CATALOGUE.md`).
- **Numbers in circulation that are wrong:**
  - TCS "15k below last year" is actually +4.7k y/y.
  - IANS −7,389 is −6,981 by our count.
  - Xpheno "600k→140k" is a mislabel.
  - LinkedIn +168% is micro-firm hiring only.
  - The Economic Survey's 39.5% is not a growth rate.
- **Data notes:**
  - PLFS 2025 redesign; the high-weight cluster in 2023-24.
  - EPFO revisions, and coverage of firms with their own PF trusts.
  - Postings are not hires.
- **PLFS citation and MoSPI acknowledgement.**

---

## Word budget

| Section | Words |
|--|--|
| Intro | 180 |
| Output | 250 |
| Who | 150 |
| Jobs | 250 + box 80 |
| Bottom rung | 350 + box 100 |
| Business | 200 |
| Demand | 100 |
| Ledger | 100 |
| Watch | 120 |
| **Total** | **~1,880 (aim to cut to ~1,600)** |

Captions are one sentence each, stating the takeaway ("Exports grew 19% while the giants grew 7%").

## To build before drafting

- AI-mention counts per call, from `audit/calls_transcripts.csv`.
- Merge the Q2FY27 rows into the chart data; leave canonical files untouched.
- Combined fresher chart data (firm + third-party).
- Rough sector fresher series: top-6 × ~1.7, with a band. Optional.
- A number-check script for the new page.

## Decisions for the user

1. **Scope:** "IT services" broadly (incl. BPM, ER&D, GCCs), or IT services firms narrowly? This outline assumes broad, with the big six as the spine.
2. **Treatment of the two-questions estimates** (replacement rate and demand shift). The outline leaves them out apart from one footnote/link, keeping this a tour, not an argument.
3. **Where it lives:** public GitHub Pages, or a private page first.
4. **Title.**
