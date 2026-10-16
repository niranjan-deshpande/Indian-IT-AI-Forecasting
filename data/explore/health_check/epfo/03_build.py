"""Build "best available" EPFO series from the vintage files written by 02_parse.py.

Run:  python3 -I 03_build.py

Rules
- Monthly values: for each month, take the LATEST vintage (release) that prints that month. EPFO reports
  print monthly rows only for the current financial year, so a month's last print is normally the May
  release after its FY closes (e.g. Apr-2022..Mar-2023 from the 20 May 2023 release). Exception: the
  Mar/Apr/May 2024 releases printed only one month, so Jan/Feb/Mar 2024 are first prints and Dec 2023
  comes from the 20 Feb 2024 release.
- FY totals: latest vintage (20 Aug 2025 release). The page-1 table misprints FY2019-20 age 22-25
  (repeats the FY2018-19 value 1,771,707); the age x component table (col d) gives 2,196,926, which
  makes the row add up to the printed total, so FY values are taken from the component table.
- July 2025 (released 23 Sep 2025, the last release before EPFO stopped publishing): the full report
  is not archived; headline numbers come from the PIB press release text.

Outputs
  epfo_monthly_age_best.csv      month x age band: net payroll, new subscribers, exits, rejoins
  epfo_fy_age_best.csv           FY x age band, same measures (FY2025-26 = Apr-Jun only, flagged)
  epfo_industry_age_best.csv     top-10 industries x age band x FY (latest vintage) and x month (last print)
  epfo_it_age_best.csv           the "computers" industry only, wide by age band, FY and monthly
  epfo_revisions.csv             first print vs last print of each month (total, 18-21, 22-25)
"""
import csv
import collections
from pathlib import Path

HERE = Path(__file__).resolve().parent
AGES = ["<18", "18-21", "22-25", "26-28", "29-35", ">35", "Total"]
IT = "ESTABLISHMENT ENGAGED IN MANUFACTURE, MARKETING SERVICING, USAGE OF COMPUTERS"
LATEST = "2025-08-20"
PIB_JUL25 = "https://www.pib.gov.in/PressReleasePage.aspx?PRID=2169975"


def read(name):
    with open(HERE / name) as f:
        return list(csv.DictReader(f))


