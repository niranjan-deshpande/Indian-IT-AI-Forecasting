import json,csv
B='/Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/benchmarks/data/'
H='model,provider,release_date,score,score_kind,n_items,eval_date,source_url,notes'.split(',')
# ---- EVA
o=json.load(open(B+'eva_bench/raw/leaderboard_models.json'))
# id: (provider, release_date, eval_date, relnote)
meta={
'scribe-realtime-gemini-3-flash-eleven-conversational-v3':('ElevenLabs (cascade; LLM Gemini 3 Flash)','','2026-05','release date blank: LLM release not verified'),
'gpt-realtime':('OpenAI (S2S)','2025-08-28','2026-05',''),
'gpt-realtime-1-5':('OpenAI (S2S)','','2026-05','v1.5 released Feb 2026 per press; exact day not found'),
'gpt-realtime-2':('OpenAI (S2S)','2026-05-07','',''),
'gpt-realtime-mini':('OpenAI (S2S)','2025-10-06','2026-05',''),
'gemini-3-1-flash-live':('Google (S2S)','2026-03-26','2026-05',''),
'scribe-realtime-claude-haiku-4-5-eleven-flash-v2':('ElevenLabs (cascade; LLM Claude Haiku 4.5)','2025-10-15','2026-05','release date is Claude Haiku 4.5 LLM'),
'scribe-realtime-gpt-5-4-eleven-flash-v2':('ElevenLabs (cascade; LLM GPT-5.4)','2026-03-05','2026-05','release date is GPT-5.4 LLM'),
'grok-voice-think-fast-1-0':('xAI (S2S)','','2026-06-10','eval date = commit adding grok results; release date not found'),
'flux-general-multi-gpt-5-4-sonic-3-5':('Deepgram Flux STT + OpenAI GPT-5.4 + Cartesia Sonic 3.5 (cascade)','2026-03-05','','release date is GPT-5.4 LLM; eval date between 2026-06 and 2026-08 (not pinned)'),
'ink-2-haiku-4-5-sonic-3-5':('Cartesia Ink 2 + Claude Haiku 4.5 + Sonic 3.5 (cascade)','2025-10-15','','release date is Haiku 4.5 LLM; eval date not pinned'),
'nova-3-gpt-5-4-mini-aura-2':('Deepgram Nova 3 + GPT-5.4 mini + Aura 2 (cascade)','2026-03-17','','release date is GPT-5.4 mini LLM; eval date not pinned'),
'parakeet-1-1b-ctc-en-us-gemma-4-26b-kokoro':('NVIDIA Parakeet + Google Gemma-4-26B + Kokoro (self-hosted cascade)','2026-04-02','','release date approx (sources disagree 03-31 to 04-02); eval date not pinned'),
'universal-3-5-pro-gpt-5-4-sonic-3-5':('AssemblyAI Universal 3.5 Pro + GPT-5.4 + Sonic 3.5 (cascade)','2026-03-05','2026-06-24','release date is GPT-5.4 LLM; eval date = commit adding AssemblyAI'),
'gpt-realtime-2-1':('OpenAI (S2S)','','2026-08-12','release date not found'),
'gpt-realtime-2-1-mini':('OpenAI (S2S)','','2026-08-12','release date not found'),
'gemini-3-5-flash-lite-live-preview':('Google (S2S)','','2026-09-14','listed on leaderboard as "Gemini 3.8 Live"; release date not found'),
'gemini-live-3-5-high':('Google (S2S)','','2026-09-15','leaderboard name "Gemini 3.8 Live Extended Thinking (High)"; release date not found'),
'gemini-live-3-5-minimal':('Google (S2S)','','2026-09-15','leaderboard name "Gemini 3.8 Live Extended Thinking (Minimal)"; release date not found'),
'grok-voice-3-0':('xAI (S2S)','','2026-10-14','eval date approx = commit adding grok results (may cover 2.0 and 3.0); release date not found'),
'grok-voice-think-fast-2-0':('xAI (S2S)','','2026-10-14','eval date approx = commit adding grok results; release date not found'),
'cartesia-managed-agents-gpt-5-5':('Cartesia Managed Agents (cascade; LLM GPT-5.5)','','2026-10-27','release date not found'),
}
rows=[]
src='https://servicenow.github.io/eva/#results (data embedded in github.com/ServiceNow/eva docs/assets/index-BNJMtYsi.js)'
for m in o:
    c=m['clean']
    if not c or 'EVA-A_pass' not in c: continue
    p=meta.get(m['id']); 
    if not p: print('nometa',m['id']); continue
    sc=c['EVA-A_pass']['pooled']; tc=c['task_completion']['pooled']['point']
    rows.append([m['name'],p[0],p[1],round(sc['point'],4),'EVA-A pass rate (pass@1 style mean over trials; all 3 accuracy metrics must pass), pooled over 213 scenarios, clean audio',213,p[2],src,
      f"task_completion (DB-state hash only)={tc:.3f}; 95% CI {sc['ci_lower']:.3f}-{sc['ci_upper']:.3f}; each row is a whole voice system (pipeline) not a single LLM; "+p[3]])
