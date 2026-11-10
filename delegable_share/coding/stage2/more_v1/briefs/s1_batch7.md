You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Code each ITEM independently, in the order given; do not go
back and adjust earlier answers to make them consistent with later ones.

Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/more_v1/s1/batch7.json
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
[23110a]
Occupation: Fast Food and Counter Workers
Task statement: Serve customers in eating places that specialize in fast service and inexpensive carry-out food.
Part: Serve a customer at the counter from order to handover.
Type: LIVE_SERVICE
Work item: one customer served at the counter
Start: customer arrives at the counter
End: customer leaves with the order
Checked by: the customer, and the shift manager

[21477a]
Occupation: Project Management Specialists
Task statement: Recruit or hire project personnel.
Part: Recruit and hire a project team member.
Type: DISCRETE
Work item: one project hire
Start: position approved
End: person hired
Checked by: HR; sponsor

[23896a]
Occupation: Stockers and Order Fillers
Task statement: Compute prices of items or groups of items.
Part: Compute prices for items or groups of items.
Type: DISCRETE
Work item: one set of computed prices for an item or group of items
Start: items needing a price identified
End: prices written down or entered
Checked by: supervisor or manager

[965a]
Occupation: Marketing Managers
Task statement: Conduct economic or commercial surveys to identify potential markets for products or services.
Part: Conduct economic or commercial surveys to identify potential markets for products or services.
Type: DISCRETE
Work item: one market opportunity assessment
Start: market question set
End: assessment delivered with the potential markets identified
Checked by: senior management

[23114a]
Occupation: Fast Food and Counter Workers
Task statement: Notify kitchen personnel of shortages or special orders.
Part: Tell kitchen staff about a shortage or a special order.
Type: DISCRETE
Work item: one shortage or special-order notice to the kitchen
Start: worker spots the shortage or receives the special request
End: kitchen staff acknowledge it
Checked by: kitchen staff

[20703a]
Occupation: General and Operations Managers
Task statement: Direct or coordinate financial or budget activities to fund operations, maximize investments, or increase efficiency.
Part: Prepare or approve an operating budget and funding plan.
Type: DISCRETE
Work item: one budget or funding plan
Start: budget cycle begins
End: budget approved
Checked by: board or owner; finance

[20701a]
Occupation: General and Operations Managers
Task statement: Prepare staff work schedules and assign specific duties.
Part: Prepare staff work schedules and assign duties.
Type: DISCRETE
Work item: one staff work schedule with assignments
Start: staffing needs and availability known
End: schedule published to staff
Checked by: staff and supervisors

[2524a]
Occupation: Payroll and Timekeeping Clerks
Task statement: Complete time sheets showing employees' arrival and departure times.
Part: Complete time sheets showing employees' arrival and departure times.
Type: DISCRETE
Work item: one pay period's time sheets completed
Start: clock or attendance records available
End: time sheets completed and passed to payroll
Checked by: supervisors, payroll

[2520a]
Occupation: Payroll and Timekeeping Clerks
Task statement: Record employee information, such as exemptions, transfers, and resignations, to maintain and update payroll records.
Part: Record an employee status change (exemptions, transfer, resignation) in the payroll records.
Type: DISCRETE
Work item: one employee status change recorded
Start: change notice or form received
End: payroll record updated
Checked by: payroll supervisor, HR, auditor

[973a]
Occupation: Computer and Information Systems Managers
Task statement: Evaluate the organization's technology use and needs and recommend improvements, such as hardware and software upgrades.
Part: Evaluate the organization's technology use and needs and recommend improvements such as hardware and software upgrades.
Type: DISCRETE
Work item: one technology evaluation with upgrade recommendation
Start: area or system chosen for evaluation
End: recommendation delivered to management
Checked by: CIO, executive management

[662a]
Occupation: First-Line Supervisors of Retail Sales Workers
Task statement: Keep records of purchases, sales, and requisitions.
Part: Keep records of purchases, sales and requisitions.
Type: DISCRETE
Work item: one day's purchase, sales and requisition records entered and reconciled
Start: day's transactions and requisition slips available
End: records entered and filed or submitted
Checked by: store manager; accounting

[3423a]
Occupation: Loan Officers
Task statement: Set credit policies, credit lines, procedures and standards in conjunction with senior managers.
Part: Set credit policies, credit lines, procedures and standards with senior managers.
Type: DISCRETE
Work item: one credit policy, procedure or standard agreed and issued
Start: need for a new or changed policy raised
End: policy approved and issued to staff
Checked by: senior management and compliance

