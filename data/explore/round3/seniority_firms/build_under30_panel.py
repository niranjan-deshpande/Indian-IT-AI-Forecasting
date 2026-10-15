"""Combine <30 share of headcount and of new hires for the 6 large firms (existing data/explore/workforce/firm_year_junior_metrics.csv)
and 4 mid-tier firms (midtier_age_tables.csv, this folder). Output: under30_panel.csv (long-ish, one row per firm-year)."""
import pandas as pd, pathlib, re
here = pathlib.Path(__file__).parent
root = here.parents[3]
big = pd.read_csv(root/'data/explore/workforce/firm_year_junior_metrics.csv')
big = big[big.fy >= 2019][['firm','fy','sh_lt30','sh_hires_lt30']].rename(columns={'sh_lt30':'hc_share_lt30','sh_hires_lt30':'hires_share_lt30'})
big['source'] = 'data/explore/workforce (ESG/GRI annexes)'
m = pd.read_csv(here/'midtier_age_tables.csv')
m = m[m.status=='CONFIRMED']
m = m[~m.fiscal_year.astype(str).str.contains('as printed')]
def fy(s):
    s = str(s); n = re.findall(r'\d+', s)[0]
    return 2000 + int(n[-2:])
m['fy'] = m.fiscal_year.map(fy)
m['firm'] = m.firm.str.lower()
rows = []
for (f, y), g in m.groupby(['firm','fy']):
    r = {'firm': f, 'fy': y, 'source': 'midtier_age_tables.csv'}
    for met, col in [('headcount_by_age','hc_share_lt30'), ('hires_by_age','hires_share_lt30')]:
        x = g[(g.metric==met)]
        sc = x.scope.fillna('')
        lvl = sc.str.startswith('Level x age'); con = sc.str.lower().str.startswith('contractual')
        firmwide = x[~lvl & ~con]
        if firmwide.age_band.isin(['<30']).any():
            x = firmwide.drop_duplicates('age_band', keep='last').set_index('age_band').value
        else:  # e.g. Mphasis FY21: no firm-wide row, sum level x age rows
            x = x[lvl].groupby('age_band').value.sum()
        lt = x.get('<30'); bands = x.reindex(['<30','30-50','>50']).dropna()
        if lt is not None and len(bands)==3:
            r[col] = round(100*lt/bands.sum(), 2)
    rows.append(r)
mid = pd.DataFrame(rows)
out = pd.concat([big, mid], ignore_index=True).sort_values(['firm','fy'])
out['note'] = out.firm.map({'hexaware':'calendar year (CY=fy)', 'coforge':'India incl. contract staff', 'persistent':'global incl. contract staff',
                            'tcs':'India only, read from charts', 'mphasis':'global; FY21 derived from level rows'}).fillna('')
out.to_csv(here/'under30_panel.csv', index=False)
print(out.pivot(index='fy', columns='firm', values='hc_share_lt30').round(1).to_string())
print(out.pivot(index='fy', columns='firm', values='hires_share_lt30').round(1).to_string())
