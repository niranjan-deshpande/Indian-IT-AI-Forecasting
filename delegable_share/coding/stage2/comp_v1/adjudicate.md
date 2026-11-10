You are the final adjudicator in a research pipeline. Use only this file: read no other file and do not search the web.
Three coders matched each work item below to a benchmark, following the instructions below, and all three chose differently. Make the final call for each item.
Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/comp_v1/adjudicated.json
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
[9327b]
Occupation: Interpreters and Translators
Task statement: Identify and resolve conflicts related to the meanings of words, concepts, practices, or behaviors.
Part: Resolve a conflict in meaning encountered in a written translation.
Type: DISCRETE
Work item: one meaning conflict resolved for a written translation
Start: an ambiguity or conflicting meaning is identified
End: the intended meaning and suitable rendering are determined
Checked by: the translator or translation reviewer
Three coders' verdicts:
  Coder 1: best gdpval (partial); second none (none). Reasoning: GDPval has written professional deliverables, which shares the text work, but no benchmark tests resolving meaning in translation.
  Coder 2: best none (none); second none (none). Reasoning: No benchmark tests translation or meaning disambiguation. GDPval writing deliverables share the text work but are different in kind.
  Coder 3: best officeval (partial); second none (none). Reasoning: OfficeVal includes document annotation and editing, but does not describe resolving bilingual meaning conflicts. No listed benchmark specifically tests this translation judgment.

[9333a]
Occupation: Interpreters and Translators
Task statement: Compile terminology and information to be used in translations, including technical terms such as those for legal or medical material.
Part: Compile a glossary of terminology and information for a translation project, including legal or medical terms.
Type: DISCRETE
Work item: one project glossary or termbase
Start: project terminology needs identified
End: glossary delivered or loaded to the termbase
Checked by: translation team; client
Three coders' verdicts:
  Coder 1: best jobbench (partial); second gdpval (partial). Reasoning: JobBench has professional requests built from real files with a checklist, which shares the research-and-compile action, but it is not linguistic work. GDPval is similar in producing a document from reference files.
  Coder 2: best gdpval (partial); second none (none). Reasoning: GDPval has professional reference-style deliverables from source files, which shares the compile-from-sources action. No benchmark covers termbase work.
  Coder 3: best officeval (partial); second none (none). Reasoning: OfficeVal includes extracting information from documents into a table, but it does not specifically require bilingual terminology research or validation. No other listed benchmark closely tests building a translation termbase.

[9336a]
Occupation: Interpreters and Translators
Task statement: Check original texts or confer with authors to ensure that translations retain the content, meaning, and feeling of the original material.
Part: Check original texts or confer with the author to confirm a translation keeps the content, meaning and feeling of the original.
Type: DISCRETE
Work item: one translation checked against its original or author
Start: query or doubt about the original raised
End: author's answer applied or the translation confirmed
Checked by: client; author
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark involves translation checking. GDPval has language-related professional work but the match is weak.
  Coder 2: best gdpval (partial); second officeval (partial). Reasoning: GDPval includes professional writing and correction tasks from reference files, which shares reading a text against a source and editing it. No benchmark has translation.
  Coder 3: best officeval (partial); second none (none). Reasoning: OfficeVal includes document annotation and revision, sharing the act of editing an existing file. It does not specifically test bilingual comparison or author clarification, and no other listed benchmark is close to translation checking.

[9339a]
Occupation: Interpreters and Translators
Task statement: Adapt software and accompanying technical documents to another language and culture.
Part: Adapt software language and cultural content for another locale.
Type: DISCRETE
Work item: one assigned software resource set localized
Start: software resources and target-locale requirements received
End: localized resources submitted for integration or review
Checked by: the localization team, software developers, or client
Three coders' verdicts:
  Coder 1: best swe_lancer (partial); second none (none). Reasoning: SWE-Lancer has code changes to a commercial app including text fixes, which shares editing resources, but no benchmark covers localization.
  Coder 2: best none (none); second none (none). Reasoning: No benchmark tests translation or localization, though SWE-Lancer touches UI text consistency in an app and GDPval has written deliverables. They differ since this work is linguistic rather than code.
  Coder 3: best officeval (partial); second none (none). Reasoning: OfficeVal includes editing supplied files while preserving their integrity, but it does not specifically test translation or software localization. No listed benchmark closely matches adapting software resources for a locale.

[1641b]
Occupation: Paralegals and Legal Assistants
Task statement: Keep and monitor legal volumes to ensure that the law library is up-to-date.
Part: Check whether legal library volumes are current and identify needed updates.
Type: DISCRETE
Work item: one legal title checked for needed updates
Start: title or publisher update information selected for review
End: title's currency established and any needed update identified
Checked by: library staff or supervising attorney
Three coders' verdicts:
  Coder 1: best officeval (partial); second none (none). Reasoning: No benchmark involves checking publication currency; the nearest is OfficeVal for comparing and annotating documents.
  Coder 2: best none (none); second none (none). Reasoning: No benchmark involves checking a library title for currency. Online-Mind2Web has website lookup but of a different kind.
  Coder 3: best online_mind2web (partial); second osworld_verified (partial). Reasoning: Online-Mind2Web includes finding information on a named live website, but it does not specifically compare legal holdings with publisher updates. OSWorld includes checking information through desktop applications, though its goals are generally simpler than legal-library currency control.

[1642a]
Occupation: Paralegals and Legal Assistants
Task statement: Appraise and inventory real and personal property for estate planning.
Part: Appraise and inventory a client's real and personal property for an estate plan.
Type: DISCRETE
Work item: one estate asset inventory with values
Start: attorney asks for property inventory for a client's estate plan
End: valued inventory delivered to the attorney
Checked by: supervising attorney; client
Three coders' verdicts:
  Coder 1: best finch (partial); second jobbench (partial). Reasoning: Finch involves compiling figures across files into a workbook, and JobBench has professional requests with real file folders.
  Coder 2: best jobbench (partial); second gdpval (partial). Reasoning: JobBench has professional requests with folders of records tied to one O*NET task and checklist grading, which shares the main action of assembling findings from files. GDPval has legal-support deliverables.
  Coder 3: best apex_agents (partial); second officeval (partial). Reasoning: APEX-Agents includes legal and financial tasks that extract and organize information from firm records, but it does not specifically describe estate inventory valuation. OfficeVal includes extracting document data into tables without the estate-planning judgment.

