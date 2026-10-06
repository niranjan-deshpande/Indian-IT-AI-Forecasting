"""UK Find a Tender (FTS) scan: OCDS release packages API (public, no key), stages=award, monthly windows 2021-01..2026-09.
Keeps only award/contract releases whose supplier parties match the 8 firms. FTS starts 2021-01-01 (post-Brexit; pre-2021 = TED/OJEU)."""
import requests, json, re, time, sys, pandas as pd
from concurrent.futures import ThreadPoolExecutor
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"}
RX={"TCS":r"tata consult","Infosys":r"infosys","HCL":r"\bhcl\b","Wipro":r"wipro","TechMahindra":r"tech ?mahindra","LTIMindtree":r"mindtree|larsen.*infotech|\blti\b","Cognizant":r"cognizant","Accenture":r"accenture"}
def get(url):
    for i in range(6):
        try:
            r=requests.get(url,headers=UA,timeout=90)
            if r.status_code==429: time.sleep(int(r.headers.get("Retry-After",10))); continue
            r.raise_for_status(); return r.json()
        except Exception as e: time.sleep(5)
    return {}
def month(ym):
    y,m=ym; nm=(y+(m==12), m%12+1)
    url=f"https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages?updatedFrom={y}-{m:02d}-01T00:00:00&updatedTo={nm[0]}-{nm[1]:02d}-01T00:00:00&stages=award&limit=100"
    out=[]; n=0
    while url:
        time.sleep(3); d=get(url); rel=d.get("releases",[]); n+=len(rel)
        for x in rel:
            sup=[p.get("name","") for p in x.get("parties",[]) if "supplier" in p.get("roles",[])]
            low=" | ".join(sup).lower()
            hit=[f for f,rx in RX.items() if re.search(rx,low)]
            if not hit: continue
            buyer=x.get("buyer",{}).get("name")
            aw=x.get("awards",[]) or [{}]
            for a in aw:
                v=(a.get("value") or {}); 
                out.append(dict(firms=";".join(hit),ocid=x.get("ocid"),release_id=x.get("id"),date=x.get("date"),tag=";".join(x.get("tag",[])),buyer=buyer,
                    title=(x.get("tender",{}) or {}).get("title"),award_title=a.get("title"),award_date=a.get("date"),value=v.get("amount"),currency=v.get("currency"),
                    n_suppliers=len(sup),suppliers="; ".join(sup)[:400],
                    contract_start=(a.get("contractPeriod") or {}).get("startDate"),contract_end=(a.get("contractPeriod") or {}).get("endDate"),
                    description=((x.get("tender",{}) or {}).get("description") or "")[:500],
                    ocds_release_url="https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages/"+str(x.get("id",""))))
        url=(d.get("links") or {}).get("next")
    print(ym,n,len(out),flush=True); return out
# Full 2021-2026 scan is rate-limited (HTTP 429, Retry-After 120s); run a SAMPLE of months sequentially.
months=[tuple(map(int,a.split("-"))) for a in sys.argv[1:]] or [(2024,10)]
res=[month(m) for m in months]
df=pd.DataFrame([r for o in res for r in o]); df.to_csv("ukfts_award_releases_firms.csv",index=False); print(len(df))
