You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Code each ITEM independently, in the order given; do not go
back and adjust earlier answers to make them consistent with later ones.

Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/pilot_v4c/s2/batch0.json
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
### Example A — Bookkeeping, Accounting, and Auditing Clerks
Work item: one batch of postings checked (e.g. a day's entries for one ledger). Start: batch of
entries and source documents received for review. End: batch marked verified, with errors corrected
or flagged. Checked by: senior accountant or auditor. Type: DISCRETE.

```json
{
  "item_id": "example-A",
  "unit_flag": false, "unit_flag_reason": "",
  "domain_reasoning": "Most of the time goes into opening entries in the accounting system and comparing them with source documents on screen.",
  "domain": "computer_use",
  "length_reasoning": "A small batch of routine entries takes a quarter of an hour; a month-end batch with many accruals and exceptions takes a couple of hours.",
  "length_p10": 15, "length_p50": 40, "length_p90": 120, "two_groups": false,
  "review_reasoning": "A senior accountant checks a short batch by opening the sign-off and spot-checking a few entries; a typical batch needs a few more entries traced to source; a month-end batch needs the exceptions and accruals checked one by one.",
  "review_p10": 4, "review_p50": 8, "review_p90": 18,
  "stakes_reasoning": "A missed miscoding usually surfaces at reconciliation and is corrected by a journal entry; a large one can reach the financial statements.",
  "stakes": "medium", "stakes_p90": "high",
  "context_reasoning": "Needs the company's chart of accounts and coding rules, learned over a few weeks.",
  "context": "medium",
  "match_reasoning": "APEX-Accounting items are month-end accounting work in an accounting system against source documents, which shares the main actions, but they produce entries and reconciliations rather than checking someone else's. DualEntry also has single bookkeeping entries, but as short cases given as data rather than a batch checked in a system.",
  "best": "apex_accounting", "best_match": "partial",
  "best_difference": "the benchmark produces accounting work; this item checks work already entered",
  "second": "dualentry", "second_match": "partial"
}
```

### Example B — Network and Computer Systems Administrators
Work item: one performance alert investigated. Start: alert raised by monitoring tool. End: cause
recorded and either adjustment requested or alert closed as no action. Checked by: on-call lead /
change board. Type: DISCRETE.

```json
{
  "item_id": "example-B",
  "unit_flag": false, "unit_flag_reason": "",
  "domain_reasoning": "The work is in monitoring dashboards, logs and device consoles.",
  "domain": "computer_use",
  "length_reasoning": "Most alerts are transient or known and closed in minutes; a real fault can take an hour or more to trace.",
  "length_p10": 5, "length_p50": 20, "length_p90": 90, "two_groups": true,
  "review_reasoning": "For a quick alert the lead reads the closing note and glances at the triggering graph; a typical one also needs the cause checked against the logs; a long investigation needs its chain of reasoning followed.",
  "review_p10": 2, "review_p50": 4, "review_p90": 12,
  "stakes_reasoning": "A wrongly closed alert usually recurs and is caught, but a missed real fault can become an outage.",
  "stakes": "medium", "stakes_p90": "high",
  "context_reasoning": "Telling noise from a real problem needs months of knowing this network's normal behaviour and history.",
  "context": "high",
  "match_reasoning": "ITBench items start from alerts and telemetry and end with the cause named, which is the same investigation, but for application services on Kubernetes rather than network devices. Terminal-Bench 2 has some system-administration diagnosis at the command line, but mostly configuration rather than alert triage.",
  "best": "itbench_sre", "best_match": "partial",
  "best_difference": "application incidents on Kubernetes rather than network performance",
  "second": "terminal_bench_2", "second_match": "partial"
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
[14661a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Perform initial debugging procedures by reviewing configuration files, logs, or code pieces to determine breakdown source.
Part: Review configuration files, logs, or code to find the likely source of a failure.
Type: DISCRETE
Work item: one defect given an initial root-cause diagnosis
Start: failure reported or reproduced
End: likely source recorded on the ticket and handed to developers
Checked by: developers

[2582a]
Occupation: Customer Service Representatives
Task statement: Refer unresolved customer grievances to designated departments for further investigation.
Part: Prepare and route a referral of an unresolved customer grievance to the designated department for investigation.
Type: DISCRETE
Work item: one grievance referral ticket
Start: representative determines the grievance cannot be resolved at first level
End: referral with case details submitted to the designated department
Checked by: receiving department and supervisor

[2585b]
Occupation: Customer Service Representatives
Task statement: Obtain and examine all relevant information to assess validity of complaints and to determine possible causes, such as extreme weather conditions that could increase utility bills.
Part: Gather and examine records and outside information to investigate a complaint's validity and cause after the contact.
Type: DISCRETE
Work item: one complaint investigation with a validity finding
Start: complaint case opened for review
End: finding on validity and cause recorded and passed for remedy or reply
Checked by: supervisor, and the staff who decide the remedy

[14651a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Investigate customer problems referred by technical support.
Part: Investigate a customer problem referred by technical support and report the findings.
Type: DISCRETE
Work item: one escalated customer problem investigated
Start: escalation ticket received from technical support
End: problem reproduced or not, findings returned to support, and defect filed if needed
Checked by: technical support / developers

[1282a]
Occupation: Computer User Support Specialists
Task statement: Answer user inquiries regarding computer software or hardware operation to resolve problems.
Part: Answer a user's question about software or hardware operation while the user is on the phone, in chat, or at the desk, resolving the problem during the contact.
Type: LIVE_SERVICE
Work item: one user call, chat, or walk-up question answered
Start: user calls, opens a chat, or walks up with a question
End: user confirms the answer or fix works, or the issue is logged for follow-up
Checked by: the user who asked; help-desk supervisor through call reviews

[18565b]
Occupation: Customer Service Representatives
Task statement: Confer with customers by telephone or in person to provide information about products or services, take or enter orders, cancel accounts, or obtain details of complaints.
Part: Take and enter an order or cancel an account while the customer is on the line or at the desk.
Type: LIVE_SERVICE
Work item: one order or account cancellation entered during a contact
Start: customer asks to order or cancel
End: order or cancellation confirmed to the customer
Checked by: the customer and the fulfilment or billing team

[18565c]
Occupation: Customer Service Representatives
Task statement: Confer with customers by telephone or in person to provide information about products or services, take or enter orders, cancel accounts, or obtain details of complaints.
Part: Obtain the details of a customer's complaint during a call or visit.
Type: LIVE_SERVICE
Work item: one complaint taken during a call or visit
Start: customer raises a complaint
End: complaint details captured and next steps explained to the customer
Checked by: the customer and the staff who investigate or resolve it

[1287b]
Occupation: Computer User Support Specialists
Task statement: Maintain records of daily data communication transactions, problems and remedial actions taken, or installation activities.
Part: Keep the daily log of data communication transactions and installation activities.
Type: DISCRETE
Work item: one day's log of transactions and installation activities
Start: start of day or shift
End: day's entries complete and log filed
Checked by: IT supervisor; auditors

[14662a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Visit beta testing sites to evaluate software performance.
Part: Evaluate software performance at a beta testing site.
Type: DISCRETE
Work item: one beta-site performance evaluation
Start: a beta site and evaluation objectives are identified
End: site observations and performance findings are documented or shared
Checked by: product team and test lead

[14644a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Create or maintain databases of known test defects.
Part: Set up a database or tracker project for known test defects.
Type: DISCRETE
Work item: one known-defects database set up
Start: need for a defect repository agreed
End: database configured with fields and workflows and opened to the team
Checked by: QA manager / team users

[2584a]
Occupation: Customer Service Representatives
Task statement: Complete contract forms, prepare change of address records, or issue service discontinuance orders, using computers.
Part: Complete a contract form, change-of-address record, or service discontinuance order in the computer while the customer is on the line or at the desk.
Type: LIVE_SERVICE
Work item: one account order (contract, address change, or discontinuance) entered during a contact
Start: customer requests the change
End: order submitted and confirmation given to the customer
Checked by: the customer and the fulfilment or billing team that acts on the order

[15204a]
Occupation: Computer User Support Specialists
Task statement: Hire, supervise, and direct workers engaged in special project work, problem-solving, monitoring, and installation of data communication equipment and software.
Part: Hire workers for special project, monitoring, and installation work: screen candidates, interview, and decide on hires.
Type: DISCRETE
Work item: one vacancy filled (hiring decision made)
Start: vacancy approved and applications received
End: candidate selected and recommendation or offer sent to HR
Checked by: HR; hiring manager

[18565a]
Occupation: Customer Service Representatives
Task statement: Confer with customers by telephone or in person to provide information about products or services, take or enter orders, cancel accounts, or obtain details of complaints.
Part: Answer a customer's call or visit asking for information about products or services.
Type: LIVE_SERVICE
Work item: one information inquiry answered during a call or visit
Start: customer asks a question
End: customer confirms the question is answered, contact ends
Checked by: the customer and QA reviewer

[14653a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Provide feedback and recommendations to developers on software usability and functionality.
Part: Write usability and functionality feedback and recommendations on a build for developers.
Type: DISCRETE
Work item: one written feedback note on a build or feature
Start: build or feature evaluated
End: feedback and recommendations sent to developers
Checked by: developers / product owner

[1282b]
Occupation: Computer User Support Specialists
Task statement: Answer user inquiries regarding computer software or hardware operation to resolve problems.
Part: Answer a user's emailed or ticketed question about software or hardware operation.
Type: DISCRETE
Work item: one written user question answered (ticket or email)
Start: question received by email or in the ticket queue
End: answer sent and ticket closed
Checked by: the user who asked; help-desk lead reviewing ticket quality

[2581a]
Occupation: Customer Service Representatives
Task statement: Contact customers to respond to inquiries or to notify them of claim investigation results or any planned adjustments.
Part: Write and send a response to a customer's inquiry or a notification of claim investigation results or a planned adjustment.
Type: DISCRETE
Work item: one written response or notification sent to a customer
Start: inquiry or investigation result ready for response
End: letter or email sent and logged on the account
Checked by: the customer, and supervisor or QA reviewer

[14656a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Install and configure recreations of software production environments to allow testing of software performance.
Part: Install and configure a recreation of the production environment for performance testing.
Type: DISCRETE
Work item: one test environment built to mirror production
Start: environment request with production specification
End: environment configured, verified, and handed to testers
Checked by: QA lead / performance testers

[14645a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Plan test schedules or strategies in accordance with project scope or delivery dates.
Part: Prepare the test strategy and schedule for a project or release according to its scope and delivery dates.
Type: DISCRETE
Work item: one test strategy and schedule for a project or release
Start: project scope and delivery dates received
End: strategy and schedule approved by project stakeholders
Checked by: QA manager / project manager

[2583a]
Occupation: Customer Service Representatives
Task statement: Determine charges for services requested, collect deposits or payments, or arrange for billing.
Part: Determine the charges for a requested service and collect a deposit or payment, or set up billing, while the customer is on the line or at the desk.
Type: LIVE_SERVICE
Work item: one service charge determined and payment or billing arrangement completed during a contact
Start: customer requests a service
End: charge quoted, payment or deposit taken or billing arranged, receipt or confirmation given
Checked by: the customer, and cash-office or billing reconciliation

[14643b]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Monitor bug resolution efforts and track successes.
Part: Produce a periodic defect-resolution status report tracking open, fixed, and closed bugs.
Type: DISCRETE
Work item: one defect status report (weekly or per sprint)
Start: pull of current defect data from the tracker
End: report with counts, trends, and blockers sent to the project team
Checked by: QA manager / project manager

[14654a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Monitor program performance to ensure efficient and problem-free operations.
Part: Investigate a performance issue identified through program monitoring.
Type: DISCRETE
Work item: one monitored performance issue investigated
Start: monitoring reveals a performance anomaly or threshold breach
End: findings are recorded and the issue is closed or escalated
Checked by: developers and operations or test lead

[2581b]
Occupation: Customer Service Representatives
Task statement: Contact customers to respond to inquiries or to notify them of claim investigation results or any planned adjustments.
Part: Call a customer back to answer an inquiry or explain claim investigation results or a planned adjustment.
Type: LIVE_SERVICE
Work item: one outbound callback delivering an answer or result
Start: customer answers the call
End: result explained, customer's questions answered, call ended
Checked by: the customer, and QA reviewer of recorded calls

[2585a]
Occupation: Customer Service Representatives
Task statement: Obtain and examine all relevant information to assess validity of complaints and to determine possible causes, such as extreme weather conditions that could increase utility bills.
Part: Look up account and usage information during the call to assess whether a complaint is valid and explain the likely cause.
Type: LIVE_SERVICE
Work item: one complaint assessed during a call or visit
Start: customer describes the complaint
End: validity and likely cause explained to the customer and noted
Checked by: the customer and QA reviewer

[1284b]
Occupation: Computer User Support Specialists
Task statement: Install and perform minor repairs to hardware, software, or peripheral equipment, following design or installation specifications.
Part: Install software or make minor software repairs (reinstall, patch, reconfigure) on a user's computer following installation specifications.
Type: DISCRETE
Work item: one software installation or minor software repair completed on a machine
Start: install or repair request received
End: software installed or fixed and ticket closed
Checked by: the user; support lead

[2587a]
Occupation: Customer Service Representatives
Task statement: Review insurance policy terms to determine whether a particular loss is covered by insurance.
Part: Read the policy terms and tell a caller whether their loss appears to be covered while they are on the line.
Type: LIVE_SERVICE
Work item: one coverage question answered during a call
Start: customer describes the loss and asks whether it is covered
End: coverage answer given and noted on the account
Checked by: the customer and claims staff who later rely on the note

[1283b]
Occupation: Computer User Support Specialists
Task statement: Enter commands and observe system functioning to verify correct operations and detect errors.
Part: Run routine diagnostic commands on systems to detect errors before users report them.
Type: DISCRETE
Work item: one routine system check round (e.g. daily check of servers, printers, network links)
Start: scheduled check begins
End: results recorded, with any errors logged as tickets
Checked by: IT supervisor; systems administrators who act on the errors

[1290a]
Occupation: Computer User Support Specialists
Task statement: Develop training materials and procedures, or train users in the proper use of hardware or software.
Part: Write training materials or procedures for the proper use of hardware or software.
Type: DISCRETE
Work item: one training guide, how-to document, or procedure
Start: need for material identified (new system, recurring question)
End: material reviewed and published to users or the knowledge base
Checked by: IT supervisor; users who follow it

[14644b]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Create or maintain databases of known test defects.
Part: Update and clean up the known-defects database: merge duplicates, update statuses, and add workarounds.
Type: DISCRETE
Work item: one curation pass over the known-defects database
Start: scheduled review or release milestone
End: records updated, duplicates merged, and known-issues list current
Checked by: QA lead / support and development teams

[14638a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Design test plans, scenarios, scripts, or procedures.
Part: Design a test plan for a software change or release.
Type: DISCRETE
Work item: one test plan
Start: requirements and scope for the change or release are available
End: test plan is prepared and shared for review or use
Checked by: test lead and project team

[14638b]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Design test plans, scenarios, scripts, or procedures.
Part: Design test scenarios, scripts, or procedures for software functionality.
Type: DISCRETE
Work item: one feature-level set of test cases or scripts
Start: feature requirements or test objectives are available
End: cases or scripts are ready for review and execution
Checked by: test lead and testers

[14659a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Design or develop automated testing tools.
Part: Design and build an automated testing tool or framework component.
Type: DISCRETE
Work item: one automated testing tool or framework component
Start: tool need or specification agreed
End: tool reviewed, merged, and in use by the team
Checked by: QA lead / code reviewer

[14643a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Monitor bug resolution efforts and track successes.
Part: Follow up on a defect marked fixed: check its status, verify the fix, and close or reopen it.
Type: DISCRETE
Work item: one resolved defect verified and closed or reopened
Start: developer marks the defect fixed
End: ticket closed or reopened with a note
Checked by: developers / QA lead

[1286b]
Occupation: Computer User Support Specialists
Task statement: Set up equipment for employee use, performing or ensuring proper installation of cables, operating systems, or appropriate software.
Part: Install and configure the operating system, software, and accounts on a new employee's computer so it is ready for use.
Type: DISCRETE
Work item: one workstation configured and handed over to an employee
Start: setup request or new-starter ticket received with hardware available
End: machine imaged, software and accounts configured, handed to employee and ticket closed
Checked by: the employee; IT supervisor

[1283a]
Occupation: Computer User Support Specialists
Task statement: Enter commands and observe system functioning to verify correct operations and detect errors.
Part: Run test commands and observe a computer or system after an installation, repair, or change to verify it works correctly.
Type: DISCRETE
Work item: one post-install or post-repair verification of a machine or system
Start: installation, repair, or change completed
End: correct operation confirmed and noted on the ticket, or error found and fix reopened
Checked by: the user; support lead closing the ticket

