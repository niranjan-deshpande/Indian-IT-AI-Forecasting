You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Code each ITEM independently, in the order given; do not go
back and adjust earlier answers to make them consistent with later ones.

Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/bpo_v1/s2/batch1.json
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
[21673a]
Occupation: Software Developers
Task statement: Prepare reports or correspondence concerning project specifications, activities, or status.
Part: Write a report on project specifications, activities or status.
Type: DISCRETE
Work item: one project report
Start: reporting date or request
End: report sent
Checked by: project manager and customer

[22893a]
Occupation: Medical Records Specialists
Task statement: Transcribe medical reports.
Part: Transcribe a dictated medical report.
Type: DISCRETE
Work item: one report transcribed
Start: dictation received
End: report returned for signature
Checked by: authoring physician

[1317a]
Occupation: Network and Computer Systems Administrators
Task statement: Perform data backups and disaster recovery operations.
Part: Run and verify a scheduled data backup.
Type: DISCRETE
Work item: one backup job run and verified
Start: scheduled backup time
End: job completed and checked in the log
Checked by: IT manager and users who may need restores

[1327b]
Occupation: Network and Computer Systems Administrators
Task statement: Load computer tapes and disks, and install software and printer paper or forms.
Part: Install software on a computer or server.
Type: DISCRETE
Work item: one software installation
Start: installation request or approved deployment is received
End: software is installed and basic operation verified
Checked by: requesting user or systems operations team

[2514b]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Prepare purchase orders and expense reports.
Part: Prepare an expense report.
Type: DISCRETE
Work item: one expense report
Start: expenses received
End: report submitted
Checked by: approver

[23265d]
Occupation: Billing and Posting Clerks
Task statement: Perform general administrative tasks, such as answering telephones, scheduling appointments, and ordering supplies or equipment.
Part: Order supplies or equipment for the office.
Type: DISCRETE
Work item: one supply or equipment order submitted
Start: supply or equipment need identified
End: order or purchasing request submitted
Checked by: purchasing staff, supplier, or supervisor

[22877a]
Occupation: Medical Records Specialists
Task statement: Assign the patient to diagnosis-related groups (DRGs), using appropriate computer software.
Part: Assign a patient case to a DRG using grouper software.
Type: DISCRETE
Work item: one inpatient encounter assigned a DRG
Start: codes finalized
End: DRG recorded
Checked by: coding auditor, billing

[2496a]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Reconcile or note and report discrepancies found in records.
Part: Reconcile records or note and report a discrepancy.
Type: DISCRETE
Work item: one discrepancy reconciled or reported
Start: discrepancy found
End: resolved or reported
Checked by: supervisor

[23251a]
Occupation: Billing and Posting Clerks
Task statement: Compare previously prepared bank statements with canceled checks and reconcile discrepancies.
Part: Compare bank statements with canceled checks and reconcile discrepancies.
Type: DISCRETE
Work item: one bank statement reconciliation
Start: statement received
End: reconciled
Checked by: supervisor

[1330a]
Occupation: Network and Computer Systems Administrators
Task statement: Maintain logs related to network functions, as well as maintenance and repair records.
Part: Keep the log of network functions.
Type: DISCRETE
Work item: one network function log update
Start: shift or period begins
End: log updated
Checked by: IT manager and auditor

[23244a]
Occupation: Billing and Posting Clerks
Task statement: Contact customers to obtain or relay account information.
Part: Call a customer to get or give account information.
Type: LIVE_SERVICE
Work item: one customer call about an account
Start: call connects
End: information exchanged
Checked by: customer; supervisor

[23325a]
Occupation: Insurance Claims and Policy Processing Clerks
Task statement: Examine letters from policyholders or agents, original insurance applications, and other company documents to determine if changes are needed and effects of changes.
Part: Review letters, applications and other documents to decide if a policy change is needed and its effect.
Type: DISCRETE
Work item: one change request assessed
Start: letter or document received
End: change determination noted
Checked by: supervisor or the processor who makes the change

[23239a]
Occupation: Billing and Posting Clerks
Task statement: Verify signatures and required information on checks.
Part: Verify signatures and required information on checks.
Type: DISCRETE
Work item: one batch of checks verified
Start: checks received
End: checks passed or returned
Checked by: supervisor

[23262b]
Occupation: Billing and Posting Clerks
Task statement: Answer inquiries regarding rates, routing, or procedures.
Part: Answer a written inquiry about rates, routing, or procedures.
Type: DISCRETE
Work item: one written rates, routing, or procedures inquiry answered
Start: written inquiry received
End: answer sent to the requester
Checked by: requester and, if reviewed, a supervisor

[14719b]
Occupation: Web Developers
Task statement: Recommend and implement performance improvements.
Part: Implement an approved website performance improvement.
Type: DISCRETE
Work item: one performance improvement implemented
Start: improvement selected for implementation
End: change completed and submitted for review or deployment
Checked by: development team and site owner

