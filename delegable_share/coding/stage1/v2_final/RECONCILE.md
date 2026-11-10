# Stage 1 reconciliation log — v2

Base coding: Claude (Opus subagent). Disputed statements replaced by the outcome of reconciliation (both picked the same coding) or adjudication (Opus).

Outcomes: claude 12, terra 5, adjudicator revision 1

## 15-1232.00
- **1283**: adjudicated: Y — The statement names two purposes, verifying correct operation after an install, repair or change, and detecting errors through routine checks, and Y gives each a realistic handover unit (a verification noted on the ticket, a recorded check round). X's live part treats command tests during a user contact as their own item, but that testing is a step inside troubleshooting already coded under 1282/1288, and 'one system operation tested' is below the handover level. → claude
- **1287**: adjudicated: Y — Y separates the two kinds of record the statement actually names, per-problem ticket notes and the daily log of communication transactions and installations, each with a unit supervisors and auditors review. The instructions frame a record-keeping statement's item as the record written after the contact, and Y flags the possible live share in its notes; X's split lumps all record types into one back-office part and makes a thin live part out of typing notes. → claude
- **1291**: adjudicated: X — Referring a major problem or defective product to a vendor or outside technician today normally means opening a vendor case or RMA from the queue after the user contact, not a warm transfer while the user waits. X's single DISCRETE part with the vendor case as its unit fits this, and Y's 25% live share has little basis. → claude
- **1295**: both picked Y → terra

## 43-4051.00
- **2579**: adjudicated: revised — Both split by where the remedy is processed, as Example D asks, but X's PHYSICAL part is not typical of this occupation, whose reps mostly work by phone or at a desk while goods are handled by returns staff. Y's part b makes the work item the whole complaint case, absorbing investigation (2585) and notification (2581), whereas the instructions say a workflow step's work item should be that step's own output. Revised: keep Y's structure but narrow part b to processing the remedy itself. → adjudicator revision
- **2582**: adjudicated: X — The statement's output is a referral that the investigating department works from, and that is a written escalation ticket or form; the customer is told about it in the live conversation (18565), but the referral itself is the handed-over item. Y's live part mainly describes call transfers, which belong to the conversation rather than to a referral for investigation. X's single DISCRETE part follows the instructions better. → claude
- **2583**: adjudicated: X — Quoting a charge and taking a deposit or payment are done while the customer is on the line or at the desk, so the activity is almost entirely live. Y's back-office part is vague and its 30% share is not well supported; processing mailed payments is closer to billing-clerk work. X's single LIVE_SERVICE part with a note on later billing set-up fits better. → claude
- **2584**: adjudicated: Y — Contract forms, address changes, and discontinuance orders are all account paperwork entered on the computer, so the statement lists alternative items for one activity rather than different activities. The distinction the instructions call for is where the work is done, and Y splits on that; X's four-way split adds detail not required by the instructions. → claude
- **18565**: adjudicated: Y — Both split live contacts by kind of item; Y's merge of orders and cancellations is reasonable since both are entered and confirmed on the spot. X names the representative as the checker for complaint intake, which fails the requirement that someone else checks or relies on the work, while Y names the staff who act on the complaint. → claude

## 15-1253.00
- **14638**: both picked Y → terra
- **14643**: adjudicated: Y — Monitoring bug resolution is ongoing and should be recast into the items it produces, as in Example B. Y names real handover units: a fixed defect verified and closed or reopened, and a periodic defect-status report, which matches the statement's 'track successes'. X's 'status update' is too thin to be a unit someone checks as a whole. → claude
- **14646**: adjudicated: X — The target is participation in design reviews, which is a live interaction; the listed subjects are the input given, not separate activities. Written comments on design or requirements documents are largely covered by 14647 (reviewing software documentation), so Y's part b risks double counting. X follows the target directly. → terra
- **14649**: adjudicated: X — Standards, methods and procedures for judging quality or release readiness are alternative forms of the same deliverable and are normally written and approved together as one criteria or quality document. Y's split invents a boundary the workplace does not use. → claude
- **14652**: adjudicated: Y — Installing and maintaining testing tools are the same kind of tool-administration work, handled one change or ticket at a time, while using the tools to run tests is a different activity. Y's two-part split captures this; X's separate install and maintain parts are thin divisions of one activity. → claude
- **14653**: both picked X → claude
- **14654**: adjudicated: X — The statement is monitoring 'to ensure efficient and problem-free operations', which is reactive and yields individual performance issues investigated. Unlike Example B, it does not name forward-looking planning, so Y's 40% reporting share is not established by the target and overlaps 14664. X codes the actionable item directly. → terra
- **14660**: both picked X → claude
- **14662**: both picked Y → terra
