You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Code each ITEM independently, in the order given; do not go
back and adjust earlier answers to make them consistent with later ones.

Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/more_v1/s2/batch10.json
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
[249b]
Occupation: Child, Family, and School Social Workers
Task statement: Evaluate personal characteristics and home conditions of foster home or adoption applicants.
Part: Interview foster or adoption applicants about their personal characteristics and circumstances.
Type: LIVE_SERVICE
Work item: one foster or adoption applicant assessment interview
Start: applicant interview begins
End: relevant circumstances and assessment next steps are discussed
Checked by: applicants and assessing social worker

[19607a]
Occupation: Civil Engineers
Task statement: Design energy-efficient or environmentally sound civil structures.
Part: Design a civil structure to be energy-efficient or environmentally sound.
Type: DISCRETE
Work item: one design package for a structure (drawings and specifications)
Start: project requirements and environmental targets set
End: design package issued for review or construction
Checked by: client, reviewing engineer, code official

[962b]
Occupation: Marketing Managers
Task statement: Advise business or other groups on local, national, or international factors affecting the buying or selling of products or services.
Part: Write advice for a group on factors affecting the buying or selling of products.
Type: DISCRETE
Work item: one advisory note on market factors
Start: request from the group received
End: note delivered
Checked by: the requesting group

[20738a]
Occupation: Mechanical Engineers
Task statement: Estimate costs or submit bids for engineering, construction, or extraction projects.
Part: Estimate costs and submit a bid for an engineering, construction or extraction project.
Type: DISCRETE
Work item: one cost estimate or bid
Start: request for bid received
End: bid submitted
Checked by: manager, customer

[57a]
Occupation: Medical and Health Services Managers
Task statement: Prepare activity reports to inform management of the status and implementation plans of programs, services, and quality initiatives.
Part: Prepare an activity report on program, service and quality initiative status.
Type: DISCRETE
Work item: one activity report
Start: reporting period data gathered
End: report sent to management
Checked by: senior management

[2472a]
Occupation: Bill and Account Collectors
Task statement: Receive payments and post amounts paid to customer accounts.
Part: Take a payment and post it to the account while the customer is on the phone or at the desk.
Type: LIVE_SERVICE
Work item: one payment taken and posted during a contact
Start: customer agrees to pay
End: payment posted and confirmed to the customer
Checked by: the customer, accounting

[2400a]
Occupation: Cashiers
Task statement: Receive payment by cash, check, credit cards, vouchers, or automatic debits.
Part: Take a customer's payment by cash, check, card, voucher or automatic debit.
Type: LIVE_SERVICE
Work item: one payment taken at the register
Start: total announced and customer offers payment
End: payment accepted and recorded
Checked by: the customer; end-of-shift drawer count

[2037a]
Occupation: Medical Assistants
Task statement: Contact medical facilities or departments to schedule patients for tests or admission.
Part: Contact a hospital, lab or imaging facility to schedule a patient's test or admission.
Type: DISCRETE
Work item: one test or admission scheduled with an outside facility
Start: physician orders a test or admission
End: booking confirmed and patient informed
Checked by: the physician and the patient

[7380a]
Occupation: Operations Research Analysts
Task statement: Perform validation and testing of models to ensure adequacy, and reformulate models, as necessary.
Part: Validate and test a model and reformulate it if needed.
Type: DISCRETE
Work item: one model validation, with any reformulation
Start: model ready for testing
End: model validated or revised and accepted
Checked by: senior analyst, project lead

[20474b]
Occupation: Training and Development Specialists
Task statement: Design, plan, organize, or direct orientation and training programs for employees or customers.
Part: Organize the resources and arrangements for an orientation or training program.
Type: DISCRETE
Work item: one program session or cohort's delivery arrangements
Start: approved program and delivery requirements are available
End: resources and arrangements are confirmed and communicated
Checked by: training coordinator, instructors, and participants

[1280a]
Occupation: Computer Programmers
Task statement: Collaborate with computer manufacturers and other users to develop new programming methods.
Part: Develop a new programming method in collaboration with manufacturers and other users.
Type: DISCRETE
Work item: one proposed programming method or method improvement
Start: a need or opportunity for a programming method is identified
End: the proposed method is developed and shared with collaborators
Checked by: collaborating programmers, users, or manufacturers

