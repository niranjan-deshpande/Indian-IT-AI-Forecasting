# Customer service, help desk, and policy-constrained tool use: benchmark search

Searched 2026-11-09. Everything below was checked against the paper or repo unless it is marked *(unverified)*. Model release dates come from the source named; where none was given, the entry says so.

## Bottom line

- **None of the benchmarks in this area has per-item human completion times.** No study I found times human agents doing these items, and nobody (METR, Epoch, or others) has fit a time horizon to any of them. METR's July 2025 cross-domain post covers 11 benchmarks and none is customer service. I couldn't find a "Kwa & Cheng" cross-domain paper that adds one.
- **The best anchor is the τ-bench family (Sierra).** Its items are real customer-service work (retail returns and exchanges, airline rebooking, telecom troubleshooting, banking support), it has scores for many models across 2024–26, its grading is documented, and per-task traces are public (HAL for airline; the taubench.com S3 submissions). Item length can be estimated three ways:
  1. Scale gold action counts and turn counts, converted with contact-centre handle times.
  2. Use simulated call durations from τ-Voice.
  3. Get the timestamped logs of the 495 real-human sessions in the Sim2Real study.
- **Human-time data for calibration** (see the section near the end):
  - Brynjolfsson, Li & Raymond: about 43 minutes per technical-support chat, mostly at Philippine BPO offices, broken down by topic.
  - Klarna: about 11–12 minutes per human-handled query.
  - Vendor handle-time tables: about 6 minutes for an average call; 8–12 minutes for telecom technical support.
- **Saturation.** On Artificial Analysis's runs, τ²-bench Telecom is at about 99% for frontier models, and the original τ²-bench is at about 85–88% on the official board. Frontier models need the harder sets: τ³-Banking (best about 55%), τᶜ-Bench, τ-Voice, and CRMArena-Pro multi-turn.

---

## 1. τ-bench (v1) and τ²-bench (text: retail, airline, telecom)

- **Paper/URL:** τ-bench, arXiv 2406.12045 (17 Jun 2024; Yao, Shinn, Razavi, Narasimhan). τ²-bench, arXiv 2506.07982 (9 Jun 2025; Barres, Dong, Ray, Si, Narasimhan). Repo: github.com/sierra-research/tau2-bench (now labelled τ-bench 2.0). Leaderboard: taubench.com.
- **Maintainer:** Sierra Research.
- **Item:** A simulated customer, played by an LLM, with a hidden goal and persona, chats with the agent. The agent has a domain policy document and tools such as order lookup, exchange and refund. Success means the final database state matches the gold state, plus required statements to the user. Examples:
  - **Retail:** the customer wants to exchange a delivered item for another variant and return a second item. The agent must authenticate the customer, look up the orders, check the policy, confirm, and call the exchange and return tools.
  - **Telecom (τ², "dual control"):** "mobile data not working." The agent must guide the user through actions on their own phone, such as toggling airplane mode or resetting APN settings.
- **Size:** retail 114–115, airline 50, telecom 114 (subsampled from 2,285 generated tasks). τ-bench 2.0 (2026-10-19) replaced 50 English retail and 50 telecom tasks and froze 50 tasks per domain for the text-v1 package.
- **Domain tag:** text (tool use through an API, no GUI).
- **Resembles:** chat and voice customer support in retail and e-commerce (returns, exchanges, order changes) and airline reservations (changes, cancellations, baggage). Telecom tier-1 technical support resembles IT help-desk troubleshooting scripts. This is very close to Indian BPO voice and chat process work.
- **Human times: none. Estimable** in four ways:
  - **(a) Action and turn counts.** τ² Table 4 gives gold actions per telecom task: service_issue mean 2.3 (range 1–8), mobile_data mean 4.3 (2–8), mms mean 6.0 (2–12). Success falls toward zero above 7 actions. One τ²-retail study (arXiv 2607.01426) reports baseline sessions of about 6.3 user turns, 15.4 assistant turns and 4.6 tool calls.
  - **(b) Calibrate to handle time.** Map action counts to minutes using handle times by call type: retail 4–8 minutes; telecom technical 8–12 minutes (vendor tables, below).
  - **(c) Simulated call durations.** Use τ-Voice call lengths (entry 3).
  - **(d) Real-human logs.** Ask the Sim2Real authors for timestamps (entry 4).
