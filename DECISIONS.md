# DECISIONS — judgment calls, alternatives, sensitivity

Sensitivity key:
- **HIGH**: changes a headline conclusion.
- **MED**: moves numbers but not conclusions.
- **LOW**: negligible or untested but expected small.

The numbers quoted come from `output/robustness_compact.md` (Part 3) and `output/part4_table.md` (Part 4).

---

## Top 5 for review

### D1. What separates S1 (demand drop) from S3 (AI deflation with price pass-through) in the model — HIGH
- **Choice.** At the firm level, S1 and S3 predict the same revenue and headcount paths once full pass-through is assumed (κ=1). The model therefore separates them through only three channels:
  - **(a) Timing.** Demand shocks are surprises: headcount adjusts with lag λ=0.5 per quarter, so utilization dips first. Labor-need cuts are anticipated and pass straight into headcount with no utilization dip (λ_labor=1).
  - **(b) Comparator exposure.** Accenture's AI-exposure loading is 0.7, while S1 hits all firms equally.
  - **(c) Service-line contrast.** Only S3 predicts that high-AI-exposure service lines slow relative to low-exposure ones.
- **Alternatives.**
  - Treat labor-need cuts as sluggish too (λ_labor=0.5). This removes channel (a).
  - Equal exposure for all firms. This removes channel (b).
  - Partial pass-through, κ=0.5.
- **Sensitivity.**
  - Part 3: S1-vs-S3 accuracy at 12 quarters is 0.77 at baseline, 0.72 with λ_labor=0.5, and 0.86 with κ=0.5.
  - Channel (a) matters only in the first 4–5 quarters after onset. Observed from quarter 6 onward (the Part 4 situation), accuracy is 0.73.
  - Part 4 (quarters 6–14) therefore rests almost entirely on (b) and (c).
- **Why it matters.** Anyone who rejects these three channels should read S1 vs S3 as **not identified** from public firm data.

### D2. AI-exposure classification of service lines — HIGH (Part 4), MED (Part 3)
- **Choice (baseline).** Classified *high*:
  - Accenture Managed Services (formerly Outsourcing)
  - Cognizant Outsourcing
  - HCLTech IT & Business Services
  - TechM BPS

  Classified *low*: Accenture/Cognizant Consulting (& Technology), HCLTech Engineering & R&D. HCLSoftware is excluded as product revenue.
- **Rationale.** Run and maintain work, application management, testing and BPO are dominated by codifiable tasks: coding, documentation, ticket resolution, transaction processing. Task-exposure studies (e.g. Eloundou et al. 2023) rate these highest. Engineering R&D is tied to physical products. Consulting is relationship- and judgment-heavy.
- **Alternatives.**
  - (A) ER&D counted as high, since it is software-engineering heavy. HCLTech then drops out.
  - (B) Consulting counted as high, since GenAI exposure of analyst and knowledge work is also high. The Accenture and Cognizant contrasts flip sign.
  - (C) BPS counted as neutral. TechM drops out.
- **Sensitivity (Part 4).**
  - Baseline: P(S1)=0.55, P(S3)=0.17.
  - Alternative A: 0.50 / 0.23.
  - **Alternative B: 0.26 / 0.58.** The S1 lean flips to S3.
  - Alternative C: 0.54 / 0.16.
- **Why it matters.** The only evidence in public data that bears directly on S3 hinges on a contestable classification.

### D3. Noise-calibration window — MED (Part 3), HIGH (Part 4)
- **Choice.** Per the brief, 2015Q2–2022Q4, excluding YoY quarters distorted by COVID (2020Q2–2021Q2). This window includes the FY22 hiring boom and its unwinding, which inflate "normal" volatility and the baseline growth means.
- **Alternative.** Pre-COVID only (2015Q2–2020Q1).
- **Sensitivity.**
  - Part 3: S1–S3 accuracy is barely changed (0.77 in both). S1–S4 goes from 0.85 to 0.89.
  - Part 4: P(S1) goes from 0.55 to 0.81, because the pre-COVID baselines are lower and the noise smaller.
