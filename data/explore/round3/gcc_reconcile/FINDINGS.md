# FINDINGS — reconciling GCC headcount with Nasscom industry totals

*Saved by the orchestrator from the subagent's report; subagents cannot write report files. Probe date: 2026-10-14.*

Files in this folder:
- `reconcile_inputs.csv`: every input, with URL and a confirmed flag.
- `gcc_scenarios.csv`, built by `build_scenarios.py`.
- `raw/`: Nasscom press releases and executive summary (PDF and text), Nasscom/Zinnov pages, RBI pages, and a scan of RBI press-release titles (prid 63300–63807).

## Summary
The puzzle — GCCs adding +460k jobs while the whole industry added only +268k — comes mostly from comparing two Nasscom products that are built on different vintages and coverage. It is not evidence that jobs outside GCCs collapsed.

Best defensible estimate, FY23→FY26:
- **GCC staff, all functions:** about +240k to +570k; central estimate about +385k.
- **GCC tech staff:** about +155k to +430k; central estimate about +260k, assuming a two-thirds tech share.
- **Rest of the industry** (excluding GCCs and the top six): roughly flat on the central estimate (about −20k to +20k). It falls by about 150k only if the 2026 GCC edition is taken at face value.

## 1. Resolution
1. **Nasscom's industry total includes GCCs (CONFIRMED).**
   - The Strategic Review 2025 press release, Note to Editors, says the September 2024 GCC restatement is factored into the industry numbers: "FY2024 … $268.8 billion and 5.67 million employees". It adds that the "re-evaluation is reflected across industry sub-sectors".
   - Before the restatement, FY24 industry headcount was 5.43m (Strategic Review 2024 press release, CONFIRMED). The restatement added 0.24m, exactly equal to the GCC revision from 1.66m to 1.90m. A coincidence is unlikely but possible (INFERRED).
   - The 2025 release splits exports equally between "Global MNCs (including GCCs) and Indian service providers" (CONFIRMED).
   - The glossary of the 2026 Strategic Review executive summary defines GCCs as covering "the technology, engineering, and operations functions, including shared services centers of MNCs in India" (CONFIRMED).
   - Nasscom does a detailed GCC analysis "every five years" (CONFIRMED). Between those studies the GCC component appears to be modelled (INFERRED).
2. **The two products are on different vintages.**
   - The 2026 Strategic Review was published in February 2026 (PDF dated 6 March 2026, CONFIRMED). The 2026 GCC report came out in May–July 2026 (press release dated 2 July 2026, CONFIRMED).
   - So the Strategic Review's FY25–26 net additions (+126k/133k and +135k) do not include the 2026 GCC level (INFERRED).
   - The 2026 Strategic Review revised FY25 for "expanded segment coverage" (CONFIRMED). The 2027 Strategic Review will probably restate again (INFERRED).
3. **The 2026 GCC edition probably widened its coverage (INFERRED).**
   - GCC counts (CONFIRMED): 1,580 in FY23 (2023 edition); more than 1,700 in FY24 (2024 edition); 2,117 in FY26. That is +417 in two years, against +415 over FY19–24.
   - "32% growth since FY2021" implies about 1,604 GCCs in FY21, which is more than the 2023 edition's FY23 count.
   - The 2026 edition lists 583 mid-market and 504 PE-backed GCCs (CONFIRMED).
   - The 2024 edition projected 2.5–2.8m staff and 2,100–2,200 GCCs by 2030 (CONFIRMED). FY26 already reaches the 2030 GCC count, and its implied headcount growth (11.4%/yr) is well above that path (4.7–6.7%/yr).
4. **The GCC headcount covers all functions.** More than 90% of GCCs are multi-functional, spanning technology, operations and product engineering (CONFIRMED). No public split by function was found for all GCCs. The closest figures:

   | segment | ER&D | IT | BPM | source |
   |--|--|--|--|--|
   | Mega GCCs (about half of all GCC staff) | ~43% | ~24% | ~33% | ER&D and BPM CONFIRMED, Zinnov Sep 2025; IT computed as the residual |
   | All GCCs, FY23 | 695k of 1.66m (42%) | — | — | CONFIRMED, GCC 4.0 edition |
   | BFSI GCCs | 10% | 37% | 53% | search snippet only |

5. **The September 2024 restatement.**

   | | old basis | new basis |
   |--|--|--|
   | FY23 GCC headcount | 1.66m (GCC 4.0 edition, CONFIRMED) | not published |
   | FY24 GCC headcount | not found | 1.90m (CONFIRMED) |
   | FY24 industry headcount | 5.43m | 5.67m |

## 2. Scenarios
All figures are in thousands. "Rest of industry" = Nasscom change − GCC change − top-six change.

Inputs:
- **Nasscom change FY23→26:** +321 to +328k. This sums net additions within each vintage (60 + 126/133 + 135) and excludes the FY24 level revision.
- **Top-six change:** −61.5k (FY23→26) and +12k (FY24→26). These are global headcounts, not India-only.
- **Tech share of GCC staff:** 0.55, 0.67 or 0.80.

