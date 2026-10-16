## FINDINGS_output.md

### 1. Baldwin (30–31 Jul 2026) and Nunes (2 Aug 2026)

**Reproduction.**
- Source: WTO `ITS_CS_QX` (sector SJ, partner World), via the free DBnomics mirror; WTO's own API needs a key.
- All nine rows of his table match to the decimal (`baldwin_table_reproduced.csv`). India: $184.7bn in 2025, growth +14.5% in 2024 and +17.3% in 2025, index 153.
- A log-linear trend fitted on 2015Q1–2022Q4 four-quarter rolling sums gives +27.0% at 2025Q4, exactly his figure (`fig_baldwin_india_obs_trend.png`).

**What the series is.**
- WTO reports India's computer/telecom/information line at about 69% of the IMF/RBI value and moves the rest into business services. Computer plus business services is identical in both sources.
- The share moved is 31–33% a year. The RBI survey's ITeS share is 31.3%, 32.5% and 30.7% (FY24–26).
- So Baldwin's $184.7bn is RBI business services ($120.5bn) plus about $64bn of BPO and engineering that RBI counts as software exports.

**Trend window** (`india_trend_gap.csv`):

| fit window | gap at 2022Q4 | gap at 2025Q4 |
|---|---|---|
| 2015Q1–2022Q4 (Baldwin) | +15.4% | +27.0% |
| 2015Q4–2022Q4 | — | +22.6% |
| 2015–19 | — | +48.6% |

- The increment after ChatGPT is about +10%.
- The cleaner statistic is Baldwin's own: 13.5% a year over 2015–22 vs 15.1% over 2022–25.

**Computer-services version** (IMF SI2, `fig_india_computer_trend.png`):

| | gap at 2022Q4 | gap at 2025Q4 | gap at 2026Q2 | growth 2015–22 | growth 2022–25 |
|---|---|---|---|---|---|
| Computer services | +16.8% | +28.5% | +30.0% | 9.6%/yr | 11.8%/yr |

**Shares, 2022–25** (`ing_dds_growth.csv`):

| | India | World | World excl. Ireland, Netherlands, Luxembourg |
|---|---|---|---|
| Computer, telecom and information | +38.4% | +42.2% | +35.5% |
| Business services | +60.9% | +30.2% | — |

**Nunes:** our numbers back his main points. Export value is not jobs, the category is broad, and the trend window drives the result. The Philippines is the weak series.

### 2. ING (16 Sep 2026, via Business Today)

`ing_gdp_shares.csv`, GDP from IMF WEO on India's fiscal-year basis:

| measure | FY20 | FY26 | ING |
|---|---|---|---|
| BoP software exports, % of GDP | 3.35% | 5.21% | 3.3% → 5.2% |
| Business services, % of GDP | — | 3.18% (3.26% for four quarters to 2026Q2) | 3.3% |
| Combined, % of GDP | — | 8.39% | 8.5% |
| BoP software exports, $bn | — | $203.7bn | "$205bn" |

- On the RBI survey, the share of GDP is 4.62% (FY20), 5.69% (FY23) and 5.66% (FY26). So the rise is mostly a BoP effect, and even on the BoP it was 4.51% by FY23.
- Digitally delivered exports, 2022–25, using the deliverable BoP items as a proxy: India +44.0% vs world +32.0% (139 reporters). Excluding India, Ireland, the Netherlands and Luxembourg, the world figure is +29.7%.

### 3. Economic Survey 2025-26, Box VII.2 (`raw_output/es/echap07.txt`)

**Definition:**
- Method: two-way fixed effects on log quarterly RBI BoP exports, Q1 FY18 to Q2 FY26.
- Treated: software, business and financial services.
- Control: travel, transport, insurance, government services and communication.
- Intervention: Q2 FY23 (Jul–Sep 2022), before ChatGPT.
- Result: coefficient 0.333, so e^0.333 − 1 ≈ 39.5%. By category: software 0.37, business 0.51, financial 0.12 (not significant).

**Replication** (`es_box_did.csv`):

| specification | coefficient |
|---|---|
| Pooled | 0.361 |
| Software | 0.329 |
| Business | 0.498 |
| Financial | 0.257 |
| Control excluding travel | 0.440 |
| Dropping COVID quarters | 0.476 |
| Sample extended to 2026Q2 | 0.392 |

**Raw growth over their window** (`es_raw_growth.csv`):

| category | growth |
|---|---|
| Software | +41.5% |
| Business services | +70.9% |
| Professional and management consulting | +92.7% |
| Control group | +15.6% (transport −15.5%, travel +101%) |

The software leg matches our BoP +38.8%. It is about twice the survey's +19.4% and far above the top six's +7%.

### 4. AIM / Unearthinsight (`aim_rpe_check.csv`, `aim_rpe_decomposition.csv`)

**Reproduction,** using FY USD revenue divided by FY-end headcount from `core_quarterly_final.csv`:

| firm | ours | Unearthinsight |
|---|---|---|
| TCS | $49,290 → $51,353, 0.59%/yr | same (exact) |
| Infosys | 2.47%/yr | exact |
| HCLTech | 0.45%/yr | exact |
| TechM | 0.75%/yr | exact |
| Wipro | $47,369 → $43,270, −1.28%/yr | $45,144 → $40,763, −1.45%/yr |

