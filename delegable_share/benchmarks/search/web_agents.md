# Browser / web-agent benchmarks: catalog for time-horizon estimation

Researcher scope: browser and web agents, especially enterprise web apps. Searched 2026-11-09 with WebSearch/WebFetch. Every number below came from a page I fetched (listed under "Sources checked") unless it is marked **unverified**. Leaderboard aggregators (benchmarklist.com, steel.dev, benchlm.ai) are secondary sources, and I flag them as such.

## Bottom line

| Benchmark | Relevance to IT/BPO | Per-item human times? | Models over time? | Verdict |
|---|---|---|---|---|
| WebArena (+ Verified / Lite) | Medium (admin back-ends: e-commerce admin, GitLab, CMS) | **Yes, extractable** from human Playwright traces for 179 tasks (one per template); mean 110 s | Yes, 2023–2026, 50+ entries | **INCLUDE** |
| WorkArena L1 (ServiceNow) | **High** (ITSM: incidents, change requests, catalog, KB) | No; **estimable** from per-task oracle action counts (1–47 actions) | Yes, 16 models from GPT-4o-mini to GPT-5 / Gemini-3-flash | **CANDIDATE (top priority)** |
| WorkArena++ L2/L3 (ServiceNow) | **High** (multi-step ITSM / HR / procurement tickets) | **Recorded but unpublished** (15 humans × 98 instances) | Yes (L2: 14 models; L3: 8) | **CANDIDATE (top priority, ask authors)** |
| StarShell enterprise suite (ServiceNow 330 + GitLab 192 + ERPNext 207) | **High** (ITSM + ERP/finance back office) | No | 2026 frontier only (one generation) | CANDIDATE |
| ERPBench (Accenture) | **High** (ERP data entry / record creation) | Tier-level means from 3 annotators | No (one frontier model) | CANDIDATE (weak) |
| SCUBA (Salesforce CRM) | **High** (CRM admin / sales / service agent) | No; human demo step counts exist | One generation (mid-2025 models) | CANDIDATE |
| Online-Mind2Web | Low–medium (consumer transactions on live sites) | No times; **per-item human step counts** (reference_length) | Yes, Jan 2025 – Mar 2026 | CANDIDATE |
| VisualWebArena | Low–medium | **Yes, extractable** from 233 human Playwright traces | Sparse, mostly 2024 | CANDIDATE (low) |
| WebChoreArena | Medium (tedious data collation / counting in admin UIs) | No | Some (GPT-4o → GPT-5) | CANDIDATE (low) |
| ST-WebAgentBench | Medium (CRM + admin with policy compliance) | No | Few, old agents | CANDIDATE as an acceptance adjustment, not a horizon source |
| Mind2Web 2 | Low (research/analyst search) | 30-task subset only, 8–44 min | One snapshot (mid-2025) | EXCLUDE |
| REAL (AGI Inc) | Low (consumer clones) | No | One snapshot (Apr 2025) | EXCLUDE |
| WebVoyager / Emergence-WebVoyager | Low (consumer lookups) | No | Yes but saturated, self-reported | EXCLUDE |
| AssistantBench, BrowseComp, BearCubs | Low (search puzzles) | AssistantBench no; BearCubs aggregate only | Yes | EXCLUDE |

**Most important finding:** No enterprise web benchmark publishes per-item human completion times. The only per-item human time source in this area is the raw human Playwright traces released for WebArena (179 tasks) and VisualWebArena (233 tasks). METR mined the WebArena traces for its July 2025 cross-domain post (5 s – 9 min range). The closest enterprise benchmark, WorkArena++ (ServiceNow), *recorded* human time-to-resolution for 98 task instances but never published it, so one request to the authors could unlock the most IT-relevant benchmark. Failing that, WorkArena L1's per-task oracle action counts and Online-Mind2Web's per-task human step counts can be converted to time with a seconds-per-action rate calibrated on the WebArena traces.

A second point: web-agent scores depend heavily on the scaffold (WebArena ranges from 14% to 74% across agent systems, many built on non-frontier models). For a ln H vs. release-date trend, use one fixed harness: the BrowserGym "GenericAgent" rows (WorkArena, WebArena) or HAL's fixed scaffolds (Online-Mind2Web). Don't use the best-system leaderboards.

---

## 1. WebArena (and WebArena-Verified, WebArena-Lite)

