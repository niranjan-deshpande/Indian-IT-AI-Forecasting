---
title: AI and jobs in Indian IT services: two questions
byline: Niranjan Deshpande · October 2026 · Working draft
thanks: Written as part of SPAR (Fall 2026), supervised by Andrei Potlogea. A checkpoint, not a finished note: numbers are provisional. Data and code: {{repo}}.
---

<!--
HOW THIS FILE WORKS
`python3 scripts/final/build_checkpoint.py` turns this file into docs/two-questions.html.
Conventions are those of note_text.md, plus:
  - [^key] marks a footnote; define it on its own line at the end as "[^key]: text". Footnotes show on hover.
  - "::: answer" ... ":::" is the short-answer box at the top of a section.
  - "::: details Title" ... ":::" is a collapsible block; it can hold paragraphs, lists and figures.
  - "::: figure NAME" ... ":::" holds a caption; the chart is built in build_checkpoint.py from repo CSVs.
-->

## Summary

Headcount at India's six largest IT services firms stopped growing in 2023. We ask two questions about AI's part in that.

1. **The replacement rate.** If a piece of work used to take 100 workers, how many does it take now?
2. **The demand response.** When AI makes the work cheaper, do clients buy more of it?

Our provisional answers:

- **About 93 instead of 100,** after three years (FY24–26). That is a saving of roughly 2% a year in the labour each piece of work needs. The plausible range is 90 to 96. The data cannot rule out no saving at all.
- **Not yet tested.** The firms kept about nine-tenths of the saving instead of cutting prices, so clients had little reason to buy more. Meanwhile the amount of work fell sharply for reasons unrelated to price, and this fall was larger than AI's direct effect. AI price cuts begin in earnest in FY27, so the real test starts now.

All of our data predate the jump in coding-agent ability around mid-2026. What follows describes the earlier generation of tools.

## 1. The framework

Employment at these firms is the volume of work they sell times the labour each unit of work needs. AI acts on the second term directly; how much it has cut it is the replacement rate, our first question.

AI can also act on volume. A firm whose costs fall can keep the saving as margin or pass it on as a lower price. If it passes it on and demand is elastic enough, volume rises and can offset the labour saved, as bank branches multiplied after ATMs cut tellers per branch.[^atm] Whether that offset is happening is our second question. Everything else that moves volume, such as client budgets, in-sourcing, or share lost to other firms, is a demand shift, which we measure separately.

In growth rates:[^model]

$$
g_L \;=\; \underbrace{d}_{\text{demand shift}} \;-\; \underbrace{s}_{\text{replacement}} \;+\; \underbrace{\varepsilon\,\varphi\, s}_{\text{volume response}} \;=\; d - s\,(1-\varepsilon\varphi)
$$

where *s* is the replacement rate, *φ* the share of the saving passed on in price, and *ε* the price elasticity of demand. AI raises employment only if *εφ* > 1: firms must pass on most of the saving, and demand must be elastic.

### What happened

The six firms are TCS, Infosys, HCLTech, Wipro, Tech Mahindra and LTIMindtree. Years are Indian fiscal years, ending in March.

Their headcount grew about 7% a year from FY16 to FY20. It then jumped by 18% in FY22 and 14% in FY23, as the firms hired heavily after COVID. It fell 4% in FY24 and has been roughly flat since. Revenue in constant currency slowed from about 9% a year before COVID to under 2% a year in FY24–26.

The level of each series tells a fuller story than its growth rate (Figure 1). During the boom the firms hired far ahead of their revenue: by FY23 headcount was 14% above its pre-COVID trend, while revenue was only 3.5% above. Since then both have fallen well below that trend. By FY26 headcount was 11% below it and revenue 18% below. Accenture, for comparison, boomed just as much and is now back on its trend.

::: figure levels
**Figure 1.** Headcount and constant-currency revenue at the top six (simple average of growth rates, cumulated) and at Accenture, compared with each series' FY16–20 trend. Values are log points relative to FY20 (×100), so a gap of 10 means about 10% below trend.
:::

Two features of this picture matter for what follows. First, part of the fall in hiring is the firms working off the extra staff they took on in FY22–23. That is neither AI nor weak demand, so we strip it out by measuring productivity net of how busy staff are.[^util] Second, revenue fell short of its old path by much more than headcount did. That revenue shortfall is the core of Question 2.

### Why the top six

We focus on the six largest firms because they are the only ones with long, consistent company data. The sector as a whole tells a similar story. In India's official labour-force survey (PLFS), employment in IT has been flat at about 5.7 million since 2022-23, and the number of young graduates working in IT has been flat at about 2.6–3.0 million (Figure 2).[^plfs]

