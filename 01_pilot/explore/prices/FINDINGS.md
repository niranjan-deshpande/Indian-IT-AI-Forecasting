# FINDINGS — official IT-services price indices: p or p/a?

*This file was saved by the orchestrator from the probe's report; the probe could not write files.*

**Headline: no official index measures price per unit of output (p) for IT services.**

## 1. Access (all free, no login)

- **US BLS PPI.** NAICS 541511, 541512, 541513 and 541519 are in "Areas of Noncoverage in the PPI System" (bls.gov/ppi/fd-id/areas-of-noncoverage-in-the-ppi-system.htm).
- **WPU4561 ("IT technical support and consulting").** BLS: "includes industry for software publishers, all other industries producing this product are excluded". It duplicates PCU513210513210506 (r=0.99999). Monthly, 2008M12–2026M08.
- **Nearest US proxies.** PCU518210 (data processing and hosting, 2000–) and PCU541610 (management consulting, 2006–); lag about 2 weeks.
- **US wage comparators.** ECI wages for professional/scientific/technical services; CES average hourly earnings for NAICS 5415.
- **UK SPPI.** HR6L (J62, 2008Q4–), HRFE (J6202, 1996–), HR6O (J6201, 2018Q4–). Quarterly, lag about 3 weeks, last period 2026Q2.
- **US BEA.** The software price index (B985RG) is quarterly through 2026Q2. The custom, own-account and prepackaged split (Table 5.6.4) is annual and ends in 2024.
- **GSA CALC+.** Federal ceiling labour rates, current snapshot only.

## 2. Level

All indices are industry-level. In CALC+, the vendors found were Accenture Federal (2,101 labour categories), Cognizant Government Solutions (152), Tata America (94) and Infosys Public Services (18). Wipro, HCL, TechM and LTIMindtree are absent.

## 3. Measurement

- **BLS management consulting (p/a).** "Respondents provide the rates for each of the professionals who bill for their time." Hours are held fixed "unless the number of hours required to provide the service changes". That clause is the only route by which S3 could appear, and it depends on respondents reporting the change.
- **ONS J62 (p/a).** A Voorburg Group 2012 paper on computer services says "the main pricing method is charge-out rates", with "a time based method for Computer Programming Activities" used in every country. The ONS's own methods document sat behind a verification page, so this rests on the international paper.
- **BEA custom software (circular).** It is a "weighted average of the prepackaged software price and of a BEA input-cost index" with an "explicit adjustment for changes in productivity" (NIPA Handbook, ch. 6). Own-account software uses the same deflator: custom and own-account are both 88.6 in 2024.
- **GSA CALC+ (p/a).** Hourly rates.

## 4. Noise

YoY log change ×100, 2015–22 excluding 2020Q2–2021Q2, n=27.

| series | s.d. | AR(1) | mean pre-2023 | mean 2023–26Q2 |
|--|--|--|--|--|
| UK J62 | 1.24 | 0.72 | 2.0 | 2.7 |
| US management consulting | 4.66 | 0.58 | 1.2 | 1.3 (2025: −0.1; 2026H1: −0.6) |
| US data processing 518210 | 0.85 | 0.66 | 0.9 | 1.8 |
| WPU4561 | 1.10 | 0.49 | 1.3 | 9.5 |
| ECI wages, prof./sci./tech. | 1.19 | 0.51 | 2.8 | 3.5 |
| BEA software price | 0.53 | 0.50 | −2.1 | −0.7 |

- **WPU4561.** The 2023–26 jump reflects software vendors repricing maintenance (e.g. +29 in 2024Q4).
- **Consulting price minus ECI.** In 2025 it was −3.4, against a −1.6 baseline. The gap is under 1 s.d.
- **UK J62.** It fell to about −1% in 2025Q2–Q3, then rose to +5% by 2026Q2.
- **Correlation with the Indian firms' median gR** (2015–22, excluding COVID):
  - US management consulting: 0.54
  - UK J62: 0.44
  - WPU4561: 0.23
  - Wage indices: 0.43–0.79. This is a common cycle.

## 5. Predicted signs

Notation: a T&M-priced index measures p/a; an output price measures p; w is wages.

| scenario | p/a (T&M index) | p (output price) | wages |
|--|--|--|--|
| S1 | softens mildly (discounting, realization) | same direction as p/a | lag |
| S2 | rises relative to w | flat | — |
| S3 | flat relative to w | falls relative to w | — |
| S4 | US/UK domestic indices barely move | — | — |

**What would separate S1 from S3:** an output-price index falling relative to both hourly rates and computer-occupation wages. In other words, p divided by p/a (which equals a) falls. Under S1, p and p/a fall together and wages follow.

**Confounds:** discount and realization cycles, quality adjustment, and the absence of any official p series to compare against.

## 6. Verdict: no

- **Keep as controls:** UK J62, ECI and CES as cyclical controls for p/a and wages. They are already scripted (about 0.25 RA-days).
- **Only route to p:** ONS SPPI microdata via the Secure Research Service, with the pricing method flagged per quote. This takes months and is a long shot.

## Files

- `01_fetch_build.py`
- `02_gsa_calc_check.py`
- `price_indices_quarterly.csv`
- `noise_stats.csv`
- `price_minus_wage_stats.csv`
- `corr_with_indian_gR.csv`
- `bea_software_prices_annual.csv`
- `gsa_calc_vendor_check.csv`
- `run_log.txt`
