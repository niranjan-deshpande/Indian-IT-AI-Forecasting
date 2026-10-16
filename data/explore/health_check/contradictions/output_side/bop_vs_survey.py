"""Reconcile RBI BoP 'computer services' (IMF SI2) with the RBI software-exports survey, using WTO's reallocation as a clue.
WTO's ITS_CS_QX moves a near-constant ~31% of India's telecom-computer-info (SI) into other business services (SJ);
SI+SJ is identical to IMF/RBI. That share matches the survey's ITeS share (ITeS/total), suggesting WTO reads RBI's
BoP 'software services' (=SI2) as computer services + ITeS/BPO.
Inputs: india_series_quarterly.csv (from baldwin_reproduce.py); data/explore/trade/rbi_survey_orgtype.csv;
        survey activity split FY24-26 from RBI press release prid=63625 / round3/red_team (typed below, USD bn).
Output: bop_vs_survey.csv. Run: python3 -I bop_vs_survey.py
"""
import os, pandas as pd
OUT = os.path.dirname(os.path.abspath(__file__))
EXPLORE = os.path.abspath(os.path.join(OUT, "..", "..", ".."))
q = pd.read_csv(os.path.join(OUT, "india_series_quarterly.csv")); q["p"] = pd.PeriodIndex(q.quarter, freq="Q")
q["fy"] = [p.year + 1 if p.quarter >= 2 else p.year for p in q.p]
fy = q.groupby("fy").agg(n=("imf_SI2", "count"), bop_SI2=("imf_SI2", "sum"), bop_SI=("imf_SI", "sum"), wto_SI=("wto_SI", lambda s: s.sum(min_count=4)), bop_SJ=("imf_SJ", "sum"))
fy = fy[fy.n == 4]
fy["wto_reallocated_share_of_SI_pct"] = (1 - fy.wto_SI / fy.bop_SI) * 100
s = pd.read_csv(os.path.join(EXPLORE, "trade", "rbi_survey_orgtype.csv"))
s["fy"] = s.fy.str[:4].astype(int) + 1
s = s.set_index("fy")[["total_usd_bn", "release_round"]].rename(columns={"total_usd_bn": "survey_total"})
# computer = IT services + software products; ITeS = BPO + engineering (round3/red_team/rbi_exports_by_activity_type.csv)
ites = pd.DataFrame({"survey_computer": {2024: 125.5 + 5.5, 2025: 131.3 + 6.8, 2026: 147.0 + 6.4}, "survey_ites": {2024: 50.1 + 9.6, 2025: 55.8 + 10.8, 2026: 56.0 + 12.0}})
r = fy.join(s, how="left").join(ites, how="left")
r["survey_ites_share_pct"] = r.survey_ites / r.survey_total * 100
r["bop_SI2_minus_survey_total"] = r.bop_SI2 - r.survey_total
r["bop_SI2_minus_survey_computer"] = r.bop_SI2 - r.survey_computer
r["bop_SI2_over_survey_total"] = r.bop_SI2 / r.survey_total
r = r.loc[2016:].round(2); r.index = [f"FY{str(i)[2:]}" for i in r.index]; r.index.name = "fy"
r.drop(columns="n").to_csv(os.path.join(OUT, "bop_vs_survey.csv")); print(r.drop(columns=["n", "release_round"]).to_string())
