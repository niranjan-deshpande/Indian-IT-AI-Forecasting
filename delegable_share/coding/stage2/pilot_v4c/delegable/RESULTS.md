# Delegable shares — pilot_v4c

D̄ = importance-weighted mean of D over items with a horizon (interpersonal, physical and no-deliverable items count as 0). Uncovered = share of weight whose matched benchmark has no horizon (or no match); it is excluded, not filled. S = expected net hours saved by delegating (gain minus review, and minus failure cost for live items), as a share of the item's unassisted hours, over the hours where delegation pays.

Headline measure: S; D alongside. Headline rows: the first two (ρ = 1, and ρ = 0.5 for benchmarks graded by tests or state checks). Other rows vary one setting from the first row.

| Scenario | Computer User Support Specialists | Customer Service Representatives | Software Quality Assurance Analysts and Testers |
|---|---|---|---|
| base | S 20% · D 58% (eq D 56%; unc 1%) | S 33% · D 85% (eq D 85%; unc 0%) | S 15% · D 66% (eq D 65%; unc 6%) |
| base, rho 0.5 (tests/state) | S 8% · D 43% (eq D 41%; unc 1%) | S 10% · D 22% (eq D 24%; unc 0%) | S 11% · D 54% (eq D 54%; unc 6%) |
| beta 0.6 | S 25% · D 63% (eq D 63%; unc 1%) | S 37% · D 88% (eq D 87%; unc 0%) | S 23% · D 82% (eq D 82%; unc 6%) |
| beta 1.0 | S 18% · D 53% (eq D 52%; unc 1%) | S 31% · D 83% (eq D 82%; unc 0%) | S 12% · D 54% (eq D 54%; unc 6%) |
| decompressed spread, both sides | S 10% · D 30% (eq D 29%; unc 1%) | S 14% · D 44% (eq D 44%; unc 0%) | S 3% · D 13% (eq D 13%; unc 6%) |
| decompressed spread, benchmarks only | S 27% · D 61% (eq D 60%; unc 1%) | S 40% · D 87% (eq D 86%; unc 0%) | S 22% · D 73% (eq D 73%; unc 6%) |
| lambda 0.25 | S 21% · D 58% (eq D 57%; unc 1%) | S 39% · D 86% (eq D 86%; unc 0%) | S 15% · D 66% (eq D 65%; unc 6%) |
| lambda 3 | S 19% · D 55% (eq D 54%; unc 1%) | S 22% · D 68% (eq D 68%; unc 0%) | S 15% · D 65% (eq D 65%; unc 6%) |
| fill from 2nd match | S 20% · D 58% (eq D 57%; unc 0%) | S 33% · D 85% (eq D 85%; unc 0%) | S 15% · D 67% (eq D 67%; unc 0%) |
| latest observed H (no date alignment) | S 11% · D 42% (eq D 40%; unc 1%) | S 19% · D 58% (eq D 57%; unc 0%) | S 8% · D 47% (eq D 47%; unc 6%) |
| +12 months (pooled trend) | S 34% · D 65% (eq D 65%; unc 1%) | S 52% · D 90% (eq D 89%; unc 0%) | S 36% · D 90% (eq D 90%; unc 6%) |

## Items (base scenario)

