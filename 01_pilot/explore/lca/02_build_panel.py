"""Combine filtered LCA extracts -> clean case-level extract + firm x quarter panel.
Input : <scratch>/filtered/*.csv.gz  (from 01_download_filter.py; source https://www.dol.gov/agencies/eta/foreign-labor/performance)
Output: lca_cases_target_firms.csv.gz, lca_firm_quarter_long.csv, lca_firm_year_positions.csv
"""
import sys, glob, re, os
import numpy as np, pandas as pd

SCR = sys.argv[1]
OUT = os.path.dirname(os.path.abspath(__file__))
ORDER = ["FY15_Q4", "FY16", "FY17", "FY2018_EOY", "FY2019"] + [f"FY{y}_Q{q}" for y in range(2020, 2026) for q in range(1, 5)] + ["FY2026_Q3"]

files = sorted(glob.glob(f"{SCR}/filtered/*.csv.gz"))
d = pd.concat([pd.read_csv(f, dtype=str) for f in files], ignore_index=True)
d["file_rank"] = d.source_file.map(lambda s: next(i for i, k in enumerate(ORDER) if k in s))

# ---------- firm mapping (tight; regex in 01 was deliberately broad) ----------
e = d.employer.fillna("").str.upper().str.replace(r"\s+", " ", regex=True).str.strip()
FIRMS = [
    ("tcs", r"^TATA CONSULTANCY"),
    ("infosys", r"^INFOSYS (LIMITED|LTD|BPO|BPM|PUBLIC SERVICES|MCCAMISH|CONSULTING|NOVA|LTD\.)"),
    ("hcltech", r"^HCL (AMERICA|TECHNOLOGIES)"),
    ("wipro", r"^WIPRO (LIMITED|LTD|LLC|TECHNOLOGIES|INC)"),
    ("techm", r"^TECH MAHINDRA"),
    ("lti", r"^LARSEN ?(&|AND) ?TOUBRO INFOTECH"),
    ("mindtree", r"^MINDTREE"),
    ("ltim", r"^LTIMINDTREE"),
    ("cognizant", r"COGNIZANT"),
    ("accenture", r"^ACCENTURE"),
    ("mphasis", r"^MPHASIS"),
    ("persistent", r"^PERSISTENT SYSTEMS"),
    ("coforge", r"^(COFORGE|NIIT TECHNOLOGIES)"),
    ("hexaware", r"^HEXAWARE"),
    ("capgemini", r"^(CAPGEMINI|IGATE)"),
]
d["firm"] = None
for f, rx in FIRMS:
    m = d.firm.isna() & e.str.contains(rx, regex=True)
    d.loc[m, "firm"] = f
emp_map = d.assign(employer_norm=e).groupby(["firm", "employer_norm"], dropna=False).size().rename("n_cases").reset_index()
emp_map.to_csv(f"{OUT}/employer_name_map.csv", index=False)
d = d[d.firm.notna()].copy()
d["firm_group"] = d.firm.replace({"lti": "ltim", "mindtree": "ltim"})  # LTIMindtree = LTI + Mindtree pre-merger

# ---------- dedupe on case number (latest release wins) ----------
d = d.sort_values("file_rank").drop_duplicates("case_number", keep="last")

# ---------- clean fields ----------
for c in ["received_date", "decision_date", "begin_date"]:
    d[c] = pd.to_datetime(d[c].str[:10], errors="coerce")
d["cal_q"] = d.decision_date.dt.to_period("Q").astype(str)
d["cal_q_recv"] = d.received_date.dt.to_period("Q").astype(str)
st = d.status.str.upper().str.replace(" ", "")
d["status_c"] = st.map({"CERTIFIED": "C", "CERTIFIED-WITHDRAWN": "CW", "WITHDRAWN": "W", "DENIED": "D"})
num = ["total_workers", "new_employment", "continued_employment", "change_previous_employment",
       "new_concurrent_employment", "change_employer", "amended_petition", "wage_from", "pw"]
for c in num:
    d[c] = pd.to_numeric(d[c].str.replace(",", ""), errors="coerce")
lvl = d.pw_level.fillna("").str.upper().str.replace("LEVEL", "").str.strip()
d["wage_level"] = lvl.where(lvl.isin(["I", "II", "III", "IV"]), "NA")

soc = d.soc_code.fillna("").str.strip().str.replace(r"[^0-9.]", "", regex=True)
d["soc6"] = soc.str[:6].where(soc.str.len() >= 6).map(lambda s: f"{s[:2]}-{s[2:]}" if isinstance(s, str) else None)
d["soc8"] = soc.where(soc.str.len() >= 9).str[6:9].where(lambda s: s.notna(), None)
d["soc8"] = np.where(d.soc8.notna() & (d.soc8 != ".00"), d.soc6 + d.soc8.fillna(""), d.soc6)

# SOC vintage + harmonized occupation group (consistent across SOC 2010 -> 2018 switch)
SOC2018_ONLY = {"15-1211", "15-1212", "15-1221", "15-1231", "15-1232", "15-1241", "15-1242", "15-1243", "15-1244",
                "15-1251", "15-1252", "15-1253", "15-1254", "15-1255", "15-1299", "13-1082", "15-2051"}
SOC2010_ONLY = {"15-1111", "15-1121", "15-1122", "15-1131", "15-1132", "15-1133", "15-1134", "15-1141", "15-1142",
                "15-1143", "15-1151", "15-1152", "15-1199"}
d["soc_vintage"] = np.where(d.soc6.isin(SOC2018_ONLY), "2018", np.where(d.soc6.isin(SOC2010_ONLY), "2010", "both/other"))


