# FINDINGS — M1: change in the revenue-per-worker residual, measuring (1−φ)s̄

*Saved by the orchestrator from the subagent's report; subagents can't write report files. Date: 2026-10-14. Run order: `m1_firm.py`, then `m1_sector_pi.py`, then `m1_summary.py`.*

## 1. Headline

**Firm scope: (1−φ)s̄ in FY24–26 is about +1 pp/yr, and the 95% CI includes 0.**
- Point estimates range from −0.2 to +2.0 across specifications.
- The widest 95% CI is −1.8 to +4.2.
- For the top six, with TCS and HCLTech bounded rather than estimated, the range is −0.15 to +2.7.

**Sector scope is illustrative only.** Exports per PLFS worker rise by 10–14 pp/yr after 2022-23, but that reflects breaks in the PLFS employment series.

**π, non-AI price drift: no evidence that it fell.** The bound on Δπ is −1.0 to +0.5 pp/yr. Applying it widens the firm-scope range to −0.7 to +3.0.

**What this rules out.** Under M1's assumption, the data reject 4%/yr of retained savings (the note's illustrative S2 case) on every baseline except the full FY16–23 one. They do not reject 0.

## 2. Firm-scope method

The definitions reproduce `scripts/final/tables_figures.py`. Table B is reproduced exactly (1.098, 2.103, 1.318; see `replication_check.csv`).

**Series variants** (all in `firm_year_panel.csv`):
- **Pilot:** constant-currency (cc) revenue only.
- **Imputed cc:** TechM (FY17–20) and the LTI group (FY17–23) don't report cc revenue for those years. For them, cc revenue = USD revenue minus that year's average USD-minus-cc gap at the firms that report both (`fx_gap_by_fy.csv`).
- **Infosys trainee fix A:** use the utilisation series that includes trainees.
- **Infosys trainee fix B:** subtract implied trainees from headcount.

**Estimators:**
- **Pooled:** firm-years pooled, in the style of Table B.
- **Within-firm:** each firm's own change from its baseline, requiring at least 2 baseline years.
- **Year-cluster t (preferred):** the firm-demeaned residual is averaged by year, so shocks common to all firms in a year stay together. The CI is a t-interval over the year averages.

**Why the preferred estimator:**
- Year shocks dominate: FY21 is −4.5 and FY23 is +2.9.
- Persistence in year averages is low: lag-1 autocorrelation is −0.07 to 0.22.

**Two checks:**
- **The D27 parametric noise model overstates uncertainty.** It implies a residual SD of 4.2 against 3.4 in the data, plus persistence the data don't show. Its SE is 2.8–3.5.
- **Two-way bootstrap** over firms and years.

## 3. Firm-scope results (4 firms with utilisation)

From `m1_firm_estimates.csv`, in pp/yr.

| series | baseline | within-firm Δ | year-cluster 95% CI | two-way bootstrap 95% | D27 SE | firms' own changes |
|---|---|---|---|---|---|---|
| pilot | FY16–23 | +0.6 | −2.3, +3.5 | −4.1, +5.8 | 3.1 | Infosys +2.3, TechM −0.3, Wipro −0.1 |
| pilot | excl. FY21 | −1.4 | −2.7, 0.0 | −4.6, +3.4 | 3.1 | Infosys +2.2, TechM −1.4, Wipro −4.9 |
| preferred* | FY16–23 | +1.3 | −1.7, +4.2 | −2.5, +5.0 | 2.8 | Infosys +1.5, LTI +3.4, TechM 0.0, Wipro −0.1 |
| preferred* | excl. FY21 | −0.2 | −1.8, +1.5 | −3.3, +2.6 | 2.8 | Infosys +1.4, LTI +2.5, TechM −0.4, Wipro −4.9 |
| preferred* | excl. FY22–23 | +2.0 | +0.1, +3.9 | −0.2, +4.5 | 3.3 | Wipro drops out |
| preferred* | FY16–20 | +1.4 | +0.1, +2.8 | −0.4, +2.8 | 3.5 | Wipro drops out |

\*Preferred = imputed cc + Infosys trainee fix A.

Pooled estimates are lower (−0.2 to +1.1), because their baseline includes HCLTech's high FY16–19 residuals.

**Sensitivity:**
- **Excluding FY21** lowers the estimate by about 1.5 pp. Wipro's FY21 value of −10.5 drives this.
- **Excluding the boom years** (FY22–23, or using a FY16–20 baseline) raises it to +1.4 to +2.0.
- **The Infosys trainee fix** brings Infosys's FY24 value down from +6.6 to +1.6. That moves Infosys's own change by 0.4–0.8 pp and the overall average by 0.1–0.3 pp.
- **Imputing cc revenue** adds LTI and raises the estimate by about 0.7 pp.

## 4. TCS and HCLTech: bounds

From `m1_tcs_hcl_bounds.csv`. Neither firm reports utilisation, so:

Δresidual = Δ(revenue per employee, cc) − Δutilisation, with Δutilisation bounded by the range seen at the four peers.

| baseline | TCS Δrpe | HCLTech Δrpe | peer Δutil range | TCS Δresidual | HCLTech Δresidual |
|---|---|---|---|---|---|
| FY16–23 | +2.4 | +2.8 | −1.4 to +1.0 | +1.4 to +3.8 | +1.8 to +4.2 |
| excl. FY21 | +1.65 | +1.9 | −1.1 to +1.55 | +0.1 to +2.75 | +0.35 to +3.0 |
| excl. FY22–23 | +2.1 | +1.2 | −2.1 to 0.0 | +2.1 to +4.2 | +1.2 to +3.3 |
| FY16–20 | +1.05 | −0.4 | −1.8 to +0.5 | +0.5 to +2.8 | −0.9 to +1.4 |

