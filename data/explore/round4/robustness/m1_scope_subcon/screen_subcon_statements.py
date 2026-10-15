"""Hand-screened subset of subcon_statement_candidates.csv that bears on (a) the cost of subcontractors relative
to own staff (the conversion factor) and (b) the direction/timing of in-sourcing. Also computes the HCLTech
implied cost per added contractor (FY22) from audit/subcontracting_series.csv.
    python3 data/explore/round4/robustness/m1_scope_subcon/screen_subcon_statements.py
Output: subcon_statements_screened.csv
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
cand = pd.read_csv(OUT / "subcon_statement_candidates.csv")
PICK = [  # firm, call, substring that identifies the sentence, use
    ("Wipro", "Q1FY23", "30% higher", "conversion: subcon cost per head ~1.3x own employees (m_mid)"),
    ("TechM", "Q2FY22", "higher than the cost of our associates", "conversion: subcon cost > own staff (m >= 1)"),
    ("TechM", "Q3FY22", "replace them with full time headcount", "mechanism: subcons replaced by own headcount"),
    ("TechM", "Q1FY24", "replacing Subcon with a full-time headcount", "mechanism: subcons replaced by own headcount"),
    ("TechM", "Q1FY24", "16% to 14%", "level: TechM target <=10%"),
    ("HCLTech", "Q1FY22", "third-party contractors whose number", "count: +~3,000 contractors over 2 quarters"),
    ("HCLTech", "Q2FY22", "3,500-odd", "count: +~3,500 contractors over 3 quarters"),
    ("HCLTech", "Q2FY24", "reduction in 3rd party contractors", "direction: FY24 contractor cut"),
    ("HCLTech", "Q1FY27", "insourcing", "direction: earlier insourcing"),
    ("Infosys", "Q4FY22", "balance demand was being fulfilled by subcons", "mechanism: subcons are the flexible margin in a boom"),
    ("Infosys", "Q1FY23", "6%-6.5% of subcon", "level: 'normal' 6-6.5% vs 11.3%"),
    ("Infosys", "Q4FY24", "optimum level of 5% to 6%", "level: optimum 5-6%"),
    ("Infosys", "Q2FY26", "increase in subcon", "direction: FY26 rise"),
    ("TCS", "Q1FY23", "9.7% of our revenues", "level: TCS 'about 7%' normal vs 9.7%"),
    ("TCS", "Q4FY24", "bottomed out", "direction: FY24 lever exhausted"),
    ("TCS", "Q4FY26", "external consultants", "direction: FY26 rise, 40 bps"),
    ("LTIMindtree", "Q1FY27", "320 bps", "direction: FY27 rise continues (+320 bps YoY)"),
    ("LTIMindtree", "Q1FY27", "taking them as subcons", "mechanism: vendor-consolidation deals take client staff as subcons"),
]
rows = []
for firm, call, key, use in PICK:
    m = cand[(cand.firm == firm) & (cand.call == call) & cand.sentence.str.contains(key, regex=False)]
    if m.empty:
        rows.append(dict(firm=firm, call=call, page="", use=use, excerpt="(not found)"))
        continue
    r = m.iloc[0]
    s = r.sentence
    i = s.find(key)
    rows.append(dict(firm=firm, call=call, call_date=r.call_date, page=r.page, use=use,
                     excerpt=s[max(0, i - 160): i + len(key) + 120]))
# HCLTech implied annual cost per added contractor, FY22 (upper bound: the 'outsourcing costs' line also contains
# outsourced work other than contractors, and grew with revenue)
S = pd.read_csv(ROOT / "audit/subcontracting_series.csv")
h = S[(S.firm == "hcltech") & (S.period_type == "quarter")].set_index("fiscal_q").subcon_inr
cph = pd.read_csv(ROOT / "data/explore/round3/seniority_firms/cost_per_head.csv")
c22 = cph[(cph.firm == "hcltech") & (cph.fy == "FY22")].cost_per_head_inr_lakh.iloc[0]
for lab, q0, q1, n in [("2 quarters to Q1FY22", "Q3FY21", "Q1FY22", 3000), ("3 quarters to Q2FY22", "Q3FY21", "Q2FY22", 3500)]:
    d = (h[q1] - h[q0]) * 4                       # INR mn, annualised
    per = d * 1e6 / n / 1e5                       # INR lakh per contractor per year
    rows.append(dict(firm="HCLTech", call=lab, use="implied cost per added contractor (upper bound)",
                     excerpt=f"outsourcing cost {q0} {h[q0]:.0f} -> {q1} {h[q1]:.0f} INR mn/qtr; x4 / {n} contractors = "
                             f"{per:.1f} lakh/yr vs employee cost per head FY22 {c22:.2f} lakh -> ratio {per / c22:.2f}"))
pd.DataFrame(rows).to_csv(OUT / "subcon_statements_screened.csv", index=False)
print(pd.DataFrame(rows)[["firm", "call", "use", "excerpt"]].to_string())
