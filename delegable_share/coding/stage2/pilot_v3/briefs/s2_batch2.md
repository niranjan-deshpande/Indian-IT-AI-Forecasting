You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Code each ITEM independently, in the order given; do not go
back and adjust earlier answers to make them consistent with later ones.

Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/pilot_v3/s2/batch2.json
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
[2587b]
Occupation: Customer Service Representatives
Task statement: Review insurance policy terms to determine whether a particular loss is covered by insurance.
Part: Review the policy terms against a reported loss and record a coverage determination for the claim.
Type: DISCRETE
Work item: one coverage determination for a reported loss
Start: loss report and policy retrieved
End: coverage decision recorded on the claim file
Checked by: claims adjuster or supervisor, and the customer

[2587a]
Occupation: Customer Service Representatives
Task statement: Review insurance policy terms to determine whether a particular loss is covered by insurance.
Part: Read the policy terms and tell a caller whether their loss appears to be covered while they are on the line.
Type: LIVE_SERVICE
Work item: one coverage question answered during a call
Start: customer describes the loss and asks whether it is covered
End: coverage answer given and noted on the account
Checked by: the customer and claims staff who later rely on the note

[14658a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Identify program deviance from standards, and suggest modifications to ensure compliance.
Part: Check a program against standards and recommend modifications to bring it into compliance.
Type: DISCRETE
Work item: one standards-compliance review of a program with recommendations
Start: program or build submitted for compliance check
End: deviations and suggested changes sent to developers
Checked by: developers / QA lead

[1282a]
Occupation: Computer User Support Specialists
Task statement: Answer user inquiries regarding computer software or hardware operation to resolve problems.
Part: Answer a user's question about software or hardware operation while the user is on the phone, in chat, or at the desk, resolving the problem during the contact.
Type: LIVE_SERVICE
Work item: one user call, chat, or walk-up question answered
Start: user calls, opens a chat, or walks up with a question
End: user confirms the answer or fix works, or the issue is logged for follow-up
Checked by: the user who asked; help-desk supervisor through call reviews

[14638b]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Design test plans, scenarios, scripts, or procedures.
Part: Design test scenarios, scripts, or procedures for software functionality.
Type: DISCRETE
Work item: one feature-level set of test cases or scripts
Start: feature requirements or test objectives are available
End: cases or scripts are ready for review and execution
Checked by: test lead and testers

[14660b]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Coordinate user or third-party testing.
Part: Compile the results of a user or third-party test round into a findings report.
Type: DISCRETE
Work item: one test round results report
Start: test round closes and feedback is collected
End: findings report sent and defects filed
Checked by: product owner / QA manager

[2585a]
Occupation: Customer Service Representatives
Task statement: Obtain and examine all relevant information to assess validity of complaints and to determine possible causes, such as extreme weather conditions that could increase utility bills.
Part: Look up account and usage information during the call to assess whether a complaint is valid and explain the likely cause.
Type: LIVE_SERVICE
Work item: one complaint assessed during a call or visit
Start: customer describes the complaint
End: validity and likely cause explained to the customer and noted
Checked by: the customer and QA reviewer

[1296a]
Occupation: Computer User Support Specialists
Task statement: Modify and customize commercial programs for internal needs.
Part: Modify or customize a commercial program (e.g. templates, macros, configuration, scripts) to meet internal needs.
Type: DISCRETE
Work item: one program customization delivered (template, macro, configuration change)
Start: customization request received
End: change tested and released to users
Checked by: requesting users; IT supervisor

[14659a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Design or develop automated testing tools.
Part: Design and build an automated testing tool or framework component.
Type: DISCRETE
Work item: one automated testing tool or framework component
Start: tool need or specification agreed
End: tool reviewed, merged, and in use by the team
Checked by: QA lead / code reviewer

[1288b]
Occupation: Computer User Support Specialists
Task statement: Read technical manuals, confer with users, or conduct computer diagnostics to investigate and resolve problems or to provide technical assistance and support.
Part: Investigate and resolve a ticketed computer problem after the contact, using diagnostics, technical manuals, and follow-up with the user.
Type: DISCRETE
Work item: one ticketed problem investigated and resolved
Start: ticket assigned or problem left open from a contact
End: fix applied and confirmed by the user, ticket closed, or ticket escalated
Checked by: the user; help-desk lead

[14640a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Develop testing programs that address areas such as database impacts, software scenarios, regression testing, negative testing, error or bug retests, or usability.
Part: Develop a test suite covering a given area such as regression, negative testing, database impacts, bug retests, or usability.
Type: DISCRETE
Work item: one test suite for one testing area of a release
Start: testing area and scope assigned
End: suite written, reviewed, and added to the test repository
Checked by: QA lead

[14645a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Plan test schedules or strategies in accordance with project scope or delivery dates.
Part: Prepare the test strategy and schedule for a project or release according to its scope and delivery dates.
Type: DISCRETE
Work item: one test strategy and schedule for a project or release
Start: project scope and delivery dates received
End: strategy and schedule approved by project stakeholders
Checked by: QA manager / project manager

[14639a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Test system modifications to prepare for implementation.
Part: Execute tests on a system modification and report whether it is ready for implementation.
Type: DISCRETE
Work item: one system modification tested (one test cycle)
Start: change deployed to the test environment and assigned for testing
End: test results recorded and change signed off or returned with defects
Checked by: release manager / development lead

[14663a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Evaluate or recommend software for testing or bug tracking.
Part: Evaluate testing or bug tracking software and recommend whether to adopt it.
Type: DISCRETE
Work item: one tool evaluation with recommendation
Start: tool need or candidate tools identified
End: evaluation and recommendation sent to the QA manager
Checked by: QA manager

[2582a]
Occupation: Customer Service Representatives
Task statement: Refer unresolved customer grievances to designated departments for further investigation.
Part: Prepare and route a referral of an unresolved customer grievance to the designated department for investigation.
Type: DISCRETE
Work item: one grievance referral ticket
Start: representative determines the grievance cannot be resolved at first level
End: referral with case details submitted to the designated department
Checked by: receiving department and supervisor

[14651a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Investigate customer problems referred by technical support.
Part: Investigate a customer problem referred by technical support and report the findings.
Type: DISCRETE
Work item: one escalated customer problem investigated
Start: escalation ticket received from technical support
End: problem reproduced or not, findings returned to support, and defect filed if needed
Checked by: technical support / developers

[1287a]
Occupation: Computer User Support Specialists
Task statement: Maintain records of daily data communication transactions, problems and remedial actions taken, or installation activities.
Part: Write up the record of a user problem and the remedial action taken in the ticketing system after it is handled.
Type: DISCRETE
Work item: one problem-and-remedy record written up for a ticket
Start: problem handled or remedy applied
End: ticket notes complete with problem, steps taken, and outcome; ticket closed or updated
Checked by: help-desk lead; other support staff who pick up the ticket later

