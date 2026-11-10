You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Code each ITEM independently, in the order given; do not go
back and adjust earlier answers to make them consistent with later ones.

Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/bpo_v1/s1/batch0.json
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
## Healthcare administration

**`healthadminbench`: HealthAdminBench**
Revenue-cycle work across a hospital records system, insurance payer portals and a fax system. Examples: gather a patient's clinical documents and submit a prior-authorisation request on the right payer portal, then record the result; identify a high-value claim denial and file an appeal with supporting documents; process an equipment order. Correct means every step is correctly recorded in each system.

## IT service desk and enterprise web applications

**`webarena`: WebArena**
A goal stated in plain language on self-hosted copies of an online store and its admin back end, a GitLab server, a content management system, a forum and a map. Examples: update a product's price and mark it out of stock; count orders cancelled in a given month; change a repository setting. Correct means the answer or the changed data matches.

**`workarena_l1`: WorkArena (single actions in ServiceNow)**
One explicit instruction in a ServiceNow IT-service-management instance. Examples: create an incident with given fields, filter the incident list by priority and assignment group, order a laptop from the service catalog, find an answer in the knowledge base, read a value off a dashboard. Correct means the record, list state or answer matches the goal.

**`scuba`: SCUBA (Salesforce)**
A task in a real Salesforce organisation as an administrator, a sales rep or a service agent. Examples: create a leads report with a filter on status; add a formula field visible only to one user profile; update a case. Correct means the organisation's configuration and records match the goal.

**`ui_cube`: UI-CUBE**
Tasks in replicas of enterprise applications (Salesforce, SAP, Concur, Workday) and in standalone interface widgets. Examples: enter an expense report from given data, update stock records, move records from one application to another, pick a date in a date picker. Correct means the application's final state matches the goal.

**`workarena_pp`: WorkArena++ (multi-step ServiceNow tickets)**
A multi-step service-desk job in ServiceNow, given either as step-by-step instructions or as a ticket assigned to the worker, as a real employee would get it. Examples: onboard a new employee (create the user, order their hardware, assign the assets); find the staff member with the fewest open incidents and assign them a new problem; work out a budget from a dashboard and place the orders. Correct means every resulting record is right.

**`starshell`: StarShell enterprise tasks**
Record-keeping tasks in three business systems: ServiceNow (incidents, catalog orders, knowledge base), GitLab (repository and issue administration), and ERPNext (create sales invoices, sales orders and linked documents, sometimes chained). Correct means the records in the system match the goal.

## Finance, accounting and spreadsheets

**`vals_finance_agent`: Vals Finance Agent**
A financial analyst's research question answered from public company filings and the web, with a calculator. Example: compare two retailers' inventory efficiency for a fiscal year and compute the difference in days inventory outstanding. Other items cover earnings beats and misses, adjustments, comparables and simple modelling. Correct means the answer matches the expert's on a checklist.

**`spreadsheetbench_2`: SpreadsheetBench 2**
A business workbook task: find and fix formula errors and hard-coded values, build or extend a financial model across many sheets, fill a template, or make a chart. Correct means the recalculated cells (or the chart) match the expected result.

**`finch`: Finch (enterprise finance workflows)**
A finance-team workflow rebuilt from real company emails and spreadsheets. Examples: import data, look up figures across several workbooks, calculate, validate, chart, and write a short report. A workflow has one to several such tasks. Correct means a finance expert accepts the output.

**`dualentry`: DualEntry accounting cases**
A short bookkeeping case given as data. Examples: classify a bank transaction to the right account ("$450 payment to Staples" → office supplies); write a journal entry; match items in a bank reconciliation; handle an accounts-payable or receivable entry. Correct means the account, amounts or classification are exactly right.

**`apex_accounting`: APEX-Accounting**
Month-end close work in a fictional company's accounting system, spreadsheets and PDFs: reconcile an account, calculate and post accruals, enter transactions, prepare schedules, explain variances. Correct means the output meets every item on an accountant-written checklist.

**`vals_emb`: Vals Excel Modeling**
Build a complete investment-banking or private-equity Excel model (leveraged buyout, discounted cash flow, merger, operating model, comparables) from a prompt and source files, with standard formatting. Correct means key output cells match the reference model.

## Software testing and QA

