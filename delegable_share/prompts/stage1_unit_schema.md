# Stage 1 prompt: unit schema — v2 (2026-11-09)

Changes from the spec appendix are listed at the bottom. Worked-example statements are
checked against O*NET 31.0 (`data/bpo_tasks.csv`).

## Inputs (per call)

- `occupation_title`, `occupation_description`
- `task_list`: every task statement for the occupation, with IDs (context only)
- `target`: the ID and text of the one statement to code

## Prompt

```
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
```

## Worked examples (to paste into the prompt)

Drawn from BPO occupations outside the pilot, so the pilot stays a clean test.

### Example A — DISCRETE, granularity choice
Bookkeeping, Accounting, and Auditing Clerks — "Check figures, postings, and
documents for correct entry, mathematical accuracy, and proper codes."

```json
{
  "split_reasoning": "One activity: checking entered records; item sizes vary but the kind of work is the same.",
  "parts": [{
    "part_id": "a",
    "text": "Check a batch of postings and their source documents for correct entry, arithmetic, and codes.",
    "time_share": 1.0,
    "type_reasoning": "Each check produces a verified (or corrected) batch that someone relies on.",
    "type": "DISCRETE",
    "unit_reasoning": "Clerks check postings in batches tied to a period or an account, and sign off the batch, not each line.",
    "work_item": "one batch of postings checked (e.g. a day's entries for one ledger)",
    "start": "batch of entries and source documents received for review",
    "end": "batch marked verified, with errors corrected or flagged",
    "checked_by": "senior accountant or auditor",
    "duplicates": [],
    "overlaps_with": []
  }],
  "notes": ""
}
```

### Example B — ONGOING recast into items
Network and Computer Systems Administrators (15-1244.00, task 1325) — "Monitor
network performance to determine whether adjustments are needed and where
changes will be needed in the future."

```json
{
  "split_reasoning": "Monitoring is continuous, but it produces two different kinds of item: reacting to problems now and planning for later.",
  "parts": [
    {
      "part_id": "a",
      "text": "Investigate a performance alert and decide whether an adjustment is needed.",
      "time_share": 0.65,
      "type_reasoning": "Each alert ends in a decision and usually a ticket note others rely on.",
      "type": "DISCRETE",
      "unit_reasoning": "Alerts are the unit that enters the queue and gets closed.",
      "work_item": "one performance alert investigated",
      "start": "alert raised by monitoring tool",
      "end": "cause recorded and either adjustment requested or alert closed as no action",
      "checked_by": "on-call lead / change board",
      "duplicates": [],
      "overlaps_with": []
    },
    {
      "part_id": "b",
      "text": "Write a periodic capacity and performance review recommending future changes.",
      "time_share": 0.35,
      "type_reasoning": "Produces a report that managers read and act on.",
      "type": "DISCRETE",
      "unit_reasoning": "The report is what is handed over and signed off.",
      "work_item": "one capacity review report (monthly or quarterly)",
      "start": "pull of the period's performance data",
      "end": "report with recommendations sent to IT manager",
      "checked_by": "IT manager",
      "duplicates": [],
      "overlaps_with": []
    }
  ],
  "notes": "Time shares are a judgment; alert volume varies a lot by site."
}
```

### Example C — COMPOUND with an interpersonal part
Database Administrators — "Train users and answer questions."

```json
{
  "split_reasoning": "Two different activities joined by 'and': teaching users, and answering their individual questions.",
  "parts": [
    {
      "part_id": "a",
      "text": "Train users on the database or reporting tools.",
      "time_share": 0.4,
      "type_reasoning": "The value is in the live session; nothing a colleague would check is produced.",
      "type": "INTERPERSONAL",
      "duplicates": [],
      "overlaps_with": []
    },
    {
      "part_id": "b",
      "text": "Answer a user's question about the database, usually by email or ticket.",
      "time_share": 0.6,
      "type_reasoning": "Each question produces a written answer the user relies on.",
      "type": "DISCRETE",
      "unit_reasoning": "Questions arrive one at a time through email or the ticket queue.",
      "work_item": "one user question answered",
      "start": "question received",
      "end": "answer sent and question closed",
      "checked_by": "the user who asked",
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

## Changes from the spec appendix, and why

1. **Full task list as context.** Lets the coder avoid inventing items another
   statement already covers, and flag overlaps (step 5). Overlaps would
   otherwise double-count importance weight.
2. **Split and classify are separate steps.** "Compound" is about structure; the
   other types are about content. A compound statement's parts still need a type.
   The old step 5 (heterogeneous items) is folded into step 1.
3. **New type LIVE_SERVICE** (decision needed — see below).
4. **New type NO_DELIVERABLE** for keeping-current statements, which are neither
   ongoing-with-items nor interpersonal. D = 0, like interpersonal.
5. **`checked_by` field.** Makes "someone else would check or rely on it" concrete,
   and gives the Stage 2 coder something to anchor fixed review minutes on.
6. **Granularity rule of thumb** ("the level at which work is handed over: queue,
   ticket, sign-off, send").
7. **Flat parts list.** Ongoing activities become several DISCRETE parts with time
   shares, so every downstream row is one work item with one weight.
8. **Reasoning fields before values** in the JSON, so the reasoning is written
   first.
9. **Don't split on "or" lists of methods** (added after reading the pilot: 15-1232
   "Read technical manuals, confer with users, or conduct computer diagnostics…").
10. **Workflow-step rule** (added after reading the pilot: 43-4051 has separate
    statements for talking to the customer, keeping records, checking changes were
    made, and referring grievances). Without it every statement collapses into
    "one call" and the overlap double-counts.
11. **v2: where-is-it-done rule.** v1 coded steps done during a live call (taking payment,
    entering an order, issuing a refund) as DISCRETE, giving Customer Service Reps only 9%
    LIVE_SERVICE. Those steps happen while the customer waits, so under the LIVE_SERVICE
    rule a failure reaches the customer. v2 types each step by where it is done and splits
    when it is done both ways (Example D, from Receptionists).
12. **v2: duplicates vs partial overlaps.** Separate fields, so exact duplicates can be
    collapsed (see `../DECISIONS.md`) while partial overlaps are only recorded.
13. **v2: the "or"-list example no longer quotes a pilot statement** (v1 quoted 15-1232
    task 1288 verbatim, which steered that item).

## Open decisions

- ~~LIVE_SERVICE treatment~~ **Decided 2026-11-09:** sampled QA + failure cost (see
  `../DECISIONS.md`). Stage 1 keeps LIVE_SERVICE as a separate type, so Stage 2 and the
  model can apply the different delegation rule to those items.
- **Examples from inside or outside the pilot?** v1 uses non-pilot occupations so pilot
  results aren't steered by the examples.
- **Three unrated Software QA statements** (added in the 2020 taxonomy change; one is
  about dust and humidity control, clearly inherited from an older occupation). They have
  no importance weight, so they can't enter the weighted average. Proposal: drop them
  from the pilot (59 → 56 statements).
- **Model and runs.** Spec says one run. A cheap check: run a second model on the pilot
  only and compare units, as a measure of how fragile they are.
