"""Print value-label sets attached to given variables. Usage: python3 -I value_labels.py FILE var1,var2"""
import sys
import pandas as pd
f, vars_ = sys.argv[1], sys.argv[2].split(",")
with pd.io.stata.StataReader(f) as r:
    r._ensure_open() if hasattr(r, "_ensure_open") else None
    labs = r.value_labels()
    lblist = r._lbllist if hasattr(r, "_lbllist") else None
    varlist = r._varlist
    for v in vars_:
        i = varlist.index(v)
        name = lblist[i] if lblist else None
        print(f"== {v} -> {name}")
        if name and name in labs:
            for k, t in labs[name].items():
                print(f"   {k}: {t}")
