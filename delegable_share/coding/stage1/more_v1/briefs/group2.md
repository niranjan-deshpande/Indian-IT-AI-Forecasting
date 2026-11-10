You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Below are 3 occupations. Code each occupation's TARGETS
independently, in the order given; do not go back and adjust earlier answers to
make them consistent with later ones, and do not let one occupation's coding
shape another's.

For each occupation, write ONE JSON array to its own file:
  Data Scientists (15-2051.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/15-2051.00.json
  Retail Salespersons (41-2031.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/41-2031.00.json
  Cashiers (41-2011.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/41-2011.00.json
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

=== OCCUPATION: Data Scientists (15-2051.00) ===
Develop and implement a set of techniques or analytics applications to transform raw data into meaningful information using data-oriented programming languages and visualization software. Apply data mining, data modeling, natural language processing, and machine learning to extract and analyze information from large structured and unstructured datasets. Visualize, interpret, and report data findings. May create dynamic data reports.

TASK LIST (context; every statement below is also a TARGET):
[21823] Analyze, manipulate, or process large sets of data using statistical software.
[21824] Apply feature selection algorithms to models predicting outcomes of interest, such as sales, attrition, and healthcare use.
[21825] Apply sampling techniques to determine groups to be surveyed or use complete enumeration methods.
[21826] Clean and manipulate raw data using statistical software.
[21827] Compare models using statistical performance metrics, such as loss functions or proportion of explained variance.
[21828] Create graphs, charts, or other visualizations to convey the results of data analysis using specialized software.
[21829] Deliver oral or written presentations of the results of mathematical modeling and data analysis to management or other end users.
[21830] Design surveys, opinion polls, or other instruments to collect data.
[21831] Identify business problems or management objectives that can be addressed through data analysis.
[21832] Identify relationships and trends or any factors that could affect the results of research.
[21833] Identify solutions to business problems, such as budgeting, staffing, and marketing decisions, using the results of data analysis.
[21834] Propose solutions in engineering, the sciences, and other fields using mathematical theories and techniques.
[21835] Read scientific articles, conference papers, or other sources of research to identify emerging analytic trends and technologies.
[21836] Recommend data-driven solutions to key stakeholders.
[21837] Test, validate, and reformulate models to ensure accurate prediction of outcomes of interest.
[21838] Write new functions or applications in programming languages to conduct analyses.

TARGETS: code all 16 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/15-2051.00.json.

=== OCCUPATION: Retail Salespersons (41-2031.00) ===
Sell merchandise, such as furniture, motor vehicles, appliances, or apparel to consumers.

TASK LIST (context; every statement below is also a TARGET):
[694] Greet customers and ascertain what each customer wants or needs.
[695] Open and close cash registers, performing tasks such as counting money, separating charge slips, coupons, and vouchers, balancing cash drawers, and making deposits.
[696] Maintain knowledge of current sales and promotions, policies regarding payment and exchanges, and security practices.
[697] Compute sales prices, total purchases, and receive and process cash or credit payment.
[698] Maintain records related to sales.
[699] Watch for and recognize security risks and thefts and know how to prevent or handle these situations.
[700] Recommend, select, and help locate or obtain merchandise based on customer needs and desires.
[701] Answer questions regarding the store and its merchandise.
[702] Describe merchandise and explain use, operation, and care of merchandise to customers.
[703] Ticket, arrange, and display merchandise to promote sales.
[704] Prepare sales slips or sales contracts.
[705] Place special orders or call other stores to find desired items.
[706] Demonstrate use or operation of merchandise.
[707] Clean shelves, counters, and tables.
[708] Exchange merchandise for customers and accept returns.
[709] Bag or package purchases and wrap gifts.
[710] Help customers try on or fit merchandise.
[711] Inventory stock and requisition new stock.
[712] Prepare merchandise for purchase or rental.
[713] Sell or arrange for delivery, insurance, financing, or service contracts for merchandise.
[714] Estimate and quote trade-in allowances.
[715] Estimate cost of repair or alteration of merchandise.
[716] Estimate quantity and cost of merchandise required, such as paint or floor covering.
[717] Rent merchandise to customers.

TARGETS: code all 24 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/41-2031.00.json.

=== OCCUPATION: Cashiers (41-2011.00) ===
Receive and disburse money in establishments other than financial institutions. May use electronic scanners, cash registers, or related equipment. May process credit or debit card transactions and validate checks.

TASK LIST (context; every statement below is also a TARGET):
[2400] Receive payment by cash, check, credit cards, vouchers, or automatic debits.
[2401] Issue receipts, refunds, credits, or change due to customers.
[2402] Count money in cash drawers at the beginning of shifts to ensure that amounts are correct and that there is adequate change.
[2403] Greet customers entering establishments.
[2405] Establish or identify prices of goods, services, or admission, and tabulate bills, using calculators, cash registers, or optical price scanners.
[2406] Issue trading stamps, and redeem food stamps and coupons.
[2408] Answer customers' questions, and provide information on procedures or policies.
[2409] Cash checks for customers.
[2410] Weigh items sold by weight to determine prices.
[2411] Calculate total payments received during a time period, and reconcile this with total sales.
[2412] Compute and record totals of transactions.
[2413] Sell tickets and other items to customers.
[2414] Keep periodic balance sheets of amounts and numbers of transactions.
[2415] Bag, box, wrap, or gift-wrap merchandise, and prepare packages for shipment.
[2416] Sort, count, and wrap currency and coins.
[2417] Process merchandise returns and exchanges.
[2419] Request information or assistance, using paging systems.
[2421] Compile and maintain non-monetary reports and records.
[2422] Monitor checkout stations to ensure they have adequate cash available and are staffed appropriately.
[2423] Post charges against guests' or patients' accounts.
[2424] Offer customers carry-out service at the completion of transactions.
[18765] Assist customers by providing information and resolving their complaints.
[18766] Maintain clean and orderly checkout areas, and complete other general cleaning duties, such as mopping floors and emptying trash cans.
[18767] Assist with duties in other areas of the store, such as monitoring fitting rooms or bagging and carrying out customers' items.
[18768] Supervise others and provide on-the-job training.
[21072] Help customers find the location of products.
[21073] Answer incoming phone calls.
[21074] Stock shelves, sort and reshelve returned items, and mark prices on items and shelves.

TARGETS: code all 28 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/41-2011.00.json.
