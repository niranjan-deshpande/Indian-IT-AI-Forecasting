"""Download Cognizant (CIK 1058290) earnings-release 8-K exhibits (99.1) and 10-Q/10-K primary docs from EDGAR."""
import json, os, time, requests, csv
BASE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'sources', 'cognizant')
BASE = os.path.abspath(BASE)
UA = {'User-Agent': 'ndeshpande research ndeshpande@college.harvard.edu'}
CIK = 1058290
def get(url):
    for k in range(5):
        r = requests.get(url, headers=UA, timeout=60)
        if r.status_code == 200:
            time.sleep(0.15); return r
        time.sleep(2)
    raise RuntimeError(f'{url} {r.status_code}')
filings = []
for fn in ['submissions.json', 'submissions-001.json']:
    d = json.load(open(os.path.join(BASE, fn)))
    r = d['filings']['recent'] if 'filings' in d else d
    for i, f in enumerate(r['form']):
        fd = r['filingDate'][i]
        if fd < '2014-01-01': continue
        if f in ('10-Q', '10-K') or (f == '8-K' and '2.02' in r['items'][i]):
            filings.append(dict(form=f, date=fd, acc=r['accessionNumber'][i], primary=r['primaryDocument'][i],
                                report=r['reportDate'][i]))
os.makedirs(os.path.join(BASE, 'edgar'), exist_ok=True)
manifest = []
for f in filings:
    accnd = f['acc'].replace('-', '')
    folder = f'https://www.sec.gov/Archives/edgar/data/{CIK}/{accnd}/'
    if f['form'] == '8-K':
        idx = get(folder + 'index.json').json()
        items = [it['name'] for it in idx['directory']['item']]
        # find exhibit 99.1: names containing ex99 / exhibit991 / ex-99
        cands = [n for n in items if n.lower().endswith(('.htm', '.html')) and n != f['primary'] and
                 any(k in n.lower() for k in ['ex99', 'ex-99', 'exhibit99', 'exhibit991', 'ex991', 'q', 'release'])]
        cands = [n for n in cands if 'index' not in n.lower()]
        docs = cands or [f['primary']]
    else:
        docs = [f['primary']]
    for doc in docs:
        local = os.path.join(BASE, 'edgar', f"{f['date']}_{f['form']}_{doc}")
        url = folder + doc
        if not os.path.exists(local):
            open(local, 'wb').write(get(url).content)
        manifest.append(dict(form=f['form'], filing_date=f['date'], report_date=f['report'], acc=f['acc'], doc=doc, url=url, local=os.path.basename(local)))
        print(f['form'], f['date'], doc)
with open(os.path.join(BASE, 'manifest.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(manifest[0].keys())); w.writeheader(); w.writerows(manifest)
