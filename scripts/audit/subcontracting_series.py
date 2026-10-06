"""Subcontracting cost as % of revenue, Indian IT-services firms, from data/tidy/panel_long.csv.

Writes audit/subcontracting_series.csv (new file; nothing existing is modified).

Rows:
  period_type = "quarter"      one row per firm x series x calendar quarter
  period_type = "fiscal_year"  sum of the 4 quarters of an Indian fiscal year (Apr-Mar) for the same series;
                               written only if all 4 quarters of both numerator and denominator exist
                               (n_q < 4 rows are written with subcon_pct_rev empty, so gaps are visible).
Units: subcon_inr and rev_inr in INR million (INR crore x10, INR lakh x0.1). Both are consolidated, from the
same firm's own filings. YoY change (pp) is computed within a series only (never across definition breaks).

Series per firm (primary = the one used for the headline table):
  tcs      cor_plus_sga  "Fees to external consultants" in cost of revenue + in SG&A (IFRS fact sheet), Q1FY12-Q4FY26 [primary]
           cor_only      the cost-of-revenue line alone (alternative; SG&A fees include non-delivery consultants)
           expense_by_nature  single "Fees to External consultants" line, Q1FY26-Q1FY27 (Q1FY27 deck only).
                         DEFINITION BREAK: Q4FY26 EBN = INR 3,971 cr vs COR+SG&A = INR 4,238 cr. Primary for Q1FY27 only.
  infosys  reported      "Cost of technical sub-contractors" (IFRS INR statements)
  hcltech  reported      "Outsourcing costs" (SEBI Ind AS P&L; = "Subcontractors + Outsourced Work" in IR cost breakup)
  wipro    reported      "Sub-contracting and technical fees" (IFRS note, expenses by nature)
  techm    reported      "Subcontracting Expense(s)"; before Q4FY17 "Services rendered by Business Associates & Others"
  mindtree reported      "Sub-contractor charges", Q4FY21-Q2FY23 only (pre-merger Mindtree)
  ltim / lti: no subcontracting line in quarterly filings. ltim "annual_report" rows FY22-FY26 are hand-entered
           from the annual reports (Board's Report table) - see LTIM_ANNUAL; they are NOT in data/tidy.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
TIDY = ROOT / "data" / "tidy"
OUT = ROOT / "audit" / "subcontracting_series.csv"

TO_MN = {"INR_mn": 1.0, "INR_cr": 10.0, "INR_lakh": 0.1}


def fiscal_q(cal_q):
    """Indian fiscal year ends 31 March: 2026Q2 (Apr-Jun 2026) -> Q1FY27."""
    y, q = int(cal_q[:4]), int(cal_q[-1])
    return f"Q{q - 1}FY{(y + 1) % 100:02d}" if q > 1 else f"Q4FY{y % 100:02d}"


def fiscal_year(cal_q):
    y, q = int(cal_q[:4]), int(cal_q[-1])
    return f"FY{(y + 1) % 100:02d}" if q > 1 else f"FY{y % 100:02d}"


def series(p, firm, metric, dims):
    """INR-million quarterly series for the first available dimension in `dims` (per quarter)."""
    x = p[(p.firm == firm) & (p.metric == metric) & (p.period_type == "quarter") & p.unit.isin(TO_MN)].copy()
    x["rank"] = x.dimension.map({d: i for i, d in enumerate(dims)})
    x = x[x["rank"].notna()]
    x["v"] = x.value * x.unit.map(TO_MN)
    # within a quarter prefer the listed dimension order, then INR_mn/INR_cr over INR_lakh (same number, coarser unit)
    x["urank"] = x.unit.map({"INR_mn": 0, "INR_cr": 1, "INR_lakh": 2})
    x = x.sort_values(["rank", "urank"]).drop_duplicates("cal_q")
    return x.set_index("cal_q")[["v", "source_url", "source_doc", "source_loc", "unit"]]


SPEC = {
    # firm: list of (series_name, [subcon dims], combine, primary_quarters_rule, definition text)
    "tcs": [
        ("cor_plus_sga", None, "Fees to external consultants: cost of revenue + SG&A lines (IFRS 'COR - SG&A Details')"),
        ("cor_only", ["Fees to external consultants (in cost of revenue)", "Fees to external consultants (COR)"],
         "Fees to external consultants: cost-of-revenue line only"),
        ("expense_by_nature", ["Fees to external consultants (expense by nature)"],
         "Fees to External consultants, 'Expense by Nature' table (Q1FY27 deck); NOT comparable with COR+SG&A"),
    ],
    "infosys": [("reported", ["total"], "Cost of technical sub-contractors (IFRS, consolidated)")],
    "hcltech": [("reported", ["total"], "Outsourcing costs (Ind AS consolidated P&L)")],
    "wipro": [("reported", ["total"], "Sub-contracting and technical fees (IFRS note, consolidated)")],
    "techm": [("reported", ["total"], "Subcontracting expenses (pre-Q4FY17: Services rendered by Business Associates & Others)")],
    "mindtree": [("reported", ["total"], "Sub-contractor charges (pre-merger Mindtree, consolidated)")],
}


# LTIMindtree (renamed LTM Limited in FY26) does not break out sub-contracting in quarterly results, but the Board's
# Report "Financial Results" table of each Integrated Annual Report does (consolidated, INR mn, revenue from operations).
# NOT in data/tidy: hand-entered here from the PDFs (checked with pdftotext on 2026-10-05). FY22 is the merged-entity
# comparative printed in the FY23 report (LTI + Mindtree combined).
LTIM_ANNUAL = [
    # fiscal_year, subcon, revenue from operations, line label, source URL (report, comparative column?)
    ("FY22", 23591, 261087, "Sub-contractor expenses",
     "https://www.ltm.com/content/dam/ltimcorporatewebsite/annual-reports-2023/pdfs/board-report-ar.pdf (FY23 Board's Report, Financial Results table, consolidated 2021-22 comparative column)"),
    ("FY23", 28286, 331830, "Sub-contractor expenses",
     "https://www.ltm.com/content/dam/ltimcorporatewebsite/annual-reports-2023/pdfs/board-report-ar.pdf (FY23 Board's Report, Financial Results table, consolidated 2022-23)"),
    ("FY24", 25599, 355170, "Sub-contracting expenses",
     "https://www.ltm.com/annual-report-2025/pdfs/ltm-ir-2024-25-board-report.pdf (FY25 Board's Report, Financial Results table, consolidated 2023-24 comparative column)"),
    ("FY25", 26312, 380081, "Sub-contracting expenses",
     "https://www.ltm.com/annual-report-2026/ltm-limited-iar-2025-26-boards-report.pdf (FY26 Board's Report, Financial Results table, consolidated 2024-25 comparative column; matches FY25 report)"),
    ("FY26", 32369, 423076, "Sub-contracting expenses",
     "https://www.ltm.com/annual-report-2026/ltm-limited-iar-2025-26-boards-report.pdf (FY26 Board's Report, Financial Results table, consolidated 2025-26)"),
]


def build():
    p = pd.read_csv(TIDY / "panel_long.csv", low_memory=False)
    for c in ["dimension", "unit", "period_type"]:
        p[c] = p[c].fillna("na").astype(str)
    rows = []
    for firm, specs in SPEC.items():
        rev = series(p, firm, "revenue", ["total"])
        for name, dims, definition in specs:
            if firm == "tcs" and name == "cor_plus_sga":
                a = series(p, firm, "subcontracting_cost",
                           ["Fees to external consultants (in cost of revenue)", "Fees to external consultants (COR)"])
                b = series(p, firm, "subcontracting_cost",
                           ["Fees to external consultants (in SG&A)", "Fees to external consultants (SG&A)"])
                idx = a.index.intersection(b.index)
                s = a.loc[idx].copy()
                s["v"] = a.loc[idx, "v"] + b.loc[idx, "v"]
                s["source_loc"] = "COR line + SG&A line (summed here)"
            else:
                s = series(p, firm, "subcontracting_cost", dims)
            for q, r in s.iterrows():
                rv = rev.loc[q] if q in rev.index else None
                rows.append(dict(
                    firm=firm, series=name, period_type="quarter", cal_q=q, fiscal_q=fiscal_q(q),
                    fiscal_year=fiscal_year(q), n_q=1,
                    subcon_inr=r.v, rev_inr=(rv.v if rv is not None else np.nan), units="INR_mn",
                    subcon_unit_as_reported=r.unit, definition=definition,
                    subcon_src=r.source_url, subcon_doc=r.source_doc, subcon_loc=r.source_loc,
                    rev_src=(rv.source_url if rv is not None else ""),
                    rev_doc=(rv.source_doc if rv is not None else "")))
    q = pd.DataFrame(rows)
    q["subcon_pct_rev"] = 100 * q.subcon_inr / q.rev_inr

    # primary flag: one series per firm-quarter for the headline table
    q["primary"] = q.series.eq("reported")
    tcs = q.firm.eq("tcs")
    q.loc[tcs & q.series.eq("cor_plus_sga"), "primary"] = True
    q.loc[tcs & q.series.eq("expense_by_nature") & q.cal_q.eq("2026Q2"), "primary"] = True

    # YoY change in pp, within series
    def lag4(cq):
        y, n = int(cq[:4]), int(cq[-1])
        return f"{y - 1}Q{n}"
    key = q.set_index(["firm", "series", "cal_q"]).subcon_pct_rev
    q["yoy_pp"] = [key.get((f, s, lag4(c)), np.nan) for f, s, c in zip(q.firm, q.series, q.cal_q)]
    q["yoy_pp"] = q.subcon_pct_rev - q.yoy_pp

    # fiscal-year aggregates (complete years only get a ratio)
    ann = []
    for (f, s, fy), g in q.groupby(["firm", "series", "fiscal_year"]):
        ok = g.subcon_inr.notna() & g.rev_inr.notna()
        n = int(ok.sum())
        sub, rv = g.loc[ok, "subcon_inr"].sum(), g.loc[ok, "rev_inr"].sum()
        ann.append(dict(firm=f, series=s, period_type="fiscal_year", cal_q="", fiscal_q=fy, fiscal_year=fy, n_q=n,
                        subcon_inr=sub if n == 4 else np.nan, rev_inr=rv if n == 4 else np.nan, units="INR_mn",
                        subcon_pct_rev=100 * sub / rv if n == 4 else np.nan,
                        definition=g.definition.iloc[0],
                        subcon_src="sum of quarterly rows (see quarter rows for each source)",
                        primary=(s != "cor_only" and s != "expense_by_nature")))
    for fy, sub, rv, label, src in LTIM_ANNUAL:
        ann.append(dict(firm="ltim", series="annual_report", period_type="fiscal_year", cal_q="", fiscal_q=fy,
                        fiscal_year=fy, n_q=np.nan, subcon_inr=float(sub), rev_inr=float(rv), units="INR_mn",
                        subcon_pct_rev=100 * sub / rv,
                        definition=f"{label} (Board's Report, consolidated; denominator = revenue from operations); "
                                   "HAND-ENTERED, not in data/tidy",
                        subcon_unit_as_reported="INR_mn", subcon_src=src, rev_src=src, primary=True))
    a = pd.DataFrame(ann)
    a["fy_num"] = a.fiscal_year.str[2:].astype(int)
    a = a.sort_values(["firm", "series", "fy_num"])
    a["yoy_pp"] = a.groupby(["firm", "series"]).apply(
        lambda g: g.subcon_pct_rev - g.set_index("fy_num").subcon_pct_rev.reindex(g.fy_num - 1).values,
        include_groups=False).reset_index(level=[0, 1], drop=True)
    a = a.drop(columns="fy_num")

    out = pd.concat([q.sort_values(["firm", "series", "cal_q"]), a], ignore_index=True)
    cols = ["firm", "series", "primary", "period_type", "cal_q", "fiscal_q", "fiscal_year", "n_q", "subcon_inr",
            "rev_inr", "units", "subcon_pct_rev", "yoy_pp", "definition", "subcon_unit_as_reported", "subcon_src",
            "subcon_doc", "subcon_loc", "rev_src", "rev_doc"]
    out = out[cols]
    for c in ["subcon_pct_rev", "yoy_pp"]:
        out[c] = out[c].round(3)
    OUT.parent.mkdir(exist_ok=True)
    out.to_csv(OUT, index=False)
    return out


if __name__ == "__main__":
    out = build()
    a = out[(out.period_type == "fiscal_year") & out.primary]
    t = a.pivot(index="fiscal_year", columns="firm", values="subcon_pct_rev")
    t = t.loc[sorted(t.index, key=lambda s: int(s[2:]))]
    print(t.round(1).to_string())
    print("rows:", len(out), "->", OUT)
