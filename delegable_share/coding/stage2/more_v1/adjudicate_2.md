You are the final adjudicator in a research pipeline. Use only this file: read no other file and do not search the web.
Three coders matched each work item below to a benchmark, following the instructions below, and all three chose differently. Make the final call for each item.
Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/more_v1/adjudicated_2.json
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
[980b]
Occupation: Computer and Information Systems Managers
Task statement: Prepare and review operational reports or project progress reports.
Part: Review a report prepared by staff before it goes out.
Type: DISCRETE
Work item: one staff report reviewed and approved
Start: staff report submitted
End: report approved or returned with changes
Checked by: the author, management
Three coders' verdicts:
  Coder 1: best jobbench (partial); second gdpval (partial). Reasoning: JobBench has checking documents against files with checklists, the nearest to reviewing. GDPval is writing.
  Coder 2: best gdpval (partial); second none (none). Reasoning: gdpval has expert review of professional deliverables, but benchmark workers produce documents rather than review them.
  Coder 3: best officeval (partial); second gdpval (partial). Reasoning: OfficeVal includes restructuring or annotating an existing document against an office request. It does not specifically test managerial approval of the substantive accuracy of an operational or project report.

[58b]
Occupation: Medical and Health Services Managers
Task statement: Plan, implement, and administer programs and services in a health care or medical facility, including personnel administration, training, and coordination of medical, nursing and physical plant staff.
Part: Implement and administer a health care program or service.
Type: DISCRETE
Work item: one program implementation instruction or operational decision
Start: an implementation step or operational issue requires action
End: instruction or decision is communicated to responsible staff
Checked by: program staff and facility leadership
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: The item is managerial decision-making and communication with no matching benchmark. GDPval management deliverables are the only distant relative.
  Coder 2: best theagentcompany (partial); second none (none). Reasoning: TheAgentCompany has tasks of messaging staff to coordinate, sharing the main action.
  Coder 3: best gdpval (partial); second jobbench (partial). Reasoning: GDPval includes expert-reviewed management deliverables from a professional brief, but not necessarily an operational decision communicated during implementation. JobBench also covers professional tasks from records but does not reproduce the ongoing facility context.

[3398a]
Occupation: Budget Analysts
Task statement: Provide advice and technical assistance with cost analysis, fiscal allocation, and budget preparation.
Part: Provide budget or cost-analysis advice to a manager or staff member during a live request.
Type: LIVE_SERVICE
Work item: one live budget assistance request answered
Start: manager or staff member asks for assistance during a contact
End: advice or technical assistance is provided to the requester
Checked by: the requesting manager or staff member
Three coders' verdicts:
  Coder 1: best crmarena_pro (partial); second tau_retail_airline (partial). Reasoning: τ-bench retail and airline have live service requests answered by looking up and applying policy, though the requests there are transactional rather than advice. CRMArena-Pro has requests answered from company data through tools.
  Coder 2: best finch (partial); second none (none). Reasoning: Finch items involve looking up figures across workbooks and calculating for a finance team, which shares the main actions but is not a live conversation. No benchmark has live budget advice.
  Coder 3: best eva_bench (partial); second sopbench (partial). Reasoning: EVA-Bench involves a live service contact in which a worker consults enterprise systems and provides an accurate response. Its scenarios concern airline, HR, and IT support rather than budget analysis and fiscal advice.

[95a]
Occupation: Training and Development Specialists
Task statement: Schedule classes based on availability of classrooms, equipment, or instructors.
Part: Schedule training classes around classroom, equipment and instructor availability.
Type: DISCRETE
Work item: one class schedule (a course run or term) with rooms, equipment and instructors booked
Start: training program or course run approved for scheduling
End: schedule confirmed and published to instructors and trainees
Checked by: instructors, trainees and training manager
Three coders' verdicts:
  Coder 1: best workarena_pp (partial); second theagentcompany (partial). Reasoning: WorkArena++ has multi-step ticket jobs creating and assigning records across a system, similar to booking several resources. It does not involve resolving time conflicts.
  Coder 2: best none (none); second none (none). Reasoning: No benchmark involves constraint scheduling across resources.
  Coder 3: best theagentcompany (partial); second osworld_2 (partial). Reasoning: TheAgentCompany includes administrative coordination across company tools and communications, although its examples do not specifically schedule training resources. OSWorld 2.0 similarly covers multi-step office workflows but not necessarily instructor and classroom scheduling.

[98b]
Occupation: Training and Development Specialists
Task statement: Monitor, evaluate, or record training activities or program effectiveness.
Part: Evaluate how effective a training program has been and report the result.
Type: DISCRETE
Work item: one training program effectiveness evaluation
Start: evaluation data (feedback forms, test results, performance measures) collected for a program
End: evaluation findings delivered to training management
Checked by: training manager or program sponsor
Three coders' verdicts:
  Coder 1: best finch (partial); second jobbench (partial). Reasoning: Finch has workflows of importing data, calculating and writing a short report, which fits the analysis and report. JobBench has data analysis tasks tied to an occupation's task with report criteria.
  Coder 2: best jobbench (partial); second gdpval (partial). Reasoning: GDPval and JobBench have analysis-plus-report deliverables from data files, and Finch has analysis and a short report in spreadsheets.
  Coder 3: best gdpval (partial); second finch (partial). Reasoning: GDPval includes professional analytical reports based on supplied materials, which resembles a training evaluation but is not necessarily focused on training effectiveness. Finch also combines spreadsheet analysis and reporting, but concentrates on finance workflows.

[21447a]
Occupation: Compliance Officers
Task statement: Evaluate applications, records, or documents to gather information about eligibility or liability issues.
Part: Evaluate an application and its records to determine eligibility or liability.
Type: DISCRETE
Work item: one application or case evaluated with eligibility finding
Start: application or records received
End: eligibility or liability finding recorded
Checked by: supervisor and decision-maker
Three coders' verdicts:
  Coder 1: best crmarena_pro (partial); second gdpval (partial). Reasoning: CRMArena-Pro has deciding whether a request meets a policy from records, sharing the main action. GDPval has compliance documents.
  Coder 2: best jobbench (partial); second gdpval (partial). Reasoning: JobBench and GDPval compliance-officer tasks involve checking documents against rules and writing a finding. TerminalBench 4 includes adjudicating claims against rules, but at the command line.
  Coder 3: best sopbench (partial); second terminal_bench_4 (partial). Reasoning: SOPBench asks workers to apply written procedures and account information to reach a compliant outcome, though its cases are service requests rather than application adjudication. Terminal-Bench 3.0/4.x includes rules-based adjudication of claims, but uses command-line workflows.

