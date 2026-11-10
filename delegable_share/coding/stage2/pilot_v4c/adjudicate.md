You are the final adjudicator in a research pipeline. Use only this file: read no other file and do not search the web.
Three coders matched each work item below to a benchmark, following the instructions below, and all three chose differently. Make the final call for each item.
Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/pilot_v4c/adjudicated.json
with one element per item: {"item_id", "reasoning", "best", "best_match", "best_difference"}. Write nothing else to that file. Then reply "done <n> items".

=== INSTRUCTIONS ===
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

=== BENCHMARK LIST ===
## Finance, accounting and spreadsheets

**`vals_emb`: Vals Excel Modeling**
Build a complete investment-banking or private-equity Excel model (leveraged buyout, discounted cash flow, merger, operating model, comparables) from a prompt and source files, with standard formatting. Correct means key output cells match the reference model.

**`vals_finance_agent`: Vals Finance Agent**
A financial analyst's research question answered from public company filings and the web, with a calculator. Example: compare two retailers' inventory efficiency for a fiscal year and compute the difference in days inventory outstanding. Other items cover earnings beats and misses, adjustments, comparables and simple modelling. Correct means the answer matches the expert's on a checklist.

**`spreadsheetbench_2`: SpreadsheetBench 2**
A business workbook task: find and fix formula errors and hard-coded values, build or extend a financial model across many sheets, fill a template, or make a chart. Correct means the recalculated cells (or the chart) match the expected result.

**`apex_accounting`: APEX-Accounting**
Month-end close work in a fictional company's accounting system, spreadsheets and PDFs: reconcile an account, calculate and post accruals, enter transactions, prepare schedules, explain variances. Correct means the output meets every item on an accountant-written checklist.

**`dualentry`: DualEntry accounting cases**
A short bookkeeping case given as data. Examples: classify a bank transaction to the right account ("$450 payment to Staples" → office supplies); write a journal entry; match items in a bank reconciliation; handle an accounts-payable or receivable entry. Correct means the account, amounts or classification are exactly right.

**`finch`: Finch (enterprise finance workflows)**
A finance-team workflow rebuilt from real company emails and spreadsheets. Examples: import data, look up figures across several workbooks, calculate, validate, chart, and write a short report. A workflow has one to several such tasks. Correct means a finance expert accepts the output.

## Customer service and contact centre

**`crmarena_pro`: CRMArena-Pro**
A request handled in a company's Salesforce CRM through its data and search tools. Examples: route an incoming case to the best service agent; decide whether a quote breaks the discount policy; qualify a sales lead; answer a question from the knowledge base. Some requests come in a conversation where the requester reveals details gradually. Correct means the answer or chosen record is the right one.

**`eva_bench`: EVA-Bench**
A phone call from a caller with a goal in one of three settings: airline customer service, HR service delivery, or an enterprise IT service desk (password resets, access requests, incident reports). Some callers are difficult or ask for several things. The worker queries and updates the relevant system during the call. Correct means the right records are changed and nothing false is said.

**`tau_voice`: τ-Voice**
The same retail, airline and telecom requests as τ-bench, handled as live phone calls, with accents, background noise and interruptions; some versions in Hindi and other languages. Correct means the same database outcome as in the chat version.

**`sopbench`: SOPBench**
A customer request in a service setting (e.g. banking, healthcare appointments, records) with a written standard operating procedure and system tools. Example: verify the account and check the balance limit before making a transfer. Correct means every required procedure step was followed and the outcome is right.

**`tau_retail_airline`: τ-bench retail and airline**
A chat with a customer who wants something done: exchange or return delivered items, change an order address, rebook or cancel a flight, add baggage. The worker has the company's policy document and tools to look up and change orders or bookings. They must verify the customer, check the policy, confirm, and make the right changes. Correct means the final database matches the correct outcome and required information was given to the customer.

**`tau_telecom`: τ²-bench telecom troubleshooting**
A chat with a mobile customer reporting a problem such as "mobile data not working" or "can't send picture messages". The worker checks the account with tools and talks the customer through steps on their own phone (toggle airplane mode, reset network settings, check the plan), following a troubleshooting policy. Correct means the problem is fixed and the account is in the right state.

**`tau_banking`: τ³-bench banking knowledge**
A chat with a fintech customer about a dispute, refund, fee or cash-back question. The worker must find the relevant rule among about 700 internal policy documents, combine it with account data from tools, and make a compliant account change (e.g. correct a refund amount). Correct means the final account state matches the policy-correct outcome.

## Software testing and QA

