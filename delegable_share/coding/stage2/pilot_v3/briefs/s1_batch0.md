You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Code each ITEM independently, in the order given; do not go
back and adjust earlier answers to make them consistent with later ones.

Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/pilot_v3/s1/batch0.json
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
[2584a]
Occupation: Customer Service Representatives
Task statement: Complete contract forms, prepare change of address records, or issue service discontinuance orders, using computers.
Part: Complete a contract form, change-of-address record, or service discontinuance order in the computer while the customer is on the line or at the desk.
Type: LIVE_SERVICE
Work item: one account order (contract, address change, or discontinuance) entered during a contact
Start: customer requests the change
End: order submitted and confirmation given to the customer
Checked by: the customer and the fulfilment or billing team that acts on the order

[2585b]
Occupation: Customer Service Representatives
Task statement: Obtain and examine all relevant information to assess validity of complaints and to determine possible causes, such as extreme weather conditions that could increase utility bills.
Part: Gather and examine records and outside information to investigate a complaint's validity and cause after the contact.
Type: DISCRETE
Work item: one complaint investigation with a validity finding
Start: complaint case opened for review
End: finding on validity and cause recorded and passed for remedy or reply
Checked by: supervisor, and the staff who decide the remedy

[14638b]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Design test plans, scenarios, scripts, or procedures.
Part: Design test scenarios, scripts, or procedures for software functionality.
Type: DISCRETE
Work item: one feature-level set of test cases or scripts
Start: feature requirements or test objectives are available
End: cases or scripts are ready for review and execution
Checked by: test lead and testers

[14638a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Design test plans, scenarios, scripts, or procedures.
Part: Design a test plan for a software change or release.
Type: DISCRETE
Work item: one test plan
Start: requirements and scope for the change or release are available
End: test plan is prepared and shared for review or use
Checked by: test lead and project team

[14639a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Test system modifications to prepare for implementation.
Part: Execute tests on a system modification and report whether it is ready for implementation.
Type: DISCRETE
Work item: one system modification tested (one test cycle)
Start: change deployed to the test environment and assigned for testing
End: test results recorded and change signed off or returned with defects
Checked by: release manager / development lead

[2578b]
Occupation: Customer Service Representatives
Task statement: Keep records of customer interactions or transactions, recording details of inquiries, complaints, or comments, as well as actions taken.
Part: Complete the interaction or transaction record (disposition codes, summary, actions taken) in after-call wrap-up.
Type: DISCRETE
Work item: one interaction record completed after a call or visit
Start: call or visit ends
End: record saved with disposition code, summary, and actions taken
Checked by: quality-assurance reviewer, supervisor, and later agents handling the account

[2580a]
Occupation: Customer Service Representatives
Task statement: Check to ensure that appropriate changes were made to resolve customers' problems.
Part: Check the account or order system to confirm that the change made to resolve a customer's problem was carried out correctly.
Type: DISCRETE
Work item: one resolution verified for a customer case
Start: follow-up date reached or confirmation of change expected
End: change confirmed and case closed, or discrepancy flagged and case reopened
Checked by: supervisor and the customer

[14650a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Update automated test scripts to ensure currency.
Part: Update automated test scripts to reflect product changes.
Type: DISCRETE
Work item: one set of automated test scripts updated for a product change
Start: product change breaks or outdates scripts
End: updated scripts reviewed, merged, and passing in the pipeline
Checked by: QA lead / code reviewer

[1286b]
Occupation: Computer User Support Specialists
Task statement: Set up equipment for employee use, performing or ensuring proper installation of cables, operating systems, or appropriate software.
Part: Install and configure the operating system, software, and accounts on a new employee's computer so it is ready for use.
Type: DISCRETE
Work item: one workstation configured and handed over to an employee
Start: setup request or new-starter ticket received with hardware available
End: machine imaged, software and accounts configured, handed to employee and ticket closed
Checked by: the employee; IT supervisor

[14658a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Identify program deviance from standards, and suggest modifications to ensure compliance.
Part: Check a program against standards and recommend modifications to bring it into compliance.
Type: DISCRETE
Work item: one standards-compliance review of a program with recommendations
Start: program or build submitted for compliance check
End: deviations and suggested changes sent to developers
Checked by: developers / QA lead

[14661a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Perform initial debugging procedures by reviewing configuration files, logs, or code pieces to determine breakdown source.
Part: Review configuration files, logs, or code to find the likely source of a failure.
Type: DISCRETE
Work item: one defect given an initial root-cause diagnosis
Start: failure reported or reproduced
End: likely source recorded on the ticket and handed to developers
Checked by: developers

[1291a]
Occupation: Computer User Support Specialists
Task statement: Refer major hardware or software problems or defective products to vendors or technicians for service.
Part: Refer a major hardware or software problem or a defective product to a vendor or specialist technician for service.
Type: DISCRETE
Work item: one vendor or technician service referral (case or RMA opened)
Start: problem judged beyond in-house repair or product found defective
End: case opened with vendor with problem details and warranty info, user informed, ticket updated
Checked by: vendor or technician; the affected user; IT supervisor

[14655a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Conduct software compatibility tests with programs, hardware, operating systems, or network environments.
Part: Run compatibility tests of a build across target programs, hardware, operating systems, or network environments.
Type: DISCRETE
Work item: one compatibility test cycle for a build
Start: build and configuration matrix ready
End: compatibility results recorded and issues filed
Checked by: QA lead / release manager

[14644a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Create or maintain databases of known test defects.
Part: Set up a database or tracker project for known test defects.
Type: DISCRETE
Work item: one known-defects database set up
Start: need for a defect repository agreed
End: database configured with fields and workflows and opened to the team
Checked by: QA manager / team users

[1297a]
Occupation: Computer User Support Specialists
Task statement: Conduct office automation feasibility studies, including workflow analysis, space design, or cost comparison analysis.
Part: Conduct an office automation feasibility study, including workflow analysis, space design, or cost comparison.
Type: DISCRETE
Work item: one office automation feasibility study report
Start: study requested or scoped
End: study with analysis and recommendation delivered to management
Checked by: IT manager; office or department management

[1290a]
Occupation: Computer User Support Specialists
Task statement: Develop training materials and procedures, or train users in the proper use of hardware or software.
Part: Write training materials or procedures for the proper use of hardware or software.
Type: DISCRETE
Work item: one training guide, how-to document, or procedure
Start: need for material identified (new system, recurring question)
End: material reviewed and published to users or the knowledge base
Checked by: IT supervisor; users who follow it

[14651a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Investigate customer problems referred by technical support.
Part: Investigate a customer problem referred by technical support and report the findings.
Type: DISCRETE
Work item: one escalated customer problem investigated
Start: escalation ticket received from technical support
End: problem reproduced or not, findings returned to support, and defect filed if needed
Checked by: technical support / developers

