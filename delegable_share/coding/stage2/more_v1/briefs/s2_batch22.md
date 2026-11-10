You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Code each ITEM independently, in the order given; do not go
back and adjust earlier answers to make them consistent with later ones.

Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/more_v1/s2/batch22.json
with one element per item, in the order given, each the output object
described in the instructions. Write nothing else to that file. Then reply
"done <n> items".

=== INSTRUCTIONS ===
You are coding features of work items. For each item you get the
occupation, the original task statement, and a definition of the work item
(where it starts and ends, and who checks it). Another team has already
decided what the work items are; use each one exactly as defined.

Describe the work as experienced people in this occupation do it today,
without AI. Do not consider what AI could or could not do; that comes from
other data.

If the work item does not fit the task statement, or is defined so that it
mixes very different kinds of work, set unit_flag to true, explain in one
sentence, and code it anyway.

Items are of two types:
  - DISCRETE: a deliverable handed over when finished.
  - LIVE_SERVICE: work done in a live conversation (phone, chat, walk-up)
    while the customer or user waits.

For each field, write one sentence of reasoning, then the value.

DOMAIN: what does the worker mainly have to do to produce this item?
  - software: write, change, or test code or configuration
  - computer_use: operate applications or websites (ticketing tools, CRM,
    ERP or billing systems, forms, web portals)
  - text: read and write documents or messages, where the output is text
    and producing it doesn't require operating other software
  Pick the one that takes most of the time. For LIVE_SERVICE items, ignore
  the talking itself and pick what else takes most of the time.

LENGTH: minutes of active work for one item, from its start to its end, for
an experienced worker in this occupation, without AI. Exclude time spent
waiting on others (queues, approvals, the customer's hold before the contact
starts). For LIVE_SERVICE items, count the whole contact from start to end.
Give the 10th, 50th and 90th percentile across the items of this kind that
such a worker handles. If the items fall into two clearly different groups
(e.g. quick fixes and long investigations), set two_groups to true and say so.

REVIEW_MINUTES: minutes a competent colleague needs to check one item well
enough to accept it: open it, read the context, verify the result. Exclude
time to fix errors. Give it for three of the items from your LENGTH answer:
the 10th-percentile item (review_p10), the median item (review_p50), and
the 90th-percentile item (review_p90). For LIVE_SERVICE items, this is the
time a quality reviewer needs to check one recorded contact of that length.

STAKES: cost of an error that slips past review, for a typical item.
  - low: cheap to fix and noticed soon (wrong ticket category; typo in an
    internal note)
  - medium: reaches a client or user and causes rework or a complaint, but
    can be reversed (wrong instructions to a user; a bug caught in testing)
  - high: financial loss, legal or regulatory exposure, data loss, or an
    outage, or hard to reverse (wrong payment; compliance filing;
    production deployment)
  If the 90th-percentile item would be in a higher category, give that as
  stakes_p90; otherwise repeat the value.

CONTEXT: how much does the item depend on knowledge specific to this
client or employer?
  - low: a skilled outsider with the item in front of them could do it
    about as fast as an insider
  - medium: needs familiarity with the client's tools, processes, or
    conventions that takes weeks to learn
  - high: needs deep knowledge of the client's systems, history, or people
    that takes months to build

Output, per item:
{
  "item_id": "...",
  "unit_flag": false, "unit_flag_reason": "",
  "domain_reasoning": "...", "domain": "software | computer_use | text",
  "length_reasoning": "...",
  "length_p10": 0, "length_p50": 0, "length_p90": 0, "two_groups": false,
  "review_reasoning": "...", "review_p10": 0, "review_p50": 0, "review_p90": 0,
  "stakes_reasoning": "...", "stakes": "low | medium | high",
  "stakes_p90": "low | medium | high",
  "context_reasoning": "...", "context": "low | medium | high"
}

BENCHMARK MATCH. Answer this last, after all the feature fields above.

The BENCHMARK LIST below describes sets of tasks used to test software
agents. Find the benchmark whose items are most like this work item in what
the worker has to do: the inputs, the actions, and what counts as a correct
result. Compare the work only. Do not consider how well AI does on any
benchmark, and do not let the benchmark list change any feature answer above:
those describe the work as people do it today.

Rate each match:
  - good: the benchmark's items are the same kind of work
  - partial: they share the main actions but differ in an important way
    (say how)
  - none: no benchmark is close. Do not force a match.

Give your best match and your second-best match (a different benchmark, or
"none"). Write two sentences of reasoning before choosing.

