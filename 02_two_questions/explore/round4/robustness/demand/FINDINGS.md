# FINDINGS — R3: robustness of M5 (demand shift d) — GCC baseline, Europe, OEWS vs CES

*Saved by the orchestrator from the subagent's report (subagents can't write report files). Date: 2026-10-15. Scripts run as `python3 -I <script> .`. Downloads (Eurostat API, ONS, RBI HTML) are in `raw/`. "Change" = mean of 2023–25 (FY24–26) minus the mean of the pre-period.*

## 1. Headline

| | M5 | R3 |
|--|--|--|
| Market term | −0.5 (US only) | −0.5 (North America + Europe, weighted by export destination) |
| Share term | −1.6 (US) | −1.6 (NA −1.56 × 0.63; Europe −1.67 × 0.37) |
| GCC term | −1.0 (0 to −2.5) | **+0.5 (−2.2 to +1.6)** |
| **Vendor-facing Δd** | **−3.1 (−7.3 to +0.1)** | **−1.6 (−7.4 to +2.2)** |
| Sector Δd (incl. GCC) | −2.1 | −2.1 (−5.2 to +0.6) |
| Unexplained vs the diagnosed −7 | ≈ 3.9 pp | **≈ 5.4 pp (−0.4 to 9.2)** |

None of the three checks closes the gap:
- **GCCs:** net of their pre-2023 growth, they drop out.
- **Europe:** on balance, it doesn't change the share term.
- **CES:** confirms the OEWS fall.

Measured shifts in client demand now explain about a quarter of the roughly −7 pp fall. This decomposition uses the growth-mean baseline; see R1 for how much the baseline matters.

## 2. GCC growth before 2023
Files: `gcc_baseline_inputs.csv`, `gcc_baseline_scenarios.csv`, `gcc_rbi_relative_growth.csv`.

**Levels.** These are industry estimates. Only change within one edition or basis is meaningful.

| FY | value | basis | status |
|--|--|--|--|
| FY19 | ~1.0m | old | CONFIRMED (Zinnov blog, 6 Feb 2020) |
| FY21 | 1.38m | old (2021 edition) | CONFIRMED |
| FY23 | 1.66m | old (GCC 4.0) | CONFIRMED |
| FY24 | 1.90m | restated Sep 2024 | CONFIRMED |
| FY19–24 | +36% | restated | NOT CONFIRMED (snippet) |
| FY24 | average 1,130+ per GCC, +24% since FY19; 1,700+ GCCs, 400+ of them new | restated | CONFIRMED (IANS); implies FY19 ≈ 1.18m |
| FY26 | 2.36m | 2026 edition, coverage probably wider | CONFIRMED |

**Additions per year, thousands:**
- Pre-2023:
  - P1 (FY19–23): 165
  - P2 (FY21–23): 140
  - P3 (FY19–24, +36%): 101
  - P4 (FY19–24): 143
- Post-2023:
  - S3 (staffing firms): 128
  - S4 (2024-edition path): 94
  - S2 (restated chain): 180
  - E26 (2026 edition): 230

**Term.** The GCC term is −(post absorption − pre absorption), where absorption = 0.67 tech share × additions ÷ vendor base.
- The vendor base is 3.6m post-2023. The 3.3m pre-2023 base is an assumption.
- Central (P2/P4 vs S3): **+0.48**.
- Range: −2.24 (P3 vs E26) to +1.60 (P1 vs S4). Excluding E26, the low end is −1.31.

**RBI census cross-check (official).** Foreign subsidiaries' I&C export growth in USD, and its gap over total software exports:

| period | foreign subsidiaries' growth (mean) | gap over total software exports |
|--|--|--|
| FY20–23 | 16.1% | mean +5.3 (FY22 +9.3, FY23 +1.2) |
| FY24–25 | 9.4% | mean +4.3 (FY24 +6.8, FY25 +1.9) |

- Total software exports grew 17.2, 18.4, 2.8 and 7.3% in FY22–25 (CONFIRMED, prid 54338, 56542, 61562, 63625).
- So GCCs gained share no faster after 2023 than before.
- Caveats: the FLA census includes foreign vendors and telecom, and its USD conversion is approximate.

## 3. European proxies
Files: `europe_proxies.py`, `europe_series_annual.csv`, `europe_prepost.csv`.

**Sources (official, CONFIRMED):**
- Eurostat `isoc_sks_itspn2`: ICT specialists by NACE, 2008–2025.
- Eurostat `nama_10_an6` (IPP GFCF; no software split) and `nama_10_gdp`.
- ONS CXNV: UK purchased (EF8L) and own-account (EF9P) software GFCF, to 2026Q2.
- ONS ABMI and YBGB.
- The UK LFS series stops in 2019.

**Breaks in the LFS:**
- 2020: Germany's Mikrozensus redesign moved about 180k workers from J58–60 to J62–63.
- 2021: the IESS break, EU-wide.
- The pre-period is therefore 2016–19 plus 2022 (plus 2020 for the EU excluding Germany).

