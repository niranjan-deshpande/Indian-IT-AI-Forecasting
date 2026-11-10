"""Top occupation codes (unweighted counts) among NIC 62 PS workers, per round. Usage: python3 -I check_nco.py WORK_DIR"""
import sys, glob, os
import pandas as pd
for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.parquet"))):
    d = pd.read_parquet(f, columns=["ps_status", "ps_nic", "ps_nco"])
    wk = d[d.ps_status.between(11, 51)]
    print(os.path.basename(f), "NIC62 top NCO:", wk.ps_nco[wk.ps_nic.str[:2] == "62"].value_counts().head(8).to_dict())
    print("   all-worker counts 213/312/251/252/351:", {c: int((wk.ps_nco == c).sum()) for c in ["213", "312", "251", "252", "351"]})
