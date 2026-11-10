You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Code each ITEM independently, in the order given; do not go
back and adjust earlier answers to make them consistent with later ones.

Write ONE JSON array to:
  /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage2/pilot/s1/batch2.json
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
[14647a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Review software documentation to ensure technical accuracy, compliance, or completeness, or to mitigate risks.
Part: Review a software document for technical accuracy, compliance, completeness, and risks, and return findings.
Type: DISCRETE
Work item: one software document reviewed with findings
Start: document submitted for review
End: findings returned or document approved
Checked by: document author / QA lead

[2581a]
Occupation: Customer Service Representatives
Task statement: Contact customers to respond to inquiries or to notify them of claim investigation results or any planned adjustments.
Part: Write and send a response to a customer's inquiry or a notification of claim investigation results or a planned adjustment.
Type: DISCRETE
Work item: one written response or notification sent to a customer
Start: inquiry or investigation result ready for response
End: letter or email sent and logged on the account
Checked by: the customer, and supervisor or QA reviewer

[2583a]
Occupation: Customer Service Representatives
Task statement: Determine charges for services requested, collect deposits or payments, or arrange for billing.
Part: Determine the charges for a requested service and collect a deposit or payment, or set up billing, while the customer is on the line or at the desk.
Type: LIVE_SERVICE
Work item: one service charge determined and payment or billing arrangement completed during a contact
Start: customer requests a service
End: charge quoted, payment or deposit taken or billing arranged, receipt or confirmation given
Checked by: the customer, and cash-office or billing reconciliation

[14664a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Conduct historical analyses of test results.
Part: Analyze historical test results for trends and report the findings.
Type: DISCRETE
Work item: one historical test results analysis report
Start: pull of past test results
End: report with trends and recommendations sent
Checked by: QA manager

[2591a]
Occupation: Customer Service Representatives
Task statement: Recommend improvements in products, packaging, shipping, service, or billing methods and procedures to prevent future problems.
Part: Write a recommendation to management for an improvement in products, packaging, shipping, service, or billing procedures based on recurring customer problems.
Type: DISCRETE
Work item: one improvement recommendation submitted
Start: recurring problem identified from customer contacts
End: recommendation with supporting examples sent to supervisor or process owner
Checked by: supervisor or the department that owns the process

[18565c]
Occupation: Customer Service Representatives
Task statement: Confer with customers by telephone or in person to provide information about products or services, take or enter orders, cancel accounts, or obtain details of complaints.
Part: Obtain the details of a customer's complaint during a call or visit.
Type: LIVE_SERVICE
Work item: one complaint taken during a call or visit
Start: customer raises a complaint
End: complaint details captured and next steps explained to the customer
Checked by: the customer and the staff who investigate or resolve it

[14659a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Design or develop automated testing tools.
Part: Design and build an automated testing tool or framework component.
Type: DISCRETE
Work item: one automated testing tool or framework component
Start: tool need or specification agreed
End: tool reviewed, merged, and in use by the team
Checked by: QA lead / code reviewer

[1285a]
Occupation: Computer User Support Specialists
Task statement: Oversee the daily performance of computer systems.
Part: Follow up a performance problem or alert on a computer system during the day and decide what action is needed.
Type: DISCRETE
Work item: one performance alert or problem followed up
Start: alert raised or slowdown noticed or reported
End: cause recorded and fix applied, escalated, or closed as no action
Checked by: IT supervisor; systems administrators

[1296a]
Occupation: Computer User Support Specialists
Task statement: Modify and customize commercial programs for internal needs.
Part: Modify or customize a commercial program (e.g. templates, macros, configuration, scripts) to meet internal needs.
Type: DISCRETE
Work item: one program customization delivered (template, macro, configuration change)
Start: customization request received
End: change tested and released to users
Checked by: requesting users; IT supervisor

[14662a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Visit beta testing sites to evaluate software performance.
Part: Evaluate software performance at a beta testing site.
Type: DISCRETE
Work item: one beta-site performance evaluation
Start: a beta site and evaluation objectives are identified
End: site observations and performance findings are documented or shared
Checked by: product team and test lead

[14652a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Install, maintain, or use software testing programs.
Part: Install, configure, or upgrade a software testing tool.
Type: DISCRETE
Work item: one testing tool installed or upgraded
Start: tool install or upgrade requested
End: tool working and available to the team
Checked by: QA team users / QA lead

[14656a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Install and configure recreations of software production environments to allow testing of software performance.
Part: Install and configure a recreation of the production environment for performance testing.
Type: DISCRETE
Work item: one test environment built to mirror production
Start: environment request with production specification
End: environment configured, verified, and handed to testers
Checked by: QA lead / performance testers

[14663a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Evaluate or recommend software for testing or bug tracking.
Part: Evaluate testing or bug tracking software and recommend whether to adopt it.
Type: DISCRETE
Work item: one tool evaluation with recommendation
Start: tool need or candidate tools identified
End: evaluation and recommendation sent to the QA manager
Checked by: QA manager

[15204a]
Occupation: Computer User Support Specialists
Task statement: Hire, supervise, and direct workers engaged in special project work, problem-solving, monitoring, and installation of data communication equipment and software.
Part: Hire workers for special project, monitoring, and installation work: screen candidates, interview, and decide on hires.
Type: DISCRETE
Work item: one vacancy filled (hiring decision made)
Start: vacancy approved and applications received
End: candidate selected and recommendation or offer sent to HR
Checked by: HR; hiring manager

[2585a]
Occupation: Customer Service Representatives
Task statement: Obtain and examine all relevant information to assess validity of complaints and to determine possible causes, such as extreme weather conditions that could increase utility bills.
Part: Look up account and usage information during the call to assess whether a complaint is valid and explain the likely cause.
Type: LIVE_SERVICE
Work item: one complaint assessed during a call or visit
Start: customer describes the complaint
End: validity and likely cause explained to the customer and noted
Checked by: the customer and QA reviewer

[1284b]
Occupation: Computer User Support Specialists
Task statement: Install and perform minor repairs to hardware, software, or peripheral equipment, following design or installation specifications.
Part: Install software or make minor software repairs (reinstall, patch, reconfigure) on a user's computer following installation specifications.
Type: DISCRETE
Work item: one software installation or minor software repair completed on a machine
Start: install or repair request received
End: software installed or fixed and ticket closed
Checked by: the user; support lead

[14654a]
Occupation: Software Quality Assurance Analysts and Testers
Task statement: Monitor program performance to ensure efficient and problem-free operations.
Part: Investigate a performance issue identified through program monitoring.
Type: DISCRETE
Work item: one monitored performance issue investigated
Start: monitoring reveals a performance anomaly or threshold breach
End: findings are recorded and the issue is closed or escalated
Checked by: developers and operations or test lead