**`swt_bench`: SWT-bench Verified**
A bug report plus the code repository before the fix. The worker writes automated tests that reproduce the reported bug. Correct means the new tests fail on the original code and pass once the (hidden) fix is applied, and they exercise the changed code.

**`sweeper_bench`: SWEeper-Bench**
A running open-source web application plus an open-ended request such as "find and fix issues in board sharing and membership". The worker must explore the app in a browser, find the faulty behaviour (which may need many steps across several user accounts), and fix the code. Correct means a browser-based check confirms the intended behaviour now works and other behaviour still works.

## IT service desk and enterprise web applications

**`webarena`: WebArena**
A goal stated in plain language on self-hosted copies of an online store and its admin back end, a GitLab server, a content management system, a forum and a map. Examples: update a product's price and mark it out of stock; count orders cancelled in a given month; change a repository setting. Correct means the answer or the changed data matches.

**`ui_cube`: UI-CUBE**
Tasks in replicas of enterprise applications (Salesforce, SAP, Concur, Workday) and in standalone interface widgets. Examples: enter an expense report from given data, update stock records, move records from one application to another, pick a date in a date picker. Correct means the application's final state matches the goal.

**`workarena_pp`: WorkArena++ (multi-step ServiceNow tickets)**
A multi-step service-desk job in ServiceNow, given either as step-by-step instructions or as a ticket assigned to the worker, as a real employee would get it. Examples: onboard a new employee (create the user, order their hardware, assign the assets); find the staff member with the fewest open incidents and assign them a new problem; work out a budget from a dashboard and place the orders. Correct means every resulting record is right.

**`starshell`: StarShell enterprise tasks**
Record-keeping tasks in three business systems: ServiceNow (incidents, catalog orders, knowledge base), GitLab (repository and issue administration), and ERPNext (create sales invoices, sales orders and linked documents, sometimes chained). Correct means the records in the system match the goal.

**`scuba`: SCUBA (Salesforce)**
A task in a real Salesforce organisation as an administrator, a sales rep or a service agent. Examples: create a leads report with a filter on status; add a formula field visible only to one user profile; update a case. Correct means the organisation's configuration and records match the goal.

**`workarena_l1`: WorkArena (single actions in ServiceNow)**
One explicit instruction in a ServiceNow IT-service-management instance. Examples: create an incident with given fields, filter the incident list by priority and assignment group, order a laptop from the service catalog, find an answer in the knowledge base, read a value off a dashboard. Correct means the record, list state or answer matches the goal.

## Computer use: desktop and office workflows

**`osworld_verified`: OSWorld**
A single goal on a Linux desktop using common applications: a browser, a spreadsheet, a word processor, an email client, an image editor, a code editor, or the operating system's settings. Examples: turn on "Do Not Track" in the browser; fill a column with formulas; convert a sheet to a chart. Correct means a check of the final file or application state passes.

**`online_mind2web`: Online-Mind2Web**
A task on a named live consumer website, e.g. find the cheapest one-way flight between two cities on a date and add a carry-on option, or search rentals with given filters. Correct means the final page or action meets every stated condition.

**`osworld_2`: OSWorld 2.0**
A long end-to-end office workflow on a desktop with real input files, desktop applications and internal websites (email, banking, team chat, application portals, GitLab). Example: follow a PDF guide, extract data from receipts, cross-check it against bank and email records, and file an expense reimbursement claim in a portal. Items cover document preparation, finance and operations analysis, administration and compliance. Correct means every checkpoint on the final state passes.

**`officeval`: OmegaUse-OfficeVal**
A real office request with one or more Word, Excel, PowerPoint or PDF files. Examples: restructure a report, reformat a spreadsheet to a standard, extract data from documents into a table, annotate a document. Correct means the output meets an expert checklist without collateral damage to the files.

## IT operations, system administration and databases

**`terminal_bench_2`: Terminal-Bench 2.0**
A Linux machine plus a written instruction, done entirely at the command line. About a third of the items are everyday IT administration: install and configure a web server with logging and rate limiting, set up a git server, recover a corrupted database file, summarise logs, optimise a query, fix a broken build. The rest are programming puzzles or research tasks. Correct means hidden tests check the final state of the machine.

**`terminal_bench_4`: Terminal-Bench 3.0/4.x**
Same command-line format, longer tasks. Some are infrastructure work: migrate a live database, recover write-ahead logs, fix a payments data pipeline, build a web form. Others are operations work done with files and scripts: process a batch of medical claims against rules, adjudicate warranty claims, prepare a statistical compliance filing. Correct means hidden tests check the outputs and the machine state.

