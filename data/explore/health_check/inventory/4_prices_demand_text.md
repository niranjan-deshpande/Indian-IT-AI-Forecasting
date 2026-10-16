# Inventory of the prices, client demand and text/disclosure data

## 1. Datasets: what each measures, source, coverage, latest period

**Prices** (`data/explore/prices/`; `price_data.md` corrects and supersedes this folder's FINDINGS)
- `price_indices_quarterly.csv` (series, cal_q, level, yoy_log100) holds 12 series through **2026Q2**:
  - US PPI: WPU4561 (equal to PCU513210513210506, software publishers only), PCU518210518210 (data processing/hosting), PCU5182105182101 (BPM), PCU541610541610 (management consulting).
  - US wages: ECI CIU2025400000000I and CIU2020000120000I; CES AHE for NAICS 5415.
  - UK SPPI: HR6L (J62), HRFE, HR6O.
  - BEA: B985RG (software price).
- `noise_stats.csv`, `price_minus_wage_stats.csv`, `corr_with_indian_gR.csv`: per-series s.d., AR(1), pre/post means, and correlations with the firms' median revenue growth (gR).
- `bea_software_prices_annual.csv`: BEA prepackaged, custom and own-account price indices, 2005–2024.
- `final_bls/ppi_518210_monthly.csv` and `_annual.csv`: through Aug 2026.
- `gsa_calc_vendor_check.csv`: one snapshot of GSA federal ceiling rates. Accenture $211, Cognizant $220, Tata $225, Infosys $158 (median hourly); Wipro, HCL, TechM and LTIM are absent.
- **No US PPI exists for NAICS 5415**, re-verified 2026-10-05.

**Firm price disclosures**
- `audit/price_firm_disclosures.csv` (434 rows) covers:
  - Infosys revenue per billed person-month, FY03–FY20;
  - Wipro, FY09–12;
  - LTI billed person-months, to Sep 2022;
  - Accenture and Cognizant qualitative pricing language.
- `audit/price_calls_quotes.csv` (389 verbatim management pricing statements, 183 transcripts, Jan 2021–Oct 2026, 8 firms; TCS Q4FY23 missing) feeds `price_calls_timeline.md`.

**AI give-back estimate, "M2"** (`round4/price_statements/`, dated 2026-10-15, the latest)
- `m2_statements.csv`: 108 coded statements, including TCS Q2FY27 (8 Oct 2026) and BPO firms.
- `m2_firm_year.csv` and `m2_aggregate.csv` (segment, fy, low, central, high, gross_*): AI give-back on same-scope work as % per year, FY24–FY27.

**Demand** (`round4/demand_shift/`, 2026-10-14; partly superseded by `robustness/demand/`, 2026-10-15)
- `bea_software_annual.csv`: NIPA 5.6.4–5.6.6, custom, own-account and prepackaged, nominal, real and price, 2010–2025.
- `bea_software_quarterly_total.csv`: total software SAAR, 2023Q1–**2026Q2**.
- `bank_tech_xbrl_long.csv`: JPM, BAC, C and WFC XBRL expense lines, FY and H1, to **H1 2026**.
- `bank_tech_budgets_disclosed.csv`: press figures, mostly unconfirmed.
- `oews_computer_occ_by_bucket.csv`: BLS OEWS computer occupations by buyer bucket, May 2015–**May 2025**.
- `rbi_destination_split.csv`: RBI export shares by destination, FY24–26.
- `consultancy_context.csv`: Gartner and ISG figures. These are circular (they measure vendor revenue).
- `d_bounds.csv`: superseded by `d_bounds_r3.csv`.
- Robustness folder:
  - `oews_ces_check.csv`: CES NAICS 5415 to **May 2026**.
  - `europe_series_annual.csv` and `europe_prepost.csv`: Eurostat ICT specialists by NACE to 2025; ONS UK purchased vs own-account software GFCF.
  - `gcc_*` files: GCC headcount from Nasscom/Zinnov, plus RBI foreign-subsidiary export growth.
  - `destination_weights.csv`, `d_bounds_r3.csv`.

**Growth by service line and AI exposure** (`round4/elasticity_xsec/`)
- `line_growth_quarterly.csv` (firm, cal_q, g, basis, line) and `line_growth_firms.csv` (window means) cover:
  - Accenture Consulting vs Managed Services;
  - Cognizant Consulting & Technology vs Outsourcing;
  - HCLTech IT&BS vs ER&D;
  - TechM IT vs BPS;
  - all to 2026Q2.
- `rbi_activity_exports.csv` and `rbi_growth_by_year.csv`: RBI exports for IT services, BPO and engineering, FY19–FY26.
- `line_exposure.csv` and `occupation_scores.csv`: Eloundou and Felten AI-exposure scores mapped to service lines.
- `listed_segment_growth.csv`: listed firms by segment, FY23–26.

**Text** (`data/explore/text_firms/`, dated 2026-09-27, no FINDINGS file)
- **A_text:** a pre-registered dictionary with four families (pricing, productivity, demand, GCC). It has **no AI/GenAI term family.**
  - `term_counts_doc.csv` covers 191 transcripts, 6 firms (no Cognizant or LTIM), 2018Q1–2026Q2.
  - Also `family_rates_fq.csv`, `pooled_by_year.csv` (rate per 10k words), `onsets.csv` and `validation_vs_gR.csv`.
- **B_more_firms:** `firm_disclosure_table.csv`, an inventory of what 16 other firms disclose (Persistent, Coforge, Mphasis, Capgemini, EPAM and others). No data series.
- **C_procurement:** UK Contracts Finder and USAspending award counts by firm-year, 2018–2026 (`counts_by_firm_year.csv`), plus 11 contract re-let pairs in `examples.csv`. The Indian firms barely appear in US federal data (TCS, Infosys and LTIM show about zero). NEXT_STEPS already rejected this source.

**Coded earnings-call statements**
- `audit/calls_statements.csv`: 2,087 statements, made of 389 pricing plus 1,711 demand (`audit/demand_calls_quotes.csv`) minus 13 duplicates.
- Coder files: `calls_coding_coder1/2.csv`. Codes are A = demand weakness, B = pricing stable, C = non-AI pricing pressure, D = AI productivity passed to clients, E = other.
- Agreement is 92.1%, κ = 0.87.
- `output/final/fig3_data.csv` has a 3-row multi-index header: statements, per_transcript and share_of_transcripts_with_any by half-year.
- `calls_disagreements.csv` lists 164 disagreements.

## 2. Current-state facts (latest available)

**Price indices, YoY log ×100, 2026Q2**
| Index | YoY | Notes |
|--|--|--|
| US PPI data processing/hosting (518210) | +0.1 | 2025 annual +3.3%; Jan–Aug 2026 +0.5% |
| US PPI management consulting | −0.9 | Negative since 2025Q3 (−1.3, −1.4, −0.3, −0.9). Minus ECI wages: −3.4 in 2025 vs a −1.6 baseline, under 1 s.d. |
| UK SPPI J62 | +5.2 | Dipped to −0.9/−1.4 in 2025Q2–Q3 |
| UK J6201 (programming) | +7.5 | |
| BEA software price | −1.2 | 2025 annual −2.0 |
| BEA custom software | | 2025 −3.0% |
| ECI wages, professional/technical | +2.6 to +3.5 | |
| CES AHE, NAICS 5415 | +2.3 | |

- WPU4561 is +20.2 but driven by software-publisher maintenance repricing in a thin sample; ignore it.
- The BPM PPI is about 0.0–0.3% in every quarter, which looks stale. Flag before use.
- Everest India ITO FTE price: +3.1% (H1'23), +1.3% (H2'23), −0.4% (H1'24). These are p/a figures.
- ISG resource-unit glide paths for deals in the 12 months to Oct 2025 run 2–3× the historical 10–20% decline over 2 years.
- Every official index is p/a or input-cost based. **No measured price per unit of output exists for Indian IT.**

**What firms said about pricing and AI give-backs**
| Period | What firms said |
|--|--|
| 2021H1 | "Stable" |
| 2021H2–22 | Rate-card and COLA increases |
| Apr 2023 | Turn: "no price expansion" (HCLTech Q4FY23) |
| Jul 2023 | HCLTech: deflation "at least two to three years away" |
| 2025 | Pass-through made explicit: LTIM Jan 2025; TCS "$100 … $95 or $90", Apr 2025 |
| 2026 | Quantified: HCLTech 2–3%/yr for its portfolio (3–5% in AI-disrupted services), "$100 million deal … maybe 80 million" (Apr 2026); LTIM ≈15% less for the same scope (Jul 2026); TCS 10–15% productivity passed on over the term (Jul 2026) |
| Oct 2026 | TCS Q2FY27: "at an overall portfolio level, the pricing is broadly stable" |

- Counter-voices: Accenture said "we don't see AI as deflationary" (Sep 2025), then that it is "giving more productivity" but more than offsetting it (Oct 2026). Cognizant (Jun 2026): "very little deflation at a aggregate industry … level."
- Pricing statements per half-year rose from 15–37 in 2021–24 to 54 (2025H2), 61 (2026H1) and 48 (2026H2 so far).
- **M2 central AI give-back for the top-six IT firms:**
  | FY | AI increment, %/yr (low–high) | Gross incl. pre-AI baseline |
  |--|--|--|
  | FY24 | 0 | |
  | FY25 | 0.10 | |
  | FY26 | 0.43 (0.01–1.32) | 1.98 |
  | FY27 | 1.51 (0.41–2.67) | 3.06 |
- The pre-AI baseline is an assumed ~1.55%/yr. BPO (Sagility only) is 0.5 for FY26 and 1.0 for FY27.

**Client budgets and in-house work**
- **Bank tech lines** (XBRL "CommunicationsAndInformationTechnology"):
  - JPM+BAC+C: $24.2bn (2022), $25.1bn (2023), $26.1bn (2024), $27.9bn (2025, +6.7%).
  - JPM+BAC, H1 2026 vs H1 2025: +11.3 log points.
  - JPM's line is partial: it fell over 2020–23 while JPM's disclosed total rose.
  - JPM's 2026 tech budget is $19.8bn (press, about +10%).
- **BEA software investment:**
  - Custom (purchased, which is circular) nominal growth: 8.0%/yr (2016–19) to 5.3%/yr (2023–25); 2025 +6.9%.
  - Own-account nominal: 4.8 to 5.7; 2025 +2.6%.
  - Own-account share of custom plus own-account: 31.1% (2015), 26.1% (2022), 27.2% (2023–24), 26.4% (2025).
  - Total software, H1 2026: +8.6 log points y/y; SAAR $809bn in 2026Q2.
- **US computer jobs (OEWS):**
  - Vendors (NAICS 5415): 1.279m (2022) to 1.207m (2025), −1.9%/yr.
  - Client in-house: 2.275m to 2.505m, +3.2%/yr.
  - In-house share: 64.0–64.9% over 2015–22, then 65.7%, 66.9% and **67.5% (2025)**.
  - CES confirms the fall: 5415 employment −1.5% (2024), −1.2% (2025), **−1.7% to May 2026**.
  - Staffing (5613) computer jobs fell 8.3%/yr.
- **Europe:**
  - EU27 ICT specialists in J62–63 grew 7.97% (2023), 5.61% (2024), **0.88% (2025)**.
  - EU in-house ICT specialists grew about 4%/yr; the in-house share stopped falling at 0.54.
  - UK purchased software GFCF fell from +7.0%/yr before to −0.4%/yr in 2023–25. Own-account rose 10.6%/yr; its share went 0.72 (2022) to 0.78 (2025). Both are unverified for method changes.
- **Export destinations:** the US takes about 54% and Europe about 31.8%.

**Demand themes in earnings calls** (coder 1, per transcript)
- **A (demand weakness):**
  | Half-year | A per transcript |
  |--|--|
  | 2021H2–2022H1 | 0.44 |
  | 2022H2 | 3.0 |
  | 2023H1 | 7.5 |
  | 2023H2 (peak) | 7.9 |
  | 2024H1 | 6.4 |
  | 2024H2–2026H1 | 4.7–5.7 |
  | 2026H2 (8 calls) | 5.9 |
- **D (AI productivity passed to clients):**
  | Half-year | D per transcript |
  |--|--|
  | 2022 | 0 |
  | 2023 | 0.25 |
  | 2024H2 | 0.63 |
  | 2025H1 | 1.44 |
  | 2026H1 | 1.63 |
  | 2026H2 | 3.0 |
  - D appears in 100% of 2026H2 transcripts.
- **B (pricing stable)** fell to 0.06 per transcript in 2026H1.
- My keyword counts within the statements (not a repo output; per transcript):
  - "discretionary": 0.12–0.38 (2021–22), 3.38 (2023H2 peak), 1.8–2.4 (2026);
  - cost take-out or consolidation: peaks at 1.56 (2023H2);
  - macro, uncertainty or tariff: about 2.4 from 2023 on.
- Demand-pass topics: "demand_weak" statements were 0–10 per half-year in 2021–22, 36–48 in 2023H1–2024H1, and 14–22 after that.
- **A_text pooled rates per 10k words (6 firms):**
  - demand family: 1.5–3.1 (2018–21), 7.84 (2023), 8.40 (2024), 4.61 (2026);
  - pricing family: about 0.5–1.1 until 2024, 1.55 (2025), **3.07 (2026)**;
  - productivity give-back family: 0 until 2021, **1.54 (2026)**.

**AI/GenAI mentions** (not in the repo; I computed this read-only on the 183 transcripts in `audit/calls_transcripts.csv`, script kept in the scratchpad)

| Half-year | "AI" per 10k words | per call | "GenAI/generative AI" per 10k | "agentic/AI agent" per 10k |
|--|--|--|--|--|
| 2021–2022 | about 2–3 | about 2 | 0 | 0 |
| 2023H1 | 10 | | | |
| 2023H2 | 28 | | 18 (peak) | |
| 2024H2 | 36 | | 23 (peak) | |
| 2025H2 | 74 | 66 | | 8.6 |
| 2026H1 | 85 | 75 | | |
| 2026H2 | 104 | 97 | 0.8 | |

- "GenAI" gave way to "AI" and "agentic" from 2025.

**Growth by service line**

Constant-currency YoY, % (mean of quarters):
| Line | 2016–22 | Recent (2024Q2–26Q2) |
|--|--|--|
| Accenture Consulting | 12.7 | 3.3 |
| Accenture Managed Services | 10.7 | 6.9 |
| Cognizant Consulting & Technology | 8.3 | 6.6 |
| Cognizant Outsourcing | 5.9 | 2.0 |
| HCLTech ER&D | 15.5 | 6.6 |
| HCLTech IT&BS | 13.8 | 4.1 |
| TechM BPS | 18.5 | 8.9 |
| TechM IT | 10.3 | 5.1 |

- Basis caveats: Cognizant is in reported USD, not constant currency. TechM is in reported currency (INR), which inflates its 2026 figures of about 16%.

RBI exports, INR log growth, %:
| Activity | FY24 | FY25 | FY26 |
|--|--|--|--|
| IT services | 7.6 | 6.7 | 15.7 |
| BPO | 0.7 | 12.9 | 4.8 |
| Engineering | 5.1 | 13.7 | 14.4 |

- **Correlation with AI exposure: none identifiable.**
  - Gaps in exposure between lines imply only 0.1–0.5 pp/yr of price-cut difference, against about 3 pp/yr of noise.
  - The exposure ranking flips depending on whether Eloundou GPT, Eloundou human or Felten scores are used.
  - The binary-class ε estimate is 0.83, with a 95% interval of −1.7 to 3.3 (p = 0.88).

## 3. Caveats and what is unmeasured
- There is no measured sector price per unit of output. Analyst "deflation" figures (Kotak 3–3.5%/yr; Jefferies about 20% over CY25–30) **assume** the pass-through rather than measure it.
- Pricing statements are cheap talk and are driven by analyst questions. Infosys and Wipro never give a number. Time-and-materials pass-through (as fewer billed hours) is never called a give-back.
- Calls coding: the pricing and demand passes read with different intensity (2.1 vs 9.3 statements per call). Compare each category over time, not levels across categories.
- 2026H2 has only 8 calls. Q2FY27 calls are held only for TCS (plus HCLTech's investor release).
- OEWS is not a true time series, and there was a SOC break in 2019, although CES corroborates the vendor-employment fall.
- BEA "purchased custom" software is vendor revenue, so it is circular.
- UK own-account software may reflect a method change.
- GCC headcount levels come from different editions on different bases.
- Bank figures: the XBRL lines are partial and the press totals are unconfirmed.
- About 13% of demand (destinations outside North America and Europe) is unmeasured. Nothing captures clients substituting their own AI tools, or share lost to other vendors.

## 4. Conclusions, and what superseded what
- **Prices:** `price_data.md` (Oct 5) supersedes `prices/FINDINGS.md`: the 5415 PPI was never published, and 518210 was added. **M2 (Oct 15) is the current word on AI give-backs:** about zero through FY26, about 1.5%/yr in FY27, mostly as expectation. The checkpoint's "firms kept about nine-tenths of the saving" rests on this.
- **Demand:** M5 (`demand_shift`) put the vendor-facing demand shift at −3.1 pp/yr (−7.3 to +0.1). **R3 (`robustness/demand`) supersedes it at −1.6 (−7.4 to +2.2):**
  - The GCC term flips from −1.0 to +0.5 once pre-2023 GCC growth is netted out; the RBI data show GCCs gained share no faster after 2023 than before.
  - Europe leaves the share term unchanged at −1.6.
  - CES confirms OEWS.
  - Market-wide demand barely moved (−0.5). The share term (in-housing) is −1.6.
  - About 5.4 pp of the roughly −7 pp diagnosed slowdown is **unexplained**.
- **Service-line exposure ("M6"):** cannot identify ε. Use it only as a consistency check, with a prior of ε ≈ 0.5–1.5 for IT.
- **Procurement:** not viable.

## 5. Candidate charts
1. US and UK price indices, YoY, 2015–2026Q2. File: `prices/price_indices_quarterly.csv`. Series PCU518210518210, PCU541610541610, HR6L, B985RG and CIU2025400000000I (yoy_log100).
2. Consulting price minus wages. File: `prices/price_minus_wage_stats.csv`, or derive it from chart 1.
3. Everest India FTE price and Infosys revenue per billed person-month, FY10–20. File: `audit/price_firm_disclosures.csv` (metric, value), plus the `price_data.md` table.
4. Pricing statements by topic per half-year. File: `audit/price_calls_quotes.csv` (call_date, topic).
5. M2 AI give-back fan chart, FY24–27. File: `round4/price_statements/m2_aggregate.csv` (low, central, high, gross_central).
6. Coded call categories A and D per transcript. File: `output/final/fig3_data.csv` (skip the 2 extra header rows; use the per_transcript A and D columns). Coder 2 version: `fig3_data_coder2.csv`.
7. A_text family rates by year. File: `text_firms/A_text/pooled_by_year.csv`. Firm-quarter detail: `family_rates_fq.csv`.
8. AI mentions per 10k words. **Not in the repo**: recompute from `audit/calls_transcripts.csv` local_path (my numbers are in §2).
9. US in-house share of computer jobs, plus vendor vs in-house levels. File: `demand_shift/oews_computer_occ_by_bucket.csv` (inhouse_share_client_over_client_plus_5415, comp_vendor_5415, comp_client_all). Overlay `robustness/demand/oews_ces_check.csv` (ces_may_5415_k, to 2026).
10. BEA custom vs own-account software growth, and the own-account share. File: `demand_shift/bea_software_annual.csv` (g_custom_nom, g_ownacct_nom, ownacct_share_nom). Quarterly total: `bea_software_quarterly_total.csv`.
11. Bank tech expense, JPM+BAC+C, FY and H1. File: `demand_shift/bank_tech_xbrl_long.csv` (concept == CommunicationsAndInformationTechnology).
12. Europe: EU vendor vs in-house ICT specialists, and UK purchased vs own-account software. File: `robustness/demand/europe_series_annual.csv` (eu27_ict_vendor_J62_J63, eu27_ict_client_narrow, uk_software_purchased_cp, uk_software_ownacct_share).
13. Waterfall of the demand-shift decomposition. File: `robustness/demand/d_bounds_r3.csv` (low, central, high).
14. Service-line growth, pre vs recent. File: `elasticity_xsec/line_growth_firms.csv` (window, mean_g).
15. RBI exports by activity. File: `elasticity_xsec/rbi_growth_by_year.csv` (it_services, bpo, engineering).

## Earnings-call quotes on demand and pricing
- **LTIMindtree Q3FY24 (Jan 2024), Sudhir Chaturvedi, p.17:** "the discretionary spend has stopped in several industries." (DEM-LTIMindtree-134)
- **Cognizant Q1CY2024 (May 2024), Ravi Kumar S., p.3:** "softness in smaller deals in the range of zero to $10 million total contract value" (DEM-Cognizant-109)
- **Infosys Q1FY26 (Jul 2025), Jayesh Sanghrajka (HTML exhibit):** "Discretionary programs are paused because of significant investments in Gen AI GPU and AI." (DEM-Infosys-191)
- **Accenture Q4FY24 (Sep 2024), Julie Sweet, p.18:** clients are "trying to save money on IT to free up the spending on areas of GenAI" (DEM-Accenture-115)
- **Wipro Q1FY27 (Jul 2026), Srini Pallia, p.14:** "the traditional IT, the traditional BPO … those budgets are getting compressed." (Wipro-35)
- **HCLTech Q4FY26 (Apr 2026), C. Vijayakumar, p.21:** "$100 million deal would be much lesser today - maybe 80 million" (HCLTech-55). Pair it with p.23: "very little has really played out in already reported numbers" (HCLTech-58).