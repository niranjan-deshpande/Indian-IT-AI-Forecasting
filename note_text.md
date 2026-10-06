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
  - A block between "::: figure 1" and ":::" is the caption of that figure. The chart itself comes from the repo CSVs.
  - "::: table midtier", "::: table residual" and "::: table agreement" are tables built from the repo CSVs;
    you write the caption (first line) and the note (after the line "---").
  - "::: table" with no name holds a table you write yourself, in pipe format.
  - {{quote infosys}} and similar insert a verified quote with its attribution. The wording comes from
    note_quotes.md and should not be edited here.
  - {{bls_sparkline}} inserts the small bar chart of the BLS index; {{repo}} inserts the repository link.
  - Under "## Appendix", each "###" heading becomes a collapsible block.
  - HTML comments like this one are kept in the page source but not shown.
-->

## 1. Summary

Headcount at India's six largest IT services firms grew 14% in FY23 (the year to March 2023). In FY24 it fell 4%, and it has been roughly flat since. Smaller Indian rivals kept growing.

Is AI the cause? Clients may simply have cut spending, or moved work elsewhere. Or AI may have cut the labor each project needs, with the savings passed to clients as lower prices. Public data cannot separate this last explanation from a fall in demand. The two look the same unless you can see prices, and no one measures the prices these firms charge.

The data do show three things. At the four firms where it can be tested, there is no sign that firms kept AI savings for themselves. There is no sign that they replaced staff with contractors. And from mid-2024, managers began to say they were passing AI savings to clients, while still citing weak demand.

A price index for IT services, along with two new disclosures by the firms, would settle the question.

## 2. The fact

The six firms are TCS, Infosys, HCLTech, Wipro, Tech Mahindra and LTIMindtree (counted as LTI plus Mindtree before they merged). Years are Indian fiscal years, which run from April to March.

On a simple average across the six firms, headcount grew about 7% a year from FY16 to FY20. In FY22 and FY23 it grew much faster, by 18% and 14%, as the firms hired heavily after COVID. In FY24 it fell by about 4%, the first fall since our data begin in FY16. It has barely grown since. Revenue slowed at the same time. In constant currency, which removes the effect of exchange rates, it grew about 9% a year before COVID but only 1–3% a year from FY24. Figure 1 shows these series alongside two rivals based outside India, Accenture and Cognizant.

::: figure 1
**Figure 1.** Annual growth at the top six firms and at Accenture and Cognizant, FY16–FY26. Revenue is in constant currency. The shaded band marks FY24. Growth is the log change ×100, which is close to the percentage change. Accenture and Cognizant are converted to Indian fiscal years (April–March); Accenture's year ends a month earlier, so 11 of its 12 months overlap. Before FY24 some firms lack constant-currency revenue, so the average covers four or five firms. Hover over a point to see exact values.
:::

Three points qualify this picture. First, FY22 and FY23 were boom years, so part of the FY24 fall is a correction. Second, the fall was broad: headcount fell at five of the six firms, all except HCLTech. Third, Accenture and Cognizant slowed too. Accenture's headcount barely grew in FY24, and Cognizant's shrank in both FY24 and FY25.

Smaller Indian firms did not follow the same path. Table 1 compares the top six with four mid-tier firms: Persistent, Coforge, Mphasis and Hexaware. In FY25 and FY26 the mid-tier firms grew revenue by 14–15% a year, against 2–3% for the top six.

::: table midtier
**Table 1.** Growth at the top six and at four mid-tier firms (%)
---
Growth of total US-dollar revenue and of total year-end headcount, as log change ×100. Acquisitions are included. Hexaware reports calendar years; each is matched to the Indian fiscal year that ends three months later.
:::

So this is not a uniform hit to Indian IT. Any explanation has to account for why the largest firms in particular stopped growing.

The comparison has limits. The mid-tier figures include acquisitions, although their revenue growth stays above 10% in FY25 even without Coforge, which bought Cigniti that year. Mphasis and Hexaware count contractors as staff. The mid-tier firms also specialize in different kinds of work. Finally, they are small. Their share of the combined revenue of all ten firms rose only from 5% in FY21 to 7% in FY26, so they can account for only a small part of the top six's slowdown.

## 3. Four explanations

Four explanations could produce these facts. Each is defined by what happened, not by whether AI was involved.

