You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Code each ITEM independently, in the order given; do not go
back and adjust earlier answers to make them consistent with later ones.

Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/bpo_v1/s2/batch2.json
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
[14698a]
Occupation: Web Developers
Task statement: Back up files from Web sites to local directories for instant recovery in case of problems.
Part: Back up website files to local directories so the site can be restored quickly.
Type: DISCRETE
Work item: one website file backup completed
Start: scheduled time or before a major change
End: backup copied to local directory and verified
Checked by: site owner and whoever restores the site

[23266b]
Occupation: Billing and Posting Clerks
Task statement: Return checks to customers or retrieve checks returned to customers in error, adjusting accounts and answering inquiries about errors as necessary.
Part: Adjust an account to correct an error involving a returned check.
Type: DISCRETE
Work item: one account adjustment for a check-return error
Start: check-return error and required correction identified
End: account adjustment entered or submitted for approval
Checked by: accounting staff or a supervisor

[2498c]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Perform general office duties, such as filing, answering telephones, and handling routine correspondence.
Part: Answer and handle a routine incoming call.
Type: LIVE_SERVICE
Work item: one routine incoming call handled
Start: incoming call received
End: caller answered, directed, or transferred
Checked by: caller or receiving staff member

[23266d]
Occupation: Billing and Posting Clerks
Task statement: Return checks to customers or retrieve checks returned to customers in error, adjusting accounts and answering inquiries about errors as necessary.
Part: Answer a written customer inquiry about a check-return error.
Type: DISCRETE
Work item: one written check-error inquiry answered
Start: written inquiry about the error received
End: explanation or status sent to the customer
Checked by: customer and, if reviewed, a supervisor

[23330a]
Occupation: Insurance Claims and Policy Processing Clerks
Task statement: Collect initial premiums and issue receipts.
Part: Take an initial premium and issue a receipt while the customer is on the line or present.
Type: LIVE_SERVICE
Work item: one premium taken and receipted during contact
Start: customer agrees to pay
End: receipt confirmed
Checked by: customer; accounting

[1300a]
Occupation: Database Administrators
Task statement: Test programs or databases, correct errors, and make necessary modifications.
Part: Test programs or databases, fix errors and make needed changes.
Type: DISCRETE
Work item: one test round with fixes
Start: change ready for test
End: tests pass and fixes done
Checked by: developers and project lead

[14724a]
Occupation: Web Developers
Task statement: Create Web models or prototypes that include physical, interface, logical, or data models.
Part: Build a web model or prototype, such as a physical, interface, logical or data model.
Type: DISCRETE
Work item: one web model or prototype
Start: design need or requirements known
End: prototype delivered for review
Checked by: client, management and development team

[14700a]
Occupation: Web Developers
Task statement: Evaluate code to ensure that it is valid, is properly structured, meets industry standards, and is compatible with browsers, devices, or operating systems.
Part: Check code for validity, structure, standards and compatibility with browsers, devices and operating systems.
Type: DISCRETE
Work item: one code change evaluated
Start: code change ready for review
End: issues list or approval returned
Checked by: developer who wrote it and team lead

[15207c]
Occupation: Network and Computer Systems Administrators
Task statement: Research new technologies by attending seminars, reading trade articles, or taking classes, and implement or recommend the implementation of new technologies.
Part: Implement an approved new technology.
Type: DISCRETE
Work item: one new technology deployment or implementation change
Start: implementation is approved and assigned
End: technology is configured, tested, and handed over
Checked by: system owner and operations team

[21648a]
Occupation: Database Administrators
Task statement: Identify, evaluate and recommend hardware or software technologies to achieve desired database performance.
Part: Identify, evaluate and recommend hardware or software for database performance.
Type: DISCRETE
Work item: one technology recommendation
Start: performance need
End: recommendation delivered
Checked by: management

[22889a]
Occupation: Medical Records Specialists
Task statement: Retrieve patient medical records for physicians, technicians, or other medical personnel.
Part: Retrieve an electronic patient record for authorized medical personnel.
Type: DISCRETE
Work item: one electronic patient record retrieved for a requester
Start: authorized retrieval request is received
End: record is made available to the requester
Checked by: the requesting physician, technician, or other authorized staff member

