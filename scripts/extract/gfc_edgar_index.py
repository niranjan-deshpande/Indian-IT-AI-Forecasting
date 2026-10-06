"""List EDGAR filings 2007-01..2012-09 for GFC-window firms; save to data/sources/gfc/<firm>/edgar_filings.json"""
import json, time, requests
UA={"User-Agent":"ndeshpande research ndeshpande@college.harvard.edu"}
CIKS={"infosys":["0001067491"],"wipro":["0001123799"],"cognizant":["0001058290"],"accenture":["0001467373","0001134538"]}
for firm,ciks in CIKS.items():
    rows=[]
    for cik in ciks:
        d=requests.get(f"https://data.sec.gov/submissions/CIK{cik}.json",headers=UA).json(); time.sleep(0.2)
        blocks=[d["filings"]["recent"]]
        for f in d["filings"].get("files",[]):
            blocks.append(requests.get("https://data.sec.gov/submissions/"+f["name"],headers=UA).json()); time.sleep(0.2)
        for r in blocks:
            for i in range(len(r["form"])):
                if "2007-01-01"<=r["filingDate"][i]<="2012-09-30":
                    rows.append(dict(cik=cik,name=d.get("name"),form=r["form"][i],date=r["filingDate"][i],acc=r["accessionNumber"][i],
                        doc=r["primaryDocument"][i],desc=r["primaryDocDescription"][i],items=r.get("items",[""]*len(r["form"]))[i]))
    rows.sort(key=lambda x:x["date"])
    json.dump(rows,open(f"data/sources/gfc/{firm}/edgar_filings.json","w"),indent=0)
    print(firm,len(rows))
