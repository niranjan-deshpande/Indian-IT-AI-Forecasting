You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Code each ITEM independently, in the order given; do not go
back and adjust earlier answers to make them consistent with later ones.

Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/bpo_v1/s1/batch1.json
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
[3483a]
Occupation: Computer Systems Analysts
Task statement: Prepare cost-benefit and return-on-investment analyses to aid in decisions on system implementation.
Part: Prepare a cost-benefit and return-on-investment analysis for a system implementation.
Type: DISCRETE
Work item: one cost-benefit/ROI analysis
Start: proposed implementation defined
End: analysis delivered
Checked by: management

[3475a]
Occupation: Computer Systems Analysts
Task statement: Assess the usefulness of pre-developed application packages and adapt them to a user environment.
Part: Evaluate a pre-developed application package for usefulness and report.
Type: DISCRETE
Work item: one package evaluation
Start: package identified
End: evaluation reported
Checked by: management; IT manager

[23330b]
Occupation: Insurance Claims and Policy Processing Clerks
Task statement: Collect initial premiums and issue receipts.
Part: Record initial premiums received by mail and send receipts.
Type: DISCRETE
Work item: one batch of premiums receipted
Start: payments received
End: receipts sent
Checked by: accounting

[2492a]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Compile statistical, financial, accounting, or auditing reports and tables pertaining to such matters as cash receipts, expenditures, accounts payable and receivable, and profits and losses.
Part: Compile a report or table on cash receipts, expenditures, payables, receivables or profit and loss.
Type: DISCRETE
Work item: one financial report
Start: period ends or request made
End: report delivered
Checked by: manager; accountant

[3466a]
Occupation: Computer Systems Analysts
Task statement: Use object-oriented programming languages, as well as client and server applications development processes and multimedia and Internet technology.
Part: Write code for a program or application using object-oriented languages and client-server and web technologies.
Type: DISCRETE
Work item: one program, module or feature coded
Start: specification or ticket assigned
End: code complete and passed to test/review
Checked by: project lead; testers

[23264c]
Occupation: Billing and Posting Clerks
Task statement: Create billing documents, shipping labels, credit memorandums, or credit forms.
Part: Create a credit memorandum or credit form.
Type: DISCRETE
Work item: one credit memorandum or credit form created
Start: credit transaction and supporting details received
End: credit document completed and routed for processing
Checked by: accounts-receivable staff or a supervisor

[22882b]
Occupation: Medical Records Specialists
Task statement: Maintain or operate a variety of health record indexes or storage and retrieval systems to collect, classify, store, or analyze information.
Part: Run an analysis or query from the record system.
Type: DISCRETE
Work item: one query or report
Start: request
End: output delivered
Checked by: requester

[14728a]
Occupation: Web Developers
Task statement: Document technical factors such as server load, bandwidth, database performance, and browser and device types.
Part: Document technical factors such as server load, bandwidth, database performance, and browser and device types.
Type: DISCRETE
Work item: one technical factors report
Start: monitoring data gathered
End: report filed or shared
Checked by: development team and management

[23265c]
Occupation: Billing and Posting Clerks
Task statement: Perform general administrative tasks, such as answering telephones, scheduling appointments, and ordering supplies or equipment.
Part: Schedule or change an appointment from a written request.
Type: DISCRETE
Work item: one appointment scheduled or changed from a written request
Start: written appointment request received
End: calendar updated and confirmation sent
Checked by: requester and staff member whose calendar is updated

[2495a]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Operate 10-key calculators, typewriters, and copy machines to perform calculations and produce documents.
Part: Do calculations on a 10-key calculator for other accounting tasks.
Type: DISCRETE
Work item: one set of calculations
Start: figures to calculate
End: totals handed over
Checked by: supervisor

[22887a]
Occupation: Medical Records Specialists
Task statement: Release information to persons or agencies according to regulations.
Part: Release information to a requester at the counter or on the phone.
Type: LIVE_SERVICE
Work item: one release made during contact
Start: requester asks and is verified
End: information provided
Checked by: requester, privacy officer

[2494b]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Access computerized financial information to answer general questions as well as those related to specific accounts.
Part: Answer a written question about accounts from computerized records.
Type: DISCRETE
Work item: one written inquiry answered
Start: inquiry received
End: reply sent
Checked by: the person asking; supervisor

[3464b]
Occupation: Computer Systems Analysts
Task statement: Provide staff and users with assistance solving computer-related problems, such as malfunctions and program problems.
Part: Resolve a user's reported computer problem from a written ticket or email after the contact.
Type: DISCRETE
Work item: one support ticket resolved
Start: ticket received
End: fix confirmed, ticket closed
Checked by: the user who raised it; help desk lead

[21648a]
Occupation: Database Administrators
Task statement: Identify, evaluate and recommend hardware or software technologies to achieve desired database performance.
Part: Identify, evaluate and recommend hardware or software for database performance.
Type: DISCRETE
Work item: one technology recommendation
Start: performance need
End: recommendation delivered
Checked by: management

