"""Build chart-ready CSVs for the jobs and bottom-rung sections (4 and 5) of
"A Health Check of India's IT Services in 2026".

Run from anywhere:  python3 -I data/explore/health_check/charts/prep_jobs.py

Reads only existing repo CSVs (no web access, no unit-level PLFS microdata:
every PLFS input is an aggregate already in the repo). Writes, into this folder:

  top6_headcount.csv      rev_vs_hc.csv          sector_employment.csv
  fresher_intake.csv      four_shares.csv        under30.csv
  infosys_grades.csv      nirf.csv               junior_pay.csv
  postings_experience.csv grad_unemp.csv         numbers_jobs.csv

PLFS figures: Periodic Labour Force Survey unit data (NSO, MoSPI), aggregated
in this repo; aggregates only. Cite MoSPI.
"""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))  # repo root
EX = os.path.join(ROOT, "data", "explore")
HC = os.path.join(EX, "health_check")


def p(*parts):
    return os.path.join(ROOT, *parts)


def rel(path):
    return os.path.relpath(path, ROOT)


def out(df, name):
    df.to_csv(os.path.join(HERE, name), index=False)
    print(f"wrote {name}: {len(df)} rows")


NUMBERS = []  # rows for numbers_jobs.csv


def num(key, value, unit, period, source_file, how, expected=None, tol=None, note=""):
    """Record a number the prose may quote; compare with the brief's figure."""
    match = ""
    if expected is not None:
        t = tol if tol is not None else 0.0
        match = "yes" if abs(float(value) - float(expected)) <= t + 1e-9 else "NO"
    NUMBERS.append(dict(key=key, value=value, unit=unit, period=period,
                        source_file=source_file, how_computed=how,
                        brief_value=expected if expected is not None else "",
                        matches_brief=match, note=note))


FIRMS6 = ["tcs", "infosys", "hcltech", "wipro", "techm"]


def calq_to_fq(cq):
    """2026Q2 -> Q1FY27 (Indian FY, Apr-Mar)."""
    y, q = int(cq[:4]), int(cq[-1])
    fy = y + 1 if q >= 2 else y
    fq = q - 1 if q >= 2 else 4
    return f"Q{fq}FY{str(fy)[-2:]}"


def calq_end(cq):
    y, q = int(cq[:4]), int(cq[-1])
    return {1: f"{y}-03-31", 2: f"{y}-06-30", 3: f"{y}-09-30", 4: f"{y}-12-31"}[q]


# ---------------------------------------------------------------------------
# 1. top6_headcount
# ---------------------------------------------------------------------------
CORE = p("data", "corrected", "core_quarterly_final.csv")
core = pd.read_csv(CORE)
hcp = core.pivot(index="cal_q", columns="firm", values="headcount")
revp = core.pivot(index="cal_q", columns="firm", values="rev_usd")

# LTI-group rule: LTIM (restated from Q1FY22 = 2021Q2) where it exists, LTI+Mindtree before.
# This is the rule that reproduces the 1,694,188 peak and round3/gcc/top6_headcount_fy.csv.
hcp["ltim_group"] = hcp["ltim"].fillna(hcp["lti"] + hcp["mindtree"])
revp["ltim_group"] = revp["ltim"].fillna(revp["lti"] + revp["mindtree"])
G6 = FIRMS6 + ["ltim_group"]

qs = [q for q in hcp.index if "2015Q1" <= q <= "2026Q2"]
rows = []
for q in qs:
    for f in G6:
        v = hcp.at[q, f]
        if pd.notna(v):
            rows.append(dict(cal_q=q, quarter_end=calq_end(q), fiscal_quarter=calq_to_fq(q),
                             firm=f, headcount_persons=int(v), status="reported"))
    tot = hcp.loc[q, G6]
    if tot.notna().all():  # complete only from 2016Q1 (Wipro new-definition series starts then)
        rows.append(dict(cal_q=q, quarter_end=calq_end(q), fiscal_quarter=calq_to_fq(q),
                         firm="top6", headcount_persons=int(tot.sum()), status="complete"))
top = pd.DataFrame(rows)

# 2026Q3 (Q2FY27): four firms reported; Infosys and LTIM carried at 2026Q2.
Q2U = os.path.join(HC, "contradictions", "q2fy27_update.csv")
upd = pd.read_csv(Q2U)
upd = upd[upd.firm.isin(["tcs", "hcltech", "wipro", "techm", "infosys", "ltim"])]
part = []
for _, r in upd.iterrows():
    f = "ltim_group" if r.firm == "ltim" else r.firm
    prev_panel = hcp.at["2026Q2", f]
    if r.status == "reported":
        assert int(r.headcount_prev_q_in_panel) == int(prev_panel), (f, r.headcount_prev_q_in_panel, prev_panel)
        part.append(dict(cal_q="2026Q3", quarter_end="2026-09-30", fiscal_quarter="Q2FY27",
                         firm=f, headcount_persons=int(r.headcount), status="reported"))
    else:
        part.append(dict(cal_q="2026Q3", quarter_end="2026-09-30", fiscal_quarter="Q2FY27",
                         firm=f, headcount_persons=int(prev_panel),
                         status=f"carried_at_2026Q2 ({r.report_date})"))
part = pd.DataFrame(part)
top = pd.concat([top, part, pd.DataFrame([dict(
    cal_q="2026Q3", quarter_end="2026-09-30", fiscal_quarter="Q2FY27", firm="top6",
    headcount_persons=int(part.headcount_persons.sum()),
    status="partial: 4 of 6 reported (TCS, HCLTech, Wipro, TechM); Infosys and LTIM carried at 2026Q2")])],
    ignore_index=True)

t6 = top[top.firm == "top6"].sort_values("cal_q").reset_index(drop=True)
t6["qoq_change_persons"] = t6.headcount_persons.diff()
peak_q = t6.loc[t6[~t6.status.str.startswith("partial")].headcount_persons.idxmax(), "cal_q"]
top = top.merge(t6[["cal_q", "qoq_change_persons"]].assign(firm="top6"), on=["cal_q", "firm"], how="left")
top["is_partial"] = top.cal_q.eq("2026Q3")
top["is_peak"] = top.firm.eq("top6") & top.cal_q.eq(peak_q)
top["source"] = np.where(top.cal_q.eq("2026Q3"), rel(Q2U) + " (+ core panel for carried firms)", rel(CORE))
top["note"] = np.where(top.firm.eq("ltim_group"),
                       "LTI+Mindtree to 2021Q1; LTIM (restated) from 2021Q2", "")
top.loc[top.firm.eq("top6"), "note"] = ("TCS+Infosys+HCLTech+Wipro+TechM+LTI group; global, permanent "
                                       "(TechM incl. direct contractors); Wipro company-wide headcount; "
                                       "complete from 2016Q1 because Wipro's comparable series starts then")
top = top.sort_values(["firm", "cal_q"])
out(top, "top6_headcount.csv")

pk = t6.set_index("cal_q").headcount_persons
num("top6_headcount_peak", int(pk[peak_q]), "persons", peak_q, rel(CORE),
    "max over complete quarters of sum of 6 firms (LTIM from 2021Q2, LTI+Mindtree before)", 1694188, 0)
