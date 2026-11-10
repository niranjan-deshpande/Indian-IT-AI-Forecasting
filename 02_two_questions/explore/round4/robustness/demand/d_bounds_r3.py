"""R3 robustness of M5 (demand shift d): (1) GCC term net of pre-2023 GCC growth, (2) Europe folded in by export
destination, (3) OEWS NAICS 5415 vs BLS CES, (4) recomputed Delta-d bounds vs the diagnosed Delta-d ~ -7.
Inputs:
  ../../demand_shift/oews_computer_occ_by_bucket.csv, ../../demand_shift/proxy_prepost_summary.csv,
  ../../demand_shift/d_bounds.csv, ../../demand_shift/rbi_destination_split.csv
  ../../../round3/offshore_competitors/bls_ces_monthly.csv (CES6054150001, SA, thousands)
  ../../../round3/gcc/rbi_fla_foreign_subs_ic.csv
  europe_prepost.csv, europe_series_annual.csv (from europe_proxies.py), gcc_baseline_inputs.csv
Outputs: oews_ces_check.csv, gcc_baseline_scenarios.csv, gcc_rbi_relative_growth.csv, destination_weights.csv, d_bounds_r3.csv
Run: python3 -I d_bounds_r3.py <this_dir>
All rates are % per year (100*log diff). Change = 2023-25 (FY24-26) mean minus pre-2023 mean.
"""
import sys, os, math
import pandas as pd, numpy as np
D = sys.argv[1]
M5 = os.path.join(D, '../../demand_shift'); R3 = os.path.join(D, '../../../round3')
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 80)
AI = 2.5   # M5's allowance for (s_vendor - s_inhouse) or relative vendor price cut, pp/yr, in [0, AI]

# ======================= (3) OEWS vs CES, NAICS 5415 =======================
oe = pd.read_csv(os.path.join(M5, 'oews_computer_occ_by_bucket.csv')).set_index('year')
ces = pd.read_csv(os.path.join(R3, 'offshore_competitors/bls_ces_monthly.csv'))
c = pd.DataFrame({'oews_total_5415_k': oe['tot_vendor_5415'] / 1000, 'oews_comp_occ_5415_k': oe['comp_vendor_5415'] / 1000,
                  'oews_comp_client_inhouse_k': oe['comp_client_all'] / 1000})
c = c.join(ces[ces.month == 5].set_index('year')['CES6054150001'].rename('ces_may_5415_k'), how='outer')
c = c.join(ces.groupby('year')['CES6054150001'].mean().rename('ces_annavg_5415_k'), how='outer')
c['oews_over_ces_may'] = c['oews_total_5415_k'] / c['ces_may_5415_k']
c['oews_comp_share_of_5415'] = c['oews_comp_occ_5415_k'] / c['oews_total_5415_k']
for k in ['oews_total_5415_k', 'oews_comp_occ_5415_k', 'oews_comp_client_inhouse_k', 'ces_may_5415_k', 'ces_annavg_5415_k']:
    c['g_' + k] = 100 * np.log(c[k]).diff()
c.index.name = 'year'
c.reset_index().to_csv(os.path.join(D, 'oews_ces_check.csv'), index=False, float_format='%.4f')
print(c.round(3).to_string())
pre, post = slice(2016, 2022), slice(2023, 2025)
def chg(col): return c.loc[post, col].mean() - c.loc[pre, col].mean()
inh = chg('g_oews_comp_client_inhouse_k')
rel = {'OEWS computer occs in 5415 (M5)': chg('g_oews_comp_occ_5415_k') - inh,
       'OEWS total 5415 employment': chg('g_oews_total_5415_k') - inh,
       'CES 5415 employment (May)': chg('g_ces_may_5415_k') - inh,
       'CES 5415 employment (annual avg)': chg('g_ces_annavg_5415_k') - inh}
