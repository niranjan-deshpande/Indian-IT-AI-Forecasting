"""M5(c): US computer-occupation employment inside client industries vs inside vendors (BLS OEWS, May 2015-May 2025).
Reads raw/oews/x_oesm{yy}in4/.../nat4d_M20yy_dl.xlsx (national, 4-digit NAICS, cross-ownership)
and raw/oews/x_oesm{yy}nat/.../national_M20yy_dl.xlsx (all-industry national totals).
Computer occupations = SOC minor group 15-1100 (SOC 2010, through May 2018) / 15-1200 (SOC 2018, from May 2019).
Run: python3 -I oews_inhouse.py <demand_shift_dir>
"""
import sys, os, glob, csv, math
import pandas as pd
D = sys.argv[1]
R = os.path.join(D, 'raw/oews')
# industry buckets by 4-digit NAICS (first 4 chars of 6-char code)
VENDOR_CSD = {'5415'}                         # computer systems design & related services (the vendor industry)
STAFFING = {'5613'}                           # employment services (IT contractors placed at clients)
MGMT_CONSULT = {'5416'}                       # management/technical consulting (Accenture-type partly)
# tech producers: software publishers (5112 -> 5132 in NAICS 2022), data processing/hosting (5182), other info services
# incl. web search/internet publishing (5191/5192), media streaming & social networks (5162, NAICS 2022), telecom (517), computer & electronic mfg (334)
TECH_PRODUCERS_4 = {'5112', '5132', '5182', '5191', '5192', '5162'}
TECH_PRODUCERS_3 = {'517', '334'}
FINANCE_3 = {'521', '522', '523', '524', '525'}   # OEWS uses aggregated codes (5220A1, 523000) from 2017
def bucket(n4):
    n3 = n4[:3]
    if n4 in VENDOR_CSD: return 'vendor_5415'
    if n4 in STAFFING: return 'staffing_5613'
    if n4 in MGMT_CONSULT: return 'mgmt_consult_5416'
    if n4 in TECH_PRODUCERS_4 or n3 in TECH_PRODUCERS_3: return 'tech_producers'
    if n3 in FINANCE_3: return 'client_finance_insurance'
    if n4.startswith('99'): return 'client_government'
    return 'client_other_private'
def num(x):
    try: return float(str(x).replace(',', ''))
    except ValueError: return float('nan')
rows = []
for yy in range(15, 26):
    f4 = glob.glob(os.path.join(R, f'x_oesm{yy}in4', '*', f'nat4d_M20{yy}_dl.xlsx'))[0]
    fn = glob.glob(os.path.join(R, f'x_oesm{yy}nat', '*', f'national_M20{yy}_dl.xlsx'))[0]
    d = pd.read_excel(f4, dtype=str); d.columns = [c.upper() for c in d.columns]
    occ = d['OCC_CODE']
    comp_code = '15-1100' if yy <= 18 else '15-1200'
    if not (occ == comp_code).any():  # transition years may use the other code
        comp_code = '15-1200' if comp_code == '15-1100' else '15-1100'
    c = d[occ == comp_code].copy(); t = d[occ == '00-0000'].copy()
    c['emp'] = c['TOT_EMP'].map(num); t['emp'] = t['TOT_EMP'].map(num)
    c['n4'] = c['NAICS'].str[:4]; t['n4'] = t['NAICS'].str[:4]
    c['b'] = c['n4'].map(bucket); t['b'] = t['n4'].map(bucket)
    nat = pd.read_excel(fn, dtype=str); nat.columns = [x.upper() for x in nat.columns]
    nat_comp = num(nat.loc[nat['OCC_CODE'] == comp_code, 'TOT_EMP'].iloc[0])
    nat_tot = num(nat.loc[nat['OCC_CODE'] == '00-0000', 'TOT_EMP'].iloc[0])
    r = {'year': 2000 + yy, 'soc_code': comp_code, 'comp_emp_national_all_ind': nat_comp, 'tot_emp_national': nat_tot,
         'comp_emp_sum_4digit': c['emp'].sum(skipna=True), 'n_comp_suppressed_4d': int(c['emp'].isna().sum())}
    for b, v in c.groupby('b')['emp'].sum().items(): r['comp_' + b] = v
    for b, v in t.groupby('b')['emp'].sum().items(): r['tot_' + b] = v
    r['comp_wage_mean_5415'] = num(c.loc[c['n4'] == '5415', 'A_MEAN'].iloc[0])
    r['comp_wage_mean_national'] = num(nat.loc[nat['OCC_CODE'] == comp_code, 'A_MEAN'].iloc[0])
    rows.append(r)
    print(yy, comp_code, 'done', flush=True)
df = pd.DataFrame(rows).set_index('year')
client_cols = ['comp_client_finance_insurance', 'comp_client_government', 'comp_client_other_private']
df['comp_client_all'] = df[client_cols].sum(axis=1)
df['inhouse_share_client_over_client_plus_5415'] = df['comp_client_all'] / (df['comp_client_all'] + df['comp_vendor_5415'])
df['share_5415_of_national_comp'] = df['comp_vendor_5415'] / df['comp_emp_national_all_ind']
for k in ['comp_emp_national_all_ind', 'comp_vendor_5415', 'comp_client_all', 'comp_client_finance_insurance',
          'comp_client_other_private', 'comp_client_government', 'comp_tech_producers', 'comp_staffing_5613', 'tot_emp_national']:
    df['g_' + k] = 100 * (df[k].map(math.log).diff())
df.reset_index().to_csv(os.path.join(D, 'oews_computer_occ_by_bucket.csv'), index=False, float_format='%.4f')
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
print(df[['soc_code', 'comp_emp_national_all_ind', 'comp_emp_sum_4digit', 'comp_vendor_5415', 'comp_client_all', 'comp_client_finance_insurance',
          'comp_client_government', 'comp_tech_producers', 'comp_staffing_5613', 'inhouse_share_client_over_client_plus_5415', 'n_comp_suppressed_4d']].round(3))
print(df[[c for c in df.columns if c.startswith('g_')]].round(2))