- **S1** Clients cut spending: demand fell.
- **S2** Each unit of work needed less labor, and prices stayed the same. The firms kept the savings.
- **S3** Each unit of work needed less labor, and the firms passed the savings to clients as lower prices.
- **S4** Work moved to other providers: clients' own offices in India (known as global capability centres, or GCCs), smaller vendors, or contractors.

AI could lie behind any of these. It is the obvious cause of S2 and S3. But clients might also cut spending because they use AI to do the work themselves (S1), or move work to providers that use AI more (S4). So the useful question is not whether AI is involved, but which mechanism is at work.

Revenue and headcount fall under S1, S3 and S4 alike, so they cannot tell these apart. Table 2 lists what each explanation predicts for other measures. The rest of the note takes these measures in turn.

::: table
**Table 2.** What each explanation predicts
| | Revenue | Headcount | Residual* | Subcontracting share | Other providers |
|---|---|---|---|---|---|
| S1 · demand fell | ↓ | ↓ | flat | ↓ or flat | slow too |
| S2 · savings kept | flat | ↓ | ↑ | — | — |
| S3 · savings passed on | ↓ | ↓ | flat (full pass-through) | — | — |
| S4 · work moved | ↓ | ↓ | flat | ↑ (contractor version) | grow |
---
\* Revenue per employee, after removing changes in utilization (the share of staff time billed to clients). Section 4 explains it. A dash means the explanation makes no specific prediction.
:::

## 4. What revenue per employee can and can't show

Revenue per employee is the measure most likely to separate the explanations. Its growth splits into two parts:

$$
g_{R/L} = g_u + (g_p - g_a)
$$

Here *g* means growth. *R* is revenue and *L* is headcount, so the left side is growth in revenue per employee. *u* is utilization, the share of staff time billed to clients. *p* is the price a firm charges per unit of work, and *a* is the labor needed per unit of work. The term in brackets is the *residual*: the part of the growth in revenue per employee that changes in utilization do not explain.

We can measure revenue and headcount for every firm, and utilization for some. We cannot measure price, labor per unit of work, or how much work was done. So we can compute the residual, but we cannot split it into its two parts.

The residual still tells us something. Suppose AI cuts the labor needed per unit of work, and firms pass a share *φ* of the savings to clients as lower prices. Then the residual rises by (1 − *φ*) times the labor saving. If firms keep all the savings (S2, where *φ* = 0), the residual should rise by the full saving, which would be several points a year. If they pass on all of it (S3 with *φ* = 1), the residual does not move. In that case revenue, headcount and utilization look exactly as they would if demand had fallen (S1), and these data cannot tell the two apart.

Table 3 compares the residual before and after FY24. It did not rise.

::: table residual
**Table 3.** Average residual, % a year
---
Average over firm-years; the small grey numbers count the firm-years. Before FY24 the firms with data are HCLTech, Infosys, Tech Mahindra and Wipro; from FY24 they are Infosys, the LTI group, Tech Mahindra and Wipro. The second row keeps only the three firms present in both periods.
:::

Three things limit this test. First, it covers only four firms: Infosys, Wipro, Tech Mahindra and the LTI group. TCS, the largest firm, and HCLTech do not report utilization. Second, TCS's revenue per employee grew about 4% a year in FY24 and FY25, more than twice its pace in FY16–20, but without utilization data we cannot tell why. Third, Infosys's residual jumped in FY24, and this may be an accident of counting. Infosys includes trainees in its headcount but not in its utilization, and it hired far fewer trainees that year.

So the evidence is weak. It shows no sign, on average, that the four firms we can test kept AI savings. To tell S1 from S3 we would need data on prices, which Section 6 discusses.

## 5. Other evidence

### 5a. Contractors

If the firms had replaced employees with contractors (the contractor version of S4), their spending on subcontractors would have risen as a share of revenue. Instead it fell at all six firms in FY24 (Figure 2). It rose again at five of the six in FY26, but it is still below its FY23 level at every firm.

::: figure 2
**Figure 2.** Spending on subcontractors as a share of revenue, FY20–FY26, as reported by each firm. LTIMindtree starts in FY22. The shaded band marks the step from FY23 to FY24. For TCS the series is fees paid to outside consultants.
:::

