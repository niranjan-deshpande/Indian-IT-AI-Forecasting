# FINDINGS.md

# Free job-posting data for India: what exists and what we collected

Collected 2026-10-15. Files are in `data/explore/health_check/postings/`; raw downloads are in `raw/` (46 MB, most of it the Indeed US/UK sector files). Scripts run with `python3 -I`:
- `build_tidy.py` builds the World Bank, LinkedIn and Indeed files.
- `scrape_revelio_company_pages.py` builds the Revelio files.
- `tidy_press.py` builds the press file.

**Bottom line:**
- No free source gives a downloadable India IT postings series by experience band. Naukri JobSpeak is still the core series.
- **Best new source:** the World Bank chart workbooks of Lightcast South Asia postings (mostly India), Aug 2020 to Mar 2025. They give:
  - the monthly AI-skill share of postings;
  - posting indices by AI-exposure quartile;
  - post-ChatGPT effects by experience band.
- **LinkedIn's India hiring rate** gives an independent hires series, Jan 2015 to May 2026.
- **Indeed and LinkedIn India numbers** exist only as text in blogs and press releases, alongside Xpheno and foundit.

## 1. Availability by source

| Source | Free? | India? | IT split? | Experience band? | Span | How to get it | Status |
|--|--|--|--|--|--|--|--|
| Lightcast via World Bank South Asia Development Update, Oct 2025 ("Jobs, AI, and Trade") | Chart xlsx free; microdata licensed | South Asia, "vast majority" India; India and city cuts for 2025 | No IT series. AI-exposure quartiles; "business services" (BPO/IT/software occupations) only as effect estimates | Yes: 0–5, 5–10, 10–15 years, as effect estimates only (no levels) | Monthly, Aug 2020 – Mar 2025; about 28m postings | Chart archive: https://openknowledge.worldbank.org/bitstreams/353110f0-35bb-4b28-b003-cef1cdba8787/download | Collected |
| Lightcast via World Bank South Asia Economic Update, Oct 2026 ("Adopting AI for Growth") | Chart xlsx free | South Asian firms: 435k firms, 25m postings | No | No | Monthly AI share, Nov 2020 – Mar 2025; firm-level effects | https://openknowledge.worldbank.org/bitstreams/5031706e-3f27-4110-a0f9-726a88d848ef/download | Collected. Same data window, no new months |
| Lightcast directly, OECD.AI, Stanford AI Index, Our World in Data | Partly | **No.** 14 to 22 rich countries | – | – | Annual | Our World in Data CSV saved in `raw/owid/` as proof of coverage | India not covered |
| LinkedIn Economic Graph hiring rate | Yes, series embedded in the page script | Yes; all industries | No | No | Monthly, Jan 2015 – May 2026 | `raw/linkedin/*.js` | Collected. Measures hires, not postings |
| LinkedIn on OECD.AI, Grad's Guide, AI Labour Market Report | Charts and press only | Yes; LinkedIn reaches under 40% of India's workforce | AI roles | Entry level in press, definition unclear | – | – | Press points |
| Indeed Hiring Lab GitHub | Yes | **No.** AU, CA, DE, FR, GB, IE, IT, NL, US | Yes (software development) | No | Daily, 2020–Oct 2026 | `raw/indeed/` | US/UK comparators only |
| Indeed "IN Labour Market Update" blog | Text and PNG charts; data.indeed.com is blocked by Cloudflare | Yes | Yes (software development, IT occupations, AI share) | No | Monthly posts, 2025–26 | hiringlab.indeed.com/au/blog | Press points |
| Revelio Public Labor Statistics and blog charts | Yes / PNG only | No: US-only, or India as an unlabelled line | – | – | – | – | Not usable |
| Revelio free company pages | Yes (HTML) | Firm level; South Asia share of headcount | No | No | Postings annual 2023–26 (2026 = Q1 only); headcount quarterly | Scraper script | Collected; noisy |
| Adzuna (adzuna.in) | API needs a free key, and I can't register one for you | Yes | Yes ("IT Jobs") | No | Live counts plus history | developer.adzuna.com | Not collected |
| Naukri JobSpeak (already held) | Yes | Yes | Yes (IT-Software) | Yes, but all industries | Jan 2021 – Aug 2026 | `workforce/jobspeak_*.csv` | Core series |
| Xpheno Active Tech Jobs; foundit Insights Tracker | Press only | Yes | Yes (Xpheno: IT services vs GCC) | Xpheno entry level; foundit 0–3 years | Monthly | Press | Press points |
| Mendeley "India Tech Career Intelligence [1M]" | CC BY | Claims India | Tech | ? | ? | – | Skipped: exactly 1.0m rows, no sources or dates, probably synthetic |

