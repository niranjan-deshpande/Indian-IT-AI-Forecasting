"""Build an IT-sector corporate labour-share proxy from RBI corporate statistics (DBIE).

Inputs (raw/rbi_corp/, text dumps captured in-browser from RBI DBIE SAP BO reports on 2026-10-15,
because the reports are JS-rendered and their export is a browser download):
  dbie_listed_annual_table2A/annual_YYYY-YY.txt
      'Performance of Listed Non-Government Non-Financial Companies - Sector-wise' (Annual), Table 2A.
      Each dump shows (prev FY, current FY) levels in Rs crore + y-o-y growth (common sample).
      Levels for a given FY are identical across the two reports that show it (checked FY24, FY25).
  dbie_listed_quarterly_table2A/quarterly_2026-27Q1.txt   (same, quarterly)
  dbie_ngnf_public_ltd_statement12_extract.json
      MCA-based 'Finances of NGNF Public Limited Companies', Statement 12 (industry-wise ratios).
  dbie_listed_annual_explanatory_notes_glossary.txt   (definitions)

Definitions (RBI glossary): Operating Profits = VOP - Expenditure (Expenditure includes staff cost,
raw material, power & fuel, other operating expenses; excludes depreciation & interest) = EBITDA
before other income. EBITDA (RBI) = Operating Profits + Other Income.

Primary proxy: labour_share = Staff Cost / (Staff Cost + Operating Profits)  (= staff cost share of
"operating value added" net of purchased inputs). Alternative: Staff / (Staff + RBI EBITDA incl. other income).

Run:  python3 -I extract_rbi_corp.py   (from this directory)
"""
import json
import os
import re

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw", "rbi_corp")
DBIE_LISTED_URL = ("https://data.rbi.org.in/DBIE/#/dbie/reports/Statistics/Corporate%20Sector/"
                   "Listed%20Non-Government%20Non-Financial%20Companies")
DBIE_PUBLTD_URL = ("https://data.rbi.org.in/DBIE/#/dbie/reports/Statistics/Corporate%20Sector/"
                   "Non-Government%20Non-Financial%20Public%20Limited%20Companies")
SECTORS = ["Manufacturing", "Services (Non-IT)", "IT"]

DEF_PRIMARY = "staff_cost / (staff_cost + operating_profit); operating_profit = VOP - expenditure (pre other income, pre D&A)"
DEF_ALT = "staff_cost / (staff_cost + EBITDA); RBI EBITDA = operating_profit + other_income"
COMMON_NOTES = ("Levels are for all listed NGNF companies with results for that period (company count varies by year; "
                "NOT a fixed panel); RBI's y-o-y growth uses a common sample. Ind AS 116 (leases) from FY2019-20 moves "
                "lease rent out of expenditure into depreciation/interest, raising operating profit and lowering this "
                "proxy by roughly 1-2 pp from FY20 onward. Staff cost includes ESOP/share-based pay and onsite/overseas "
                "staff of Indian-listed IT firms (standalone accounts as filed with exchanges).")


def num(s):
    s = s.strip()
    if s in ("-", "", "@", "$"):
        return None
    return float(s.replace(",", ""))


def parse_dump(path):
    """Return dict[(sector, period)] -> {item: (level, growth)}."""
    lines = [l.strip() for l in open(path, encoding="utf-8").read().splitlines() if l.strip()]
    sectors = [s.strip() for s in lines[0].split("|")]
    assert sectors == SECTORS, sectors
    periods = [p.strip() for p in lines[1].split("|")[1:]]
    nper = len(periods) // len(sectors)
    ncos = [num(x) for x in lines[2].split("|")[1:]]
    out = {}
    for si, sec in enumerate(sectors):
        for pi in range(nper):
            k = si * nper + pi
            out[(sec, periods[k])] = {"n_companies": ncos[k]}
    for line in lines[3:]:
        parts = [p.strip() for p in line.split("|")]
        item, vals = parts[0], parts[1:]
        assert len(vals) == 2 * len(periods), (path, item, len(vals))
        for si, sec in enumerate(sectors):
            for pi in range(nper):
                k = si * nper + pi
                out[(sec, periods[k])][item] = (num(vals[2 * k]), num(vals[2 * k + 1]))
    return out