def write(name, rows, keys=None):
    keys = keys or list(rows[0].keys())
    with open(HERE / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


def fy_of(month):
    y, m = map(int, month.split("-"))
    s = y if m >= 4 else y - 1
    return f"FY{s}-{str(s + 1)[2:]}"


age = read("epfo_age_net_payroll_vintages.csv")
comp = read("epfo_age_components_vintages.csv")
ind = read("epfo_industry_age_vintages.csv")

# ---------- monthly by age ----------
last = {}   # (month) -> vintage
first = {}
for r in age:
    if r["period_type"] != "month":
        continue
    p, v = r["period"], r["vintage_release_date"]
    if p not in last or v > last[p]:
        last[p] = v
    if p not in first or v < first[p]:
        first[p] = v

age_idx = {(r["vintage_release_date"], r["period"], r["age_band"]): r for r in age}
comp_idx = {(r["vintage_release_date"], r["period"], r["age_band"]): r
            for r in comp if r["table"] == "net_payroll"}
comp_nn = {(r["vintage_release_date"], r["period"], r["age_band"]): r
           for r in comp if r["table"] == "net_new_subscribers"}

monthly = []
for p in sorted(last):
    v = last[p]
    for a in AGES:
        r = age_idx[(v, p, a)]
        c = comp_idx.get((v, p, a), {})
        nn = comp_nn.get((v, p, a), {})
        monthly.append({
            "month": p, "fy": fy_of(p), "age_band": a,
            "net_payroll": r["net_payroll"],
            "new_subscribers": c.get("a_new", ""), "exited": c.get("b_exited", ""),
            "rejoined": c.get("c_rejoined", ""),
            "net_new_subscribers": nn.get("d_net", ""),
            "estab_first_ecr": r["estab_first_ecr"] if a == "Total" else "",
            "vintage_release_date": v, "first_print_release_date": first[p],
            "is_first_print": int(v == first[p]),
            "source": "EPFO Net Payroll Data report", "source_file": r["source_file"],
            "source_url": r["source_url"], "archive_url": r["archive_url"]})
# July 2025 headline (PIB) -- the 20 Sep 2025 report itself is not retrievable
for a, net, new in [("Total", 2104000, 979000), ("18-25", 913000, 598000)]:
    monthly.append({
        "month": "2025-07", "fy": "FY2025-26", "age_band": a, "net_payroll": net,
        "new_subscribers": new, "exited": "", "rejoined": "1643000" if a == "Total" else "",
        "net_new_subscribers": "", "estab_first_ecr": "",
        "vintage_release_date": "2025-09-23", "first_print_release_date": "2025-09-23",
        "is_first_print": 1, "source": "PIB press release (rounded lakh figures)",
        "source_file": "", "source_url": PIB_JUL25, "archive_url": ""})
write("epfo_monthly_age_best.csv", monthly)

# ---------- FY by age (latest vintage, component table) ----------
fy_rows = []
for (v, p, a), c in sorted(comp_idx.items()):
    if v != LATEST:
        continue
    nn = comp_nn.get((v, p, a), {})
    page1 = age_idx.get((v, p, a), {})
    is_fy = p.startswith("FY")
    fy_rows.append({
        "period": p if is_fy else p, "period_type": "FY" if is_fy else "month",
        "age_band": a, "net_payroll": c["d_net"], "new_subscribers": c["a_new"],
        "exited": c["b_exited"], "rejoined": c["c_rejoined"],
        "net_new_subscribers": nn.get("d_net", ""),
        "page1_net_payroll": page1.get("net_payroll", ""),
        "note": ("FY2017-18 covers Sep-2017 to Mar-2018 only" if p == "FY2017-18" else
                 "page-1 table misprints this cell (1771707)" if (p == "FY2019-20" and a == "22-25")
                 else ""),
        "vintage_release_date": v, "source_file": c["source_file"],
        "source_url": c["source_url"], "archive_url": c["archive_url"]})
# FY2025-26 partial (Apr-Jun) as a sum of months
part = collections.defaultdict(lambda: collections.Counter())
for c in comp_idx.values():
    if c["vintage_release_date"] == LATEST and c["period"].startswith("2025-"):
        for k in ("a_new", "b_exited", "c_rejoined", "d_net"):
            part[c["age_band"]][k] += int(c[k])
src = next(c for c in comp_idx.values() if c["vintage_release_date"] == LATEST)
for a in AGES:
    fy_rows.append({
        "period": "FY2025-26 (Apr-Jun)", "period_type": "FY_partial", "age_band": a,
        "net_payroll": part[a]["d_net"], "new_subscribers": part[a]["a_new"],
        "exited": part[a]["b_exited"], "rejoined": part[a]["c_rejoined"],
        "net_new_subscribers": "", "page1_net_payroll": "",
        "note": "sum of Apr-Jun 2025; first or second prints", "vintage_release_date": LATEST,
        "source_file": src["source_file"], "source_url": src["source_url"],
        "archive_url": src["archive_url"]})
fy_rows = [r for r in fy_rows if r["period_type"] != "month"]
write("epfo_fy_age_best.csv", fy_rows)

# ---------- industry x age ----------
ind_last = {}
for r in ind:
    if r["period_type"] != "month" or r["age_band"] == "All":
        continue
    p, v = r["period"], r["vintage_release_date"]
    if p not in ind_last or v > ind_last[p]:
        ind_last[p] = v
ind_best = []
for r in ind:
    keep = ((r["period_type"] == "FY" and r["vintage_release_date"] == LATEST) or
            (r["period_type"] == "month" and ind_last.get(r["period"]) == r["vintage_release_date"]))
    if keep:
        ind_best.append({k: r[k] for k in ("period", "period_type", "age_band", "industry",
                                            "net_payroll", "vintage_release_date", "source_file",
                                            "source_url", "archive_url")})
ind_best.sort(key=lambda r: (r["period_type"], r["period"], r["age_band"], r["industry"]))
write("epfo_industry_age_best.csv", ind_best)

# IT ("computers") wide by age; blank = not in that band's top 10 that period
tot_idx = {(r["period"], r["age_band"]): r for r in ind_best if r["industry"].startswith("Grand Total")}
it = collections.defaultdict(dict)
meta = {}
for r in ind_best:
    if r["industry"] == IT:
        it[(r["period_type"], r["period"])][r["age_band"]] = int(r["net_payroll"])
        meta[(r["period_type"], r["period"])] = r
# also the all-industry totals by age for the same period (page-1 / component tables)
allind = {}
for r in fy_rows:
    allind[(r["period"], r["age_band"])] = int(r["net_payroll"])
for r in monthly:
    if r["source"].startswith("EPFO"):
        allind[(r["month"], r["age_band"])] = int(r["net_payroll"])
it_rows = []
for (pt, p), d in sorted(it.items()):
    m = meta[(pt, p)]
    row = {"period": p, "period_type": pt}
    for a in ["18-21", "22-25", "26-28"]:
        row[f"it_{a}"] = d.get(a, "")
        row[f"all_{a}"] = allind.get((p, a), "")
        row[f"it_share_{a}"] = (round(d[a] / allind[(p, a)], 4)
                                if a in d and allind.get((p, a)) else "")
    row["it_18_25"] = d["18-21"] + d["22-25"] if "18-21" in d and "22-25" in d else ""
    row["it_18_28"] = (row["it_18_25"] + d["26-28"]) if row["it_18_25"] != "" and "26-28" in d else ""
    row["it_other_bands_reported"] = ";".join(a for a in d if a not in ("18-21", "22-25", "26-28"))
    row.update({"vintage_release_date": m["vintage_release_date"], "source_file": m["source_file"],
                "source_url": m["source_url"], "archive_url": m["archive_url"]})
    it_rows.append(row)
write("epfo_it_age_best.csv", it_rows)

# ---------- revisions ----------
rev = []
for p in sorted(last):
    if first[p] == last[p]:
        continue
    for a in ["Total", "18-21", "22-25"]:
        f0 = int(age_idx[(first[p], p, a)]["net_payroll"])
        f1 = int(age_idx[(last[p], p, a)]["net_payroll"])
        rev.append({"month": p, "age_band": a, "first_print": f0, "last_print": f1,
                    "first_release": first[p], "last_release": last[p],
                    "revision_pct": round(100 * (f1 - f0) / abs(f0), 1) if f0 else ""})
write("epfo_revisions.csv", rev)

# ---------- equal-lag comparisons (revision-consistent) ----------
# (a) first print of every month: same ~2-month lag for every month
ind_first = {}
for r in ind:
    if r["period_type"] == "month" and r["industry"] == IT:
        k = (r["period"], r["age_band"])
        if k not in ind_first or r["vintage_release_date"] < ind_first[k]["vintage_release_date"]:
            ind_first[k] = r
fp = []
for p in sorted(first):
    v = first[p]
    row = {"month": p, "fy": fy_of(p), "first_release": v}
    for a in AGES:
        row[f"net_{a}"] = age_idx[(v, p, a)]["net_payroll"]
    for a in ["18-21", "22-25", "26-28"]:
        r = ind_first.get((p, a))
        row[f"it_{a}"] = r["net_payroll"] if r and r["vintage_release_date"] == v else ""
    src = age_idx[(v, p, "Total")]
    row.update({"source_file": src["source_file"], "source_url": src["source_url"],
                "archive_url": src["archive_url"]})
    fp.append(row)
fp.append({"month": "2025-07", "fy": "FY2025-26", "first_release": "2025-09-23",
           "net_Total": 2104000, "source_url": PIB_JUL25,
           "source_file": "PIB press release; 18-25 combined net = 913000 (not split 18-21/22-25)"})
write("epfo_monthly_first_print.csv", fp, keys=list(fp[0].keys()))

# (b) Apr-Jun as printed in each year's 20-August release (lags 2-4 months for every year)
q1 = []
for r0 in sorted({r["vintage_release_date"] for r in age if r["vintage_release_date"][5:] == "08-20"}):
    yr = r0[:4]
    months = [f"{yr}-04", f"{yr}-05", f"{yr}-06"]
    row = {"fy": fy_of(months[0]), "release": r0}
    for a in AGES:
        vals = [age_idx.get((r0, m, a)) for m in months]
        row[f"net_{a}"] = sum(int(x["net_payroll"]) for x in vals) if all(vals) else ""
        cv = [comp_idx.get((r0, m, a)) for m in months]
        row[f"new_{a}"] = sum(int(x["a_new"]) for x in cv) if all(cv) else ""
    for a in ["18-21", "22-25", "26-28"]:
        vals = [r for r in ind if r["vintage_release_date"] == r0 and r["industry"] == IT
                and r["age_band"] == a and r["period"] in months]
        row[f"it_{a}"] = sum(int(x["net_payroll"]) for x in vals) if len(vals) == 3 else ""
    src = age_idx[(r0, months[0], "Total")]
    row.update({"source_file": src["source_file"], "source_url": src["source_url"],
                "archive_url": src["archive_url"]})
    q1.append(row)
write("epfo_q1_aug_release.csv", q1)