**`swt_bench`: SWT-bench Verified**
A bug report plus the code repository before the fix. The worker writes automated tests that reproduce the reported bug. Correct means the new tests fail on the original code and pass once the (hidden) fix is applied, and they exercise the changed code.

**`sweeper_bench`: SWEeper-Bench**
A running open-source web application plus an open-ended request such as "find and fix issues in board sharing and membership". The worker must explore the app in a browser, find the faulty behaviour (which may need many steps across several user accounts), and fix the code. Correct means a browser-based check confirms the intended behaviour now works and other behaviour still works.

## Customer service and contact centre

**`tau_voice`: τ-Voice**
The same retail, airline and telecom requests as τ-bench, handled as live phone calls, with accents, background noise and interruptions; some versions in Hindi and other languages. Correct means the same database outcome as in the chat version.

**`tau_retail_airline`: τ-bench retail and airline**
A chat with a customer who wants something done: exchange or return delivered items, change an order address, rebook or cancel a flight, add baggage. The worker has the company's policy document and tools to look up and change orders or bookings. They must verify the customer, check the policy, confirm, and make the right changes. Correct means the final database matches the correct outcome and required information was given to the customer.

**`tau_telecom`: τ²-bench telecom troubleshooting**
A chat with a mobile customer reporting a problem such as "mobile data not working" or "can't send picture messages". The worker checks the account with tools and talks the customer through steps on their own phone (toggle airplane mode, reset network settings, check the plan), following a troubleshooting policy. Correct means the problem is fixed and the account is in the right state.

**`sopbench`: SOPBench**
A customer request in a service setting (e.g. banking, healthcare appointments, records) with a written standard operating procedure and system tools. Example: verify the account and check the balance limit before making a transfer. Correct means every required procedure step was followed and the outcome is right.

**`eva_bench`: EVA-Bench**
A phone call from a caller with a goal in one of three settings: airline customer service, HR service delivery, or an enterprise IT service desk (password resets, access requests, incident reports). Some callers are difficult or ask for several things. The worker queries and updates the relevant system during the call. Correct means the right records are changed and nothing false is said.

**`crmarena_pro`: CRMArena-Pro**
A request handled in a company's Salesforce CRM through its data and search tools. Examples: route an incoming case to the best service agent; decide whether a quote breaks the discount policy; qualify a sales lead; answer a question from the knowledge base. Some requests come in a conversation where the requester reveals details gradually. Correct means the answer or chosen record is the right one.

**`tau_banking`: τ³-bench banking knowledge**
A chat with a fintech customer about a dispute, refund, fee or cash-back question. The worker must find the relevant rule among about 700 internal policy documents, combine it with account data from tools, and make a compliant account change (e.g. correct a refund amount). Correct means the final account state matches the policy-correct outcome.

## Professional and office work (mixed)

**`theagentcompany`: TheAgentCompany**
A task inside a simulated software company with a code host, project tracker, file share and team chat with colleagues. Covers developer, project-manager, HR, admin, finance and data roles. Example: collect equipment requests from colleagues by chat, look up prices in a shared spreadsheet, total them, and message the requester. Correct means checkpoints on the final files, records and messages pass.

**`gdpval`: GDPval**
A realistic work request written by an experienced professional in one of 44 occupations (e.g. customer service representatives, software developers, accountants, order clerks, administrative assistants, compliance officers, project managers), with reference files. The deliverable is usually a document, spreadsheet, slide deck or PDF. Correct means expert reviewers judge it at least as good as a professional's deliverable.

**`apex_agents`: APEX-Agents**
A task inside a simulated firm's files, email, chat, spreadsheets and presentations, for investment-banking analysts, management consultants or corporate lawyers. Examples: update a buyout model, build a comparables table, draft a legal certificate, find affected people in a spreadsheet. The worker returns a message or a file. Correct means every expert-written criterion is met.

**`jobbench`: JobBench**
A professional request with a folder of real public-record files, each tied to one O*NET task. Example (biostatistician): check a trial's analysis plan against cohort data, recompute the sample size under a new design, and tabulate baseline characteristics. Correct means a long checklist of expert criteria is met.

## Software development and maintenance

**`swe_bench_pro`: SWE-bench Pro**
An issue description, written requirements and an interface specification for a product codebase (Python, Go, JavaScript/TypeScript), some from private company repositories. The change typically touches several files (around 100 lines across 4 files). Correct means hidden tests for the new behaviour pass and existing tests still pass.