**FY23–26 revenue per employee growth, per year:**

| top six | TCS | Infosys | HCLTech | LTIMindtree | Wipro | TechM |
|---|---|---|---|---|---|---|
| 3.6% | 4.2% | 5.0% | 5.0% | 3.7% | −0.1% | −0.1% |

**The 60/40 split,** checked with a simple accounting split (log points):

| window | revenue per employee | revenue | average headcount | share from fewer heads |
|---|---|---|---|---|
| FY23–26, top six | +10.3 | +6.9 | −3.4 | about 33% |
| FY19–26, top six | — | — | rose by 39 | none |

The "60% from workforce cuts" doesn't hold for FY19–26, because headcount rose. The AI share cannot be identified from these data.

### 5. Brokers vs M2 (`broker_deflation_vs_m2.csv`)

**The broker figures:**
- **Kotak** (29 Apr 2026): "3.5% pricing erosion" base case, with unit and horizon unstated.
- **HCLTech:** 3–5% a year in AI-disrupted services, equal to 2–3% of its portfolio, from FY27.
- **ICICI Securities:** 2–3% a year on traditional services (about 30% of the industry), peaking FY26–28. The $40bn figure assumes 50% deflation of the at-risk segment.
- **JPMorgan:** no numeric deflation rate in the coverage, only 2–3% growth now and 3–4% medium term.

**Our M2:**

| | AI-specific, central | range | gross |
|---|---|---|---|
| FY26 | 0.43 | 0.01–1.32 | 1.98 |
| FY27 | 1.51 | 0.41–2.67 | 3.06 |

**Why they differ:**
- Forecasts vs measured.
- Gross vs AI-specific: the usual pre-AI give-back is about 1.55 a year.
- Part of the portfolio vs all of it: ICICI's 2–3% on 30% of revenue is 0.6–0.9 pp of the portfolio.
- Price vs billed hours: fewer billed hours on time-and-materials work counts as deflation for brokers, and M2 understates it.

### 6. BoP vs survey (`bop_vs_survey.csv`)

- If the BoP software line includes ITeS, it is below the survey total in every year: −$34bn to −$39bn over FY19–23, narrowing to −$18bn in FY26.
- On that reading the level gap is a definitional mismatch. The growth gap is real.
- This is unconfirmed from RBI documents.

### Reproduced vs cited

- **Reproduced:** Baldwin's table and +27%; the computer-services version of his chart (built); ING's ratios; ING's +45% vs +32%; Unearthinsight's revenue-per-employee figures.
- **Approximately replicated:** the Economic Survey's estimate.
- **Cite only:** the 60/40 split, and the Kotak, ICICI and HCLTech deflation figures (taken from press coverage, not the notes).

### Recommended wording (output half)

> "India's IT and business-services output is still growing in dollar terms. The RBI's survey puts software exports at $221bn in FY26, up 19% since FY23 (about 6% a year). Balance-of-payments data grow about twice as fast, and those are the basis for the more upbeat external readings. The growth is concentrated outside the six largest firms, whose dollar revenue rose 7%. India is holding, not gaining, its ~30% share of world computer-services exports (excluding Ireland). Its outperformance is in business services. These are export values, not volumes or jobs: revenue per employee at the top six rose from $48.6k to $53.8k (2022Q4 to 2026Q2) while their headcount fell."

**Footnotes to attach:**
- **Baldwin's +27%:** about 15 points of it predate ChatGPT, and his series includes about $64bn of reclassified BPO and engineering exports.
- **The Economic Survey's 39.5%:** a relative difference-in-differences estimate, not export growth.
- **Broker deflation figures:** these are gross forecasts. Our measured AI-specific give-back is about 0.4% in FY26, with about 1.5% expected in FY27.

Sources: [DBnomics WTO ITS_CS_QX](https://db.nomics.world/WTO/ITS_CS_QX), [Baldwin](https://rbaldwin.substack.com/p/the-jobs-ai-was-supposed-to-eliminate), [Nunes](https://marcusnunes.substack.com/p/a-critical-look-at-the-jobs-ai-was), [Business Today/ING](https://www.businesstoday.in/jobs/story/reshaping-not-shrinking-how-indias-205-billion-tech-engine-defies-job-threats-in-ai-era-556430-2026-09-18), [Economic Survey Ch.7](https://www.indiabudget.gov.in/economicsurvey/doc/eschapter/echap07.pdf), [AIM](https://analyticsindiamag.com/it-services/indian-its-revenue-per-employee-is-rising-but-is-ai-getting-too-much-credit), [Kotak/ANI Apr](https://news.webindia123.com/news/Articles/Business/20260429/4445043.html), [Kotak/ANI Aug](https://www.newkerala.com/news/a/ai-led-deflation-weak-demand-keep-it-sector-growth-358.htm), [JPMorgan/People Matters](https://www.peoplematters.in/news/ai-and-emerging-tech/as-ai-slows-it-growth-jp-morgan-expects-tcs-and-infosys-to-outperform-wipro-hcl-tech-50585), [ICICI Securities](https://www.icicidirect.com/research/equity/finace/indian-it-sector-analysis-2026-valuation-growth-ai-risks-and-top-picks), [RBI survey FY26](https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63625).
