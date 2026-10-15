# FINDINGS — M4: junior vs experienced employment growth, s_J − s_E (2023–2026)

*Saved by the orchestrator from the subagent's report (subagents can't write report files). Measurement M4 in ESTIMATION_PLAN.md. Date: 2026-10-14.*

**Vintage.** Firm data run to FY26 (year ending March 2026) and PLFS data to CY2025. Both predate the summer-2026 step change in coding agents, so these results describe the period before it.

**Sign convention.** The model gives g_J − g_E = −(s_J − s_E). Every estimate below is s_J − s_E in percentage points per year; a positive number means AI hits juniors harder. Changes are measured in log points of the junior/experienced ratio, using the identity Δlogit(under-30 share) = g_J − g_E. Firm and sector scopes are never mixed.

## 1. Headline

| scope | preferred range | central | verdict |
|--|--|--|--|
| Firm: top six, under-30 vs 30+ | −2 to +3 | ~0 to +1 | Not distinguishable from 0 once the FY22–23 hiring boom is netted out |
| Sector: PLFS NIC 62+63, 21–25 (or 21–30) vs 31–40 (or 31–60) | +1 to +3 | ~+2 | Suggestive; 90% CI includes 0 |

**Breakdown points**
- **Firm scope.** The boom need only explain 23–28% of the post-FY23 relative junior decline (23% headcount-weighted, 28% simple mean). Equivalently, 34–47% of the FY21–23 junior bump must have unwound by FY25/26. Attrition of 20–30% a year alone would unwind 49–66% over three years. So the firm-scope gap is not robust.
- **Sector scope.** Confounders would have to explain all of a relative junior decline of 1.4–1.9 log points a year. PLFS shows no boom-era bulge of juniors, but the CI already includes 0.

## 2. Mechanism: the boom unwound through the hiring mix, not ageing out

**Infosys stock-flow** (`stockflow.py`)
- The under-30 headcount reconciles exactly over FY16–22: stock + hires − exits − net crossings of age 30.
- From FY23 it no longer reconciles: 29–38k exits a year (about 10% of headcount) are missing, consistent with reported turnover becoming voluntary-only.
- Allocating those missing exits in proportion to reported exits, the share of under-30s crossing 30 is 7.2% a year in FY24–26, against 8.5% in FY16–21. So there is no excess ageing out.
- Extreme allocations give bounds of 0.4% and 19% a year; neither is plausible.

**Infosys boom-cohort check** (`infosys_boom_cohort_ageing.csv`)
- Excess under-30 hiring in FY22–23 was about 103k freshers and about 9k other under-30 hires.
- Assumptions: freshers are 22 at hire; laterals are aged 23–29; 15–25% of each cohort exits per year.
- Under these assumptions, boom cohorts produce only 0.5–1.1k extra crossings of age 30 a year in FY24–26, about 0.3–0.5% of FY23 under-30 headcount.
- **The fresher bulge reaches 30 in FY30–31,** with about 7–19k extra crossings in FY30. That will mechanically depress under-30 shares then. Part B must not read it as AI.

**What changed instead: the hiring mix (Infosys, FY24–26 vs FY16–21 average)**
- Under-30 hires: 42.3k vs 43.1k (flat).
- 30+ hires: 18.7k vs 11.3k (+65%).
- Under-30 share of hires: 68% vs 79%.

**Other firms**
- Ageing-out rates did not rise where they can be measured: Wipro 18.7% vs 17.3%; LTIM 12.1% vs Mindtree 12.4%.
- The share of exits missing from reported turnover is 5–10% of headcount at HCL, Wipro, LTIM and Persistent, and over 30% at TechM and Hexaware, where reported exits are voluntary-only.

## 3. Estimates by design

All estimates are in `estimates_summary.csv`.

### Firm scope

**Design 1: stock-flow** (`design1_estimates.csv`)
- Method: the FY24–26 gap, with excess ageing out added back, minus the firm's own pre-period gap.
- Results (without / with the ageing adjustment):
  - Infosys: +2.7 / +5.6.
  - Wipro: +1.9 / −1.0 (pre-period FY20–21 only).
  - LTIM vs Mindtree: +7.7 / +8.2 (a change of entity).
- Leans high: it doesn't net out hiring pulled forward into FY22–23 (work done by reducing the bench).

**Design 2: counterfactual trend** (`design2_*.csv`)
- Pre-trend, from OLS on logit(under-30 share) through FY21: mean of the large six −6.5 log points a year.

| counterfactual | mean | headcount-weighted |
|--|--|--|
| FY23 to latest, no boom correction | +2.5 (firm range −3.3 TechM to +11.5 LTIM) | +2.2 |
| Boom bump decays passively, 20%/yr | +0.1 | −0.4 |
| Boom bump decays passively, 30%/yr | −0.8 | −1.3 |
| Full cycle, FY21 to latest | −1.8 | −2.1 |

- Assumptions: the FY15–21 trend would have continued, and the FY22–23 bump was temporary.
- With no trend (a stable pyramid), the full-cycle figure is +4.7. But that counterfactual is contradicted by FY14–21, when the under-30 share fell at 5 of 6 firms.
- Share of the boom bump that must unwind for the gap to be zero:
  - Infosys 0.29 and HCL 0.11: the boom can explain their decline.
  - TCS 3.7: the boom can't explain it (full-cycle gap +1.2).
  - LTIM: no bump, so +11.5 is unexplained; the merger is the likely confounder.
  - Wipro and TechM: no gap to explain.