num("top6_headcount_2026Q2", int(pk["2026Q2"]), "persons", "2026Q2 (Q1FY27)", rel(CORE), "sum of 6 firms")
fyend = {f"FY{str(y)[-2:]}": f"{y}Q1" for y in range(2016, 2027)}
num("top6_headcount_FY23_end", int(pk["2023Q1"]), "persons", "Mar 2023", rel(CORE), "sum at 2023Q1", 1679489, 0)
num("top6_headcount_FY26_end", int(pk["2026Q1"]), "persons", "Mar 2026", rel(CORE), "sum at 2026Q1", 1618023, 0)
num("top6_headcount_change_FY23_FY26_pct", round((pk["2026Q1"] / pk["2023Q1"] - 1) * 100, 1), "pct",
    "Mar 2023 -> Mar 2026", rel(CORE), "simple % change", -3.7, 0.05)
num("top6_headcount_change_peak_to_2026Q2_pct", round((pk["2026Q2"] / pk[peak_q] - 1) * 100, 1), "pct",
    f"{peak_q} -> 2026Q2", rel(CORE), "simple % change")
q3 = part.set_index("firm")
rep = q3[q3.status == "reported"]
netadd = int((rep.headcount_persons - hcp.loc["2026Q2", rep.index]).sum())
num("q2fy27_net_adds_4_firms", netadd, "persons", "Q2FY27 (Jul-Sep 2026)", rel(Q2U),
    "sum of QoQ change for TCS, HCLTech, Wipro, TechM vs 2026Q2 panel", 9438, 0)
num("top6_headcount_2026Q3_partial", int(t6.headcount_persons.iloc[-1]), "persons", "2026Q3 (Q2FY27)",
    rel(Q2U), "4 reported + Infosys and LTIM carried at 2026Q2",
    note="partial; Infosys reports 23 Oct, LTM 16 Oct")

# ---------------------------------------------------------------------------
# 2. rev_vs_hc
# ---------------------------------------------------------------------------
rv = []
fy_rows = {}
for y in range(2016, 2027):
    qtrs = [f"{y-1}Q2", f"{y-1}Q3", f"{y-1}Q4", f"{y}Q1"]
    r = revp.loc[qtrs, G6]
    assert r.notna().all().all(), (y, r)
    fy_rows[f"FY{str(y)[-2:]}"] = dict(rev=r.values.sum(), hc=pk[f"{y}Q1"])
base = fy_rows["FY19"]
for fy, d in fy_rows.items():
    for metric, val, unit in [
        ("revenue_usd", round(d["rev"], 1), "USD mn (sum of 4 quarters)"),
        ("headcount_fy_end", int(d["hc"]), "persons (end-March)"),
        ("revenue_index", round(d["rev"] / base["rev"] * 100, 1), "index FY19=100"),
        ("headcount_index", round(d["hc"] / base["hc"] * 100, 1), "index FY19=100"),
        ("revenue_per_employee", round(d["rev"] / d["hc"] * 1000, 1), "USD k (FY revenue / FY-end headcount)"),
    ]:
        rv.append(dict(period=fy, freq="FY", metric=metric, value=val, unit=unit))
qrpe = []
for q in t6[t6.status == "complete"].cal_q:
    rr = revp.loc[q, G6]
    if rr.notna().all():
        rv.append(dict(period=q, freq="quarter", metric="revenue_per_employee_annualised",
                       value=round(rr.sum() * 4 / pk[q] * 1000, 2),
                       unit="USD k (quarterly revenue x4 / end-quarter headcount)"))
rvdf = pd.DataFrame(rv)
rvdf["source"] = rel(CORE)
rvdf["note"] = ("Top-6 incl. LTI group rule; Wipro revenue = IT Services segment while headcount is "
                "company-wide; USD, not constant currency")
out(rvdf, "rev_vs_hc.csv")
qr = rvdf[rvdf.metric == "revenue_per_employee_annualised"].set_index("period").value
num("rev_per_employee_2022Q4", round(qr["2022Q4"], 1), "USD k", "2022Q4", rel(CORE),
    "annualised quarterly USD revenue / end-quarter headcount, top-6", 48.6, 0.05)
num("rev_per_employee_2026Q2", round(qr["2026Q2"], 1), "USD k", "2026Q2", rel(CORE), "as above", 53.8, 0.05)
num("rev_per_employee_FY23", round(fy_rows["FY23"]["rev"] / fy_rows["FY23"]["hc"] * 1000, 1), "USD k", "FY23",
    rel(CORE), "FY revenue / FY-end headcount (FY basis; differs from the quarterly measure)")
num("rev_per_employee_FY26", round(fy_rows["FY26"]["rev"] / fy_rows["FY26"]["hc"] * 1000, 1), "USD k", "FY26",
    rel(CORE), "FY revenue / FY-end headcount")
num("top6_revenue_FY26", round(fy_rows["FY26"]["rev"] / 1000, 2), "USD bn", "FY26", rel(CORE), "sum of 4 quarters")
num("top6_revenue_change_FY23_FY26_pct", round((fy_rows["FY26"]["rev"] / fy_rows["FY23"]["rev"] - 1) * 100, 1),
    "pct", "FY23 -> FY26", rel(CORE), "simple % change in USD revenue")

# ---------------------------------------------------------------------------
# 3. sector_employment
# ---------------------------------------------------------------------------
EMP = os.path.join(EX, "round3", "plfs", "employment_levels_long.csv")
SENS = os.path.join(HC, "contradictions", "plfs", "sensitivity_and_counts.csv")
CHG = os.path.join(HC, "contradictions", "plfs_change_ci.csv")
SSP = os.path.join(EX, "round3", "sector_aggregates", "sector_series_pulled.csv")
REC = os.path.join(EX, "round3", "gcc_reconcile", "reconcile_inputs.csv")

ROUND_MID = {"2017-18": "2018-01-01", "2018-19": "2019-01-01", "2019-20": "2020-01-01",
             "2020-21": "2021-01-01", "2021-22": "2022-01-01", "2022-23": "2023-01-01",
             "2023-24": "2024-01-01", "cy2024": "2024-07-01", "cy2025": "2025-07-01"}
ROUND_LABEL = {k: (k.upper().replace("CY", "CY") if k.startswith("cy") else k) for k in ROUND_MID}


def round_flag(r, cluster=True):
    f = []
    if r == "cy2025":
        f.append("CY2025 survey redesign (monthly sampling, new strata, ~2.5x sample): break in series")
    if cluster and r in ("2023-24", "cy2024"):
        f.append("one high-weight sampling cluster (~9% of total); 2023-24 and CY2024 share Jan-Jun 2024 records")
    if r == "2021-22":
        f.append("strata change in 2021-22; part of the jump is artefact")
    return "; ".join(f)