[2487b]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Operate computers programmed with accounting software to record, store, and analyze information.
Part: Run analyses or queries in the accounting software and report results.
Type: DISCRETE
Work item: one analysis or report query run
Start: request made
End: results delivered
Checked by: requesting manager

[14713a]
Occupation: Web Developers
Task statement: Respond to user email inquiries, or set up automated systems to send responses.
Part: Answer a user's email inquiry.
Type: DISCRETE
Work item: one user email inquiry answered
Start: inquiry email received
End: reply sent
Checked by: the user who asked

[14714a]
Occupation: Web Developers
Task statement: Develop or implement procedures for ongoing Web site revision.
Part: Develop or put in place procedures for the ongoing revision of the website.
Type: DISCRETE
Work item: one website revision procedure
Start: need for a revision process identified
End: procedure documented and in use
Checked by: site owner and content staff

[1311b]
Occupation: Database Administrators
Task statement: Select and enter codes to monitor database performance and to create production databases.
Part: Enter commands to create a production database.
Type: DISCRETE
Work item: one production database created
Start: creation approved
End: database ready for use
Checked by: application owner

[1303c]
Occupation: Database Administrators
Task statement: Train users and answer questions.
Part: Answer a user's database question received in writing.
Type: DISCRETE
Work item: one written user question answered
Start: written question received
End: answer sent to the user
Checked by: the user

[1322a]
Occupation: Network and Computer Systems Administrators
Task statement: Design, configure, and test computer hardware, networking software and operating system software.
Part: Design, configure, and test a network or operating system software configuration.
Type: DISCRETE
Work item: one tested network or operating system configuration
Start: configuration requirement or change request received
End: configuration is tested and handed over or deployed
Checked by: network or systems operations team

[1313a]
Occupation: Database Administrators
Task statement: Write and code logical and physical database descriptions and specify identifiers of database to management system, or direct others in coding descriptions.
Part: Code logical and physical database descriptions and specify their identifiers to the DBMS.
Type: DISCRETE
Work item: one coded set of database definitions
Start: database design or definition change received
End: descriptions and identifiers coded and submitted or applied
Checked by: database lead and application developers

[1299a]
Occupation: Database Administrators
Task statement: Modify existing databases and database management systems or direct programmers and analysts to make changes.
Part: Modify an existing database or database management system.
Type: DISCRETE
Work item: one database or DBMS change implemented
Start: change requirement or request received
End: change implemented and handed over
Checked by: requesting team and database lead

[15206b]
Occupation: Network and Computer Systems Administrators
Task statement: Configure, monitor, and maintain email applications or virus protection software.
Part: Investigate an alert from email or virus protection.
Type: DISCRETE
Work item: one email or virus alert investigated
Start: alert raised
End: dealt with and logged
Checked by: IT manager and affected users

[23256a]
Occupation: Billing and Posting Clerks
Task statement: Track accumulated hours and dollar amounts charged to each client job to calculate client fees for professional services, such as legal or accounting services.
Part: Track hours and dollars charged to a client job and calculate the client fee.
Type: DISCRETE
Work item: one client job's fee calculated
Start: billing period closes
End: fee ready to bill
Checked by: client; supervisor

[3470a]
Occupation: Computer Systems Analysts
Task statement: Expand or modify system to serve new purposes or improve work flow.
Part: Change or extend a system to serve a new purpose or improve workflow.
Type: DISCRETE
Work item: one system enhancement delivered
Start: change request approved
End: change released and accepted
Checked by: system owner; users

[23330b]
Occupation: Insurance Claims and Policy Processing Clerks
Task statement: Collect initial premiums and issue receipts.
Part: Record initial premiums received by mail and send receipts.
Type: DISCRETE
Work item: one batch of premiums receipted
Start: payments received
End: receipts sent
Checked by: accounting

[22882a]
Occupation: Medical Records Specialists
Task statement: Maintain or operate a variety of health record indexes or storage and retrieval systems to collect, classify, store, or analyze information.
Part: Index and file records in storage and retrieval systems.
Type: DISCRETE
Work item: one batch of records indexed
Start: records received
End: indexed and stored
Checked by: HIM supervisor, record users

[1320b]
Occupation: Network and Computer Systems Administrators
Task statement: Operate master consoles to monitor the performance of computer systems and networks and to coordinate computer network access and use.
Part: Coordinate access to the network or system for a user or job.
Type: DISCRETE
Work item: one access request coordinated
Start: request received
End: access given or refused and noted
Checked by: the requesting user

[14702a]
Occupation: Web Developers
Task statement: Analyze user needs to determine technical requirements.
Part: Analyze what users need and turn it into technical requirements.
Type: DISCRETE
Work item: one set of technical requirements
Start: user request or need raised
End: requirements documented and confirmed
Checked by: client or manager and development team