**`cybench`: Cybench**
A professional capture-the-flag security challenge (cryptography, web exploitation, binary exploitation, reverse engineering, forensics) on a security-tools machine. The worker must find a hidden secret string. Correct means the exact string is found.

**`itbench_sre`: ITBench (site reliability)**
A snapshot of a failing Kubernetes application: alerts, events, logs, traces, metrics and service topology. The worker investigates with command-line tools and reports which components caused the incident. Correct means every true root-cause component is named, with no wrong ones.

**`terminal_bench_1`: Terminal-Bench 1.0**
Same format as Terminal-Bench 2.0, with shorter everyday items. Example: "I checked out master and can't find my changes; find them and merge them in." Others cover git, builds and server setup.

**`spider2`: Spider 2.0**
A business question over a large company data warehouse (often 1,000+ columns) plus its documentation. The worker explores the schema and writes SQL; some items are full data-transformation projects. Correct means the query returns the right result table.

**`dba_bench`: DBA-Bench**
A live PostgreSQL database under load plus a symptom alert (e.g. checkout writes timing out). The worker diagnoses the cause using metrics, SQL and admin tools, then fixes it. Example: stale statistics cause a bad query plan, fixed by re-analysing the table. Correct means the problem is resolved and no unsafe action was taken.

## Software development and maintenance

**`swe_bench_pro`: SWE-bench Pro**
An issue description, written requirements and an interface specification for a product codebase (Python, Go, JavaScript/TypeScript), some from private company repositories. The change typically touches several files (around 100 lines across 4 files). Correct means hidden tests for the new behaviour pass and existing tests still pass.

**`swe_bench_verified`: SWE-bench Verified**
A bug report or feature request (a GitHub issue) for an open-source Python library, plus the full code repository. The worker must change the code so the described problem is fixed. Correct means hidden unit tests that check the fix pass, and existing tests still pass.

**`multi_swe_bench`: Multi-SWE-bench**
Same as SWE-bench, but the repositories are in Java, TypeScript, JavaScript, Go, Rust, C and C++. Example: a Java RPC library fails to convert date and time types; fix the conversion. Correct means hidden tests that reproduce the issue now pass.

**`swe_bench_multimodal`: SWE-bench Multimodal**
A bug report for a JavaScript front-end library that includes screenshots of the visual problem (e.g. a tab component rendering wrongly), plus the repository. The worker changes the code; correct means hidden tests, some comparing rendered output, pass.

**`swe_lancer`: SWE-Lancer (individual contributor tasks)**
A real paid freelance job on a commercial expense-management app (React Native / TypeScript), e.g. make the zip-code hint text consistent across two screens, or fix a broken workflow. The worker gets the job description and the codebase and submits a code change. Correct means end-to-end browser tests written by engineers pass.

**`swe_rebench`: SWE-rebench / SWE-bench Live**
Recently filed bug reports and requests on open-source repositories, collected each month, in the same format as SWE-bench: issue plus repository in, code change out, judged by hidden tests.

**`metr_th`: METR task suite**
Self-contained technical tasks in a sandboxed computer with a written instruction. Examples: fix a bug in a machine-learning codebase, write a script that processes data, solve a security challenge, optimise a model training run. A few items are single quick actions, such as choosing which file to open. Each task has an automatic scoring function that checks the result.

## Professional and office work (mixed)

**`jobbench`: JobBench**
A professional request with a folder of real public-record files, each tied to one O*NET task. Example (biostatistician): check a trial's analysis plan against cohort data, recompute the sample size under a new design, and tabulate baseline characteristics. Correct means a long checklist of expert criteria is met.

**`apex_agents`: APEX-Agents**
A task inside a simulated firm's files, email, chat, spreadsheets and presentations, for investment-banking analysts, management consultants or corporate lawyers. Examples: update a buyout model, build a comparables table, draft a legal certificate, find affected people in a spreadsheet. The worker returns a message or a file. Correct means every expert-written criterion is met.

**`theagentcompany`: TheAgentCompany**
A task inside a simulated software company with a code host, project tracker, file share and team chat with colleagues. Covers developer, project-manager, HR, admin, finance and data roles. Example: collect equipment requests from colleagues by chat, look up prices in a shared spreadsheet, total them, and message the requester. Correct means checkpoints on the final files, records and messages pass.

**`gdpval`: GDPval**
A realistic work request written by an experienced professional in one of 44 occupations (e.g. customer service representatives, software developers, accountants, order clerks, administrative assistants, compliance officers, project managers), with reference files. The deliverable is usually a document, spreadsheet, slide deck or PDF. Correct means expert reviewers judge it at least as good as a professional's deliverable.