| item | type | work item | w | benchmark | H (min) | π at p50 | D | S | delegated lengths (min) |
|---|---|---|---|---|---|---|---|---|---|
| 1282a | LIVE | one user call, chat, or walk-up question answered | 2.02 | eva_bench | 142.7 | 0.817 | 0.8079 | 0.2883 | 0.5–38.8 |
| 1282b | DISC | one written user question answered (ticket or email) | 1.52 | gdpval | 4551.0 | 0.983 | 0.9986 | 0.435 | 2.1–594.8 |
| 1283a | DISC | one post-install or post-repair verification of a machine or | 2.14 | terminal_bench_1 | 1018.5 | 0.932 | 0.9998 | 0.5119 | 1.5–964.8 |
| 1283b | DISC | one routine system check round (e.g. daily check of servers, | 1.51 | terminal_bench_2 | 3944.5 | 0.96 | 1.0 | 0.4981 | 4.6–349.7 |
| 1284b | DISC | one software installation or minor software repair completed | 1.89 | osworld_verified | 166.6 | 0.662 | 0.9966 | 0.2852 | 2.3–387.4 |
| 1285a | DISC | one performance alert or problem followed up | 2.39 | itbench_sre | 75.6 | 0.306 | 0.2403 | 0.0101 | 3.9–32.4 |
| 1286b | DISC | one workstation configured and handed over to an employee | 2.36 | terminal_bench_2 | 3944.5 | 0.93 | 1.0 | 0.6219 | 7.2–1097.0 |
| 1287a | DISC | one problem-and-remedy record written up for a ticket | 2.08 | workarena_l1 | 372.2 | 0.937 | 1.0 | 0.3677 | 0.5–133.5 |
| 1287b | DISC | one day's log of transactions and installation activities | 1.39 | workarena_l1 | 372.2 | 0.767 | 0.9999 | 0.3096 | 3.6–426.7 |
| 1288b | DISC | one ticketed problem investigated and resolved | 2.17 | terminal_bench_2 | 3944.5 | 0.96 | 0.9994 | 0.5886 | 3.4–3711.1 |
| 1290a | DISC | one training guide, how-to document, or procedure | 1.32 | gdpval | 4551.0 | 0.894 | 0.9996 | 0.4308 | 13.1–11322.7 |
| 1291a | DISC | one vendor or technician service referral (case or RMA opene | 3.40 | workarena_pp | 144.2 | 0.634 | 0.9693 | 0.2063 | 2.5–149.6 |
| 1292a | DISC | one evaluation with recommendation (product, upgrade, or imp | 3.39 | gdpval | 4551.0 | 0.724 | 0.9997 | 0.3303 | 21.4–53229.2 |
| 1296a | DISC | one program customization delivered (template, macro, config | 2.89 | spreadsheetbench_2 | 137.8 | 0.309 | 0.397 | 0.0185 | 22.7–291.9 |
| 1297a | DISC | one office automation feasibility study report | 3.17 | gdpval | 4551.0 | 0.307 | 0.9649 | 0.1117 | 114.6–7246.4 |
| 15204a | DISC | one vacancy filled (hiring decision made) | 0.73 | none (no horizon) |  |  |  |  | – |
| 2578a | LIVE | one set of contact notes entered during a call or visit | 1.81 | eva_bench | 142.7 | 0.851 | 0.9911 | 0.4699 | 0.7–39.2 |
| 2578b | DISC | one interaction record completed after a call or visit | 2.72 | workarena_l1 | 372.2 | 0.958 | 0.968 | 0.1467 | 1.3–55.3 |
| 2579a | LIVE | one refund, exchange, or bill adjustment entered during a ca | 2.72 | tau_voice | 125.8 | 0.857 | 0.9789 | 0.449 | 0.5–33.5 |
| 2579b | DISC | one refund, exchange, or bill adjustment processed from a qu | 1.47 | tau_retail_airline | 425.3 | 0.903 | 0.9997 | 0.3314 | 1.0–189.6 |
| 2580a | DISC | one resolution verified for a customer case | 4.39 | workarena_l1 | 372.2 | 0.927 | 0.9998 | 0.2624 | 0.7–78.2 |
| 2581a | DISC | one written response or notification sent to a customer | 2.32 | gdpval | 4551.0 | 0.983 | 1.0 | 0.3871 | 1.2–320.5 |
| 2581b | LIVE | one outbound callback delivering an answer or result | 1.90 | tau_voice | 125.8 | 0.801 | 0.972 | 0.379 | 1.1–34.4 |
| 2582a | DISC | one grievance referral ticket | 4.07 | crmarena_pro | 829.8 | 0.942 | 1.0 | 0.4476 | 1.3–182.8 |
| 2583a | LIVE | one service charge determined and payment or billing arrange | 4.18 | tau_voice | 125.8 | 0.837 | 0.9843 | 0.4371 | 0.7–34.1 |
| 2584a | LIVE | one account order (contract, address change, or discontinuan | 2.46 | tau_voice | 125.8 | 0.818 | 0.972 | 0.3973 | 0.8–34.2 |
| 2584b | DISC | one account order processed from a written request | 1.64 | tau_retail_airline | 425.3 | 0.903 | 0.9997 | 0.3314 | 1.0–189.6 |
| 2585a | LIVE | one complaint assessed during a call or visit | 1.63 | tau_voice | 125.8 | 0.769 | 0.9115 | 0.2977 | 1.2–34.4 |
| 2585b | DISC | one complaint investigation with a validity finding | 2.00 | crmarena_pro | 829.8 | 0.866 | 0.9996 | 0.4289 | 4.7–801.2 |
| 2587a | LIVE | one coverage question answered during a call | 1.62 | sopbench | 1041.1 | 0.96 | 1.0 | 0.6253 | 1.0–146.3 |
| 2587b | DISC | one coverage determination for a reported loss | 2.43 | tau_banking | 99.4 | 0.521 | 0.2096 | 0.0046 | 8.9–32.1 |
| 2589b | DISC | one return invoice prepared for a disputed shipment | 2.37 | starshell | 154.6 | 0.689 | 0.9817 | 0.2173 | 2.7–95.6 |
| 2591a | DISC | one improvement recommendation submitted | 3.16 | gdpval | 4551.0 | 0.894 | 0.9999 | 0.4511 | 6.3–20267.4 |
| 18565a | LIVE | one information inquiry answered during a call or visit | 1.87 | tau_voice | 125.8 | 0.878 | 0.9974 | 0.5337 | 0.5–34.0 |
| 18565b | LIVE | one order or account cancellation entered during a contact | 1.63 | tau_voice | 125.8 | 0.837 | 0.985 | 0.4382 | 0.7–34.5 |
| 18565c | LIVE | one complaint taken during a call or visit | 1.17 | eva_bench | 142.7 | 0.817 | 0.972 | 0.397 | 1.0–39.1 |
| 14638a | DISC | one test plan | 1.74 | gdpval | 4551.0 | 0.587 | 0.9911 | 0.2211 | 18.5–5602.4 |
| 14638b | DISC | one feature-level set of test cases or scripts | 2.61 | swt_bench | 449.0 | 0.461 | 0.8485 | 0.1099 | 10.5–1083.4 |
| 14639a | DISC | one system modification tested (one test cycle) | 4.21 | sweeper_bench | 257.2 | 0.349 | 0.4869 | 0.0425 | 18.4–1061.3 |
| 14640a | DISC | one test suite for one testing area of a release | 4.52 | swt_bench | 449.0 | 0.273 | 0.7224 | 0.06 | 20.4–2896.7 |
| 14641a | DISC | one defect report filed in the bug tracker | 4.69 | workarena_l1 | 372.2 | 0.855 | 0.9148 | 0.1696 | 3.4–149.2 |
| 14643a | DISC | one resolved defect verified and closed or reopened | 2.47 | sweeper_bench | 257.2 | 0.773 | 0.8888 | 0.1717 | 3.1–167.1 |
| 14643b | DISC | one defect status report (weekly or per sprint) | 1.65 | finch | 236.6 | 0.616 | 0.9843 | 0.2354 | 4.5–327.4 |
| 14644a | DISC | one known-defects database set up | 0.62 | scuba (no horizon) |  |  |  |  | – |
| 14644b | DISC | one curation pass over the known-defects database | 3.53 | workarena_pp | 144.2 | 0.144 | 0.0 | 0.0 | – |
| 14645a | DISC | one test strategy and schedule for a project or release | 4.00 | gdpval | 4551.0 | 0.549 | 0.9939 | 0.2027 | 27.5–7623.9 |
| 14647a | DISC | one software document reviewed with findings | 3.71 | gdpval | 4551.0 | 0.915 | 0.9979 | 0.3984 | 14.4–8163.7 |
| 14648a | DISC | one test procedure documented | 4.30 | gdpval | 4551.0 | 0.915 | 1.0 | 0.4296 | 6.8–4461.4 |
| 14649a | DISC | one quality standard or set of release-readiness criteria | 4.12 | gdpval | 4551.0 | 0.489 | 0.9485 | 0.1548 | 24.6–6255.5 |
| 14650a | DISC | one set of automated test scripts updated for a product chan | 4.09 | swt_bench | 449.0 | 0.605 | 0.9643 | 0.1762 | 14.7–1345.1 |
| 14651a | DISC | one escalated customer problem investigated | 3.81 | sweeper_bench | 257.2 | 0.259 | 0.2282 | 0.0075 | 17.6–125.7 |
| 14652a | DISC | one testing tool installed or upgraded | 1.49 | terminal_bench_2 | 3944.5 | 0.905 | 0.9997 | 0.5141 | 7.2–21957.8 |
| 14652b | DISC | one test run executed with results recorded | 2.77 | sweeper_bench | 257.2 | 0.632 | 0.9067 | 0.1828 | 5.5–1075.8 |
| 14653a | DISC | one written feedback note on a build or feature | 2.56 | gdpval | 4551.0 | 0.95 | 1.0 | 0.4165 | 3.4–2230.7 |
| 14654a | DISC | one monitored performance issue investigated | 3.97 | itbench_sre | 75.6 | 0.149 | 0.0 | 0.0 | – |
| 14655a | DISC | one compatibility test cycle for a build | 3.88 | sweeper_bench | 257.2 | 0.19 | 0.512 | 0.0353 | 25.4–1252.7 |
| 14656a | DISC | one test environment built to mirror production | 3.45 | terminal_bench_2 | 3944.5 | 0.413 | 0.9015 | 0.1261 | 29.2–6074.2 |
| 14657a | LIVE | one problem diagnosed during a live session with field staff | 1.67 | tau_telecom | 13944.6 | 0.962 | 0.9997 | 0.7057 | 2.0–1134.1 |
| 14657b | DISC | one written diagnosis and recommended solution | 1.67 | gdpval | 4551.0 | 0.875 | 0.9972 | 0.2809 | 3.4–815.7 |
| 14658a | DISC | one standards-compliance review of a program with recommenda | 3.70 | none (no horizon) |  |  |  |  | – |
| 14659a | DISC | one automated testing tool or framework component | 3.60 | swe_bench_pro | 295.8 | 0.051 | 0.0 | 0.0 | – |
| 14660a | DISC | one user or third-party test round organized | 1.34 | theagentcompany (no horizon) |  |  |  |  | – |
| 14660b | DISC | one test round results report | 0.83 | gdpval | 4551.0 | 0.857 | 0.9997 | 0.4207 | 19.4–14668.2 |
| 14661a | DISC | one defect given an initial root-cause diagnosis | 3.66 | itbench_sre | 75.6 | 0.149 | 0.0 | 0.0 | – |
| 14662a | DISC | one beta-site performance evaluation | 3.33 | sweeper_bench | 257.2 | 0.231 | 0.9083 | 0.0754 | 27.1–2028.8 |
| 14663a | DISC | one tool evaluation with recommendation | 3.25 | gdpval | 4551.0 | 0.685 | 0.9977 | 0.2722 | 26.4–63512.6 |
| 14664a | DISC | one historical test results analysis report | 3.29 | finch | 236.6 | 0.282 | 0.7852 | 0.0693 | 14.1–1798.2 |
