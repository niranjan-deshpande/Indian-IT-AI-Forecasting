"""Writes ROOT/audit/corrections_1b.csv (audit Task 1b findings that change or flag data values).

Every replace value is computed from primary-source numbers already in data/raw (cited per row); old values are read
from the current tidy files so that build_corrected.py's old_value assertion is meaningful.
"""
import numpy as np
import pandas as pd
from audit_common import AUD, ROOT, load_yoy, load_core, indian_fiscal

yoy, core = load_yoy(), load_core()
raw = pd.read_csv(ROOT / "data" / "raw" / "accenture.csv", low_memory=False, dtype={"cal_q": str})
net = raw[(raw.metric == "revenue") & (raw.dimension == "total") & (raw.period_type == "quarter")
          & raw.notes.str.contains("Net revenues", na=False)]


def yv(f, q, c):
    return float(yoy[(yoy.firm == f) & (yoy.cal_q == q)][c].iloc[0])


def cv(f, q, c):
    return float(core[(core.firm == f) & (core.cal_q == q)][c].iloc[0])


rows = []
ACN = [("2017Q4", "Q1FY18", "Q1FY17"), ("2018Q1", "Q2FY18", "Q2FY17"), ("2018Q2", "Q3FY18", "Q3FY17"), ("2018Q3", "Q4FY18", "Q4FY17")]
for q, fq, fq0 in ACN:
    cur = net[(net.fiscal_q == fq) & (net.source_loc == "Summary of Revenues (three months)")].iloc[0]
    prev = net[(net.fiscal_q == fq0) & (net.source_url == cur.source_url)].iloc[0]       # prior-year column, same release
    new = 100 * np.log(cur.value / prev.value)
    rows.append(dict(firm="accenture", cal_q=q, fiscal_q=fq, column="gR_usd", dimension="total",
                     old_value=f"{yv('accenture', q, 'gR_usd'):.4f}", new_value=f"{new:.4f}", action="replace",
                     reason="ASC 606 basis mix: tidy rev_usd for FY18 quarters is the restated post-ASC 606 vintage (incl. reimbursements, from FY19 releases) "
                            "while the FY17 base is net revenues; gR_usd = log(gross_FY18/net_FY17) overstates USD growth by ~3.5-4pp. "
                            "Replaced by the like-for-like log change of net revenues printed in the same FY18 release (current and prior-year columns). "
                            "Applied at yoy level because no single level series is consistent across FY18 (FY19 growth needs the gross FY18 level).",
                     source_url=cur.source_url,
                     source_loc="Summary of Revenues (three months), current and prior-year columns",
                     evidence=f"net revenues {fq} {cur.value:.3f} vs {fq0} {prev.value:.3f} USD mn (release reports USD growth {cv('accenture', q, 'rev_rep_yoy'):.0f}%); "
                              f"tidy rev_usd {fq} = {cv('accenture', q, 'rev_usd'):.3f} (post-ASC 606 restated)"))

rows.append(dict(firm="wipro", cal_q="2018Q3", fiscal_q="Q2FY19", column="headcount", dimension="total",
                 old_value=f"{cv('wipro', '2018Q3', 'headcount'):.0f}", new_value="", action="flag_only",
                 reason="Level step of ~9,000 employees transferred with the Alight deal (rebadging, company says not inorganic); "
                        "raises Wipro gL by ~5pp in 2018Q3-2019Q2. Value is correct as reported; not adjusted (no DIVEST-style adjustment exists for inflows).",
                 source_url="https://www.wipro.com/content/dam/nexus/en/investor/quarterly-results/2018-2019/q2fy19/transcripts-conference-call-q2-fy19.pdf",
                 source_loc="p15 (CFO/analyst Q&A)",
                 evidence="'There is no inorganic component, it is all organic. About 9000 employees come for the large deal which we had won from Alight'"))

