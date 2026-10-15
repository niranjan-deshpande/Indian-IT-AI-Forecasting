"""Employee cost per average headcount (INR lakh/yr), from data/raw/<firm>.csv quarterly rows.
Illustrative seniority-mix proxy only: confounded by wage inflation, INR/USD (onsite pay), onsite share, subcontractors (excluded from cost),
and scope mismatch (cost is consolidated; headcount may exclude some subsidiaries)."""
import pandas as pd, pathlib
root = pathlib.Path(__file__).resolve().parents[4]
rows = []
def fy(q): return 'FY' + q[-2:]
for f, unit, dims in [('tcs','INR_mn',['Employee cost (in SG&A)','Employee cost (in cost of revenue)']),
                      ('hcltech','INR_cr',['total']), ('wipro','INR_mn',['total']), ('techm','INR_mn',['total'])]:
    d = pd.read_csv(root/f'data/raw/{f}.csv').sort_values('doc_date')
    e = d[(d.metric=='employee_cost') & (d.unit==unit) & (d.period_type=='quarter') & d.dimension.isin(dims)]
    e = e.drop_duplicates(['fiscal_q','dimension'], keep='last').groupby('fiscal_q').value.sum()
    h = d[(d.metric=='headcount') & (d.dimension=='total')].drop_duplicates('fiscal_q', keep='last').set_index('fiscal_q').value
    x = pd.DataFrame({'cost': e, 'hc': h}).dropna()
    x['fy'] = [fy(q) for q in x.index]
    g = x.groupby('fy').agg(cost=('cost','sum'), hc=('hc','mean'), n=('cost','count'))
    g = g[g.n==4]
    scale = 1e6 if unit=='INR_mn' else 1e7
    g['cost_per_head_inr_lakh'] = g.cost*scale/g.hc/1e5
    g['firm'] = f
    rows.append(g.reset_index())
out = pd.concat(rows)[['firm','fy','cost_per_head_inr_lakh','hc','n']]
out['yoy_log_x100'] = out.groupby('firm').cost_per_head_inr_lakh.transform(lambda s: 100*(s.apply(lambda v: __import__('math').log(v)).diff()))
out.to_csv(pathlib.Path(__file__).parent/'cost_per_head.csv', index=False, float_format='%.2f')
print(out[out.fy>='FY18'].pivot(index='fy', columns='firm', values='yoy_log_x100').round(1).to_string())
print(out[out.fy>='FY18'].pivot(index='fy', columns='firm', values='cost_per_head_inr_lakh').round(1).to_string())