Add these fields to each item's output, after the feature fields:
  "match_reasoning": "...",
  "best": "<benchmark id or none>", "best_match": "good | partial | none",
  "best_difference": "if partial: the important difference, else empty",
  "second": "<benchmark id or none>", "second_match": "good | partial | none"

=== WORKED EXAMPLES (other occupations) ===
### Example A — Executive Secretaries and Executive Administrative Assistants
Work item: one document checked and returned with revisions (e.g. a letter, memo or report).
Start: document received for checking. End: marked-up document returned to the author. Checked
by: the author, and the executive who signs it. Type: DISCRETE.

```json
{
  "item_id": "example-A",
  "unit_flag": false, "unit_flag_reason": "",
  "domain_reasoning": "The work is reading and marking up text; the editor is just where it happens.",
  "domain": "text",
  "length_reasoning": "A one-page letter takes a few minutes; a long report with tables and house-style rules takes most of an hour.",
  "length_p10": 5, "length_p50": 15, "length_p90": 60, "two_groups": false,
  "review_reasoning": "For a short letter the author accepts or rejects the tracked changes in a minute or two; a typical memo needs the changes read in context; a long report needs a few sections reread.",
  "review_p10": 1, "review_p50": 3, "review_p90": 10,
  "stakes_reasoning": "A missed error is usually caught by the signer; one that goes out is embarrassing but rarely costly.",
  "stakes": "low", "stakes_p90": "medium",
  "context_reasoning": "Needs the company's house style and the executive's preferences, learned in a few weeks.",
  "context": "medium",
  "match_reasoning": "GDPval items are written deliverables judged by experts, which shares the main action of producing a professional document, but they create a document from a brief rather than correcting someone else's. No other benchmark involves editing text.",
  "best": "gdpval", "best_match": "partial",
  "best_difference": "the benchmark produces a new document; this item corrects an existing one",
  "second": "none", "second_match": "none"
}
```

### Example B — Market Research Analysts and Marketing Specialists
Work item: one statistics release reviewed and summarised. Start: new release of industry figures
published. End: note on the notable changes sent to the team. Checked by: marketing manager.
Type: DISCRETE.

```json
{
  "item_id": "example-B",
  "unit_flag": false, "unit_flag_reason": "",
  "domain_reasoning": "Most of the time goes into pulling the figures into a spreadsheet and comparing them with earlier releases.",
  "domain": "computer_use",
  "length_reasoning": "A routine monthly release with small changes takes a quarter of an hour; a large annual release with revised series takes a few hours.",
  "length_p10": 15, "length_p50": 45, "length_p90": 180, "two_groups": false,
  "review_reasoning": "For a routine release the manager reads the note; a typical one needs a couple of figures checked against the release; a large one needs the comparisons spot-checked.",
  "review_p10": 2, "review_p50": 5, "review_p90": 15,
  "stakes_reasoning": "A wrong figure in the note can mislead a planning decision, but it is usually caught when the trend report is written.",
  "stakes": "medium", "stakes_p90": "medium",
  "context_reasoning": "Needs to know which series matter for this company's markets, learned over a few weeks.",
  "context": "medium",
  "match_reasoning": "Finch items are business spreadsheet workflows that include pulling figures across sheets and checking them, which shares the main actions, but they are finance and accounting workbooks rather than published statistics. SpreadsheetBench 2 has similar workbook work but builds models to a specification.",
  "best": "finch", "best_match": "partial",
  "best_difference": "finance workbooks rather than published industry statistics, and no written summary",
  "second": "spreadsheetbench_2", "second_match": "partial"
}
```

### Example C — Receptionists and Information Clerks (LIVE_SERVICE)
Work item: one appointment booked or changed during a call or visit. Start: caller or visitor asks
for an appointment. End: slot confirmed to the person and entered in the calendar. Checked by: the
caller, and the staff member whose calendar it is. Type: LIVE_SERVICE.

```json
{
  "item_id": "example-C",
  "unit_flag": false, "unit_flag_reason": "",
  "domain_reasoning": "Apart from talking, the time goes into finding and booking a slot in the scheduling system.",
  "domain": "computer_use",
  "length_reasoning": "A simple booking takes a couple of minutes; one needing several people's availability or a reschedule chain takes ten.",
  "length_p10": 2, "length_p50": 4, "length_p90": 10, "two_groups": false,
  "review_reasoning": "A quality reviewer listens to the call, mostly at higher speed, and checks the calendar entry; a long reschedule chain takes a little longer to follow.",
  "review_p10": 1, "review_p50": 2, "review_p90": 4,
  "stakes_reasoning": "A wrong booking causes a missed or double-booked appointment, noticed on the day and rebooked.",
  "stakes": "low", "stakes_p90": "medium",
  "context_reasoning": "Needs the office's booking rules and who sees whom, picked up quickly.",
  "context": "low",
  "match_reasoning": "τ-Voice items are phone calls in which the worker looks up and changes a booking under a policy while the caller waits, which is the same kind of work. The chat version of τ-bench is the same task by text.",
  "best": "tau_voice", "best_match": "good",
  "best_difference": "",
  "second": "tau_retail_airline", "second_match": "good"
}
```