**`swe_rebench`: SWE-rebench / SWE-bench Live**
Recently filed bug reports and requests on open-source repositories, collected each month, in the same format as SWE-bench: issue plus repository in, code change out, judged by hidden tests.

**`metr_th`: METR task suite**
Self-contained technical tasks in a sandboxed computer with a written instruction. Examples: fix a bug in a machine-learning codebase, write a script that processes data, solve a security challenge, optimise a model training run. A few items are single quick actions, such as choosing which file to open. Each task has an automatic scoring function that checks the result.

**`swe_bench_verified`: SWE-bench Verified**
A bug report or feature request (a GitHub issue) for an open-source Python library, plus the full code repository. The worker must change the code so the described problem is fixed. Correct means hidden unit tests that check the fix pass, and existing tests still pass.

**`swe_lancer`: SWE-Lancer (individual contributor tasks)**
A real paid freelance job on a commercial expense-management app (React Native / TypeScript), e.g. make the zip-code hint text consistent across two screens, or fix a broken workflow. The worker gets the job description and the codebase and submits a code change. Correct means end-to-end browser tests written by engineers pass.

**`multi_swe_bench`: Multi-SWE-bench**
Same as SWE-bench, but the repositories are in Java, TypeScript, JavaScript, Go, Rust, C and C++. Example: a Java RPC library fails to convert date and time types; fix the conversion. Correct means hidden tests that reproduce the issue now pass.

**`swe_bench_multimodal`: SWE-bench Multimodal**
A bug report for a JavaScript front-end library that includes screenshots of the visual problem (e.g. a tab component rendering wrongly), plus the repository. The worker changes the code; correct means hidden tests, some comparing rendered output, pass.

## Computer use: desktop and office workflows

**`officeval`: OmegaUse-OfficeVal**
A real office request with one or more Word, Excel, PowerPoint or PDF files. Examples: restructure a report, reformat a spreadsheet to a standard, extract data from documents into a table, annotate a document. Correct means the output meets an expert checklist without collateral damage to the files.

**`osworld_verified`: OSWorld**
A single goal on a Linux desktop using common applications: a browser, a spreadsheet, a word processor, an email client, an image editor, a code editor, or the operating system's settings. Examples: turn on "Do Not Track" in the browser; fill a column with formulas; convert a sheet to a chart. Correct means a check of the final file or application state passes.

**`osworld_2`: OSWorld 2.0**
A long end-to-end office workflow on a desktop with real input files, desktop applications and internal websites (email, banking, team chat, application portals, GitLab). Example: follow a PDF guide, extract data from receipts, cross-check it against bank and email records, and file an expense reimbursement claim in a portal. Items cover document preparation, finance and operations analysis, administration and compliance. Correct means every checkpoint on the final state passes.

**`online_mind2web`: Online-Mind2Web**
A task on a named live consumer website, e.g. find the cheapest one-way flight between two cities on a date and add a carry-on option, or search rentals with given filters. Correct means the final page or action meets every stated condition.

## IT operations, system administration and databases

**`itbench_sre`: ITBench (site reliability)**
A snapshot of a failing Kubernetes application: alerts, events, logs, traces, metrics and service topology. The worker investigates with command-line tools and reports which components caused the incident. Correct means every true root-cause component is named, with no wrong ones.

**`terminal_bench_1`: Terminal-Bench 1.0**
Same format as Terminal-Bench 2.0, with shorter everyday items. Example: "I checked out master and can't find my changes; find them and merge them in." Others cover git, builds and server setup.

**`terminal_bench_4`: Terminal-Bench 3.0/4.x**
Same command-line format, longer tasks. Some are infrastructure work: migrate a live database, recover write-ahead logs, fix a payments data pipeline, build a web form. Others are operations work done with files and scripts: process a batch of medical claims against rules, adjudicate warranty claims, prepare a statistical compliance filing. Correct means hidden tests check the outputs and the machine state.

**`cybench`: Cybench**
A professional capture-the-flag security challenge (cryptography, web exploitation, binary exploitation, reverse engineering, forensics) on a security-tools machine. The worker must find a hidden secret string. Correct means the exact string is found.

