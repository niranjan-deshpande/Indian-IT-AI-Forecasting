---
title: A Health Check of India's IT Services in 2026
byline: Niranjan Deshpande · October 2026
thanks: Written as part of SPAR (Fall 2026), supervised by Andrei Potlogea. Data and code: {{repo}}.
---

<!--
HOW THIS FILE WORKS
`python3 scripts/final/build_health_check.py` turns this file into docs/health-check.html.
Conventions are those of checkpoint_text.md:
  - [^key] marks a footnote; define it on its own line at the end as "[^key]: text".
  - "::: figure NAME" ... ":::" holds a caption; the chart is built in the builder from CSVs in data/explore/health_check/charts/.
  - "::: table" ... ":::" is a hand-written table: caption line, pipe rows, "---", note line.
  - "::: details Title" ... ":::" is a collapsible block.
Every number in the prose is checked by scripts/final/health_check_number_check.py.
-->

## Summary

India's IT services sector is still growing, but it no longer adds jobs at its old pace, and it takes a smaller share of each year's young graduates.

1. **Output is growing.** Exports of software and IT-enabled services reached $221 billion in FY26, 19% more than in FY23. India's share of world computer-services exports has held at about 30%.
2. **The largest firms are not.** The six biggest firms grew revenue by between 0.6% and 3.2% a year in constant currency over FY24–26, against about 9% before COVID. Growth has moved to the captive centres of foreign firms (GCCs), mid-sized firms and business-process firms.
3. **Employment has lagged output.** The six firms employ 3.7% fewer people than in March 2023. Across the sector, employment is growing by at most about 2% a year.
4. **The entry level has narrowed.** Fresher hiring is far below its FY22 peak. Counts have recovered somewhat since FY24, but IT's share of young graduates, of young formal-sector entrants and of entry-level openings is lower than before the boom ended.
5. **The firms show little strain, and AI has barely reached prices.** Attrition, utilisation and margins are normal. AI-related price cuts were about 0.4% in FY26; firms expect about 1.5% in FY27.

Almost all of these data end in FY26 or calendar 2025, before the jump in coding-agent capability around mid-2026. They describe the sector as it entered that change.

::: table
**Table 1.** Summary indicators
| Indicator | Latest | Comparison | Source |
|---|---|---|---|
| Software and IT-enabled services exports | $221bn (FY26) | $186bn in FY23 | RBI |
| India's share of world computer-services exports, excluding Ireland | 30.1% (2025) | 29.3% in 2022 | IMF |
| Revenue growth, six largest firms, constant currency | 0.6% (FY26) | 8.7% a year in FY16–20 | Filings |
| Revenue growth in US dollars, four mid-tier firms | 14.9% (FY26) | 2.2% for the six largest | Filings |
| Headcount, six largest firms | 1.62m (Mar 2026) | 1.68m in Mar 2023 | Filings |
| Employment in IT (NIC 62–63) | 5.7m (2025) | 5.5m in 2022-23 | PLFS |
| Employment, industry estimate | 5.95m (FY26) | +2.3% on FY25 | Nasscom |
| Fresher hires, TCS, Infosys and HCLTech | 76,000 (FY26) | 218,000 in FY22 | Filings |
| IT share of salaried graduates aged 21–25 | 16% (2025) | 20% in 2022-23 | PLFS |
| IT share of net payroll additions aged 18–25 | 3.9% (FY25) | 5.8% in FY22 | EPFO |
| Real monthly pay, IT workers aged 21–25 | ₹30,900 (2025) | ₹35,200 in 2024 | PLFS |
| Attrition, six largest firms | 12–14% (Jun 2026) | 22–28% at the 2022 peak | Filings |
| Labour share of value added, six largest firms | 0.71 (FY26) | 0.69 in FY22 | Filings |
| AI-related price cuts | 0.4% (FY26) | about 1.5% expected in FY27 | Earnings calls |
---
Constant-currency growth removes exchange-rate effects. PLFS 2025 uses a redesigned survey; the change since 2022-23 is not statistically significant. Sources and definitions are in the appendix.
:::

## 1. Introduction

For three decades IT services have been one of the main routes into salaried work for India's graduates. The sector employs about six million people, and its exports are worth about 5½% of GDP.[^gdp] In 2026 its prospects became contested. Share prices of the largest firms fell sharply in February, as investors priced in AI coding tools, and headlines since have claimed both that AI is hollowing out Indian IT and that its exports are booming.[^selloff]

