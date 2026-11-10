You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Code each ITEM independently, in the order given; do not go
back and adjust earlier answers to make them consistent with later ones.

Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/comp_v1/s1/batch2.json
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
[18492b]
Occupation: Paralegals and Legal Assistants
Task statement: Prepare for trial by performing tasks such as organizing exhibits.
Part: Organize electronic exhibits and related materials for trial.
Type: DISCRETE
Work item: one electronic exhibit set prepared for trial
Start: trial materials and exhibit instructions received
End: electronic exhibits organized and made available to the trial team
Checked by: trial attorney

[10647a]
Occupation: Heavy and Tractor-Trailer Truck Drivers
Task statement: Collect delivery instructions from appropriate sources, verifying instructions and routes.
Part: Collect and verify delivery instructions and the route for a load from dispatch, the customer or the receiver.
Type: DISCRETE
Work item: one load's delivery instructions collected and verified
Start: load assigned
End: instructions and route confirmed with source
Checked by: dispatcher and customer

[20877a]
Occupation: Lawyers
Task statement: Prepare, draft, and review legal documents, such as wills, deeds, patent applications, mortgages, leases, and contracts.
Part: Draft a new legal document.
Type: DISCRETE
Work item: one document drafted
Start: instruction
End: sent
Checked by: client

[1258a]
Occupation: Credit Analysts
Task statement: Consult with customers to resolve complaints and verify financial and credit transactions.
Part: Resolve a customer's complaint or verify a transaction while the customer is on the phone or at the desk.
Type: LIVE_SERVICE
Work item: one complaint or verification handled during a customer contact
Start: customer raises the complaint or asks for verification
End: customer told the outcome
Checked by: the customer, and the supervisor

[1866a]
Occupation: Registered Nurses
Task statement: Engage in research activities related to nursing.
Part: Develop a nursing research protocol.
Type: DISCRETE
Work item: one nursing research protocol or amendment
Start: research question or need for amendment is identified
End: protocol or amendment is submitted for review
Checked by: research lead and ethics review body

[1859b]
Occupation: Registered Nurses
Task statement: Prescribe or recommend drugs, medical devices, or other forms of treatment, such as physical therapy, inhalation therapy, or related therapeutic procedures.
Part: Recommend or prescribe a treatment after reviewing clinical information outside patient contact.
Type: DISCRETE
Work item: one treatment recommendation or prescription completed outside patient contact
Start: clinical information and a treatment need are available
End: recommendation or prescription is documented and sent
Checked by: the responsible clinician and dispensing or treatment team

[1844a]
Occupation: Registered Nurses
Task statement: Order, interpret, and evaluate diagnostic tests to identify and assess patient's condition.
Part: Order tests within protocol, review the results, and act on or report them.
Type: DISCRETE
Work item: one diagnostic result reviewed and acted on or reported
Start: result returned or test needed
End: result interpreted and communicated or action taken
Checked by: physician, patient

[3977a]
Occupation: Technical Writers
Task statement: Analyze developments in specific field to determine need for revisions in previously published materials and development of new material.
Part: Analyze field developments and recommend whether documentation needs revision or new material.
Type: DISCRETE
Work item: one documentation-needs assessment
Start: field developments identified for assessment
End: assessment of needed revisions or new material communicated
Checked by: publication manager, editor, or subject-matter lead

[20910a]
Occupation: Proofreaders and Copy Markers
Task statement: Typeset and measure dimensions, spacing, and positioning of page elements, such as copy and illustrations, to verify conformance to specifications, using printer's ruler or layout software.
Part: Typeset copy and page elements using layout software.
Type: DISCRETE
Work item: one page or assigned layout typeset
Start: copy, illustrations, and layout specifications are received
End: typeset layout is saved and submitted for review
Checked by: editor or production team

[2885b]
Occupation: Electricians
Task statement: Perform business management duties, such as maintaining records or files, preparing reports, or ordering supplies or equipment.
Part: Order supplies or equipment.
Type: DISCRETE
Work item: one supply order placed
Start: need identified
End: order confirmed
Checked by: owner; supplier

