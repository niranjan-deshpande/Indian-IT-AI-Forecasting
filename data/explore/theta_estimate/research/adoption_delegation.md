# Adoption A(t), deployed delegation rates, and disclosed effort reductions: Indian IT services and BPO

*Compiled 2026-11-07. Purpose: inputs for the bottom-up θ model, to compare with the top-down estimate of about 2.3 pp a year of realised labour replacement over FY24–FY26 (range 1.5–3.6).*

## How this was built, and the labels

- **Earnings calls FY24 to Q1 FY27.** I read these from the repo's local transcript corpus; `audit/calls_transcripts.csv` lists each local path and source URL.
  - Firms covered: TCS, Infosys (SEC 6-K exhibits), HCLTech, Wipro, Tech Mahindra, LTIMindtree and Cognizant. That is 111 calls from Apr 2023 to Jul 2026.
  - I converted them to text and searched the full text. Every quote below from these calls was read in context.
  - The TCS Q1 FY27 transcript URL the brief gave returns HTTP 403 to automated fetch. The repo copy (`data/sources/tcs/2026-27_q1_transcript.pdf`) was downloaded from that same URL, and I read the quote there.
- **Two sub-agents in this session searched the web and opened sources.** One covered the Q2 FY27 calls (Oct 2026), annual reports and 20-F/10-K filings, Microsoft press releases and BPO firms. The other covered global delegation and success-rate benchmarks.
  - Their full notes, with every URL opened and verbatim quotes, are Appendices A and B.
  - I re-opened two of their key sources myself: the Microsoft release of 3 Jun 2026 and Cognizant's Q3 CY26 8-K exhibit 99.1. Both matched.
- **Verification labels:**
  - **P**: primary, meaning the company's own document, or a filing or transcript, opened directly.
  - **V**: a vendor or company marketing page or case study, opened.
  - **Pr**: press-only; the number was seen only in a press article that was opened.
  - **S**: snippet-only; seen only in a search snippet. Do not cite these.
- **Scope labels:**
  - **FW**: firm-wide.
  - **LL**: line-level, meaning one service line such as testing, AMS or BPO.
  - **SC**: a single client or case.
  - **POT**: a potential, target or "achievable" figure, not a realised one.
- **Headcount denominators** come from the repo panel (`data/explore/round3/gcc/top6_headcount_fy.csv`, fiscal-year-end, global). FY24/FY25/FY26:
  - TCS 601,546 / 607,979 / 584,519
  - Infosys 317,240 / 323,578 / 328,594
  - HCLTech 227,481 / 223,420 / 227,181
  - Wipro 232,614 / 233,346 / 242,156
  - Tech Mahindra 145,455 / 148,731 / 147,623
  - LTIMindtree 81,650 / 84,307 / 87,950
  - Cognizant (10-K): 336,800 at end-2024, 351,600 at end-2025, 359,900 at 30 Sep 2026.

---

## 1. Adoption over time, A(t)

### 1.1 Three kinds of number that should not be mixed

1. **Trained or certified.** Every firm reports these and they are large, but the definitions vary widely.
   - Infosys's "AI-aware" (84%) and Tech Mahindra's "AI-enabled through learning" (80%) are e-learning reach.
   - Wipro's three-tier GenAI training, Tech Mahindra's belts and Cognizant's "frontier AI badges" are deeper.
   - None of these measures use.
2. **Licensed or seated.**
   - GitHub Copilot seat counts are rare.
   - Large Microsoft 365 Copilot (office assistant) deployments: 50,000+ seats each at Cognizant, Infosys, TCS and Wipro (Dec 2025), rising to 100,000+ each at Infosys, TCS and Wipro (Jun 2026).
   - TCS has 50,000 Claude licences (Jun 2026) across engineering, finance, legal, marketing and sales.
3. **Active use.** The direct figures are:
   - Tech Mahindra: one-third of its IT-services workforce "using GitHub Copilot" (Oct 2024).
   - Wipro: 20,000+ (FY25) and 60,000+ (FY26) associates "leveraging AI developer tools".
   - Infosys: 30,000 developers "deployed" on GitHub Copilot (Apr 2026), and 80,000+ "working today on coding tools such as Claude Code or Codex" (Jul 2026).
   - Microsoft 365 Copilot activity: 86% of TCS's licensed users use it daily; monthly active use is 91%+ at Infosys and 95%+ at Wipro (Jun 2026).
   - Cognizant's share of code that is AI-generated or AI-assisted is a usage-intensity measure, not a head count.

### 1.2 Firm-by-firm evidence (chronological)

| Firm | Date (FY) | Type | Statement (exact or near-exact) | Implied share of headcount | Source | Ver. |
|---|---|---|---|---|---|---|
| Infosys | Jul 2023 (Q1 FY24) | trained | "We have trained 40,000 employees on generative AI." | ~12% | Q1 FY24 call (SEC 6-K exv99w05) | P |
| Infosys | Oct 2023 (Q2 FY24) | trained | "We have trained 57,000 employees in Generative AI." | ~17% | Q2 FY24 call | P |
| Infosys | Jan 2024 (Q3 FY24) | trained | "We have 100,000 employees trained in Generative AI areas." | ~31% | Q3 FY24 call | P |
| Infosys | Jul 2024 (Q1 FY25) | trained | "over 270,000 of our employees are now well trained in building a wide range of AI-powered solutions" | ~85% | Q1 FY25 call | P |
| Infosys | Mar 2025 (20-F FY25) | trained | "Over 2,75,000 of our people are trained on AI at different levels of proficiency" | 85% of 323,578 | 20-F FY25 (App. A) | P |
| Infosys | Oct 2025 (Q2 FY26) | trained | "About 90% of our employees are AI aware" | 90% | Q2 FY26 call | P |
| Infosys | Mar 2026 (20-F FY26) | trained | "84% of our workforce is now AI-aware" | 84% | 20-F FY26 (App. A) | P |
| Infosys | Apr 2026 (Q4 FY26) | licensed/active (coding) | "We have deployed over 30,000 developers on GitHub Copilot." | 9.1% | Q4 FY26 call | P |
| Infosys | Jun 2026 | licensed/active (M365) | 100,000+ seats; "over 91% monthly active users" | ~28% monthly active (91k / ~330k) | Microsoft release, 3 Jun 2026 | P (re-opened) |
| Infosys | Jul 2026 (Q1 FY27) | **active (coding agents)** | "From our delivery team, over 80,000 employees are working today on coding tools such as Claude Code or Codex for our clients and for some projects inside." | ~24% | Q1 FY27 call | P |
| Infosys | Oct 2026 (Q2 FY27) | active | Asked about the 80,000: "that number is increasing" (no new figure) | – | Q2 FY27 media call (App. A) | P |
| TCS | Jul 2023 (Q1 FY24) | trained | "over 50,000 TCSers trained in AI/ML solution-building skills"; plan for "a talent pool of over 100,000 Gen AI trained associates" | ~8% | Q1 FY24 call | P |
| TCS | FY26 annual report (May 2026) | trained (advanced) | "over 2,70,000 employees now possess advanced AI skills" | ~46% of 584,519 | press coverage of AR (App. A) | **Pr** |
| TCS | Jun 2026 | licensed/active (M365) | "empowered over 100,000 associates with Microsoft 365 Copilot"; "86% of Copilot-licensed associates actively use AI in their daily work" | ~14.5% daily active (86k / 593,798) | Microsoft release, 3 Jun 2026 | P (re-opened) |
| TCS | Jun–Jul 2026 (Q1 FY27) | licensed (Claude) | Anthropic partnership "gives us … 50,000 licenses" | ~8% | Q1 FY27 call; press release (App. A) | P |
| Wipro | Oct 2023 (Q2 FY24) | trained (basic) | "we've trained as many as 180,000 employees in basic Gen AI general principles" | ~74% | Q2 FY24 call | P |
| Wipro | Jan 2024 (Q3 FY24) | trained (basic) | "210,000 Wiproites who have been trained on AI 101 skills" | ~88% | Q3 FY24 call | P |
| Wipro | Oct 2024 (Q2 FY25) | trained (advanced) + qualitative active | "trained and certified over 44,000 employees on Advanced AI, and we have a significant number of employees actively using AI developer tools" | 19% advanced | Q2 FY25 call | P |
| Wipro | Mar 2025 (20-F FY25) | **active (developer tools)** | "over 20,000 associates leveraging AI developer tools" | **8.6%** | 20-F FY25 (App. A) | P |
| Wipro | Dec 2025 | licensed (M365) | "over 50,000 Copilot licenses deployed" | ~21% | Microsoft release, 11 Dec 2025 (App. A) | P |
| Wipro | Mar 2026 (20-F FY26) | **active (developer tools)**, trained | "over 60,000 associates leveraging AI developer tools"; 212,663 completed GenAI training (33k basic, 85k advanced, 93k master) | **24.8%** active; 88% trained | 20-F FY26 (App. A) | P |
| Wipro | Jun 2026 | active (M365) | "over 95% monthly active usage"; "more than 29,000 end-user developed agents"; "more than 250,000 FTE days saved every quarter" | ~39% monthly active if ~100k seats | Microsoft release, 3 Jun 2026 | P (re-opened) |
| HCLTech | Apr 2025 (Q4 FY25) | trained | "trained more than 100,000 users and 4,000 developers in AI / Gen AI in 2025" | ~47% | Q4 FY25 call | P |
| HCLTech | Jan 2026 (Q3 FY26) | trained | "38,000-plus additional employees have been trained on GenAI" | – | Q3 FY26 call | P |
| HCLTech | Apr 2026 (Q4 FY26) | trained/certified | "we've trained 135,000 employees in GenAI technologies"; "11,800 AI builders and … 700-plus black belts" | 59% trained; 5% builders | Q4 FY26 call | P |
| HCLTech | FY26 annual report | trained/agents | 144,000+ trained; ~63,000 at specialised levels; "1000+ AI agents" | 63% | AR FY26 (App. A) | P |
| HCLTech | — | active | **No active-use or seat figure found in any call or report.** | – | – | – |
| Tech Mahindra | Jan 2024 (Q3 FY24) | trained (coding) | "trained 16,000 associates in Pair Programming" | ~11% | Q3 FY24 call | P |
| Tech Mahindra | Apr 2024 (Q4 FY24) | trained | "reskilling over 50,000 employees on AI" | ~34% | Q4 FY24 call | P |
| Tech Mahindra | Jul 2024 (Q1 FY25) | trained (coding) | "25,000 plus people that we have trained in AI pair programming" | ~17% | Q1 FY25 call | P |
| Tech Mahindra | Oct 2024 (Q2 FY25) | **active (coding)** | "1/3 of our IT services workforce is now using GitHub Copilot" | **33% of IT-services staff** (≈20–25% of total; the IT/BPO split is not given) | Q2 FY25 call | P |
| Tech Mahindra | Jul 2025 (Q1 FY26) | trained | "77,000 plus employees … trained in AI and Gen-AI" | ~52% | Q1 FY26 call | P |
| Tech Mahindra | Apr 2026 (Q4 FY26) | trained | "80% of the people who have been trained on AI"; "95% of our peak and prime accounts have some version … of GenAI" | 80% | Q4 FY26 call | P |
| Tech Mahindra | Jul 2026 (Q1 FY27) | certified | "over 65% of our associates certified as white, blue, or brown belt" | 65% | Q1 FY27 call | P |
| Tech Mahindra | Oct 2026 (Q2 FY27) | trained (tools) | "More than 24,000 IT associates have been upskilled on AI productivity tools, over 4,500 … on agent platforms, and approximately 48,000 hold an AI certification" | 16% tools; 32% certified (of 152,206) | Q2 FY27 call (App. A) | P |
| LTIMindtree | Jan 2024 (Q3 FY24) | trained | "trained over 10,000 employees on GenAI" | ~12% | Q3 FY24 call | P |
| LTIMindtree | Oct 2024 (Q2 FY25) | trained | "63% of our workforce is trained and equipped with Gen AI capabilities" | 63% | Q2 FY25 call | P |
| LTIMindtree | Oct 2025 (Q2 FY26) | trained | "over 80,000 employees have completed the GenAI Foundation Training Program" | ~95% | Q2 FY26 call | P |
| LTIMindtree | Jan 2026 (Q3 FY26) | trained | "more than 50% of our employees achieving intermediate or advanced AI skills" | >50% | Q3 FY26 call | P |
| LTIMindtree | Apr 2026 (Q4 FY26) | trained/platform | "more than 30,000 of developers are trained on the GitHub, Copilot"; "almost 70% of our developers are already on the GitHub platforms" (on the GitHub platform, not necessarily Copilot) | 34% trained | Q4 FY26 call | P |
| Cognizant | Nov 2023 (Q3 CY23) | trained | "trained about 55,000 of our employees on generative AI this year" | ~16% | Q3 CY23 call | P |
| Cognizant | Apr 2024 | licensed/trained | "purchased 25,000 Microsoft 365 Copilot seats"; "35,000 Cognizant developers have been trained on Github Copilot" (+40,000 planned) | 7% / 10% | Microsoft release, 22 Apr 2024 (App. A); the Q1 CY24 call also cites the plan to train 25,000 | P |
| Cognizant | 2024 (10-K FY24) | trained | "more than 168,000 associates … have taken generative AI trainings in 2024" | 50% | 10-K FY24 | P |
| Cognizant | Oct 2025 (Q3 CY25) | trained | "trained almost all our employees, more than 250,000 plus employees on AI-led skills" | ~72% | Q3 CY25 call | P |
| Cognizant | end-2025 (10-K FY25) | trained | "upskilled more than 330,000 associates on GenAI" (Jul 2023 to end-2025) | 94% | 10-K FY25 | P |
| Cognizant | Jul 2026 (Q2 CY26) | certified | "10,000 Claude-certified architects" | 3% | Q2 CY26 call | P |
| Cognizant | Oct 2026 (Q3 CY26) | certified | "over 95,000 frontier AI badges and certifications"; press: held by "over 45,000" associates | ~13% hold one | 8-K ex. 99.1 (re-opened); the 45k is **Pr** | P/Pr |
| Four firms | Dec 2025 | licensed (M365) | "Each of these companies will deploy over 50,000 Microsoft Copilot licenses" (Cognizant, Infosys, TCS, Wipro) | 8–21% | Microsoft release, 11 Dec 2025 | P |

