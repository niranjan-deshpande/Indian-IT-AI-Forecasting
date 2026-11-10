"""R3 (M5 robustness), task 2: European client-side tech-demand proxies, pre (2016-22) vs post (2023-25).
Inputs (raw/, downloaded 2026-10-15, official sources):
  eurostat_isoc_sks_itspn2_long.csv  Eurostat isoc_sks_itspn2, employed ICT specialists by NACE Rev.2 (LFS), thousands
  eurostat_nama_10_an6_long.csv      Eurostat nama_10_an6, GFCF by asset (N117G intellectual property products)
  eurostat_nama_10_gdp_long.csv      Eurostat nama_10_gdp, EU27 GDP
  ons_cxnv.csv                       ONS business investment dataset CXNV (software GFCF: total EF3C, purchased EF8L, own-account EF9P; CP NSA, GBP m)
  ons_abmi_qna.json, ons_ybgb_qna.json  ONS UK real GDP (ABMI, CVM) and GDP deflator (YBGB)
Outputs: europe_series_annual.csv, europe_prepost.csv
Run: python3 -I europe_proxies.py <this_dir>
Growth = 100*diff(log) (% per year). Pre = average over 2016-22 growth years excluding LFS break years
(2020: German Mikrozensus redesign moved ~180k ICT specialists from J58-J60 to J62_J63; 2021: EU-wide IESS LFS break);
alt pre = 2016-19. Post = 2023-25.
"""
import sys, os, json, csv, math
import pandas as pd
D = sys.argv[1]; R = os.path.join(D, 'raw')
YRS = list(range(2014, 2026))
s = pd.DataFrame(index=pd.Index(YRS, name='year'))

# ---- Eurostat ICT specialists by NACE ----
e = pd.read_csv(os.path.join(R, 'eurostat_isoc_sks_itspn2_long.csv'))
e = e[e.unit == 'THS_PER']
SECTIONS = list('ABCDEFGHIJKLMNOPQRSTU') + ['NRP']
def lfs(geo):
    p = e[e.geo == geo].pivot(index='time', columns='nace_r2', values='value').reindex(YRS)
    p = p.reindex(columns=sorted(set(p.columns) | set(SECTIONS)))
    tot = p[SECTIONS].fillna(0).sum(axis=1)   # small confidential sections (DE: A,B,I,T,U) treated as 0
    tot[p['J62_J63'].isna()] = float('nan')
    out = pd.DataFrame(index=p.index)
    out['vendor_J62_J63'] = p['J62_J63']
    out['vendor_J58_J60_J62_J63'] = p['J58-J60'] + p['J62_J63']
    out['all_industries'] = tot
    out['client_broad'] = tot - p['J62_J63']                      # everything outside J62-63
    out['client_narrow'] = tot - p['J'] - p['C26'] - p['M69-M71'] - p['N']   # excl. all of J, electronics mfg, consulting/head offices, admin incl. staffing
    out['client_finance_K'] = p['K']
    return out
for geo, tag in [('EU27_2020', 'eu27'), ('DE', 'de')]:
    o = lfs(geo)
    for c in o: s[f'{tag}_ict_{c}'] = o[c]
s['eu27xde_ict_vendor_J62_J63'] = s['eu27_ict_vendor_J62_J63'] - s['de_ict_vendor_J62_J63']
s['eu27xde_ict_client_narrow'] = s['eu27_ict_client_narrow'] - s['de_ict_client_narrow']
s['eu27xde_ict_client_broad'] = s['eu27_ict_client_broad'] - s['de_ict_client_broad']
s['eu27_ict_inhouse_share_narrow'] = s['eu27_ict_client_narrow'] / (s['eu27_ict_client_narrow'] + s['eu27_ict_vendor_J62_J63'])
s['eu27_ict_inhouse_share_broad'] = s['eu27_ict_client_broad'] / (s['eu27_ict_client_broad'] + s['eu27_ict_vendor_J62_J63'])

# ---- Eurostat GDP and IPP GFCF ----
g = pd.read_csv(os.path.join(R, 'eurostat_nama_10_gdp_long.csv'))
s['eu27_real_gdp'] = g[g.unit == 'CLV20_MEUR'].set_index('time')['value'].reindex(YRS)
a = pd.read_csv(os.path.join(R, 'eurostat_nama_10_an6_long.csv'))
ipp = a[(a.asset10 == 'N117G') & (a.unit == 'CLV20_MEUR')].pivot(index='time', columns='geo', values='value').reindex(YRS)
s['eu27_ipp_gfcf_real'] = ipp['EU27_2020']
s['eu27xie_ipp_gfcf_real_approx'] = ipp['EU27_2020'] - ipp['IE']   # chain-linked volumes are not additive: approximation
s['de_fr_ipp_gfcf_real'] = ipp['DE'] + ipp['FR']

# ---- ONS UK ----
r = list(csv.reader(open(os.path.join(R, 'ons_cxnv.csv'), encoding='utf-8', errors='replace')))
cd = r[1]
def ons_q(cdid):
    j = cd.index(cdid); vals = {}
    for row in r:
        lab = row[0]
        if len(lab) == 7 and lab[4:6] == ' Q' and row[j] not in ('', None):
            vals.setdefault(int(lab[:4]), []).append(float(row[j]))
    return pd.Series({y: sum(v) for y, v in vals.items() if len(v) == 4}).reindex(YRS)