[7358a]
Occupation: Tax Preparers
Task statement: Compute taxes owed or overpaid, using adding machines or personal computers, and complete entries on forms, following tax form instructions and tax tables.
Part: Compute tax owed or overpaid and enter the figures on tax forms while the client waits.
Type: LIVE_SERVICE
Work item: One return's tax calculations and form entries made during an appointment
Start: Required figures are available during the client appointment
End: Tax owed or overpaid is computed and entered on the forms during the appointment
Checked by: Client and return reviewer
Three coders' verdicts:
  Coder 1: best ui_cube (partial); second officeval (partial). Reasoning: UI-CUBE has entering given data into enterprise application forms, which shares the data-entry action. No benchmark covers tax computation.
  Coder 2: best apex_accounting (partial); second ui_cube (partial). Reasoning: APEX-Accounting has calculating and entering figures from source documents, which shares the main actions. UI-CUBE has entering data into forms in enterprise apps, but without tax rules.
  Coder 3: best sopbench (partial); second apex_accounting (partial). Reasoning: SOPBench tests rule-governed transactions during service requests, but does not specifically calculate and enter a tax return. APEX-Accounting covers financial calculations and entries, but is an asynchronous month-end accounting workflow.

[7360a]
Occupation: Tax Preparers
Task statement: Use all appropriate adjustments, deductions, and credits to keep clients' taxes to a minimum.
Part: Identify and apply appropriate adjustments, deductions, and credits while preparing a return with the client present.
Type: LIVE_SERVICE
Work item: One return's tax benefits selected and applied during an appointment
Start: Client's relevant tax information is available during the appointment
End: Applicable adjustments, deductions, and credits are applied during the appointment
Checked by: Client and return reviewer
Three coders' verdicts:
  Coder 1: best tau_retail_airline (partial); second sopbench (partial). Reasoning: τ-bench has live service work following a policy and entering changes in a system, which shares the main action. SOPBench requires following a written procedure with system tools.
  Coder 2: best sopbench (partial); second none (none). Reasoning: SOPBench has a customer request handled with a written procedure and system tools, sharing the guided workflow. No benchmark covers tax preparation.
  Coder 3: best gdpval (partial); second eva_bench (partial). Reasoning: GDPval includes professional accounting-style deliverables, but it does not specifically model selecting tax benefits with a client present. EVA-Bench involves live service with system updates, but its scenarios are not tax preparation.

[7360b]
Occupation: Tax Preparers
Task statement: Use all appropriate adjustments, deductions, and credits to keep clients' taxes to a minimum.
Part: Identify and apply appropriate adjustments, deductions, and credits while preparing a return in the office.
Type: DISCRETE
Work item: One return's tax benefits selected and applied in the office
Start: Client's relevant tax information is available for review
End: Applicable adjustments, deductions, and credits are applied to the return
Checked by: Return reviewer and client
Three coders' verdicts:
  Coder 1: best dualentry (partial); second finch (partial). Reasoning: DualEntry has classifying items to the right accounts under rules, sharing rule-based classification. Finch has data validation workflows.
  Coder 2: best apex_accounting (partial); second jobbench (partial). Reasoning: No benchmark covers tax software, so the nearest involve preparing financial records in a system. APEX-Accounting has accountant-checked entries in an accounting system, and JobBench has professional requests tied to O*NET tasks.
  Coder 3: best terminal_bench_4 (partial); second apex_accounting (partial). Reasoning: Terminal-Bench 3.0/4.x includes processing claims against rules and preparing compliance outputs, but not individual tax-benefit selection in tax software. APEX-Accounting also applies accounting rules to financial records, but is not a tax-return preparation benchmark.

[7361a]
Occupation: Tax Preparers
Task statement: Interview clients to obtain additional information on taxable income and deductible expenses and allowances.
Part: Interview a client to obtain missing information on income, expenses and allowances.
Type: LIVE_SERVICE
Work item: one client interview during an appointment or call
Start: client begins answering questions
End: information obtained and noted for the return
Checked by: preparer; reviewer
Three coders' verdicts:
  Coder 1: best tau_retail_airline (partial); second sopbench (partial). Reasoning: τ-bench has live exchanges where the worker asks the customer questions and enters results into a system under a policy. SOPBench is following a procedure in a customer request.
  Coder 2: best sopbench (partial); second eva_bench (partial). Reasoning: SOPBench has customer requests following a procedure with system tools, sharing the live-conversation action, but here the worker collects information rather than acting on a request. EVA-Bench has phone calls that query records.
  Coder 3: best eva_bench (partial); second sopbench (partial). Reasoning: EVA-Bench involves live calls that gather information and update records, but its settings are not tax preparation. SOPBench also combines information gathering and procedural record handling but is not specifically a tax interview.

[7362a]
Occupation: Tax Preparers
Task statement: Review financial records, such as income statements and documentation of expenditures to determine forms needed to prepare tax returns.
Part: Review a client's financial records during an appointment to determine which tax forms are needed.
Type: LIVE_SERVICE
Work item: One client's records reviewed for required tax forms during an appointment
Start: Client presents or discusses financial records during the appointment
End: Needed forms are identified during the appointment
Checked by: Tax preparer and client
Three coders' verdicts:
  Coder 1: best tau_retail_airline (partial); second jobbench (partial). Reasoning: No benchmark covers live tax intake; tau_retail_airline is a live exchange under policy. JobBench has the records-to-forms reasoning but is not live.
  Coder 2: best none (none); second none (none). Reasoning: No benchmark involves identifying forms from a client's records in a live meeting. SOPBench follows procedure for customer requests but is a different task.
  Coder 3: best sopbench (partial); second gdpval (partial). Reasoning: SOPBench involves applying rules to information obtained in a service interaction, but its examples focus on system transactions rather than determining tax forms from financial records. GDPval covers professional financial work, but not a live tax appointment.