So there is no evidence of a shift to contractors. One caveat: this measures spending, not the number of contractors, so a change in the rates contractors charge would also move it.

### 5b. Where the work went

Section 2 showed that smaller Indian firms kept growing. Some work may also have moved to GCCs. Three public sources bear on this. Foreign-owned companies in India, as counted by the Reserve Bank of India's census, raised their exports of information and communication services from ₹6.5 lakh crore in FY22 to ₹8.5 lakh crore in FY23. Indian affiliates of US companies employed about 900,000 people in professional services in 2023, up from about 600,000 in 2019, according to the US Bureau of Economic Analysis. And on the job site Naukri, postings by GCCs in September 2026 were up 4% on a year earlier, while postings by IT services firms were down 4%.

These figures fit the idea that some work moved to GCCs, but they are weak evidence. The first two include foreign-owned IT vendors as well as clients' own offices, and job postings are not hires. At most, they are consistent with a partial shift of this kind.

One piece of evidence from the earlier pilot is dropped here. The pilot compared how closely the Indian firms tracked Accenture before and after 2023. That comparison turned out to rest on a single episode, the boom and bust of 2021–22.

### 5c. What management said

Earnings calls show how managers explained the slowdown. We collected 2,087 statements by managers from 183 earnings-call transcripts, covering the six firms plus Accenture and Cognizant from 2021 to 2026. Two large language models (LLMs) each sorted every statement into one of five categories, working independently. They agreed on 92% of statements. Figure 3 tracks two of the categories: statements about weak demand (category A), and statements that AI savings were being passed to clients (category D).

::: figure 3
**Figure 3.** Statements per earnings-call transcript, by half-year, 2021–2026. The small numbers under the axis count the transcripts in each half-year. The second half of 2026 is incomplete (8 transcripts) and drawn lighter. Categories A and D were collected in different passes, so compare trends within a panel, not levels across panels.
:::

Talk of weak demand peaked in 2023, at nearly eight statements per transcript, and has since settled at about five. Talk of passing AI savings to clients was close to zero before mid-2024 and has risen since. Managers added the AI story to the demand story; they did not swap one for the other. The pattern is the same whichever model's codes are used.

The shift shows in the managers' own words. In late 2023 the explanation was demand:

{{quote infosys}}

In early 2024, TCS said prices were stable:

{{quote seksaria}}

By 2025 and 2026, managers were describing AI savings passed to clients:

{{quote krithivasan}}

{{quote vijayakumar}}

These are claims, not measurements. Managers choose which explanations to give investors.

## 6. The price gap