**Design 2b: growth-conditioned trend** (`design2b_*.csv`)
- Method: fixed-effects regression of the change in logit share on revenue growth and its lag, estimated over years up to FY23 (21 firm-years; coefficient 0.79, SE 0.47).
- FY24–26 residual: **+0.9 (90% CI −4.5 to +6.4)**.
- Firm residuals: HCL +12.6, TCS +7.2, Infosys +2.0, Wipro −4.5, TechM −10.5.

**Design 3: cross-firm** (`design3_*.csv`)
- Regressing the change from FY23 to latest on boom size across 9 firms: slope −0.35 (SE 0.16). Bigger booms were followed by bigger declines.
- Intercept −8.45 (SE 2.62). Net of the pre-trend this gives **+1.2 to +1.9 (90% CI about ±4.3)**.
- Large-firm-only specifications are uninformative.

**Infosys job levels: JL3 and below vs the rest** (`infosys_joblevel_trend.csv`)
- Pre-trend −6.9 log points a year.
- FY23–26: +16.2. This is inflated because the boom cohort is being promoted out of JL3, which is ageing out in job-level terms. 130% of the bump would have to unwind.
- Full cycle FY21–26: +2.2.

**Mid-tier** (outside top-six scope; no pre-trend)
- Persistent: −29 log points a year raw from FY23; −14 a year over FY22–26.
- Mphasis: −16 a year from FY23; −2 a year over FY21–25.
- Hexaware: about 0.
- Coforge: only two years of data.

### Sector scope

**Design 4: PLFS age gap within NIC 62+63** (`plfs_gap.py`, `plfs_gap_*.csv`)
- Aggregate tables only. The SE combines the two bands' SEs and ignores their covariance, which is conservative.
- **Preferred: mean of 2023-24 and CY2025 vs mean of 2017-18 to 2020-21, no trend**
  - 21–25 vs 31–40: **+1.4 (90% CI −2.2 to 5.0)**.
  - 21–30 vs 31–60: **+1.9 (−0.7 to 4.4)**. This comparison is robust to the boom, because the 2021–23 intake is still under 30 in CY2025.
- Single-window variants are noisy:

| window | 21–25 vs 31–40 | 21–30 vs 31–60 |
|--|--|--|
| 2020-21 → CY2025, no trend | +5.3 [0.1, 10.4] | +3.8 [−0.2, 7.9] |
| same, net of 2017–21 pre-trend | +16.4 [6.0, 26.8] | +5.4 [−2.5, 13.4] |
| 2022-23 → CY2025, no trend | −6.2 [−16.4, 4.0] | −6.1 [−13.6, 1.5] |
| same, net of pre-trend | +4.9 [−8.7, 18.5] | −4.4 [−14.6, 5.7] |

- The sector pre-trend (+11 log points a year, SE 5.5) reflects the 2017–21 expansion and shouldn't be extrapolated.
- Assumptions:
  - Without AI, the age mix would have stayed at its 2017–21 average.
  - The CY2025 survey redesign is neutral to the age mix within the industry.
  - Only 2023-24 is used, not CY2024, because the two share Jan–Jun 2024 records.
- **Not done: a difference-in-differences against graduates in other industries.** It needs one added cut in `round3/plfs/analyze.py`: graduate workers outside NIC 62/63, by age band.

**Design 5: relative pay** (`plfs_relative_pay*.csv`)
- Mean pay of ages 21–25 relative to 31–40 among IT regular wage workers: 0.643 (2020-21), 0.587 (2022-23), 0.583 (CY2024), 0.523 (CY2025). For all graduates the ratio is flat at 0.53–0.58.
- Difference-in-differences, IT minus all graduates: **−5.4 log points a year (SE 1.85)** over 2020-21 → CY2025. Over 2022-23 → CY2025 it is −4.6 (SE 4.1).
- Medians don't confirm this: 0.553 (2022-23), 0.560 (CY2025).
- Interpretation: relative junior pay falls while relative junior quantity is flat or falling, and the supply of young graduates is rising. That points to a relative fall in demand for juniors. This is directional only; without an elasticity it can't be converted into s_J − s_E.
- Firm Rule-5 medians measure workforce composition, not price, so they add no independent test.

## 4. Caveats
- Firm age data come from voluntary GRI tables with varying scope:
  - TCS: India only, read off charts.
  - Persistent and Coforge: include contract staff.
  - Hexaware: calendar years.
- LTIM before FY23 is LTI + Mindtree.
- From about FY23, turnover is voluntary-only at most firms, so the stock-flow relies on allocating the missing exits.
- Pre-periods are short (Wipro FY19–21; HCL has two data points).
- Two or three post-FY23 years give low power. The firm spread (−3 to +12) exceeds any pooled estimate.
- PLFS records age, not experience, so under-30 is not the same as fresher.

## Files
- **Scripts:** `stockflow.py`, `trend_xfirm.py`, `plfs_gap.py`, `make_summary.py` (run in that order).
- **Design 1:** `stockflow_firm_year.csv`, `stockflow_summary.csv`, `design1_estimates.csv`, `infosys_boom_cohort_ageing.csv`.
- **Design 2:** `design2_firm_trend.csv`, `design2_pooled_large.csv`.
- **Design 2b:** `design2b_growth_conditioned.csv`, `design2b_coefs.csv`.
- **Design 3:** `design3_crossfirm.csv`, `design3_regressions.csv`.
- **Infosys job levels:** `infosys_joblevel_trend.csv`.
- **PLFS (designs 4–5):** `plfs_gap_by_round.csv`, `plfs_gap_estimates.csv`, `plfs_gap_multiround.csv`, `plfs_relative_pay.csv`, `plfs_relative_pay_estimates.csv`.
- **Summary:** `estimates_summary.csv`.
