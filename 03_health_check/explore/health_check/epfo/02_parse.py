"""Parse archived EPFO "Net Payroll Data" monthly reports into tidy long CSVs.

Run:  python3 -I 02_parse.py   (from anywhere; paths are relative to this file)

Inputs : raw/*.pdf (downloaded by 01_download.sh), wayback_captures.txt
Needs  : pdftotext (poppler) on PATH
Outputs (in this folder):
  epfo_age_net_payroll_vintages.csv   page-1 table: net payroll by age band, every period in every vintage
  epfo_age_components_vintages.csv    new subscribers / exits / rejoins / net, by age band and period
  epfo_industry_age_vintages.csv      net payroll for the top-10 industries within each age band
Each row carries the release date (vintage), the raw file, the original EPFO URL and the archive URL.
"""
import csv
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"

MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
AGE_ROWS = {"less than 18": "<18", "18-21": "18-21", "22-25": "22-25", "26-28": "26-28",
            "29-35": "29-35", "more than 35": ">35", "total": "Total"}
AGE_COLS = ["<18", "18-21", "22-25", "26-28", "29-35", ">35", "Total"]
NUM = r"-?\d+"

captures = {}
for line in (HERE / "wayback_captures.txt").read_text().split("\n"):
    if line.strip():
        ts, url = line.split()[:2]
        captures[ts] = url


def period_norm(tok):
    """'Apr-2019','Apr-19','April 2025','2018-19','2017-18 (from Sep-17)' -> ('2019-04','month') etc."""
    t = tok.strip()
    m = re.match(r"^(20\d\d)-(\d\d)\b", t)
    if m:
        return f"FY{m.group(1)}-{m.group(2)}", "FY"
    m = re.match(r"^([A-Za-z]{3})[a-z]*[- ](\d{2,4})$", t)
    if m and m.group(1).lower() in MONTHS:
        y = int(m.group(2))
        y = y + 2000 if y < 100 else y
        return f"{y}-{MONTHS[m.group(1).lower()]:02d}", "month"
    return None, None


def release_date(text):
    m = re.search(r"Date\s+(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+),?\s*(\d{4})", text[:3000])
    if not m:
        return None
    return f"{m.group(3)}-{MONTHS[m.group(2)[:3].lower()]:02d}-{int(m.group(1)):02d}"


def meta_for(pdf):
    ts = re.search(r"__wb(\d{14})", pdf.name).group(1)
    url = captures.get(ts, "")
    return {"source_file": f"raw/{pdf.name}", "source_url": url,
            "archive_url": f"https://web.archive.org/web/{ts}id_/{url}"}


def parse_page1(text):
    """Net payroll by age band (page 1)."""
    out = []
    head = text.split("Notes:")[0]
    lines = head.split("\n")
    pending_fy1718 = False
    for ln in lines:
        s = ln.strip()
        if "2017-18" in s:
            pending_fy1718 = True
        nums = re.findall(r"(?<![\w-])" + NUM + r"(?![\w-])", s)
        lab = re.match(r"^([A-Za-z]{3}-\d{2,4}|20\d\d-\d\d)", s)
        if lab:
            per, typ = period_norm(lab.group(1))
            rest = s[len(lab.group(1)):]
            nums = re.findall(r"(?<![\w-])" + NUM + r"(?![\w-])", rest)
            if per == "2017-09" and pending_fy1718:  # "Sep-17)" continuation of "2017-18 (from"
                per, typ = "FY2017-18", "FY"
            if per == "FY2017-18":
                nums = [n for n in nums if n not in ("17",)]
        elif pending_fy1718 and len(nums) >= 7 and not re.search(r"[A-Za-z]{3}-\d", s):
            per, typ = "FY2017-18", "FY"
        else:
            continue
        if per == "FY2017-18" and len(nums) >= 8 and nums[0] == "17":
            nums = nums[1:]  # stray "17" from a wrapped "(from Sep-17)" label
        if per == "FY2017-18" and len(nums) < 7:
            continue  # label line only; numbers on next line
        if len(nums) < 7:
            continue
        vals = [int(x) for x in nums[:7]]
        estab = int(nums[7]) if len(nums) > 7 else None
        for a, v in zip(AGE_COLS, vals):
            out.append({"period": per, "period_type": typ, "age_band": a, "net_payroll": v,
                        "estab_first_ecr": estab if a == "Total" else ""})
        if per == "FY2017-18":
            pending_fy1718 = False
    return out


