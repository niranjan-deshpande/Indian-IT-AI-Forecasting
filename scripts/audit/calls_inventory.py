"""STEP 1: reconstruct the 183-transcript inventory of the price pass -> audit/calls_transcripts.csv.
Cross-checks: count 183; firm counts vs coverage table; every (firm, call, call_date, source_doc, url)
in audit/price_calls_quotes.csv is in the inventory; price-pass quotes re-verify against our text.
Optionally dumps page-tagged corpus text to a scratch dir (argv[1]) for reading."""
import sys, os, csv, collections
sys.path.insert(0, os.path.dirname(__file__))
from calls_common import ROOT, FIRMS, build_docs, pages_of, locate

docs = build_docs()
cols = ["firm", "call", "call_date", "half_year", "local_path", "source_url"]
with open(f"{ROOT}/audit/calls_transcripts.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(docs)

print("transcripts:", len(docs))
print("by firm:", dict(collections.Counter(d['firm'] for d in docs)))
yc = collections.Counter((d['firm'], d['call_date'][:4]) for d in docs)
print("firm x year:")
for F in FIRMS:
    print(f"  {F:12s}", [yc[(F, str(y))] for y in range(2021, 2027)])
hc = collections.Counter(d['half_year'] for d in docs)
print("by half-year:", dict(sorted(hc.items())))
for F in FIRMS:
    cs = [d['call'] for d in docs if d['firm'] == F]
    print(f"  {F}: {cs[0]}..{cs[-1]}")

# cross-check with price pass
idx = {(d['firm'], d['call']): d for d in docs}
P = list(csv.DictReader(open(f"{ROOT}/audit/price_calls_quotes.csv")))
bad = 0; nf = 0
for r in P:
    d = idx.get((r['firm'], r['call']))
    if d is None or d['call_date'] != r['call_date'] or d['local_path'] != r['source_doc'] or d['source_url'] != r['source_url']:
        bad += 1; print("MISMATCH", r['id'], r['firm'], r['call'])
        continue
    pg, ep, st = locate(r['firm'], r['call'], r['quote'])
    if st != "exact":
        nf += 1; print("PRICE QUOTE NOT FOUND", r['id'])
print(f"price rows: {len(P)}; metadata mismatches: {bad}; quotes not re-found: {nf}")
print("calls with >=1 price row:", len({(r['firm'], r['call']) for r in P}))

if len(sys.argv) > 1:
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for d in docs:
        with open(f"{out}/{d['firm']}_{d['call']}.txt", "w") as f:
            for pn, x in pages_of(d['firm'], d['call']):
                f.write(f"\n=== PAGE {pn} ===\n{x}")
