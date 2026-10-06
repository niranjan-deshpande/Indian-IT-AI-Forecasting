import json,re,os,requests,time,sys
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
d=json.load(open(sys.argv[1])); outdir=sys.argv[2]; os.makedirs(outdir,exist_ok=True)
s=requests.Session(); s.headers.update({'User-Agent':UA}); s.get('https://www.nseindia.com/',timeout=30)
resdays=set(x['sort_date'][:10] for x in d if x['desc'].startswith('Financial Result'))
idx=[]
for x in sorted(d,key=lambda x:x['sort_date']):
    day=x['sort_date'][:10]
    t=x['desc'].lower()
    keep = t.startswith('financial result') or 'investor presentation' in t or (day in resdays and ('press release' in t or 'outcome' in t or 'update' in t))
    if not keep: continue
    u=x['attchmntFile']; fn=day+'_'+u.split('/')[-1]
    idx.append((fn,u,x['desc'],x['attchmntText'][:200].replace('\t',' ').replace('\n',' ')))
    if os.path.exists(os.path.join(outdir,fn)): continue
    for k in range(3):
        try:
            r=s.get(u,timeout=60,headers={'Referer':'https://www.nseindia.com/'})
            if r.status_code==200 and len(r.content)>1000:
                open(os.path.join(outdir,fn),'wb').write(r.content); break
        except Exception as e: pass
        time.sleep(2)
    print(fn,r.status_code,len(r.content),file=sys.stderr); time.sleep(0.5)
with open(os.path.join(outdir,'index.tsv'),'w') as o:
    for row in idx: o.write('\t'.join(row)+'\n')
