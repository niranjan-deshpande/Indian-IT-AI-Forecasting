# Round 4 synthesis: Part A diagnosis, FY24–26 (first pass, 2026-10-15)

This document combines measurements M1–M6 using the model in ESTIMATION_PLAN.md. Each measurement's details and sources are in its folder's FINDINGS.md. Growth rates are % per year, in log points.

**Scope.** The main scope is the top six firms. M1 covers four of them (Infosys, Wipro, TechM, LTI); TCS and HCLTech are bounded rather than measured. M2 is revenue-weighted across the top six. M3 is the top six's simple average. Sector-scope M1 isn't usable, so this document doesn't attempt a sector decomposition.

**Vintage.** All outcome data end in FY26 or CY2025, before coding agents' step change in summer 2026.

## 1. Inputs

| measurement | FY24–26 value | range | source |
|--|--|--|--|
| M1: (1−φ)s̄, the savings firms kept | ≈ +1.0 | spec range −0.2 to +2.0; 95% CI −1.8 to +4.2; with π bound −0.7 to +3.0 | `residual/` |
| M2: φs̄, the AI-driven price cut, net of the pre-AI baseline | ≈ +0.2 (FY24 0, FY25 0.1, FY26 0.4) | 0 to ~0.6; ×2 bias gives ~1.3 | `price_statements/` |
| M3: top-six headcount growth | −0.97 (baseline FY16–20 +7.37) | — | `output/final/note_numbers.csv` |
| M3': top-six revenue growth, constant currency | +1.60 (baseline FY16–20 +8.70) | — | same |
| M4: s_J − s_E | firm ≈ 0 to +1 (−2 to +3); sector ≈ +2 (CI includes 0) | relative junior pay in IT −5.4 log pts/yr vs all graduates (SE 1.9) | `junior_gap/` |
| M5: Δd from outside measures, vendor-facing, excluding GCCs | ≈ −3.1 | −7.3 to +0.1; market part ≈ −0.5 (±1) | `demand_shift/` |
| M6: ε | not identified | literature prior: IT 0.5–1.5; BPO 0.2–0.9 | `elasticity_xsec/` |

## 2. Identification

**Replacement rate:** s̄ = M1 + M2 ≈ 1.0 + 0.2 = **≈ 1.2 pp/yr**.
- Plausible range: 0 to 2.5.
- Widest range, combining the extreme specifications and bias bounds: −0.7 to ~4.

**Pass-through:** φ = M2 / s̄ ≈ 0.15, but it is effectively unidentified, because both terms are small next to their noise. The point estimates suggest firms passed on little of a small saving in FY24–26. The FY27 statements (φs̄ ≈ 1.5) suggest pass-through is now starting.

**Change since the FY16–20 baseline** (with π and ρ held unchanged and s = 0 in the baseline):
- Employment: Δg_L = −0.97 − 7.37 = **−8.3**.
- Revenue: Δg_R = 1.60 − 8.70 = **−7.1**.

**Volume.** Δg_Q = Δg_L + s̄ ≈ −8.3 + 1.2 = **−7.1**. As a cross-check, Δg_R − Δg_p ≈ −7.1 + 0.2 = −6.9. The two routes agree.

**Demand shift.** Δd = Δg_Q + ε·Δg_p ≈ −7.1 − 0.2ε, which is **≈ −7 for any ε between 0 and 1.5**. Because pass-through has been tiny, ε barely matters for the past. It starts to matter only from FY27.

## 3. Decomposition of the 8.3 pp slowdown in top-six employment growth

| component | pp/yr | share |
|--|--|--|
| AI replacement (s̄) | ≈ −1.2 (0 to −2.5) | ≈ 15% (0–30%) |
| Volume / demand (Δd + εΔg_p) | ≈ −7.1 | ≈ 85% |

**What accounts for the demand fall.** M5's measured shifts explain about half of the roughly −7 pp: −3.1 for vendors excluding GCCs, within −7.3 to +0.1.
- US clients moving IT work in-house: about −1.6, range −3.3 to −0.4. Vendors' share of US computer jobs fell, and staffing-firm computer jobs fell 22%.
- Work moving to GCCs: about −1, range 0 to −2.5.
- The overall client market: about −0.5.

The remaining roughly 3–4 pp is unexplained. Candidates:
- the FY16–20 baseline overstates normal growth after the FY22–23 boom pulled demand forward;
- Europe, which is about 30% of exports and isn't measured;
- share lost to mid-tier and other Indian firms;
- clients substituting their own AI tools, which the US jobs data wouldn't show.

## 4. Juniors

- **Quantities.** No junior-specific AI effect can be distinguished in headcount (firm level: s_J − s_E ≈ 0 to +1).
- **Hiring mix.** Firms shifted hiring toward experienced staff: at Infosys, hiring of 30+ staff rose 65% while under-30 hiring was flat.
- **Price.** The clearest signal is pay. Relative junior pay in IT fell about 5 log points a year faster than for graduates generally (SE 1.9). With graduate supply rising, that points to weaker demand for juniors.
- **Part B warning.** The boom-era fresher cohort turns 30 around FY30–31. That will push under-30 shares down mechanically, and it should not be read as an AI effect.

## 5. Headline for Part A (draft)

In FY24–26 the slowdown at India's largest IT firms was mostly a fall in demand for their services, about 7 of the 8.3 pp drop in employment growth.
- **AI replacement was small:** about 1 pp a year, plausibly 0–2.5, i.e. 0–30% of the slowdown.
- **Little of that saving reached prices:** about 0.2 pp a year.
- **Measured shifts explain about half the demand fall:** US clients moving work in-house, and GCCs.
- **The rest is unexplained**, plausibly the post-boom hangover.
- **Juniors:** no junior-specific employment effect is distinguishable yet, but their relative pay is falling.

Each step rests on a stated assumption: the M1 baseline (π and ρ unchanged), the representativeness of M2's management statements, and the FY16–20 baseline. All of it predates the 2026 capability step change, and FY27 statements suggest pass-through is now accelerating.

## 6. Robustness checks still to run
- **Baseline window** for M3: FY16–20 vs a trend that excludes the boom. This mainly moves the unexplained residual.
- **Scope consistency:** recompute M1 for the top six, using the TCS and HCLTech bounds.
- **Subcontracting bias in M1:** in-housing of subcontracted work could lower M1 by about 1 pp, which would raise s̄ to about 2.
- **M5:** pre-2023 GCC growth; a European demand proxy; a cross-check of the OEWS data on US IT-services jobs (NAICS 5415) against BLS CES.