inhouse_share_2022 = oe.loc[2022, 'inhouse_share_client_over_client_plus_5415']
us_oews_variants = []
for k, v in rel.items():
    lo, hi = inhouse_share_2022 * v, inhouse_share_2022 * (v + AI)
    us_oews_variants.append({'vendor_series': k, 'vendor_growth_change': round(v + inh, 2), 'inhouse_growth_change': round(inh, 2),
                             'relative_shift': round(v, 2), 'share_low': round(lo, 2), 'share_central': round((lo + hi) / 2, 2), 'share_high': round(hi, 2)})
us_oews = pd.DataFrame(us_oews_variants); print(us_oews.to_string())

# ======================= (1) GCC term net of pre-2023 GCC growth =======================
TECH = 0.67           # tech share of GCC staff (round-3 central; same in both periods, so it scales both)
BASE_PRE, BASE_POST = 3.3, 3.6   # vendor (non-GCC) tech base, millions; post from M5 (~3.6m); pre is an assumption (~8% smaller)
pre_sc = {   # all-function GCC additions, thousand per year, pre-2023
    'P1 old basis FY19-23 (1.0m -> 1.66m)': (1660 - 1000) / 4,
    'P2 old basis FY21-23 (1.38m -> 1.66m)': (1660 - 1380) / 2,
    'P3 restated FY19-24, +36% (1.40m -> 1.90m; NOT CONFIRMED)': (1900 - 1900 / 1.36) / 5,
    'P4 restated FY19-24, count x avg (~1.18m -> 1.90m)': (1900 - 1300 * (1130 / 1.24) / 1000) / 5,
}
post_sc = {  # all-function GCC additions, thousand per year, FY24-26
    'S3 staffing-firm net hiring FY24-26 (385k)': 385 / 3,
    'S4 2024-edition path (282k)': 282 / 3,
    'S2 restated chain FY23-26 (540k)': 540 / 3,
    'E26 2026 edition FY24-26 (1.90m -> 2.36m)': (2360 - 1900) / 2,
}
rows = []
for kp, vp in pre_sc.items():
    for kq, vq in post_sc.items():
        a_pre = 100 * vp * TECH / (BASE_PRE * 1000); a_post = 100 * vq * TECH / (BASE_POST * 1000)
        rows.append({'pre_scenario': kp, 'pre_adds_k_per_yr': round(vp, 1), 'pre_absorption_pct_of_base': round(a_pre, 2),
                     'post_scenario': kq, 'post_adds_k_per_yr': round(vq, 1), 'post_absorption_pct_of_base': round(a_post, 2),
                     'delta_d_gcc': round(-(a_post - a_pre), 2)})
