"""Download Infosys quarterly fact-sheet PDFs (FY2012..FY2027) from the Wayback Machine (infosys.com returns 403 to scripts).
Original infosys.com URL is kept as source_url; the archived copy is at web.archive.org/web/<ts>id_/<url>."""
import re, os, time, json, requests  # note: Q4FY16 and Q3FY26 needed manual retries (Wayback rate limiting)
BASE = "data/sources/infosys"
lines = [l.split() for l in open(f"{BASE}/wayback_cdx_quarterly_results.txt")]
best = {}
for l in lines:
    ts, url = l[1], l[2]
    m = re.search(r"quarterly-results/(\d{4})-(\d{4})/q(\d)/(?:documents/)?(fact-sheet)\.pdf$", url, re.I)
    if not m: continue
    fy = int(m.group(2)); q = int(m.group(3))
    if fy < 2012: continue
    key = f"Q{q}FY{fy%100:02d}"
    best.setdefault(key, (ts, url))
os.makedirs(f"{BASE}/factsheets", exist_ok=True)
meta = {}
for key, (ts, url) in sorted(best.items(), key=lambda x: (x[0][4:], x[0][:2])):
    fn = f"{BASE}/factsheets/infosys_{key}_fact-sheet.pdf"
    wb = f"https://web.archive.org/web/{ts}id_/{url}"
    canon = re.sub(r"^http://|:80", "", url); canon = "https://" + canon.replace("https://", "")
    meta[key] = dict(ts=ts, wayback=wb, url=canon, file=fn)
    if os.path.exists(fn) and os.path.getsize(fn) > 10000: continue
    for attempt in range(3):
        try:
            r = requests.get(wb, timeout=180)
            c = r.content
            if c[:2] == b"\x1f\x8b":  # some snapshots are served gzip-encoded
                import gzip; c = gzip.decompress(c)
            if c[:4] == b"%PDF": open(fn, "wb").write(c); break
        except Exception as e: print(e)
        time.sleep(30)
    print(key, ts, os.path.getsize(fn) if os.path.exists(fn) else "FAIL")
    time.sleep(6)
json.dump(meta, open(f"{BASE}/factsheets/meta.json", "w"), indent=1)
print(sorted(meta))
