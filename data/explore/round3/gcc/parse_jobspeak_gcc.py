"""Extract the Naukri JobSpeak 'GCC' industry-index row from text-layer JobSpeak PDFs in raw/jobspeak/.
Each report table shows 13 months (same month last year .. report month). Later vintages overwrite earlier.
Reports from 2025 onward render the industry table as images (no text layer) - not parsed.
Run: python3 -I parse_jobspeak_gcc.py   (needs pdftotext on PATH)
"""
import subprocess, re, csv, datetime
REPORTS = [('July-2024', 2024, 7), ('August-2024', 2024, 8), ('September-2024', 2024, 9), ('October-2024', 2024, 10)]
vals = {}
for name, y, m in REPORTS:
    txt = subprocess.run(['pdftotext', '-layout', f'raw/jobspeak/js_{name}.pdf', '-'], capture_output=True, text=True).stdout
    row = [l for l in txt.splitlines() if re.match(r'\s*GCC\s+\d', l)]
    if not row: print(name, 'no GCC table row'); continue
    nums = re.findall(r'-?\d+%|\d+', row[0])
    idx = [int(x) for x in nums if not x.endswith('%')]
    yoy = [x for x in nums if x.endswith('%')]
    months = [(y - 1 + (m + k - 1) // 12, (m + k - 1) % 12 + 1) for k in range(13)]
    url = f'https://www.infoedge.in/pdfs/News_Events_pdfs/Naukri-Jobspeak-{name}.pdf'
    for (yy, mm), v in zip(months, idx[-13:]):
        vals[f'{yy}-{mm:02d}'] = (v, name, url)
    print(name, idx[-13:], yoy)
with open('jobspeak_gcc_index.csv', 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['month', 'gcc_index', 'vintage_report', 'source_url'])
    for k in sorted(vals): w.writerow([k, *vals[k]])
