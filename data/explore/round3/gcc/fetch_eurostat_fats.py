"""EU27 outward FATS: persons employed in EU-controlled affiliates in India.
2010-2020: fats_out2_r2 (indic_bp=EMP); 2021-2023: fats_out_activ (indic_sbs=EMP_NR). Writes eurostat_fats_india.csv.
Run: python3 -I fetch_eurostat_fats.py
"""
import json, urllib.request, csv
B = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/'
Q = [('fats_out2_r2', 'indic_bp=EMP'), ('fats_out_activ', 'indic_sbs=EMP_NR')]
rows = []
for ds, ind in Q:
    for nace in ['B-S_X_O', 'J', 'J62_J63', 'J62', 'M', 'N']:
        url = f'{B}{ds}?format=JSON&lang=en&geo=EU27_2020&partner=IN&nace_r2={nace}&{ind}'
        try:
            d = json.load(urllib.request.urlopen(url, timeout=60))
        except Exception as e:
            continue
        if 'value' not in d: continue
        times = {v: k for k, v in d['dimension']['time']['category']['index'].items()}
        st = d.get('status', {})
        for i, t in sorted(times.items()):
            v = d['value'].get(str(i)); s = st.get(str(i), '')
            rows.append(dict(dataset=ds, nace_r2=nace, year=t, persons_employed=v if v is not None else '', flag=s, source_url=url))
with open('eurostat_fats_india.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows: print(r['dataset'], r['nace_r2'], r['year'], r['persons_employed'], r['flag'])