This piece collects the evidence on how the sector is doing now, drawing on filings of the six largest firms and 21 smaller listed firms, RBI and IMF trade data, the government's labour force survey (PLFS), provident-fund payroll records (EPFO), engineering-college placement data, job-postings indices, earnings-call transcripts and price data. Where other estimates circulate widely, we check them against the same sources (Section 8). We do not try to say how much of what we find is caused by AI.[^twoq]

We read "IT services" broadly, to include IT services firms, business-process management (BPM), engineering services and GCCs. Years are Indian fiscal years ending in March unless stated otherwise.

## 2. Output has kept growing

By the RBI's annual survey, India exported $221 billion of software and IT-enabled services in FY26. That is 8.2% more than in FY25 and 19% more than in FY23, or about 6% a year in dollars. In FY26 the growth came from IT services, which rose 12%, while BPO exports were flat.[^bop]

::: figure exports_orgtype
**Figure 1.** Software and IT-enabled services exports by type of exporter, FY12–FY26, US$ billion. Public-limited exporters include the large listed Indian firms; private-limited exporters include GCCs, foreign-owned vendors and unlisted Indian firms. The survey method changed around FY23.
:::

::: figure exports_activity
**Figure 2.** Exports by activity, FY24–FY26, US$ billion. IT services drove the growth in FY26; in FY25, IT services and BPO added similar amounts.
:::

India is not losing this work to other countries. Its share of world computer-services exports, excluding Ireland, was 29.3% in 2022 and 30.1% in 2025.[^ireland] In the first half of 2026 India's computer-services exports grew 11%, as fast as those of 24 other delivery countries combined. Poland, Romania and the Philippines grew too, but from far smaller bases.

::: figure india_world_share
**Figure 3.** India's share of world computer-services exports (excluding Ireland) and of exports from 30 emerging delivery countries, 2015–2025. The share fell before 2022 and has been flat since.
:::

## 3. Growth has moved away from the largest firms

The six largest firms are TCS, Infosys, HCLTech, Wipro, Tech Mahindra and LTIMindtree. They earned $86 billion in FY26, 7% more than in FY23, while total exports grew 19%. Their constant-currency growth fell from 8.7% a year in FY16–20 to 1.5%, 3.2% and 0.6% in FY24–26. Accenture and Cognizant, which compete for the same clients and also deliver mostly from India, grew about 5% in FY26.

::: figure revgrowth_peers
**Figure 4.** Annual revenue growth, FY16–FY26: the six largest firms (revenue-weighted, constant currency), four mid-tier firms, Accenture and Cognizant.
:::

All these firms over-hired after COVID. Accenture's revenue is back on its pre-COVID trend; that of the six firms is about 16% below it.

::: figure rev_trend_levels
**Figure 5.** Revenue and headcount relative to each firm group's FY16–20 trend, log points. Zero means on trend.
:::

The slowdown is uneven across the six. TCS revenue shrank in constant currency in each of the four quarters to March 2026. LTIMindtree and Tech Mahindra grew 6–7% in the latest quarter. Weakness is concentrated in particular firms rather than in particular client industries or regions.[^firmspecific]

::: figure firm_cc_quarterly
**Figure 6.** Year-on-year constant-currency revenue growth by firm, quarterly, 2022 to September 2026.
:::

The growth went elsewhere. Between FY23 and FY26 the four largest mid-tier firms (Persistent, Coforge, Mphasis and Hexaware) raised dollar revenue by 39%, and three listed BPM firms by 48%. GCCs added roughly 260,000 technology jobs, within a wide range.[^gcc] The rest of the listed IT mid-market did not take up the slack: of 12 other IT and engineering-services firms, five employed fewer people in FY26 than in FY23. In the RBI survey, private-limited exporters' share of exports rose from 35% in FY13 to 61% in FY26. This is a continuation of a long trend, not a break after 2023.[^gccpace]

::: figure segment_change
**Figure 7.** Change in headcount and US-dollar revenue, FY23 to FY26, by segment. GCC employment is a range of estimates of technology jobs added. Listed-firm headcounts are global.
:::

## 4. Employment has not kept pace

