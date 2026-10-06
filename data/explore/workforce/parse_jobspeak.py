"""Parse Naukri JobSpeak monthly PDFs (Info Edge IR: https://www.infoedge.in/pdfs/News_Events_pdfs/Naukri-Jobspeak-<Mon>-<YYYY>.pdf)
-> tidy CSV of the 13-month annex windows (index level, base Jul-2008=1000).
Months are assigned from the report month in the FILE NAME (last column = report month, 12 columns before it),
because the PDFs' header rows contain typos (e.g. Jul-2024 annex labels Jan'24 as Jan'23).
Rows: IT-Software/Software Services, BPO/ITES, experience bands (annex exists ~Nov-2022..Dec-2024 only).
Usage: python parse_jobspeak.py <dir_with_pdftotext_-layout_txt> <out_csv>"""
import re, sys, glob, os, pandas as pd
MON = {m:i for i,m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split(),1)}
ROWS = {"it_software":r"^\s*IT-Software\s*/\s*Software Services", "bpo_ites":r"^\s*BPO\s*/\s*ITES",
        "exp_0_3":r"^\s*0\s*-\s*3\s*yrs", "exp_4_7":r"^\s*4\s*-\s*7\s*yrs", "exp_8_12":r"^\s*8\s*-\s*12\s*yrs",
        "exp_13_16":r"^\s*13\s*-\s*1[56]\s*yrs", "exp_16plus":r"^\s*(>\s*16|16\s*\+|above 16)\s*yrs"}
recs=[]
for f in sorted(glob.glob(os.path.join(sys.argv[1],"*.txt"))):
    b=os.path.basename(f); m=re.search(r"Jobspeak-([A-Za-z]+)-?(\d{4})",b,re.I)
    rp=pd.Period(f"{m.group(2)}-{MON[m.group(1)[:3].lower()]:02d}",freq="M")
    months=[str(rp-k) for k in range(12,-1,-1)]
    done=set()
    for ln in open(f,errors="ignore").read().splitlines():
        for k,pat in ROWS.items():
            if k in done or not re.search(pat,ln,re.I): continue
            nums=[int(x) for x in re.findall(r"(?<![\d.%+\-])(\d{3,5})(?![\d%])",ln)]
            if len(nums)>=13:
                done.add(k)
                for mm,v in zip(months,nums[:13]):
                    recs.append(dict(series=k,month=mm,value=v,vintage=b.replace(".txt",".pdf"),report_month=str(rp)))
d=pd.DataFrame(recs)
d["source_url"]="https://www.infoedge.in/pdfs/News_Events_pdfs/"+d.vintage
d.to_csv(sys.argv[2],index=False); print(d.groupby("series").month.agg(["min","max","nunique","count"]))