[15208a]
Occupation: Network and Computer Systems Administrators
Task statement: Implement and provide technical support for voice services and equipment, such as private branch exchange, voice mail system, and telecom system.
Part: Configure and implement a voice service or system change.
Type: DISCRETE
Work item: one voice service implementation or configuration change
Start: approved voice service requirement or change request received
End: service change is configured, tested, and handed over
Checked by: voice operations team or service owner

[14707a]
Occupation: Web Developers
Task statement: Write supporting code for Web applications or Web sites.
Part: Write supporting code for a web application or website.
Type: DISCRETE
Work item: one supporting code change
Start: task assigned
End: code reviewed and merged
Checked by: code reviewer and development team

[23320b]
Occupation: Insurance Claims and Policy Processing Clerks
Task statement: Organize or work with detailed office or warehouse records, using computers to enter, access, search or retrieve data.
Part: Search for and retrieve a record when someone asks.
Type: DISCRETE
Work item: one record retrieval request
Start: request received
End: record supplied to the requester
Checked by: the requester

[1311a]
Occupation: Database Administrators
Task statement: Select and enter codes to monitor database performance and to create production databases.
Part: Enter commands to set up monitoring of database performance.
Type: DISCRETE
Work item: one performance monitoring setup
Start: database needs monitoring
End: monitoring working
Checked by: DBA team

[23317a]
Occupation: Insurance Claims and Policy Processing Clerks
Task statement: Contact insured or other involved persons to obtain missing information.
Part: Phone the insured or other involved person and obtain missing claim information while they are on the line.
Type: LIVE_SERVICE
Work item: one outbound call to obtain missing claim information
Start: person reached and asked for the missing details
End: information obtained and noted on file
Checked by: the insured, and the adjuster waiting for the data

[14723a]
Occupation: Web Developers
Task statement: Monitor security system performance logs to identify problems and notify security specialists when problems occur.
Part: Review security performance logs to find problems.
Type: DISCRETE
Work item: one security log review
Start: review period begins or alert seen
End: log reviewed and findings noted
Checked by: security specialists and site owner

[11409a]
Occupation: Data Entry Keyers
Task statement: Resolve garbled or indecipherable messages, using cryptographic procedures and equipment.
Part: Resolve a garbled or indecipherable message using cryptographic procedures.
Type: DISCRETE
Work item: one message resolved
Start: message flagged
End: message readable
Checked by: sender; supervisor

[1330b]
Occupation: Network and Computer Systems Administrators
Task statement: Maintain logs related to network functions, as well as maintenance and repair records.
Part: Record maintenance and repair work after it is done.
Type: DISCRETE
Work item: one maintenance or repair record
Start: work finished
End: record filed
Checked by: IT manager

[23260a]
Occupation: Billing and Posting Clerks
Task statement: Review compiled data on operating costs and revenues to set rates.
Part: Review cost and revenue data to set rates.
Type: DISCRETE
Work item: one rate decision
Start: review period
End: rates set or recommended
Checked by: management

[3476a]
Occupation: Computer Systems Analysts
Task statement: Define the goals of the system and devise flow charts and diagrams describing logical operational steps of programs.
Part: Define the goals of a computer system.
Type: DISCRETE
Work item: one system goals statement
Start: system purpose and stakeholder needs available
End: goals documented and submitted for review
Checked by: system owner and management

[2493a]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Code documents according to company procedures.
Part: Code a batch of documents with account codes per company procedure.
Type: DISCRETE
Work item: one batch of documents coded
Start: documents received
End: coded documents passed to posting
Checked by: supervisor; posting clerk

[3479a]
Occupation: Computer Systems Analysts
Task statement: Recommend new equipment or software packages.
Part: Recommend new equipment or software packages.
Type: DISCRETE
Work item: one recommendation memo
Start: need or option identified
End: recommendation delivered
Checked by: management

[1332b]
Occupation: Network and Computer Systems Administrators
Task statement: Maintain an inventory of parts for emergency repairs.
Part: Update the parts inventory and flag reorders.
Type: DISCRETE
Work item: one inventory update
Start: parts used or counted
End: inventory records updated
Checked by: IT manager

[23266c]
Occupation: Billing and Posting Clerks
Task statement: Return checks to customers or retrieve checks returned to customers in error, adjusting accounts and answering inquiries about errors as necessary.
Part: Answer a customer's live inquiry about a check-return error.
Type: LIVE_SERVICE
Work item: one live check-error inquiry answered
Start: customer asks about the check error
End: explanation or status relayed to the customer
Checked by: customer and, if reviewed, a supervisor

[22891b]
Occupation: Medical Records Specialists
Task statement: Scan patients' health records into electronic formats.
Part: Index and quality-check scanned images.
Type: DISCRETE
Work item: one batch of scans indexed and checked
Start: scan complete
End: images in the chart
Checked by: HIM supervisor

[23328a]
Occupation: Insurance Claims and Policy Processing Clerks
Task statement: Pay small claims.
Part: Pay a small claim.
Type: DISCRETE
Work item: one small claim paid
Start: claim approved as small
End: payment issued and recorded
Checked by: supervisor, accounting, auditor