Headcount at the six firms peaked at 1.69 million in September 2022. It fell about 4% in FY24 and has been roughly flat since, at 1.62 million in March 2026. In the quarter to September 2026, the four firms that have reported added 9,400 people, mostly freshers.

::: figure top6_headcount
**Figure 8.** Combined headcount of the six largest firms, quarterly, 2015 to September 2026. The last point includes only four firms' new figures.
:::

With revenue still growing, revenue per employee has risen, from $48,600 at the end of 2022 to $53,900 in mid-2026.

::: figure rev_vs_hc
**Figure 9.** Revenue and headcount of the six largest firms, indexed to FY19 = 100.
:::

Across the whole sector, the evidence points to slow growth. Nasscom estimates 5.95 million employees in FY26, 2.3% more than a year earlier, while its revenue estimate rose 6.1%. The PLFS counts 5.7 million people working in IT (NIC 62–63) in 2025, 4% more than in 2022-23.[^plfs] The survey's margin of error, from −7% to +15%, cannot tell that apart from no growth or from 2% a year. Another half a million software and ICT workers are employed in other industries, about 190,000 more than in 2022-23; many are probably GCC staff classified under their parent firm's industry.

::: figure sector_employment
**Figure 10.** Employment in IT (NIC 62–63) from the PLFS, with 90% confidence intervals, and Nasscom's industry estimate, which is revised with each edition. The shaded portion counts ICT workers in other industries. The 2025 survey was redesigned.
:::

::: details How many jobs has the sector added?
Four estimates circulate. Read like for like, they agree with each other and with slow growth.

- **Nasscom:** +135,000 in FY26 (+2.3%). This includes GCCs and BPM, and is published before the year ends.
- **Goldman Sachs, via the World Bank:** the six largest firms shed about 64,000 jobs over three years, which our data reproduce (63,557), while the rest of the sector "added around 700,000".[^goldman] About 240,000 of that is Nasscom adding GCCs to its count. Like for like, the figure is about 390,000.
- **ICRIER:** "employment has continued to grow". This rests on PLFS data for 2021-22 to 2023-24, which we reproduce. It ends before the flat period.[^icrier]
- **PLFS:** +4% from 2022-23 to 2025, with a margin of error of about ±11 points.
:::

## 5. The entry level has narrowed

The FY22 hiring boom was extreme. TCS, Infosys and HCLTech hired about 218,000 freshers that year. By FY25 they hired 65,000, and in FY26 76,000. Staffing firms' estimates for the whole sector have the same shape, though their figures for the peak range from 400,000 to 600,000.[^fresher3p] Counts bottomed in FY24 and have recovered partly. Stated targets for FY27 are lower: 25,000 offers at TCS, 20,000 at Infosys, and none announced at Wipro or HCLTech.

::: figure fresher_intake
**Figure 11.** Fresher hires at the largest firms, FY16–FY26, with stated FY27 targets (hollow bars) and third-party estimates for the whole sector (points; hollow points are projections).
:::

The clearer signal is in shares. On every measure we have, IT's share of young entrants has fallen, while young graduates found more jobs elsewhere. Salaried graduates aged 21–25 working in IT held at about one million from 2022-23 to 2025, while salaried jobs for that age group grew by about a third.

::: figure four_shares
**Figure 12.** IT's share of four flows of young entrants: salaried graduates aged 21–25 (PLFS); net payroll additions aged 18–25 (EPFO); entry-level (0–2 years) technology openings (Xpheno); and fresher job postings (foundit).[^shares]
:::

Inside the firms, the workforce has grown older. The share of employees under 30 fell after FY23 at 8 of 10 large firms. At Infosys, the junior grade fell from 46% of staff in FY23 to 30% in FY26.[^cohort]

::: figure under30
**Figure 13.** Share of employees under 30, FY23 and latest year, ten large firms.
:::

::: figure infosys_grades
**Figure 14.** Infosys employees by grade, FY14–FY26.
:::

The pipeline shows the same pattern. Among NIRF-ranked engineering colleges, the number of graduates placed fell for the class of 2023-24, the first fall in the series, even as the number of graduates rose.[^nirf] Real pay of IT workers aged 21–25 fell 12% in 2025, while pay of those aged 31–40 fell 2%.[^pay]

