"""Helper: print PDF page numbers (1-based) whose text matches a regex. usage: findpage.py file.pdf 'regex' [context_lines]"""
import sys, re, subprocess
pdf, pat = sys.argv[1], sys.argv[2]
ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 0
txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
for i, page in enumerate(txt.split('\f'), 1):
    lines = page.split('\n')
    for j, l in enumerate(lines):
        if re.search(pat, l):
            print(f'p{i}: ' + ' | '.join(x.strip() for x in lines[max(0,j-ctx):j+ctx+1]))
