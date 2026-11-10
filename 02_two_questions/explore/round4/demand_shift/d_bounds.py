"""M5: combine proxies into a pre/post comparison and a bound on d (market-wide and vendor-facing), then map onto the (d, eps) line.
Inputs (this folder): bea_software_annual.csv, oews_computer_occ_by_bucket.csv, bank_tech_xbrl_long.csv,
raw/bea/NipaDataA.txt, ../../round3/plfs/occupation_split.csv
Outputs: proxy_series_annual.csv, proxy_prepost_summary.csv, d_bounds.csv, d_eps_mapping.csv
Run: python3 -I d_bounds.py <demand_shift_dir>
Growth rates are 100*log differences (approx % per year).
"""
import sys, os, csv, math
import pandas as pd
D = sys.argv[1]
bea = pd.read_csv(os.path.join(D, 'bea_software_annual.csv')).set_index('year')
oe = pd.read_csv(os.path.join(D, 'oews_computer_occ_by_bucket.csv')).set_index('year')
bk = pd.read_csv(os.path.join(D, 'bank_tech_xbrl_long.csv'))
# extra NIPA: real GDP, corporate profits
A = {}
with open(os.path.join(D, 'raw/bea/NipaDataA.txt')) as f:
    r = csv.reader(f); next(r)
    for c, p, v in r:
        if c in ('A191RX', 'A051RC'):
            A[(c, int(p))] = float(v.replace(',', ''))
yrs = list(range(2015, 2026))
s = pd.DataFrame(index=pd.Index(yrs, name='year'))
s['bea_custom_nom'] = bea['custom_nom']; s['bea_ownacct_nom'] = bea['ownacct_nom']; s['bea_prepack_nom'] = bea['prepack_nom']
s['bea_custom_real'] = bea['custom_real']; s['bea_ownacct_real'] = bea['ownacct_real']
s['bea_ownacct_share_of_custom_plus_own'] = bea['ownacct_share_nom']
s['gdp_deflator'] = bea['gdp_deflator']
s['real_gdp'] = [A[('A191RX', y)] for y in yrs]; s['corp_profits_nom'] = [A[('A051RC', y)] for y in yrs]
s['oews_comp_5415'] = oe['comp_vendor_5415']; s['oews_comp_client_inhouse'] = oe['comp_client_all']
s['oews_comp_client_finance'] = oe['comp_client_finance_insurance']; s['oews_comp_staffing_5613'] = oe['comp_staffing_5613']
s['oews_comp_all_industries'] = oe['comp_emp_national_all_ind']
s['oews_inhouse_share'] = oe['inhouse_share_client_over_client_plus_5415']
fy = bk[(bk.period == 'FY') & (bk.concept == 'CommunicationsAndInformationTechnology')].pivot(index='year', columns='bank', values='value_usd_mn')
s['bank3_comm_it_expense'] = fy[['JPM', 'BAC', 'C']].sum(axis=1, min_count=3).reindex(yrs)
s['bank2_comm_it_expense_bac_c'] = fy[['BAC', 'C']].sum(axis=1, min_count=2).reindex(yrs)
pl = pd.read_csv(os.path.join(D, '../../round3/plfs/occupation_split.csv'))
pl = pl[pl.population == 'all_ages'].set_index('round')
s['plfs_ict_share_outside_it_india'] = None
for rnd, y in [('2022-23', 2022), ('2023-24', 2023), ('cy2024', 2024), ('cy2025', 2025)]:
    s.loc[y, 'plfs_ict_share_outside_it_india'] = pl.loc[rnd, 'share_outside']
s.reset_index().to_csv(os.path.join(D, 'proxy_series_annual.csv'), index=False, float_format='%.4f')

def g(col):
    x = s[col].astype(float)
    return 100 * (x.map(math.log).diff())
def avg(col, y0, y1):
    return g(col).loc[y0:y1].mean()
