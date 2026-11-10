"""Build rbi_fla_foreign_subs_ic.csv from RBI FLA census press releases saved in raw/rbi_fla/.
Table 9C 'Information and communication' exports of foreign subsidiaries (Rs crore), both years in each round;
within-round growth (same respondent set) in INR and approx USD.
USD conversion: average INR/USD implied by Infosys annual INR revenue / USD revenue (data/corrected/core_quarterly_final.csv),
an approximation of the RBI reference rate. Run from this folder: python3 -I build_fla_csv.py
"""
import re, os, html, csv
PR = {'51367': '2019-20', '52719': '2020-21', '54408': '2021-22', '56359': '2022-23', '58874': '2023-24', '61524': '2024-25'}
FX = {'2018-19': 70.07, '2019-20': 71.04, '2020-21': 74.08, '2021-22': 74.58, '2022-23': 80.59, '2023-24': 82.79, '2024-25': 84.55}
num = lambda s: float(s.replace(',', ''))
rows = []
for p, rnd in PR.items():
    t = open(f'raw/rbi_fla/prid_{p}.html', encoding='utf-8', errors='ignore').read()
    t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S))))
    date = re.search(r'Date\s*:\s*([A-Za-z]{3} \d{1,2}, \d{4})', t).group(1)
    out = {}
    for tab, key in (('9A', 'Sales'), ('9C', 'Export')):
        h = re.search(rf'Table {tab}: Activity-wise {key} of ([\d,]+)\*? Foreign subsidiary', t)
        seg = t[h.start(): h.start() + 6000]
        yrs = re.findall(r'20\d\d-\d\d', seg[:900])[:2]
        if tab == '9A':
            m = re.search(r'Information and communication ([\d,]+) ([\d,]+) ([\d,]+)', seg); vals = m.group(2), m.group(3)
            tm = re.search(r'Total ([\d,]+) ([\d,]+) ([\d,]+)', seg); tots = tm.group(2), tm.group(3)
        else:
            m = re.search(r'Information and communication ([\d,]+) ([\d,]+)', seg); vals = m.group(1), m.group(2)
            tm = re.search(r'Total ([\d,]+) ([\d,]+)', seg); tots = tm.group(1), tm.group(2)
        out[tab] = (yrs, vals, tots, h.group(1))
    yrs, ex, extot, nsub = out['9C']; _, sa, _, _ = out['9A']
    url = f'https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid={p}'
    g_inr = 100 * (num(ex[1]) / num(ex[0]) - 1)
    g_usd = 100 * ((num(ex[1]) / FX[yrs[1]]) / (num(ex[0]) / FX[yrs[0]]) - 1)
    rows.append(dict(census_round=rnd, release_date=date, n_foreign_subsidiaries=nsub.replace(',', ''),
                     prev_fy=yrs[0], cur_fy=yrs[1],
                     ic_exports_prev_rs_cr=num(ex[0]), ic_exports_cur_rs_cr=num(ex[1]),
                     all_activity_exports_prev_rs_cr=num(extot[0]), all_activity_exports_cur_rs_cr=num(extot[1]),
                     ic_sales_prev_rs_cr=num(sa[0]), ic_sales_cur_rs_cr=num(sa[1]),
                     ic_exports_cur_usd_bn_approx=round(num(ex[1]) * 1e7 / FX[yrs[1]] / 1e9, 1),
                     within_round_growth_inr_pct=round(g_inr, 1), within_round_growth_usd_pct_approx=round(g_usd, 1),
                     source_url=url))
with open('rbi_fla_foreign_subs_ic.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows: print(r['cur_fy'], r['ic_exports_cur_rs_cr'], r['ic_exports_cur_usd_bn_approx'], r['within_round_growth_inr_pct'], r['within_round_growth_usd_pct_approx'], r['n_foreign_subsidiaries'])
