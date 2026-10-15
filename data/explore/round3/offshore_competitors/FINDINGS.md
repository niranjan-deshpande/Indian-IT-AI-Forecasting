# FINDINGS — S4d: did IT-services work leave India after 2023?

*Saved by the orchestrator from the subagent's report; subagents cannot write report files. Date: 2026-10-14. Builds on `data/explore/trade/FINDINGS.md`. CSVs and scripts in this folder were written by the subagent.*

## 1. Headline
- **No sign of work leaving India after 2023.**
  - India's share of US computer-services imports (BEA) was 24.4% (2022), 23.9%, 25.0% and 25.1% (2025).
  - Its share of world computer-services exports (IMF BOP, balanced panel of 84 reporters) went from 20.4% (2022) to 19.5% (2025); excluding Ireland, from 29.3% to 30.1%.
  - Against 30 emerging delivery countries (balanced 2015–25), India's share was 65.9% (2022) and 65.2% (2025).
  - In H1 (25 countries), India's share was 66.8% (2022) and 66.6% (2026). India and the others both grew about 11–13% a year.
- **Competitors grow fast but from a small base.**
  - India added $5.3bn of US computer imports in 2022–25; 15 low-cost locations together added $1.3bn ($2.6bn → $3.9bn).
  - India's share of EU imports from outside the EU eased from 10.0% to 9.4% (2022–24), because the US and UK grew faster.
  - Among partners other than the US, UK and Switzerland, India rose from 30.3% to 31.2%.
- **No onshoring.** US NAICS 5415 employment (BLS CES, Jan–Sep averages) changed +1.2% in 2023, then −1.3%, −1.5% and −1.6% in 2024–26.
- **Non-Indian vendors didn't move delivery.**
  - Cognizant's India share of headcount was 72.6%, 72.8%, 73.1%, 71.7% and 73.1% (2021–25).
  - India accounted for 15,400 of Cognizant's 14,800 net additions in 2025.
  - Accenture's 10-Ks for FY23–25 say India and the Philippines are its "largest and second largest" locations; they give no counts.
- **Surprises.**
  - India's share of US computer imports fell from 46.6% to 24.4% over 2015–22, before AI. The affiliated share of US computer imports fell from 85% to 66%, and Canada, Ireland and the UK rose.
  - Over 2019–22, BEA's India series fell while India's own balance-of-payments exports rose about 55%. BEA levels are a poor guide.
  - US other-business-services (BPO) imports from the Philippines fell from $4.5bn to $3.8bn over 2022–25, and Mexico and Costa Rica also fell. India rose from $14.4bn to $20.4bn.
- **Verdict.**
  - S4d is largely ruled out in aggregate for 2023 to H1 2026.
  - That India's value share didn't fall also mildly argues against an India-specific S3.
  - Caveat: these are values, not jobs. If only junior work moved abroad, it would not show up here.

## 2. Sources

