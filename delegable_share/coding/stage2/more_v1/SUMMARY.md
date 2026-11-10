# Stage 2 summary — more_v1

780 items × 3 coders (s1 = claude-sonnet (subagent), s2 = claude-sonnet (subagent), t = gpt-6.1-terra). Combined: median of numbers and ordered categories; domain by median κ.

## Spread between coders

- Median item length (p50), max/min across coders: median ratio 1.50, quartiles 1.25–2.00, 22 items above 3×.
- Stakes: all three agree on 310, within one step on 446, two steps apart on 24.
- Context: all agree 503, one step 277, two steps 0.
- Domain: all agree 628, two agree 152, three-way split 0.
- Coder tendency in p50 length (median ratio to combined): s1 ×1.00, s2 ×1.00, t ×1.00.
- Review line a + b·h (fit to the three median points): median b 0.185, quartiles 0.098–0.336; median a 1.0 min. Slope short→typical vs typical→long (medians): 0.167 vs 0.181.
- Unit flags: 86 items flagged by at least one coder; 60 items with two groups noted.

## Combined features by occupation (medians across items)

| Occupation | Items | p50 min | p90 min | review p10 | stakes (L/M/H) | context (L/M/H) | domain (sw/cu/tx) |
|---|---|---|---|---|---|---|---|
| Computer Programmers | 14 | 135 | 540 | 8 | 3/10/1 | 0/8/6 | 12/1/1 |
| Information Security Analysts | 11 | 90 | 360 | 8 | 0/3/8 | 0/2/9 | 3/2/6 |
| Telemarketers | 13 | 6 | 15 | 1 | 8/5/0 | 7/6/0 | 0/12/1 |
| Payroll and Timekeeping Clerks | 22 | 37.5 | 150 | 5 | 0/9/13 | 0/22/0 | 0/21/1 |
| Bill and Account Collectors | 24 | 10 | 25 | 2 | 3/15/6 | 0/24/0 | 0/22/2 |
| Medical Transcriptionists | 21 | 8 | 30 | 1 | 4/8/9 | 7/13/1 | 0/10/11 |
| Data Scientists | 15 | 240 | 960 | 15 | 0/14/1 | 2/11/2 | 9/0/6 |
| Retail Salespersons | 21 | 7 | 20 | 2 | 12/9/0 | 7/14/0 | 0/17/4 |
| Cashiers | 23 | 2 | 5 | 1 | 18/4/1 | 20/3/0 | 0/20/3 |
| Office Clerks, General | 23 | 15 | 45 | 2 | 15/7/1 | 3/20/0 | 0/19/4 |
| General and Operations Managers | 18 | 210 | 960 | 10 | 3/11/4 | 1/3/14 | 0/9/9 |
| Project Management Specialists | 20 | 90 | 300 | 6.5 | 4/13/3 | 1/14/5 | 0/8/12 |
| Elementary School Teachers, Except Special Education | 18 | 35 | 120 | 2.5 | 12/6/0 | 3/14/1 | 0/4/14 |
| Medical Assistants | 15 | 8 | 20 | 2 | 4/9/2 | 1/14/0 | 0/14/1 |
| Construction Laborers | 1 | 10 | 25 | 1 | 0/0/1 | 1/0/0 | 0/0/1 |
| Cooks, Restaurant | 3 | 25 | 75 | 3 | 2/1/0 | 0/3/0 | 0/3/0 |
| Police and Sheriff's Patrol Officers | 16 | 13.5 | 35 | 2 | 2/4/10 | 1/15/0 | 0/8/8 |
| Insurance Sales Agents | 21 | 30 | 90 | 3 | 1/10/10 | 0/21/0 | 0/17/4 |
| Graphic Designers | 18 | 120 | 480 | 4 | 11/7/0 | 5/13/0 | 0/14/4 |
| Marketing Managers | 19 | 300 | 1200 | 10 | 0/15/4 | 0/6/13 | 0/5/14 |
| Loan Officers | 16 | 30 | 90 | 5 | 1/7/8 | 0/15/1 | 0/14/2 |
| Computer and Information Systems Managers | 20 | 120 | 360 | 8 | 2/11/7 | 0/3/17 | 2/7/11 |
| Medical and Health Services Managers | 22 | 300 | 1320 | 15 | 0/14/8 | 0/5/17 | 0/10/12 |
| Budget Analysts | 13 | 120 | 480 | 10 | 0/10/3 | 0/5/8 | 0/11/2 |
| Training and Development Specialists | 20 | 135 | 480 | 9 | 4/15/1 | 0/17/3 | 0/8/12 |
| Compliance Officers | 15 | 30 | 90 | 3 | 0/7/8 | 1/13/1 | 0/4/11 |
| Operations Research Analysts | 13 | 600 | 2400 | 20 | 0/12/1 | 0/8/5 | 2/6/5 |
| Civil Engineers | 15 | 600 | 3600 | 20 | 0/1/14 | 0/14/1 | 0/9/6 |
| Mechanical Engineers | 31 | 480 | 1800 | 15 | 0/15/16 | 1/12/18 | 0/13/18 |
| Economists | 13 | 960 | 3600 | 30 | 0/10/3 | 4/8/1 | 3/3/7 |
| Child, Family, and School Social Workers | 20 | 90 | 210 | 9 | 0/8/12 | 0/6/14 | 0/5/15 |
| Public Relations Specialists | 17 | 480 | 1440 | 10 | 0/14/3 | 0/12/5 | 0/3/14 |
| Editors | 21 | 60 | 180 | 5 | 9/10/2 | 2/12/7 | 0/1/20 |
| Licensed Practical and Licensed Vocational Nurses | 12 | 6.5 | 20 | 1 | 4/4/4 | 3/9/0 | 0/11/1 |
| Pharmacists | 28 | 10 | 35 | 2 | 2/11/15 | 6/20/2 | 0/21/7 |
| Home Health Aides | 1 | 10 | 25 | 2 | 0/1/0 | 0/1/0 | 0/1/0 |
| Security Guards | 7 | 3 | 15 | 1 | 2/3/2 | 2/5/0 | 0/2/5 |
| Waiters and Waitresses | 13 | 2 | 5 | 1 | 12/0/1 | 11/2/0 | 0/7/6 |
| Fast Food and Counter Workers | 9 | 2 | 6 | 1 | 8/0/1 | 7/2/0 | 0/6/3 |
| First-Line Supervisors of Retail Sales Workers | 19 | 60 | 210 | 5 | 4/11/4 | 2/11/6 | 0/12/7 |
| Real Estate Sales Agents | 32 | 45 | 120 | 5 | 9/14/9 | 8/22/2 | 0/13/19 |
| Shipping, Receiving, and Inventory Clerks | 9 | 10 | 35 | 1 | 3/6/0 | 0/9/0 | 0/8/1 |
| Medical Secretaries and Administrative Assistants | 19 | 10 | 30 | 1 | 4/13/2 | 2/17/0 | 0/15/4 |
| First-Line Supervisors of Office and Administrative Support Workers | 28 | 60 | 180 | 4 | 4/24/0 | 0/19/9 | 0/12/16 |
| Carpenters | 7 | 30 | 120 | 2 | 3/3/1 | 1/5/1 | 0/2/5 |
| Maintenance and Repair Workers, General | 5 | 30 | 120 | 3 | 3/2/0 | 0/5/0 | 0/3/2 |
| Team Assemblers | 2 | 15 | 42.5 | 2 | 1/1/0 | 0/2/0 | 0/1/1 |
| Laborers and Freight, Stock, and Material Movers, Hand | 1 | 5 | 12 | 1 | 1/0/0 | 1/0/0 | 0/1/0 |
| Stockers and Order Fillers | 16 | 11.5 | 37.5 | 1 | 10/6/0 | 4/11/1 | 0/14/2 |