[21452b]
Occupation: Compliance Officers
Task statement: Issue licenses to individuals meeting standards.
Part: Issue licenses to qualified applicants from the back office and send them out.
Type: DISCRETE
Work item: one license issued and sent
Start: application approved
End: license issued and mailed or delivered
Checked by: the licensee and the agency
Three coders' verdicts:
  Coder 1: best workarena_pp (partial); second ui_cube (partial). Reasoning: WorkArena++ items involve creating and completing records in an enterprise system following a workflow, which is the same kind of back-office issuance. SCUBA and UI-CUBE are similar record work in other applications.
  Coder 2: best starshell (partial); second ui_cube (partial). Reasoning: StarShell tasks are record creation in business systems with correct fields, which matches generating a license record. They do not include producing and mailing a document.
  Coder 3: best ui_cube (partial); second workarena_l1 (partial). Reasoning: UI-CUBE includes entering and updating records in enterprise systems from supplied information. Its tasks do not specifically cover legally effective license issuance and delivery following approval.

[21456a]
Occupation: Compliance Officers
Task statement: Score tests and observe equipment operation and control to rate ability of applicants.
Part: Score a written test and record the result.
Type: DISCRETE
Work item: one test scored and result recorded
Start: completed test received
End: score recorded and result issued
Checked by: the applicant and supervisor
Three coders' verdicts:
  Coder 1: best officeval (partial); second gdpval (partial). Reasoning: OfficeVal processes documents to a standard, partially matching. GDPval has similar compliance deliverables.
  Coder 2: best none (none); second none (none). Reasoning: No benchmark marks tests against a key and records results. DualEntry has short exact-answer cases, but in bookkeeping.
  Coder 3: best ui_cube (partial); second none (none). Reasoning: UI-CUBE covers entering structured results in business applications, but does not reproduce scoring an applicant's test against a rubric. No listed benchmark closely matches the complete scoring and result-issuance task.

[7380a]
Occupation: Operations Research Analysts
Task statement: Perform validation and testing of models to ensure adequacy, and reformulate models, as necessary.
Part: Validate and test a model and reformulate it if needed.
Type: DISCRETE
Work item: one model validation, with any reformulation
Start: model ready for testing
End: model validated or revised and accepted
Checked by: senior analyst, project lead
Three coders' verdicts:
  Coder 1: best metr_th (partial); second jobbench (partial). Reasoning: METR tasks are technical tasks in a sandbox such as fixing a modelling bug and scripts that check results, which matches testing and fixing a model. JobBench has analytic professional tasks judged by checklist.
  Coder 2: best jobbench (partial); second metr_th (partial). Reasoning: JobBench has analyst tasks that recompute and check analyses against data with expert criteria, sharing validation work. METR tasks involve writing scripts to process and test data in a sandbox.
  Coder 3: best swt_bench (partial); second spreadsheetbench_2 (partial). Reasoning: SWT-bench tests the design of automated tests against code, but model validation also assesses assumptions and may require reformulation. SpreadsheetBench 2 includes finding and fixing model formulas, although many operations research models are not spreadsheets.

[1419b]
Occupation: Mechanical Engineers
Task statement: Oversee installation, operation, maintenance, or repair to ensure that machines or equipment are installed and functioning according to specifications.
Part: Verify and sign off that equipment is installed and functioning to specification.
Type: DISCRETE
Work item: one installation or repair acceptance record
Start: installation or repair complete
End: conformance confirmed and record signed
Checked by: customer, plant manager, quality or safety staff
Three coders' verdicts:
  Coder 1: best jobbench (partial); second gdpval (partial). Reasoning: Jobbench has professional requests checking files against criteria and writing results, which is close to verifying conformance from data. Much of this item is physical inspection, which no benchmark covers.
  Coder 2: best none (none); second none (none). Reasoning: No benchmark involves physically verifying equipment and signing off. Only distant overlap with document-writing tasks.
  Coder 3: best gdpval (partial); second none (none). Reasoning: GDPval includes professional records checked by experts, but its usual work is office-based. No listed benchmark closely reproduces physical equipment inspection and acceptance testing.

[19628a]
Occupation: Mechanical Engineers
Task statement: Design integrated mechanical or alternative systems, such as mechanical cooling systems with natural ventilation systems, to improve energy efficiency.
Part: Design an integrated mechanical system (e.g. cooling combined with natural ventilation) to improve energy efficiency.
Type: DISCRETE
Work item: one integrated system design package
Start: building energy goals set
End: design issued
Checked by: client, reviewing engineer, code official
Three coders' verdicts:
  Coder 1: best gdpval (partial); second none (none). Reasoning: GDPval includes mechanical engineering deliverables, which is closest in kind. No benchmark covers integrated system design with calculations and drawings.
  Coder 2: best none (none); second none (none). Reasoning: No benchmark involves building systems design.
  Coder 3: best jobbench (partial); second none (none). Reasoning: JobBench covers expert-assessed professional technical tasks, but its described examples do not involve producing a mechanical design package. No other listed benchmark closely matches integrated building-system engineering and drawings.

[20733b]
Occupation: Mechanical Engineers
Task statement: Research, design, evaluate, install, operate, or maintain mechanical products, equipment, systems or processes to meet requirements.
Part: Design a mechanical product, equipment item, system, or process to meet requirements.
Type: DISCRETE
Work item: one mechanical design package
Start: design requirements and constraints assigned
End: design package issued for review or implementation
Checked by: engineering lead, client, or downstream production team
Three coders' verdicts:
  Coder 1: best gdpval (partial); second jobbench (partial). Reasoning: GDPval includes engineering deliverables judged by experts, sharing the output of a technical package. JobBench has computation tasks tied to engineering-type occupations.
  Coder 2: best none (none); second gdpval (none). Reasoning: No benchmark involves CAD and engineering design. GDPval has engineering deliverables but is document-based.
  Coder 3: best jobbench (partial); second gdpval (partial). Reasoning: JobBench evaluates professional technical deliverables against expert criteria, but its described example is not mechanical CAD design. GDPval also evaluates professional work products but does not specifically describe mechanical design packages.

