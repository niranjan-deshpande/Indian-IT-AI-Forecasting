# Price data for Indian IT services: is there a usable g_p?

*Compiled 2026-10-05. Firm-level values: `audit/price_firm_disclosures.csv` (434 rows, each with source URL/document and page/section). Raw downloads (official series, broker and advisory PDFs, Infosys/Wipro 20-Fs) are in the session scratchpad, not the repo.*

**Bottom line.** No public source gives a measured, sector-wide price per unit of work (p) for Indian IT services in any period since 2015.

- **Measured series** are either **p/a** (revenue per billed person-month or per FTE, hourly or charge-out-rate price indices) or **modelled input cost** (BEA).
- **Measured p** exists only for narrow managed-services "resource units" (ISG).
- **Sector-wide p** exists only as **analyst estimates** for 2025–28. These estimates are built by *assuming* that productivity gains are passed through to clients, so they cannot be used to test S3 against S1.

**Labels.**
- *measured*: an official or firm-reported statistic.
- *estimated*: an analyst or advisory estimate.
- *commentary*: a qualitative statement.
- *derived*: my own arithmetic on measured values, stated as such.

**Relevance to g_p.**
- *direct*: measures p.
- *proxy*: measures p/a, or measures p for a narrow slice.
- *weak*: sign only, or p·Q.

## (a) Source table

### A1. Corrections to the previous probe (data/explore/prices/FINDINGS.md, NEXT_STEPS §5 C1)

| prior claim | verdict | evidence |
|---|---|---|
| BLS PPI does not cover NAICS 5415 | **Confirmed. Also, BLS has never published one.** | "Areas of Noncoverage in the PPI System" (bls.gov/ppi/fd-id/areas-of-noncoverage-in-the-ppi-system.htm, last modified 4 Mar 2026) lists 541511, 541512, 541513 and 541519. The BLS API v2 returns "Series does not exist" for PCU541511541511, PCU541512541512, PCU5415--5415--, PCU541513541513 and PCU541519541519. No 5415 entries appear in the current `pc.industry` file, the discontinued NAICS file `nd.industry`, or the SIC file `pd.industry`; the SIC file has 7372 and 7374 but no 7371 or 7373. Holdway (BLS), Voorburg Group 2008 sector paper, p.15: the US "does not publish or collect price data for ISIC Division 62". |
| WPU4561 is the nearest US index | **Confirmed, with caveats** | WPU4561 is "IT technical support and consulting services (partial)", Dec 2008 = 100, monthly, 2008M12–2026M08 (`wp.series`). WPU456101 and WPU45610101 are identical. It moves in step jumps, e.g. 121.6 → 138.1 in Jan 2024, and fell 165.1 → 142.9 in Apr 2025, which suggests a thin sample. The prior probe said it is built only from software publishers' secondary output; I did not re-verify that. |
| UK SPPI J62 is priced from charge-out rates | **Plausible, but not verified for the ONS itself** | The ONS methods document is behind a human-verification wall (405/HTML returned). Voorburg 2012 sector paper (Vizner, pp.17–21): "the main pricing method is charge-out rates", and all countries use time-based methods for programming. The ONS survey page (8 Apr 2025) says the index covers prices UK businesses charge UK businesses and government. Imports from India are therefore out of scope. |
| BEA custom-software deflator is input-cost based | **Confirmed** | NIPA Handbook ch.6 (Dec 2024), table of methods, line "Custom software": a weighted average of the prepackaged software price and a BEA input-cost index, with a productivity adjustment based on BLS multifactor productivity. Holdway 2008 gives the weights as about 75% input cost and 25% prepackaged. Own-account software uses the same index (Y005RG = Y004RG). |

### A2. Official price indices (all free; figures computed from downloaded files on 2026-10-05; annual % change)

**Series values by year (annual % change)**

| Series | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BLS WPU4561 (annual average, FRED `fredgraph.csv?id=WPU4561`) | +2.5 | +0.4 | +0.6 | +0.9 | +2.3 | +0.9 | +0.4 | +1.5 | +7.1 | +22.6 | +3.2 |
| BLS WPU45, professional services (partial) | +2.4 | +1.5 | +2.3 | +1.8 | +2.1 | +0.6 | +5.0 | +4.1 | +4.8 | +5.1 | +4.0 |
| BEA custom software Y004RG (NIPA T5.6.4 line 4, `NipaDataA.txt`) | −1.3 | −1.0 | −1.8 | −2.3 | −1.9 | −2.9 | −3.3 | −1.1 | +0.1 | −0.7 | −3.0 |
| BEA total software B985RG | −2.2 | −1.6 | −2.1 | −2.6 | −1.6 | −2.3 | −3.0 | −1.9 | 0.0 | +0.7 | −2.4 |
| BEA gross output price, computer systems design (TGO107-A, `GrossOutput.xlsx`) | −1.4 | −1.2 | −1.6 | −2.2 | −1.6 | −2.3 | −2.7 | −1.0 | +0.3 | 0.0 | −2.4 |
| BEA price index, imports of computer services (NIPA T4.2.4B, IA001165) | −0.4 | +0.2 | +0.4 | +0.1 | +1.1 | +1.6 | +1.0 | +0.1 | +2.2 | +3.8 | +2.6 |
| UK ONS SPPI J62 HR6L (generator CSV) | +0.5 | +1.5 | +1.5 | +2.5 | +1.4 | +3.4 | +2.7 | +4.0 | +4.1 | +2.8 | +0.6 |
| UK ONS SPPI J6202 consultancy, HRFE | +0.5 | +1.4 | +1.5 | +2.5 | +1.2 | +1.5 | +1.6 | +3.4 | +3.6 | +4.0 | +0.7 |
| UK ONS SPPI J6201 programming, HR6O | – | – | – | – | +5.0 | +5.1 | +3.9 | +5.0 | +4.6 | +2.2 | +0.7 |
| Eurostat SPPI J62, EU27 (`sts_sepp_a`, PRC_PRR, updated 2026-10-01) | 0.4 | 0.3 | 1.0 | 1.5 | 1.1 | 1.5 | 0.9 | 2.2 | 3.8 | 3.5 | 2.6 |
| BoJ SPPI custom software, excl. tax (PRCS15_4201350001 to 2020; PRCS20_4201450001 from 2021) | – | +1.8 | +0.8 | +1.7 | +0.8 | +1.2 | +0.3 | −0.6 | +2.8 | +3.8 | +3.8 |