- **Model results over time:**
  - **HAL airline (50 tasks, two scaffolds, 15 models):** models released Jan–Aug 2025, from DeepSeek-R1 (Jan 2025) to GPT-5 and Claude Opus 4.1 (Aug 2025). Best is 56% (o4-mini-high, Claude 3.7 Sonnet). HAL has paused updates.
  - **Official τ² board (snapshot 2026-10):** Qwen3.5-397B-A17B 87.9%, Gemini 3.0 Pro 85.4%, Claude Opus 4.5 85.3% overall pass^1.
  - **τ² paper (2025):** telecom pass^1 is gpt-4.1 34%, o4-mini 42%, claude-3.7-sonnet 49%. gpt-4.1 scores 74% on retail and 56% on airline.
  - **Artificial Analysis telecom:** 440 models, top 99.1% (GLM-5.2, JT-35B-Flash). It plots score against release date. Its implementation differs from the official board.
  - Scores are not comparable across 1.x and 2.0, or across user simulators.
- **Item-level results:**
  - **HAL:** zipped traces per run (encrypted; decrypt with hal-decrypt). Strip `taken_actions` using `task.actions`, per HAL's 2026-10-05 notice.
  - **taubench.com:** 2.0 submissions carry every task/trial observation in `benchmark-submission.json` under web/leaderboard/public/submissions/. Trajectories are copied to `s3://sierra-tau-bench-public/`; I didn't confirm that bucket is publicly readable.
  - Submissions have an optional `model_release.release_date` field.
- **Grading:** deterministic comparison of the final database state with gold, plus required-output checks. 2.0 adds natural-language assertions judged by an LLM (gpt-5.4-mini) and communication checks. Metric is pass^k.
- **Time horizon computed by anyone?** No.
- **Verdict: CANDIDATE, top priority (nearest to INCLUDE).** It meets criteria 1, 3, 4 and 5. Gap: human times. Fastest fix: compute per-item gold action count and median turn count from public traces. Fit minutes = a + b·actions, anchored on handle times by call type. Validate on a timed human-agent pilot of about 30 tasks: a person plays the agent through the tool API, which takes a few days of contractor time. The frontier is saturated on telecom, so pair it with τ³-Banking, τᶜ or τ-Voice.
- **Sources:** arxiv.org/abs/2406.12045; arxiv.org/html/2506.07982; github.com/sierra-research/tau2-bench (README, CHANGELOG.md, docs/leaderboard-submission.md); taubench.com; hal.cs.princeton.edu/taubench_airline; artificialanalysis.ai/evaluations/tau2-bench; arxiv.org/pdf/2607.01426.

## 2. τ³-bench Knowledge / τ-Banking ("τ-Knowledge")

- **Paper/URL:** arXiv 2603.04370, "τ-Knowledge: Evaluating Conversational Agents over Unstructured Knowledge" (4 Mar 2026; Shi, Zytek, Razavi, Narasimhan, Barres). Announced 18 Mar 2026 as τ³-bench. Shipped in the tau2-bench repo as domain `banking_knowledge`.
- **Maintainer:** Sierra.
- **Item:** fintech customer support. The agent must find the relevant policy among about 700 linked knowledge documents (698), combine it with tool outputs, and make a verifiable, policy-compliant account change. Example from the changelog: task_074 is a refund that should be corrected to $14.50. **97 tasks.**
- **Domain tag:** text.
- **Resembles:** bank and card back-office and contact-centre work: disputes, refunds, cash-back and fee queries, using knowledge-base lookup. Close to Indian banking BPO.
- **Human times:** none. Estimable as in entry 1. Document-retrieval steps add length.
- **Model results:** best was about 25.5% pass^1 at release (Mar 2026). The taubench.com τ³-Banking tab later shows Qwen 3.8 Max 55.2%, Claude Opus 5 48.7%, Grok 4.5 47.9%. Grading changed in v1.0.1 (2026-07-15), so scores before and after are not comparable.
- **Item-level results:** same submission mechanism as entry 1.
- **Grading:** database-state hash plus actions. v1.0.1 relaxed the rule so extra read calls no longer zero the reward.
- **Time horizon computed by anyone?** No.
- **Verdict: CANDIDATE.** It is unsaturated and the work is very close to banking BPO. Gaps: human times (as in entry 1), and the score series spans only about 8 months with one grading break.
- **Sources:** arxiv.org/abs/2603.04370; sierra.ai/resources/research/tau-3-bench-knowledge; taubench.com; tau2-bench CHANGELOG.md.

## 3. τ-Voice and τ-bench 2.0 voice/i18n (voice-v1, voice-v2, τ-i18n, τ-Entity)

