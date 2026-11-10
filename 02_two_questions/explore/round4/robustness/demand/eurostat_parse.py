"""Parse Eurostat JSON-stat (dissemination API v1.0) into long CSV.
Run: python3 -I eurostat_parse.py <in.json> <out.csv>
"""
import sys, json, itertools, csv
j = json.load(open(sys.argv[1]))
ids, size = j['id'], j['size']
cats = [sorted(j['dimension'][d]['category']['index'].items(), key=lambda kv: kv[1]) for d in ids]
vals, stat = j.get('value', {}), j.get('status', {})
with open(sys.argv[2], 'w', newline='') as f:
    w = csv.writer(f); w.writerow(ids + ['value', 'flag'])
    strides = [1] * len(size)
    for i in range(len(size) - 2, -1, -1): strides[i] = strides[i + 1] * size[i + 1]
    for k, v in vals.items():
        k = int(k); idx = [(k // strides[i]) % size[i] for i in range(len(size))]
        w.writerow([cats[i][idx[i]][0] for i in range(len(ids))] + [v, stat.get(str(k), '')])
