"""Aggregate NIRF UG-4yr placement data to a graduating-year series.
Run: python3 -I 03_aggregate_nirf.py <seniority_sector dir>
For each institution x graduating year, keep the value from the LATEST edition reporting it.
Balanced panel = institutions with a non-missing row for every grad year 2016-17..2023-24.
Tier: 'elite' = name contains IIT/Indian Institute of Technology/NIT/National Institute of Technology/IIIT/IISc/BITS;
'other' = everything else (mostly private and state colleges, the mass IT-services campus pool)."""
import sys, os, re, pandas as pd, numpy as np
base = sys.argv[1]
d = pd.read_csv(os.path.join(base, 'nirf_ug4_placement_long.csv'))
d = d[(d.n_grad_min_time > 0)]
# revision check on overlapping cells
k = ['inst_id', 'grad_year']
dup = d[d.duplicated(k, keep=False)].sort_values(k + ['edition'])
g = dup.groupby(k)
rev = pd.DataFrame({'placed_rng': g.n_placed.agg(lambda s: s.max() - s.min()), 'placed_mean': g.n_placed.mean()})
print('overlap cells', len(rev), 'share with any revision to n_placed', round((rev.placed_rng > 0).mean(), 3))
lat = d.sort_values('edition').groupby(k).tail(1).copy()
pat = r'Indian Institute of Technology|\bIIT\b|National Institute of Technology|\bNIT\b|Indian Institute of Information Technology|\bIIIT|Indian Institute of Science|Birla Institute'
lat['tier'] = np.where(lat.inst_name.str.contains(pat, case=False, regex=True), 'elite', 'other')
years = [f'{y}-{str(y+1)[2:]}' for y in range(2016, 2024)]
cnt = lat[lat.grad_year.isin(years)].groupby('inst_id').grad_year.nunique()
bal = cnt[cnt == len(years)].index
rows = []
for sample, sub in [('all_unbalanced', lat), ('balanced', lat[lat.inst_id.isin(bal)])]:
    for tier in ['all', 'elite', 'other']:
        s = sub if tier == 'all' else sub[sub.tier == tier]
        for gy, x in s[s.grad_year.isin(['2015-16'] + years)].groupby('grad_year'):
            rows.append(dict(sample=sample, tier=tier, grad_year=gy, n_inst=x.inst_id.nunique(),
                             graduates=x.n_grad_min_time.sum(), placed=x.n_placed.sum(),
                             higher_studies=x.n_higher_studies.sum(),
                             placement_rate=round(x.n_placed.sum() / x.n_grad_min_time.sum(), 3),
                             median_of_inst_median_salary=x.median_salary_inr.median(),
                             grad_wtd_mean_salary=round((x.median_salary_inr * x.n_grad_min_time).sum() / x.n_grad_min_time.sum())))
out = pd.DataFrame(rows)
out['source'] = 'NIRF Data Submitted by Institution PDFs, Engineering, editions 2019-2025: https://www.nirfindia.org/nirfpdfcdn/<edition>/pdf/Engineering/<ID>.pdf (row-level URLs in nirf_ug4_placement_long.csv)'
out.to_csv(os.path.join(base, 'nirf_ug4_placement_by_gradyear.csv'), index=False)
pd.set_option('display.width', 250)
print(out[out['sample'] == 'balanced'].drop(columns='source').to_string(index=False))
print(out[(out['sample'] == 'all_unbalanced') & (out.tier == 'all')].drop(columns='source').to_string(index=False))