::: figure sector
**Figure 2.** Employment in IT services (industry codes 62 and 63) in India's Periodic Labour Force Survey, with 90% confidence intervals. Left: all workers. Right: graduates aged 21–30. The survey changed design in 2025, and the 2023-24 and calendar-2024 rounds share half their sample. One very heavily weighted village or block inflates both, by about 5% on the left and about 10% on the right. Source: PLFS unit-level data (MoSPI), our tabulation.
:::

The work did not leave India. Excluding Ireland, India's share of world computer-services exports was flat from 2022 to 2025 (Figure 17 below).

## 2. Question 1: How many workers does a piece of work need now?

::: answer
About 2% fewer a year in FY24–26, so about **93 workers per 100** after three years (plausibly 90–96). Firms kept about nine-tenths of the saving. Sampling noise is large enough that we cannot rule out no saving at all.
:::

### Where a saving has to show up

Nobody publishes how many people each piece of work needs. But a labour saving cannot simply vanish. If a firm needs 7% fewer people for the same work, one of two things happens:

- **It keeps the saving.** It charges the same price with fewer people, so its revenue per employee rises.
- **It passes the saving on.** It cuts its price, so revenue per employee stays put but clients pay less.

So the replacement rate is the sum of two things we can measure: the saving kept, seen in revenue per employee, and the saving passed on, seen in prices. We measure each in turn and add them up.[^sum]

### The saving kept: revenue per employee

**The data.** For each of the six firms we have quarterly revenue in constant currency and headcount from FY16 to FY26. For four of them we also have utilisation: the share of staff time billed to clients.

**The test.** For each firm, we take growth in revenue per employee and subtract the change in utilisation. What is left is growth in revenue per *busy* employee.[^residual] We then ask whether this grew faster in FY24–26 than in the same firm's own past (FY16–20), and average the answer across the six. TCS and HCLTech do not report utilisation, so for them we allow its change to lie anywhere in the range seen at the other four.[^tcshcl]

**The result.** On this test, revenue per busy employee grew about 1 percentage point a year faster after 2023 than before.

**A correction.** This understates the saving, for a reason particular to these years. When a firm uses subcontractors, it books their work as revenue but does not count them as employees. In FY24 all six firms cut back on subcontractors and brought that work in-house (Figure 3). Their spending on subcontractors fell by 1.2 to 3.9 percentage points of revenue. That moved work onto the payroll without adding revenue, which pulls down revenue per employee even if no one became less productive.

::: figure subcon
**Figure 3.** Spending on subcontractors as a share of revenue, FY20–FY26, as each firm reports it. It fell at all six firms in FY24. For TCS the series is fees paid to outside consultants.
:::

We correct for this by asking how many employees the subcontracted work would have needed.[^subcon] With the correction, the saving kept is about **2.1 points a year** (1.5 to 3.0 across the assumptions we cannot pin down).

The correction is the largest single assumption in this section. It treats the fall in subcontracting spending as fewer subcontractors, not cheaper ones. If more than about 60% of the fall came from lower contractor rates, AI's share of the slowdown drops below a fifth.[^subcon_break]

The estimate also depends on which years count as "before". Figure 4 shows it for four choices. Including the COVID year FY21 in the baseline lowers it; leaving out the boom years raises it. The corrected estimate is positive in every case.

::: figure kept
**Figure 4.** The saving kept: how much faster revenue per busy employee grew in FY24–26 than in each firm's own baseline, averaged over the top six. Each row uses a different baseline. Grey: before the subcontracting correction. Blue: after. Thick bars show the range across the assumptions we cannot pin down (how TCS and HCLTech's utilisation changed, and how much a subcontractor costs relative to an employee). Thin bars add sampling noise (95% intervals). Equal weight on each firm.
:::

### The saving passed on: what firms said about prices

There is no price index for IT services in India, and the US statistics office does not cover the industry.[^noindex] So we read what the firms told investors.

**The data.** We searched every earnings-call transcript from January 2023 to October 2026 for the eight firms in our panel, plus investor days, four BPO firms, filings and a few older contracts for the pre-AI baseline, and collected 108 statements about pricing. We checked each quote against the original document.[^m2data]

**The test.** Before AI, these firms already gave clients routine annual "productivity" discounts on long contracts, typically 10–15% over a contract's life. TCS says this is not related to AI. We count only the cut *on top of* that routine discount, and only on the same scope of work. We then turn statements such as a 10–15% cut over a contract's life, or 3–5% a year in the services AI affects, into a percentage of each firm's total revenue per year.[^m2convert]

**The result.** Almost nothing was passed on in FY24–26 (Figure 5). The AI price cut was about 0 in FY24, 0.1% in FY25 and 0.4% in FY26. It rises to about 1.5% in FY27 (0.4 to 2.7), though much of that is still what firms expect rather than what they have booked.

The firms say this themselves. HCLTech's chief executive said in April 2026 that "very little has really played out in already reported numbers," and expected it from FY27. In October 2026 TCS's finance chief said that "at an overall portfolio level, the pricing is broadly stable."