def group(s6, s8):
    if not isinstance(s6, str):
        return "UNK"
    if s6 in ("15-1131", "15-1132", "15-1133", "15-1134", "15-1251", "15-1252", "15-1254", "15-1255"):
        return "DEV"
    if s8 == "15-1199.01" or s6 == "15-1253":
        return "QA"
    if s6 in ("15-1121", "15-1211"):
        return "SYSAN"
    if s6 in ("15-1141", "15-1242", "15-1243") or s8 in ("15-1199.06", "15-1199.07"):
        return "DB"
    if s6 in ("15-1199", "15-1299"):
        return "OTHCOMP"
    if s6 in ("15-1151", "15-1152", "15-1231", "15-1232"):
        return "SUPPORT"
    if s6 in ("15-1142", "15-1143", "15-1244", "15-1241"):
        return "NETWORK"
    if s6 in ("15-1122", "15-1212"):
        return "INFOSEC"
    if s6 in ("15-1111", "15-1221") or s6.startswith("15-2"):
        return "MATH_RES"
    if s6 == "13-1111":
        return "MGMT_AN"
    if s6.startswith("13-"):
        return "OTHBUS"
    if s6 == "11-3021":
        return "CIS_MGR"
    if s6.startswith("11-"):
        return "OTHMGR"
    if s6.startswith("17-"):
        return "ENG"
    return "OTHER"


d["occ_group"] = [group(a, b) for a, b in zip(d.soc6, d.soc8)]

# employment type (positions). New-to-firm = new + new concurrent + change of employer; existing = continued + change in previous + amended
d["pos_new"] = d[["new_employment", "new_concurrent_employment", "change_employer"]].sum(axis=1, min_count=1)
d["pos_existing"] = d[["continued_employment", "change_previous_employment", "amended_petition"]].sum(axis=1, min_count=1)

keep = ["source_file", "case_number", "status", "status_c", "received_date", "decision_date", "cal_q", "cal_q_recv", "visa_class",
        "employer", "firm", "firm_group", "soc_code", "soc6", "soc8", "soc_vintage", "soc_title", "occ_group", "job_title",
        "full_time", "begin_date", "total_workers", "new_employment", "continued_employment", "change_previous_employment",
        "new_concurrent_employment", "change_employer", "amended_petition", "pos_new", "pos_existing", "wage_from", "wage_to",
        "wage_unit", "pw", "pw_unit", "pw_level", "wage_level", "pw_source", "worksite_state", "h1b_dependent"]
d[keep].to_csv(f"{OUT}/lca_cases_target_firms.csv.gz", index=False, compression="gzip")

# ---------- firm x quarter long panel (certified positions, by decision quarter) ----------
c = d[d.status_c == "C"].copy()
rows = []
for firmcol in ["firm", "firm_group"]:
    for split, col in [("total", None), ("soc6", "soc6"), ("occ_group", "occ_group"), ("wage_level", "wage_level")]:
        keys = [firmcol, "cal_q"] + ([col] if col else [])
        g = c.groupby(keys, dropna=False).agg(positions=("total_workers", "sum"), cases=("case_number", "size")).reset_index()
        g["split"] = split
        g["category"] = g[col] if col else "all"
        g = g.rename(columns={firmcol: "firm"})
        rows.append(g[["firm", "cal_q", "split", "category", "positions", "cases"]])
    g = c.groupby([firmcol, "cal_q"]).agg(new=("pos_new", "sum"), existing=("pos_existing", "sum")).reset_index().rename(columns={firmcol: "firm"})
    g = g.melt(["firm", "cal_q"], var_name="category", value_name="positions")
    g["split"] = "emp_type"; g["cases"] = np.nan
    rows.append(g[["firm", "cal_q", "split", "category", "positions", "cases"]])
p = pd.concat(rows).drop_duplicates(["firm", "cal_q", "split", "category"])
p = p[p.cal_q != "NaT"]
p["source"] = "https://www.dol.gov/agencies/eta/foreign-labor/performance (OFLC LCA disclosure files FY2015-FY2026Q3)"
p.to_csv(f"{OUT}/lca_firm_quarter_long.csv", index=False)

# ---------- firm x year sample sizes ----------
d["dol_fy"] = (d.decision_date.dt.year + (d.decision_date.dt.month >= 10)).astype("Int64")
d["cal_year"] = d.decision_date.dt.year.astype("Int64")
fy = d.pivot_table(index="firm_group", columns="dol_fy", values="total_workers", aggfunc="sum").where(lambda x: x > 0)
fyc = d[d.status_c == "C"].pivot_table(index="firm_group", columns="dol_fy", values="total_workers", aggfunc="sum")
fyc.to_csv(f"{OUT}/lca_firm_year_positions.csv")
print("certified positions by firm x DOL fiscal year (decision date):\n", fyc.round(0).to_string())
print("\ncertified cases by firm x FY:\n", d[d.status_c == "C"].pivot_table(index="firm_group", columns="dol_fy", values="case_number", aggfunc="size").to_string())
print("\nstatus mix:", d.status_c.value_counts().to_dict())
print("SOC vintage by FY:\n", pd.crosstab(d.dol_fy, d.soc_vintage).to_string())
print("occ_group shares (certified positions, all years, 8 firms):\n",
      (c[c.firm_group.isin(["tcs", "infosys", "hcltech", "wipro", "techm", "ltim", "cognizant", "accenture"])]
       .groupby("occ_group").total_workers.sum() / c.total_workers.sum()).sort_values(ascending=False).round(3).to_string())
