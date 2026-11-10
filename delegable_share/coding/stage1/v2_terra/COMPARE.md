# Stage 1 comparison: `coding/stage1/v2` (A) vs `coding/stage1/v2_terra` (B)

## Share of importance by type

| Occupation | Run | DISCRETE | LIVE_SERVICE | INTERPERSONAL | PHYSICAL | NO_DELIVERABLE | Parts |
|---|---|---|---|---|---|---|---|
| Computer User Support Specialists | A | 63% | 7% | 14% | 10% | 5% | 26 |
| Computer User Support Specialists | B | 53% | 15% | 14% | 13% | 5% | 26 |
| Customer Service Representatives | A | 50% | 40% | 7% | 2% | 0% | 22 |
| Customer Service Representatives | B | 47% | 42% | 7% | 4% | 0% | 28 |
| Software Quality Assurance Analysts and Testers | A | 91% | 2% | 5% | 2% | 0% | 37 |
| Software Quality Assurance Analysts and Testers | B | 95% | 1% | 4% | 0% | 0% | 33 |

## Agreement: 38 of 56 statements have the same number of parts and a type mix within 0.25 (half-L1).

## Disagreements (largest type-mix difference first)

### 14662 — Visit beta testing sites to evaluate software performance.  (type-mix distance 0.60)
- Aa PHYSICAL 0.60: Travel to a beta testing site and evaluate the software's performance in place.
- Ab DISCRETE 0.40: one beta site visit report
- Ba DISCRETE 1.00: one beta-site performance evaluation

### 1283 — Enter commands and observe system functioning to verify correct operations and detect errors.  (type-mix distance 0.40)
- Aa DISCRETE 0.60: one post-install or post-repair verification of a machine or system
- Ab DISCRETE 0.40: one routine system check round (e.g. daily check of servers, printers, network links)
- Ba LIVE_SERVICE 0.40: one system operation tested during a live support contact
- Bb DISCRETE 0.60: one system operation checked

### 2582 — Refer unresolved customer grievances to designated departments for further investigation.  (type-mix distance 0.40)
- Aa DISCRETE 1.00: one grievance referral ticket
- Ba LIVE_SERVICE 0.40: one grievance referred during a customer contact
- Bb DISCRETE 0.60: one grievance referral submitted for investigation

### 14653 — Provide feedback and recommendations to developers on software usability and functionality.  (type-mix distance 0.40)
- Aa DISCRETE 0.60: one written feedback note on a build or feature
- Ab INTERPERSONAL 0.40: Discuss usability and functionality with developers in meetings or informal conversation.
- Ba DISCRETE 1.00: one set of usability or functionality feedback

### 14646 — Participate in product design reviews to provide input on functional requirements, product designs, schedules, or potential problems.  (type-mix distance 0.35)
- Aa INTERPERSONAL 0.65: Take part in product design review meetings, giving input on requirements, designs, schedules, and risks.
- Ab DISCRETE 0.35: one set of written review comments on a design or requirements document
- Ba INTERPERSONAL 1.00: Participate in a product design review and provide testing-related input.

### 14660 — Coordinate user or third-party testing.  (type-mix distance 0.35)
- Aa DISCRETE 0.40: one user or third-party test round organized
- Ab DISCRETE 0.25: one test round results report
- Ac INTERPERSONAL 0.35: Coordinate with users or third-party testers during testing through meetings and check-ins.
- Ba DISCRETE 1.00: one user or third-party testing round coordinated

### 1287 — Maintain records of daily data communication transactions, problems and remedial actions taken, or installation activities.  (type-mix distance 0.30)
- Aa DISCRETE 0.60: one problem-and-remedy record written up for a ticket
- Ab DISCRETE 0.40: one day's log of transactions and installation activities
- Ba LIVE_SERVICE 0.30: one support interaction record entered during a live contact
- Bb DISCRETE 0.70: one transaction, problem, or installation record completed

### 1295 — Inspect equipment and read order sheets to prepare for delivery to users.  (type-mix distance 0.30)
- Aa PHYSICAL 0.70: Inspect computer equipment and prepare it physically for delivery to users.
- Ab DISCRETE 0.30: one delivery order reviewed and matched to equipment
- Ba PHYSICAL 1.00: Inspect equipment against order sheets to prepare it for delivery to users.

