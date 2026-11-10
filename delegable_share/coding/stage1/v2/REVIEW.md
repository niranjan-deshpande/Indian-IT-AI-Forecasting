# Stage 1 unit schema v2 — pilot, for hand-check

Coded 2026-11-09: Opus subagents (one per occupation), prompt v2; duplicates collapsed where Claude and GPT-6.1 Terra both flagged them (Stage 1b).
Cross-check against Terra: `v2_terra/COMPARE.md`. Duplicate pass: `DUPLICATES.md`. Full reasoning: `units_final.csv`.

Weight = O*NET importance × time share (collapsed pairs: mean of the two).

## Computer User Support Specialists

Share of weight: DISCRETE 65%, INTERPERSONAL 15%, PHYSICAL 11%, NO_DELIVERABLE 6%, LIVE_SERVICE 4%

| Task | Statement | Part | Type | Share | Work item (start → end; checked by) | Overlaps |
|---|---|---|---|---|---|---|
| 1282 | Answer user inquiries regarding computer software or hardware operation to resolve problems. | a | LIVE_SERVICE | 0.60 | one user call, chat, or walk-up question answered (user calls, opens a chat, or walks up with a question → user confirms the answer or fix works, or the issue is logged for follow-up; the user who asked; help-desk supervisor through call reviews) | 1288;1287;1291 **collapsed with 1288a** |
| 1282 | ″ | b | DISCRETE | 0.40 | one written user question answered (ticket or email) (question received by email or in the ticket queue → answer sent and ticket closed; the user who asked; help-desk lead reviewing ticket quality) | 1288;1287 |
| 1283 | Enter commands and observe system functioning to verify correct operations and detect errors. | a | DISCRETE | 0.60 | one post-install or post-repair verification of a machine or system (installation, repair, or change completed → correct operation confirmed and noted on the ticket, or error found and fix reopened; the user; support lead closing the ticket) | 1284;1286;1285 |
| 1283 | ″ | b | DISCRETE | 0.40 | one routine system check round (e.g. daily check of servers, printers, network links) (scheduled check begins → results recorded, with any errors logged as tickets; IT supervisor; systems administrators who act on the errors) | 1285;1287 |
| 1284 | Install and perform minor repairs to hardware, software, or peripheral equipment, following design or installation specifications. | a | PHYSICAL | 0.50 | *Install or make minor repairs to computer hardware or peripheral equipment (e.g. replace a drive, memory, keyboard, or printer part) following specifications.* | 1286;1291;1283 |
| 1284 | ″ | b | DISCRETE | 0.50 | one software installation or minor software repair completed on a machine (install or repair request received → software installed or fixed and ticket closed; the user; support lead) | 1286;1282;1288;1283 |
| 1285 | Oversee the daily performance of computer systems. | a | DISCRETE | 0.60 | one performance alert or problem followed up (alert raised or slowdown noticed or reported → cause recorded and fix applied, escalated, or closed as no action; IT supervisor; systems administrators) | 1283;1288;1291 |
| 1285 | ″ | b | DISCRETE | 0.40 | one daily system status review (start of day or shift; pull of monitoring data and logs → status recorded and any issues raised as tickets; IT supervisor) | 1283;1287 |
| 1286 | Set up equipment for employee use, performing or ensuring proper installation of cables, operating systems, or appropriate software. | a | PHYSICAL | 0.40 | *Physically set up computer equipment at an employee's workstation, including placing hardware and running and connecting cables.* | 1284;1295 |
| 1286 | ″ | b | DISCRETE | 0.60 | one workstation configured and handed over to an employee (setup request or new-starter ticket received with hardware available → machine imaged, software and accounts configured, handed to employee and ticket closed; the employee; IT supervisor) | 1284;1283;1295 |
| 1287 | Maintain records of daily data communication transactions, problems and remedial actions taken, or installation activities. | a | DISCRETE | 0.60 | one problem-and-remedy record written up for a ticket (problem handled or remedy applied → ticket notes complete with problem, steps taken, and outcome; ticket closed or updated; help-desk lead; other support staff who pick up the ticket later) | 1282;1288 |
| 1287 | ″ | b | DISCRETE | 0.40 | one day's log of transactions and installation activities (start of day or shift → day's entries complete and log filed; IT supervisor; auditors) | 1283;1285;1284;1286 |
| 1288 | Read technical manuals, confer with users, or conduct computer diagnostics to investigate and resolve problems or to provide technical assistance and support. | b | DISCRETE | 0.55 | one ticketed problem investigated and resolved (ticket assigned or problem left open from a contact → fix applied and confirmed by the user, ticket closed, or ticket escalated; the user; help-desk lead) | 1282;1291;1284;1287 |
| 1289 | Confer with staff, users, and management to establish requirements for new systems or modifications. | a | INTERPERSONAL | 1.00 | *Meet with staff, users, and management to establish requirements for new systems or modifications.* | 1292;1297;1296 |
| 1290 | Develop training materials and procedures, or train users in the proper use of hardware or software. | a | DISCRETE | 0.40 | one training guide, how-to document, or procedure (need for material identified (new system, recurring question) → material reviewed and published to users or the knowledge base; IT supervisor; users who follow it) |  |
| 1290 | ″ | b | INTERPERSONAL | 0.60 | *Train users, individually or in groups, in the proper use of hardware or software.* | 1282 |
| 1291 | Refer major hardware or software problems or defective products to vendors or technicians for service. | a | DISCRETE | 1.00 | one vendor or technician service referral (case or RMA opened) (problem judged beyond in-house repair or product found defective → case opened with vendor with problem details and warranty info, user informed, ticket updated; vendor or technician; the affected user; IT supervisor) | 1282;1284;1288;1287 |
| 1292 | Prepare evaluations of software or hardware, and recommend improvements or upgrades. | a | DISCRETE | 1.00 | one evaluation with recommendation (product, upgrade, or improvement) (request or identified need to assess a product or system → evaluation and recommendation sent to IT manager; IT manager; purchasing decision-makers) | 1297;1289 |
| 1293 | Read trade magazines and technical manuals, or attend conferences and seminars to maintain knowledge of hardware and software. | a | NO_DELIVERABLE | 1.00 | *Read trade magazines and technical manuals, or attend conferences and seminars, to keep up with hardware and software.* | 1288 |
| 1295 | Inspect equipment and read order sheets to prepare for delivery to users. | a | PHYSICAL | 0.70 | *Inspect computer equipment and prepare it physically for delivery to users.* | 1286 |
| 1295 | ″ | b | DISCRETE | 0.30 | one delivery order reviewed and matched to equipment (order sheet received → items and configuration confirmed against the order and delivery ready to schedule; the receiving user; IT supervisor or asset manager) | 1286 |
| 1296 | Modify and customize commercial programs for internal needs. | a | DISCRETE | 1.00 | one program customization delivered (template, macro, configuration change) (customization request received → change tested and released to users; requesting users; IT supervisor) | 1289 |
| 1297 | Conduct office automation feasibility studies, including workflow analysis, space design, or cost comparison analysis. | a | DISCRETE | 1.00 | one office automation feasibility study report (study requested or scoped → study with analysis and recommendation delivered to management; IT manager; office or department management) | 1292;1289 |
| 15204 | Hire, supervise, and direct workers engaged in special project work, problem-solving, monitoring, and installation of data communication equipment and software. | a | DISCRETE | 0.25 | one vacancy filled (hiring decision made) (vacancy approved and applications received → candidate selected and recommendation or offer sent to HR; HR; hiring manager) |  |
| 15204 | ″ | b | INTERPERSONAL | 0.75 | *Supervise and direct workers doing special project work, problem-solving, monitoring, and installation of data communication equipment and software.* |  |