[20735a]
Occupation: Mechanical Engineers
Task statement: Develop or test models of alternate designs or processing methods to assess feasibility, sustainability, operating condition effects, potential new applications, or necessity of modification.
Part: Develop a model of an alternative design or processing method.
Type: DISCRETE
Work item: one alternative design or process model
Start: alternative and modeling requirements identified
End: model prepared for review or testing
Checked by: engineering or test team
Three coders' verdicts:
  Coder 1: best metr_th (partial); second jobbench (partial). Reasoning: METR tasks are self-contained technical tasks writing scripts and models, which is the closest shape. JobBench has professional analysis from real files.
  Coder 2: best none (none); second none (none). Reasoning: No benchmark covers engineering simulation or CAD modelling.
  Coder 3: best jobbench (partial); second metr_th (partial). Reasoning: JobBench tests professional analytical deliverables from source materials, but its described tasks do not specifically build mechanical engineering models. METR includes technical modeling and code tasks, although it does not generally reproduce CAD or process-model preparation.

[23988a]
Occupation: Economists
Task statement: Review documents written by others.
Part: Review a document written by someone else and give comments.
Type: DISCRETE
Work item: one document reviewed with comments
Start: document received
End: comments returned
Checked by: the author, editor
Three coders' verdicts:
  Coder 1: best jobbench (partial); second gdpval (partial). Reasoning: GDPval deliverables are professional documents, but producing rather than critiquing them. JobBench includes checking others' analysis against data.
  Coder 2: best gdpval (partial); second officeval (partial). Reasoning: gdpval deliverables are expert-judged professional documents, sharing the review of text, but it creates rather than reviews. officeval has annotating documents.
  Coder 3: best officeval (partial); second none (none). Reasoning: OfficeVal includes annotating documents, sharing the action of returning comments on an existing file. Its checklist-oriented file tasks do not specifically require substantive economic peer review.

[245a]
Occupation: Child, Family, and School Social Workers
Task statement: Refer clients to community resources for services, such as job placement, debt counseling, legal aid, housing, medical treatment, or financial assistance, and provide concrete information, such as where to go and how to apply.
Part: Refer a client to a community resource and explain how to access it during a live contact.
Type: LIVE_SERVICE
Work item: one community resource referral made during a client contact
Start: client's need for a community resource identified
End: resource and application or access instructions provided to the client
Checked by: client and, where contacted, receiving agency
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark involves advising a client on community resources.
  Coder 2: best sopbench (partial); second eva_bench (partial). Reasoning: Live client contact with lookup and guidance is closest to SOPBench-type service procedures, though those change system records. EVA-Bench handles calls with a service goal.
  Coder 3: best eva_bench (partial); second sopbench (partial). Reasoning: EVA-Bench involves live conversations in which a worker looks up information and provides accurate guidance, but its settings are not community social-service referrals. SOPBench also involves rule-based service guidance, although it does not specifically match local resources to social-work client needs.

[251a]
Occupation: Child, Family, and School Social Workers
Task statement: Place children in foster or adoptive homes, institutions, or medical treatment centers.
Part: Place a child in a foster or adoptive home, institution or treatment center.
Type: DISCRETE
Work item: one child placement completed
Start: decision that a child needs placement
End: child placed and placement documented
Checked by: supervisor, court, receiving caregiver
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark covers placement of a child. TheAgentCompany has multi-party coordination with documentation, which only loosely compares.
  Coder 2: best healthadminbench (partial); second none (none). Reasoning: HealthAdminBench has multi-system case work with documents and portals, which shares the administrative steps. No benchmark involves child welfare judgment.
  Coder 3: best workarena_pp (partial); second healthadminbench (partial). Reasoning: WorkArena++ includes multi-step coordination and record updates, but it does not test child-placement suitability, safeguards, or physical handoff. HealthAdminBench coordinates services across records and outside organizations, but concerns healthcare administration rather than child placement.

[1764a]
Occupation: Public Relations Specialists
Task statement: Respond to requests for information from the media or designate an appropriate spokesperson or information source.
Part: Answer a reporter's information request, or direct them to the right spokesperson, while they are on the phone.
Type: LIVE_SERVICE
Work item: one media inquiry answered or routed during a call
Start: reporter asks for information
End: information given or spokesperson named to the reporter before the call ends
Checked by: the reporter, and the communications director
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark involves answering a journalist live. Phone benchmarks are customers with database tasks, not information or routing to a spokesperson.
  Coder 2: best tau_voice (partial); second eva_bench (partial). Reasoning: Tau-Voice is a live call where the worker uses policy and tools to answer, which is like this call. The task here is giving information, not a database change.
  Coder 3: best eva_bench (partial); second tau_voice (partial). Reasoning: EVA-Bench involves live calls where the worker consults systems and gives accurate information, but its scenarios are service-desk and customer-service requests rather than media inquiries. τ-Voice similarly tests live policy-based service conversations, not public communications.

[515a]
Occupation: Licensed Practical and Licensed Vocational Nurses
Task statement: Record food and fluid intake and output.
Part: Record a patient's food and fluid intake and output.
Type: DISCRETE
Work item: one patient's intake and output record for a shift
Start: intake and output measured or collected during the shift
End: totals entered in the chart
Checked by: supervising RN, physician
Three coders' verdicts:
  Coder 1: best ui_cube (partial); second workarena_l1 (partial). Reasoning: UI-CUBE items enter given data into enterprise applications until the final state matches, which is what charting totals is. WorkArena single actions are similar record entries.
  Coder 2: best none (none); second none (none). Reasoning: No benchmark is close; the work is summing measurements into a clinical chart. The nearest data-entry benchmarks are in business systems.
  Coder 3: best healthadminbench (partial); second ui_cube (partial). Reasoning: HealthAdminBench uses hospital records systems but focuses on administrative revenue-cycle workflows. UI-CUBE covers structured data entry, though not clinical intake and output charting.

[1810a]
Occupation: Pharmacists
Task statement: Analyze prescribing trends to monitor patient compliance and to prevent excessive usage or harmful interactions.
Part: Review prescribing and dispensing data for patient compliance, overuse, or harmful interactions, and flag cases.
Type: DISCRETE
Work item: one drug utilization review report or flagged case list
Start: dispensing or prescribing data pulled for the review
End: findings reported and flagged cases passed on
Checked by: pharmacy manager, prescribers, insurers
Three coders' verdicts:
  Coder 1: best spider2 (partial); second jobbench (partial). Reasoning: Spider 2.0 has business questions answered from data, which shares the query and review action. JobBench has analytic checks of professional data.
  Coder 2: best healthadminbench (partial); second finch (partial). Reasoning: Finch has pulling and validating data and reporting, which shares the data steps, but is finance. HealthAdminBench is healthcare record work, but revenue-cycle rather than clinical review.
  Coder 3: best jobbench (partial); second healthadminbench (partial). Reasoning: JobBench includes expert professional analysis of supplied records, but its described tasks do not specifically perform drug utilization review. HealthAdminBench uses medical records and payer systems, but focuses on revenue-cycle submissions rather than clinical prescribing trends.