- **Paper / URL:** Zhou et al., "WebArena: A Realistic Web Environment for Building Autonomous Agents," arXiv 2307.13854 (ICLR 2024); https://webarena.dev, https://github.com/web-arena-x/webarena. WebArena-Verified: https://github.com/ServiceNow/webarena-verified (NeurIPS 2025 SEA workshop).
- **Release date:** July 2023. WebArena-Verified was presented Dec 2025 (PyPI Jan 2026, Docker Feb 2026). WebArena-Lite (165 tasks) is part of VisualAgentBench (2024).
- **Maintainer:** CMU (web-arena-x). WebArena-Verified is maintained by ServiceNow.
- **What one item looks like:** A natural-language intent run against self-hosted clones of an e-commerce store, a Magento **shopping admin** back end, a Reddit-style forum, GitLab, a CMS, and a map. Example of the admin/back-office kind: "Update the product 'X' price to $Y and mark it out of stock," or "How many orders were cancelled in March 2023?" **812 tasks** from about 241 templates (sources differ on the template count: 170, 187 or 241). WebArena-Verified keeps all 812 with audited answers and a 258-task Hard subset (the paper says 137; the repo now says 258).
- **Domain tag:** computer_use (web, DOM-based)
- **Resembles:** e-commerce back-office admin (order and product maintenance, sales reporting), content moderation, GitLab repo and issue administration (app maintenance). It does not cover ITSM directly.
- **Human times:** **Per-item, extractable.** The authors released human Playwright traces (`<task_id>.zip`) for **179 tasks**, one per template (Google Drive link in `resources/README.md`). Playwright traces carry per-action timestamps, so you can compute wall-clock time per item. Templates share structure, so the times can be assigned to all 812 instances by template. The paper reports a **mean of 110 s per task** (5 CS grad students; 78.24% success). METR extracted the trace times and reports a **range of about 5 s to 9 min**. The median is not published: it needs extraction, and I expect it to be around 1–2 min.
- **Model results over time:** Very rich, 2023–2026. From the WebArena tracker via steel.dev (secondary): GPT-4-0613 14.9% (2023); GPT-4o 13.05%; OpenAI Operator/CUA 58.1% (Jan 2025, self-reported); IBM CUGA 61.7%; Kimi K2.5 58.9%; OpAgent 71.6% (Jan 2026); WebTactix (DeepSeek v3.2) 74.3% (top, 2026). BrowserGym fixed-harness GenericAgent rows: GPT-4o-mini 17.4%, Llama-3.1-70b 18.4%, GPT-4o 31.4%, Claude-3.5-Sonnet 36.2%, Claude-3.7-Sonnet 44.6%. **WebArena-Verified** (frontier labs now report this one): GPT-5.2 65.4%, GPT-5.4 67.3% (OpenAI, Mar 2026, self-reported). Aggregators also list Qwen3.8-27B 64.8% and Muse Spark 1.1 69% (**unverified**). BenchLM lists Claude Mythos Preview 68.7%, GPT-5.4 Pro 65.8% and Claude Opus 4.6 64.5% on original WebArena (**unverified**, aggregator snapshot May 2026). Human ceiling is 78.24%, so the benchmark is close to saturation.
- **Item-level results public?** Yes, scattered. The original repo has execution traces with per-task pass/fail (`merge_log.txt`) for GPT-3.5/4. Many 2025–26 systems publish full trajectories (OpAgent, ColorBrowserAgent, IBM CUGA, Claude Code + GBOX). The Zeno results browser has per-task results. BrowserGym/AgentLab runs produce per-task results. METR's July 2025 post says it had only overall scores, but per-task data does exist for many systems.
- **Grading:** Programmatic. Exact or fuzzy answer match plus state checks on the back-end DB/URL; the original also used some LLM-judge fuzzy matching. WebArena-Verified replaces substring and LLM-judge matching with deterministic type-aware comparison and offline trace replay.
- **Time horizon already computed?** **Yes, by METR** ("How Does Time Horizon Vary Across Domains?", 14 Jul 2025). It used human times from the public traces but only overall scores, so it used the fallback method with no β fit. Finding: frontier horizon on computer use (WebArena, OSWorld) was about 40–100× shorter than the software/reasoning cluster as of early 2025, with a similar doubling rate. I could not find a separate "Kwa & Cheng" paper beyond this METR post. I found no other WebArena horizon estimates (Epoch only mirrors METR's main suite).
- **Verdict: INCLUDE.** It is the best-documented web benchmark with recoverable per-item human times and the longest model time series. Caveats: tasks are short (seconds to minutes), so it pins the low end of the curve. Scores are scaffold-dominated, so use a fixed harness. Contamination is growing. Going forward, use WebArena-Verified for new models; the human traces map onto the same task IDs.
- **Sources checked:** https://github.com/web-arena-x/webarena ; https://github.com/web-arena-x/webarena/blob/main/resources/README.md ; https://arxiv.org/pdf/2307.13854 ; https://metr.org/blog/2025-07-14-how-does-time-horizon-vary-across-domains ; https://raw.githubusercontent.com/ServiceNow/webarena-verified/main/README.md ; https://neurips.cc/virtual/2025/124576 ; https://leaderboard.steel.dev/leaderboards/webarena.md ; https://benchmarklist.com/benchmarks/webarena/ ; https://openai.com/index/introducing-gpt-5-4 (via search summary) ; https://benchlm.ai/benchmarks/webarena-verified

## 2. WorkArena (L1, ServiceNow)

- **Paper / URL:** Drouin et al., "WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks?", arXiv 2403.07718 (ICML 2024); https://github.com/ServiceNow/WorkArena ; leaderboard at https://huggingface.co/spaces/ServiceNow/browsergym-leaderboard
- **Release date:** Mar 2024 (v5 Jul 2024).
- **Maintainer:** ServiceNow Research (with Mila).
- **What one item looks like:** One atomic ServiceNow action from an explicit goal on a real ServiceNow instance. Example: FilterIncidentList ("filter the incident list to show incidents where priority = 1 and assignment group = X"). Other tasks: CreateIncident, CreateChangeRequest, CreateProblem, CreateUser, CreateHardwareAsset; order an item from the service catalog (laptop, iPad); search the knowledge base for an answer; read a value from a dashboard chart; navigate the "All" menu; impersonate a user. **33 tasks, 19,912 instances.**
- **Domain tag:** computer_use (web, enterprise)
- **Resembles:** **IT service desk / ITSM L1 agent work**: logging incidents, change requests and problems, user provisioning, asset records, catalog fulfilment, KB lookup, queue filtering and sorting, simple reporting. This is the closest match in the web area to the Indian IT-services ITSM workforce.
- **Human times:** **None published.** I could not verify the "human ~78%" figure that steel.dev lists for WorkArena-L1; it looks like a conflation with WebArena's 78.24%. **Estimable:** the paper gives per-task **oracle Playwright action counts**: dashboards 1–2, KB search 4, menus 3–7, catalog 4–9, sort 7.4–8.3, filter 12.7–19.9, forms 10–47.1. Multiply by a seconds-per-action rate calibrated on the WebArena human traces, or run a small timing study: 33 templates, free ServiceNow developer instance, about 1 day of annotator time.
- **Model results over time:** BrowserGym leaderboard, fixed GenericAgent harness, via the benchmarklist mirror (secondary; imported Aug 2026): GPT-4o-mini 27.0, Llama-3.1-70b 27.9, GPT-5-nano 40.6, Llama-3.1-405b 43.3, GPT-4o 45.5, o3-mini 48.2, GPT-oss-120b 50.9, Claude-3.5-Sonnet 56.4, o1-mini 56.7, GPT-5-mini 60.6, Claude-4-Sonnet 63.3, **GPT-5 79.1**, IpaziaHPA-Gemini-3-flash 90.3 (custom agent). The original paper had GPT-3.5 6.1 and GPT-4o 42.7. There are no 2026 Claude/Gemini-Pro GenericAgent rows; the StarShell paper (section 4) gives 2026 frontier numbers on 330 WorkArena-derived tasks.
- **Item-level results public?** Per-task breakdowns in the papers. The BrowserGym leaderboard stores per-model JSON (I could not render the HF Space to confirm per-task granularity). AgentLab produces per-task traces for anyone rerunning.
- **Grading:** Programmatic validators: DB queries for created records and orders, client-side checks of list state, answer matching for KB and dashboards.
- **Time horizon already computed?** No.
- **Verdict: CANDIDATE (top priority).** It has the best job relevance plus a good model time series. Gap: no human times. Close it by (a) converting oracle action counts to time, calibrated against WebArena's human traces, or (b) running a 33-template human timing study. Tasks are short (likely 20 s – 3 min), so like WebArena it covers only the short end.
- **Sources checked:** https://arxiv.org/html/2403.07718 ; https://github.com/ServiceNow/WorkArena ; https://benchmarklist.com/benchmarks/workarena_l1/ ; https://huggingface.co/spaces/ServiceNow/browsergym-leaderboard (did not render) ; https://www.servicenow.com/blogs/2024/introducing-workarena-benchmark

## 3. WorkArena++ (L2 / L3, ServiceNow)

- **Paper / URL:** Boisvert, Thakkar, Gasse et al., "WorkArena++: Towards Compositional Planning and Reasoning-based Common Knowledge Work Tasks," arXiv 2407.05291 (NeurIPS 2024 D&B); same repo as WorkArena.
- **Release date:** Jul 2024 (v2 Feb 2025).
- **Maintainer:** ServiceNow Research.
- **What one item looks like:** A realistic multi-step workflow composed from L1 atoms. L2 gives explicit step-by-step instructions in chat. L3 gives only a **ticket assigned to the agent**, as a human employee would receive it. Examples: onboard a new user (create the user, order their hardware from the catalog, assign assets); find the agent with the fewest assigned incidents and assign them the new problem; work out a budget allocation from a dashboard and place orders. **682 tasks** (341 workflows × 2 levels) across 5 skills: planning, information retrieval, data-driven decisions, memorization, contextual understanding.
- **Domain tag:** computer_use (web, enterprise)
- **Resembles:** **IT service desk L1/L2 work end-to-end**: ticket triage and assignment, onboarding and offboarding, procurement through the catalog, expense and budget checks, SLA-style data lookups. L3's ticket format is the closest web benchmark to "process a service-desk ticket."
- **Human times:** **Recorded, not published.** 15 volunteers (mostly ServiceNow staff and Montreal students, 15 min training) solved up to 7 tasks each over 98 instances (49 × L2/L3), and "time to resolution" was recorded. Human success was 93.9%. The paper reports no time figures, and the repo contains `make_human_eval_curriculum.py` but no timing data. **Ask the authors** (Léo Boisvert, Alexandre Drouin, Maxime Gasse at ServiceNow Research) for the per-instance times. Otherwise, estimate from the oracle traces, which the paper says can be generated for every task.
- **Model results over time:** Paper (2024): GPT-4o 3.0% L2 and 0% L3; everything else 0. BrowserGym leaderboard (benchmarklist mirror, secondary): **L2**: GPT-4o-mini 1.3, Llama-3.1-70b 2.1, GPT-oss-20b 2.6, GPT-5-nano 3.4, Llama-405b 7.2, GPT-4o 8.5, GPT-oss-120b 11.5, o1-mini 14.9, Claude-3.5-Sonnet 39.1, Claude-4-Sonnet 40.4, GPT-5-mini 47.7, **GPT-5 69.4**. **L3**: nearly all 0, Claude-3.5-Sonnet 0.4, **GPT-5 11.5**. This is a clear capability ramp, useful for the β slope.
- **Item-level results public?** Per-skill breakdowns are in the paper. Leaderboard JSON is per model. Rerunning with AgentLab gives per-task results.
- **Grading:** Programmatic validators (DB state checks) for every subtask, done by an oracle-backed validator.
- **Time horizon already computed?** No.
- **Verdict: CANDIDATE (top priority).** It is the most job-relevant web benchmark, and the human times already exist. Gap: they are unpublished, the human sample is small (98 instances), and there are no 2026 frontier runs. Close by asking the authors for the timing logs and running current models through AgentLab (needs a gated ServiceNow instance from the HF pool).
- **Sources checked:** https://arxiv.org/abs/2407.05291 ; https://arxiv.org/html/2407.05291v2 (both halves) ; https://benchmarklist.com/benchmarks/workarena_l2/ ; https://benchmarklist.com/benchmarks/workarena_l3/ ; https://github.com/ServiceNow/WorkArena

## 4. StarShell enterprise suite ("Terminal Agents Suffice for Enterprise Automation")

- **Paper / URL:** Bechard, Marquez Ayala, Chen, … Rajeswar, arXiv 2604.00073 (v4 14 Oct 2026; TMLR 10/2026); https://github.com/ServiceNow/StarShell ; HF collection ServiceNow-AI/starshell.
- **Release date:** Apr 2026 (v4 Oct 2026).
- **Maintainer:** ServiceNow.
- **What one item looks like:** The same enterprise task done by a web (Playwright) agent, a terminal (API/bash) agent, or a tool-use (MCP) agent. **729 tasks:** ServiceNow 330 (the 33 WorkArena templates × 10 seeds, re-verified), GitLab 192 (from WebArena), ERPNext 207 (new; ERP records such as invoices and sales orders, with "hard" templates chaining dependent subtasks). Example: order an iPad Pro from the service catalog; create a sales invoice in ERPNext.
- **Domain tag:** computer_use / software (web vs API)
- **Resembles:** ITSM (ServiceNow), **finance & accounting / ERP back office** (ERPNext), app maintenance (GitLab).
- **Human times:** None. Agent wall-clock per ServiceNow task for web agents is 109–153 s across 4 models. The ServiceNow half inherits WorkArena's oracle action counts (section 2).
- **Model results over time:** One generation only (2026). Web-agent success over all 729 tasks: Claude Sonnet 4.6 72.2%, Claude Opus 4.6 79.9%, GPT-5.4 Thinking 73.4%, Gemini 3.1 Pro 68.9%; terminal agents are similar or better and 3–8× cheaper. The ServiceNow per-category web success rate (mean of the 4 models) is useful: catalog 90.6, KB 90.0, impersonation 95.0, list filter 70.0, form creation 67.0, list sort 62.5, navigation 52.5, dashboard 36.2.
- **Item-level results public?** Per-category tables are in the paper. The repo has a trace viewer and says logs are recorded for every run; I could not confirm that per-task result files are published.
- **Grading:** Programmatic state checks against the live platform.
- **Time horizon already computed?** No.
- **Verdict: CANDIDATE.** It gives frontier-2026 points on WorkArena tasks and adds an ERP/finance back-office domain. Gap: no human times and a single model generation. Use it as the 2026 endpoint for a WorkArena-based series, with times from section 2's oracle conversion. It is also a useful caution that web-agent success may understate what an API-connected agent achieves on the same work.
- **Sources checked:** https://arxiv.org/html/2604.00073 (both halves) ; https://github.com/ServiceNow/StarShell

## 5. ERPBench (Accenture)

- **Paper / URL:** Bhagtani, Sridhar, Pouyan, Zhao, Siow, "ERPBench: A State-Grounded Evaluation Paradigm for Computer-Use Agents in Enterprise Software," arXiv 2609.17885 (v2 23 Sep 2026).
- **Release date:** Sep 2026. The benchmark is **not yet released**; the authors say "we intend to release."
- **Maintainer:** Accenture Agentic AI Center of Excellence.
- **What one item looks like:** A pixel-only computer-use agent working in self-hosted **ERPNext**. Tiers: T1 edits one field (e.g., a customer's tax ID); T2 creates a full Customer or Supplier record (6–9 fields); T3 chains documents (Lead → Opportunity → status advance). **30 tasks**, 5 runs each.
- **Domain tag:** computer_use (web, enterprise)
- **Resembles:** **Data entry / master-data maintenance, F&A and sales-ops back office.**
- **Human times:** **Tier-level means from 3 annotators.** Expert #1: T1 41.4 s, T2 85.7 s, T3 99.9 s. Expert #2: 89.1, 150.5, 395.5 s. Novice #3: 42.3, 93.2, 100.7 s. No per-task times are reported, and the timing method is not described.
- **Model results over time:** One frontier point, Claude Sonnet 4.6 (T1/T2/T3 = 94/100/100%), plus open models: Holo3-35B 34/0/3, Qwen3-VL-32B 32/0/3, OpenCUA-32B 23/0/0, UI-TARS-1.5-7B 9/0/0.
- **Item-level results public?** No (not released).
- **Grading:** State-grounded. The DB is read through the Frappe REST API and every target field must match (tolerance 0.01). Partial credit is field-weighted for T2 and by chain depth for T3.
- **Time horizon already computed?** No.
- **Verdict: CANDIDATE (weak).** It has the right domain and real human times, but it is tiny (30 tasks), saturated by the frontier, and has no time series. It is mainly a sanity check that short ERP data-entry tasks (≤ 2 min) are near-solved by 2026 frontier models. Revisit when released.
- **Sources checked:** https://arxiv.org/html/2609.17885v2

## 6. SCUBA (Salesforce Computer Use Benchmark)

- **Paper / URL:** arXiv 2509.26506 (ICLR 2026); https://sfrcua.github.io/SCUBA/
- **Release date:** 30 Sep 2025 (code Oct 2025).
- **Maintainer:** Salesforce AI Research.
- **What one item looks like:** A task in a live **Salesforce sandbox org** for one of three personas: platform admin, sales rep, or service agent. Example (admin): "Add a formula field named 'Days to close' to the Opportunity object, visible only to Marketing User." One example task in the alphaxiv listing takes 31 human steps across 8 pages. **300 tasks from 60 templates**, 3 difficulty levels.
- **Domain tag:** computer_use (web, enterprise)
- **Resembles:** **CRM administration, customer-service agent case handling, sales-ops data maintenance**: core BPO / CX back-office work.
- **Human times:** None. **Human demonstration trajectories exist**: annotators recorded prescribed actions, and the paper's Figure 4 shows average human step counts. Release status of the demos is unclear (the code is on GitHub). Time is estimable as steps × calibrated seconds per step.
- **Model results over time:** One generation (mid-2025). Zero-shot browser-use: GPT-5 51.3%, o3 45.7%, Claude-4-Sonnet 34.7%, Gemini-2.5-Pro 31.0%. Computer-use: Agent-S2.5 + GPT-5 39.0%, Claude-4-Sonnet CU 27.0%, OpenAI CUA 16.0%, UI-TARS-1.5-7B 2.7%, OpenCUA-7B 0.7%. Agent time per task is reported (GPT-5 about 19 min).
- **Item-level results public?** Not confirmed. The project-page leaderboard did not render.
- **Grading:** Rule-based evaluators against org state; binary success plus milestone (partial) scores.
- **Time horizon already computed?** No.
- **Verdict: CANDIDATE.** High job relevance, agent times are long (minutes), and difficulty tiers exist. Gaps: no human times, single generation, and it needs a Salesforce org to rerun. Close by getting the human demo step counts or times from Salesforce, and possibly rerunning newer models.
- **Sources checked:** https://arxiv.org/html/2509.26506v1 ; https://sfrcua.github.io/SCUBA/ ; https://alphaxiv.org/benchmarks/salesforce-ai-research/scuba (search snippet)

## 7. Online-Mind2Web

- **Paper / URL:** Xue et al., "An Illusion of Progress? Assessing the Current State of Web Agents," arXiv 2504.01382 (COLM 2025); https://github.com/OSU-NLP-Group/Online-Mind2Web ; HF dataset osunlp/Online-Mind2Web ; HAL: https://hal.cs.princeton.edu/online_mind2web
- **Release date:** Apr 2025 (v4 Oct 2025).
- **Maintainer:** OSU NLP Group. Independent runs by Princeton HAL.
- **What one item looks like:** A task on a specified live website, e.g. "On united.com, find the cheapest one-way economy flight from X to Y on date Z and add the carry-on option," or a shopping or rental search with filters. **300 tasks, 136 sites.**
- **Domain tag:** computer_use (web, live)
- **Resembles:** Consumer-side transactions such as booking and search-and-filter. It overlaps weakly with customer-service agents executing on a customer's behalf. Little back-office content.
- **Human times:** **No times, but per-item human step counts.** Each task carries `reference_length`, the number of steps a human annotator needed. Buckets: easy ≤5 steps (83 tasks), medium 6–10 (143), hard ≥11 (74). Steps can be converted to time with a calibrated seconds-per-step rate.
- **Model results over time:** HAL (fixed scaffolds, verified): DeepSeek R1 (Jan 2025) 25.3, Gemini 2.0 Flash 29.0, Claude-3.7 Sonnet 38.3, GPT-4.1 36.3, o3 39.0 (SeeAct), Claude Sonnet 4 40.0, GPT-5 Medium 42.3 (Aug 2025). The paper's human-evaluated agents: Claude CU 3.7 and Operator (61.3%), with Operator 83.1% on easy. Vendor self-reports: Gemini 2.5 Computer Use 69.0% (Oct 2025), ChatGPT Atlas agent 70.9%, **GPT-5.4 92.8%** (Mar 2026). Aggregators show Browser Use Cloud at 97% (**unverified**). Vendor numbers use different judges and step budgets, so they are not comparable with HAL's.
- **Item-level results public?** **Yes.** HAL publishes encrypted per-run trace archives (decrypt with hal-decrypt) and a per-task success heatmap. The OSU repo publishes human labels and WebJudge labels per task (`data/evaluation_results`).
- **Grading:** WebJudge LLM-as-judge (about 85% agreement with humans), plus a human-evaluation option.
- **Time horizon already computed?** Not that I found.
- **Verdict: CANDIDATE.** It has per-item difficulty in human steps, per-task results for about 20 model × scaffold combinations over Jan–Aug 2025, and a long vendor series to 2026. Gaps: consumer rather than enterprise tasks; steps need converting to time; live-site drift; judge noise. Useful as a second web curve with medium-length tasks.
- **Sources checked:** https://arxiv.org/abs/2504.01382 ; https://arxiv.org/html/2504.01382v4 ; https://github.com/OSU-NLP-Group/Online-Mind2Web ; https://hal.cs.princeton.edu/online_mind2web ; https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-2-5-Computer-Use-Model-Card.pdf (via search) ; https://openai.com/index/introducing-gpt-5-4 (via search) ; https://leaderboard.steel.dev/leaderboards/online-mind2web.md (search snippet)

## 8. VisualWebArena

- **Paper / URL:** Koh et al., arXiv 2401.13649 (ACL 2024); https://github.com/web-arena-x/visualwebarena
- **Release date:** Jan 2024.
- **Maintainer:** CMU.
- **What one item looks like:** A visually grounded task on Classifieds, Shopping or Reddit clones, e.g. "Find the red bicycle listed in the image and comment on its post asking if it is still available." **910 tasks.**
- **Domain tag:** computer_use
- **Resembles:** Marketplace moderation and listing management; little enterprise content.
- **Human times:** **Per-item, extractable.** Human Playwright traces exist for **233 tasks** (one per template), the same format as WebArena's. Human success is 88.7%. No time statistics are published.
- **Model results over time:** Mostly 2024: GPT-3.5 2.97, Gemini-Pro 6.04, GPT-4 12.75, GPT-4V 16.37, GPT-4o 19.78 (benchmarklist mirror). Scattered later agent papers report higher, but I found no consistent 2025–26 frontier series.
- **Item-level results public?** GPT-4V+SoM traces for all 910 tasks.
- **Grading:** Programmatic, plus some VLM-based evaluators for image-matching tasks.
- **Time horizon already computed?** No.
- **Verdict: CANDIDATE (low).** Human times are recoverable, but job relevance is low and recent model coverage is thin. Its main use is extra per-item web time points for calibrating seconds per action.
- **Sources checked:** https://github.com/web-arena-x/visualwebarena ; https://benchmarklist.com/benchmarks/visualwebarena/ ; https://arxiv.org/html/2401.13649v2 (search snippet)

## 9. WebChoreArena

- **Paper / URL:** Miyai et al., arXiv 2506.01952; https://webchorearena.github.io
- **Release date:** Jun 2025 (v2 Aug 2026).
- **Maintainer:** University of Tokyo (Yamasaki lab).
- **What one item looks like:** A tedious task in the WebArena environments that needs massive memory, calculation or long-term memory. Example: "In the shopping admin, sum the total quantity of all orders containing product X placed in Q1 2023." **532 tasks.**
- **Domain tag:** computer_use
- **Resembles:** **Back-office reconciliation and reporting chores** (counting, aggregating, cross-checking records in admin UIs).
- **Human times:** None. **Estimable:** a timing study is cheap because it reuses WebArena's Docker sites.
- **Model results over time:** GPT-4o 2.6–6.8%, Claude 3.7 Sonnet about 23%, Gemini 2.5 Pro 37.8–44.9% (BrowserGym/AgentOccam harnesses). The v2 abstract mentions GPT-5; I did not get exact numbers.
- **Item-level results public?** Not confirmed.
- **Grading:** Programmatic answer and state checks, as in WebArena.
- **Time horizon already computed?** No.
- **Verdict: CANDIDATE (low).** Relevant "chore" content, but no human times. Run a human timing study on a sample if back-office aggregation tasks need representing.
- **Sources checked:** https://arxiv.org/abs/2506.01952 ; search summaries (emergentmind, steel.dev registry)

## 10. ST-WebAgentBench

- **Paper / URL:** Levy et al. (IBM Research), arXiv 2410.06703 (v4 May 2025; ICLR 2026); https://sites.google.com/view/st-webagentbench/home
- **Release date:** Oct 2024.
- **Maintainer:** IBM Research.
- **What one item looks like:** A WebArena or SuiteCRM task paired with organizational policies. Example: "In SuiteCRM, create contact Alice Johnson, Marketing Director," with the policy "ask the user for permission before clicking Create." **222 tasks, 646 policy instances**, 6 dimensions (consent, scope, strict execution, hierarchy, security, error handling).
- **Domain tag:** computer_use
- **Resembles:** **CRM data entry and admin under SOP/compliance constraints**, which is directly about whether output is *acceptable* and not merely complete.
- **Human times:** None.
- **Model results over time:** Only 3 agents (AWM, WebVoyager agent, WorkArena-Legacy); completion 24.3% on average, CuP (completion under policy) 15.0%. CuP is about 38% lower than raw completion.
- **Item-level results public?** A leaderboard exists on the project site; per-task results are not confirmed.
- **Grading:** Programmatic task success plus policy-violation detectors. Reports CR, CuP and a risk ratio.
- **Time horizon already computed?** No.
- **Verdict: CANDIDATE, but as an *acceptance haircut*, not a horizon source.** The CR-to-CuP ratio speaks directly to "would the output be accepted" in regulated BPO work. It needs runs on current models.
- **Sources checked:** https://arxiv.org/html/2410.06703v4 ; https://iclr.cc/virtual/2026/poster/10009904

## 11. Mind2Web 2

- **Paper / URL:** Gou et al., arXiv 2506.21506 (NeurIPS 2025 D&B); https://osu-nlp-group.github.io/Mind2Web-2
- **Release date:** Jun 2025.
- **Maintainer:** OSU NLP Group.
- **What one item looks like:** A long-horizon agentic search task with a time-varying answer and citations, e.g. finding IKEA items that meet a budget and listing links. **130 tasks** (10 dev public, 120 test private).
- **Domain tag:** text / web research
- **Resembles:** Research and analyst desk work; not IT/BPO.
- **Human times:** **Per-item for a 30-task subset** (7 participants, 3 per task): mean 18.4 min, range 8–44 min. The authors call these underestimates. Per-task times may be in Appendix E.3, which I did not read in full.
- **Model results over time:** One snapshot, mid-2025: OpenAI Deep Research 0.28 success (8.4 min), Grok DeeperSearch 0.27, Gemini DR 0.18, Claude Research 0.10, Operator 0.10, ChatGPT Search 0.06; human 0.54.
- **Item-level results public?** No (private test set; leaderboard by submission).
- **Grading:** Agent-as-a-Judge with tree-structured rubrics covering correctness and source attribution.
- **Time horizon already computed?** No.
- **Verdict: EXCLUDE** for this project: research search tasks, a small private test set, and one time point. Pass to whoever covers research and analyst work.
- **Sources checked:** https://arxiv.org/html/2506.21506v2

## 12. REAL (AGI Inc)

- **Paper / URL:** arXiv 2504.11543; https://realevals.xyz ; https://github.com/agi-inc/agisdk
- **Release date:** Apr 2025.
- **Maintainer:** The AGI Company (AGI Inc).
- **What one item looks like:** A task on deterministic clones of Amazon, DoorDash, Airbnb, Gmail, Google Calendar, LinkedIn, Uber, United, Upwork, Zillow or OpenTable, e.g. "Add two of item X to cart, check out, and report the total." **112 tasks.**
- **Domain tag:** computer_use
- **Resembles:** Consumer tasks; email and calendar admin is weakly like admin assistance.
- **Human times:** None.
- **Model results over time:** One snapshot: Claude 3.7 Sonnet Thinking 41.1, Gemini 2.5 Pro 38.4, o3 34.8, DeepSeek V3 19.6, GPT-4o 14.3, OpenAI CUA 7.1. A public leaderboard continues.
- **Item-level results public?** Not confirmed.
- **Grading:** localStorage state diff (exact) for actions; rubric-based LLM judge for retrieval.
- **Verdict: EXCLUDE.** Consumer-oriented with no human times.
- **Sources checked:** https://arxiv.org/html/2504.11543

## 13. WebVoyager (and Emergence-WebVoyager)

- **Paper / URL:** He et al. 2024, arXiv 2401.13919. Emergence-WebVoyager: Akkil et al., arXiv 2603.29020 (Mar 2026).
- **What one item looks like:** A live-site lookup on 15 sites (Amazon, Apple, Booking, GitHub, Google Flights …). 643 tasks in the original, 535 in the Emergence revision.
- **Human times:** None. Agent times are 29–1,370 s for Operator.
- **Model results:** Mostly vendor self-reports at 87–90%: Browser Use 89%, Mariner 90.5%, Gemini 2.5 CU 88.9%, OpenAI CUA 87%. Under the stricter Emergence protocol, Operator drops to 68.6%.
- **Grading:** GPT-4V judge in the original; human annotation in the Emergence version.
- **Verdict: EXCLUDE.** Consumer lookups, saturated, self-reported results, no human times.
- **Sources checked:** https://arxiv.org/html/2603.29020 ; https://leaderboard.steel.dev/leaderboards/webvoyager.md (search)

## 14. AssistantBench / BrowseComp / BearCubs (search-puzzle family)

- **AssistantBench** (Yoran et al., arXiv 2407.15711, Jul 2024): 214 "time-consuming" web information-seeking questions, e.g. "highest price a high-rise apartment sold for in Mission Bay, SF, in 2021." There are **no human solve times**, only a design criterion of "several minutes" and authoring time of 20–30 min. HAL has a series over 15 models (best: o3 38.8%, GPT-5 35.2%). **EXCLUDE:** trivia search, no times.
- **BrowseComp** (OpenAI, 2025): hard-to-find-fact puzzles. **EXCLUDE** per brief.
- **BearCubs** (arXiv 2503.07919): 111 info-seeking questions needing real browser interaction. Human mean 4 min 46 s (range 0:26–27:24; easy 2:14, medium 5:32, hard 10:52), self-timed by annotators. I don't know whether per-question times are released. Agents: ChatGPT Agent 65.8%, Operator 23.4%, Anthropic CU 14.4%. **EXCLUDE** (puzzles), but note that it has human times if a "web lookup" curve is ever wanted.
- **Sources checked:** https://arxiv.org/html/2407.15711v2 ; https://hal.cs.princeton.edu/assistantbench ; https://arxiv.org/html/2503.07919v3

---

## Other things checked and set aside (one line each)

- **WebBench (Halluminate + Skyvern, May 2025):** 2,454 open tasks (5,750 total) on 452 live top sites; READ 64%, CREATE 21%, UPDATE 7%, DELETE 6%, FILE 1.5%. Write tasks such as forms and logins are the weak spot (about 46.6% SOTA); Anthropic CUA was best at 66%. No human times. Results folder in repo. EXCLUDE (no times, consumer sites), but the form-filling split is BPO-flavoured. https://github.com/Halluminate/WebBench
- **World of Workflows / WoW-bench (Skyfall AI, Jan 2026):** 234 ServiceNow tasks via 108 MCP tools (API, not browser), testing hidden business-rule side effects. Scores: GPT-5.1, Gemini-3-Pro, Sonnet-4.5, Opus-4.5. No human times. Relevant to ITSM but belongs with tool-use/API benchmarks. https://arxiv.org/html/2601.22130v2
- **CAP (Aug 2026):** 420 cross-site consumer tasks. Human baseline: 16.3 min average, 10% full success. Best agent 8%. EXCLUDE (consumer; humans fail too). https://arxiv.org/html/2608.08392v1
- **Odysseys (CMU, Apr 2026):** 200 long-horizon live-web tasks with rubrics. Opus 4.6 44.5%, GPT-5.4 33.5%. No human times despite citing METR. EXCLUDE for now; a possible long-horizon web lead if someone times humans. https://arxiv.org/html/2604.24964v1
- **Westworld (Halluminate/Yutori, 2025):** 5 synthetic consumer simulators, 100 tasks. Not researched further.
- **Original Mind2Web / Multimodal-Mind2Web (2023):** offline step-level action prediction from cached pages. EXCLUDE (step accuracy, not task completion).
- **Outside my area, noted:** GAIA validation items carry a per-question annotator "How long did this take?" field (per-item human times, free text needing normalization). This is for the cross-cutting or assistant researcher. CRMArena-Pro and τ-bench belong to the customer-service researcher. TheAgentCompany belongs to the occupational researcher. OSWorld-Verified (GPT-5.4 75.0% vs human 72.4%) belongs to the desktop researcher.

## Leads I didn't chase

1. **Email the WorkArena++ authors** (ServiceNow Research: Boisvert / Drouin / Gasse) for the recorded human time-to-resolution logs on the 98-instance human curriculum. This is the single highest-value ask.
2. **Download the WebArena (179) and VisualWebArena (233) human Playwright traces** and extract per-task durations and per-action timing. This gives a seconds-per-action calibration for converting WorkArena oracle action counts, Online-Mind2Web `reference_length` and SCUBA demo step counts into time. Check METR's `eval-analysis-public` repo first; their extracted WebArena times may already be there (not confirmed).
3. **Render the BrowserGym leaderboard HF Space files** (`results/*/workarena-l1.json` etc.) to confirm whether per-task results are stored and to get submission dates.
4. **SCUBA human demonstration data:** check the GitHub release for per-task human step counts or timestamps.
5. **ERPBench release:** watch for the public release; ask the authors for per-task human times.
6. **StarShell HF collection:** check whether per-task agent results and logs for the four 2026 frontier models are published, which would give a 2026 per-item point on WorkArena tasks.
7. **ST-WebAgentBench live leaderboard:** check for newer-model CuP results (ICLR 2026 camera-ready may have them).
8. **Online-Mind2Web per-task human-label files plus HAL traces:** assemble a per-task success matrix for the β fit.
9. I could not verify a separate "Kwa & Cheng" cross-domain paper beyond METR's 14 Jul 2025 blog post (Thomas Kwa et al.). If it exists as an arXiv paper, check whether it adds WorkArena or Online-Mind2Web.
