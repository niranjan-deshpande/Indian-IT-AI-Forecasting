"""Collects the M1 deliverable: (1-phi)s_bar ranges for FY24-26 by scope, plus breakdown points.
Run after m1_firm.py and m1_sector_pi.py.   python3 data/explore/round4/residual/m1_summary.py"""
from pathlib import Path
import pandas as pd

D = Path(__file__).resolve().parent
E = pd.read_csv(D / "m1_firm_estimates.csv")
T6 = pd.read_csv(D / "m1_top6_range.csv")
SC = pd.read_csv(D / "sector_m1_changes.csv")
PREF = "imputed cc + Infosys trainee-incl. utilisation"
rows = []
for _, r in E[E.series.isin([PREF, "pilot (cc only)"])].iterrows():
    rows.append(dict(scope="firm: 4 firms with utilisation", series=r.series, window=r.window,
                     estimate=r.yearclust, lo95=r.yearclust_lo95, hi95=r.yearclust_hi95,
                     d27_lo95=r.within_d27_lo95, d27_hi95=r.within_d27_hi95, firms=r.firms_within,
                     dpi_rho_needed_to_reach_0=r.yearclust, dpi_rho_needed_to_reach_4=r.yearclust - 4,
                     dpi_rho_needed_for_lo95_above_0=r.yearclust_lo95))
for _, r in T6[T6.series.str.startswith("imputed")].iterrows():
    rows.append(dict(scope="firm: top six (TCS, HCLTech bounded by peer utilisation range)", series=r.series,
                     window=r.window, estimate=r.eq_mid, lo95=None, hi95=None, bound_lo=r.eq_lo, bound_hi=r.eq_hi,
                     revw_lo=r.revw_lo, revw_hi=r.revw_hi, firms=r.firms,
                     dpi_rho_needed_to_reach_0=r.eq_mid, dpi_rho_needed_to_reach_4=r.eq_mid - 4))
for _, r in SC.iterrows():
    rows.append(dict(scope="sector (illustrative only)", series=r.series, window=r.windows, estimate=r.delta,
                     lo95=r.delta_lo95, hi95=r.delta_hi95, firms="", dpi_rho_needed_to_reach_0=r.delta))
S = pd.DataFrame(rows)
S.round(2).to_csv(D / "m1_summary.csv", index=False)
pd.set_option("display.width", 250)
print(S.round(2).to_string())
