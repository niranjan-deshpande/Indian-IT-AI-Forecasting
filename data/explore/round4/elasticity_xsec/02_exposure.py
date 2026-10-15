"""M6 step 2: exposure per service line / segment.
line -> occupation mix (JUDGMENTAL weights, written out in line_occupation_map.csv) -> occupation exposure score.
Scores (all from data/explore/lca/exposure, unweighted across occupations):
  E_gpt   Eloundou et al. (2023) GPT-4 rating, beta = E1 + 0.5*E2 (dv_rating_beta), O*NET-SOC 2019
  E_human Eloundou et al. (2023) human-annotator rating, beta (human_rating_beta)
  F_lm    Felten-Raj-Seamans Language-Modeling AIOE, SOC 2010
Each score is converted to its percentile rank across all occupations in its file (0-1), so that the three are on a
common scale and a proportional mapping to price cuts (s_j proportional to exposure) is defined.
Two composition variants:
  compA  'task-content' mixes (base)
  compB  alternative: consulting = strategy/analyst-heavy, BPO = back-office (F&A/data) heavy rather than voice,
         ER&D = more software-heavy (embedded), managed services = less BPO.
Output: line_occupation_map.csv, occupation_scores.csv, line_exposure.csv"""
from pathlib import Path
import pandas as pd
HERE = Path(__file__).resolve().parent
EXP = HERE.parents[1] / "lca" / "exposure"
el = pd.read_csv(EXP / "eloundou_occ_level.csv")
fe = pd.read_csv(EXP / "felten_aioe_soc2010.csv")
el["soc6"] = el["O*NET-SOC Code"].str[:7]
el_pct = el.assign(E_gpt=el.dv_rating_beta.rank(pct=True), E_human=el.human_rating_beta.rank(pct=True))
fe_pct = fe.assign(F_lm=fe["Language Modeling AIOE"].rank(pct=True))

# occupation bundles: code (SOC2018 / O*NET 2019 6-digit, SOC2010 for Felten)
OCC = {
    "DEV":    ("Software developers",                 ["15-1252"], ["15-1132", "15-1133"]),
    "TEST":   ("Software QA analysts & testers",      ["15-1253"], ["15-1199"]),
    "SYSAN":  ("Computer systems analysts",           ["15-1211"], ["15-1121"]),
    "INFRA":  ("Network & computer systems admins",   ["15-1244"], ["15-1142"]),
    "HELP":   ("Computer user support specialists",   ["15-1232"], ["15-1151"]),
    "ITMGR":  ("Computer & IS managers",              ["11-3021"], ["11-3021"]),
    "CSR":    ("Customer service representatives",    ["43-4051"], ["43-4051"]),
    "BOOKK":  ("Bookkeeping/accounting clerks",       ["43-3031"], ["43-3031"]),
    "ACCT":   ("Accountants & auditors",              ["13-2011"], ["13-2011"]),
    "DATAE":  ("Data entry keyers",                   ["43-9021"], ["43-9021"]),
    "OFFSUP": ("Supervisors of office/admin workers", ["43-1011"], ["43-1011"]),
    "HRAS":   ("HR assistants",                       ["43-4161"], ["43-4161"]),
    "MGMTAN": ("Management analysts",                 ["13-1111"], ["13-1111"]),
    "MKTRES": ("Market research analysts",            ["13-1161"], ["13-1161"]),
    "MECH":   ("Mechanical engineers",                ["17-2141"], ["17-2141"]),
    "ELEC":   ("Electronics engineers",               ["17-2072"], ["17-2072"]),
    "HW":     ("Computer hardware engineers",         ["17-2061"], ["17-2061"]),
    "DRAFT":  ("Mechanical drafters",                 ["17-3013"], ["17-3013"]),
    "INDENG": ("Industrial engineers",                ["17-2112"], ["17-2112"]),
}
srows = []
for k, (title, c18, c10) in OCC.items():
    e = el_pct[(el_pct.soc6.isin(c18)) & (el_pct["O*NET-SOC Code"].str.endswith(".00"))]
    f = fe_pct[fe_pct["SOC Code"].isin(c10)]
    assert len(e) and len(f), k
    srows.append(dict(occ=k, title=title, soc2018=";".join(c18), soc2010=";".join(c10),
                      E_gpt_raw=e.dv_rating_beta.mean(), E_human_raw=e.human_rating_beta.mean(),
                      F_lm_raw=f["Language Modeling AIOE"].mean(),
                      E_gpt=e.E_gpt.mean(), E_human=e.E_human.mean(), F_lm=f.F_lm.mean()))