[7281b]
Occupation: Management Analysts
Task statement: Interview personnel and conduct on-site observation to ascertain unit functions, work performed, and methods, equipment, and personnel used.
Part: Observe work on site to ascertain unit functions, methods, equipment, and staffing.
Type: DISCRETE
Work item: one on-site work observation record
Start: observation session or work process is selected
End: observations are recorded and available to the study team
Checked by: study lead or analyst

[9331a]
Occupation: Interpreters and Translators
Task statement: Read written materials, such as legal documents, scientific works, or news reports, and rewrite material into specified languages.
Part: Read a written source document such as a legal, scientific or news text and translate it into the target language.
Type: DISCRETE
Work item: one document translated
Start: source document received
End: translation delivered to client
Checked by: client; reviewer; end readers

[21520a]
Occupation: Accountants and Auditors
Task statement: Report to management regarding the finances of establishment.
Part: Report to management on the finances of the establishment.
Type: DISCRETE
Work item: one financial report to management
Start: period closed
End: report delivered
Checked by: management

[20908b]
Occupation: Proofreaders and Copy Markers
Task statement: Archive documents, conduct research, and read copy, using the internet and various computer programs.
Part: Research a fact or reference online to verify copy.
Type: DISCRETE
Work item: one research question answered
Start: question arises while reading
End: answer found and recorded
Checked by: author or editor

[3790a]
Occupation: Lawyers
Task statement: Perform administrative and management functions related to the practice of law.
Part: Prepare billing and time records.
Type: DISCRETE
Work item: one billing cycle
Start: period end
End: invoices sent
Checked by: clients

[5165a]
Occupation: Proofreaders and Copy Markers
Task statement: Read proof sheets aloud, calling out punctuation marks and spelling unusual words and proper names.
Part: Read proof sheets aloud to a partner, calling out punctuation and spelling unusual words and names, so that errors are caught and marked.
Type: DISCRETE
Work item: one proof read aloud with a partner and marked
Start: reading begins
End: proof read through and marks entered
Checked by: editor or author

[18494a]
Occupation: Paralegals and Legal Assistants
Task statement: File pleadings with court clerks.
Part: File pleadings through an electronic court filing system.
Type: DISCRETE
Work item: one pleading submitted electronically to the court
Start: approved pleading and filing instructions received
End: submission completed and court acknowledgment or rejection received
Checked by: court clerk and supervising attorney

[2335c]
Occupation: Childcare Workers
Task statement: Identify signs of emotional or developmental problems in children and bring them to parents' or guardians' attention.
Part: Communicate an identified emotional or developmental concern to a parent or guardian in writing.
Type: DISCRETE
Work item: one written concern communicated to a parent or guardian
Start: observations indicating a concern are available for communication
End: written concern is sent to the parent or guardian
Checked by: the parent or guardian and childcare supervisor

[7286a]
Occupation: Management Analysts
Task statement: Recommend purchase of storage equipment and design area layout to locate equipment in space available.
Part: Recommend purchase of storage equipment.
Type: DISCRETE
Work item: one equipment recommendation
Start: need identified
End: recommendation delivered
Checked by: management; purchasing

[6643a]
Occupation: Secondary School Teachers, Except Special and Career/Technical Education
Task statement: Prepare materials and classrooms for class activities.
Part: Prepare materials for a class activity.
Type: DISCRETE
Work item: one lesson's materials prepared
Start: lesson planned
End: materials ready
Checked by: the teacher; students who use them

[3788b]
Occupation: Lawyers
Task statement: Search for and examine public and other legal records to write opinions or establish ownership.
Part: Search and examine legal records to support a legal opinion.
Type: DISCRETE
Work item: one record-search finding for an opinion
Start: opinion question and record-search scope identified
End: relevant record findings documented for the opinion
Checked by: lawyer preparing or reviewing the opinion

