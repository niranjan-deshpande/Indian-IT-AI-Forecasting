"""Extract India KLEMS (RBI) nominal GVA and labour income share for Business Services
(71t74, which contains computer & related activities / IT services), Post & Telecom (64),
the services aggregate and the total economy.

KLEMS does not publish labour compensation in levels. Labour income = LSH_va x VA (current prices).
LSH_va = (CE + eta * MI) / GVA, where CE = compensation of employees, MI = mixed income of the
self-employed and eta = a time-invariant, industry-group-specific labour fraction of MI estimated
from NSS/PLFS wage data (Data Manual 2024, ch. 7, eq. 7.1).

Run:  python3 -I extract_klems.py   (from this directory)
"""
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw", "klems")

RELEASES = [
    ("India KLEMS July 2024 (RBI, released 2024-07-08; data 1980-81 to 2022-23)",
     "INDIAKLEMS08072024.xlsx",
     "https://rbidocs.rbi.org.in/rdocs/content/docs/INDIAKLEMS08072024.xlsx"),
    ("India KLEMS January 2024 (RBI, released 2024-01-09; data 1980-81 to 2021-22)",
     "INDIAKLEMS09012024.xlsx",
     "https://rbidocs.rbi.org.in/rdocs/content/docs/INDIAKLEMS09012024.xlsx"),
]
INDUSTRIES = {"71t74": "Business Service", "64": "Post and Telecommunication"}

NOTE_LSH = ("labour_comp = LSH_va x VA (KLEMS publishes only the share). LSH_va = (CE + eta*MI)/GVA; "
            "eta = fixed labour fraction of self-employed mixed income, estimated for industry groups "
            "from NSS/PLFS wages (Data Manual 2024 ch.7). ")
NOTE_BS = ("Business Service = NACE rev1 71-74: renting of machinery, computer & related activities "
           "(IT/ITeS), R&D, other business activities (legal, accounting, consulting, advertising, "
           "architecture, staffing, security etc.). Much broader than IT. CE/MI come from NAS 'real estate, "
           "ownership of dwellings & professional services' split by KLEMS; eta shared with Financial "
           "services, Real estate and Other services.")
NOTE_PT = "Post and Telecommunication (NACE 64); IT services are NOT in this industry."


def industry_rows(path, release, url):
    va = pd.read_excel(path, sheet_name="VA", header=None)
    lsh = pd.read_excel(path, sheet_name="LSH_va", header=None)
    out = []
    for df_name, df in (("VA", va), ("LSH_va", lsh)):
        assert str(df.iloc[1, 1]).strip() == "Industry code", (df_name, df.iloc[1, :3].tolist())
    years = [str(y).strip() for y in va.iloc[1, 3:].tolist()]
    assert years == [str(y).strip() for y in lsh.iloc[1, 3:].tolist()]
    for code, label in INDUSTRIES.items():
        rv = va[va.iloc[:, 1].astype(str).str.strip() == code]
        rl = lsh[lsh.iloc[:, 1].astype(str).str.strip() == code]
        assert len(rv) == 1 and len(rl) == 1, code
        assert label.lower() in str(rv.iloc[0, 2]).lower(), rv.iloc[0, 2]
        for j, fy in enumerate(years):
            g = float(rv.iloc[0, 3 + j])
            s = float(rl.iloc[0, 3 + j])
            out.append(dict(source_release=release, industry_code=code,
                            industry_label=str(rv.iloc[0, 2]).strip(), fy=fy,
                            gva_nominal_inr_crore=round(g, 2), labour_comp_inr_crore=round(g * s, 2),
                            labour_share=round(s, 6), source_url=url, sheet="VA; LSH_va",
                            notes=NOTE_LSH + (NOTE_BS if code == "71t74" else NOTE_PT)))
    return out


def aggregate_rows(path, release, url, sheet, code, label):
    d = pd.read_excel(path, sheet_name=sheet, header=None)
    years = [str(y).strip() for y in d.iloc[1, 2:].tolist()]
    va_row = d[(d.iloc[:, 0].astype(str).str.strip() == "Value Added")]
    assert "Current" in str(va_row.iloc[0, 1]), va_row.iloc[0, 1]
    ls_row = d[d.iloc[:, 0].astype(str).str.strip() == "Labour income share"]
    assert len(va_row) == 1 and len(ls_row) == 1
    out = []
    for j, fy in enumerate(years):
        g, s = va_row.iloc[0, 2 + j], ls_row.iloc[0, 2 + j]
        if pd.isna(g) or pd.isna(s):
            continue
        g, s = float(g), float(s)
        out.append(dict(source_release=release, industry_code=code, industry_label=label, fy=fy,
                        gva_nominal_inr_crore=round(g, 2), labour_comp_inr_crore=round(g * s, 2),
                        labour_share=round(s, 6), source_url=url, sheet=sheet,
                        notes=NOTE_LSH + f"Aggregate from '{sheet}' sheet (Tornqvist aggregation of 27 industries)."
                        + (" 2023-24 is provisional (economy only)." if "Prov" in fy else "")))
    return out


def main():
    rows = []
    for release, fname, url in RELEASES:
        p = os.path.join(RAW, fname)
        if not os.path.exists(p):
            print("missing", p, file=sys.stderr)
            continue
        rows += industry_rows(p, release, url)
        rows += aggregate_rows(p, release, url, "Economy", "TOTAL", "Total Economy")
        rows += aggregate_rows(p, release, url, "Services", "SERV", "Services (aggregate)")
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(HERE, "klems_labour_share.csv"), index=False)
    latest = df[df.source_release.str.startswith("India KLEMS July 2024")]
    piv = latest.pivot_table(index="fy", columns="industry_code", values="labour_share", aggfunc="first")
    print(piv.tail(15).round(3).to_string())
    bs = latest[latest.industry_code == "71t74"].set_index("fy")
    print(bs[["gva_nominal_inr_crore", "labour_comp_inr_crore"]].tail(8).round(0).to_string())
    old = df[df.source_release.str.startswith("India KLEMS January 2024")]
    cmp_ = old[old.industry_code == "71t74"].set_index("fy").labour_share.to_frame("jan24").join(
        bs.labour_share.to_frame("jul24"))
    print(cmp_.tail(6).round(3).to_string())


if __name__ == "__main__":
    main()