[1812c]
Occupation: Pharmacists
Task statement: Maintain records, such as pharmacy files, patient profiles, charge system files, inventories, control records for radioactive nuclei, or registries of poisons, narcotics, or controlled drugs.
Part: Maintain pharmacy charge or billing records.
Type: DISCRETE
Work item: one charge or billing record updated
Start: charge information or correction received
End: record updated and saved
Checked by: pharmacy billing staff and auditors
Three coders' verdicts:
  Coder 1: best dualentry (partial); second starshell (partial). Reasoning: DualEntry cases involve recording entries to the right account with exact amounts, which matches in record accuracy. StarShell also updates business records in systems.
  Coder 2: best workarena_l1 (good); second scuba (partial). Reasoning: WorkArena level 1 has single record updates in a business system, the same action. DualEntry has billing record entries, but as short data cases.
  Coder 3: best healthadminbench (partial); second ui_cube (partial). Reasoning: HealthAdminBench includes healthcare billing records and system updates, but focuses on broader hospital revenue-cycle workflows rather than a single pharmacy charge update. UI-CUBE also tests structured financial record entry without the pharmacy billing context.

[1812d]
Occupation: Pharmacists
Task statement: Maintain records, such as pharmacy files, patient profiles, charge system files, inventories, control records for radioactive nuclei, or registries of poisons, narcotics, or controlled drugs.
Part: Maintain inventory, controlled-drug, poison, or radioactive-material records.
Type: DISCRETE
Work item: one inventory or regulated-stock record entry or reconciliation
Start: stock movement or reconciliation due
End: record updated and discrepancies noted
Checked by: pharmacy management and regulatory auditors
Three coders' verdicts:
  Coder 1: best dualentry (partial); second apex_accounting (partial). Reasoning: DualEntry reconciliation cases match items and flag differences, which is like reconciling stock records. APEX-Accounting has account reconciliation in an accounting system.
  Coder 2: best apex_accounting (partial); second dualentry (partial). Reasoning: APEX-Accounting has reconciliations and entering transactions with checklist grading, sharing the main actions, but with stock rather than money. DualEntry has matching and entering records to exact amounts.
  Coder 3: best ui_cube (partial); second healthadminbench (partial). Reasoning: UI-CUBE includes updating stock records in enterprise systems, but it does not specifically cover regulated pharmacy inventory or controlled-drug reconciliation. HealthAdminBench uses healthcare systems, but focuses on revenue-cycle processes rather than regulated stock records.

[1821b]
Occupation: Pharmacists
Task statement: Assay radiopharmaceuticals, verify rates of disintegration, and calculate the volume required to produce the desired results, to ensure proper dosages.
Part: Calculate and record the volume needed for the desired dose.
Type: DISCRETE
Work item: one radiopharmaceutical dose calculated and recorded
Start: assay result available
End: volume calculated and entered in the dose record
Checked by: physician, radiation safety officer
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark matches a dose calculation. Vals Finance Agent has calculations from data.
  Coder 2: best dualentry (partial); second none (none). Reasoning: DualEntry has short cases where amounts must be exactly right.
  Coder 3: best jobbench (partial); second none (none). Reasoning: JobBench includes specialist calculations from supplied data checked against expert criteria, but its described cases do not involve radiopharmaceutical dosing. No other listed benchmark closely matches this clinical calculation and recording work.

[1822b]
Occupation: Pharmacists
Task statement: Manage pharmacy operations, hiring or supervising staff, performing administrative duties, or buying or selling non-pharmaceutical merchandise.
Part: Complete an administrative pharmacy-management task or report.
Type: DISCRETE
Work item: one pharmacy administrative report, schedule, or filing
Start: administrative requirement or reporting period identified
End: item completed and filed or communicated
Checked by: pharmacy management, staff, or regulators
Three coders' verdicts:
  Coder 1: best gdpval (partial); second osworld_2 (partial). Reasoning: GDPval has administrative deliverables, though broad. OSWorld 2.0 includes administration and compliance workflows across systems.
  Coder 2: best osworld_2 (partial); second gdpval (partial). Reasoning: OSWorld 2.0 has office workflows such as compliance and administration across files and portals, which shares the main actions. GDPval has administrative document deliverables.
  Coder 3: best theagentcompany (partial); second gdpval (partial). Reasoning: TheAgentCompany includes schedules and administrative records in workplace systems, but not pharmacy-specific management or regulatory filings. GDPval similarly covers professional reports without this particular pharmacy context.

[1822c]
Occupation: Pharmacists
Task statement: Manage pharmacy operations, hiring or supervising staff, performing administrative duties, or buying or selling non-pharmaceutical merchandise.
Part: Purchase non-pharmaceutical merchandise for the pharmacy.
Type: DISCRETE
Work item: one non-pharmaceutical merchandise order
Start: merchandise need identified
End: order submitted to the supplier
Checked by: supplier and pharmacy management
Three coders' verdicts:
  Coder 1: best starshell (partial); second gdpval (partial). Reasoning: StarShell includes creating purchase and sales orders in ERPNext from given data, which shares the main action, but here the worker first decides what to buy. GDPval order-clerk requests are similar in procurement content but deliver documents.
  Coder 2: best online_mind2web (partial); second webarena (partial). Reasoning: Online-Mind2Web has finding items and placing a selection on a live shopping site, which shares the ordering action. WebArena has online store tasks such as managing products.
  Coder 3: best workarena_pp (partial); second ui_cube (partial). Reasoning: WorkArena++ includes determining what to buy and placing orders through an enterprise system. Its examples use service catalog purchases rather than pharmacy merchandise replenishment.

[1823b]
Occupation: Pharmacists
Task statement: Work in hospitals or clinics or for Health Management Organizations (HMOs), dispensing prescriptions, serving as a medical team consultant, or specializing in specific drug therapy areas, such as oncology or nuclear pharmacotherapy.
Part: Answer a team member's question or advise on a specialty drug therapy.
Type: DISCRETE
Work item: one consult on drug therapy answered
Start: consult request received
End: advice given and noted
Checked by: requesting clinician
Three coders' verdicts:
  Coder 1: best gdpval (partial); second none (none). Reasoning: GDPval has professional advice documents judged by experts, sharing the written answer. No benchmark covers clinical drug consults.
  Coder 2: best none (none); second none (none). Reasoning: No benchmark involves answering clinical drug-therapy questions. The closest are research question benchmarks, which are finance based.
  Coder 3: best jobbench (partial); second healthadminbench (partial). Reasoning: JobBench includes professional expert tasks grounded in reference files, but it does not specifically reproduce a live clinical drug consult. HealthAdminBench uses hospital systems but tests administrative revenue-cycle work rather than clinical advice.

