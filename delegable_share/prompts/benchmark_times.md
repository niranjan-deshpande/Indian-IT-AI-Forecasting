# Benchmark item times — estimation prompt v1 (2026-11-09)

Purpose: give benchmark items human times estimated the same way as the work items' lengths
(Stage 2), so the ratio of work-item length to benchmark horizon uses one estimator on both sides
and a systematic bias largely cancels. First used blind on items with published times
(`benchmarks/timing_validation/`) to measure the estimator's error.

Coders: two Sonnet subagents and GPT-6.1 Terra; median of the three. Coders see the item text and
a one-line description of the benchmark, never the published time, any AI result, or the model.

## Prompt

```
You are estimating how long people take to do individual tasks from
benchmarks (sets of tasks used to test software agents). For each item you
get a one-line description of the benchmark and the item's full text: what
the worker is given and asked to do.

Estimate the active working time, in minutes, for an experienced
professional in this kind of work, without AI, to finish the item to the
standard the benchmark checks. Assume they have already spent a few hours
getting familiar with the codebase, system, or tools involved; that
familiarisation is not counted. Count reading the task, investigating,
doing the work, and checking it. Don't count waiting.

Judge from the item text only. Don't consider how hard the item is for AI.

For each item, write one or two sentences of reasoning about what the work
involves, then give:
  - estimate_min: your best estimate (the time a typical such professional
    would take)
  - low_min, high_min: a range you are fairly confident contains it

Output, per item:
{"item_id": "...", "reasoning": "...", "estimate_min": 0, "low_min": 0, "high_min": 0}
```

## Benchmark descriptions shown to coders

- `swe_bench_verified`: a GitHub issue for an open-source Python library; the worker changes the
  code in the repository so the issue is fixed; hidden tests check the fix.
- `terminal_bench_2`: a Linux machine and a written instruction, done at the command line; hidden
  tests check the final state of the machine.
- `gdpval`: a realistic work request written by an experienced professional, with reference
  files attached; the deliverable is a document, spreadsheet, slide deck or similar file; done
  when an expert reviewer judges it at least as good as a professional's.
- `sweeper_bench`: an open-source web app's code and a running copy, plus a vague request such as
  "find and fix issues in <product area>" with no bug report; the worker finds the faulty
  behaviour by using the app and fixes the code; done when the bug is gone and nearby features
  still work.
- `swt_bench`: a bug report and the code repository before the fix; the worker writes automated
  tests that fail on the buggy code and would pass once it is fixed (the fix itself is not
  required).
- `swe_bench_pro`: a product codebase (Python, Go, JS/TS) with a written problem statement,
  requirements and interface specification; the worker implements the change, typically across
  several files; hidden tests check the new behaviour and that existing tests still pass.
- `tau_retail_airline`: a chat with a customer of an online store or an airline who wants
  something done (exchange, return, cancel or change an order or booking); the worker verifies
  the customer, applies the written policy, confirms details and makes the right system changes;
  done when the records are correct and required facts were told to the customer.
- `tau_telecom`: a chat with a mobile customer whose phone has a problem; the worker checks the
  account and talks the customer through steps on their phone following a troubleshooting
  manual; done when the phone works and the account is right.
- `tau_banking`: a chat with a bank customer about a card, dispute, refund, fee or rewards
  question; the worker finds the relevant rules among many internal policy documents, checks
  account data and makes the policy-correct change; done when the account state is right.
- `tau_voice`: a phone call from a customer of a store, airline or mobile carrier who wants
  something fixed or changed; the worker verifies the caller, follows the written policy and
  makes the right system changes; done when the records are right.
- `eva_bench`: a phone call to an airline, an HR service desk or an IT service desk; the worker
  verifies the caller, looks up and updates records and tells the caller the right information;
  done when the right records are changed and nothing false or disallowed was said.
- `crmarena_pro`: a request handled in a company's CRM system through search and query tools,
  e.g. route a case to the best agent, check a quote against policy, qualify a lead, answer from
  knowledge articles; done when the returned record or answer is correct.
- `sopbench`: a customer request in a service setting (bank, DMV, clinic, hotel, library, shop,
  university) with a written standard operating procedure and system tools; the worker makes the
  required checks in order and either performs the action or declines it with the reason.
- `workarena_l1`: one explicit instruction in a ServiceNow IT-service-management web interface
  (create a record, filter a list, order a catalog item, find a knowledge-base answer, read a
  chart); done when the record, list or answer matches the goal.
- `workarena_pp`: a multi-step service-desk job in ServiceNow, given as numbered steps or as a
  ticket that points to a company procedure; done when all resulting records are correct.
- `starshell`: one record-keeping instruction in a business system (ServiceNow, GitLab or an ERP
  system), sometimes several chained; done when the records match the goal.
- `osworld_verified`: one task on an Ubuntu desktop stated in a sentence or two (edit a
  spreadsheet, change an app setting, export a file, a multi-app workflow); done when the final
  file or application state matches the instruction.
- `finch`: a real-world finance or accounting spreadsheet workflow (often several linked
  workbooks, sometimes PDFs), with a written instruction of one to five sub-tasks; done when the
  returned workbook matches an expert's.
- `spreadsheetbench_2`: a business workflow on a large multi-sheet workbook (complete a financial
  model or schedule, audit and repair errors, or build a specified chart); done when the workbook
  matches an expert's.
- `terminal_bench_1`: a Linux machine and a written instruction for an everyday command-line
  job (git, builds, servers, small data tasks); hidden tests check the final state.
- `itbench_sre`: a snapshot of a failing Kubernetes application (alerts, events, logs, traces,
  metrics, service topology); the worker investigates with command-line tools and reports which
  components caused the incident; correct when every true root cause is named and no wrong one.

## v2: reference items (anchors)

v1 compressed estimates badly (slope of log estimate on log published ≈ 0.3). v2 adds a block of
reference items with known times between the instructions and the items (text in
`scripts/bench_times.py`, `ANCHOR_INTRO`). Pilot anchors: `benchmarks/timing_validation/anchors.jsonl`,
11 held-out items (8 Terminal-Bench 2 tasks at 5–960 min, 3 SWE-bench Verified issues, one per
bucket below 4 h). They come from the same two benchmarks as the test items, so the test shows
whether anchors fix compression, not whether they transfer to other kinds of work.

## Notes

- The "few hours of familiarisation, not counted" wording follows how SWE-bench Verified's
  annotators were asked to estimate; it also matches the low-context benchmark worker that the
  spec's context stretch m is defined against.
- Scoring: rank correlation with published times; median ratio estimate/published (the bias);
  share within 2×; for bucketed items, share of estimates inside the bucket and ordinal agreement.
