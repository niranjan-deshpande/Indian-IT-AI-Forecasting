"""Helpers to load raw downloads into tidy frames."""
import json, pandas as pd, os
RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "raw_output")
def dn_tidy(fname):
    d = json.load(open(os.path.join(RAW, "wto", fname)))
    rows = []
    for s in d["series"]["docs"]:
        dims = s["dimensions"]
        for p, v in zip(s["period"], s["value"]):
            rows.append(dict(reporter=dims["reporting-economies"], sector=dims["products-sector"], period=p, value=None if v == "NA" else v))
    t = pd.DataFrame(rows); t["value"] = pd.to_numeric(t["value"], errors="coerce") / 1000.0  # USD mn -> bn
    return t
def imf(fname):
    d = pd.read_csv(os.path.join(RAW, "imf", fname), low_memory=False)
    d = d[d.COUNTRY.notna()]
    d["value"] = d.OBS_VALUE / 1e9  # SCALE 6? check below
    return d