[11402b]
Occupation: Data Entry Keyers
Task statement: Compile, sort, and verify the accuracy of data before it is entered.
Part: Compile and verify data for entry, including organizing electronic source data.
Type: DISCRETE
Work item: One batch of source data compiled and checked before entry
Start: Source data received for preparation
End: Data organized and accuracy checked for entry
Checked by: Data entry keyer or supervisor

[23321a]
Occupation: Insurance Claims and Policy Processing Clerks
Task statement: Provide customer service, such as limited instructions on proceeding with claims or referrals to auto repair facilities or local contractors.
Part: Advise a policyholder how to proceed with a claim or refer them to a repair facility or contractor during a call or visit.
Type: LIVE_SERVICE
Work item: one customer inquiry answered during a call
Start: customer states the need
End: customer has instructions or referral
Checked by: the customer; supervisor via call monitoring

[1319a]
Occupation: Network and Computer Systems Administrators
Task statement: Plan, coordinate, and implement network security measures to protect data, software, and hardware.
Part: Plan and put in place security measures to protect data, software and hardware.
Type: DISCRETE
Work item: one security measure planned and implemented
Start: security risk or requirement identified
End: measure working and documented
Checked by: IT manager and auditor

[23329a]
Occupation: Insurance Claims and Policy Processing Clerks
Task statement: Process, prepare, and submit business or government forms, such as submitting applications for coverage to insurance carriers.
Part: Prepare and submit a business or government form, such as an application to a carrier.
Type: DISCRETE
Work item: one form or application submitted
Start: information gathered
End: form submitted
Checked by: carrier or agency

[1306a]
Occupation: Database Administrators
Task statement: Develop data models describing data elements and how they are used, following procedures and using pen, template, or computer software.
Part: Build data models describing data elements and their use.
Type: DISCRETE
Work item: one data model
Start: data needs gathered
End: model reviewed and issued
Checked by: developers and data owner

[1323a]
Occupation: Network and Computer Systems Administrators
Task statement: Recommend changes to improve systems and network configurations, and determine hardware or software requirements related to such changes.
Part: Recommend changes to improve systems and network configurations and the hardware or software they need.
Type: DISCRETE
Work item: one improvement recommendation
Start: weakness or opportunity noticed
End: recommendation delivered
Checked by: IT manager

[3477a]
Occupation: Computer Systems Analysts
Task statement: Develop, document, and revise system design procedures, test procedures, and quality standards.
Part: Write or revise a design procedure, test procedure or quality standard.
Type: DISCRETE
Work item: one procedure or standard written or revised
Start: need for a procedure identified
End: document approved and issued
Checked by: project lead; QA

[14717a]
Occupation: Web Developers
Task statement: Establish appropriate server directory trees.
Part: Set up the server directory tree for a website.
Type: DISCRETE
Work item: one server directory structure established
Start: new site or deployment planned
End: directory tree created and documented
Checked by: development team and hosting staff

[15208c]
Occupation: Network and Computer Systems Administrators
Task statement: Implement and provide technical support for voice services and equipment, such as private branch exchange, voice mail system, and telecom system.
Part: Provide voice service technical support while the user is present or connected.
Type: LIVE_SERVICE
Work item: one live voice service support contact
Start: user reports a voice service issue during a contact
End: fix or next step is communicated to the user
Checked by: affected user

[23323a]
Occupation: Insurance Claims and Policy Processing Clerks
Task statement: Review and verify data, such as age, name, address, and principal sum and value of property, on insurance applications and policies.
Part: Review an application or policy and verify the data on it.
Type: DISCRETE
Work item: one application or policy verified
Start: document received
End: verified or corrected and returned
Checked by: underwriter or supervisor

[11403a]
Occupation: Data Entry Keyers
Task statement: Compare data with source documents, or re-enter data in verification format to detect errors.
Part: Compare entered data with sources or re-enter to find errors.
Type: DISCRETE
Work item: one batch verified
Start: entry complete
End: errors flagged
Checked by: supervisor

[1324b]
Occupation: Network and Computer Systems Administrators
Task statement: Confer with network users about solutions to existing system problems.
Part: Follow up with a user about a system problem by email or ticket.
Type: DISCRETE
Work item: one written follow-up on a system problem
Start: user message or ticket received
End: reply sent and ticket updated
Checked by: the user