**`dba_bench`: DBA-Bench**
A live PostgreSQL database under load plus a symptom alert (e.g. checkout writes timing out). The worker diagnoses the cause using metrics, SQL and admin tools, then fixes it. Example: stale statistics cause a bad query plan, fixed by re-analysing the table. Correct means the problem is resolved and no unsafe action was taken.

**`spider2`: Spider 2.0**
A business question over a large company data warehouse (often 1,000+ columns) plus its documentation. The worker explores the schema and writes SQL; some items are full data-transformation projects. Correct means the query returns the right result table.

**`terminal_bench_2`: Terminal-Bench 2.0**
A Linux machine plus a written instruction, done entirely at the command line. About a third of the items are everyday IT administration: install and configure a web server with logging and rate limiting, set up a git server, recover a corrupted database file, summarise logs, optimise a query, fix a broken build. The rest are programming puzzles or research tasks. Correct means hidden tests check the final state of the machine.

=== ITEMS ===
[3465d]
Occupation: Computer Systems Analysts
Task statement: Test, maintain, and monitor computer programs and systems, including coordinating the installation of computer programs and systems.
Part: Coordinate the installation of a program or system with users and technical staff.
Type: DISCRETE
Work item: one installation or rollout coordinated
Start: installation scheduled
End: installation complete and accepted
Checked by: users and IT manager

[23317a]
Occupation: Insurance Claims and Policy Processing Clerks
Task statement: Contact insured or other involved persons to obtain missing information.
Part: Phone the insured or other involved person and obtain missing claim information while they are on the line.
Type: LIVE_SERVICE
Work item: one outbound call to obtain missing claim information
Start: person reached and asked for the missing details
End: information obtained and noted on file
Checked by: the insured, and the adjuster waiting for the data

[3482a]
Occupation: Computer Systems Analysts
Task statement: Use the computer in the analysis and solution of business problems, such as development of integrated production and inventory control and cost analysis systems.
Part: Use the computer to analyze and solve a business problem, e.g. building a production, inventory or cost system.
Type: DISCRETE
Work item: one business problem analyzed and solved
Start: problem posed
End: solution delivered
Checked by: the requesting business unit

[1324a]
Occupation: Network and Computer Systems Administrators
Task statement: Confer with network users about solutions to existing system problems.
Part: Talk to a user, while they are on the line or at the desk, about a current system problem.
Type: LIVE_SERVICE
Work item: one live conversation about a system problem
Start: user calls or arrives with a problem
End: problem fixed or referred and user told
Checked by: the user and the IT manager

[3464a]
Occupation: Computer Systems Analysts
Task statement: Provide staff and users with assistance solving computer-related problems, such as malfunctions and program problems.
Part: Help a user fix a computer problem while the user is on the phone, chat or at the desk.
Type: LIVE_SERVICE
Work item: one user problem fixed during a live contact
Start: user reports the problem
End: user confirms it works
Checked by: the user

[23263a]
Occupation: Billing and Posting Clerks
Task statement: Compile reports of cost factors, such as labor, production, storage, and equipment.
Part: Compile a report of cost factors such as labor, production, storage and equipment.
Type: DISCRETE
Work item: one cost factor report
Start: period ends
End: report delivered
Checked by: management

[3465c]
Occupation: Computer Systems Analysts
Task statement: Test, maintain, and monitor computer programs and systems, including coordinating the installation of computer programs and systems.
Part: Investigate a monitoring alert or exception for a computer program or system.
Type: DISCRETE
Work item: one monitoring alert or exception investigated
Start: alert or exception appears in monitoring results
End: findings and any necessary escalation are recorded
Checked by: operations team

[11406a]
Occupation: Data Entry Keyers
Task statement: Maintain logs of activities and completed work.
Part: Keep a log of activities and completed work.
Type: DISCRETE
Work item: one shift's work log
Start: shift starts
End: log completed
Checked by: supervisor

[23315a]
Occupation: Insurance Claims and Policy Processing Clerks
Task statement: Post or attach information to claim file.
Part: Post or attach incoming information and documents to a claim file.
Type: DISCRETE
Work item: one batch of documents posted to claim files
Start: documents or information received
End: items attached and file updated
Checked by: adjuster and downstream claim handlers

