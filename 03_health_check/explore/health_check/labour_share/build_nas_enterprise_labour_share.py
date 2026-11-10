"""Build nas_enterprise_labour_share.csv from MoSPI downloads in raw/nas and raw/assse.

Run from anywhere:  python3 -I build_nas_enterprise_labour_share.py
Inputs are untrusted downloads; they are only parsed (openpyxl data_only; pdftotext).

Sources
- NAS 2025 (2011-12 base), statements 8.13 and 7.1/7.1B/7.1C
- NAS 2026 (2022-23 base), statements 8.13 and 7.1/7.1B/7.1C
- ASUSE 2021-22, 2022-23, 2023-24, 2025 full reports (activity category S7 'Information and
  Communication', NIC 2008 divisions 58-63)
"""
import csv
import os
import re
import subprocess
import tempfile

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_NAS = os.path.join(HERE, "raw", "nas")
RAW_ENT = os.path.join(HERE, "raw", "assse")
OUT = os.path.join(HERE, "nas_enterprise_labour_share.csv")

URL25 = "https://www.mospi.gov.in/sites/default/files/reports_and_publication/statistical_publication/National_Accounts/NAS2025/{}.xlsx"
URL26 = "https://www.mospi.gov.in/uploads/publications_reports/NAS-2026-Statements/{}.xlsx"
EDITIONS = {
    "NAS2025_2011base": dict(prefix="NAS2025", url=URL25, base="2011-12"),
    "NAS2026_2022base": dict(prefix="NAS2026", url=URL26, base="2022-23"),
}
YEAR_RE = re.compile(r"^\d{4}-\d{2}$")

COLS = ["source", "industry_label", "industry_scope_note", "fy", "price_basis", "gva_inr_crore",
        "ce_inr_crore", "os_mi_inr_crore", "labour_share", "table_id", "source_url", "notes"]
rows = []