[7363a]
Occupation: Tax Preparers
Task statement: Furnish taxpayers with sufficient information and advice to ensure correct tax form completion.
Part: Advise a taxpayer in person or by phone so they can supply what is needed for correct forms.
Type: LIVE_SERVICE
Work item: one taxpayer advised during an appointment or call
Start: taxpayer asks or preparer starts advising
End: taxpayer confirms understanding
Checked by: taxpayer
Three coders' verdicts:
  Coder 1: best sopbench (partial); second tau_retail_airline (partial). Reasoning: SOPBench has customer requests with written procedures and a checked outcome, which resembles guided information gathering. τ-bench chat has policy-guided conversations.
  Coder 2: best tau_banking (partial); second sopbench (partial). Reasoning: τ³ banking knowledge involves finding the right rules in a large policy set and applying them in a customer chat, which is similar. It differs because it makes an account change rather than giving advice. SOPBench also has procedure-following in customer requests.
  Coder 3: best eva_bench (partial); second sopbench (partial). Reasoning: EVA-Bench involves live calls with information lookup and accurate advice, but its settings do not include tax preparation. SOPBench similarly uses policy-guided service requests but is not specifically a taxpayer-advice appointment.

[7365a]
Occupation: Tax Preparers
Task statement: Calculate form preparation fees according to return complexity and processing time required.
Part: Calculate a return preparation fee while the client is present or on the line.
Type: LIVE_SERVICE
Work item: One preparation fee calculated during a client contact
Start: Return complexity and processing time are available during the contact
End: Fee is calculated and communicated to the client
Checked by: Client and practice staff
Three coders' verdicts:
  Coder 1: best sopbench (partial); second tau_retail_airline (partial). Reasoning: SOPBench has a customer request handled under a written procedure with a checked outcome, which resembles quoting under a fee policy, but there is no system change. τ-bench chat requires policy-following with tools, which is close but is about orders.
  Coder 2: best tau_retail_airline (partial); second sopbench (partial). Reasoning: Tau-bench has live customer contacts applying a policy, matching quoting under a schedule. SOPBench is a procedure-following service request.
  Coder 3: best tau_voice (partial); second eva_bench (partial). Reasoning: τ-Voice covers live customer conversations using company rules and tools, but does not specifically calculate tax-preparation fees. EVA-Bench also involves live service calls and system lookups in different service settings.

[7366a]
Occupation: Tax Preparers
Task statement: Check data input or verify totals on forms prepared by others to detect errors in arithmetic, data entry, or procedures.
Part: Check a return prepared by someone else for errors in arithmetic, entry or procedure.
Type: DISCRETE
Work item: one return reviewed and corrected
Start: prepared return handed over for review
End: return verified with errors corrected or flagged
Checked by: preparer; client
Three coders' verdicts:
  Coder 1: best spreadsheetbench_2 (partial); second finch (partial). Reasoning: SpreadsheetBench 2 has finding and fixing errors in business workbooks, which is the same checking action. Finch includes validation of figures across files.
  Coder 2: best apex_accounting (partial); second dualentry (partial). Reasoning: APEX-Accounting has checking and correcting of financial records against a checklist, sharing the verification action, but not tax returns. DualEntry has exact-answer bookkeeping cases which are far smaller.
  Coder 3: best gdpval (partial); second apex_accounting (partial). Reasoning: GDPval includes professional accounting deliverables and can involve reviewing financial material, but it does not specifically model tax-return review and correction. APEX-Accounting also involves checking financial records and calculations, though its focus is month-end accounting rather than tax returns.

[20363a]
Occupation: Tax Preparers
Task statement: Answer questions and provide future tax planning to clients.
Part: Answer a client's tax question during a live contact.
Type: LIVE_SERVICE
Work item: One client's tax question answered during a live contact
Start: Client asks a tax question
End: Answer is provided or the next step is explained during the contact
Checked by: Client
Three coders' verdicts:
  Coder 1: best sopbench (partial); second tau_retail_airline (partial). Reasoning: SOPBench has customers asking for service answered under procedures with tools, and Tau-bench is a similar live conversation with policy lookup.
  Coder 2: best tau_banking (partial); second sopbench (partial). Reasoning: Tau banking has the worker apply a policy to a customer's account question in a chat, similar to answering a rules question from a client, but it ends in an account change. SOPBench has procedure-following over a customer request.
  Coder 3: best eva_bench (partial); second sopbench (partial). Reasoning: EVA-Bench tests live phone interactions that provide accurate information and use relevant records, but its domains do not include tax advice. SOPBench also tests policy-based answers and actions, though its examples are service procedures rather than tax-law advice.

[20363c]
Occupation: Tax Preparers
Task statement: Answer questions and provide future tax planning to clients.
Part: Provide future tax-planning advice during a client consultation.
Type: LIVE_SERVICE
Work item: One live tax-planning consultation
Start: Client's future tax-planning needs are raised during a consultation
End: Planning advice and relevant next steps are discussed with the client
Checked by: Client
Three coders' verdicts:
  Coder 1: best tau_retail_airline (partial); second none (none). Reasoning: No benchmark covers live tax advisory conversations; tau_retail_airline is a live chat under a policy but with database changes rather than advice. GDPval has accountant-style deliverables but is not live.
  Coder 2: best none (none); second tau_banking (partial). Reasoning: No benchmark has live tax advice. Tau-bench conversations apply policy to accounts but do not advise on planning, and Vals Finance Agent answers finance questions without a live client.
  Coder 3: best tau_voice (partial); second tau_banking (partial). Reasoning: τ-Voice tests live conversations using policies and account information, but its service requests are not individualized future tax planning. τ³-bench banking also applies detailed rules to customer facts, but in chat and for banking account actions.

