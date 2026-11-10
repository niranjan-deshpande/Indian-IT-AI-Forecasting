"""M5(a): BEA NIPA Table 5.6.5/5.6.6/5.6.4 - private software investment by type.
Reads raw/bea/NipaDataA.txt and NipaDataQ.txt (BEA flat files, apps.bea.gov/national/Release/TXT/).
Run: python3 -I bea_software.py <demand_shift_dir>
"""
import csv, sys, os, math
D = sys.argv[1]
def load(path):
    out = {}
    with open(path) as f:
        r = csv.reader(f); next(r)
        for code, per, val in r:
            try: out[(code, per)] = float(val.replace(',', ''))
            except ValueError: pass
    return out
A = load(os.path.join(D, 'raw/bea/NipaDataA.txt'))
Q = load(os.path.join(D, 'raw/bea/NipaDataQ.txt'))
S = {  # code: label   (C=current $mn, X=chained 2017 $mn, G=price index 2017=100)
 'B985RC':'software_nom','Y003RC':'prepack_nom','Y004RC':'custom_nom','Y005RC':'ownacct_nom',
 'B985RX':'software_real','Y003RX':'prepack_real','Y004RX':'custom_real','Y005RX':'ownacct_real',
 'B985RG':'software_px','Y003RG':'prepack_px','Y004RG':'custom_px','Y005RG':'ownacct_px',
 'Y053RC':'govt_software_nom','A008RC':'nonres_fi_nom','A191RD':'gdp_deflator','A191RC':'gdp_nom',
}
years = list(range(2010, 2026))
rows = []
for y in years:
    r = {'year': y}
    for c, lab in S.items(): r[lab] = A.get((c, str(y)))
    r['ownacct_share_nom'] = r['ownacct_nom'] / (r['custom_nom'] + r['ownacct_nom'])
    r['ownacct_share_of_software_nom'] = r['ownacct_nom'] / r['software_nom']
    r['custom_share_of_gdp_pct'] = 100 * r['custom_nom'] / r['gdp_nom']
    r['custom_plus_own_nom'] = r['custom_nom'] + r['ownacct_nom']
    rows.append(r)
# growth (log points x100)
def g(a, b): return None if (a is None or b is None) else 100 * math.log(b / a)
for i in range(1, len(rows)):
    for k in ['software_nom','custom_nom','ownacct_nom','prepack_nom','custom_real','ownacct_real','custom_plus_own_nom','custom_px','ownacct_px','gdp_nom','nonres_fi_nom']:
        rows[i]['g_' + k] = g(rows[i-1][k], rows[i][k])
cols = list(rows[-1].keys())
with open(os.path.join(D, 'bea_software_annual.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in rows: w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})
# quarterly total software, 2026 H1 vs 2025 H1 (detail by type not published quarterly in flat file)
qs = {p: Q.get(('B985RC', p)) for p in ['2025Q1','2025Q2','2026Q1','2026Q2']}
h1 = g(qs['2025Q1'] + qs['2025Q2'], qs['2026Q1'] + qs['2026Q2'])
with open(os.path.join(D, 'bea_software_quarterly_total.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['period', 'software_nom_saar_mn'])
    for y in range(2023, 2027):
        for q in range(1, 5):
            v = Q.get(('B985RC', f'{y}Q{q}'))
            if v: w.writerow([f'{y}Q{q}', v])
# summary: pre (2016-2022 avg annual log growth) vs post (2023-2025)
def avg(k, y0, y1):
    v = [r['g_' + k] for r in rows if y0 <= r['year'] <= y1 and r.get('g_' + k) is not None]
    return sum(v) / len(v)
print('series, avg g 2016-19, avg g 2016-22, avg g 2023-25, 2024, 2025')
for k in ['software_nom','prepack_nom','custom_nom','ownacct_nom','custom_plus_own_nom','custom_real','ownacct_real','custom_px','ownacct_px','gdp_nom','nonres_fi_nom']:
    by = {r['year']: r.get('g_' + k) for r in rows}
    print(f"{k:22s} {avg(k,2016,2019):6.2f} {avg(k,2016,2022):6.2f} {avg(k,2023,2025):6.2f} {by[2024]:6.2f} {by[2025]:6.2f}")
print('own-account share of (custom+own):', {r['year']: round(r['ownacct_share_nom'], 4) for r in rows if r['year'] >= 2014})
print('custom % GDP:', {r['year']: round(r['custom_share_of_gdp_pct'], 3) for r in rows if r['year'] >= 2014})
print('total software 2026H1 vs 2025H1 log pts:', round(h1, 2))