::: figure prices
**Figure 5.** Price cuts given to clients, % of revenue per year, top six (weighted by revenue). Grey: the routine pre-AI productivity discount, which we assume at about 1.5% a year. Blue: the extra cut attributed to AI, with its range. FY27 is mostly what firms expect, so it is drawn lighter.
:::

For the AI price cut to have averaged even 1% a year over FY24–26, firms would have had to understate it about five-fold. Some pass-through is hidden from this method, though: on time-and-materials contracts, which are 43–48% of revenue at the firms that report it, savings reach clients as fewer billed hours, which managers never describe as a price cut. So this is probably an underestimate, by an amount we cannot size.

### Adding up

The replacement rate is the sum: 2.1 kept plus 0.2 passed on, so about **2.3 percentage points a year**. Across the assumptions we cannot pin down it ranges from 1.5 to 3.6. With sampling noise the range is −0.8 to 7.1 (Figure 6).

In the terms of our question: over FY24–26, a piece of work that took 100 people came to take about 93 (90 to 96).

::: figure sbar
**Figure 6.** The replacement rate and its two parts, percentage points a year, FY24–26 against FY16–20. Dots are central estimates. Thick bars span the assumptions we cannot pin down; thin bars add sampling noise. The axis at the top converts the total into workers needed per 100 after three years.
:::

Three points about this number:

- **Firms kept most of it.** About nine-tenths of the saving was kept and one-tenth passed on. This reverses a claim in our earlier note that there was "no sign firms kept AI savings." That claim rested on four firms and no subcontracting correction.
- **It is an average over everything the firms do.** Testing and routine maintenance probably saw much larger savings, and client-facing consulting smaller ones.
- **It is small next to the slowdown.** Headcount growth fell by about 8 points a year against its pre-COVID pace. AI's direct effect explains about 2 of those 8.

### The strongest objection

Everything above compares *growth rates*: did revenue per employee grow faster after 2023 than before? A different comparison gives a different answer. In *levels*, revenue per employee at the top six is still about 11% below where its FY16–20 trend would have put it, the same gap as in FY23 (Figure 7). On that view the firms are only recovering lost ground, and there is no room for an AI saving at all.[^level]

::: figure rpelevel
**Figure 7.** Revenue per employee (constant currency), top six and Accenture, relative to each series' FY16–20 trend (log points ×100). The top six fell well below trend during the boom and have not recovered the gap. Accenture has recovered to above its trend.
:::

The two views make different assumptions. The growth view treats the FY21–23 dip as a one-off that firms will not make up. The level view expects them to climb back to their old path. We cannot yet tell which is right, and more years of data will help. For now we report the growth-rate estimate and flag that the level view argues for a smaller number.

::: details Juniors: were they replaced faster?

**Short answer: probably, but the evidence is weak.** Junior employment grew about 0 to 2 points a year more slowly than experienced employment, relative to the past, depending on the data. If so, the replacement rate for juniors was about 2.3–3.3% a year, against 1.3–2.3% for experienced staff.[^jsplit]

**How firms changed: hiring, not firing.** Firms did not push juniors out faster. They hired more experienced people instead. At Infosys, whose hiring and exit data by age reconcile exactly with its headcount and go back furthest, under-30 hiring in FY24–26 was about the same as in FY16–21 (42,000 against 43,000 a year), while hiring of people aged 30 and over rose 65% (Figure 8). The share of under-30s among new hires fell from 79% to 68%.

::: figure infosyshires
**Figure 8.** Infosys hires by age, FY16–FY26. The FY22–23 spike is the post-COVID boom; FY24–26 is shaded. Source: Infosys ESG reports, via our firm panel.
:::

**Headcount.** The share of under-30s in headcount fell from FY23 at most of the large firms (Figure 9). But much of that is the boom unwinding: firms hired huge numbers of freshers in FY22–23, so the share had to fall back. Once we allow for that, the firm data show a junior gap of about 0 to 1 point a year (range −2 to +3).[^jfirm] In the labour-force survey, which covers the whole sector, the gap is about 1.4 to 1.9 points a year, but its 90% confidence interval includes zero.[^jplfs]

::: figure under30
**Figure 9.** Share of headcount under 30, by firm, FY16–FY26, from the firms' voluntary sustainability reports. TCS is India only and read off charts. LTIMindtree before FY23 is Mindtree. Firms differ in scope, so compare trends within a firm.
:::

**Pay.** In IT, pay for 21–25-year-olds relative to 31–40-year-olds fell from 0.64 in 2020-21 to 0.52 in 2025. Among all graduates the same ratio stayed between 0.53 and 0.58 (Figure 10). Falling relative pay alongside flat junior numbers, while the supply of graduates grows, points to weaker demand for juniors. But 2020-21 was an unusually high year. Measured from 2017-18, the relative decline is about 1.6 points a year rather than 5, so this is suggestive, not firm.[^jpay]