S = pd.DataFrame(srows).set_index("occ")
S.round(3).to_csv(HERE / "occupation_scores.csv")

# activity blocks
ADM  = {"DEV": .40, "TEST": .15, "SYSAN": .10, "INFRA": .15, "HELP": .10, "ITMGR": .10}
BPO_A = {"CSR": .45, "BOOKK": .15, "ACCT": .10, "DATAE": .10, "OFFSUP": .10, "HRAS": .05, "MKTRES": .05}
BPO_B = {"CSR": .20, "BOOKK": .25, "ACCT": .20, "DATAE": .15, "OFFSUP": .10, "HRAS": .10}
ERD_A = {"DEV": .30, "MECH": .20, "ELEC": .15, "HW": .10, "DRAFT": .10, "INDENG": .10, "TEST": .05}
ERD_B = {"DEV": .50, "TEST": .10, "MECH": .15, "ELEC": .10, "HW": .10, "DRAFT": .05}
CONS_A = {"MGMTAN": .25, "SYSAN": .20, "DEV": .30, "ITMGR": .10, "MKTRES": .10, "TEST": .05}
CONS_B = {"MGMTAN": .50, "MKTRES": .15, "SYSAN": .15, "DEV": .15, "ITMGR": .05}
PROD = {"DEV": .60, "TEST": .10, "SYSAN": .10, "ITMGR": .10, "MKTRES": .10}
def mix(*parts):
    out = {}
    for w, block in parts:
        for k, v in block.items():
            out[k] = out.get(k, 0) + w * v
    return out
COMP = {
  "compA": {
    "ACN_Consulting": CONS_A, "ACN_ManagedSvcs": mix((.6, ADM), (.4, BPO_A)),
    "CTSH_ConsultTech": CONS_A, "CTSH_Outsourcing": mix((.8, ADM), (.2, BPO_A)),
    "HCL_ITBS": mix((.9, ADM), (.1, BPO_A)), "HCL_ERD": ERD_A,
    "TECHM_IT": ADM, "TECHM_BPS": BPO_A,
    "RBI_IT_services": ADM, "RBI_BPO": BPO_A, "RBI_Engineering": ERD_A, "RBI_SW_products": PROD},
  "compB": {
    "ACN_Consulting": CONS_B, "ACN_ManagedSvcs": mix((.75, ADM), (.25, BPO_B)),
    "CTSH_ConsultTech": mix((.5, CONS_B), (.5, ADM)), "CTSH_Outsourcing": mix((.9, ADM), (.1, BPO_B)),
    "HCL_ITBS": mix((.95, ADM), (.05, BPO_B)), "HCL_ERD": ERD_B,
    "TECHM_IT": mix((.8, ADM), (.2, ERD_B)), "TECHM_BPS": BPO_B,
    "RBI_IT_services": ADM, "RBI_BPO": BPO_B, "RBI_Engineering": ERD_B, "RBI_SW_products": PROD},
}
mrows, lrows = [], []
for cv, lines in COMP.items():
    for line, w in lines.items():
        assert abs(sum(w.values()) - 1) < 1e-9, (cv, line)
        for k, v in w.items():
            mrows.append(dict(composition=cv, line=line, occ=k, title=OCC[k][0], weight=round(v, 4)))
        row = dict(composition=cv, line=line)
        for m in ["E_gpt", "E_human", "F_lm", "E_gpt_raw", "E_human_raw", "F_lm_raw"]:
            row[m] = sum(v * S.loc[k, m] for k, v in w.items())
        lrows.append(row)
pd.DataFrame(mrows).to_csv(HERE / "line_occupation_map.csv", index=False)
L = pd.DataFrame(lrows)
L.round(4).to_csv(HERE / "line_exposure.csv", index=False)
print(S[["E_gpt_raw", "E_human_raw", "F_lm_raw", "E_gpt", "E_human", "F_lm"]].round(2).to_string())
print(L.round(3).to_string())
