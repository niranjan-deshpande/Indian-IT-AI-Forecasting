You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Code each ITEM independently, in the order given; do not go
back and adjust earlier answers to make them consistent with later ones.

Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/pilot/s1/batch1.json
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
[14648a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Document test procedures to ensure replicability and compliance with standards.
Part: Write up a test procedure in enough detail that it can be repeated and meets documentation standards.
Type: DISCRETE
Work item: one test procedure documented
Start: test procedure designed or run
End: procedure document reviewed and stored in the test repository
Checked by: QA lead / compliance auditor

[2579a]
Occupation: Customer Service Representatives
Task statement: Resolve customers' service or billing complaints by performing activities such as exchanging merchandise, refunding money, or adjusting bills.
Part: Process an exchange, refund, or bill adjustment while the customer is on the line or at the desk.
Type: LIVE_SERVICE
Work item: one refund, exchange, or bill adjustment entered during a call or visit
Start: customer agrees to the proposed remedy
End: refund, exchange, or adjustment entered and confirmed to the customer
Checked by: the customer, and supervisor or finance for adjustments above limits

[1287a]
Occupation: Computer User Support Specialists
Task statement: Maintain records of daily data communication transactions, problems and remedial actions taken, or installation activities.
Part: Write up the record of a user problem and the remedial action taken in the ticketing system after it is handled.
Type: DISCRETE
Work item: one problem-and-remedy record written up for a ticket
Start: problem handled or remedy applied
End: ticket notes complete with problem, steps taken, and outcome; ticket closed or updated
Checked by: help-desk lead; other support staff who pick up the ticket later

[2579b]
Occupation: Customer Service Representatives
Task statement: Resolve customers' service or billing complaints by performing activities such as exchanging merchandise, refunding money, or adjusting bills.
Part: Process the refund, exchange, or bill adjustment for a written or escalated complaint after the contact, once the remedy has been decided.
Type: DISCRETE
Work item: one refund, exchange, or bill adjustment processed from a queued case
Start: case with an approved or decided remedy reaches the representative's queue
End: refund, exchange, or adjustment entered or submitted and the case noted
Checked by: supervisor and billing or finance team

[2581b]
Occupation: Customer Service Representatives
Task statement: Contact customers to respond to inquiries or to notify them of claim investigation results or any planned adjustments.
Part: Call a customer back to answer an inquiry or explain claim investigation results or a planned adjustment.
Type: LIVE_SERVICE
Work item: one outbound callback delivering an answer or result
Start: customer answers the call
End: result explained, customer's questions answered, call ended
Checked by: the customer, and QA reviewer of recorded calls

[14649a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Develop or specify standards, methods, or procedures to determine product quality or release readiness.
Part: Develop or specify a quality standard, method, or release-readiness criteria.
Type: DISCRETE
Work item: one quality standard or set of release-readiness criteria
Start: need for a standard or criteria identified
End: document approved and published to the team
Checked by: QA manager / engineering leadership

[14657b]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Collaborate with field staff or customers to evaluate or diagnose problems and recommend possible solutions.
Part: Write up the diagnosis and recommended solutions after working with field staff or customers.
Type: DISCRETE
Work item: one written diagnosis and recommended solution
Start: live session or field report ends
End: recommendation sent to field staff, customer, or developers
Checked by: field staff / customer / developers

[14643a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Monitor bug resolution efforts and track successes.
Part: Follow up on a defect marked fixed: check its status, verify the fix, and close or reopen it.
Type: DISCRETE
Work item: one resolved defect verified and closed or reopened
Start: developer marks the defect fixed
End: ticket closed or reopened with a note
Checked by: developers / QA lead

[14644b]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Create or maintain databases of known test defects.
Part: Update and clean up the known-defects database: merge duplicates, update statuses, and add workarounds.
Type: DISCRETE
Work item: one curation pass over the known-defects database
Start: scheduled review or release milestone
End: records updated, duplicates merged, and known-issues list current
Checked by: QA lead / support and development teams

[1282b]
Occupation: Computer User Support Specialists
Task statement: Answer user inquiries regarding computer software or hardware operation to resolve problems.
Part: Answer a user's emailed or ticketed question about software or hardware operation.
Type: DISCRETE
Work item: one written user question answered (ticket or email)
Start: question received by email or in the ticket queue
End: answer sent and ticket closed
Checked by: the user who asked; help-desk lead reviewing ticket quality

[1288b]
Occupation: Computer User Support Specialists
Task statement: Read technical manuals, confer with users, or conduct computer diagnostics to investigate and resolve problems or to provide technical assistance and support.
Part: Investigate and resolve a ticketed computer problem after the contact, using diagnostics, technical manuals, and follow-up with the user.
Type: DISCRETE
Work item: one ticketed problem investigated and resolved
Start: ticket assigned or problem left open from a contact
End: fix applied and confirmed by the user, ticket closed, or ticket escalated
Checked by: the user; help-desk lead

[14660a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Coordinate user or third-party testing.
Part: Organize a round of user or third-party testing: scope, participants, test scripts, schedule, and access.
Type: DISCRETE
Work item: one user or third-party test round organized
Start: decision to run user or third-party testing
End: participants briefed with scripts, schedule, and access
Checked by: QA manager / test participants

[14652b]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Install, maintain, or use software testing programs.
Part: Use testing tools to run a test session and record the results.
Type: DISCRETE
Work item: one test run executed with results recorded
Start: test run scheduled or triggered
End: results logged in the test management tool
Checked by: QA lead / developers

[2582a]
Occupation: Customer Service Representatives
Task statement: Refer unresolved customer grievances to designated departments for further investigation.
Part: Prepare and route a referral of an unresolved customer grievance to the designated department for investigation.
Type: DISCRETE
Work item: one grievance referral ticket
Start: representative determines the grievance cannot be resolved at first level
End: referral with case details submitted to the designated department
Checked by: receiving department and supervisor

[1287b]
Occupation: Computer User Support Specialists
Task statement: Maintain records of daily data communication transactions, problems and remedial actions taken, or installation activities.
Part: Keep the daily log of data communication transactions and installation activities.
Type: DISCRETE
Work item: one day's log of transactions and installation activities
Start: start of day or shift
End: day's entries complete and log filed
Checked by: IT supervisor; auditors

[2587a]
Occupation: Customer Service Representatives
Task statement: Review insurance policy terms to determine whether a particular loss is covered by insurance.
Part: Read the policy terms and tell a caller whether their loss appears to be covered while they are on the line.
Type: LIVE_SERVICE
Work item: one coverage question answered during a call
Start: customer describes the loss and asks whether it is covered
End: coverage answer given and noted on the account
Checked by: the customer and claims staff who later rely on the note

[1292a]
Occupation: Computer User Support Specialists
Task statement: Prepare evaluations of software or hardware, and recommend improvements or upgrades.
Part: Evaluate a piece of software or hardware and recommend improvements or upgrades.
Type: DISCRETE
Work item: one evaluation with recommendation (product, upgrade, or improvement)
Start: request or identified need to assess a product or system
End: evaluation and recommendation sent to IT manager
Checked by: IT manager; purchasing decision-makers