## Widest disagreements on length (p50 ratio > 3)

- 2403a (Cashiers): one customer greeted — p50 by coder 0.3;1;0.1 min
- 20733b (Mechanical Engineers): one mechanical design package — p50 by coder 900;3000;6000 min
- 255a (Child, Family, and School Social Workers): one research study or summary — p50 by coder 360;2400;960 min
- 1280a (Computer Programmers): one proposed programming method or method improvement — p50 by coder 480;600;2400 min
- 21837a (Data Scientists): one model validated and reformulated — p50 by coder 480;300;1440 min
- 2474a (Bill and Account Collectors): one account note entered during a customer contact — p50 by coder 9;2;3 min
- 1269a (Computer Programmers): one program's documentation (or revision note) with code comments — p50 by coder 30;45;120 min
- 1277a (Computer Programmers): one systems software change or maintenance task — p50 by coder 120;180;480 min
- 2412b (Cashiers): one transaction-total entry or summary — p50 by coder 20;15;5 min
- 21476b (Project Management Specialists): one proposed project plan modification reviewed or approved — p50 by coder 60;30;120 min
- 973a (Computer and Information Systems Managers): one technology evaluation with upgrade recommendation — p50 by coder 2400;4800;1200 min
- 21450a (Compliance Officers): one violation referral — p50 by coder 180;360;90 min
- 7388a (Operations Research Analysts): one experiment designed, run and evaluated — p50 by coder 1800;1200;4800 min
- 20491a (Civil Engineers): one design drawing and specification set — p50 by coder 4800;2400;9600 min
- 7538a (Economists): one analysis report or forecast — p50 by coder 2400;600;960 min
- 20679a (Maintenance and Repair Workers, General): one repair aid designed (sketch or drawing) — p50 by coder 60;120;240 min
- 5317a (Information Security Analysts): one security configuration change — p50 by coder 20;40;75 min
- 955b (Marketing Managers): one distribution strategy or network plan — p50 by coder 480;1800;1800 min
- 6563a (Elementary School Teachers, Except Special Education): one class project, trip or guest visit arranged — p50 by coder 150;75;240 min
- 1820a (Pharmacists): one written procedure created or revised — p50 by coder 240;150;480 min
- 674a (First-Line Supervisors of Retail Sales Workers): one promotion or ad campaign plan with copy — p50 by coder 300;150;480 min
- 951a (Marketing Managers): one marketing strategy or strategy evaluation — p50 by coder 3000;2400;960 min

