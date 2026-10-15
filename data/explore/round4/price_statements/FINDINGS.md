# FINDINGS — M2: AI-driven price change on same-scope work (φs̄), from management statements

*Saved by the orchestrator from the subagent's report; subagents can't write report files. Date: 2026-10-15. Coverage: calls from Jan 2023 to Oct 2026, investor days in 2025–26, and BPO firms.*

## 1. Headline

The AI-driven price cut on same-scope work (φs̄) was close to zero through FY26. It rises to roughly 1–2.5%/yr in FY27.

Results are in % per year: low / central / high for the AI increment; central only for the gross figure.

| year | IT top six: AI increment | IT top six: gross | BPO: AI increment | BPO: gross |
|--|--|--|--|--|
| FY24 | 0 / 0 / 0.25 | 1.55 | 0 / 0 / 0.25 | 1.0–1.5 |
| FY25 | 0.01 / 0.10 / 0.35 | 1.65 | 0 / 0.5 / 1.0 | 1.5–2.0 |
| FY26 | 0.01 / 0.43 / 1.32 | 1.98 | 0 / 0.5 / 1.0 | 1.5–2.0 |
| FY27 (partly expected) | 0.41 / 1.51 / 2.67 | 3.06 | 0.25 / 1.0 / 3.0 | 1.75–4.0 |

- **AI increment** is the give-back net of pre-AI productivity give-backs, which belong in π (non-AI price drift), not φs̄. **Gross** = baseline + increment.
- **BPO rests on one firm** (Sagility).
- **Bias bound ×0.5–×2:** IT FY26 becomes 0–2.6 and FY27 0.2–5.3.

## 2. Method

1. **Corpus scan.** `scan_corpus.py` covered all transcripts from 2023 on in `audit/calls_transcripts.csv` (8 firms). It produced 408 candidate sentences (`scan_candidates.csv`). These, plus the 90 quantitative rows in `audit/price_calls_quotes.csv`, were screened by hand, and key exchanges were re-read in full.
2. **Extension** (sources saved in `raw/`):
   - TCS Q2FY27 transcript (call 8 Oct 2026). HCLTech Q2FY27: investor release only.
   - Investor and analyst days: TCS (Oct and Dec 2025), Infosys AI Day (Feb 2026), LTIMindtree (May and Jun 2026), Cognizant (2025–26 conferences), Accenture, TechM.
   - BPO firms: Sagility, Firstsource, eClerx, HGS.
   - Pre-2023 contracts, and 10-K/20-F disclosures on contract mix and tenure.
   - Not covered: Q2FY27 calls for Infosys, Wipro, TechM and LTIMindtree.
3. **Classification fields:** firm, date, speaker, segment, type, scope, horizon, tense, whether net of baseline, magnitude, quote, page, URL.
4. **Verification.** Quotes were machine-checked against the primary text. 107 of 108 are CONFIRMED. EXT-BPO-11 (Sagility) is unconfirmed only because the text layer reads "yearon-year"; it is used as context only.

## 3. Statements (`m2_statements.csv`, 108 rows)

**Counts**
- By segment: 81 IT, 27 BPO.
- By speaker: 92 management, 14 filing or contract text, 2 analyst (flagged).
- By type:

  | type | rows |
  |--|--|
  | timing or bound | 25 |
  | renewal structure | 22 |
  | pre-AI baseline | 20 |
  | delivery productivity (measures s, not φs) | 12 |
  | portfolio deflation rate | 7 |
  | give-back over contract term | 7 |
  | price, same scope | 5 |
  | single deal | 5 |
  | deal value, same scope | 3 |
  | price increase | 2 |

- Only about 16 IT and 5 BPO rows carry a usable magnitude.

**Core statements**

| firm, date | statement | scope / horizon |
|--|--|--|
| HCLTech, Jul 2023 | deflation "at least two to three years away" | timing |
| TCS, Jul 2024 | rejects 5–20% renewal cuts | renewals |
| TCS, Apr 2025 | "$100 → $95 or $90" | AI-for-IT work; one-off; expectation |
| HCLTech, Oct 2025 | in 5 of its top-10 renewals, AI shrank the scope of work | renewals; no % |
| TCS, Jan 2026 | 10–15% over the contract term is built into renewals, "not related to AI" | pre-AI baseline |
| HCLTech, Apr 2026 | 3–5%/yr in AI-disrupted services, equal to 2–3%/yr of HCL's portfolio; "incremental" to traditional productivity | per year; expectation |
| HCLTech, Apr 2026 | "very little has really played out in already reported numbers"; expected from FY27 | timing |
| HCLTech, Apr 2026 | a $100M deal would now be "maybe 80 million" | new deals; one-off |
| TCS, Jul 2026 | "around 10% to 15%" "through the tenure", front-loaded | renewals; over the term |
| LTIMindtree, Jul 2026 | same scope about 15% lower than a year earlier, for "certain category of services" | new deals; one-off |
| TCS, Oct 2026 | "some frontloading of productivity benefits"; "at an overall portfolio level, the pricing is broadly stable" | caps H1 FY27 |
| Cognizant, Jun 2026 | "very little deflation at a aggregate industry and company level" | comparator |
| Infosys, Apr 2026 | growth "more than the compression"; volumes flat | upper bound below ~3% |
| Sagility (BPO), May 2025 – Jul 2026 | 150–200 bps a year; 100–150 bps before AI; 4–5% expected in 2–3 years | gross; includes offshoring |
| eClerx (BPO), Jan 2026 | top clients have not asked for an annual pass-back | lower bound |

