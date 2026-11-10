# Delegable shares — pilot_v4c

D̄ = importance-weighted mean of D over items with a horizon (interpersonal, physical and no-deliverable items count as 0). Uncovered = share of weight whose matched benchmark has no horizon (or no match); it is excluded, not filled. S = expected net hours saved by delegating (gain minus review, and minus failure cost for live items), as a share of the item's unassisted hours, over the hours where delegation pays.

Headline measure: S; D alongside. Headline rows: the first two (ρ = 1, and ρ = 0.5 for benchmarks graded by tests or state checks). Other rows vary one setting from the first row.

| Scenario | Computer User Support Specialists | Customer Service Representatives | Software Quality Assurance Analysts and Testers |
|---|---|---|---|
| base | S 21% · D 58% (eq D 57%; unc 1%) | S 33% · D 85% (eq D 85%; unc 0%) | S 15% · D 66% (eq D 66%; unc 4%) |
| base, rho 0.5 (tests/state) | S 9% · D 44% (eq D 42%; unc 1%) | S 10% · D 23% (eq D 25%; unc 0%) | S 11% · D 54% (eq D 54%; unc 4%) |
| beta 0.6 | S 25% · D 63% (eq D 63%; unc 1%) | S 38% · D 88% (eq D 87%; unc 0%) | S 23% · D 83% (eq D 83%; unc 4%) |
| beta 1.0 | S 18% · D 53% (eq D 52%; unc 1%) | S 31% · D 83% (eq D 82%; unc 0%) | S 12% · D 54% (eq D 54%; unc 4%) |
| decompressed spread, both sides | S 9% · D 29% (eq D 28%; unc 1%) | S 14% · D 43% (eq D 43%; unc 0%) | S 3% · D 12% (eq D 12%; unc 4%) |
| decompressed spread, benchmarks only | S 27% · D 61% (eq D 60%; unc 1%) | S 40% · D 87% (eq D 86%; unc 0%) | S 21% · D 72% (eq D 71%; unc 4%) |
| lambda 0.25 | S 21% · D 59% (eq D 58%; unc 1%) | S 40% · D 86% (eq D 86%; unc 0%) | S 15% · D 66% (eq D 66%; unc 4%) |
| lambda 3 | S 20% · D 56% (eq D 55%; unc 1%) | S 22% · D 69% (eq D 69%; unc 0%) | S 15% · D 66% (eq D 66%; unc 4%) |
| fill from 2nd match | S 21% · D 58% (eq D 58%; unc 0%) | S 33% · D 85% (eq D 85%; unc 0%) | S 15% · D 66% (eq D 66%; unc 0%) |
| latest observed H (no date alignment) | S 11% · D 42% (eq D 40%; unc 1%) | S 19% · D 58% (eq D 57%; unc 0%) | S 7% · D 46% (eq D 46%; unc 4%) |
| +12 months (pooled trend) | S 35% · D 65% (eq D 65%; unc 1%) | S 53% · D 90% (eq D 89%; unc 0%) | S 37% · D 91% (eq D 91%; unc 4%) |

## Items (base scenario)