[1824b]
Occupation: Pharmacists
Task statement: Assess the identity, strength, or purity of medications.
Part: Record the test result and release or quarantine the batch.
Type: DISCRETE
Work item: one batch quality test result recorded
Start: test completed
End: result recorded and batch released or held
Checked by: pharmacy manager, quality assurance, inspectors
Three coders' verdicts:
  Coder 1: best apex_accounting (partial); second terminal_bench_4 (partial). Reasoning: APEX-Accounting has recording results in a company system checked against a checklist, and Terminal-Bench 4 has processing batches against rules. Neither involves pharmaceutical quality records.
  Coder 2: best none (none); second none (none). Reasoning: No benchmark involves recording a laboratory quality result and releasing a batch. Process-against-rules tasks in Terminal-Bench 3.0 are the nearest but are done at the command line.
  Coder 3: best sopbench (partial); second ui_cube (partial). Reasoning: SOPBench requires applying written rules to system records and taking a compliant action, but its examples do not involve medication batch quality disposition. UI-CUBE covers updating enterprise records but not quality-release judgment.

[20406a]
Occupation: Pharmacists
Task statement: Update or troubleshoot pharmacy information databases.
Part: Update a pharmacy information database.
Type: DISCRETE
Work item: one pharmacy database update
Start: database change requirement received
End: change entered and verified
Checked by: pharmacy users or system administrator
Three coders' verdicts:
  Coder 1: best scuba (partial); second ui_cube (partial). Reasoning: SCUBA has configuration and record updates in an enterprise system, sharing the main action. UI-CUBE has updating records in applications.
  Coder 2: best workarena_l1 (partial); second starshell (partial). Reasoning: workarena_l1 has explicit single record changes in an enterprise system, a close match on actions, but a different system. starshell has record changes in business systems.
  Coder 3: best ui_cube (partial); second scuba (partial). Reasoning: UI-CUBE tests updates to enterprise application records and configuration, but it does not specifically use pharmacy databases or clinical verification. SCUBA also tests system record and configuration changes in Salesforce rather than a pharmacy system.

[2276a]
Occupation: Waiters and Waitresses
Task statement: Collect payments from customers.
Part: Take a customer's payment for the meal and return change or the card.
Type: LIVE_SERVICE
Work item: one table's payment taken
Start: customer hands over cash or card for the check
End: payment processed and change or receipt returned
Checked by: manager at cash-out, and the customer
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark involves taking a face-to-face payment at a point of sale. Service benchmarks involve policy-driven database changes, which is a different kind of work.
  Coder 2: best tau_retail_airline (partial); second ui_cube (partial). Reasoning: This is a live POS transaction; tau_retail_airline is a live service with transactions and tools, though by chat. UI-CUBE is application operation.
  Coder 3: best sopbench (partial); second tau_retail_airline (partial). Reasoning: SOPBench includes financial transactions under service procedures, but it does not represent collecting a restaurant table's payment and returning cash or a card. τ-bench retail handles order and refund transactions, but does so remotely rather than at the table.

[2277a]
Occupation: Waiters and Waitresses
Task statement: Write patrons' food orders on order slips, memorize orders, or enter orders into computers for transmittal to kitchen staff.
Part: Write, memorize, or enter a food order while the patrons are ordering.
Type: LIVE_SERVICE
Work item: one table's food order captured during ordering
Start: patrons begin giving their food selections
End: selections are recorded or memorized and confirmed as needed
Checked by: patrons and kitchen staff
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark covers taking a spoken order at a table. The phone-service benchmarks involve policy checks and record changes rather than capturing a menu order.
  Coder 2: best tau_retail_airline (partial); second tau_voice (partial). Reasoning: τ-bench has live conversations where the worker captures a customer's request into a system under a policy, similar to taking an order. It is in person with no policy lookups; τ-Voice is the spoken version.
  Coder 3: best tau_voice (partial); second none (none). Reasoning: τ-Voice involves live customer requests and correct transaction details, but its retail, airline and telecom cases are not restaurant order taking. No other benchmark closely represents capturing a table's spoken food order.

[2294a]
Occupation: Waiters and Waitresses
Task statement: Describe and recommend wines to customers.
Part: Describe wines and recommend one to a table.
Type: LIVE_SERVICE
Work item: one table advised on wine
Start: customer asks about wine or server offers the list
End: customer chooses a wine
Checked by: the customer
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark covers advising a diner in person. The call-centre benchmarks involve system lookups that this item lacks.
  Coder 2: best tau_retail_airline (partial); second none (none). Reasoning: tau_retail_airline involves a live chat advising a customer toward a choice under company knowledge, which shares the conversational advising, but its correctness is a database state. Nothing else is close.
  Coder 3: best tau_voice (partial); second none (none). Reasoning: τ-Voice covers live customer conversations using service information, but its calls concern account or booking actions rather than wine recommendations. No other listed benchmark closely tests restaurant wine advice.

[18748a]
Occupation: Waiters and Waitresses
Task statement: Provide guests with information about local areas, including directions.
Part: Give a guest information about the local area, such as directions.
Type: LIVE_SERVICE
Work item: one guest's local question answered
Start: guest asks
End: guest has the information
Checked by: the guest
Three coders' verdicts:
  Coder 1: best webarena (partial); second online_mind2web (partial). Reasoning: Online-Mind2Web has finding information on live websites, and WebArena includes a map, which is close to the lookup part, but neither is a face-to-face question. No live-service benchmark covers this.
  Coder 2: best none (none); second none (none). Reasoning: No benchmark involves answering a guest's local question from memory. The closest chat service tasks use policies and databases.
  Coder 3: best online_mind2web (partial); second none (none). Reasoning: Online-Mind2Web involves finding information on consumer websites, but it does not involve a live restaurant guest or necessarily provide directions. No other listed benchmark closely matches an informal local-information exchange.

