import json,random
R='/Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/benchmarks/data/sopbench/'
doms=['bank','dmv','healthcare','hotel','library','online_market','university']
T={};
for d in doms:
    x=json.load(open(R+f'raw/{d}_tasks.json'))
    for act,v in x.items():
        for i,t in enumerate(v): T[f'{d}:{act}:{i}']=(d,act,i,t)
ids=sorted(T); print(len(ids))
S=random.Random(2026).sample(ids,24)
def flat(c,out):
    if isinstance(c,dict): return
    if isinstance(c,list):
        if len(c)>=2 and c[0]=='single' and isinstance(c[1],str):
            out.append(c[1]); return
        for e in c: flat(e,out)
    return
def rd(n): return n.replace('internal_','').replace('_',' ')
def trunc(t,n):
    w=t.split(); return t if len(w)<=n else ' '.join(w[:n])+' [truncated]'
desc={'bank':'a retail bank','dmv':'a state DMV (driver licensing and vehicle registration)','healthcare':'a healthcare provider (patient records, appointments, billing)','hotel':'a hotel (bookings, room changes, services)','library':'a library (loans, holds, accounts)','online_market':'an online marketplace (orders, returns, accounts)','university':'a university registrar/administration office'}
out=[]
for k in S:
    d,act,i,t=T[k]
    chk=[]; flat(t['constraints_original'],chk)
    seen=[]; [seen.append(c) for c in chk if c not in seen]
    nodes=[n for n in t['directed_action_graph']['nodes'] if isinstance(n,list)]
    tools=[n[0] for n in nodes]
    gold=[n for n in tools if not n.startswith('internal_')]
    p=[f"Setting: a customer-service request at {desc[d]}. The worker follows the organisation's written standard operating procedure (SOP) and uses its system tools; a customer message arrives and the worker must decide whether the requested action may be carried out under the SOP, and do it or decline it accordingly.",
       f"Requested action: {act.replace('_',' ')}.",
       f"Customer's first message: \"{t['user_prompt']}\"",
       "SOP policy parameters: "+', '.join(f"{a}={b}" for a,b in t['constraint_parameters'].items()),
       "SOP conditions to verify before acting (using lookup tools): "+('; '.join(rd(c) for c in seen) if seen else 'none')+'.',
       "Correct outcome: "+("every condition holds, so the requested action must be performed." if t['action_should_succeed'] else "at least one condition fails, so the action must be declined (with the reason explained) and not performed."),
       "Tools involved in the gold flow: "+', '.join(tools)+'.',
       "Done when every required check was made in the required structure, the final system state is right, and the right decision was given to the customer."]
    text=trunc('\n'.join(p),300)
    out.append({"item_id":"sopbench:"+k,"benchmark":"sopbench","text":text,"meta":{"domain":d,"target_action":act,"action_should_succeed":t['action_should_succeed'],"gold_tool_calls":len(tools),"n_sop_checks":len(seen),"source_file":f"data/{d}_tasks.json (Leezekun/SOPBench)"}})
with open(R+'items.jsonl','w') as fh:
    for o in out: fh.write(json.dumps(o,ensure_ascii=False)+'\n')
import collections
print(collections.Counter(o['meta']['domain'] for o in out),max(len(o['text'].split()) for o in out))
print(out[0]['text']);print(out[7]['text'])