**Upper tail, not used as rates**
- Competitor bids 70–80% lower over 5-year deals (TechM's account).
- Cognizant: one deal cut more than 50% over five years.
- Accenture: one deal "reducing costs by half".
- TCS analyst-day showcase deals: 20–30%.

**Baseline evidence**
- HCLTech (FY23): annual productivity commitments "for several years".
- Contracts filed as exhibits (Health Net–Cognizant 2010; Nielsen–TCS 2018) contain productivity commitments, but the percentages are redacted.
- Accenture (Jun 2023): at least 10%/yr in managed services.
- Analysts' 3–5%/yr figures are labelled as analyst estimates.

## 4. Conversion (`m2_convert.py`, giving `m2_firm_year.csv` and `m2_aggregate.csv`)

**Conversion rules**
- **R0, baseline.** Pre-AI give-backs are part of π. Only the AI increment counts toward φs̄.
- **R1, portfolio rate per year, net of baseline** (HCLTech): used directly.
- **R2, one-off discount D on renewals or new deals:** rate = D × r × a.
  - r = share of revenue repriced each year: 0.20–0.35, central 0.275.
  - a = share of revenue in affected services: 0.4–0.6.
- **R3, give-back G spread over contract term T:** rate = g × k × c_t.
  - g = G/T: 2.0–5.0, central 3.1.
  - k = share that is AI-driven: 0, 0.5 or 1. TCS gives the same 10–15% for pre-AI renewals.
  - c_t = cumulative share of revenue on AI-era terms: FY25 0–0.1, FY26 0.15–0.45, FY27 0.45–0.75.
  - TCS's FY27 high is capped at 2.0, given "broadly stable".
- **R4, firms that give no number** (Infosys, Wipro, TechM): 0 to 2× the revenue-weighted mean of the firms that do.
- **Weights:** trailing-four-quarter USD revenue, 2025Q3–2026Q2. TCS, HCLTech and LTIMindtree together are 57% of top-six revenue.

**Pre-AI baseline**
- **IT (an assumption):** 2–5%/yr per contract × 0.40–0.55 of revenue on multi-year terms = 0.8–2.75, central 1.55. Supporting shares:
  - Accenture managed services: 49.6%.
  - Cognizant outsourcing: 35.9%.
  - Infosys fixed-price: 54%.
  - Wipro fixed-price plus volume-based: 52.4%.
- **BPO:** Sagility's own figure of 100–150 bps, which includes offshoring.

## 5. Breakdown points (`m2_breakdown.csv`)

| conclusion | central | what would overturn it |
|--|--|--|
| FY24–26 average < 1 pp/yr | 0.18 | all firms understating by 5.7× (11× to reach 2 pp) |
| FY26 < 1 pp | 0.43 | a uniform 2.3× understatement, or Infosys, Wipro and TechM each at 1.76 pp |
| FY27 ≥ 1 pp | 1.51 | FY27 statements overstated by more than 1.5× |
| BPO FY26 < 1 pp | 0.5 | Sagility's baseline ≤ 0.75 pp, or its gross understated by ≥ 0.5 pp |

## 6. Caveats
- Three firms supply most of the quantification. Infosys and Wipro never give a number.
- Answers to deflation questions likely understate; showcase deals overstate. The net bias probably understates φs̄.
- **Time-and-materials work** (43–48% of revenue at Cognizant, Wipro and Infosys) passes savings through as fewer billed hours. Managers never call this a give-back, so statement-based M2 understates φs̄ there.
- "Same scope" is fuzzy: scope rises at renewal, Sagility's figure includes offshoring, and HCLTech's 3–5% is framed as a shrink in industry spend.
- The IT baseline is an assumption; the percentages in primary sources are redacted.
- FY27 is mostly expectation.
- BPO rests on one firm, and eClerx points lower.
- Q2FY27 coverage is TCS only.

## 7. Files
- `scan_corpus.py`, `scan_candidates.csv`
- `build_m2_statements.py`, `m2_statements_corpus.csv` (62 rows)
- `merge_extension.py`, `m2_statements.csv` (108 rows)
- `m2_convert.py`, `m2_firm_year.csv`, `m2_aggregate.csv`, `m2_breakdown.csv`
- `raw/it_q2fy27/`, `raw/bpo/`, `raw/baseline/` (each includes the helpers' `agent_rows.csv`)