- **Paper/URL:** arXiv 2603.13686, "τ-Voice: Benchmarking Full-Duplex Voice Agents on Real-World Domains" (14 Mar 2026; Ray, Dhandhania, Barres, Narasimhan). τ-bench 2.0 release, 2026-10-19.
- **Maintainer:** Sierra.
- **Item:** the τ² retail, airline and telecom tasks run as live full-duplex audio calls with a simulated caller, including accents, background noise and interruptions. **278 tasks:** retail 114, airline 50, telecom 114.
  - **2.0 additions:** voice-v2 and text in six languages, *including Hindi* (en, es, pt, hi, zh, ko), with 50 tasks per domain per language. Also τ-Entity "intake," over 200 tasks, voice by default.
- **Domain tag:** text, as audio.
- **Resembles:** inbound voice contact-centre calls, the core Indian BPO voice process. Entity intake resembles data capture by phone.
- **Human times:** none. **Estimable directly:** every simulated call has a wall-clock duration (call limit 1,200 s in the paper, 2,400 s in 2.0). The paper's example retail call lasted about 3 minutes. Median call duration per task with a competent agent is a lower bound on human talk time; add wrap-up time to get handle time. I couldn't confirm that per-call durations are published. The submission schema has `interaction_metrics`, which is worth checking.
- **Model results:**
  - **Paper (all-domain pass@1, clean / realistic audio):** gemini-live-2.5-flash-native-audio (Dec 2025) 31/26; gpt-realtime-1.5 (Feb 2026) 49/35; grok-voice-agent (Dec 2025) 51/38. Text baselines: GPT-5 85%, GPT-4.1 54%.
  - **taubench.com τ³-Voice tab (later):** Ava Zero 86.0%, phonic-1 83.2%, gpt-live-1 79.9%. Dates for these models not given.
- **Item-level results:** 2.0 voice-v2 packages carry per-task observations and quality diagnostics.
- **Grading:** same task reward as text. Post-hoc judges score naturalness and speech fidelity but do not change the reward.
- **Time horizon computed by anyone?** No.
- **Verdict: CANDIDATE.** It is the most direct voice-BPO analogue, with a built-in duration measure and Hindi coverage. Gaps: a short model series (Dec 2025 onward), and call durations need confirming or regenerating ourselves by running the open code.
- **Sources:** arxiv.org/abs/2603.13686; arxiv.org/html/2603.13686; github.com/sierra-research/tau2-bench (README, CHANGELOG); taubench.com.

## 4. Sim2Real human-user study on τ-bench (data source, not a benchmark)

- **Paper/URL:** arXiv 2603.11245, "Mind the Sim2Real Gap in User Simulation for Agentic Tasks" (11 Mar 2026, v2 31 Jul 2026; Zhou, …, Neubig, Wu, Sap; CMU). COLM 2026 submission.
- **What it is:** 451 Prolific participants in the US played the *customer* on 165 τ-bench retail and airline tasks against a GPT-5.2 agent. Three batches give 495 sessions.
- **Key numbers:**
  - Agent success with real humans: **63.6%**, against up to 77.8% with LLM user simulators. Simulators are "easy mode."
  - The τ-bench binary reward is largely orthogonal to human-perceived quality.
- **Human times:** none reported. No compensation or duration is given, and no data release URL is in the text. But the chat-interface logs almost certainly have timestamps, which would give a per-task human-paced conversation length.
- **Verdict: CANDIDATE data source.** Email the authors for timestamped session logs, which would give per-item conversation durations for 165 τ-bench tasks. Also apply the success discount for real versus simulated users when mapping to real work.
- **Sources:** arxiv.org/abs/2603.11245; arxiv.org/html/2603.11245v2; PDF appendix A.1.

## 5. τᶜ-Bench (TASTE harder extension of τ²)

- **Paper/URL:** arXiv 2605.28556, "A Matter of TASTE: Improving Coverage and Difficulty of Agent Benchmarks" (27 May 2026).
- **Item:** auto-generated, difficulty-evolved tasks in the τ² airline, retail and telecom domains. They more than double the unique tool combinations. Validity is judged by an LLM.
- **Domain tag:** text.
- **Resembles:** same as entry 1.
- **Human times:** none. Longer action chains make the action-count estimate useful.
- **Model results:** 11 agent/user pairs. For example, Gemini-3-Flash falls from 0.82–0.94 on τ² to 0.28–0.61. Model release dates are not in the abstract.
- **Item-level results:** not checked.
- **Grading:** τ² grading.
- **Time horizon computed by anyone?** No.
- **Verdict: CANDIDATE, low priority.** Useful to add harder, longer items to the τ² curve. Gaps: synthetic tasks, and LLM-judged validity.
- **Sources:** arxiv.org/pdf/2605.28556; huggingface.co/papers/2605.28556.