- **Related fix (see D19).** An earlier run gave P(S1)=0.99 under this alternative. That came from a spurious cross-firm "common" component in the service-line contrast, estimated from 3 firms. That component was removed.

### D4. Nuisance drifts (the main cap on detection power) — HIGH
- **Choice.** Every scenario allows two persistent drifts in demand that are unrelated to the scenario:
  - A common drift across firms, b ~ N(0, τ_b²). τ_b = 1.45%/yr, calibrated as the s.d. of annual cross-firm median growth in calm pre-2023 years.
  - A firm-specific drift, h_f ~ N(0, τ_h²), with **τ_h = 2%/yr by judgment**. The data do not identify it: the sampling-corrected estimate is 0, the uncorrected s.d. of firm-relative drift changes is 3.0%/yr, and it is confounded with Wipro's Capco acquisition.
- **Alternatives.** τ = 0 (no nuisance drift); τ_b = 4.
- **Sensitivity.**
  - Part 3: with τ=0, S1–S4 goes from 0.85 to 0.98 and S1–S3 from 0.77 to 0.81. With τ_b=4 there is little change.
  - Part 4: with τ_b=4, P(S4) goes from 0.29 to 0.46.
- **Why it matters.** Persistent drifts do not average out, which is why accuracy plateaus after about 4–6 quarters. More quarters of the same public metrics buy little.

### D5. Part 4 onset quarter and baseline — HIGH
- **Choice.** Onset at 2023Q1: the first quarter of falling headcount, i.e. the start of the FY24 slowdown. FY2025–27 data (2024Q2–2026Q2) are quarters 6–14 after onset. Baseline = each firm's mean YoY growth in 2015Q2–2022Q4 (ex-COVID), requiring ≥8 quarters. LTIMindtree uses the average of LTI and Mindtree.
- **Alternatives.**
  - Onset at 2024Q2 (i.e. FY25 treated as a new shock).
  - A pre-COVID baseline (see D3).
- **Sensitivity.** With onset at 2024Q2, P(S4) goes from 0.29 to 0.88. Treated as a fresh shock, the large Indian-vs-comparator gap in 2024Q2–2025Q1 looks like Indian-specific volume loss.
- **Why it matters.** Part 4 results should be read as illustrative only.

---

## Data decisions