| name | publisher | what it measures | unit / disaggregation | period & frequency | lag | access | confirmed? | URL |
|--|--|--|--|--|--|--|--|--|
| International services, Table 2.3 | BEA (official) | US imports by partner × service type; affiliation only for all countries combined | $m; ~90 areas; many (D) suppressions, including the Philippines | 1999–2025, annual | ~6 months | free, no key | **CONFIRMED** (all areas pulled) | https://apps.bea.gov/iTable/?reqid=62&step=7&isuri=1&product=4&tablelist=30583 |
| IMF BOP, SI2 and SJ credits | IMF (national compilers) | each country's computer and other-business-services exports | USD; 146 annual reporters. No SI2 for the UK, China, Canada, Vietnam, Chile, Thailand, Switzerland, Spain or Sweden | 2012–2025 annual; quarterly to 2026Q2 (57 reporters) | ~1 quarter | free SDMX | **CONFIRMED** | https://api.imf.org/external/sdmx/2.1/data/IMF.STA,BOP/.CD_T.SI2+SJ+S.USD.A+Q?startPeriod=2012 |
| bop_its6_det | Eurostat (official) | EU27 computer imports by partner | €m; limited partner list | 2010–2024, annual | ~16 months | free API | **CONFIRMED** | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/bop_its6_det |
| Cognizant 10-K, Workforce section | SEC filing | headcount: India, North America, Continental Europe, UK, rest of world | persons | FY21–FY25 | ~6 weeks | free | **CONFIRMED** | https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001058290&type=10-K |
| Accenture 10-K | SEC filing | qualitative location wording only | — | FY23–FY25 (FY26 not yet filed) | — | free | **CONFIRMED** (no number) | https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001467373&type=10-K |
| CES6054150001, CES6054000001 | BLS (official) | US employment: computer systems design; professional and technical services | thousands, seasonally adjusted | monthly to Sep 2026 (preliminary) | ~1 month | free API | **CONFIRMED** | https://api.bls.gov/publicAPI/v1/timeseries/data/ |
| ABSL Poland 2025 | **industry body** | business-service-centre jobs: 488.7k at Q1 2025, +6.2% | survey; method not stated | annual | ~3 months | free | **CONFIRMED** (news page; PDF not read) | https://absl.pl/en/news/p/absl-report-polands-business-services-sector-grows-value-and-strategic-importance |
| IBPAP | **industry body** | Philippines IT-BPM: $40bn+ (+5%), 1.9m jobs (+4%) in 2025 | opaque | annual | — | press only | **NOT CONFIRMED** (secondary) | https://www.philstar.com/business/2026/01/29/2504140/it-bpm-revenues-breach-40-billion-mark/amp/ |
| UK trade in services by partner country | ONS (official, in development) | UK imports by service type × partner | £m, quarterly | to at least 2024Q2 | ~4 months | free xlsx | **NOT CONFIRMED** (release pages seen in search) | https://www.ons.gov.uk/releases/uktradeinservicesbypartnercountryapriltojune2024 |
| WTO–OECD BaTIS / UNCTADstat; PSA; central banks of Poland, Romania, Mexico, Vietnam, Egypt | various | bilateral and world matrices; national balance of payments | — | — | — | free | **NOT CHECKED** (the IMF pull covers most of these countries, but not Vietnam or Chile) | — |

## 3. What each source tells us
- **IMF India share (the best metric).**
  - A fall in India's share after 2023 would support S4d; a flat or rising share undermines it. Result: flat.
  - S1: India's level kept growing about 12% a year, which undermines S1 for India as a delivery location.
  - S3: weak evidence against, since repricing could be industry-wide.
  - Caveats:
    - USD valuation (a strong euro and zloty in 2025 flatter CEE countries);
    - India's figure includes GCCs and on-site billing;
    - possible compilation jump in 2022.
- **BEA by partner.**
  - Tests where US clients buy from. India's share has been stable since 2022; the 2015–22 fall reflects booking through affiliates in Canada, Ireland and the UK.
  - Coverage of India is only about 13% of RBI-reported software exports to the US, and competitor cells are suppressed.
- **Eurostat.** India's share eased mildly, as US/UK suppliers grew faster. The data end in 2024; recheck with the 2025 release (around spring 2027).
- **Cognizant.** A firm-level S4d test: no shift. One firm only, and "rest of world" is lumped together (28,300 → 30,700).
- **BLS 5415.** Onshoring would mean US jobs rising; they fell, which points to a shock common to both countries.
- **ABSL and IBPAP.** Context only: moderate growth, no surge.

## 4. Numbers

