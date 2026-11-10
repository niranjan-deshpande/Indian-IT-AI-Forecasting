import json,random,re,collections
R='/Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/benchmarks/data/crmarena_pro/'
CONF={'confidential_company_knowledge','private_customer_information','internal_operation_data'}
P={}
for org in ['b2b','b2c']:
    for e in json.load(open(R+f'raw/tasks_{org}.json')):
        if e['task'] in CONF: continue
        P[f"{org}:{e['idx']}"]=(org,e)
ids=sorted(P); print(len(ids))
S=random.Random(2026).sample(ids,24)
def norm(t): return re.sub(r'[ \t]+',' ',re.sub(r'\n\s*\n+','\n',t)).strip()
def trunc(t,n):
    w=t.split(); return t if len(w)<=n else ' '.join(w[:n])+' [truncated]'
out=[]
for k in S:
    org,e=P[k]
    setting={'b2b':'a B2B (business-to-business) company','b2c':'a B2C (business-to-consumer) company'}[org]
    head=f"Setting: the worker is an employee of {setting} using its Salesforce CRM (cases, leads, opportunities, quotes, knowledge articles, call transcripts, accounts), querying the data with SOQL/SOSL searches and then returning a final answer. Task type: {e['task'].replace('_',' ')}."
    req=norm(e['metadata'].get('required',''))
    q=norm(e['query'])
    body=f"Request: {q}"
    if req: body+="\nGuidance supplied with the request: "+req
    foot="Done when the returned answer matches the correct answer ("+("exact id/value" if e['reward_metric']=='exact_match' else "free-text answer judged by word overlap")+")."
    text=trunc(head+"\n"+trunc(body,220)+"\n"+foot,300)
    out.append({"item_id":"crmarena_pro:"+k,"benchmark":"crmarena_pro","text":text,"meta":{"org":org,"task_type":e['task'],"reward_metric":e['reward_metric'],"native_idx":e['idx'],"gold_answer":e['answer'],"source_file":f"tasks_{org}.json (HF Salesforce/CRMArenaPro)"}})
with open(R+'items.jsonl','w') as fh:
    for o in out: fh.write(json.dumps(o,ensure_ascii=False)+'\n')
print(collections.Counter(o['meta']['org'] for o in out), max(len(o['text'].split()) for o in out)); print(out[0]['text'])