::: figure nirf
**Figure 15.** Placement rate and median salary of four-year engineering graduates by graduating class, NIRF-ranked institutions, elite and other.
:::

::: figure junior_pay
**Figure 16.** Real monthly pay of salaried IT workers by age, and of all graduates aged 21–25, at 2025 prices. The 2025 survey was redesigned.
:::

Job postings point the same way. In the World Bank's analysis of Lightcast postings in South Asia, postings in AI-exposed occupations that asked for up to five years' experience fell most after ChatGPT, while those asking for ten or more years did not fall.[^lightcast]

::: figure postings_experience
**Figure 17.** Change in job postings after November 2022 per standard deviation of AI exposure, by experience required, with 95% confidence intervals. South Asia, mostly India; Lightcast data analysed by the World Bank.
:::

::: details Evidence against a collapse
Several indicators qualify the picture above.

- **Counts have recovered.** Sector fresher intake roughly doubled from FY24 to FY25 on Xpheno's estimates, and TeamLease's employer survey shows IT firms' hiring intentions rebounding in 2025–26.[^teamlease]
- **Fresher postings outside IT are strong.** Naukri's postings for 0–3 years' experience, across all industries, are back to their 2022 level. IT postings remain about 30% below.
- **Graduate unemployment is high but not rising.** About 40% of graduates aged 15–25 in the labour force were unemployed in 2023-24, close to State of Working India's figure. The rate fell from about 48% in 2017-18, and on the weekly measure it has not moved since.

::: figure grad_unemp
**Figure 18.** Unemployment rate of graduates aged 15–25 and 21–25, on the principal-status and weekly-status measures.
:::

- **The decline is milder than abroad.** India's technology postings and hiring fell by about a third from 2022. Software postings in the US and UK fell by about two-thirds.
:::

## 6. The firms show little strain

The six firms are not in financial distress. Attrition is back to 12–14%, from 22–28% at its 2022 peak. Utilisation is at or above its pre-COVID average at the four firms that report it, and the value of deals signed over the past year is flat or rising.

::: figure stress_gauges
**Figure 19.** Attrition and utilisation by firm, quarterly, against each firm's 2016–19 average.
:::

Workers' share of value added at the six firms has held at about 0.7 since FY16. Pay and value added per average employee both rose about 21% from FY23 to FY26. The firms have become smaller relative to their output, more senior and more expensive per head, but not more profitable at their workers' expense.[^labourshare]

::: figure labour_share
**Figure 20.** Labour share of value added: the six largest firms, listed IT firms in the RBI's company data, and three mid-tier firms, FY16–FY26.
:::

Prices have barely moved. No official price index covers IT services.[^noindex] Firms' own statements on earnings calls imply AI-related price cuts of 0.1% in FY25 and 0.4% in FY26, with about 1.5% expected in FY27. Brokers' forecasts of 2–3.5% a year of "AI deflation" include the routine annual discounts of about 1.5% that predate AI.[^m2]

::: figure price_giveback
**Figure 21.** AI-related price cuts implied by management statements, FY24–FY27, with range; the band shows brokers' forecasts.
:::

## 7. Client demand has softened and shifted

The United States buys about 54% of India's IT exports, and its clients are doing more of this work themselves. The in-house share of US computer jobs rose from 64–65% in 2015–22 to 67.5% in 2025. Employment at US IT-services firms has fallen 5% since March 2023.

::: figure us_inhouse
**Figure 22.** In-house share of US computer occupations, 2015–2025, and employment in US computer systems design firms (NAICS 5415), monthly.
:::

On earnings calls, managers' talk of weak demand peaked in 2023 and has stayed well above pre-2022 levels. Mentions of AI, and of passing AI savings on to clients, have risen steeply since 2025.

::: figure call_themes
**Figure 23.** Earnings-call statements per call about weak demand and about passing AI savings to clients, and mentions of AI per 10,000 words, by half-year.
:::

## 8. How other estimates compare

We checked widely cited figures against the sources above. Most are right about direction; several are wrong about size or meaning.