**Usage intensity: Cognizant's share of code from AI** (firm-wide, self-reported, all P from calls/8-K)

| Quarter | Statement | Definition |
|---|---|---|
| Q3 CY24 (Oct 2024) | "generating 150,000 lines of accepted code per month … 2 million lines … annually" | lines of AI code accepted (absolute, not a share) |
| Q4 CY24 (Feb 2025) | "20% of our code accepted by our developers was generated by AI" | share of accepted code |
| Q2 CY25 (Jul 2025) | "nearly 30% of our code was AI-generated in quarter two" | AI-generated |
| Q3 CY25 (Oct 2025) | "approximately 30% of our internal code was AI-generated" | AI-generated, "internal" |
| Q4 CY25 (Feb 2026) | "32% of our code is AI assisted"; "over 30% of our developer effort in software development cycles is AI-assisted and agentic" | AI-*assisted* (looser) |
| Q1 CY26 (Apr 2026) | "nearly 40% of our code to be AI-assisted" | AI-assisted |
| Q3 CY26 (Oct 2026) | "over 50% of our code now AI-assisted" | AI-assisted |

The wording moves from "accepted … generated by AI" to "AI-assisted", so the later points are not strictly comparable with the first. Infosys reports only absolute counts of lines generated with AI: 3 million (Apr 2024), "more than 25 mn" (Oct 2025) and "over 28 mn" (Jan 2026). These cannot be turned into shares.

**Surveys (context for the denominator; not specific to IT firms)**
- Microsoft and LinkedIn Work Trend Index, India (May 2024): "92% of knowledge workers in India use AI at work", and 72% bring their own AI tools. Self-reported; covers all knowledge workers (P, App. A).
- EY Work Reimagined (Dec 2025): 62% of Indian employees report frequent GenAI use (**Pr**).
- Stack Overflow 2025, global professional developers: 50.6% use AI tools daily and 14.1% use agents daily (P, App. B). DORA 2025: 90% of technology professionals use AI (P, App. B).
- Nasscom Strategic Review (Feb 2026): "2 Mn+ professionals upskilled in AI (including 200k–300k in advanced AI)", out of a sector of about 5.8 million (P for the 2M; the 5.8M is S).

### 1.3 A rough sector timeline (my synthesis; tied to the evidence above)

"Active" here means the share of all employees, delivery and support staff alike, who use a GenAI coding or work assistant or agent in their actual work at least monthly. Firms disclose too little to separate daily from monthly use, except TCS's 86% daily use of M365 Copilot.

| Fiscal year (end point) | Trained (any GenAI course) | Licensed / seated | **Active use, A(t)** (central; range) | Anchors | Confidence |
|---|---|---|---|---|---|
| FY24 (Mar 2024) | 15–90% by firm; median ~30% | Pilots only; Copilot trained cohorts of 16k (Tech Mahindra) and 35k (Cognizant) | **~3% (1–6%)** | No firm gave an active-use count. Tech Mahindra and Cognizant cohorts were trained, not licensed. Infosys's 3M lines of code imply small-scale use | Low |
| FY25 (Mar 2025) | 50–85% | Copilot seats in the tens of thousands at the leaders | **~12% (8–20%)** | Wipro 8.6% active (Mar 2025); Tech Mahindra one-third of IT-services staff on Copilot (Oct 2024, the upper bound); Cognizant 20% of code from AI (Q4 CY24) | Medium-low |
| FY26 (Mar 2026) | 60–95% | M365 Copilot 50k+ each at four firms (8–21% of headcount); GitHub Copilot 30k at Infosys; Claude/Codex/Devin enterprise deals begin | **~22% (15–30%)** | Wipro 24.8% active developer-tool users (Mar 2026); Infosys 9% on Copilot (Apr 2026, likely incomplete as Claude/Codex users were already ramping); Cognizant 32–40% of code AI-assisted | Medium |
| FY27 to date (Jul–Oct 2026) | 65–95% | M365 Copilot 100k+ each at TCS, Infosys and Wipro; 50k Claude seats at TCS | **~30% (25–40%)** for coding and agent tools. Any GenAI work tool used monthly: ~30–45% | Infosys 24%+ on Claude Code or Codex and "increasing"; monthly M365 Copilot use 28% (Infosys) and ~39% (Wipro); TCS 14.5% daily on M365 Copilot; Cognizant >50% of code AI-assisted | Medium |

**Caveats on A(t).**
- **(a) Denominator.** Coding tools are relevant mainly to application development and maintenance staff, perhaps 40–60% of headcount.
  - On that base, the FY27 developer adoption share is roughly 50–65%. For example, Infosys's 80k is drawn "from our delivery team".
  - The model should therefore set A per task line, not per head.
- **(b) The firms selected what to disclose,** and leaders disclose earlier.
  - HCLTech and TCS give no figure on active coding-tool use.
  - The sector average is probably at or below the Wipro and Infosys path.
- **(c) Microsoft 365 Copilot is an office assistant.** Its very high monthly-active rates (91–95%) are for an assistant seated mainly on office and support roles. It says little about delegation of delivery work.
- **(d) Adoption accelerated within FY26–FY27,** so a year-average A for FY26 is lower than the end-point. A simple average over FY24–FY26 is about **12%** (range 8–19%).

---

## 2. Deployed delegation and success rates (proxies for the acceptance probability)

The definitions differ in ways that matter.
- "**Handled**" or "**contained**" means AI touched the interaction and no human was requested. This is not "**resolved**".
- Intercom's resolution rate counts *assumed* resolutions, where the customer leaves without asking for more help.
- "**AI-assisted code**" counts code that a human edited.
- Back-office straight-through-processing (STP) rates are mostly the result of rules, OCR and e-invoicing, not GenAI.