[20364a]
Occupation: Tax Preparers
Task statement: Explain federal and state tax laws to individuals and companies.
Part: Explain federal or state tax law to an individual or company during a live contact.
Type: LIVE_SERVICE
Work item: One live explanation of tax law to a client
Start: Client's need for an explanation is raised
End: Relevant law is explained during the contact
Checked by: Client
Three coders' verdicts:
  Coder 1: best vals_finance_agent (partial); second tau_retail_airline (partial). Reasoning: SOPBench and τ-bench are policy-following conversations, but they change records, while this is only an explanation. Vals Finance Agent answers expert questions from documents, which matches the knowledge component.
  Coder 2: best tau_retail_airline (partial); second sopbench (partial). Reasoning: Tau-bench chat/voice has the worker answer a customer under a policy while they wait, similar in form. SOPBench uses a written procedure in a service setting.
  Coder 3: best eva_bench (partial); second tau_banking (partial). Reasoning: EVA-Bench covers live calls requiring correct information and system lookup, but its domains do not include tax law. Tau banking similarly combines policy research and account facts in a customer conversation, though it concerns banking policies rather than tax law.

[2880a]
Occupation: Electricians
Task statement: Plan layout and installation of electrical wiring, equipment, or fixtures, based on job specifications and local codes.
Part: Plan the layout and installation of wiring and fixtures from job specs and local codes.
Type: DISCRETE
Work item: one installation layout plan for a job
Start: job specs received
End: layout plan ready for installation
Checked by: foreman; code inspector
Three coders' verdicts:
  Coder 1: best jobbench (partial); second gdpval (partial). Reasoning: JobBench has professional requests with source files that need checks against standards, which shares the code-checking work. It does not involve physical layout drawings.
  Coder 2: best gdpval (partial); second none (none). Reasoning: GDPval has professional work requests from specs, which shares planning from a brief, but no benchmark covers wiring layout. The match is weak.
  Coder 3: best osworld_verified (partial); second none (none). Reasoning: OSWorld includes producing and modifying files in desktop applications, but its goals do not specifically involve electrical installation design. No listed benchmark closely tests a code-compliant electrical layout plan.

[2885a]
Occupation: Electricians
Task statement: Perform business management duties, such as maintaining records or files, preparing reports, or ordering supplies or equipment.
Part: Maintain records and prepare reports on jobs.
Type: DISCRETE
Work item: one job's records and report completed
Start: job finished
End: records filed or report sent
Checked by: owner; customer
Three coders' verdicts:
  Coder 1: best gdpval (partial); second none (none). Reasoning: GDPval includes admin and order-clerk style deliverables, which share the record-writing work. No benchmark is specific to trade job records.
  Coder 2: best osworld_2 (partial); second theagentcompany (partial). Reasoning: OSWorld 2.0 has office workflows that gather data from documents and file it in portals, which shares the main actions of compiling job data and filing, but it is more admin-heavy and not trade-specific. APEX-Accounting has record preparation but for month-end close.
  Coder 3: best ui_cube (partial); second osworld_2 (partial). Reasoning: UI-CUBE covers entering business data into enterprise applications, resembling recording completed job information. It does not specifically cover electrician job records and customer reports.

[2885b]
Occupation: Electricians
Task statement: Perform business management duties, such as maintaining records or files, preparing reports, or ordering supplies or equipment.
Part: Order supplies or equipment.
Type: DISCRETE
Work item: one supply order placed
Start: need identified
End: order confirmed
Checked by: owner; supplier
Three coders' verdicts:
  Coder 1: best online_mind2web (partial); second webarena (partial). Reasoning: Online-Mind2Web tasks find items on live websites and set options, which shares the search-and-order actions. They use consumer sites, not trade supplier accounts, and WebArena has store tasks on a self-hosted shop.
  Coder 2: best webarena (partial); second online_mind2web (partial). Reasoning: WebArena has shopping and store tasks on web storefronts, which matches placing an order online, though it is a self-hosted store. Online-Mind2Web has tasks on live shopping sites.
  Coder 3: best workarena_pp (partial); second online_mind2web (partial). Reasoning: WorkArena++ includes placing orders after checking business information, but its examples concern service-catalog and office purchases rather than electrical supplies. Online-Mind2Web also involves finding products or services on live sites, though not necessarily completing a business supply order.

[2892a]
Occupation: Electricians
Task statement: Provide preliminary sketches or cost estimates for materials or services.
Part: Provide a preliminary sketch for a job.
Type: DISCRETE
Work item: one preliminary sketch
Start: customer requests job
End: sketch given
Checked by: customer
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark involves producing sketches or drawings.
  Coder 2: best gdpval (partial); second none (none). Reasoning: GDPval has professional deliverables from a brief, which shares producing a customer-facing work product, but a hand sketch of a wiring layout is not a document or spreadsheet. No other benchmark involves drawing a sketch.
  Coder 3: best osworld_verified (partial); second none (none). Reasoning: OSWorld includes drawing or image-editing actions in desktop applications. It does not specifically involve site assessment or an electrician's preliminary job sketch.

[1843b]
Occupation: Registered Nurses
Task statement: Consult and coordinate with healthcare team members to assess, plan, implement, or evaluate patient care plans.
Part: Consult a physician or other team member about a specific patient issue and agree on a plan.
Type: DISCRETE
Work item: one patient-specific consult or coordination exchange
Start: nurse contacts team member
End: plan or order agreed and noted
Checked by: physician, other team member
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark covers clinical coordination; HealthAdminBench is clinical admin work in records systems, which only overlaps in the recording step.
  Coder 2: best theagentcompany (partial); second none (none). Reasoning: TheAgentCompany has tasks involving messaging colleagues and recording outcomes. EVA-Bench is a live call, which differs.
  Coder 3: best eva_bench (partial); second healthadminbench (partial). Reasoning: EVA-Bench includes live coordination with system lookups and record updates, but its service-desk settings do not cover clinical decision-making. HealthAdminBench uses hospital records, though its tasks concern revenue-cycle administration rather than agreeing a patient care plan.

