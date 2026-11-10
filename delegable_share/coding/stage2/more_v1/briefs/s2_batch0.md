You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Code each ITEM independently, in the order given; do not go
back and adjust earlier answers to make them consistent with later ones.

Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/more_v1/s2/batch0.json
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
[6536a]
Occupation: Elementary School Teachers, Except Special Education
Task statement: Observe and evaluate students' performance, behavior, social development, and physical health.
Part: Observe a student and record an evaluation of their academic performance, behavior, social development or health.
Type: DISCRETE
Work item: one student's observation note or evaluation entry
Start: teacher observes a student's work or behavior and decides it is worth recording
End: note or checklist entry saved in the teacher's records
Checked by: the teacher themselves later, parents, counselor, and principal

[23071a]
Occupation: Police and Sheriff's Patrol Officers
Task statement: Question individuals entering secured areas to determine their business, directing and rerouting individuals as necessary.
Part: Ask people entering a secured area their business and admit or redirect them.
Type: LIVE_SERVICE
Work item: one entrant screened at a checkpoint
Start: person approaches the entry point
End: person admitted, redirected or refused
Checked by: facility security or supervisor

[2462a]
Occupation: Real Estate Sales Agents
Task statement: Contact property owners and advertise services to solicit property sales listings.
Part: Send mailings or emails advertising services to property owners to solicit listings.
Type: DISCRETE
Work item: one solicitation mailing or email batch
Start: target owner list assembled
End: campaign sent
Checked by: broker

[20555a]
Occupation: Public Relations Specialists
Task statement: Plan or direct development or communication of programs to maintain favorable public or stockholder perceptions of an organization's accomplishments, agenda, or environmental responsibility.
Part: Plan a program to maintain favorable public or stockholder perceptions of an organization.
Type: DISCRETE
Work item: one public or stockholder perception program plan
Start: organizational perception objective and relevant information are received
End: program plan is submitted to management
Checked by: communications and organizational management

[2038b]
Occupation: Medical Assistants
Task statement: Perform general office duties, such as answering telephones, taking dictation, or completing insurance forms.
Part: Transcribe dictated office or clinical material.
Type: DISCRETE
Work item: one dictated document transcribed
Start: dictation is received
End: transcription is completed and returned or filed
Checked by: the person who dictated it

[3416a]
Occupation: Loan Officers
Task statement: Submit applications to credit analysts for verification and recommendation.
Part: Submit an application to credit analysts for verification and recommendation.
Type: DISCRETE
Work item: one application submitted to credit analysis
Start: application package complete
End: package sent to the analyst and acknowledged
Checked by: credit analyst

[4628b]
Occupation: Telemarketers
Task statement: Schedule appointments for sales representatives to meet with prospective customers or for customers to attend sales presentations.
Part: Arrange appointments after the call from callbacks and written requests.
Type: DISCRETE
Work item: one batch of appointments scheduled
Start: requests or callbacks received
End: appointments entered and confirmations sent
Checked by: the sales representatives

[5319a]
Occupation: Information Security Analysts
Task statement: Monitor use of data files and regulate access to safeguard information in computer files.
Part: Review usage of data files and report unusual access.
Type: DISCRETE
Work item: one access log review with findings
Start: log period or alert selected for review
End: findings reported or cleared
Checked by: security manager or auditor

[9718a]
Occupation: First-Line Supervisors of Office and Administrative Support Workers
Task statement: Analyze financial activities of establishments or departments and provide input into budget planning and preparation processes.
Part: Analyze the unit's financial results and give input into the budget.
Type: DISCRETE
Work item: one financial analysis with budget input
Start: financial figures and budget request received
End: analysis and budget input submitted
Checked by: department manager, finance

[23878b]
Occupation: Stockers and Order Fillers
Task statement: Receive and count stock items, and record data manually or on computer.
Part: Record the counted quantities manually or on a computer.
Type: DISCRETE
Work item: one shipment receiving record
Start: shipment counted
End: quantities entered in the log or system
Checked by: inventory control and purchasing; supervisor

[24026b]
Occupation: Editors
Task statement: Respond to questions from the public.
Part: Answer a member of the public's emailed or written question.
Type: DISCRETE
Work item: one written public question answered
Start: question received
End: reply sent
Checked by: the person asking, editor