emp = pd.read_csv(EMP)
se_rows = []
for grp, series, extra in [("nic62_63", "plfs_nic62_63", ""),
                           ("ictocc_outside_it", "plfs_ict_occupations_outside_nic62_63",
                            "ICT occupations (NCO) in industries other than NIC 62-63; NCO-2004 to NCO-2015 "
                            "switch in 2021-22: compare only from 2022-23")]:
    x = emp[(emp.group == grp) & (emp.cut == "all")]
    for _, r in x.iterrows():
        fl = round_flag(r["round"], cluster=(grp == "nic62_63"))
        if grp == "ictocc_outside_it" and r["round"] < "2022-23" and not r["round"].startswith("cy"):
            fl = "; ".join([s for s in [fl, "pre-2022-23 not comparable (NCO-2004)"] if s])
        se_rows.append(dict(series=series, period=ROUND_LABEL[r["round"]], plot_date=ROUND_MID[r["round"]],
                            value_persons=round(r.estimate), se_persons=round(r.se),
                            ci90_lo_persons=round(r.ci90_lo), ci90_hi_persons=round(r.ci90_hi),
                            n_unweighted=int(r.n_unweighted), vintage="", flag=fl, note=extra,
                            source=rel(EMP) + " (PLFS, NSO/MoSPI; aggregates)"))
sens = pd.read_csv(SENS)
for r_, lab in [("2023-24", "2023-24"), ("cy2024", "CY2024")]:
    v = sens[(sens["round"] == r_) & (sens.item == "it_62_63_all_ages_ups__excl_top_fsu")].estimate.iloc[0]
    se_rows.append(dict(series="plfs_nic62_63_excl_high_weight_cluster", period=lab, plot_date=ROUND_MID[r_],
                        value_persons=round(v), se_persons=np.nan, ci90_lo_persons=np.nan, ci90_hi_persons=np.nan,
                        n_unweighted=np.nan, vintage="", flag="sensitivity: drops the single highest-weight FSU",
                        note="no SE computed", source=rel(SENS)))
# Nasscom levels by edition (vintage). Levels are revised every edition: compare growth within an edition.
ssp = pd.read_csv(SSP)
ssp = ssp[ssp.series == "Industry direct employment"]
nas = []
for _, r in ssp.iterrows():
    nas.append(dict(fy="FY" + r.fiscal_year[-2:], value_m=float(r.value), vintage=r.vintage,
                    note=r.notes, source=rel(SSP)))
rec = pd.read_csv(REC)
for _, r in rec.iterrows():
    it = str(r.iloc[0])
    if it.startswith("Nasscom industry employment FY24 restated"):
        nas.append(dict(fy="FY24", value_m=5.67, vintage="SR Feb 2025 (restated for GCC coverage, Sep 2024)",
                        note="restatement adds ~0.24m, matching Nasscom-Zinnov GCC revision", source=rel(REC)))
    if it.startswith("Nasscom net hiring (SR2025 vintage)"):
        nas.append(dict(fy="FY25", value_m=5.8, vintage="SR Feb 2025 (estimate)",
                        note="'total headcount 5.8 Mn'; net addition 126k", source=rel(REC)))
    if it.startswith("Nasscom net hiring (SR2024 vintage)"):
        nas.append(dict(fy="FY23", value_m=5.37, vintage="SR Feb 2024 (implied: 5.43m minus 60k net hiring)",
                        note="inferred, not published as a level", source=rel(REC)))
for d in nas:
    y = int("20" + d["fy"][2:])
    se_rows.append(dict(series="nasscom_direct_employment", period=d["fy"], plot_date=f"{y}-03-31",
                        value_persons=round(d["value_m"] * 1e6), se_persons=np.nan, ci90_lo_persons=np.nan,
                        ci90_hi_persons=np.nan, n_unweighted=np.nan, vintage=d["vintage"],
                        flag="industry-body estimate; method not public; FY26 published Feb 2026 (partly projected)",
                        note=d["note"], source=d["source"]))
sedf = pd.DataFrame(se_rows)
sedf["value_m"] = (sedf.value_persons / 1e6).round(3)
sedf = sedf.sort_values(["series", "plot_date", "vintage"], kind="stable")
sedf = sedf[["series", "period", "plot_date", "value_persons", "value_m", "se_persons", "ci90_lo_persons",
             "ci90_hi_persons", "n_unweighted", "vintage", "flag", "note", "source"]]
out(sedf, "sector_employment.csv")

e = emp[(emp.group == "nic62_63") & (emp.cut == "all")].set_index("round")
num("plfs_nic62_63_cy2025", round(e.at["cy2025", "estimate"] / 1e6, 2), "million persons", "CY2025",
    rel(EMP), "survey-weighted UPS employment, NIC 62+63, all ages", 5.70, 0.005,
    note=f"90% CI {e.at['cy2025','ci90_lo']/1e6:.2f}-{e.at['cy2025','ci90_hi']/1e6:.2f}m")
num("plfs_nic62_63_2022_23", round(e.at["2022-23", "estimate"] / 1e6, 2), "million persons", "2022-23", rel(EMP), "as above")
chg = pd.read_csv(CHG).set_index(["series", "from_round", "to_round"])
c = chg.loc[("nic62_63", "2022-23", "cy2025")]
num("plfs_change_2022_23_to_cy2025_pct", c.pct_log, "pct (log x100)", "2022-23 -> CY2025", rel(CHG),
    "log change, rounds treated as independent; CI understates uncertainty across the design break", 4.1, 0.05,
    note=f"90% CI {c.pct_ci90_lo} to {c.pct_ci90_hi}")
num("plfs_change_2022_23_to_cy2025_ci90_lo_pct", c.pct_ci90_lo, "pct", "2022-23 -> CY2025", rel(CHG), "", -7.0, 0.05)
num("plfs_change_2022_23_to_cy2025_ci90_hi_pct", c.pct_ci90_hi, "pct", "2022-23 -> CY2025", rel(CHG), "", 15.2, 0.05)
recheck = np.log(e.at["cy2025", "estimate"] / e.at["2022-23", "estimate"]) * 100
num("plfs_change_recomputed_from_levels", round(recheck, 1), "pct (log x100)", "2022-23 -> CY2025", rel(EMP),
    "ln(CY2025/2022-23)x100 recomputed from levels", 4.1, 0.05)
ci = chg.loc[("ict_occ_outside_nic62_63", "2022-23", "cy2025")]
num("plfs_ict_outside_change", int(ci.change), "persons", "2022-23 -> CY2025", rel(CHG),
    "level change, ICT occupations outside NIC 62-63", 188000, 500,
    note=f"{int(ci.level_from)} -> {int(ci.level_to)}; 90% CI {int(ci.ci90_lo)} to {int(ci.ci90_hi)}")
num("plfs_nic62_63_2023_24_excl_cluster", round(sens[(sens["round"] == "2023-24") & (sens.item == "it_62_63_all_ages_ups__excl_top_fsu")].estimate.iloc[0] / 1e6, 2),
    "million persons", "2023-24", rel(SENS), "excluding highest-weight FSU")
num("nasscom_employment_FY26", 5.95, "million", "FY26 (SR Feb 2026)", rel(SSP), "as published", 5.95, 0)
num("nasscom_employment_growth_FY26_pct", round((5.95 / 5.815 - 1) * 100, 1), "pct", "FY25->FY26, SR2026 edition",
    rel(SSP), "5.95/5.815 - 1 (Nasscom states +2.3%, +135k)", 2.3, 0.05)

