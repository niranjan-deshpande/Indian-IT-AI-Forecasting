# R1: How sensitive is the Part A decomposition to the baseline? (top six, FY24–26)

*Saved by the orchestrator from the subagent's report (subagents can't write report files). Date: 2026-10-15.*

- Script: `r1_baseline.py`. It reads `output/final/table_A*.csv`, `data/corrected/*_final.csv` and `round4/demand_shift/d_bounds.csv`.
- Units: growth is log points × 100, using table_A definitions. Headcount is average-based; revenue is in constant currency (cc) unless stated.
- "Actual" means the FY24–26 mean.
- Deltas are averaged over the firms that have both an actual and a counterfactual value ("matched"). Row a0 reproduces the synthesis.

## 1. Counterfactuals

What each counterfactual assumes FY24–26 growth would have been without the slowdown:

| id | counterfactual |
|--|--|
| a0 / a | FY16–20 mean growth. a0 uses the table_A group rows; a uses matched firms. |
| b0 / b | FY16–23 mean growth. This includes the FY21 dip and the FY22–23 boom. |
| c | Level trend. The FY16–20 trend is extended from the FY20 level. Counterfactual growth is whatever gets back to that path by FY26: 2·g₀ − (sum of FY21–23 growth)/3. |
| c_fit | As c, but the trend is an OLS fit to FY15/16–FY20 log levels. |
| c21 | As c, but anchored at FY21. The COVID dip is treated as permanent. |
| d | The FY16–20 mean, decelerated by 7 × a slope. The slope comes from FY12–20, TCS and Infosys only, using USD revenue. |
| d_cc / d_fe / d13 | Variants of d: the cc slope; a firm-fixed-effects slope across all firms; a FY13–20 window. |
| e | Difference-in-differences: the FY16–20 mean plus the change seen at Accenture and Cognizant. e_acn and e_ctsh use one comparator each. |

## 2. Results

Assumptions: s̄ = 1.2; Δd ≈ Δg_Q; M5's measured demand shift = −3.1 (range −7.3 to +0.1).

| cf | Δg_L | Δg_R (cc) | Δg_Q, headcount route (s̄ 0 to 2.5) | Δg_Q, revenue route | AI share (s̄ 1.2 / 2.5) | Residual, headcount route [range] | Residual, revenue route |
|--|--|--|--|--|--|--|--|
| a0 | −8.34 | −7.10 | −7.1 (−8.3 to −5.8) | −6.9 | 14% / 30% | −4.0 [−8.5, +1.5] | −3.8 |
| a | −7.77 | −7.16 | −6.6 | −7.0 | 15% / 32% | −3.5 [−7.9, +2.1] | −3.9 |
| b0 | −10.10 | −7.54 | −8.9 | −7.3 | 12% / 25% | −5.8 [−10.2, −0.3] | −4.2 |
| b | −10.61 | −8.15 | −9.4 | −8.0 | 11% / 24% | −6.3 [−10.8, −0.8] | −4.9 |
| c | −2.95 | −5.71 | −1.8 (−3.0 to −0.5) | −5.5 | 41% / 85% | +1.4 [−3.1, +6.9] | −2.4 |
| c_fit | −3.02 | −5.19 | −1.8 | −5.0 | 40% / 83% | +1.3 | −1.9 |
| c21 | −1.65 | −3.04 | −0.5 | −2.8 | 73% / 152% | +2.7 | +0.3 |
| d | −0.81 | +0.16 | +0.4 | +0.4 | 149% / 310% | +3.5 | +3.5 |
| d_cc | −0.81 | −4.58 | +0.4 | −4.4 | 149% | +3.5 | −1.3 |
| d_fe | −2.07 | −0.29 | −0.9 | −0.1 | 58% / 121% | +2.2 | +3.0 |
| d13 | −4.06 | −3.08 | −2.9 | −2.9 | 30% / 62% | +0.2 | +0.2 |
| e | −1.53 | −3.07 | −0.3 (−1.5 to +1.0) | −2.9 | 78%* / 163%* | +0.7† | −1.9† |
| e_acn | −2.27 | −3.11 | −1.1 | −2.9 | 53%* | −0.1† | −1.9† |
| e_ctsh | −0.80 | −3.03 | +0.4 | −2.8 | 150%* | +1.4† | −1.8† |

\* Upper bound. This assumes s̄ is specific to the Indian firms. If AI replacement affects all vendors equally, it cancels out against the comparators.

† Common shocks cancel out against the comparators. The only measured shift left to compare is the GCC channel: −1.0 (range −2.5 to 0).

**Samples.** Headcount covers 5 firms (Wipro has no FY16–20 baseline). cc revenue covers 4 (TCS, Infosys, HCLTech, Wipro).

