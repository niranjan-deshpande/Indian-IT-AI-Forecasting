import sys,re,glob,subprocess
pat=re.compile(sys.argv[2],re.I)
for f in sorted(glob.glob(sys.argv[1])):
    n=int(re.search(r'Pages:\s+(\d+)',subprocess.run(['pdfinfo',f],capture_output=True,text=True).stdout).group(1))
    for p in range(1,n+1):
        t=subprocess.run(['pdftotext','-f',str(p),'-l',str(p),f,'-'],capture_output=True,text=True).stdout
        t=re.sub(r'\s+',' ',t)
        for m in pat.finditer(t):
            s=t[max(0,m.start()-220):m.end()+220]
            if re.search(r'\d[\d,]{2,}|\d+\s?(k|thousand)',s,re.I):
                print(f"{f} p{p}: ...{s}...\n")
