# FINDINGS — R2: M1 at top-six scope, corrected for the subcontracting bias

*Saved by the orchestrator from the subagent's report (subagents can't write report files). Date: 2026-10-15. Run order: `scan_subcon_statements.py` → `screen_subcon_statements.py` → `m1_scope_subcon.py`. All figures are pp/yr (log points).*

## 1. Headline

The comparison below uses the scope and baseline that match M3: top six, equal weights, FY16–20 baseline.

| | first pass | top six, uncorrected | top six, corrected for subcontracting |
|--|--|--|--|
| M1 = (1−φ)s̄ | ≈ 1.0 (4 firms) | 1.0 (0.7–1.6) | **2.1** (1.8–2.4 across k; 1.5–3.0 with the utilisation bound) |
| s̄ = M1 + M2 | ≈ 1.2 (0–2.5) | 1.2 (0.7–2.2) | **2.3** (2.0–2.6 across k; 1.5–3.6 with bounds; −0.8 to 7.1 with 95% sampling error) |
| AI share of the 8.3 pp slowdown | ≈ 15% | 15% (9–27%) | **28%** (24–31%; 18–43%; −10% to 86%) |
| φ = M2/s̄ | 0.15 | 0.17 | **≈ 0.09** (0.01–0.39; unidentified once sampling error is included) |

Here k is the conversion factor from subcontracting cost to revenue delivered by subcontractors (§4).

**R1 caveat:** the "share of 8.3 pp" depends on the baseline. R1 recommends reporting s̄ in pp/yr instead.

## 2. Method for top-six M1

- **Estimator.** A year-cluster estimator over six firms.
  - The measured firms (Infosys, Wipro, TechM, LTI) use the preferred residual. This reproduces `m1_firm_estimates.csv` exactly.
  - TCS and HCLTech use revenue per employee (cc) minus the assumed change in utilisation, applied in the post years only. Their sampling noise is included.
- **Weights.** Equal (1/6), or FY26 USD revenue: TCS 35%, Infosys 23%, HCLTech 17%, Wipro 12%, TechM 7%, LTI 6%.
- **Uncertainty.** TCS and HCLTech's change in utilisation is bounded by the range observed at peers. Intervals are reported three ways:
  - bound: the midpoints at the two ends of the utilisation range;
  - union95: the worst-case 95% interval across that range;
  - MC95: a Monte Carlo interval with uniform utilisation and t-distributed sampling error.
- **Sample gaps.** Wipro drops out of the excl. FY22–23 and FY16–20 windows.

## 3. Top-six M1, uncorrected (`m1_top6.csv`)

| baseline | weights | central | bound | union95 | MC95 | 4 firms |
|--|--|--|--|--|--|--|
| FY16–23 | equal | 1.39 | 1.12–1.93 | −2.08 to 5.14 | −1.69 to 4.70 | 1.27 |
| FY16–23 | revenue | 1.62 | 1.20–2.44 | −2.06 to 5.70 | −1.53 to 5.12 | 1.16 |
| excl. FY21 | equal | 0.07 | −0.28–0.60 | −2.42 to 2.74 | −1.99 to 2.32 | −0.18 |
| excl. FY21 | revenue | 0.42 | −0.13–1.25 | −2.55 to 3.66 | −1.89 to 3.04 | −0.18 |
| excl. FY22–23 | equal | 1.97 | 1.75–2.59 | −1.28 to 5.61 | −0.85 to 5.19 | 2.04 |
| excl. FY22–23 | revenue | 2.12 | 1.80–3.04 | −1.54 to 6.38 | −0.94 to 5.82 | 1.92 |
| FY16–20 | equal | 1.02 | 0.72–1.63 | −0.73 to 3.08 | −0.31 to 2.67 | 1.43 |
| FY16–20 | revenue | 1.12 | 0.68–2.02 | −1.37 to 4.06 | −0.78 to 3.45 | 1.63 |

- Changing scope moves the central estimate by −0.4 to +0.5.
- No top-six 95% interval excludes 0. The four-firm FY16–20 and excl. FY22–23 intervals did exclude 0; adding TCS and HCLTech removes that.

