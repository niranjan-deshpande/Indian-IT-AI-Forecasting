You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Code each ITEM independently, in the order given; do not go
back and adjust earlier answers to make them consistent with later ones.

Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/more_v1/s1/batch11.json
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
[1274a]
Occupation: Computer Programmers
Task statement: Write or contribute to instructions or manuals to guide end users.
Part: Write or contribute to instructions or a manual for end users.
Type: DISCRETE
Work item: one user guide or manual section
Start: program ready to be documented for users
End: guide reviewed and published
Checked by: technical lead and end users

[21448a]
Occupation: Compliance Officers
Task statement: Advise licensees or other individuals or groups concerning licensing, permit, or passport regulations.
Part: Advise a licensee or applicant on regulations while they are on the phone or at the desk.
Type: LIVE_SERVICE
Work item: one licensing inquiry answered during a call or visit
Start: person asks about regulations
End: person has the answer and the contact ends
Checked by: the inquirer, and supervisor on review

[789a]
Occupation: Medical Secretaries and Administrative Assistants
Task statement: Prepare correspondence or assist physicians or medical scientists with preparation of reports, speeches, articles, or conference proceedings.
Part: Prepare correspondence for the practice or physician.
Type: DISCRETE
Work item: one letter prepared for signature or sending
Start: request or instructions for the letter
End: letter signed and sent
Checked by: physician, recipient

[710a]
Occupation: Retail Salespersons
Task statement: Help customers try on or fit merchandise.
Part: Help a customer try on or fit merchandise.
Type: LIVE_SERVICE
Work item: one customer helped to try on or fit items
Start: customer asks to try items
End: customer decides on fit
Checked by: the customer

[528d]
Occupation: Licensed Practical and Licensed Vocational Nurses
Task statement: Make appointments, keep records, or perform other clerical duties in doctors' offices or clinics.
Part: Process other routine office or clinic clerical items, such as forms.
Type: DISCRETE
Work item: one routine clerical item processed
Start: form or other clerical item is received
End: the item is completed and filed or forwarded
Checked by: clinic office staff or the recipient

[20477b]
Occupation: Training and Development Specialists
Task statement: Supervise, evaluate, or refer instructors to skill development classes.
Part: Evaluate an instructor and refer them to skill development classes.
Type: DISCRETE
Work item: one instructor evaluation with any development referral
Start: instructor observed or review due
End: evaluation delivered and referral made
Checked by: the instructor and training manager

[18564a]
Occupation: Payroll and Timekeeping Clerks
Task statement: Conduct verifications of employment.
Part: Verify employment for an authorized requester during a live contact.
Type: LIVE_SERVICE
Work item: one employment verification provided during a live contact
Start: authorized requester asks for employment verification
End: permitted information is provided or the request is referred during the contact
Checked by: authorized requester

[9728a]
Occupation: First-Line Supervisors of Office and Administrative Support Workers
Task statement: Arrange for necessary maintenance or repair work.
Part: Arrange for maintenance or repair work.
Type: DISCRETE
Work item: one maintenance or repair job arranged
Start: fault reported
End: repair scheduled with vendor or facilities and confirmed done
Checked by: staff using the equipment, facilities

[727a]
Occupation: Insurance Sales Agents
Task statement: Confer with clients to obtain and provide information when claims are made on a policy.
Part: Talk with a client who is making a claim to collect and give information.
Type: LIVE_SERVICE
Work item: one claim contact with a client
Start: client reports or asks about a claim
End: information collected and next steps explained
Checked by: the client, and the insurer's claims team

[300a]
Occupation: Graphic Designers
Task statement: Determine size and arrangement of illustrative material and copy, and select style and size of type.
Part: Decide the size and arrangement of images and copy on a layout and choose the typeface and type size.
Type: DISCRETE
Work item: one layout with image/copy arrangement and type specified
Start: copy and illustrative material available for the job
End: layout with sizes, arrangement and type fixed and passed on for review
Checked by: art director or client

[1269a]
Occupation: Computer Programmers
Task statement: Compile and write documentation of program development and subsequent revisions, inserting comments in the coded instructions so others can understand the program.
Part: Write documentation of a program's development and each revision, and add comments in the code.
Type: DISCRETE
Work item: one program's documentation (or revision note) with code comments
Start: program or revision completed
End: documentation and comments finished and filed or committed
Checked by: other programmers who maintain the code; the lead developer