s['uk_software_total_cp'] = ons_q('EF3C')
s['uk_software_purchased_cp'] = ons_q('EF8L')
s['uk_software_ownacct_cp'] = ons_q('EF9P')
s['uk_software_ownacct_share'] = s['uk_software_ownacct_cp'] / (s['uk_software_ownacct_cp'] + s['uk_software_purchased_cp'])
def ons_a(fn):
    j = json.load(open(os.path.join(R, fn)))
    return pd.Series({int(x['year']): float(x['value']) for x in j['years']}).reindex(YRS)
s['uk_real_gdp'] = ons_a('ons_abmi_qna.json'); s['uk_gdp_deflator'] = ons_a('ons_ybgb_qna.json')
s.reset_index().to_csv(os.path.join(D, 'europe_series_annual.csv'), index=False, float_format='%.4f')

def gr(x): return 100 * x.astype(float).map(math.log).diff()
PRE = [2016, 2017, 2018, 2019, 2022]          # LFS: drop break years 2020 (DE) and 2021 (EU)
PRE_ALL = list(range(2016, 2023)); PRE_1619 = list(range(2016, 2020)); POST = [2023, 2024, 2025]
spec = [
 ('eu27_ict_vendor_J62_J63', 'EU27 ICT specialists in NACE J62-63 (vendors)', 'vendor-side labour (outcome)', PRE),
 ('eu27_ict_client_narrow', 'EU27 ICT specialists in client industries (excl. J, C26, M69-71, N)', 'non-circular: in-house tech labour', PRE),
 ('eu27_ict_client_broad', 'EU27 ICT specialists outside J62-63', 'non-circular: in-house tech labour (broad)', PRE),
 ('eu27_ict_client_finance_K', 'EU27 ICT specialists in finance & insurance', 'non-circular: in-house tech labour', PRE),
 ('eu27_ict_all_industries', 'EU27 ICT specialists, all industries', 'market tech labour (includes AI s)', PRE),
 ('eu27xde_ict_vendor_J62_J63', 'EU27 excl. DE, ICT specialists in J62-63', 'vendor-side labour', [y for y in PRE_ALL if y != 2021]),
 ('eu27xde_ict_client_narrow', 'EU27 excl. DE, ICT specialists in client industries', 'in-house tech labour', [y for y in PRE_ALL if y != 2021]),
 ('eu27_real_gdp', 'EU27 real GDP', 'non-circular driver (market d)', PRE_ALL),
 ('eu27xie_ipp_gfcf_real_approx', 'EU27 excl. IE real GFCF in IPP (software+R&D+other)', 'non-circular-ish driver: client IP investment (includes purchased software => partly circular)', PRE_ALL),
 ('de_fr_ipp_gfcf_real', 'DE+FR real GFCF in IPP', 'as above, no Irish/Dutch IP relocations', PRE_ALL),
 ('uk_real_gdp', 'UK real GDP (ONS ABMI)', 'non-circular driver (market d)', PRE_ALL),
 ('uk_gdp_deflator', 'UK GDP deflator (ONS YBGB)', 'deflator', PRE_ALL),
 ('uk_software_ownacct_cp', 'UK own-account software GFCF, nominal (ONS EF9P)', 'non-circular: in-house software work (labour-cost based)', PRE_ALL),
 ('uk_software_purchased_cp', 'UK purchased software GFCF, nominal (ONS EF8L)', 'CIRCULAR: purchased custom + packaged software = vendor output', PRE_ALL),
 ('uk_software_total_cp', 'UK total software GFCF, nominal (ONS EF3C)', 'partly circular', PRE_ALL),
]
rows = []
def row(name, lab, role, x, pre):
    return {'series': name, 'label': lab, 'role': role, 'pre_years': ','.join(map(str, pre)),
            'avg_g_pre': round(x.loc[pre].mean(), 2), 'avg_g_2016_19': round(x.loc[PRE_1619].mean(), 2),
            'avg_g_2023_25': round(x.loc[POST].mean(), 2), 'g_2023': round(x.loc[2023], 2), 'g_2024': round(x.loc[2024], 2), 'g_2025': round(x.loc[2025], 2),
            'change_vs_pre': round(x.loc[POST].mean() - x.loc[pre].mean(), 2), 'change_vs_2016_19': round(x.loc[POST].mean() - x.loc[PRE_1619].mean(), 2)}
for c, lab, role, pre in spec:
    rows.append(row(c, lab, role, gr(s[c]), pre))
for a_, b_, lab, pre in [('eu27_ict_vendor_J62_J63', 'eu27_ict_client_narrow', 'EU27: J62-63 minus client (narrow) ICT-specialist growth', PRE),
                         ('eu27_ict_vendor_J62_J63', 'eu27_ict_client_broad', 'EU27: J62-63 minus all-outside-J62-63 ICT-specialist growth', PRE),
                         ('eu27xde_ict_vendor_J62_J63', 'eu27xde_ict_client_narrow', 'EU27 excl. DE: J62-63 minus client (narrow)', [y for y in PRE_ALL if y != 2021]),
                         ('uk_software_purchased_cp', 'uk_software_ownacct_cp', 'UK: purchased minus own-account software GFCF, nominal', PRE_ALL)]:
    rows.append(row(f'{a_}-{b_}', lab, 'vendor vs in-house relative shift', gr(s[a_]) - gr(s[b_]), pre))
out = pd.DataFrame(rows)
out.to_csv(os.path.join(D, 'europe_prepost.csv'), index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 50)
print(out.drop(columns=['label', 'role']).to_string())
print(s[['eu27_ict_vendor_J62_J63', 'eu27_ict_client_narrow', 'eu27_ict_client_broad', 'eu27_ict_inhouse_share_narrow', 'uk_software_purchased_cp', 'uk_software_ownacct_cp', 'uk_software_ownacct_share']].round(3).to_string())