# ---------------------------------------------------------------------------
# 4. fresher_intake
# ---------------------------------------------------------------------------
FHB = os.path.join(EX, "workforce", "fresher_hires_annual_best.csv")
FTP = os.path.join(HC, "fresher_thirdparty", "fresher_thirdparty_long.csv")
fh = pd.read_csv(FHB)
ftp = pd.read_csv(FTP).set_index("record_id")
FIRM_MAP = {"tcs": "tcs", "infosys": "infosys", "hcltech": "hcltech", "wipro": "wipro", "techm": "techm",
            "lti": "ltim_group", "mindtree": "ltim_group", "ltimindtree": "ltim_group"}
fr = []
for _, r in fh[(fh.fy >= 2016) & (fh.fy <= 2026)].iterrows():
    fr.append(dict(fy=f"FY{str(r.fy)[-2:]}", group="firm", series=f"firm_fresher_hires_{r.firm}",
                   entity=r.firm, kind="actual", value_persons=r.fresher, value_low=np.nan, value_high=np.nan,
                   scope="company-wide fresher intake (definitions vary: hired/onboarded/trained)",
                   published="", outlet="", record_id="", note="", source=rel(FHB)))
for rid, fy in [("ftp0004", "FY25"), ("ftp0007", "FY26")]:
    r = ftp.loc[rid]
    fr.append(dict(fy=fy, group="firm", series="firm_fresher_hires_wipro", entity="wipro", kind="actual",
                   value_persons=r.value, value_low=np.nan, value_high=np.nan,
                   scope="company-wide fresher intake", published=r.date_published, outlet=r.outlet,
                   record_id=rid, note="management statement (press)", source=rel(FTP)))
frd = pd.DataFrame(fr)
# firm sums
fw = frd.copy()
fw["g"] = fw.entity.map(FIRM_MAP)
byf = fw.groupby(["fy", "g"]).value_persons.sum().unstack()
for fy, r in byf.iterrows():
    if r[["tcs", "infosys", "hcltech"]].notna().all():
        fr.append(dict(fy=fy, group="sum", series="sum_tcs_infosys_hcltech", entity="TCS+Infosys+HCLTech",
                       kind="actual", value_persons=r[["tcs", "infosys", "hcltech"]].sum(),
                       value_low=np.nan, value_high=np.nan, scope="sum of firm rows",
                       published="", outlet="", record_id="", note="", source=rel(FHB)))
    have = [g for g in ["tcs", "infosys", "hcltech", "wipro", "techm", "ltim_group"] if pd.notna(r.get(g))]
    if {"tcs", "infosys", "hcltech"} <= set(have) and len(have) >= 4:
        missing = sorted(set(["tcs", "infosys", "hcltech", "wipro", "techm", "ltim_group"]) - set(have))
        fr.append(dict(fy=fy, group="sum", series="sum_top6_available", entity="top-6 (firms available)",
                       kind="actual", value_persons=r[have].sum(), value_low=np.nan, value_high=np.nan,
                       scope="sum of available top-6 firms",
                       published="", outlet="", record_id="",
                       note=("missing: " + ", ".join(missing)) if missing else "all six",
                       source=rel(FHB) + "; " + rel(FTP)))
# FY27 targets and H1 actuals
TGT = [("ftp0034", "tcs", "target", "offers (CEO to PTI, Apr 2026)"),
       ("ftp0037", "infosys", "target", "Q4FY26 call; repeated on Q1FY27 call"),
       ("ftp0036", "wipro", "target", "no target disclosed ('completely on demand'); blank is not zero"),
       ("ftp0040", "hcltech", "target", "no FY27 target disclosed; blank is not zero"),
       ("ftp0041", "cognizant", "target", "CY2026, cut from 24-25k (Feb) to 20k (Jul); not top-6")]
for rid, ent, kind, note in TGT:
    r = ftp.loc[rid]
    fr.append(dict(fy="FY27", group="firm_target", series=f"fy27_target_{ent}", entity=ent, kind=kind,
                   value_persons=r.value, value_low=np.nan, value_high=np.nan, scope=r.geo_scope,
                   published=r.date_published, outlet=r.outlet, record_id=rid, note=note, source=rel(FTP)))
h1 = [("ftp0013", "tcs", "FY27 H1 onboarded ~24k (14k Q1 + 10k Q2); low-tier outlets"),
      ("ftp0015", "infosys", "FY27 Q1 only (>4k)")]
for rid, ent, note in h1:
    r = ftp.loc[rid]
    fr.append(dict(fy="FY27", group="firm_partial", series=f"fy27_partial_{ent}", entity=ent,
                   kind="actual_partial_year", value_persons=r.value, value_low=np.nan, value_high=np.nan,
                   scope=r.geo_scope, published=r.date_published, outlet=r.outlet, record_id=rid,
                   note=note, source=rel(FTP)))
hcl_h1 = ftp.loc["ftp0017"].value + ftp.loc["ftp0019"].value
fr.append(dict(fy="FY27", group="firm_partial", series="fy27_partial_hcltech", entity="hcltech",
               kind="actual_partial_year", value_persons=hcl_h1, value_low=np.nan, value_high=np.nan,
               scope="company-wide", published="2026-10-13", outlet="People Matters / LapaasVoice",
               record_id="ftp0017+ftp0019", note="H1 FY27 = Q1 1,056 + Q2 6,136 (flat vs H1 FY26 7,180)",
               source=rel(FTP)))
# third-party sector estimates
TP = [("ftp0450", "xpheno", "projection", "in-year projection (Feb 2022): 'almost double' 225k; derived"),
      ("ftp0451", "xpheno", "actual", "2026 vintage of the FY22 peak; 33% above the 2022 figure, revision unexplained"),
      ("ftp0453", "xpheno", "actual", "'lowest in two decades'"),
      ("ftp0459", "xpheno", "actual", "~120k, -80% from peak"),
      ("ftp0085", "han_digital", "actual", "IT-BPM incl. GCCs and BPO (wider scope)"),
      ("ftp0086", "han_digital", "actual", "estimate; IT-BPM incl. GCCs and BPO"),
      ("ftp0087", "han_digital", "projection", "'up to' 210k (+20%): upper bound"),
      ("ftp0153", "teamlease_digital", "actual", "presented as FY23 actual"),
      ("ftp0137", "teamlease_digital", "actual",
       "85-95k 'tech services', published 13 Mar 2025 (in-year); about equal to top-6 own hires, so likely large firms only")]
for rid, pub, kind, note in TP:
    r = ftp.loc[rid]
    fr.append(dict(fy=r.period, group="thirdparty", series=r.series, entity=pub, kind=kind,
                   value_persons=r.value, value_low=r.value_low, value_high=r.value_high, scope=r.geo_scope,
                   published=r.date_published, outlet=r.outlet, record_id=rid, note=note, source=rel(FTP)))
