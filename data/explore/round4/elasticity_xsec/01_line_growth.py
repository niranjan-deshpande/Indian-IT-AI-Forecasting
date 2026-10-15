"""M6 step 1: service-line revenue growth, pre (2016-2022 ex-COVID) vs recent (2024Q2-2026Q2).
Replicates scripts/03_part2.py::sl_growth (D33: reported cc YoY where given, else YoY log change of levels in
reported currency) without modifying it. Splices Accenture Outsourcing->Managed Services and TechM BPO->BPS.
Output: line_growth_firms.csv (one row per firm x line x window)."""
from pathlib import Path
import numpy as np, pandas as pd
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
p = pd.read_csv(ROOT / "data/tidy/panel_long.csv", low_memory=False)

x = p[(p.dim_type == "service_line") & (p.metric == "segment_growth_yoy") & (p.period_type == "quarter")]
x = x.sort_values("basis").drop_duplicates(["firm", "cal_q", "dimension"])
g = x[["firm", "cal_q", "dimension", "value", "basis"]].rename(columns={"value": "g"})
g["g"] = 100 * np.log1p(g.g / 100)
lev = p[(p.dim_type == "service_line") & (p.metric == "segment_revenue") & (p.period_type == "quarter")].copy()
lev["dimension"] = lev.dimension.replace({"BPO": "BPS"})
lev = lev.sort_values(["unit", "doc_date"], ascending=[True, False]).drop_duplicates(["firm", "cal_q", "dimension"])
out = []
for (f, dim), s in lev.groupby(["firm", "dimension"]):
    s = s.set_index("cal_q").value.sort_index()
    for q in s.index:
        ql = f"{int(q[:4]) - 1}Q{q[-1]}"
        if ql in s.index and s[ql] > 0:
            out.append(dict(firm=f, cal_q=q, dimension=dim, g=100 * np.log(s[q] / s[ql]), basis="level_reported_ccy"))
lv = pd.DataFrame(out)
g["dimension"] = np.where((g.firm == "techm") & (g.dimension == "BPO"), "BPS", g.dimension)
both = pd.concat([g, lv], ignore_index=True)
both["pri"] = both.basis.map({"cc": 0, "reported": 1}).fillna(2)
slg = both.sort_values("pri").drop_duplicates(["firm", "cal_q", "dimension"]).drop(columns="pri")

LINES = {  # (firm, reported dimension) -> line id used in M6
    ("accenture", "Consulting"): "ACN_Consulting",
    ("accenture", "Outsourcing"): "ACN_ManagedSvcs", ("accenture", "Managed Services"): "ACN_ManagedSvcs",
    ("cognizant", "Consulting and technology services"): "CTSH_ConsultTech",
    ("cognizant", "Outsourcing services"): "CTSH_Outsourcing",
    ("hcltech", "IT and Business Services"): "HCL_ITBS",
    ("hcltech", "Engineering and R&D Services"): "HCL_ERD",
    ("techm", "IT"): "TECHM_IT", ("techm", "BPS"): "TECHM_BPS",
}
slg["line"] = [LINES.get((f, d)) for f, d in zip(slg.firm, slg.dimension)]
slg = slg.dropna(subset=["line"]).sort_values("pri" if "pri" in slg else "basis")
# where both pre- and post-rename rows exist for a quarter, keep the first (cc preferred)
slg = slg.drop_duplicates(["firm", "cal_q", "line"])
slg.to_csv(HERE / "line_growth_quarterly.csv", index=False)

COVID = ["2020Q2", "2020Q3", "2020Q4", "2021Q1", "2021Q2"]
WIN = {"pre_2016_2022": ("2016Q1", "2022Q4"), "pre_2016_2019": ("2016Q1", "2019Q4"),
       "fy24_2023Q1_2024Q1": ("2023Q1", "2024Q1"), "recent_2024Q2_2026Q2": ("2024Q2", "2026Q2")}
rows = []
for (f, line), s in slg.groupby(["firm", "line"]):
    for w, (a, b) in WIN.items():
        z = s[(s.cal_q >= a) & (s.cal_q <= b) & (~s.cal_q.isin(COVID))]
        rows.append(dict(firm=f, line=line, window=w, mean_g=z.g.mean(), sd_g=z.g.std(), n_q=len(z),
                         first_q=z.cal_q.min(), last_q=z.cal_q.max(), bases=";".join(sorted(z.basis.unique()))))
r = pd.DataFrame(rows)
r.to_csv(HERE / "line_growth_firms.csv", index=False)
print(r.pivot_table(index=["firm", "line"], columns="window", values=["mean_g", "n_q"]).round(2).to_string())