[1845b]
Occupation: Registered Nurses
Task statement: Monitor all aspects of patient care, including diet and physical activity.
Part: Review recorded aspects of a patient's care, including diet and activity.
Type: DISCRETE
Work item: one patient's care review for a shift or review period
Start: care records and observations for the period are available
End: review and any issues requiring follow-up are documented or communicated
Checked by: the patient's care team
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark involves clinical record review. HealthAdminBench uses a hospital records system but for revenue cycle work.
  Coder 2: best gdpval (partial); second healthadminbench (partial). Reasoning: HealthAdminBench works in hospital records but on revenue-cycle tasks rather than clinical review. GDPval has nursing-type work with documents, which shares reading records and writing a summary.
  Coder 3: best healthadminbench (partial); second none (none). Reasoning: HealthAdminBench uses hospital records, but its tasks concern revenue-cycle administration rather than clinical nursing review. No other listed benchmark closely matches reviewing a patient's care over a shift.

[1846b]
Occupation: Registered Nurses
Task statement: Direct or supervise less-skilled nursing or healthcare personnel or supervise a particular unit.
Part: Make the shift's patient assignments and delegate tasks to staff.
Type: DISCRETE
Work item: one shift's assignment sheet
Start: start-of-shift staffing known
End: assignments communicated to staff
Checked by: nurse manager, staff
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: Nothing in the list involves staffing allocation; the closest is TheAgentCompany with HR/admin planning tasks, but with a very different setting.
  Coder 2: best gdpval (partial); second none (none). Reasoning: GDPval includes scheduling and staffing-style deliverables from a brief, similar to producing a sheet. No benchmark covers clinical assignment.
  Coder 3: best workarena_pp (partial); second crmarena_pro (partial). Reasoning: WorkArena++ includes assigning work using staff and workload records, but not clinical acuity or nursing delegation. CRMArena-Pro also includes routing cases to suitable agents without the patient-safety constraints.

[1857b]
Occupation: Registered Nurses
Task statement: Conduct specified laboratory tests.
Part: Enter and communicate the result of a specified laboratory test.
Type: DISCRETE
Work item: one laboratory test or panel result entered and released
Start: test result is available
End: result is recorded and made available to the care team
Checked by: the ordering clinician and laboratory or nursing supervisor
Three coders' verdicts:
  Coder 1: best healthadminbench (partial); second dualentry (partial). Reasoning: HealthAdminBench works in a hospital records system, entering and recording clinical data accurately, which is the closest in action. DualEntry cases also require exact transcription of values into the right fields but in accounting.
  Coder 2: best workarena_l1 (partial); second healthadminbench (partial). Reasoning: HealthAdminBench has recording values in health systems; WorkArena single actions are entering records with given fields.
  Coder 3: best ui_cube (partial); second healthadminbench (partial). Reasoning: UI-CUBE tests transferring supplied data into application records, but does not specifically involve clinical result verification and release. HealthAdminBench uses healthcare systems but targets administrative rather than laboratory-result workflows.

[2337a]
Occupation: Childcare Workers
Task statement: Keep records on individual children, including daily observations and information about activities, meals served, and medications administered.
Part: Write a child's daily record, including observations, meals and medications.
Type: DISCRETE
Work item: one child's daily record
Start: day's activities occur
End: record completed
Checked by: parents, director, licensing inspector
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark involves writing child records; the nearest is TheAgentCompany with record-keeping in company systems, which is very different in content. GDPval produces documents but not daily logs.
  Coder 2: best gdpval (partial); second none (none). Reasoning: GDPval has written records produced by workers in many occupations, which shares the main action of writing a structured record from known facts, but there is no benchmark for child-care logs. TheAgentCompany has record-keeping tasks but in software-company tools.
  Coder 3: best ui_cube (partial); second healthadminbench (partial). Reasoning: UI-CUBE tests entering information into application records, but does not require observing a child throughout the day or documenting medication safely. HealthAdminBench also updates healthcare-related systems but focuses on administrative revenue-cycle work.

[18757a]
Occupation: Childcare Workers
Task statement: Communicate with children's parents or guardians about daily activities, behaviors, and related issues.
Part: Update a parent verbally at drop-off or pickup.
Type: LIVE_SERVICE
Work item: one parent update at drop-off or pickup
Start: parent arrives
End: parent leaves with the child informed
Checked by: parent
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark involves in-person parent updates. The service benchmarks are about system actions.
  Coder 2: best tau_retail_airline (partial); second none (none). Reasoning: Tau-bench and EVA-Bench are live conversations with customers, which shares the live interaction, but they involve database lookups and changes, unlike a face-to-face update. No benchmark is a face-to-face handover.
  Coder 3: best eva_bench (partial); second none (none). Reasoning: EVA-Bench tests live conversations with information exchange, but its contacts are system-mediated service requests rather than childcare handoffs. No other listed benchmark closely represents an in-person update about a child's day.

[18757b]
Occupation: Childcare Workers
Task statement: Communicate with children's parents or guardians about daily activities, behaviors, and related issues.
Part: Send a parent a written message, daily report or return a call.
Type: DISCRETE
Work item: one written update or callback to a parent
Start: need to communicate arises
End: message sent
Checked by: parent
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark involves writing parent communications. TheAgentCompany has messaging tasks but with different content.
  Coder 2: best gdpval (partial); second theagentcompany (partial). Reasoning: GDPval has short written messages in professional occupations, which shares the main action of writing to a client, but none are childcare updates. TheAgentCompany includes writing messages to colleagues.
  Coder 3: best tau_voice (partial); second gdpval (partial). Reasoning: τ-Voice includes live phone communication with a customer, but its calls are transactional service requests rather than childcare updates. GDPval includes written professional deliverables, but not the described brief parent updates or callbacks.