=== BENCHMARK LIST ===
## Software development and maintenance

**`swe_bench_verified`: SWE-bench Verified**
A bug report or feature request (a GitHub issue) for an open-source Python library, plus the full code repository. The worker must change the code so the described problem is fixed. Correct means hidden unit tests that check the fix pass, and existing tests still pass.

**`swe_rebench`: SWE-rebench / SWE-bench Live**
Recently filed bug reports and requests on open-source repositories, collected each month, in the same format as SWE-bench: issue plus repository in, code change out, judged by hidden tests.

**`metr_th`: METR task suite**
Self-contained technical tasks in a sandboxed computer with a written instruction. Examples: fix a bug in a machine-learning codebase, write a script that processes data, solve a security challenge, optimise a model training run. A few items are single quick actions, such as choosing which file to open. Each task has an automatic scoring function that checks the result.

**`swe_bench_multimodal`: SWE-bench Multimodal**
A bug report for a JavaScript front-end library that includes screenshots of the visual problem (e.g. a tab component rendering wrongly), plus the repository. The worker changes the code; correct means hidden tests, some comparing rendered output, pass.

**`swe_lancer`: SWE-Lancer (individual contributor tasks)**
A real paid freelance job on a commercial expense-management app (React Native / TypeScript), e.g. make the zip-code hint text consistent across two screens, or fix a broken workflow. The worker gets the job description and the codebase and submits a code change. Correct means end-to-end browser tests written by engineers pass.

**`multi_swe_bench`: Multi-SWE-bench**
Same as SWE-bench, but the repositories are in Java, TypeScript, JavaScript, Go, Rust, C and C++. Example: a Java RPC library fails to convert date and time types; fix the conversion. Correct means hidden tests that reproduce the issue now pass.

**`swe_bench_pro`: SWE-bench Pro**
An issue description, written requirements and an interface specification for a product codebase (Python, Go, JavaScript/TypeScript), some from private company repositories. The change typically touches several files (around 100 lines across 4 files). Correct means hidden tests for the new behaviour pass and existing tests still pass.

## IT service desk and enterprise web applications

**`webarena`: WebArena**
A goal stated in plain language on self-hosted copies of an online store and its admin back end, a GitLab server, a content management system, a forum and a map. Examples: update a product's price and mark it out of stock; count orders cancelled in a given month; change a repository setting. Correct means the answer or the changed data matches.

**`starshell`: StarShell enterprise tasks**
Record-keeping tasks in three business systems: ServiceNow (incidents, catalog orders, knowledge base), GitLab (repository and issue administration), and ERPNext (create sales invoices, sales orders and linked documents, sometimes chained). Correct means the records in the system match the goal.

**`workarena_pp`: WorkArena++ (multi-step ServiceNow tickets)**
A multi-step service-desk job in ServiceNow, given either as step-by-step instructions or as a ticket assigned to the worker, as a real employee would get it. Examples: onboard a new employee (create the user, order their hardware, assign the assets); find the staff member with the fewest open incidents and assign them a new problem; work out a budget from a dashboard and place the orders. Correct means every resulting record is right.

**`scuba`: SCUBA (Salesforce)**
A task in a real Salesforce organisation as an administrator, a sales rep or a service agent. Examples: create a leads report with a filter on status; add a formula field visible only to one user profile; update a case. Correct means the organisation's configuration and records match the goal.

**`workarena_l1`: WorkArena (single actions in ServiceNow)**
One explicit instruction in a ServiceNow IT-service-management instance. Examples: create an incident with given fields, filter the incident list by priority and assignment group, order a laptop from the service catalog, find an answer in the knowledge base, read a value off a dashboard. Correct means the record, list state or answer matches the goal.

**`ui_cube`: UI-CUBE**
Tasks in replicas of enterprise applications (Salesforce, SAP, Concur, Workday) and in standalone interface widgets. Examples: enter an expense report from given data, update stock records, move records from one application to another, pick a date in a date picker. Correct means the application's final state matches the goal.