## 4. The subcontracting correction

**Why it's needed.** Revenue per employee counts revenue delivered by subcontractors but not their headcount. When subcontracting falls, revenue per own employee falls even though own-staff productivity hasn't changed. That understates M1.

**The correction.**

corr = −100·[ln(1 + c_s,t/(c_e·m)) − ln(1 + c_s,t−1/(c_e·m))] ≈ −Δc_s·k, where k = 1/(c_e·m)

- c_s = subcontracting cost as a share of revenue (`audit/subcontracting_series.csv`).
- c_e = employee cost as a share of revenue: TCS 0.552, HCLTech 0.526, Wipro 0.548, TechM 0.527, Infosys 0.533, LTI 0.601. LTI's figure comes from Mindtree's FY22 accounts only.
- m = subcontractor cost relative to own staff.
  - Lower bound m ≥ 1: Wipro said subcontractors are "typically about 30% higher than your own employees", and TechM also said they cost more.
  - m_mid = 1.3.
  - Upper bound m ≤ 1/c_e, which is zero gross margin on subcontracted work.
  - HCLTech's FY22 changes in cost per added contractor imply 1.5–2.2× (an upper bound).
  - Together these give k ∈ [1.0, 1.9], with k_mid ≈ 1.4.

**Changes in c_s and the resulting correction** (`subcon_corrections_firm_year.csv`; k_mid):

| firm | Δc_s FY24 / FY25 / FY26 (pp of revenue) | correction FY24 / FY25 / FY26 | Δ vs own baseline, FY16–23 / FY16–20 |
|--|--|--|--|
| TCS | −2.90 / −1.99 / +0.93 | +3.6 / +2.6 / −1.2 | +2.05 / +1.97 |
| TechM | −2.15 / −1.85 / −0.28 | +2.6 / +2.3 / +0.4 | +2.02 / +2.14 |
| Infosys | −1.62 / −0.02 / +0.70 | +2.1 / 0.0 / −0.9 | +1.31 / +1.29 |
| LTI | −1.32 / −0.29 / +0.73 | +1.5 / +0.3 / −0.9 | +0.24 / +0.34 |
| Wipro | −1.26 / −0.24 / +0.38 | +1.5 / +0.3 / −0.5 | −0.38 / n.a. |
| HCLTech | −1.47 / −0.31 / +1.20 | +1.8 / +0.4 / −1.5 | −0.33 / −0.57 |

- **Where the bias sits.** Against each firm's own trend, it is concentrated at TCS, TechM and Infosys. HCLTech and Wipro were already cutting subcontracting before FY24.
- **FY26 reversal.** Subcontracting rose again in FY26 at 5 of 6 firms; TCS and Infosys both mentioned it on calls. Ignoring that would overstate M1 by 0.8–1.0.
- **FY27.** LTIMindtree's subcontracting was up about 320 bps YoY in Q1FY27 (an analyst's figure). Any FY27 update to M1 will be biased upward.

**Corrected top-six M1** (central at k_mid; range of centrals across k; bounds; union95):

| baseline | weights | k_mid | k range | bounds | union95 |
|--|--|--|--|--|--|
| FY16–23 | equal | 2.23 | 2.00–2.45 | 1.73–2.98 | −1.65 to 6.70 |
| FY16–23 | revenue | 2.70 | 2.40–2.98 | 1.98–3.81 | −1.58 to 7.83 |
| excl. FY21 | equal | 1.08 | 0.80–1.34 | 0.45–1.87 | −2.68 to 5.53 |
| excl. FY21 | revenue | 1.66 | 1.33–1.99 | 0.78–2.82 | −2.63 to 6.90 |
| excl. FY22–23 | equal | 2.86 | 2.62–3.10 | 2.40–3.72 | −0.54 to 6.90 |
| excl. FY22–23 | revenue | 3.18 | 2.90–3.47 | 2.57–4.38 | −0.86 to 8.19 |
| FY16–20 | equal | 2.10 | 1.80–2.38 | 1.50–2.99 | −0.86 to 5.93 |
| FY16–20 | revenue | 2.35 | 2.01–2.67 | 1.57–3.58 | −1.44 to 7.25 |