::: table
**Table 2.** Widely cited figures and what the data show
| Claim | Source | What we find | Reproduced? |
|---|---|---|---|
| The industry added 135,000 jobs in FY26 | Nasscom | Consistent with the PLFS | No |
| The rest of the sector added 700,000 jobs | Goldman Sachs, via World Bank | About 390,000 like for like | Partly |
| Employment has continued to grow | ICRIER | True to 2023-24; flat since | Yes |
| IT's share of young salaried graduates fell from 20.0% to 15.8% | Future of India | Correct | Yes |
| IT's share of value added going to labour has fallen | Future of India | Not on company or RBI data | Yes |
| About 40% of young graduates are unemployed | State of Working India | Correct on principal status | Yes |
| Entry-level hiring rose 168% | LinkedIn | Refers to hiring by firms of 1–10 staff | No |
| India's business-services exports are 27% above trend | Richard Baldwin | Correct; about half the gap predates ChatGPT | Yes |
| AI-exposed exports rose 39.5% | Economic Survey 2025-26 | A relative estimate, not a growth rate | Yes |
| IT hiring fell from 600,000 to 140,000 | Xpheno, via Economic Times | Fresher intake, not net hiring | No |
| AI will deflate prices by 2–3.5% a year | Brokers | Forecasts that include routine discounts | No |
---
"Reproduced" means we rebuilt the figure from data we hold. The full catalogue of sources, with every number checked, is in the repository.
:::

## 9. What to watch

- **FY27 results.** Infosys reports on 23 October. Whether the uptick in headcount and fresher hiring at TCS and HCLTech spreads to the other firms.
- **Prices.** Whether AI-related price cuts reach the 1.5% firms expect for FY27.
- **Coding agents.** Whether the mid-2026 jump in capability appears in FY27 hiring, especially at entry level.
- **GCCs.** The RBI's census of foreign-owned firms, due in late October 2026, is the best official read on captive centres.
- **Employment data.** PLFS 2026, and whether EPFO resumes its payroll releases, which stopped after September 2025.
- **Graduates.** NIRF placement data for the class of 2024-25.

## Appendix

### Sources and methods

**Firms.** Quarterly filings, fact sheets and investor releases of TCS, Infosys, HCLTech, Wipro, Tech Mahindra, LTIMindtree (LTI and Mindtree before the merger), Accenture and Cognizant; annual reports of 21 other listed firms; ESG and GRI disclosures for age data. Growth rates are log changes unless stated. Headcounts are global.

**Sector.** RBI Survey on Computer Software and ITES Exports; IMF balance of payments and WTO trade-in-services data; US Bureau of Economic Analysis and Bureau of Labor Statistics; Nasscom and Nasscom–Zinnov industry estimates, used with care; RBI company finances and MoSPI national accounts for value added.

**Workers.** PLFS unit-level data, 2017-18 to 2025; EPFO monthly payroll reports to July 2025; NIRF institutional data for graduating classes 2015-16 to 2023-24; Naukri JobSpeak, foundit, Xpheno, TeamLease and LinkedIn as published; World Bank South Asia Development Update (October 2025) for Lightcast postings.

**Prices and demand.** Price statements from earnings calls of eight firms, 2021–2026, coded by two independent coders; BLS occupational and payroll employment.

### Figures we cite but cannot reproduce

Staffing-firm estimates of sector fresher intake (Xpheno, HAN Digital, TeamLease Digital) and of GCC hiring; Nasscom's employment and revenue estimates; Nasscom–Zinnov GCC counts; the Lightcast postings analysis; LinkedIn's hiring rate; foundit and Xpheno postings data; ICRIER's firm survey; brokers' forecasts. Each is labelled as such where it appears.

### Corrections to figures in circulation

- TCS headcount in September 2026 was 4,700 *higher* than a year earlier, not 15,000 lower; it is 15,000 below its level of June 2025.
- The five largest firms' headcount fell by 6,981 in FY26, not 7,389.
- The five largest firms added about 160 people in the nine months to December 2025, not 17; both round to zero.
- Xpheno's "600,000 to 140,000" refers to fresher intake, not net hiring.

### Data notes

- **PLFS 2025** uses a new design with monthly sampling and a sample about 2.5 times larger, so changes into 2025 combine real change with design effects. The 2023-24 round includes one sampling unit with a very large weight; without it, IT employment is about 0.3 million lower that year.
- **EPFO** figures are revised down heavily after first release; we use final annual totals. EPFO's industry tables show only the ten largest industries in each age band, so IT is visible only for ages 18–28.
- **Postings are not hires.** Large IT firms recruit freshers mostly through campus drives that job portals do not see.

