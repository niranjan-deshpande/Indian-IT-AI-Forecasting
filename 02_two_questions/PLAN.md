# Estimation plan: what has happened to Indian IT employment, and what could happen by 2030

*Draft v2, 2026-10-14. v1 listed sources. This version says what each source measures and how the sources combine into estimates.*

*Sections 1–5 are the plan (formerly `ESTIMATION_PLAN.md`). Sections 6–8 are the numbers, file map and constraints handed to the writing agent on 2026-10-15 (formerly `HANDOFF.md`; its job description and model restatement are dropped, since the page `checkpoint_text.md` → `docs/two-questions.html` has been written). The approved outline (`OUTLINE.md`, 2026-10-15) was dropped as fully superseded by `checkpoint_text.md`; see git history.*

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

## 6. Numbers at handoff (2026-10-15)
Scope is the top six firms. The window is FY24–26 against a pre-2023 baseline. Units are pp/yr. All data predate the summer-2026 step change in coding agents.

### Replacement rate s̄
- **Central: about 2.3 pp/yr.** Range 2.0–2.6 across the subcontracting conversion factor; 1.5–3.6 within the identification bounds; −0.8 to 7.1 including sampling error. Neither 0 nor "firms kept 4%/yr" can be rejected. Source: `round4/robustness/m1_scope_subcon/`.
  - M1 for the top six is about 1.0 uncorrected and about 2.1 after correcting for in-sourcing of subcontracted work. Subcontracting fell 1.2–3.9 pp of revenue in FY24–25, which biases revenue per employee down. The correction assumes the fall was in volume, not contractor rates.
  - M2 (AI-driven price cut, net of pre-AI give-backs): FY24 0, FY25 0.1, FY26 0.4, FY27 about 1.5 (0.4–2.7; partly expected). Pre-AI give-backs were about 1.5%/yr (assumed; contract percentages are redacted). Source: `round4/price_statements/`.
  - So φ ≈ 0.1: firms kept most of the saving. **This contradicts the existing note's claim of "no sign firms kept AI savings".**
- **Tension.** In levels, revenue per employee is still about 11 log points below its FY16–20 trend (`round4/robustness/baseline/`). That argues against any gain. Report this openly; don't resolve it by fiat.
- **Juniors, s_J − s_E** (`round4/junior_gap/`):
  - Firm level: about 0 to +1 (range −2 to +3).
  - Sector level (PLFS): about +2, with a CI that includes 0.
  - Strongest signal: junior relative pay in IT fell 5.4 log points/yr faster than for all graduates (SE 1.85).
  - Mechanism: hiring tilted toward experienced staff. At Infosys, 30+ hires rose 65% while under-30 hires were flat.
  - Boom-era freshers turn 30 around FY30–31. That will mechanically lower under-30 shares then and should not be read as AI.

### Demand shift d
- **The implied shift depends on the yardstick** (`round4/robustness/baseline/`):

  | yardstick | headcount | constant-currency revenue |
  |--|--|--|
  | FY16–20 growth means | −8.3 | −7.1 (so d ≈ −7) |
  | level trend | −3.0 | −5.7 |
  | vs Accenture/Cognizant | −1.5 | −3.1 |

  - Top-six revenue is about 18 log points below its pre-COVID path. Accenture is back on trend.
  - The FY22–23 boom over-hired staff (+14 log points vs trend), not revenue (+3.5).
- **What we measure directly** (`round4/robustness/demand/`, which supersedes `round4/demand_shift/`):
  - Vendor-facing d is about −1.6 (−7.4 to +2.2).
  - Client markets: about −0.5. GDP, bank tech budgets and in-house software spending are all flat.
  - Clients moving work in-house: about −1.6. US in-house share of computer jobs rose from 64–65% to 67.5%, and BLS CES confirms the fall in vendor employment. Continental Europe is about 0; the UK may be large but is unverified.
  - GCCs: about +0.5. GCC growth did not speed up after 2023.
- **Unexplained.** About 5 pp against the growth-mean yardstick; about 3 pp of revenue growth against peers. Candidates:
  - a work mix weighted toward routine run/maintenance work;
  - clients using their own AI tools;
  - share lost to other vendors.

### Elasticity ε
- Not identified (`round4/elasticity_xsec/`).
- Because φs̄ was tiny in FY24–26, ε barely affects the past decomposition. It matters from FY27, as price cuts start.
- Literature prior: IT services 0.5–1.5 (centre 0.9); BPO 0.2–0.9 (centre 0.5). Sources include Bessen and Tevlin–Whelan.

### Context, for the setup only
- Sector employment is flat: PLFS NIC 62–63 is about 5.5–5.7m since 2022-23. Young graduates in IT are about 2.6–2.8m.
- Exports rose 19% in USD over FY23–26, growing outside the big firms.
- India's share of world computer-services exports is flat, so the work stayed in India.
- 21 other listed firms did not absorb the slack organically.

Sources: `02_two_questions/explore/round3/` (see `round3/SYNTHESIS.md`) and `round3/plfs/`.

## 7. Where the measurements live
- **Plan:** sections 1–5 above
- **First-pass synthesis:** `02_two_questions/explore/round4/SYNTHESIS.md`. Outdated on s̄ (1.2) and on the AI share; use the robustness folders instead.
- **Measurements:**
  - `round4/residual` (M1)
  - `round4/price_statements` (M2)
  - `round4/junior_gap` (M4)
  - `round4/demand_shift` (M5)
  - `round4/elasticity_xsec` (M6)
- **Robustness:**
  - `round4/robustness/baseline` (R1)
  - `round4/robustness/m1_scope_subcon` (R2)
  - `round4/robustness/demand` (R3)
- Every folder has a `FINDINGS.md` with methods, numbers, URLs and caveats. CSVs and scripts sit alongside.
- **Earlier work:**
  - `02_two_questions/explore/round3/`: sector, GCCs, offshoring, seniority, red team, listed panel, PLFS.
  - The existing note: `01_pilot/note_text.md` → `docs/index.html`.

## 8. Standing constraints
- **PLFS data agreement (MoSPI).**
  - Unit-level data stay in gitignored `data/sources/plfs/`.
  - Only aggregates are published.
  - Cite PLFS (MoSPI).
  - Email a copy of any publication to nssunit.dsdd@mospi.gov.in.
- **Stale claims in the existing note,** to fix later and not now:
  - "no sign firms kept AI savings" (§1, §4);
  - the one-month Naukri GCC postings comparison (noise);
  - the RBI census comparison across rounds (§5b).