## Professional and office work (mixed)

**`gdpval`: GDPval**
A realistic work request written by an experienced professional in one of 44 occupations (e.g. customer service representatives, software developers, accountants, order clerks, administrative assistants, compliance officers, project managers), with reference files. The deliverable is usually a document, spreadsheet, slide deck or PDF. Correct means expert reviewers judge it at least as good as a professional's deliverable.

**`theagentcompany`: TheAgentCompany**
A task inside a simulated software company with a code host, project tracker, file share and team chat with colleagues. Covers developer, project-manager, HR, admin, finance and data roles. Example: collect equipment requests from colleagues by chat, look up prices in a shared spreadsheet, total them, and message the requester. Correct means checkpoints on the final files, records and messages pass.

**`jobbench`: JobBench**
A professional request with a folder of real public-record files, each tied to one O*NET task. Example (biostatistician): check a trial's analysis plan against cohort data, recompute the sample size under a new design, and tabulate baseline characteristics. Correct means a long checklist of expert criteria is met.

**`apex_agents`: APEX-Agents**
A task inside a simulated firm's files, email, chat, spreadsheets and presentations, for investment-banking analysts, management consultants or corporate lawyers. Examples: update a buyout model, build a comparables table, draft a legal certificate, find affected people in a spreadsheet. The worker returns a message or a file. Correct means every expert-written criterion is met.

## Customer service and contact centre

**`eva_bench`: EVA-Bench**
A phone call from a caller with a goal in one of three settings: airline customer service, HR service delivery, or an enterprise IT service desk (password resets, access requests, incident reports). Some callers are difficult or ask for several things. The worker queries and updates the relevant system during the call. Correct means the right records are changed and nothing false is said.

**`tau_banking`: τ³-bench banking knowledge**
A chat with a fintech customer about a dispute, refund, fee or cash-back question. The worker must find the relevant rule among about 700 internal policy documents, combine it with account data from tools, and make a compliant account change (e.g. correct a refund amount). Correct means the final account state matches the policy-correct outcome.

**`tau_telecom`: τ²-bench telecom troubleshooting**
A chat with a mobile customer reporting a problem such as "mobile data not working" or "can't send picture messages". The worker checks the account with tools and talks the customer through steps on their own phone (toggle airplane mode, reset network settings, check the plan), following a troubleshooting policy. Correct means the problem is fixed and the account is in the right state.

**`tau_retail_airline`: τ-bench retail and airline**
A chat with a customer who wants something done: exchange or return delivered items, change an order address, rebook or cancel a flight, add baggage. The worker has the company's policy document and tools to look up and change orders or bookings. They must verify the customer, check the policy, confirm, and make the right changes. Correct means the final database matches the correct outcome and required information was given to the customer.

**`crmarena_pro`: CRMArena-Pro**
A request handled in a company's Salesforce CRM through its data and search tools. Examples: route an incoming case to the best service agent; decide whether a quote breaks the discount policy; qualify a sales lead; answer a question from the knowledge base. Some requests come in a conversation where the requester reveals details gradually. Correct means the answer or chosen record is the right one.

**`tau_voice`: τ-Voice**
The same retail, airline and telecom requests as τ-bench, handled as live phone calls, with accents, background noise and interruptions; some versions in Hindi and other languages. Correct means the same database outcome as in the chat version.

**`sopbench`: SOPBench**
A customer request in a service setting (e.g. banking, healthcare appointments, records) with a written standard operating procedure and system tools. Example: verify the account and check the balance limit before making a transfer. Correct means every required procedure step was followed and the outcome is right.

## Healthcare administration

**`healthadminbench`: HealthAdminBench**
Revenue-cycle work across a hospital records system, insurance payer portals and a fax system. Examples: gather a patient's clinical documents and submit a prior-authorisation request on the right payer portal, then record the result; identify a high-value claim denial and file an appeal with supporting documents; process an equipment order. Correct means every step is correctly recorded in each system.

## IT operations, system administration and databases

**`cybench`: Cybench**
A professional capture-the-flag security challenge (cryptography, web exploitation, binary exploitation, reverse engineering, forensics) on a security-tools machine. The worker must find a hidden secret string. Correct means the exact string is found.

**`terminal_bench_2`: Terminal-Bench 2.0**
A Linux machine plus a written instruction, done entirely at the command line. About a third of the items are everyday IT administration: install and configure a web server with logging and rate limiting, set up a git server, recover a corrupted database file, summarise logs, optimise a query, fix a broken build. The rest are programming puzzles or research tasks. Correct means hidden tests check the final state of the machine.