gs = pd.DataFrame(rows); gs.to_csv(os.path.join(D, 'gcc_baseline_scenarios.csv'), index=False)
print(gs[['pre_scenario', 'pre_absorption_pct_of_base', 'post_scenario', 'post_absorption_pct_of_base', 'delta_d_gcc']].to_string())
cen = gs[(gs.pre_scenario.str.startswith('P2')) | (gs.pre_scenario.str.startswith('P4'))]
cen = cen[cen.post_scenario.str.startswith('S3')]['delta_d_gcc'].mean()
plaus = gs[~gs.post_scenario.str.startswith('E26')]  # E26 likely includes coverage widening
gcc = {'low': gs.delta_d_gcc.min(), 'low_excl_E26': plaus.delta_d_gcc.min(), 'central': cen, 'high': gs.delta_d_gcc.max()}
print('GCC term', {k: round(v, 2) for k, v in gcc.items()})
# RBI FLA: foreign subsidiaries' I&C exports growth minus total software exports growth (USD, approx)
fla = pd.read_csv(os.path.join(R3, 'gcc/rbi_fla_foreign_subs_ic.csv'))
fla['fy'] = fla['cur_fy'].str[:4].astype(int) + 1
tot = {2022: 17.2, 2023: 18.4, 2024: 2.8, 2025: 7.3}   # RBI software survey, USD growth (gcc_baseline_inputs.csv)
fr = fla[['fy', 'within_round_growth_usd_pct_approx', 'within_round_growth_inr_pct']].copy()
fr['total_sw_exports_growth_usd'] = fr['fy'].map(tot)
fr['foreign_subs_minus_total'] = fr['within_round_growth_usd_pct_approx'] - fr['total_sw_exports_growth_usd']
fr.to_csv(os.path.join(D, 'gcc_rbi_relative_growth.csv'), index=False)
print(fr.to_string())
fla_pre = fr[fr.fy.isin([2020, 2021, 2022, 2023])]['within_round_growth_usd_pct_approx'].mean()
fla_post = fr[fr.fy.isin([2024, 2025])]['within_round_growth_usd_pct_approx'].mean()
rel_pre = fr[fr.fy.isin([2022, 2023])]['foreign_subs_minus_total'].mean(); rel_post = fr[fr.fy.isin([2024, 2025])]['foreign_subs_minus_total'].mean()
print(f'FLA foreign-subs I&C export growth: FY20-23 {fla_pre:.1f}, FY24-25 {fla_post:.1f}; relative to total: FY22-23 {rel_pre:.1f}, FY24-25 {rel_post:.1f}')

# ======================= (2) Europe =======================
ds = pd.read_csv(os.path.join(M5, 'rbi_destination_split.csv'))
ds = ds[ds.fiscal_year.isin(['2023-24', '2024-25', '2025-26'])].groupby('destination')['share_pct'].mean()
w_us = ds['United States of America'] + ds['Canada']; w_eu = ds['Europe']; w_uk = ds['of which United Kingdom']; w_eux = w_eu - w_uk
W = w_us + w_eu
wt = {'north_america': w_us / W, 'europe': w_eu / W, 'uk_within_europe': w_uk / w_eu, 'rest_of_europe_within_europe': w_eux / w_eu}
pd.DataFrame([{'item': k, 'weight': round(v, 4)} for k, v in wt.items()] +
             [{'item': 'raw_share_pct_' + k, 'weight': round(v, 2)} for k, v in [('NA', w_us), ('Europe', w_eu), ('UK', w_uk), ('unmeasured_other', 100 - W)]]
             ).to_csv(os.path.join(D, 'destination_weights.csv'), index=False)
print('weights', {k: round(v, 3) for k, v in wt.items()}, 'unmeasured', round(100 - W, 1))
ep = pd.read_csv(os.path.join(D, 'europe_prepost.csv')).set_index('series')
es = pd.read_csv(os.path.join(D, 'europe_series_annual.csv')).set_index('year')
# market term, Europe (real): GDP (EU, UK), real IPP GFCF (EU excl IE, DE+FR), total ICT-specialist employment (includes AI s => lower bound)
eu_mkt_obs = {'EU27 real GDP': ep.loc['eu27_real_gdp', 'change_vs_pre'], 'UK real GDP': ep.loc['uk_real_gdp', 'change_vs_pre'],
              'EU27 excl IE real IPP GFCF': ep.loc['eu27xie_ipp_gfcf_real_approx', 'change_vs_pre'], 'DE+FR real IPP GFCF': ep.loc['de_fr_ipp_gfcf_real', 'change_vs_pre'],
              'EU27 ICT specialists all industries': ep.loc['eu27_ict_all_industries', 'change_vs_pre'],
              'UK own-account software real (nominal - GDP deflator)': ep.loc['uk_software_ownacct_cp', 'change_vs_pre'] - ep.loc['uk_gdp_deflator', 'change_vs_pre']}
