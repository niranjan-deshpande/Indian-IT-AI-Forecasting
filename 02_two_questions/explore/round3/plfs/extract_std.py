"""Read person-level first-visit files, keep mapped variables, harmonise, attach official weights,
and save standardised unit-level parquet files INSIDE data/sources (microdata never leaves it).
Usage: python3 -I extract_std.py EXTRACTED_DIR MAPPING_CSV OUT_WORK_DIR"""
import sys, os
import numpy as np
import pandas as pd

ext, mapf, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
m = pd.read_csv(mapf, dtype=str).fillna("")

def num(s):
    return pd.to_numeric(pd.Series(s).astype(str).str.strip().replace({"": np.nan, "nan": np.nan}), errors="coerce")

for rnd, g in m.groupby("round", sort=False):
    rel = g["file"].iloc[0]
    mp = {r.std_var: r.source_var for r in g.itertuples() if r.source_var}
    df = pd.read_stata(os.path.join(ext, rel), columns=list(mp.values()), convert_categoricals=False)
    df = df.rename(columns={v: k for k, v in mp.items()})
    o = pd.DataFrame(index=df.index)
    for c in ["quarter", "month", "visit", "state", "district", "stratum", "group", "substratum",
              "subsample", "fsu", "sgsb", "sss", "hhno", "person"]:
        if c in df:
            o[c] = df[c].astype(str).str.strip()
    for c in ["sector", "sex", "age", "gedu", "tedu", "ps_status", "ss_status", "cws_status",
              "earn_regular", "nss", "nsc", "mult", "no_qtr"]:
        if c in df:
            o[c] = num(df[c]).values
    for c in ["ps_nic", "ss_nic", "cws_nic", "ps_nco", "cws_nco"]:
        o[c] = df[c].astype(str).str.strip().replace({"nan": ""}) if c in df else ""
    # official weights (see README of each release)
    if rnd == "cy2025":
        o["w"] = o["mult"] / 100.0
        o["strata"] = o["state"] + "_" + o["sector"].astype(int).astype(str) + "_" + o["stratum"] + "_" + o["group"] + "_" + o["substratum"]
        o["psu"] = o["month"] + "_" + o["fsu"]
    else:
        div = np.where(o["nss"] == o["nsc"], 100.0, 200.0)
        o["w"] = o["mult"] / div / o["no_qtr"]
        o["strata"] = o["state"] + "_" + o["sector"].astype(int).astype(str) + "_" + o["stratum"] + "_" + o["substratum"]
        o["psu"] = o["quarter"] + "_" + o["fsu"]
    o["round"] = rnd
    o.to_parquet(os.path.join(out, f"{rnd}.parquet"), index=False)
    print(rnd, len(o), "pop(m)=%.1f" % (o["w"].sum() / 1e6), "missing w:", o["w"].isna().sum(),
          "psu:", o["psu"].nunique(), "strata:", o["strata"].nunique(), flush=True)