[5322a]
Occupation: Information Security Analysts
Task statement: Document computer security and emergency measures policies, procedures, and tests.
Part: Document security and emergency policies, procedures and tests.
Type: DISCRETE
Work item: one policy, procedure or test record document
Start: policy or test needs documenting
End: document approved and filed
Checked by: security manager or auditor

[21450a]
Occupation: Compliance Officers
Task statement: Report law or regulation violations to appropriate boards or agencies.
Part: Report a violation of law or regulation to the appropriate board or agency.
Type: DISCRETE
Work item: one violation referral
Start: violation documented
End: referral accepted by the board or agency
Checked by: receiving board or agency

[6537a]
Occupation: Elementary School Teachers, Except Special Education
Task statement: Prepare materials and classrooms for class activities.
Part: Prepare the materials for a class activity: copy, cut, collate and assemble handouts and supplies.
Type: DISCRETE
Work item: one lesson's set of materials prepared
Start: lesson activity chosen and needs identified
End: materials copied, assembled and ready at the point of use
Checked by: the teacher, and the principal on request

[951a]
Occupation: Marketing Managers
Task statement: Identify, develop, or evaluate marketing strategy, based on knowledge of establishment objectives, market characteristics, and cost and markup factors.
Part: Develop or evaluate a marketing strategy using company objectives, market characteristics and cost and markup factors.
Type: DISCRETE
Work item: one marketing strategy or strategy evaluation
Start: planning cycle or strategic need begins
End: strategy presented and approved
Checked by: senior management

[19629b]
Occupation: Mechanical Engineers
Task statement: Direct the installation, operation, maintenance, or repair of renewable energy equipment, such as heating, ventilating, and air conditioning (HVAC) or water systems.
Part: Commission equipment and document that it performs to specification.
Type: DISCRETE
Work item: one commissioning record for a system
Start: installation complete
End: performance verified and record issued
Checked by: building owner, inspector

[1268a]
Occupation: Computer Programmers
Task statement: Conduct trial runs of programs and software applications to be sure they will produce the desired information and that the instructions are correct.
Part: Run a program or application on trial data and check that its output and instructions are correct.
Type: DISCRETE
Work item: one program test cycle with results recorded
Start: program or change ready for testing
End: test results recorded and discrepancies reported or cleared
Checked by: the lead developer or QA, who accept the program for release

[2449a]
Occupation: Real Estate Sales Agents
Task statement: Generate lists of properties that are compatible with buyers' needs and financial resources.
Part: Generate lists of properties matching a buyer's needs and finances.
Type: DISCRETE
Work item: one property shortlist for a buyer
Start: buyer criteria and budget known
End: shortlist sent to buyer
Checked by: the buyer

[714a]
Occupation: Retail Salespersons
Task statement: Estimate and quote trade-in allowances.
Part: Inspect a trade-in item and quote an allowance to the customer.
Type: LIVE_SERVICE
Work item: one trade-in allowance quoted
Start: customer offers an item for trade-in
End: allowance quoted and accepted or declined
Checked by: the customer; sales manager

[2469a]
Occupation: Real Estate Sales Agents
Task statement: Secure construction or purchase financing with own firm or mortgage company.
Part: Secure construction or purchase financing for a client through own firm or a mortgage company.
Type: DISCRETE
Work item: one financing application submitted and followed to a decision
Start: client chooses a financing option
End: financing approved or declined
Checked by: lender; the client

[1275a]
Occupation: Computer Programmers
Task statement: Investigate whether networks, workstations, the central processing unit of the system, or peripheral equipment are responding to a program's instructions.
Part: Investigate whether networks, workstations, the CPU or peripherals respond correctly to a program's instructions.
Type: DISCRETE
Work item: one investigation of a program-to-equipment problem
Start: suspected equipment non-response reported or noticed
End: cause identified and reported or fixed
Checked by: the system administrator or requester

[20705a]
Occupation: General and Operations Managers
Task statement: Perform personnel functions, such as selection, training, or evaluation.
Part: Select staff by reviewing applicants and making hiring decisions.
Type: DISCRETE
Work item: one hiring decision for an opening
Start: opening approved
End: candidate selected and offer made
Checked by: HR; senior executive

[5316a]
Occupation: Information Security Analysts
Task statement: Monitor current reports of computer viruses to determine when to update virus protection systems.
Part: Review current virus and threat reports and decide when to update virus protection.
Type: DISCRETE
Work item: one threat-report review ending in an update decision
Start: new threat report or advisory received
End: update decision recorded or communicated
Checked by: security manager and the IT team

