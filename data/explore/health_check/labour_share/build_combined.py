"""Combine all labour-share measures into one long tidy file + chart-ready tables.

Inputs (all in this folder, built by the other scripts):
  firm_labour_share.csv, rbi_corp_it_labour_share.csv, nas_enterprise_labour_share.csv,
  klems_labour_share.csv, plfs_it_wagebill_approx.csv, plfs_it_real_earnings.csv
Outputs:
  labour_share_combined.csv   long: measure, scope, fy, labour_share, numerator, denominator, unit, source_url, note
  chart1_labour_share_measures.csv  wide FY x measure (main candidate chart)
  chart2_substack_replication.csv   PLFS wage bill / NAS IT GVA (old and new base) vs firm/RBI measures
  chart3_real_earnings_juniors.csv  real median & mean earnings by age band, IT vs all graduates

Run: python3 -I build_combined.py
"""
from pathlib import Path

import pandas as pd

H = Path(__file__).resolve().parent
rows = []


def fy_label(fy):
    """'FY24' / '2023-24' / '2023-24 (Provisional)' -> '2023-24'."""
    s = str(fy).strip()
    if s.startswith("FY"):
        y = 2000 + int(s[2:])
        return f"{y-1}-{str(y)[2:]}"
    return s.split(" ")[0]


# 1. firm-level (consolidated, global)
f = pd.read_csv(H / "firm_labour_share.csv")
for firm, lab in [("top6_sum", "Top-6 firms (consolidated, global)"), ("mid3_sum", "Mid-tier 3 (Persistent, Coforge, Mphasis)")]:
    for r in f[f.firm.eq(firm)].itertuples():
        rows.append(dict(measure=f"firm_{firm}", label=lab, scope="employee benefit expense / (employee cost + EBITDA); consolidated",
                         fy=fy_label(r.fy), labour_share=r.labour_share_va, numerator=r.employee_cost_inr_cr,
                         denominator=r.value_added_inr_cr, unit="INR crore", source_url=r.source_url, note=r.notes))

# 2. RBI listed IT companies (DBIE sector-wise, annual), operating-profit definition
rb = pd.read_csv(H / "rbi_corp_it_labour_share.csv")
ann = rb[rb.source.str.contains(r"\(Annual\)") & rb["sample"].str.contains("sector = IT")]
for defn, tag in [("operating_profit = VOP", "rbi_listed_it_op"), ("RBI EBITDA = operating_profit + other_income", "rbi_listed_it_ebitda")]:
    for r in ann[ann.labour_share_definition.str.contains(defn, regex=False)].itertuples():
        rows.append(dict(measure=tag, label="RBI: listed non-govt non-financial IT companies" + (" (EBITDA incl. other income)" if "ebitda" in tag else ""),
                         scope=r.labour_share_definition, fy=fy_label(r.fy), labour_share=r.labour_share, numerator=r.staff_cost,
                         denominator=r.value_added, unit=r.unit, source_url=r.source_url, note=f"n={r.n_companies}; {r.notes}"))

# 3. NAS: broad group CE/GVA (private corporations; all sectors ex dwellings)
n = pd.read_csv(H / "nas_enterprise_labour_share.csv")
for src, base in [("NAS2025_2011base", "2011-12 base"), ("NAS2026_2022base", "2022-23 base")]:
    pc = n[n.source.eq(src) & n.table_id.str.contains("7.1B", na=False)]
    for r in pc.itertuples():
        rows.append(dict(measure=f"nas_group_privcorp_{base[:4]}", label=f"NAS: real estate+dwellings+professional services, private corporations ({base})",
                         scope="CE / GVA at basic prices", fy=r.fy, labour_share=r.labour_share, numerator=r.ce_inr_crore,
                         denominator=r.gva_inr_crore, unit="INR crore", source_url=r.source_url, note=r.table_id))
    ex = n[n.source.eq(src) & n.industry_label.str.startswith("DERIVED")]
    for r in ex.itertuples():
        rows.append(dict(measure=f"nas_group_exdwell_{base[:4]}", label=f"NAS: same group, all sectors, minus ownership of dwellings ({base})",
                         scope="CE / (group GVA - dwellings GVA)", fy=r.fy, labour_share=r.labour_share, numerator=r.ce_inr_crore,
                         denominator=r.gva_inr_crore, unit="INR crore", source_url=r.source_url, note=r.notes))

