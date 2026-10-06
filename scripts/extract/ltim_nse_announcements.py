import requests,json,time,sys,datetime as dt
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
sym=sys.argv[1]; start=dt.date.fromisoformat(sys.argv[2]); end=dt.date.fromisoformat(sys.argv[3]); out=sys.argv[4]
s=requests.Session(); s.headers.update({'User-Agent':UA,'Accept-Language':'en-US,en;q=0.9'})
s.get('https://www.nseindia.com/',timeout=30)
allr=[]
d=start
while d<end:
    e=min(d+dt.timedelta(days=90),end)
    url=f"https://www.nseindia.com/api/corporate-announcements?index=equities&symbol={sym}&from_date={d:%d-%m-%Y}&to_date={e:%d-%m-%Y}"
    for k in range(3):
        try:
            r=s.get(url,headers={'Referer':'https://www.nseindia.com/companies-listing/corporate-filings-announcements','Accept':'application/json'},timeout=30)
            js=r.json(); break
        except Exception as ex:
            time.sleep(2); s.get('https://www.nseindia.com/',timeout=30); js=[]
    print(d,e,len(js),file=sys.stderr)
    allr+=js; d=e+dt.timedelta(days=1); time.sleep(0.7)
json.dump(allr,open(out,'w'),indent=0)