[2491a]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Calculate, prepare, and issue bills, invoices, account statements, and other financial statements according to established procedures.
Part: Calculate, prepare, and issue a bill or invoice.
Type: DISCRETE
Work item: one bill or invoice issued
Start: billable transaction or billing information received
End: bill or invoice calculated and issued
Checked by: customer or payer and billing supervisor

[1298a]
Occupation: Database Administrators
Task statement: Develop standards and guidelines for the use and acquisition of software and to protect vulnerable information.
Part: Write standards and guidelines for acquiring and using software and for protecting vulnerable information.
Type: DISCRETE
Work item: one standard or guideline document
Start: need for a standard identified
End: standard approved and issued
Checked by: management and security officer

[22887b]
Occupation: Medical Records Specialists
Task statement: Release information to persons or agencies according to regulations.
Part: Release information in response to written requests.
Type: DISCRETE
Work item: one release request fulfilled
Start: request received
End: records sent and logged
Checked by: requester, privacy officer

[1320a]
Occupation: Network and Computer Systems Administrators
Task statement: Operate master consoles to monitor the performance of computer systems and networks and to coordinate computer network access and use.
Part: Handle an alert or issue seen on the master console.
Type: DISCRETE
Work item: one console alert handled
Start: alert seen
End: fixed or escalated and logged
Checked by: IT manager and affected users

[2506a]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Transfer details from separate journals to general ledgers or data processing sheets.
Part: Transfer entries from separate journals to the general ledger or processing sheets.
Type: DISCRETE
Work item: one batch of journal entries posted to the ledger
Start: journal ready
End: ledger updated
Checked by: supervisor; accountant

[3465b]
Occupation: Computer Systems Analysts
Task statement: Test, maintain, and monitor computer programs and systems, including coordinating the installation of computer programs and systems.
Part: Perform a maintenance change on a computer program or system.
Type: DISCRETE
Work item: one program or system maintenance change
Start: maintenance need or scheduled change identified
End: change applied and its completion recorded
Checked by: system owner and operations team

[14730a]
Occupation: Web Developers
Task statement: Develop system interaction or sequence diagrams.
Part: Draw system interaction or sequence diagrams.
Type: DISCRETE
Work item: one set of interaction or sequence diagrams
Start: design or feature to be described
End: diagrams reviewed and shared
Checked by: development team

[15207b]
Occupation: Network and Computer Systems Administrators
Task statement: Research new technologies by attending seminars, reading trade articles, or taking classes, and implement or recommend the implementation of new technologies.
Part: Recommend implementation of a new technology.
Type: DISCRETE
Work item: one new technology implementation recommendation
Start: technology and potential organizational use identified
End: recommendation is communicated for review
Checked by: IT manager or technology decision-maker

[23321b]
Occupation: Insurance Claims and Policy Processing Clerks
Task statement: Provide customer service, such as limited instructions on proceeding with claims or referrals to auto repair facilities or local contractors.
Part: Send written instructions or referrals to a policyholder after the contact.
Type: DISCRETE
Work item: one written instruction or referral
Start: request noted
End: message sent
Checked by: policyholder

[23242a]
Occupation: Billing and Posting Clerks
Task statement: Operate typing, adding, calculating, or billing machines.
Part: Use office or billing equipment to process a billing calculation or document.
Type: DISCRETE
Work item: one billing calculation or document processed using office equipment
Start: billing information or document supplied for processing
End: calculation or document produced for the next billing step
Checked by: billing staff or a supervisor

[23320a]
Occupation: Insurance Claims and Policy Processing Clerks
Task statement: Organize or work with detailed office or warehouse records, using computers to enter, access, search or retrieve data.
Part: Enter, file and organize office records on the computer.
Type: DISCRETE
Work item: one batch of records entered or filed
Start: records or documents received
End: records entered and filed
Checked by: supervisor or colleagues using the records

[2486a]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Check figures, postings, and documents for correct entry, mathematical accuracy, and proper codes.
Part: Check a batch of figures, postings and documents for correct entry, arithmetic and codes.
Type: DISCRETE
Work item: one batch of entries checked and corrected
Start: batch received for checking
End: batch passed or corrections made
Checked by: supervisor; auditor