| window | scenario | GCC change, all functions | GCC tech change (0.55 / 0.67 / 0.80) | rest of industry |
|--|--|--|--|--|
| FY23–26 | S1: chained across the restatement (1.66m → 2.36m); invalid | +700 | 385 / 469 / 560 | −314 |
| FY23–26 | S2: restated basis; FY23 back-cast to 1.79–1.84m | +520 to +573 (central 540) | 297 / 362 / 432 | −154 (−190 to −131) |
| FY23–26 | S3: staffing-firm net hiring (60 + 110–140 + 200) | +370 to +400 (central 385) | 212 / **258** / 308 | **+1 (−18 to +19)** |
| FY23–26 | S4: 2024-edition path (+60, then 4.7–6.7%/yr) | +242 to +322 (central 282) | 155 / 189 / 226 | +104 (+60 to +147) |
| FY23–26 | S0: Nasscom total excludes GCCs (rejected) | — | — | +386 |
| FY24–26 | S2: 1.90m → 2.36m | +460 | 253 / 308 / 368 | −208 |
| FY24–26 | S3: staffing-firm net hiring | +310 to +340 | 179 / 218 / 260 | −73 |
| FY24–26 | S4: 2024-edition path | +182 to +262 | 122 / 149 / 178 | +30 |

Worked example (S3, FY23–26):
- Rest of industry: 325 − 385 − (−61.5) ≈ +1k.
- GCC tech change: 385 × 0.67 ≈ 258k.

S2 requires the rest of the industry (mid-tier firms, multinational vendors, BPM firms and small firms) to have shrunk by about 150k while the listed mid-tier firms grew. That is implausible. S3 and S4 bracket the plausible range.

## 3. RBI
- **The 2025-26 round of RBI's census of foreign liabilities and assets (FLA) is NOT out (CONFIRMED).**
  - Press releases prid 63300–63807 were scanned (6 August to 14 October 2026).
  - The latest entry on the census publications page is the 2024-25 round (29 October 2025, prid 61524).
  - prid 63479 (31 August 2026) is a different release: the survey of mutual funds' foreign assets and liabilities.
- **Software exports survey 2025-26 (prid 63625, 18 September 2026; CONFIRMED).**
  - It has no employment table.
  - It splits exporters by organisation type only: private limited, public limited and others.
  - Tables 8–10 cover foreign affiliates of Indian companies (Mode 3, $17.9bn), not foreign-owned firms operating in India.
- **Employee counts are collected but not published (CONFIRMED).**
  - The RBI FAQ says the survey asks for the "number of employees in item number 8 of Part C", as at end-March.
  - The counts are absent from the 2025-26 release and from Bulletin articles covering 2010-11, 2012-13, 2013-14 and 2016-17. The March 2018 article is the last full one found.

## 4. Sources
All URLs are also in `reconcile_inputs.csv`.
- **Nasscom (industry body), CONFIRMED:**
  - Strategic Review 2024 press release: https://nasscom.in/sites/default/files/media_pdf/nasscom-strategic-review-2024-press-release.pdf
  - Strategic Review 2025 press release: https://nasscom.in/sites/default/files/media_pdf/Nasscom%20SR%20Press%20release.pdf
  - Strategic Review 2026 executive summary: https://nasscom.in/modules/custom/nasscom_general/docs/Nasscom-Strategic%20Review-2026-Executive%20Summary.pdf
- **Nasscom–Zinnov GCC reports, CONFIRMED:**
  - GCC 4.0 edition: https://nasscom.in/knowledge-center/publications/gcc-40-india-redefining-globalization-blueprint
  - 2024 edition (5-Year Journey): https://nasscom.in/knowledge-center/publications/india-gcc-landscape-report-5-year-journey
  - IANS coverage of the 2024 edition: https://ianslive.in/gccs-projected-to-create-up-to-28-lakh-jobs-in-india-by-2030--20240912133249
  - 2026 edition landing page: https://zinnov.com/centers-of-excellence/zinnov-nasscom-india-gcc-landscape-2026-report/
  - 2026 edition press release: https://www.prnewswire.com/in/news-releases/india-s-gccs-are-increasingly-leading-the-ai-mandate-for-global-enterprises-driving-global-value-creation-nasscom--zinnov-report-302817463.html
- **Zinnov Mega GCC report, CONFIRMED:** https://zinnov.com/centers-of-excellence/decoding-mega-gccs-inside-the-rare-gcc-cohort-driving-impact-report/
- **Mid-market GCC report, secondary (news):** https://india.entrepreneur.com/technology/mid-market-gccs-set-to-drive-the-next-phase-of-growth/490546
- **RBI, CONFIRMED:**
  - prid 63625: https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63625
  - FAQ: https://rbi.org.in/SCRIPTs/FAQView.aspx?Id=142
  - Bulletin: https://www.rbi.org.in/Scripts/BS_ViewBulletin.aspx?Id=17425
  - Census publications page: https://rbi.org.in/Scripts/AnnualPublications.aspx?head=Annual+Census+on+Foreign+Liabilities+and+Assets+of+Indian+Companies
- **Staffing-firm hiring figures, secondary:** `../gcc/gcc_estimates_secondary.csv`.

## 5. Could not check
- The full 2026 GCC report (business-email form). It may contain a split by function, FY24–25 figures on the 2026 basis, and a statement on coverage.
- The full Strategic Review (members only), including its GCC sub-totals.
- The old-basis FY24 and restated FY23 GCC levels. "+36% headcount FY19–24" comes from a search snippet only.
- The RBI survey questionnaire (the .xls download hit a CAPTCHA; not bypassed).
- Bulletin articles after 2016-17 (none found).
- India-only headcount for the top six.