Notes on the series:
- **WPU45:** base Jun 2009. 2015–2025 shown.
- **ONS:** the HR6L, HRFE and HR6O titles say "OUTPUT DOMESTIC". HR6L was 131.7 in 2026Q2. HR6O has annual data only from 2018.
- **Eurostat:** 2015–2021 carry flag "i" (imputed). The country series (DE, FR, IE, SE etc.) are in the scratchpad.
- **BoJ:** the 2015-base series starts in 2015, so there is no 2015 change. The tax-inclusive series is distorted by consumption-tax changes.

**What each index measures and how it relates to g_p**

| source | what it measures | period, frequency | label | relevance to g_p | p or p/a? |
|---|---|---|---|---|---|
| **BLS PPI NAICS 5415 / 541511–541519** | — (does not exist) | — | — | none | — |
| **BLS WPU4561** | Repriced contracts with fixed characteristics, under the general PPI method (no 4561-specific fact sheet found). Domestic US producers only, thin and partial sample. | 2008M12–2026M08, monthly | measured | weak (volatile, unknown sample, not Indian vendors) | p by design; in practice unclear |
| **BEA custom-software price** | Modelled: input cost (US software-occupation wages plus inputs) adjusted for productivity, blended with prepackaged software prices. No transactions observed. | 1959–2025, annual (total software also quarterly) | measured, but modelled | weak and circular (it builds in an assumed productivity rate) | modelled input cost; not p and not p/a |
| **BEA gross output price, NAICS 5415** | Industry gross-output deflator. Its source data were not found; it tracks the custom-software index (my inference). | 1997–2025, annual | measured (modelled) | weak | as above |
| **BEA import price, computer services** | Not an observed import price. NIPA Handbook ch.8 (Tables 8.A/8.B): "fixed-weighted price index" made from the BLS PPIs for data processing and software publishing. | annual | measured (proxy) | weak; does not observe Indian vendors' prices | US domestic PPI proxy |
| **BLS import/export price indexes (MXP)** | Services covered are only air freight and air passenger fares (BLS MXP overview PDF, 2025). | — | — | none | — |
| **UK ONS SPPI J62** | Prices that UK-resident businesses charge UK businesses and government. Method: probably charge-out rates (see A1). | 1996– (HRFE), 2008Q4– (HR6L), 2018Q4– (HR6O); quarterly | measured | proxy (domestic, excludes imports) | p/a (likely) |
| **Eurostat SPPI J62** | Transaction prices of resident producers; national methods, mostly charge-out or time-based. France 2008: 75% working-time pricing, 7% contract pricing (Holdway 2008). | annual and quarterly | measured | proxy | mainly p/a |
| **BoJ SPPI custom software** | 人月単価 (contract value per person-month), per BoJ FAQ for the 2005-base SPPI. Domestic B2B. | annual and monthly | measured | proxy | **p/a** |
| **India WPI / new Services PPI (OEA, DPIIT)** | The WPI covers goods only (OEA WPI/PPI Manual, base 2022-23). The Services PPIs launched 15 Jun 2026 cover only securities, banking, pension funds, insurance, telecom, railways and air passenger travel. IT is not in phase 1 or the named phase-2 list (Working Group report §8.2.8; press release `eaindustry.nic.in/press_release/sppi/sppi_press_release_202608.pdf`). | quarterly from 2026 | — | none | — |
| **India national-accounts deflator, IT/computer services** | 2004-05 series: deflated with CPI(AL)/CPI(IW), and WPI for the organised segment (MoSPI Sources & Methods 2012, §19.28). 2011-12 series, quarterly GDP methodology (28 Jul 2017), item 14: "Deflator used is WPI". 2022-23 base: not verified. | — | measured | none (a goods or consumer deflator, not a service price) | neither |
| **RBI** | No IT-services price index found (search incomplete, see log). | — | — | none | — |
| **Voorburg Group / OECD-Eurostat SPPI guide** | Methods literature | 2006–2013 | commentary | — | — |

Points from the Voorburg Group papers and the SPPI guide:
- Time-based or charge-out pricing dominates. Only Korea and the Netherlands use model pricing, and only for small firms (Vizner 2012).
- The guide notes there is no method "to measure changes in productivity per consultancy hour".
- Holdway (2008) gives a worked example in which replacing in-house developers with Bangalore staff, lowering the day rate from $1,800 to $1,400, should be recorded as a −22% price change if quality is unchanged.

### A2b. Final-pass check: BLS PPI for NAICS 5415 and 518210 (re-verified 2026-10-05)

Both series below are **US domestic producer prices**. They are a proxy for offshore Indian vendors' prices, not a measure of them. Files are in `data/explore/prices/final_bls/`.

**1. NAICS 5415 / 541511 / 541512 (computer systems design and related services): no BLS PPI exists.**
- The BLS API v2 (queried 2026-10-05) returns "Series does not exist" for PCU5415--5415--, PCU541511541511 and PCU541512541512 (`bls_api_2014_2023.json`, `bls_api_2024_2026.json`).
- The PPI industry list `pc.industry` and the discontinued-industry list `nd.industry` contain no 5415 or 54151x code. Both were downloaded from download.bls.gov/pub/time.series earlier today; copies are `pc_pc.industry` and `nd_nd.industry`.
- Source: BLS, "Areas of Noncoverage in the PPI System", https://www.bls.gov/ppi/fd-id/areas-of-noncoverage-in-the-ppi-system.htm (last modified March 4, 2026). It lists 541511 "Custom Computer Programming Services", 541512 "Computer Systems Design Services", 541513 "Computer Facilities Management Services" and 541519 "Other Computer Related Services" as not covered.

