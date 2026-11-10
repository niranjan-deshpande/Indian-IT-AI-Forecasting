You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Below are 3 occupations. Code each occupation's TARGETS
independently, in the order given; do not go back and adjust earlier answers to
make them consistent with later ones, and do not let one occupation's coding
shape another's.

For each occupation, write ONE JSON array to its own file:
  Registered Nurses (29-1141.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/comp_v1/29-1141.00.json
  Childcare Workers (39-9011.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/comp_v1/39-9011.00.json
  Janitors and Cleaners, Except Maids and Housekeeping Cleaners (37-2011.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/comp_v1/37-2011.00.json
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

=== OCCUPATION: Registered Nurses (29-1141.00) ===
Assess patient health problems and needs, develop and implement nursing care plans, and maintain medical records. Administer nursing care to ill, injured, convalescent, or disabled patients. May advise patients on health maintenance and disease prevention or provide case management. Licensing or registration required.

TASK LIST (context; every statement below is also a TARGET):
[1839] Maintain accurate, detailed reports and records.
[1840] Monitor, record, and report symptoms or changes in patients' conditions.
[1841] Record patients' medical information and vital signs.
[1842] Modify patient treatment plans as indicated by patients' responses and conditions.
[1843] Consult and coordinate with healthcare team members to assess, plan, implement, or evaluate patient care plans.
[1844] Order, interpret, and evaluate diagnostic tests to identify and assess patient's condition.
[1845] Monitor all aspects of patient care, including diet and physical activity.
[1846] Direct or supervise less-skilled nursing or healthcare personnel or supervise a particular unit.
[1847] Prepare patients for and assist with examinations or treatments.
[1848] Observe nurses and visit patients to ensure proper nursing care.
[1849] Assess the needs of individuals, families, or communities, including assessment of individuals' home or work environments, to identify potential health or safety problems.
[1850] Instruct individuals, families, or other groups on topics such as health education, disease prevention, or childbirth and develop health improvement programs.
[1851] Prepare rooms, sterile instruments, equipment, or supplies and ensure that stock of supplies is maintained.
[1852] Inform physician of patient's condition during anesthesia.
[1854] Administer local, inhalation, intravenous, or other anesthetics.
[1855] Provide health care, first aid, immunizations, or assistance in convalescence or rehabilitation in locations such as schools, hospitals, or industry.
[1856] Perform physical examinations, make tentative diagnoses, and treat patients en route to hospitals or at disaster site triage centers.
[1857] Conduct specified laboratory tests.
[1859] Prescribe or recommend drugs, medical devices, or other forms of treatment, such as physical therapy, inhalation therapy, or related therapeutic procedures.
[1860] Direct or coordinate infection control programs, advising or consulting with specified personnel about necessary precautions.
[1861] Perform administrative or managerial functions, such as taking responsibility for a unit's staff, budget, planning, or long-range goals.
[1862] Provide or arrange for training or instruction of auxiliary personnel or students.
[1863] Refer students or patients to specialized health resources or community agencies furnishing assistance.
[1864] Consult with institutions or associations regarding issues or concerns relevant to the practice and profession of nursing.
[1865] Work with individuals, groups, or families to plan or implement programs designed to improve the overall health of communities.
[1866] Engage in research activities related to nursing.
[20413] Administer medications to patients and monitor patients for reactions or side effects.

TARGETS: code all 27 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/comp_v1/29-1141.00.json.

=== OCCUPATION: Childcare Workers (39-9011.00) ===
Attend to children at schools, businesses, private households, and childcare institutions. Perform a variety of tasks, such as dressing, feeding, bathing, and overseeing play.

TASK LIST (context; every statement below is also a TARGET):
[2331] Support children's emotional and social development, encouraging understanding of others and positive self-concepts.
[2332] Care for children in institutional setting, such as group homes, nursery schools, private businesses, or schools for people with disabilities.
[2333] Sanitize toys and play equipment.
[2334] Discipline children and recommend or initiate other measures to control behavior, such as caring for own clothing and picking up toys and books.
[2335] Identify signs of emotional or developmental problems in children and bring them to parents' or guardians' attention.
[2336] Observe and monitor children's play activities.
[2337] Keep records on individual children, including daily observations and information about activities, meals served, and medications administered.
[2338] Instruct children in health and personal habits, such as eating, resting, and toilet habits.
[2339] Read to children and teach them simple painting, drawing, handicrafts, and songs.
[2342] Organize and store toys and materials to ensure order in activity areas.
[2344] Sterilize bottles and prepare formulas.
[2346] Dress children and change diapers.
[2347] Help children with homework and school work.
[2348] Perform housekeeping duties, such as laundry, cleaning, dish washing, and changing of linens.
[2349] Accompany children to and from school, on outings, and to medical appointments.
[18756] Maintain a safe play environment.
[18757] Communicate with children's parents or guardians about daily activities, behaviors, and related issues.
[18758] Assist in preparing food and serving meals and refreshments to children.
[18759] Create developmentally appropriate lesson plans.
[18760] Regulate children's rest periods.
[18761] Perform general administrative tasks, such as taking attendance, editing internal paperwork, and making phone calls.
[18762] Organize and participate in recreational activities and outings, such as games and field trips.
[18763] Provide care for children with physical, developmental, or mental health disabilities.
[18764] Perform general personnel functions, such as supervision, training, and scheduling.

TARGETS: code all 24 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/comp_v1/39-9011.00.json.

=== OCCUPATION: Janitors and Cleaners, Except Maids and Housekeeping Cleaners (37-2011.00) ===
Keep buildings in clean and orderly condition. Perform heavy cleaning duties, such as cleaning floors, shampooing rugs, washing walls and glass, and removing rubbish. Duties may include tending furnace and boiler, performing routine maintenance activities, notifying management of need for repairs, and cleaning snow or debris from sidewalk.

TASK LIST (context; every statement below is also a TARGET):
[9538] Service, clean, or supply restrooms.
[9539] Gather and empty trash.
[9540] Clean building floors by sweeping, mopping, scrubbing, or vacuuming.
[9541] Follow procedures for the use of chemical cleaners and power equipment to prevent damage to floors and fixtures.
[9542] Mix water and detergents or acids in containers to prepare cleaning solutions, according to specifications.
[9543] Strip, seal, finish, and polish floors.
[9544] Notify managers concerning the need for major repairs or additions to building operating systems.
[9545] Requisition supplies or equipment needed for cleaning and maintenance duties.
[9546] Clean windows, glass partitions, or mirrors, using soapy water or other cleaners, sponges, or squeegees.
[9547] Steam-clean or shampoo carpets.
[9548] Set up, arrange, or remove decorations, tables, chairs, ladders, or scaffolding to prepare facilities for events, such as banquets or meetings.
[9549] Clean and polish furniture and fixtures.
[9550] Dust furniture, walls, machines, or equipment.
[9551] Move heavy furniture, equipment, or supplies, either manually or with hand trucks.
[9552] Remove snow from sidewalks, driveways, or parking areas, using snowplows, snow blowers, or snow shovels, or spread snow-melting chemicals.
[9554] Spray insecticides or fumigants to prevent insect or rodent infestation.
[9555] Make adjustments or minor repairs to heating, cooling, ventilating, plumbing, or electrical systems.
[9559] Clean chimneys, flues, and connecting pipes, using power or hand tools.
[20590] Monitor building security and safety by performing tasks such as locking doors after operating hours or checking electrical appliance use to ensure that hazards are not created.
[20591] Mow or trim lawns or shrubbery, using mowers or hand or power trimmers, and clear debris from grounds.
[20592] Drive vans, industrial trucks, or other vehicles required to travel to, or to perform, cleaning work.

TARGETS: code all 21 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/comp_v1/37-2011.00.json.
