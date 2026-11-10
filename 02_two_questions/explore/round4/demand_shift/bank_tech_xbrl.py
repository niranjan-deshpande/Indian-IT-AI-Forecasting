"""M5(b): Big-4 US bank technology expense lines from SEC XBRL companyfacts (data.sec.gov).
Annual = 12-month duration facts from 10-K filings (latest filed value per period end, i.e. restated where restated).
Also H1 (6-month YTD to June) facts from 10-Q, for a 2026 read.
Run: python3 -I bank_tech_xbrl.py <demand_shift_dir>
"""
import json, sys, os, csv
from datetime import date
D = sys.argv[1]
BANKS = {'0000019617': 'JPM', '0000070858': 'BAC', '0000831001': 'C', '0000072971': 'WFC'}
CONCEPTS = ['CommunicationsAndInformationTechnology', 'InformationTechnologyAndDataProcessing', 'EquipmentExpense',
            'ProfessionalAndContractServicesExpense', 'ProfessionalFees', 'NoninterestExpense', 'OccupancyNet',
            'LaborAndRelatedExpense', 'Revenues', 'RevenuesNetOfInterestExpense']
rows = []
for cik, tk in BANKS.items():
    d = json.load(open(os.path.join(D, f'raw/sec/cf_{cik}.json')))
    g = d['facts'].get('us-gaap', {})
    for c in CONCEPTS:
        if c not in g: continue
        best = {}
        for u, facts in g[c]['units'].items():
            if u != 'USD': continue
            for f in facts:
                if 'start' not in f: continue
                s, e = date.fromisoformat(f['start']), date.fromisoformat(f['end'])
                days = (e - s).days
                if 360 <= days <= 370 and f.get('form', '').startswith('10-K'): kind = 'FY'
                elif 178 <= days <= 185 and e.month == 6 and f.get('form', '').startswith('10-Q'): kind = 'H1'
                else: continue
                key = (kind, e.year)
                if key not in best or f['filed'] > best[key]['filed']: best[key] = f
        for (kind, y), f in best.items():
            rows.append({'bank': tk, 'concept': c, 'period': kind, 'year': y, 'value_usd_mn': f['val'] / 1e6,
                         'form': f['form'], 'filed': f['filed'], 'accn': f['accn']})
rows.sort(key=lambda r: (r['bank'], r['concept'], r['period'], r['year']))
with open(os.path.join(D, 'bank_tech_xbrl_long.csv'), 'w', newline='') as fo:
    w = csv.DictWriter(fo, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
# quick print
from collections import defaultdict
t = defaultdict(dict)
for r in rows: t[(r['bank'], r['concept'], r['period'])][r['year']] = r['value_usd_mn']
for k in sorted(t):
    ys = sorted(y for y in t[k] if y >= 2013)
    print(k, ' '.join(f"{y}:{t[k][y]:.0f}" for y in ys))
