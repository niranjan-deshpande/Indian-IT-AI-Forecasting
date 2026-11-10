You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Code each ITEM independently, in the order given; do not go
back and adjust earlier answers to make them consistent with later ones.

Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/more_v1/s1/batch21.json
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
[21455b]
Occupation: Compliance Officers
Task statement: Visit establishments to verify that valid licenses or permits are displayed and that licensing standards are being upheld.
Part: Write up the result of an inspection visit.
Type: DISCRETE
Work item: one inspection record
Start: visit ends
End: inspection result recorded and filed
Checked by: supervisor

[1822c]
Occupation: Pharmacists
Task statement: Manage pharmacy operations, hiring or supervising staff, performing administrative duties, or buying or selling non-pharmaceutical merchandise.
Part: Purchase non-pharmaceutical merchandise for the pharmacy.
Type: DISCRETE
Work item: one non-pharmaceutical merchandise order
Start: merchandise need identified
End: order submitted to the supplier
Checked by: supplier and pharmacy management

[21474b]
Occupation: Project Management Specialists
Task statement: Prepare and submit budget estimates, progress reports, or cost tracking reports.
Part: Prepare and submit a progress report.
Type: DISCRETE
Work item: one progress report
Start: reporting period ends
End: report submitted
Checked by: project manager; client

[979a]
Occupation: Computer and Information Systems Managers
Task statement: Evaluate data processing proposals to assess project feasibility and requirements.
Part: Evaluate a data processing proposal for feasibility and requirements.
Type: DISCRETE
Work item: one proposal evaluated for feasibility
Start: proposal received
End: feasibility assessment delivered
Checked by: CIO, sponsoring manager

[2472a]
Occupation: Bill and Account Collectors
Task statement: Receive payments and post amounts paid to customer accounts.
Part: Take a payment and post it to the account while the customer is on the phone or at the desk.
Type: LIVE_SERVICE
Work item: one payment taken and posted during a contact
Start: customer agrees to pay
End: payment posted and confirmed to the customer
Checked by: the customer, accounting

[778a]
Occupation: Medical Secretaries and Administrative Assistants
Task statement: Receive and route messages or documents, such as laboratory results, to appropriate staff.
Part: Receive messages and documents such as lab results and route them to the right staff.
Type: DISCRETE
Work item: one message or document received and routed
Start: message or result arrives
End: delivered to the responsible staff member
Checked by: clinician or staff member receiving it

[20276b]
Occupation: Shipping, Receiving, and Inventory Clerks
Task statement: Examine shipment contents and compare with records, such as manifests, invoices, or orders, to verify accuracy.
Part: Compare the count and condition with the manifest, invoice or order and sign off or flag discrepancies.
Type: DISCRETE
Work item: one shipment verified against its manifest, invoice or order
Start: contents counted and inspected
End: receipt confirmed or discrepancies reported
Checked by: purchasing, accounting, supervisor

[20405a]
Occupation: Pharmacists
Task statement: Contact insurance companies to resolve billing issues.
Part: Contact an insurer to resolve a billing issue such as a rejected claim.
Type: DISCRETE
Work item: one billing issue resolved with an insurer
Start: claim rejection or billing problem identified
End: claim resolved or payment confirmed
Checked by: pharmacy manager, patient, insurer

[20492a]
Occupation: Civil Engineers
Task statement: Analyze survey reports, maps, drawings, blueprints, aerial photography, or other topographical or geologic data.
Part: Analyze survey reports, maps, drawings and aerial or geologic data to characterize a site for design.
Type: DISCRETE
Work item: one site data analysis memo or base map
Start: survey and topographic data received
End: analysis delivered to the design team
Checked by: design engineers who rely on it; senior engineer

[2458a]
Occupation: Real Estate Sales Agents
Task statement: Advise clients on market conditions, prices, mortgages, legal requirements, and related matters.
Part: Advise a client live about market conditions and transaction matters.
Type: LIVE_SERVICE
Work item: one live client advisory consultation
Start: client raises a market or transaction matter
End: advice explained and discussed with the client
Checked by: client

[1812c]
Occupation: Pharmacists
Task statement: Maintain records, such as pharmacy files, patient profiles, charge system files, inventories, control records for radioactive nuclei, or registries of poisons, narcotics, or controlled drugs.
Part: Maintain pharmacy charge or billing records.
Type: DISCRETE
Work item: one charge or billing record updated
Start: charge information or correction received
End: record updated and saved
Checked by: pharmacy billing staff and auditors