**`itbench_sre`: ITBench (site reliability)**
A snapshot of a failing Kubernetes application: alerts, events, logs, traces, metrics and service topology. The worker investigates with command-line tools and reports which components caused the incident. Correct means every true root-cause component is named, with no wrong ones.

**`dba_bench`: DBA-Bench**
A live PostgreSQL database under load plus a symptom alert (e.g. checkout writes timing out). The worker diagnoses the cause using metrics, SQL and admin tools, then fixes it. Example: stale statistics cause a bad query plan, fixed by re-analysing the table. Correct means the problem is resolved and no unsafe action was taken.

**`spider2`: Spider 2.0**
A business question over a large company data warehouse (often 1,000+ columns) plus its documentation. The worker explores the schema and writes SQL; some items are full data-transformation projects. Correct means the query returns the right result table.

**`terminal_bench_4`: Terminal-Bench 3.0/4.x**
Same command-line format, longer tasks. Some are infrastructure work: migrate a live database, recover write-ahead logs, fix a payments data pipeline, build a web form. Others are operations work done with files and scripts: process a batch of medical claims against rules, adjudicate warranty claims, prepare a statistical compliance filing. Correct means hidden tests check the outputs and the machine state.

**`terminal_bench_1`: Terminal-Bench 1.0**
Same format as Terminal-Bench 2.0, with shorter everyday items. Example: "I checked out master and can't find my changes; find them and merge them in." Others cover git, builds and server setup.

## Software testing and QA

**`swt_bench`: SWT-bench Verified**
A bug report plus the code repository before the fix. The worker writes automated tests that reproduce the reported bug. Correct means the new tests fail on the original code and pass once the (hidden) fix is applied, and they exercise the changed code.

**`sweeper_bench`: SWEeper-Bench**
A running open-source web application plus an open-ended request such as "find and fix issues in board sharing and membership". The worker must explore the app in a browser, find the faulty behaviour (which may need many steps across several user accounts), and fix the code. Correct means a browser-based check confirms the intended behaviour now works and other behaviour still works.

## Finance, accounting and spreadsheets

**`apex_accounting`: APEX-Accounting**
Month-end close work in a fictional company's accounting system, spreadsheets and PDFs: reconcile an account, calculate and post accruals, enter transactions, prepare schedules, explain variances. Correct means the output meets every item on an accountant-written checklist.

**`vals_emb`: Vals Excel Modeling**
Build a complete investment-banking or private-equity Excel model (leveraged buyout, discounted cash flow, merger, operating model, comparables) from a prompt and source files, with standard formatting. Correct means key output cells match the reference model.

**`dualentry`: DualEntry accounting cases**
A short bookkeeping case given as data. Examples: classify a bank transaction to the right account ("$450 payment to Staples" → office supplies); write a journal entry; match items in a bank reconciliation; handle an accounts-payable or receivable entry. Correct means the account, amounts or classification are exactly right.

**`vals_finance_agent`: Vals Finance Agent**
A financial analyst's research question answered from public company filings and the web, with a calculator. Example: compare two retailers' inventory efficiency for a fiscal year and compute the difference in days inventory outstanding. Other items cover earnings beats and misses, adjustments, comparables and simple modelling. Correct means the answer matches the expert's on a checklist.

**`spreadsheetbench_2`: SpreadsheetBench 2**
A business workbook task: find and fix formula errors and hard-coded values, build or extend a financial model across many sheets, fill a template, or make a chart. Correct means the recalculated cells (or the chart) match the expected result.

**`finch`: Finch (enterprise finance workflows)**
A finance-team workflow rebuilt from real company emails and spreadsheets. Examples: import data, look up figures across several workbooks, calculate, validate, chart, and write a short report. A workflow has one to several such tasks. Correct means a finance expert accepts the output.

## Computer use: desktop and office workflows

**`osworld_verified`: OSWorld**
A single goal on a Linux desktop using common applications: a browser, a spreadsheet, a word processor, an email client, an image editor, a code editor, or the operating system's settings. Examples: turn on "Do Not Track" in the browser; fill a column with formulas; convert a sheet to a chart. Correct means a check of the final file or application state passes.

**`online_mind2web`: Online-Mind2Web**
A task on a named live consumer website, e.g. find the cheapest one-way flight between two cities on a date and add a carry-on option, or search rentals with given filters. Correct means the final page or action meets every stated condition.