[18761a]
Occupation: Childcare Workers
Task statement: Perform general administrative tasks, such as taking attendance, editing internal paperwork, and making phone calls.
Part: Take and record children's attendance for a session.
Type: DISCRETE
Work item: one group attendance record for a session
Start: children arrive or the attendance check begins
End: attendance recorded and filed for the session
Checked by: director; licensing inspector
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark involves taking attendance; TheAgentCompany has admin record-keeping tasks, which shares only the record entry. UI-CUBE has entering data in applications.
  Coder 2: best workarena_l1 (partial); second ui_cube (partial). Reasoning: UI-CUBE and WorkArena single actions are simple record entry in applications, which share the form entry, but attendance is taken by observing children in the room. No benchmark involves a physical headcount.
  Coder 3: best ui_cube (partial); second workarena_l1 (partial). Reasoning: UI-CUBE includes entering records from supplied data into enterprise applications, but does not involve observing children's arrival or attendance safety. WorkArena's single-action tasks also include entering specified fields in a system.

[21507a]
Occupation: Accountants and Auditors
Task statement: Collect and analyze data to detect deficient controls, duplicated effort, extravagance, fraud, or non-compliance with laws, regulations, and management policies.
Part: Collect and analyze data to test for control weaknesses, duplicated effort, fraud or non-compliance.
Type: DISCRETE
Work item: one control or fraud test with exceptions documented
Start: test area selected
End: workpaper completed with exceptions listed
Checked by: audit senior or manager
Three coders' verdicts:
  Coder 1: best apex_accounting (partial); second spider2 (partial). Reasoning: APEX-Accounting has reconciliations and checklists in accounting systems and spreadsheets, close to the testing work. Spider 2 has data queries that resemble the data analysis part.
  Coder 2: best terminal_bench_4 (partial); second spider2 (partial). Reasoning: Terminal-Bench 4 includes operations work processing claims against rules and preparing compliance filings, which is similar to testing data against rules and listing exceptions. Spider 2.0 covers analysing large data sets with SQL.
  Coder 3: best jobbench (partial); second apex_accounting (partial). Reasoning: JobBench includes professional analysis of source records against occupation-specific requirements. Its described examples do not specifically test audit controls and document exceptions in a workpaper.

[21519a]
Occupation: Accountants and Auditors
Task statement: Analyze business operations, trends, costs, revenues, financial commitments, and obligations to project future revenues and expenses or to provide advice.
Part: Analyze business information to project future revenues and expenses.
Type: DISCRETE
Work item: one revenue and expense forecast
Start: historical data, commitments, and forecast assumptions are gathered
End: forecast and assumptions are submitted
Checked by: management or finance manager
Three coders' verdicts:
  Coder 1: best spreadsheetbench_2 (partial); second finch (partial). Reasoning: SpreadsheetBench 2 builds or extends financial models across sheets, sharing the main action, but to a specification. Finch has finance workflows with calculation and a short report.
  Coder 2: best finch (good); second vals_emb (partial). Reasoning: Finch items pull figures across workbooks and calculate and write up results from company data, which is the same kind of work. Vals Excel Modeling builds a full model but to a given specification.
  Coder 3: best vals_emb (good); second spreadsheetbench_2 (partial). Reasoning: Vals Excel Modeling includes building an operating model from source information and assumptions, closely matching the spreadsheet forecasting work. SpreadsheetBench 2 also covers extending financial models, although its individual tasks can be narrower than a full forecast.

[21522a]
Occupation: Accountants and Auditors
Task statement: Evaluate taxpayer finances to determine tax liability, using knowledge of interest and discount rates, annuities, valuation of stocks and bonds, and amortization valuation of depletable assets.
Part: Evaluate a taxpayer's finances to determine tax liability.
Type: DISCRETE
Work item: one tax liability analysis
Start: records received
End: computation completed
Checked by: reviewer, taxpayer or client
Three coders' verdicts:
  Coder 1: best finch (partial); second gdpval (partial). Reasoning: Finch includes computing and validating figures across workbooks, and GDPval includes accountant deliverables. Neither is specifically tax computation.
  Coder 2: best jobbench (partial); second apex_accounting (partial). Reasoning: JobBench items are professional analyses over real files that are checked against an expert checklist, which shares the compute-from-records work. APEX-Accounting is accounting calculations from company records but not tax.
  Coder 3: best gdpval (partial); second apex_accounting (partial). Reasoning: GDPval includes realistic accounting and tax-related professional deliverables, but it spans many tasks rather than specifically computing a taxpayer's liability. APEX-Accounting includes financial calculations and accounting-system work, though it focuses on company close rather than tax liability analysis.

[21526a]
Occupation: Accountants and Auditors
Task statement: Compute taxes owed and prepare tax returns, ensuring compliance with payment, reporting, or other tax requirements.
Part: Compute taxes owed and prepare the return.
Type: DISCRETE
Work item: one tax return
Start: documents received
End: return filed
Checked by: client and tax authority
Three coders' verdicts:
  Coder 1: best osworld_2 (partial); second apex_accounting (partial). Reasoning: OSWorld 2.0 includes extracting data from documents and filing in portals, which shares the main actions. APEX-Accounting has accountant-written checklists for accounting outputs.
  Coder 2: best apex_accounting (partial); second terminal_bench_4 (partial). Reasoning: APEX-Accounting has preparing schedules and calculations from records, which is the closest. Terminal-Bench 4 has preparing a compliance filing by script, but is done at a command line.
  Coder 3: best jobbench (partial); second gdpval (partial). Reasoning: JobBench includes occupation-specific professional work using source records and expert-graded deliverables. Its described tasks do not specifically cover end-to-end tax return preparation and filing.

[21528b]
Occupation: Accountants and Auditors
Task statement: Represent clients before taxing authorities and provide support during litigation involving financial issues.
Part: Prepare written responses to authorities or litigation analyses.
Type: DISCRETE
Work item: one written response or support analysis
Start: notice or request received
End: response sent
Checked by: client, authority or attorney
Three coders' verdicts:
  Coder 1: best gdpval (partial); second apex_agents (partial). Reasoning: GDPval and APEX-Agents have professionals writing a response or analysis from files, sharing the main action. Neither is an authority response.
  Coder 2: best jobbench (partial); second apex_accounting (partial). Reasoning: JobBench has professional requests with real files and an expert checklist, which shares the analyse-and-write action. APEX-Accounting has accounting analysis with documents.
  Coder 3: best apex_agents (partial); second jobbench (partial). Reasoning: APEX-Agents includes financial and legal analysis from firm materials, but does not specifically model responses to taxing authorities. JobBench similarly tests occupation-specific analysis from source files without necessarily covering a live dispute.