### 2583 — Determine charges for services requested, collect deposits or payments, or arrange for billing.  (type-mix distance 0.30)
- Aa LIVE_SERVICE 1.00: one service charge determined and payment or billing arrangement completed during a contact
- Ba LIVE_SERVICE 0.70: one service charge and payment arrangement handled during a contact
- Bb DISCRETE 0.30: one service charge and payment arrangement processed

### 1291 — Refer major hardware or software problems or defective products to vendors or technicians for service.  (type-mix distance 0.25)
- Aa DISCRETE 1.00: one vendor or technician service referral (case or RMA opened)
- Ba LIVE_SERVICE 0.25: one service referral made during a live contact
- Bb DISCRETE 0.75: one vendor or technician service referral

### 2579 — Resolve customers' service or billing complaints by performing activities such as exchanging merchandise, refunding money, or adjusting bills.  (type-mix distance 0.15)
- Aa LIVE_SERVICE 0.65: one refund, exchange, or bill adjustment entered during a call or visit
- Ab DISCRETE 0.35: one complaint case resolved from the written queue
- Ba LIVE_SERVICE 0.50: one customer remedy processed during a contact
- Bb DISCRETE 0.35: one customer remedy processed after a contact
- Bc PHYSICAL 0.15: Handle returned and replacement merchandise as part of an exchange.

### 2584 — Complete contract forms, prepare change of address records, or issue service discontinuance orders, using computers.  (type-mix distance 0.00)
- Aa LIVE_SERVICE 0.60: one account order (contract, address change, or discontinuance) entered during a contact
- Ab DISCRETE 0.40: one account order processed from a written request
- Ba LIVE_SERVICE 0.20: one contract form completed during a contact
- Bb DISCRETE 0.20: one contract form completed for processing
- Bc LIVE_SERVICE 0.40: one account change or discontinuance order entered during a contact
- Bd DISCRETE 0.20: one account change or discontinuance order processed

### 18565 — Confer with customers by telephone or in person to provide information about products or services, take or enter orders, cancel accounts, or obtain details of complaints.  (type-mix distance 0.00)
- Aa LIVE_SERVICE 0.40: one information inquiry answered during a call or visit
- Ab LIVE_SERVICE 0.35: one order or account cancellation entered during a contact
- Ac LIVE_SERVICE 0.25: one complaint taken during a call or visit
- Ba LIVE_SERVICE 0.30: one product or service inquiry answered live
- Bb LIVE_SERVICE 0.30: one customer order taken or entered during a contact
- Bc LIVE_SERVICE 0.15: one account cancellation handled during a contact
- Bd LIVE_SERVICE 0.25: one customer's complaint details obtained during a contact

### 14638 — Design test plans, scenarios, scripts, or procedures.  (type-mix distance 0.00)
- Aa DISCRETE 1.00: one test plan or test case set for a feature or release
- Ba DISCRETE 0.40: one test plan
- Bb DISCRETE 0.60: one feature-level set of test cases or scripts

### 14643 — Monitor bug resolution efforts and track successes.  (type-mix distance 0.00)
- Aa DISCRETE 0.60: one resolved defect verified and closed or reopened
- Ab DISCRETE 0.40: one defect status report (weekly or per sprint)
- Ba DISCRETE 1.00: one defect resolution status update

### 14649 — Develop or specify standards, methods, or procedures to determine product quality or release readiness.  (type-mix distance 0.00)
- Aa DISCRETE 1.00: one quality standard or set of release-readiness criteria
- Ba DISCRETE 0.40: one set of quality or release-readiness standards
- Bb DISCRETE 0.60: one quality or release-readiness assessment procedure

### 14652 — Install, maintain, or use software testing programs.  (type-mix distance 0.00)
- Aa DISCRETE 0.35: one testing tool installed or upgraded
- Ab DISCRETE 0.65: one test run executed with results recorded
- Ba DISCRETE 0.15: one testing program installation
- Bb DISCRETE 0.25: one testing program maintenance update
- Bc DISCRETE 0.60: one test suite run using a testing program

### 14654 — Monitor program performance to ensure efficient and problem-free operations.  (type-mix distance 0.00)
- Aa DISCRETE 0.60: one performance anomaly investigated
- Ab DISCRETE 0.40: one performance report (per release or period)
- Ba DISCRETE 1.00: one monitored performance issue investigated