[784a]
Occupation: Medical Secretaries and Administrative Assistants
Task statement: Perform various clerical or administrative functions, such as ordering and maintaining an inventory of supplies.
Part: Order office or clinical supplies.
Type: DISCRETE
Work item: one supply order placed
Start: supply need identified
End: order submitted to the supplier or purchasing department
Checked by: purchasing staff, supervisor, or supplier

[3412a]
Occupation: Loan Officers
Task statement: Review and update credit and loan files.
Part: Review and update a credit or loan file.
Type: DISCRETE
Work item: one credit or loan file reviewed and updated
Start: file pulled for review
End: file updated and refiled
Checked by: supervisor or auditor

[7382a]
Occupation: Operations Research Analysts
Task statement: Define data requirements, and gather and validate information, applying judgment and statistical tests.
Part: Specify, gather and validate the data a project needs.
Type: DISCRETE
Work item: one validated data set with its data requirements
Start: data needs defined
End: validated data handed to modeling
Checked by: project lead and downstream modelers

[9723c]
Occupation: First-Line Supervisors of Office and Administrative Support Workers
Task statement: Design, implement, or evaluate staff training and development programs, customer service initiatives, or performance measurement criteria.
Part: Define or revise performance measurement criteria.
Type: DISCRETE
Work item: one set of performance criteria defined or revised
Start: need for measures identified
End: criteria approved and issued
Checked by: manager, HR

[19628a]
Occupation: Mechanical Engineers
Task statement: Design integrated mechanical or alternative systems, such as mechanical cooling systems with natural ventilation systems, to improve energy efficiency.
Part: Design an integrated mechanical system (e.g. cooling combined with natural ventilation) to improve energy efficiency.
Type: DISCRETE
Work item: one integrated system design package
Start: building energy goals set
End: design issued
Checked by: client, reviewing engineer, code official

[733b]
Occupation: Insurance Sales Agents
Task statement: Inspect property, examining its general condition, type of construction, age, and other characteristics, to decide if it is a good insurance risk.
Part: Decide whether the property is a good risk and record the assessment.
Type: DISCRETE
Work item: one property risk assessment
Start: site inspection finished
End: assessment recorded and sent to underwriter
Checked by: underwriter

[19559a]
Occupation: Training and Development Specialists
Task statement: Evaluate modes of training delivery, such as in-person or virtual, to optimize training effectiveness, training costs, or environmental impacts.
Part: Evaluate in-person versus virtual delivery for effectiveness, cost and environmental impact and recommend one.
Type: DISCRETE
Work item: one delivery-mode evaluation with recommendation
Start: question of delivery mode raised for a program
End: recommendation delivered
Checked by: training manager

[720b]
Occupation: Insurance Sales Agents
Task statement: Customize insurance programs to suit individual customers, often covering a variety of risks.
Part: Develop a customized insurance program from a customer's documented risks and needs.
Type: DISCRETE
Work item: one customized insurance coverage proposal
Start: customer's risk and coverage information is available
End: proposed coverage combination is prepared for presentation
Checked by: customer and insurer

[102a]
Occupation: Training and Development Specialists
Task statement: Develop alternative training methods if expected improvements are not seen.
Part: Develop an alternative training method when a program has not produced the expected improvement.
Type: DISCRETE
Work item: one revised training approach for an underperforming program
Start: evaluation shows expected improvement not achieved
End: revised approach proposed and approved
Checked by: training manager or program sponsor

[20737a]
Occupation: Mechanical Engineers
Task statement: Assist drafters in developing the structural design of products, using drafting tools or computer-assisted drafting equipment or software.
Part: Assist drafters with the structural design of products by providing sketches, mark-ups and CAD input.
Type: DISCRETE
Work item: one drawing input package for a drafter
Start: design concept ready for drafting
End: drawing completed and approved
Checked by: drafter, design lead

[1823b]
Occupation: Pharmacists
Task statement: Work in hospitals or clinics or for Health Management Organizations (HMOs), dispensing prescriptions, serving as a medical team consultant, or specializing in specific drug therapy areas, such as oncology or nuclear pharmacotherapy.
Part: Answer a team member's question or advise on a specialty drug therapy.
Type: DISCRETE
Work item: one consult on drug therapy answered
Start: consult request received
End: advice given and noted
Checked by: requesting clinician

