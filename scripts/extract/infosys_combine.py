"""Combine Infosys parsed outputs into data/raw/infosys.csv (schema order), dropping exact within-document duplicates."""
import pandas as pd, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from infosys_common import COLS, BASE
parts = [pd.read_csv(f"{BASE}/{f}", dtype=str) for f in ["parsed_factsheets.csv", "parsed_subcontract.csv", "parsed_manual.csv"]]
d = pd.concat(parts, ignore_index=True)[COLS]
d["value_num"] = pd.to_numeric(d["value"])
key = ["fiscal_q", "metric", "dimension", "dim_type", "unit", "basis", "period_type", "source_url"]
# same doc, same key, same value -> keep first (e.g. revenue shown in both P&L and constant-currency block)
d = d.drop_duplicates(key + ["value_num"])
# same doc, same key, different values -> flag
dup = d[d.duplicated(key, keep=False)]
if len(dup):
    print("CONFLICTS within document:", len(dup)); print(dup[key + ["value", "source_loc"]].head(40).to_string())
d = d.sort_values(["period_end", "metric", "dim_type", "dimension", "doc_date"]).drop(columns="value_num")
os.makedirs("data/raw", exist_ok=True)
d.to_csv("data/raw/infosys.csv", index=False)
print("rows", len(d))
