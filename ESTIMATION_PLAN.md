# Estimation plan: what has happened to Indian IT employment, and what could happen by 2030

*Draft v2, 2026-10-14. v1 listed sources. This version says what each source measures and how the sources combine into estimates.*

## 1. Question and structure

**Policy question.** Is India's IT sector still growing as a source of good jobs, and in particular as an entry point for young graduates? If not, why not?

The work has two parts:
- **Part A, diagnosis (2023–2026).** This is the core. It estimates or bounds the parameters from what has already happened.
- **Part B, scenarios (to 2030).** These are conditional futures, not forecasts with confidence intervals. Each starts from Part A's estimates and moves the replacement rate along paths informed by capability trends.

**Vintage caveat.** Coding agents improved in a step change from around summer 2026. The Part A outcome data almost all predate that, so Part A describes the period before it. Every capability or productivity study cited carries a date.

**Segments:**
- IT services: NIC 62–63.
- BPO: NIC 822 (call centres), part of NIC 82.

**Worker groups:** junior and experienced. "Junior" is proxied by age 21–25 in PLFS and under-30 in firm reports.

**Scope rule.** Each equation is estimated at a single scope: either the top six firms or the whole sector. Never mix scopes within one equation.

## 2. Model

All variables are annual growth rates. Employment is labour per unit of work times volume: L = a·Q.

| Parameter | Meaning |
|--|--|
| s | Replacement rate: the % fall per year in labour per unit of work. Separate values s_J (junior) and s_E (experienced). s̄ is their labour-weighted average. |
| φ | Share of the cost saving passed to clients as a lower price per unit. |
| ε | Price elasticity of volume. |
| d | Demand shift at a constant price. This includes clients moving work in-house or to their own AI tools. |
| π | Non-AI price drift. |
| ρ | Non-AI productivity growth. |

How the parameters combine:

| Quantity | Equation |
|--|--|
| Price | g_p = −φ s̄ + π |
| Volume | g_Q = d − ε g_p |
| Employment | g_L = g_Q − s̄ − ρ |
| Revenue | g_R = g_p + g_Q |

## 3. Measurement equations

| # | Observable | Measures | Main identifying assumption | Data | Owner |
|--|--|--|--|--|--|
| M1 | Change in the revenue-per-worker residual (net of utilisation), FY24–26 vs FY16–23 | (1−φ) s̄ | π and ρ are unchanged from the pre-2023 baseline | Firm panel (Table B); exports per PLFS worker at sector scope | `round4/residual` |
| M2 | AI-driven price change on work of the same scope (deal, renewal or portfolio give-backs) | φ s̄ | The statements are representative and "same scope" is really the same scope | Calls corpus plus Q1–Q2 FY27 calls | `round4/price_statements` |
| M3 | Employment growth by segment | d − ε g_p − s̄ − ρ | Sampling error only | Firm headcount; PLFS | (in hand) |
| M4 | Junior minus experienced employment growth | −(s_J − s_E) | Other forces reshaping the pyramid can be netted out, especially unwinding of the FY22 hiring boom | Firm under-30 panels; PLFS age bands; Infosys job levels | `round4/junior_gap` |
| M5 | Outside demand shifters: client IT budgets including in-house spending; BEA purchased vs own-account software; in-house tech employment | d | The proxy moves one-for-one with the demand curve at a constant price. It must not be vendor revenue, which would be circular. | BEA; client filings; PLFS occupation split | `round4/demand_shift` |
| M6 | Across service lines or segments: revenue growth against the AI price cut | ε, from variation in φs across lines | Exposure is the only systematic difference between lines | Service-line revenue; task-exposure scores; RBI exports by activity | `round4/elasticity_xsec` |

**What is identified:**
- s̄ = M1 + M2.
- φ = M2 / s̄.
- s_J − s_E from M4.
- M3 then gives a line in (d, ε) space.
- M5 picks a point on that line. M6 gives an independent check on ε.

**How sources combine.** This is partial identification. Each measurement, together with an explicit bound on its bias, defines a region of parameter values. The estimate is the intersection of those regions. For every headline we also report a breakdown point: how wrong an assumption would have to be to overturn it.

Where sampling errors are known (PLFS, firm noise from the pilot's noise calibration), they widen the regions. Sources with no measurement equation are context only: benchmarks, METR horizons for the level of s, general CEO commentary, and job postings.

## 4. Part B: scenarios

- Start from Part A's estimates of s̄, φ, s_J − s_E, and the (d, ε) region.
- Move s(t) along paths built from capability evidence: METR horizons including the post-2026 step change, benchmarks, and the ratio of AI cost to Indian labour cost. Pass these through an adoption lag. Capability evidence enters only through the rate of change of s, never its level.
- Report junior and total employment in 2030 for each scenario, together with the signs that would show we are in it.

## 5. Open questions
- **Junior definition.** Age 21–25 or 0–3 years' experience? PLFS records age only.
- **GCCs.** Treat them as part of d, or as their own segment?
- **Headline.** Should Part A or Part B lead? This plan assumes Part A.
