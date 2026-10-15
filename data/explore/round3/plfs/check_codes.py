"""Aggregate checks of code formats in standardised files. Usage: python3 -I check_codes.py WORK_DIR"""
import sys, glob, os
import pandas as pd
for f in sorted(glob.glob(os.path.join(sys.argv[1], "*.parquet"))):
    d = pd.read_parquet(f, columns=["ps_status", "ps_nic", "ps_nco", "cws_nic", "earn_regular", "cws_status"])
    wk = d[d.ps_status.between(11, 51)]
    print(os.path.basename(f), "nic len:", wk.ps_nic.str.len().value_counts().to_dict(),
          "nco len:", wk.ps_nco.str.len().value_counts().to_dict())
    print("  nco starting 25/35 (top):", wk.ps_nco[wk.ps_nco.str[:2].isin(["25", "35"])].value_counts().head(12).to_dict())
    print("  nic 62/63 5d (top):", wk.ps_nic[wk.ps_nic.str[:2].isin(["62", "63"])].value_counts().head(10).to_dict(),
          " 822xx:", int((wk.ps_nic.str[:3] == "822").sum()))
    rs = d[d.cws_status.isin([31, 71, 72])]
    print("  regular CWS n=", len(rs), "earn>0:", int((rs.earn_regular > 0).sum()), "earn na:", int(rs.earn_regular.isna().sum()))