def fmt(v): return None if v is None or (isinstance(v, float) and math.isnan(v)) else round(float(v), 2)
rows = []
spec = [
 ('real_gdp', 'Client driver: US real GDP', 'non-circular driver (market d, real)'),
 ('corp_profits_nom', 'Client driver: US corporate profits (nominal)', 'non-circular driver (market d, nominal)'),
 ('gdp_deflator', 'US GDP deflator (for nominal->real)', 'deflator'),
 ('bea_ownacct_nom', 'BEA own-account software (nominal)', 'non-circular: in-house work, labour-cost based'),
 ('bea_ownacct_real', 'BEA own-account software (real, 2017$)', 'non-circular: in-house work volume (input-cost deflator)'),
 ('bea_custom_nom', 'BEA purchased custom software (nominal)', 'CIRCULAR: = vendor output p*Q (all vendors incl. imports)'),
 ('bea_custom_real', 'BEA purchased custom software (real)', 'CIRCULAR-ish: vendor revenue / input-cost index (same index as own-account)'),
 ('bea_prepack_nom', 'BEA prepackaged software/SaaS (nominal)', 'substitute product; not d for services'),
 ('oews_comp_client_inhouse', 'OEWS computer occs in client industries (US)', 'non-circular: in-house tech labour'),
 ('oews_comp_client_finance', 'OEWS computer occs in finance & insurance (US)', 'non-circular: in-house tech labour'),
 ('oews_comp_5415', 'OEWS computer occs in NAICS 5415 (US)', 'vendor-side labour (outcome, not proxy)'),
 ('oews_comp_staffing_5613', 'OEWS computer occs in employment services (US)', 'contract IT labour (vendor-like)'),
 ('oews_comp_all_industries', 'OEWS computer occs, all industries (US)', 'market labour (includes AI s)'),
 ('bank3_comm_it_expense', 'JPM+BAC+C comms & IT expense line (10-K)', 'client tech budget; partly circular (vendor share w)'),
 ('bank2_comm_it_expense_bac_c', 'BAC+C comms & IT expense line (10-K)', 'client tech budget; partly circular'),
]
for col, lab, role in spec:
    gg = g(col)
    rows.append({'series': col, 'label': lab, 'role': role,
                 'avg_g_2016_19': fmt(avg(col, 2016, 2019)), 'avg_g_2016_22': fmt(avg(col, 2016, 2022)),
                 'avg_g_2023_25': fmt(avg(col, 2023, 2025)), 'g_2024': fmt(gg.loc[2024]), 'g_2025': fmt(gg.loc[2025]),
                 'change_vs_2016_22': fmt(avg(col, 2023, 2025) - avg(col, 2016, 2022)),
                 'change_vs_2016_19': fmt(avg(col, 2023, 2025) - avg(col, 2016, 2019))})
# relative growth: vendor vs in-house
rel = [('oews_comp_5415', 'oews_comp_client_inhouse', 'OEWS: 5415 minus client in-house computer-occ growth'),
       ('bea_custom_nom', 'bea_ownacct_nom', 'BEA: custom minus own-account nominal growth')]
for a, b, lab in rel:
    d = g(a) - g(b)
    rows.append({'series': f'{a}-{b}', 'label': lab, 'role': 'vendor vs in-house relative shift',
                 'avg_g_2016_19': fmt(d.loc[2016:2019].mean()), 'avg_g_2016_22': fmt(d.loc[2016:2022].mean()),
                 'avg_g_2023_25': fmt(d.loc[2023:2025].mean()), 'g_2024': fmt(d.loc[2024]), 'g_2025': fmt(d.loc[2025]),
                 'change_vs_2016_22': fmt(d.loc[2023:2025].mean() - d.loc[2016:2022].mean()),
                 'change_vs_2016_19': fmt(d.loc[2023:2025].mean() - d.loc[2016:2019].mean())})
summ = pd.DataFrame(rows)
summ.to_csv(os.path.join(D, 'proxy_prepost_summary.csv'), index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 60)
print(summ[['series', 'avg_g_2016_19', 'avg_g_2016_22', 'avg_g_2023_25', 'g_2024', 'g_2025', 'change_vs_2016_22', 'change_vs_2016_19']].to_string())

