"""Within-edition YoY change in UG-4yr placements (same institutions, same reporting vintage),
avoiding mixing first-reported and revised numbers. Run: python3 -I 04_within_edition_yoy.py <dir>"""
import sys, os, numpy as np, pandas as pd
base = sys.argv[1]
d = pd.read_csv(os.path.join(base, 'nirf_ug4_placement_long.csv')); d = d[d.n_grad_min_time > 0]
pat = r'Indian Institute of Technology|\bIIT\b|National Institute of Technology|\bNIT\b|Indian Institute of Information Technology|\bIIIT|Indian Institute of Science|Birla Institute'
tier = d.groupby('inst_id').inst_name.last().str.contains(pat, case=False, regex=True).map({True: 'elite', False: 'other'})
d['tier'] = d.inst_id.map(tier)
rows = []
for ed, x in d.groupby('edition'):
    gys = sorted(x.grad_year.unique())[-2:]  # last two grad years in this edition
    p = x[x.grad_year.isin(gys)].pivot_table(index=['inst_id', 'tier'], columns='grad_year',
            values=['n_placed', 'n_grad_min_time', 'n_higher_studies', 'median_salary_inr']).dropna()
    for t in ['all', 'elite', 'other']:
        q = p if t == 'all' else p[p.index.get_level_values('tier') == t]
        a, b = gys
        rows.append(dict(edition=ed, tier=t, from_grad_year=a, to_grad_year=b, n_inst=len(q),
            placed_from=q[('n_placed', a)].sum(), placed_to=q[('n_placed', b)].sum(),
            dlog_placed_x100=round(100 * np.log(q[('n_placed', b)].sum() / q[('n_placed', a)].sum()), 1),
            dlog_graduates_x100=round(100 * np.log(q[('n_grad_min_time', b)].sum() / q[('n_grad_min_time', a)].sum()), 1),
            rate_from=round(q[('n_placed', a)].sum() / q[('n_grad_min_time', a)].sum(), 3),
            rate_to=round(q[('n_placed', b)].sum() / q[('n_grad_min_time', b)].sum(), 3),
            median_dlog_inst_median_salary_x100=round(100 * np.log(q[('median_salary_inr', b)] / q[('median_salary_inr', a)]).replace([np.inf, -np.inf], np.nan).median(), 1),
            source=f'https://www.nirfindia.org/Rankings/{ed}/EngineeringRanking.html (institution PDFs)'))
out = pd.DataFrame(rows); out.to_csv(os.path.join(base, 'nirf_within_edition_yoy.csv'), index=False)
pd.set_option('display.width', 250); print(out.drop(columns='source').to_string(index=False))