print('Europe market observables', {k: round(v, 2) for k, v in eu_mkt_obs.items()})
core = [eu_mkt_obs[k] for k in ['EU27 real GDP', 'UK real GDP', 'EU27 excl IE real IPP GFCF', 'DE+FR real IPP GFCF', 'EU27 ICT specialists all industries']]
eu_mkt = {'central': float(np.mean(core)), 'low': -1.5, 'high': 0.5}   # same +/-1 judgement band as M5's US market term
# share term, continental EU (LFS ICT specialists; in-house share x relative shift + AI allowance)
lfs = []
for rs, share_col in [('eu27_ict_vendor_J62_J63-eu27_ict_client_narrow', 'eu27_ict_inhouse_share_narrow'),
                      ('eu27_ict_vendor_J62_J63-eu27_ict_client_broad', 'eu27_ict_inhouse_share_broad'),
                      ('eu27xde_ict_vendor_J62_J63-eu27xde_ict_client_narrow', 'eu27_ict_inhouse_share_narrow')]:
    sh = es.loc[2022, share_col]; v = ep.loc[rs, 'change_vs_pre']
    lfs.append((sh * v, sh * (v + AI)))
eu_lfs = {'low': min(l for l, h in lfs), 'high': max(h for l, h in lfs), 'central': float(np.mean([(l + h) / 2 for l, h in lfs]))}
# UK: ONS software GFCF purchased vs own-account (analogue of M5's BEA term)
uk_sh = es.loc[2022, 'uk_software_ownacct_share']; v = ep.loc['uk_software_purchased_cp-uk_software_ownacct_cp', 'change_vs_pre']
uk_gfcf = {'low': uk_sh * v, 'high': uk_sh * (v + AI)}; uk_gfcf['central'] = (uk_gfcf['low'] + uk_gfcf['high']) / 2
# UK combined, M5 convention (envelope; central = mean of method centrals): UK GFCF and EU-LFS read-across
uk = {'low': min(uk_gfcf['low'], eu_lfs['low']), 'high': max(uk_gfcf['high'], eu_lfs['high']), 'central': (uk_gfcf['central'] + eu_lfs['central']) / 2}
eu_share = {k: wt['uk_within_europe'] * uk[k] + wt['rest_of_europe_within_europe'] * eu_lfs[k] for k in ['low', 'central', 'high']}
print('EU LFS share', {k: round(v, 2) for k, v in eu_lfs.items()}, 'UK GFCF share', {k: round(v, 2) for k, v in uk_gfcf.items()}, 'Europe share', {k: round(v, 2) for k, v in eu_share.items()})

# ======================= (4) recomputed bounds =======================
m5 = pd.read_csv(os.path.join(M5, 'd_bounds.csv')).set_index('component')
us_mkt = m5.loc['delta_d_market (US, real)', ['low', 'central', 'high']].astype(float).to_dict()
bea = m5.loc['delta_d_share via BEA nominal (US)', ['low', 'central', 'high']].astype(float).to_dict()
oews_m5 = us_oews.iloc[0]; oews_ces = us_oews[us_oews.vendor_series == 'CES 5415 employment (May)'].iloc[0]
def comb(a, b): return {'low': min(a['low'], b['low']), 'high': max(a['high'], b['high']), 'central': (a['central'] + b['central']) / 2}
oews_env = {'low': min(oews_m5.share_low, oews_ces.share_low), 'high': max(oews_m5.share_high, oews_ces.share_high),
            'central': (oews_m5.share_central + oews_ces.share_central) / 2}