[23108b]
Occupation: Fast Food and Counter Workers
Task statement: Monitor and order supplies or food items, and restock as necessary to maintain inventory.
Part: Order food and supplies needed to maintain inventory.
Type: DISCRETE
Work item: one food or supply replenishment order
Start: stock needs are identified
End: order is submitted to the supplier or purchasing team
Checked by: manager and supplier or purchasing team
Three coders' verdicts:
  Coder 1: best workarena_l1 (partial); second starshell (partial). Reasoning: Workarena level 1 includes ordering items from a catalog in a web system, sharing the main actions, but here the quantities come from counting stock and judgement on usage. Starshell has ERP order records but not stock judgement.
  Coder 2: best online_mind2web (partial); second ui_cube (partial). Reasoning: Online-Mind2Web has ordering items on a site with conditions, sharing the main action, but without stock counting or par levels. UI-CUBE has enterprise form-entry tasks.
  Coder 3: best workarena_pp (partial); second ui_cube (partial). Reasoning: WorkArena++ includes placing orders based on business requirements, but its examples concern service catalog purchases rather than food replenishment. UI-CUBE also includes stock-record and enterprise transaction tasks, though not necessarily a supplier replenishment order.

[669a]
Occupation: First-Line Supervisors of Retail Sales Workers
Task statement: Formulate pricing policies for merchandise, according to profitability requirements.
Part: Set pricing policies for merchandise to meet profitability targets.
Type: DISCRETE
Work item: one pricing decision or price update for a product line
Start: margin target and cost data available
End: prices approved and entered
Checked by: district manager or buying office
Three coders' verdicts:
  Coder 1: best finch (partial); second webarena (partial). Reasoning: Finch has calculation across workbooks, which matches the margin work. WebArena has updating a product price in a store back end.
  Coder 2: best spreadsheetbench_2 (partial); second gdpval (partial). Reasoning: SpreadsheetBench 2 tasks compute and update workbook figures to a specification, sharing the main action, but do not include entering prices into a system. GDPval has retail professional requests.
  Coder 3: best webarena (partial); second spreadsheetbench_2 (partial). Reasoning: WebArena includes changing a product's price in an online-store administration system. Its explicit price updates do not generally require developing a line-wide pricing decision from costs and margin targets.

[2451a]
Occupation: Real Estate Sales Agents
Task statement: Arrange for title searches to determine whether clients have clear property titles.
Part: Arrange a title search to confirm a client's property title is clear.
Type: DISCRETE
Work item: one title search ordered and result reviewed
Start: property under contract
End: title result received and shared with parties
Checked by: escrow or title company; buyer; lender
Three coders' verdicts:
  Coder 1: best healthadminbench (partial); second osworld_2 (partial). Reasoning: HealthAdminBench has submitting requests on portals and recording results, a similar action pattern. OSWorld 2.0 includes portal filing workflows.
  Coder 2: best gdpval (partial); second none (none). Reasoning: GDPval has document review and written communication, sharing the main action. No benchmark covers ordering title searches.
  Coder 3: best osworld_2 (partial); second theagentcompany (partial). Reasoning: OSWorld 2.0 includes multi-step requests that submit information, cross-check results, and communicate outcomes, but not specifically title searches. TheAgentCompany also coordinates records and messages across parties in a different business context.

[2453a]
Occupation: Real Estate Sales Agents
Task statement: Answer clients' questions regarding construction work, financing, maintenance, repairs, and appraisals.
Part: Answer a client's questions about construction, financing, maintenance, repairs or appraisals while they are on the call or in person.
Type: LIVE_SERVICE
Work item: one client question answered live
Start: client asks question
End: client has the answer
Checked by: the client
Three coders' verdicts:
  Coder 1: best tau_voice (partial); second none (none). Reasoning: Tau-voice involves live calls answering requests, sharing the live format, but with database changes. No other benchmark matches.
  Coder 2: best none (none); second none (none). Reasoning: No benchmark is a live question-and-answer with no system action. tau_banking has answering questions from policy documents but ends in an account change.
  Coder 3: best eva_bench (partial); second none (none). Reasoning: EVA-Bench involves answering questions during live calls using system information, but its scenarios are not real estate advice. No other benchmark closely matches live property-specific professional advice.

[2461a]
Occupation: Real Estate Sales Agents
Task statement: Investigate clients' financial and credit status to determine eligibility for financing.
Part: Review a client's financial and credit status to judge eligibility for financing.
Type: DISCRETE
Work item: one buyer financial eligibility review
Start: buyer provides financial information
End: eligibility assessment given or pre-approval requested
Checked by: the lender; the buyer
Three coders' verdicts:
  Coder 1: best gdpval (partial); second none (none). Reasoning: GDPval has professional assessment documents built from supplied financial files, which shares the main action, but not eligibility judgment for lending. No finance benchmark covers consumer credit review.
  Coder 2: best vals_finance_agent (partial); second finch (partial). Reasoning: Vals Finance Agent has calculation-based finance answers from documents, which shares reading and calculating. Finch has workflows that validate figures across files.
  Coder 3: best sopbench (partial); second osworld_2 (partial). Reasoning: SOPBench includes policy-based financial service requests using account information and system tools, but not real-estate buyer pre-qualification. OSWorld 2.0 includes finance and application-portal workflows, though it is not specifically focused on mortgage eligibility.

[2468b]
Occupation: Real Estate Sales Agents
Task statement: Solicit and compile listings of available rental properties.
Part: Compile available rental listings.
Type: DISCRETE
Work item: one rental listing compiled
Start: landlord provides property details
End: listing published or added to list
Checked by: landlord; broker
Three coders' verdicts:
  Coder 1: best ui_cube (partial); second gdpval (partial). Reasoning: UI-CUBE has entering data into application forms, and GDPval has producing a written item from supplied details.
  Coder 2: best gdpval (partial); second online_mind2web (partial). Reasoning: GDPval has work requests that produce a document from provided details, and Online-Mind2Web covers actions on websites. This item is mainly writing and posting a listing.
  Coder 3: best webarena (partial); second online_mind2web (partial). Reasoning: WebArena includes creating or changing content in web applications, sharing the record-entry action but not specifically rental listings. Online-Mind2Web covers rentals as a consumer search rather than compiling and publishing a listing.

[2471b]
Occupation: Real Estate Sales Agents
Task statement: Locate and appraise undeveloped areas for building sites, based on evaluations of area market conditions.
Part: Appraise undeveloped land as building sites from local market conditions.
Type: DISCRETE
Work item: one site evaluation
Start: site identified
End: evaluation delivered to client
Checked by: client or developer
Three coders' verdicts:
  Coder 1: best gdpval (partial); second vals_finance_agent (partial). Reasoning: Vals Finance Agent has research questions answered from public data with calculation, partly like market research and valuation. GDPval has real estate professional deliverables.
  Coder 2: best vals_finance_agent (partial); second gdpval (partial). Reasoning: Vals Finance Agent answers an analyst's research question from public sources with calculation, which shares the research and valuation work. It uses company filings rather than local land and market data, and the output is shorter than a client evaluation.
  Coder 3: best jobbench (partial); second gdpval (partial). Reasoning: JobBench includes professional evaluations based on public-record files, but does not specifically model local land appraisal and site suitability. GDPval similarly includes expert-reviewed professional deliverables without a dedicated undeveloped-land workflow.