[48a]
Occupation: Medical and Health Services Managers
Task statement: Direct or conduct recruitment, hiring, and training of personnel.
Part: Direct or conduct recruitment and hiring of personnel.
Type: DISCRETE
Work item: one vacancy filled
Start: vacancy approved
End: offer accepted and hire recorded
Checked by: HR, senior administration

[3399a]
Occupation: Budget Analysts
Task statement: Summarize budgets and submit recommendations for the approval or disapproval of funds requests.
Part: Summarize a budget and recommend approval or disapproval of a funds request.
Type: DISCRETE
Work item: one funds request recommendation
Start: request received
End: recommendation submitted
Checked by: approving authority

[9426c]
Occupation: Medical Transcriptionists
Task statement: Receive patients, schedule appointments, and maintain patient records.
Part: Schedule or change an appointment from a written request.
Type: DISCRETE
Work item: one written appointment request processed
Start: written scheduling request received
End: appointment entered or changed and response sent
Checked by: patient and clinical scheduling staff

[21823a]
Occupation: Data Scientists
Task statement: Analyze, manipulate, or process large sets of data using statistical software.
Part: Run an analysis on a large dataset using statistical software and summarise the results.
Type: DISCRETE
Work item: one analysis of a dataset answering a defined question
Start: question and data access in hand
End: results (tables, numbers, short summary) delivered to the requester
Checked by: requesting manager or stakeholder; reviewing colleague

[9731a]
Occupation: First-Line Supervisors of Office and Administrative Support Workers
Task statement: Plan layouts of stockrooms, warehouses, or other storage areas, considering turnover, size, weight, or related factors pertaining to items stored.
Part: Plan the layout of a stockroom or storage area given turnover, size and weight of items.
Type: DISCRETE
Work item: one storage layout plan
Start: layout need or change identified
End: plan approved and given to those who set it up
Checked by: manager, storage staff

[20737a]
Occupation: Mechanical Engineers
Task statement: Assist drafters in developing the structural design of products, using drafting tools or computer-assisted drafting equipment or software.
Part: Assist drafters with the structural design of products by providing sketches, mark-ups and CAD input.
Type: DISCRETE
Work item: one drawing input package for a drafter
Start: design concept ready for drafting
End: drawing completed and approved
Checked by: drafter, design lead

[20708a]
Occupation: General and Operations Managers
Task statement: Manage the movement of goods into and out of production facilities to ensure efficiency, effectiveness, or sustainability of operations.
Part: Coordinate a plan for goods moving into or out of a production facility.
Type: DISCRETE
Work item: one goods-movement plan or schedule
Start: production, inventory, and shipment needs identified
End: movement arrangements communicated to responsible teams
Checked by: production, warehouse, and logistics staff

[783a]
Occupation: Medical Secretaries and Administrative Assistants
Task statement: Transmit correspondence or medical records by mail, e-mail, or fax.
Part: Transmit correspondence or medical records electronically or by fax.
Type: DISCRETE
Work item: one correspondence or medical-records package transmitted
Start: document and authorized transmission request received
End: package sent and transmission recorded or confirmed as required
Checked by: recipient and sending office

[2453b]
Occupation: Real Estate Sales Agents
Task statement: Answer clients' questions regarding construction work, financing, maintenance, repairs, and appraisals.
Part: Answer a client's emailed or texted questions on the same topics.
Type: DISCRETE
Work item: one written client question answered
Start: message received
End: reply sent
Checked by: the client

[1431b]
Occupation: Mechanical Engineers
Task statement: Design test control apparatus or equipment or develop procedures for testing products.
Part: Develop procedures for testing products.
Type: DISCRETE
Work item: one product test procedure
Start: product test requirement defined
End: procedure approved
Checked by: quality staff, test technicians

[10780a]
Occupation: Laborers and Freight, Stock, and Material Movers, Hand
Task statement: Record numbers of units handled or moved, using daily production sheets or work tickets.
Part: Record the number of units handled or moved on the daily production sheet or work ticket.
Type: DISCRETE
Work item: one daily production sheet or work ticket completed
Start: shift or job finished, counts of units known
End: sheet or ticket filled in and handed to the supervisor
Checked by: supervisor, and payroll or production control