Coder notes:

- **1282**: Live versus written share depends heavily on whether the desk is phone-first or ticket-first; 1288 covers the investigation behind harder questions and overlaps substantially.
- **1283**: Part b is close to 1285 (overseeing daily performance); the boundary between the two statements is blurry.
- **1284**: Hardware/software split share is a judgment; remote software deployment makes part b more common in some sites.
- **1285**: 'Oversee' is vague; for a user support specialist this is likely a modest share of time, and it overlaps heavily with 1283.
- **1286**: 'Ensuring proper installation' may mean checking others' work; treated as part of the same setup items.
- **1287**: Some ticket notes are typed while the user is still on the line; treated here as wrap-up work done after the contact, which may understate a live share.
- **1288**: Strong overlap with 1282; the two statements describe largely the same problem-resolution workflow from different angles.
- **1289**: If a written requirements summary is produced, it could be treated as a DISCRETE item; the statement only says 'confer'.
- **1290**: Share between writing and delivering training is a judgment and varies by organization.
- **1291**: Unclear whether follow-up until the item is returned is part of the referral; treated as ending when the case is handed over.
- **1293**: Reading manuals to solve a specific problem belongs to 1288, not here.
- **1295**: The physical/paperwork share is a judgment; the order reading may be small.
- **1297**: Studies may be large; a single report could be close to project scale. Some site visits for space design may be physical, but they are minor.
- **15204**: Interviewing is itself interpersonal; part a is coded at the level of the hiring decision.