## 6. CRMArena

- **Paper/URL:** arXiv 2411.02305 (Nov 2024; NAACL 2025). Repo github.com/SalesforceAIResearch/CRMArena. Leaderboard huggingface.co/spaces/Salesforce/CRMArena-Leaderboard.
- **Maintainer:** Salesforce AI Research.
- **Item:** a question or action for a service persona (agent, manager or analyst) against a realistic Salesforce org, done through SOQL/SOSL and API tools. **9 tasks × 130 queries = 1,170 items.** About 30% are unanswerable in 5 of the tasks. Task types:
  - New Case Routing: pick the best human agent for an incoming case.
  - Handle Time Understanding, e.g. "which agent has the shortest average handle time".
  - Policy Violation Identification, e.g. does this case breach the knowledge-article policy.
  - Knowledge QA, Top Issue, Monthly Trend, Best Region, Named Entity Disambiguation, Transfer Count.
- **Domain tag:** software (CRM API) / text.
- **Resembles:** service-desk supervisor and analyst work, case routing, quality assurance against policy, and CRM data lookup.
- **Human times:** none per item. Ten Salesforce-using experts had about 45 minutes for 5 queries (one per task), which is a **budget of roughly 9 minutes per query**. That is an allocation, not a measured time, and they rated realism rather than solving for score.
- **Model results:** gpt-4o 54.4, claude-3.5-sonnet 41.8 (with a duplicate row showing 64.3), o1 64.3, deepseek-r1 9.0 (function calling) to 35.1 (ReAct), llama3.1 family. All released mid-2024 to Jan 2025. The leaderboard has no newer entries.
- **Item-level results:** per-task table in the paper and leaderboard. Per-query results not found.
- **Grading:** exact match on IDs; F1 for Knowledge QA.
- **Time horizon computed by anyone?** No.
- **Verdict: EXCLUDE, superseded by CRMArena-Pro.** Its items are mostly analytic lookups rather than handling a case, and its model series is stale.
- **Sources:** arxiv.org/html/2411.02305; salesforce-crmarena-leaderboard.hf.space; github.com/SalesforceAIResearch/CRMArena.

## 7. CRMArena-Pro

- **Paper/URL:** arXiv 2505.18878 (May 2025; TMLR, accepted Feb 2026). HF dataset `Salesforce/CRMArenaPro`. Repo github.com/SalesforceAIResearch/CRMArena.
- **Maintainer:** Salesforce AI Research.
- **Item:** **19 task types** across service, sales and CPQ (configure, price, quote) in B2B and B2C Salesforce orgs, single-turn and multi-turn. The multi-turn setting uses a simulated user who reveals information gradually. **4,280 queries** (2,140 per org, about 100 per task). Examples:
  - Service Case Routing.
  - Quote Approval: does this quote violate discount policy.
  - Invalid Configuration Identification, Lead Qualification, Knowledge QA, Handle Time Understanding.
  - Confidentiality-awareness probes.
- **Domain tag:** software (CRM API) / text.
- **Resembles:**
  - Customer-service case handling and routing.
  - Sales operations and quote approval, which are F&A-adjacent back office.
  - CRM data work, close to Indian BPO "CRM back office" processes.
- **Human times:** none per item. Same expert protocol as CRMArena (about 45 minutes for 5 queries, so about 9 minutes per query as a budget). No human success rate.
- **Model results (overall % single-turn B2B/B2C; multi-turn B2B/B2C):**
  - gemini-2.5-pro-preview-03-25: 54.1/58.3; 35.1/30.0
  - o1-2024-12-17: 47.5/49.5; 32.5/30.4
  - gemini-2.5-flash, gemini-2.0-flash, gpt-4o-2024-11-20, gpt-4o-mini, llama4-maverick, llama3.1-405b/70b
  - No CRMArena-Pro leaderboard; no newer models found.
