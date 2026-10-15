"""Print variable names, labels and row counts of Stata files (metadata only).
Usage: python3 -I inspect_dta.py FILE [FILE ...]"""
import sys
import pandas as pd

for f in sys.argv[1:]:
    with pd.io.stata.StataReader(f) as r:
        vl = r.variable_labels()
        try:
            lab = r.value_labels()
        except Exception:
            lab = {}
        print(f"=== {f}")
        print("data_label:", r.data_label)
        n = r.nobs if hasattr(r, "nobs") else None
        print("nobs:", getattr(r, "_nobs", n))
        for k, v in vl.items():
            print(f"  {k}\t{v}")
        if lab:
            print("  value label sets:", list(lab)[:50])