[21670a]
Occupation: Software Developers
Task statement: Modify existing software to correct errors, adapt it to new hardware, or upgrade interfaces and improve performance.
Part: Change existing software to fix an error, adapt it to new hardware, update an interface or improve performance.
Type: DISCRETE
Work item: one change request or bug fix to existing software
Start: change or bug ticket assigned
End: change tested, merged and released
Checked by: code reviewer, QA and users

[23256a]
Occupation: Billing and Posting Clerks
Task statement: Track accumulated hours and dollar amounts charged to each client job to calculate client fees for professional services, such as legal or accounting services.
Part: Track hours and dollars charged to a client job and calculate the client fee.
Type: DISCRETE
Work item: one client job's fee calculated
Start: billing period closes
End: fee ready to bill
Checked by: client; supervisor

[1328a]
Occupation: Network and Computer Systems Administrators
Task statement: Gather data pertaining to customer needs, and use the information to identify, predict, interpret, and evaluate system and network requirements.
Part: Gather data about customer needs and use it to identify, predict and evaluate system and network requirements.
Type: DISCRETE
Work item: one system requirements assessment
Start: customer need raised
End: requirements assessment delivered
Checked by: IT manager and customer

[23265a]
Occupation: Billing and Posting Clerks
Task statement: Perform general administrative tasks, such as answering telephones, scheduling appointments, and ordering supplies or equipment.
Part: Answer and direct a general telephone call.
Type: LIVE_SERVICE
Work item: one general telephone call answered and handled
Start: telephone call received
End: caller's request handled or call transferred
Checked by: caller and receiving staff

[23333a]
Occupation: Insurance Claims and Policy Processing Clerks
Task statement: Obtain computer printout of policy cancellations, or retrieve cancellation cards from file.
Part: Obtain a computer printout of policy cancellations.
Type: DISCRETE
Work item: one policy-cancellation printout
Start: cancellation list needed and system data available
End: printout generated and made available
Checked by: policy administration or accounting staff

[3478a]
Occupation: Computer Systems Analysts
Task statement: Review and analyze computer printouts and performance indicators to locate code problems, and correct errors by correcting codes.
Part: Review printouts and performance indicators to find a code problem and correct the code.
Type: DISCRETE
Work item: one code defect located and corrected
Start: problem indicator noticed
End: corrected code verified
Checked by: project lead; users

[14710a]
Occupation: Web Developers
Task statement: Perform Web site tests according to planned schedules, or after any Web site or product revision.
Part: Run website tests on a planned schedule or after any site or product change.
Type: DISCRETE
Work item: one website test run
Start: scheduled time or site revision completed
End: results recorded and defects reported
Checked by: development team lead

[15208d]
Occupation: Network and Computer Systems Administrators
Task statement: Implement and provide technical support for voice services and equipment, such as private branch exchange, voice mail system, and telecom system.
Part: Resolve a voice service support issue outside a live user contact.
Type: DISCRETE
Work item: one voice service support issue handled
Start: voice service incident or request is assigned
End: outcome is verified and recorded, or the issue is escalated
Checked by: voice operations team and affected user

[14704a]
Occupation: Web Developers
Task statement: Develop databases that support Web applications and Web sites.
Part: Build or change a database that supports a website or web application.
Type: DISCRETE
Work item: one database or schema built or changed
Start: data requirements known
End: database working and handed to developers
Checked by: application developers and tech lead

[23255a]
Occupation: Billing and Posting Clerks
Task statement: Consult sources, such as rate books, manuals, or insurance company representatives, to determine specific charges or information such as rules, regulations, or government tax and tariff information.
Part: Consult rate books, manuals or insurers to find the correct charge or rule.
Type: DISCRETE
Work item: one charge or rule determined
Start: question arises
End: answer found
Checked by: supervisor

[2498c]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Perform general office duties, such as filing, answering telephones, and handling routine correspondence.
Part: Answer and handle a routine incoming call.
Type: LIVE_SERVICE
Work item: one routine incoming call handled
Start: incoming call received
End: caller answered, directed, or transferred
Checked by: caller or receiving staff member

[21649a]
Occupation: Database Administrators
Task statement: Plan and install upgrades of database management system software to enhance database performance.
Part: Plan and install an upgrade to the database management system software.
Type: DISCRETE
Work item: one DBMS upgrade planned and installed
Start: upgrade decided
End: upgrade verified in production
Checked by: management and users