[303b]
Occupation: Graphic Designers
Task statement: Draw and print charts, graphs, illustrations, and other artwork, using computer.
Part: Draw and print an illustration or other artwork using a computer.
Type: DISCRETE
Work item: one computer-drawn illustration or artwork
Start: artwork brief or reference materials received
End: artwork completed and printed or supplied for use
Checked by: client or creative supervisor

[23972a]
Occupation: Graphic Designers
Task statement: Write or edit copy for clients.
Part: Write or edit copy for a client's design job.
Type: DISCRETE
Work item: one piece of copy written or edited for a client
Start: copy need or draft text received
End: final copy delivered to the client
Checked by: client

[23056a]
Occupation: Police and Sheriff's Patrol Officers
Task statement: Review facts of incidents to determine if criminal act or statute violations were involved.
Part: Review the facts of an incident and decide whether a crime or statute violation occurred.
Type: DISCRETE
Work item: one incident reviewed with a determination of offense or no offense
Start: facts of the incident gathered
End: determination recorded (offense, no offense, charge type)
Checked by: supervisor, prosecutor

[729a]
Occupation: Insurance Sales Agents
Task statement: Select company that offers type of coverage requested by client to underwrite policy.
Part: Pick the insurance company that offers the coverage a client asked for.
Type: DISCRETE
Work item: one carrier selected for a client's coverage
Start: coverage requirements known
End: carrier chosen and recorded
Checked by: client, agency manager

[670a]
Occupation: First-Line Supervisors of Retail Sales Workers
Task statement: Estimate consumer demand and determine the types and amounts of goods to be sold.
Part: Estimate consumer demand and decide the types and amounts of goods to be sold.
Type: DISCRETE
Work item: one buying plan for a category or period
Start: sales history and trends reviewed
End: quantities and types decided and submitted
Checked by: store manager or buyer

[23438b]
Occupation: Carpenters
Task statement: Maintain records, document actions, and present written progress reports.
Part: Write a progress report on the job for the employer or client.
Type: DISCRETE
Work item: one written progress report
Start: reporting period or milestone reached
End: report delivered to employer or client
Checked by: employer, general contractor or client

[306a]
Occupation: Graphic Designers
Task statement: Develop graphics and layouts for product illustrations, company logos, and Web sites.
Part: Develop graphics or layouts for a product illustration.
Type: DISCRETE
Work item: one product illustration or its layout
Start: product illustration brief and references received
End: illustration or layout submitted for review
Checked by: client or creative supervisor

[780a]
Occupation: Medical Secretaries and Administrative Assistants
Task statement: Interview patients to complete documents, case histories, or forms, such as intake or insurance forms.
Part: Interview a patient to complete intake, case history or insurance forms.
Type: LIVE_SERVICE
Work item: one patient's forms completed during an interview
Start: patient arrives or is called for intake
End: completed and signed forms handed to staff
Checked by: clinician, billing, patient

[1818a]
Occupation: Pharmacists
Task statement: Refer patients to other health professionals or agencies when appropriate.
Part: Refer a patient to another health professional or agency while speaking with them.
Type: LIVE_SERVICE
Work item: one patient referred during a counseling contact
Start: pharmacist identifies a need beyond pharmacy
End: patient told where to go and agrees
Checked by: the patient

[7536b]
Occupation: Economists
Task statement: Study economic and statistical data in area of specialization, such as finance, labor, or agriculture.
Part: Analyze data in the specialization and write up a short brief of the findings.
Type: DISCRETE
Work item: one data analysis brief
Start: question or data release in hand
End: brief sent
Checked by: supervisor, colleagues, client

[4240a]
Occupation: Home Health Aides
Task statement: Maintain records of patient care, condition, progress, or problems to report and discuss observations with supervisor or case manager.
Part: Write up a visit's care record covering the patient's condition, progress, or problems.
Type: DISCRETE
Work item: one visit care record written
Start: care visit or shift ends
End: record submitted to the agency
Checked by: supervising nurse or case manager

[21474b]
Occupation: Project Management Specialists
Task statement: Prepare and submit budget estimates, progress reports, or cost tracking reports.
Part: Prepare and submit a progress report.
Type: DISCRETE
Work item: one progress report
Start: reporting period ends
End: report submitted
Checked by: project manager; client