# 4. KLEMS business services (latest release)
k = pd.read_csv(H / "klems_labour_share.csv")
rel = [s for s in k.source_release.unique() if "July 2024" in s][0]
for r in k[k.source_release.eq(rel) & k.industry_label.eq("Business Service")].itertuples():
    rows.append(dict(measure="klems_business_services", label="India KLEMS: Business services (labour income incl. imputed self-employed)",
                     scope="labour income / nominal GVA", fy=fy_label(r.fy), labour_share=r.labour_share, numerator=r.labour_comp_inr_crore,
                     denominator=r.gva_nominal_inr_crore, unit="INR crore", source_url=r.source_url, note=rel))

# 5. ASUSE information & communication, hired-worker establishments
for r in n[n.source.str.startswith("ASUSE") & n.industry_label.str.contains("HWE")].itertuples():
    rows.append(dict(measure="asuse_ic_hwe", label="ASUSE: unincorporated info & communication, hired-worker establishments",
                     scope="emoluments / GVA", fy=r.fy, labour_share=r.labour_share, numerator=r.ce_inr_crore,
                     denominator=r.gva_inr_crore, unit="INR crore", source_url=r.source_url, note="tiny sector; excludes employer PF/ESIC"))

# 6. Substack replication: PLFS wage bill (approx, repo aggregates) / NAS IT GVA (Statement 8.13 item 3, current prices)
wb = pd.read_csv(H / "plfs_it_wagebill_approx.csv").set_index("round").wage_bill_inr_crore_approx
it = n[n.industry_label.eq("Information and computer related services") & n.price_basis.eq("current")]
for src, base, pair in [("NAS2025_2011base", "2011", {}), ("NAS2026_2022base", "2022", {"2024-25": "cy2025"})]:
    for r in it[it.source.eq(src)].itertuples():
        rnd = pair.get(r.fy, r.fy)
        if rnd in wb.index:
            rows.append(dict(measure=f"plfs_wagebill_over_nas_it_gva_{base}", label=f"PLFS wage bill (approx) / NAS IT GVA ({base} base) - Substack method",
                             scope="survey take-home earnings x employment x 12 / GVA", fy=r.fy, labour_share=round(wb[rnd] / r.gva_inr_crore, 4),
                             numerator=wb[rnd], denominator=r.gva_inr_crore, unit="INR crore", source_url=r.source_url,
                             note=f"PLFS round {rnd}; wage bill from plfs_it_wagebill_approx.csv"))

c = pd.DataFrame(rows)
c["labour_share"] = c.labour_share.astype(float).round(4)
c.to_csv(H / "labour_share_combined.csv", index=False)

w = c.pivot_table(index="fy", columns="measure", values="labour_share").sort_index()
w = w[w.index >= "2011-12"]
w.to_csv(H / "chart1_labour_share_measures.csv")
pd.set_option("display.width", 250)
print(w.round(3).to_string())

# chart 2: Substack replication table
nasit = it.pivot_table(index="fy", columns="source", values="gva_inr_crore")
rep = nasit.join(w[[x for x in w.columns if x.startswith("plfs_") or x in ("firm_top6_sum", "rbi_listed_it_op")]], how="left")
rep.to_csv(H / "chart2_substack_replication.csv")
print(rep.round(3).to_string())

# chart 3: real earnings
e = pd.read_csv(H / "plfs_it_real_earnings.csv")
e = e[e["sample"].isin(["cws_regular_nic62_63", "cws_regular_all_grads"])]
e3 = e[["round", "sample", "age_band", "median_real_cy2025_inr", "mean_real_cy2025_inr", "n_unweighted", "median_inr", "mean_inr", "cpi_period_avg"]]
e3.to_csv(H / "chart3_real_earnings_juniors.csv", index=False)