| series | pre | 2023–25 | change |
|--|--|--|--|
| EU27 ICT specialists in J62–63 (vendors) | 6.73 | 4.82 (2025: +0.9) | −1.91 |
| EU27 in-house, narrow | 3.66 | 3.22 | −0.44 |
| EU27 in-house, broad | 3.59 | 2.90 | −0.69 |
| Relative vendor − in-house: narrow / broad / EU excl. DE | | | −1.47 / −1.22 / −0.87 |
| EU27 ICT specialists, all | 4.60 | 3.61 | −0.99 |
| EU27 real GDP | 1.81 | 1.04 | −0.77 |
| UK real GDP | 1.56 | 0.92 | −0.64 |
| EU27 excl. IE real IPP GFCF / DE+FR | | | −0.06 / −0.12 |
| UK purchased software GFCF, nominal | 6.98 | −0.40 | −7.37 |
| UK own-account software GFCF, nominal | 6.75 | 10.63 | +3.89 (real +2.1) |

**In-house shares:**
- EU (narrow): 0.62 (2016), 0.55 (2022), 0.54 (2023–25). The drift toward vendors stopped rather than reversed.
- UK own-account share of software investment: 0.70 (2016), 0.72 (2022), 0.78 (2025).

**Terms (M5 formula):**
- Continental EU share: −0.8 to +0.9, central ≈ 0.
- UK share from software GFCF: −8.1 to −6.3. This is circular on the vendor side, and the 2023 own-account surge (+16%) hasn't been checked for method changes. Combined UK: −8.1 / **−3.6** / +0.9.
- Europe share (UK 47%): −4.2 / −1.7 / +0.9.
- Europe market: −0.52, ±1.

**Weights.** FY24–26: North America 55.0%, Europe 31.8% (UK 15.0%), other 13.2%. Renormalised: NA 0.634, Europe 0.366.

## 4. OEWS vs CES, NAICS 5415
File: `oews_ces_check.csv`.

- OEWS and CES levels track closely: the ratio is 0.987–1.021 over 2015–25. CES also shows the 2022 jump (+7.4%).

| growth, %/yr | 2016–22 | 2023–25 | change |
|--|--|--|--|
| CES (May) | 3.61 | −0.59 | −4.20 |
| OEWS total 5415 | 3.86 | −0.34 | −4.20 |
| OEWS computer occupations in 5415 | | | −4.48 |

- CES fell a further −1.7% in the year to May 2026.
- Computer occupations' share of 5415 employment went from 0.518 to 0.494. That mix shift (about −0.3 pp/yr) is the only part that rests on OEWS alone.
- **Verdict:** the OEWS fall is real, not an artefact. With CES, the US share term becomes −3.1 / −2.3 / −1.5 (OEWS gave −3.3 / −2.5 / −1.7).

## 5. Recomputed bounds
Files: `d_bounds_r3.py`, `d_bounds_r3.csv`.

| component | low | central | high |
|--|--|--|--|
| Market (destination-weighted) | −1.50 | −0.51 | +0.50 |
| Share, US | −3.32 | −1.56 | −0.36 |
| Share, Europe | −4.24 | −1.67 | +0.90 |
| Share (destination-weighted) | −3.66 | −1.60 | +0.10 |
| GCC (net of pre-2023 growth) | −2.24 | +0.48 | +1.60 |
| **Vendor-facing total** | **−7.40** | **−1.62** | **+2.20** |
| Sector total (incl. GCC) | −5.16 | −2.11 | +0.60 |

**Sensitivities of the vendor-facing central:**
- GCC term = 0: −2.1
- UK from EU-LFS read-across only: −1.0
- UK from ONS GFCF only: −2.2
- US proxies applied to all demand: −1.6

Across these, the unexplained part vs −7 is 4.8–6.0 pp (central 5.4).

**Remaining candidates** (Europe is no longer "unmeasured"; GCCs drop out):
- the baseline overstates post-boom normal growth (see R1);
- clients substitute their own AI tools;
- share lost to other vendors;
- the UK share term, if the ONS surge is genuine.

## 6. Not done / not confirmed
- No GCC headcount for FY16–18.
- "+36%" unconfirmed; Nasscom PDFs not opened (406 / members only).
- The 3.3m pre-2023 vendor base is an assumption.
- ONS own-account method revisions not checked.
- No UK occupation-by-industry series.
- The Eurostat IPP series includes R&D.

## Files
- **Scripts:** `eurostat_parse.py`, `europe_proxies.py`, `d_bounds_r3.py`
- **CSVs:** `europe_series_annual.csv`, `europe_prepost.csv`, `gcc_baseline_inputs.csv`, `gcc_baseline_scenarios.csv`, `gcc_rbi_relative_growth.csv`, `oews_ces_check.csv`, `destination_weights.csv`, `d_bounds_r3.csv`
- **raw/:** downloads. `eurostat_isoc_sks_itsn2_eu27.json` (a 404 stub) and `rbi_prid_55767.html` were not used.