**2. NAICS 518210, data processing, hosting and related services: series PCU518210518210** (industry 518210, product 518210, not seasonally adjusted, base Dec 2000 = 100).
- **History:** the BLS fact sheet says "a new price index for Data Processing and Related Services was introduced into the PPI in January 2002, with historical data dating to December 2000". The `pc.series` record matches: begin 2000 M12, base date 200012, latest 2026 M08.
- **Method,** from the same fact sheet: "Each month, companies provide net transaction prices for a specified service. The transaction is an actual contract selected by probability, where the price-determining characteristics are held constant while the service is repriced." Also: "The prices used in index calculation are the actual prices billed for the selected service contract."
- **Fact sheet:** https://www.bls.gov/ppi/factsheets/producer-price-index-for-the-data-processing-and-related-services-industry-naics-518210.htm (last modified November 7, 2008).

Annual-average % change, computed from BLS API monthly values (`ppi_518210_monthly.csv`, `ppi_518210_annual.csv`):

| 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (Jan–Aug vs Jan–Aug 2025) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| +0.3 | +1.2 | +1.5 | +0.3 | +0.5 | +2.9 | +1.0 | +1.0 | +1.5 | +1.3 | +3.3 | +0.5 |

The last four months of 2026 data (May–Aug) are preliminary: BLS footnote "All indexes are subject to monthly revisions up to four months after original publication".

| source | what it measures | period, frequency | label | relevance to g_p | p or p/a? |
|---|---|---|---|---|---|
| BLS PPI PCU518210518210 | Contract repricing (fixed characteristics) for US-resident data-processing, hosting and BPM providers | 2000M12–2026M08, monthly | measured | **proxy**: the closest US output-price index to managed and run services, but domestic producers only, a different industry from 5415, and not Indian vendors | **p** (per contract, characteristics held fixed) |

**Reading.** US domestic contract prices for data-processing and hosting services rose about 0.3–1.5% a year in 2015–2019 and 2021–2024. They rose 2.9% in 2020 and 3.3% in 2025. There is no sign of deflation in this proxy through Aug 2026. This does not tell us what Indian vendors charge.

### A3. Firm disclosures (own documents; values in `audit/price_firm_disclosures.csv`)

| source | what it measures | period | freq. | free/paid | figures (with citation) | label | relevance to g_p | p or p/a? |
|---|---|---|---|---|---|---|---|---|
| **Infosys Form 20-F, Item 5 "Results of operations – Revenues"** (SEC EDGAR CIK 1067491; one URL per year in the CSV) | Growth of total/onsite/offshore **billed person-months** (IT services; "services other than BPM" to FY14), and change in **revenue per billed person-month** onsite/offshore/blended (called "rates" to FY10, "revenue productivity" FY11–FY15, "revenue realization" FY16–FY20; FY17+ 20-Fs define it as "revenue per billed person month"). USD reported terms. | FY2003–FY2020 (Apr–Mar years) | annual | free | Blended revenue/billed-PM, % YoY: FY10 −4.0; FY11 +1.8; FY12 +4.7; FY13 −3.0; FY14 +1.2; **FY15 −2.8; FY16 −4.7; FY17 −2.7; FY18 +1.5; FY19 −0.8; FY20 −1.5**. Billed PM growth: FY15 9.3; FY16 14.5; FY17 10.2; FY18 6.0; FY19 9; FY20 8.0. (FY2003–FY09 onsite/offshore "rates" also in CSV, e.g. FY08 +6.9/+6.1, FY04 blended "pricing decline of 5.0% in U.S. dollar terms".) Paragraph dropped from the FY2021 20-F onward (searched FY21–FY26 full text). | measured | **proxy** (best firm-level series that exists) | **p/a** (revenue per billed hour-equivalent); billed PM = a·Q |
| Infosys quarterly fact sheets, "Effort and Revenues – Consolidated IT Services" table (local copies `data/sources/infosys/factsheets/`) | Billed effort (person-months) and revenue (USD m), onsite/offshore/total | Q1FY12–Q4FY18 (Jun-2011–Mar-2018); dropped from Q1FY19 (FY19+ sheets keep only effort *mix* %) | quarterly | free | e.g. Q4FY15 296,791 PM / $1,949.34m; Q4FY18 391,793 PM / $2,551m. Derived (not firm-reported) revenue per billed PM: ≈$7.0k (FY14–1HFY15) → ≈$6.3–6.5k (FY17–FY18); YoY −4% to −7% in Q3FY15–Q3FY16, −1% to −4% in FY17, +0.7% to +3.5% in 2HFY18. | measured (levels); derived (ratios) | proxy | p/a |
| Infosys Q3FY16 earnings call (company-filed 6-K 0001067491-16-000061, Ex.99.6, CFO remarks) | Realization (revenue per billed PM), reported and **constant currency** | Q3FY16 (Dec-2015) | one quarter shown; CFOs gave this on most calls FY12–FY18 | free | YoY −4.5% reported, **−1.1% cc**; QoQ −2.5% reported / −2.0% cc (−1.5%/−1.0% ex one-off fee); volume +3.1% QoQ | measured (firm-reported, spoken) | proxy | p/a |
| Derived: Infosys realization adjusted to constant currency (my calculation) | (1+realization_rep)×(1+g_cc)/(1+g_rep)−1, with company-wide reported and cc revenue growth from local Q4 fact sheets (FY15–18 cc growth built from the quarterly "Constant currency – YoY" tables; FY19 9.0% and FY20 9.8% cc as printed in the Q4FY19/Q4FY20 sheets) | FY15–FY20 | annual | — | cc-adjusted revenue per billed PM ≈ FY15 −1.3; FY16 −1.1; FY17 −1.9; FY18 +0.1; FY19 +0.2; FY20 −0.1 (%) | **derived from measured** (approximation: cc revenue is company-wide incl. BPO/products, realization is IT services; ignores onsite/offshore mix) | proxy | p/a |
| **Wipro Form 20-F**, Item 5 IT Services segment (CIK 1123799) | "Volume" growth, onsite-offshore mix effect, onsite/offshore "price realization" change (undefined in filing; presumably revenue per billed PM) | FY2009–FY2012 only | annual | free | FY09 offshore +3.8, onsite +3.2; FY10 onsite +3.68, offshore −1.42; FY11 volume +16.8, mix +2.2, onsite −2.7, offshore +0.7; FY12 volume +11.5, mix +1.3, onsite +2.3, offshore +0.6 (%). No volume/price attribution in FY2013–FY2026 20-Fs (full-text search). | measured | proxy (pre-2015 only) | p/a |
| **LTI (pre-merger LTIMindtree) quarterly fact sheets** (`data/sources/ltim/lti_*_fs.pdf`) | Billed person-months onsite/offshore; revenue USD m | Q4FY16–Q2FY23 (Mar-2016–Sep-2022); not in post-merger LTIMindtree sheets | quarterly | free | e.g. Q4FY19 13,681 + 48,923 PM, $353.8m; Q2FY23 17,095 + 95,726 PM, $601.0m | measured | proxy | p/a (R/billed PM); billed PM = a·Q |
| **Accenture 10-K/10-Q MD&A** (local `data/sources/accenture/flat/`) | Qualitative "pricing" statement each quarter. Accenture **defines "pricing" as "contract profitability or margin on the work that we sell"** | FY2015–FY2026 (47 filings) | quarterly | free | 2015–16 "relatively stable"/"improvement"; FY2020 Q3–FY2021 Q2 "pricing pressure" (esp. consulting); FY22 "improved across our business"; Q3 FY23 "lower in some areas"; **10-K FY2023 → Q1 FY2025: "lower pricing across the business"**; Q2 FY25 "relatively stable"; Q3 FY25–Q2 FY26 "improved in several/some areas"; Q3 FY26 (Jun-2026) "relatively stable". | commentary | weak (sign only) | neither — margin concept, mixes p with w·a |
| **Cognizant 10-K/10-Q MD&A** (local `data/sources/cognizant/txt/`) | Qualitative pricing statements | 2014–2026 | quarterly | free | "pricing pressure within our core portfolio" (10-K FY2019 → 10-Q Q3 2020); "pricing pressure on our non-digital services" (Q1 2021 → Q3 2022); "pricing improvements" cited as margin tailwind in 2022. No quantified price figure in any filing. | commentary | weak | p (direction only) |
| TCS (press releases, fact sheets, analyst decks FY07–FY27, local) | — | — | — | — | **No pricing, realization or billed-effort metric ever disclosed** (only utilization, T&M vs fixed-price revenue shares, and occasional qualitative "volumes as well as realisation" e.g. Q3FY14 press release). | — | none | — |
| HCLTech, Tech Mahindra, LTIMindtree (post-merger) investor releases (local) | Revenue per employee (HCLTech, $K p.a.) only | — | quarterly | free | e.g. HCLTech Q1FY27 revenue per employee $65.5K (investor release) | measured | weak | R/L, not p |