| item | type | work item | w | benchmark | H (min) | π at p50 | D | S | delegated lengths (min) |
|---|---|---|---|---|---|---|---|---|---|
| 1282a | LIVE | one user call, chat, or walk-up question answered | 2.02 | eva_bench | 143.1 | 0.818 | 0.8079 | 0.289 | 0.5–38.8 |
| 1282b | DISC | one written user question answered (ticket or email) | 1.52 | gdpval | 4729.4 | 0.984 | 0.9986 | 0.4358 | 2.1–594.8 |
| 1283a | DISC | one post-install or post-repair verification of a machine or | 2.14 | terminal_bench_1 | 1101.0 | 0.936 | 0.9998 | 0.5182 | 1.5–964.8 |
| 1283b | DISC | one routine system check round (e.g. daily check of servers, | 1.51 | terminal_bench_2 | 4104.6 | 0.961 | 1.0 | 0.4996 | 4.6–349.7 |
| 1284b | DISC | one software installation or minor software repair completed | 1.89 | osworld_verified | 170.1 | 0.665 | 0.997 | 0.2887 | 2.3–399.7 |
| 1285a | DISC | one performance alert or problem followed up | 2.39 | itbench_sre | 78.7 | 0.313 | 0.2598 | 0.0116 | 3.8–34.7 |
| 1286b | DISC | one workstation configured and handed over to an employee | 2.36 | terminal_bench_2 | 4104.6 | 0.933 | 1.0 | 0.6245 | 7.2–1097.0 |
| 1287a | DISC | one problem-and-remedy record written up for a ticket | 2.08 | workarena_l1 | 396.3 | 0.94 | 1.0 | 0.3718 | 0.5–133.5 |
| 1287b | DISC | one day's log of transactions and installation activities | 1.39 | workarena_l1 | 396.3 | 0.776 | 0.9999 | 0.3175 | 3.6–454.3 |
| 1288b | DISC | one ticketed problem investigated and resolved | 2.17 | terminal_bench_2 | 4104.6 | 0.961 | 0.9994 | 0.5912 | 3.4–3711.1 |
| 1290a | DISC | one training guide, how-to document, or procedure | 1.32 | gdpval | 4729.4 | 0.897 | 0.9996 | 0.4346 | 13.1–11322.7 |
| 1291a | DISC | one vendor or technician service referral (case or RMA opene | 3.40 | workarena_pp | 157.4 | 0.651 | 0.9778 | 0.2209 | 2.5–165.0 |
| 1292a | DISC | one evaluation with recommendation (product, upgrade, or imp | 3.39 | gdpval | 4729.4 | 0.731 | 0.9998 | 0.3355 | 21.4–55526.9 |
| 1296a | DISC | one program customization delivered (template, macro, config | 2.89 | spreadsheetbench_2 | 145.3 | 0.318 | 0.4287 | 0.0214 | 21.8–318.3 |
| 1297a | DISC | one office automation feasibility study report | 3.17 | gdpval | 4729.4 | 0.314 | 0.9679 | 0.1158 | 114.6–7456.6 |
| 15204a | DISC | one vacancy filled (hiring decision made) | 0.73 | none (no horizon) |  |  |  |  | – |
| 2578a | LIVE | one set of contact notes entered during a call or visit | 1.81 | eva_bench | 143.1 | 0.851 | 0.9911 | 0.4706 | 0.7–39.2 |
| 2578b | DISC | one interaction record completed after a call or visit | 2.72 | workarena_l1 | 396.3 | 0.96 | 0.9686 | 0.15 | 1.3–59.0 |
| 2579a | LIVE | one refund, exchange, or bill adjustment entered during a ca | 2.72 | tau_voice | 126.2 | 0.857 | 0.9798 | 0.4497 | 0.5–33.9 |
| 2579b | DISC | one refund, exchange, or bill adjustment processed from a qu | 1.47 | tau_retail_airline | 447.6 | 0.906 | 0.9998 | 0.3361 | 1.0–197.9 |
| 2580a | DISC | one resolution verified for a customer case | 4.39 | workarena_l1 | 396.3 | 0.931 | 0.9999 | 0.2667 | 0.7–83.2 |
| 2581a | DISC | one written response or notification sent to a customer | 2.32 | gdpval | 4729.4 | 0.984 | 1.0 | 0.3878 | 1.2–320.5 |
| 2581b | LIVE | one outbound callback delivering an answer or result | 1.90 | tau_voice | 126.2 | 0.801 | 0.972 | 0.3798 | 1.1–34.4 |
| 2582a | DISC | one grievance referral ticket | 4.07 | crmarena_pro | 929.9 | 0.947 | 1.0 | 0.454 | 1.3–182.8 |
| 2583a | LIVE | one service charge determined and payment or billing arrange | 4.18 | tau_voice | 126.2 | 0.837 | 0.9843 | 0.4379 | 0.7–34.1 |
| 2584a | LIVE | one account order (contract, address change, or discontinuan | 2.46 | tau_voice | 126.2 | 0.819 | 0.972 | 0.3981 | 0.8–34.2 |
| 2584b | DISC | one account order processed from a written request | 1.64 | tau_retail_airline | 447.6 | 0.906 | 0.9998 | 0.3361 | 1.0–197.9 |
| 2585a | LIVE | one complaint assessed during a call or visit | 1.63 | tau_voice | 126.2 | 0.77 | 0.9115 | 0.2985 | 1.2–34.4 |
| 2585b | DISC | one complaint investigation with a validity finding | 2.00 | crmarena_pro | 929.9 | 0.877 | 0.9997 | 0.4415 | 4.7–801.2 |
| 2587a | LIVE | one coverage question answered during a call | 1.62 | sopbench | 1161.7 | 0.963 | 1.0 | 0.6342 | 1.0–146.3 |
| 2587b | DISC | one coverage determination for a reported loss | 2.43 | tau_banking | 99.5 | 0.521 | 0.2096 | 0.0046 | 8.9–32.1 |
| 2589b | DISC | one return invoice prepared for a disputed shipment | 2.37 | starshell | 163.1 | 0.698 | 0.9858 | 0.2259 | 2.7–101.4 |
| 2591a | DISC | one improvement recommendation submitted | 3.16 | gdpval | 4729.4 | 0.897 | 0.9999 | 0.4552 | 6.3–21163.6 |
| 18565a | LIVE | one information inquiry answered during a call or visit | 1.87 | tau_voice | 126.2 | 0.878 | 0.9976 | 0.5344 | 0.5–34.4 |
| 18565b | LIVE | one order or account cancellation entered during a contact | 1.63 | tau_voice | 126.2 | 0.837 | 0.985 | 0.4389 | 0.7–34.5 |
| 18565c | LIVE | one complaint taken during a call or visit | 1.17 | eva_bench | 143.1 | 0.818 | 0.972 | 0.3978 | 1.0–39.1 |
| 14638a | DISC | one test plan | 1.74 | gdpval | 4729.4 | 0.594 | 0.9921 | 0.2264 | 18.5–5807.4 |
| 14638b | DISC | one feature-level set of test cases or scripts | 2.61 | swt_bench | 452.7 | 0.463 | 0.8485 | 0.1108 | 10.5–1083.4 |
| 14639a | DISC | one system modification tested (one test cycle) | 4.21 | sweeper_bench | 261.6 | 0.352 | 0.495 | 0.0436 | 17.9–1090.4 |
| 14640a | DISC | one test suite for one testing area of a release | 4.52 | swt_bench | 452.7 | 0.274 | 0.7224 | 0.0606 | 20.4–2896.7 |
| 14641a | DISC | one defect report filed in the bug tracker | 4.69 | workarena_l1 | 396.3 | 0.861 | 0.9259 | 0.1774 | 3.4–161.2 |
| 14643a | DISC | one resolved defect verified and closed or reopened | 2.47 | sweeper_bench | 261.6 | 0.775 | 0.8925 | 0.1741 | 3.1–170.3 |
| 14643b | DISC | one defect status report (weekly or per sprint) | 1.65 | finch | 253.0 | 0.629 | 0.9878 | 0.2468 | 4.5–351.2 |
| 14644a | DISC | one known-defects database set up | 0.62 | scuba (no horizon) |  |  |  |  | – |
| 14644b | DISC | one curation pass over the known-defects database | 3.53 | workarena_pp | 157.4 | 0.154 | 0.0 | 0.0 | – |
| 14645a | DISC | one test strategy and schedule for a project or release | 4.00 | gdpval | 4729.4 | 0.557 | 0.9946 | 0.2079 | 27.5–7902.9 |
| 14647a | DISC | one software document reviewed with findings | 3.71 | gdpval | 4729.4 | 0.917 | 0.9979 | 0.4018 | 14.4–8486.5 |
| 14648a | DISC | one test procedure documented | 4.30 | gdpval | 4729.4 | 0.917 | 1.0 | 0.4326 | 6.8–4461.4 |
| 14649a | DISC | one quality standard or set of release-readiness criteria | 4.12 | gdpval | 4729.4 | 0.497 | 0.9526 | 0.1594 | 24.6–6507.0 |
| 14650a | DISC | one set of automated test scripts updated for a product chan | 4.09 | swt_bench | 452.7 | 0.607 | 0.9657 | 0.1774 | 14.7–1371.4 |
| 14651a | DISC | one escalated customer problem investigated | 3.81 | sweeper_bench | 261.6 | 0.262 | 0.2406 | 0.0081 | 17.6–131.2 |
| 14652a | DISC | one testing tool installed or upgraded | 1.49 | terminal_bench_2 | 4104.6 | 0.908 | 0.9997 | 0.5184 | 7.2–21957.8 |
| 14652b | DISC | one test run executed with results recorded | 2.77 | sweeper_bench | 261.6 | 0.635 | 0.91 | 0.1851 | 5.5–1102.8 |
| 14653a | DISC | one written feedback note on a build or feature | 2.56 | gdpval | 4729.4 | 0.952 | 1.0 | 0.4185 | 3.4–2230.7 |
| 14654a | DISC | one monitored performance issue investigated | 3.97 | itbench_sre | 78.7 | 0.154 | 0.0 | 0.0 | – |
| 14655a | DISC | one compatibility test cycle for a build | 3.88 | sweeper_bench | 261.6 | 0.193 | 0.5199 | 0.0362 | 25.4–1277.3 |
| 14656a | DISC | one test environment built to mirror production | 3.45 | terminal_bench_2 | 4104.6 | 0.421 | 0.9083 | 0.1305 | 29.2–6324.8 |
| 14657a | LIVE | one problem diagnosed during a live session with field staff | 1.67 | tau_telecom | 14743.1 | 0.963 | 0.9998 | 0.712 | 2.0–1214.6 |
| 14657b | DISC | one written diagnosis and recommended solution | 1.67 | gdpval | 4729.4 | 0.878 | 0.9976 | 0.2847 | 3.4–842.6 |
| 14658a | DISC | one standards-compliance review of a program with recommenda | 3.70 | none (no horizon) |  |  |  |  | – |
| 14659a | DISC | one automated testing tool or framework component | 3.60 | swe_bench_pro | 302.9 | 0.052 | 0.0 | 0.0 | – |
| 14660a | DISC | one user or third-party test round organized | 1.34 | theagentcompany | 201.2 | 0.196 | 0.6517 | 0.0362 | 22.2–1135.2 |
| 14660b | DISC | one test round results report | 0.83 | gdpval | 4729.4 | 0.861 | 0.9997 | 0.425 | 19.4–14668.2 |
| 14661a | DISC | one defect given an initial root-cause diagnosis | 3.66 | itbench_sre | 78.7 | 0.154 | 0.0 | 0.0 | – |
| 14662a | DISC | one beta-site performance evaluation | 3.33 | sweeper_bench | 261.6 | 0.233 | 0.9115 | 0.077 | 27.1–2062.0 |
| 14663a | DISC | one tool evaluation with recommendation | 3.25 | gdpval | 4729.4 | 0.692 | 0.9979 | 0.2771 | 26.4–66552.4 |
| 14664a | DISC | one historical test results analysis report | 3.29 | finch | 253.0 | 0.293 | 0.8078 | 0.0749 | 13.8–1960.7 |
