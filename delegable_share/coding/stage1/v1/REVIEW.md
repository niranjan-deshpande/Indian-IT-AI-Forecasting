# Stage 1 unit schema — pilot, for hand-check

Coded 2026-11-09 by three Opus subagents (one per occupation), prompt v1. 56 statements → 71 parts; validator: 0 problems.
Full reasoning per part is in `units.csv`. Weight = O*NET importance × time share.

## Computer User Support Specialists

| Task | Statement | Part | Type | Share | Work item (start → end; checked by) | Overlaps |
|---|---|---|---|---|---|---|
| 1282 | Answer user inquiries regarding computer software or hardware operation to resolve problems. | a | LIVE_SERVICE | 0.60 | one user call or walk-up inquiry resolved (user's call, chat, or walk-up request → user confirms the problem is resolved (or it is escalated), ticket logged; the user; help desk lead via ticket review) | 1288 |
| 1282 | ″ | b | DISCRETE | 0.40 | one emailed or ticketed user inquiry answered (ticket or email received → answer sent, user confirms or ticket auto-closes; the user who asked) | 1288 |
| 1283 | Enter commands and observe system functioning to verify correct operations and detect errors. | a | DISCRETE | 1.00 | one system or workstation verification check (install/repair completed or scheduled check due → system confirmed working, or error recorded and ticket opened; user of the system; supervisor or ticket reviewer) | 1285 |
| 1284 | Install and perform minor repairs to hardware, software, or peripheral equipment, following design or installation specifications. | a | PHYSICAL | 0.55 | *Install or perform minor repairs on computer hardware or peripheral equipment following specifications.* |  |
| 1284 | ″ | b | DISCRETE | 0.45 | one software install or repair request completed (install or repair request ticket assigned → software installed/fixed and tested, ticket closed; the requesting user) |  |
| 1285 | Oversee the daily performance of computer systems. | a | DISCRETE | 0.50 | one daily system status check (start of the day's monitoring review → status logged, any issues opened as tickets; IT supervisor) | 1283 |
| 1285 | ″ | b | DISCRETE | 0.50 | one performance issue or alert investigated (alert raised or slowdown reported → cause recorded and fix applied, escalated, or closed as no action; IT supervisor or systems administrator) | 1288 |
| 1286 | Set up equipment for employee use, performing or ensuring proper installation of cables, operating systems, or appropriate software. | a | PHYSICAL | 0.40 | *Physically set up equipment at an employee's workstation and install or check cables.* |  |
| 1286 | ″ | b | DISCRETE | 0.60 | one employee machine imaged and configured (setup request for a new employee or replacement machine → machine configured with OS, software, and accounts; handed to employee and ticket closed; the employee; IT supervisor) | 1284 |
| 1287 | Maintain records of daily data communication transactions, problems and remedial actions taken, or installation activities. | a | DISCRETE | 0.60 | one incident record (problem and remedy) written (problem handled → record entered in the ticket or log system; help desk lead; colleagues handling later incidents) |  |
| 1287 | ″ | b | DISCRETE | 0.25 | one installation record entered (installation completed → asset/installation log updated; IT asset manager or auditor) |  |
| 1287 | ″ | c | DISCRETE | 0.15 | one daily data communication transaction log (end of day's transactions → log completed and filed; IT supervisor or network administrator) |  |
| 1288 | Read technical manuals, confer with users, or conduct computer diagnostics to investigate and resolve problems or to provide technical assistance and support. | a | DISCRETE | 1.00 | one technical problem ticket investigated and resolved (problem reported or ticket assigned → fix applied and confirmed, resolution recorded, ticket closed; the user; help desk lead) | 1282 |
| 1289 | Confer with staff, users, and management to establish requirements for new systems or modifications. | a | INTERPERSONAL | 1.00 | *Confer with staff, users, and management to establish requirements for new systems or modifications.* |  |
| 1290 | Develop training materials and procedures, or train users in the proper use of hardware or software. | a | DISCRETE | 0.40 | one training guide or procedure document (need identified (new system, recurring question) → document reviewed and published to users or the knowledge base; IT supervisor; users who follow it) |  |
| 1290 | ″ | b | INTERPERSONAL | 0.60 | *Train users in the proper use of hardware or software.* |  |
| 1291 | Refer major hardware or software problems or defective products to vendors or technicians for service. | a | DISCRETE | 1.00 | one problem escalated to a vendor or technician (decision that the problem exceeds in-house repair → vendor case or RMA opened with details, service arranged, user informed; vendor or technician; IT supervisor) |  |
| 1292 | Prepare evaluations of software or hardware, and recommend improvements or upgrades. | a | DISCRETE | 1.00 | one product evaluation with recommendation (request or need to assess a product or upgrade → evaluation and recommendation sent to manager; IT manager) |  |
| 1293 | Read trade magazines and technical manuals, or attend conferences and seminars to maintain knowledge of hardware and software. | a | NO_DELIVERABLE | 1.00 | *Read trade magazines and manuals or attend conferences to maintain knowledge of hardware and software.* |  |
| 1295 | Inspect equipment and read order sheets to prepare for delivery to users. | a | PHYSICAL | 1.00 | *Inspect equipment against order sheets and prepare it for delivery to users.* |  |
| 1296 | Modify and customize commercial programs for internal needs. | a | DISCRETE | 1.00 | one customization of a commercial program delivered (customization request from a user group → change tested and released to users; requesting users; IT supervisor) |  |
| 1297 | Conduct office automation feasibility studies, including workflow analysis, space design, or cost comparison analysis. | a | DISCRETE | 1.00 | one office automation feasibility study report (management request to assess an automation option → report with analysis and recommendation delivered to management; management) | 1292 |
| 15204 | Hire, supervise, and direct workers engaged in special project work, problem-solving, monitoring, and installation of data communication equipment and software. | a | INTERPERSONAL | 0.20 | *Hire workers for special project, problem-solving, monitoring, and installation work.* |  |
| 15204 | ″ | b | INTERPERSONAL | 0.80 | *Supervise and direct workers engaged in special project, problem-solving, monitoring, and installation work.* |  |

Coder notes:

- **1282**: Channel split shares are a judgment; 1288 covers the troubleshooting behind the same tickets, so the two statements substantially overlap.
- **1283**: Could be read as a step within installation/repair (1284) or daily oversight (1285) rather than a standalone item.
- **1284**: Shares between hardware and software depend heavily on the site; software installs also overlap with new-employee setup in 1286.
- **1285**: For a user support specialist 'oversee' is loosely defined; shares are a judgment.
- **1286**: 'Ensuring proper installation' may mean supervising others' setup, which would be interpersonal; coded as doing it oneself.
- **1287**: Part a is often written as the closing step of tickets counted under 1282/1288; the daily transaction log may be rare in modern settings.
- **1288**: Heavily overlaps with 1282; the line between answering an inquiry and investigating a problem is blurry.
- **1289**: Meetings may produce a written requirements note, which would be a checkable deliverable.
- **1291**: Includes a phone call with the vendor in some cases, but the deliverable is the case record.
- **1295**: Reading the order sheet is a small desk component not split out.
- **1297**: Larger in scope than a single deliverable may suggest; site visits for space design may involve some physical work.
- **15204**: Hiring may produce a hiring recommendation document, but the core work is interviewing.

## Customer Service Representatives

| Task | Statement | Part | Type | Share | Work item (start → end; checked by) | Overlaps |
|---|---|---|---|---|---|---|
| 2578 | Keep records of customer interactions or transactions, recording details of inquiries, complaints, or comments, as well as actions taken. | a | DISCRETE | 1.00 | one interaction record written after a customer contact (customer contact or transaction ends (or wrap-up time begins) → note with reason for contact, details, and actions taken saved to the customer's account; other reps who handle the account later; quality-assurance reviewer or supervisor) |  |
| 2579 | Resolve customers' service or billing complaints by performing activities such as exchanging merchandise, refunding money, or adjusting bills. | a | DISCRETE | 1.00 | one complaint resolved with an exchange, refund, or bill adjustment processed (complaint accepted as valid and remedy chosen → exchange, refund, or adjustment entered in the system and case marked resolved; customer; billing or finance team; supervisor who approves adjustments above limits) |  |
| 2580 | Check to ensure that appropriate changes were made to resolve customers' problems. | a | DISCRETE | 1.00 | one resolved case verified (follow-up check on a customer's fix) (follow-up reminder or case due for verification → change confirmed in the account/order system and case closed, or discrepancy flagged and case reopened; customer; supervisor or quality reviewer) |  |
| 2581 | Contact customers to respond to inquiries or to notify them of claim investigation results or any planned adjustments. | a | DISCRETE | 1.00 | one outbound customer response or notification sent/completed (case reaches a decision or pending inquiry is ready for reply → customer reached (or written notice sent) with the answer, outcome, or planned adjustment, and contact logged; customer; supervisor or quality reviewer) |  |
| 2582 | Refer unresolved customer grievances to designated departments for further investigation. | a | DISCRETE | 1.00 | one escalation/referral of an unresolved grievance (rep determines the grievance cannot be resolved at their level → escalation ticket with case summary routed to the designated department and customer informed; receiving department (e.g. claims, billing, investigations); supervisor) |  |
| 2583 | Determine charges for services requested, collect deposits or payments, or arrange for billing. | a | DISCRETE | 1.00 | one service request priced and payment collected or billing arranged (customer requests a service → charges calculated and quoted, and payment/deposit posted or billing set up on the account; customer; billing/finance team; cash reconciliation or audit) |  |
| 2584 | Complete contract forms, prepare change of address records, or issue service discontinuance orders, using computers. | a | DISCRETE | 1.00 | one account form or service order completed (contract, address change, or discontinuance) (customer request with needed details received → form or order completed and submitted in the system; downstream fulfilment/service teams; billing; customer) |  |
| 2585 | Obtain and examine all relevant information to assess validity of complaints and to determine possible causes, such as extreme weather conditions that could increase utility bills. | a | DISCRETE | 1.00 | one complaint investigated with validity and probable cause recorded (complaint details received → determination (valid/not valid, probable cause) recorded on the case; supervisor; billing or claims department; customer via the eventual decision) |  |
| 2586 | Solicit sales of new or additional services or products. | a | INTERPERSONAL | 1.00 | *Solicit sales of new or additional services or products from customers.* |  |
| 2587 | Review insurance policy terms to determine whether a particular loss is covered by insurance. | a | DISCRETE | 1.00 | one coverage determination for a reported loss (customer reports a loss or asks whether it is covered → coverage decision (covered / not covered / refer) recorded and communicated; claims adjuster or supervisor; customer) |  |
| 2589 | Compare disputed merchandise with original requisitions and information from invoices and prepare invoices for returned goods. | a | PHYSICAL | 0.40 | *Inspect disputed or returned merchandise and compare it with the original requisition and invoice details.* |  |
| 2589 | ″ | b | DISCRETE | 0.60 | one return invoice prepared for a disputed shipment (comparison of returned goods against requisition and invoice completed → return/credit invoice issued and posted to the account; billing/accounts receivable; customer) |  |
| 2591 | Recommend improvements in products, packaging, shipping, service, or billing methods and procedures to prevent future problems. | a | DISCRETE | 1.00 | one improvement recommendation submitted (rep notices a recurring problem pattern → written suggestion or feedback submitted to supervisor or the responsible department; supervisor or management of the responsible department) |  |
| 18565 | Confer with customers by telephone or in person to provide information about products or services, take or enter orders, cancel accounts, or obtain details of complaints. | a | LIVE_SERVICE | 1.00 | one customer call or walk-up contact handled (customer's call is answered or customer approaches the counter → information given, order entered, account cancelled, or complaint details captured, and contact ends; customer; quality-assurance call monitoring or supervisor) |  |

Coder notes:

- **2579**: Boundary with 2585 (assessing complaint validity) and 18565 (taking complaint details) is a judgment; this part covers only the remedy step.
- **2581**: Could be split into 'answer pending inquiries' vs 'notify claim outcomes'; also could be LIVE_SERVICE when done by phone. The inquiry-answering portion is close to 18565.
- **2583**: Usually done during a live call (18565); in-person payment collection may involve some cash handling.
- **2584**: Partly overlaps 18565, which mentions taking orders and cancelling accounts during the conversation; this statement covers the back-end paperwork.
- **2586**: Could alternatively be LIVE_SERVICE with 'one sales offer made / order taken' as the item; the order entry itself overlaps 18565.
- **2589**: Whether the comparison is hands-on depends on the setting; if done from documents only, part a would be DISCRETE and merge with b.
- **2591**: Some recommendations may be given verbally in team meetings, which would be INTERPERSONAL.
- **18565**: Record-keeping after the contact is 2578; back-end form completion is 2584.

## Software Quality Assurance Analysts and Testers

| Task | Statement | Part | Type | Share | Work item (start → end; checked by) | Overlaps |
|---|---|---|---|---|---|---|
| 14638 | Design test plans, scenarios, scripts, or procedures. | a | DISCRETE | 1.00 | one test plan or test-case set for a feature or release (requirements or user stories for the feature/release received → test plan and cases written, reviewed and baselined in the test management tool; QA lead / test manager, and developers or product owner who review coverage) | 14640;14648 |
| 14639 | Test system modifications to prepare for implementation. | a | DISCRETE | 1.00 | one system modification (change request or build) tested and signed off (modification deployed to the test environment and assigned for testing → test cases executed, results recorded and pass/fail sign-off given for implementation; release manager / change board and development lead) |  |
| 14640 | Develop testing programs that address areas such as database impacts, software scenarios, regression testing, negative testing, error or bug retests, or usability. | a | DISCRETE | 1.00 | one test suite for one testing area of an application (decision to cover a testing area (e.g. need for a regression suite) and review of the application scope → suite of test cases written, reviewed and added to the test repository; QA lead / test manager) | 14638 |
| 14641 | Document software defects, using a bug tracking system, and report defects to software developers. | a | DISCRETE | 1.00 | one bug report filed (defect observed during testing → ticket filed with steps to reproduce, severity and evidence, and assigned to developers; developer who picks up the bug and QA lead during triage) | 14642 |
| 14642 | Identify, analyze, and document problems with program function, output, online screen, or content. | a | DISCRETE | 1.00 | one program problem analyzed and documented (unexpected behavior, output or content noticed → problem isolated, reproduced and written up with analysis; developer who fixes it and QA lead) | 14641 |
| 14643 | Monitor bug resolution efforts and track successes. | a | DISCRETE | 0.60 | one defect followed through to verified closure or reopening (defect marked fixed or overdue in the tracker → fix retested and ticket closed, or reopened with notes; development lead and QA lead) | 14640 |
| 14643 | ″ | b | DISCRETE | 0.40 | one defect-status / resolution report (weekly, per sprint or per release) (pull of defect data from the tracker for the period → report with open/closed counts, trends and blockers sent to stakeholders; project manager / QA manager) | 14664 |
| 14644 | Create or maintain databases of known test defects. | a | DISCRETE | 0.20 | one known-defect database or tracker project set up (need for a defect repository for a product or project identified → database configured with fields, workflow and access, and released to the team; QA lead and team members who use it) |  |
| 14644 | ″ | b | DISCRETE | 0.80 | one maintenance pass over a batch of known-defect records (scheduled review or triage of the defect list → records updated, duplicates merged and known-issues list current; QA lead, developers and support staff who rely on the known-issues list) | 14641 |
| 14645 | Plan test schedules or strategies in accordance with project scope or delivery dates. | a | DISCRETE | 1.00 | one test strategy and schedule for a project or release (project scope and delivery dates received → test strategy and schedule approved by project and QA management; project manager and QA manager) | 14638 |
| 14646 | Participate in product design reviews to provide input on functional requirements, product designs, schedules, or potential problems. | a | INTERPERSONAL | 1.00 | *Take part in product design reviews, giving input on requirements, designs, schedules and potential problems.* | 14653 |
| 14647 | Review software documentation to ensure technical accuracy, compliance, or completeness, or to mitigate risks. | a | DISCRETE | 1.00 | one software document reviewed with comments returned (document (spec, user guide, release notes) submitted for review → review comments or approval returned to the author; document author and document owner / QA lead) |  |
| 14648 | Document test procedures to ensure replicability and compliance with standards. | a | DISCRETE | 1.00 | one test procedure document written or updated (test procedure designed or changed → procedure document reviewed and stored in the test repository; QA lead and compliance / audit reviewers) | 14638 |
| 14649 | Develop or specify standards, methods, or procedures to determine product quality or release readiness. | a | DISCRETE | 1.00 | one quality standard or release-readiness criteria document (need for a new or revised quality standard identified → standard approved and published to teams; QA manager and engineering / release management) |  |
| 14650 | Update automated test scripts to ensure currency. | a | DISCRETE | 1.00 | one set of automated test scripts updated (one pull request) (application change or failing/outdated scripts identified → updated scripts pass review and run green in the test pipeline; peer reviewer / automation lead) |  |
| 14651 | Investigate customer problems referred by technical support. | a | DISCRETE | 1.00 | one escalated customer problem investigated (escalation ticket received from technical support → problem reproduced or ruled out, findings returned to support and bug filed if needed; technical support staff and development team) | 14657;14661 |
| 14652 | Install, maintain, or use software testing programs. | a | DISCRETE | 0.30 | one testing tool installed, upgraded or reconfigured (request or need to install or update a testing tool → tool working in the test environment and available to the team; QA team members who use the tool) | 14656 |
| 14652 | ″ | b | DISCRETE | 0.70 | one test run executed with results recorded (build ready and test run scheduled → tests executed and results logged in the test management tool; QA lead and development team) | 14639 |
| 14653 | Provide feedback and recommendations to developers on software usability and functionality. | a | DISCRETE | 1.00 | one set of usability/functionality recommendations for a feature or build (feature or build available for evaluation → recommendations sent to developers or logged as improvement tickets; developers and product owner) | 14646 |
| 14654 | Monitor program performance to ensure efficient and problem-free operations. | a | DISCRETE | 0.60 | one performance anomaly investigated (alert, slow response or degraded metric observed → cause recorded and bug filed or anomaly closed as no action; development lead / operations team) | 14661 |
| 14654 | ″ | b | DISCRETE | 0.40 | one performance report (per period or release) (pull of performance metrics for the period or build → report with trends and issues sent to stakeholders; QA manager and development lead) |  |
| 14655 | Conduct software compatibility tests with programs, hardware, operating systems, or network environments. | a | DISCRETE | 1.00 | one compatibility test cycle for a build across a configuration matrix (build and list of target configurations received → results matrix recorded and incompatibilities filed as bugs; QA lead and release manager) | 14639 |
| 14656 | Install and configure recreations of software production environments to allow testing of software performance. | a | DISCRETE | 1.00 | one production-like test environment built and configured (request for a test environment matching production → environment configured, verified against production settings and handed to testers; testers using it and QA / operations lead) | 14652 |
| 14657 | Collaborate with field staff or customers to evaluate or diagnose problems and recommend possible solutions. | a | LIVE_SERVICE | 1.00 | one field/customer problem case diagnosed with a recommended solution (field staff or customer raises a problem needing QA input → diagnosis and recommended solution given and recorded on the case; field staff or customer, and technical support) | 14651 |
| 14658 | Identify program deviance from standards, and suggest modifications to ensure compliance. | a | DISCRETE | 1.00 | one program or module reviewed for standards compliance with suggested modifications (program or module submitted for standards review → deviations and suggested modifications sent to developers; developers and QA lead) |  |
| 14659 | Design or develop automated testing tools. | a | DISCRETE | 1.00 | one automated testing tool or framework feature delivered (need for a test tool or framework feature defined → tool or feature reviewed, merged and available to testers; automation lead / peer reviewers and testers using it) |  |
| 14660 | Coordinate user or third-party testing. | a | DISCRETE | 0.60 | one user/third-party test round organized, with consolidated results (decision to run user or third-party testing for a release → results consolidated and summary or sign-off sent to project management; project manager / business owner) |  |
| 14660 | ″ | b | INTERPERSONAL | 0.40 | *Liaise with users or third-party testers during testing, answering questions and keeping them on track.* |  |
| 14661 | Perform initial debugging procedures by reviewing configuration files, logs, or code pieces to determine breakdown source. | a | DISCRETE | 1.00 | one failure triaged to a likely source (failure observed or ticket assigned → likely source identified and recorded on the ticket for developers; developer who fixes the defect) | 14642 |
| 14662 | Visit beta testing sites to evaluate software performance. | a | PHYSICAL | 0.70 | *Travel to a beta testing site and observe and evaluate the software's performance on site.* |  |
| 14662 | ″ | b | DISCRETE | 0.30 | one beta site visit report (return from the site visit with notes and data → report with findings and issues sent to development and product management; development lead and product manager) | 14657 |
| 14663 | Evaluate or recommend software for testing or bug tracking. | a | DISCRETE | 1.00 | one tool evaluation with recommendation (need for a new or replacement testing/bug-tracking tool raised → evaluation and recommendation sent to QA or IT management; QA manager / IT management) |  |
| 14664 | Conduct historical analyses of test results. | a | DISCRETE | 1.00 | one historical test-results analysis report (pull of past test results for the releases or period in scope → analysis with trends and recommendations sent to QA management; QA manager) | 14643 |

Coder notes:

- **14638**: Overlaps heavily with 14640 (testing programs by area) and 14648 (documenting procedures); boundaries between these three statements are blurry.
- **14640**: Essentially the same work as 14638 at a slightly different grain.
- **14642**: Nearly the same work item as 14641; 14642 puts more weight on the analysis before the write-up.
- **14643**: Fix retesting in part a also appears in 14640 ('error or bug retests'). Time shares are a judgment.
- **14644**: Many teams use a commercial bug tracker, so 'create' may mostly be configuration; the 0.2/0.8 split is a judgment.
- **14645**: Could be folded into the test plan of 14638 in some organizations.
- **14646**: Some reviews are done asynchronously with written comments on a design document, which would make that portion DISCRETE.
- **14648**: Overlaps with 14638, which also mentions procedures.
- **14652**: 'Use' testing programs is largely the means for test execution covered by other statements (e.g. 14639, 14655).
- **14653**: Some of this feedback is given verbally in stand-ups or reviews, which would be INTERPERSONAL.
- **14654**: Time shares are a judgment.
- **14655**: Testing on physical hardware or devices may involve some hands-on setup away from the computer; not split out because it is usually a small share.
- **14656**: If physical servers must be racked or cabled, part of this work would be PHYSICAL; today it is mostly virtual.
- **14657**: Could be read as DISCRETE if most diagnosis is done offline; overlaps with 14651.
- **14659**: A whole framework could be project-scale; the item is meant as one tool or feature.
- **14660**: A test round may be close to project scale; time shares are a judgment.
- **14662**: The on-site part is largely observation and conversation with site staff; it could also be read as INTERPERSONAL.