## Unit flags

- 1269a (1/3): A whole program's documentation and a short revision note with comments are very different amounts of work.
- 1270a (1/3): A program, module or update includes everything from a small fix to a new package, and ends with release, which mixes very different sizes of work.
- 1272a (1/3): One revision to an existing program ranges from a one-line fix to a large feature, so the work mixes very different sizes.
- 1277a (1/3): A systems software change covers anything from a configuration tweak to a long program change, which mixes very different kinds of work.
- 1280a (2/3): Developing a new programming method with outside collaborators is open-ended research, not a repeatable work item. | A proposed programming method can range from a small helper technique to research-level work with outside collaborators, so the item is loosely defined.
- 21049a (2/3): One website and one site feature are very different in size and kind of work. | The item covers anything from a small feature to a whole site, which mixes very different amounts of work.
- 5317a (1/3): Security configuration changes range from a simple access-rule tweak to onboarding new software across tools, which are different kinds of work.
- 2480b (1/3): Routine account changes and deceased-customer purge actions involve materially different verification and handling requirements.
- 9425a (1/3): This is a judgment step inside transcribing a report, not a separate deliverable, so it overlaps with the whole transcription.
- 21837a (1/3): Validation and reformulation are two quite different pieces of work and the length varies hugely.
- 826a (2/3): The item mixes enquiries, orders and complaints, which differ in length and work. | The item covers questions, orders and complaints together, which are very different kinds of contact.
- 829a (1/3): A bill, contract, policy, invoice or check are very different documents, from a two-minute check to a long contract, so the item mixes kinds of work.
- 830b (2/3): One electronic document or message processed using an office system covers very different jobs (scan and file, route an email, enter data) that the statement does not pin down. | Electronic document or message processing covers a very broad mix, from forwarding an email to transcribing voicemail to scanning, so the item is loosely defined.
- 838a (1/3): The item covers any business or government form or expense report, which range from a one-line form to a multi-receipt report.
- 944a (1/3): Assisting a customer on the sales floor can be anything from pointing to an aisle to finding stock and ringing a sale, so it mixes very different kinds of work.
- 945b (2/3): Launching a campaign or promotion mixes very different work such as ad placement, pricing changes in systems, staff briefing and coordinating vendors. | Launching a campaign mixes very different kinds of work, such as booking media, coordinating staff, and setting up systems.
- 20703a (2/3): Budget cycle begins to budget approved covers gathering inputs, building the model, negotiating and presenting, which are very different kinds of work over weeks. | A full operating budget cycle spans weeks and mixes modelling, negotiation with department heads and approval meetings, and the end depends on others' decisions.
- 20708b (2/3): Goods-movement problems range from a late truck to a plant-layout inefficiency, which are very different kinds of work. | A goods-movement issue covers anything from a delayed truck to a layout redesign, so the item mixes very different kinds of work.
- 21475a (1/3): Project document covers very different kinds of document (status report, charter, minutes, risk log) with different effort.
- 21477a (2/3): Position approved to person hired spans sourcing, screening, interviewing, offer and onboarding paperwork, which are very different kinds of work spread over weeks. | A hire spans writing the posting, screening, interviewing and offering over weeks, which mixes very different kinds of work with much waiting.
- 6539a (1/3): A lesson plan and a weekly plan differ greatly in scope, so the item mixes work of very different size.
- 6559a (1/3): One student report and one activity report are different in length and effort, and the item mixes both.
- 2042b (2/3): A monthly batch of statements with collection follow-up combines bulk billing runs and individual calls and letters, so the unit is large and mixed. | The item combines producing and mailing statements with phone and letter follow-up of overdue accounts, which are different kinds of work.
- 23061a (1/3): This is a quick live radio or phone exchange but is typed as discrete.
- 734a (1/3): Installing a bookkeeping system ranges from setting up a small accounting package to a multi-week implementation, and it sits oddly under an insurance sales role.
- 734b (2/3): A bookkeeping system problem could be a setting, a data fix or training, and fits oddly under an insurance agent. | A bookkeeping system problem could be anything from a wrong entry to a software setup fault, and is unusual for an insurance sales agent.
- 954a (2/3): A full hiring decision from shortlisting through interviews to approval mixes screening, interviewing, and writing and spans weeks. | A hiring decision bundles screening, interviewing and offer approval, which are different kinds of work.
- 955b (1/3): A distribution strategy proposal and setting up an operational distribution network can involve substantially different work.
- 3423a (1/3): Need raised to policy approved and issued combines analysis, drafting, meetings with senior managers and compliance sign-off, which are very different kinds of work over weeks.
- 966a (2/3): The item covers a failed backup, a security alert and an access request, which are different kinds of work with very different effort. | The item combines backup recovery, security incident response, and access requests, which involve materially different investigations and controls.
- 969b (2/3): One piece of staff work could be code, a design or an analysis, which are very different to review. | The item combines reviews of potentially very different staff outputs, such as code, system designs, and project documents.
- 977a (2/3): A hiring decision mixes screening, interviews and discussions, which are different kinds of work. | A staffing decision bundles sourcing, technical interviewing and recommendation, which differ in kind.
- 48a (2/3): Filling a vacancy mixes very different work (sourcing, screening, interviewing, offer negotiation) over weeks, so it is not one item. | One vacancy filled spans posting, screening, interviewing, references and offer negotiation, which mixes very different kinds of work.
- 49a (2/3): Setting up a new system and modifying an existing one are very different in size and kind of work. | The item runs from identifying a need to users accepting a change in use, mixing a small field tweak with a multi-month system rollout and including training and adoption work.
- 58b (2/3): A program implementation instruction or operational decision covers very different kinds of work, from a short staffing note to a policy decision needing analysis. | An operational decision can range from a one-line instruction to a complex program decision, mixing very different work.
- 62b (1/3): The item ends with an implementation plan rather than implementing the approved medical program or service.
- 3398a (1/3): Budget advice requests range from a quick figure lookup to cost-analysis help that is really a small analysis project, so the item mixes very different kinds of work.
- 100a (1/3): A whole training program run bundles outreach, enrollment handling and scheduling, which is much bigger than one participant or task.
- 108b (1/3): The item begins after terms are agreed and covers drafting and signature rather than the negotiation specified in the task.
- 7387a (1/3): A whole system study from observation through analysis and documented findings mixes site observation, data gathering, analysis and reporting and ranges from days to weeks.
- 7388a (1/3): Design, running and evaluating an experiment mixes very different work, from planning to data collection to analysis, and takes far longer than a single item.
- 152a (1/3): The unit combines bid proposals, environmental impact statements, and property or right-of-way descriptions, which require substantially different analyses and deliverables.
- 19608a (1/3): A full design package mixes calculations, drawings, specifications and permitting, far broader than one task.
- 20491a (1/3): A design drawing and specification set covers very different projects, from a small culvert to a road interchange, so the work mixes very different amounts and kinds of work.
- 1430a (2/3): Design versus analysis, and robotics versus waste management versus biomedical, are very different kinds of work lumped into one item. | The item covers any design or analysis in any emerging field, so the work and its size vary hugely.
- 19628a (1/3): An integrated system design package from energy goals to issued design combines load calculation, equipment selection, drawings and code review, very different work over weeks.
- 20733b (2/3): A mechanical design package ranges from a small bracket to a whole system, which are very different kinds and sizes of work. | A mechanical design package ranges from a bracket to a whole system, which mixes very different amounts and kinds of work.
- 20735a (1/3): An alternative design or process model covers very different work from a spreadsheet estimate to a CAD or simulation model.
- 20737a (2/3): The item ends at drawing completed and approved, which includes the drafter's work and approval time, not only the engineer's input package. | The stated output is an input package for a drafter, but the endpoint includes completion and approval of the drafter's drawing.
- 7538a (1/3): One analysis report or forecast spans quick data briefs to months-long model-based forecasts, mixing very different kinds of work.
- 7544b (2/3): The item combines writing the assessment and grading it, two different jobs with different timing. | The item bundles writing an assignment or exam and grading student work, which are different kinds of work with very different lengths.
- 20053a (2/3): A whole paper from question to publication mixes data work, modelling, writing and peer review, far beyond one task. | A full paper from question to publication spans months of data work, writing and peer review, mixing very different activities and lengths.
- 235a (2/3): The item mixes a live interview with writing the assessment afterwards. | The item combines an interview (often long and in person) with a written assessment, which are different kinds of work.
- 238b (2/3): The item combines counselling and diagnosing a student's problem with arranging services, which are very different kinds of work. | Assessing a problem and arranging services are two different kinds of work whose effort varies hugely by case.
- 244a (1/3): The item covers very different services (child care, treatment, job training) with very different effort, though it fits the task statement.
- 251a (1/3): The item covers the whole placement from decision to documentation, mixing searching, contacting, court and caregiver work, with very different effort by case.
- 255a (2/3): A research study and a summary of existing research are very different amounts of work, so the item mixes kinds of work. | The item combines a research study, which may require original data collection and analysis, with a potentially much shorter research summary.
- 1768a (1/3): The item runs from the event idea to the event being held, mixing planning with running the event, which is very different work.
- 19809a (2/3): Coordinating a response mixes drafting statements, handling media calls and meetings with management, over days. | The item spans the whole incident response from first alert to handover, mixing media work, stakeholder meetings and writing, so its length varies enormously.
- 20557a (2/3): A short employee newsletter and a stockholders' report are very different kinds of work in length, review and legal weight. | A short employee newsletter and a stockholders' report are very different kinds of work.
- 1783a (2/3): Taking an issue through the whole print production cycle is a long oversight job combining many tasks. | Taking an issue through production to print is a long coordination of many different kinds of work, not one bounded piece.
- 1793a (1/3): An editorial policy decision mixes consultation, judgment and communication of very different scope, from a style tweak to a major policy change.
- 1794a (1/3): Obtaining a permission mixes drafting a request, tracing rights holders over days, and negotiating terms, so cases range from a quick form to a long negotiation.
- 24025b (1/3): A story, article, editorial or newsletter mix very different lengths and kinds of work, from a short brief to a researched feature.
- 528c (1/3): One office or clinic record update covers anything from a demographic change to a clinical chart entry, which differ in kind and effort.
- 528d (2/3): One routine clerical item covers forms, referrals, faxes and filing that differ greatly in kind and effort. | Routine clerical items such as forms, records requests and referrals differ widely in kind and the definition is too broad.
- 1812d (1/3): A single record entry takes minutes while a full reconciliation takes much longer, so the item mixes two kinds of work.
- 1822b (3/3): The item covers a report, a schedule or a filing, which are very different kinds of work. | The item covers reports, schedules and filings, which are very different kinds of work. | The item groups substantially different administrative outputs, including staff schedules, reports and potentially regulatory filings.
- 1823a (1/3): It mixes clinical review of the order with the physical preparation and release of the medication, which are very different kinds of work.
- 20895b (1/3): The item ends when paramedics arrive, so it mixes a short call with waiting and first-aid or crowd management whose length depends on response time.
- 665a (1/3): A hiring decision bundles screening, interviewing and negotiating, which are different kinds of work.
- 665d (2/3): A promotion and a dismissal are very different kinds of work (a positive decision and announcement versus documented progressive discipline with legal exposure), so the item mixes them. | The item combines promotion and dismissal decisions, which involve substantially different procedures and consequences.
- 669a (1/3): A pricing policy decision and a routine price update are very different kinds of work, and the task statement is about policy.
- 2446b (1/3): An entire open house contains multiple visitor conversations and idle periods rather than one live conversation while a customer waits.
- 787b (1/3): The item combines applying account credits with collections follow-up, which are distinct financial and customer-contact workflows.
- 789b (1/3): Reports, speeches, articles and conference papers are very different in length and effort, and help ranges from formatting a draft to writing from scratch.
- 9706a (1/3): Implementing a policy mixes anything from updating a one-page checklist to retraining a team, so the items vary hugely in kind and size.
- 9711a (2/3): The item bundles sourcing, interviews and a decision over weeks, mixing different kinds of work. | A whole vacancy filled mixes sourcing, screening, interviewing and offer work over weeks.
- 9714a (2/3): Records on inventory, personnel, orders, supplies and machine maintenance are very different kinds of record keeping. | The batch covers inventory, personnel, orders, supplies and maintenance records, which mix different systems and kinds of update.
- 9716a (1/3): A management or government report covers anything from a routine weekly count to a formal regulatory filing, which are very different kinds of work.
- 9722a (1/3): The item covers any customer service request, so it mixes very different kinds of requests; the task is also supervisor-level help rather than a defined deliverable.
- 9722b (3/3): The item is any administrative work item from a queue, which mixes data entry, correspondence and difficult cases. | The item is defined as any queued administrative item, which mixes very different kinds of work. | The item combines unspecified subordinate administrative tasks that can involve very different workflows and outputs.
- 9723a (3/3): Designing a programme and evaluating one are very different work of very different length, and the item allows either. | Designing a programme and evaluating one are different kinds of work with very different durations, so the item mixes them. | The item combines designing and rolling out a training program with the distinct alternative of evaluating an existing program.
- 9723b (3/3): Planning or evaluating an initiative covers very different jobs, from a small script change to a unit-wide program, and planning and evaluating are different work. | Planning an initiative and evaluating one are very different kinds of work and span weeks, so the item mixes work. | The item combines planning and launching an initiative with the distinct alternative of evaluating an existing initiative.
- 9727a (3/3): Equipment acquisition, disposal, relocation and security services are very different kinds of work of very different length. | The item spans very different services (buying equipment, disposing of assets, relocation, parking, security) that mix kinds of work. | The item combines substantially different services, including purchasing, relocation, asset disposal, and security coordination.
- 23431a (1/3): The item mixes reading plans and a materials takeoff with physically marking out the layout on site.
