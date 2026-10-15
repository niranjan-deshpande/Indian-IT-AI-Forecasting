"""Parse NIRF institution PDFs (Engineering, editions 2019-2025): UG 4-year placement table.
Run: python3 -I 02_parse_nirf.py <seniority_sector dir>
Output: nirf_ug4_placement_long.csv (one row per edition x institution x graduating year)."""
import sys, os, re, subprocess, csv
base = sys.argv[1]
pdfdir = os.path.join(base, 'raw', 'nirf', 'pdf')
row_re = re.compile(r'^\s*(\d{4}-\d{2})\s+(\S+)\s+(\S+)\s+(\d{4}-\d{2})\s+(\S+)\s+(\d{4}-\d{2})\s+(\S+)\s+(\S+)\s+(\S+?)(?:\(.*?)?\s+(\d+|-|<blank>)?\s*$')
def num(s):
    s = (s or '').strip().replace(',', '')
    m = re.match(r'^(\d+(?:\.\d+)?)', s)
    return float(m.group(1)) if m else None
out = []
for ed in sorted(os.listdir(pdfdir)):
    sub = 'ENGINEERING' if ed == '2019' else 'Engineering'
    for fn in sorted(os.listdir(os.path.join(pdfdir, ed))):
        p = os.path.join(pdfdir, ed, fn)
        txt = subprocess.run(['pdftotext', '-layout', p, '-'], capture_output=True, text=True).stdout
        m = re.search(r'Institute Name:\s*(.+?)\s*\[', txt); name = m.group(1).strip() if m else ''
        i = txt.find('UG [4 Years Program(s)]: Placement')
        if i < 0: continue
        j = txt.find('Program(s)]: Placement', i + 40)
        block = txt[i: j if j > 0 else i + 4000]
        for line in block.splitlines():
            r = row_re.match(line)
            if not r: continue
            g = r.groups()
            out.append(dict(edition=ed, inst_id=fn[:-4], inst_name=name, intake_year=g[0],
                            grad_year=g[5], n_grad_min_time=num(g[6]), n_placed=num(g[7]),
                            median_salary_inr=num(g[8]), n_higher_studies=num(g[9]),
                            source_url=f'https://www.nirfindia.org/nirfpdfcdn/{ed}/pdf/{sub}/{fn}'))
with open(os.path.join(base, 'nirf_ug4_placement_long.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print(len(out), 'rows')