**Top six, equal weight** (`m1_top6_range.csv`):

| baseline | range |
|---|---|
| FY16–23 | +1.3 to +2.1 |
| excl. FY21 | −0.15 to +0.7 |
| excl. FY22–23 | +1.85 to +2.7 |
| FY16–20 | +0.7 to +1.7 |

Weighting by revenue instead gives −0.1 to +3.1.

## 5. Sector scope: not usable

From `sector_rpw_by_round.csv` and `sector_m1_changes.csv`.

| windows | exports growth, pre / post | employment growth, pre / post | Δ residual (95% CI) |
|---|---|---|---|
| 2017-18→2022-23 vs 2022-23→CY2025 | 12.9 / 10.8 | 16.9 / 1.6 | +13.2 (9.0, 17.4) |
| post window ends CY2024 | | | +10.9 (0.1, 21.8) |
| both windows within one survey design | | | +22.0 (−18.9, 62.8) |
| RBI total / NIC 62+63+822 | | | +12.2 (7.8, 16.5) |

Reasons it can't be used:
- **The denominator has breaks.** The 2021-22 strata change produced a 44% jump in employment, there was another strata change in 2023-24, and the 2025 redesign. Baseline employment growth of 16.9%/yr exceeds export growth, which is implausible.
- **Exports aren't total revenue.**
- **GCC exports are valued cost-plus**, so they track wages. Private-limited firms' share of exports rose from 56.1% to 60.8% over FY23–26.
- **The two export sources disagree:** BoP shows 10.8%/yr, the RBI survey 6.0%/yr.
- **There is no utilisation adjustment.**

## 6. π: non-AI price drift

From `pi_wage_evidence.csv` and `pi_price_index_evidence.csv`.

**Wages**
- **PLFS mean earnings in USD, IT (NIC 62/63), change in growth after 2022-23:**
  - age 26–30: Δ +2.3 (SE 2.4);
  - age 31–40: Δ −0.5 (SE 3.2);
  - age 21–25: Δ −5.3 (SE 4.2), across the 2025 survey break.
- **Firm employee cost per head in USD, change in growth (FY24–26 vs FY17–23):** HCL +5.4, TCS +3.8, TechM +0.7, Wipro +0.45. These numbers are pushed up mechanically when firms hire fewer freshers.

**Rate indices, change in growth after 2023 (pp/yr)**

| index | vs 2016–22 | vs 2016–19 |
|---|---|---|
| UK SPPI J62 (HR6L) | +0.4 | +1.0 |
| US PPI, management consulting | +0.2 | +1.8 |
| US ECI, professional services | +0.6 | +1.2 |

**What firms said on calls**
- FY22–23: explicit rate increases (HCLTech, LTIMindtree).
- After 2023: pricing described as "stable", with competitive intensity in large deals.
- Infosys: realisation up 3.6% over 9M FY25, and a 3.5% benefit from Project Maximus, its non-AI pricing programme. That is a non-AI price rise.

**Bound: Δπ between −1.0 and +0.5 pp/yr.** This is a judgement, not an estimate.

**An uncorrected bias that pushes M1 down.** Subcontracting cost fell by 1.2–3.9 pp of revenue at all six firms between FY23 and the FY24–26 average. Bringing that work in-house adds own staff without adding revenue. That could lower M1 by about 1 pp/yr, more at TCS and TechM. This is an order-of-magnitude estimate that rests on assumptions.

## 7. Breakdown points

From `m1_summary.csv`. Each column is the shift in π+ρ, in pp/yr, needed to reach that outcome.

| specification | estimate | to reach 0 | to make CI exclude 0 | to reach 4 |
|---|---|---|---|---|
| FY16–23 | +1.3 | +1.3 | −1.7 | −2.7 |
| excl. FY21 | −0.2 | already ≤ 0 | −1.8 | −4.2 |
| FY16–20 | +1.4 | +1.4 | already excludes 0 | −2.6 |
| top six FY16–23 (midpoint) | +1.6 | +1.6 | n/a | −2.4 |

## 8. Input to s̄ = M1 + M2

| scope | (1−φ)s̄, pp/yr |
|---|---|
| Firm, 4 firms (Infosys, Wipro, TechM, LTI) | about +1.0; specification range −0.2 to +2.0; 95% CI −1.8 to +4.2; −0.7 to +3.0 with the π bound |
| Firm, top six (TCS and HCLTech bounded) | −0.15 to +2.7; −0.65 to +3.7 with the π bound |
| Sector | Not usable |

## Files

**Scripts:**
- `m1_firm.py`
- `m1_sector_pi.py`
- `m1_summary.py`

**Data and checks:**
- `firm_year_panel.csv`
- `fx_gap_by_fy.csv`
- `replication_check.csv`
- `noise_check.csv`

**Results:**
- `m1_firm_estimates.csv`
- `m1_tcs_hcl_bounds.csv`
- `m1_top6_range.csv`
- `m1_summary.csv`
- `sector_rpw_by_round.csv`
- `sector_m1_changes.csv`
- `pi_wage_evidence.csv`
- `pi_price_index_evidence.csv`