[1255a]
Occupation: Credit Analysts
Task statement: Generate financial ratios, using computer programs, to evaluate customers' financial status.
Part: Run a customer's financial statements through software to produce financial ratios.
Type: DISCRETE
Work item: one set of financial ratios for a customer
Start: financial statements entered or loaded
End: ratio output checked and attached to the file
Checked by: the analyst's credit manager

[2892a]
Occupation: Electricians
Task statement: Provide preliminary sketches or cost estimates for materials or services.
Part: Provide a preliminary sketch for a job.
Type: DISCRETE
Work item: one preliminary sketch
Start: customer requests job
End: sketch given
Checked by: customer

[1865a]
Occupation: Registered Nurses
Task statement: Work with individuals, groups, or families to plan or implement programs designed to improve the overall health of communities.
Part: Plan a community health program with groups or families.
Type: DISCRETE
Work item: one community program plan
Start: community need identified
End: plan agreed
Checked by: program sponsor, community partners

[2880a]
Occupation: Electricians
Task statement: Plan layout and installation of electrical wiring, equipment, or fixtures, based on job specifications and local codes.
Part: Plan the layout and installation of wiring and fixtures from job specs and local codes.
Type: DISCRETE
Work item: one installation layout plan for a job
Start: job specs received
End: layout plan ready for installation
Checked by: foreman; code inspector

[20693a]
Occupation: Heavy and Tractor-Trailer Truck Drivers
Task statement: Check all load-related documentation for completeness and accuracy.
Part: Check a load's shipping documents for completeness and accuracy before departing or delivering.
Type: DISCRETE
Work item: one load's documents checked
Start: documents handed to driver
End: documents confirmed complete or errors raised
Checked by: dispatcher and shipper

[3793a]
Occupation: Lawyers
Task statement: Help develop federal and state programs, draft and interpret laws and legislation, and establish enforcement procedures.
Part: Help develop a federal or state program.
Type: DISCRETE
Work item: one program proposal or design component
Start: program need or design assignment identified
End: proposal or design component submitted for review
Checked by: agency leadership or program team

[9334a]
Occupation: Interpreters and Translators
Task statement: Adapt translations to students' cognitive and grade levels, collaborating with educational team members as necessary.
Part: Adapt a translated school material to the cognitive and grade level of students, collaborating with the education team.
Type: DISCRETE
Work item: one school material adapted to student level
Start: translated material and target level identified
End: adapted material approved by the education team
Checked by: teacher or education team

[3785b]
Occupation: Lawyers
Task statement: Prepare legal briefs and opinions, and file appeals in state and federal courts of appeal.
Part: Prepare a legal opinion on a specified question.
Type: DISCRETE
Work item: one legal opinion
Start: opinion assignment and relevant facts received
End: opinion finalized and delivered
Checked by: client or supervising lawyer

[1258b]
Occupation: Credit Analysts
Task statement: Consult with customers to resolve complaints and verify financial and credit transactions.
Part: Check records and follow up in writing to settle a complaint or verify a transaction after the contact.
Type: DISCRETE
Work item: one complaint or verification followed up and closed
Start: case needing records check after contact
End: outcome communicated and case closed
Checked by: credit manager

[20363d]
Occupation: Tax Preparers
Task statement: Answer questions and provide future tax planning to clients.
Part: Develop written future tax-planning recommendations for a client.
Type: DISCRETE
Work item: One set of written tax-planning recommendations
Start: Client's planning circumstances and objectives are available
End: Recommendations are prepared and sent to the client
Checked by: Client and tax practice reviewer

[10645a]
Occupation: Heavy and Tractor-Trailer Truck Drivers
Task statement: Read and interpret maps to determine vehicle routes.
Part: Read maps or route atlases to work out the route for a delivery.
Type: DISCRETE
Work item: one trip route determined
Start: delivery assignment received
End: route chosen and ready to drive
Checked by: the driver and dispatcher (delivery on time)

