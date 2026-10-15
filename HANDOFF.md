# Handoff: outlining and writing the internal checkpoint (2026-10-15)

## 1. The job
Write an internal checkpoint page for Andrei Potlogea, the supervisor. It is for a meeting on 16 Oct 2026. **Outline first, and get the user's agreement before building anything.**

**Audience and tone**
- This is a semi-finished checkpoint, not a polished note.
- It needs no background or "what changed since last week" section. The user sends that context in Slack.
- Write plainly: short sentences, no jargon, every number traceable. The user's standard is "something George Orwell would like".
- Follow the conventions of the existing note:
  - text lives in a markdown file;
  - charts are built from repo CSVs;
  - sections are numbered;
  - appendix items are collapsible;
  - numbers are checked by a script.
- References: `note_text.md`, `scripts/final/build_note.py`, `scripts/final/note_number_check.py`.

**Organise everything around one question with two parts.** The user rejected the previous outline because it read as seven loosely related topics.
1. **The replacement rate.** How much has AI cut the labour needed per unit of work, overall and for juniors?
2. **Demand.** What has happened to demand for these firms' work: (a) how far it has *shifted*, and (b) how it responds to price (*elasticity*)?

Every section and figure should serve one of these. Context (sector size, exports, the fact that work stayed in India) supports the setup; it doesn't get its own sections.

**Suggested skeleton** (the next agent should refine it with the user):
1. **The question and the accounting.** Jobs = work done × labour per unit of work. Two short paragraphs, plus one box with the model.
2. **Estimate 1: the replacement rate.** Overall, then juniors. Show how it is measured and what would overturn it.
3. **Estimate 2: demand.**
   - (a) The shift: what we measure, what the arithmetic implies, and what is left unexplained.
   - (b) Elasticity: why the past data can't pin it down, and the prior we use instead.
4. **What the two estimates imply together.** The decomposition under three yardsticks: growth rates, levels, and peers.
5. **What would sharpen each estimate, and next steps.** Next steps are the scenarios to 2030.

Appendix: methods, robustness, sources, PLFS citation.

## 2. The model
This is in `ESTIMATION_PLAN.md` (one page), with measurements M1–M6. All terms are annual growth rates.

| symbol | meaning |
|--|--|
| s̄ | replacement rate: % fall in labour per unit of work (s_J for juniors, s_E for experienced staff) |
| φ | share of the saving passed on to clients as lower prices |
| d | demand shift at a constant price |
| ε | price elasticity of demand |
| π, ρ | non-AI price drift; non-AI productivity growth |

Equations:
- Price: g_p = −φs̄ + π
- Volume: g_Q = d − ε·g_p
- Employment: g_L = g_Q − s̄ − ρ

What identifies what:
- s̄ = M1 + M2, where M1 = (1−φ)s̄ (savings firms kept) and M2 = φs̄ (savings passed on in price).
- s_J − s_E comes from M4.
- Employment and revenue give the volume change. M5 measures d directly. M6 was meant to give ε but cannot.
- Combining is by partial identification: bounds, with breakdown points. Each source must have a measurement equation; a source without one is context only.

## 3. Current numbers for each estimate
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

Sources: `data/explore/round3/` (see `round3/SYNTHESIS.md`) and `round3/plfs/`.

## 4. Where things are
- **Plan:** `ESTIMATION_PLAN.md`
- **First-pass synthesis:** `data/explore/round4/SYNTHESIS.md`. Outdated on s̄ (1.2) and on the AI share; use the robustness folders instead.
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
  - `data/explore/round3/`: sector, GCCs, offshoring, seniority, red team, listed panel, PLFS.
  - The existing note: `note_text.md` → `docs/index.html`.

## 5. Constraints and preferences
- **Delegation.** The user wants research delegated to Opus subagents, a handful at a time. Subagents cannot write `.md` files, so ask them to return findings text and save it yourself.
- **Build only on approval.** Don't build or publish until the user approves the outline. The repo is public and GitHub Pages serves `docs/`. A private claude.ai page was proposed for the Andrei version; the user hasn't decided.
- **PLFS data agreement (MoSPI).**
  - Unit-level data stay in gitignored `data/sources/plfs/`.
  - Only aggregates are published.
  - Cite PLFS (MoSPI).
  - Email a copy of any publication to nssunit.dsdd@mospi.gov.in.
- **Nothing is committed.** That covers `round3/`, `round4/`, `ESTIMATION_PLAN.md` and this file. The `raw/` subfolders hold over 1 GB of downloads and aren't gitignored. Ask before committing, and propose gitignoring `data/explore/round*/**/raw/`.
- **Stale claims in the existing note,** to fix later and not now:
  - "no sign firms kept AI savings" (§1, §4);
  - the one-month Naukri GCC postings comparison (noise);
  - the RBI census comparison across rounds (§5b).
- **Session memory** lives in `~/.claude/projects/…/memory/` (Andrei's Oct 6 direction, the two-estimate restructure, PLFS access, delegation preference).