rows.sort(key=lambda r:(r[7] or '9999',r[3]))
with open(B+'eva_bench/scores.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(H); w.writerows(rows)
print(len(rows))
# ---- CRM
crm=[('o1','OpenAI','2024-12-05',47.5,49.5),('gpt-4o','OpenAI','2024-05-13',26.7,29.2),('gpt-4o-mini','OpenAI','2024-07-18',21.3,18.6),
('gemini-2.5-pro','Google','2025-03-25',54.1,58.3),('gemini-2.5-flash','Google','2025-04-17',41.9,46.7),('gemini-2.0-flash','Google','2025-02-05',33.1,36.5),
('llama4-maverick','Meta','2025-04-05',32.6,37.5),('llama3.1-405b','Meta','2024-07-23',28.7,26.5),('llama3.1-70b','Meta','2024-07-23',25.2,24.9)]
mt={'o1':(32.5,30.4),'gpt-4o':(19.7,18.3),'gpt-4o-mini':(19.3,15.8),'gemini-2.5-pro':(35.1,30.0),'gemini-2.5-flash':(30.1,23.4),'gemini-2.0-flash':(26.9,23.4),'llama4-maverick':(23.7,14.9),'llama3.1-405b':(21.0,20.0),'llama3.1-70b':(16.3,15.1)}
rows=[]
for n,pr,rd,b,c in crm:
    rows.append([n,pr,rd,round((b+c)/200,4),'Single-turn task completion, mean of B2B and B2C "All" (each = mean of 4 skill averages), 19 task types; ReAct agent',3800,'2025-05',
     'https://arxiv.org/abs/2505.18878 (Table 2)',f"B2B {b}, B2C {c}; multi-turn B2B/B2C All = {mt[n][0]}/{mt[n][1]}; release date: Gemini 2.5 models are preview dates; eval date approx = paper submission 2025-05-24"])
with open(B+'crmarena_pro/scores.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(H); w.writerows(rows)
# ---- SOP
txt=open(B+'sopbench/raw/README.md').read().split('\n')
rel={'o4-mini-high':'2025-04-16','GPT-5':'2025-08-07','GPT-5-mini':'2025-08-07','Gemini-2.5-Flash':'2025-04-17','Gemini-2.5-Pro':'2025-03-25','GPT-4.1':'2025-04-14','GPT-4o':'2024-05-13','Claude-3-7-Sonnet':'2025-02-24','GPT-4.1-mini':'2025-04-14','GPT-4o-mini':'2024-07-18','Claude-3-5-Sonnet':'2024-10-22','Gemini-2.0-Flash':'2025-02-05','Qwen3.5-4B':'2026-03-02','Deepseek-R1':'2025-01-20','Gemma-4-E4B-it':'2026-04-02','Qwen3.5-2B':'2026-03-02','Gemma-4-E2B-it':'2026-04-02','Llama3.1-70B-Instruct':'2024-07-23','Qwen2.5-32B-Instruct':'2024-09-19','Qwen2.5-72B-Instruct':'2024-09-19','Qwen2.5-14B-Instruct':'2024-09-19','Llama3.1-8B-Instruct':'2024-07-23','Qwen2.5-7B-Instruct':'2024-09-19'}
prov=lambda n:'OpenAI' if n.startswith(('o4','GPT')) else 'Google' if n.startswith(('Gemini','Gemma')) else 'Anthropic' if n.startswith('Claude') else 'Alibaba' if n.startswith('Qwen') else 'Meta' if n.startswith('Llama') else 'DeepSeek'
rows=[]
for l in txt:
    if l.startswith('| **') or not l.startswith('|'): continue
    c=[x.strip() for x in l.strip('|').split('|')]
    if len(c)!=9 or not c[1].replace('.','').isdigit(): continue
    m=c[0]; name,mode=m.split(' (',1); mode=mode.rstrip(')')
    n=name
    note=f"harness {mode} as listed in README; domains bank/dmv/healthcare/market/university/library/hotel = {'/'.join(c[1:8])}; one setting per model in README table; eval date unknown (README last commit 2026-09-13)"
    if n in('Gemini-2.5-Flash','Gemini-2.5-Pro'): note+='; release date is the preview (Gemini 2.5 Flash preview-04-17 / Pro preview-03-25)'
    if 'Qwen3.5' in n or 'Gemma-4' in n: note+='; release date approximate from comparison sites, unverified'
    rows.append([n+(' thinking' if 'thinking' in mode else ''),prov(n),rel[n],round(float(c[8])/100,4),'Overall pass rate over all 830 tasks (action performed iff SOP allows), pass@1',830,'',
     'https://github.com/Leezekun/SOPBench (README results table)',note])
rows.sort(key=lambda r:r[2])
with open(B+'sopbench/scores.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(H); w.writerows(rows)
print(len(rows))