**Files.** `r1_summary.csv`, `r1_decomposition.csv`, `r1_counterfactuals.csv`, `r1_firm_counterfactuals.csv`, `r1_level_gaps_group.csv`, `r1_comparators_levels.csv`, `r1_deceleration_slope.csv`.

## 3. Findings

1. **The decomposition is very sensitive to the baseline.**
   - Only the growth-rate means (a, b) give an 8–10 pp headcount slowdown.
   - Level, deceleration and comparator baselines give about 1–4 pp.
   - Baseline b, which includes the boom, makes the residual larger.

2. **"AI's share is small" does not survive.**
   - The share is under 30% only under a and b.
   - Under c it is about 40% (0–85%). Under the deceleration and comparator baselines it ranges from 30% to over 100%.
   - What survives is an absolute claim: s̄ ≈ 1.2 pp/yr (0–2.5) is smaller than the revenue-route volume shortfall (−2.8 to −8.0) under every baseline except the steep deceleration.

3. **A level baseline also undercuts s̄ itself.**
   - Revenue per employee (cc) was 10.9 log points below its FY16–20 trend at FY23, and still 10.6 below at FY26.
   - FY24–26 growth in revenue per employee (+2.6) was no faster than in FY16–20 (+2.5).
   - If levels are the right counterfactual for M1 too, there is no room for a positive s̄ beyond noise. This is indicative only, because the firm sets are unbalanced.

4. **The hangover explains the employment residual but not the revenue residual.**
   - On the headcount route, the residual is +1.4 under c, so it is over-explained.
   - On the revenue route, which has no s̄ term, it is −2.4 under c and −1.9 under c_fit. It is about 0 only under c21 (+0.3) or d13 (+0.2).

5. **The FY22–23 boom overshoot was in staff, not revenue.**
   - By FY23, against trend: headcount +14.1 log points, cc revenue +3.5.
   - By FY26: headcount −11.0, cc revenue −17.8.
   - The pull-forward story explains the headcount slowdown, but not why cc revenue is about 16% below its pre-COVID path.
   - Accenture overshot in both (+13.9 / +14.0) and is back on trend (−0.9 / +0.6).
   - Cognizant did not boom, and still slowed 7 pp.

6. **Against the comparators there is an India-specific revenue gap.**
   - Indian firms minus comparators: headcount −1.5 (range −0.8 to −2.3); cc revenue −3.1, almost the same with either comparator.
   - So about 80% of the headcount slowdown and about 57% of the revenue slowdown is common to global IT services.
   - The India-specific gap is about −3 pp/yr, or about −1.9 net of GCCs. Candidates: share loss, Europe, or client-side AI substitution concentrated in the Indian firms' work mix.
   - Revenue per employee accelerated more at the comparators (+1.5 and +2.8) than at the Indian firms (+0.6 to +1.2). There is no sign the Indian firms gained more AI productivity.

7. **The deceleration counterfactual is fragile.**
   - FY12–20 slopes (−0.5 to −1.0 pp/yr) come from the post-GFC slowdown from 15–20% growth.
   - Within FY16–20 there is no deceleration: headcount +0.66 ± 0.60, cc revenue −0.31 ± 0.35.
   - Treat d13 as the reasonable case and d as an extreme.

8. **The two routes to volume agree only under growth-rate baselines.**
   - Under a and b they are within 0.4–1.5 pp. Under c, d and e they differ by 1.5–4.8 pp, so report the revenue route alongside.
   - USD revenue understates the slowdown by about 2 pp because of FX, so use cc.

9. **Composition matters at the margin.**
   - Matched firms give Δg_L −7.8, compared with table_A's −8.3.
   - HCLTech's FY16–20 baseline includes acquisitions, which inflates its level gap.

## 4. What survives every reasonable counterfactual (a, b, c, c_fit, c21, d13, e)
- s̄ ≈ 1.2 pp/yr (0–2.5), stated in absolute terms, is smaller than the revenue-route volume shortfall (−2.8 to −8.0).
- Top-six cc revenue growth fell by at least about 3 pp/yr against every counterfactual, and by about 3 pp/yr relative to Accenture and Cognizant.
- M5's range is wide enough that the residual's range includes 0 under every baseline except b. The "unexplained 3–4 pp" was never statistically established.

## 5. What does not survive
- "AI was 15% (0–30%) of the slowdown."
- "The slowdown was 8.3 pp." It is 1.5–4 pp under level, deceleration and comparator baselines.
- "The hangover explains the residual." It does on the employment route only.

## 6. Suggested wording
- Report s̄ in pp/yr, not as a share.
- Show the decomposition under a, c and e side by side.
- Describe the hangover as an over-hiring correction: it explains much of the headcount slowdown, but not the revenue shortfall. Top-six revenue is about 18 log points below its pre-COVID trend, while Accenture is on trend.
- Make the comparator gap (India-specific cc revenue about −3 pp/yr) the main open question for M5.