| Line | Metric | Number | Date / period | Exact definition (source's words) | Population | Source | Ver. |
|---|---|---|---|---|---|---|---|
| Code | Share of code from AI (Indian IT, firm-wide) | 20% → ~30% → 32% → ~40% → >50% | Q4 CY24 → Q3 CY26 | "code accepted by our developers was generated by AI" (Q4 CY24); later "AI-assisted" | Cognizant, firm-wide | Cognizant calls; 8-K ex 99.1 Oct 2026 | P |
| Code | Share of new code from AI (big tech) | 75% (from 50% "last fall") | Apr 2026 | "75% of all new code at Google is now AI-generated and approved by engineers" | Google | blog.google, Cloud Next 2026 | P |
| Code | Code written by software | 20–30% | Apr 2025 | "written by software" | Microsoft (Nadella) | TechCrunch | Pr |
| Code | Code written by or with LLMs | 95–100% (from ~40% in Feb 2026) | Jul 2026 | "written by or with LLMs" | Coinbase | Cointelegraph | Pr |
| Code | Copilot completion acceptance | 33% of suggestions; 20% of lines | Nov–Dec 2024 | "average acceptance rate" | ZoomInfo, >400 devs | arXiv 2501.13282 | P |
| Code | Agentic pull-request (PR) acceptance on GitHub | Codex 65%, Claude Code 53%, Cursor 51%, Devin 49%, Copilot agent 38%; humans 77% | to Jun 2025 | "% Accepted" | 456k PRs | arXiv 2507.15003 | P |
| Code | Agentic PR merge probability | Claude 84%, Codex 74%, Cursor 64%, Copilot 60%, Devin 43%; humans 84–86% | to Nov 2025 | model-adjusted "merge probability" | 9,428 PRs, popular Python repos | arXiv 2607.21832 | P |
| Code | Merged agentic PRs still needing human rework | 15.4% | 2026 paper | "required explicit reviewer involvement through feedback or direct commits" | 9,799 PRs | arXiv 2605.22534 | P |
| Code | Auto-generated code changes shipped unchanged | 79% | Aug 2024 | "shipped 79% of the auto-generated code reviews without any additional changes" | Amazon Java upgrades (Amazon Q) | Jassy post, via simonwillison.net | Pr |
| Code | Share of own work fully delegable | 0–20% (majority of respondents) | Aug 2025 | "fully delegate" | 132 Anthropic engineers | anthropic.com research | P |
| Code (Indian IT) | Agentic spec-to-code accuracy | 87%, "estimated 9x productivity" | Q2 FY27 (Oct 2026) | "validated, review-ready code … engineers approving every output. It averaged 87% accuracy" | one core-banking migration (HCLTech) | HCLTech Q2 FY27 call | P (SC) |
| Code (practitioner view) | Unattended production fixes | "very limited" | Apr 2026 | "ability to run production environment fixes without human-in-the-loop is very limited" | HCLTech CEO, industry view | HCLTech Q4 FY26 call | P |
| IT ops | Incident tickets auto-remediated | 38% | FY25 | "automated remediation of 38% of the incident tickets" | one Tech Mahindra client | Tech Mahindra integrated AR FY25 | P (SC) |
| IT ops | Recurring incidents auto-remediated | "over a third" (of *recurring* incidents) | Jul 2026 | "auto remediating over a third of recurring incidents"; alert noise −85% | one LTIMindtree client (energy) | LTIMindtree Q1 FY27 call | P (SC) |
| IT ops | Incidents resolved automatically | ~30% of all incidents; ~67% of data-centre, network and cloud tickets by bots; 17% of a 45% automation potential realised in year 1 | Mar 2026 | "~30% automated resolution rate across total incident volumes" | one HCLTech client (AIOps on ServiceNow) | hcltech.com case study | V (SC) |
| IT ops | Employee IT requests "handled" | 90%+ | Feb 2026 | "handling 90%+ of employee IT requests" | ServiceNow internal | ServiceNow newsroom | V |
| IT ops | L1 incidents fully resolved by AI agent | ≈7% of all incidents (15% eligible × 46% resolved) | 2026 | "Coverage of incidents currently eligible" × "Resolution rate of eligible incidents" | ServiceNow internal | servicenow.com customer page (403) | **S** |
| IT ops | Autonomous resolution | Broadcom 88%; Mercari 74% | undated | "autonomous resolution rate" / "handled 74% of IT tickets autonomously" (likely of bot-channel tickets) | two Moveworks clients | moveworks.com | V |
| Support | Chats handled by AI | 80% (≈850 FTE) | FY2025 | "handled 80% of customer service chats" (chat channel only) | Klarna | Klarna 20-F FY2025 (SEC) | P |
| Support | Chats handled by AI | two-thirds | Feb 2024 (first month) | "handles two-thirds of … customer service chats" | Klarna | klarna.com press | P |
| Support | Resolution rate | 77% → 64% (as scale grew) | Sep 2025 → Aug 2026 (cumulative) | "77% resolution rate" → "64% resolved autonomously" | help.salesforce.com | Salesforce Q2 FY26 and Q2 FY27 transcripts | P |
| Support | Resolution rate | 76% average | Nov 2026 page | includes confirmed and *assumed* resolutions (customer leaves without asking for more help) | 12,000+ Fin customers | fin.ai; Intercom help article | V |
| Support | Resolution rate | 50% → 70%+ | Oct 2025 | "Resolution rates increased from 50% to over 70%" | Chime (Sierra client) | sierra.ai | V |
| Support | Inquiries resolved without a human | "over half" | FY2025 | resolve "without human intervention" | Lemonade | Lemonade 10-K FY2025 | P |
| Support | Issues fully resolved in self-service | 14% (36% for "very simple" issues) | Aug 2024 | "fully resolved in self-service" | 5,728 customers (Gartner survey) | gartner.com press release (blocked) | **S** |
| Support (voice) | Calls handled by voice agent | 75% in business hours; 100% after hours | May 2026 | "autonomously handle 75% of business-hour calls" | Florida Prepaid (Salesforce client) | Salesforce Q1 FY27 transcript | P (SC) |
| Support (Indian IT) | Containment improvement | +3 pp; 90% intent identification | Jan 2025 | "3% user containment improvement rates" | one TCS client (30,000 chats a day) | TCS Q3 FY25 call | P (SC) |
| Support (Indian IT) | Call volume reduction | 12% | Oct 2025 | "12% reduction in customer service call volumes" | one Infosys client | Infosys Q2 FY26 call | P (SC) |
| Support (practitioner view) | Contact-centre staff reduction | "by 75%" (anecdote) | Jul 2025 | "contact centers where a very large number of people get reduced by 75%" | HCLTech CEO, unnamed cases | HCLTech Q1 FY26 call | P (anecdote) |
| Support (Indian vendor) | Automation rate; end-to-end resolution | 84%; 70% | undated (likely before GenAI) | "Automation Rate" / "End-to-End Query Resolution" | Zurich (Haptik client) | Haptik PDF | V |
| Back office | Claims fully automated; first notice of loss (FNOL) taken by AI | ~55% of claims; 96% of FNOL | FY2025 | "roughly 55% of our claims were automated … start to finish" | Lemonade (renters, pet) | Lemonade 10-K FY2025 | P |
| Back office | Touchless invoices | 70% (>500k invoices) | Jul 2026 | "achieved 70 percent touchless processing" | one Wipro healthcare client | Wipro AGM 6-K (SEC) | P (SC) |
| Back office | Provider-enrolment effort automated | "up to 90%" | Jul 2026 | "automating their manual effort up to 90%" | one Wipro healthcare client | Wipro Q1 FY27 call | P (SC) |
| Back office | Purchase-order (PO) processing, manual intervention | "up to ~90%" reduction | Apr 2024 | "reduced manual intervention in PO processing by up to ~90%" | one TCS client | TCS Q4 FY24 call | P (SC) |
| Back office | Explanation-of-benefits documents automated (GenAI) | ~60% of 1.26M a year | Sep 2026 | "~60% automated today" (exceptions go to humans) | one Conduent client | Conduent investor deck (SEC) | P (SC) |
| Back office | Invoice STP (mostly not AI) | average 32.6%; best-in-class 49.2% | 2025 | "processed … straight-through" | Ardent Partners survey | Tungsten relaying Ardent | V-relay |
| Back office | Invoice exception rate | 18.4% average | Jan 2026 | "invoice exception rate" | Ardent, State of ePayables 2025 | payablesplace.ardentpartners.com | P |
| Back office | STP (insurer, not specific to AI) | 90.3% | 2025 | Manulife STP measure | Manulife | SEC 40-F exhibit | P |
| Back office | Credit auto-adjudication | auto finance 48% → >85% (target); small business 50% → 70% (target) | Sep 2025 | "auto-adjudicated" | TD Bank | SEC 6-K | P |
| Back office | US payer claims STP | ~80% "industry benchmark" (rules-based) | May 2026 | "legacy CAPS plateau at 80% STP" (no source given) | US payers | HealthAxis blog | V |

**Reading for the model's acceptance probability.**
- **Code:** a per-suggestion acceptance of ~30%. Agentic PR acceptance of 40–85% on public repos, with humans at ~77–86%, and ~15% of merged agent PRs still reworked by humans. Firm-level "share of code" of 30–50% (Cognizant), and 75% at Google, the frontier.
- **IT ops:** realistic full resolution is **~7–35% of all incidents**. The 70–90% figures count "handled" requests or bot-channel tickets.
- **Support:** autonomous resolution of **~55–80%** at AI-first deployers (Klarna, Salesforce, Lemonade, Fin), against a customer-side 14% fully resolved in self-service (Gartner, snippet). Salesforce's own rate fell as scope widened. No Indian BPO discloses an AI-handled share.
- **Back office:** GenAI-specific touchless rates of **~55–70%** on single programmes (Lemonade, Wipro, Conduent). Legacy rules-based STP already sits at 30–90% depending on the process, so the AI increment is smaller than the headline.

---

## 3. Disclosed productivity and effort reductions by service line

### 3.1 Firm-wide or portfolio-level statements

| Firm | Date | Claim (exact words) | Scope | What it measures | Source | Ver. |
|---|---|---|---|---|---|---|
| **TCS** | 9 Jul 2026 (Q1 FY27) | "One quantification I can give you is in most places, the productivity gain passed on is around 10% to 15% range." Later: "there is an overall productivity we are able to achieve, about 10% to 15%, when we leverage AI for client engagements. You should look at that productivity gain coming through the tenure of the project … usually is compensated by additional opportunities." "By and large … it's a rule of thumb, saying we can expect a 10% to 15% productivity on average. But we are able to offer a front loaded commitment." | FW, but only for engagements where AI is leveraged; cumulative **over the contract tenure**, not per year; varies by line (new development vs monitoring vs production support) | Productivity passed to clients at renewal (θ times pass-through, over the contract) | TCS Q1 FY27 transcript, pp. 11 and 22–23 (repo copy of the tcs.com URL in the brief; the live URL returns 403) | **P, verified** |
| TCS | Oct 2026 (Q2 FY27) | "there is a deflation because of the productivity benefit"; "some front-loading of productivity benefits"; revenue per employee shows "a slight reduction" | FW, qualitative | – | TCS Q2 FY27 transcript (NSE) | P |
| **Tech Mahindra** | Apr 2026 (Q4 FY26) | "We started measuring the true AI-led productivity improvement in our programs starting last year and 7% improvement might not sound much but I think it's a very healthy start … This is an AI-led only productivity improvement." (The sentence between reads "It includes everything else that we have done from an optimization or bringing in lean principles", which contradicts it; most likely "excludes" was meant.) | **FW across programmes, measured, FY26** | AI-only productivity in delivery programmes | Tech Mahindra Q4 FY26 call | P |
| Tech Mahindra | Oct 2025 / Jul 2026 | "Nobody's expecting … 80% productivity over the next five years"; "getting into a 70%, 80% productivity benefit over a 5-year deal … [is] not visible today without very significant process or system changes by the client" | FW, a ceiling on commitments | – | Tech Mahindra Q2 FY26 and Q1 FY27 calls | P |
| **HCLTech** | Apr 2026 (Q4 FY26) | "40% of the industry runs the risk of being disrupted by AI and can shrink 3% to 5% CAGR for a few years … application development support, traditional infrastructure operations, customer support"; "it would translate to 2% to 3% for our portfolio"; "very little has really played out in already reported numbers" | Industry (40% of spend) and FW (2–3% for HCLTech); forward-looking | Revenue deflation a year | HCLTech Q4 FY26 call | P |
| HCLTech | Oct 2026 (Q2 FY27) | "able to offset AI-driven deflation by gaining market share"; revenue per employee +2.4% YoY | FW, qualitative | – | HCLTech Q2 FY27 call | P |
| **LTIMindtree (LTM)** | Jul 2026 (Q1 FY27) | "the same requirement or the same deal, I would have priced probably, let us say, 15% higher a year back, but the same scope of work I am picking up at, let us say, 15% less" | FW, order book | Price per unit of scope a year earlier (θ times pass-through plus competition) | LTIMindtree Q1 FY27 call | P |
| LTM | Oct 2026 (Q2 FY27) | "60% of the total … productivity headwinds has already been, passed on to the customers"; "probably 60%-70% of our portfolios, we are done with it" | FW | Share of the eventual pass-through already given | LTM Q2 FY27 call (NSE) | P |
| Infosys | Oct 2026 (Q2 FY27) | "continued sharing of AI driven productivity benefits"; "vast majority of the benefit of the AI productivity is already baked in"; on a company-wide AI effort figure, no number given | FW, qualitative | – | Infosys Q2 FY27 6-K | P |
| Infosys | Jul 2025 (Q1 FY26) | Analyst: "You did share some numbers of 5% to 15% related benefits that are being passed in, through AI programs." CFO did not dispute it and attributed the guidance to macro conditions | FW for AI programmes, **attributed by an analyst**; the original Infosys statement was not located | Benefits passed to clients | Infosys Q1 FY26 call | P (analyst's words) |
| Cognizant | Oct 2025 / Feb 2026 | "productivity has gone up 30%, which means there is more throughput" (tied to the ~30% AI code share); revenue per person +5% and margin per person +8% over the trailing 12 months, "share with our clients the productivity win" | FW (software development) | Developer throughput | Cognizant Q3 CY25 and Q4 CY25 calls | P |
| Wipro | Jun 2026 | "more than 250,000 FTE days saved every quarter" from M365 Copilot. My conversion: ~4,000 FTE, ≈1.7% of headcount, assuming ~62 working days a quarter | FW, office assistant only, self-reported time saved | Hours saved | Microsoft release, 3 Jun 2026 | P (re-opened) |
| Wipro | Oct 2026 (Q2 FY27) | Contract "average tenor" of about 2–2.5 years, so "we should be at that inflection curve in a few quarters" | FW | Timing of pass-through | Wipro Q2 FY27 call | P |
| Nasscom | Feb 2026 | FY27 hiring shifts from volume to skill mix, with AI productivity passed to clients | Sector, qualitative | – | Catalogue IND-01g | P |

### 3.2 Service-line statements (management estimates of what is achievable)

| Line | Claim | Date | Who | Scope | Source | Ver. |
|---|---|---|---|---|---|---|
| **BPO / business process operations** | "the biggest impact is on the BPO business, which could be as much as 40% to 50%" | Oct 2025 (Q2 FY26; repeats the Investor Day) | HCLTech CEO | LL, POT | HCLTech Q2 FY26 call | P |
| BPO + testing | "DPO [sic: BPO] and testing … benefits would be to the extent of 50% … programs which is promising 50% savings from their current outsourced spend" | Jul 2024 (Q1 FY25) | HCLTech CEO | LL, POT / contracted | HCLTech Q1 FY25 call | P |
| Customer service | "if there are large customer service programs, we see that there could be benefits to the clients of 20% to 40%" | Apr 2025 (Q4 FY25) | Infosys CEO | LL, POT | Infosys Q4 FY25 call | P |
| **Software development (SDLC)** | "In SDLC, 25% to 30% is what we think is doable with a lot of maturity … to scale for the entire 1000 or 2000 people … could run into a couple of years" | Oct 2025 | HCLTech CEO | LL, POT | HCLTech Q2 FY26 call | P |
| SDLC | "You start with single digits, 10% to 15% productivity, then there's an evolution to reach 20%-25%" | Oct 2025 (Q2 FY26) | TCS (Aarthi Subramanian) | LL; realised now 10–15%, target 20–25% | TCS Q2 FY26 call | P |
| SDLC (phases) | "the 5% to 20% productivity on certain phases of the programs are possible. I didn't say the entire project end-to-end" | Jul 2024 (Q1 FY25) | TCS CEO | LL, phase-level | TCS Q1 FY25 call | P |
| Application development and maintenance (ADM) | "productivity improvement anywhere from 10% to 30% by adoption of a GitHub Copilot … a very gradual journey" | Jul 2024 | HCLTech CEO | LL, POT | HCLTech Q1 FY25 call | P |
| SDLC (platform) | "automating design, build, and test workflows, resulting in 30% to 40% increased developer productivity" | Oct 2025 | HCLTech (AI Force) | LL, where deployed | HCLTech Q2 FY26 call | P |
| **IT ops / AMS / infrastructure** | "In IT Ops, application support and maintenance, it will be 10% to 15% … if you have fully leveraged the existing machine learning and rule-based automation, then incremental impact can be 10% or 15%"; and in Jul 2025: "the incremental benefit from Generative AI is only marginal" | Oct 2025; Jul 2025 | HCLTech CEO | LL, POT (incremental to earlier automation) | HCLTech Q2 FY26 and Q1 FY26 calls | P |
| ADM and infrastructure (analyst) | "ISG basically spoke about some 30% cost savings in ADM and infra due to GenAI" | Jul 2024 | Analyst citing ISG | LL | TCS Q1 FY25 call (analyst's question) | P (2nd-hand) |
| Application managed services | ADMS "is actually seeing the productivity expectations on large contract renewals"; "lesser head-count requirements" | Oct 2026 | Tech Mahindra | LL, qualitative | Tech Mahindra Q2 FY27 call | P |
| Coding + test-case creation | "achieved 15–30% effort savings in coding and test case creation"; 18–20% manual effort in other cases | FY26 | Tech Mahindra | SC/LL cases | Tech Mahindra integrated AR FY26 | P |
| Testing | "reducing manual testing efforts by 70%" | Jan 2026 | TCS, Finnish insurer | SC | TCS Q3 FY26 call | P |
| Testing | "50% reduction in overall manual effort, the elimination of manual testing" | Apr 2025 | TCS client | SC | TCS Q4 FY25 call | P |
| Legacy modernisation | "40% to 60% productivity improvement in large legacy code conversions" | Jul 2023 | LTIMindtree | LL, use-case | LTIMindtree Q1 FY24 call | P |
| Legacy modernisation | "reduced migration effort by close to 30 percent" | Jul 2026 | Wipro, one large US bank | SC | Wipro AGM 6-K (SEC) | P |
| Legacy modernisation | Hertz COBOL to microservices: 60% lower cost, 60% faster | 2026 | Infosys | SC | catalogue / θ literature §7 (Infosys Q4 FY26 / Q1 FY27) | P |
| Development (agents) | "12 specialized AI agents … reducing … cumulative development effort by 38%" | Oct 2026 | LTM client | SC | LTM Q2 FY27 call | P |
| Mixed / end-to-end | "over 20x gains for specific activities and an overall end-to-end process productivity in the range of 40% to 50%" | Oct 2025 | Infosys | SC ("some of the use cases") | Infosys Q2 FY26 call | P |
| Mixed | "40% effort reduction"; "80% less rework" | Oct 2026 | Infosys cases | SC | Infosys Q2 FY27 6-K | P |
| Incident handling | "about 40% reduction in incident handling effort"; deal priced on "roughly 40% fewer tickets, 20% lower mean time to resolution" | Jul 2026 | Tech Mahindra | SC (contracted targets) | Tech Mahindra Q1 FY27 call | P |
| Operations (AIOps) | IT operations efficiency +18% (BP) | Apr 2026 | Infosys | SC | Infosys Q4 FY26 call | P |
| Claims / business process operations (BPO) | "cut manual effort by 60% for a mid-sized payer"; fraud-dispute pilot ">50%"; brokerage deal "committing to more than 50% productivity improvement over five years" | Jul 2026 | Cognizant | SC (one pilot, one contracted commitment) | Cognizant Q2 CY26 call | P |
| Office / knowledge work (M365) | "20–25% productivity improvements in research and content production tasks"; "25–35% reduction in selective work-cycle time" | Jun 2026 | TCS | internal, task-level | Microsoft release, 3 Jun 2026 | P |
| BPO (firm view) | "seeing productivity from AI and automation in existing accounts"; renewals "despite having some deflation … maintain the revenue base at neutral" | Oct 2026 | Firstsource | FW, qualitative | Firstsource Q2 FY27 call | P |

### 3.3 Analysts and surveys (all mix θ with pass-through, demand and contract timing)

| Source | Claim | Date | Ver. |
|---|---|---|---|
| Kotak Institutional Equities | Gross AI-led deflation ~7%, net 3.5% (FY27E); base case 3.5% a year of AI-led pricing erosion, appearing first in renewals | Apr / Sep 2026 | Pr (catalogue IND-03b, IND-03e) |
| ICICI Securities | AI to deflate traditional services revenue by ~2–3% a year, peaking FY26–FY28; ~30% of industry at risk | 2026 | P (catalogue IND-05a, IND-05b) |
| Jefferies | Worst case: FY26–31 revenue CAGR 3 pp lower (~15% cumulative deflation); application managed services is 22–45% of revenue at several firms | 2025–26 | Pr (catalogue IND-08d) |
| J.P. Morgan | AI deflation "only in its second year", with further headwinds expected; no rate given | 2026 | Pr (catalogue IND-04b) |
| Analyst on the HCLTech Q4 FY26 call | Renewals already carried 10–15% price cuts over the life of a deal, before AI | Apr 2026 | P (catalogue IND-08b note) |
| EY India | IT productivity +43–45% over 5 years; development ~60%, BPO 52% | 2025 | Pr; method undisclosed (θ literature §7) |

### 3.4 What this implies for the comparison with 2.3 pp a year (notes, not estimates)

- **The only measured firm-wide figure is Tech Mahindra's 7% AI-only productivity improvement across programmes in FY26.** That is a first full measurement year, at an A(FY26) of ~20–25% for the sector. In the model's units it is a one-year saving of about 7% of programme effort, or roughly 28–35% per active user if all of it came from active users.
  - Against this, the top-down estimate of ~2.3 pp a year (FY24–FY26 average) is *lower*.
  - The two fit if FY24–FY25 were near zero (A ≈ 3–12%) and FY26 carried most of the saving, or if Tech Mahindra's programme measure is not fully realised in headcount (HCLTech: "very little has really played out in already reported numbers").
- **TCS's "10–15% passed on" is cumulative over the contract tenure,** typically 3–5 years, and only where AI is leveraged. With an analyst-stated pre-AI baseline of 3–5% a year, the AI increment over the old productivity commitments may be only a few points a year.
- **Order of line-level potentials, consistent across HCLTech, TCS and Infosys:**
  1. BPO and testing (40–50%)
  2. Customer service (20–40%)
  3. SDLC (25–30% with maturity; 10–15% realised in 2025)
  4. IT ops/AMS (10–15%, incremental, "marginal")
- **HCLTech's 3–5% CAGR shrinkage of the AI-disrupted 40% of spend** works out to ~1.2–2.0% a year of industry spend, or 2–3% for HCLTech's portfolio. That is in the same range as the top-down 1.5–3.6 pp, though it is a forward-looking revenue figure.

---

## 4. Gaps

- **No firm discloses firm-wide shares** of tickets auto-resolved, BPO interactions handled by AI, or a seat count for a GitHub or other coding assistant against headcount. The exceptions are Infosys (30k Copilot; 80k on Claude Code/Codex), Wipro (60k on developer tools) and Tech Mahindra (one-third on Copilot).
- **HCLTech and TCS give no active coding-tool count.** TCS's FY26 annual-report figure of 270,000 with "advanced AI skills" is press-only.
- **BPO firms disclose nothing usable on adoption.** Concentrix, Teleperformance, Firstsource, Genpact and EXL give no AI-handled share. WNS/Capgemini, HGS and iEnergizer were not searched.
- **Unverified: Tech Mahindra "76% … achieved AI certification".** A third party attributes this to the FY26 annual report; the sub-agent did not find it in the report text.
- **Microsoft 365 Copilot figures come from Microsoft's own release**, so they are vendor-reported.

---

## 5. Sources opened

### 5.1 Earnings-call transcripts read locally (repo corpus; source URLs in `audit/calls_transcripts.csv`)

Key URLs for the quotes above:
- TCS Q1 FY27 (9 Jul 2026): https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2026-27/q1/Management%20Commentary/Transcript%20of%20the%20Q1%202026-27%20Earnings%20Conference%20Call%20held%20on%20Jul%209,%202026.pdf (local `data/sources/tcs/2026-27_q1_transcript.pdf`; live fetch returns 403 today)
- TCS Q2 FY26 (9 Oct 2025): https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2025-26/q2/Management%20Commentary/ (full path in the audit CSV; local `2025-26_q2_transcript.pdf`)
- TCS Q1 FY25, Q4 FY25, Q3 FY26, Q3 FY25, Q4 FY24, Q1 FY24: tcs.com Management Commentary PDFs (audit CSV)
- Infosys calls (SEC 6-K exhibit 99.5):
  - Q1 FY24 …/000106749123000049/exv99w05.htm
  - Q2 FY24 …/000106749123000057/
  - Q3 FY24 …/000106749124000004/
  - Q4 FY24 …/000106749124000016/
  - Q1 FY25 …/000106749124000026/
  - Q4 FY25 https://www.sec.gov/Archives/edgar/data/1067491/000106749125000010/exv99w05.htm
  - Q1 FY26 https://www.sec.gov/Archives/edgar/data/1067491/000106749125000022/exv99w05.htm
  - Q2 FY26 …/000106749125000036/
  - Q3 FY26 …/000106749126000004/
  - Q4 FY26 https://www.sec.gov/Archives/edgar/data/1067491/000106749126000018/exv99w05.htm
  - Q1 FY27 https://www.sec.gov/Archives/edgar/data/1067491/000106749126000038/exv99w05.htm
- HCLTech:
  - Q1 FY25 https://www.hcltech.com/sites/default/files/documents/investor-reports/Hcltech-call-earnings-Jul12-2024.pdf
  - Q4 FY25 https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech-Earnings-Q4FY25-Transcript.pdf
  - Q1 FY26 https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech-Earnings-Q1FY26-Transcript-18.pdf
  - Q2 FY26 https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech-Earnings-Q2FY26-transcript-updated_0.pdf
  - Q3 FY26 https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech-Earnings-Q3-FY26-Transcript.pdf
  - Q4 FY26 https://www.hcltech.com/sites/default/files/documents/investor-reports/hcltech-earnings-q4-fy26-transcript.pdf
  - Q1 FY27 https://www.hcltech.com/sites/default/files/documents/investor-reports/HCLTech-Earnings-Q1-FY27-Transcript.pdf
- Tech Mahindra:
  - Q2 FY25 https://insights.techmahindra.com/investors/tml-q2-fy-25-earnings-transcript.pdf
  - Q4 FY26 https://insights.techmahindra.com/investors/tml-q4-fy-26-earnings-transcript.pdf
  - Q3 FY24, Q4 FY24, Q1 FY25, Q1 FY26, Q2 FY26, Q1 FY27: insights.techmahindra.com (audit CSV)
- LTIMindtree:
  - Q4 FY26 https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2026/04/earnings-call-transcript-q4fy26.pdf
  - Q1 FY27 https://www.ltimindtree.com/content/dam/ltimcorporatewebsite/uploads/investors/2026/07/earnings-call-transcript-q1fy27.pdf
  - Q1 FY24, Q3 FY24, Q2 FY25, Q2 FY26, Q3 FY26: audit CSV
- Cognizant (cognizant.q4cdn.com):
  - Q3 CY24 https://cognizant.q4cdn.com/123993165/files/doc_financials/2024/q3/00/CTSH-Q3-2024-Earnings-Call-Transcript.pdf
  - Q4 CY24 https://cognizant.q4cdn.com/123993165/files/doc_financials/2024/q4/CTSH-Q4-2024-Earnings-Transcript.pdf
  - Q2 CY25 https://cognizant.q4cdn.com/123993165/files/doc_earnings/2025/q2/transcript/Transcript_CTSHQ2-2025-Earnings-Call.pdf
  - Q3 CY25 https://cognizant.q4cdn.com/123993165/files/doc_earnings/2025/q3/transcript/Transcript_CTSHQ3-2025-Earnings-Call.pdf
  - Q4 CY25 https://cognizant.q4cdn.com/123993165/files/doc_earnings/2025/q4/transcript/Transcript_CTSHQ4-2025-Earnings-Call.pdf
  - Q1 CY26 https://cognizant.q4cdn.com/123993165/files/doc_earnings/2026/q1/transcript/Transcript_CTSHQ1-2026-Earnings-Call.pdf
  - Q2 CY26 https://cognizant.q4cdn.com/123993165/files/doc_earnings/2026/q2/transcript/Transcript_CTSHQ2-2026-Earnings-Call.pdf
  - Q3 CY23 and Q1 CY24: audit CSV
- Wipro: Q2 FY24, Q3 FY24, Q2 FY25, Q1 FY27 transcripts (local `data/sources/wipro/`; links in `wipro_links_fy15_fy27.txt`)

### 5.2 Opened on the web in this session (by me)

- https://news.microsoft.com/source/asia/2026/06/03/infosys-tcs-and-wipro-scale-microsoft-365-copilot-to-over-300000-employees (re-verified the 86%, 91% and 95% figures, 29,000 agents and 250,000 FTE-days)
- https://www.sec.gov/Archives/edgar/data/1058290/000105829026000039/exhibit9919302026.htm (Cognizant Q3 CY26: >50% of code AI-assisted, 95,000 certifications, headcount 359,900)
- TCS Q1 FY27 transcript URL from the brief: HTTP 403, so the repo copy was used

### 5.3 Opened by the sub-agents

All URLs are in Appendices A and B below, which hold their notes verbatim.

---

## Appendix A — sub-agent notes: firm disclosures (Q2 FY27 calls, annual reports, Microsoft releases, surveys, BPO)

### Firm-level AI adoption / productivity disclosures — notes (compiled 2026-11-07)

Conventions: "primary" = read in company document (transcript, filing, press release, annual report) opened directly; "press-only" = number seen only in press article opened; "snippet-only" = seen only in search-result snippet, page not opened/verified.

#### A. October 2026 (Q2 FY27 / Q3 CY26) results

##### TCS Q2 FY27 — earnings call transcript (call Oct 8? 2026; filed Oct 14, 2026)
URL opened (downloaded PDF, 28pp): https://nsearchives.nseindia.com/corporate/TCS_CORPCS_14102026155941_SEInt14102026_signed.pdf
- Headcount: "This quarter, we continue to invest in future-ready talent, onboarding top talent globally, taking our workforce to 598,056 associates." (Sudeep Kunnumal, p.7)
- Learning: "Our learning hours saw a 17% QoQ increase to 17.1 million hours." (p.8)
- AI revenue: "Annualized AI revenue reached $3.1 billion and crossed 10% of our overall revenue." (Krithivasan p.2); Q&A: "This quarter, we saw AI revenue grow by 19%, while the traditional non-AI revenue declined" (analyst Ruchi Mukhija, p.13 — analyst's statement, not mgmt).
- Deflation (qualitative only): Krithivasan: "I don't want to say it is complete, Sudheer, on one hand, there is a deflation because of the productivity benefit." (p.11) ; "I don't want to conclude by saying that the deflation part is complete"
- Samir Seksaria: "there would be some front-loading of productivity benefits that could happen. But at the same time, we are seeing better pricing on the AI revenues we are generating. And if you take the revenue per employee, you will see there's a slight reduction, not a significant one." (p.18)
- Case-level: "Our approach, supported by TCS' agentic platform, targets 25% to 30% faster implementation." (S/4HANA programme, 27 sites) ; HR ops client: "double operational efficiency and increase self-serve adoption from less than 10% to 30%."; "21 Forward-Deployment Engineers are now working directly with business on executions." (p.7)
- Freshers: "We onboarded 10,000 graduates from the University this year globally" [sic]; analyst: "we added 14,000 freshers last quarter, we've added 10,000 in this quarter, and our net addition is just 13-odd thousand people over the last two quarters"
- NO number on trained/certified, licences, agents count, % code AI-generated, tickets in this transcript.

TCS Q2 FY27 press release (tcs.com PDF): https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2026-27/q2/IFRS/Press%20Release%20-%20USD.pdf — 403 blocked (curl and WebFetch). Search snippet only: "This quarter our employee base reached over 598,000, while attrition remained stable at 13.3%" and "sequential increase in learning hours to 17.1 million" (snippet-only; consistent with transcript). No AI-trained number seen. A search-summary claim that TCS Q1 FY27 PR said it would "equip 50,000 associates" was NOT verified (snippet-only, ambiguous).

##### Infosys Q2 FY27 (Oct 23, 2026) — SEC 6-K, accession 0001067491-26-000044
Index: https://www.sec.gov/Archives/edgar/data/1067491/000106749126000044/ (opened via index.json)
- EX-99.5 earnings call transcript: https://www.sec.gov/Archives/edgar/data/1067491/000106749126000044/exv99w05.htm
- EX-99.3 media conference transcript: https://www.sec.gov/Archives/edgar/data/1067491/000106749126000044/exv99w03.htm
- EX-99.4 fact sheet: https://www.sec.gov/Archives/edgar/data/1067491/000106749126000044/exv99w04.htm
- EX-99.1 USD press release: https://www.sec.gov/Archives/edgar/data/1067491/000106749126000044/exv99w01.htm
(infosys.com PDFs 403 to curl/WebFetch.)

Quotes:
- Headcount (fact sheet): "Total employees 332,542 [Sep 30 2026] 328,062 [Jun 30 2026] 331,991 [Sep 30 2025]"; S/W professionals 314,508.
- Call (CFO): "Net headcount increased by about 4,400 employees." "We hired about 13,000 freshers in H1 in line with our target of approximately 20,000 for FY27." Salil: "8,000 in the quarter and 20,000 for the full year."
- AI revenue: "Our AI revenue was standout at 10.5% of our total revenue, growing 29% sequentially." CFO: "the first number that we had published was on our AI Day for Q3 of last year, which was 5.5%."
- Coding tools (media call, Uma Kannan Q): "Last time, you said 80,000 employees are working on coding tools. I mean, what is it happening now? Like are there any increase in numbers?" Salil Parekh: "Yes. So that number is increasing. Also, what we are doing is the certification numbers are going up, the people who are getting trained are going up." -> NO new number given; 80,000 refers to the Q1 FY27 disclosure (user already has).
- Training qualitative: "Then we have people who have been trained and certified on the different model technologies and on different capabilities with our partner companies." ; "we have the certification and training, which is quite extensive within our system. We are building out the FDE capability." ; media: "plus all the training that we have done for all of our people, which many and more are certified now"
- Topaz Fabric: "we have 15 different foundation models where a client can choose ... so you can do the Sonnet or you can do the Fable"
- Effort reductions (case examples, call prepared remarks): "The result was 40% faster time to market, 80% less rework and 30% more defects caught before go-live." ; "by embedding AI agents into the software modernization lifecycle, we helped an education technology company modernize its aging platform with significantly lower risk and effort, achieving 40% effort reduction"
- Productivity pass-through/deflation: "H2 margins will be impacted by compensation hikes, softer revenue seasonality, continued sharing of AI driven productivity benefits and ramp-up of large deals." ; "across the client base, there is demand or request requirement, which is focused on productivity benefits from the AI that are getting passed on." ; "Expectations for AI-led productivity commitments are increasing competitive intensity and reshaping commercial model." ; "I think what we see is the effect or the expectation on the productivity is about similar." ; "if that has already happened, then vast majority of the benefit of the AI productivity is already baked in." ; media: "Now there are sometimes asks that are much higher than what we can derive from the AI productivity, which is where we say that it does'nt fit our economic profile." ; "AI is helping clients improve productivity, but it can also reduce traditional billable work." (journalist Q) ; "once you finish with all the work that you are doing through productivity, it is done."
- Offshore shift: onsite effort 22.6% (Q2 FY27) vs 23.2% (Q2 FY26); "we will have offshoring impact of 1%" (guidance).
- Cyber: "half of these cyber vulnerabilities are being uncovered by employees or by agents" (context: client vulnerability discovery).

##### HCLTech Q2 FY27 — earnings call Oct 12, 2026 (transcript filed Oct 15, 2026)
URL opened (PDF downloaded): https://www.hcltech.com/sites/default/files/document/open/call-trans/2026-10/CallTrancript.pdf
- Headcount: "Our people count stood at 230,339 as of the end of last quarter, a net increase of 6,450 sequentially." (press: 6,136 freshers in Q2 — snippet-only)
- Productivity proxy: "Revenue per employee improved by 2.4% YoY, a clear sign that our AI strategy is improving productivity across the business."
- Deflation: "You can also see that we are able to offset AI-driven deflation by gaining market share in our core services and through our Advanced AI offerings"
- AI revenue: "Advanced AI revenue reached $219 million this quarter, up 28.4% sequentially and 78% YoY. And the annualized Advanced AI revenue is now $876 million." ; "Our agentic AI offerings has crossed $100 million per quarter this quarter."
- Agents: "AI Force Agent Store now offers 900- plus agents, enabling reuse of proven capabilities and greater autonomy across enterprise workflows." (catalogue of agents, not deployed count)
- Case: "It averaged 87% accuracy for an estimated 9x productivity gain." (core-banking spec-to-code agent, "about 10 minutes per routine")
- Margin: "Project Ascend, including AI-driven efficiencies, gave us 73 basis points" (QoQ EBIT bridge)
- Anthropic: "Today, we announced a global Premier partnership with Anthropic ... HCLSoftware will become an Anthropic ISV partner, embedding Claude and Claude Code into select enterprise products" — no seat number.
- Talent (qualitative, no numbers): "We continue to enable our employees to become AI builders, AI super users, and AI operators." ; "We are developing a centralized FDE Academy with tracks aligned to OpenAI, Anthropic, AWS, Google, and NVIDIA."
- NO numbers on trained/licensed/active users, % code, tickets.

##### Wipro Q2 FY27 — call Oct 15, 2026
Transcript opened (PDF, 15pp): https://www.wipro.com/content/dam/nexus/en/investor/quarterly-results/2026-2027/q2fy27/q2fy27-earnings-transcript.pdf
SEC 6-K (CIK 1123799) acc. 0001193125-26-426841: press release EX-99.1 https://www.sec.gov/Archives/edgar/data/1123799/000119312526426841/d188224dex991.htm ; highlights EX-99.5 https://www.sec.gov/Archives/edgar/data/1123799/000119312526426841/d188224dex995.htm
- Headcount (EX-99.5): "TOTAL HEADCOUNT 236,328 ATTRITION VOL – TTM 13.8% NET UTILIZATION EXCLUDING TRAINEES 83.4%". Analyst: "the 6,500-plus people being cut in this quarter" (press: fell by 6,716).
- Deflation timing (CFO Aparna Iyer): "Typically, our contracts are about 2 to 2.5 years in terms of the average tenor, right? And we've been in this cycle for at least last 2 years and or thereabouts, 1.5 to 2 years. So in some sense, a lot of the contracts that we've had have been refreshed and renewed. So in some sense that we should be at that inflection curve in a few quarters."
- CHRO Saurabh Govil on headcount: "From the headcount, if you look at it, year-on-year it's flattish. ... first half, we didn't go on campus. ... We're also driving productivity from AI projects."
- Srini Pallia (BFSI): "AI and data investments are growing meaningfully. And you know, some of them are through reallocation, and some of them are through productivity takeout."
- NO numbers on trained/licensed/active users, agents count, % code, tickets in transcript or press release.

##### Tech Mahindra Q2 FY27 — call Oct 15, 2026
Transcript opened (PDF, 20pp): https://insights.techmahindra.com/investors/tml-q2-fy-27-earnings-transcript.pdf
Press release opened (PDF, 8pp): https://insights.techmahindra.com/investors/tml-q2-fy-27-press-release.pdf
- TRAINED / SKILLED / CERTIFIED (Mohit Joshi, prepared remarks): "More than 24,000 IT associates have been upskilled on AI productivity tools, over 4,500 have been skilled on agent platforms, and approximately 48,000 hold an AI certification."
- "We have curated a special internal course to ensure 200 engineers get trained in the next quarter on some deep techniques to hone models and harnesses."
- "AI Velocity Cells ... has already delivered 16 client-relevant capstones in seven weeks"
- Press release: "'Build with Gemini', a Google Cloud hands-on workshop rolled out to12,500+ associates worldwide" [sic]
- Headcount (PR): "Total headcount at 152,206 • LTM IT attrition at 11.7%"; boilerplate "With 146,000+ professionals across 90 countries".
- Effort/deflation: "In some areas, automation will reduce the effort required to deliver existing services and may put pressure on effort-based revenue models." ; "Traditionally, ADMS, while it has grown very well this quarter, 7.6% year-on-year, that business is actually seeing the productivity expectations on large contract renewals." ; "differentiated AI toolchain resulting in lesser greater productivity and lesser head-count requirements, therefore feeding back into our growth as those people are released from existing fixed-price projects." ; "I feel that clients, whether or not they deliver productivity internally, will continue to expect productivity from their partners and from their vendors."
- Pricing: "about three quarters back, we had spoken about how we had come out with a pricing mechanism which could price for both the human and agents working together ... we are pricing the tokens as well when we are looking at agent pricing along with the human in the loop."
- Analyst Q (Sudheer Guntupalli) cited "AI coding tools like Claude Code have been seeing stagnation in their ARR" — analyst claim, Joshi declined to comment; "this whole deflation debate is completely warped".
- Margin: "there was a gap of at least 3% to 4% on margin that could have been driven by pyramid rationalization, which we've not really exercised"

##### LTM (formerly LTIMindtree) Q2 FY27 — call Oct 16, 2026 (transcript filed Oct 22, 2026)
Transcript opened (PDF, 32pp): https://nsearchives.nseindia.com/corporate/LTI_22102026115536_Stockexchangesigned_1.pdf
- Headcount: "At the end of Q2 FY2027, total headcount stood at 88,835, reflecting a net addition of 949 employees sequentially." "Total fresher additions for the quarter were 1,743." Utilization ex-trainees 86.4%.
- TRAINED/CERTIFIED: "Our AI 1,000 program to develop Forward Deployed Engineers is on track, with nearly 1,000 employees in mentor-led and persona-based journeys, and 2,000 plus certifications across Claude, Gemini, Copilot, and Azure AI."
- Tools (no seat count): "Through our partnership with Anthropic, we have now fully embedded Claude and Claude Code into our BlueVerse™ AI delivery fabric." ; "We partnered with Cognition to bring its software engineering agent, Devin into BlueVerse™ RightLogic."
- AI revenue: "AI revenue for the quarter has reached 13.4% of our overall revenue, a growth of 40% year-over-year." "Including enterprise AI, cumulative AI revenue grew 47% year-over-year."
- Effort cases: "we deployed 12 specialized AI agents across the SDLC, as part of the large-scale payment modernization program, reducing the delivery cycle time by 50% and cumulative development effort by 38%." ; HR agent "has the potential to reduce HR tickets by 40% through agent-led self-service." ; marketing content "generated 50% productivity gains and enabled 10x faster campaign launches." ; water ops "reduced manual effort by 50% and enabled 2x faster recovery."
- DEFLATION (Q from Girish Pai: "You talked about deflation to the tune of some 25% [at analyst meet]. Where do we think we are in the deflation cycle?"). Venu Lambu: "And there was 60% of the total, sort of adoption towards productivity headwinds has already been, passed on to the customers at different phases." ; "With regard to the LTM, big clients, we are done with it which essentially means probably 60%- 70 % of our portfolios, we are done with it. And there will always be 20%, 30% of the portfolio, which will go through different renewal cycles ... But I would expect from an industry standpoint, this will go on for a couple of years."  [Note: the "~25% deflation" figure is the analyst's paraphrase of an earlier analyst-meet remark; Lambu did not dispute it on this call.]
- Analyst (Rishi Jhunjhunwala): top BFSI client "talked about tech vendor spends being down 30% year-on-year as a result of AI adoption and otherwise insourcing"; Lambu: consolidation "from 50 plus vendors to about five vendors" ... "we already called out the productivity headwinds that we will have to bear for the first two quarters ... we are done with that productivity headwind."
- Lambu: "in the whole of last year as well, when we delivered, we did not increase the headcount"

##### Cognizant Q3 CY2026 — results Oct 29, 2026
8-K acc. 0001058290-26-000039. Press release EX-99.1 opened: https://www.sec.gov/Archives/edgar/data/1058290/000105829026000039/exhibit9919302026.htm ; earnings supplement EX-99.3 opened: https://www.sec.gov/Archives/edgar/data/1058290/000105829026000039/exhibit9939302026.htm
- CODE SHARE + CERTS (Ravi Kumar S, press release): "We are making that transition alongside our clients, with over 50% of our code now AI-assisted, over 95,000 frontier AI badges and certifications earned by our associates and continued improvement in revenue and adjusted operating income per employee." (Supplement slide: "95,000+ frontier AI badges and certifications")
- Headcount: "Total headcount as of September 30, 2026 was 359,900, an increase of 3,200 from June 30, 2026 and an increase of 10,100 from September 30, 2025." Attrition TTM 12.6%.
- "Expanded its partnership with Google Cloud by establishing a new Gemini Frontier Capability Group backed by 18,000 dedicated Cognizant associates."
- Devin case: "A seven-person Cognizant team used Devin to handle the legacy conversion. Delivery throughput rose by roughly a third and Odyssey recorded a 37 percent net cost saving against the conventional approach."
- TriZetto: "Workflow Agentic Processing capability lets AI agents carry out a health plan's standard operating procedures to automate processing of eligible routine pending claims"
- Project Leap: "reshaping productivity through competitive offerings and upskilling our workforce ... We now expect to record total costs of $180 million to $250 million"
Call transcript NOT opened (roic.ai 403; not on EDGAR). Press coverage of call opened: https://www.crnasia.com/india/news/2026/cognizant-q3-earnings-we-view-agentic-ai-as-the-most-significant-enterprise-opportunity-since-digitisation-ceo-says  (PRESS-ONLY figures):
  - "over 50 percent of the company's software development is AI-assisted as of the end of Q3"
  - "Cognizant has over 8,500 AI engagements"
  - "Over 45,000 Cognizant associates have earned over 95,000 certifications across frontier AI platforms" "with another 65,000-plus associates in progress"  -> denominator for the 95,000 badges = 45,000 people (press-only)
  - "over 55,000 associates complete Build with Gemini"
  - SkillSpring (AI-native learning platform) "used by approximately 315,000 associates"
  - Talcott programme "delivers 30 percent productivity gains"
  - "Revenue per associate, excluding GenC trainees, increases over 3 percent"; "adjusted operating income per associate increases more than 5 percent"
- Snippet-only (search summary): Q3 2025 call "Approximately 30% of internal code was AI-generated in the quarter, with longer-term potential to reach 50%"; "Over 250,000 associates trained in AI-related skills" (user already has 2025 calls, presumably).

#### B. Annual reports / 20-F / 10-K

##### Infosys 20-F FY2026 (filed 2026-06-15) — opened: https://www.sec.gov/Archives/edgar/data/1067491/000119312526270520/infy-20260331.htm
- "In FY26, 81.8% of our workforce trained with annual employee learning hours averaging at 113.3 hours. Cumulatively, 84% of our workforce is now AI‑aware, reflecting strong progress in future‑ready skills."
- Denominator: "As of March 31, 2026, we had 328,594 employees, of which 310,887 were professionals involved in service delivery to clients, including trainees." (84% x 328,594 ≈ 276k — my arithmetic)
- "In FY26, 10,766 fresh graduates completed the training at Global Education Center (GEC) campus, Mysore"; "Generative AI and prompt engineering courses have been introduced to ensure freshers are adept in the new skills."
- No licence/coding-tool/code-share numbers found in 20-F FY26 text.
##### Infosys 20-F FY2025 (filed 2025-07-01) — opened: https://www.sec.gov/Archives/edgar/data/1067491/000095017025091925/infy-20250331.htm
- "Over 270,000 of our employees today are AI-aware." ; "Over 2,75,000 of our people are trained on AI at different levels of proficiency." ; "500+ sales personnel have been certified on AI application for Growth from Kellogg School of Business"
- Denominator: 323,578 employees at March 31, 2025 (stated in FY26 20-F).

##### Wipro 20-F FY2026 (filed 2026-06-02) — opened: https://www.sec.gov/Archives/edgar/data/1123799/000119312526253514/wit-20260331.htm
- ACTIVE TOOL USE: "Across our delivery teams, we have over 60,000 associates leveraging AI developer tools, boosting our overall productivity."
- "We are actively building an AI-ready workforce covering over 240,000 employees ... We have enabled over 180 AI learning pathways"
- TRAINED (tiers): "Over 2,12,663 associates have completed GenAI training across three tiers - (i) 33,000+ at the basic level; (ii) 85,000+ at the advanced level; and (iii) 93,000+ at the master level"
- Account academies: "overall skilling coverage of 91.8% (78k/85k) associates"
- Op levers: "Using next-generation technology including GenAI to drive automation"
##### Wipro 20-F FY2025 (filed 2025-05-22) — opened: https://www.sec.gov/Archives/edgar/data/1123799/000095017025076303/wit-20250331.htm
- ACTIVE TOOL USE: "Across our delivery teams, we have over 20,000 associates leveraging AI developer tools, boosting our overall productivity."
- "We are actively building an AI-ready workforce covering over 230,000 employees ... We have enabled over 50 AI learning pathways"
- => Wipro associates using AI developer tools: 20,000+ (FY25, ~Mar 2025) -> 60,000+ (FY26, ~Mar 2026). Denominators: ~230k / ~240k "employees" (boilerplate).

##### Cognizant 10-K FY2025 (filed 2026-02-12) — opened: https://www.sec.gov/Archives/edgar/data/1058290/000105829026000008/ctsh-20251231.htm
- TRAINED: "AI skill building is a core focus – from July 2023 to end of 2025, we have upskilled more than 330,000 associates on GenAI via more than 1,000 learning programs."
- TOOLS (no seat count): "We encourage learning through experimentation by providing access to leading AI tools, including Microsoft Copilot, GitHub CoPilot, Google Gemini Code Assist and Windsurf."
- "In 2025, Cognizant achieved a GUINNESS WORLD RECORD™ for the largest online GenAI hackathon by hosting a global Vibe Coding Week. Associates were given access to leading vibe coding tools ... producing more than 30,000 prototypes."
- "We are redesigning career paths to transition roles highly impacted by AI to higher value roles"
- Headcount: "We finished 2025 with approximately 351,600 employees as compared to 336,800 employees at the end of 2024."
##### Cognizant 10-K FY2024 (filed 2025-02-12) — opened: https://www.sec.gov/Archives/edgar/data/1058290/000105829025000017/ctsh-20241231.htm
- "more than 168,000 associates, including 1,700 leaders, have taken generative AI trainings in 2024, including through Cognizant's Synapse program." ; "In 2024, more than 277,000 employees acquired at least one skill through our learning ecosystem." Headcount end-2024: 336,800.

##### TCS annual report FY2026 (Integrated AR 2025-26, released ~May 15 2026)
- tcs.com AR PDFs return 403. Opened BRSR FY2026 exchange filing (part of IAR): https://d162horukp7uyq.cloudfront.net/17dac84832edeef8eb8f90cee0f3dfe5f8a0d8f7779ccc12cc2b62ee60ca3984.pdf — only gives employees: "Permanent ... 5,84,519 ; Other than Permanent 32,918 ; Total 6,17,437" (end FY2026). No AI-skill numbers in BRSR.
- PRESS-ONLY (The Federal, 16 May 2026, AGM/AR coverage): https://thefederal.com/category/business/tcs-targets-global-ai-leadership-as-130-top-clients-choose-its-ai-services-243323 — "Krithivasan stated that over 2,70,000 employees now possess advanced AI skills, a threefold increase from the previous year."
- SNIPPET-ONLY: Q4 FY26 PR "270k+ with higher proficiency in AI/ML"; Q1 FY26 "114,000 people with higher order AI skills"; Q3 FY26 "over 217,000 associates with advanced AI skills"; "69 million learning hours" FY2026. (User has these calls.)

##### Vendor press releases (coding assistants / Copilot)
1. Microsoft Source Asia, Dec 11, 2025 — opened: https://news.microsoft.com/source/asia/2025/12/11/cognizant-infosys-tcs-and-wipro-emerge-as-frontier-firms-with-microsoft-deploying-copilot-and-agentic-ai-across-the-enterprise/
   - "Each of these companies will deploy over 50,000 Microsoft Copilot licenses" ; "The four companies will collectively deploy over 200,000 Microsoft Copilot licenses"
   - Wipro: "With over 50,000 Copilot licenses deployed and more than 25,000 employees upskilled"
   - TCS: "TCS has equipped tens of thousands of its professionals with Microsoft AI solutions." "All TCS employees now have a personalized AI Coach"
2. Microsoft Source Asia, June 3, 2026 — opened: https://news.microsoft.com/source/asia/2026/06/03/infosys-tcs-and-wipro-scale-microsoft-365-copilot-to-over-300000-employees
   - Each of Infosys, TCS, Wipro >100,000 employees on M365 Copilot; "taking the collective commitment past 300,000 seats in under six months."
   - Infosys: "is seeing significant expansion with over 91% monthly active users."
   - TCS: Krithivasan: "At TCS, we have empowered over 100,000 associates with Microsoft 365 Copilot to enhance everyday productivity"; "86% of Copilot‑licensed associates actively use AI in their daily work." ; "20–25% productivity improvements in research and content production tasks." ; "25–35% reduction in selective work-cycle time through AI-assistance."
   - Wipro: "Wipro has reached over 95% monthly active usage of Microsoft 365 Copilot" "with associates generating 7.5 million prompts each month and averaging 23 actions per user per week." ; "translat[es] into more than 250,000 FTE days saved every quarter." ; "more than 29,000 end-user developed agents and over 60 enterprise-grade agentic solutions now in use" ; "appraisal agent reducing performance review effort by nearly 70%"
   - NOTE: M365 Copilot = office assistant, NOT a coding assistant.
   - Press echo: PeopleMatters June 4 2026 https://www.peoplematters.in/news/ai-and-emerging-tech/infosys-tcs-and-wipro-now-have-300000-employees-using-copilot-as-ai-moves-into-daily-work-50090
3. TCS–Anthropic, June 11, 2026 — press release text opened via syndication: https://www.analyticsinsight.net/press-release/tcs-and-anthropic-launch-global-premier-partnership-to-drive-enterprise-ai-scaling (tcs.com 403)
   - "TCS will equip 50,000 associates across engineering, finance, legal, marketing, and sales" (enterprise-wide Claude licensing). Claude Code named for "BFSI Products and Platforms teams" (software engineering, IT ops) — no separate Claude Code seat count.
4. Cognizant–Microsoft, Apr 22, 2024 — opened: https://news.microsoft.com/source/2024/04/22/cognizant-and-microsoft-announce-global-partnership-to-expand-adoption-of-generative-ai-in-the-enterprise-and-drive-industry-transformation/
   - "Cognizant purchased 25,000 Microsoft 365 Copilot seats for Cognizant associates" "along with 500 Sales Copilot seats and 500 Services Copilot seats"
   - "35,000 Cognizant developers have been trained on Github Copilot" "with an additional 40,000 developers slated to receive training" (TRAINED, not licensed)
5. HCLTech–OpenAI, June 30, 2025 — snippet-only (not opened): internal ChatGPT Enterprise rollout; "workforce of over 223,000 employees" (no seat count found). https://www.hcltech.com/press-releases/hcltech-and-openai-collaborate-drive-enterprise-scale-ai-adoption
6. Infosys GitHub Copilot 2024 — snippet-only: "more than 18,000 developers ... generated over 7 million lines of code using GitHub Copilot" (Infosys–Microsoft expansion, 2024; not opened).

##### HCLTech Annual Report FY2026
- Corporate profile PDF opened: https://www.hcltech.com/sites/default/files/en/corporate/3098/annual-report-corporate-profile-2025-26.pdf
  - CEO letter: "In FY26, we trained over 144,000 employees in GenAI, including 11,800 certified AI Builders and more than 700 certified blackbelts."
  - Headcount table: "FY26 227,181 [employees] 11,744 [freshers added]; FY25 223,420 7,829; FY24 227,481 12,141"
- MD&A PDF opened: https://www.hcltech.com/sites/default/files/en/corporate/3098/annual-report-mda-2025-26.pdf
  - "This initiative has reached over 144,000+ unique employees, with approximately 63,000 individuals advancing through specialized proficiency levels and more than 11,000 attaining the substantial expertise required to drive AI use-case realization ... over 700 Blackbelt-certified practitioners"
  - "These risks are amplified by rapid shifts in client expectations and AI-driven productivity baselines, which can quickly obsolete traditional IT services offerings."
- AR web page opened: https://www.hcltech.com/hcl-annual-report-2025/artificial-intelligence (now serves FY26 content): "144 K+ Employees trained on GenAI 1000 + AI agents 1000 + AI Lab projects delivered to date ... *as of March 31, 2026"; "Agentic AI-driven Talent Navigator ... enabling 40% faster hiring fulfillment"
- FY25 figure SNIPPET-ONLY: "In FY25, we trained over 106,000 employees in AI/GenAI."

##### Tech Mahindra Integrated Annual Report FY2025-26 — opened (PDF): https://insights.techmahindra.com/investors/tml-integrated-annual-report-fy-2025-2026.pdf
- "Approx. 80% of all associates are Ai-enabled through learning • Over 84% of client-facing associates allocated to Billed Projects have undergone Ai-related enablement" (p.124)
- "Training and development highlights in FY26: • 45,000+ associates were trained or certified in AI • ... 9,500+ certified on Hyperscalers like AWS, Google, and Microsoft"
- Agents: "Orion was launched on three hyperscaler marketplaces, with a growing library of more than 350 service and industry-specific agents available out of the box." (catalogue)
- Case: "GenAI-led BRD and test case generation, reducing manual effort by 18–20% ... achieved 15–30% effort savings in coding and test case creation"
- Case: "saving over 102,000 hours annually" (repair automation + Legal Assistant Bot, Azure OpenAI)
- Headcount: "147,623 Total employees 140,216 (TML+ Integrated Companies) + 7,407 (Subsidiaries)" (FY26)
- Margin levers: "Project Fortius ... actions across pricing, productivity in fixed-price engagements, optimisation of subcontractor costs"
- SNIPPET-ONLY (multibagg third-party summary, NOT found in AR text by my grep): "76% have completed advanced AI training and achieved AI certification" — treat as unverified.
##### Tech Mahindra Integrated Annual Report FY2024-25 — opened (PDF): https://insights.techmahindra.com/investors/tml-integrated-annual-report-fy-2024-2025.pdf
- "Over 12,000 of our employees are certified in AI across hyperscalers."
- Client case: "AI-enabled auto-healing techniques optimised IT operations, resulting in automated remediation of 38% of the incident tickets"
- PRESS (snippet-only): PeopleMatters (2025) CEO "Over 77,000 employees have already been trained in AI and generative AI capabilities."
##### Tech Mahindra BRSR FY2026 downloaded (https://insights.techmahindra.com/investors/tml-brsr-fy2026.pdf) — not separately mined.

#### C. Sector surveys (India)
1. Nasscom Annual Strategic Review 2026 press release (Feb 24, 2026) — opened PDF: https://d3r3sr3o54kk15.cloudfront.net/s3fs-public/media_pdf/India%E2%80%99s%20tech%20industry%20continues%20to%20redefine%20AI-led%20transformation%2C%20efficiency%20and%20skilling--%20Nasscom%20Annual%20Strategic%20Review%202026.pdf
   - "Workforce: industry continued to be a net hirer, with net employee growth ~2.3%; 2 Mn+ professionals upskilled in AI (including 200k–300k in advanced AI)" [TRAINED; denominator ~5.8 Mn industry headcount FY25 per search summary, snippet-only]
   - "'Human + AI' becomes the operating model"
2. Microsoft & LinkedIn Work Trend Index 2024 India (May 16, 2024) — opened: https://news.microsoft.com/source/asia/2024/05/16/92-of-indian-knowledge-workers-use-ai-in-the-workplace-finds-microsoft-and-linkedin-2024-work-trend-index/
   - "Ninety-two percent of knowledge workers in India use AI at work as compared to the global figure of 75%" ; "72% of Indian AI users are bringing their own AI tools to work (BYOAI)." [ACTIVE (self-report, any use), all knowledge workers, not IT-specific; global n=31,000/31 countries]
   - WTI 2025 India: snippet-only — ">75% of Indian knowledge workers already use AI at work" (Entrepreneur India; unconfirmed); "93% of Indian leaders plan to use AI agents within 12-18 months" (Business Today Aug 20 2025; snippet-only)
3. EY 2025 Work Reimagined Survey — PRESS-ONLY (PeopleMatters, Dec 24 2025): https://www.peoplematters.in/news/ai-and-emerging-tech/62percent-of-indian-employees-use-genai-regularly-as-workplace-adoption-surges-ey-47821 — "62% of Indian employees report frequent use of GenAI tools"; global sample "15,000 employees and 1,500 employers across 29 countries"; no sector split.
   - snippet-only: "up to 77% of Indian knowledge professionals currently utilise generative AI on a daily basis, up from 46% in 2024" (IANS-sourced; source survey unclear)
4. ANSR–Talent500 "AI Advantage Survey 2025" — SNIPPET-ONLY for numbers: "44%" of India tech/GCC workforce use AI daily, "another 36% tap into AI occasionally"; ">3,000 professionals across India's GCCs"; coding top use case (68%); ">60% cite 25–50% productivity gains". Publisher blog opened (https://talent500.com/blog/ai-advantage-report-2025-india-future-of-work, Oct 30 2025) only states "43.8% of professionals consider AI 'a core part of their work'" and "One in two professionals say AI is helping them meet their OKRs faster." [ACTIVE self-report; GCC sample, not IT services firms]
5. Nasscom–BCG women in tech (Aug 2024) — snippet-only: "One in five women use GenAI tools almost daily"; "76% of male professionals and 80% of female professionals in India use GenAI".
6. Stack Overflow 2025 — snippet-only: India "highest proportion of developers expressing some or significant trust in AI at 56%"; no India usage split found. GitHub Octoverse 2025 — snippet-only: >5M Indian devs joined GitHub in a year; "80% of new developers are using GitHub Copilot in their first week" (GLOBAL, not India).
Distinction: Nasscom 2M+ = trained; WTI 92% / EY 62% / ANSR 44% daily = self-reported active use (any AI, broad samples); none = licensed seats.

#### D. BPO firms
##### Genpact
- 10-K FY2025 (filed 2026-02-26) opened: https://www.sec.gov/Archives/edgar/data/1398659/000139865926000004/g-20251231.htm
  - "In 2025, our employees completed over 12.5 million learning hours, including an increase on time spent in technology and AI skilling by 1.5 times year-over-year. We now have more than 7,000 AI builders and nearly 20,000 AI practitioners, with more than 9,000 external certifications awarded in 2025"
  - "AI practitioners are domain experts who are trained to use AI in the flow of work for client processes."
  - "Our average headcount increased to approximately 146,000 in 2025 from approximately 135,400 in 2024."
- Q3 2026 press release (Nov 5, 2026) opened: https://www.sec.gov/Archives/edgar/data/1398659/000139865926000017/genpactltdexhibit991q326.htm — "Advanced Technology Solutions net revenues were $405 million, up 30.3% ... 29% of total"; "Core Business Services net revenues were $980 million, flat year over year". No adoption/agent-share metrics.
- Snippet-only (earlier calls): ">400 GenAI solutions in the market" (Q4 2025); Q1 2026 CEO: agentic revenues have "zero bearing on headcount"; Q2 2026: expects ">$1 billion in agentic TCV during 2026".
##### EXL
- Q3 2026 press release (Oct 27, 2026) opened: https://www.sec.gov/Archives/edgar/data/1297989/000129798926000028/exlq326pressrelease.htm — "Data and AI-led revenue, almost two-thirds of our business, grew 36% on a reported basis and 31% organically." ; "have over 74,000 employees". No adoption metric.
- 10-K FY2025 opened: https://www.sec.gov/Archives/edgar/data/1297989/000129798926000008/exls-20251231.htm — only "increase in investments in digital and generative AI capabilities of $2.8 million" (SG&A); no workforce AI metrics found.
- Snippet-only: Q3 2025 call ">65 AI agents autonomously manage data modernization..."; iMerit Scholars ">30,000 domain experts".
##### Concentrix
- 10-K FY2025 (FYE Nov 30 2025) opened: https://www.sec.gov/Archives/edgar/data/1803599/000180359926000027/cnxc-20251130.htm — "a team of approximately 455,000 employees and staff"; "the transition of lower complexity support to online and self-support options, driven by heavy automation and the increased use of new technologies, reduces volumes in the voice channel."; "In 2025, we launched our Next Wave AI-readiness accreditation course, a five-part training" (no count). No share-of-interactions-by-AI number.
- Q3 FY2026 PR (Sep 29, 2026) opened: https://www.sec.gov/Archives/edgar/data/1803599/000180359926000147/exhibit991q32026.htm — boilerplate only.
##### Firstsource Q2 FY27 — call Oct 29, 2026; transcript opened: https://media.firstsource.com/Landing-pages/Investor%20Relation/Investor%20relations%20PDF%20&%20Reports/Financial-Information/FY2026-2027/Q2/EarningsCallTranscript-Q2FY27.pdf
- "Voice AI is live across our eligibility, patient access, and collections offerings, and Denials AI continues to gain traction."
- "about 80% of the gross hiring that we are doing today is offshore or nearshore. India and the Philippines accounted for about 85% of the Q2 hirings. We are seeing productivity from AI and automation in existing accounts alongside non-linear pricing. ... more than 50% of our business is nonlinear in nature"
- Deflation: "in a couple of our existing customers where we've had renewals, I think we've been able to come out of that exercise despite having some deflation in the existing scope of work, still be able to maintain the revenue base at neutral"
- Analyst: "roughly 3,000 odd employees [added] during quarter 2"
- No % of interactions handled by AI.
##### eClerx Q2 FY27 — SNIPPET-ONLY: "over 280 employees now Claude AI certified"; delivery headcount 23,151.
##### Teleperformance — SNIPPET-ONLY: plans "to embed AI in workflows for 500,000 employees" (cryptobriefing); TP.ai FAB "500+ AI projects"; no interaction share found.
##### Not covered (time): WNS/Capgemini, HGS, iEnergizer — no searches run.

#### SUMMARY TABLE (see handback message for same table)
(identical to returned table)


## Appendix B — sub-agent notes: delegation / success-rate benchmarks

### Deployed delegation / acceptance-rate evidence (compiled 2026-11-07)

Status legend: PRIMARY = I opened the company/author/vendor page itself; PRESS = only seen in press coverage I opened; SNIPPET = only in search snippet.

#### Line 1: Software / code

##### Google (Alphabet) share of new code AI-generated
- URL opened: https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/cloud-next-2026-sundar-pichai/ (Sundar Pichai, Cloud Next '26, 22 Apr 2026)
- Quote: "Today, 75% of all new code at Google is now AI-generated and approved by engineers, up from 50% last fall."
- PRIMARY. Population: Google internal. Definition: share of "new code" "AI-generated and approved by engineers" (not codebase; measurement unit not specified - earlier Google research used characters).
- Earlier: Q3 2024 call ">25%" (Fortune press, not opened); Oct 2025 "nearly half" (snippet only).

##### Agentic PR merge rates (GitHub, AIDev dataset)
- URL opened: https://arxiv.org/html/2507.15003 (Li, Zhang, Hassan, "The Rise of AI Teammates in SE 3.0", v1 20 Jul 2025)
- Population: AIDev dataset, 456,535 PRs by 47,303 developers across 61,453 repos; cut-off 22 Jun 2025.
- Text: "OpenAI Codex achieves the highest acceptance rate at 64%, followed by Devin at 49% and GitHub Copilot at 35%"; Table 5 "%Accepted": Human 76.8%, Codex 65.3%, Devin 48.9%, Copilot 38.2%, Cursor 51.4%, Claude Code 52.5% (text vs table inconsistent; table denominators are closed PRs presumably). PRIMARY.
- URL opened: https://arxiv.org/html/2607.21832 (Mazloomzadeh, Morovati, Khomh, 23 Jul 2026)
- Population: 220,612 closed PRs from 489 popular Python repos; 9,428 agentic PRs; through 20 Nov 2025.
- Quotes: "Among the studied agents, Claude (84.3%) and Codex (73.5%) achieve the highest PRs merge probabilities." "Cursor ... estimated merge probability of 63.9%"; "Devin exhibits the lowest merge probability, with only 43% of its generated PRs being accepted." Copilot 59.6% (Table 3, model-adjusted). Human PR merge rate per quarter 0.840-0.856. Raw Table 1 counts: Codex 5,451/6,057 merged; Claude 166/219; Copilot 874/1,259; Cursor 291/541; Devin 512/1,355. PRIMARY.
- URL opened: https://arxiv.org/abs/2605.22534 (Peralta et al., 21 May 2026, "Why Are Agentic PRs Merged or Rejected?")
- 11,048 closed agentic PRs -> 9,799 human-reviewed. "Among merged PRs, 15.4% required explicit reviewer involvement through feedback or direct commits"; "only 35.7% of rejected PRs reflected clear agentic failures." PRIMARY (abstract).

#### Line 3: Customer support

##### Intercom Fin
- URL opened: https://fin.ai/ (accessed Nov 2026): Fin "averaging 76% across 12,000+ customers, with many seeing over 85%"; "2 million weekly resolutions". PRIMARY (vendor marketing).
- Definition URL opened: https://www.intercom.com/help/en/articles/8205718-fin-resolutions-how-are-they-measured : resolution counted when, following Fin's last answer, customer "confirms the answer was satisfactory" (confirmed) or "exit[s] the conversation without requesting further assistance" (assumed). Reopened -> "that resolution will be deducted and not charged". NB assumed resolutions included.
- Snippet-only: earlier 2026 figures 67% (7,000+ customers), 71%.

##### Klarna
- URL opened: https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/ (27 Feb 2024; first month after launch)
- "The AI assistant has had 2.3 million conversations, two-thirds of Klarna's customer service chats"; "equivalent work of 700 full-time agents"; "25% drop in repeat inquiries"; "resolve their errands in less than 2 mins compared to 11 mins previously". PRIMARY. Definition: "handles"/"conversations" (not resolution).
- Snippet-only: FY2025 annual report "80% of all customer service chats" (via WhiteSight); Nov 2025 "work of 853 full-time agents", $60m saved (press).

#### Line 4: Back office

##### Ardent Partners State of ePayables 2025
- URL opened: https://payablesplace.ardentpartners.com/2026/01/state-of-epayables-part-nine-ap-benchmarks-and-best-in-class-performance/ (Jan 2026)
- "The invoice exception rate for AP departments is, on average, 18.4%." Best-in-class "process more than 1.8 times as many of their invoices in a straight-through manner than their peers"; average cost $9.84/invoice; cycle time 8.2 days. No touchless % in blog post; no AI attribution. PRIMARY (blog summary of report).
- Snippet-only: best-in-class touchless 49.2% vs average 32.6% (vendor summaries, Tungsten citing AP Metrics That Matter 2025 based on 2024 data).
- NADP Claims Metrics 2025 PDF opened (https://www.nadp.org/wp-content/uploads/2025/08/FINAL-Claims-Metrics-Survey.pdf) - it is only the questionnaire; defines auto-adjudication as claims "systematically processed to a finalized status without MANUAL intervention and/or SUSPENSION exceptions". No results.

#### Line 1 (cont.)

##### Stack Overflow Developer Survey 2025
- URL opened: https://survey.stackoverflow.co/2025/ai (fielded mid-2025)
- "84% of respondents are using or planning to use AI tools" (33,662 responses); professional devs using AI daily 50.6%; trust in accuracy: highly trust 3.1%, somewhat trust 29.6%, somewhat distrust 26.1%, highly distrust 19.6% (33,244 responses); AI agents at work: 14.1% daily, 9% weekly, 7.8% monthly/infrequent; biggest frustration "AI solutions that are almost right, but not quite" 66% (31,476 responses). PRIMARY.

##### DORA 2025 (Google Cloud)
- URL opened: https://blog.google/technology/developers/dora-report-2025/ (Sep 2025; survey Jun 13-Jul 21 2025 per snippet; ~5,000 tech professionals)
- AI adoption 90%; median 2 h/day with AI; 24% trust "a great deal"(4%)/"a lot"(20%); 30% "a little"(23%)/"not at all"(7%); >80% say productivity enhanced; 59% favorable effect on code quality. PRIMARY.

##### Copilot suggestion acceptance
- URL opened: https://arxiv.org/html/2501.13282 (Bakal et al., ZoomInfo, Jan 2025; >400 developers; data Nov-Dec 2024)
- "an average acceptance rate of 33% for suggestions and 20% for lines of code". PRIMARY.
- Snippet-only: GitHub/Accenture RCT "around 30%" accepted; Ziegler et al. 2022 (arXiv 2205.06537) 27%.

##### Anthropic internal
- URL opened: https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic (Dec 2025; survey Aug 2025 of 132 engineers/researchers + 53 interviews + 200k Claude Code transcripts Feb & Aug 2025)
- "they use Claude in 59% of their work" (vs 28% 12 months earlier); "+50% productivity gains"; more than half can "fully delegate" "only between 0-20% of their work to Claude"; "27% of their Claude-assisted work wouldn't have been done without it"; Claude Code consecutive tool calls 9.8 -> 21.2; human turns per transcript 6.2 -> 4.1. PRIMARY. KEY for delegation: full delegation 0-20% of work.

##### Coinbase
- URL opened: https://cointelegraph.com/news/over-95-of-coinbases-code-is-now-written-with-ai (14 Jul 2026): Rob Witoff (head of platform) "close to 100% of our code, probably somewhere between 95% and 100%, is written by or with LLMs today"; Feb 2026 Coinbase blog said ~40%. PRESS (direct interview quote). "by or with" = assisted, not autonomous.
- Snippet-only: Armstrong Sep 2025 ~40% of daily code AI-generated (The Block).
##### Robinhood: snippet-only, Tenev Jul 2025 ~50% of new code (20VC podcast, via Business Insider).
##### Microsoft: snippet-only/press-not-opened: Nadella 29 Apr 2025 LlamaCon "maybe 20, 30 percent of the code that is inside of our repos today ... written by software".
##### Cognizant: URL opened https://openthemagazine.com/technology/infosys-cognizant-and-ai-who-keeps-the-savings : CEO Ravi Kumar S (Q3 2026 call ~29 Oct 2026) "more than half the company's code was AI-assisted". PRESS-ONLY.

#### Line 3 (cont.)

##### Salesforce help.salesforce.com (Agentforce, "Customer Zero")
- URL opened & PDF text read: https://s205.q4cdn.com/626266368/files/doc_financials/2026/q2/Salesforce-Inc-Q2-FY26-Earnings-Conference-Call-9-3-25.pdf (call 3 Sep 2025)
- Benioff: "we've done the 1.4 million customer support conversations with a 77% resolution rate" (over "the last six months as Customer Zero"); "In the last nine months, about a million and a half conversations happen directly with these agents, and a million and a half of these conversations happen with humans"; accuracy "probably about in the 90s"; "there's a lot that ... has to be escalated to the humans"; support humans "about 6,000 of them or 7,000 or 8,000 of them, or 9,000". PRIMARY.
- Snippet-only: Aug 2026 call summary (MarketBeat 403) ">5 million customer conversations, resolving 64% autonomously"; older call "380,000 conversations ... resolution rate of 84%".

##### Gartner self-service
- Gartner press release 19 Aug 2024 (https://www.gartner.com/en/newsroom/press-releases/2024-08-19-gartner-survey-finds-only-14-percent-of-customer-service-issues-are-fully-resolved-in-self-service) - 403 / Cloudflare challenge when fetched; figures SNIPPET-ONLY: "only 14% of customer service issues are fully resolved in self-service"; survey of 5,728 customers; "very simple" issues only 36%.

#### Line 2: IT operations

##### ServiceNow (internal, "Now on Now")
- URL opened: https://newsroom.servicenow.com/press-releases/details/2026/ServiceNow-launches-Autonomous-Workforce-that-thinks-and-acts-adds-Moveworks-to-the-ServiceNow-AI-Platform/default.aspx (26 Feb 2026)
- "At ServiceNow, our Autonomous Workforce is handling 90%+ of employee IT requests." L1 Service Desk AI Specialist "is already resolving assigned IT cases autonomously, and it's 99% faster". City of Raleigh: "Now Assist is already resolving 98% of initial touchpoints". PRIMARY (vendor). Definition: "handling" requests (not incidents; not "resolved").
- Snippet-only (servicenow.com customer page 403): "15% Coverage of incidents currently eligible for L1 Service Desk AI Specialist"; "46% Resolution rate of eligible incidents resolved by L1 Service Desk AI specialist" -> implies ~7% of all incidents fully AI-resolved. IMPORTANT contrast with 90% "handling" headline.
- Snippet-only: Docusign "targeting autonomous resolution of 90% of all IT tickets" (5 May 2026 release) - target only.

##### Moveworks
- URL opened: https://www.moveworks.com/us/en/solutions/it-service-desk : Broadcom "achieved an 88% autonomous resolution rate"; Mercari "handled 74% of IT tickets autonomously". PRIMARY (vendor marketing; undated; definitional base unclear - Moveworks typically counts issues raised via its bot, not all tickets).

##### HCLTech (Indian IT vendor, client case)
- URL opened (curl): https://www.hcltech.com/case-study/autonomous-it-operations-enterprise-resilience (published 23 Mar 2026; "global food and beverage leader"; AIOps/ITOM on ServiceNow)
- "~30% automated resolution rate across total incident volumes"; "50,000 tickets handled automatically per month"; "BOT resolution of ~67% tickets across data center, network and cloud environments"; "90% automation success rate"; "~45% automation potential identified, with 17% realized in the first year"; "70% reduction in Mean Time to Resolve (MTTR)". PRIMARY (vendor). Mix of rules/bots (Ansible, self-healing bots) and AI/ML - not purely GenAI.
- URL opened (curl): https://www.hcltech.com/case-study/service-desk-modernization-using-agentic-transformation-powered-by-hcltech-aiforce : "Targeted 30% reduction in manual intervention in the first year, with a roadmap to reach 40% by the next year" - target, not achieved rate.

#### Line 3 (cont.) - more support figures

##### Klarna FY2025 20-F (primary, supersedes snippet above)
- URL opened (curl): https://www.sec.gov/Archives/edgar/data/2003292/000200329226000007/klar-20251231.htm (20-F filed 26 Feb 2026)
- "Our AI assistant has handled 80% of customer service chats in the year ended December 31, 2025 (according to our service chat log data), with no drop in consumer satisfaction levels"; "Our AI assistant handled 80% of customer service chats in the year ended December 31, 2025 ... doing the work equivalent of over 850 full-time agents (estimated based on the average monthly reduction in chat and telephone conversations handled by full-time agents in 2025 ...)"; "Since launch, our AI assistant has had 31 million conversations". PRIMARY. Definition: "handled" chats (chat channel only; not phone; not "resolved").

##### Salesforce FY27 transcripts (primary)
- URL opened: https://s205.q4cdn.com/626266368/files/doc_financials/2027/q2/Salesforce-Q2-FY27-Earnings-Transcript.pdf (call 26 Aug 2026): "Salesforce's help agent has surpassed five million customer conversations with 64% resolved autonomously." PRIMARY (cumulative since Oct 2024 launch).
- URL opened: https://s205.q4cdn.com/626266368/files/doc_financials/2027/q1/Salesforce-Q1-FY27-Earnings-Transcript.pdf (call 27 May 2026): "since we deployed Agentforce on help.salesforce.com and on 1-800-NO-SOFTWARE, well, only 15 months ago, it's autonomously handled now four million inquiries. It's now double what human agents are handling." Florida Prepaid "using Agentforce Voice to autonomously handle 75% of business-hour calls and 100% of after-hour calls." Engineers ~15,000 "mostly flat" for two years due to AI. PRIMARY.
- NB: 77% (Sep 2025, 1.4M conv.) vs 64% (Aug 2026, 5M cumulative) - resolution rate fell as volume/scope grew, or definition changed.

##### Lemonade CX.AI (customer inquiries) - see Line 4 entry: "over half of Lemonade's customer inquiries are handled this way" (bot "built to understand and resolve customer requests without human intervention").

##### IBM AskHR (internal HR service desk)
- URL opened: https://www.ibm.com/case-studies/ibm-askhr : "achieved a 94% containment rate of common questions"; "more than 11.5 million employee interactions in 2024 alone"; "40% reduction in the HR team's operational costs over four years". PRIMARY (vendor case). Denominator = "common questions" only.

##### Sierra - Chime
- URL opened: https://sierra.ai/customers/chime : "Resolution rates increased from 50% to over 70%"; "more than two-thirds of member questions are now resolved instantly" (orig. published 23 Oct 2025). PRIMARY (vendor), no definition.
- Snippet-only: Sierra Wilson 77% resolution/containment; SoftBank 70% self-resolution (AI-judged).

##### Haptik (Indian vendor) report (undated, likely 2023-24)
- URL opened (curl): https://www.haptik.ai/hubfs/Content%20Assets/Content%20Assets%20-%20Reports/%5BHaptik%20Report%5D%20How%20Global%20Brands%20Elevated%20CX%20with%20Conversational%20AI.pdf
- Zurich (insurance) case: "84% Automation Rate", "70% End-to-End Query Resolution"; Tata Asset Management quote "the IVA seamlessly handles 70% of query flow"; a case listing "40% Support Call Deflection to IVA", "90% End-to-End Query Resolution", "67% Reduction in Call Center Queries" (layout makes attribution to Jio ambiguous). PRIMARY (vendor), undated, pre-GenAI likely.

##### Indian BPO disclosures
- Firstsource Q1 FY27 call transcript opened (https://media.firstsource.com/Landing-pages/Investor%20Relation/Investor%20relations%20PDF%20&%20Reports/Financial-Information/FY2026-2027/Q1/EarningsCallTranscript-Q1FY27.pdf, 6 Aug 2026): no % of interactions handled by AI disclosed. Headcount 36,875.
- HGS (snippet-only): Q3 FY26 call (13 Feb 2026) "21 AI assistants already supporting 4.5 million minutes of voice interactions and close to 3 million minutes of digital interactions" - volume, not share.
- Gartner forecast (snippet only, Mar 2025): "by 2029, agentic AI will autonomously resolve 80% of common customer service issues without human intervention" - a forecast, not deployment.

#### Line 4 (cont.) - back office

##### Lemonade FY2025 10-K
- URL opened (curl): https://www.sec.gov/Archives/edgar/data/1691421/000169142126000016/lmnd-20251231.htm (filed 25 Feb 2026)
- "as of December 31, 2025, 96% of the time, it is AI Jim that will take the first notice of loss from a Lemonade customer without human intervention"; "As of December 31, 2025, roughly 55% of our claims were automated, resulting in instant or near-instant processing from start to finish." CX.AI: "Currently, over half of Lemonade's customer inquiries are handled this way" [resolve without human intervention]. PRIMARY. Note: "automated" includes rules engines + ML; Lemonade lines are simple (renters/pet).
- Q3 2025 shareholder letter (https://www.lemonade.com/investor-relations-bo/wp-content/uploads/2025/11/LMND-Shareholder-Letter_Q3_25.pdf): LAE ratio 13% -> 7% over 3 yrs; "claims department shrank in absolute terms, even as claims volume increased by >2.5x". PRIMARY.

##### Wipro (Indian IT) - AP touchless for client
- URL opened (curl): https://www.sec.gov/Archives/edgar/data/1123799/000119312526308467/d36563dex991.htm (6-K: proceedings of 80th AGM, 15 Jul 2026)
- "For a global healthcare company, our AI-enabled automation platform processed more than 500K invoices representing over $8 billion in value. The solution achieved 70 percent touchless processing"; "For a large US bank, we used generative AI to modernise legacy applications through automated code generation ... reduced migration effort by close to 30 percent". PRIMARY.

##### Conduent (BPO) - EOB processing
- URL opened (curl): https://www.sec.gov/Archives/edgar/data/1677703/000167770326000118/ex991consolidatedinvesto.htm (8-K investor presentation 30 Sep 2026)
- "For a leading U.S. health benefits company, our GenAI-powered solution converts varied EOB formats into structured, workflow-ready data ... 1.26M EOBs annually ~60% automated today ~$800K annual savings opportunity". PRIMARY. GenAI-attributable.

##### Manulife STP (legacy+digital, not AI-specific)
- URL opened (curl): https://www.sec.gov/Archives/edgar/data/1086888/000119312526127627/d45448dex993.htm (proxy circular, Mar 2026): "STP was 90% in 2025, a 1-percentage point improvement from 2024"; target 90.0%, actual 90.3%. PRIMARY. Definition in proxy: "Measures Manulife's processing time for customers" (share of transactions processed straight through).

##### TD Bank (credit adjudication, rules/ML)
- URL opened (curl): https://www.sec.gov/Archives/edgar/data/947263/000119312525223463/d64335dex992.htm (TD Investor Day, 29 Sep 2025)
- "TD Auto Finance auto-adjudicated 48% [FY'24] > 85% [medium-term target]"; "Small Business auto-adjudicated 50% [FY'24] 70% [target]". PRIMARY. Credit decisions; largely rules/ML scorecards, not GenAI.

##### Sun Life (Indonesia medical claims)
- URL opened (curl): https://www.sec.gov/Archives/edgar/data/1097362/000109736226000032/a2026q3slfenrlive.htm (Q3 2026, 5 Nov 2026): "implemented automated claims adjudication enhancements ... increasing straight through processing by nearly 20% within two months". PRIMARY (relative increase only).

##### Health payer auto-adjudication benchmark
- URL opened: https://healthaxis.com/resources/blogs/maximizing-claims-processing-efficiency-with-ai-breaking-the-80percent-ceiling (vendor blog, 29 May 2026): "The 80% straight-through processing (STP) rate became an industry benchmark"; "legacy CAPS plateau at 80% STP". VENDOR BLOG, unsourced; legacy rules-based automation.
- Cigna 10-K FY2025 opened: mentions "electronic (auto-adjudication) versus manual claim processing" as driver of completion factors; no rate disclosed.
- CAQH Index 2025 executive report: not opened; no auto-adjudication rate found.

##### Ardent Partners AP touchless (via vendor)
- URL opened: https://www.tungstenautomation.com/learn/blog/ai-in-accounts-payable-metrics-that-matter : "with an average of 32.6% of all invoices processed in this manner [straight-through]"; "Ardent Partners' best-in-class performance of 49.2% straight-through processing"; exceptions "averaging 14%"; best-in-class 9%; source "AP Metrics that Matter in 2025" (19th edition). VENDOR-RELAYED (Tungsten is a sponsor); NOT AI-attributable (mostly e-invoicing/OCR/rules).

#### Line 1 (cont.)
##### HCLTech Q2 FY27 earnings call (12 Oct 2026)
- Text read from transcript filed with BSE/NSE 15 Oct 2026 (company IR: https://www.hcltech.com/investor-relations; PDF was already downloaded in the shared scratchpad by a sibling agent - I read the text but did not myself fetch the URL): "for a leading private bank's complex core banking migration, we built an agentic AI solution that converts functional specifications into validated, review-ready code for the target platform in about 10 minutes per routine, with engineers approving every output. It averaged 87% accuracy for an estimated 9x productivity gain." PRIMARY (text).
##### GitHub Octoverse 2025
- URL opened: https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/ (28 Oct 2025): Copilot coding agent "1+ million pull requests that were created between May 2025 and September 2025"; no merge rate given. PRIMARY.

#### Additional code items
- Microsoft: URL opened https://techcrunch.com/2025/04/29/microsoft-ceo-says-up-to-30-of-the-companys-code-was-written-by-ai/ - Nadella, LlamaCon 29 Apr 2025: 20-30% of code in repos "written by software"; Zuckerberg had no figure for Meta. PRESS.
- Robinhood: URL opened https://www.entrepreneur.com/business-news/robinhood-is-using-ai-to-generate-half-of-all-new-code/494758 (17 Jul 2025, 20VC podcast): Tenev: human share "If I had to guess, it's in the minority"; "close to 100%" of engineers use AI; ~50% is reporter paraphrase. PRESS.
- Amazon: URL opened https://www.simonwillison.net/2024/Aug/24/andy-jassy-amazon-ceo (reproduces Jassy LinkedIn post, Aug 2024): "our developers shipped 79% of the auto-generated code reviews without any additional changes"; "the equivalent of 4,500 developer-years of work". PRESS/BLOG reproduction of CEO post; 2024 (pre-window) but the cleanest "accepted without rework" code figure.

#### Gaps / not found
- No Indian IT or BPO firm (TCS, Infosys, HCLTech, Wipro, TechM, Firstsource, HGS, eClerx) discloses an aggregate share of tickets/interactions/code handled by AI; only single-client case studies.
- No primary 2025-26 CAQH/NADP auto-adjudication result, IOFM/APQC touchless %, or Everest/HFS/ISG AIOps auto-resolution benchmark found.
- No verified KYC/onboarding automation rate (Indian bank 20-F/annual report grep found nothing).
- Gartner 14% self-service resolution page blocked (snippet-only).
