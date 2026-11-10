"""Build per-round variable mapping from Stata variable labels (metadata only, no records read).
Usage: python3 -I build_mapping.py EXTRACTED_DIR OUT_CSV
Matching is by variable label; the result is reviewed by hand and checked in check_mapping output."""
import sys, os, re, csv
import pandas as pd

ROUNDS = {  # round -> person-level first-visit file (relative to EXTRACTED_DIR)
    "2017-18": "2017-18/STATA_PLFS_July2017_June2018/hh_per_fv_2017-18.dta",
    "2018-19": "2018-19/PLFS_2028_19_STATA/PerV1_2018-19.dta",
    "2019-20": "2019-20/STATA_PLFS_19_20/PERFV_2019-20.dta",
    "2020-21": "2020-21/STATA_Unit_level_data_PLFS_July2020_June2021/perv1.dta",
    "2021-22": "2021-22/PLFS_Data_2021-22_STATA/perv1.dta",
    "2022-23": "2022-23/Data_in_STATA/perv1 (2).dta",
    "2023-24": "2023-24/STATA_data_PLFS_2023_2024/perv1.dta",
    "cy2024": "cy2024/Data_in_STATA/cperv1.dta",
    "cy2025": "cy2025/Data_in_STATA/cperv12025.dta",
}
# std name -> (label regex, occurrence index)
SPEC = [
    ("quarter", r"^quarter$", 0), ("month", r"^month$", 0), ("visit", r"^visit$", 0),
    ("sector", r"^sector$", 0), ("state", r"^state/ut code$", 0), ("district", r"^district code$", 0),
    ("stratum", r"^stratum$", 0), ("group", r"^group$", 0), ("substratum", r"^sub-stratum$", 0),
    ("subsample", r"^sub-sample$", 0), ("fsu", r"^fsu$", 0), ("sgsb", r"^sample sg/sb no\.?$", 0),
    ("sss", r"^second stage stratum no\.?$", 0), ("hhno", r"^sample household number$", 0),
    ("person", r"^person serial no\.?$", 0), ("sex", r"^(sex|gender)$", 0), ("age", r"^age$", 0),
    ("gedu", r"^general educa?ion level$", 0), ("tedu", r"^technical educa?ion level$", 0),
    ("ps_status", r"^status code$", 0), ("ps_nic", r"^industry code \(nic\)$", 0),
    ("ps_nco", r"^occupation code \(nco\)$", 0),
    ("ss_status", r"^status code$", 1), ("ss_nic", r"^industry code \(nic\)$", 1),
    ("cws_status", r"^current weekly status \(cws\)$", 0), ("cws_nic", r"^industry code \(cws\)$", 0),
    ("cws_nco", r"^occupation code \(cws\)$", 0),
    ("earn_regular", r"^earnings for regular salari", 0),
    ("nss", r"^ns count .*sub-?sample", 0), ("nsc", r"^ns count", -1),
    ("mult", r"multiplier$", 0), ("no_qtr", r"(occur[ae]nce|count of contributing).*4 qua", 0),
]

rows = []
base = sys.argv[1]
for rnd, rel in ROUNDS.items():
    with pd.io.stata.StataReader(os.path.join(base, rel)) as r:
        vl = r.variable_labels()
        nobs = r._nobs
    items = [(k, (v or "").strip().lower()) for k, v in vl.items()]
    for std, pat, occ in SPEC:
        hits = [k for k, lab in items if re.search(pat, lab)]
        if std == "nsc":  # NSC is the Ns count that is NOT the sub-sample one
            hits = [k for k, lab in items if lab.startswith("ns count") and "sub-sample" not in lab]
            occ = 0
        col = hits[occ] if len(hits) > (occ if occ >= 0 else -occ - 1) else ""
        rows.append(dict(round=rnd, file=rel, n_records=nobs, std_var=std, source_var=col,
                         source_label=dict(items).get(col, "") if col else ""))
with open(sys.argv[2], "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
piv = pd.DataFrame(rows).pivot(index="std_var", columns="round", values="source_var")
print(piv.reindex([s[0] for s in SPEC]).to_string())