frd = pd.DataFrame(fr)
frd["fy_num"] = frd.fy.str[2:].astype(int)
frd = frd.sort_values(["group", "series", "fy_num"]).drop(columns="fy_num")
out(frd, "fresher_intake.csv")
s3 = frd[frd.series == "sum_tcs_infosys_hcltech"].set_index("fy").value_persons
num("fresher_tcs_infy_hcl_FY22", int(s3["FY22"]), "persons", "FY22", rel(FHB), "TCS+Infosys+HCLTech", 218000, 500)
num("fresher_tcs_infy_hcl_FY23", int(s3["FY23"]), "persons", "FY23", rel(FHB), "TCS+Infosys+HCLTech")
num("fresher_tcs_infy_hcl_FY25", int(s3["FY25"]), "persons", "FY25", rel(FHB), "TCS+Infosys+HCLTech", 65000, 500)
num("fresher_tcs_infy_hcl_FY26", int(s3["FY26"]), "persons", "FY26", rel(FHB), "TCS+Infosys+HCLTech", 76000, 500)
num("fresher_tcs_infy_hcl_change_FY22_FY26_pct", round((s3["FY26"] / s3["FY22"] - 1) * 100, 1), "pct",
    "FY22 -> FY26", rel(FHB), "simple % change", -65, 0.5)
s6 = frd[frd.series == "sum_top6_available"].set_index("fy").value_persons
for fy in ["FY25", "FY26"]:
    num(f"fresher_top6_{fy}", int(s6[fy]), "persons", fy, rel(FHB) + "; " + rel(FTP),
        "sum of six firms incl. Wipro press figure")
num("fy27_stated_targets_tcs_infy_cognizant", 25000 + 20000 + 20000, "persons", "FY27 (Cognizant CY2026)",
    rel(FTP), "TCS 25k offers + Infosys 20k + Cognizant 20k")

# ---------------------------------------------------------------------------
# 5. four_shares
# ---------------------------------------------------------------------------
SH = os.path.join(HC, "contradictions", "plfs", "it_shares_of_grad_groups.csv")
EPI = os.path.join(HC, "epfo", "epfo_it_age_best.csv")
EPQ = os.path.join(HC, "epfo", "epfo_q1_aug_release.csv")
PRS = os.path.join(HC, "postings", "press_datapoints.csv")
fs = []
sh = pd.read_csv(SH)
a = sh[(sh.measure == "it_share_of_salaried_grads_ups31") & (sh.age == "21_25")]
for _, r in a.iterrows():
    fs.append(dict(panel="a", series="plfs_it_share_salaried_grads_21_25", period=ROUND_LABEL[r["round"]],
                   plot_date=ROUND_MID[r["round"]], share_pct=round(r.share * 100, 2),
                   ci90_lo_pct=round(r.ci90_lo * 100, 2), ci90_hi_pct=round(r.ci90_hi * 100, 2),
                   numerator=np.nan, denominator=np.nan, unit_note=f"n_num={r.n_num}, n_den={r.n_den}",
                   flag=round_flag(r["round"]),
                   source=rel(SH) + " (PLFS, NSO/MoSPI; UPS, NIC 62+63, regular salaried graduates)"))
for r_ in ["2023-24", "cy2024"]:
    v = sens[(sens["round"] == r_) & (sens.item == "it_share_of_salaried_grads_21_25__excl_top_fsu")].estimate.iloc[0]
    fs.append(dict(panel="a", series="plfs_it_share_salaried_grads_21_25_excl_cluster", period=ROUND_LABEL[r_],
                   plot_date=ROUND_MID[r_], share_pct=round(v * 100, 2), ci90_lo_pct=np.nan, ci90_hi_pct=np.nan,
                   numerator=np.nan, denominator=np.nan, unit_note="", flag="sensitivity: excludes highest-weight FSU",
                   source=rel(SENS)))
ep = pd.read_csv(EPI)
ep = ep[(ep.period_type == "FY") & (ep.period >= "FY2018-19")]
for _, r in ep.iterrows():
    den = r["all_18-21"] + r["all_22-25"]
    fy = "FY" + r.period[-2:]
    fs.append(dict(panel="b", series="epfo_it_share_net_payroll_18_25_annual", period=fy,
                   plot_date=f"20{r.period[-2:]}-03-31", share_pct=round(r.it_18_25 / den * 100, 2),
                   ci90_lo_pct=np.nan, ci90_hi_pct=np.nan, numerator=int(r.it_18_25), denominator=int(den),
                   unit_note="net payroll additions, persons", flag="annual totals frozen; 20 Aug 2025 release",
                   source=rel(EPI)))
eq = pd.read_csv(EPQ)
for _, r in eq.iterrows():
    nu = r["it_18-21"] + r["it_22-25"]
    de = r["net_18-21"] + r["net_22-25"]
    fy = "FY" + r.fy[-2:]
    fs.append(dict(panel="b", series="epfo_it_share_net_payroll_18_25_apr_jun_aug_release", period=fy + " Apr-Jun",
                   plot_date=f"20{int(r.fy[-2:])-1}-06-30", share_pct=round(nu / de * 100, 2),
                   ci90_lo_pct=np.nan, ci90_hi_pct=np.nan, numerator=int(nu), denominator=int(de),
                   unit_note="net payroll additions, persons",
                   flag="Apr-Jun as printed in each year's August release (same revision stage); "
                        "not comparable with annual totals",
                   source=rel(EPQ)))
# (c) Xpheno entry-level share of active tech openings
ftp_all = pd.read_csv(FTP)
prs = pd.read_csv(PRS)


def monthly(series_ftp, series_prs):
    a_ = ftp_all[ftp_all.series == series_ftp][["period", "value", "source_type"]].rename(columns={"period": "month"})
    a_["origin"] = "ftp"
    b_ = prs[prs.series == series_prs][["month", "value", "publisher"]].copy()
    b_["source_type"] = np.where(b_.publisher.str.contains("primary"), "primary", "press")
    b_["origin"] = "prs"
    x = pd.concat([a_, b_.drop(columns="publisher")]).dropna(subset=["value"])
    x = x[x.month.str.match(r"^\d{4}-\d{2}$")]
    res = {}
    for m, g in x.groupby("month"):
        prim = g[g.source_type == "primary"]
        pick = prim if len(prim) else g
        vals = pick.value.mode()
        res[m] = (vals.max(), sorted(g.value.unique().tolist()))
    return res


ent = monthly("xpheno_entry_level_tech_openings_0_2y", "xpheno_entry_level_openings")
tot = monthly("xpheno_active_tech_openings", "xpheno_active_tech_openings_total")
for m in sorted(set(ent) & set(tot)):
    nu, nu_all = ent[m]
    de, de_all = tot[m]
    conflict = []
    if len(nu_all) > 1:
        conflict.append(f"entry values seen {nu_all}")
    if len(de_all) > 1:
        conflict.append(f"total values seen {de_all}; primary/mode used")
    fs.append(dict(panel="c", series="xpheno_entry_level_0_2y_share_of_active_tech_openings", period=m,
                   plot_date=m + "-01", share_pct=round(nu / de * 100, 2), ci90_lo_pct=np.nan, ci90_hi_pct=np.nan,
                   numerator=int(nu), denominator=int(de), unit_note="active openings (4-week window), rounded to 1k",
                   flag="; ".join(conflict), source=rel(FTP) + "; " + rel(PRS)))