## Healthcare administration

**`healthadminbench`: HealthAdminBench**
Revenue-cycle work across a hospital records system, insurance payer portals and a fax system. Examples: gather a patient's clinical documents and submit a prior-authorisation request on the right payer portal, then record the result; identify a high-value claim denial and file an appeal with supporting documents; process an equipment order. Correct means every step is correctly recorded in each system.

=== ITEMS ===
[1286b]
Occupation: Computer User Support Specialists
Task statement: Set up equipment for employee use, performing or ensuring proper installation of cables, operating systems, or appropriate software.
Part: Install and configure the operating system, software, and accounts on a new employee's computer so it is ready for use.
Type: DISCRETE
Work item: one workstation configured and handed over to an employee
Start: setup request or new-starter ticket received with hardware available
End: machine imaged, software and accounts configured, handed to employee and ticket closed
Checked by: the employee; IT supervisor
Three coders' verdicts:
  Coder 1: best terminal_bench_1 (partial); second osworld_verified (partial). Reasoning: Closest benchmark: terminal_bench_1, which shares the main actions; difference: this is largely image-based set-up with graphical tools rather than a command-line task. Second choice osworld_verified.
  Coder 2: best osworld_verified (partial); second terminal_bench_1 (partial). Reasoning: OSWorld has desktop configuration tasks. Terminal-Bench 1.0 has everyday setup.
  Coder 3: best workarena_pp (partial); second osworld_verified (partial). Reasoning: WorkArena++ includes onboarding that creates accounts and arranges hardware, but it does not generally perform the physical workstation imaging and handover. OSWorld includes desktop configuration actions, but usually as narrower single goals.

[1287b]
Occupation: Computer User Support Specialists
Task statement: Maintain records of daily data communication transactions, problems and remedial actions taken, or installation activities.
Part: Keep the daily log of data communication transactions and installation activities.
Type: DISCRETE
Work item: one day's log of transactions and installation activities
Start: start of day or shift
End: day's entries complete and log filed
Checked by: IT supervisor; auditors
Three coders' verdicts:
  Coder 1: best workarena_l1 (partial); second none (none). Reasoning: Closest benchmark: workarena_l1, which shares the main actions; difference: benchmark is single records; here the log aggregates a day's entries. Second choice none.
  Coder 2: best theagentcompany (partial); second workarena_pp (partial). Reasoning: TheAgentCompany has record-keeping across tools, and WorkArena covers ticket records. Neither matches a day's log summary closely.
  Coder 3: best starshell (partial); second workarena_l1 (partial). Reasoning: StarShell includes maintaining enterprise service records, but its tasks are discrete system updates rather than a consolidated daily communications and installation log. WorkArena single actions similarly involve entering or retrieving service-management records.

[1288b]
Occupation: Computer User Support Specialists
Task statement: Read technical manuals, confer with users, or conduct computer diagnostics to investigate and resolve problems or to provide technical assistance and support.
Part: Investigate and resolve a ticketed computer problem after the contact, using diagnostics, technical manuals, and follow-up with the user.
Type: DISCRETE
Work item: one ticketed problem investigated and resolved
Start: ticket assigned or problem left open from a contact
End: fix applied and confirmed by the user, ticket closed, or ticket escalated
Checked by: the user; help-desk lead
Three coders' verdicts:
  Coder 1: best osworld_verified (partial); second workarena_pp (partial). Reasoning: OSWorld has desktop goals. WorkArena++ has tickets.
  Coder 2: best terminal_bench_2 (partial); second osworld_verified (partial). Reasoning: Terminal-Bench 2 has everyday IT administration at the command line, matching in kind. OSWorld has desktop settings.
  Coder 3: best terminal_bench_1 (partial); second workarena_pp (partial). Reasoning: Terminal-Bench includes diagnosis and repair of computer problems, but its tasks are command-line based rather than user-support tickets with follow-up. WorkArena++ handles service-desk tickets, but emphasizes record workflows rather than diagnosing and fixing a user's computer.

