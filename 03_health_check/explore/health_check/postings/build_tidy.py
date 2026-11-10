"""Build tidy CSVs of India job-posting / hiring series from free downloads in raw/.

Run: python3 -I build_tidy.py   (from any directory)

Inputs (all downloaded 2026-10-15):
  raw/worldbank/sadu25b_charts/SADU-October-2025-Charts-Chapter-2.xlsx
      World Bank South Asia Development Update Oct 2025 "Jobs, AI, and Trade", chart data.
      Underlying data: Lightcast online job postings, South Asia (vast majority India),
      Aug 2020 - Mar 2025, ~28m postings. Chart archive:
      https://openknowledge.worldbank.org/bitstreams/353110f0-35bb-4b28-b003-cef1cdba8787/download
  raw/worldbank/saeu26b_charts/SAEU-October-2026-Charts-Chapter-2.xlsx
      World Bank South Asia Economic Update Oct 2026 "Adopting AI for Growth", chart data.
      https://openknowledge.worldbank.org/bitstreams/5031706e-3f27-4110-a0f9-726a88d848ef/download
  raw/linkedin/clientlib-economic-graph_2026-10-15.js
      LinkedIn Economic Graph homepage chart "Hiring Rate Indexed to Average of 2016"
      (India, UK, US; monthly from Jan 2015; series hard-coded in the page JS).
  raw/indeed/*.csv  Indeed Hiring Lab GitHub (no India series exists; US/GB comparators).

Outputs (in this folder):
  wb_lightcast_ai_share_monthly.csv    AI-skill share of postings, South Asia (mostly India)
  wb_lightcast_exposure_quartile_index.csv  posting index by AI-exposure quartile (Aug 2020 = 1)
  wb_lightcast_point_estimates.csv     country/city AI shares, DiD coefficients (by experience etc.)
  linkedin_hiring_rate_monthly.csv     LinkedIn hiring-rate index (2016 avg = 1), IN/UK/US
  indeed_comparators_monthly.csv       US/GB software-dev postings index and AI share (no India)
"""
import os
import re

import openpyxl
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
WB25 = os.path.join(RAW, "worldbank", "sadu25b_charts", "SADU-October-2025-Charts-Chapter-2.xlsx")
WB26 = os.path.join(RAW, "worldbank", "saeu26b_charts", "SAEU-October-2026-Charts-Chapter-2.xlsx")
URL25 = "https://openknowledge.worldbank.org/bitstreams/353110f0-35bb-4b28-b003-cef1cdba8787/download"
URL26 = "https://openknowledge.worldbank.org/bitstreams/5031706e-3f27-4110-a0f9-726a88d848ef/download"


def sheet_rows(path, name):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    rows = [tuple(c for c in r) for r in wb[name].iter_rows(values_only=True)]
    return [r for r in rows if any(c is not None for c in r)]


def clean(r):
    return [c for c in r if c is not None]


# ---------------------------------------------------------------- 1. AI share monthly
out = []
for r in sheet_rows(WB25, "2.8A"):
    r = clean(r)
    if len(r) == 2 and hasattr(r[0], "year"):
        out.append(dict(month=r[0].strftime("%Y-%m"), series="ai_share_all_postings", value_pct=r[1],
                        geography="South Asia (Lightcast; mostly India)", source="WB SADU Oct 2025 Fig 2.8A", source_url=URL25))
hdr = None
for r in sheet_rows(WB25, "2.8B"):
    r = clean(r)
    if r and r[0] == "Date":
        hdr = [h.split(" (")[0] for h in r[1:]]
        continue
    if hdr and r and hasattr(r[0], "year"):
        for h, v in zip(hdr, r[1:]):
            out.append(dict(month=r[0].strftime("%Y-%m"), series=f"skill_share_{h}", value_pct=v,
                            geography="South Asia (Lightcast; mostly India)", source="WB SADU Oct 2025 Fig 2.8B", source_url=URL25))
mon = {m: i + 1 for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}
for r in sheet_rows(WB26, "2.2.F"):
    r = clean(r)
    if len(r) == 2 and isinstance(r[0], str) and re.match(r"\d{4} [A-Z][a-z]{2}$", r[0]):
        y, m = r[0].split()
        out.append(dict(month=f"{y}-{mon[m]:02d}", series="ai_share_firm_postings", value_pct=r[1],
                        geography="South Asia firms (Lightcast; mostly India)", source="WB SAEU Oct 2026 Fig 2.2.F", source_url=URL26))