[21533a]
Occupation: Accountants and Auditors
Task statement: Process invoices for payment.
Part: Process an invoice for payment.
Type: DISCRETE
Work item: one invoice processed
Start: invoice received
End: queued for payment
Checked by: AP supervisor and vendor
Three coders' verdicts:
  Coder 1: best starshell (partial); second dualentry (partial). Reasoning: StarShell creates invoices and linked documents in ERPNext, which shares the action of entering a business document in an ERP, but it is sales rather than payables processing. DualEntry covers accounts-payable entries but as data cases rather than operating a system.
  Coder 2: best dualentry (good); second apex_accounting (good). Reasoning: DualEntry has bookkeeping cases on accounts-payable entries and classification, which is the same kind of work. APEX-Accounting has entering transactions in an accounting system.
  Coder 3: best apex_accounting (good); second dualentry (partial). Reasoning: APEX-Accounting includes entering transactions and handling accounting records using source documents and systems, closely matching invoice processing. DualEntry includes accounts-payable cases but is a short data classification exercise rather than a complete system workflow.

[3778b]
Occupation: Lawyers
Task statement: Gather evidence to formulate defense or to initiate legal actions by such means as interviewing clients and witnesses to ascertain the facts of a case.
Part: Collect documents and other evidence.
Type: DISCRETE
Work item: one evidence collection
Start: request made
End: evidence indexed
Checked by: supervising attorney
Three coders' verdicts:
  Coder 1: best officeval (partial); second jobbench (partial). Reasoning: OfficeVal has extracting data from documents into a table, and JobBench has case folders of files; neither includes collecting from others.
  Coder 2: best theagentcompany (partial); second apex_agents (partial). Reasoning: TheAgentCompany has collecting files and organising them across a shared system. APEX-Agents has finding items in firm files.
  Coder 3: best apex_agents (partial); second theagentcompany (partial). Reasoning: APEX-Agents includes legal work involving locating and organizing information across firm files. Its described tasks do not specifically collect and index evidence for litigation.

[3785c]
Occupation: Lawyers
Task statement: Prepare legal briefs and opinions, and file appeals in state and federal courts of appeal.
Part: File an appeal in a state or federal appellate court.
Type: DISCRETE
Work item: one appeal initiation filing
Start: decision to appeal and filing requirements established
End: required initiation documents submitted to the appellate court
Checked by: court clerk and supervising lawyer
Three coders' verdicts:
  Coder 1: best apex_agents (partial); second healthadminbench (partial). Reasoning: APEX-Agents includes drafting legal documents for corporate lawyers, matching the drafting part. HealthAdminBench has a filing on a portal, but in healthcare.
  Coder 2: best healthadminbench (partial); second apex_agents (partial). Reasoning: HealthAdminBench files documents through payer portals, similar to filing. APEX-Agents drafts legal documents.
  Coder 3: best osworld_2 (partial); second none (none). Reasoning: OSWorld 2.0 includes assembling information and submitting it through an application portal, but its examples do not involve appellate filings or legal deadlines. No other listed benchmark is closer to this filing workflow.

[3788a]
Occupation: Lawyers
Task statement: Search for and examine public and other legal records to write opinions or establish ownership.
Part: Search and examine legal records to establish ownership.
Type: DISCRETE
Work item: one ownership or title search finding
Start: property or asset and search scope identified
End: ownership findings documented or communicated
Checked by: client, supervising lawyer, or transaction team
Three coders' verdicts:
  Coder 1: best osworld_2 (partial); second gdpval (partial). Reasoning: OSWorld 2.0 has workflows that gather data from portals and documents, cross-check them and produce a record, which shares the main actions, but not in a legal-title setting. GDPval has written findings from reference files but without searching records.
  Coder 2: best vals_finance_agent (partial); second online_mind2web (partial). Reasoning: Vals Finance Agent has research questions answered from public filings found on the web, which shares the main action of searching public records and documenting a finding. Online-Mind2Web has live website navigation.
  Coder 3: best jobbench (partial); second apex_agents (partial). Reasoning: JobBench uses public-record files for expert professional tasks, sharing the source-review and finding-documentation pattern but not specifically title searching. APEX-Agents includes legal tasks in firm files, though its described examples are not ownership searches.

[3790c]
Occupation: Lawyers
Task statement: Perform administrative and management functions related to the practice of law.
Part: Open and close matters, run conflict checks, file.
Type: DISCRETE
Work item: one matter opened or closed
Start: new matter
End: file complete
Checked by: firm
Three coders' verdicts:
  Coder 1: best ui_cube (partial); second workarena_l1 (partial). Reasoning: WorkArena and UI-CUBE tasks create records with given fields in enterprise systems, which fits the data-entry part. They don't include the conflict analysis.
  Coder 2: best starshell (partial); second theagentcompany (partial). Reasoning: StarShell and UI-CUBE are record creation and updates across business systems, matching opening a matter. TheAgentCompany has admin tasks across a file share.
  Coder 3: best workarena_pp (partial); second theagentcompany (partial). Reasoning: WorkArena++ involves multi-step administrative workflows that create and check related system records. It does not specifically perform legal matter intake, conflict checks, or closure.

[3792c]
Occupation: Lawyers
Task statement: Probate wills and represent and advise executors and administrators of estates.
Part: Advise an executor or administrator during a live consultation.
Type: LIVE_SERVICE
Work item: one live estate-advice consultation
Start: executor or administrator raises a question during a consultation
End: lawyer explains the advice and the consultation concludes
Checked by: executor or administrator
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark has live legal advice. The service benchmarks are about policy-bound system actions.
  Coder 2: best sopbench (partial); second tau_retail_airline (partial). Reasoning: SOPBench has service conversations that must follow written procedure with the right outcome, which shares live advice under rules, but it is banking and healthcare appointments rather than legal advice. tau-bench has policy-driven chats.
  Coder 3: best tau_voice (partial); second eva_bench (partial). Reasoning: τ-Voice involves live consultations with policy and record lookups, but its retail, airline, and telecom issues differ substantially from individualized estate advice. EVA-Bench similarly tests live service conversations rather than legal consultation.

