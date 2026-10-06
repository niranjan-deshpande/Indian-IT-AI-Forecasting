# FINDINGS — Workforce seniority: are juniors being cut?
*Sources: firm ESG/BRSR/GRI tables and Naukri JobSpeak. Saved by the orchestrator from the probe's report; the probe could not write files.*

## 1. Access

**Firm ESG/GRI/BRSR tables**
- Free annual PDFs, published about 2–4 months after the fiscal year ends.
- Age tables are in the GRI annexes and ESG data books. The BRSR core form splits only by gender.
- Coverage by firm:

| firm | years |
|--|--|
| Infosys | FY14–26 |
| Wipro | FY19–26 |
| HCL | FY20–26 |
| TechM | FY18–26 |
| Mindtree | FY16–22 |
| LTIM | FY23–26 |
| TCS | India-only charts, FY16–25 |

**Naukri JobSpeak**
- Free monthly PDFs at infoedge.in (`/pdfs/News_Events_pdfs/Naukri-Jobspeak-<Mon>-<YYYY>.pdf`), published about 7 days after month end.
- Index levels run Jan-2021 to Aug-2026.
- Experience bands run Nov-2021 to Dec-2024; 2025–26 values were read off the charts.

## 2. Level
- **Firm tables:** firm-level, all 6 Indian firms. Cognizant and Accenture were not probed.
- **JobSpeak:** India-wide by industry. The experience bands cover all industries, not IT specifically.

## 3. Measurement
- **Firm tables:** stocks and flows by age band (<30, 30–50, >50), used as a proxy for how cuts fall by seniority.
  - Infosys also reports job level (Junior = JL3 and below).
  - No firm reports median tenure or experience.
- **JobSpeak:** postings, i.e. labour demand (maps to Q or a·Q). It is not an official statistic, and it excludes "gig employment, hyperlocal hiring, or campus placement".

## 4. Noise
- **JobSpeak IT-Software, YoY log ×100**
  - 2022 only (n=12 months): s.d. 23.1, AR(1) 0.56.
  - Annual means: −33 (2023), −2 (2024), 0 (2025), +1.5 (2026).
  - Correlation with pilot gL: 0.55 (n=18).
- **Infosys change in <30 share**
  - FY15–21 mean −2.0 pp/yr (s.d. 1.9, n=7).
  - FY24–26 mean −3.0.

## Results

**<30 share, FY23 → latest**

| firm | <30 share FY23 → latest | revenue change (log pts) |
|--|--|--|
| Infosys | 59.6 → 50.7 | +10 |
| HCL | 41.3 → 34.3 | +15 |
| LTIM | 44.5 → 35.0 | +15 |
| TCS India (to FY25) | 52.9 → 47.7 | +8 |
| Wipro | 53.3 → 48.4 | −7 |
| TechM | 48.3 → 46.7 | −3 |

- The pre-FY22 trend was already −1.4 to −2 pp/yr. It accelerated only at Infosys (−3.0 vs −2.0) and TCS (−2.6 vs −1.7).

**Infosys job levels, FY23–26**
- Junior headcount fell 47 log pts; middle and senior rose 22; revenue rose 10.
- The junior share fell 5.4 pp/yr, against a 1.7 pp/yr pre-trend.
- Some of this is promotion of the FY22 intake.

**Hires per $bn revenue, FY25–26 vs pre-COVID (junior relative to senior)**
- Infosys: −47.
- LTIM vs LTI+Mindtree: −45.
- Wipro: +10.
- The <30 share of new hires shows no persistent shift at HCL, Wipro or LTIM.

**Fresher hires vs the FY16–23 revenue relation** (firm fixed effects; n=19; residual s.d. 35 log pts)
- Infosys: −59, −49, −31 for FY24–26 (narrowing).
- TCS: −18, +13.
- HCL: −49 to −91, but its baseline covers only the FY22–23 boom.

**JobSpeak gap (0–3 yrs minus 16+ yrs, YoY, all industries)**
- −35 (2023), −20 (2024), −4 (2025), +4 (2026). Cyclical and now reversed.

## 5. Predicted signs
- **S1:** junior hiring falls in proportion to revenue and reverses later; seniors fall too.
- **S2/S3:** junior share and hiring fall persistently, conditional on revenue, while seniors are held. Under S3, revenue lags as well.
- **S4:** cuts across all levels. Captives poach experienced staff, so the junior share could even rise.

**Confounds**
- The pyramid was already ageing: the <30 share has fallen since FY14.
- The FY22 hiring surge left a hangover, and that intake is now being promoted.
- Low attrition reduces replacement hiring.

## 6. Verdict
**Conditional yes (~2 RA-days).** The data are collected. Infosys job levels and hires by age are informative. Annual data with 3 post-shock years give low power, and JobSpeak is weak for IT.

## Files
- `workforce_firm_tidy.csv`
- `firm_year_junior_metrics.csv`
- `fresher_hires_annual_best.csv`
- `jobspeak_monthly.csv`
- `jobspeak_expband_yoy_combined.csv`
- `analyze_firms.py`
- `analyze_jobspeak.py`
- `parse_jobspeak.py`