::: figure juniorpay
**Figure 10.** Pay of 21–25-year-olds relative to 31–40-year-olds (mean monthly earnings of regular wage workers), in IT and among all graduates, with ±1 standard error. Source: PLFS unit-level data (MoSPI), our tabulation. The 2025 survey has a new design.
:::

**Across the sector.** Graduate placements at top engineering colleges fell for the class of 2023-24, the first fall in data going back to 2016-17.[^nirf] The number of young graduates working in IT stayed flat while the number employed elsewhere grew, so IT's share of them fell from 12.8% to 9.9% between 2022-23 and 2025 (part of that growth elsewhere may reflect the 2025 survey redesign). GCCs (global firms' own offices in India) hire few freshers: on one job portal in July 2026, their rising fresher postings offset only about a fifth of the fall at IT firms.

**A warning for the forecast.** The freshers hired in the boom turn 30 around FY30–31. That will push down under-30 shares mechanically, and it will not be AI.
:::

::: details Vintage: which AI are we measuring?

Our outcome data run to March 2026 for the firms and to December 2025 for the labour-force survey. Coding agents improved sharply around mid-2026, and the 2025 trial by METR that found AI slowed experienced developers has since been updated to find speed-ups. So our estimates describe the tools of 2023 to early 2026. They are a floor for what comes next, not a forecast of it.
:::

## 3. Question 2: When AI makes the work cheaper, do clients buy more?

::: answer
**We can't tell yet, because the work hasn't got cheaper.** AI-driven price cuts were only about 0.2% a year, on top of the routine discounts firms always gave. What we can say is that the amount of work fell sharply for other reasons, and by more than AI's direct effect. About half of that fall is shared with Accenture and Cognizant. We can explain only a small part of it.
:::

### The test hasn't happened

Clients can only respond to a price cut they receive. With AI price cuts of about 0.2% a year in FY24–26, even very price-sensitive clients would have bought only a fraction of a percent more. So FY24–26 tells us almost nothing about how clients respond to cheaper work.

This is a finding in itself. Through FY26 the route by which AI could add jobs was switched off, because the firms kept the saving. It switches on in FY27, as contract renewals start to carry AI price cuts.

### But the amount of work did fall

Since prices barely moved, the fall in the amount of work is almost entirely a shift in demand: something other than AI-driven prices made clients buy less from these firms.

How large a fall depends on what "normal" growth would have been, and there is no single right answer. We use three yardsticks (Figure 11):

- **Pre-COVID growth rates.** Revenue would have kept growing at its FY16–20 pace of about 9% a year. Against this, revenue growth fell about 7 points a year.
- **The pre-COVID path.** Revenue would have returned to the level its FY16–20 trend implied by FY26. Against this, it fell about 6 points a year.
- **Peers.** The top six would have slowed only as much as Accenture and Cognizant did. Against this, they fell about 3 points a year further.

::: figure yardsticks
**Figure 11.** How much growth fell in FY24–26, in percentage points a year, under three views of what "normal" would have been. Headcount and constant-currency revenue, top six. The peers yardstick subtracts the slowdown at Accenture and Cognizant.
:::

The peer comparison is the most informative. About half of the top six's revenue slowdown (57%) was shared with Accenture and Cognizant, so much of what hit Indian firms hit global IT services generally. About 3 points a year is specific to the Indian firms.[^peers]

### What moved demand

We took each plausible cause and measured it with data that do not come from the firms' own revenue.[^circular] Figure 12 puts them side by side.

::: figure demand
**Figure 12.** What we can measure of the demand shift, percentage points a year. The three points at the top are the fall in constant-currency revenue growth under each yardstick, which is the total to be explained. Below are the measured causes (comparing 2023–25 with 2016–22) with their plausible ranges, and their sum. The gap between the sum and the totals is what we cannot explain.
:::

**Clients' overall spending: little change.** The clients are mostly in the US (about 54% of exports) and Europe (about 32%). In the US, the drivers of IT spending held up after 2023: GDP grew faster, big banks' technology spending grew about as fast as in 2016–22, and firms' spending on software built by their own staff kept growing (Figure 13). Europe slowed somewhat, with GDP growth down about 0.7 points. Overall: about −0.5 points a year (range −1.5 to +0.5).[^market]

::: figure clients
**Figure 13.** Growth in US drivers of client IT spending, 2016–22 and 2023–25 (% a year). None slowed sharply. Bank technology spending is the sum of reported technology and communications expense at JPMorgan, Bank of America and Citi.
:::

**Clients doing the work themselves: some.** In the US, the share of computer jobs held by clients' own staff, rather than by IT service firms, was stable at 64–65% from 2015 to 2022, then rose to 67.5% by 2025 (Figure 14). Employment at US IT service firms fell in the official payroll data too. In continental Europe there is no such shift. In the UK, investment data suggest a large one; we include it, but have not checked those data for method changes, and without it the figure would be about −1.0. Overall: about −1.6 points a year (range −3.7 to +0.1).[^inhouse]