[1254a]
Occupation: Credit Analysts
Task statement: Complete loan applications, including credit analyses and summaries of loan requests, and submit to loan committees for approval.
Part: Complete a loan application with credit analysis and a summary of the request, and submit it to the loan committee.
Type: DISCRETE
Work item: one loan application package submitted to committee
Start: loan request taken up by the analyst
End: package submitted to the loan committee
Checked by: loan committee
Three coders' verdicts:
  Coder 1: best finch (partial); second apex_agents (partial). Reasoning: Finch involves workbooks, calculation and a written report for finance experts, and APEX-Agents has analyst deliverables.
  Coder 2: best apex_agents (partial); second jobbench (partial). Reasoning: APEX-Agents has analysts reading firm files and producing analyses or drafts against expert criteria, sharing the main work. JobBench has professional analysis requests with source files.
  Coder 3: best gdpval (partial); second apex_agents (partial). Reasoning: GDPval includes realistic professional financial deliverables based on source files, resembling a credit package but not specifically a committee loan application. APEX-Agents includes financial analysis and modeling, but its scenarios focus on investment banking rather than loan underwriting.

[6664a]
Occupation: Secondary School Teachers, Except Special and Career/Technical Education
Task statement: Select, store, order, issue, and inventory classroom equipment, materials, and supplies.
Part: Pick supplies and place orders.
Type: DISCRETE
Work item: one supply order
Start: need identified
End: order placed
Checked by: department head or purchasing
Three coders' verdicts:
  Coder 1: best online_mind2web (partial); second theagentcompany (partial). Reasoning: Online-Mind2Web tasks involve searching a shopping website and selecting items to conditions, which shares browsing and picking, but not budgets or approval processes. TheAgentCompany has procurement-style tasks with price lookups but in chat and files.
  Coder 2: best workarena_l1 (partial); second online_mind2web (partial). Reasoning: WorkArena level 1 has ordering items from a service catalog, which shares the main action of placing an order in a web system. Online-Mind2Web has shopping on websites.
  Coder 3: best workarena_pp (partial); second workarena_l1 (partial). Reasoning: WorkArena++ includes determining what to order and placing orders through an enterprise system, which shares the main actions. WorkArena also includes ordering an item from a service catalog, usually with explicit instructions.

[8113a]
Occupation: Sales Representatives, Wholesale and Manufacturing, Except Technical and Scientific Products
Task statement: Answer customers' questions about products, prices, availability, product uses, and credit terms.
Part: Answer a customer's question by phone or in person.
Type: LIVE_SERVICE
Work item: one customer question answered live
Start: customer asks
End: customer has the answer
Checked by: customer
Three coders' verdicts:
  Coder 1: best tau_voice (partial); second tau_retail_airline (partial). Reasoning: tau-Voice has live calls in which the worker looks things up and answers under policy, which shares the main actions, but the benchmark checks database changes. tau-bench chat is the same task by text.
  Coder 2: best tau_retail_airline (partial); second crmarena_pro (partial). Reasoning: Tau-bench has chats where the worker looks up information and answers under a policy. CRMArena-Pro has answering questions from CRM data.
  Coder 3: best crmarena_pro (partial); second tau_voice (partial). Reasoning: CRMArena-Pro includes answering company knowledge-base questions and handling sales-related requests. It is not specifically a live wholesale product conversation and may involve different CRM tasks.

[8114a]
Occupation: Sales Representatives, Wholesale and Manufacturing, Except Technical and Scientific Products
Task statement: Recommend products to customers, based on customers' needs and interests.
Part: Recommend products suited to a customer's needs during a live contact.
Type: LIVE_SERVICE
Work item: one product recommendation communicated during a customer contact
Start: customer's needs or interests are discussed
End: suitable product options are recommended to the customer
Checked by: customer
Three coders' verdicts:
  Coder 1: best tau_retail_airline (partial); second crmarena_pro (partial). Reasoning: τ-bench has customer chats where the worker looks up products and orders and advises, but changes records. CRMArena-Pro has answering questions from a company's data.
  Coder 2: best crmarena_pro (partial); second tau_retail_airline (partial). Reasoning: CRMArena-Pro has requests answered from a company's CRM and knowledge base, including conversations where details emerge gradually, which is similar. τ-bench retail has customer chats with product lookups.
  Coder 3: best tau_voice (partial); second crmarena_pro (partial). Reasoning: τ-Voice involves live customer calls and system lookups, but its described tasks concern service changes rather than wholesale product recommendations. CRMArena-Pro includes sales-lead qualification and knowledge-base answers, but is not primarily a live product-recommendation encounter.

[8128b]
Occupation: Sales Representatives, Wholesale and Manufacturing, Except Technical and Scientific Products
Task statement: Plan, assemble, and stock product displays in retail stores, or make recommendations to retailers regarding product displays, promotional programs, and advertising.
Part: Recommend display, promotional, or advertising arrangements to a retailer during a live contact.
Type: LIVE_SERVICE
Work item: one retail display or promotion recommendation given live
Start: retailer discusses display or promotional needs
End: recommendation communicated to the retailer
Checked by: retailer
Three coders' verdicts:
  Coder 1: best none (none); second none (none). Reasoning: No benchmark involves advising a retailer on displays and promotions in a live conversation. The service-call benchmarks are about changing records under policy.
  Coder 2: best tau_retail_airline (partial); second none (none). Reasoning: Tau-bench and EVA-Bench are live conversations while the worker uses tools, which shares the live element, but they follow service policies rather than give sales advice. No benchmark covers merchandising.
  Coder 3: best crmarena_pro (partial); second eva_bench (partial). Reasoning: CRMArena-Pro includes sales-related information gathering and recommendations, but not specifically live merchandising advice. EVA-Bench covers live conversations with system support, though its scenarios do not involve retailer display recommendations.