- **Item-level results:** the main paper reports skill-level results only; per-task results may be in the appendix. Running it yourself is easy because data and code are open.
- **Grading:** exact match, with a gpt-4o answer extractor for multi-turn; F1 for Knowledge QA; LLM judge for confidentiality.
- **Time horizon computed by anyone?** No.
- **Verdict: CANDIDATE.** The work is realistic and heterogeneous (19 types × 2 orgs × 2 turn settings, so per-type human times would give useful spread). Gaps:
  1. Human times. Fix: time 3–5 Salesforce admins on about 5 items per task type (about 95 items, about 15 hours).
  2. The model series covers only Jul 2024 – Apr 2025. Fix: rerun the open harness on 2025–26 models.
- **Sources:** arxiv.org/html/2505.18878; github.com/SalesforceAIResearch/CRMArena; huggingface.co/datasets/Salesforce/CRMArenaPro; mlanthology.org/tmlr/2026/huang2026tmlr-crmarenapro.

## 8. CRM-Agent-Bench

- **Paper/URL:** arXiv 2610.32004 (23 Oct 2026; Banerjee, Lan, Cao). Repo github.com/salesforce-misc/crm-agent-bench (agent recipes; I couldn't confirm the task data or per-task results are there).
- **Maintainer:** Salesforce.
- **Item:** stateful multi-turn tasks, each with an executable contract checking actions, arguments, order, response, target state and protected state. **555 tasks in 9 domains:** retail 95, customer support 125, field service 23, **IT service management 66**, payments 73, travel 93, onboarding 41, sales 18, marketing 21. Example: `payments_transfer_frozen_source_01`. The agent must not attempt a transfer from a frozen account and must explain why.
- **Domain tag:** text (tool use).
- **Resembles:** customer support, the ITSM help desk, payments operations and onboarding (KYC-like). Broad coverage of the BPO list.
- **Human times:** none (human validation is listed as future work). Per-task LLM latency is reported, but that is model latency, not human time.
- **Model results:** 16 systems, all 2026-era (Gemini 3.8 Flash 83.6%; Claude Sonnet 5, GPT-5.5, GPT-5.6 81.3%; Claude Opus 5 three-round mean 83.3%; GPT-4.1 Nano 64.3%). Release dates are not given. It is a single snapshot, so there is no trend over time.
- **Item-level results:** per-domain in the paper. Per-task not confirmed.
- **Grading:** strict conjunction of programmatic checks. An LLM judge (gpt-5-mini) handles response content only.
- **Time horizon computed by anyone?** No.
- **Verdict: CANDIDATE, low priority.** It has good ITSM and payments coverage, but it is near-saturated (64–84%), has a single time snapshot, and no human times. Useful only if we rerun older models on it.
- **Sources:** arxiv.org/abs/2610.32004; arxiv.org/html/2610.32004.

## 9. EVA-Bench (ServiceNow voice agents)

- **Paper/URL:** arXiv 2605.13841 (13 May 2026, v3 9 Sep 2026; EMNLP 2026 Findings). Code and scenarios at github.com/ServiceNow/eva; site servicenow.github.io/eva; HF dataset "eva-bench".
- **Maintainer:** ServiceNow AI Research.
- **Item:** a bot-to-bot audio call. A simulated caller with a goal and persona phones a voice agent that queries and modifies a scenario database. Example: rebook a flight departing before 10 pm under a fare cap. **213 scenarios in 3 domains:** Airline Customer Service Management, Healthcare HR Service Delivery, and **Enterprise IT Service Management (help desk)**. Each domain has single-intent, multi-intent and adversarial scenarios.
- **Domain tag:** text, as audio.
- **Resembles:** voice IT service desk (password resets, access requests, incidents), HR shared-services calls, and airline voice support. A good fit for Indian IT help-desk and BPO voice work.
- **Human times:** none. Estimable from simulated call durations, as with τ-Voice, if logged. The paper reports per-turn latency (more than 5 s for accurate cascades) but no call length.
- **Model results (EVA-A pass@1):** 12 systems, all 2026-era: Nova-3 + GPT-5.4 + Sonic-3 0.504; GPT-Realtime-1.5 0.467; Gemini-3.1-Flash-Live 0.292; GPT-Realtime-mini 0.163. No system scores above 0.5 on both accuracy and experience. A leaderboard is on the site.
- **Item-level results:** a local run writes per-record result.json and metrics.json. Public per-scenario results for the 12 systems not confirmed.
- **Grading:** EVA-A combines task completion (database state) and faithfulness. EVA-X covers conciseness, turn-taking, latency and progression. Simulator errors are detected and regenerated.
- **Time horizon computed by anyone?** No.
- **Verdict: CANDIDATE.** It is the only open voice benchmark with an ITSM help-desk domain. Gaps: human times (use call durations or a timed pilot), and a short model series. Low per-domain counts (about 70 each) limit the curve fit.
- **Sources:** arxiv.org/abs/2605.13841; arxiv.org/html/2605.13841; github.com/ServiceNow/eva.

## 10. CirrusBench (Alibaba cloud-service tickets)

- **Paper/URL:** arXiv 2603.28569 (30 Mar 2026; Alibaba Group and Fudan; submitted to KDD 2026). Framework at github.com/CirrusAI. I couldn't confirm the dataset is released.
- **Item:** a real historical cloud customer-service ticket, replayed turn by turn. Customer turns are merged. Checkpoints are labelled Solution, Standard, Inquire, Clarify or Appease. Tool mocks are recorded from real calls, with up to five reference documents (SOPs, wikis). About 51% of items include screenshots, converted to text by OCR. **1,925 tasks** (1,500 without tools, 425 with). Categories include server, registration, SMS service, website and email.
- **Domain tag:** text.
- **Resembles:** tier-1 and tier-2 technical support for a cloud or SaaS vendor, close to Indian IT-services and product-support desks.
- **Human times:** none reported. The "efficiency" metrics count tokens and skipped sub-tasks, not seconds. **Estimable:** the source tickets are real, so Alibaba holds the true handle times; checkpoint counts per task are a proxy.
- **Model results (Pass@1 with/without tools):** GPT-5 16.7/23.8; GPT-5-mini 15.2/22.1; Qwen3-Max 14.3/17.1; DeepSeek-V3.2 9.6/15.2; GPT-4o 6.8/7.0; GPT-5.2 is in Table 3. Models range from 2024 to late 2025, so there is a modest time spread and scores are unsaturated.
- **Item-level results:** not found.
- **Grading:** LLM judge (DeepSeek-V3.2; 91.5% agreement with experts) checks whether each checkpoint reply contains the key content.
- **Time horizon computed by anyone?** No.
- **Verdict: CANDIDATE, low priority.** Real tickets and low scores are attractive. But the data release is uncertain, it is graded by an LLM judge, and there are no times. Ask the authors for ticket handle times.
- **Sources:** arxiv.org/abs/2603.28569; arxiv.org/html/2603.28569.

## 11. SOPBench

- **Paper/URL:** arXiv 2503.08669 (Mar 2025, v2 Jun 2025; EMNLP 2026 main). Repo github.com/Leezekun/SOPBench (code, data, and **24k+ agent trajectories**).
- **Maintainer:** UCSB (Xifeng Yan group) and collaborators.
- **Item:** a customer request in one of 7 customer-service domains, served by a sandbox with tools and a service-specific SOP. Code verifiers check that the agent follows SOP constraints and reaches the correct outcome. For example, verify the account and check the balance limit before a transfer. **About 830–900 test cases, 167 tools, 70 SOPs.** The domain list wasn't on the abstract page; it reportedly includes banking, healthcare, DMV, library, hotel and university *(unverified)*.
- **Domain tag:** text.
- **Resembles:** SOP-driven BPO process work in banking service, appointment and records handling.
- **Human times:** none. Estimable from SOP step counts, since the verifier encodes the required steps.
- **Model results:** 18 models (2024 to mid-2025). o4-mini-high is best; strong models score about 30–50%.
- **Item-level results:** yes, the trajectories are released in the repo.
- **Grading:** rule-based verifiers from the SOP code (no LLM judge).
- **Time horizon computed by anyone?** No.
- **Verdict: CANDIDATE.** It has clean grading and public item-level trajectories. Gaps: synthetic and somewhat toy-like items, a model series that ends mid-2025, and no times.
- **Sources:** arxiv.org/abs/2503.08669; aclanthology.org/2026.emnlp-main.936.

## 12. ECom-Bench

- **Paper/URL:** arXiv 2507.05639 (Jul 2025; EMNLP 2025 main). Repo github.com/XiaoduoAILab/ECom-Bench.
- **Maintainer:** Xiaoduo AI Lab and SJTU.
- **Item:** an e-commerce (JD-style home appliance) support task built by trained customer-service staff from real chats. A persona-driven simulated user interacts through 21 MCP tool categories, and some items include images. Examples: a price-protection refund with screenshot proof; scheduling an installation for Thursday; issuing a personal invoice. **53 tasks (18 multimodal).**
- **Domain tag:** text (some multimodal).
- **Resembles:** e-commerce chat support (refunds, invoices, installation scheduling).
- **Human times:** none.
- **Model results (pass^1):** GPT-4o 44.0, Doubao-1.5-Pro 39.0, DeepSeek-V3 36.5, Qwen-Max 15.1. The series covers 2024–early 2025 models only.
- **Item-level results:** not found.
- **Grading:** rule-based (database state, required retrieval calls, output keywords).
- **Verdict: EXCLUDE.** Only 53 items and a stale series. It is a τ-bench clone with no time data.
- **Sources:** arxiv.org/html/2507.05639v2.

## 13. CXBench (regulated customer-experience workflows)

- **Paper/URL:** arXiv 2610.25954 (19 Oct 2026; Yu, …, Briand, Muñoz).
- **Item:** a customer request with tools and explicit regulatory process requirements (disclosures, consent, authority, ordering). Rule cards link each cited obligation to evidence in the trace. **120 tasks, 6 regulated domains.** The domain names weren't on the abstract page; likely finance and insurance-type domains *(unverified)*.
- **Domain tag:** text.
- **Resembles:** regulated banking, insurance and telecom calls where compliance scripting matters, typical of BPO QA scorecards.
- **Human times:** none.
- **Model results:** 7 models, 840 runs. 55.5% of runs are "false passes": the outcome is correct but process checks fail. Only 13.8% pass both. Per-model scores not checked.
- **Grading:** hybrid. Deterministic checks for order and authority; LLM judge for semantic requirements.
- **Verdict: CANDIDATE, low priority / methodological.** The key point for us is acceptance. Outcome-only grading (as in τ-bench) overstates acceptability for regulated work. Small, a single snapshot, no times, and data release unclear.
- **Sources:** arxiv.org/abs/2610.25954.

## 14. JourneyBench ("Beyond IVR")

- **Paper/URL:** arXiv 2601.00596 (2 Jan 2026; EACL 2026 Industry).
- **Item:** support conversations generated from graph-structured SOPs, in 3 domains. The score is the User Journey Coverage Score (policy adherence). **703 conversations**, averaging about 3.3 tool calls each.
- **Domain tag:** text.
- **Model results:** GPT-4o and GPT-4o-mini. The paper studies agent design rather than tracking frontier models.
- **Human times:** none.
- **Verdict: EXCLUDE.** Few models, synthetic, and focused on agent design.
- **Sources:** arxiv.org/abs/2601.00596.

## 15. ServiceBench (complaint handling under information asymmetry)

- **Paper/URL:** arXiv 2610.24733 (Oct 2026; Hong Kong PolyU).
- **Item:** a complaint scenario reconstructed from real public X/Twitter complaint threads with brands. The agent must resolve it under information asymmetry. **2,500 scenarios, 184 complaint categories, 5 industries:** airlines, hotels, restaurants, retail, ride-hailing and delivery.
- **Domain tag:** text.
- **Resembles:** complaint and escalation desks, social-media customer care (a common BPO line).
- **Human times:** none. The authors note the lack of any human-agent baseline.
- **Model results:** GPT-5, GPT-4o, GPT-4o-mini, DeepSeek-V4-Pro, Gemini-2.5-Flash, Llama-3.3-70B, Qwen3-32B, scored on 1–5 "justice" scales.
- **Grading:** LLM judge (GPT-5) scores; not pass/fail.
- **Verdict: EXCLUDE.** There is no binary acceptance outcome, so it doesn't fit the logistic framework. Release unclear.
- **Sources:** arxiv.org/html/2610.24733.

## 16. ABCD (Action-Based Conversations Dataset), for calibration only

- **Paper/URL:** arXiv 2104.00783 (Apr 2021, NAACL 2021). ASAPP.
- **Item:** more than 10,000 *human-to-human* customer-service chats, collected with "Expert Live Chat." Trained agents followed policy guidelines for 55 user intents, such as refunds, address changes and account access. Average **22.1 turns per dialogue**, the highest among the comparable datasets. Wait times were kept under 10 minutes; no duration field was found.
- **Use:** turn counts and action sequences of humans doing τ-like retail tasks. They could anchor a turns-to-minutes conversion if combined with a per-turn chat time.
- **Verdict: EXCLUDE as a benchmark.** It is a dialogue-state dataset with no agentic model series. Keep it as a calibration reference.
- **Sources:** arxiv.org/abs/2104.00783 (PDF text).

---

## Human-time calibration sources (for estimating item lengths)

| Source | What it gives | Notes |
|---|---|---|
| Brynjolfsson, Li & Raymond, "Generative AI at Work" (NBER w31161; arXiv 2304.11771v2) | Technical-support chats for US small businesses, handled mostly by **Philippine BPO agents**. Sessions average about **40 minutes**; baseline handle time is **43 minutes**; 1.7 chats/hour before AI and 2.5 after. AI saves 4–6 minutes per chat, varying by topic. Payroll and account topics are 50% of chats. | The closest analogue to Indian BPO. Handle time includes concurrent chats, so it overstates the effort for a single chat. |
| Klarna (20-F, Feb 2026, as reported by a secondary source) *(primary not opened)* | Human agents about **11–12 minutes** per query, against about 2 minutes for the AI assistant. | Company-reported. |
| Vendor handle-time tables (Sprinklr via ringly/kayako; HiveDesk; Talkdesk) *(vendor, unaudited)* | Average call about **6 minutes 10 seconds**. Retail voice 3–8 minutes. Telecom billing 2–4 minutes, telecom technical 8–12 minutes. Tech/SaaS 7–11 minutes. Simple order status 3–5 minutes. | Definitions differ on whether after-call work is included. |
| τ²-retail session profile (arXiv 2607.01426) | About 6.3 user turns, 15.4 assistant turns and 4.6 tool calls per baseline session. Escalated sessions about 16.5 assistant turns and 9.5 tool calls. | Agent-side, but gives the structure needed to convert turns to minutes. |
| ABCD | Human-human chats average 22.1 turns. | No timestamps. |

**Suggested estimator for the τ family:** minutes_i = handle time for the call type × (actions_i / mean actions for that call type), or a regression on turns and actions. Validate on a small timed pilot: a contractor acts as the agent using the τ tool API and a human or LLM customer. Run 20–30 tasks per domain. Real-user logs from the Sim2Real study, or τ-Voice call lengths, give independent cross-checks.

---

## Noted in passing (other researchers' areas)

- **SCUBA (Salesforce):** computer use inside the Salesforce CRM UI. Desktop/browser lane.
- **WorkArena / WorkArena++ (ServiceNow):** browser lane. Has ITSM-flavoured tasks.
- **FaulT-Bench (arXiv 2608.27021):** network troubleshooting from user tickets. IT-ops lane.
- **SiriusHelper (arXiv 2605.00043):** a Tencent big-data ops benchmark built from production incidents. IT-ops lane.
- **FrontierFinance (arXiv 2604.05912)** and **OmegaUse-OfficeVal (arXiv 2607.27155):** both report human-expert hours per task. Back-office and occupational lanes.

## Leads I didn't chase

- **τ-bench 2.0 submission packages:** check whether `interaction_metrics` or `benchmark-diagnostics.json` record per-call durations for voice-v1 and voice-v2. If so, these are free per-item duration proxies. My fetch of the second half of the τ-Voice paper failed.
- **Public access to `s3://sierra-tau-bench-public/`** (per-task trajectories with model release dates) and the HAL encrypted traces: confirm both and pull item-level success.
- **Sim2Real authors (Zhou, Sap; CMU):** request timestamped human-user logs (495 sessions, 165 tasks).
- **τ-Entity (intake, 200+ tasks, voice):** the domain looks like data capture by phone; no details read.
- **OlaBench (arXiv 2510.22143):** industrial customer-service benchmark; GPT-5.2 70.6, Gemini 3 Pro 70.8; construction not read.
- **CXMArena (arXiv 2505.09436):** synthetic contact-centre tasks (intent prediction, agent quality adherence, article search, multi-turn RAG with tools). Not agentic end-to-end; not read further.
- **TelcoAgent-Bench (arXiv 2604.06209), English/Arabic telecom troubleshooting; Ticket-Bench (arXiv 2509.14477), multilingual ticket purchase; DRIP-R (arXiv 2605.07699), retail policy ambiguity; MANTRA (arXiv 2605.06334), compliance tasks:** abstracts only or not read.
- **Full-Duplex-Bench-v3 (arXiv 2604.04847), MTVA-Bench (arXiv 2609.20152), EchoChain (arXiv 2604.16456):** voice tool-use benchmarks, not customer-service-specific; not read.
- **SOPBench domain list** and **CXBench domain list:** not verified.
- **Indian-language voice:** AI4Bharat "Voice of India" (ASR only, 15 languages) and vendor Hinglish function-calling tests (caller.digital). Neither is an agent benchmark, but they bear on the Hindi voice-v2 numbers.
- **Kwa & Cheng cross-domain paper:** not found by search. Neither METR's 2025 cross-domain post nor anything else I found includes a customer-service benchmark.