[1820a]
Occupation: Pharmacists
Task statement: Plan, implement, or maintain procedures for mixing, packaging, or labeling pharmaceuticals, according to policy and legal requirements, to ensure quality, security, and proper disposal.
Part: Plan, put in place, and update procedures for mixing, packaging, labeling, security, and disposal of pharmaceuticals.
Type: DISCRETE
Work item: one written procedure created or revised
Start: need for a procedure or change identified
End: procedure approved and issued to staff
Checked by: pharmacy manager, inspectors

[19811a]
Occupation: Public Relations Specialists
Task statement: Develop plans or materials to communicate organizational activities that are beneficial to the environment, public safety, or other important social issues.
Part: Develop a plan for communicating organizational activities benefiting the environment, public safety, or other social issues.
Type: DISCRETE
Work item: one social-issue communication plan
Start: organizational activity and communication objective are identified
End: plan is submitted for review or approval
Checked by: communications management and the relevant program team

[3405a]
Occupation: Budget Analysts
Task statement: Compile and analyze accounting records and other data to determine the financial resources required to implement a program.
Part: Compile and analyze accounting records to determine the financial resources a program needs.
Type: DISCRETE
Work item: one program resource estimate
Start: program defined
End: estimate delivered
Checked by: program manager, finance

[2281a]
Occupation: Waiters and Waitresses
Task statement: Prepare checks that itemize and total meal costs and sales taxes.
Part: Prepare a check itemising a table's meal and adding tax.
Type: DISCRETE
Work item: one check prepared
Start: table asks for the bill or meal ends
End: itemised check printed and brought to the table
Checked by: customer, and manager at cash-out

[676a]
Occupation: First-Line Supervisors of Retail Sales Workers
Task statement: Establish credit policies and operating procedures.
Part: Establish credit policies and operating procedures.
Type: DISCRETE
Work item: one credit policy or procedure issued
Start: need for or change to credit rules identified
End: policy communicated to staff
Checked by: store or district manager; finance

[23105a]
Occupation: Fast Food and Counter Workers
Task statement: Serve food, beverages, or desserts to customers in such settings as take-out counters of restaurants or lunchrooms, business or industrial establishments, hotel rooms, and cars.
Part: Serve food, beverages, or desserts to a customer.
Type: LIVE_SERVICE
Work item: one customer order served
Start: food or beverage is ready for handoff
End: order is handed to the customer
Checked by: customer and shift supervisor

[18765a]
Occupation: Cashiers
Task statement: Assist customers by providing information and resolving their complaints.
Part: Provide information requested by a customer.
Type: LIVE_SERVICE
Work item: one customer information request answered
Start: the customer requests information
End: the information is provided or the customer is directed to someone who can help
Checked by: the customer and cashier's supervisor

[827a]
Occupation: Office Clerks, General
Task statement: Answer telephones, direct calls, and take messages.
Part: Answer an incoming call, direct it to the right person, or take a message.
Type: LIVE_SERVICE
Work item: one incoming call answered, transferred or message taken
Start: phone rings and clerk picks up
End: call transferred or message written and caller ends the call
Checked by: the caller and the person receiving the call or message

[1813b]
Occupation: Pharmacists
Task statement: Provide specialized services to help patients manage conditions, such as diabetes, asthma, smoking cessation, or high blood pressure.
Part: Document the consult and follow-up plan.
Type: DISCRETE
Work item: one patient management consult documented
Start: consult ends
End: note and follow-up plan recorded
Checked by: prescriber, pharmacy manager, insurer

[967b]
Occupation: Computer and Information Systems Managers
Task statement: Consult with users, management, vendors, and technicians to assess computing needs and system requirements.
Part: Write up assessed computing needs and system requirements from the consultations.
Type: DISCRETE
Work item: one needs assessment / system requirements document
Start: consultations completed for a request
End: requirements document issued to management and the project team
Checked by: requesting manager, project lead

[2481b]
Occupation: Bill and Account Collectors
Task statement: Arrange for debt repayment or establish repayment schedules, based on customers' financial situations.
Part: Establish or update a repayment schedule from written customer information or an approved request.
Type: DISCRETE
Work item: one repayment schedule established or updated outside a contact
Start: written repayment information or an approved request is received
End: schedule is entered and confirmation is sent as required
Checked by: customer and collections supervisor