def num(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def r2(x):
    return "" if x is None else f"{x:.2f}"


def share(ce, gva):
    return "" if ce is None or not gva else f"{ce / gva:.4f}"


def sheet_rows(path):
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    ws = wb.worksheets[0]
    return [list(r) for r in ws.iter_rows(values_only=True)]


def english_label(row):
    """Last non-numeric text cell in the row (the English label column)."""
    texts = [str(c).strip() for c in row if isinstance(c, str) and c.strip()]
    texts = [t for t in texts if re.search(r"[A-Za-z]", t)]
    return texts[-1] if texts else ""


# ---------------------------------------------------------------- NAS 8.13 (IT line)
IT_SCOPE = {
    "NAS2025_2011base": ("Information and computer related services (sub-item of Real estate, ownership "
                         "of dwellings & professional services). 2011-12 base; MoSPI does not publish the "
                         "NIC list for this line in the statement; 2022-23-base Sources & Methods maps the "
                         "same line to NIC 2008 divisions 62+63."),
    "NAS2026_2022base": ("Information and computer related services = compilation category C53 'Computer "
                         "and information related services', NIC 2008 divisions 62+63 (Sources & Methods "
                         "for NAS, Sep 2026, ch.18)."),
}


SUBSTACK_MATCH = {("NAS2025_2011base", "2017-18"), ("NAS2025_2011base", "2023-24"),
                  ("NAS2026_2022base", "2022-23"), ("NAS2026_2022base", "2023-24"),
                  ("NAS2026_2022base", "2024-25")}


def nas_813(src):
    ed = EDITIONS[src]
    path = os.path.join(RAW_NAS, f"{ed['prefix']}_8.13.xlsx")
    data = sheet_rows(path)
    # year header row: the row with most yyyy-yy cells
    hdr_i = max(range(len(data)), key=lambda i: sum(1 for c in data[i] if isinstance(c, str) and YEAR_RE.match(c.strip())))
    hdr = data[hdr_i]
    seen = {}
    colmap = []  # (col, fy, basis)
    for j, c in enumerate(hdr):
        if isinstance(c, str) and YEAR_RE.match(c.strip()):
            fy = c.strip()
            basis = "current" if fy not in seen else f"constant_{ed['base']}"
            seen[fy] = True
            colmap.append((j, fy, basis))
    # find the IT block and the dwelling block
    labels = [english_label(r) for r in data]
    def block(start_label):
        i0 = next(i for i, l in enumerate(labels) if l.lower().startswith(start_label.lower()))
        out = {}
        for i in range(i0 + 1, i0 + 4):
            l = labels[i].lower()
            key = "output" if "output" in l else "input" if "input" in l else "gva_unadj" if "gross value added" in l else None
            if key:
                out[key] = data[i]
        return out
    it = block("Information and computer related services")
    dw = block("Ownership of dwellings")
    for j, fy, basis in colmap:
        go, ic, gva = num(it["output"][j]), num(it["input"][j]), num(it["gva_unadj"][j])
        rows.append(dict(
            source=src, industry_label="Information and computer related services",
            industry_scope_note=IT_SCOPE[src], fy=fy, price_basis=basis,
            gva_inr_crore=r2(gva), ce_inr_crore="", os_mi_inr_crore="", labour_share="",
            table_id="Statement 8.13, item 3 (GVA unadjusted for FISIM)",
            source_url=ed["url"].format("8.13"),
            notes=(f"GVA is 'Gross Value Added unadjusted for FISIM' (FISIM only deducted at the "
                   f"real-estate+dwellings+professional-services total). Output={r2(go)}, input={r2(ic)}. "
                   "CE/OS for this line are not published anywhere in NAS."
                   + (" Matches the 'IT value added' figure in Future of India Substack (2 Oct 2026)."
                      if basis == "current" and (src, fy) in SUBSTACK_MATCH else ""))))
    return {fy: num(dw["gva_unadj"][j]) for j, fy, basis in colmap if basis == "current"}


# ---------------------------------------------------------------- NAS 7.1 family (CE by industry)
SECTOR = {"7.1": "all institutional sectors", "7.1A": "public sector", "7.1B": "private corporations",
          "7.1C": "households (incl. NPISH and ownership of dwellings)"}


def nas_71(src, stmt, dwelling_gva=None):
    ed = EDITIONS[src]
    path = os.path.join(RAW_NAS, f"{ed['prefix']}_{stmt}.xlsx")
    data = sheet_rows(path)
    yr_i = max(range(len(data)), key=lambda i: sum(1 for c in data[i] if isinstance(c, str) and YEAR_RE.match(c.strip())))
    lab_i = next(i for i, r in enumerate(data) if any(isinstance(c, str) and "Compensation of employee" in c for c in r))
    yrs, cur = [], None
    for j, c in enumerate(data[yr_i]):
        if isinstance(c, str) and YEAR_RE.match(c.strip()):
            cur = c.strip()
        yrs.append(cur)
    cols = {}
    for j, c in enumerate(data[lab_i]):
        if not isinstance(c, str) or yrs[j] is None:
            continue
        c = c.strip().lower()
        key = ("gva" if c.startswith("gross value added") else "ce" if c.startswith("compensation") else
               "os" if c.startswith("operating surplus") else "cfc" if c.startswith("consumption of fixed") else
               "tax" if c.startswith("production taxes") else None)
        if key:
            cols.setdefault(yrs[j], {})[key] = j
    labels = [english_label(r) for r in data]
    ri = next(i for i, l in enumerate(labels) if l.lower().startswith("real estate, ownership of dwelling"))
    r = data[ri]
    for fy, cj in cols.items():
        gva, ce, os_ = num(r[cj["gva"]]), num(r[cj["ce"]]), num(r[cj["os"]])
        cfc, tax = num(r[cj["cfc"]]), num(r[cj["tax"]])
        rows.append(dict(
            source=src, industry_label=labels[ri],
            industry_scope_note=(f"Real estate (NIC 68) + ownership of dwellings + IT (62-63) + legal/accounting + "
                                 f"R&D/professional (69-75) + admin & support (77-82); {SECTOR[stmt]}"),
            fy=fy, price_basis="current", gva_inr_crore=r2(gva), ce_inr_crore=r2(ce), os_mi_inr_crore=r2(os_),
            labour_share=share(ce, gva), table_id=f"Statement {stmt}, item 9",
            source_url=ed["url"].format(stmt),
            notes=(f"GVA at basic prices = CE + OS/MI + CFC + production taxes less subsidies; CFC={r2(cfc)}, "
                   f"net production taxes={r2(tax)}. OS/MI is net of CFC. No finer industry split of CE is published.")))
        if stmt == "7.1" and dwelling_gva and dwelling_gva.get(fy):
            g2 = gva - dwelling_gva[fy]
            rows.append(dict(
                source=src, industry_label="DERIVED: item 9 minus Ownership of dwellings",
                industry_scope_note="Real estate + IT + professional + admin/support services (excl. ownership of dwellings); all sectors",
                fy=fy, price_basis="current", gva_inr_crore=r2(g2), ce_inr_crore=r2(ce), os_mi_inr_crore="",
                labour_share=share(ce, g2),
                table_id="Statement 7.1 item 9 less Statement 8.13 item 2 (dwellings GVA unadjusted for FISIM)",
                source_url=ed["url"].format("7.1") + " ; " + ed["url"].format("8.13"),
                notes=("Derived by us, not published. Assumes compensation of employees in ownership of dwellings "
                       "is ~0 (imputed/actual rent of households). Denominator still includes FISIM deduction "
                       "for the whole group. Crude proxy only: IT is ~35-40% of this GVA.")))


# ---------------------------------------------------------------- ASUSE (S7 Information & communication)
ASUSE = [
    # (source, fy label, pdf, code, table regexes for: est count, workers, emoluments, gva/worker, gva/estt, url)
    ("ASUSE_2021-22", "2021-22", "ASUSE_2021_22_Report.pdf", "S7",
     dict(est=r"^Table 10:", wrk=r"^Table 40:", emo=r"^Table 44:", gpw=r"^Table 46:", gpe=r"^Table 48:"),
     "https://www.mospi.gov.in/sites/default/files/publication_reports/ASUSE_2021_22_Report_FinalN1.pdf",
     "Reference period April 2021-March 2022 (Tables 10, 40, 44, 46, 48)."),
    ("ASUSE_2022-23", "2022-23", "ASUSE_2022_23_Report.pdf", "S7|S07",
     dict(est=r"^Table 6:", wrk=r"^Table 31:", emo=r"^Table 33:", gpw=r"^Table 35:", gpe=r"^Table 37:"),
     "https://www.mospi.gov.in/sites/default/files/publication_reports/ASUSE_2022_23_Report_FinalN.pdf",
     "Survey period October 2022-September 2023 (Tables 6, 31, 33, 35, 37)."),
    ("ASUSE_2023-24", "2023-24", "ASUSE_2023_24_Full_Report.pdf", "S7",
     dict(est=r"^Table 6:", wrk=r"^Table 31:", emo=r"^Table 33:", gpw=r"^Table 35:", gpe=r"^Table 37:"),
     "https://www.mospi.gov.in/sites/default/files/publication_reports/ASUSE_2023_24_Full_Report-L.pdf",
     "Survey period October 2023-September 2024 (Tables 6, 31, 33, 35, 37)."),
    ("ASUSE_2025", "CY2025", "ASUSE_2025_Full_Report.pdf", "S7",
     dict(est=r"^Table 6:", wrk=r"^Table 27:", emo=r"^Table 29:", gpw=r"^Table 31:", gpe=r"^Table 33:"),
     "https://www.mospi.gov.in/uploads/publications_reports/publications_reports1778063953577_942565ce-f832-4fc4-aa99-90b0b2a5a6e1_ASUSE_2025_Full_Report.pdf",
     "Calendar year January-December 2025 (Tables 6, 27, 29, 31, 33)."),
]


def asuse_rows(txt_path, code_re, table_re):
    """Return list of (sec, est, numbers) for rows of `code` in tables matching table_re."""
    row_re = re.compile(r"^\s*(" + code_re + r")\s+(-?[\d.]+(?:\s+-?[\d.]+)+)\s*$")
    out, in_table, sec, est = [], False, None, None
    with open(txt_path, encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            s = line.strip()
            if re.match(r"^Table\s+\d+[A-Za-z]?\s*:", s):
                in_table = bool(re.search(table_re, s))
                continue
            if not in_table:
                continue
            m = re.search(r"Sec\.?\s*:\s*(\w+)", line)
            if m:
                sec = m.group(1)
            m = re.search(r"Est\.?\s*:\s*(\w+)", line)
            if m:
                est = m.group(1)
            m = row_re.match(line)
            if m:
                out.append((sec, est, [float(x) for x in m.group(2).split()]))
    return out


def pick(lst, sec, est=None):
    for s, e, nums in lst:
        if s == sec and (est is None or e == est or e is None):
            return nums
    raise ValueError(f"row not found sec={sec} est={est}")


def asuse():
    with tempfile.TemporaryDirectory() as td:
        for src, fy, pdf, code, tabs, url, period in ASUSE:
            txt = os.path.join(td, pdf + ".txt")
            subprocess.run(["pdftotext", "-layout", os.path.join(RAW_ENT, pdf), txt], check=True)
            est = asuse_rows(txt, code, tabs["est"])
            wrk = asuse_rows(txt, code, tabs["wrk"])
            emo = asuse_rows(txt, code, tabs["emo"])
            gpw = asuse_rows(txt, code, tabs["gpw"])
            gpe = asuse_rows(txt, code, tabs["gpe"])
            n_hwe = pick(est, "Combined", "HWE")[-2]
            n_all = pick(est, "Combined", "All")[-2]
            w_hwe = pick(wrk, "Combined", "HWE")[-1]
            w_all = pick(wrk, "Combined", "All")[-1]
            e_all = pick(emo, "Combined", "All")  # formal, informal, all*, hired formal, informal, all*, estts, sample
            emol_per, hired = e_all[2], e_all[5]
            # these tables have rural/urban/combined as columns, so exactly one row per code
            assert len(gpw) == 1 and len(gpe) == 1, (src, len(gpw), len(gpe))
            g_w = gpw[0][2]  # rural OAE,HWE,all, urban OAE,HWE,all, combined OAE,HWE,all
            g_e = gpe[0][2]
            gva_hwe_w, gva_all_w = g_w[7] * w_hwe / 1e7, g_w[8] * w_all / 1e7  # Rs -> crore
            gva_hwe_e, gva_all_e = g_e[7] * n_hwe / 1e7, g_e[8] * n_all / 1e7
            emol = emol_per * hired / 1e7
            check = (f"Cross-check via GVA/establishment x establishments: HWE {gva_hwe_e:.0f}, all {gva_all_e:.0f} crore. "
                     f"Inputs: HWEs={n_hwe:.0f}, all estts={n_all:.0f}; workers HWE={w_hwe:.0f}, all={w_all:.0f}; "
                     f"hired workers={hired:.0f}; emoluments per hired worker (all*)=Rs {emol_per:.0f}; "
                     f"GVA/worker HWE=Rs {g_w[7]:.0f}, all=Rs {g_w[8]:.0f}.")
            scope = ("ASUSE activity category S7 'Information and Communication' = NIC 2008 divisions 58-63 "
                     "(publishing, film/broadcast, telecom, IT, info services); unincorporated non-agricultural "
                     "establishments only")
            common = dict(source=src, fy=fy, price_basis="current", os_mi_inr_crore="", source_url=url)
            rows.append(dict(common, industry_label="S7 Information and Communication - hired worker establishments (HWE)",
                             industry_scope_note=scope + "; HWEs only",
                             gva_inr_crore=r2(gva_hwe_w), ce_inr_crore=r2(emol), labour_share=share(emol, gva_hwe_w),
                             table_id=f"Derived from {code.split('|')[0]} rows, Sec:Combined: " + ", ".join(t.strip('^:') for t in tabs.values()),
                             notes=(f"Derived: GVA = GVA per worker (HWE, market estts) x HWE workers; CE = emoluments per hired "
                                    f"worker x hired workers (emoluments exclude employer PF/ESIC etc., so understate CE). "
                                    f"{period} {check}")))
            rows.append(dict(common, industry_label="S7 Information and Communication - all establishments",
                             industry_scope_note=scope + "; OAEs + HWEs",
                             gva_inr_crore=r2(gva_all_w), ce_inr_crore=r2(emol), labour_share=share(emol, gva_all_w),
                             table_id=f"Derived from {code.split('|')[0]} rows, Sec:Combined: " + ", ".join(t.strip('^:') for t in tabs.values()),
                             notes=("Same emoluments as HWE row; denominator adds own-account establishments whose GVA is "
                                    f"almost all mixed income, so this ratio understates the employee share. {period}")))


# ---------------------------------------------------------------- ASSSE (no usable levels)
def assse():
    rows.append(dict(
        source="ASSSE_pilot_2022-23", industry_label="(none: no NIC 62/63 or Section J estimates)",
        industry_scope_note="Pilot ASSSE, incorporated service enterprises, FY 2022-23, 4,086 responding sample units",
        fy="2022-23", price_basis="current", gva_inr_crore="", ce_inr_crore="", os_mi_inr_crore="", labour_share="",
        table_id="Technical Report of Pilot Study on ASSSE (Apr 2025), Statements 6-7, Appendix A Tables 3, 8, 9",
        source_url="https://www.mospi.gov.in/sites/default/files/publication_reports/TECHNICAL%20REPORT_ASSSE.pdf",
        notes=("Placeholder row. The pilot publishes only unweighted, sample-based percentage shares by output size "
               "class for broad activity categories (construction, trade, other services); NIC division 62 appears only "
               "in a count of sampled enterprises (349). No GVA or compensation levels. The full survey (ASI-SSE 2026) "
               "was in the field in 2026; no results published as of 2026-10-15.")))


def main():
    for src in EDITIONS:
        dw = nas_813(src)
        for stmt in ("7.1", "7.1B", "7.1C"):
            nas_71(src, stmt, dwelling_gva=dw)
    asuse()
    assse()
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
