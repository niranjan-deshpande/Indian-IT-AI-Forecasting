"""Approximate PLFS wage bill for IT (NIC 62+63) from repo AGGREGATES only (no unit data).

wage_bill ~= sum over age bands of employment(band, UPS, NIC 62+63) x mean monthly earnings(band) x 12
  earnings: CWS regular wage workers in NIC 62/63 (round3/plfs/earnings_regular_salaried.csv)
  bands without an earnings cell: 15-20 gets the 21-25 mean; 41-60 gets the 31-40 mean (likely an understatement)
This mimics the Substack's numerator ("PLFS earnings scaled to the population") only roughly: it applies
regular-salaried means to all workers (incl. ~10% self-employed/casual) and mixes UPS employment with CWS earnings.

Run: python3 -I build_plfs_wagebill_approx.py
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
PLFS = HERE.parents[1] / "round3" / "plfs"
emp = pd.read_csv(PLFS / "employment_levels_long.csv")
earn = pd.read_csv(PLFS / "earnings_regular_salaried.csv")

emp = emp[emp.group.eq("nic62_63")]
e = earn[earn["sample"].eq("cws_regular_nic62_63")].set_index(["round", "age_band"]).mean_inr
bandmap = {"age_15_20": "21-25", "age_21_25": "21-25", "age_26_30": "26-30", "age_31_40": "31-40", "age_41_60": "31-40"}
out = []
for rnd, g in emp.groupby("round"):
    tot = g.loc[g.cut.eq("all"), "estimate"].iloc[0]
    bands = g[g.cut.isin(bandmap)]
    wb = sum(r.estimate * e[(rnd, bandmap[r.cut])] * 12 for r in bands.itertuples())
    covered = bands.estimate.sum()
    wb_scaled = wb * tot / covered  # scale for ages outside 15-60
    out.append({"round": rnd, "employment_nic62_63": round(tot), "employment_in_bands": round(covered),
                "wage_bill_inr_crore_approx": round(wb_scaled / 1e7), "wage_bill_lakh_crore_approx": round(wb_scaled / 1e12, 2),
                "method": "sum_band emp(UPS) x CWS regular mean earnings x 12; 15-20->21-25 mean, 41-60->31-40 mean; scaled to all ages",
                "source": "data/explore/round3/plfs/employment_levels_long.csv; earnings_regular_salaried.csv (repo aggregates of PLFS unit data)"})
o = pd.DataFrame(out)
o.to_csv(HERE / "plfs_it_wagebill_approx.csv", index=False)
print(o[["round", "employment_nic62_63", "wage_bill_lakh_crore_approx"]].to_string(index=False))
