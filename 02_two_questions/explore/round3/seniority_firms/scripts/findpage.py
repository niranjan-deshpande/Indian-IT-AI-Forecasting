import sys, subprocess
fn = sys.argv[1]
txt = subprocess.run(['pdftotext', '-layout', fn, '-'], capture_output=True, text=True).stdout
pages = txt.split('\f')
for k in sys.argv[2:]:
    print(k, [i + 1 for i, p in enumerate(pages) if k in p])