# (d) foundit IT share of fresher postings
fd = ftp_all[ftp_all.series == "foundit_it_share_of_fresher_postings"]
for _, r in fd.iterrows():
    feb = "CXOToday" in str(r.outlet)
    fs.append(dict(panel="d", series="foundit_it_industry_share_of_fresher_postings", period=r.period,
                   plot_date=r.period + "-01", share_pct=r.value, ci90_lo_pct=np.nan, ci90_hi_pct=np.nan,
                   numerator=np.nan, denominator=np.nan, unit_note="share of fresher (0-3 yr) postings, rounded",
                   flag=("Feb snapshot table (CXOToday, Mar 2025); different vintage/table from Jul pair"
                         if feb else ("Jul 2025 vs Jul 2026 pair from same BT article (preferred comparison)"
                                      if r.period in ("2025-07", "2026-07") else "single article; undated page")),
                   source=rel(FTP) + f" ({r.record_id}; {r.outlet}, {r.date_published})"))
fb = prs[prs.series == "foundit_it_share_of_fresher_postings_by_function"]
for _, r in fb.iterrows():
    fs.append(dict(panel="d", series="foundit_it_function_share_of_fresher_postings", period=r.month,
                   plot_date=r.month + "-01", share_pct=r.value, ci90_lo_pct=np.nan, ci90_hi_pct=np.nan,
                   numerator=np.nan, denominator=np.nan, unit_note="share by job function, not industry",
                   flag="function-based; foundit's own release; not the same measure as the industry 24%",
                   source=rel(PRS)))
fsd = pd.DataFrame(fs)
out(fsd, "four_shares.csv")
pa = fsd[fsd.series == "plfs_it_share_salaried_grads_21_25"].set_index("period").share_pct
num("plfs_it_share_young_salaried_grads_2022_23", round(pa["2022-23"], 1), "pct", "2022-23", rel(SH),
    "IT (NIC 62+63) share of regular-salaried graduates aged 21-25, UPS", 20.4, 0.05)
num("plfs_it_share_young_salaried_grads_cy2025", round(pa["CY2025"], 1), "pct", "CY2025", rel(SH), "as above", 16.0, 0.05)
pb = fsd[fsd.series == "epfo_it_share_net_payroll_18_25_annual"].set_index("period")
num("epfo_it_18_25_change_FY22_FY25_pct", round((pb.at["FY25", "numerator"] / pb.at["FY22", "numerator"] - 1) * 100, 1),
    "pct", "FY22 -> FY25", rel(EPI), "IT heading, net payroll additions ages 18-25", -31, 0.5,
    note=f"{int(pb.at['FY22','numerator'])} -> {int(pb.at['FY25','numerator'])}")
num("epfo_it_share_18_25_FY22", round(pb.at["FY22", "share_pct"], 1), "pct", "FY22", rel(EPI),
    "IT 18-25 / all-industry 18-25 net additions", 5.8, 0.05)
num("epfo_it_share_18_25_FY25", round(pb.at["FY25", "share_pct"], 1), "pct", "FY25", rel(EPI), "as above", 3.9, 0.05)
pq = fsd[fsd.series == "epfo_it_share_net_payroll_18_25_apr_jun_aug_release"].set_index("period").share_pct
num("epfo_it_share_18_25_FY26_AprJun", round(pq["FY26 Apr-Jun"], 1), "pct", "Apr-Jun 2025", rel(EPQ),
    "Apr-Jun, August-release vintage", note=f"same window FY22 {pq['FY22 Apr-Jun']:.1f}%, FY25 {pq['FY25 Apr-Jun']:.1f}%")
pc = fsd[fsd.series.str.startswith("xpheno")].set_index("period").share_pct
num("xpheno_entry_share_2025_06", round(pc["2025-06"], 1), "pct", "Jun 2025", rel(FTP), "18k / 112k", 16.1, 0.05)
num("xpheno_entry_share_2026_10", round(pc["2026-10"], 1), "pct", "Oct 2026", rel(FTP),
    "15k / 123k (123k from Xpheno LinkedIn; 120k in one outlet gives 12.5%)", 12.2, 0.05)
num("xpheno_entry_share_2026_06_low", round(pc["2026-06"], 1), "pct", "Jun 2026", rel(FTP), "10k / 93k")
num("foundit_it_share_fresher_postings_2025_07", 32, "pct", "Jul 2025", rel(FTP), "as reported (BT, 6 Aug 2026)", 32, 0)
num("foundit_it_share_fresher_postings_2026_07", 24, "pct", "Jul 2026", rel(FTP), "as reported (BT, 6 Aug 2026)", 24, 0,
    note="foundit's own Jul 2026 release gives 22% by function (press_datapoints.csv); different cut")

# ---------------------------------------------------------------------------
# 6. under30
# ---------------------------------------------------------------------------
U30 = os.path.join(EX, "round3", "seniority_firms", "under30_panel.csv")
u = pd.read_csv(U30)
LAB = {"tcs": "TCS", "infosys": "Infosys", "hcltech": "HCLTech", "wipro": "Wipro", "techm": "TechM",
       "ltimindtree": "LTIMindtree", "lti": "LTI (pre-merger)", "mindtree": "Mindtree (pre-merger)",
       "persistent": "Persistent", "mphasis": "Mphasis", "hexaware": "Hexaware", "coforge": "Coforge"}
u = u[u.fy >= 2019].copy()
u["firm_label"] = u.firm.map(LAB)
u["slope_point"] = ""
TEN = ["tcs", "infosys", "hcltech", "wipro", "techm", "ltimindtree", "persistent", "mphasis", "hexaware", "coforge"]
slope = []
for f in TEN:
    g = u[(u.firm == f) & u.hc_share_lt30.notna()].sort_values("fy")
    st = g[g.fy >= 2023].iloc[0]
    en = g.iloc[-1]
    u.loc[st.name, "slope_point"] = "start"
    u.loc[en.name, "slope_point"] = "end"
    d = en.hc_share_lt30 - st.hc_share_lt30
    slope.append((f, int(st.fy), int(en.fy), d))
u["change_start_to_end_pp"] = np.nan
for f, s0, e0, d in slope:
    u.loc[(u.firm == f) & (u.slope_point == "end"), "change_start_to_end_pp"] = round(d, 2)
u["direction"] = ""
for f, s0, e0, d in slope:
    u.loc[(u.firm == f) & (u.slope_point == "end"), "direction"] = "fell" if d <= -1 else ("rose" if d >= 1 else "flat (|chg|<1pp)")
u["fy"] = "FY" + u.fy.astype(str).str[-2:]
u = u.rename(columns={"hc_share_lt30": "hc_share_lt30_pct", "hires_share_lt30": "hires_share_lt30_pct",
                      "note": "scope_note", "source": "source_detail"})
u["source"] = rel(U30)
u.loc[u.firm == "coforge", "scope_note"] = u.loc[u.firm == "coforge", "scope_note"] + "; no FY23/FY24 value: slope starts FY25"
out(u, "under30.csv")
nfell = sum(1 for *_, d in slope if d <= -1)
num("under30_share_fell_firms", nfell, "firms of 10", "FY23 -> latest", rel(U30),
    "count of firms with under-30 headcount share down >=1pp (Coforge from FY25)", 8, 0,
    note="; ".join(f"{f} {s0}->{e0} {d:+.1f}pp" for f, s0, e0, d in slope))