[1324a]
Occupation: Network and Computer Systems Administrators
Task statement: Confer with network users about solutions to existing system problems.
Part: Talk to a user, while they are on the line or at the desk, about a current system problem.
Type: LIVE_SERVICE
Work item: one live conversation about a system problem
Start: user calls or arrives with a problem
End: problem fixed or referred and user told
Checked by: the user and the IT manager

[14722a]
Occupation: Web Developers
Task statement: Provide clear, detailed descriptions of Web site specifications, such as product features, activities, software, communication protocols, programming languages, and operating systems software and hardware.
Part: Write clear, detailed descriptions of website specifications such as features, software, protocols and systems.
Type: DISCRETE
Work item: one website specification document
Start: requirements known
End: specification issued
Checked by: development team and client

[3484a]
Occupation: Computer Systems Analysts
Task statement: Specify inputs accessed by the system and plan the distribution and use of the results.
Part: Specify the inputs a system will use and plan how its results are distributed and used.
Type: DISCRETE
Work item: one input/output specification
Start: system design underway
End: specification approved
Checked by: developers; users

[1333a]
Occupation: Network and Computer Systems Administrators
Task statement: Coordinate with vendors and with company personnel to facilitate purchases.
Part: Coordinate with vendors and company staff so that a purchase is made.
Type: DISCRETE
Work item: one purchase coordinated
Start: need approved
End: order placed with vendor
Checked by: purchasing or IT manager

[3465c]
Occupation: Computer Systems Analysts
Task statement: Test, maintain, and monitor computer programs and systems, including coordinating the installation of computer programs and systems.
Part: Investigate a monitoring alert or exception for a computer program or system.
Type: DISCRETE
Work item: one monitoring alert or exception investigated
Start: alert or exception appears in monitoring results
End: findings and any necessary escalation are recorded
Checked by: operations team

[3482a]
Occupation: Computer Systems Analysts
Task statement: Use the computer in the analysis and solution of business problems, such as development of integrated production and inventory control and cost analysis systems.
Part: Use the computer to analyze and solve a business problem, e.g. building a production, inventory or cost system.
Type: DISCRETE
Work item: one business problem analyzed and solved
Start: problem posed
End: solution delivered
Checked by: the requesting business unit

[23255a]
Occupation: Billing and Posting Clerks
Task statement: Consult sources, such as rate books, manuals, or insurance company representatives, to determine specific charges or information such as rules, regulations, or government tax and tariff information.
Part: Consult rate books, manuals or insurers to find the correct charge or rule.
Type: DISCRETE
Work item: one charge or rule determined
Start: question arises
End: answer found
Checked by: supervisor

[21676a]
Occupation: Software Developers
Task statement: Store, retrieve, and manipulate data for analysis of system capabilities and requirements.
Part: Pull and work with data to analyze a system's capabilities and requirements.
Type: DISCRETE
Work item: one data analysis of system capabilities or requirements
Start: question about capacity or requirements raised
End: findings delivered
Checked by: project manager and systems analysts

[23316a]
Occupation: Insurance Claims and Policy Processing Clerks
Task statement: Transmit claims for payment or further investigation.
Part: Transmit a completed claim for payment or for further investigation.
Type: DISCRETE
Work item: one claim transmitted for payment or investigation
Start: claim reviewed and ready to route
End: claim received by payment or investigation unit
Checked by: payment unit, investigator, or supervisor

[23240a]
Occupation: Billing and Posting Clerks
Task statement: Prepare itemized statements, bills, or invoices and record amounts due for items purchased or services rendered.
Part: Prepare itemized statements, bills or invoices and record amounts due.
Type: DISCRETE
Work item: one batch of invoices prepared and recorded
Start: billing data ready
End: invoices ready to send
Checked by: customers; supervisor

[3464a]
Occupation: Computer Systems Analysts
Task statement: Provide staff and users with assistance solving computer-related problems, such as malfunctions and program problems.
Part: Help a user fix a computer problem while the user is on the phone, chat or at the desk.
Type: LIVE_SERVICE
Work item: one user problem fixed during a live contact
Start: user reports the problem
End: user confirms it works
Checked by: the user