[22877a]
Occupation: Medical Records Specialists
Task statement: Assign the patient to diagnosis-related groups (DRGs), using appropriate computer software.
Part: Assign a patient case to a DRG using grouper software.
Type: DISCRETE
Work item: one inpatient encounter assigned a DRG
Start: codes finalized
End: DRG recorded
Checked by: coding auditor, billing

[23323a]
Occupation: Insurance Claims and Policy Processing Clerks
Task statement: Review and verify data, such as age, name, address, and principal sum and value of property, on insurance applications and policies.
Part: Review an application or policy and verify the data on it.
Type: DISCRETE
Work item: one application or policy verified
Start: document received
End: verified or corrected and returned
Checked by: underwriter or supervisor

[14707a]
Occupation: Web Developers
Task statement: Write supporting code for Web applications or Web sites.
Part: Write supporting code for a web application or website.
Type: DISCRETE
Work item: one supporting code change
Start: task assigned
End: code reviewed and merged
Checked by: code reviewer and development team

[3474a]
Occupation: Computer Systems Analysts
Task statement: Analyze information processing or computation needs and plan and design computer systems, using techniques such as structured analysis, data modeling, and information engineering.
Part: Analyze information processing needs and produce a system design using structured analysis and data modeling.
Type: DISCRETE
Work item: one system design
Start: requirements gathered
End: design document approved
Checked by: project lead; developers

[1325b]
Occupation: Network and Computer Systems Administrators
Task statement: Monitor network performance to determine whether adjustments are needed and where changes will be needed in the future.
Part: Write a periodic network performance and capacity report on future changes.
Type: DISCRETE
Work item: one periodic performance report
Start: reporting period ends
End: report sent
Checked by: IT manager

[1311a]
Occupation: Database Administrators
Task statement: Select and enter codes to monitor database performance and to create production databases.
Part: Enter commands to set up monitoring of database performance.
Type: DISCRETE
Work item: one performance monitoring setup
Start: database needs monitoring
End: monitoring working
Checked by: DBA team

[23239a]
Occupation: Billing and Posting Clerks
Task statement: Verify signatures and required information on checks.
Part: Verify signatures and required information on checks.
Type: DISCRETE
Work item: one batch of checks verified
Start: checks received
End: checks passed or returned
Checked by: supervisor

[14705a]
Occupation: Web Developers
Task statement: Renew domain name registrations.
Part: Renew a domain name registration.
Type: DISCRETE
Work item: one domain renewal
Start: renewal notice or due date
End: renewal confirmed
Checked by: site owner or management

[23330a]
Occupation: Insurance Claims and Policy Processing Clerks
Task statement: Collect initial premiums and issue receipts.
Part: Take an initial premium and issue a receipt while the customer is on the line or present.
Type: LIVE_SERVICE
Work item: one premium taken and receipted during contact
Start: customer agrees to pay
End: receipt confirmed
Checked by: customer; accounting

[23262b]
Occupation: Billing and Posting Clerks
Task statement: Answer inquiries regarding rates, routing, or procedures.
Part: Answer a written inquiry about rates, routing, or procedures.
Type: DISCRETE
Work item: one written rates, routing, or procedures inquiry answered
Start: written inquiry received
End: answer sent to the requester
Checked by: requester and, if reviewed, a supervisor

[23266b]
Occupation: Billing and Posting Clerks
Task statement: Return checks to customers or retrieve checks returned to customers in error, adjusting accounts and answering inquiries about errors as necessary.
Part: Adjust an account to correct an error involving a returned check.
Type: DISCRETE
Work item: one account adjustment for a check-return error
Start: check-return error and required correction identified
End: account adjustment entered or submitted for approval
Checked by: accounting staff or a supervisor

[23240a]
Occupation: Billing and Posting Clerks
Task statement: Prepare itemized statements, bills, or invoices and record amounts due for items purchased or services rendered.
Part: Prepare itemized statements, bills or invoices and record amounts due.
Type: DISCRETE
Work item: one batch of invoices prepared and recorded
Start: billing data ready
End: invoices ready to send
Checked by: customers; supervisor