| # | decision | alternatives | sensitivity |
|--|--|--|--|
| D6 | **All metrics as YoY log changes (×100).** Revenue = firm-reported constant-currency YoY growth. Headcount = YoY log change of end-of-period headcount. Utilization = YoY log change within one series. | QoQ cc growth: TCS gives no QoQ cc for most of FY22–26, Accenture reports YoY only. QoQ USD growth: FX-contaminated, and Accenture is ~50% non-USD. | MED. YoY removes seasonality but makes noise highly autocorrelated (ρ≈0.85), which is modelled explicitly. |
| D7 | **Accenture quarters assigned to the calendar quarter of their end month** (Nov→Q4, Feb→Q1, May→Q2, Aug→Q3). | Interpolate to calendar quarters. Rejected: it fabricates data. | LOW. A one-month offset on a smooth YoY series. |
| D8 | **Latest vintage wins** when a figure was restated (917 of 32k cells). All vintages are kept in `data/raw`. | First-reported values. | LOW for totals (revenue/headcount rarely restated). MED for segment shares after reorganizations. |
| D9 | **LTIMindtree is not spliced.** LTI and Mindtree enter the pre-2023 calibration as separate firms; LTIMindtree enters from Q1FY22 (the restated combined series). | Sum LTI+Mindtree (combined headcount is 3% lower than the sum; utilization definitions differ); or drop LTIM. | LOW. LTIM is 1 of 8 firms in Parts 3–4. |
| D10 | **HCLTech Q1FY25 divestiture:** the reported 7,398 divested employees are subtracted from the base of YoY windows spanning it. | Leave unadjusted (HCL headcount growth would be understated by ~3pp for 4 quarters). | LOW. |
| D11 | **One utilization series per firm, chosen by longest consistent coverage:** <br>• excluding trainees: TCS, Infosys, Wipro, LTI, LTIM <br>• including trainees: HCLTech, TechM, Mindtree, Accenture (definition unstated) <br>• Cognizant: offshore utilization through 2023, then blended; YoY changes computed within each series and spliced at the change level. | Excluding trainees everywhere (TechM's series stops after FY25). | LOW–MED. Utilization is missing for TCS and HCLTech in the recent period regardless. |
| D12 | **Acquisitions not adjusted:** Wipro–Capco (2021), HCL–IBM products (2019), Cognizant–Belcan (~4pp of growth, 2024Q4–2025Q2). Reported cc growth includes inorganic revenue. | Subtract disclosed inorganic contribution where available. | MED for Cognizant's recent growth; biases its service-line contrast toward S3 (Belcan sits in engineering/consulting). |
| D13 | **Verticals mapped to 4 broad groups** (financial services; tech/media/telecom; health & public; other industry, incl. manufacturing, consumer, resources and Accenture "Products"). **Geographies mapped to 3 regions** (North America incl. "Americas"; Europe incl. UK and EMEA; rest of world). Keyword rules are in `03_part2.py`. | Finer mapping: impossible to keep consistent through 20+ reorganizations. | MED for the cross-section; Accenture "Products" and TechM "Others" are rough fits. |
| D14 | **Subcontracting share = INR subcontracting cost / INR consolidated revenue.** For TCS: USD "fees to external consultants" (cost-of-revenue + SG&A lines) / USD revenue. | Report levels only. | LOW. Descriptive only. TCS's Q1FY27 definition break is flagged. |
| D15 | **Deal value:** trailing-4-quarter sum of the reported quarterly figure, then YoY. The measure differs by firm: <br>• Wipro: large deals (bookings start only in FY23) <br>• Cognizant: reported trailing-12-month bookings <br>• Accenture: new bookings <br>• others: total/large-deal TCV as defined by each firm | Exclude TCV. | LOW. TCV adds little power; noise s.d. ~25%. |
| D16 | Wipro revenue = **IT Services segment** (USD), not consolidated. | Consolidated INR. | LOW. |
| D17 | Revenue per employee uses **end-of-period** headcount. | Average of opening and closing headcount. | LOW for YoY changes. |
| D18 | Missing cc growth (e.g. Mindtree, TechM before 2019) is **left missing**, not replaced by USD growth. | Fill with USD growth. Rejected: that mixes FX into the series. | LOW. It reduces the calibration sample. |
| D24 | Infosys fact sheets taken from **Wayback Machine copies** of the original infosys.com PDFs (the site blocks scripts). The original URL is recorded as source_url; the archive timestamp is in source_doc. | Skip the fact sheets. That would lose utilization, segments and client buckets. | LOW. They are byte copies of the primary documents. |

## Model decisions (Parts 3–4)

| # | decision | alternatives | sensitivity |
|--|--|--|--|
| D19 | **Service-line contrast (SLc) has no cross-firm common component**; its estimated common variance is moved to the firm-specific part. Rationale: a within-firm difference has no reason to co-move across firms. The pre-COVID estimate (3 firms) produced a spurious 0.8 correlation with common revenue shocks. | Estimate a common component as for the other metrics. | HIGH. The fix moved pre-COVID Part 4 from P(S1)=0.99 to 0.81, and baseline Part 4 from (S1 0.43, S3 0.36) to (S1 0.55, S3 0.17). The baseline shift comes from the SLc signal now being weighed as firm-specific evidence. |
| D20 | **Linear-Gaussian scenario models** with closed-form marginal likelihood; scenarios specified as persistent drifts (%/yr) starting at onset. | Nonlinear state space with MCMC; one-off level shocks. | MED. Drift shapes are identical across scenarios by construction, so separation never comes from assumed shape differences. |
| D21 | **Effect-size prior:** d ~ N(4, 2²) %/yr under every scenario, informed by analyst "3–5% deflation" talk; this is not data. The simulated truth uses d = 2, 4 or 6. | Scenario-specific priors. | HIGH for power. At d=2%/yr, no pair except S1–S2 and S2–S3/S2–S4 reaches 80%. |
| D22 | **S3 pass-through κ=1** (price falls one-for-one with labor per unit). | κ=0.5. | MED. Partial pass-through makes S3 easier to tell from S1 and harder to tell from S2. |
| D23 | **Partial adjustment speed λ=0.5 per quarter** for surprise volume changes. | 0.3 or 0.7. | MED. It only affects the first ~4 quarters. |
| D25 | **S4 modelled only as the GCC variant**: volume falls for Indian vendors only; comparators are unaffected. The subcontractor variant is not modelled; subcontracting is shown descriptively. | Comparators also partially affected (Accenture/Cognizant also lose work to GCCs). | HIGH for S4 identification. If comparators also lose work, S4 collapses into S1. |
| D26 | **Firm AI-exposure loading:** 1.0 for Indian vendors and Cognizant, 0.7 for Accenture (consulting-heavy mix). Exposure gap between service-line groups `dexp`=0.5. | Equal loadings. | MED. This is channel (b) in D1. |
| D27 | **Noise:** each metric follows an AR(1) process, and its shocks are split into a common part (the cross-firm mean each quarter) and a firm-specific part, with correlations across metrics. After the code review: firm-specific variance is rescaled by n/(n−1), and the full firm-specific covariance / n is subtracted from the common part. | Independent across firms (would overstate power, since firms share shocks). | MED. The AR(1) coefficients are likely biased down (~0.07); a +0.07 sensitivity lowers S1–S3 accuracy from 0.77 to 0.74. |
| D28 | **Accuracy metric:** pairwise, equal prior odds, ties (identical predictions) split evenly. "Separates" = ≥80% accuracy. | Threshold of log BF > log 10. | LOW. Both are reported (`E_logBF`, `P_strong` in `output/sim_results.csv`). |
| D29 | **Firms available per metric in the simulation** = firms with ≥6 of 9 recent quarters of data: <br>• revenue, headcount, TCV: all 8 <br>• utilization: 6 (not TCS/HCLTech) <br>• SLc: 4 | Assume all firms report everything. | MED. More utilization or service-line coverage would raise power (the noise ×0.5 case is roughly an upper bound). |
| D30 | **COVID quarters excluded** from calibration and baselines: YoY quarters 2020Q2–2021Q2 (the shock itself and the first base-effect quarter). | Exclude only 2020Q2–Q4. | LOW–MED. |

## Part 2 decisions

| # | decision | alternatives | sensitivity |
|--|--|--|--|
| D31 | **Episode windows** (calendar): <br>• GFC 2008Q3–2009Q4 <br>• COVID 2020Q2–2020Q4 <br>• FY24 slowdown 2023Q1–2024Q1 <br>• recent 2024Q2–2026Q2 | Fiscal-year windows. | LOW. |
| D32 | **Vertical/geography "follows demand" test** = share of cross-firm × segment variance in recent growth (and in deceleration vs 2017–19) explained by segment vs firm means. | Regression with firm and segment fixed effects plus a comparator interaction. | MED. Small n (24–32 cells). |
| D33 | **Service-line growth** uses the firm-reported YoY cc growth where given, otherwise the YoY log change of reported levels in reported currency (Cognizant, TechM INR). Quarterly rows only. | Drop firms without cc. | LOW–MED (FX noise). |
