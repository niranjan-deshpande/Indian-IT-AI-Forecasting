You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Code each ITEM independently, in the order given; do not go
back and adjust earlier answers to make them consistent with later ones.

Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/pilot_v3/s2/batch3.json
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
  "review_reasoning": "A senior accountant checks a short batch by opening the sign-off and spot-checking a few entries; a typical batch needs a few more entries traced to source; a month-end batch needs the exceptions and accruals checked one by one.",
  "review_p10": 4, "review_p50": 8, "review_p90": 18,
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
  "review_reasoning": "For a quick alert the lead reads the closing note and glances at the triggering graph; a typical one also needs the cause checked against the logs; a long investigation needs its chain of reasoning followed.",
  "review_p10": 2, "review_p50": 4, "review_p90": 12,
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
  "review_reasoning": "A quality reviewer listens to the call, mostly at higher speed, and checks the calendar entry; a long reschedule chain takes a little longer to follow.",
  "review_p10": 1, "review_p50": 2, "review_p90": 4,
  "stakes_reasoning": "A wrong booking causes a missed or double-booked appointment, noticed on the day and rebooked.",
  "stakes": "low", "stakes_p90": "medium",
  "context_reasoning": "Needs the office's booking rules and who sees whom, picked up quickly.",
  "context": "low"
}
```

=== ITEMS ===
[2581a]
Occupation: Customer Service Representatives
Task statement: Contact customers to respond to inquiries or to notify them of claim investigation results or any planned adjustments.
Part: Write and send a response to a customer's inquiry or a notification of claim investigation results or a planned adjustment.
Type: DISCRETE
Work item: one written response or notification sent to a customer
Start: inquiry or investigation result ready for response
End: letter or email sent and logged on the account
Checked by: the customer, and supervisor or QA reviewer

[14664a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Conduct historical analyses of test results.
Part: Analyze historical test results for trends and report the findings.
Type: DISCRETE
Work item: one historical test results analysis report
Start: pull of past test results
End: report with trends and recommendations sent
Checked by: QA manager

[2580a]
Occupation: Customer Service Representatives
Task statement: Check to ensure that appropriate changes were made to resolve customers' problems.
Part: Check the account or order system to confirm that the change made to resolve a customer's problem was carried out correctly.
Type: DISCRETE
Work item: one resolution verified for a customer case
Start: follow-up date reached or confirmation of change expected
End: change confirmed and case closed, or discrepancy flagged and case reopened
Checked by: supervisor and the customer

[14641a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Document software defects, using a bug tracking system, and report defects to software developers.
Part: Write up a defect in the bug tracking system and assign or report it to the developers.
Type: DISCRETE
Work item: one defect report filed in the bug tracker
Start: defect observed during testing
End: ticket filed with steps to reproduce, severity, and evidence, and assigned to a developer
Checked by: developers / triage lead

[2583a]
Occupation: Customer Service Representatives
Task statement: Determine charges for services requested, collect deposits or payments, or arrange for billing.
Part: Determine the charges for a requested service and collect a deposit or payment, or set up billing, while the customer is on the line or at the desk.
Type: LIVE_SERVICE
Work item: one service charge determined and payment or billing arrangement completed during a contact
Start: customer requests a service
End: charge quoted, payment or deposit taken or billing arranged, receipt or confirmation given
Checked by: the customer, and cash-office or billing reconciliation

[2585b]
Occupation: Customer Service Representatives
Task statement: Obtain and examine all relevant information to assess validity of complaints and to determine possible causes, such as extreme weather conditions that could increase utility bills.
Part: Gather and examine records and outside information to investigate a complaint's validity and cause after the contact.
Type: DISCRETE
Work item: one complaint investigation with a validity finding
Start: complaint case opened for review
End: finding on validity and cause recorded and passed for remedy or reply
Checked by: supervisor, and the staff who decide the remedy

[2578b]
Occupation: Customer Service Representatives
Task statement: Keep records of customer interactions or transactions, recording details of inquiries, complaints, or comments, as well as actions taken.
Part: Complete the interaction or transaction record (disposition codes, summary, actions taken) in after-call wrap-up.
Type: DISCRETE
Work item: one interaction record completed after a call or visit
Start: call or visit ends
End: record saved with disposition code, summary, and actions taken
Checked by: quality-assurance reviewer, supervisor, and later agents handling the account

[2578a]
Occupation: Customer Service Representatives
Task statement: Keep records of customer interactions or transactions, recording details of inquiries, complaints, or comments, as well as actions taken.
Part: Enter details of the customer's inquiry, complaint, or comment and the actions taken into the account notes while the customer is on the line or at the desk.
Type: LIVE_SERVICE
Work item: one set of contact notes entered during a call or visit
Start: customer states the reason for the contact
End: notes and actions logged on the account before the contact ends
Checked by: quality-assurance reviewer and later agents who read the account history

[1286b]
Occupation: Computer User Support Specialists
Task statement: Set up equipment for employee use, performing or ensuring proper installation of cables, operating systems, or appropriate software.
Part: Install and configure the operating system, software, and accounts on a new employee's computer so it is ready for use.
Type: DISCRETE
Work item: one workstation configured and handed over to an employee
Start: setup request or new-starter ticket received with hardware available
End: machine imaged, software and accounts configured, handed to employee and ticket closed
Checked by: the employee; IT supervisor

[14643b]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Monitor bug resolution efforts and track successes.
Part: Produce a periodic defect-resolution status report tracking open, fixed, and closed bugs.
Type: DISCRETE
Work item: one defect status report (weekly or per sprint)
Start: pull of current defect data from the tracker
End: report with counts, trends, and blockers sent to the project team
Checked by: QA manager / project manager

[14656a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Install and configure recreations of software production environments to allow testing of software performance.
Part: Install and configure a recreation of the production environment for performance testing.
Type: DISCRETE
Work item: one test environment built to mirror production
Start: environment request with production specification
End: environment configured, verified, and handed to testers
Checked by: QA lead / performance testers

[14648a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Document test procedures to ensure replicability and compliance with standards.
Part: Write up a test procedure in enough detail that it can be repeated and meets documentation standards.
Type: DISCRETE
Work item: one test procedure documented
Start: test procedure designed or run
End: procedure document reviewed and stored in the test repository
Checked by: QA lead / compliance auditor

[1292a]
Occupation: Computer User Support Specialists
Task statement: Prepare evaluations of software or hardware, and recommend improvements or upgrades.
Part: Evaluate a piece of software or hardware and recommend improvements or upgrades.
Type: DISCRETE
Work item: one evaluation with recommendation (product, upgrade, or improvement)
Start: request or identified need to assess a product or system
End: evaluation and recommendation sent to IT manager
Checked by: IT manager; purchasing decision-makers

[14650a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Update automated test scripts to ensure currency.
Part: Update automated test scripts to reflect product changes.
Type: DISCRETE
Work item: one set of automated test scripts updated for a product change
Start: product change breaks or outdates scripts
End: updated scripts reviewed, merged, and passing in the pipeline
Checked by: QA lead / code reviewer

[14647a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Review software documentation to ensure technical accuracy, compliance, or completeness, or to mitigate risks.
Part: Review a software document for technical accuracy, compliance, completeness, and risks, and return findings.
Type: DISCRETE
Work item: one software document reviewed with findings
Start: document submitted for review
End: findings returned or document approved
Checked by: document author / QA lead

[14649a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Develop or specify standards, methods, or procedures to determine product quality or release readiness.
Part: Develop or specify a quality standard, method, or release-readiness criteria.
Type: DISCRETE
Work item: one quality standard or set of release-readiness criteria
Start: need for a standard or criteria identified
End: document approved and published to the team
Checked by: QA manager / engineering leadership