## 2. What we collected

| File | Content |
|--|--|
| `wb_lightcast_ai_share_monthly.csv` | AI-skill share of postings (Fig 2.8A); by skill (AI, ML, neural networks, NLP, GenAI; Fig 2.8B); firm-level share (Oct 2026 report, Fig 2.2.F) |
| `wb_lightcast_exposure_quartile_index.csv` | Posting index (Aug 2020 = 1) by AI-exposure quartile and complementarity-adjusted quartile (Figs 2.9C/D) |
| `wb_lightcast_point_estimates.csv` | AI share by country and Indian city; wage premia; post-ChatGPT effects by complementarity, education and **experience**; business services; annex table A2.12; firm-level effects (Oct 2026) |
| `linkedin_hiring_rate_monthly.csv` | Hiring-rate index (2016 = 1) for India, UK and US, with year-on-year % |
| `indeed_comparators_monthly.csv` | US/UK software-development postings index (Feb 2020 = 100); AI share of postings |
| `revelio_firm_postings.csv`, `revelio_firm_headcount_q.csv`, `revelio_firm_region_share.csv` | 13 IT-services firms |
| `press_datapoints.csv` | 260 points: Xpheno (15 series), foundit (16), Indeed India (17), LinkedIn (6). Each has a URL and quote; all flagged `reproducible=False` |

## 3. Headline numbers

**Lightcast via the World Bank (South Asia, mostly India; white-collar; not IT-only)**
- **AI-skill share of postings:** 2.65% in Dec 2022, rising to 6.51% in Mar 2025. GenAI went from 0.02% to 0.68%.
- **AI share by place, 2025:** India 5.8%; Bangalore 11.0%, Hyderabad 9.6%, Pune 7.0%.
- **Business services:** AI share rose from 5.8% to 11.8%. Postings fell 35% (±11) relative to other occupations after ChatGPT, and posted wages fell 8% (±4).
- **Posting index, Nov 2022 → Mar 2025:**
  - Most AI-exposed quartile (includes software developers): 2.45 → 1.53 (−37%).
  - Least-exposed quartile: 2.56 → 2.81 (+10%).
- **By experience (+1 sd of AI exposure, after ChatGPT):**
  - 0–5 years: −11.9% (±4.7).
  - 5–10 years: −3.2% (±3.9).
  - 10–15 years: +3.1% (±4.1).
  - Annex A2.12: coefficient −0.290 (s.e. 0.058) for 0–5 years. The share of postings asking for 0–5 years falls 2.5 percentage points.

**LinkedIn India hiring rate (annual mean, 2016 = 1)**
- 2.40 (2021), **2.64 (2022)**, 2.09 (2023), 1.97 (2024), 1.91 (2025), **1.79 (Jan–May 2026)**.
- That is −32% against 2022. Year-on-year change was negative in 11 of the last 12 months (May 2026: −6.3%).
- Press figures for Q2 2026: entry-level hiring −12.5% year on year against −10.5% overall. Entry-level AI-engineer hiring +55%.

**Xpheno active tech openings (press)**
- **Total:** 133k (Jan 2023), 136k (Jan 2025), 102k (Nov 2025), 93k (Jun 2026, the low), 120k (Oct 2026, +15–17% year on year).
- **IT services:** 52k (Jun 2025), 36k (Jun 2026, −31% year on year), 66k (Oct 2026, +57%).
- **GCCs:** 11–19k, up 64% year on year by Oct 2026.
- **Entry level:** 13–15k throughout, about 12% of openings. Year-on-year change was −18% to −19% for most of H1 2026, −44% in Jun 2026, and +15% in Oct 2026.

