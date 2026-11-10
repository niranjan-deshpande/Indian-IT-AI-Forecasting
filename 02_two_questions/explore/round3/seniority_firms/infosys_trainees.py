"""Implied Infosys trainee pool from utilization incl. vs excl. trainees.
trainee_effort_share = 1 - U_incl/U_excl (share of IT-services effort spent by trainees).
Calibrated against reported trainee counts FY11-FY18 (Infosys stopped reporting Trainees after Q4FY18).
Inputs: data/raw/infosys.csv (fact sheets). Output: infosys_trainees_implied.csv"""
import pandas as pd, numpy as np, pathlib
root = pathlib.Path(__file__).resolve().parents[4]
d = pd.read_csv(root/'data/raw/infosys.csv')
d = d.sort_values('doc_date')
u = d[d.metric.isin(['utilization_incl_trainees','utilization_excl_trainees']) & (d.dimension=='total')]
u = u.drop_duplicates(['fiscal_q','metric'], keep='last').pivot(index='fiscal_q', columns='metric', values='value')
h = d[(d.metric=='headcount_breakdown') & d.dimension.isin(['Trainees','S/W professionals'])]
h = h.drop_duplicates(['fiscal_q','dimension'], keep='last').pivot(index='fiscal_q', columns='dimension', values='value')
src = d[d.metric=='utilization_incl_trainees'].drop_duplicates('fiscal_q', keep='last').set_index('fiscal_q')[['period_end','source_url','source_loc']]
t = u.join(h).join(src)
t['trainee_effort_share_pct'] = 100*(1 - t.utilization_incl_trainees/t.utilization_excl_trainees)
t['naive_trainees'] = t.trainee_effort_share_pct/100 * t['S/W professionals']
cal = t.dropna(subset=['Trainees','naive_trainees'])
k = (cal.Trainees*cal.naive_trainees).sum()/(cal.naive_trainees**2).sum()   # OLS through origin
corr = np.corrcoef(cal.Trainees, cal.naive_trainees)[0,1]
t['implied_trainees_calibrated'] = (k*t.naive_trainees).round(0)
t['reported_trainees_share_pct'] = 100*t.Trainees/t['S/W professionals']
t = t.sort_values('period_end')
t['fy'] = t.index.str[-4:]
out = t.reset_index()[['fiscal_q','fy','period_end','utilization_incl_trainees','utilization_excl_trainees','trainee_effort_share_pct','S/W professionals','Trainees','reported_trainees_share_pct','implied_trainees_calibrated','source_url','source_loc']]
out.to_csv(pathlib.Path(__file__).parent/'infosys_trainees_implied.csv', index=False, float_format='%.2f')
print(f'calibration k={k:.3f}, corr(reported, naive)={corr:.2f}, n={len(cal)}')
ann = out.groupby('fy').agg(effort_share=('trainee_effort_share_pct','mean'), implied=('implied_trainees_calibrated','mean'), reported=('Trainees','mean'), nq=('fiscal_q','count'))
print(ann.round(1).to_string())