for q in ["2024Q3", "2024Q4", "2025Q1", "2025Q2"]:
    rows.append(dict(firm="hcltech", cal_q=q, fiscal_q=indian_fiscal(q), column="gR", dimension="total",
                     old_value=f"{yv('hcltech', q, 'gR'):.4f}", new_value="", action="flag_only",
                     reason="Reported cc YoY includes the revenue effect of the Q1/Q2FY25 divestiture (base not adjusted), while gL has the D10 base "
                            "adjustment: gR and gL are on different perimeters for these 4 quarters, so gRPE/resid are biased down by the (unquantified) divested revenue share.",
                     source_url="https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech_Q4_FY25_Investor_Release.pdf",
                     source_loc="p15, footnote to vertical mix table",
                     evidence="'Financial Services includes the impact of a divestiture in Q2 FY25'; headcount: Q1FY25 release p3 'Reduction in headcount due to divestiture (7,398)'"))

for q, url, loc in [("2024Q4", "https://www.sec.gov/Archives/edgar/data/1058290/000105829025000007/exhibit99212312024.htm", "earnings supplement (Ex.99.2) revenue footnote"),
                    ("2025Q1", "https://www.sec.gov/Archives/edgar/data/1058290/000105829025000124/exhibit9923312025.htm", "earnings supplement (Ex.99.2) revenue footnote"),
                    ("2025Q2", "https://www.sec.gov/Archives/edgar/data/1058290/000105829025000266/exhibit9926302025.htm", "earnings supplement (Ex.99.2) footnote 1")]:
    rows.append(dict(firm="cognizant", cal_q=q, fiscal_q=q, column="gR", dimension="total",
                     old_value=f"{yv('cognizant', q, 'gR'):.4f}", new_value="", action="flag_only",
                     reason="Inorganic: Belcan (and Thirdera) add ~4pp to YoY revenue growth (D12, not adjusted). Comparator growth gap vs Indian firms is biased.",
                     source_url=url, source_loc=loc,
                     evidence="Q2 2025: 'revenue from our recently completed acquisition of Belcan contributed approximately 4 percentage points to year-over-year revenue growth'; "
                              "Q1 2025: 'Belcan and Thirdera contributed approximately 4 percentage points'"))

# sign errors from the '(x.x)%' parsing bug in scripts/extract/ltim_parse_tables.parse_num (see ltim_sign_scan.py)
scan = pd.read_csv(AUD / "ltim_sign_scan.csv")
x = pd.read_csv(ROOT / "data" / "raw" / "ltim.csv", low_memory=False, dtype={"cal_q": str})
for r in scan[scan.verdict == "negative_printed"].itertuples():
    src = x[(x.firm == r.firm) & (x.fiscal_q == r.fiscal_q) & (x.metric == r.metric) & (x.dimension == r.dimension)
            & (x.basis == r.basis) & (x.doc_date == r.doc_date) & ((x.value - r.value).abs() < 1e-9)].iloc[0]
    rows.append(dict(firm=r.firm, cal_q=r.cal_q, fiscal_q=r.fiscal_q, column=r.metric, dimension=r.dimension,
                     old_value=f"{r.value:.1f}", new_value=f"{-abs(r.value):.1f}", action="replace",
                     reason="Sign error: the document prints a negative growth as '(x.x)%', which parse_num in "
                            "scripts/extract/ltim_parse_tables.py reads as positive (it only recognises '(x)' and '(x%)').",
                     source_url=r.source_url, source_loc=r.source_loc, evidence=f"printed token {r.printed!r} in the cited table row",
                     basis=src.basis, unit=src.unit, period_type=src.period_type, doc_date=r.doc_date))

out = pd.DataFrame(rows).reindex(columns=["firm", "cal_q", "fiscal_q", "column", "dimension", "old_value", "new_value", "action", "reason",
                                          "source_url", "source_loc", "evidence", "basis", "unit", "period_type", "doc_date"])
out.to_csv(AUD / "corrections_1b.csv", index=False)
print(out[["firm", "cal_q", "column", "old_value", "new_value", "action"]].to_string())