[21668a]
Occupation: Software Developers
Task statement: Determine system performance standards.
Part: Set the performance standards that a system must meet.
Type: DISCRETE
Work item: one set of system performance standards
Start: system requirements being scoped
End: standards documented and agreed with stakeholders
Checked by: project manager and stakeholders

[21669a]
Occupation: Software Developers
Task statement: Develop or direct software system testing or validation procedures, programming, or documentation.
Part: Develop software system testing or validation procedures.
Type: DISCRETE
Work item: one software test or validation procedure
Start: requirements and the system or change to be tested are available
End: procedure is documented and made available to testers
Checked by: test lead and development team

[2490b]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Classify, record, and summarize numerical and financial data to compile and keep financial records, using journals and ledgers or computers.
Part: Summarize recorded financial data for a period.
Type: DISCRETE
Work item: one period summary of financial data
Start: period closes
End: summary delivered
Checked by: accountant; manager

[23237a]
Occupation: Billing and Posting Clerks
Task statement: Post stop-payment notices to prevent payment of protested checks.
Part: Post a stop-payment notice to prevent payment of a protested check.
Type: DISCRETE
Work item: one stop-payment notice posted
Start: notice received
End: notice posted
Checked by: bank; supervisor

[23243a]
Occupation: Billing and Posting Clerks
Task statement: Resolve discrepancies in accounting records.
Part: Resolve a discrepancy in accounting records.
Type: DISCRETE
Work item: one discrepancy resolved
Start: discrepancy found
End: records corrected
Checked by: supervisor

[22880a]
Occupation: Medical Records Specialists
Task statement: Enter data, such as demographic characteristics, history and extent of disease, diagnostic procedures, or treatment into computer.
Part: Enter patient data into the computer.
Type: DISCRETE
Work item: one patient record's data entered
Start: source documents available
End: data entered
Checked by: HIM supervisor

[1301a]
Occupation: Database Administrators
Task statement: Plan, coordinate, and implement security measures to safeguard information in computer files against accidental or unauthorized damage, modification or disclosure.
Part: Plan and coordinate measures to safeguard computer-file information.
Type: DISCRETE
Work item: one security measures plan
Start: system protection need or risk identified
End: measures documented and coordinated for implementation
Checked by: security management and system owners

[21651a]
Occupation: Database Administrators
Task statement: Test changes to database applications or systems.
Part: Test changes to database applications or systems.
Type: DISCRETE
Work item: one change tested
Start: change ready
End: results reported
Checked by: developers and project lead

[2500b]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Receive, record, and bank cash, checks, and vouchers.
Part: Record mailed or accumulated cash, checks and vouchers in the accounting records.
Type: DISCRETE
Work item: one batch of received payments recorded
Start: payments or vouchers received
End: receipts entered and batch totals agreed
Checked by: accounting supervisor

[1303b]
Occupation: Database Administrators
Task statement: Train users and answer questions.
Part: Answer a user's database question during a live contact.
Type: LIVE_SERVICE
Work item: one user question answered during a live contact
Start: user asks the question
End: answer communicated to the user
Checked by: the user

[3465b]
Occupation: Computer Systems Analysts
Task statement: Test, maintain, and monitor computer programs and systems, including coordinating the installation of computer programs and systems.
Part: Perform a maintenance change on a computer program or system.
Type: DISCRETE
Work item: one program or system maintenance change
Start: maintenance need or scheduled change identified
End: change applied and its completion recorded
Checked by: system owner and operations team

[14723b]
Occupation: Web Developers
Task statement: Monitor security system performance logs to identify problems and notify security specialists when problems occur.
Part: Notify security specialists of a problem found in the logs.
Type: DISCRETE
Work item: one security problem escalated
Start: problem identified in logs
End: notice sent and acknowledged
Checked by: security specialists

[22892b]
Occupation: Medical Records Specialists
Task statement: Schedule medical appointments for patients.
Part: Schedule from written requests and referrals.
Type: DISCRETE
Work item: one batch of appointments scheduled
Start: requests received
End: appointments made, confirmations sent
Checked by: clinic, patients

[14719a]
Occupation: Web Developers
Task statement: Recommend and implement performance improvements.
Part: Recommend a website performance improvement.
Type: DISCRETE
Work item: one performance improvement recommendation
Start: performance issue or improvement opportunity identified
End: recommendation communicated to the decision-maker
Checked by: development lead or site owner

[2506a]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Transfer details from separate journals to general ledgers or data processing sheets.
Part: Transfer entries from separate journals to the general ledger or processing sheets.
Type: DISCRETE
Work item: one batch of journal entries posted to the ledger
Start: journal ready
End: ledger updated
Checked by: supervisor; accountant

[23242a]
Occupation: Billing and Posting Clerks
Task statement: Operate typing, adding, calculating, or billing machines.
Part: Use office or billing equipment to process a billing calculation or document.
Type: DISCRETE
Work item: one billing calculation or document processed using office equipment
Start: billing information or document supplied for processing
End: calculation or document produced for the next billing step
Checked by: billing staff or a supervisor

