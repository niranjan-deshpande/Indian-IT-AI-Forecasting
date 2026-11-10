You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Below are 3 occupations. Code each occupation's TARGETS
independently, in the order given; do not go back and adjust earlier answers to
make them consistent with later ones, and do not let one occupation's coding
shape another's.

For each occupation, write ONE JSON array to its own file:
  Carpenters (47-2031.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/47-2031.00.json
  Maintenance and Repair Workers, General (49-9071.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/49-9071.00.json
  Team Assemblers (51-2092.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/51-2092.00.json
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

=== OCCUPATION: Carpenters (47-2031.00) ===
Construct, erect, install, or repair structures and fixtures made of wood and comparable materials, such as concrete forms; building frameworks, including partitions, joists, studding, and rafters; and wood stairways, window and door frames, and hardwood floors. May also install cabinets, siding, drywall, and batt or roll insulation. Includes brattice builders who build doors or brattices (ventilation walls or partitions) in underground passageways.

TASK LIST (context; every statement below is also a TARGET):
[23430] Follow established safety rules and regulations and maintain a safe and clean environment.
[23431] Study specifications in blueprints, sketches, or building plans to prepare project layout and determine dimensions and materials required.
[23432] Measure and mark cutting lines on materials, using a ruler, pencil, chalk, and marking gauge.
[23433] Shape or cut materials to specified measurements, using hand tools, machines, or power saws.
[23434] Install structures or fixtures, such as windows, frames, floorings, trim, or hardware, using carpenters' hand or power tools.
[23435] Verify trueness of structure, using plumb bob and level.
[23436] Select and order lumber or other required materials.
[23437] Arrange for subcontractors to deal with special areas, such as heating or electrical wiring work.
[23438] Maintain records, document actions, and present written progress reports.
[23439] Build or repair cabinets, doors, frameworks, floors, or other wooden fixtures used in buildings, using woodworking machines, carpenter's hand tools, or power tools.
[23440] Erect scaffolding or ladders for assembling structures above ground level.
[23441] Anchor and brace forms and other structures in place, using nails, bolts, anchor rods, steel cables, planks, wedges, and timbers.
[23442] Inspect ceiling or floor tile, wall coverings, siding, glass, or woodwork to detect broken or damaged structures.
[23443] Assemble and fasten materials to make frameworks or props, using hand tools and wood screws, nails, dowel pins, or glue.
[23444] Bore boltholes in timber, masonry or concrete walls, using power drill.
[23445] Maintain job records and schedule work crew.
[23446] Remove damaged or defective parts or sections of structures and repair or replace, using hand tools.
[23447] Install rough door and window frames, subflooring, fixtures, or temporary supports in structures undergoing construction or repair.
[23448] Finish surfaces of woodwork or wallboard in houses or buildings, using paint, hand tools, or paneling.
[23449] Examine structural timbers and supports to detect decay, and replace timbers as required, using hand tools, nuts, and bolts.
[23450] Apply shock-absorbing, sound-deadening, or decorative paneling to ceilings or walls.
[23451] Cover subfloors with building paper to keep out moisture and lay hardwood, parquet, or wood-strip-block floors by nailing floors to subfloor or cementing them to mastic or asphalt base.
[23452] Fill cracks or other defects in plaster or plasterboard and sand patch, using patching plaster, trowel, and sanding tool.
[23453] Perform minor plumbing, welding, or concrete mixing work.
[23454] Prepare cost estimates for clients or employers.
[23455] Construct forms or chutes for pouring concrete.
[23456] Build sleds from logs and timbers for use in hauling camp buildings and machinery through wooded areas.
[23457] Work with or remove hazardous material.
[23458] Dig or direct digging of post holes and set poles to support structures.

TARGETS: code all 29 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/47-2031.00.json.

=== OCCUPATION: Maintenance and Repair Workers, General (49-9071.00) ===
Perform work involving the skills of two or more maintenance or craft occupations to keep machines, mechanical equipment, or the structure of a building in repair. Duties may involve pipe fitting; HVAC maintenance; insulating; welding; machining; carpentry; repairing electrical or mechanical equipment; installing, aligning, and balancing new equipment; and repairing buildings, floors, or stairs.

TASK LIST (context; every statement below is also a TARGET):
[3022] Assemble, install, or repair wiring, electrical or electronic components, pipe systems, plumbing, machinery, or equipment.
[3023] Diagnose mechanical problems and determine how to correct them, checking blueprints, repair manuals, or parts catalogs, as necessary.
[3024] Inspect, operate, or test machinery or equipment to diagnose machine malfunctions.
[3025] Record type and cost of maintenance or repair work.
[3026] Clean or lubricate shafts, bearings, gears, or other parts of machinery.
[3028] Plan and lay out repair work, using diagrams, drawings, blueprints, maintenance manuals, or schematic diagrams.
[3030] Adjust functional parts of devices or control instruments, using hand tools, levels, plumb bobs, or straightedges.
[3031] Paint or repair roofs, windows, doors, floors, woodwork, plaster, drywall, or other parts of building structures.
[3032] Operate cutting torches or welding equipment to cut or join metal parts.
[3033] Align and balance new equipment after installation.
[3034] Inspect used parts to determine changes in dimensional requirements, using rules, calipers, micrometers, or other measuring instruments.
[3035] Set up and operate machine tools to repair or fabricate machine parts, jigs, fixtures, or tools.
[3037] Fabricate or repair counters, benches, partitions, or other wooden structures, such as sheds or outbuildings.
[19897] Assemble boilers at installation sites, using tools such as levels, plumb bobs, hammers, torches, or other hand tools.
[19898] Install equipment to improve the energy or operational efficiency of residential or commercial buildings.
[19899] Perform routine maintenance on boilers, such as replacing burners or hoses, installing replacement parts, or reinforcing structural weaknesses to ensure optimal boiler efficiency.
[19900] Position, attach, or blow insulating materials to prevent energy losses from buildings, pipes, or other structures or objects.
[20670] Dismantle machines, equipment, or devices to access and remove defective parts, using hoists, cranes, hand tools, or power tools.
[20671] Perform routine maintenance, such as inspecting drives, motors, or belts, checking fluid levels, replacing filters, or doing other preventive maintenance actions.
[20672] Repair machines, equipment, or structures, using tools such as hammers, hoists, saws, drills, wrenches, or equipment such as precision measuring instruments or electrical or electronic testing devices.
[20673] Maintain or repair specialized equipment or machinery located in cafeterias, laundries, hospitals, stores, offices, or factories.
[20674] Order parts, supplies, or equipment from catalogs or suppliers.
[20675] Perform general cleaning of buildings or properties.
[20676] Train or manage maintenance personnel or subcontractors.
[20677] Provide groundskeeping services, such as landscaping or snow removal.
[20678] Estimate costs to repair machinery, equipment, or building structures.
[20679] Design new equipment to aid in the repair or maintenance of machines, mechanical equipment, or building structures.

TARGETS: code all 27 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/49-9071.00.json.

=== OCCUPATION: Team Assemblers (51-2092.00) ===
Work as part of a team having responsibility for assembling an entire product or component of a product. Team assemblers can perform all tasks conducted by the team in the assembly process and rotate through all or most of them, rather than being assigned to a specific task on a permanent basis. May participate in making management decisions affecting the work. Includes team leaders who work as part of the team.

TASK LIST (context; every statement below is also a TARGET):
[8468] Rotate through all the tasks required in a particular production process.
[8469] Determine work assignments and procedures.
[8472] Provide assistance in the production of wiring assemblies.
[20157] Perform quality checks on products and parts.
[20158] Package finished products and prepare them for shipment.
[20159] Shovel, sweep, or otherwise clean work areas.
[20160] Review work orders and blueprints to ensure work is performed according to specifications.
[20161] Complete production reports to communicate team production level to management.
[20162] Maintain production equipment and machinery.
[20163] Supervise assemblers and train employees on job procedures.
[20164] Operate machinery and heavy equipment, such as forklifts.

TARGETS: code all 11 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/51-2092.00.json.