**`osworld_2`: OSWorld 2.0**
A long end-to-end office workflow on a desktop with real input files, desktop applications and internal websites (email, banking, team chat, application portals, GitLab). Example: follow a PDF guide, extract data from receipts, cross-check it against bank and email records, and file an expense reimbursement claim in a portal. Items cover document preparation, finance and operations analysis, administration and compliance. Correct means every checkpoint on the final state passes.

**`officeval`: OmegaUse-OfficeVal**
A real office request with one or more Word, Excel, PowerPoint or PDF files. Examples: restructure a report, reformat a spreadsheet to a standard, extract data from documents into a table, annotate a document. Correct means the output meets an expert checklist without collateral damage to the files.

=== ITEMS ===
[2186a]
Occupation: Cooks, Restaurant
Task statement: Plan and price menu items.
Part: Plan menu items and set their prices based on food cost.
Type: DISCRETE
Work item: one menu or menu change with costed prices
Start: decision to add or revise dishes
End: final menu with prices approved
Checked by: chef or owner

[3403a]
Occupation: Budget Analysts
Task statement: Perform cost-benefit analyses to compare operating programs, review financial requests, or explore alternative financing methods.
Part: Perform a cost-benefit analysis comparing programs, reviewing requests or exploring financing.
Type: DISCRETE
Work item: one cost-benefit analysis
Start: question posed
End: analysis delivered
Checked by: management

[23074a]
Occupation: Police and Sheriff's Patrol Officers
Task statement: Inform citizens of community services and recommend options to facilitate longer-term problem resolution.
Part: Tell a citizen about community services and suggest options for longer-term resolution.
Type: LIVE_SERVICE
Work item: one citizen referred to community services during a contact
Start: citizen raises a problem or officer sees the need
End: citizen given information and referral
Checked by: the citizen, and the supervisor

[1412b]
Occupation: Mechanical Engineers
Task statement: Confer with engineers or other personnel to implement operating procedures, resolve system malfunctions, or provide technical information.
Part: Send written technical information or an answer to a colleague's query.
Type: DISCRETE
Work item: one written technical answer to a colleague
Start: query received
End: answer sent
Checked by: the colleague who asked

[245a]
Occupation: Child, Family, and School Social Workers
Task statement: Refer clients to community resources for services, such as job placement, debt counseling, legal aid, housing, medical treatment, or financial assistance, and provide concrete information, such as where to go and how to apply.
Part: Refer a client to a community resource and explain how to access it during a live contact.
Type: LIVE_SERVICE
Work item: one community resource referral made during a client contact
Start: client's need for a community resource identified
End: resource and application or access instructions provided to the client
Checked by: client and, where contacted, receiving agency

[667a]
Occupation: First-Line Supervisors of Retail Sales Workers
Task statement: Establish and implement policies, goals, objectives, and procedures for the department.
Part: Establish and put in place policies, goals, objectives and procedures for the department.
Type: DISCRETE
Work item: one department policy, goal set or procedure issued
Start: need or company target identified
End: policy or goals communicated to staff
Checked by: store manager or district manager

[7384a]
Occupation: Operations Research Analysts
Task statement: Prepare management reports defining and evaluating problems and recommending solutions.
Part: Write a management report defining and evaluating a problem and recommending solutions.
Type: DISCRETE
Work item: one management report
Start: analysis complete
End: report delivered to management
Checked by: management and the project lead

[18746a]
Occupation: Waiters and Waitresses
Task statement: Assist host or hostess by answering phones to take reservations or to-go orders, and by greeting, seating, and thanking guests.
Part: Answer the phone and take a dining reservation.
Type: LIVE_SERVICE
Work item: one phone reservation
Start: caller requests a reservation
End: reservation details are recorded and confirmed to the caller
Checked by: caller and host or hostess

[4739a]
Occupation: Shipping, Receiving, and Inventory Clerks
Task statement: Record shipment data, such as weight, charges, space availability, damages, or discrepancies, for reporting, accounting, or recordkeeping purposes.
Part: Record a shipment's weight, charges, space, damages and discrepancies in the shipping records.
Type: DISCRETE
Work item: one shipment record completed in the system
Start: shipment weighed, counted and inspected
End: record entered and saved with charges and exceptions noted
Checked by: accounting, inventory control, shipping supervisor

[304a]
Occupation: Graphic Designers
Task statement: Review final layouts and suggest improvements, as needed.
Part: Review a final layout and suggest improvements.
Type: DISCRETE
Work item: one final layout reviewed with suggested changes
Start: final layout ready for review
End: suggested improvements returned or layout signed off
Checked by: designer who made it, art director or client

