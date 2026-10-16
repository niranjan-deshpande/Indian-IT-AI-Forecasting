"""Parse raw Screener / Tickertape downloads into a tidy firm-FY table.
Run with: python3 -I parse_firm_financials.py
Writes raw_parsed_screener_tickertape.csv (intermediate, one row per firm-FY).
"""
import os, re, json, html as htmllib
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'raw', 'firms')
FIRMS = {
    'tcs': ('TCS', 'TCS'), 'infosys': ('INFY', 'INFY'), 'hcltech': ('HCLTECH', 'HCLT'),
    'wipro': ('WIPRO', 'WIPR'), 'techm': ('TECHM', 'TEML'), 'ltim': ('LTM', 'LRTI'),
    'mindtree': ('MINDTREE', 'MINT'), 'persistent': ('PERSISTENT', 'PERS'),
    'coforge': ('COFORGE', 'COFO'), 'mphasis': ('MPHASIS', 'MBFL'),
}


def num(s):
    s = s.replace(',', '').replace('%', '').strip()
    try:
        return float(s)
    except ValueError:
        return None


def parse_screener(sym):
    h = open(os.path.join(RAW, f'screener_{sym}_consolidated.html'), errors='ignore').read()
    i = h.find('id="profit-loss"')
    sec = h[i:]
    sec = sec[:sec.find('</table>')]
    heads = re.findall(r'<th[^>]*>(.*?)</th>', sec, re.S)
    heads = [re.sub(r'<[^>]+>', '', x).strip() for x in heads]
    rows = {}
    for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', sec, re.S):
        cells = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)
        if not cells:
            continue
        cells = [htmllib.unescape(re.sub(r'<[^>]+>', '', c)).replace('\xa0', ' ').strip() for c in cells]
        label = cells[0].replace('+', '').strip()
        rows[label] = cells[1:]
    cols = heads[1:]
    out = []
    for j, c in enumerate(cols):
        m = re.match(r'(\w{3}) (\d{4})', c)
        if not m:
            continue
        rec = {'period': c}
        for lab, key in [('Sales', 'sales'), ('Revenue', 'sales'), ('Expenses', 'expenses'),
                         ('Operating Profit', 'op'), ('Other Income', 'other_income'),
                         ('Interest', 'interest'), ('Depreciation', 'dep'),
                         ('Profit before tax', 'pbt')]:
            if lab in rows and j < len(rows[lab]):
                rec[key] = num(rows[lab][j])
        out.append(rec)
    return pd.DataFrame(out)


def parse_screener_exp(sym):
    p = os.path.join(RAW, f'screener_{sym}_expenses.json')
    if not os.path.exists(p):
        return {}
    d = json.load(open(p))
    return {k: num(v) for k, v in d.get('Employee Cost %', {}).items() if k.startswith(('Mar', 'Jun', 'Dec'))}


def parse_tt(sid):
    d = json.load(open(os.path.join(RAW, f'tickertape_{sid}_income_annual.json')))['data']
    out = {}
    for r in d:
        if not r['displayPeriod'].startswith('FY'):
            continue
        out[r['endDate'][:7]] = r
    return out


rows = []
for firm, (sym, sid) in FIRMS.items():
    s = parse_screener(sym)
    e = parse_screener_exp(sym)
    t = parse_tt(sid)
    for _, r in s.iterrows():
        mon, yr = r['period'].split()[:2]
        rec = dict(firm=firm, period=r['period'], **{k: r.get(k) for k in
                   ['sales', 'expenses', 'op', 'other_income', 'interest', 'dep', 'pbt']})
        rec['scr_emp_pct'] = e.get(r['period'])
        mm = {'Mar': '03', 'Jun': '06', 'Dec': '12'}.get(mon)
        tr = t.get(f'{yr}-{mm}')
        if tr:
            rec.update(tt_trev=tr['incTrev'], tt_emp=tr['incEpc'], tt_ebitda=tr['incEbi'],
                       tt_dep=tr['incDep'], tt_ope=tr['incOpe'], tt_sga=tr['incSga'],
                       tt_raw=tr['incRaw'], tt_pfc=tr['incPfc'])
        rows.append(rec)
df = pd.DataFrame(rows)
df.to_csv(os.path.join(HERE, 'raw_parsed_screener_tickertape.csv'), index=False)
pd.set_option('display.width', 250, 'display.max_rows', 300)
print(df.to_string())
