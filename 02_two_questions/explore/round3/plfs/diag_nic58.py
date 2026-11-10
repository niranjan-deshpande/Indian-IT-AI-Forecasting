"""Weighted share of NIC 58 ICT-occupation workers in NIC 582 (software publishing). Usage: python3 -I diag_nic58.py WORK_DIR"""
import sys, os
import pandas as pd
for r in ["2021-22", "2022-23", "2023-24", "cy2024", "cy2025"]:
    d = pd.read_parquet(os.path.join(sys.argv[1], r + ".parquet"))
    s = d.ps_status.isin([11, 12, 21, 31, 41, 51]) & d.ps_nco.isin(["251", "252", "351"]) & (d.ps_nic.str[:2] == "58")
    ict = d.ps_status.isin([11, 12, 21, 31, 41, 51]) & d.ps_nco.isin(["251", "252", "351"])
    w582 = d.w[s & (d.ps_nic.str[:3] == "582")].sum()
    print(r, "NIC58 ICT (k)=%.0f" % (d.w[s].sum() / 1e3), "of which 582 share=%.2f" % (w582 / d.w[s].sum()),
          " outside-IT share if 58 counted as IT=%.3f" % ((d.w[ict & ~d.ps_nic.str[:2].isin(["62", "63", "58"])].sum()) / d.w[ict].sum()))
