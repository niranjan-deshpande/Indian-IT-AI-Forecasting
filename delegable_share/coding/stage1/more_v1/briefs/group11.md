You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Below are 3 occupations. Code each occupation's TARGETS
independently, in the order given; do not go back and adjust earlier answers to
make them consistent with later ones, and do not let one occupation's coding
shape another's.

For each occupation, write ONE JSON array to its own file:
  Licensed Practical and Licensed Vocational Nurses (29-2061.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/29-2061.00.json
  Pharmacists (29-1051.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/29-1051.00.json
  Home Health Aides (31-1121.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/31-1121.00.json
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

=== OCCUPATION: Licensed Practical and Licensed Vocational Nurses (29-2061.00) ===
Care for ill, injured, or convalescing patients or persons with disabilities in hospitals, nursing homes, clinics, private homes, group homes, and similar institutions. May work under the supervision of a registered nurse. Licensing required.

TASK LIST (context; every statement below is also a TARGET):
[507] Observe patients, charting and reporting changes in patients' conditions, such as adverse reactions to medication or treatment, and taking any necessary action.
[508] Administer prescribed medications or start intravenous fluids, noting times and amounts on patients' charts.
[509] Answer patients' calls and determine how to assist them.
[510] Measure and record patients' vital signs, such as height, weight, temperature, blood pressure, pulse, or respiration.
[511] Provide basic patient care or treatments, such as taking temperatures or blood pressures, dressing wounds, treating bedsores, giving enemas or douches, rubbing with alcohol, massaging, or performing catheterizations.
[512] Help patients with bathing, dressing, maintaining personal hygiene, moving in bed, or standing and walking.
[513] Supervise nurses' aides or assistants.
[514] Work as part of a healthcare team to assess patient needs, plan and modify care, and implement interventions.
[515] Record food and fluid intake and output.
[516] Evaluate nursing intervention outcomes, conferring with other healthcare team members as necessary.
[517] Assemble and use equipment, such as catheters, tracheotomy tubes, or oxygen suppliers.
[518] Collect samples, such as blood, urine, or sputum from patients, and perform routine laboratory tests on samples.
[519] Prepare patients for examinations, tests, or treatments and explain procedures.
[520] Prepare or examine food trays for conformance to prescribed diet.
[521] Apply compresses, ice bags, or hot water bottles.
[522] Clean rooms and make beds.
[523] Inventory and requisition supplies and instruments.
[524] Provide medical treatment or personal care to patients in private home settings, such as cooking, keeping rooms orderly, seeing that patients are comfortable and in good spirits, or instructing family members in simple nursing tasks.
[525] Sterilize equipment and supplies, using germicides, sterilizer, or autoclave.
[527] Wash and dress bodies of deceased persons.
[528] Make appointments, keep records, or perform other clerical duties in doctors' offices or clinics.
[529] Set up equipment and prepare medical treatment rooms.

TARGETS: code all 22 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/29-2061.00.json.

=== OCCUPATION: Pharmacists (29-1051.00) ===
Dispense drugs prescribed by physicians and other health practitioners and provide information to patients about medications and their use. May advise physicians and other health practitioners on the selection, dosage, interactions, and side effects of medications.

TASK LIST (context; every statement below is also a TARGET):
[1808] Review prescriptions to assure accuracy, to ascertain the needed ingredients, and to evaluate their suitability.
[1809] Provide information and advice regarding drug interactions, side effects, dosage, and proper medication storage.
[1810] Analyze prescribing trends to monitor patient compliance and to prevent excessive usage or harmful interactions.
[1811] Order and purchase pharmaceutical supplies, medical supplies, or drugs, maintaining stock and storing and handling it properly.
[1812] Maintain records, such as pharmacy files, patient profiles, charge system files, inventories, control records for radioactive nuclei, or registries of poisons, narcotics, or controlled drugs.
[1813] Provide specialized services to help patients manage conditions, such as diabetes, asthma, smoking cessation, or high blood pressure.
[1814] Advise customers on the selection of medication brands, medical equipment, or healthcare supplies.
[1815] Collaborate with other health care professionals to plan, monitor, review, or evaluate the quality or effectiveness of drugs or drug regimens, providing advice on drug applications or characteristics.
[1816] Compound and dispense medications as prescribed by doctors and dentists, by calculating, weighing, measuring, and mixing ingredients, or oversee these activities.
[1818] Refer patients to other health professionals or agencies when appropriate.
[1819] Prepare sterile solutions or infusions for use in surgical procedures, emergency rooms, or patients' homes.
[1820] Plan, implement, or maintain procedures for mixing, packaging, or labeling pharmaceuticals, according to policy and legal requirements, to ensure quality, security, and proper disposal.
[1821] Assay radiopharmaceuticals, verify rates of disintegration, and calculate the volume required to produce the desired results, to ensure proper dosages.
[1822] Manage pharmacy operations, hiring or supervising staff, performing administrative duties, or buying or selling non-pharmaceutical merchandise.
[1823] Work in hospitals or clinics or for Health Management Organizations (HMOs), dispensing prescriptions, serving as a medical team consultant, or specializing in specific drug therapy areas, such as oncology or nuclear pharmacotherapy.
[1824] Assess the identity, strength, or purity of medications.
[1825] Teach pharmacy students serving as interns in preparation for their graduation or licensure.
[1826] Publish educational information for other pharmacists, doctors, or patients.
[20404] Offer health promotion or prevention activities, such as training people to use blood pressure devices or diabetes monitors.
[20405] Contact insurance companies to resolve billing issues.
[20406] Update or troubleshoot pharmacy information databases.

TARGETS: code all 21 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/29-1051.00.json.

=== OCCUPATION: Home Health Aides (31-1121.00) ===
Monitor the health status of an individual with disabilities or illness, and address their health-related needs, such as changing bandages, dressing wounds, or administering medication. Work is performed under the direction of offsite or intermittent onsite licensed nursing staff. Provide assistance with routine healthcare tasks or activities of daily living, such as feeding, bathing, toileting, or ambulation. May also help with tasks such as preparing meals, doing light housekeeping, and doing laundry depending on the patient's abilities.

TASK LIST (context; every statement below is also a TARGET):
[4240] Maintain records of patient care, condition, progress, or problems to report and discuss observations with supervisor or case manager.
[4241] Provide patients with help moving in and out of beds, baths, wheelchairs, or automobiles and with dressing and grooming.
[4242] Provide patients and families with emotional support and instruction in areas such as caring for infants, preparing healthy meals, living independently, or adapting to disability or illness.
[4244] Entertain, converse with, or read aloud to patients to keep them mentally healthy and alert.
[4245] Plan, purchase, prepare, or serve meals to patients or other family members, according to prescribed diets.
[4246] Direct patients in simple prescribed exercises or in the use of braces or artificial limbs.
[4247] Check patients' pulse, temperature, and respiration.
[4248] Change dressings.
[4249] Perform a variety of duties as requested by client, such as obtaining household supplies or running errands.
[4250] Accompany clients to doctors' offices or on other trips outside the home, providing transportation, assistance, and companionship.
[4252] Care for children with disabilities or who have sick parents or parents with disabilities.
[4253] Massage patients or apply preparations or treatments, such as liniment, alcohol rubs, or heat-lamp stimulation.
[18694] Care for patients by changing bed linens, washing and ironing laundry, cleaning, or assisting with their personal care.
[18695] Administer prescribed oral medications, under the written direction of physician or as directed by home care nurse or aide, and ensure patients take their medicine.
[20577] Bathe patients.

TARGETS: code all 15 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/31-1121.00.json.
