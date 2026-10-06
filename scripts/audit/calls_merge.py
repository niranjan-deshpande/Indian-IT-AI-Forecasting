"""STEP 3: merge price + demand statements -> audit/calls_statements.csv (+ audit/calls_merge_log.csv).

Duplicate rule: a demand row is a cross-pass duplicate of a price row if both are from the same call and
their whitespace/case-normalised texts overlap: one contains the other, or they share a run of >= 12
consecutive words. The price row (original id) is kept; the demand row is dropped and logged.
"""
import sys, os, csv, re
sys.path.insert(0, os.path.dirname(__file__))
from calls_common import ROOT, FIRMS, half_year

P = list(csv.DictReader(open(f"{ROOT}/audit/price_calls_quotes.csv")))
D = list(csv.DictReader(open(f"{ROOT}/audit/demand_calls_quotes.csv")))


def words(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.findall(r"[a-z0-9']+", s.lower())


def overlap(a, b, k=12):
    wa, wb = words(a), words(b)
    sa, sb = " ".join(wa), " ".join(wb)
    if sa in sb or sb in sa:
        return True, min(len(wa), len(wb))
    grams = {tuple(wa[i:i + k]) for i in range(len(wa) - k + 1)}
    best = 0
    for i in range(len(wb) - k + 1):
        if tuple(wb[i:i + k]) in grams:
            j = k
            while i + j < len(wb) and " ".join(wb[i:i + j + 1]) in sa:
                j += 1
            best = max(best, j)
    return best >= k, best


log, drop = [], set()
for d in D:
    for p in P:
        if (p['firm'], p['call']) != (d['firm'], d['call']):
            continue
        ok, n = overlap(p['quote'], d['quote'])
        if ok:
            drop.add(d['id'])
            log.append(dict(dropped_id=d['id'], kept_id=p['id'], firm=d['firm'], call=d['call'],
                            shared_words=n, dropped_quote=d['quote'], kept_quote=p['quote'],
                            reason="same call, overlapping text (containment or >=12-word shared run); price row kept"))
            break

cols = ["stmt_id", "source_pass", "firm", "call", "call_date", "half_year", "speaker", "quote",
        "source_url", "source_doc", "page"]
out = []
for src, rows in (("price", P), ("demand", D)):
    for r in rows:
        if r['id'] in drop:
            continue
        out.append(dict(stmt_id=r['id'], source_pass=src, firm=r['firm'], call=r['call'], call_date=r['call_date'],
                        half_year=half_year(r['call_date']), speaker=r['speaker'], quote=r['quote'],
                        source_url=r['source_url'], source_doc=r['source_doc'], page=r['page']))
out.sort(key=lambda r: (FIRMS.index(r['firm']), r['call_date'], r['source_pass'] != 'price', r['stmt_id']))
assert len({r['stmt_id'] for r in out}) == len(out)
with open(f"{ROOT}/audit/calls_statements.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(out)
lc = ["dropped_id", "kept_id", "firm", "call", "shared_words", "reason", "dropped_quote", "kept_quote"]
with open(f"{ROOT}/audit/calls_merge_log.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=lc); w.writeheader(); w.writerows(log)
print(f"price {len(P)} + demand {len(D)} - dropped {len(drop)} = {len(out)} statements")
