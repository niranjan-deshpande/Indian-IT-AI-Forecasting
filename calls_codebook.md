# Earnings-call codebook

*Used to code `audit/calls_statements.csv`: 2,087 verbatim management statements from 183 transcripts, Jan 2021 – Oct 2026, eight firms. Coder 1 is the extraction agent (`audit/calls_coding_coder1.csv`). Coder 2 is a separate agent that saw only this codebook and the statements (`audit/calls_coding_coder2.csv`).*

## Categories

Assign each statement **one primary category** and, optionally, **one secondary category**.

| code | category | definition |
|---|---|---|
| **A** | Demand weakness | Clients spending less, deferring, or cutting discretionary work, for any reason. |
| **B** | Pricing stable | Management says prices or rates are holding. |
| **C** | Pricing pressure or deflation, not attributed to AI | Renewal discounts, competitive pricing, or rate cuts with no AI link. |
| **D** | AI productivity passed to clients | Savings from AI or automation explicitly given to clients through lower prices, smaller deal values, or productivity commitments. |
| **E** | Other or unclear | Anything that does not fit A–D. |

## Decision rules

1. **Code the quote.** If the statement answers an analyst question, the recorded context note can supply the link to AI (for example, the analyst asked about AI deflation).
2. **D requires two things:**
   - AI, GenAI, automation or "technology progress" is named, explicitly or through rule 1; and
   - savings reach clients: lower prices, smaller deal values, productivity commitments, or AI-linked deflation. Forecasts count.
3. **C covers pass-backs and pressure with no AI link.** This includes productivity commitments or pass-backs with no AI or automation named, generic pricing pressure, renewal discounts, and competitive pricing.
4. **E covers these pricing and productivity statements:**
   - price increases, COLA and realization gains;
   - AI productivity estimates that say nothing about passing savings to clients;
   - margin walks.
5. **B covers stable pricing and denials of AI deflation.** For example: "prices stable", "no deterioration", and explicit denials that AI is deflating pricing.
6. **A covers demand weakness.** This means spending cuts, deferrals, client caution, macro conditions, furloughs, ramp-downs, cancellations, and clients focusing on cost optimisation.
   - Demand strength is **E**.
   - Denials of weakness ("no slowdown", "no delays") are **E**.
7. **Mixed statements.**
   - Primary is the claim the statement presents as the explanation of the revenue, deal or headcount trend.
   - If an overall claim and a segment claim differ, primary is the overall claim.
   - The other claim goes to secondary.

## One example per category

All are verbatim and appear in `audit/calls_statements.csv`.

- **A. DEM-TCS-093.** TCS Q2FY24, 11 Oct 2023, K Krithivasan (CEO & MD), PDF p.23: "Our growth was affected by the holding back of discretionary spends by clients."
- **B. TCS-15.** TCS Q3FY24, 11 Jan 2024, Samir Seksaria (CFO), PDF p.17: "Gaurav, I will distinguish realization from pricing. Pricing environment is stable. Realization is an outcome. You can measure it as revenue per FTE and you will notice that it has been improving"
- **C. Accenture-18.** Accenture Q1FY25, 19 Dec 2024, Julie Sweet (Chair & CEO), PDF p.20: "It's a very competitive market, which is what we've been saying every quarter and we did see lower pricing across the business, which has been pretty consistent."
- **D. LTIMindtree-19.** LTIMindtree Q3FY25, 20 Jan 2025, Debashis Chatterjee (CEO & MD), PDF p.7: "Tech companies continue to be at the forefront of AI adoption. In the spirit of doing more for less, we are passing on AI-driven productivity benefits to our clients." (The quote opens with a sentence on vertical growth, omitted here.)
- **E. DEM-Infosys-010.** Infosys Q4FY21, 14 Apr 2021, Salil Parekh (CEO & MD), HTML exhibit: "In terms of what we are seeing in the demand environment, it is one of the strongest demand environments that we have seen for a while."

## Reliability

Coder 2 was a separate agent. It saw only the categories, rules and examples above, plus each statement's quote and its context note. The statements were shuffled, and coder 2 did not see coder 1's codes or which extraction pass a statement came from. Results are in `output/final/calls_agreement.csv` and `calls_confusion.csv`, produced by `scripts/final/calls_analysis.py`.