[9423a]
Occupation: Medical Transcriptionists
Task statement: Set up and maintain medical files and databases, including records such as x-ray, lab, and procedure reports, medical histories, diagnostic workups, admission and discharge summaries, and clinical resumes.
Part: Set up a medical files database using the workplace's approved system.
Type: DISCRETE
Work item: one medical records database or collection set up
Start: request and requirements for a record collection received
End: collection configured and made available to authorized staff
Checked by: medical records supervisor or system users

[242a]
Occupation: Child, Family, and School Social Workers
Task statement: Collect supplementary information needed to assist client, such as employment records, medical records, or school reports.
Part: Collect employment, medical, school or other records needed to help a client.
Type: DISCRETE
Work item: one set of supplementary records obtained for a case
Start: need for outside records identified
End: records received and filed in the case
Checked by: the caseworker and supervisor

[5319a]
Occupation: Information Security Analysts
Task statement: Monitor use of data files and regulate access to safeguard information in computer files.
Part: Review usage of data files and report unusual access.
Type: DISCRETE
Work item: one access log review with findings
Start: log period or alert selected for review
End: findings reported or cleared
Checked by: security manager or auditor

[787c]
Occupation: Medical Secretaries and Administrative Assistants
Task statement: Perform bookkeeping duties, such as credits or collections, preparing and sending financial statements or bills, and keeping financial records.
Part: Post payments and keep the financial records.
Type: DISCRETE
Work item: one batch of payments and entries posted
Start: payments and charges collected
End: posted and balanced in the records
Checked by: practice manager, accountant

[23062a]
Occupation: Police and Sheriff's Patrol Officers
Task statement: Verify that the proper legal charges have been made against law offenders.
Part: Check that the charges made against an offender are the right ones.
Type: DISCRETE
Work item: one set of charges verified for an offender
Start: arrest made or charges drafted
End: charges confirmed or corrected on the record
Checked by: supervisor or prosecutor

[9713a]
Occupation: First-Line Supervisors of Office and Administrative Support Workers
Task statement: Prepare and issue work schedules, deadlines, and duty assignments for office or administrative staff.
Part: Prepare and issue the work schedule for staff.
Type: DISCRETE
Work item: one staff work schedule prepared and issued
Start: coverage needs and availability known
End: schedule issued to staff
Checked by: staff, department manager

[834b]
Occupation: Office Clerks, General
Task statement: Review files, records, and other documents to obtain information to respond to requests.
Part: Review files and records to obtain information for a queued or written request.
Type: DISCRETE
Work item: one request's records lookup completed
Start: request for information received
End: relevant information supplied or lookup result recorded
Checked by: requester or colleague preparing the response

[23067b]
Occupation: Police and Sheriff's Patrol Officers
Task statement: Investigate traffic accidents and other accidents to determine causes and to determine if a crime has been committed.
Part: Write up the accident findings in a crash report.
Type: DISCRETE
Work item: one crash report
Start: scene work finished
End: report submitted and approved
Checked by: supervisor, insurers, courts

[20161a]
Occupation: Team Assemblers
Task statement: Complete production reports to communicate team production level to management.
Part: Complete production reports showing the team's output for management.
Type: DISCRETE
Work item: one production report
Start: end of shift or reporting period
End: report submitted to management
Checked by: production supervisor or manager

[20051a]
Occupation: Economists
Task statement: Provide litigation support, such as writing reports for expert testimony or testifying as an expert witness.
Part: Write an expert report for litigation.
Type: DISCRETE
Work item: one expert report
Start: engagement and data received
End: report served
Checked by: retaining attorney, opposing experts, court

[51a]
Occupation: Medical and Health Services Managers
Task statement: Conduct and administer fiscal operations, including accounting, planning budgets, authorizing expenditures, establishing rates for services, and coordinating financial reporting.
Part: Conduct or oversee accounting for facility operations.
Type: DISCRETE
Work item: one accounting-period reconciliation
Start: period transactions and account records are available
End: reconciliation is reviewed and filed or forwarded
Checked by: finance staff and auditors

