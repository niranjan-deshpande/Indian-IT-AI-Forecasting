# FINDINGS — M6: ε from cross-line variation in AI exposure

*Saved by the orchestrator from the subagent's report (subagents can't write report files). Date: 2026-10-14. RBI HTML is in `raw/rbi/`.*

## 1. Headline

**M6 does not identify ε, and not even its sign robustly.**

- **The price-cut gaps between lines are tiny.** Mapping occupation-level exposure to service lines gives gaps of 0.1–0.5 pp/yr (at φs̄ = 2.5%/yr).
- **Demand-shift noise is large.** Line-specific shifts run about 3 pp/yr, and engineering services in the RBI data moved 12 pp relative to IT. With N = 4, SE(ε) ≈ 3 / (0.3 × 2) ≈ 5. Getting SE ≈ 0.5 would need gaps of about 3 pp/yr.
- **The exposure ordering depends on which score is used.**
  - Eloundou's GPT-4 ratings put IT/ADM above BPO.
  - Eloundou's human ratings and Felten's score put BPO above IT.
  - Felten ranks consulting highest, which matches D2 alternative B.
- **Plausible values only appear when a gap is imposed.** Using the D2 binary classes with an assumed high-minus-low gap of 2.5 pp/yr:
  - firm lines give ε = 0.13–1.36;
  - RBI BPO vs IT gives ε ≈ −1.0 to −0.1;
  - all bands are about ±2.5.

There is a weak lean towards ε < 1, but only where BPO or managed services are classed as most exposed.

## 2. Data

**Firm lines** (`01_line_growth.py`). These replicate D33's `sl_growth`, with Accenture Outsourcing spliced into Managed Services and TechM BPO into BPS.

| firm | lines compared |
|--|--|
| Accenture | Consulting vs Managed Services |
| Cognizant | Consulting & Technology vs Outsourcing |
| HCLTech | IT&BS vs ER&D (HCLSoftware excluded) |
| TechM | IT vs BPS |

- Baseline window: 2016–22 excluding COVID (alternative: 2016–19). Recent window: 2024Q2–2026Q2.
- HCLTech's baseline starts in 2019Q2.
- Some line splits end too early to use: Infosys and Wipro end in 2023Q1, TCS in 2017Q1.

**RBI exports by activity, FY19–FY26** (`rbi_activity_exports.csv`)
- Press releases: 51278, 52258, 54338, 56542, 58937, 61562, 63625. Values are consistent across vintages.
- Growth is in INR, so exchange-rate effects cancel within contrasts.

**Listed-firm panel by segment**, FY23–26 (`listed_segment_growth.csv`).

## 3. Exposure measure (`02_exposure.py`, `line_occupation_map.csv`, `line_exposure.csv`)

Each line gets a judgmental occupation mix (19 SOC codes). The activity blocks:

| block | main occupations |
|--|--|
| ADM | developers 40%, QA testers 15%, systems analysts 10%, sysadmins 15%, helpdesk 10%, IT managers 10% |
| BPO-A | customer service reps 45%, plus F&A clerks, accountants, data entry |
| ER&D | embedded developers 30%, plus engineers and drafters |
| Consulting | management analysts 25%, systems analysts 20%, developers 30% |

- Managed-services lines are ADM/BPO blends: Accenture 60/40, Cognizant 80/20, HCLTech 90/10.
- Composition B is an alternative mix.
- Scores used: Eloundou β (GPT and human ratings) and Felten LM AIOE, each raw and as percentile ranks.
- Price cut for line j: c_j = φs̄ · e_j / ē.

| line (composition A) | E_gpt β | E_human β | Felten LM |
|--|--|--|--|
| Consulting | 0.66 | 0.50 | 1.19 |
| Accenture Managed Services | 0.72 | 0.54 | 0.92 |
| HCLTech IT&BS | 0.76 | 0.52 | 0.88 |
| IT / ADM | 0.78 | 0.52 | 0.87 |
| BPO | 0.63 | 0.57 | 1.00 |
| ER&D / engineering | 0.66 | 0.46 | 0.79 |

## 4. Firm-line estimates (`03_estimate.py`, `firm_contrasts.csv`, `eps_firm_estimates.csv`)

**Contrasts.** Change in growth of the D2-high line minus the D2-low line, recent window vs 2016–22, in pp/yr (2016–19 baseline in brackets):

| firm | contrast |
|--|--|
| Accenture | +5.7 [+5.3] |
| Cognizant | −2.2 [−2.8] |
| HCLTech | −0.8 [−3.9] |
| TechM | −4.4 [−2.7] |

**Method.** OLS through the origin, which is equivalent to firm fixed effects. Inference uses a sign-flip test (16 assignments), leave-one-out, and a noise band assuming σ = 3 pp/yr.

**Continuous mappings** (φs̄ = 2.5, 2016–22 baseline). None is informative:

| mapping | ε | band |
|--|--|--|
| composition A, E_gpt | 5.5 | −13 to 24 |
| composition A, E_human | −1.5 | −28 to 25 |
| composition A, Felten | −7.1 | −33 to 19 |
| composition B, E_gpt | 7.1 | −6 to 20 |
| composition B, Felten | −7.7 | −27 to 12 |

**D2 binary classes**, with an assumed gap of 2.5 pp/yr:

| D2 variant | ε (2016–22) | ε (2016–19) |
|--|--|--|
| Baseline | 0.83 (95% −1.7 to 3.3, sign-flip p = 0.88) | 0.59 |
| A: ER&D counted as high | 0.88 | 0.97 |
| B: consulting counted as high | 0.13 | 0.09 |
| C: BPS counted as neutral | 1.36 | 0.82 |

Leave-one-out on the baseline ranges from 0.01 (without Accenture) to 1.36.

## 5. Segment level (`rbi_segment_growth.csv`, `rbi_growth_by_year.csv`, `eps_rbi_estimates.csv`)

YoY log growth in INR, %:

| activity | FY20 | FY21 | FY22 | FY23 | FY24 | FY25 | FY26 | FY25–26 avg | Δ vs FY20–23 |
|--|--|--|--|--|--|--|--|--|--|
| IT services | 7.0 | 7.2 | 20.9 | 23.9 | 7.6 | 6.7 | 15.7 | 11.2 | −3.6 |
| BPO | 14.2 | 16.5 | 12.3 | 26.8 | 0.7 | 12.9 | 4.8 | 8.8 | −8.6 |
| Engineering | 10.7 | −3.9 | −6.5 | 20.8 | 5.1 | 13.7 | 14.4 | 14.0 | +8.8 |

- **BPO vs IT.** BPO slowed 5.0 pp more than IT (2.8 excluding FY21; 4.9 on an FY20–22 baseline).
  - If BPO is the more exposed segment, ε ≈ −1.0 to −0.1 (band ±2.4).
  - Under GPT-based exposure the ordering flips and ε comes out above 5.
- **Engineering vs IT.** Engineering grew 12 pp faster. No ε in [0, 4] can produce that, so segment-specific demand shifts dominate (GCC engineering, autos, semiconductors).
- **Data caveats:**
  - The FY23 survey changed method: all activities jumped more than 20%, and BPO sub-lines were reclassified.
  - The FY26 survey frame grew by 12%.
  - GCC growth is concentrated in IT and engineering, so the demand shift d_j is correlated with activity.
- **Listed-firm panel, FY23–26 revenue CAGR in INR (USD):**

  | segment | INR | USD |
  |--|--|--|
  | BPM (5 firms; includes 7,432 acquired heads) | 15.8% | 13.9% |
  | ER&D (5 firms) | 10.6% | 7.7% |
  | IT services (7 firms, excluding the mid-tier four) | 8.9% | 4.4% |
  | Mid-tier four | 15.4% | 11.7% |

  This contradicts RBI on BPO. The listed BPM firms are healthcare and analytics firms that grow by acquisition, and the panel has no pre-2023 baseline.

## 6. Historical analogues (prior for ε)

From a literature-search subagent. No published estimate exists for outsourced IT or BPO.

| source | good / period | number | status |
|--|--|--|--|
| Bessen 2019, *Economic Policy* 34(100), Table 1 | textiles, steel, autos | early 1.3 / 2.2 / 2.4 vs 1950 0.2 / −1.2 / 0.4 | CONFIRMED |
| Bessen, NBER chapter c14029 | cotton, steel, autos | 2.13→0.02; 3.49→0.16; 6.77→0.15 | CONFIRMED |
| Bessen 2015, IMF F&D | ATMs and tellers | tellers per branch 20→13; branches +43%; teller jobs held | CONFIRMED |
| Tevlin & Whelan, FEDS 2000-11 | US computer capital | user-cost elasticity −1.6 | CONFIRMED |
| Byrne, Corrado & Sichel, NBER WP 25188 | AWS cloud | prices −7 to −17%/yr; revenue +55–70%/yr; no elasticity | CONFIRMED |
| Nakano & Nishimura 2024, arXiv 2401.08594 | Japan's computer-services imports | Armington elasticity 1.07 (s.e. 0.05) | CONFIRMED |
| Raissi & Tulin, IMF WP/15/161 | Indian goods exports | −0.86 long run | CONFIRMED |
| McKinsey Global Institute 2003 | offshoring | clients save 58¢ per dollar | UNCONFIRMED |
| Demirci, Hannane & Zhu 2025, *Management Science* | freelance writing and coding after ChatGPT | job posts −21% (a cross-price effect) | CONFIRMED |
| Brynjolfsson 1996 | IT demand | not retrieved | UNCONFIRMED |

**Suggested prior (a judgment call):**
- IT services: ε ≈ 0.5–1.5, centre ~0.9.
- BPO: ε ≈ 0.2–0.9, centre ~0.5.

Note: an elasticity measured against other vendors is higher than the market-level elasticity. Savings that clients capture in-house show up as a shift in d, not in ε.

## 7. Verdict
- **Use M6 as a consistency check only.** Check it against the (d, ε) line from M3/M5, and take ε's prior from §6.
- **What would make it usable:** observed line-specific price cuts from M2, such as ADM or BPO renewals compared with consulting, showing gaps of a few pp/yr.

## Files
| script | outputs |
|--|--|
| `01_line_growth.py` | `line_growth_quarterly.csv`, `line_growth_firms.csv` |
| `02_exposure.py` | `occupation_scores.csv`, `line_occupation_map.csv`, `line_exposure.csv` |
| `03_estimate.py` | `firm_contrasts.csv`, `eps_firm_estimates.csv`, `rbi_segment_growth.csv`, `eps_rbi_estimates.csv` |
| `04_summary.py` | `rbi_growth_by_year.csv`, `listed_segment_growth.csv`, `m6_summary.csv` |

`rbi_activity_exports.csv` is hand-transcribed from `raw/rbi/`.