## 5. Recombination (`sbar_phi_ai_share.csv`)

**M2**, FY24–26 average:
- revenue-weighted: 0.18 (0.01–0.64; up to 1.28 with the bias bound);
- equal-weighted: 0.20 (0.03–0.59; up to 1.19).

**s̄**, equal weights, corrected at k_mid:

| baseline | s̄ | k range | bounds | wide | AI share of 8.3 pp |
|--|--|--|--|--|--|
| FY16–23 | 2.43 | 2.20–2.65 | 1.76–3.57 | −1.62 to 7.89 | 29% |
| excl. FY21 | 1.28 | 1.00–1.54 | 0.48–2.46 | −2.65 to 6.72 | 15% |
| excl. FY22–23 | 3.06 | 2.82–3.30 | 2.43–4.31 | −0.51 to 8.09 | 37% |
| **FY16–20** | **2.30** | 2.00–2.58 | 1.53–3.58 | −0.84 to 7.11 | **28%** |

- **Other variants, by baseline (FY16–23 / excl. FY21 / excl. FY22–23 / FY16–20):**
  - revenue-weighted, corrected: 2.87 / 1.84 / 3.36 / 2.52;
  - uncorrected, equal weights: 1.59 / 0.27 / 2.17 / 1.22.
- **φ:** 0.05–0.16 across variants; 0.09 on FY16–20 (0.01–0.39). It is unidentified once sampling error is included.
- **The two volume routes now reconcile only with an in-sourcing term.**
  - Revenue route: Δg_Q ≈ −6.9.
  - Employment route: −2.3 (s̄) − 6.9 (volume) + 1.1 (subcontracted work moved in-house) = −8.1, against −8.3 observed.
  - Δd ≈ −7 and the unexplained 3–4 pp are unchanged.

## 6. What changes from the first pass

1. **s̄ roughly doubles:** from ≈ 1.2 to ≈ 2.3 (1.5–3.6 within bounds; 1.0–3.4 across windows).
2. **AI share rises from about 15% to about 28%** (18–43%). Demand is still the majority.
3. **4%/yr retained is no longer rejected** in any window after the correction.
4. **Zero is not rejected** anywhere at top-six scope.
5. **Unchanged:** φ is small; Δd ≈ −7; the unexplained 3–4 pp; pass-through starts in FY27.
6. **New term:** in-sourcing added about +1.1 pp/yr to employment, partly offsetting the fall in demand. It reverses in FY26–27.

## 7. Breakdown points and caveats

- **Price vs volume.** If part of the fall in subcontracting cost was lower contractor rates rather than fewer contractors, the correction is too large.
  - FY16–20, equal weights: 59% of the fall would have to be price for the AI share to drop below 20%.
  - FY16–23: 92% would have to be price.
- **What the cost lines contain.**
  - HCLTech's line includes outsourced work as well as contractors.
  - TCS's line includes SG&A consultants. Its cost-of-revenue-only line moves the same way (−3.93 vs −3.96 pp).
- **Headcount assumption.** Reported headcount is assumed to exclude subcontractors. HCLTech states this explicitly; LTI and Mindtree are silent.
- **Missing correction years.** LTI's subcontracting series starts in FY22, and HCLTech's FY16–17 is missing. Both are given a zero correction in those years.
- **Fixed inputs.** c_e is fixed per firm. In-sourced staff are assumed to be billed at normal utilisation.
- **Vintage.** All data predate the summer-2026 capability step change.

## 8. Files
**Scripts:**
- `scan_subcon_statements.py`
- `screen_subcon_statements.py`
- `m1_scope_subcon.py`

**Outputs:**
- `subcon_statement_candidates.csv`
- `subcon_statements_screened.csv`
- `replication_4firm.csv`
- `employee_cost_share.csv`
- `subcon_corrections_firm_year.csv`
- `subcon_correction_summary.csv`
- `subcon_fy26_and_breakdown.csv`
- `m1_top6.csv`
- `sbar_phi_ai_share.csv`
