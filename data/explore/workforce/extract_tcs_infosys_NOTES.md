# TCS / Infosys workforce extract: notes

Built by `build_extract_tcs_infosys.py`, which checks the transcribed values against reported totals. `fetch_pdf.sh` sends the browser headers that infosys.com (Akamai) needs.

**Infosys (best source).** ESG Databooks FY21–26 (Annexure 4, pp.18–32) and Sustainability Reports FY16–20 (annexures) give:
- headcount by age (<=30, 31–50, >50), FY14–26
- headcount by job level (Associate/Junior = JL3 and below, Middle = JL4–5, Senior = JL6–8, Top), FY14–26
- hires and turnover by age x gender. FY16–22 are also split by region; the script sums them.

Two definition changes:
- Turnover for FY16–22 is total turnover; from FY22 it is voluntary IT-services LTM. FY22 appears both ways (87,160 vs 60,903).
- From FY23 "Senior" includes "Top". FY22–23 were restated to include Stater.

Fresher counts come from AR highlights and CEO letters. FY16–19 are "freshers trained" (a proxy). FY20 is missing.

**TCS.** No age tables in numbers, only infographics:
- GRI Sustainability Reports FY16–19 and IARs FY20–25. I read the chart labels; figures are India-only except FY16 (global).
- Grade split (%) for FY16 only. Average age for FY16–20.
- BRSR turnover by gender, FY20–26. Restated in FY24 to an IT-services basis; voluntary-only from FY26.
- Freshers: FY16, FY20 (H1 lower bound), FY22 (conflicting 100k/110k/118k), FY23, FY25, FY26.

**Not disclosed:**
- TCS: age counts, hires/turnover by age after FY17, grade split after FY16, freshers for FY17–19, FY21, FY24.
- Neither firm: median age, tenure, experience, or turnover rates by grade.