us_share = comb(oews_env, bea)
mk = {k: wt['north_america'] * us_mkt[k] + wt['europe'] * eu_mkt[k] for k in ['low', 'central', 'high']}
sh = {k: wt['north_america'] * us_share[k] + wt['europe'] * eu_share[k] for k in ['low', 'central', 'high']}
gc = {'low': gcc['low'], 'central': gcc['central'], 'high': gcc['high']}
out = []
def add(comp, d, basis): out.append({'component': comp, 'low': round(d['low'], 2), 'central': round(d['central'], 2), 'high': round(d['high'], 2), 'basis': basis})
add('M5 original: vendor total excl. GCC scope', m5.loc['delta_d total: vendor (excl. GCC), US-weighted', ['low', 'central', 'high']].astype(float).to_dict(), 'M5 d_bounds.csv (US proxies applied to all demand)')
add('market, US (M5, unchanged)', us_mkt, 'M5')
add('market, Europe', eu_mkt, 'central = mean of EU/UK real GDP, real IPP GFCF (EU ex IE, DE+FR), EU ICT-specialist employment changes; band = M5 judgement +/-1')
add('market, destination-weighted', mk, f"weights NA {wt['north_america']:.3f}, Europe {wt['europe']:.3f} (FY24-26 RBI shares renormalised; other ~{100 - W:.0f}% assumed like the weighted average)")
add('share, US OEWS (M5: computer occs in 5415)', {'low': oews_m5.share_low, 'central': oews_m5.share_central, 'high': oews_m5.share_high}, 'M5')
add('share, US OEWS with CES 5415 as vendor series', {'low': oews_ces.share_low, 'central': oews_ces.share_central, 'high': oews_ces.share_high}, 'CES May 5415 employment growth replaces OEWS computer-occ growth')
add('share, US BEA (M5, unchanged)', bea, 'M5')
add('share, US combined (r3)', us_share, 'envelope of OEWS/CES and BEA; central = mean of method centrals')
add('share, continental EU (LFS ICT specialists)', eu_lfs, 'in-house share 2022 x (relative J62-63 vs client shift + [0,2.5]); narrow, broad, ex-DE variants')
add('share, UK (ONS software GFCF purchased vs own-account)', uk_gfcf, 'own-account share 2022 x (relative nominal shift + [0,2.5]); purchased includes packaged software')
add('share, UK combined', uk, 'envelope of UK GFCF and EU-LFS read-across; central = mean')
add('share, Europe', eu_share, 'UK and rest-of-Europe weighted by RBI destination shares')
add('share, destination-weighted', sh, 'NA and Europe weighted')
add('GCC, net of pre-2023 GCC growth', gc, 'post minus pre GCC tech absorption as % of vendor base; see gcc_baseline_scenarios.csv')
tot = {k: mk[k] + sh[k] + gc[k] for k in ['low', 'central', 'high']}
add('R3 vendor total (top-six-type scope, excl. GCCs)', tot, 'market + share + GCC; ranges added (conservative)')
add('R3 sector total (incl. GCCs)', {k: mk[k] + sh[k] for k in ['low', 'central', 'high']}, 'market + share')
for lab, alt in [('sens: GCC central = 0', {**tot, 'central': mk['central'] + sh['central']}),
                 ('sens: UK share = EU LFS only', {k: mk[k] + wt['north_america'] * us_share[k] + wt['europe'] * eu_lfs[k] + gc[k] for k in ['low', 'central', 'high']}),
                 ('sens: UK share = ONS GFCF only', {k: mk[k] + wt['north_america'] * us_share[k] + wt['europe'] * (wt['uk_within_europe'] * uk_gfcf[k] + wt['rest_of_europe_within_europe'] * eu_lfs[k]) + gc[k] for k in ['low', 'central', 'high']}),
                 ('sens: US-only proxies applied to all demand (M5 convention) + r3 GCC + CES', {k: us_mkt[k] + us_share[k] + gc[k] for k in ['low', 'central', 'high']})]:
    add(lab, alt, 'sensitivity')
DIAG = -7.0
res = pd.DataFrame(out)
res['residual_pp_vs_diag_-7 (= -7 - central)'] = (DIAG - res['central']).round(2)
res.to_csv(os.path.join(D, 'd_bounds_r3.csv'), index=False)
print(res[['component', 'low', 'central', 'high', 'residual_pp_vs_diag_-7 (= -7 - central)']].to_string())