### PLFS acknowledgement

This page uses unit-level data from the Periodic Labour Force Survey, Ministry of Statistics and Programme Implementation (MoSPI), Government of India. Only aggregate tabulations are shown. The analysis and conclusions are ours, not MoSPI's.

[^gdp]: Exports in the RBI survey were 5.7% of GDP in FY26. Balance-of-payments figures, which classify the same exports differently, give a share nearer 8½% when business services are included.
[^selloff]: See, for example, Rest of World's coverage of the sell-off (6 February 2026).
[^twoq]: A separate working paper attempts that decomposition, under stated assumptions: [two questions about AI and jobs in Indian IT](two-questions.html).
[^bop]: Balance-of-payments data grow about twice as fast as the RBI survey over FY23–26 (39% against 19%). The survey is the more conservative measure, and we use it throughout.
[^ireland]: Ireland's exports are mostly the booked revenue of US technology firms' European headquarters and swamp the world total. Including Ireland, India's share was 20.4% in 2022 and 19.5% in 2025.
[^firmspecific]: Across firms and segments in FY24–26, differences between firms explain about 40% of the variation in growth by client industry and by region; the client industry or region itself explains 2–6%.
[^gcc]: No official statistic counts GCC employment. Our central estimate reconciles Nasscom–Zinnov reports, which are not comparable across editions, with staffing firms' hiring estimates. The plausible range is about 155,000 to 430,000 technology jobs.
[^gccpace]: GCC hiring was about 100,000–165,000 a year before 2023 and 94,000–180,000 after. In the RBI's census of foreign-owned firms, their exports grew about 5 points a year faster than total software exports in FY20–23 and about 4 points faster in FY24–25.
[^plfs]: Usual-status workers in National Industrial Classification divisions 62 (computer programming and consultancy) and 63 (information services). BPM work is mostly classified elsewhere. All PLFS figures are our tabulations of MoSPI unit-level data.
[^goldman]: World Bank, *India Development Update*, October 2026, p. 41, citing a Goldman Sachs client report (July 2026) that we could not obtain.
[^icrier]: ICRIER, *AI and Jobs: This Time Is No Different* (February 2026), Section 7. The report's survey of 651 firms finds 55% reporting lower entry-level employment and 35% higher; we cannot reproduce it.
[^fresher3p]: Xpheno, HAN Digital and TeamLease Digital, as reported in the press. None publishes its method. Xpheno's FY22 figure was about 450,000 when first estimated and 600,000 when quoted in 2026.
[^shares]: The PLFS and EPFO shares are our tabulations. The Xpheno and foundit shares are as published and cannot be reproduced. EPFO's last annual figure is FY25.
[^cohort]: Part of the fall is mechanical: staff hired in the FY22–23 boom are being promoted out of the junior grade and, from about FY30, will pass age 30. At Infosys, hiring of staff over 30 was about 65% higher a year in FY24–26 than in FY16–21, while hiring of under-30s was about the same.
[^nirf]: Comparing the same institutions within the same NIRF edition: the number placed fell about 1.8% while graduates rose about 3.3%. Placements include all employers, GCCs among them.
[^pay]: Mean monthly earnings of regular salaried workers, deflated by the consumer price index. The 2025 fall coincides with the survey redesign and is a single year; earlier rounds show steady growth.
[^lightcast]: World Bank, *South Asia Development Update*, October 2025, Annex Table A2.12. Postings for 0–5 years of experience fell 11.9% per standard deviation of AI exposure; those for 10–15 years rose 3.1%, not significantly. The data end in March 2025.
[^teamlease]: TeamLease's survey changed its sample in 2025, so the size of the rebound is uncertain.
[^labourshare]: Labour share is employee costs divided by employee costs plus operating profit. A widely shared chart showing a falling labour share combines survey take-home pay with national-accounts output; on that basis the six firms' wage bill alone would exceed the whole sector's.
[^noindex]: The US Bureau of Labor Statistics does not publish a producer price index for computer systems design, and no Indian index exists.
[^m2]: Coded from 108 statements on earnings calls and at investor days by eight IT firms and four BPO firms, converted to an effect on total revenue. The method and its assumptions are documented in the repository (round4/price_statements). The broker range is from Kotak, ICICI Securities and HCLTech's own guidance, as reported.
