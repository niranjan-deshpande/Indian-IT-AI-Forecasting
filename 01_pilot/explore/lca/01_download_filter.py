"""Download DOL OFLC LCA (H-1B) disclosure xlsx files, filter to target IT-services employers, delete raw.
Source page: https://www.dol.gov/agencies/eta/foreign-labor/performance
Usage: python 01_download_filter.py <scratch_dir> <file_name> [<file_name> ...]
Writes <scratch_dir>/filtered/<file>.csv.gz ; raw xlsx deleted after filtering.
"""
import sys, os, re, subprocess, csv, gzip, datetime, json
from python_calamine import CalamineWorkbook

BASE = "https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/"
URLS = {"LCA_Disclosure_Data_FY2026_Q3.xlsx": "https://www.dol.gov//media/LCA_Disclosure_Data_FY2026_Q3.xlsx"}
UA = "ndeshpande research ndeshpande@college.harvard.edu"  # browser UA is blocked by Akamai for file downloads

EMP_RE = re.compile(r"TATA CONSULTANCY|INFOSYS|HCL AMERICA|HCL TECHNOLOGIES|WIPRO|TECH MAHINDRA|LTIMINDTREE|LARSEN\s*(&|AND)\s*TOUBRO INFOTECH|MINDTREE|COGNIZANT|ACCENTURE|MPHASIS|PERSISTENT SYSTEMS|COFORGE|NIIT TECHNOLOGIES|HEXAWARE|CAPGEMINI|IGATE", re.I)

SYN = {
 "case_number": ["CASE_NUMBER", "CASE_NO", "LCA_CASE_NUMBER"],
 "status": ["CASE_STATUS", "STATUS"],
 "received_date": ["RECEIVED_DATE", "CASE_SUBMITTED", "LCA_CASE_SUBMIT", "SUBMITTED_DATE"],
 "decision_date": ["DECISION_DATE", "LCA_CASE_DECISION_DATE"],
 "visa_class": ["VISA_CLASS", "PROGRAM"],
 "employer": ["EMPLOYER_NAME", "LCA_CASE_EMPLOYER_NAME"],
 "employer_state": ["EMPLOYER_STATE"],
 "soc_code": ["SOC_CODE", "LCA_CASE_SOC_CODE"],
 "soc_title": ["SOC_TITLE", "SOC_NAME", "LCA_CASE_SOC_NAME"],
 "job_title": ["JOB_TITLE", "LCA_CASE_JOB_TITLE"],
 "full_time": ["FULL_TIME_POSITION"],
 "begin_date": ["BEGIN_DATE", "EMPLOYMENT_START_DATE", "LCA_CASE_EMPLOYMENT_START_DATE", "PERIOD_OF_EMPLOYMENT_START_DATE"],
 "end_date": ["END_DATE", "EMPLOYMENT_END_DATE", "LCA_CASE_EMPLOYMENT_END_DATE", "PERIOD_OF_EMPLOYMENT_END_DATE"],
 "total_workers": ["TOTAL_WORKER_POSITIONS", "TOTAL_WORKERS"],
 "new_employment": ["NEW_EMPLOYMENT"],
 "continued_employment": ["CONTINUED_EMPLOYMENT"],
 "change_previous_employment": ["CHANGE_PREVIOUS_EMPLOYMENT"],
 "new_concurrent_employment": ["NEW_CONCURRENT_EMPLOYMENT", "NEW_CONCURRENT_EMP"],
 "change_employer": ["CHANGE_EMPLOYER"],
 "amended_petition": ["AMENDED_PETITION"],
 "wage_from": ["WAGE_RATE_OF_PAY_FROM", "WAGE_RATE_OF_PAY", "LCA_CASE_WAGE_RATE_FROM", "WAGE_RATE_OF_PAY_FROM_1"],
 "wage_to": ["WAGE_RATE_OF_PAY_TO", "LCA_CASE_WAGE_RATE_TO", "WAGE_RATE_OF_PAY_TO_1"],
 "wage_unit": ["WAGE_UNIT_OF_PAY", "LCA_CASE_WAGE_RATE_UNIT", "WAGE_UNIT_OF_PAY_1"],
 "pw": ["PREVAILING_WAGE", "PW_1", "PREVAILING_WAGE_1"],
 "pw_unit": ["PW_UNIT_OF_PAY", "PW_UNIT_1", "PW_UNIT_OF_PAY_1"],
 "pw_level": ["PW_WAGE_LEVEL", "PW_LEVEL", "PW_WAGE_LEVEL_1"],
 "pw_source": ["PW_WAGE_SOURCE", "PW_SOURCE", "PW_OTHER_SOURCE", "PW_OTHER_SOURCE_1"],
 "worksite_state": ["WORKSITE_STATE", "WORKSITE_STATE_1", "LCA_CASE_WORKLOC1_STATE"],
 "worksite_city": ["WORKSITE_CITY", "WORKSITE_CITY_1", "LCA_CASE_WORKLOC1_CITY"],
 "h1b_dependent": ["H1B_DEPENDENT", "H_1B_DEPENDENT"],
}

def norm(h):
    return re.sub(r"[\s\-/]+", "_", str(h).strip().upper())

def fmt(v):
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.isoformat()[:10]
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return "" if v is None else str(v)

def process(scratch, fname):
    out = os.path.join(scratch, "filtered", fname.replace(".xlsx", ".csv.gz"))
    if os.path.exists(out):
        print("skip", fname); return
    raw = os.path.join(scratch, "raw", fname)
    url = URLS.get(fname, BASE + fname)
    os.makedirs(os.path.dirname(raw), exist_ok=True); os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run(["curl", "-s", "-L", "-A", UA, "--retry", "3", "-o", raw, url], check=True)
    size = os.path.getsize(raw)
    wb = CalamineWorkbook.from_path(raw)
    sh = wb.get_sheet_by_index(0)
    rows = sh.iter_rows()
    header = [norm(h) for h in next(rows)]
    idx = {}
    for k, cands in SYN.items():
        for c in cands:
            if c in header:
                idx[k] = header.index(c); break
    emp_i = idx["employer"]
    n_all = 0; n_keep = 0
    tmp = out + ".tmp"
    with gzip.open(tmp, "wt", newline="") as f:
        w = csv.writer(f)
        w.writerow(["source_file"] + list(SYN.keys()))
        for r in rows:
            n_all += 1
            e = r[emp_i] if emp_i < len(r) else None
            if e and EMP_RE.search(str(e)):
                n_keep += 1
                w.writerow([fname] + [fmt(r[idx[k]]) if k in idx and idx[k] < len(r) else "" for k in SYN])
    os.rename(tmp, out)
    meta = dict(file=fname, url=url, bytes=size, rows_total=n_all, rows_kept=n_keep,
                missing_fields=[k for k in SYN if k not in idx], header=header)
    with open(os.path.join(scratch, "filtered", fname.replace(".xlsx", ".meta.json")), "w") as f:
        json.dump(meta, f)
    os.remove(raw)
    print(fname, size, n_all, n_keep, "missing:", meta["missing_fields"], flush=True)

if __name__ == "__main__":
    for fn in sys.argv[2:]:
        try:
            process(sys.argv[1], fn)
        except Exception as ex:
            print("ERROR", fn, repr(ex), flush=True)