[958a]
Occupation: Marketing Managers
Task statement: Use sales forecasting or strategic planning to ensure the sale and profitability of products, lines, or services, analyzing business developments and monitoring market trends.
Part: Prepare a sales forecast and strategic plan to ensure sales and profitability of products or lines.
Type: DISCRETE
Work item: one sales forecast and plan for a product line and period
Start: planning period begins and sales data collected
End: forecast and plan presented and approved
Checked by: senior management and finance

[98a]
Occupation: Training and Development Specialists
Task statement: Monitor, evaluate, or record training activities or program effectiveness.
Part: Record training activity such as attendance, completions and scores in the training records system.
Type: DISCRETE
Work item: one training session's records entered and closed out
Start: training session ends
End: attendance and results recorded in the training system
Checked by: training manager, HR, auditors

[1826a]
Occupation: Pharmacists
Task statement: Publish educational information for other pharmacists, doctors, or patients.
Part: Write educational information for pharmacists, doctors, or patients.
Type: DISCRETE
Work item: one educational handout, bulletin, or article
Start: topic chosen or requested
End: piece published or distributed
Checked by: editor or pharmacy manager, readers

[23876b]
Occupation: Stockers and Order Fillers
Task statement: Examine and inspect stock items for wear or defects, reporting any damage to supervisors.
Part: Report damaged stock to a supervisor.
Type: DISCRETE
Work item: one damage report to a supervisor
Start: damaged or worn item found
End: report delivered to the supervisor
Checked by: supervisor

[1278b]
Occupation: Computer Programmers
Task statement: Consult with and assist computer operators or system analysts to define and resolve problems in running computer programs.
Part: Investigate a program-running problem after receiving a request from an operator or analyst and report findings.
Type: DISCRETE
Work item: one follow-up investigation of a program-running problem
Start: a problem is referred for investigation
End: findings or recommended next steps are communicated to the operator or analyst
Checked by: the operator or system analyst

[2441a]
Occupation: Real Estate Sales Agents
Task statement: Confer with escrow companies, lenders, home inspectors, and pest control operators to ensure that terms and conditions of purchase agreements are met before closing dates.
Part: Coordinate with escrow, lender, inspector and pest control contacts so purchase conditions are met before closing.
Type: DISCRETE
Work item: one purchase transaction's pre-closing conditions tracked to completion
Start: purchase agreement accepted
End: all conditions confirmed met and closing cleared
Checked by: broker; buyer and seller; escrow

[9728a]
Occupation: First-Line Supervisors of Office and Administrative Support Workers
Task statement: Arrange for necessary maintenance or repair work.
Part: Arrange for maintenance or repair work.
Type: DISCRETE
Work item: one maintenance or repair job arranged
Start: fault reported
End: repair scheduled with vendor or facilities and confirmed done
Checked by: staff using the equipment, facilities

[7539a]
Occupation: Economists
Task statement: Formulate recommendations, policies, or plans to solve economic problems or to interpret markets.
Part: Formulate recommendations, policies or plans to solve an economic problem or interpret a market.
Type: DISCRETE
Work item: one recommendation memo or policy plan
Start: problem defined
End: recommendation delivered
Checked by: client, management

[19631a]
Occupation: Mechanical Engineers
Task statement: Recommend the use of utility or energy services that minimize carbon footprints.
Part: Recommend utility or energy services that minimize a client's carbon footprint.
Type: DISCRETE
Work item: one energy services recommendation
Start: client energy use understood
End: recommendation delivered
Checked by: client

[1427a]
Occupation: Mechanical Engineers
Task statement: Establish or coordinate the maintenance or safety procedures, service schedule, or supply of materials required to maintain machines or equipment in the prescribed condition.
Part: Establish maintenance or safety procedures, service schedules and supply of materials for equipment.
Type: DISCRETE
Work item: one maintenance and safety procedure and schedule for an equipment type
Start: equipment and maintenance needs identified
End: procedure and schedule issued
Checked by: maintenance manager, safety officer

[3426b]
Occupation: Loan Officers
Task statement: Prepare reports to send to customers whose accounts are delinquent, and forward irreconcilable accounts for collector action.
Part: Forward an irreconcilable account to a collector.
Type: DISCRETE
Work item: one account referred for collection
Start: efforts to resolve fail
End: account file transferred to the collector
Checked by: collections team