## Customer Service Representatives

Share of weight: DISCRETE 50%, LIVE_SERVICE 40%, INTERPERSONAL 7%, PHYSICAL 2%

| Task | Statement | Part | Type | Share | Work item (start → end; checked by) | Overlaps |
|---|---|---|---|---|---|---|
| 2578 | Keep records of customer interactions or transactions, recording details of inquiries, complaints, or comments, as well as actions taken. | a | LIVE_SERVICE | 0.40 | one set of contact notes entered during a call or visit (customer states the reason for the contact → notes and actions logged on the account before the contact ends; quality-assurance reviewer and later agents who read the account history) | 18565;2579 |
| 2578 | ″ | b | DISCRETE | 0.60 | one interaction record completed after a call or visit (call or visit ends → record saved with disposition code, summary, and actions taken; quality-assurance reviewer, supervisor, and later agents handling the account) | 2582;2580 |
| 2579 | Resolve customers' service or billing complaints by performing activities such as exchanging merchandise, refunding money, or adjusting bills. | a | LIVE_SERVICE | 0.65 | one refund, exchange, or bill adjustment entered during a call or visit (customer agrees to the proposed remedy → refund, exchange, or adjustment confirmed to the customer; the customer, and supervisor or finance for adjustments above limits) | 18565;2583;2585 |
| 2579 | ″ | b | DISCRETE | 0.35 | one complaint case resolved from the written queue (complaint received by email, letter, or web form → remedy processed, customer notified, case closed; the customer, supervisor, and billing or finance team) | 2585;2581;2589;2580 |
| 2580 | Check to ensure that appropriate changes were made to resolve customers' problems. | a | DISCRETE | 1.00 | one resolution verified for a customer case (follow-up date reached or confirmation of change expected → change confirmed and case closed, or discrepancy flagged and case reopened; supervisor and the customer) | 2579;2581 |
| 2581 | Contact customers to respond to inquiries or to notify them of claim investigation results or any planned adjustments. | a | DISCRETE | 0.55 | one written response or notification sent to a customer (inquiry or investigation result ready for response → letter or email sent and logged on the account; the customer, and supervisor or QA reviewer) | 2579;2585;2587 |
| 2581 | ″ | b | LIVE_SERVICE | 0.45 | one outbound callback delivering an answer or result (customer answers the call → result explained, customer's questions answered, call ended; the customer, and QA reviewer of recorded calls) | 18565;2580 |
| 2582 | Refer unresolved customer grievances to designated departments for further investigation. | a | DISCRETE | 1.00 | one grievance referral ticket (representative determines the grievance cannot be resolved at first level → referral with case details submitted to the designated department; receiving department and supervisor) | 2578;2585 |
| 2583 | Determine charges for services requested, collect deposits or payments, or arrange for billing. | a | LIVE_SERVICE | 1.00 | one service charge determined and payment or billing arrangement completed during a contact (customer requests a service → charge quoted, payment or deposit taken or billing arranged, receipt or confirmation given; the customer, and cash-office or billing reconciliation) | 18565;2584;2579 |
| 2584 | Complete contract forms, prepare change of address records, or issue service discontinuance orders, using computers. | a | LIVE_SERVICE | 0.60 | one account order (contract, address change, or discontinuance) entered during a contact (customer requests the change → order submitted and confirmation given to the customer; the customer and the fulfilment or billing team that acts on the order) | 18565;2583 |
| 2584 | ″ | b | DISCRETE | 0.40 | one account order processed from a written request (written or online request received → order entered and confirmation sent to the customer; the customer and the fulfilment or billing team) |  |
| 2585 | Obtain and examine all relevant information to assess validity of complaints and to determine possible causes, such as extreme weather conditions that could increase utility bills. | a | LIVE_SERVICE | 0.45 | one complaint assessed during a call or visit (customer describes the complaint → validity and likely cause explained to the customer and noted; the customer and QA reviewer) | 18565;2579 |
| 2585 | ″ | b | DISCRETE | 0.55 | one complaint investigation with a validity finding (complaint case opened for review → finding on validity and cause recorded and passed for remedy or reply; supervisor, and the staff who decide the remedy) | 2587;2589;2579;2581;2582 |
| 2586 | Solicit sales of new or additional services or products. | a | INTERPERSONAL | 1.00 | *Offer and promote new or additional services or products to customers during contacts.* | 18565 |
| 2587 | Review insurance policy terms to determine whether a particular loss is covered by insurance. | a | LIVE_SERVICE | 0.40 | one coverage question answered during a call (customer describes the loss and asks whether it is covered → coverage answer given and noted on the account; the customer and claims staff who later rely on the note) | 18565 |
| 2587 | ″ | b | DISCRETE | 0.60 | one coverage determination for a reported loss (loss report and policy retrieved → coverage decision recorded on the claim file; claims adjuster or supervisor, and the customer) | 2585;2581 |
| 2589 | Compare disputed merchandise with original requisitions and information from invoices and prepare invoices for returned goods. | a | PHYSICAL | 0.35 | *Physically inspect disputed merchandise and compare it with the original requisition.* | 2585 |
| 2589 | ″ | b | DISCRETE | 0.65 | one return invoice prepared for a disputed shipment (disputed goods and original requisition and invoice in hand → return invoice issued and sent to billing and the customer; billing or accounts receivable, and the customer) | 2579;2585 |
| 2591 | Recommend improvements in products, packaging, shipping, service, or billing methods and procedures to prevent future problems. | a | DISCRETE | 1.00 | one improvement recommendation submitted (recurring problem identified from customer contacts → recommendation with supporting examples sent to supervisor or process owner; supervisor or the department that owns the process) | 2578 |
| 18565 | Confer with customers by telephone or in person to provide information about products or services, take or enter orders, cancel accounts, or obtain details of complaints. | a | LIVE_SERVICE | 0.40 | one information inquiry answered during a call or visit (customer asks a question → customer confirms the question is answered, contact ends; the customer and QA reviewer) | 2581 |
| 18565 | ″ | b | LIVE_SERVICE | 0.35 | one order or account cancellation entered during a contact (customer asks to order or cancel → order or cancellation confirmed to the customer; the customer and the fulfilment or billing team) | 2584;2583;2586 |
| 18565 | ″ | c | LIVE_SERVICE | 0.25 | one complaint taken during a call or visit (customer raises a complaint → complaint details captured and next steps explained to the customer; the customer and the staff who investigate or resolve it) | 2578;2579;2585 |

Coder notes:

- **2578**: The live versus wrap-up share depends on the center's after-call-work policy.
- **2579**: Notification of the remedy for written cases also falls under 2581.
- **2580**: Some checks happen immediately during the original call; this coding assumes the typical follow-up after the contact.
- **2581**: Outbound calls are initiated by the representative, which fits LIVE_SERVICE only loosely; channel mix varies by employer.
- **2582**: The customer is often told of the escalation during the call, but writing the referral is usually wrap-up work.
- **2583**: Some billing arrangements may be completed later in the back office; assumed small.
- **2584**: 18565 includes 'enter orders' and 'cancel accounts', which overlaps part a.
- **2585**: The split between quick and deep assessments varies a lot by industry.
- **2586**: Could be read as LIVE_SERVICE if the sale and order entry are counted here rather than under 18565.
- **2587**: Applies only to insurance-sector representatives; the live share is a guess.
- **2589**: Physical share depends on whether the representative sees the goods or only photos and documents.
- **2591**: Some recommendations are made orally in team meetings, which would be INTERPERSONAL.
- **18565**: This broad statement overlaps the live parts of many other statements; shares across parts are a judgment.

## Software Quality Assurance Analysts and Testers

Share of weight: DISCRETE 91%, INTERPERSONAL 5%, PHYSICAL 2%, LIVE_SERVICE 2%

| Task | Statement | Part | Type | Share | Work item (start → end; checked by) | Overlaps |
|---|---|---|---|---|---|---|
| 14638 | Design test plans, scenarios, scripts, or procedures. | a | DISCRETE | 1.00 | one test plan or test case set for a feature or release (requirements or change specification received for testing → test plan and cases reviewed and approved in the test management tool; QA lead / test manager) | 14640;14645;14648 |
| 14639 | Test system modifications to prepare for implementation. | a | DISCRETE | 1.00 | one system modification tested (one test cycle) (change deployed to the test environment and assigned for testing → test results recorded and change signed off or returned with defects; release manager / development lead) | 14641;14642;14652;14655 |
| 14640 | Develop testing programs that address areas such as database impacts, software scenarios, regression testing, negative testing, error or bug retests, or usability. | a | DISCRETE | 1.00 | one test suite for one testing area of a release (testing area and scope assigned → suite written, reviewed, and added to the test repository; QA lead) | 14638;14650;14659 |
| 14641 | Document software defects, using a bug tracking system, and report defects to software developers. | a | DISCRETE | 1.00 | one defect report filed in the bug tracker (defect observed during testing → ticket filed with steps to reproduce, severity, and evidence, and assigned to a developer; developers / triage lead) | 14642;14661 **collapsed with 14642a** |
| 14643 | Monitor bug resolution efforts and track successes. | a | DISCRETE | 0.60 | one resolved defect verified and closed or reopened (developer marks the defect fixed → ticket closed or reopened with a note; developers / QA lead) | 14640;14641 |
| 14643 | ″ | b | DISCRETE | 0.40 | one defect status report (weekly or per sprint) (pull of current defect data from the tracker → report with counts, trends, and blockers sent to the project team; QA manager / project manager) | 14664 |
| 14644 | Create or maintain databases of known test defects. | a | DISCRETE | 0.15 | one known-defects database set up (need for a defect repository agreed → database configured with fields and workflows and opened to the team; QA manager / team users) | 14652;14663 |
| 14644 | ″ | b | DISCRETE | 0.85 | one curation pass over the known-defects database (scheduled review or release milestone → records updated, duplicates merged, and known-issues list current; QA lead / support and development teams) | 14641;14643 |
| 14645 | Plan test schedules or strategies in accordance with project scope or delivery dates. | a | DISCRETE | 1.00 | one test strategy and schedule for a project or release (project scope and delivery dates received → strategy and schedule approved by project stakeholders; QA manager / project manager) | 14638;14649 |
| 14646 | Participate in product design reviews to provide input on functional requirements, product designs, schedules, or potential problems. | a | INTERPERSONAL | 0.65 | *Take part in product design review meetings, giving input on requirements, designs, schedules, and risks.* |  |
| 14646 | ″ | b | DISCRETE | 0.35 | one set of written review comments on a design or requirements document (design document circulated for review → comments submitted to the document owner; product owner / design lead) | 14647 |
| 14647 | Review software documentation to ensure technical accuracy, compliance, or completeness, or to mitigate risks. | a | DISCRETE | 1.00 | one software document reviewed with findings (document submitted for review → findings returned or document approved; document author / QA lead) | 14646;14658 |
| 14648 | Document test procedures to ensure replicability and compliance with standards. | a | DISCRETE | 1.00 | one test procedure documented (test procedure designed or run → procedure document reviewed and stored in the test repository; QA lead / compliance auditor) | 14638 |
| 14649 | Develop or specify standards, methods, or procedures to determine product quality or release readiness. | a | DISCRETE | 1.00 | one quality standard or set of release-readiness criteria (need for a standard or criteria identified → document approved and published to the team; QA manager / engineering leadership) | 14645;14658 |
| 14650 | Update automated test scripts to ensure currency. | a | DISCRETE | 1.00 | one set of automated test scripts updated for a product change (product change breaks or outdates scripts → updated scripts reviewed, merged, and passing in the pipeline; QA lead / code reviewer) | 14640;14659 |
| 14651 | Investigate customer problems referred by technical support. | a | DISCRETE | 1.00 | one escalated customer problem investigated (escalation ticket received from technical support → problem reproduced or not, findings returned to support, and defect filed if needed; technical support / developers) | 14641;14657;14661 |
| 14652 | Install, maintain, or use software testing programs. | a | DISCRETE | 0.35 | one testing tool installed or upgraded (tool install or upgrade requested → tool working and available to the team; QA team users / QA lead) | 14656;14663 |
| 14652 | ″ | b | DISCRETE | 0.65 | one test run executed with results recorded (test run scheduled or triggered → results logged in the test management tool; QA lead / developers) | 14639;14655 |
| 14653 | Provide feedback and recommendations to developers on software usability and functionality. | a | DISCRETE | 0.60 | one written feedback note on a build or feature (build or feature evaluated → feedback and recommendations sent to developers; developers / product owner) | 14641;14642 |
| 14653 | ″ | b | INTERPERSONAL | 0.40 | *Discuss usability and functionality with developers in meetings or informal conversation.* | 14646 |
| 14654 | Monitor program performance to ensure efficient and problem-free operations. | a | DISCRETE | 0.60 | one performance anomaly investigated (slowdown or error spotted in monitoring or test results → cause recorded and defect filed or anomaly closed; developers / QA lead) | 14642;14661 |
| 14654 | ″ | b | DISCRETE | 0.40 | one performance report (per release or period) (pull of the period's performance data → report sent to the development team; development lead / QA manager) | 14656;14664 |
| 14655 | Conduct software compatibility tests with programs, hardware, operating systems, or network environments. | a | DISCRETE | 1.00 | one compatibility test cycle for a build (build and configuration matrix ready → compatibility results recorded and issues filed; QA lead / release manager) | 14639;14652;14656 |
| 14656 | Install and configure recreations of software production environments to allow testing of software performance. | a | DISCRETE | 1.00 | one test environment built to mirror production (environment request with production specification → environment configured, verified, and handed to testers; QA lead / performance testers) | 14652 |
| 14657 | Collaborate with field staff or customers to evaluate or diagnose problems and recommend possible solutions. | a | LIVE_SERVICE | 0.50 | one problem diagnosed during a live session with field staff or a customer (session begins with the problem described → likely cause identified and next steps agreed; the customer or field staff member) | 14651 |
| 14657 | ″ | b | DISCRETE | 0.50 | one written diagnosis and recommended solution (live session or field report ends → recommendation sent to field staff, customer, or developers; field staff / customer / developers) | 14651;14661 |
| 14658 | Identify program deviance from standards, and suggest modifications to ensure compliance. | a | DISCRETE | 1.00 | one standards-compliance review of a program with recommendations (program or build submitted for compliance check → deviations and suggested changes sent to developers; developers / QA lead) | 14647;14649 |
| 14659 | Design or develop automated testing tools. | a | DISCRETE | 1.00 | one automated testing tool or framework component (tool need or specification agreed → tool reviewed, merged, and in use by the team; QA lead / code reviewer) | 14640;14650 |
| 14660 | Coordinate user or third-party testing. | a | DISCRETE | 0.40 | one user or third-party test round organized (decision to run user or third-party testing → participants briefed with scripts, schedule, and access; QA manager / test participants) | 14638;14645 |
| 14660 | ″ | b | DISCRETE | 0.25 | one test round results report (test round closes and feedback is collected → findings report sent and defects filed; product owner / QA manager) | 14641 |
| 14660 | ″ | c | INTERPERSONAL | 0.35 | *Coordinate with users or third-party testers during testing through meetings and check-ins.* |  |
| 14661 | Perform initial debugging procedures by reviewing configuration files, logs, or code pieces to determine breakdown source. | a | DISCRETE | 1.00 | one defect given an initial root-cause diagnosis (failure reported or reproduced → likely source recorded on the ticket and handed to developers; developers) | 14642;14651;14657 |
| 14662 | Visit beta testing sites to evaluate software performance. | a | PHYSICAL | 0.60 | *Travel to a beta testing site and evaluate the software's performance in place.* | 14657 |
| 14662 | ″ | b | DISCRETE | 0.40 | one beta site visit report (site visit ends → report with findings sent to the development and product teams; product manager / development lead) | 14654 |
| 14663 | Evaluate or recommend software for testing or bug tracking. | a | DISCRETE | 1.00 | one tool evaluation with recommendation (tool need or candidate tools identified → evaluation and recommendation sent to the QA manager; QA manager) | 14652 |
| 14664 | Conduct historical analyses of test results. | a | DISCRETE | 1.00 | one historical test results analysis report (pull of past test results → report with trends and recommendations sent; QA manager) | 14643;14654 |

Coder notes:

- **14638**: Boundary with 14640 (testing programs) and 14648 (documenting procedures) is fuzzy.
- **14640**: Close to 14638; 'testing programs' could also mean automated suites, which overlap 14659.
- **14641**: 14642 includes identifying and analyzing the problem, which shares the documentation step with this statement.
- **14643**: Time shares are a judgment; part a overlaps the bug retests named in 14640.
- **14644**: Day-to-day defect entry belongs to 14641; this coding treats maintenance as curation.
- **14645**: Overlaps with test plans in 14638, which often contain the schedule.
- **14646**: The share of written versus meeting input varies by organization.
- **14648**: Close to the 'procedures' part of 14638.
- **14652**: 'Use' testing programs overlaps most test-execution statements.
- **14653**: The split between written and spoken feedback is a judgment.
- **14654**: Time shares are a judgment.
- **14655**: Hardware-based compatibility testing may involve some hands-on setup.
- **14656**: Where physical servers must be racked or cabled, a small physical part could be split off.
- **14657**: Whether live sessions count as LIVE_SERVICE or INTERPERSONAL is debatable.
- **14660**: Time shares are a judgment.
- **14662**: The on-site part could be coded INTERPERSONAL rather than PHYSICAL; it is mostly observation and talking with site users.
