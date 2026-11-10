import json,random,re
R='/Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/benchmarks/data/eva_bench/'
D={};ids=[]
for f in ['airline','itsm','medical_hr']:
    for x in json.load(open(R+f'raw/{f}_dataset.json')):
        k=f+'/'+x['id']; ids.append(k); D[k]=(f,x)
ids=sorted(ids)
sample=random.Random(2026).sample(ids,24)
dom={'airline':'a phone call to an airline customer-service line (reservations: rebooking, cancellations, compensation, seats, baggage)',
 'itsm':'a phone call to an enterprise IT service desk (employee verification, access, hardware, account and incident requests)',
 'medical_hr':'a phone call to a healthcare organisation HR service-delivery line (provider credentialing, licence, privileges, leave, payroll and HR requests)'}
def sub(t,x):
    en=x.get('culture_overrides',{}).get('en',{})
    t=t.replace('<FIRST_NAME_ROMANIZED>',en.get('first_name','')).replace('<LAST_NAME_ROMANIZED>',en.get('last_name',''))
    t=t.replace('<FIRST_NAME>',en.get('first_name','')).replace('<LAST_NAME>',en.get('last_name',''))
    t=re.sub(r'<LOC:([^>]*)>',r'\1',t)
    return t
def trunc(t,n):
    w=t.split()
    return t if len(w)<=n else ' '.join(w[:n])+' [truncated]'
out=[]
for k in sample:
    f,x=D[k]
    ug=x['user_goal']; dt=ug['decision_tree']; sc=x.get('scenario_context',{})
    tr=x['ground_truth']['expected_trace']['trace']
    calls=[e['tool_name'] for e in tr if e['event_type']=='tool_call']
    cond=[]
    for c in calls: cond.append(c)
    parts=[f"Setting: {dom[f]}. The worker is the service agent answering the call, with access to the organisation's policy and database tools; they must verify the caller's identity first."]
    if sc.get('premise'): parts.append("Situation: "+sub(sc['premise'],x))
    parts.append("Caller's goal: "+sub(ug['high_level_user_goal'],x))
    parts.append("Required outcomes: "+' '.join(f"({i+1}) {sub(c,x)}" for i,c in enumerate(dt['must_have_criteria'])))
    cat=sc.get('category')
    if cat: parts.append(f"Scenario type: {cat}.")
    parts.append(f"Gold tool-call sequence ({len(calls)} calls): "+', '.join(calls)+'.')
    parts.append("Done when the database ends in the expected state (the right records created or changed, nothing disallowed done) and the caller is told the correct information.")
    # budget: trim parts[...] progressively
    text='\n'.join(parts)
    w=len(text.split())
    if w>300:
        # trim required outcomes first
        parts[3]=trunc(parts[3],90); text='\n'.join(parts)
    text=trunc(text,300)
    nw=len(set(calls))
    out.append({"item_id":"eva_bench:"+k.replace('/',':'),"benchmark":"eva_bench","text":text,
      "meta":{"domain":f,"native_id":x['id'],"category":cat,"gold_tool_calls":len(calls),"n_intents":len(sc.get('intents',[])) or None,"source_file":f"data/{f}_dataset.json (ServiceNow/eva)"}})
with open(R+'items.jsonl','w') as fh:
    for o in out: fh.write(json.dumps(o,ensure_ascii=False)+'\n')
print(len(out)); 
import collections; print(collections.Counter(o['meta']['domain'] for o in out)); print(max(len(o['text'].split()) for o in out))
print(out[0]['text']); print(out[5]['text'])