[2443a]
Occupation: Real Estate Sales Agents
Task statement: Prepare documents such as representation contracts, purchase agreements, closing statements, deeds, and leases.
Part: Prepare transaction documents such as representation contracts, purchase agreements, closing statements, deeds and leases.
Type: DISCRETE
Work item: one document set for a transaction (contract, agreement or lease)
Start: deal terms agreed
End: documents sent to parties for signature
Checked by: broker; clients; escrow or attorney

[23069a]
Occupation: Police and Sheriff's Patrol Officers
Task statement: Notify patrol units to take violators into custody or to provide needed assistance or medical aid.
Part: Tell patrol units to pick up violators or give help or medical aid.
Type: DISCRETE
Work item: one request for units to pick up a violator or give aid
Start: need for custody pickup or aid identified
End: responding unit acknowledges
Checked by: responding unit and dispatcher

[9723c]
Occupation: First-Line Supervisors of Office and Administrative Support Workers
Task statement: Design, implement, or evaluate staff training and development programs, customer service initiatives, or performance measurement criteria.
Part: Define or revise performance measurement criteria.
Type: DISCRETE
Work item: one set of performance criteria defined or revised
Start: need for measures identified
End: criteria approved and issued
Checked by: manager, HR

[7390a]
Occupation: Operations Research Analysts
Task statement: Develop business methods and procedures, including accounting systems, file systems, office systems, logistics systems, and production schedules.
Part: Develop business methods and procedures such as accounting, filing, logistics or production scheduling systems.
Type: DISCRETE
Work item: one business procedure or system design
Start: need for a new method identified
End: procedure documented and handed to the business
Checked by: process owner and management

[23067b]
Occupation: Police and Sheriff's Patrol Officers
Task statement: Investigate traffic accidents and other accidents to determine causes and to determine if a crime has been committed.
Part: Write up the accident findings in a crash report.
Type: DISCRETE
Work item: one crash report
Start: scene work finished
End: report submitted and approved
Checked by: supervisor, insurers, courts

[1423b]
Occupation: Mechanical Engineers
Task statement: Develop, coordinate, or monitor all aspects of production, including selection of manufacturing methods, fabrication, or operation of product designs.
Part: Coordinate or monitor production and address a production issue.
Type: DISCRETE
Work item: one production issue reviewed and coordinated
Start: production issue or variance identified
End: required action communicated to responsible personnel
Checked by: production manager or manufacturing team

[21471a]
Occupation: Project Management Specialists
Task statement: Monitor the performance of project team members to provide performance feedback.
Part: Assess and document a project team member's performance for feedback.
Type: DISCRETE
Work item: one team member performance assessment
Start: performance information for a team member is available for review
End: observations are recorded or prepared for feedback
Checked by: project manager or personnel manager

[51c]
Occupation: Medical and Health Services Managers
Task statement: Conduct and administer fiscal operations, including accounting, planning budgets, authorizing expenditures, establishing rates for services, and coordinating financial reporting.
Part: Review and authorize expenditures.
Type: DISCRETE
Work item: one expenditure authorization decision
Start: expenditure request is received
End: decision is recorded and communicated
Checked by: requesting staff, purchasing, and finance

[965a]
Occupation: Marketing Managers
Task statement: Conduct economic or commercial surveys to identify potential markets for products or services.
Part: Conduct economic or commercial surveys to identify potential markets for products or services.
Type: DISCRETE
Work item: one market opportunity assessment
Start: market question set
End: assessment delivered with the potential markets identified
Checked by: senior management

[2276a]
Occupation: Waiters and Waitresses
Task statement: Collect payments from customers.
Part: Take a customer's payment for the meal and return change or the card.
Type: LIVE_SERVICE
Work item: one table's payment taken
Start: customer hands over cash or card for the check
End: payment processed and change or receipt returned
Checked by: manager at cash-out, and the customer

[19630a]
Occupation: Mechanical Engineers
Task statement: Evaluate mechanical designs or prototypes for energy performance or environmental impact.
Part: Evaluate a mechanical design or prototype for energy performance and environmental impact.
Type: DISCRETE
Work item: one design energy and environmental evaluation
Start: design or prototype available
End: evaluation issued
Checked by: design team, client

[7377a]
Occupation: Operations Research Analysts
Task statement: Formulate mathematical or simulation models of problems, relating constants and variables, restrictions, alternatives, conflicting objectives, and their numerical parameters.
Part: Formulate a mathematical or simulation model of a problem with its variables, constraints and objectives.
Type: DISCRETE
Work item: one formulated model with documented assumptions
Start: problem defined and data available
End: model formulation documented and accepted for testing
Checked by: senior analyst or project lead