# ---------------------------------------------------------------------------
# 7. infosys_grades
# ---------------------------------------------------------------------------
WFT = os.path.join(EX, "workforce", "workforce_firm_tidy.csv")
w = pd.read_csv(WFT)
w = w[(w.firm == "infosys") & (w.metric == "headcount_by_grade")].copy()
w["doc_year"] = w.source_doc.str.extract(r"(\d{4})-\d{2}").astype(int)
gr = []
for fy, g in w.groupby("fiscal_year"):
    latest = g[g.doc_year == g.doc_year.max()]
    vals = latest.set_index("dimension").value_num
    senior = vals.get("grade_senior", 0) + vals.get("grade_top", 0)
    bands = {"junior": vals["grade_junior"], "middle": vals["grade_middle"], "senior_incl_top": senior}
    total = sum(bands.values())
    for b, v in bands.items():
        gr.append(dict(fy=f"FY{str(fy)[-2:]}", band=b, headcount_persons=int(v), total_persons=int(total),
                       share_pct=round(v / total * 100, 2), source_doc=latest.source_doc.iloc[0],
                       note=("Top reported separately and folded into Senior" if "grade_top" in vals.index
                             else "Senior already includes Top in this vintage"),
                       source=rel(WFT)))
gdf = pd.DataFrame(gr)
gdf.loc[gdf.band == "junior", "note"] += "; junior = job level JL3 and below"
out(gdf, "infosys_grades.csv")
gj = gdf[gdf.band == "junior"].set_index("fy").share_pct
num("infosys_junior_share_FY23", round(gj["FY23"], 1), "pct of headcount", "FY23", rel(WFT),
    "JL3-and-below / (junior+middle+senior incl. top), latest vintage (ESG Databook 2023-24)", 46, 0.5,
    note="46.2% using the 2022-23 databook vintage")
num("infosys_junior_share_FY26", round(gj["FY26"], 1), "pct of headcount", "FY26", rel(WFT), "as above", 30, 0.5)

# ---------------------------------------------------------------------------
# 8. nirf
# ---------------------------------------------------------------------------
NB = os.path.join(EX, "round3", "seniority_sector", "nirf_ug4_placement_by_gradyear.csv")
NW = os.path.join(EX, "round3", "seniority_sector", "nirf_within_edition_yoy.csv")
nb = pd.read_csv(NB)
nr = []
for _, r in nb.iterrows():
    nr.append(dict(comparison="by_grad_year", sample=r["sample"], tier=r.tier, grad_year=r.grad_year,
                   n_inst=r.n_inst, graduates=r.graduates, placed=r.placed, higher_studies=r.higher_studies,
                   placement_rate_pct=round(r.placement_rate * 100, 1),
                   median_inst_median_salary_inr_yr=r.median_of_inst_median_salary,
                   grad_wtd_mean_salary_inr_yr=r.grad_wtd_mean_salary,
                   placement_rate_from_pct=np.nan, dlog_placed_x100=np.nan, dlog_graduates_x100=np.nan,
                   median_dlog_inst_median_salary_x100=np.nan, source=rel(NB)))
nw = pd.read_csv(NW)
for _, r in nw.iterrows():
    nr.append(dict(comparison="within_edition", sample=f"nirf_{r.edition}_edition", tier=r.tier,
                   grad_year=r.to_grad_year, n_inst=r.n_inst, graduates=np.nan, placed=r.placed_to,
                   higher_studies=np.nan, placement_rate_pct=round(r.rate_to * 100, 1),
                   median_inst_median_salary_inr_yr=np.nan, grad_wtd_mean_salary_inr_yr=np.nan,
                   placement_rate_from_pct=round(r.rate_from * 100, 1), dlog_placed_x100=r.dlog_placed_x100,
                   dlog_graduates_x100=r.dlog_graduates_x100,
                   median_dlog_inst_median_salary_x100=r.median_dlog_inst_median_salary_x100, source=rel(NW)))
nrd = pd.DataFrame(nr)
# balanced = 147 institutions present every year; all_unbalanced = all reporting that year;
# within_edition = same institutions in one NIRF edition, change from the previous class (from_* columns)
out(nrd, "nirf.csv")
w25 = nw[(nw.edition == 2025) & (nw.tier == "all")].iloc[0]
num("nirf_placement_rate_within_2025_edition_from", round(w25.rate_from * 100, 1), "pct", "class 2022-23 (NIRF 2025 edition)",
    rel(NW), "within-edition, 183 institutions", 73.8, 0.05,
    note="73.8->70.1 is the within-edition sample; unbalanced all-institution series gives 74.1->70.1; balanced panel 75.2->71.6")
num("nirf_placement_rate_within_2025_edition_to", round(w25.rate_to * 100, 1), "pct", "class 2023-24 (NIRF 2025 edition)",
    rel(NW), "within-edition", 70.1, 0.05)
num("nirf_dlog_placed_class_2023_24", w25.dlog_placed_x100, "log pts x100", "class 2023-24 vs 2022-23", rel(NW),
    "within-edition", note=f"graduates {w25.dlog_graduates_x100:+}")
bal = nb[(nb["sample"] == "balanced") & (nb.tier == "all")].set_index("grad_year")
num("nirf_balanced_placement_rate_2022_23", round(bal.at["2022-23", "placement_rate"] * 100, 1), "pct", "class 2022-23",
    rel(NB), "balanced panel, 147 institutions")
num("nirf_balanced_placement_rate_2023_24", round(bal.at["2023-24", "placement_rate"] * 100, 1), "pct", "class 2023-24",
    rel(NB), "balanced panel, 147 institutions")

# ---------------------------------------------------------------------------
# 9. junior_pay
# ---------------------------------------------------------------------------
RE = os.path.join(HC, "labour_share", "plfs_it_real_earnings.csv")
re_ = pd.read_csv(RE)
SAMP = {"cws_regular_nic62_63": "IT (NIC 62+63), all regular wage workers",
        "cws_regular_nic62_63_grads": "IT (NIC 62+63), graduates",
        "cws_regular_all_grads": "All graduates, all industries"}
jp = []
for _, r in re_.iterrows():
    jp.append(dict(round=ROUND_LABEL[r["round"]], plot_date=ROUND_MID[r["round"]], sample=r["sample"],
                   sample_label=SAMP[r["sample"]], age_band=r.age_band,
                   mean_real_inr_month=r.mean_real_cy2025_inr, mean_se_real_inr=r.mean_se_real_cy2025_inr,
                   ci90_lo_inr=round(r.mean_real_cy2025_inr - 1.645 * r.mean_se_real_cy2025_inr),
                   ci90_hi_inr=round(r.mean_real_cy2025_inr + 1.645 * r.mean_se_real_cy2025_inr),
                   median_real_inr_month=r.median_real_cy2025_inr, mean_nominal_inr_month=r.mean_inr,
                   n_unweighted=r.n_unweighted,
                   flag=round_flag(r["round"], cluster=False),
                   note="CWS regular wage workers, previous month's earnings; CPI-Combined (base 2012), CY2025 prices; "
                        "medians heaped at round numbers, use means",
                   source=rel(RE) + " (PLFS, NSO/MoSPI; aggregates)"))