[21676a]
Occupation: Software Developers
Task statement: Store, retrieve, and manipulate data for analysis of system capabilities and requirements.
Part: Pull and work with data to analyze a system's capabilities and requirements.
Type: DISCRETE
Work item: one data analysis of system capabilities or requirements
Start: question about capacity or requirements raised
End: findings delivered
Checked by: project manager and systems analysts

[1320a]
Occupation: Network and Computer Systems Administrators
Task statement: Operate master consoles to monitor the performance of computer systems and networks and to coordinate computer network access and use.
Part: Handle an alert or issue seen on the master console.
Type: DISCRETE
Work item: one console alert handled
Start: alert seen
End: fixed or escalated and logged
Checked by: IT manager and affected users

[3476b]
Occupation: Computer Systems Analysts
Task statement: Define the goals of the system and devise flow charts and diagrams describing logical operational steps of programs.
Part: Create flowcharts or diagrams describing the logical operational steps of a program.
Type: DISCRETE
Work item: one program logic diagram or diagram set
Start: program function and requirements identified
End: logic diagrams completed and shared
Checked by: programmers and technical lead

[1324b]
Occupation: Network and Computer Systems Administrators
Task statement: Confer with network users about solutions to existing system problems.
Part: Follow up with a user about a system problem by email or ticket.
Type: DISCRETE
Work item: one written follow-up on a system problem
Start: user message or ticket received
End: reply sent and ticket updated
Checked by: the user

[1325a]
Occupation: Network and Computer Systems Administrators
Task statement: Monitor network performance to determine whether adjustments are needed and where changes will be needed in the future.
Part: Investigate a performance alert on the network and decide if an adjustment is needed.
Type: DISCRETE
Work item: one performance alert investigated
Start: alert or slowdown noticed
End: adjustment made or finding logged
Checked by: IT manager

[3484a]
Occupation: Computer Systems Analysts
Task statement: Specify inputs accessed by the system and plan the distribution and use of the results.
Part: Specify the inputs a system will use and plan how its results are distributed and used.
Type: DISCRETE
Work item: one input/output specification
Start: system design underway
End: specification approved
Checked by: developers; users

[21666a]
Occupation: Software Developers
Task statement: Coordinate installation of software system.
Part: Coordinate the installation of a software system with users, IT staff and vendors until it is in service.
Type: DISCRETE
Work item: one software system installation coordinated
Start: installation approved and scheduled
End: system installed, verified and handed to users
Checked by: users and IT operations

[2500a]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Receive, record, and bank cash, checks, and vouchers.
Part: Take cash or a check from a payer at the counter, record it and give a receipt.
Type: LIVE_SERVICE
Work item: one payment received at the counter
Start: payer hands over payment
End: payment recorded and receipt given
Checked by: payer and cash supervisor

[23260a]
Occupation: Billing and Posting Clerks
Task statement: Review compiled data on operating costs and revenues to set rates.
Part: Review cost and revenue data to set rates.
Type: DISCRETE
Work item: one rate decision
Start: review period
End: rates set or recommended
Checked by: management

[1318b]
Occupation: Network and Computer Systems Administrators
Task statement: Maintain and administer computer networks and related computing environments, including computer hardware, systems software, applications software, and all configurations.
Part: Handle an administration request such as an account, access or software setup.
Type: DISCRETE
Work item: one administration request handled
Start: request logged
End: request completed and user told
Checked by: the requesting user

[23251a]
Occupation: Billing and Posting Clerks
Task statement: Compare previously prepared bank statements with canceled checks and reconcile discrepancies.
Part: Compare bank statements with canceled checks and reconcile discrepancies.
Type: DISCRETE
Work item: one bank statement reconciliation
Start: statement received
End: reconciled
Checked by: supervisor

[1333a]
Occupation: Network and Computer Systems Administrators
Task statement: Coordinate with vendors and with company personnel to facilitate purchases.
Part: Coordinate with vendors and company staff so that a purchase is made.
Type: DISCRETE
Work item: one purchase coordinated
Start: need approved
End: order placed with vendor
Checked by: purchasing or IT manager

[22892a]
Occupation: Medical Records Specialists
Task statement: Schedule medical appointments for patients.
Part: Book an appointment while the patient is on the phone or at the desk.
Type: LIVE_SERVICE
Work item: one appointment booked during contact
Start: patient requests
End: slot confirmed
Checked by: patient, clinic