[1322a]
Occupation: Network and Computer Systems Administrators
Task statement: Design, configure, and test computer hardware, networking software and operating system software.
Part: Design, configure, and test a network or operating system software configuration.
Type: DISCRETE
Work item: one tested network or operating system configuration
Start: configuration requirement or change request received
End: configuration is tested and handed over or deployed
Checked by: network or systems operations team

[22881a]
Occupation: Medical Records Specialists
Task statement: Identify, compile, abstract, and code patient data, using standard classification systems.
Part: Abstract and code an encounter using standard classification systems.
Type: DISCRETE
Work item: one encounter abstracted and coded
Start: chart ready for coding
End: codes finalized
Checked by: coding auditor, billing

[2510a]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Complete and submit tax forms and returns, workers' compensation forms, pension contribution forms, and other government documents.
Part: Complete and submit tax, workers' compensation, pension and other government forms.
Type: DISCRETE
Work item: one government form completed and submitted
Start: filing due
End: form submitted
Checked by: agency; supervisor

[21672a]
Occupation: Software Developers
Task statement: Obtain and evaluate information on factors such as reporting formats required, costs, or security needs to determine hardware configuration.
Part: Gather information on reporting formats, costs and security needs and use it to specify the hardware configuration.
Type: DISCRETE
Work item: one hardware configuration recommendation
Start: system requirements and constraints gathered
End: recommended hardware configuration delivered
Checked by: project manager and IT purchasing

[1317a]
Occupation: Network and Computer Systems Administrators
Task statement: Perform data backups and disaster recovery operations.
Part: Run and verify a scheduled data backup.
Type: DISCRETE
Work item: one backup job run and verified
Start: scheduled backup time
End: job completed and checked in the log
Checked by: IT manager and users who may need restores

[2487a]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Operate computers programmed with accounting software to record, store, and analyze information.
Part: Record transactions in the accounting software.
Type: DISCRETE
Work item: one batch of transactions recorded
Start: source documents ready
End: batch posted
Checked by: supervisor; accountant

[18561a]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Prepare and process payroll information.
Part: Prepare and process payroll information.
Type: DISCRETE
Work item: one payroll run
Start: pay period closes
End: payroll processed
Checked by: employees; supervisor

[21669c]
Occupation: Software Developers
Task statement: Develop or direct software system testing or validation procedures, programming, or documentation.
Part: Develop software system documentation.
Type: DISCRETE
Work item: one software documentation document or update
Start: a system or change requires documentation
End: documentation is submitted or published
Checked by: technical reviewers and documentation users

[23266c]
Occupation: Billing and Posting Clerks
Task statement: Return checks to customers or retrieve checks returned to customers in error, adjusting accounts and answering inquiries about errors as necessary.
Part: Answer a customer's live inquiry about a check-return error.
Type: LIVE_SERVICE
Work item: one live check-error inquiry answered
Start: customer asks about the check error
End: explanation or status relayed to the customer
Checked by: customer and, if reviewed, a supervisor

[23313a]
Occupation: Insurance Claims and Policy Processing Clerks
Task statement: Prepare insurance claim forms or related documents, and review them for completeness.
Part: Prepare a claim form or related document and review it for completeness.
Type: DISCRETE
Work item: one claim form prepared and checked for completeness
Start: claim notice or information received
End: complete form ready for adjudication or routed
Checked by: claims adjuster or supervisor

[1315a]
Occupation: Database Administrators
Task statement: Revise company definition of data as defined in data dictionary.
Part: Revise the company's definitions of data in the data dictionary.
Type: DISCRETE
Work item: one data dictionary update
Start: change identified
End: dictionary revised
Checked by: data owners

[2502a]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Compare computer printouts to manually maintained journals to determine if they match.
Part: Compare computer printouts with manually kept journals to see if they match.
Type: DISCRETE
Work item: one printout-to-journal comparison
Start: printout produced
End: match confirmed or differences noted
Checked by: supervisor

[3472a]
Occupation: Computer Systems Analysts
Task statement: Determine computer software or hardware needed to set up or alter systems.
Part: Decide which software or hardware is needed to set up or change a system and list it.
Type: DISCRETE
Work item: one set of hardware/software requirements for a system
Start: system need defined
End: requirements list delivered
Checked by: project lead; purchasing/IT manager

[2514a]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Prepare purchase orders and expense reports.
Part: Prepare a purchase order.
Type: DISCRETE
Work item: one purchase order
Start: need for purchase
End: order issued
Checked by: approver; supplier

[22884a]
Occupation: Medical Records Specialists
Task statement: Process and prepare business or government forms.
Part: Prepare a business or government form.
Type: DISCRETE
Work item: one form prepared and submitted
Start: form needed
End: form submitted
Checked by: receiving agency, supervisor

[2491c]
Occupation: Bookkeeping, Accounting, and Auditing Clerks
Task statement: Calculate, prepare, and issue bills, invoices, account statements, and other financial statements according to established procedures.
Part: Prepare and issue a financial statement.
Type: DISCRETE
Work item: one financial statement prepared and issued
Start: period's accounting figures available
End: statement prepared and issued
Checked by: accountant or financial manager