### A4. Sourcing advisory / industry bodies

| source | what it measures | period | freq. | free/paid | figures (with citation) | label | relevance to g_p | p or p/a? |
|---|---|---|---|---|---|---|---|---|
| **ISG Index Insider**, "AI Isn't the Only Reason Providers Are Feeling Pricing Pressure", S. Jones & M. Rose, 31 Oct 2025, https://isg-one.com/articles/index-insider--ai-isn-t-the-only-reason-providers-are-feeling-pricing-pressure (Data Watch section) | Contracted **resource-unit (RU) price** glide paths in IT managed-services contracts (ISG deal data; sample not stated) | historical vs. deals of the prior 12 months (≈Nov 2024–Oct 2025) | ad hoc | free | Historically RU prices fall 10–20% by end of contract year 2; in the last 12 months this "doubled or even tripling in some cases"; example server RU $20 → $16 at year 2 (vs. $18 historically). Verified by WebFetch 2026-10-05. | measured (ISG contract data) | **direct, but narrow**: within-contract unit prices for managed services (mostly infrastructure-type RUs), all vendors, not Indian-specific | **p** (price per resource unit), but RUs are infrastructure-style units; ADM priced on FTE/T&M is not covered |
| ISG Index Insider, "Infrastructure Outsourcing Prices Continue Double-Digit Declines", Jones & Sauter, 17 Mar 2023, https://isg-one.com/articles/index-insider-infrastructure-outsourcing-prices-continue-double-digit-declines | Committed infrastructure unit prices over contract life | contracts ≈2018–2023 | ad hoc | free | 10–30% cumulative over 5 years depending on transformation; market prices may fall up to 2× the contracted rate | measured/commentary (secondhand via sub-agent; not re-verified) | proxy for infra p | p |
| ISG Index Insider, 8 Sep 2023 and 1 Dec 2023 (mainframe) | Indexed unit price, infra managed services | ~20 yrs to 2023; mainframe 2016–21 | ad hoc | free | chart only (values not machine-readable); mainframe prices "stopped declining" in 2020 | measured (unreadable) / commentary | proxy | p |
| CIO.com (S. Overby), 30 Sep 2016, https://www.cio.com/article/236210/, reporting ISG "Automation Index" | Total client cost reduction by tower for $10M+ ACV deals vs. baseline | ≈2016 | one-off | free | 26–66% total; 14–28 pts from automation; arbitrage+process alone 20–30% | measured (ISG), baseline = client's pre-deal cost (not vendor price change) | weak | client cost, not vendor p |
| **ISG Index** quarterly releases (ir.isg-one.com; PRNewswire) | Annual contract value (ACV) of commercial outsourcing/managed-services deals ≥$5M | 2015–2Q26 | quarterly | free | 2015 ACV −8% ($23.7B), avg ACV/deal −20% 2012–15 (release 14 Jan 2016); 2025 managed-services ACV $43.4B (+1.3%); 2Q26 $10.9B (+2.7%) with commentary on "pricing deflation" (release 9 Jul 2026) | measured | weak (p·Q, new contracts only) | p·Q |
| **Everest Group Pricing Index™** H1 2023, H2 2023, H1 2024 (free PDFs, e.g. https://www.everestgrp.com/wp-content/uploads/2024/09/Everest_Group_-_Pricing_Index_H1_2024.pdf, "Pricing Index benchmarks" table and "Key methodology points") | **FTE-based** price (final-bid/BAFO, year-1, no COLA/FX) from Everest live-deal database, by delivery location | H1 2022–H1 2024 (+projection to H1 2025) | semi-annual | free summary | **India ITO-standard**, 12-month change: +3.1% (H1'23), +1.3% (H2'23), −0.4% (H1'24); projected −0.7% (H1'25). India ITO-advanced: +4.7%, +2.1%, +1.4%; proj. +0.9%. US ITO-standard −0.2% (H1'24). Values verified in local pdftotext copies. | measured (advisory database) | proxy | **p/a** (per-FTE rate) |
| Everest Pricing Bulletin, 1 Oct 2024, https://www.everestgrp.com/media/the-pricing-bulletin-ai-efficiencies-and-competition-drive-cloud-infrastructure-pricing-down/ | Like-for-like cloud-infrastructure deal price | ≈2021–24 | ad hoc | free | deal sizes down 15–20% for same scope and volume | estimated (basis not stated) | proxy (infra/cloud only) | p |
| Everest "Cost Optimization and Price Reset" page (24 Jun 2025, upd. 18 Nov 2025) | Self-reported client negotiation outcomes | 2025 | — | free (marketing) | 35–40% price cut RFP→contract; 20–30% yr-1 savings | commentary (marketing) | weak | negotiation discount, not market p |
| Everest PriceBook / full Pricing Index; Avasant AvaMark; Forrester "Global IT Services Market Forecast 2025–2029" (RES189829, $1,495); NelsonHall | rate cards, pricing benchmarks, spend forecasts | — | — | **paywalled** | contents not seen; Forrester summary: IT services CAGR 1.8% ex-IaaS 2024–29 (p·Q) | — | unknown | mostly p/a or p·Q |
| Gartner (N. Suda, quoted in TechTarget, 26 Mar 2026, https://www.techtarget.com/ai/feature/Businesses-face-complex-cost-cutting-options-with-GenAI) | Mid-contract price cuts won by CIOs citing AI | 2025–26 | — | free | 5–30% | commentary | proxy (renegotiated contracts only) | p |
| Gartner IT spending forecasts (press releases 403-blocked; figures only from search snippets) | IT services spending | 2024–26 | quarterly | free | 2026 IT services growth forecast +8.7% (Feb 26), +5.3% (Jul 26) — **unverified** | estimated (unverified) | weak | p·Q |
| **HFS Research** "Stop buying AI like labor" (Daher & Biswas, 15 Jul 2026; 304 G2000 buyers, with EY), https://www.hfsresearch.com/research/stop-buying-ai-like-labor/ ; HFS news 30 Jun 2026 | Buyer expectations of AI-led service cost; renegotiation behaviour | 2026 | survey | free summary | avg expected price decline 19% (40% expect 10–30% lower; 34% >30%); some clients seek 25–30% cuts on >$50M-ACV contracts within 24 months | estimated (survey of expectations) / commentary | proxy | p (expected) |
| HFS webinar deck 24 Jul 2025 (slide 23) | "Services-as-software" scenario | 2024–35 | — | free | tech services ~$1.5T → ~$1T, −3% to −5% CAGR | estimated (scenario) | weak | p·Q |
| Nasscom Strategic Review 2023 and 2026 (exec. summaries) | Industry commentary | CY2022; FY26 | annual | summary free | "significant pricing pressures" in CY2022; shift FTE→outcome pricing; **no quantified price estimate** | commentary | weak | — |
| CIO.com 7 Apr 2015 (Alsbridge, ISG's S. Hall) | Automation-led bids | 2015 | — | free | some bids up to 40% below competitors | commentary | weak | p (bids) |

### A5. Equity research and news quoting analysts (secondhand unless a PDF is cited)

| source | what it measures | period | free/paid | figures (with citation) | label | relevance | p or p/a? |
|---|---|---|---|---|---|---|---|
| **Kotak Institutional Equities**, "Caught in the narrative war", 20 Feb 2026 (summary, https://www.equitybulls.com/category.php?id=367189) | AI deflation of existing services spend | ~FY26–FY29 | summary free; report paid | **~16% gross revenue deflation on existing services spend over 3 years**; assumes 50% of savings reinvested → 2–3% downside to growth; peak FY2027E (verified by curl) | estimated | **proxy for p on existing scope** (gross); net = mixed | gross ≈ p (fixed scope); net mixes p and Q |
| Kotak IE sector report via ANI, 25 Aug 2026, https://www.aninews.in/news/business/ai-could-drive-3-35-annual-revenue-deflation-in-indian-it-services-through-fy28-kotak20260825140021/ | AI-led annual revenue deflation, Indian IT | through FY2028; crossover FY2029 | free (news) | **3–3.5% a year**; highest in app development and CX BPO, lowest in infra; clients in multi-year managed-services deals demand future AI savings upfront (verified by curl; a later re-fetch by the orchestrator on 2026-10-05 returned HTTP 403, so it was not independently re-checked) | estimated (secondhand) | proxy | mixed (net) |
| Kotak IE via ANI, 30 Sep 2026, https://aninews.in/news/business/ai-deflation-weak-demand-to-keep-large-it-growth-muted-in-q2fy27-mid-tier-to-outperform-kotak20260930115045/ | gross vs. net deflation | current (period not stated; reads as annual) | free | "gross deflation of ~7% and net deflation of 3.5%" (verified) | estimated (secondhand) | proxy | gross ≈ p; net mixed |
| Kotak IE, other notes (BusinessToday 6 May 2025: 2–3% over 2–3 yrs; Whalesbook 6 Mar 2026: raised to 3–3.5% FY27–28; 3 Jul 2026: upper end, "higher productivity pass-throughs"); "Doubly difficult" PDF 4 Aug 2025 (commentary) | as above | 2025–28 | free | see column | estimated / commentary (sub-agent; not all re-verified) | proxy | mixed |
| **Jefferies** via Tribune/ANI, 12 Sep 2025, https://www.tribuneindia.com/news/ai/al-may-drive-20-revenue-deflation-in-it-services-over-cy25-30-jefferies | AI revenue deflation on existing IT services | CY25–30 | free (news) | **~20% revenue deflation over CY25–30**; 5–35% productivity boost by service line; non-AI services decline 1–3% a year (verified by WebFetch) | estimated (secondhand) | proxy | ≈p on existing scope (gross) |
| **HSBC** via Medianama, 17 Oct 2025, https://www.medianama.com/2025/10/223-hsbc-report-ai-impact-on-indian-it-sector-10/ ; later raised to 14–16% gross (India Dispatch 26 Feb 2026; BS 10 Mar 2026) | AI revenue contraction | 3–4 yrs | free (news) | 8–10% over 3–4 years (≤3–4%/yr); custom app dev −4.5pp, AMS −2.1pp, BPO −1.2pp | estimated (secondhand; not re-verified) | proxy | mixed |
| **Motilal Oswal**, "Productivity gains and Indian IT – value at risk?", 5 Jun 2025, https://ftp.motilaloswal.com/emailer/Research/IT-20250605-MOSL-SU-PG012.pdf p.1 | automatable effort | near term | free PDF | 44% of ADM hours automatable; ADM ≈30% of revenue → ~12–13% of revenue at risk (verified in PDF) | estimated | proxy for **a**; p only if passed through | a |
| Motilal Oswal sector update 24 Nov 2025 (PDF, p.3) | history FY15–19 | FY15–19 | free PDF | fixed-price mix rose (Infosys 41%→53%, HCLT 44%→49%, Wipro 49%→59%); "employee productivity basically flatlined" (verified) | measured (firm data compiled) / commentary | weak | R/L |
| Motilal Oswal, TCS 4QFY26 (9 Apr 2026, https://bsmedia.business-standard.com/_media/bs/data/market-reports/equity-brokertips/2026-04/17758080410.48368500.pdf, p.1) | revenue per employee vs. margin | FY26 | free PDF | ~8% productivity gains and ~5% INR depreciation yet modest margin flow-through; "AI deflation [is] sucking up all productivity benefits" (verified) | commentary + analyst inference | proxy (suggests p fell as a fell) | p/a (R/L) and inference about p |
| Motilal Oswal, Infosys 4QFY26 (23 Apr 2026, https://bsmedia.business-standard.com/_media/bs/data/market-reports/equity-brokertips/2026-04/17770201200.85965100.pdf, p.2) | relayed management commentary | FY26 | free PDF | FY26 growth "led by realization improvements (RPP), partly offsetting flattish volumes"; new deals embed AI productivity commitments upfront over 3–5-year terms; repricing visible at bid/renewal (verified) | commentary (secondhand management) | proxy | **p/a** rising, a·Q flat |
| **ICICI Securities** (B. Tiwary), "Sound and Fury: The AI Question!", 26 Mar 2026, https://www.icicidirect.com/mailcontent/idirect_itsectorupdate_march26.pdf p.1 | modelled AI deflation | FY27–28 | free PDF | ~2–3% annual deflation in traditional services; models 2–3% AI-led revenue deflation in both FY27 and FY28 (verified) | estimated | proxy | mixed |
| CLSA (Asianet 22 Aug 2026; TradingView 19 Aug 2026) | AI deflation | to FY30 | news | "typically estimated at 2–4%", offset by new AI volumes by FY30 | estimated (secondhand; not re-verified) | proxy | mixed |
| Forrester (S. Roy) blog 7 Jul 2017, https://www.forrester.com/blogs/17-07-07-whither_indian_it | annuity revenue erosion | 2017–20 | free | automation/cloud/SaaS cut annuity revenue (~60% of total) by up to 40% → ~a quarter of total revenue | estimated (not re-verified) | weak | mixed |
| Business Standard 8 Jun 2017 (Infosys executive) | renewal cost take-out | 2017 | free/partial | renewing clients ask for 20–30% cost take-out for same projects | commentary (management, secondhand) | proxy (renewals only) | p |
| Historical broker commentary 2016–2020 (Sharekhan 29 Aug 2016; PhillipCapital 7 Jan 2017; Nomura & Kotak 11 Feb 2019; PL & HDFC Sec 4 Jun 2020; ex-Infosys CFO 1 Sep 2018 — all Business Standard) | pricing pressure on renewals / traditional services | 2016–20 | partial paywall | qualitative only; no quantified sector price change | commentary | weak | — |
| JPMorgan (Reuters 10 Feb 2023; ANI 28 Jun 2026), Nomura (5 Dec 2025), Emkay on Accenture Q4 (BusinessToday 5 Oct 2026), Anand Rathi (ANI 3 Aug 2026), PL/JM (BS 24 Jul 2026) | qualitative | 2023–26 | news | "deflate pricing"; "revenue deflation from accelerated discounting"; Accenture pricing "declined in many areas in Q4" | commentary | weak | p (direction) |
| Prabhudas Lilladher "20–50% deflation in affected services" (Multibagg, 2 May 2026) | — | — | — | original note **not found** | estimated (low confidence, not used) | — | — |

## (b) Assessment

**Can g_p be calibrated for any period? No.** No source provides a measured sector-level p for Indian IT services, for any period. There are four reasons.

1. **Official indices observe the wrong producers and price the wrong thing.**
   - Every index covers resident producers selling domestically (UK, EU, Japan, US). None observes an offshore Indian vendor's invoice.
   - Where the method is documented, it is time-based (charge-out rates per hour or day, or per person-month at the BoJ), so it measures **p/a**.
   - The US has no index for NAICS 5415. BEA's deflators for software and for 5415 are modelled from input cost plus an assumed productivity rate, which is circular for our question.
   - India deflates IT GVA with the WPI or CPI and has no IT services price index.
2. **Firm disclosures are p/a and stop early.**
   - Infosys reported growth in revenue per billed person-month and in billed person-months (= a·Q) every year FY2003–FY2020 (20-F), and quarterly levels FY12–FY18 (fact sheets).
   - Wipro did so only for FY09–FY12. LTI published billed person-months to Sep 2022.
   - TCS, HCLTech and TechM never did. Accenture's "pricing" is a margin concept.
3. **Sector "deflation" figures for 2025–28 are model outputs, not observations.**
   - Kotak, Jefferies, HSBC, Motilal Oswal and ICICI Securities derive them from segment productivity gains × an assumed pass-through share (Kotak assumes 50% of savings is reinvested).
   - They assume S3 rather than test it.
4. **The one measured p is narrow.** ISG's figures are contracted resource-unit price paths in managed-services deals: all vendors, mainly infrastructure-style units, sample not published. Price declines built into contracts existed long before GenAI.

**Bounds (state with labels; all are firm- or segment-specific, not sector).** Since g_p = g_{p/a} + g_a, any p/a series gives an *upper* bound on g_p if labour per unit a is non-increasing. That is an assumption, not a sourced fact. Mix shifts (onsite/offshore, service line) contaminate every p/a figure.

| period | evidence | g_p statement | label |
|---|---|---|---|
| FY2015–FY2017 (Apr 2014–Mar 2017) | Infosys revenue per billed person-month (20-F), USD reported: −2.8 / −4.7 / −2.7%. Constant-currency adjusted (my calculation): ≈ −1.3 / −1.1 / −1.9%. Q3FY16 cc −1.1% YoY confirmed by the CFO on the earnings call. | Infosys g_p ≤ about −1% to −2% a year if a was non-increasing. No lower bound. | measured p/a; bound is **derived** plus an assumption |
| FY2018–FY2020 | Same series: +1.5 / −0.8 / −1.5% reported; cc-adjusted ≈ +0.1 / +0.2 / −0.1%. | Infosys g_p ≤ about 0% a year (same assumption) | measured p/a → derived |
| FY2021–FY2024 | No firm series (Infosys stopped disclosing). Everest India ITO-standard FTE price: +3.1% (H1'23), +1.3% (H2'23), −0.4% (H1'24); projected −0.7% (H1'25). | g_p ≤ about +3% to −0.4% a year (same assumption) | measured p/a (advisory) → derived |
| 2024–2026 (contracts) | ISG resource-unit glide path: historically −10% to −20% by contract year 2 (≈ −5% to −11% a year); for deals signed in the 12 months to Oct 2025, about twice that (server example −20% over 2 years ≈ −10.6% a year). | p for managed-services resource units: about −5% to −11% a year historically, steeper for 2025 deals. Not sector-wide. | measured (narrow) |
| FY2026–FY2028 | Analyst gross deflation on the existing book: Kotak ~16% over 3 years (~5.6% a year) and "~7%" (Sep 2026); Jefferies ~20% over CY25–30 (~4.4% a year). Net: 2–3.5% a year (Kotak, ICICI Sec, CLSA "2–4%", HSBC ≤3–4%). | Sector g_p on unchanged scope ≈ **−4% to −7% a year**. Net revenue effect of "deflation" (mixing p and Q) ≈ −2% to −3.5% a year. | **estimated**, conditional on assumed pass-through |
| sign checks | Accenture "lower pricing across the business" (10-K FY23 → 10-Q Q1 FY25), then stable or improved (margin concept). Cognizant "pricing pressure" (2019–2022). Infosys FY26 growth "led by realization improvements … partly offsetting flattish volumes" (MOSL relaying management). TCS ~8% productivity gains with little margin flow-through (MOSL inference). | direction only | commentary |

**Implication for S1 vs S3.**
- The pieces are consistent with S3 in 2025–26: analysts' gross deflation is large, while FTE rates (Everest) and Infosys realization (FY26) are flat or slightly rising, so p/a is not falling while p is said to fall, i.e. a is falling.
- But the only quantification of p in that story is the analysts' assumption itself. No public source lets the pilot calibrate g_p independently of the S3 hypothesis.
- The best pre-AI baseline is Infosys FY15–FY20: cc revenue per billed person-month roughly −1% to −2% a year, then flat. That bounds Infosys's g_p from above, not the sector's.

**Cheapest next steps (not done here):**
- Assemble Infosys's quarterly cc realization from the FY12–FY18 call transcripts in local EDGAR 6-K exhibits (p/a, quarterly).
- Buy the ISG, Everest or Avasant benchmark data, which hold like-for-like renewal prices (p).
- ONS SPPI microdata via the Secure Research Service (long shot; domestic producers only).

## Management statements timeline (earnings calls) — see price_calls_timeline.md

The full timeline is in `price_calls_timeline.md`. It covers 389 verbatim management statements from 183 transcripts, Jan 2021 – Oct 2026, all 8 firms; only TCS Q4FY23 is missing. Row-level data with page citations are in `audit/price_calls_quotes.csv`. All of it is **commentary**. Three quotes were re-checked against the source text by the orchestrator: Infosys Q1FY26 (SEC 6-K, live), HCLTech Q4FY26 p.21 and Accenture Q3FY23 p.11.

How the language moved:
- **2021H1:** pricing called "stable".
- **2021H2–2022:** rate-card and COLA increases (HCLTech realization +1%, then +30 bps; TechM ≈1% margin from pricing over FY23).
- **Apr–Jun 2023:** "no price expansion".
- **2023H2–2024:** pricing "stable"; AI deflation said to be "two to three years away" (HCLTech).
- **2025:** pass-through of AI savings made explicit (LTIMindtree from Jan 2025; TCS "$100 … $95 or $90", Apr 2025; Wipro and Infosys from Oct 2025).
- **2026:** quantified. HCLTech gives 2–3% a year portfolio deflation and "$100 million deal … maybe 80 million"; LTIMindtree ≈15% less for the same scope; TCS says renewals carry 10–15% productivity "even without AI".

Relevance to g_p:
- These statements are commentary, not measured prices.
- They suggest g_p was about 0 or positive in 2021–22 and flat in 2023–24.
- From 2025, extra AI-related deflation of roughly −2% to −3% a year is claimed, mostly as a forecast.
- On top of that sits pre-existing managed-services give-back of roughly −2% to −5% a year on that work.
- HCLTech says "very little" of this shows in reported numbers yet.

## (c) Search log

**Constraint.** The session-wide WebSearch cap (200 queries, shared across this agent's three sub-searches) was reached. Items marked "not attempted" below were not searched because of that cap. Fetches via WebFetch and curl of URLs already known continued to work. No browser pane was used.

**Firm disclosures (local plus EDGAR)**
- **Infosys local fact sheets:** 61 local PDFs (Q1FY12–Q1FY27) converted with pdftotext. "Effort and Revenues" tables are present Q1FY12–Q4FY18 and absent from Q1FY19 on (only effort mix % remains).
- **Infosys 20-Fs, FY2005–FY2026:** 22 filings downloaded from EDGAR (CIK 1067491) into the scratchpad. The person-month and realization paragraph is present FY2005–FY2020 (covering FY2003–FY2020) and absent FY2021–FY2026.
- **Infosys transcripts in local 6-K exhibits:** grep for pricing/realization. Q3FY16 CFO statement recorded; the rest is left to the transcript agent.
- **Wipro 20-Fs, FY2009–FY2026:** 18 filings downloaded (CIK 1123799). Volume and price realization appear in the FY09–FY12 MD&A only.
- **LTI fact sheets (local):** billed person-months Q4FY16–Q2FY23. Post-merger LTIMindtree sheets have none.
- **TCS:** local press releases, fact sheets, analyst decks and operating-metrics sheets FY07–FY27. No pricing, realization or effort metric.
- **HCLTech, TechM (local):** revenue per employee only.
- **Accenture 10-K/10-Q (local, 2014–2026):** qualitative "pricing" sentence each quarter. Accenture defines pricing as contract margin.
- **Cognizant 10-K/10-Q (local, 2014–2026):** qualitative only.
- **Mphasis, Hexaware, Persistent:** not checked (search cap).

**Official indices**
- **BLS:**
  - Noncoverage page: WebFetch worked; curl got "Access Denied".
  - API v2: series-does-not-exist for 5415 IDs.
  - `download.bls.gov` pc/wp/nd/pd series files: 403 without full browser headers, 200 with them.
  - FRED `fredgraph.csv` for WPU4561 and WPU45.
  - MXP overview PDF; July 2025 discontinuation notice (nothing in 5415).
  - Not attempted: Monthly Labor Review articles.
- **BEA:**
  - Worked: `NipaDataA.txt`, `SeriesRegister.txt`, `GrossOutput.xlsx`, `ValueAdded.xlsx`, NIPA Handbook ch.6 and ch.8.
  - Not found: source documentation for the 5415 gross-output price.
- **ONS:**
  - Worked: generator CSVs for HR6L, HRFE and HR6O; QMI (Oct 2025), which gives no J62 method; survey page.
  - Failed: methods documents (webarchive 405; ons.gov.uk returned a human-verification page).
- **Eurostat:**
  - Worked: API `sts_sepp_a` and `sts_sepp_q`; `sts_esms` metadata.
  - Failed: `sts_os_pp_esms` (404).
- **BoJ:** stat-search API (PR02); 2005-base FAQ; 2020-base outline; BoJ Review 2024-E-6.
- **India:**
  - Worked: OEA/DPIIT site, Services PPI press release Aug 2026, WPI/PPI Manual, metadata, Working Group report; MoSPI Sources & Methods 2012 and quarterly GDP methodology 2017 (URLs found in the site's JavaScript bundle).
  - Not attempted: the older 2014–2020 OEA pilot SPPI reports, RBI, and the MoSPI 2022-23 base methodology.
- **Voorburg:** papers index; 2008 (Holdway) and 2012 (Vizner, scanned) sector papers; 2013 paper; OECD-Eurostat SPPI guide 2007. No ISIC 62 sector paper after 2012.

**Sourcing advisory**
- **ISG:** 8 Index Insider articles fetched. Quarterly press releases for 4Q15, 4Q25, 1Q26 and 2Q26. ISG presentation PDFs (1Q21, 4Q23, 4Q24, 2Q26) returned 404 or had moved. The claimed "renewals 20–30% lower" ISG statistic was **not found**.
- **Everest:**
  - Free: Pricing Index H1'23, H2'23 and H1'24 PDFs; Pricing Bulletin 1 Oct 2024; Cost Optimization page.
  - **Paywalled:** PriceBook (about 65 roles × 10 geographies) and the full Pricing Index report. Later editions (H2'24 onward) not located.
- **Gartner:** press releases returned 403 to WebFetch and curl; forecast figures were seen only in search snippets and are **unverified**. TechTarget articles quoting Suda and Lovelock fetched.
- **HFS:** news item (30 Jun 2026), "Stop buying AI like labor" summary, Sep 2026 FS survey, webinar deck.
- **Avasant:** pricing-trend pages are commentary only; AvaMark data **paywalled**.
- **Forrester:** forecast RES189829 **paywalled** ($1,495); summary only. 2017 blog read.
- **Nasscom:** Strategic Review 2023 and 2026 summaries, and 2024/2025 press releases: no quantified pricing.
- **NelsonHall:** one quote only. Zinnov, UnearthInsight, IDC, Kearney: nothing on price. Deloitte GOS 2024: snippet only, **unverified**.

**Equity research and news (about 45 sources)**
- **Broker PDFs read:**
  - Kotak "Doubly difficult" (4 Aug 2025).
  - Motilal Oswal: 5 Jun 2025, 24 Nov 2025, 5 Feb 2026 Morning India, TCS 4QFY26, Infosys 4QFY26 (bsmedia.business-standard.com broker-tips PDFs).
  - ICICI Securities sector update (26 Mar 2026).
- **News summaries:** ANI (curl; WebFetch got 403), BusinessToday, Business Standard (partial paywall), Medianama, Tribune, Equitybulls, Whalesbook, Asianet, TradingView/Moneycontrol mirrors, Reuters via MarketScreener, Forbes India, India Dispatch.
- **Re-verified by me:**
  - Kotak 16% gross over 3 years (Equitybulls) and 3–3.5% a year (ANI 25 Aug 2026).
  - Kotak "~7% gross, 3.5% net" (ANI 30 Sep 2026).
  - Jefferies 20% over CY25–30 (Tribune).
  - ISG 31 Oct 2025 article.
  - Everest India figures.
  - MOSL and ICICI Securities PDF figures.
  - One sub-agent claim was **corrected**: the Infosys "−1.1% cc" is Q3FY16 YoY, not full-year FY16.
- **Paywalled or not accessed:** Kotak KINSITE full reports; HSBC, Jefferies and CLSA full reports (press summaries only).
- **Not found:**
  - Quantified estimates from Nomura, Goldman, BofA, Citi, UBS, Macquarie or Bernstein.
  - The original Prabhudas Lilladher "20–50%" note.
  - Any 2016–17 broker estimate of "automation deflation x% a year".
  - Any analyst volume-vs-price decomposition using Infosys effort data.
  - "Morgan Stanley 2–3% a year" appeared only in a search snippet (**unverified**, not used).
