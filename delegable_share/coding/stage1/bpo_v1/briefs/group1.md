You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Below are 4 occupations. Code each occupation's TARGETS
independently, in the order given; do not go back and adjust earlier answers to
make them consistent with later ones, and do not let one occupation's coding
shape another's.

For each occupation, write ONE JSON array to its own file:
  Computer Systems Analysts (15-1211.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/bpo_v1/15-1211.00.json
  Bookkeeping, Accounting, and Auditing Clerks (43-3031.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/bpo_v1/43-3031.00.json
  Billing and Posting Clerks (43-3021.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/bpo_v1/43-3021.00.json
  Data Entry Keyers (43-9021.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/bpo_v1/43-9021.00.json
with one element per target, in the order given. Each element is the output
object described in the instructions, with "task_id" added as its first key.
Write nothing else to those files. Then reply "done <n> items" per occupation,
plus at most three sentences on anything you found ambiguous.


=== INSTRUCTIONS ===
You are building a coding schema for occupational tasks. Another team will
later estimate how long each piece of work takes and how it is checked, so
your job is only to say what the units of work ARE.

Describe the work as experienced people in this occupation do it today,
without AI. Do not consider what AI could or could not do.

You will see the occupation's full task list for context, and one TARGET
statement to code. Code only the target.

STEP 1 — SPLIT. Decide whether the target should be split into parts. Split
when it joins different activities ("write training materials, or train
users"), or when it covers very different kinds of item (quick replies and
long investigations). Give each part a share of the target's working time;
shares sum to 1. If no split is needed, there is one part with share 1.

Do NOT split when "or"/"and" only lists alternative methods, tools, or
inputs for the same deliverable. "Check records, call the client, or consult
the policy manual to settle a billing question" is one activity (settling
the question) done by different means.

DO split when the same activity is normally done in two different places:
partly while a customer or user is still on the line or at the desk, and
partly afterwards from written requests or in the back office (see step 4
and Example D).

STEP 2 — CLASSIFY each part as exactly one of:
  - DISCRETE: produces distinct deliverables, one after another.
    Example: answer a user's emailed question about software.
  - ONGOING: a continuing activity with no single deliverable, but which
    produces discrete items (alerts handled, reports written). Name them in
    step 3.
  - LIVE_SERVICE: work done in a live conversation (phone, chat, walk-up)
    with a customer or user, while they wait. This covers the conversation
    itself AND any work done during it while the customer is still there:
    looking up an account, entering an order, taking a payment, issuing a
    refund, booking an appointment.
    Example: take a customer's call about a billing error.
    Example: enter a change-of-address order while the customer is on the
    phone.
  - INTERPERSONAL: the value is in the live interaction itself, and nothing
    a colleague could check is produced (meetings, teaching, negotiating,
    supervising, persuading).
    Example: meet with staff to set requirements.
  - PHYSICAL: needs hands-on work away from a computer.
    Example: install cables.
  - NO_DELIVERABLE: produces nothing anyone else checks or relies on
    (keeping up with developments, reading manuals to stay current).

  If one activity is partly physical and partly at a computer, split it in
  step 1.

STEP 3 — ONGOING parts: replace the activity with the discrete items it
produces (e.g. "one alert investigated", "one weekly capacity report").
If there are several kinds, make each kind its own part with its own share
of time, and classify each as DISCRETE.

STEP 4 — WORK ITEM. For every DISCRETE or LIVE_SERVICE part, name the work
item: one deliverable, in today's workflow, that a worker finishes and that
someone else would check or rely on as a whole. Give:
  - work_item: one line ("one support ticket")
  - start: where it starts ("customer's first message")
  - end: where it ends ("customer confirms the fix, ticket closed")
  - checked_by: who checks or relies on it (supervisor, client, end user,
    downstream team, auditor)
  Pick the level at which work is handed over today: the thing that goes
  into a queue, gets a ticket, gets signed off, or is sent. Not a single
  keystroke-level step, and not a whole project.

  Many task lists describe one workflow in several statements (talk to the
  customer; record the interaction; check the fix was made; refer what you
  can't solve). When the target describes one step of such a workflow, the
  work item is that step's own output (e.g. "one interaction record written
  after a call"), not the whole workflow. The other statements cover the
  other steps.

  Then ask WHERE that step is normally done. If the customer or user is
  still on the line or at the desk while it is done, the part is
  LIVE_SERVICE, and its start and end lie inside the contact (e.g. "one
  refund entered during a customer call": from "customer agrees to the
  remedy" to "refund confirmed to the customer"). If it is normally done
  after the contact ends (wrap-up, back office, a queue of written
  requests), it is DISCRETE. If both happen in substantial shares, split
  into two parts by where the work is done (Example D).

STEP 5 — OVERLAP. Compare each part with the other statements.
  - duplicates: IDs of statements that describe the SAME work item (same
    inputs, actions and output), so that coding both would count the same
    work twice. Use this only when one of the two would be redundant.
  - overlaps_with: IDs of statements that share some of the work but each
    also covers work the other does not.
  Leave a list empty if there are none. Code the part fully either way.

Before each decision, write one sentence of reasoning. Put the reasoning
before the value in the JSON.

Output JSON only:
{
  "split_reasoning": "...",
  "parts": [
    {
      "part_id": "a",
      "text": "the part of the statement, rewritten as a standalone task",
      "time_share": 1.0,
      "type_reasoning": "...",
      "type": "DISCRETE | LIVE_SERVICE | INTERPERSONAL | PHYSICAL | NO_DELIVERABLE",
      "unit_reasoning": "... (omit for non-coded types)",
      "work_item": "...",
      "start": "...",
      "end": "...",
      "checked_by": "...",
      "duplicates": ["task_id", ...],
      "overlaps_with": ["task_id", ...]
    }
  ],
  "notes": "anything ambiguous a human reviewer should look at"
}

=== WORKED EXAMPLES (other occupations) ===
Drawn from occupations outside both the pilot and the BPO set (examples swapped 2026-11-10;
the earlier ones came from BPO occupations and would have leaked into the BPO run).

### Example A — DISCRETE, granularity choice
Executive Secretaries and Executive Administrative Assistants (43-6014.00, task 2797) — "Review
work done by others to check for correct spelling and grammar, ensure that company format
policies are followed, and recommend revisions."

```json
{
  "split_reasoning": "One activity: checking documents others wrote; documents vary in length but the kind of work is the same.",
  "parts": [{
    "part_id": "a",
    "text": "Check a document written by someone else for spelling, grammar and house format, and mark the revisions needed.",
    "time_share": 1.0,
    "type_reasoning": "Each check produces a marked-up document that the author relies on.",
    "type": "DISCRETE",
    "unit_reasoning": "Documents arrive one at a time and go back to the author as a whole, not page by page.",
    "work_item": "one document checked and returned with revisions (e.g. a letter, memo or report)",
    "start": "document received for checking",
    "end": "marked-up document returned to the author",
    "checked_by": "the author, and the executive who signs it",
    "duplicates": [],
    "overlaps_with": []
  }],
  "notes": ""
}
```

### Example B — ONGOING recast into items
Market Research Analysts and Marketing Specialists (13-1161.00, task 5442) — "Monitor industry
statistics and follow trends in trade literature."

```json
{
  "split_reasoning": "Monitoring is continuous, but it produces two different kinds of item: notes on each new release of figures, and periodic trend reports.",
  "parts": [
    {
      "part_id": "a",
      "text": "Review a new release of industry statistics and send the team a note on the changes that matter.",
      "time_share": 0.5,
      "type_reasoning": "Each release ends in a short note that colleagues read and act on.",
      "type": "DISCRETE",
      "unit_reasoning": "Releases arrive on a schedule and each one is reviewed and reported on once.",
      "work_item": "one statistics release reviewed and summarised",
      "start": "new release of industry figures published",
      "end": "note on the notable changes sent to the team",
      "checked_by": "marketing manager",
      "duplicates": [],
      "overlaps_with": []
    },
    {
      "part_id": "b",
      "text": "Write a periodic trend report drawing on industry statistics and trade literature.",
      "time_share": 0.5,
      "type_reasoning": "Produces a report that managers read and plan from.",
      "type": "DISCRETE",
      "unit_reasoning": "The report is what is handed over and signed off.",
      "work_item": "one trend report (monthly or quarterly)",
      "start": "period's statistics and articles gathered",
      "end": "report with implications sent to marketing management",
      "checked_by": "marketing manager",
      "duplicates": [],
      "overlaps_with": []
    }
  ],
  "notes": "Time shares are a judgment; they depend on how often figures are released."
}
```

### Example C — COMPOUND with an interpersonal part
Human Resources Specialists (13-1071.00, task 18867) — "Provide management with information or
training related to interviewing, performance appraisals, counseling techniques, or
documentation of performance issues."

```json
{
  "split_reasoning": "Two different activities joined by 'or': training managers, and answering a manager's question about a specific case.",
  "parts": [
    {
      "part_id": "a",
      "text": "Train managers on interviewing, appraisals or documenting performance issues.",
      "time_share": 0.4,
      "type_reasoning": "The value is in the live session; nothing a colleague would check is produced.",
      "type": "INTERPERSONAL",
      "duplicates": [],
      "overlaps_with": []
    },
    {
      "part_id": "b",
      "text": "Answer a manager's question about handling a specific case, usually by email.",
      "time_share": 0.6,
      "type_reasoning": "Each question produces written guidance the manager relies on.",
      "type": "DISCRETE",
      "unit_reasoning": "Questions arrive one at a time, by email or the HR ticket queue.",
      "work_item": "one manager's question answered with written guidance",
      "start": "question received",
      "end": "guidance sent and question closed",
      "checked_by": "the manager who asked; HR lead for sensitive cases",
      "duplicates": [],
      "overlaps_with": []
    }
  ],
  "notes": "If training materials are written as part of this, they belong to a separate statement."
}
```

### Example D — one activity done in two places (live and afterwards)
Receptionists and Information Clerks (43-4171.00, task 751) — "Schedule
appointments and maintain and update appointment calendars."

```json
{
  "split_reasoning": "One activity, keeping the calendar, but done in two places: live with a caller or visitor who is waiting, and afterwards from written requests and staff changes.",
  "parts": [
    {
      "part_id": "a",
      "text": "Book, move, or cancel an appointment while the caller or visitor is on the line or at the desk.",
      "time_share": 0.7,
      "type_reasoning": "The person is waiting while the booking is made, so this is work done during a live contact.",
      "type": "LIVE_SERVICE",
      "unit_reasoning": "Each request is booked and confirmed within one call or visit.",
      "work_item": "one appointment booked or changed during a call or visit",
      "start": "caller or visitor asks for an appointment",
      "end": "slot confirmed to the person and entered in the calendar",
      "checked_by": "the caller, and the staff member whose calendar it is",
      "duplicates": [],
      "overlaps_with": []
    },
    {
      "part_id": "b",
      "text": "Update calendars from emailed requests, cancellations, and changes in staff availability.",
      "time_share": 0.3,
      "type_reasoning": "Done from a queue of written requests with no one waiting, so each update is an ordinary deliverable.",
      "type": "DISCRETE",
      "unit_reasoning": "Receptionists work through the day's written requests in a batch and send confirmations.",
      "work_item": "one batch of calendar updates from the day's written requests",
      "start": "requests or availability changes received by email or message",
      "end": "calendars updated and confirmations sent",
      "checked_by": "staff whose calendars these are",
      "duplicates": [],
      "overlaps_with": []
    }
  ],
  "notes": "The live share depends on how much booking comes in by phone versus online or email."
}
```

=== OCCUPATION: Computer Systems Analysts (15-1211.00) ===
Analyze science, engineering, business, and other data processing problems to develop and implement solutions to complex applications problems, system administration issues, or network concerns. Perform systems management and integration functions, improve existing computer systems, and review computer system capabilities, workflow, and schedule limitations. May analyze or recommend commercially available software.

TASK LIST (context; every statement below is also a TARGET):
[3464] Provide staff and users with assistance solving computer-related problems, such as malfunctions and program problems.
[3465] Test, maintain, and monitor computer programs and systems, including coordinating the installation of computer programs and systems.
[3466] Use object-oriented programming languages, as well as client and server applications development processes and multimedia and Internet technology.
[3467] Confer with clients regarding the nature of the information processing or computation needs a computer program is to address.
[3468] Coordinate and link the computer systems within an organization to increase compatibility so that information can be shared.
[3469] Consult with management to ensure agreement on system principles.
[3470] Expand or modify system to serve new purposes or improve work flow.
[3471] Interview or survey workers, observe job performance, or perform the job to determine what information is processed and how it is processed.
[3472] Determine computer software or hardware needed to set up or alter systems.
[3473] Train staff and users to work with computer systems and programs.
[3474] Analyze information processing or computation needs and plan and design computer systems, using techniques such as structured analysis, data modeling, and information engineering.
[3475] Assess the usefulness of pre-developed application packages and adapt them to a user environment.
[3476] Define the goals of the system and devise flow charts and diagrams describing logical operational steps of programs.
[3477] Develop, document, and revise system design procedures, test procedures, and quality standards.
[3478] Review and analyze computer printouts and performance indicators to locate code problems, and correct errors by correcting codes.
[3479] Recommend new equipment or software packages.
[3480] Read manuals, periodicals, and technical reports to learn how to develop programs that meet staff and user requirements.
[3481] Supervise computer programmers or other systems analysts or serve as project leaders for particular systems projects.
[3482] Use the computer in the analysis and solution of business problems, such as development of integrated production and inventory control and cost analysis systems.
[3483] Prepare cost-benefit and return-on-investment analyses to aid in decisions on system implementation.
[3484] Specify inputs accessed by the system and plan the distribution and use of the results.
[20950] Troubleshoot program and system malfunctions to restore normal functioning.

TARGETS: code all 22 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/bpo_v1/15-1211.00.json.

=== OCCUPATION: Bookkeeping, Accounting, and Auditing Clerks (43-3031.00) ===
Compute, classify, and record numerical data to keep financial records complete. Perform any combination of routine calculating, posting, and verifying duties to obtain primary financial data for use in maintaining accounting records. May also check the accuracy of figures, calculations, and postings pertaining to business transactions recorded by other workers.

TASK LIST (context; every statement below is also a TARGET):
[2486] Check figures, postings, and documents for correct entry, mathematical accuracy, and proper codes.
[2487] Operate computers programmed with accounting software to record, store, and analyze information.
[2488] Comply with federal, state, and company policies, procedures, and regulations.
[2489] Debit, credit, and total accounts on computer spreadsheets and databases, using specialized accounting software.
[2490] Classify, record, and summarize numerical and financial data to compile and keep financial records, using journals and ledgers or computers.
[2491] Calculate, prepare, and issue bills, invoices, account statements, and other financial statements according to established procedures.
[2492] Compile statistical, financial, accounting, or auditing reports and tables pertaining to such matters as cash receipts, expenditures, accounts payable and receivable, and profits and losses.
[2493] Code documents according to company procedures.
[2494] Access computerized financial information to answer general questions as well as those related to specific accounts.
[2495] Operate 10-key calculators, typewriters, and copy machines to perform calculations and produce documents.
[2496] Reconcile or note and report discrepancies found in records.
[2497] Perform financial calculations, such as amounts due, interest charges, balances, discounts, equity, and principal.
[2498] Perform general office duties, such as filing, answering telephones, and handling routine correspondence.
[2499] Prepare bank deposits by compiling data from cashiers, verifying and balancing receipts, and sending cash, checks, or other forms of payment to banks.
[2500] Receive, record, and bank cash, checks, and vouchers.
[2501] Calculate and prepare checks for utilities, taxes, and other payments.
[2502] Compare computer printouts to manually maintained journals to determine if they match.
[2503] Reconcile records of bank transactions.
[2504] Prepare trial balances of books.
[2505] Monitor status of loans and accounts to ensure that payments are up to date.
[2506] Transfer details from separate journals to general ledgers or data processing sheets.
[2507] Compile budget data and documents, based on estimated revenues and expenses and previous budgets.
[2508] Calculate costs of materials, overhead, and other expenses, based on estimates, quotations and price lists.
[2509] Match order forms with invoices, and record the necessary information.
[2510] Complete and submit tax forms and returns, workers' compensation forms, pension contribution forms, and other government documents.
[2511] Maintain inventory records.
[2514] Prepare purchase orders and expense reports.
[18561] Prepare and process payroll information.

TARGETS: code all 28 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/bpo_v1/43-3031.00.json.

=== OCCUPATION: Billing and Posting Clerks (43-3021.00) ===
Compile, compute, and record billing, accounting, statistical, and other numerical data for billing purposes. Prepare billing invoices for services rendered or for delivery or shipment of goods.

TASK LIST (context; every statement below is also a TARGET):
[23237] Post stop-payment notices to prevent payment of protested checks.
[23238] Verify accuracy of billing data and revise any errors.
[23239] Verify signatures and required information on checks.
[23240] Prepare itemized statements, bills, or invoices and record amounts due for items purchased or services rendered.
[23241] Perform bookkeeping work, including posting data or keeping other records concerning costs of goods or services or the shipment of goods.
[23242] Operate typing, adding, calculating, or billing machines.
[23243] Resolve discrepancies in accounting records.
[23244] Contact customers to obtain or relay account information.
[23245] Review documents, such as purchase orders, sales tickets, charge slips, or hospital records, to compute fees or charges due.
[23246] Keep records of invoices and support documents.
[23247] Route statements for mailing or over-the-counter delivery to customers.
[23248] Monitor equipment to ensure proper operation.
[23249] Fix minor problems, such as equipment jams, and notify repair personnel of major equipment problems.
[23250] Weigh envelopes containing statements to determine correct postage and affix postage, using stamps or metering equipment.
[23251] Compare previously prepared bank statements with canceled checks and reconcile discrepancies.
[23255] Consult sources, such as rate books, manuals, or insurance company representatives, to determine specific charges or information such as rules, regulations, or government tax and tariff information.
[23256] Track accumulated hours and dollar amounts charged to each client job to calculate client fees for professional services, such as legal or accounting services.
[23257] Update manuals when rates, rules, or regulations are amended.
[23258] Compute credit terms, discounts, shipment charges, or rates for goods or services to complete billing documents.
[23259] Load machines with statements, cancelled checks, or envelopes to prepare statements for distribution to customers or stuff envelopes by hand.
[23260] Review compiled data on operating costs and revenues to set rates.
[23262] Answer inquiries regarding rates, routing, or procedures.
[23263] Compile reports of cost factors, such as labor, production, storage, and equipment.
[23264] Create billing documents, shipping labels, credit memorandums, or credit forms.
[23265] Perform general administrative tasks, such as answering telephones, scheduling appointments, and ordering supplies or equipment.
[23266] Return checks to customers or retrieve checks returned to customers in error, adjusting accounts and answering inquiries about errors as necessary.

TARGETS: code all 26 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/bpo_v1/43-3021.00.json.

=== OCCUPATION: Data Entry Keyers (43-9021.00) ===
Operate data entry device, such as keyboard or photo composing perforator. Duties may include verifying data and preparing materials for printing.

TASK LIST (context; every statement below is also a TARGET):
[11401] Read source documents such as canceled checks, sales reports, or bills, and enter data in specific data fields or onto tapes or disks for subsequent entry, using keyboards or scanners.
[11402] Compile, sort, and verify the accuracy of data before it is entered.
[11403] Compare data with source documents, or re-enter data in verification format to detect errors.
[11404] Store completed documents in appropriate locations.
[11405] Locate and correct data entry errors, or report them to supervisors.
[11406] Maintain logs of activities and completed work.
[11407] Select materials needed to complete work assignments.
[11408] Load machines with required input or output media, such as paper, cards, disks, tape, or Braille media.
[11409] Resolve garbled or indecipherable messages, using cryptographic procedures and equipment.

TARGETS: code all 9 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/bpo_v1/43-9021.00.json.