[4741a]
Occupation: Shipping, Receiving, and Inventory Clerks
Task statement: Confer or correspond with establishment representatives to rectify problems, such as damages, shortages, or nonconformance to specifications.
Part: Contact a supplier or other establishment to resolve damage, shortage or nonconformance on a shipment.
Type: DISCRETE
Work item: one shipment problem resolved with the sender or receiver
Start: damage, shortage or mismatch found
End: agreed remedy confirmed and the case closed
Checked by: purchasing, supervisor, accounting
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark is about resolving a shipment dispute with a supplier by correspondence.
  Coder 2: best theagentcompany (partial); second gdpval (partial). Reasoning: TheAgentCompany tasks involve messaging colleagues, looking up records and updating files, which shares the correspondence and record keeping. GDPval has written correspondence deliverables for order clerks and similar roles.
  Coder 3: best crmarena_pro (partial); second tau_retail_airline (partial). Reasoning: CRMArena-Pro handles service cases using company records and knowledge, but its examples do not specifically resolve shipment discrepancies with another establishment. τ-bench handles order problems with policy and system updates, though from the customer-service side.

[779a]
Occupation: Medical Secretaries and Administrative Assistants
Task statement: Greet visitors, ascertain purpose of visit, and direct them to appropriate staff.
Part: Greet a visitor, find out why they came and direct them to the right staff.
Type: LIVE_SERVICE
Work item: one visitor greeted and directed
Start: visitor arrives at the desk
End: visitor sent or taken to the right person
Checked by: visitor, staff expecting them
Three coders' verdicts:
  Coder 1: best eva_bench (partial); second tau_voice (partial). Reasoning: EVA-Bench has live calls where the worker finds out what the caller wants and queries a system, similar to routing a visitor. It is a phone call rather than a walk-up.
  Coder 2: best tau_voice (partial); second eva_bench (partial). Reasoning: Tau-Voice is a live service contact where the worker uses a lookup to resolve the request, which is similar. It is a walk-up greeting, not a phone call.
  Coder 3: best none (none); second none (none). Reasoning: No listed benchmark closely models greeting an in-person visitor and directing them to staff. Customer-service benchmarks involve conversations and lookups but focus on completing account or booking requests.

[9713a]
Occupation: First-Line Supervisors of Office and Administrative Support Workers
Task statement: Prepare and issue work schedules, deadlines, and duty assignments for office or administrative staff.
Part: Prepare and issue the work schedule for staff.
Type: DISCRETE
Work item: one staff work schedule prepared and issued
Start: coverage needs and availability known
End: schedule issued to staff
Checked by: staff, department manager
Three coders' verdicts:
  Coder 1: best gdpval (partial); second spreadsheetbench_2 (partial). Reasoning: SpreadsheetBench 2 has workbook tasks filled to a specification, which shares the scheduling spreadsheet work. GDPval includes administrative deliverables like schedules.
  Coder 2: best spreadsheetbench_2 (partial); second theagentcompany (partial). Reasoning: τ-Voice and τ-bench handle bookings under policy, which is a scheduling flavour, but they are customer conversations. SpreadsheetBench 2 involves building a workbook to a specification, which resembles preparing the roster.
  Coder 3: best theagentcompany (partial); second spreadsheetbench_2 (partial). Reasoning: TheAgentCompany includes coordinating staff information and producing a shared operational result, but does not specifically center on preparing a staff work schedule. SpreadsheetBench 2 includes filling and modifying workbooks but not the full coverage and issuance workflow.

[23431a]
Occupation: Carpenters
Task statement: Study specifications in blueprints, sketches, or building plans to prepare project layout and determine dimensions and materials required.
Part: Study blueprints, sketches or plans to lay out the job and work out dimensions and materials required.
Type: DISCRETE
Work item: one job (or phase) laid out with dimensions and materials list
Start: plans or sketches received for the job
End: layout marked out and materials list ready
Checked by: foreman or general contractor, and the crew using the layout
Three coders' verdicts:
  Coder 1: best gdpval (partial); second none (none). Reasoning: GDPval has takeoff-type deliverables for professionals in occupations like these, sharing the reading of plans and calculating action. No benchmark involves reading blueprints and laying out physical work.
  Coder 2: best none (none); second none (none). Reasoning: No benchmark involves reading construction plans or physical layout.
  Coder 3: best jobbench (partial); second none (none). Reasoning: JobBench includes occupation-specific analysis of supplied documents and a professional deliverable, but not physical construction layout. No other benchmark closely matches measuring and marking a job site.

[23436a]
Occupation: Carpenters
Task statement: Select and order lumber or other required materials.
Part: Select lumber and other materials needed for the job and place the order with the supplier.
Type: DISCRETE
Work item: one materials order placed with a supplier
Start: materials list for the job or phase available
End: order confirmed with supplier and delivery scheduled
Checked by: foreman or contractor who pays; the crew who receives it
Three coders' verdicts:
  Coder 1: best starshell (partial); second workarena_l1 (partial). Reasoning: StarShell creates orders in an ERP, which shares the action of placing an order with given items. WorkArena L1 catalogue orders are similar.
  Coder 2: best theagentcompany (partial); second gdpval (partial). Reasoning: TheAgentCompany has tasks that collect requirements, look up prices and total them, sharing the main actions. They do not involve construction quantities or confirming delivery with a supplier.
  Coder 3: best workarena_pp (partial); second online_mind2web (partial). Reasoning: WorkArena++ includes placing orders after consulting business information, which shares the requisition and record actions. Online-Mind2Web also involves finding options on a website, but neither focuses on construction materials and supplier delivery.