| metric | 2015 | 2019 | 2022 | 2023 | 2024 | 2025 | file |
|--|--|--|--|--|--|--|--|
| India share of US computer-services imports, % | 46.6 | 37.6 | 24.4 | 23.9 | 25.0 | 25.1 | `india_share_summary.csv` |
| same, excluding Ireland and Canada, % | 58.6 | 56.3 | 38.6 | 39.3 | 39.7 | 38.2 | `india_share_summary.csv` |
| US computer imports from India, $bn | 13.7 | 15.6 | 12.7 | 13.6 | 15.9 | 18.0 | `bea_us_computer_imports_by_country.csv` |
| US computer imports from 15 low-cost locations, $bn | 1.4 | 2.2 | 2.6 | 3.0 | 3.5 | 3.9 | `bea_us_computer_imports_by_country.csv` |
| US other-business-services imports from the Philippines, $bn | 1.1 | 1.6 | 4.5 | 4.4 | 4.1 | 3.8 | `bea_us_computer_imports_by_country.csv` |
| India share of world computer exports, % (n=84) | 27.3 | 19.6 | 20.4 | 20.2 | 19.8 | 19.5 | `india_share_summary.csv` |
| same, excluding Ireland, % | 34.6 | 27.8 | 29.3 | 29.5 | 29.9 | 30.1 | `india_share_summary.csv` |
| India share of delivery group, % (n=30) | 75.2 | 66.6 | 65.9 | 65.4 | 65.4 | 65.2 | `india_share_summary.csv` |
| India computer exports, $bn | 74.1 | 91.3 | 141.1 | 157.3 | 175.3 | 197.3 | `imf_computer_exports_by_country.csv` |
| India share of EU imports from outside the EU, % | (outlier) | 7.5 | 10.0 | 9.6 | 9.4 | — | `eurostat_india_share.csv` |
| Cognizant India share of headcount, % | — | — | 72.8 | 73.1 | 71.7 | 73.1 | `cognizant_headcount_by_location.csv` |
| US 5415 employment, Jan–Sep average, thousands (2026: 2,368) | 1,904 | 2,188 | 2,444 | 2,475 | 2,442 | 2,406 | `bls_ces_monthly.csv` |

**India vs 24 other delivery countries, H1 (Jan–Jun)** (`imf_h1_india_vs_delivery_group.csv`)

| | 2023 | 2024 | 2025 | 2026 |
|--|--|--|--|--|
| India's share | 67.0% | 66.5% | 66.6% | 66.6% |
| India y/y growth | +13.9% | +8.9% | +12.9% | +11.1% |
| others' y/y growth | +12.7% | +11.4% | +12.7% | +11.1% |

**Computer-export growth, 2022–25 CAGR**

| country | CAGR |
|--|--|
| India | 11.8% |
| Poland | 18.3% |
| Romania | 11.5% |
| Philippines | 10.1% |
| Brazil | 19.3% |
| Serbia | 22.6% |
| Colombia | 15.8% |
| Ukraine | −3.2% |
| Sri Lanka | −9.1% |

## 5. Not checked
- **Missing countries:** Vietnam, China, the UK and Chile have no SI2 data in the IMF pull.
- **Not pulled:** the ONS file, BaTIS/UNCTAD, and the Philippine PSA and central-bank data.
- **Not read or not used:** the ABSL report's methodology; Accenture's India headcount (third-party estimates exist but weren't used).
- **Not checked:** the Indian firms' own nearshore hubs.
- **Jobs vs value:** none of these sources show jobs, so a shift of only junior work abroad would be invisible.

## Files
- **CSVs:**
  - `india_share_summary.csv`
  - `bea_us_computer_imports_by_country.csv`
  - `imf_computer_exports_by_country.csv`
  - `imf_h1_india_vs_delivery_group.csv`
  - `eurostat_eu27_computer_imports_by_partner.csv`
  - `eurostat_india_share.csv`
  - `cognizant_headcount_by_location.csv`
  - `bls_ces_monthly.csv`
- **Scripts:**
  - `fetch_bea_by_country.py`
  - `fetch_imf_world.py`
  - `fetch_eurostat.py`
  - `analyze.py`
  - `analyze_quarterly.py`
  - `build_eurostat.py`
  - `build_bls_filings.py`
- **raw/:** 11 MB of downloads, including the 10-K text files.
