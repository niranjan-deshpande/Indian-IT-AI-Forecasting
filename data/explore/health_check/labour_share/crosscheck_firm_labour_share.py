"""Cross-check firm_labour_share.csv against (a) repo quarterly panel (employee cost, revenue summed to FY)
and (b) Screener's integer-rounded Employee Cost %, plus primary-filing spot checks typed in below.
Writes crosscheck_firm_labour_share.csv. Run: python3 -I crosscheck_firm_labour_share.py
"""
import os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))

out = pd.read_csv(os.path.join(HERE, 'firm_labour_share.csv'))
p = pd.read_csv(os.path.join(REPO, 'data', 'tidy', 'panel_long.csv'))
p = p[p.metric.isin(['employee_cost', 'revenue']) & p.unit.str.startswith('INR')]
p = p[(p.dim_type == 'total') | (p.metric == 'employee_cost')]
p = p[p.dimension != 'Employee cost (expense by nature)']  # TCS FY26: avoid double count with COR+SG&A split
p = p[p.fiscal_q.str.match(r'Q\dFY\d\d$')]
p['fy'] = 'FY' + p.fiscal_q.str[-2:]
p['v'] = p.value / p.unit.map({'INR_cr': 1, 'INR_mn': 10})
g = p.groupby(['firm', 'metric', 'fy']).agg(v=('v', 'sum'), nq=('fiscal_q', 'nunique')).reset_index()
g = g[g.nq == 4]
rows = []
fmap = {'ltim': 'ltim'}
for _, r in g.iterrows():
    col = 'employee_cost_inr_cr' if r.metric == 'employee_cost' else 'revenue_inr_cr'
    m = out[(out.firm == r.firm) & (out.fy == r.fy)]
    if m.empty or r.fy < 'FY16':
        continue
    used = m[col].iloc[0]
    rows.append(dict(check='repo_panel_vs_used', firm=r.firm, fy=r.fy, item=r.metric, repo_or_primary=round(r.v, 1),
                     used=used, diff_pct=round((used / r.v - 1) * 100, 2)))

# Screener integer Employee Cost % vs used employee cost / revenue
sp = pd.read_csv(os.path.join(HERE, 'raw_parsed_screener_tickertape.csv'))
sp = sp[sp.period.str.startswith('Mar')]
sp['fy'] = 'FY' + sp.period.str[6:8]
sp['firm'] = sp.apply(lambda r: 'lti' if (r.firm == 'ltim' and r.fy <= 'FY22') else r.firm, axis=1)
for _, r in sp.iterrows():
    m = out[(out.firm == r.firm) & (out.fy == r.fy)]
    if m.empty or pd.isna(r.scr_emp_pct) or (r.firm == 'lti' and r.fy == 'FY22'):  # Screener FY22 = restated LTIM
        continue
    rr = m.employee_cost_to_revenue.iloc[0] * 100
    rows.append(dict(check='screener_int_pct_vs_used', firm=r.firm, fy=r.fy, item='employee_cost_pct_revenue',
                     repo_or_primary=r.scr_emp_pct, used=round(rr, 2), diff_pct=round(rr - r.scr_emp_pct, 2)))

# Primary-filing spot checks (INR crore), filled from filings read in this task
PRIMARY = [
    # firm, fy, item, value, source
    ('lti', 'FY16', 'revenue', 5846.4, 'LTI FY17 SEBI consolidated results (Ind AS), CFS_outcome.pdf p3'),
    ('lti', 'FY16', 'employee_cost', 3526.6, 'LTI FY17 SEBI consolidated results (Ind AS), CFS_outcome.pdf p3'),
    ('lti', 'FY17', 'revenue', 6500.9, 'LTI FY17 SEBI consolidated results, CFS_outcome.pdf p3'),
    ('lti', 'FY17', 'employee_cost', 3775.8, 'LTI FY17 SEBI consolidated results, CFS_outcome.pdf p3 (Tickertape: 3,715.3)'),
    ('lti', 'FY21', 'employee_cost', 7428.9, 'LTI Q1FY22 SEBI consolidated results, year ended Mar-21 column'),
    ('lti', 'FY21', 'revenue', 12369.8, 'LTI Q1FY22 SEBI consolidated results, year ended Mar-21 column'),
    ('lti', 'FY22', 'employee_cost', 9700.7, 'LTI Q4FY22 SEBI consolidated results'),
    ('infosys', 'FY17', 'employee_cost_pct_revenue', 5612 / 10208 * 100, 'Infosys 20-F FY2017 IFRS USD (5,612/10,208)'),
    ('infosys', 'FY16', 'employee_cost_pct_revenue', 5236 / 9501 * 100, 'Infosys 20-F FY2017 IFRS USD (5,236/9,501)'),
    ('hcltech', 'FY16', 'revenue', 40913.0, 'HCL IR release Q3FY16: 12m Apr15-Mar16 revenue (US GAAP)'),
    ('hcltech', 'FY16', 'ebitda', 8795.0, 'HCL IR release Q3FY16: 12m Apr15-Mar16 EBITDA (US GAAP)'),
]
for firm, fy, item, v, src in PRIMARY:
    m = out[(out.firm == firm) & (out.fy == fy)]
    col = {'revenue': 'revenue_inr_cr', 'employee_cost': 'employee_cost_inr_cr', 'ebitda': 'ebitda_inr_cr',
           'employee_cost_pct_revenue': 'employee_cost_to_revenue'}[item]
    used = m[col].iloc[0] * (100 if item.endswith('pct_revenue') else 1)
    diff = (used - v) if item.endswith('pct_revenue') else (used / v - 1) * 100
    rows.append(dict(check='primary_filing', firm=firm, fy=fy, item=item, repo_or_primary=round(v, 2),
                     used=round(used, 2), diff_pct=round(diff, 2), source=src))

cc = pd.DataFrame(rows)
cc.to_csv(os.path.join(HERE, 'crosscheck_firm_labour_share.csv'), index=False)
pd.set_option('display.width', 200, 'display.max_rows', 400)
print(cc[cc.check != 'screener_int_pct_vs_used'].to_string())
s = cc[cc.check == 'screener_int_pct_vs_used']
print('screener int pct: max |diff| =', s.diff_pct.abs().max(), '; n>0.5:', (s.diff_pct.abs() > 0.5).sum(), 'of', len(s))
print(s[s.diff_pct.abs() > 0.5])
