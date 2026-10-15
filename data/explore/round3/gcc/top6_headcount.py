"""Top-six combined March (fiscal-year-end) headcount and shortfall vs trend.
Input: data/corrected/core_quarterly_final.csv. FY t = quarter ending March of year t (cal_q 'tQ1').
LTIMindtree before FY22 = LTI + Mindtree (DECISIONS D9 notes the combined restated series is ~3% below the sum).
Run from repo root: python3 -I data/explore/round3/gcc/top6_headcount.py
"""
import csv, math
SRC = 'data/corrected/core_quarterly_final.csv'
OUT = 'data/explore/round3/gcc/top6_headcount_fy.csv'
rows = list(csv.DictReader(open(SRC)))
hc, src = {}, {}
for r in rows:
    if r['cal_q'].endswith('Q1') and r['headcount']:
        fy = int(r['cal_q'][:4])
        hc[(r['firm'], fy)] = float(r['headcount']); src[(r['firm'], fy)] = r['headcount_src']
def firm_hc(f, fy):
    if f == 'ltim' and (f, fy) not in hc:
        if ('lti', fy) in hc and ('mindtree', fy) in hc:
            return hc[('lti', fy)] + hc[('mindtree', fy)], 'lti+mindtree'
        return None, ''
    return hc.get((f, fy)), src.get((f, fy), '')
firms = ['tcs', 'infosys', 'hcltech', 'wipro', 'techm', 'ltim']
out = []
for fy in range(2016, 2027):
    vals = {f: firm_hc(f, fy) for f in firms}
    if any(v[0] is None for v in vals.values()):
        print('missing', fy, [f for f, v in vals.items() if v[0] is None]); continue
    tot = sum(v[0] for v in vals.values())
    out.append(dict(fy=f'FY{fy%100:02d}', **{f: int(vals[f][0]) for f in firms}, top6=int(tot),
                    source_file=SRC, source_urls=' | '.join(vals[f][1] for f in firms)))
tot = {int(o['fy'][2:]) + 2000: o['top6'] for o in out}
pre = (tot[2020] / tot[2016]) ** (1 / 4) - 1
print('pre-COVID CAGR FY16-FY20: %.2f%%' % (100 * pre))
for o in out:
    fy = int(o['fy'][2:]) + 2000
    o['yoy_pct'] = round(100 * (tot[fy] / tot[fy - 1] - 1), 1) if fy - 1 in tot else ''
    o['trend7_from_FY23'] = int(tot[2023] * 1.07 ** (fy - 2023)) if fy >= 2023 else ''
    o['trend7_from_FY20'] = int(tot[2020] * 1.07 ** (fy - 2020)) if fy >= 2020 else ''
    o['trendpre_from_FY23'] = int(tot[2023] * (1 + pre) ** (fy - 2023)) if fy >= 2023 else ''
with open(OUT, 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
for o in out:
    print({k: v for k, v in o.items() if k != 'source_urls' and k != 'source_file'})
a = tot[2026]
print('FY26 actual', a)
print('shortfall vs flat from FY23:', tot[2023] - a)
print('shortfall vs 7%% from FY23: %d' % (tot[2023] * 1.07 ** 3 - a))
print('shortfall vs 7%% from FY20: %d' % (tot[2020] * 1.07 ** 6 - a))
print('shortfall vs pre-COVID CAGR from FY23: %d' % (tot[2023] * (1 + pre) ** 3 - a))
print('shortfall vs 7%% from FY24 base? (FY24->26): %d' % (tot[2024] * 1.07 ** 2 - a))
