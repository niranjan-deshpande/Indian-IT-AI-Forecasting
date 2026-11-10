You are a coder in a research pipeline. Follow the instructions below exactly.

Use only the information in this file. Do not read any other files and do not
search the web. Below are 3 occupations. Code each occupation's TARGETS
independently, in the order given; do not go back and adjust earlier answers to
make them consistent with later ones, and do not let one occupation's coding
shape another's.

For each occupation, write ONE JSON array to its own file:
  Graphic Designers (27-1024.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/27-1024.00.json
  Marketing Managers (11-2021.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/11-2021.00.json
  Loan Officers (13-2072.00) -> /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/13-2072.00.json
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

=== OCCUPATION: Graphic Designers (27-1024.00) ===
Design or create graphics to meet specific commercial or promotional needs, such as packaging, displays, or logos. May use a variety of mediums to achieve artistic or decorative effects.

TASK LIST (context; every statement below is also a TARGET):
[299] Create designs, concepts, and sample layouts, based on knowledge of layout principles and esthetic design concepts.
[300] Determine size and arrangement of illustrative material and copy, and select style and size of type.
[301] Use computer software to generate new images.
[302] Mark up, paste, and assemble final layouts to prepare layouts for printer.
[303] Draw and print charts, graphs, illustrations, and other artwork, using computer.
[304] Review final layouts and suggest improvements, as needed.
[305] Confer with clients to discuss and determine layout design.
[306] Develop graphics and layouts for product illustrations, company logos, and Web sites.
[307] Key information into computer equipment to create layouts for client or supervisor.
[308] Prepare illustrations or rough sketches of material, discussing them with clients or supervisors and making necessary changes.
[309] Study illustrations and photographs to plan presentation of materials, products, or services.
[310] Prepare notes and instructions for workers who assemble and prepare final layouts for printing.
[312] Photograph layouts, using camera, to make layout prints for supervisors or clients.
[313] Produce still and animated graphics for on-air and taped portions of television news broadcasts, using electronic video equipment.
[15228] Maintain archive of images, photos, or previous work products.
[15229] Research new software or design concepts.
[23970] Prepare digital files for printing.
[23971] Research the target audience of projects.
[23972] Write or edit copy for clients.

TARGETS: code all 19 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/27-1024.00.json.

=== OCCUPATION: Marketing Managers (11-2021.00) ===
Plan, direct, or coordinate marketing policies and programs, such as determining the demand for products and services offered by a firm and its competitors, and identify potential customers. Develop pricing strategies with the goal of maximizing the firm's profits or share of the market while ensuring the firm's customers are satisfied. Oversee product development or monitor trends that indicate the need for new products and services.

TASK LIST (context; every statement below is also a TARGET):
[950] Develop pricing strategies, balancing firm objectives and customer satisfaction.
[951] Identify, develop, or evaluate marketing strategy, based on knowledge of establishment objectives, market characteristics, and cost and markup factors.
[952] Evaluate the financial aspects of product development, such as budgets, expenditures, research and development appropriations, or return-on-investment and profit-loss projections.
[954] Direct the hiring, training, or performance evaluations of marketing or sales staff and oversee their daily activities.
[955] Negotiate contracts with vendors or distributors to manage product distribution, establishing distribution networks or developing distribution strategies.
[956] Consult with product development personnel on product specifications, such as design, color, or packaging.
[957] Compile lists describing product or service offerings.
[958] Use sales forecasting or strategic planning to ensure the sale and profitability of products, lines, or services, analyzing business developments and monitoring market trends.
[959] Select products or accessories to be displayed at trade or special production shows.
[960] Confer with legal staff to resolve problems, such as copyright infringement or royalty sharing with outside producers or distributors.
[961] Coordinate or participate in promotional activities or trade shows, working with developers, advertisers, or production managers, to market products or services.
[962] Advise business or other groups on local, national, or international factors affecting the buying or selling of products or services.
[963] Initiate market research studies, or analyze their findings.
[964] Consult with buying personnel to gain advice regarding the types of products or services expected to be in demand.
[965] Conduct economic or commercial surveys to identify potential markets for products or services.
[19502] Consult with buying personnel to gain advice regarding environmentally sound or sustainable products.
[19503] Develop business cases for environmental marketing strategies.
[19504] Integrate environmental information into product or company marketing strategies, policies, or activities.
[19505] Recommend modifications to products, packaging, production processes, or other characteristics to improve the environmental soundness or sustainability of products.
[20709] Formulate, direct, or coordinate marketing activities or policies to promote products or services, working with advertising or promotion managers.

TARGETS: code all 20 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/11-2021.00.json.

=== OCCUPATION: Loan Officers (13-2072.00) ===
Evaluate, authorize, or recommend approval of commercial, real estate, or credit loans. Advise borrowers on financial status and payment methods. Includes mortgage loan officers and agents, collection analysts, loan servicing officers, loan underwriters, and payday loan officers.

TASK LIST (context; every statement below is also a TARGET):
[3407] Approve loans within specified limits, and refer loan applications outside those limits to management for approval.
[3408] Meet with applicants to obtain information for loan applications and to answer questions about the process.
[3409] Analyze applicants' financial status, credit, and property evaluations to determine feasibility of granting loans.
[3410] Explain to customers the different types of loans and credit options that are available, as well as the terms of those services.
[3411] Obtain and compile copies of loan applicants' credit histories, corporate financial statements, and other financial information.
[3412] Review and update credit and loan files.
[3413] Review loan agreements to ensure that they are complete and accurate according to policy.
[3414] Compute payment schedules.
[3415] Stay abreast of new types of loans and other financial services and products to better meet customers' needs.
[3416] Submit applications to credit analysts for verification and recommendation.
[3417] Handle customer complaints and take appropriate action to resolve them.
[3418] Work with clients to identify their financial goals and to find ways of reaching those goals.
[3421] Market bank products to individuals and firms, promoting bank services that may meet customers' needs.
[3422] Supervise loan personnel.
[3423] Set credit policies, credit lines, procedures and standards in conjunction with senior managers.
[3425] Analyze potential loan markets and develop referral networks to locate prospects for loans.
[3426] Prepare reports to send to customers whose accounts are delinquent, and forward irreconcilable accounts for collector action.

TARGETS: code all 17 statements above, in that order, and write them to /Users/ndeshpande/Documents/2-misc/1-AI/SPAR---Andrei/delegable_share/coding/stage1/more_v1/13-2072.00.json.