::: figure inhouse
**Figure 14.** Left: share of US computer jobs held by clients' own staff rather than by IT service firms (BLS occupational survey). Right: employment at US computer-systems-design firms (NAICS 5415), two official sources, index 2022 = 100.
:::

**Clients' own offices in India (GCCs): no extra effect.** Global firms' captive centres in India kept growing fast. But they were already growing fast before 2023. Their estimated hiring absorbed about 2.4% of the vendors' workforce a year after 2023, against about 2.8% before. Official export data point the same way: foreign-owned firms in India, of which GCCs are a large part, outpaced India's total exports by a similar margin before and after (Figure 15). What matters for the slowdown is a change in that pace, and we find none: about +0.5 points a year (range −2.2 to +1.6).[^gcc]

::: figure gcc
**Figure 15.** Export growth of foreign-owned firms' Indian subsidiaries (information and communication services), compared with India's total software exports, by fiscal year. The gap is similar before and after 2023. Source: RBI census of foreign liabilities and assets and RBI software exports survey. The subsidiary series also includes foreign-owned vendors such as Accenture and Cognizant.
:::

**Smaller Indian firms: not measured, but bounded.** Four mid-tier firms (Persistent, Coforge, Mphasis and Hexaware) grew fast, but they are a selected set of winners. Across 21 listed firms below the top six, the twelve IT and engineering firms outside those four added only about 2% to their headcount organically over three years (Figure 16). Even if every dollar of the 21 firms' revenue growth had been taken from the top six, it would account for at most about 1.5 points a year. We leave this out of the measured total below.[^midtier]

::: figure listed
**Figure 16.** Change in headcount, FY23 to FY26, at the top six and at 21 smaller listed Indian firms, by group. The lighter part of each bar is staff added through acquisitions (a lower bound). Headcounts are global.
:::

**Work leaving India: no.** India's share of world computer-services exports was flat from 2022 to 2025, as was its share of US imports (Figure 17). US IT-services employment fell too, so the work did not move back to the US either.

::: figure share
**Figure 17.** India's share of world computer-services exports (excluding Ireland, whose exports are mostly multinationals' booking) and of US computer-services imports, 2015–2025. Sources: IMF balance of payments; BEA.
:::

**What is left.** Adding up client spending, in-housing and GCCs gives about −1.6 points a year. Against the pre-COVID growth yardstick, that leaves about 5 points a year unexplained. Against peers, the Indian-specific 3 points are largely unexplained.[^unexplained] The candidates we have not been able to measure:

- **The firms' mix of work.** If the top six do more routine maintenance than Accenture, they may be more exposed to clients cutting that work first.
- **Clients using AI themselves.** A client whose own staff now use AI tools may need less outside help. This would not show up in any of the data above.
- **The hangover from the boom.** Clients may have pulled projects forward into FY22–23, leaving less to do now.

**One point to note:** some of the demand shift may itself be AI, arriving by another route. If clients are doing more in-house with their own AI tools, that is AI cutting demand for these firms, not AI making their work cheaper. We cannot yet separate the two. It matters for the future: if so, demand will keep shifting as the tools improve.

### How responsive are clients to price?

We tried to measure this directly by comparing service lines that should be more or less exposed to AI, such as application maintenance against consulting.[^m6] It did not work: the AI price differences between lines are tiny (0.1 to 0.5 points a year), while each line's demand moves by several points a year for its own reasons. Our estimate's standard error was about 5, so the data are consistent with almost anything.

So we take a range from history. When technology made textiles, steel and cars cheaper in their early decades, demand responded strongly, with elasticities above 1; once those industries matured, it responded weakly. The two estimates closest to IT services are of a similar size: about 1.6 for business purchases of computers, and about 1.1 for one country's imports of computer services.[^eps] We use 0.5 to 1.5 for IT services (centre 0.9), and 0.2 to 0.9 for BPO.

**What that implies.** For AI to add jobs, the share of the saving passed on times clients' responsiveness must exceed 1 (Section 1). Even if firms passed on the whole saving, that would need an elasticity above 1: just above the centre of the plausible range for IT, and outside the range for BPO. With firms passing on about a tenth of the saving, AI removes jobs almost one-for-one with the labour it saves (Figure 18).

::: figure jevons
**Figure 18.** AI's net effect on job growth, percentage points a year, for a replacement rate of 2.3 points a year, as a function of the share of the saving passed on to clients. Each line is a different price elasticity. Above zero, AI adds jobs. The marker shows FY24–26.
:::

## 4. What the two answers say about FY24–26

::: answer
AI took roughly 2 points a year off job growth directly. Cheaper work made almost no difference. On most yardsticks, demand shifting away from these firms did more.
:::

