"""Aggregate check of the Jan-Jun 2024 overlap between the 2023-24 and CY2024 first-visit files.
Usage: python3 -I check_overlap.py WORK_DIR"""
import sys, os
import pandas as pd
a = pd.read_parquet(os.path.join(sys.argv[1], "2023-24.parquet"))
b = pd.read_parquet(os.path.join(sys.argv[1], "cy2024.parquet"))
print("2023-24 quarters:", a.quarter.value_counts().sort_index().to_dict())
print("cy2024 quarters:", b.quarter.value_counts().sort_index().to_dict())
key = ["quarter", "fsu", "sgsb", "sss", "hhno", "person"]
for d in (a, b):
    for c in key:
        d[c] = d[c].astype(str).str.strip().str.lstrip("0")
ov_a = a[a.quarter.isin(["Q3", "3"])]
m = ov_a.merge(b, on=key, suffixes=("_a", "_b"))
print("2023-24 Q3 records:", len(ov_a), " matched in CY2024:", len(m))
for c in ["age", "sex", "gedu", "ps_status"]:
    print(f"  identical {c}: {(m[c + '_a'] == m[c + '_b']).mean():.4f}")
print("  identical ps_nic:", (m.ps_nic_a == m.ps_nic_b).mean().round(4), " mult identical:", (m.mult_a == m.mult_b).mean().round(4))
print("  share Jan-Jun 2024 in each annual file: 2023-24 =", round(a.quarter.isin(['Q3', 'Q4']).mean(), 3),
      " cy2024 =", round(b.quarter.isin(['Q3', 'Q4']).mean(), 3))