jpd = pd.DataFrame(jp)
out(jpd, "junior_pay.csv")
jj = jpd[(jpd["sample"] == "cws_regular_nic62_63") & (jpd.age_band == "21-25")].set_index("round").mean_real_inr_month
num("it_real_pay_21_25_cy2024", jj["CY2024"], "INR/month, CY2025 prices", "CY2024", rel(RE), "mean, IT all regular wage")
num("it_real_pay_21_25_cy2025", jj["CY2025"], "INR/month, CY2025 prices", "CY2025", rel(RE), "mean")
num("it_real_pay_21_25_change_pct", round((jj["CY2025"] / jj["CY2024"] - 1) * 100, 1), "pct", "CY2024 -> CY2025",
    rel(RE), "simple % change in real mean", -12, 0.5, note="spans the CY2025 survey redesign")
j31 = jpd[(jpd["sample"] == "cws_regular_nic62_63") & (jpd.age_band == "31-40")].set_index("round").mean_real_inr_month
num("it_real_pay_31_40_change_pct", round((j31["CY2025"] / j31["CY2024"] - 1) * 100, 1), "pct", "CY2024 -> CY2025",
    rel(RE), "simple % change in real mean")

# ---------------------------------------------------------------------------
# 10. postings_experience
# ---------------------------------------------------------------------------
WB = os.path.join(HC, "postings", "wb_lightcast_point_estimates.csv")
LI = os.path.join(HC, "postings", "linkedin_hiring_rate_monthly.csv")
JS = os.path.join(EX, "workforce", "jobspeak_monthly.csv")
wb = pd.read_csv(WB)
pe = []
for _, r in wb[wb.figure == "SADU25 2.11F"].iterrows():
    band = r["item"].split(":")[-1].strip()
    pe.append(dict(panel="A", series="lightcast_post_chatgpt_effect_by_experience", category=f"{band} yrs",
                   value=r.value, ci95_lo=round(r.value - r.ci95_halfwidth, 2), ci95_hi=round(r.value + r.ci95_halfwidth, 2),
                   unit="% change in postings per +1 sd AI exposure (log pts x100)",
                   period=r.period, note="Lightcast South Asia (mostly India), white-collar, not IT-only; relative to less-exposed occupations",
                   source=rel(WB) + " (World Bank SADU Oct 2025, Fig 2.11F)"))
for _, r in wb[(wb.figure == "SADU25 annex A2.12") & wb["item"].str.contains("share of postings")].iterrows():
    band = r["item"].split("experience")[-1].strip()
    pe.append(dict(panel="A2", series="lightcast_did_share_of_postings_by_experience", category=band,
                   value=r.value * 100, ci95_lo=round((r.value - 1.96 * r.ci95_halfwidth) * 100, 2),
                   ci95_hi=round((r.value + 1.96 * r.ci95_halfwidth) * 100, 2),
                   unit="pp change in share of postings (coef x100; CI = 1.96 x s.e.)", period="Aug 2020-Mar 2025",
                   note="annex table A2.12", source=rel(WB)))
li = pd.read_csv(LI)
li = li[li.country == "India"].copy()
li["year"] = li.month.str[:4].astype(int)
js = pd.read_csv(JS)
js["year"] = js.month.str[:4].astype(int)
for name, df, col, cov in [("linkedin_india_hiring_rate", li, "hiring_rate_idx_2016avg_eq_1", LI),
                           ("jobspeak_it_software_postings", js, "idx_it_software", JS)]:
    ann = df[df.year >= 2021].groupby("year").agg(v=(col, "mean"), n=(col, "count"),
                                                    last=("month", "max"))
    b = ann.at[2022, "v"]
    for y, r in ann.iterrows():
        pe.append(dict(panel="B", series=name, category=str(y), value=round(r.v / b, 3), ci95_lo=np.nan, ci95_hi=np.nan,
                       unit="annual mean, index 2022=1", period=f"{y} ({int(r.n)} months, to {r['last']})",
                       note=("hires (LinkedIn members), all industries" if "linkedin" in name
                             else "Naukri IT-Software postings index"),
                       source=rel(cov)))
ped = pd.DataFrame(pe)
out(ped, "postings_experience.csv")
l05 = ped[(ped.panel == "A") & (ped.category == "0-5 yrs")].iloc[0]
num("lightcast_0_5yr_effect", l05.value, "pct (log pts x100) per +1sd exposure", "Dec 2022-Mar 2025 vs before",
    rel(WB), "World Bank Fig 2.11F", -11.9, 0.05, note=f"95% CI {l05.ci95_lo} to {l05.ci95_hi}")
pb2 = ped[ped.panel == "B"].set_index(["series", "category"]).value
num("linkedin_india_2026_vs_2022", round((pb2[("linkedin_india_hiring_rate", "2026")] - 1) * 100, 1), "pct",
    "Jan-May 2026 mean vs 2022 mean", rel(LI), "annual-mean index")
num("jobspeak_it_2026_vs_2022", round((pb2[("jobspeak_it_software_postings", "2026")] - 1) * 100, 1), "pct",
    "Jan-Aug 2026 mean vs 2022 mean", rel(JS), "annual-mean index")

# ---------------------------------------------------------------------------
# 11. grad_unemp
# ---------------------------------------------------------------------------
GU = os.path.join(HC, "contradictions", "plfs", "grad_unemployment_variants.csv")
gu = pd.read_csv(GU)
gu = gu[(gu.sex == "persons") & gu.age.isin(["15_25", "21_25"])]
CON = {"ups": "principal status (usual)", "cws": "weekly status (current)", "upss": "official ps+ss (usual)"}
ug = []
for _, r in gu.iterrows():
    ug.append(dict(round=ROUND_LABEL[r["round"]], plot_date=ROUND_MID[r["round"]], age=r.age.replace("_", "-"),
                   concept=r.concept, concept_label=CON[r.concept], ur_pct=round(r.ur * 100, 1),
                   se_pct=round(r.se * 100, 2), ci90_lo_pct=round(r.ci90_lo * 100, 1), ci90_hi_pct=round(r.ci90_hi * 100, 1),
                   n_unemployed=r.n_unemp, n_labour_force=r.n_lf, flag=round_flag(r["round"], cluster=False),
                   note="graduates (degree and above); CY2025 fall shows on usual status only, not weekly",
                   source=rel(GU) + " (PLFS, NSO/MoSPI; aggregates)"))
ugd = pd.DataFrame(ug)
out(ugd, "grad_unemp.csv")
gz = ugd.set_index(["round", "age", "concept"]).ur_pct
num("grad_ur_15_25_ups_2023_24", gz[("2023-24", "15-25", "ups")], "pct", "2023-24", rel(GU), "principal status")
num("grad_ur_15_25_cws_2023_24", gz[("2023-24", "15-25", "cws")], "pct", "2023-24", rel(GU), "weekly status")
num("grad_ur_21_25_upss_cy2025", gz[("CY2025", "21-25", "upss")], "pct", "CY2025", rel(GU), "official ps+ss")
num("grad_ur_21_25_cws_cy2025", gz[("CY2025", "21-25", "cws")], "pct", "CY2025", rel(GU), "weekly status")

# ---------------------------------------------------------------------------
out(pd.DataFrame(NUMBERS), "numbers_jobs.csv")
bad = [n["key"] for n in NUMBERS if n["matches_brief"] == "NO"]
print("mismatches vs brief:", bad if bad else "none")