ai = pd.DataFrame(out)
ai["note"] = "Share of postings requiring AI-related skills. Lightcast South Asia sample is white-collar, urban and mostly Indian; not IT-only."
ai.to_csv(os.path.join(HERE, "wb_lightcast_ai_share_monthly.csv"), index=False)

# ---------------------------------------------------------------- 2. exposure quartile indices
out = []
for sh, label in [("2.9C", "AIOE quartile"), ("2.9D", "complementarity-adjusted AIOE quartile")]:
    for r in sheet_rows(WB25, sh):
        r = clean(r)
        if len(r) == 3 and isinstance(r[0], (int, float)) and hasattr(r[1], "year"):
            out.append(dict(month=r[1].strftime("%Y-%m"), grouping=label, quartile=int(r[0]), index_aug2020_eq_1=r[2],
                            source=f"WB SADU Oct 2025 Fig {sh}", source_url=URL25))
pd.DataFrame(out).to_csv(os.path.join(HERE, "wb_lightcast_exposure_quartile_index.csv"), index=False)

# ---------------------------------------------------------------- 3. point estimates
pts = []


def add(fig, item, value, unit, extra="", ci=None, src=URL25, period=""):
    pts.append(dict(figure=fig, item=item, value=value, ci95_halfwidth=ci, unit=unit, period=period, note=extra, source_url=src))


for r in sheet_rows(WB25, "2.8C"):
    r = clean(r)
    if len(r) == 2 and isinstance(r[1], (int, float)):
        add("SADU25 2.8C", f"AI share of postings: {r[0]}", r[1], "pct", period="2025 (Jan-Mar)")
for r in sheet_rows(WB25, "2.8D"):
    r = clean(r)
    if len(r) == 3 and isinstance(r[1], (int, float)):
        add("SADU25 2.8D", f"AI share of postings: {r[0]}", r[1], "pct", period="2025 (Jan-Mar)")
for r in sheet_rows(WB25, "2.9A"):
    r = clean(r)
    if len(r) == 3 and isinstance(r[1], (int, float)):
        add("SADU25 2.9A", f"Posted-wage premium: {r[0]}", r[1], "pct", ci=r[2])
for r in sheet_rows(WB25, "2.10D"):
    r = clean(r)
    if len(r) == 4 and isinstance(r[1], (int, float)):
        add("SADU25 2.10D", f"Post-ChatGPT effect of +1sd AI exposure on postings, complementarity {r[0]}", r[1],
            "pct (log pts x100)", ci=r[3], period="Dec 2022-Mar 2025 vs before")
for r in sheet_rows(WB25, "2.11B"):
    r = clean(r)
    if r and isinstance(r[-1], (int, float)):
        pass
rows = [clean(r) for r in sheet_rows(WB25, "2.11B")]
period = None
for r in rows:
    if len(r) == 3 and isinstance(r[2], (int, float)):
        period = r[0]
        add("SADU25 2.11B", f"AI-skill share of postings, {r[1]} ({period})", r[2], "pct",
            period="Nov 2022" if period == "Pre-GPT" else "Mar 2025")
    elif len(r) == 2 and isinstance(r[1], (int, float)) and period and not any(p["item"] == f"AI-skill share of postings, {r[0]} ({period})" for p in pts):
        add("SADU25 2.11B", f"AI-skill share of postings, {r[0]} ({period})", r[1], "pct",
            period="Nov 2022" if period == "Pre-GPT" else "Mar 2025")
for sh, lab in [("2.11C", "Business services vs other, post-ChatGPT"), ("2.11E", "Post-ChatGPT effect of +1sd exposure, education"),
                ("2.11F", "Post-ChatGPT effect of +1sd exposure on postings, experience band")]:
    seen = set()
    for r in sheet_rows(WB25, sh):
        r = clean(r)
        if len(r) >= 2 and isinstance(r[1], (int, float)) and r[0] not in seen:
            seen.add(r[0])
            ci = r[-1] if len(r) >= 3 else None
            add(f"SADU25 {sh}", f"{lab}: {r[0]}", r[1], "pct (log pts x100)", ci=ci, period="Dec 2022-Mar 2025 vs Aug 2020-Nov 2022")