[3398b]
Occupation: Budget Analysts
Task statement: Provide advice and technical assistance with cost analysis, fiscal allocation, and budget preparation.
Part: Respond to a written request for budget or cost-analysis advice or technical assistance.
Type: DISCRETE
Work item: one written budget assistance request answered
Start: written request for assistance is received
End: guidance or technical response is sent
Checked by: the requesting manager or staff member

[20740b]
Occupation: Mechanical Engineers
Task statement: Solicit new business.
Part: Prepare a written capability pitch or proposal for a prospect.
Type: DISCRETE
Work item: one pitch or proposal to a prospect
Start: prospect identified
End: proposal sent
Checked by: sales manager, prospective customer

[20734b]
Occupation: Mechanical Engineers
Task statement: Investigate equipment failures or difficulties to diagnose faulty operation and recommend remedial actions.
Part: Diagnose the cause of a failure and recommend remedial action in a report.
Type: DISCRETE
Work item: one failure investigation report
Start: failure or problem reported
End: report with cause and remedy issued
Checked by: maintenance manager, plant management

[3407a]
Occupation: Loan Officers
Task statement: Approve loans within specified limits, and refer loan applications outside those limits to management for approval.
Part: Approve a loan within the officer's authority, or refer it to management if it is above the limit.
Type: DISCRETE
Work item: one loan application decided (approved or referred)
Start: completed application and analysis ready for decision
End: approval issued or referral sent to management
Checked by: management, credit risk and the borrower

[58a]
Occupation: Medical and Health Services Managers
Task statement: Plan, implement, and administer programs and services in a health care or medical facility, including personnel administration, training, and coordination of medical, nursing and physical plant staff.
Part: Plan a health care program or service.
Type: DISCRETE
Work item: one program or service plan
Start: program or service planning need is identified
End: plan is submitted to the responsible leadership
Checked by: facility leadership and affected department heads

[246a]
Occupation: Child, Family, and School Social Workers
Task statement: Arrange for medical, psychiatric, and other tests that may disclose causes of difficulties and indicate remedial measures.
Part: Arrange medical, psychiatric or other tests to find causes of a client's difficulties.
Type: DISCRETE
Work item: one test or evaluation arranged for a client
Start: need for testing decided
End: test booked and client and provider notified
Checked by: client, testing provider, supervisor

[665c]
Occupation: First-Line Supervisors of Retail Sales Workers
Task statement: Hire, train, and evaluate personnel in sales or marketing establishments, promoting or firing workers when appropriate.
Part: Evaluate an employee's work performance.
Type: DISCRETE
Work item: One employee performance evaluation
Start: Review period or evaluation request begins
End: Assessment is completed and communicated
Checked by: Employee, store manager, and human resources

[9420b]
Occupation: Medical Transcriptionists
Task statement: Perform data entry and data retrieval services, providing data for inclusion in medical records and for transmission to physicians.
Part: Retrieve medical data for inclusion in records or transmission to a physician.
Type: DISCRETE
Work item: one medical data retrieval request fulfilled
Start: request or instruction to retrieve information received
End: requested data supplied to the record or physician
Checked by: requesting physician or medical records staff

[528a]
Occupation: Licensed Practical and Licensed Vocational Nurses
Task statement: Make appointments, keep records, or perform other clerical duties in doctors' offices or clinics.
Part: Make or change appointments while a patient is on the phone or at the desk.
Type: LIVE_SERVICE
Work item: one appointment made or changed during a patient contact
Start: patient requests an appointment or change
End: appointment is entered and confirmed to the patient
Checked by: the patient and clinic staff

[784b]
Occupation: Medical Secretaries and Administrative Assistants
Task statement: Perform various clerical or administrative functions, such as ordering and maintaining an inventory of supplies.
Part: Update supply inventory records from counts and receipts.
Type: DISCRETE
Work item: one inventory record update
Start: supply count, receipt, or adjustment received
End: inventory record updated
Checked by: office manager or purchasing staff

[20554a]
Occupation: Public Relations Specialists
Task statement: Write press releases or other media communications to promote clients.
Part: Write a press release or other media communication for a client.
Type: DISCRETE
Work item: one press release or media communication
Start: news item and brief received
End: release approved and distributed
Checked by: client or communications manager

