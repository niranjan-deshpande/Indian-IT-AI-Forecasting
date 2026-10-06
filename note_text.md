---
title: Is AI hitting Indian IT services? What public data can and can't tell us
byline: Niranjan Deshpande · October 2026 · Pilot note
thanks: Written as part of SPAR (Fall 2026). Thanks to Andrei Potlogea for supervision. Data and code: {{repo}}.
---

<!--
HOW THIS FILE WORKS
This is the text of the note. `python3 scripts/final/build_note.py` turns it into docs/index.html.
Edit freely. A few conventions:
  - "## 1. Summary" makes a numbered section; "### 5a. Contractors" a subsection.
  - *italic*, **bold**, [link text](https://...) work as usual. Straight quotes become curly ones.
  - A block between "::: figure NAME" and ":::" is the caption of that figure. The chart itself is built
    from the repo CSVs. Names: fact, midtier, verticals, residual, subcontracting, calls, bls.
  - "::: table residual" and "::: table agreement" are tables built from the repo CSVs; you write the
    caption (first line) and the note (after the line "---").
  - "::: table" with no name holds a table you write yourself, in pipe format.
  - $$ ... $$ on their own lines make a displayed equation (LaTeX).
  - {{quote infosys}} and similar insert a verified quote with its attribution. The wording comes from
    note_quotes.md and should not be edited here.
  - {{repo}} inserts the repository link.
  - Under "## Appendix", each "###" heading becomes a collapsible block.
  - HTML comments like this one are kept in the page source but not shown.
-->

## 1. Summary

Headcount at India's six largest IT services firms grew for years: by about 7% a year before COVID, and by 14% in FY23 (the year to March 2023). In FY24 it fell 4%, and it has been roughly flat since. Smaller Indian rivals kept growing.

Is AI the cause? Clients may have cut spending or moved work elsewhere. Or AI may have cut the labor each project needs. Using just public data, we cannot distinguish falling demand from AI savings being passed on to clients as lower prices. Observing prices would help, but these data are not public.

The data do show three things. At the four firms where it can be tested, there is no sign that firms kept AI savings for themselves. There is no sign that they replaced staff with contractors. And from mid-2024, managers began to say they were passing AI savings to clients, while still citing weak demand.

A price index for IT services, along with two new disclosures by the firms, would settle the question.

## 2. The fact

The six firms are TCS, Infosys, HCLTech, Wipro, Tech Mahindra and LTIMindtree (LTI plus Mindtree before they merged). Years are Indian fiscal years, April to March.

On a simple average across the six, headcount grew about 7% a year from FY16 to FY20, then 18% in FY22 and 14% in FY23 as the firms hired after COVID. In FY24 it fell about 4%, the first fall since our data begin in FY16, and it has barely grown since. Revenue in constant currency, which removes the effect of exchange rates, slowed from about 9% a year before COVID to 1–3% a year from FY24 (Figure 1).

::: figure fact
**Figure 1.** Annual growth at the top six and at Accenture and Cognizant, FY16–FY26. The shaded band marks FY24. Growth is the log change ×100, close to the percentage change. Accenture and Cognizant are converted to Indian fiscal years; Accenture's year ends a month earlier, so 11 of its 12 months overlap. Before FY24 the average covers four or five firms, because some lack constant-currency revenue.
:::

We should note, however, that FY22 and FY23 were boom years, so part of the FY24 fall is a correction; and that this fall was broad, since headcount fell at five of the six firms (all except HCLTech). Accenture and Cognizant slowed too. Accenture's headcount barely grew in FY24, and Cognizant's shrank in both FY24 and FY25.

Smaller Indian firms did not follow. Four mid-tier firms (Persistent, Coforge, Mphasis and Hexaware) grew faster than the top six throughout FY22–FY26, and the revenue gap widened sharply from FY25 (Figure 2). In FY25 and FY26 they grew revenue by 14–15% a year, against 2–3% for the top six.

::: figure midtier
**Figure 2.** Growth at the top six and at four mid-tier firms, FY22–FY26 (log change ×100). Growth of total US-dollar revenue and of total year-end headcount. Acquisitions are included. Hexaware reports calendar years, each matched to the Indian fiscal year that ends three months later.
:::

The contrast does not depend on how firms count staff. Mphasis and Hexaware include contractors in their headcount; without them, Persistent and Coforge grew even faster (dashed line). Nor does it rest on one acquisition: without Coforge, which bought Cigniti in FY25, mid-tier revenue still grew more than 10% that year.

The mid-tier firms also serve a different mix of clients (Figure 3). They depend more on financial services, and Persistent earns most of its revenue from software and healthcare clients.

::: figure verticals
**Figure 3.** Share of revenue by client industry. Top six: January–March 2026. Mid-tier firms: FY26 (Hexaware: calendar 2025). Financial services includes banking and insurance. Firms group industries differently; "not separate" means the firm reports that industry only combined with another (hover for each firm's own categories).
:::

So this is not a uniform hit to Indian IT. Any explanation has to account for why the largest firms in particular stopped growing. But the mid-tier firms are small: their share of the ten firms' combined revenue rose only from 5% in FY21 to 7% in FY26, so they can account for only a small part of the top six's slowdown.

## 3. Four scenarios

There are a few scenarios that could produce these descriptive facts:

- **S1** Demand fell: clients cut spending.
- **S2** Each unit of work needed less labor, prices held, and the firms kept the savings.
- **S3** Each unit of work needed less labor, and the firms passed the savings to clients as lower prices.
- **S4** Work moved to other providers: clients' own offices in India (global capability centres, or GCCs), smaller vendors, or contractors.

AI could lie behind any of these: not only S2 and S3, but also S1, if clients use AI to do the work themselves, and S4, if they move work to providers that use AI more. So the question is which mechanism is at work, not whether AI is involved.

Revenue and headcount fall under S1, S3 and S4 alike, so they cannot tell these apart. Table 1 adds three measures that can:

- **The residual** is the growth in revenue per employee that is not explained by changes in how much of their time staff spend on billable work. Section 4 explains it.
- **The subcontracting share** is spending on subcontractors (outside staff hired to do part of the work) as a share of revenue. If a firm replaced employees with subcontractors, its headcount would fall but this share would rise.
- **Other providers** are smaller vendors and GCCs.

In the rest of this note, we examine each of these measures in turn.

::: table
**Table 1.** What each scenario predicts
| | Revenue | Headcount | Residual | Subcontracting share | Other providers |
|---|---|---|---|---|---|
| S1 · demand fell | ↓ | ↓ | flat | ↓ or flat | slow too |
| S2 · savings kept | flat | ↓ | ↑ | — | — |
| S3 · savings passed on | ↓ | ↓ | flat (full pass-through) | — | — |
| S4 · work moved | ↓ | ↓ | flat | ↑ (contractor version) | grow |
---
A dash means no specific prediction.
:::

## 4. What revenue per employee can and can't show

Growth in revenue per employee splits into two parts:

$$
g_{R/L} = g_u + (g_p - g_a)
$$

Here *g* means growth, *R* is revenue, *L* is headcount, *u* is utilization (the share of staff time billed to clients), *p* is the price per unit of work, and *a* is the labor needed per unit of work. In words: revenue per employee rises if staff bill more of their time, if each unit of work sells for more, or if each unit takes less labor. The term in brackets is the residual.

We observe revenue and headcount for every firm and utilization for some, but not price, labor per unit or the amount of work. So we can compute the residual but not split it into its two parts.

Luckily, the residual is still informative. Suppose AI cuts the labor needed per unit of work by *s*% a year, so *g*<sub>a</sub> = −*s*. Suppose firms pass a share *φ* of this saving to clients by cutting prices, so *g*<sub>p</sub> = −*φs*. Then the residual is

$$
g_p - g_a = -\varphi s + s = (1 - \varphi)\, s
$$

If firms keep all the savings (S2, *φ* = 0), the residual rises by the full *s*: a 4% labor saving raises it by 4 points. If they pass on all of it (S3 with *φ* = 1), the residual does not move. A fall in demand (S1) also leaves it unchanged, because price and labor per unit stay the same. So under full pass-through, S1 and S3 look identical in these data.

Figure 4 shows the residual for each firm that reports utilization. It did not rise after FY23. Table 2 shows that this holds if we drop the COVID year, FY21, or keep only the firms with data in both periods.

::: figure residual
**Figure 4.** The residual (growth in revenue per employee net of utilization), by firm and year, FY16–FY26. Solid lines are averages over firm-years before and from FY24. The dashed line shows what S2 would predict if AI saved 4% of labor a year, an illustrative figure.
:::

::: table residual
**Table 2.** Average residual, % a year
---
Average over firm-years; small grey numbers count firm-years. Before FY24 the firms with data are HCLTech, Infosys, Tech Mahindra and Wipro; from FY24, Infosys, the LTI group, Tech Mahindra and Wipro. The second row keeps the three firms present in both periods.
:::

This test has limits. It covers only four firms, because TCS, the largest, and HCLTech do not report utilization. TCS's revenue per employee grew about 4% a year in FY24 and FY25, more than twice its FY16–20 pace, and we cannot tell why. And Infosys's jump in FY24 may be an accident of counting: its headcount includes trainees but its utilization does not, and it hired far fewer trainees that year.

So the evidence is weak: on average, the four firms we can test show no sign of keeping AI savings. Telling S1 from S3 needs price data, which Section 6 discusses.

## 5. Other evidence

### 5a. Contractors

If the firms had replaced employees with subcontractors, the subcontracting share would have risen. Instead it fell at all six firms in FY24 (Figure 5). It rose at five of the six in FY26, but it remains below its FY23 level everywhere. So there is no evidence of a shift to contractors, although the share measures spending rather than people, so changes in contractor rates also move it.

::: figure subcontracting
**Figure 5.** Spending on subcontractors as a share of revenue, FY20–FY26, as reported by each firm. LTIMindtree starts in FY22. For TCS the series is fees paid to outside consultants.
:::

### 5b. Where the work went

Some work may also have moved to GCCs. Three public sources bear on this:

- **Foreign-owned companies in India** raised their exports of information and communication services from ₹6.5 lakh crore in FY22 to ₹8.5 lakh crore in FY23 (Reserve Bank of India census).
- **Indian affiliates of US companies** employed about 900,000 people in professional services in 2023, up from about 600,000 in 2019 (US Bureau of Economic Analysis).
- **Job postings** by GCCs in September 2026 were up 4% on a year earlier, while postings by IT services firms were down 4% (Naukri).

These fit a partial shift to GCCs, but they are weak evidence: the first two include foreign-owned IT vendors as well as clients' own offices, and postings are not hires.

### 5c. What management said

We collected 2,087 statements by managers from 183 earnings-call transcripts: the six firms plus Accenture and Cognizant, 2021–2026. Two large language models (LLMs) independently sorted each statement into one of five categories, and agreed on 92% of them. Figure 6 tracks two categories: weak demand (A) and AI savings passed to clients (D).

::: figure calls
**Figure 6.** Statements per earnings-call transcript, by half-year. Small numbers under the axis count transcripts. The second half of 2026 is incomplete (8 transcripts) and drawn lighter. A and D were collected in different passes, so compare trends within a panel, not levels across panels.
:::

Talk of weak demand peaked in 2023 at nearly eight statements per transcript and has since settled at about five. Talk of passing on AI savings was close to zero before mid-2024 and has risen since. Managers added the AI story to the demand story rather than replacing it. The pattern holds under either model's codes.

In late 2023 the explanation was demand:

{{quote infosys}}

In early 2024, TCS said prices were stable:

{{quote seksaria}}

By 2025 and 2026, managers described passing AI savings to clients:

{{quote krithivasan}}

{{quote vijayakumar}}

These are claims, not measurements: managers choose which explanations to give investors.

## 6. The price gap

Telling S1 from S3 needs the prices these firms charge per unit of work, and no such measure exists. India has no price index for IT services, and the US Bureau of Labor Statistics (BLS) does not cover computer systems design ([Areas of Noncoverage](https://www.bls.gov/ppi/fd-id/areas-of-noncoverage-in-the-ppi-system.htm)).

The nearest substitutes are weak. A BLS index for US data processing and hosting, which tracks the price of the same contracts over time, has risen every year since 2015, by 0.3% to 3.2% (Figure 7). But it covers US firms only. ISG, a sourcing adviser, reports that prices in a narrow set of managed-services contracts have recently been falling faster.

::: figure bls
**Figure 7.** BLS producer price index for data processing and hosting (PPI 518210), change in the annual average. 2026 compares January–August with the same months of 2025.
:::

Infosys offers a partial check for an earlier period. Until FY20 it reported billed person-months, and revenue per billed person-month equals *p*/*a*. If labor per unit did not rise (an assumption), Infosys's prices fell by at least 1–2% a year in FY15–17 and were flat or falling in FY18–20. The series ends before the period that matters.

Analysts' estimates of AI price cuts, such as Kotak's and Jefferies', assume a pass-through rate, so they cannot test one. The appendix lists every source we checked.

## 7. What would settle it

Four kinds of data would settle the question (Table 3).

::: table
**Table 3.** Data that would separate the scenarios
| Data | Who could collect it | Separates | Available? |
|---|---|---|---|
| A price index for IT services | India's statistics office or the RBI | S1 from S3 | No |
| Billed effort (person-months) | The firms; SEBI, the market regulator, could require it | S2 from S1 and S3† | Infosys to FY20, LTI to 2022 |
| GCC headcount by parent company | The RBI, in its census of foreign-owned companies | S1 from S4 | No |
| Headcount by role, for each firm | The firms | S2 and S3 from S1 | No |
---
† With revenue, billed effort gives *p*/*a*, the same quantity as the residual, for TCS and HCLTech too. Like the residual, it cannot separate S1 from S3 under full pass-through.
:::

The cheapest step with the biggest payoff is a price index for IT services, because every other conclusion here is limited by its absence.

## 8. Limitations

1. The sample is six large firms, plus four mid-tier firms in one comparison.
2. TCS and HCLTech do not report utilization, so their revenue per employee cannot be broken down.
3. The data were collected with the help of LLMs. A check of 30 random values against the source documents found no errors.
4. The call statements were coded by two LLMs working independently and have not been checked by hand.
<!-- UPDATE after manual spot check of calls_spotcheck.csv -->
5. Managers' statements reflect what they want investors to hear.
6. The figures are not adjusted for acquisitions.

## Appendix: data and methods

### Sources

Quarterly fact sheets, investor releases, annual reports, SEC filings (20-F and 6-K) and earnings-call transcripts, from company websites and SEC EDGAR. Other series: the RBI Census on Foreign Liabilities and Assets, BEA data on US multinationals' foreign affiliates, Naukri JobSpeak and the BLS producer price index. Every number traces to a file in the repository: {{repo}}.

### Definitions

- **Growth** is the log change ×100.
- **Fiscal years** run April to March. Quarterly year-on-year growth is combined into fiscal-year growth using the previous year's revenue as weights; a fiscal year needs all four quarters.
- **Headcount growth** is the average of the four quarterly year-on-year changes, which approximates growth of average headcount.
- **Comparators** are converted to Indian fiscal years. Cognizant's quarters line up exactly; Accenture's end in May, August, November and February, so 11 of 12 months overlap.
- **The residual** is revenue-per-employee growth in constant currency minus the change in utilization, within each firm's own utilization series.

### Audit

- **Spot check.** 30 random values were checked against the source documents; all 30 matched.
- **Corrections.** LTI and Mindtree negative growth rates, printed as "(x.x)%", had lost their minus sign; the parser now reads them correctly. Cognizant's attrition used a different definition in two quarters and now uses the trailing-twelve-month rate throughout. Accenture's FY18 US-dollar revenue growth mixed figures from before and after an accounting change (ASC 606); it now uses like-for-like growth from Accenture's FY18 releases.
- **Decisions.** The LTI business is counted once: LTI plus Mindtree through FY22, LTIMindtree from FY23. HCLTech's sale of a business is not adjusted for, because HCLTech did not disclose its revenue. Wipro growth figures that span a break in its reporting are left out.
- **Dropped.** An earlier version compared how closely the Indian firms tracked Accenture before and after 2023. That comparison rested on a single episode, the boom and bust of 2021–22, and is not used.

### Call coding

Each statement gets one main category:

- **A, demand weakness:** clients spending less, or delaying or cutting discretionary work.
- **B, pricing stable:** prices or rates are holding, or AI is not cutting prices.
- **C, pricing pressure without AI:** renewal discounts, competitive pricing or rate cuts, with no link to AI.
- **D, AI savings passed to clients:** savings from AI or automation given to clients through lower prices, smaller deals or productivity commitments.
- **E, other or unclear:** anything else, including statements that demand is strong.

::: table agreement
**Agreement between the two models**, main category
---
"Model 1 codes matched" is the share of the first model's codes in each category that the second model also gave. κ is Cohen's kappa, which measures agreement beyond chance, for that category against the rest.
:::

**How the statements were collected.** A pricing pass searched for keywords and kept 389 statements about prices, renewals or passing savings to clients (about 2 per call). A demand pass used 12 groups of search terms, read effectively every transcript in full, and kept 1,711 statements that explain revenue, deals or headcount through demand (about 9 per call). Merging the two and removing 13 duplicates gives 2,087. Every quote was checked by machine to be word for word, from a manager, with the speaker confirmed. A comes mostly from the demand pass and D from the pricing pass, so their levels should not be compared.

### Price data: what we looked for

We looked for any measure of the price these firms charge per unit of work (*p*), in any period since 2015, and found none. Most series that exist measure the price of an hour or a person-month of labor. That is *p*/*a*, which rises when AI cuts the labor per unit of work even if the price per unit is unchanged, so it cannot separate the scenarios.

::: table
**Price sources checked**
| Source | What it measures | Why it falls short |
|---|---|---|
| US BLS producer price index for computer systems design (NAICS 5415) | Nothing: BLS has never published one | — |
| US BLS index for IT technical support and consulting | Prices of a thin, partial sample of US contracts | US producers only; erratic (+23% in 2024) |
| US BEA price indices for custom software and computer systems design | Modelled from input costs and an assumed productivity rate | No prices observed; the assumption builds in the answer |
| US BEA price index for imports of computer services | Built from US domestic producer prices | Does not observe Indian vendors |
| UK, EU and Japanese producer price indices for IT services | Domestic prices, mostly per hour, day or person-month | Price per unit of labor (*p*/*a*); domestic producers only |
| India: wholesale prices, new services price indices, national accounts | Goods; finance, telecom and transport services; IT output deflated with goods or consumer prices | No IT services price |
| Infosys annual reports (20-F) | Revenue per billed person-month, FY03–FY20 | *p*/*a*; one firm; stops in FY20 |
| Wipro annual reports; LTI fact sheets | Price realization, FY09–FY12; billed person-months to 2022 | *p*/*a*; short series |
| TCS, HCLTech, Tech Mahindra | No price or billed-effort figure ever disclosed | — |
| Accenture and Cognizant filings | A sentence on "pricing" each quarter | Direction only; Accenture's "pricing" means contract margin |
| ISG (sourcing adviser) | Unit prices in managed-services contracts | A true price per unit, but for a narrow, mostly infrastructure slice, across all vendors |
| Everest Group Pricing Index | Price per full-time worker, by delivery country | *p*/*a*; free editions end in 2024 |
| Gartner, HFS Research | Surveys of what clients expect to pay | Expectations, not prices |
| Everest PriceBook, Avasant, Forrester, NelsonHall | Rate cards and benchmarks | Paywalled; not seen |
| Nasscom | Industry reviews | No price figures |
| Equity research (about 45 reports and press summaries) | Forecasts of AI "deflation"; revenue per employee | See below |
| Earnings calls (389 statements about pricing) | What managers say about prices | Claims, not measurements |
---
Links, page references and figures for every source are in `price_data.md` in the repository.
:::

**Equity research.** Brokers do publish industry-wide numbers, but none is a measured price. Kotak, Jefferies, HSBC, ICICI Securities and CLSA forecast that AI will cut industry revenue by about 2–4% a year from 2025 to 2028; Kotak's gross estimate is about 16% over three years, and Jefferies' about 20% over 2025–30. Each is built by multiplying an estimated productivity gain by an assumed share passed on to clients, so it assumes the answer to our question. Other reports compile revenue per employee, which mixes price, labor per unit and utilization. We found no broker that estimates a historical, industry-wide price per unit of work. This is not surprising: since Infosys stopped reporting billed effort in FY20, no public data allow it.

The closest thing to an industry average is Everest's price per full-time worker delivered from India, which changed by between +3.1% and −0.4% a year in 2023–24. But that is a price per unit of labor, not per unit of work.

**Gaps in the search.** We saw only press summaries of the full Kotak, HSBC, Jefferies and CLSA reports, which are paywalled. We found no quantified estimates from Nomura, Goldman Sachs, BofA, Citi, UBS, Macquarie or Bernstein. The web search reached its query limit, so it was not exhaustive: we did not check the mid-tier firms' disclosures, the RBI, or India's earlier pilot service price indices.

