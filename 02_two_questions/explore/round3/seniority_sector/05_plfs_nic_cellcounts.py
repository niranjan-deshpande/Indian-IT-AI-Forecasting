"""Pull unweighted case counts for PLFS industry-code variables from the public NADA variable
pages on microdata.gov.in (no login needed for metadata; unit-level data need a free login).
Sums cases whose NIC code starts with 62 or 63 (2-digit or 5-digit codes).
Run: python3 -I 05_plfs_nic_cellcounts.py <out_csv>"""
import sys, re, html, csv, urllib.request
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'
targets = [  # (catalog id, round label, file, variable path, description)
    (213, 'PLFS 2023-24 (Jul-Jun), first-visit person file perv1', 'perv1', 'F4/V206', 'Usual principal status industry code (NIC)'),
    (213, 'PLFS 2023-24 (Jul-Jun), first-visit person file perv1', 'perv1', 'F4/V305', 'CWS industry code'),
    (292, 'PLFS quarterly Apr-Jun..Oct-Dec 2025, person file MPER_Q2_Q4_2025', 'MPER_Q2_Q4_2025', 'F2/V75', 'industry code ind16'),
]
def fetch(u):
    r = urllib.request.Request(u, headers={'User-Agent': UA})
    return urllib.request.urlopen(r, timeout=60).read().decode('utf-8', 'ignore')
rows = []
for cid, rnd, f, v, desc in targets:
    url = f'https://microdata.gov.in/NADA/index.php/catalog/{cid}/variable/{v}'
    t = fetch(url)
    t = re.sub(r'<script.*?</script>', '', t, flags=re.S)
    t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', t)))
    valid = re.search(r'Valid:\s*(\d+)', t); valid = int(valid.group(1)) if valid else None
    seg = t[t.find('Value Category Cases'):t.find('Warning')]
    pairs = re.findall(r'(\d+)\s+(?:\S+\s+)??(\d+)\s+[\d.]+%', seg)
    c62 = sum(int(n) for code, n in pairs if code.startswith('62'))
    c63 = sum(int(n) for code, n in pairs if code.startswith('63'))
    rows.append(dict(catalog=cid, round=rnd, variable=v, description=desc, valid_cases=valid,
                     n_categories_parsed=len(pairs), cases_nic62=c62, cases_nic63=c63, source_url=url))
    print(rows[-1])
with open(sys.argv[1], 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