# Annex table A2.12 (typed from PDF, SADU Oct 2025 p.55): DiD by experience band, coefficient on Post x AIOE (s.e.)
for band, b, se, outcome in [("0-5 years", -0.290, 0.058, "log postings"), ("5-10 years", -0.078, 0.048, "log postings"),
                             ("10-15 years", 0.076, 0.052, "log postings"), ("0-5 years", -0.025, 0.011, "share of postings"),
                             ("5-10 years", 0.011, 0.009, "share of postings"), ("10-15 years", 0.014, 0.005, "share of postings")]:
    add("SADU25 annex A2.12", f"DiD Post-ChatGPT x AIOE, {outcome}, experience {band}", b, "coef (s.e. in ci col)", ci=se,
        extra="ci95_halfwidth column holds the standard error for this row", period="Aug 2020-Mar 2025")
# SAEU 2026 firm-level
seen = set()
for sh in ["2.2.D", "2.2.E"]:
    for r in sheet_rows(WB26, sh):
        r = clean(r)
        if len(r) == 3 and isinstance(r[1], (int, float)) and (sh, r[0]) not in seen:
            seen.add((sh, r[0]))
            add(f"SAEU26 {sh}", f"Firm-level post-ChatGPT effect of pre-period AI exposure: {str(r[0]).replace(chr(10), ' ')}", r[1],
                "coef x IQR" if sh == "2.2.D" else "coef", ci=r[2], src=URL26, period="Jan 2020-Mar 2025")
pd.DataFrame(pts).to_csv(os.path.join(HERE, "wb_lightcast_point_estimates.csv"), index=False)

# ---------------------------------------------------------------- 4. LinkedIn hiring rate
js = open(os.path.join(RAW, "linkedin", "clientlib-economic-graph_2026-10-15.js"), encoding="utf-8").read()
rows = []
for key, label in [("india", "India"), ("uk", "United Kingdom"), ("us", "United States")]:
    m = re.search(r"key: '%s', label: '[^']+', values: \[([^\]]+)\]" % key, js)
    vals = [float(x) for x in re.findall(r"[-\d.]+", m.group(1))]
    for i, v in enumerate(vals):
        y, mo = 2015 + i // 12, i % 12 + 1
        rows.append(dict(month=f"{y}-{mo:02d}", country=label, hiring_rate_idx_2016avg_eq_1=v))
li = pd.DataFrame(rows)
assert re.search(r"START_YEAR = 2015, START_MONTH = 1", js)
li["source_url"] = "https://economicgraph.linkedin.com/ (chart 'Hiring Rate Indexed to Average of 2016', page JS, read 2026-10-15)"
li = li.sort_values(["country", "month"])
li["yoy_pct"] = li.groupby("country")["hiring_rate_idx_2016avg_eq_1"].pct_change(12) * 100
li.to_csv(os.path.join(HERE, "linkedin_hiring_rate_monthly.csv"), index=False)

# ---------------------------------------------------------------- 5. Indeed comparators (no India)
ind = []
for cc in ["US", "GB"]:
    d = pd.read_csv(os.path.join(RAW, "indeed", f"job_postings_by_sector_{cc}.csv"))
    d = d[(d["display_name"] == "Software Development") & (d["variable"] == "total postings")].copy()
    d["month"] = d["date"].str[:7]
    g = d.groupby("month")["indeed_job_postings_index"].mean().reset_index()
    for _, r in g.iterrows():
        ind.append(dict(month=r["month"], country=cc, series="software_dev_postings_idx_feb2020_eq_100", value=round(r["indeed_job_postings_index"], 2)))
a = pd.read_csv(os.path.join(RAW, "indeed", "AI_posting.csv"))
a = a[a.jobcountry.isin(["US", "GB"])].copy()
a["month"] = a["date"].str[:7]
for (m, c), v in a.groupby(["month", "jobcountry"])["AI_share_postings"].mean().items():
    ind.append(dict(month=m, country=c, series="ai_share_postings_pct", value=round(v, 3)))
ind = pd.DataFrame(ind)
ind["source_url"] = "https://github.com/hiring-lab (job_postings_tracker, ai-tracker); monthly mean of daily values"
ind.to_csv(os.path.join(HERE, "indeed_comparators_monthly.csv"), index=False)

print("ok")