# ---------------- bounds on the change in d (2023-25 vs pre-2023), pp per year ----------------
S = summ.set_index('series')
oews_rel = S.loc['oews_comp_5415-oews_comp_client_inhouse', 'change_vs_2016_22']     # change in vendor-minus-inhouse labour growth
bea_rel = S.loc['bea_custom_nom-bea_ownacct_nom', 'change_vs_2016_22']              # change in vendor-minus-inhouse nominal growth
sigma_oews = 1 - s.loc[2022, 'oews_inhouse_share']          # vendor share of US computer labour (client+5415), 2022
sigma_bea = 1 - s.loc[2022, 'bea_ownacct_share_of_custom_plus_own']  # custom share of custom+own, 2022
gp_ai = 2.5   # illustrative AI price cut phi*s (pp/yr), from the illustrative line
# d_share = (1 - sigma) * (relative volume shift vendor vs in-house)
# OEWS: relative volume shift = relative labour shift + (s_vendor - s_inhouse); s_vendor - s_inhouse in [0, 2.5]
oews_lo = (1 - sigma_oews) * (oews_rel + 0.0); oews_hi = (1 - sigma_oews) * (oews_rel + 2.5)
# BEA nominal: relative volume shift = relative nominal shift - (vendor price change - in-house unit cost change); that gap in [-2.5, 0]
bea_lo = (1 - sigma_bea) * (bea_rel + 0.0); bea_hi = (1 - sigma_bea) * (bea_rel + gp_ai)
bounds = [
 {'component': 'delta_d_market (US, real)', 'low': -1.5, 'central': -0.5, 'high': 0.5,
  'basis': 'Drivers: real GDP growth +%.2f pp vs 2016-22 (+%.2f vs 2016-19); own-account real %.2f pp; bank tech lines %.2f pp nominal; custom+own nominal %.2f pp is partly circular (custom = vendor revenue): adding back up to 0.73*2.5 = 1.8 pp of AI price pass-through and subtracting inflation change gives -2.5 to -0.4. Range set by judgement across these.' % (
      S.loc['real_gdp', 'change_vs_2016_22'], S.loc['real_gdp', 'change_vs_2016_19'], S.loc['bea_ownacct_real', 'change_vs_2016_22'], S.loc['bank3_comm_it_expense', 'change_vs_2016_22'],
      (avg('bea_custom_nom', 2023, 2025) * 0 + (g('bea_custom_nom') * sigma_bea + g('bea_ownacct_nom') * (1 - sigma_bea)).loc[2023:2025].mean() - (g('bea_custom_nom') * sigma_bea + g('bea_ownacct_nom') * (1 - sigma_bea)).loc[2016:2022].mean()))},
 {'component': 'delta_d_share via OEWS labour (US)', 'low': round(oews_lo, 2), 'central': round((oews_lo + oews_hi) / 2, 2), 'high': round(oews_hi, 2),
  'basis': '(1-sigma)=%.3f x [relative labour shift %.2f pp + (s_vendor - s_inhouse) in 0..2.5]. Lower bound if vendors adopt AI no faster than in-house teams; offshoring of 5415 US jobs would make it too negative.' % (1 - sigma_oews, oews_rel)},
 {'component': 'delta_d_share via BEA nominal (US)', 'low': round(bea_lo, 2), 'central': round((bea_lo + bea_hi) / 2, 2), 'high': round(bea_hi, 2),
  'basis': '(1-sigma)=%.3f x [relative nominal shift %.2f pp + vendor relative price cut 0..2.5]. Weights are nominal shares; BEA counts only part of programmer time as own-account, so sigma is high and this is a small number.' % (1 - sigma_bea, bea_rel)},
 {'component': 'delta_d_share via GCC (India, vendor scope only)', 'low': -2.5, 'central': -1.0, 'high': 0.0,
  'basis': 'Round-3 synthesis: GCC tech jobs +~260k FY23-26 (range 155-430k), ~87k/yr on a vendor base of roughly 3.5-4m, i.e. 2-3%/yr of vendor volume, but GCCs were also growing before 2023 (pre-2023 GCC growth not confirmed here), so only part is a change vs baseline. Zero at sector scope if GCCs are inside the sector.'},
]
oews_c = (oews_lo + oews_hi) / 2; bea_c = (bea_lo + bea_hi) / 2
share_lo, share_c, share_hi = min(oews_lo, bea_lo), (oews_c + bea_c) / 2, max(oews_hi, bea_hi)
bounds.append({'component': 'delta_d_share US combined', 'low': round(share_lo, 2), 'central': round(share_c, 2), 'high': round(share_hi, 2), 'basis': 'envelope of OEWS and BEA; central = mean of the two centrals'})
mk = bounds[0]
for scope, gcc in [('vendor (excl. GCC), US-weighted', bounds[3]), ('sector incl. GCC, US-weighted', {'low': 0, 'central': 0, 'high': 0})]:
    bounds.append({'component': f'delta_d total: {scope}', 'low': round(mk['low'] + share_lo + gcc['low'], 2),
                   'central': round(mk['central'] + share_c + gcc['central'], 2), 'high': round(mk['high'] + share_hi + gcc['high'], 2),
                   'basis': 'market + US share shift + GCC channel (ranges added: deliberately conservative)'})
pd.DataFrame(bounds).to_csv(os.path.join(D, 'd_bounds.csv'), index=False)
for b in bounds: print(b['component'], b['low'], b['central'], b['high'])

# ---------------- mapping onto the illustrative line d + 2.5*eps = 2.5 (+ rho + eps*pi) ----------------
# d_post = d_base + delta_d ; d_base = pre-2023 volume growth at constant price = g_L,base + rho (+eps*pi), with pi=rho=0 in the illustrative line.
out = []
tot = {b['component']: b for b in bounds}
for scope in ['vendor (excl. GCC), US-weighted', 'sector incl. GCC, US-weighted']:
    b = tot[f'delta_d total: {scope}']
    for d_base in [3.0, 5.0, 7.0]:
        for lab in ['low', 'central', 'high']:
            d_post = d_base + b[lab]
            eps = (2.5 - d_post) / 2.5
            out.append({'scope': scope, 'baseline_gL_pre2023_eq_d_base_if_rho_pi_0': d_base, 'delta_gL': -d_base, 'delta_d_case': lab, 'delta_d': b[lab], 'd_post': round(d_post, 2),
                        'eps_on_line_d+2.5eps=2.5 (equiv. delta_d+2.5eps=2.5+delta_gL)': round(eps, 2), 'eps_in_[0,1.5]': 0 <= eps <= 1.5})
m = pd.DataFrame(out); m.to_csv(os.path.join(D, 'd_eps_mapping.csv'), index=False)
print(m.to_string())