Under the growth-rate yardstick, the pieces add up (Figure 19). Headcount growth fell by about 8.3 points a year. AI replacement explains about 2.3. Clients' response to the small price cuts adds back about 0.2. Bringing subcontracted work in-house added back about 1.1 to headcount. The demand shift accounts for the remaining 7 points, of which we can measure only about 1.6.[^routes]

::: figure decomp
**Figure 19.** The fall in top-six headcount growth, FY24–26 against FY16–20, split into its parts (percentage points a year). Bars below zero lowered job growth; bars above raised it.
:::

The other yardsticks do not split so neatly (Table 1). Against the pre-COVID path, headcount fell only 3 points below normal while revenue fell 6. Taken at face value, that leaves no room for an AI saving (the objection in Section 2). Against peers, any saving that all IT firms share cancels out, so the comparison only tells us whether Indian firms were hit harder.

::: table
**Table 1.** The slowdown in FY24–26 under three yardsticks, percentage points a year
| Yardstick | Headcount | Revenue | AI replacement | Price response | Demand shift (measured part) |
|---|---|---|---|---|---|
| Pre-COVID growth rates | −8.3 | −7.1 | −2.3 | +0.2 | −7 (−1.6) |
| Pre-COVID path | −3.0 | −5.7 | −2.3 or less | +0.2 | −5.5 (−1.6) |
| Peers (Accenture, Cognizant) | −1.5 | −3.1 | 0 if shared | ≈0 | −3 (≈0) |
---
The demand shift is the fall in revenue less the small price effect. Under the path yardstick, headcount fell less than revenue and AI replacement together imply; this is the level objection of Section 2. Under the peers yardstick, the measured US in-sourcing affects all vendors and so cancels out.
:::

Two conclusions survive every yardstick. The AI replacement rate, about 2 points a year, is smaller than the fall in demand. And the price response was negligible. We report the replacement rate in points a year rather than as a share of the slowdown, because that share swings from about a quarter to more than all of it depending on the yardstick.

## 5. Looking ahead to 2030

*This section is a placeholder. It will turn the two answers into conditional scenarios, not forecasts.*

The scenarios will vary four things:

- **The replacement rate,** starting at about 2% a year and rising after the mid-2026 jump in coding agents. Capability evidence will set how fast it rises: how long a task AI agents can complete (METR), the updated METR developer trial, coding benchmarks, and the cost of AI relative to Indian wages.
- **The share passed on,** rising from about a tenth toward what firms' FY27 statements imply.
- **Clients' responsiveness to price,** across the historical range, since our data cannot pin it down.
- **The demand shift,** including the possibility that clients' own use of AI keeps pulling work in-house.

Juniors will be modelled separately, with the FY30–31 ageing of the boom cohort netted out. For each scenario we will report total and junior employment in 2030, and the early signs that would tell us we are on that path.

## 6. What would sharpen each answer

**Question 1 (the replacement rate):**

- **FY27 results.** The first year after the jump in coding agents, and the first with real price cuts, so both halves of the saving should become visible.
- **Billed effort.** Person-months billed to clients would show workers per unit of work directly. Infosys published this until FY20.
- **Utilisation for TCS and HCLTech.** Together they are half of the top six's revenue.
- **More years,** to settle whether growth rates or levels are the right comparison.

**Question 2 (the demand response):**

- **A price index for IT services.** None exists in India, and the US statistics office does not cover the industry.
- **Price cuts by service line.** If firms reported renewal discounts separately for, say, application maintenance and consulting, gaps of a few points would identify clients' responsiveness.
- **GCC employment.** The RBI collects employee counts in its software exports survey but does not publish them. Its next census of foreign-owned firms is due in late October 2026.
- **A UK series on in-house IT work,** to check the one large, unverified piece of the demand shift.

## Appendix

### How the four scenarios of our earlier note map onto this

Our first note asked which of four scenarios explained the slowdown. In this framework they become values of the parameters:

- **Demand fell** (S1) is a fall in the market part of the demand shift.
- **Savings kept** (S2) and **savings passed on** (S3) are the two halves of the replacement rate. We now estimate both: mostly kept.
- **Work moved elsewhere** (S4) is the share part of the demand shift: in-sourcing, GCCs and smaller firms. Of these, only US in-sourcing is clearly visible.

### Methods in brief

All growth rates are log changes ×100. "FY24–26 against FY16–20" means the average annual growth in FY24–26 minus the average in FY16–20, computed firm by firm and then averaged with equal weight on the six firms, unless stated. Ranges are of two kinds: *bounds* span assumptions we cannot pin down (for example, how much a subcontractor costs relative to an employee); *sampling* intervals add year-to-year noise. Every number has a measurement folder in the repository with a FINDINGS.md file that lists data, code, sources and the point at which each conclusion would break:

- the saving kept: `data/explore/round4/residual/` and `round4/robustness/m1_scope_subcon/`;
- the saving passed on: `round4/price_statements/`;
- juniors: `round4/junior_gap/`;
- the demand shift: `round4/demand_shift/` and `round4/robustness/demand/`;
- responsiveness to price: `round4/elasticity_xsec/`;
- yardsticks: `round4/robustness/baseline/`;
- sector, GCCs, smaller firms and trade: `data/explore/round3/`.

### Sources

Company filings, investor presentations and earnings-call transcripts for the eight firms; Reserve Bank of India software exports survey and census of foreign liabilities and assets; IMF balance of payments; US Bureau of Economic Analysis; US Bureau of Labor Statistics (occupational employment, payroll employment, producer prices); Eurostat; UK Office for National Statistics; Nasscom and Zinnov (industry estimates, used with care); NIRF institutional data; job-portal reports (foundit, Naukri).

This page uses unit-level data from the Periodic Labour Force Survey, Ministry of Statistics and Programme Implementation (MoSPI), Government of India. Only aggregate tabulations are shown. The analysis and conclusions are ours, not MoSPI's.

[^atm]: James Bessen, "Toil and Technology," *Finance & Development*, March 2015. In urban areas, tellers per branch fell from about 20 to 13 between 1988 and 2004, while the number of branches rose by 43%, so teller employment held up.
[^model]: In growth rates, employment = volume − replacement rate − other productivity growth; volume = demand shift − elasticity × price change; price change = −(share passed on) × replacement rate + other price drift. Holding the "other" terms at their pre-2023 values and substituting gives the equation shown.
[^util]: Utilisation is the share of staff time billed to clients. A firm that over-hired has staff on the bench; as it puts them to work, revenue rises with no new hiring. Our measure of productivity removes changes in utilisation, so working off the bench does not count as an AI saving.
[^plfs]: Usual-status workers in National Industrial Classification divisions 62 (computer programming and consultancy) and 63 (information services). GCC staff may be classified here or under their parent firm's industry; they cannot be identified separately. Our tabulation matches MoSPI's published labour-force figures exactly in seven of nine rounds.
[^sum]: Strictly, the change in revenue per busy employee measures (1 − share passed on) × replacement rate, and the AI price cut measures (share passed on) × replacement rate. Their sum is the replacement rate. This assumes that price drift and productivity growth unrelated to AI continued at their pre-2023 pace. We checked US and UK service price indices and wage data and found no sign that non-AI price growth fell after 2023 (bound: −1.0 to +0.5 points a year).
[^residual]: Revenue per employee rises when staff bill more of their time, when each unit of work sells for more, or when each unit takes less labour. Subtracting the change in utilisation removes the first. What remains is price per unit divided by labour per unit. For Infosys, whose headcount includes trainees but whose utilisation excludes them, we use the utilisation series that includes trainees.
[^tcshcl]: The four firms with utilisation data saw changes between about −2 and +1.5 points a year depending on the window. Allowing TCS and HCLTech anywhere in that range moves the six-firm average by up to about half a point either way.
[^subcon]: Each point of revenue paid to subcontractors corresponds to about 1.0–1.9 points of revenue's worth of own-employee work, because firms pay their own staff about 53–60% of revenue and a subcontractor costs between one and two times an employee (Wipro said "about 30% higher"). We use 1.4. Subcontracting rose again at five of six firms in FY26, and the correction includes that reversal.
[^subcon_break]: This is for the FY16–20 baseline. With the FY16–23 baseline, over 90% of the fall would need to be lower rates.
[^noindex]: The US Bureau of Labor Statistics lists computer systems design among its "areas of noncoverage" for producer prices. The UK index for computer programming appears to price charge-out rates, and the nearest US indices cover data processing and software publishers, so none measures price per unit of outsourced IT work.
[^m2data]: Eight firms: the top six, Accenture and Cognizant. Investor days for TCS, Infosys and LTIMindtree in 2025–26. BPO firms: Sagility, Firstsource, eClerx and HGS. 107 of 108 quotes were confirmed word for word against the source; the other is a text-extraction problem and is used only as context. Only about 16 IT statements give a usable number, and TCS, HCLTech and LTIMindtree supply most of them. Infosys, Wipro and Tech Mahindra (43% of top-six revenue) give no usable rate, so we allow their AI cut to lie anywhere between zero and twice the revenue-weighted average of the other three. Yearly figures in Figure 5 weight firms by revenue; the 0.2 used in the replacement rate weights them equally, as in Figure 4. Both round to 0.2.
[^m2convert]: A one-off discount on renewals reaches total revenue gradually: about 20–35% of revenue is renewed each year, and about 40–60% of revenue is in services exposed to AI. A cut spread over a contract reaches revenue as contracts roll onto AI-era terms. The pre-AI routine discount (2–5% a year on the 40–55% of revenue under multi-year contracts) is our assumption, because contract percentages are redacted in the filings we found.
[^level]: Indicative only: the firms with data differ across years.
[^jsplit]: Under-30s were about 45–52% of top-six staff over FY23–26, so we take half. With a junior–experienced gap g, the junior rate is then the average rate (2.3) plus about 0.5g, and the experienced rate the average minus about 0.5g. These ranges hold the average fixed; its own uncertainty (1.5 to 3.6) widens them.
[^jfirm]: The FY22–23 hiring boom raised the under-30 share above its long-run downward trend. We net out the boom three ways: by assuming the bump decays as staff leave or age; by conditioning on revenue growth; and by comparing firms with bigger and smaller booms. The estimates range from about −2 to +3 points a year, centred near 0 to +1. The boom need only explain about a quarter of the post-2023 decline for the gap to vanish.
[^jplfs]: Workers aged 21–25 against 31–40: +1.4 (90% interval −2.2 to +5.0). Aged 21–30 against 31–60: +1.9 (−0.7 to +4.4). Average of 2023-24 and 2025 against the average of 2017-18 to 2020-21.
[^jpay]: The difference between the IT and all-graduate log ratios fell by 5.4 points a year from 2020-21 to 2025 (standard error 1.85), but by about 1.6 points a year on a precision-weighted trend fitted to all rounds from 2017-18 (calendar 2024 left out, as it shares half its sample with 2023-24; including it gives 1.5). That trend is not statistically different from zero. Medians fall somewhat more steeply, by about 2.6 points a year.
[^nirf]: National Institutional Ranking Framework data for the same institutions in the same edition: undergraduate engineering graduates placed fell about 1.8% while graduates rose about 3.4%; the placement rate fell from 73.8% to 70.1%. These are placements with all employers, including GCCs.
[^peers]: Accenture and Cognizant have the bulk of their delivery staff in India too. Their revenue growth fell by about 4 points a year against their own FY16–20 pace, against about 7 for the top six.
[^circular]: Client spending on outside IT services is the same money as these firms' revenue, so it cannot be used to explain their revenue. We use measures of clients' own activity and of in-house work instead.
[^market]: US: real GDP, bank technology expense lines (JPMorgan's line is partial), and BEA own-account software investment. Europe: EU and UK real GDP, EU investment in intellectual property, and EU employment of ICT specialists. We weight North America and Europe by their shares of India's exports (55% and 32%) and assume the remaining 13% behaves like the average. Against a 2016–19 baseline, bank technology spending slowed by about 1 point.
[^inhouse]: Bureau of Labor Statistics Occupational Employment and Wage Statistics: computer occupations in client industries against those in computer systems design (NAICS 5415). The payroll survey (CES) confirms the fall in NAICS 5415 employment: growth fell from 3.6% a year in 2016–22 to −0.6% in 2023–25. The range allows for vendors adopting AI faster than in-house teams, which would exaggerate the shift. In Europe we use Eurostat counts of ICT specialists by industry.
[^gcc]: No official statistic counts GCC staff. Pre-2023 levels come from Nasscom and Zinnov, whose report editions are not comparable; the post-2023 central estimate (about 260,000 tech jobs added from FY23 to FY26) comes from staffing firms' hiring estimates, which we could not confirm. The RBI census series covers all foreign-owned firms in information and communication, including vendors such as Accenture and Cognizant, and its "before" period is only FY22–23. For captive centres, export values track the wage bill.
[^midtier]: The 21 firms' combined US-dollar revenue rose by about $3.6 billion from FY23 to FY26 (16 firms with dollar figures), against top-six revenue of about $81 billion in FY23. That is about 4.5% over three years, or 1.5 points a year, and it includes acquisitions and the firms' own normal growth.
[^unexplained]: The measured causes come from data on clients, so most of them (US in-sourcing especially) affect Accenture and Cognizant as much as the Indian firms. They therefore explain little of the gap with peers.
[^m6]: Pairs of business lines within Accenture, Cognizant, HCLTech and Tech Mahindra, and India's exports of IT services against BPO and engineering services. Exposure to AI comes from occupation-level scores (Eloundou et al.; Felten et al.). Different scores even disagree on whether BPO or IT is more exposed.
[^eps]: Bessen (2019), *Economic Policy*: price elasticities of 1.3–2.4 for textiles, steel and cars in their early decades, falling to 0.2–0.4 or below by 1950. Tevlin and Whelan (2000): 1.6 for US business investment in computers (an elasticity with respect to their user cost). Nakano and Nishimura (2024): 1.07 for Japan's imports of computer services, which measures substitution between imported and domestic services and so is an upper reference for the market as a whole. No published estimate exists for outsourced IT services. All elasticities here are stated as positive numbers.
[^routes]: The volume change can be computed two ways: from headcount plus the replacement rate, or from revenue less the price change. Under this yardstick they agree (about −7) once the in-sourcing of subcontracted work is counted.