[2277b]
Occupation: Waiters and Waitresses
Task statement: Write patrons' food orders on order slips, memorize orders, or enter orders into computers for transmittal to kitchen staff.
Part: Write or enter a patron's food order for the kitchen after taking it at the table.
Type: DISCRETE
Work item: one table's food order transmitted to the kitchen
Start: server leaves the table with the order
End: order slip or computer order is submitted to the kitchen
Checked by: kitchen staff

[19504a]
Occupation: Marketing Managers
Task statement: Integrate environmental information into product or company marketing strategies, policies, or activities.
Part: Integrate environmental information into a product or company marketing strategy, policy or activity.
Type: DISCRETE
Work item: one marketing strategy or activity revised with environmental content
Start: environmental information gathered
End: revised strategy or plan approved
Checked by: marketing director

[1775b]
Occupation: Public Relations Specialists
Task statement: Plan or conduct market or public opinion research to test products or determine potential for product success, communicating results to client or management.
Part: Conduct market or public opinion research and communicate its results.
Type: DISCRETE
Work item: one research findings report
Start: research question and approach are established
End: findings are analyzed and communicated to the client or management
Checked by: client or management

[23125a]
Occupation: Fast Food and Counter Workers
Task statement: Plan, prepare, and deliver meals to individuals with special dietary needs.
Part: Plan a meal for an individual with special dietary needs.
Type: DISCRETE
Work item: one special-diet meal plan
Start: individual's dietary requirements and meal request are available
End: meal selection or preparation instructions are established
Checked by: food preparer, supervisor, or individual receiving the meal

[111b]
Occupation: Training and Development Specialists
Task statement: Refer trainees to employer relations representatives, to locations offering job placement assistance, or to appropriate social services agencies, if warranted.
Part: Prepare and send a trainee referral after the live contact.
Type: DISCRETE
Work item: one written trainee referral
Start: referral need and relevant trainee information are identified
End: referral information is sent to the trainee or receiving resource
Checked by: trainee and receiving representative or agency

[694a]
Occupation: Retail Salespersons
Task statement: Greet customers and ascertain what each customer wants or needs.
Part: Greet a customer and find out what they want or need.
Type: LIVE_SERVICE
Work item: one customer greeted and needs established
Start: customer enters or approaches
End: customer's need identified and help begins
Checked by: the customer; floor manager

[2135a]
Occupation: Security Guards
Task statement: Call police or fire departments in cases of emergency, such as fire or presence of unauthorized persons.
Part: Call the police or fire department to report an emergency or unauthorised person.
Type: DISCRETE
Work item: one emergency call to police or fire dispatch
Start: guard decides the situation needs outside help
End: dispatcher confirms responders are sent
Checked by: emergency dispatcher, and the supervisor who reviews the incident

[23951a]
Occupation: Public Relations Specialists
Task statement: Post and update content on the company's Web site and social media outlets.
Part: Post or update content on the website or social media.
Type: DISCRETE
Work item: one post or page update published
Start: content ready for posting
End: content live on the site or channel
Checked by: communications manager and the audience

[23972a]
Occupation: Graphic Designers
Task statement: Write or edit copy for clients.
Part: Write or edit copy for a client's design job.
Type: DISCRETE
Work item: one piece of copy written or edited for a client
Start: copy need or draft text received
End: final copy delivered to the client
Checked by: client

[9719a]
Occupation: First-Line Supervisors of Office and Administrative Support Workers
Task statement: Develop or update procedures, policies, or standards.
Part: Write or revise a procedure, policy or standard.
Type: DISCRETE
Work item: one procedure, policy or standard drafted or updated
Start: need for a new or changed procedure identified
End: document approved and issued
Checked by: manager

[23894a]
Occupation: Stockers and Order Fillers
Task statement: Keep records on the use or damage of stock or stock-handling equipment.
Part: Update records on the use or damage of stock or stock-handling equipment.
Type: DISCRETE
Work item: one batch of use or damage log entries
Start: use or damage events to log
End: entries written in the log or system
Checked by: supervisor, inventory control, maintenance

[98b]
Occupation: Training and Development Specialists
Task statement: Monitor, evaluate, or record training activities or program effectiveness.
Part: Evaluate how effective a training program has been and report the result.
Type: DISCRETE
Work item: one training program effectiveness evaluation
Start: evaluation data (feedback forms, test results, performance measures) collected for a program
End: evaluation findings delivered to training management
Checked by: training manager or program sponsor