def listed_rows():
    data = {}
    src_of = {}
    d = os.path.join(RAW, "dbie_listed_annual_table2A")
    for fn in sorted(os.listdir(d)):
        m = re.match(r"annual_(\d{4}-\d{2})\.txt$", fn)
        if not m:
            continue
        for key, rec in parse_dump(os.path.join(d, fn)).items():
            if key in data:  # same FY shown in two reports: check identical levels
                a, b = data[key], rec
                for it in ("Staff Cost", "Operating Profits", "Sales"):
                    assert a[it][0] == b[it][0], (key, it, a[it], b[it])
                continue
            data[key] = rec
            src_of[key] = fn
    rows = []
    for (sec, fy), r in sorted(data.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        staff, op, ebitda, oi, sales = (r["Staff Cost"][0], r["Operating Profits"][0], r["EBITDA"][0],
                                        r["Other Income"][0], r["Sales"][0])
        g_staff, g_op = r["Staff Cost"][1], r["Operating Profits"][1]
        rel = f"report year {src_of[(sec, fy)][7:14]}"
        base = dict(
            source=("RBI DBIE 'Performance of Listed Non-Government Non-Financial Companies - Sector-wise' (Annual), "
                    "data releases 'Performance of Private Corporate Business Sector during <FY>'; accessed 2026-10-15"),
            sample=f"{int(r['n_companies'])} listed non-govt non-financial companies, sector = {sec}",
            fy=fy, staff_cost=staff, ebitda_or_operating_profit=op, unit="INR crore",
            n_companies=int(r["n_companies"]), source_url=DBIE_LISTED_URL,
            table_id=f"Table 2A (Sector-wise, Annual), {rel}; raw/rbi_corp/dbie_listed_annual_table2A/{src_of[(sec, fy)]}",
        )
        note = (f"sales={sales:,.0f}; other_income={oi:,.0f}; RBI EBITDA={ebitda:,.0f}; common-sample y-o-y growth: "
                f"staff {g_staff}%, operating profit {g_op}%. " + COMMON_NOTES)
        rows.append(dict(base, value_added=staff + op, labour_share=staff / (staff + op),
                         labour_share_definition=DEF_PRIMARY, notes=note))
        if sec == "IT":
            rows.append(dict(base, ebitda_or_operating_profit=ebitda, value_added=staff + ebitda,
                             labour_share=staff / (staff + ebitda), labour_share_definition=DEF_ALT, notes=note))
    # quarterly (latest quarter)
    qd = os.path.join(RAW, "dbie_listed_quarterly_table2A")
    for fn in sorted(os.listdir(qd)):
        for (sec, per), r in parse_dump(os.path.join(qd, fn)).items():
            if sec != "IT":
                continue
            staff, op = r["Staff Cost"][0], r["Operating Profits"][0]
            rows.append(dict(
                source=("RBI DBIE 'Performance of Listed Non-Government Non-Financial Companies - Sector-wise' "
                        "(Quarterly), report for Q1:2026-27; accessed 2026-10-15"),
                sample=f"{int(r['n_companies'])} listed non-govt non-financial companies, sector = IT",
                fy=per, staff_cost=staff, ebitda_or_operating_profit=op, value_added=staff + op, unit="INR crore",
                labour_share=staff / (staff + op), labour_share_definition=DEF_PRIMARY,
                n_companies=int(r["n_companies"]), source_url=DBIE_LISTED_URL,
                table_id=f"Table 2A (Sector-wise, Quarterly); raw/rbi_corp/dbie_listed_quarterly_table2A/{fn}",
                notes=(f"Quarterly, not annualised; y-o-y growth (common sample): staff {r['Staff Cost'][1]}%, "
                       f"operating profit {r['Operating Profits'][1]}%. " + COMMON_NOTES)))
    return rows


def publtd_rows():
    j = json.load(open(os.path.join(RAW, "dbie_ngnf_public_ltd_statement12_extract.json"), encoding="utf-8"))
    rows = []
    for v in j["vintages"]:
        m = re.search(r"Select ([\d,]+) Public Limited Companies.*?(\d{4}-\d{2}) to (\d{4}-\d{2})", v["title"])
        ntot, y0, y1 = m.group(1), m.group(2), m.group(3)
        for ind in ("Information and communication", "Computer Services"):
            if ind not in v:
                continue
            rec = v[ind]
            years = rec["years"].split(",")
            rem = [float(x) for x in rec["rem"].split(",")]
            op = [float(x) for x in rec["op"].split(",")]
            for fy, r_te, o in zip(years, rem, op):
                r_te, o = r_te / 100, o / 100
                staff_sales = r_te * (1 - o)  # TE/sales ~ 1 - OP/sales (ignores D&A, interest, other op. revenue)
                rows.append(dict(
                    source=(f"RBI 'Finances of Non-Government Non-Financial Public Limited Companies, {y1}' (MCA "
                            f"audited accounts; {ntot} companies, {y0} to {y1}); DBIE Statement 12, tab {v['tab']}"),
                    sample=(f"{rec['n']} NGNF public limited companies (listed + unlisted), industry = {ind}"
                            + (" (NIC 2008 section J: publishing, broadcasting, telecom, IT & information services)"
                               if ind.startswith("Information") else " (Indian-GAAP-era classification)")),
                    fy=fy, staff_cost=round(staff_sales * 100, 2), ebitda_or_operating_profit=o * 100,
                    value_added=round((staff_sales + o) * 100, 2), unit="per cent of sales (derived)",
                    labour_share=staff_sales / (staff_sales + o),
                    labour_share_definition=("DERIVED: r=(remuneration/total expenditure)*(1 - OP/sales) approximates "
                                             "remuneration/sales; labour_share = r/(r + OP/sales)"),
                    n_companies=int(rec["n"]), source_url=DBIE_PUBLTD_URL,
                    table_id=("Statement 12: Select Financial Ratios ... Industry-wise (rows 'Remuneration to employees "
                              "to total expenditure', 'Operating profit to sales'); "
                              "raw/rbi_corp/dbie_ngnf_public_ltd_statement12_extract.json"),
                    notes=(f"Published ratios: remuneration/total expenditure={r_te*100:.1f}%, OP/sales={o*100:.1f}%. "
                           "Approximation ignores depreciation+interest in total expenditure (understates remuneration/"
                           "sales by roughly (D&A+interest)/sales x rem/TE, i.e. biases the share down ~1-3 pp). "
                           "Each vintage is its own 3-year common sample; sample changes across vintages. "
                           + ("Includes telecom (capital-intensive, high OP margin) so the level is well below pure IT."
                              if ind.startswith("Information") else
                              "Historical Indian-GAAP sample of many small unlisted firms; erratic year to year."))))
    return rows


def main():
    rows = listed_rows() + publtd_rows()
    cols = ["source", "sample", "fy", "staff_cost", "ebitda_or_operating_profit", "value_added", "unit",
            "labour_share", "labour_share_definition", "n_companies", "source_url", "table_id", "notes"]
    df = pd.DataFrame(rows)[cols]
    df["labour_share"] = df["labour_share"].round(4)
    df.to_csv(os.path.join(HERE, "rbi_corp_it_labour_share.csv"), index=False)
    it = df[df["sample"].str.endswith("sector = IT")]
    show = it.pivot_table(index="fy", columns="labour_share_definition", values="labour_share", aggfunc="first")
    show.columns = ["ls_staff_over_staff+EBITDA_incl_OI", "ls_staff_over_staff+OP"]
    print(show.round(3).to_string())
    lst = df[df["sample"].str.contains("sector = ") & (df["labour_share_definition"] == DEF_PRIMARY)]
    lst = lst.assign(sector=lst["sample"].str.split("sector = ").str[1])
    print(lst.pivot_table(index="fy", columns="sector", values="labour_share", aggfunc="first").round(3).to_string())
    pl = df[df["unit"].str.startswith("per cent")]
    pl = pl.assign(vintage=pl["source"].str.extract(r"Companies, (\d{4}-\d{2})")[0],
                   industry=pl["sample"].str.extract(r"industry = ([A-Za-z ]+)")[0])
    print(pl.pivot_table(index="fy", columns=["industry", "vintage"], values="labour_share").round(3).to_string())


if __name__ == "__main__":
    main()