**Overall:** agreement on the primary category is **92.1%** (1,923 of 2,087), Cohen's κ = **0.87**. It is 81.5% on the pricing-pass statements and 94.6% on the demand-pass statements.

**By category:**

| category | coder 1 count | coder 2 count | both agree | coder 1's codes that coder 2 matched | positive agreement | κ (this category vs the rest) |
|---|---|---|---|---|---|---|
| A | 796 | 743 | 724 | 91.0% | 94.1% | 0.91 |
| B | 47 | 54 | 41 | 87.2% | 81.2% | 0.81 |
| C | 72 | 83 | 55 | 76.4% | 71.0% | 0.70 |
| D | 117 | 91 | 82 | 70.1% | 78.8% | 0.78 |
| E | 1,055 | 1,116 | 1,021 | 96.8% | 94.1% | 0.88 |

**Where the coders disagree:**
- **A vs E (71 cases):** coder 1 coded A, coder 2 coded E. These are mostly mixed statements about strength and weakness.
- **D vs C (22 cases):** coder 1 coded D, coder 2 coded C. In these the AI link is implied but not named in the quote, so coder 2 applied rule 3.

All 164 disagreements are listed for resolution in `calls_disagreements.csv`. A random sample of 30 statements (seed 20261006), with both codings, is in `calls_spotcheck.csv` for hand-checking.

**Figure 3** is drawn from coder 1's codes. A version from coder 2's codes is `figures/final/fig3_call_categories_coder2.png`, and it shows the same pattern.

## How the statements were extracted

Both passes use the same 183 transcripts, listed in `audit/calls_transcripts.csv`. Every transcript comes from a company IR site or SEC EDGAR. TCS Q4FY23 is missing: tcs.com blocks downloads, and no archive copy exists.

Both passes apply the same rules:
- management statements only;
- speaker confirmed against the transcript;
- quote machine-checked as a whitespace-normalised verbatim substring, with "..." marking an elision;
- page re-derived from the PDF (Infosys HTML exhibits have no pages).

### Pricing pass (previous round): 389 statements, `audit/price_calls_quotes.csv`

- **Keyword screen:** price/pricing, deflation, discount, renewal, give back, pass on/through, productivity commitment/benefit/gain, consolidation, cost take-out, fixed price, outcome-based, realization, rate card/increase/cut, bill rate, COLA, like-for-like, cannibalization, commercial model.
- **Selection:** each hit was read in context. Kept only management statements about prices, renewal terms, deflation or passing productivity to clients.
- **Yield:** about 2.1 statements per call.

### Demand pass (this round): 1,711 statements, `audit/demand_calls_quotes.csv`

- **Dictionary** (`audit/calls_demand_dictionary.json`): 12 term families — discretionary, demand, spending/budgets, caution, macro/uncertainty/"environment", delays/decision-making, ramp-down/insourcing, cancellations, slowdown/weakness, furlough/pause, verticals/geographies, headcount/hiring — plus demand-strength terms such as pipeline or robust.
- **Screen:** ±900-character windows around each hit. These covered 88–99% of each firm's text, so in practice every transcript was read in full.
- **Selection:** kept management statements that explain revenue, deals, growth or headcount through demand, in either direction (weakness or strength).
- **One row per distinct claim** within a call: overall demand, discretionary spend, each vertical, each geography, deal timing, link to hiring, outlook.
- **Duplicates:** near-duplicates within a call (≥60% word overlap) were dropped, keeping the clearer one. There was no cap on rows per call.
- **Yield:** about 9.3 statements per call.
- **Merge:** 389 + 1,711 − 13 cross-pass duplicates = 2,087. In each duplicate pair the pricing row was kept; pairs are logged in `audit/calls_merge_log.csv`.
- **Scripts:** `scripts/audit/calls_inventory.py`, `calls_demand_extract.py`, `calls_merge.py`, `calls_common.py`.

### Why per-category counts depend on extraction intensity

The demand pass read more broadly than the pricing pass (9.3 vs 2.1 statements per call). Raw counts of A and E (mostly from the demand pass) and of B, C and D (mostly from the pricing pass) therefore measure extraction intensity as well as what management said.

Figure 3 normalises by the number of transcripts, which fixes differences in calls per half-year. It does not fix differences between the passes. Within each category, the pattern over time is valid, because both passes used the same procedure in every half-year. Comparing levels across categories is not.