[20160a]
Occupation: Team Assemblers
Task statement: Review work orders and blueprints to ensure work is performed according to specifications.
Part: Review work orders and blueprints so that work is done to specification.
Type: DISCRETE
Work item: one work order and drawings reviewed before assembly
Start: work order received
End: specifications understood and issues raised, assembly begins
Checked by: team leader or supervisor; quality
Three coders' verdicts:
  Coder 1: best jobbench (partial); second none (none). Reasoning: JobBench has professional requests built on real public-record files with checklists, which shares the read-and-check-against-specification action. No benchmark involves engineering drawings.
  Coder 2: best none (none); second none (none). Reasoning: No benchmark involves reading blueprints to check an assembly order.
  Coder 3: best officeval (partial); second jobbench (partial). Reasoning: OfficeVal includes reviewing and annotating supplied documents, but not interpreting manufacturing drawings before assembly. JobBench has occupation-specific source-file analysis, though not specifically this shop-floor check.

[20161a]
Occupation: Team Assemblers
Task statement: Complete production reports to communicate team production level to management.
Part: Complete production reports showing the team's output for management.
Type: DISCRETE
Work item: one production report
Start: end of shift or reporting period
End: report submitted to management
Checked by: production supervisor or manager
Three coders' verdicts:
  Coder 1: best finch (partial); second officeval (partial). Reasoning: Finch has workflows of entering data and writing a short report, which fits, though in finance. OfficeVal has extracting data into tables.
  Coder 2: best officeval (good); second finch (partial). Reasoning: OfficeVal items fill and reformat reports and spreadsheets from given data, which is the same kind of work. Finch builds reports from workbooks but in finance.
  Coder 3: best ui_cube (partial); second finch (partial). Reasoning: UI-CUBE includes entering and moving operational records in enterprise applications, but does not specifically prepare team production reports. Finch includes compiling figures and reporting them, though its workflows are finance-oriented.

[23876b]
Occupation: Stockers and Order Fillers
Task statement: Examine and inspect stock items for wear or defects, reporting any damage to supervisors.
Part: Report damaged stock to a supervisor.
Type: DISCRETE
Work item: one damage report to a supervisor
Start: damaged or worn item found
End: report delivered to the supervisor
Checked by: supervisor
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark covers writing a short damage note to a supervisor. TheAgentCompany messaging tasks are far larger.
  Coder 2: best theagentcompany (partial); second none (none). Reasoning: TheAgentCompany includes short messages to colleagues, similar in action but not in damage reporting. OSWorld has small form tasks.
  Coder 3: best workarena_l1 (partial); second starshell (partial). Reasoning: WorkArena single-action tasks include creating an incident record with supplied details, sharing the basic reporting action but not inspecting damaged physical stock. StarShell also includes incident record-keeping, with the same important difference.

[23881a]
Occupation: Stockers and Order Fillers
Task statement: Compare merchandise invoices to items actually received to ensure that shipments are correct.
Part: Compare the merchandise invoice with the items actually received to confirm the shipment is correct.
Type: DISCRETE
Work item: one shipment checked against its invoice
Start: delivery unloaded with invoice in hand
End: invoice confirmed or discrepancies noted and passed on
Checked by: purchasing, accounts payable, or supervisor
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark involves physically counting delivered goods. DualEntry matching is data-only and does not involve inspection.
  Coder 2: best dualentry (partial); second none (none). Reasoning: DualEntry has matching items in reconciliations, which resembles comparing invoice lines to goods, but the physical check is outside any benchmark. No benchmark has counting goods.
  Coder 3: best ui_cube (partial); second apex_accounting (partial). Reasoning: UI-CUBE includes updating stock records in enterprise applications, but does not model physically counting a delivered shipment against its invoice. APEX-Accounting includes checking financial records, though it focuses on accounting close rather than receiving goods.

[23882a]
Occupation: Stockers and Order Fillers
Task statement: Itemize and total customer merchandise selection at checkout counter, using cash register, and accept cash or charge card for purchases.
Part: Itemize and total a customer's purchases at the register and take cash or card payment.
Type: LIVE_SERVICE
Work item: one customer sale at the register
Start: customer presents items at checkout
End: payment taken and receipt given
Checked by: the customer; store manager at till reconciliation
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark involves scanning and cashing out in person. The retail chat benchmark is about order changes, not a checkout.
  Coder 2: best tau_retail_airline (partial); second none (none). Reasoning: tau-bench retail has customer chats with orders and payments under policy, which shares the live customer and system action, but it is chat or phone service rather than a physical register. No benchmark matches a point-of-sale scan and payment closely.
  Coder 3: best ui_cube (partial); second sopbench (partial). Reasoning: UI-CUBE includes entering transaction data and changing records in enterprise applications. It does not include scanning physical merchandise and accepting payment at a live checkout.

[23885b]
Occupation: Stockers and Order Fillers
Task statement: Take inventory or examine merchandise to identify items to be reordered or replenished.
Part: Compile the list of items to be reordered or replenished from the counts.
Type: DISCRETE
Work item: one reorder or replenishment list
Start: counts of stock on hand complete
End: list passed to purchasing or the supervisor
Checked by: supervisor or purchasing
Three coders' verdicts:
  Coder 1: best finch (partial); second spreadsheetbench_2 (partial). Reasoning: Finch involves looking up figures across workbooks and calculating, sharing the main action. SpreadsheetBench 2 has similar workbook work.
  Coder 2: best spreadsheetbench_2 (partial); second gdpval (partial). Reasoning: SpreadsheetBench 2 has workbook tasks of calculating from data. GDPval has order clerk work.
  Coder 3: best ui_cube (partial); second workarena_l1 (partial). Reasoning: UI-CUBE includes updating stock records and moving data within enterprise applications, but does not specifically describe compiling a reorder list from completed counts. WorkArena single-action tasks similarly involve filtering or reading records rather than producing a stock replenishment list.

[23886a]
Occupation: Stockers and Order Fillers
Task statement: Issue or distribute materials, products, parts, and supplies to customers or coworkers, based on information from incoming requisitions.
Part: Issue requested materials or products while a customer or coworker waits.
Type: LIVE_SERVICE
Work item: one requisition issued during a live contact
Start: customer or coworker presents a requisition or request
End: requested available items are handed over
Checked by: recipient and stockroom supervisor
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: The work is mostly physical handing over of goods, with no benchmark involving it. System recording alone does not match any listed benchmark.
  Coder 2: best tau_retail_airline (partial); second starshell (partial). Reasoning: τ-bench retail has live requests to look up and change orders while the customer waits, the closest live work, but lacks physical handing over. ERPNext tasks in StarShell cover the stock record side.
  Coder 3: best ui_cube (partial); second workarena_pp (partial). Reasoning: UI-CUBE includes stock-record updates in enterprise applications, but does not include physically retrieving and handing over items during a live contact. WorkArena++ includes catalog orders and asset workflows but likewise lacks the physical issue step.