[2584b]
Occupation: Customer Service Representatives
Task statement: Complete contract forms, prepare change of address records, or issue service discontinuance orders, using computers.
Part: Process contract forms, change-of-address records, or discontinuance orders from written or online requests.
Type: DISCRETE
Work item: one account order processed from a written request
Start: written or online request received
End: order entered and confirmation sent to the customer
Checked by: the customer and the fulfilment or billing team
Three coders' verdicts:
  Coder 1: best workarena_l1 (partial); second ui_cube (partial). Reasoning: WorkArena L1 items are single explicit record actions in a service system, similar to entering an order from a request, but in an IT service tool. UI-CUBE has entering data into enterprise applications from given data.
  Coder 2: best ui_cube (good); second workarena_l1 (good). Reasoning: UI-CUBE has entering data from given input into enterprise apps, the same action. WorkArena single actions create records.
  Coder 3: best tau_retail_airline (partial); second starshell (partial). Reasoning: Tau-bench retail and airline includes checking policy and changing a customer's order or account information. Its requests are handled interactively in chat rather than from a written queue.

[2587b]
Occupation: Customer Service Representatives
Task statement: Review insurance policy terms to determine whether a particular loss is covered by insurance.
Part: Review the policy terms against a reported loss and record a coverage determination for the claim.
Type: DISCRETE
Work item: one coverage determination for a reported loss
Start: loss report and policy retrieved
End: coverage decision recorded on the claim file
Checked by: claims adjuster or supervisor, and the customer
Three coders' verdicts:
  Coder 1: best sopbench (partial); second crmarena_pro (partial). Reasoning: Closest benchmark: sopbench, which shares the main actions; difference: benchmark customer requests are handled live; this is a written determination. Second choice crmarena_pro.
  Coder 2: best tau_banking (partial); second sopbench (partial). Reasoning: tau_banking applies policy documents to a case and ends in a policy-correct outcome, similar reasoning. SOPBench is a written procedure applied to a case.
  Coder 3: best terminal_bench_4 (partial); second jobbench (partial). Reasoning: Terminal-Bench 3.0/4.x includes adjudicating claims against written rules, but its examples concern warranty or medical claims and use a command-line workflow. JobBench includes professional analyses against source documents, though it is not specifically an insurance coverage-determination benchmark.

[14652b]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Install, maintain, or use software testing programs.
Part: Use testing tools to run a test session and record the results.
Type: DISCRETE
Work item: one test run executed with results recorded
Start: test run scheduled or triggered
End: results logged in the test management tool
Checked by: QA lead / developers
Three coders' verdicts:
  Coder 1: best osworld_verified (partial); second workarena_l1 (partial). Reasoning: OSWorld has operating applications. WorkArena L1 has recording single records.
  Coder 2: best terminal_bench_1 (partial); second osworld_verified (partial). Reasoning: Terminal-Bench runs tools and checks state, a rough match. OSWorld has operating applications.
  Coder 3: best sweeper_bench (partial); second swt_bench (partial). Reasoning: SWEeper-Bench includes running and checking software behavior, but also requires locating and fixing issues in code. SWT-bench involves software testing, but asks for new automated regression tests rather than executing and logging a scheduled run.

[14655a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Conduct software compatibility tests with programs, hardware, operating systems, or network environments.
Part: Run compatibility tests of a build across target programs, hardware, operating systems, or network environments.
Type: DISCRETE
Work item: one compatibility test cycle for a build
Start: build and configuration matrix ready
End: compatibility results recorded and issues filed
Checked by: QA lead / release manager
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark is close in inputs, actions and correct result.. Second choice none.
  Coder 2: best terminal_bench_2 (partial); second osworld_verified (partial). Reasoning: No benchmark runs tests across hardware and OS matrices; the nearest are command-line test running tasks. Terminal-Bench has setup and test work but not across devices.
  Coder 3: best sweeper_bench (partial); second swt_bench (partial). Reasoning: SWEeper-Bench involves exploring a running application to find faulty behavior, but it also requires fixing code rather than reporting a compatibility matrix. SWT-bench concerns testing software behavior, but produces automated regression tests for one reported bug.

[14658a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Identify program deviance from standards, and suggest modifications to ensure compliance.
Part: Check a program against standards and recommend modifications to bring it into compliance.
Type: DISCRETE
Work item: one standards-compliance review of a program with recommendations
Start: program or build submitted for compliance check
End: deviations and suggested changes sent to developers
Checked by: developers / QA lead
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark is close in inputs, actions and correct result.. Second choice none.
  Coder 2: best jobbench (partial); second swt_bench (partial). Reasoning: JobBench has checks of work against a standard with a checklist, matching in kind. SWT-bench examines code for defects but writes tests.
  Coder 3: best sweeper_bench (partial); second gdpval (partial). Reasoning: SWEeper-Bench requires exploring software to identify faults, but it also requires implementing fixes instead of reporting standards deviations. GDPval includes expert-reviewed professional analysis, though it is not specifically a program compliance inspection.