def parse_components(text):
    """Pages 2..: per period, rows of (a) new, (b) exited, (c) rejoined, (d) net, by age."""
    body = text.split("Notes:", 1)[1] if "Notes:" in text else text
    body = re.split(r"STATEWISE", body)[0]
    out = []
    period = None
    table = "net_payroll"
    for ln in body.split("\n"):
        s = ln.strip()
        if not s:
            continue
        if "Net new EPF" in s or ("Subscribers" in s and "Net" in s and "Payroll" not in s):
            table = "net_new_subscribers"
        elif re.search(r"Net Payroll\b", s) and "DATA" not in s:
            table = "net_payroll"
        if "Report due" in s:
            table = "net_payroll"  # each set starts again after a 'Report due' banner
        m = re.match(r"^(20\d\d-\d\d)\b", s)
        if m and len(re.findall(NUM, s)) <= 3:
            period = f"FY{m.group(1)}"
            continue
        m = re.match(r"^([A-Z][a-z]+)\s+(20\d\d)$", s)
        if m and m.group(1)[:3].lower() in MONTHS:
            period = f"{m.group(2)}-{MONTHS[m.group(1)[:3].lower()]:02d}"
            continue
        low = s.lower()
        for key, band in AGE_ROWS.items():
            if low.startswith(key):
                nums = re.findall(r"(?<![\w-])" + NUM + r"(?![\w-])", s[len(key):])
                if len(nums) == 4 and period:
                    a, b, c, d = map(int, nums)
                    out.append({"table": table, "period": period,
                                "period_type": "FY" if period.startswith("FY") else "month",
                                "age_band": band, "a_new": a, "b_exited": b,
                                "c_rejoined": c, "d_net": d})
                break
    return out


def parse_industry(text):
    if "INDUSTRY WISE" not in text:
        return [], []
    sec = text.split("INDUSTRY WISE", 1)[1]
    sec = re.split(r"Age Slab|Number of New EPF Subscribers during", sec)[0]
    out, totals = [], []
    band, cols, pend = None, None, None
    for ln in sec.split("\n"):
        s = ln.strip()
        if not s:
            continue
        m = re.match(r"Age Bucket:\s*(.+)$", s)
        if m:
            band = AGE_ROWS.get(m.group(1).strip().lower(), m.group(1).strip())
            continue
        if s.startswith("Industry"):
            h = re.sub(r"\((?:From|from)[^)]*\)", "", s)
            h = re.sub(r"(?i)\(?\s*from\s+sep-?\d+\s*\)?", "", h)
            h = h.replace("Sep-05", "2024-25")  # typo in Aug-2025 release (29-35 header)
            toks = re.findall(r"20\d\d-\d\d|[A-Z][a-z]{2}-\d{2,4}", h)
            cols = [period_norm(t) for t in toks]
            continue
        if cols is None:
            continue
        s = re.sub(r"COMPUTERS(-?\d)", r"COMPUTERS \1", s)
        if pend and s == "COMPUTERS":  # wrapped name, numbers follow on the next line
            pend = (pend[0] + " COMPUTERS", pend[1])
            continue
        if pend and re.fullmatch(r"(?:" + NUM + r"\s+)*" + NUM, s):
            s = "From " + s  # numbers-only continuation line
        m = re.match(r"^(.*?[A-Za-z\)\.])\s+((?:" + NUM + r"\s+)*" + NUM + r")$", s)
        if not m:
            continue
        name = re.sub(r"\s+", " ", m.group(1)).strip()
        nums = [int(x) for x in m.group(2).split()]
        if name.startswith("Page"):
            continue
        if len(nums) != len(cols):
            # a row wrapped over two lines (name or first value on line 1, rest on line 2)
            if pend and len(pend[1]) + len(nums) == len(cols):
                cont = "" if name.lower() == "from" else " " + name
                name, nums = (pend[0] + cont).strip(), pend[1] + nums
                pend = None
            else:
                if pend:
                    out.append({"_bad": True, "name": pend[0], "band": band, "n": len(pend[1]), "k": len(cols)})
                pend = (name, nums)
                continue
        elif pend:
            out.append({"_bad": True, "name": pend[0], "band": band, "n": len(pend[1]), "k": len(cols)})
            pend = None
        for (per, typ), v in zip(cols, nums):
            row = {"period": per, "period_type": typ, "age_band": band, "industry": name,
                   "net_payroll": v}
            if name.upper().startswith(("TOTAL TOP 10", "GRAND TOTAL")):
                row["age_band"] = "All"
                totals.append(row)
            elif name.upper().startswith("SUB TOTAL"):
                totals.append(row)
            else:
                out.append(row)
    return out, totals


def main():
    age_rows, comp_rows, ind_rows, problems = [], [], [], []
    for pdf in sorted(RAW.glob("*.pdf")):
        text = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True,
                              text=True).stdout
        if not text.strip():
            problems.append(f"{pdf.name}: no text")
            continue
        vint = release_date(text)
        meta = {"vintage_release_date": vint, **meta_for(pdf)}
        for r in parse_page1(text):
            age_rows.append({**meta, **r})
        for r in parse_components(text):
            comp_rows.append({**meta, **r})
        inds, tots = parse_industry(text)
        for r in inds:
            if r.get("_bad"):
                problems.append(f"{pdf.name}: industry row width mismatch {r}")
                continue
            ind_rows.append({**meta, **r})
        for r in tots:
            ind_rows.append({**meta, **r})

    def write(name, rows):
        keys = list(rows[0].keys())
        for r in rows:
            for k in r:
                if k not in keys:
                    keys.append(k)
        with open(HERE / name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)
        print(f"{name}: {len(rows)} rows")

    write("epfo_age_net_payroll_vintages.csv", age_rows)
    write("epfo_age_components_vintages.csv", comp_rows)
    write("epfo_industry_age_vintages.csv", ind_rows)
    for p in problems:
        print("PROBLEM", p)


if __name__ == "__main__":
    main()