To tell S1 from S3, we need the prices these firms charge per unit of work. No such measure exists. India has no price index for IT services. The US Bureau of Labor Statistics (BLS) does not cover computer systems design in its producer price index ([Areas of Noncoverage](https://www.bls.gov/ppi/fd-id/areas-of-noncoverage-in-the-ppi-system.htm)).

The nearest substitutes are weak. A BLS index for US data processing and hosting tracks the price of the same contracts over time. It has risen every year since 2015, by between 0.3% and 3.2% {{bls_sparkline}}. But it measures prices charged by US firms, so it is a proxy at best. ISG, a sourcing adviser, tracks prices in a narrow set of managed-services contracts, and reports that these prices have recently been falling faster.

Infosys offers a partial check for an earlier period. Until FY20 it reported how many person-months of work it billed. Revenue per billed person-month equals the price per unit of work divided by the labor per unit (*p*/*a*). If labor per unit did not rise, which is an assumption rather than a fact, then Infosys's prices fell by at least 1–2% a year in FY15–17 and were flat or falling in FY18–20. But this series ends before the period that matters.

Analysts at brokers such as Kotak and Jefferies have estimated how far AI will cut prices. Their estimates assume a pass-through rate, so they cannot be used to test one.

## 7. What would settle it

Four kinds of data would separate the explanations (Table 4). None is public today in usable form.

::: table
**Table 4.** Data that would separate the explanations
| Data | Who could collect it | Separates | Available? |
|---|---|---|---|
| A price index for IT services | India's national statistics office or the RBI | S1 from S3 | No |
| Billed effort (person-months) | The firms; SEBI, India's market regulator, could require it | S2 from S1 and S3, with revenue† | Infosys until FY20, LTI until 2022 |
| GCC headcount by parent company | The RBI, as part of its census of foreign-owned companies | S1 from S4 | No |
| Headcount by role, for each firm | The firms | S2 and S3 from S1 | No |
---
† Revenue per billed person-month is *p*/*a*, the same quantity as the residual. It would extend the Section 4 test to TCS and HCLTech, but like the residual it cannot separate S1 from S3 if savings are fully passed on.
:::

The cheapest step with the biggest payoff is a price index for IT services, because every other conclusion in this note is limited by its absence.

## 8. Limitations

1. The sample is six large firms, plus four mid-tier firms in one comparison.
2. TCS and HCLTech do not report utilization, so their revenue per employee cannot be broken down.
3. The data were collected with the help of LLMs. A check of 30 randomly chosen values against the source documents found no errors.
4. The earnings-call statements were coded by two LLMs working independently, and have not been checked by hand.
<!-- UPDATE after manual spot check of calls_spotcheck.csv -->
5. Managers' statements reflect what they want investors to hear.
6. The figures are not adjusted for acquisitions.

## Appendix: data and methods

### Sources

Quarterly fact sheets, investor releases, annual reports, filings with the US Securities and Exchange Commission (20-F and 6-K), and earnings-call transcripts from company websites and SEC EDGAR. The mid-tier figures come from annual reports. Other series: the RBI Census on Foreign Liabilities and Assets, BEA data on US multinationals' foreign affiliates, Naukri JobSpeak and the BLS producer price index. Every number traces to a file in the repository: {{repo}}.

### Definitions

- **Growth** is the log change ×100, which is close to the percentage change.
- **Fiscal years** are Indian fiscal years, April to March. Quarterly year-on-year growth is combined into fiscal-year growth using the previous year's revenue as weights. A fiscal-year value needs all four quarters.
- **Headcount growth** is the average of the four quarterly year-on-year changes, which approximates the growth of average headcount.
- **Comparators** are converted to Indian fiscal years. Cognizant's quarters line up exactly. Accenture's quarters end in May, August, November and February, so 11 of 12 months overlap.
- **The residual** is growth in revenue per employee in constant currency, minus the change in utilization within each firm's own series.

### Audit

- **Spot check.** 30 randomly drawn values were checked against the source documents. All 30 matched.
- **Corrections.** Negative growth rates for LTI and Mindtree, printed as "(x.x)%" in their reports, had lost their minus sign; the parser now reads them correctly. Cognizant's attrition used a different definition in two quarters and now uses the trailing-twelve-month rate throughout. Accenture's FY18 US-dollar revenue growth mixed figures from before and after an accounting change (ASC 606); it now uses the like-for-like growth from Accenture's FY18 releases.
- **Decisions.** The LTI business is counted once: LTI plus Mindtree through FY22, LTIMindtree from FY23. HCLTech's sale of a business is not adjusted for, because HCLTech did not disclose its revenue. Wipro growth figures that span a break in its reporting are left out.

### Call coding

Each statement gets one main category:

- **A, demand weakness:** clients spending less, or delaying or cutting discretionary work, for any reason.
- **B, pricing stable:** managers say prices or rates are holding, or deny that AI is cutting prices.
- **C, pricing pressure without AI:** renewal discounts, competitive pricing or rate cuts, with no link to AI.
- **D, AI savings passed to clients:** savings from AI or automation given to clients through lower prices, smaller deals or productivity commitments.
- **E, other or unclear:** anything else, including statements that demand is strong.

::: table agreement
**Agreement between the two models**, main category
---
"Model 1 codes matched" is the share of the first model's codes in each category that the second model also gave. κ is Cohen's kappa, a measure of agreement that allows for chance, for that category against the rest.
:::

**How the statements were collected.** The statements come from two passes over the same transcripts. A pricing pass searched for keywords and kept 389 statements about prices, renewals, falling prices, or passing savings to clients (about 2 per call). A demand pass used a list of 12 groups of terms, read effectively every transcript in full, and kept 1,711 statements that explain revenue, deals or headcount through demand (about 9 per call). Merging the two and removing 13 duplicates gives 2,087. Every quote was checked by machine to be word for word, from a manager, with the speaker confirmed. Category A comes mostly from the demand pass and category D from the pricing pass, which is why their levels should not be compared.
