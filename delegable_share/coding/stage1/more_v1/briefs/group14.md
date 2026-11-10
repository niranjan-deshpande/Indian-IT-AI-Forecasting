You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Below are 3 occupations. Code each occupation's TARGETS
independently, in the order given; do not go back and adjust earlier answers to
make them consistent with later ones, and do not let one occupation's coding
shape another's.

For each occupation, write ONE JSON array to its own file:
  Shipping, Receiving, and Inventory Clerks (43-5071.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/43-5071.00.json
  Medical Secretaries and Administrative Assistants (43-6013.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/43-6013.00.json
  First-Line Supervisors of Office and Administrative Support Workers (43-1011.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/43-1011.00.json
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

=== OCCUPATION: Shipping, Receiving, and Inventory Clerks (43-5071.00) ===
Verify and maintain records on incoming and outgoing shipments involving inventory. Duties include verifying and recording incoming merchandise or material and arranging for the transportation of products. May prepare items for shipment.

TASK LIST (context; every statement below is also a TARGET):
[4737] Prepare documents, such as work orders, bills of lading, or shipping orders, to route materials.
[4739] Record shipment data, such as weight, charges, space availability, damages, or discrepancies, for reporting, accounting, or recordkeeping purposes.
[4740] Contact carrier representatives to make arrangements or to issue instructions for shipping and delivery of materials.
[4741] Confer or correspond with establishment representatives to rectify problems, such as damages, shortages, or nonconformance to specifications.
[4742] Requisition and store shipping materials and supplies to maintain inventory of stock.
[4744] Compute amounts, such as space available, shipping, storage, or demurrage charges, using computer or price list.
[19834] Compare shipping routes or methods to determine which have the least environmental impact.
[20276] Examine shipment contents and compare with records, such as manifests, invoices, or orders, to verify accuracy.
[20277] Pack, seal, label, or affix postage to prepare materials for shipping, using hand tools, power tools, or postage meter.
[20278] Deliver or route materials to departments using handtruck, conveyor, or sorting bins.
[20279] Determine shipping methods, routes, or rates for materials to be shipped.

TARGETS: code all 11 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/43-5071.00.json.

=== OCCUPATION: Medical Secretaries and Administrative Assistants (43-6013.00) ===
Perform secretarial duties using specific knowledge of medical terminology and hospital, clinic, or laboratory procedures. Duties may include scheduling appointments, billing patients, and compiling and recording medical charts, reports, and correspondence.

TASK LIST (context; every statement below is also a TARGET):
[775] Schedule and confirm patient diagnostic appointments, surgeries, or medical consultations.
[776] Compile and record medical charts, reports, or correspondence, using typewriter or personal computer.
[777] Answer telephones and direct calls to appropriate staff.
[778] Receive and route messages or documents, such as laboratory results, to appropriate staff.
[779] Greet visitors, ascertain purpose of visit, and direct them to appropriate staff.
[780] Interview patients to complete documents, case histories, or forms, such as intake or insurance forms.
[781] Maintain medical records, technical library, or correspondence files.
[782] Operate office equipment, such as voice mail messaging systems, and use word processing, spreadsheet, or other software applications to prepare reports, invoices, financial statements, letters, case histories, or medical records.
[783] Transmit correspondence or medical records by mail, e-mail, or fax.
[784] Perform various clerical or administrative functions, such as ordering and maintaining an inventory of supplies.
[786] Transcribe recorded messages or practitioners' diagnoses or recommendations into patients' medical records.
[787] Perform bookkeeping duties, such as credits or collections, preparing and sending financial statements or bills, and keeping financial records.
[788] Complete insurance or other claim forms.
[789] Prepare correspondence or assist physicians or medical scientists with preparation of reports, speeches, articles, or conference proceedings.
[20438] Schedule tests or procedures for patients, such as lab work or x-rays, based on physician orders.

TARGETS: code all 15 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/43-6013.00.json.

=== OCCUPATION: First-Line Supervisors of Office and Administrative Support Workers (43-1011.00) ===
Directly supervise and coordinate the activities of clerical and administrative support workers.

TASK LIST (context; every statement below is also a TARGET):
[9703] Resolve customer complaints or answer customers' questions regarding policies and procedures.
[9704] Supervise the work of office, administrative, or customer service employees to ensure adherence to quality standards, deadlines, and proper procedures, correcting errors or problems.
[9705] Provide employees with guidance in handling difficult or complex problems or in resolving escalated complaints or disputes.
[9706] Implement corporate or departmental policies, procedures, and service standards in conjunction with management.
[9707] Discuss job performance problems with employees to identify causes and issues and to work on resolving problems.
[9708] Train or instruct employees in job duties or company policies or arrange for training to be provided.
[9709] Evaluate employees' job performance and conformance to regulations and recommend appropriate personnel action.
[9710] Review records or reports pertaining to activities such as production, payroll, or shipping to verify details, monitor work activities, or evaluate performance.
[9711] Recruit, interview, and select employees.
[9712] Interpret and communicate work procedures and company policies to staff.
[9713] Prepare and issue work schedules, deadlines, and duty assignments for office or administrative staff.
[9714] Maintain records pertaining to inventory, personnel, orders, supplies, or machine maintenance.
[9715] Compute figures such as balances, totals, or commissions.
[9716] Research, compile, and prepare reports, manuals, correspondence, or other information required by management or governmental agencies.
[9717] Coordinate activities with other supervisory personnel or with other work units or departments.
[9718] Analyze financial activities of establishments or departments and provide input into budget planning and preparation processes.
[9719] Develop or update procedures, policies, or standards.
[9720] Make recommendations to management concerning such issues as staffing decisions or procedural changes.
[9721] Consult with managers or other personnel to resolve problems in areas such as equipment performance, output quality, or work schedules.
[9722] Participate in the work of subordinates to facilitate productivity or to overcome difficult aspects of work.
[9723] Design, implement, or evaluate staff training and development programs, customer service initiatives, or performance measurement criteria.
[9724] Develop work schedules according to budgets and workloads.
[9725] Monitor inventory levels and requisition or purchase supplies as needed.
[9727] Plan for or coordinate office services, such as equipment or supply acquisition or organization, disposal of assets, relocation, parking, maintenance, or security services.
[9728] Arrange for necessary maintenance or repair work.
[9729] Keep informed of provisions of labor-management agreements and their effects on departmental operations.
[9730] Coordinate or perform activities associated with shipping, receiving, distribution, or transportation.
[9731] Plan layouts of stockrooms, warehouses, or other storage areas, considering turnover, size, weight, or related factors pertaining to items stored.

TARGETS: code all 28 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/43-1011.00.json.