**foundit (press)**
- **IT/software-services industry:** −4% to −11% year on year, Mar–Aug 2026.
- **IT function:** +55% year on year in Feb 2026, slowing to +5% by Aug.
- **Entry level (0–3 years):** −2% in Mar 2026, falling to −10% in Jul.
- **IT's share of fresher postings:** 22% (Jul 2026).

**Indeed India (press and blog)**
- **All postings:** +60% to +84% above pre-pandemic levels, but 16–25% below the Jan 2023 peak in 2025. Year-on-year change: −20% (Oct 2025), +8.3% (Jul 2026).
- **Software development:** −18% over three months to Jul 2026.
- **AI mentions:** 8.2% → 11.7% of all postings (Sep 2024 → Sep 2025); 22.8% of software-development postings.

**Revelio (global, firm level)**
- New postings per month for TCS, Infosys, Wipro, HCLTech and TechM combined: 16.7k, 19.5k, 16.7k, 17.6k (2023 to Q1 2026).
- There is no trend, and individual firms swing wildly. Not a hiring measure.

## 4. Comparison with JobSpeak (annual mean, 2022 = 1.00)

| Year | JobSpeak IT | JobSpeak 0–3 yrs (all industries) | JobSpeak 16+ yrs | LinkedIn India | Lightcast, most-exposed quartile | Indeed US software | Indeed UK software |
|--|--|--|--|--|--|--|--|
| 2021 | 0.93 | 0.87 | 0.82 | 0.91 | 0.98 | 0.76 | 0.77 |
| 2023 | 0.72 | 0.91 | 1.27 | 0.79 | 1.33 | 0.46 | 0.57 |
| 2024 | 0.70 | 0.88 | 1.51 | 0.75 | 0.93 | 0.36 | 0.39 |
| 2025 | 0.70 | – | – | 0.72 | 0.70 (Q1) | 0.33 | 0.36 |
| 2026 | 0.72 | – | – | 0.68 | – | 0.38 | 0.39 |

- **JobSpeak and LinkedIn agree closely:** about −30% since 2022, flat to drifting down.
- **The US and UK fell about twice as far.**
- **The Lightcast quartile index peaks in 2023** because Lightcast's coverage was growing then. Only the gap between quartiles is informative.
- **Xpheno and JobSpeak** both show a 2026 H2 upturn (JobSpeak IT +10% year on year in Aug; Xpheno +15% in Sep–Oct).
- **foundit shows weakness** in IT-software industry postings over the same months.

## 5. Caveats
- **Postings are not hires.** Big IT firms hire freshers through campus drives and their own portals, which no posting source sees.
- **Lightcast South Asia is skewed:** 51% professionals and 22% managers, against 6% and 3% in labour-force surveys. Its coverage changes over time. There are gaps in Apr–May 2023 and Feb 2024. It is not IT-only, and no India-only time series was published. The effect estimates are relative (exposed vs less-exposed occupations, one break in Nov 2022) and end in Mar 2025.
- **LinkedIn:** coverage is under 40% of India's workforce and skews urban and tech. The homepage series stops at May 2026.
- **Revelio:** profile-based. TCS headcount is about 2.5 times the reported figure, and postings jump erratically.
- **Press series:** definitions differ (Xpheno counts open roles at a point in time; foundit is an index). Numbers are rounded and sometimes revised. Duplicate months were kept from the earliest article.

## 6. Three candidate charts
1. **"India's tech postings fell by a third; the US and UK by two-thirds."** Index with 2022 = 100: JobSpeak `idx_it_software`, LinkedIn India, and Indeed US/UK software development (`indeed_comparators_monthly.csv`).
2. **"Entry-level postings took the AI hit; senior postings didn't."** Dot-and-whisker chart from `wb_lightcast_point_estimates.csv` (figure `SADU25 2.11F`, with 2.11E alongside). Label it as Lightcast South Asia, 2020–25, relative to less-exposed occupations.
3. **"AI skills doubled their share of postings after ChatGPT."** Line chart of `wb_lightcast_ai_share_monthly.csv` (`ai_share_all_postings`, with GenAI on a second axis), marked at Nov 2022. Alternative: Xpheno IT-services vs GCC vs entry-level openings, 2025–26, from `press_datapoints.csv`, labelled as press-sourced.