[19611a]
Occupation: Civil Engineers
Task statement: Identify environmental risks and develop risk management strategies for civil engineering projects.
Part: Identify environmental risks of a civil engineering project and develop risk management strategies.
Type: DISCRETE
Work item: one environmental risk assessment and management plan
Start: project scope and site information available
End: assessment and mitigation strategies issued
Checked by: project manager, client, permitting agency

[23063b]
Occupation: Police and Sheriff's Patrol Officers
Task statement: Photograph or draw diagrams of crime or accident scenes and interview principals and eyewitnesses.
Part: Interview principals and eyewitnesses and record their statements.
Type: DISCRETE
Work item: one witness or principal statement taken
Start: officer begins questioning the person
End: statement recorded
Checked by: supervisor, detective or prosecutor

[147a]
Occupation: Civil Engineers
Task statement: Compute load and grade requirements, water flow rates, or material stress factors to determine design specifications.
Part: Compute load, grade, flow-rate or material-stress requirements and record the resulting design specifications.
Type: DISCRETE
Work item: one design calculation package for a structure or system component
Start: design criteria and site data for the component in hand
End: calculations checked and specifications issued to the design team
Checked by: senior or reviewing engineer; the licensed engineer who stamps the design

[1786a]
Occupation: Editors
Task statement: Read, evaluate and edit manuscripts or other materials submitted for publication, and confer with authors regarding changes in content, style or organization, or publication.
Part: Read, evaluate and edit a submitted manuscript.
Type: DISCRETE
Work item: one manuscript evaluated and edited
Start: manuscript received
End: edited manuscript or evaluation returned
Checked by: author, publisher

[21467a]
Occupation: Project Management Specialists
Task statement: Identify project needs such as resources, staff, or finances by reviewing project objectives and schedules.
Part: Identify the resources, staff and funding a project needs from its objectives and schedule.
Type: DISCRETE
Work item: one project needs assessment
Start: objectives and schedule reviewed
End: needs list sent for approval
Checked by: project sponsor or finance

[826a]
Occupation: Office Clerks, General
Task statement: Communicate with customers, employees, and other individuals to answer questions, disseminate or explain information, take orders, and address complaints.
Part: Talk with a customer or employee in person or by phone to answer a question, take an order, or handle a complaint.
Type: LIVE_SERVICE
Work item: one customer or employee enquiry, order or complaint handled in a live contact
Start: person asks a question or raises an issue
End: answer given, order taken or complaint logged and person satisfied or referred
Checked by: the customer or employee; office manager for complaints

[50a]
Occupation: Medical and Health Services Managers
Task statement: Develop and implement organizational policies and procedures for the facility or medical unit.
Part: Develop or revise an organizational policy or procedure.
Type: DISCRETE
Work item: one policy or procedure document
Start: need for a new or revised policy or procedure is identified
End: document is submitted for approval
Checked by: facility leadership and compliance staff

[1275a]
Occupation: Computer Programmers
Task statement: Investigate whether networks, workstations, the central processing unit of the system, or peripheral equipment are responding to a program's instructions.
Part: Investigate whether networks, workstations, the CPU or peripherals respond correctly to a program's instructions.
Type: DISCRETE
Work item: one investigation of a program-to-equipment problem
Start: suspected equipment non-response reported or noticed
End: cause identified and reported or fixed
Checked by: the system administrator or requester

[6537a]
Occupation: Elementary School Teachers, Except Special Education
Task statement: Prepare materials and classrooms for class activities.
Part: Prepare the materials for a class activity: copy, cut, collate and assemble handouts and supplies.
Type: DISCRETE
Work item: one lesson's set of materials prepared
Start: lesson activity chosen and needs identified
End: materials copied, assembled and ready at the point of use
Checked by: the teacher, and the principal on request

[18563a]
Occupation: Payroll and Timekeeping Clerks
Task statement: Keep track of leave time, such as vacation, personal, and sick leave, for employees.
Part: Record an employee's leave taken or requested against their balance.
Type: DISCRETE
Work item: one leave entry recorded
Start: leave request or report received
End: leave entered and balance updated
Checked by: payroll supervisor, employee

[21469a]
Occupation: Project Management Specialists
Task statement: Monitor costs incurred by project staff to identify budget issues.
Part: Review costs incurred by project staff against the budget to spot budget issues.
Type: DISCRETE
Work item: one periodic cost review against budget
Start: period's cost data available
End: budget issues flagged to manager
Checked by: project manager; finance