[514b]
Occupation: Licensed Practical and Licensed Vocational Nurses
Task statement: Work as part of a healthcare team to assess patient needs, plan and modify care, and implement interventions.
Part: Contribute to planning and modifying patient care with the healthcare team.
Type: DISCRETE
Work item: one patient care plan contribution or update
Start: patient needs or a need to modify care are identified
End: the nurse's contribution is communicated and incorporated into the care plan
Checked by: the supervising registered nurse and healthcare team

[9423a]
Occupation: Medical Transcriptionists
Task statement: Set up and maintain medical files and databases, including records such as x-ray, lab, and procedure reports, medical histories, diagnostic workups, admission and discharge summaries, and clinical resumes.
Part: Set up a medical files database using the workplace's approved system.
Type: DISCRETE
Work item: one medical records database or collection set up
Start: request and requirements for a record collection received
End: collection configured and made available to authorized staff
Checked by: medical records supervisor or system users

[1818b]
Occupation: Pharmacists
Task statement: Refer patients to other health professionals or agencies when appropriate.
Part: Send a referral or notification to another provider or agency.
Type: DISCRETE
Work item: one referral communication sent
Start: decision to refer made
End: referral sent to the provider or agency
Checked by: receiving provider

[242a]
Occupation: Child, Family, and School Social Workers
Task statement: Collect supplementary information needed to assist client, such as employment records, medical records, or school reports.
Part: Collect employment, medical, school or other records needed to help a client.
Type: DISCRETE
Work item: one set of supplementary records obtained for a case
Start: need for outside records identified
End: records received and filed in the case
Checked by: the caseworker and supervisor

[21829b]
Occupation: Data Scientists
Task statement: Deliver oral or written presentations of the results of mathematical modeling and data analysis to management or other end users.
Part: Write up the results of modelling and analysis as a report or slide deck for management or end users.
Type: DISCRETE
Work item: one results report or slide deck
Start: analysis results ready to communicate
End: report or deck delivered to management or end users
Checked by: manager; end users

[2028b]
Occupation: Medical Assistants
Task statement: Collect blood, tissue, or other laboratory specimens, log the specimens, and prepare them for testing.
Part: Log collected specimens for laboratory testing.
Type: DISCRETE
Work item: one specimen log entry
Start: a collected specimen and its identifying information are available
End: the specimen is entered in the log
Checked by: laboratory staff

[1776a]
Occupation: Editors
Task statement: Prepare, rewrite and edit copy to improve readability, or supervise others who do this work.
Part: Prepare, rewrite and edit a piece of copy to improve readability.
Type: DISCRETE
Work item: one piece of copy edited
Start: copy received for editing
End: edited copy passed to the next stage
Checked by: the author, senior editor or the publisher

[20708b]
Occupation: General and Operations Managers
Task statement: Manage the movement of goods into and out of production facilities to ensure efficiency, effectiveness, or sustainability of operations.
Part: Resolve an identified goods-movement problem affecting facility operations.
Type: DISCRETE
Work item: one goods-movement issue resolved
Start: delay, inefficiency, or other movement issue identified
End: corrective arrangement decided and communicated
Checked by: logistics and production managers

[980a]
Occupation: Computer and Information Systems Managers
Task statement: Prepare and review operational reports or project progress reports.
Part: Prepare an operational or project progress report for management.
Type: DISCRETE
Work item: one operational or progress report
Start: reporting period data gathered
End: report sent to management
Checked by: CIO, executive management

[23104a]
Occupation: Fast Food and Counter Workers
Task statement: Request and record customer orders, and compute bills, using cash registers, multi-counting machines, or pencil and paper.
Part: Ask for and record a customer's order and work out the bill on the register.
Type: LIVE_SERVICE
Work item: one customer order entered and totalled
Start: customer steps up to order
End: order confirmed and total quoted
Checked by: the customer and the kitchen that makes it

[676a]
Occupation: First-Line Supervisors of Retail Sales Workers
Task statement: Establish credit policies and operating procedures.
Part: Establish credit policies and operating procedures.
Type: DISCRETE
Work item: one credit policy or procedure issued
Start: need for or change to credit rules identified
End: policy communicated to staff
Checked by: store or district manager; finance

