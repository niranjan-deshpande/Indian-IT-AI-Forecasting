You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Code each ITEM independently, in the order given; do not go
back and adjust earlier answers to make them consistent with later ones.

Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/pilot/s1/batch3.json
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
time to fix errors. Give it for two of the items from your LENGTH answer:
the 10th-percentile item (review_p10) and the median item (review_p50). For
LIVE_SERVICE items, this is the time a quality reviewer needs to check one
recorded contact of that length.

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
  "review_reasoning": "...", "review_p10": 0, "review_p50": 0,
  "stakes_reasoning": "...", "stakes": "low | medium | high",
  "stakes_p90": "low | medium | high",
  "context_reasoning": "...", "context": "low | medium | high"
}

=== WORKED EXAMPLES (other occupations) ===
The work items are those from the Stage 1 worked examples (non-pilot occupations). The numbers are
our judgment, there to show the scale and level of detail. Worth checking before the run.

### Example A — Bookkeeping, Accounting, and Auditing Clerks
Work item: one batch of postings checked (e.g. a day's entries for one ledger). Start: batch of
entries and source documents received for review. End: batch marked verified, with errors corrected
or flagged. Checked by: senior accountant or auditor. Type: DISCRETE.

```json
{
  "item_id": "example-A",
  "unit_flag": false, "unit_flag_reason": "",
  "domain_reasoning": "Most of the time goes into opening entries in the accounting system and comparing them with source documents on screen.",
  "domain": "computer_use",
  "length_reasoning": "A small batch of routine entries takes a quarter of an hour; a month-end batch with many accruals and exceptions takes a couple of hours.",
  "length_p10": 15, "length_p50": 40, "length_p90": 120, "two_groups": false,
  "review_reasoning": "A senior accountant checks a short batch by opening the sign-off and spot-checking a few entries; a typical batch needs a few more entries traced to source.",
  "review_p10": 4, "review_p50": 8,
  "stakes_reasoning": "A missed miscoding usually surfaces at reconciliation and is corrected by a journal entry; a large one can reach the financial statements.",
  "stakes": "medium", "stakes_p90": "high",
  "context_reasoning": "Needs the company's chart of accounts and coding rules, learned over a few weeks.",
  "context": "medium"
}
```

### Example B — Network and Computer Systems Administrators
Work item: one performance alert investigated. Start: alert raised by monitoring tool. End: cause
recorded and either adjustment requested or alert closed as no action. Checked by: on-call lead /
change board. Type: DISCRETE.

```json
{
  "item_id": "example-B",
  "unit_flag": false, "unit_flag_reason": "",
  "domain_reasoning": "The work is in monitoring dashboards, logs and device consoles.",
  "domain": "computer_use",
  "length_reasoning": "Most alerts are transient or known and closed in minutes; a real fault can take an hour or more to trace.",
  "length_p10": 5, "length_p50": 20, "length_p90": 90, "two_groups": true,
  "review_reasoning": "For a quick alert the lead reads the closing note and glances at the triggering graph; a typical one also needs the cause checked against the logs.",
  "review_p10": 2, "review_p50": 4,
  "stakes_reasoning": "A wrongly closed alert usually recurs and is caught, but a missed real fault can become an outage.",
  "stakes": "medium", "stakes_p90": "high",
  "context_reasoning": "Telling noise from a real problem needs months of knowing this network's normal behaviour and history.",
  "context": "high"
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
  "review_reasoning": "A quality reviewer listens to the call, mostly at higher speed, and checks the calendar entry.",
  "review_p10": 1, "review_p50": 2,
  "stakes_reasoning": "A wrong booking causes a missed or double-booked appointment, noticed on the day and rebooked.",
  "stakes": "low", "stakes_p90": "medium",
  "context_reasoning": "Needs the office's booking rules and who sees whom, picked up quickly.",
  "context": "low"
}
```

=== ITEMS ===
[18565a]
Occupation: Customer Service Representatives
Task statement: Confer with customers by telephone or in person to provide information about products or services, take or enter orders, cancel accounts, or obtain details of complaints.
Part: Answer a customer's call or visit asking for information about products or services.
Type: LIVE_SERVICE
Work item: one information inquiry answered during a call or visit
Start: customer asks a question
End: customer confirms the question is answered, contact ends
Checked by: the customer and QA reviewer

[14660b]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Coordinate user or third-party testing.
Part: Compile the results of a user or third-party test round into a findings report.
Type: DISCRETE
Work item: one test round results report
Start: test round closes and feedback is collected
End: findings report sent and defects filed
Checked by: product owner / QA manager

[2587b]
Occupation: Customer Service Representatives
Task statement: Review insurance policy terms to determine whether a particular loss is covered by insurance.
Part: Review the policy terms against a reported loss and record a coverage determination for the claim.
Type: DISCRETE
Work item: one coverage determination for a reported loss
Start: loss report and policy retrieved
End: coverage decision recorded on the claim file
Checked by: claims adjuster or supervisor, and the customer

[14640a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Develop testing programs that address areas such as database impacts, software scenarios, regression testing, negative testing, error or bug retests, or usability.
Part: Develop a test suite covering a given area such as regression, negative testing, database impacts, bug retests, or usability.
Type: DISCRETE
Work item: one test suite for one testing area of a release
Start: testing area and scope assigned
End: suite written, reviewed, and added to the test repository
Checked by: QA lead

[1283b]
Occupation: Computer User Support Specialists
Task statement: Enter commands and observe system functioning to verify correct operations and detect errors.
Part: Run routine diagnostic commands on systems to detect errors before users report them.
Type: DISCRETE
Work item: one routine system check round (e.g. daily check of servers, printers, network links)
Start: scheduled check begins
End: results recorded, with any errors logged as tickets
Checked by: IT supervisor; systems administrators who act on the errors

[14657a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Collaborate with field staff or customers to evaluate or diagnose problems and recommend possible solutions.
Part: Diagnose a problem in a live call or session with field staff or a customer.
Type: LIVE_SERVICE
Work item: one problem diagnosed during a live session with field staff or a customer
Start: session begins with the problem described
End: likely cause identified and next steps agreed
Checked by: the customer or field staff member

[1282a]
Occupation: Computer User Support Specialists
Task statement: Answer user inquiries regarding computer software or hardware operation to resolve problems.
Part: Answer a user's question about software or hardware operation while the user is on the phone, in chat, or at the desk, resolving the problem during the contact.
Type: LIVE_SERVICE
Work item: one user call, chat, or walk-up question answered
Start: user calls, opens a chat, or walks up with a question
End: user confirms the answer or fix works, or the issue is logged for follow-up
Checked by: the user who asked; help-desk supervisor through call reviews

[2578a]
Occupation: Customer Service Representatives
Task statement: Keep records of customer interactions or transactions, recording details of inquiries, complaints, or comments, as well as actions taken.
Part: Enter details of the customer's inquiry, complaint, or comment and the actions taken into the account notes while the customer is on the line or at the desk.
Type: LIVE_SERVICE
Work item: one set of contact notes entered during a call or visit
Start: customer states the reason for the contact
End: notes and actions logged on the account before the contact ends
Checked by: quality-assurance reviewer and later agents who read the account history

[14641a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Document software defects, using a bug tracking system, and report defects to software developers.
Part: Write up a defect in the bug tracking system and assign or report it to the developers.
Type: DISCRETE
Work item: one defect report filed in the bug tracker
Start: defect observed during testing
End: ticket filed with steps to reproduce, severity, and evidence, and assigned to a developer
Checked by: developers / triage lead

[2584b]
Occupation: Customer Service Representatives
Task statement: Complete contract forms, prepare change of address records, or issue service discontinuance orders, using computers.
Part: Process contract forms, change-of-address records, or discontinuance orders from written or online requests.
Type: DISCRETE
Work item: one account order processed from a written request
Start: written or online request received
End: order entered and confirmation sent to the customer
Checked by: the customer and the fulfilment or billing team

[1283a]
Occupation: Computer User Support Specialists
Task statement: Enter commands and observe system functioning to verify correct operations and detect errors.
Part: Run test commands and observe a computer or system after an installation, repair, or change to verify it works correctly.
Type: DISCRETE
Work item: one post-install or post-repair verification of a machine or system
Start: installation, repair, or change completed
End: correct operation confirmed and noted on the ticket, or error found and fix reopened
Checked by: the user; support lead closing the ticket

[14653a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Provide feedback and recommendations to developers on software usability and functionality.
Part: Write usability and functionality feedback and recommendations on a build for developers.
Type: DISCRETE
Work item: one written feedback note on a build or feature
Start: build or feature evaluated
End: feedback and recommendations sent to developers
Checked by: developers / product owner

[2589b]
Occupation: Customer Service Representatives
Task statement: Compare disputed merchandise with original requisitions and information from invoices and prepare invoices for returned goods.
Part: Match the dispute against requisition and invoice records and prepare an invoice for the returned goods.
Type: DISCRETE
Work item: one return invoice prepared for a disputed shipment
Start: disputed goods and original requisition and invoice in hand
End: return invoice issued and sent to billing and the customer
Checked by: billing or accounts receivable, and the customer

[14643b]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Monitor bug resolution efforts and track successes.
Part: Produce a periodic defect-resolution status report tracking open, fixed, and closed bugs.
Type: DISCRETE
Work item: one defect status report (weekly or per sprint)
Start: pull of current defect data from the tracker
End: report with counts, trends, and blockers sent to the project team
Checked by: QA manager / project manager

[18565b]
Occupation: Customer Service Representatives
Task statement: Confer with customers by telephone or in person to provide information about products or services, take or enter orders, cancel accounts, or obtain details of complaints.
Part: Take and enter an order or cancel an account while the customer is on the line or at the desk.
Type: LIVE_SERVICE
Work item: one order or account cancellation entered during a contact
Start: customer asks to order or cancel
End: order or cancellation confirmed to the customer
Checked by: the customer and the fulfilment or billing team

[14645a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Plan test schedules or strategies in accordance with project scope or delivery dates.
Part: Prepare the test strategy and schedule for a project or release according to its scope and delivery dates.
Type: DISCRETE
Work item: one test strategy and schedule for a project or release
Start: project scope and delivery dates received
End: strategy and schedule approved by project stakeholders
Checked by: QA manager / project manager

