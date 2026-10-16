"""Build CPI-Combined (base 2012=100) period averages and deflate PLFS IT earnings.

Inputs
  raw/cpi/cpi2012_YYYY.json  MoSPI CPI API, All India, Combined, General index, monthly
     https://api.mospi.gov.in/api/cpi/getCPIIndex?base_year=2012&series=Current&year=YYYY&state_code=99&sector_code=3&group_code=0&Format=JSON&limit=100
  ../../round3/plfs/earnings_regular_salaried.csv  (repo aggregate, nominal INR/month, CWS regular wage workers)

Outputs
  cpi_combined_monthly.csv, cpi_combined_period_avg.csv, plfs_it_real_earnings.csv

Run: python3 -I build_cpi_real_earnings.py  (from any directory)
"""
import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw" / "cpi"
EARN = HERE.parents[1] / "round3" / "plfs" / "earnings_regular_salaried.csv"
API = ("https://api.mospi.gov.in/api/cpi/getCPIIndex?base_year=2012&series=Current&year={y}"
       "&state_code=99&sector_code=3&group_code=0&Format=JSON&limit=100")
MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July",
                                      "August", "September", "October", "November", "December"], 1)}

rows = []
for f in sorted(RAW.glob("cpi2012_*.json")):
    d = json.loads(f.read_text())
    for r in d["data"]:
        rows.append({"year": int(r["year"]), "month": MONTHS[r["month"]], "cpi_combined_2012": float(r["index"]),
                     "yoy_inflation_pct": float(r["inflation"]) if r["inflation"] not in (None, "") else None, "status": r["status"],
                     "source_url": API.format(y=r["year"])})
m = pd.DataFrame(rows).sort_values(["year", "month"]).reset_index(drop=True)
m["date"] = pd.to_datetime(dict(year=m.year, month=m.month, day=1))
assert m.groupby("year").size().eq(12).all(), m.groupby("year").size()
m[["date", "year", "month", "cpi_combined_2012", "yoy_inflation_pct", "status", "source_url"]].to_csv(
    HERE / "cpi_combined_monthly.csv", index=False)


def avg(start, end):
    s = m[(m.date >= start) & (m.date <= end)]
    assert len(s) == 12, (start, end, len(s))
    return s.cpi_combined_2012.mean()


periods = []
for y in range(2016, 2025):  # Indian FY Apr-Mar (FY ending y+1), needs Mar of y+1
    if y + 1 <= 2025:
        periods.append(("FY", f"{y}-{str(y+1)[2:]}", f"{y}-04-01", f"{y+1}-03-01"))
for y in range(2016, 2025):  # PLFS rounds Jul-Jun
    if y + 1 <= 2025:
        periods.append(("PLFS_JulJun", f"{y}-{str(y+1)[2:]}", f"{y}-07-01", f"{y+1}-06-01"))
for y in range(2016, 2026):
    periods.append(("CY", f"cy{y}", f"{y}-01-01", f"{y}-12-01"))
p = pd.DataFrame([{"period_type": t, "period": lab, "start": s, "end": e, "cpi_avg": round(avg(s, e), 3)}
                  for t, lab, s, e in periods])
p["source"] = "MoSPI CPI-Combined All India General index (base 2012=100), monthly average; api.mospi.gov.in"
p.to_csv(HERE / "cpi_combined_period_avg.csv", index=False)

# ---- deflate PLFS earnings: rounds 2017-18..2023-24 are Jul-Jun; cy2024, cy2025 calendar years
lookup = {}
for _, r in p.iterrows():
    if r.period_type == "PLFS_JulJun":
        lookup[r.period] = r.cpi_avg
    if r.period_type == "CY":
        lookup[r.period] = r.cpi_avg
e = pd.read_csv(EARN)
e["cpi_period_avg"] = e["round"].map(lookup)
assert e.cpi_period_avg.notna().all(), e.loc[e.cpi_period_avg.isna(), "round"].unique()
base = lookup["cy2025"]
e["deflator_to_cy2025"] = base / e.cpi_period_avg
for c in ["mean_inr", "median_inr", "p25_inr", "p75_inr", "mean_se"]:
    e[c.replace("_inr", "").replace("mean_se", "mean_se") + "_real_cy2025_inr"] = (e[c] * e.deflator_to_cy2025).round(0)
e["cpi_basis"] = ("CPI-Combined base 2012; Jul-Jun average for 2017-18..2023-24 rounds, "
                  "Jan-Dec average for cy2024/cy2025; expressed in CY2025 prices")
e["source_nominal"] = ("data/explore/round3/plfs/earnings_regular_salaried.csv (PLFS unit data aggregated in repo; "
                       "CWS regular wage workers, earnings >0, previous month, INR)")
e["source_cpi"] = "https://api.mospi.gov.in/api/cpi/getCPIIndex (base_year=2012, All India, Combined, General)"
e.to_csv(HERE / "plfs_it_real_earnings.csv", index=False)

# summary
w = e.pivot_table(index="round", columns=["sample", "age_band"], values="median_real_cy2025_inr")
order = [f"{y}-{str(y+1)[2:]}" for y in range(2017, 2024)] + ["cy2024", "cy2025"]
print(w.reindex(order).round(0).to_string())
w2 = e.pivot_table(index="round", columns=["sample", "age_band"], values="mean_real_cy2025_inr")
print(w2.reindex(order).round(0).to_string())
print(p.to_string())
