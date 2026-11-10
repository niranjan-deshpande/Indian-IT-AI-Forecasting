You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Below are 3 occupations. Code each occupation's TARGETS
independently, in the order given; do not go back and adjust earlier answers to
make them consistent with later ones, and do not let one occupation's coding
shape another's.

For each occupation, write ONE JSON array to its own file:
  Elementary School Teachers, Except Special Education (25-2021.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/25-2021.00.json
  Medical Assistants (31-9092.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/31-9092.00.json
  Construction Laborers (47-2061.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/47-2061.00.json
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

=== OCCUPATION: Elementary School Teachers, Except Special Education (25-2021.00) ===
Teach academic and social skills to students at the elementary school level.

TASK LIST (context; every statement below is also a TARGET):
[6535] Establish and enforce rules for behavior and procedures for maintaining order among the students.
[6536] Observe and evaluate students' performance, behavior, social development, and physical health.
[6537] Prepare materials and classrooms for class activities.
[6538] Adapt teaching methods and instructional materials to meet students' varying needs and interests.
[6539] Plan and conduct activities for a balanced program of instruction, demonstration, and work time that provides students with opportunities to observe, question, and investigate.
[6540] Instruct students individually and in groups, using teaching methods such as lectures, discussions, and demonstrations.
[6541] Establish clear objectives for all lessons, units, and projects and communicate those objectives to students.
[6542] Assign and grade class work and homework.
[6543] Read books to entire classes or small groups.
[6544] Prepare, administer, and grade tests and assignments to evaluate students' progress.
[6545] Confer with parents or guardians, teachers, counselors, and administrators to resolve students' behavioral and academic problems.
[6546] Meet with parents and guardians to discuss their children's progress and to determine priorities for their children and their resource needs.
[6547] Maintain accurate and complete student records as required by laws, district policies, and administrative regulations.
[6548] Prepare students for later grades by encouraging them to explore learning opportunities and to persevere with challenging tasks.
[6549] Guide and counsel students with adjustment or academic problems or with special academic interests.
[6550] Prepare and implement remedial programs for students requiring extra help.
[6551] Prepare objectives and outlines for courses of study, following curriculum guidelines or requirements of states and schools.
[6552] Provide a variety of materials and resources for children to explore, manipulate, and use, both in learning activities and in imaginative play.
[6553] Enforce administration policies and rules governing students.
[6554] Confer with other staff members to plan and schedule lessons promoting learning, following approved curricula.
[6555] Meet with other professionals to discuss individual students' needs and progress.
[6556] Use computers, audio-visual aids, and other equipment and materials to supplement presentations.
[6557] Prepare for assigned classes and show written evidence of preparation upon request of immediate supervisors.
[6558] Collaborate with other teachers and administrators in the development, evaluation, and revision of elementary school programs.
[6559] Prepare reports on students and activities as required by administration.
[6560] Instruct and monitor students in the use and care of equipment and materials to prevent injuries and damage.
[6561] Organize and lead activities designed to promote physical, mental, and social development, such as games, arts and crafts, music, and storytelling.
[6562] Attend professional meetings, educational conferences, and teacher training workshops to maintain and improve professional competence.
[6563] Plan and supervise class projects, field trips, visits by guest speakers or other experiential activities, and guide students in learning from those activities.
[6564] Organize and label materials and display students' work.
[6565] Attend staff meetings and serve on committees, as required.
[6566] Administer standardized ability and achievement tests, and interpret results to determine student strengths and needs.
[6567] Supervise, evaluate, and plan assignments for teacher assistants and volunteers.
[6568] Involve parent volunteers and older students in children's activities to facilitate involvement in focused, complex play.
[6569] Perform administrative duties, such as school library assistance, hall and cafeteria monitoring, and bus loading and unloading.
[6570] Select, store, order, issue, and inventory classroom equipment, materials, and supplies.
[6571] Provide students with disabilities with assistive devices, supportive technology, and assistance accessing facilities, such as restrooms.
[6572] Sponsor extracurricular activities, such as clubs, student organizations, and academic contests.

TARGETS: code all 38 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/25-2021.00.json.

=== OCCUPATION: Medical Assistants (31-9092.00) ===
Perform administrative and certain clinical duties under the direction of a physician. Administrative duties may include scheduling appointments, maintaining medical records, billing, and coding information for insurance purposes. Clinical duties may include taking and recording vital signs and medical histories, preparing patients for examination, drawing blood, and administering medications as directed by physician.

TASK LIST (context; every statement below is also a TARGET):
[2024] Interview patients to obtain medical information and measure their vital signs, weight, and height.
[2025] Show patients to examination rooms and prepare them for the physician.
[2026] Record patients' medical history, vital statistics, or information such as test results in medical records.
[2027] Prepare and administer medications as directed by a physician.
[2028] Collect blood, tissue, or other laboratory specimens, log the specimens, and prepare them for testing.
[2029] Explain treatment procedures, medications, diets, or physicians' instructions to patients.
[2030] Help physicians examine and treat patients, handing them instruments or materials or performing such tasks as giving injections or removing sutures.
[2031] Authorize drug refills and provide prescription information to pharmacies.
[2032] Prepare treatment rooms for patient examinations, keeping the rooms neat and clean.
[2033] Clean and sterilize instruments and dispose of contaminated supplies.
[2034] Schedule appointments for patients.
[2035] Change dressings on wounds.
[2036] Greet and log in patients arriving at office or clinic.
[2037] Contact medical facilities or departments to schedule patients for tests or admission.
[2038] Perform general office duties, such as answering telephones, taking dictation, or completing insurance forms.
[2039] Inventory and order medical, lab, or office supplies or equipment.
[2040] Perform routine laboratory tests and sample analyses.
[2041] Set up medical laboratory equipment.
[2042] Keep financial records or perform other bookkeeping duties, such as handling credit or collections or mailing monthly statements to patients.
[2043] Operate x-ray, electrocardiogram (EKG), or other equipment to administer routine diagnostic tests.

TARGETS: code all 20 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/31-9092.00.json.

=== OCCUPATION: Construction Laborers (47-2061.00) ===
Perform tasks involving physical labor at construction sites. May operate hand and power tools of all types: air hammers, earth tampers, cement mixers, small mechanical hoists, surveying and measuring equipment, and a variety of other equipment and instruments. May clean and prepare sites, dig trenches, set braces to support the sides of excavations, erect scaffolding, and clean up rubble, debris, and other waste materials. May assist other craft workers.

TASK LIST (context; every statement below is also a TARGET):
[11455] Clean or prepare construction sites to eliminate possible hazards.
[11456] Read plans, instructions, or specifications to determine work activities.
[11457] Control traffic passing near, in, or around work zones.
[11458] Signal equipment operators to facilitate alignment, movement, or adjustment of machinery, equipment, or materials.
[11459] Dig ditches or trenches, backfill excavations, or compact and level earth to grade specifications, using picks, shovels, pneumatic tampers, or rakes.
[11460] Position, join, align, or seal structural components, such as concrete wall sections or pipes.
[11461] Measure, mark, or record openings or distances to layout areas where construction work will be performed.
[11462] Load, unload, or identify building materials, machinery, or tools, distributing them to the appropriate locations, according to project plans or specifications.
[11463] Erect or dismantle scaffolding, shoring, braces, traffic barricades, ramps, or other temporary structures.
[11464] Position or dismantle forms for pouring concrete, using saws, hammers, nails, or bolts.
[11465] Lubricate, clean, or repair machinery, equipment, or tools.
[11466] Operate jackhammers or drills to break up concrete or pavement.
[11467] Smooth or finish freshly poured cement or concrete, using floats, trowels, screeds, or powered cement finishing tools.
[11468] Operate or maintain air monitoring or other sampling devices in confined or hazardous environments.
[11469] Install sewer, water, or storm drain pipes, using pipe-laying machinery or laser guidance equipment.
[11471] Provide assistance to craft workers, such as carpenters, plasterers, or masons.
[11472] Tend pumps, compressors, or generators to provide power for tools, machinery, or equipment or to heat or move materials, such as asphalt.
[11473] Mop, brush, or spread paints, cleaning solutions, or other compounds over surfaces to clean them or to provide protection.
[11474] Place, consolidate, or protect case-in-place concrete or masonry structures.
[11477] Mix, pour, or spread concrete, using portable cement mixers.
[11478] Grind, scrape, sand, or polish surfaces, such as concrete, marble, terrazzo, or wood flooring, using abrasive tools or machines.
[11479] Tend machines that pump concrete, grout, cement, sand, plaster, or stucco through spray guns for application to ceilings or walls.
[11480] Mix ingredients to create compounds for covering or cleaning surfaces.
[11481] Raze buildings or salvage useful materials.
[11482] Spray materials, such as water, sand, steam, vinyl, paint, or stucco, through hoses to clean, coat, or seal surfaces.
[11483] Apply caulking compounds by hand or caulking guns to protect against entry of water or air.
[19838] Perform site activities required of green certified construction practices, such as implementing waste management procedures, identifying materials for reuse, or installing erosion or sedimentation control mechanisms.

TARGETS: code all 27 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/47-2061.00.json.
