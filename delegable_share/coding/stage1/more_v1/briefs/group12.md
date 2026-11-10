You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Below are 3 occupations. Code each occupation's TARGETS
independently, in the order given; do not go back and adjust earlier answers to
make them consistent with later ones, and do not let one occupation's coding
shape another's.

For each occupation, write ONE JSON array to its own file:
  Security Guards (33-9032.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/33-9032.00.json
  Waiters and Waitresses (35-3031.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/35-3031.00.json
  Fast Food and Counter Workers (35-3023.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/35-3023.00.json
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

=== OCCUPATION: Security Guards (33-9032.00) ===
Guard, patrol, or monitor premises to prevent theft, violence, or infractions of rules. May operate x-ray and metal detector equipment.

TASK LIST (context; every statement below is also a TARGET):
[2131] Patrol industrial or commercial premises to prevent and detect signs of intrusion and ensure security of doors, windows, and gates.
[2132] Answer alarms and investigate disturbances.
[2133] Monitor and authorize entrance and departure of employees, visitors, and other persons to guard against theft and maintain security of premises.
[2134] Write reports of daily activities and irregularities, such as equipment or property damage, theft, presence of unauthorized persons, or unusual occurrences.
[2135] Call police or fire departments in cases of emergency, such as fire or presence of unauthorized persons.
[2136] Circulate among visitors, patrons, or employees to preserve order and protect property.
[2137] Answer telephone calls to take messages, answer questions, and provide information during non-business hours or when switchboard is closed.
[2138] Warn persons of rule infractions or violations, and apprehend or evict violators from premises, using force when necessary.
[2139] Operate detecting devices to screen individuals and prevent passage of prohibited articles into restricted areas.
[2140] Escort or drive motor vehicle to transport individuals to specified locations or to provide personal protection.
[2141] Inspect and adjust security systems, equipment, or machinery to ensure operational use and to detect evidence of tampering.
[2143] Monitor and adjust controls that regulate building systems, such as air conditioning, furnace, or boiler.
[20894] Lock doors and gates of entrances and exits to secure buildings.
[20895] Respond to medical emergencies by administering basic first aid or by obtaining assistance from paramedics.

TARGETS: code all 14 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/33-9032.00.json.

=== OCCUPATION: Waiters and Waitresses (35-3031.00) ===
Take orders and serve food and beverages to patrons at tables in dining establishment.

TASK LIST (context; every statement below is also a TARGET):
[2275] Check patrons' identification to ensure that they meet minimum age requirements for consumption of alcoholic beverages.
[2276] Collect payments from customers.
[2277] Write patrons' food orders on order slips, memorize orders, or enter orders into computers for transmittal to kitchen staff.
[2278] Take orders from patrons for food or beverages.
[2279] Check with customers to ensure that they are enjoying their meals, and take action to correct any problems.
[2280] Serve food or beverages to patrons, and prepare or serve specialty dishes at tables as required.
[2281] Prepare checks that itemize and total meal costs and sales taxes.
[2283] Present menus to patrons and answer questions about menu items, making recommendations upon request.
[2284] Inform customers of daily specials.
[2285] Clean tables or counters after patrons have finished dining.
[2286] Prepare hot, cold, and mixed drinks for patrons, and chill bottles of wine.
[2287] Explain how various menu items are prepared, describing ingredients and cooking methods.
[2288] Prepare tables for meals, including setting up items such as linens, silverware, and glassware.
[2289] Perform food preparation duties, such as preparing salads, appetizers, and cold dishes, portioning desserts, and brewing coffee.
[2290] Stock service areas with supplies such as coffee, food, tableware, and linens.
[2291] Garnish and decorate dishes in preparation for serving.
[2292] Fill salt, pepper, sugar, cream, condiment, and napkin containers.
[2293] Escort customers to their tables.
[2294] Describe and recommend wines to customers.
[2295] Bring wine selections to tables with appropriate glasses, and pour the wines for customers.
[18744] Roll silverware, set up food stations, or set up dining areas to prepare for the next shift or for large parties.
[18745] Remove dishes and glasses from tables or counters, and take them to kitchen for cleaning.
[18746] Assist host or hostess by answering phones to take reservations or to-go orders, and by greeting, seating, and thanking guests.
[18747] Perform cleaning duties, such as sweeping and mopping floors, vacuuming carpet, tidying up server station, taking out trash, or checking and cleaning bathroom.
[18748] Provide guests with information about local areas, including directions.

TARGETS: code all 25 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/35-3031.00.json.

=== OCCUPATION: Fast Food and Counter Workers (35-3023.00) ===
Perform duties such as taking orders and serving food and beverages. Serve customers at counter or from a steam table. May take payment. May prepare food and beverages.

TASK LIST (context; every statement below is also a TARGET):
[23099] Communicate with customers regarding orders, comments, and complaints.
[23100] Accept payment from customers, and make change as necessary.
[23101] Scrub and polish counters, steam tables, and other equipment, and clean glasses, dishes, and fountain equipment.
[23102] Perform cleaning duties, such as sweeping, mopping, and washing dishes, to keep equipment and facilities sanitary.
[23103] Balance receipts and payments in cash registers.
[23104] Request and record customer orders, and compute bills, using cash registers, multi-counting machines, or pencil and paper.
[23105] Serve food, beverages, or desserts to customers in such settings as take-out counters of restaurants or lunchrooms, business or industrial establishments, hotel rooms, and cars.
[23106] Prepare daily food items, and cook simple foods and beverages, such as sandwiches, salads, soups, pizza, or coffee, using proper safety precautions and sanitary measures.
[23107] Clean and organize eating, service, and kitchen areas.
[23108] Monitor and order supplies or food items, and restock as necessary to maintain inventory.
[23109] Brew coffee and tea, and fill containers with requested beverages.
[23110] Serve customers in eating places that specialize in fast service and inexpensive carry-out food.
[23111] Collect and return dirty dishes to the kitchen for washing.
[23112] Wash dishes, glassware, and silverware after meals.
[23113] Wrap menu items such as sandwiches, hot entrees, and desserts for serving or for takeout.
[23114] Notify kitchen personnel of shortages or special orders.
[23115] Prepare and serve cold drinks, frozen milk drinks, or desserts, using drink-dispensing, milkshake, or frozen-custard machines.
[23116] Select food items from serving or storage areas and place them in dishes, on serving trays, or in take-out bags.
[23117] Replenish foods at serving stations.
[23118] Perform personnel activities, such as supervising and training employees.
[23119] Take customers' orders and write ordered items on tickets, giving ticket stubs to customers when needed to identify filled orders.
[23120] Distribute food to servers.
[23121] Set up dining areas for meals, and clear them following meals.
[23122] Add relishes and garnishes to food orders, according to instructions.
[23123] Deliver orders to kitchens, and pick up and serve food when it is ready.
[23124] Arrange tables and decorations according to instructions.
[23125] Plan, prepare, and deliver meals to individuals with special dietary needs.

TARGETS: code all 27 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/35-3023.00.json.
