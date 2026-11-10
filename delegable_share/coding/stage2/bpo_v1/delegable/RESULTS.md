# Delegable shares — bpo_v1

D̄ = importance-weighted mean of D over items with a horizon (interpersonal, physical and no-deliverable items count as 0). Uncovered = share of weight whose matched benchmark has no horizon (or no match); it is excluded, not filled. S = expected net hours saved by delegating (gain minus review, and minus failure cost for live items), as a share of the item's unassisted hours, over the hours where delegation pays.

Headline measure: S; D alongside. Headline rows: the first two (ρ = 1, and ρ = 0.5 for benchmarks graded by tests or state checks). Other rows vary one setting from the first row.

| Scenario | Billing and Posting Clerks | Bookkeeping, Accounting, and Auditing Clerks | Computer Systems Analysts | Data Entry Keyers | Database Administrators | Insurance Claims and Policy Processing Clerks | Medical Records Specialists | Network and Computer Systems Administrators | Software Developers | Web Developers |
|---|---|---|---|---|---|---|---|---|---|---|
| base | S 14% · D 57% (eq D 56%; unc 10%) | S 9% · D 34% (eq D 35%; unc 4%) | S 13% · D 55% (eq D 55%; unc 3%) | S 6% · D 33% (eq D 31%; unc 39%) | S 14% · D 52% (eq D 51%; unc 11%) | S 24% · D 73% (eq D 75%; unc 5%) | S 11% · D 38% (eq D 39%; unc 0%) | S 19% · D 66% (eq D 65%; unc 0%) | S 12% · D 41% (eq D 40%; unc 0%) | S 28% · D 81% (eq D 82%; unc 4%) |
| base, rho 0.5 (tests/state) | S 6% · D 38% (eq D 37%; unc 10%) | S 5% · D 23% (eq D 23%; unc 4%) | S 10% · D 46% (eq D 47%; unc 3%) | S 0% · D 9% (eq D 8%; unc 39%) | S 11% · D 41% (eq D 42%; unc 11%) | S 10% · D 41% (eq D 43%; unc 5%) | S 5% · D 12% (eq D 13%; unc 0%) | S 8% · D 44% (eq D 44%; unc 0%) | S 11% · D 36% (eq D 36%; unc 0%) | S 20% · D 78% (eq D 78%; unc 4%) |
| beta 0.6 | S 21% · D 71% (eq D 70%; unc 10%) | S 13% · D 44% (eq D 45%; unc 4%) | S 22% · D 70% (eq D 70%; unc 3%) | S 13% · D 40% (eq D 37%; unc 39%) | S 22% · D 67% (eq D 66%; unc 11%) | S 30% · D 91% (eq D 91%; unc 5%) | S 14% · D 61% (eq D 61%; unc 0%) | S 28% · D 78% (eq D 78%; unc 0%) | S 18% · D 58% (eq D 57%; unc 0%) | S 36% · D 84% (eq D 85%; unc 4%) |
| beta 1.0 | S 12% · D 46% (eq D 45%; unc 10%) | S 8% · D 28% (eq D 28%; unc 4%) | S 9% · D 44% (eq D 45%; unc 3%) | S 4% · D 25% (eq D 23%; unc 39%) | S 11% · D 41% (eq D 41%; unc 11%) | S 22% · D 64% (eq D 66%; unc 5%) | S 10% · D 32% (eq D 33%; unc 0%) | S 16% · D 57% (eq D 57%; unc 0%) | S 10% · D 36% (eq D 35%; unc 0%) | S 24% · D 77% (eq D 77%; unc 4%) |
| decompressed spread, both sides | S 3% · D 11% (eq D 12%; unc 10%) | S 3% · D 9% (eq D 10%; unc 4%) | S 1% · D 5% (eq D 6%; unc 3%) | S 1% · D 6% (eq D 6%; unc 39%) | S 2% · D 8% (eq D 8%; unc 11%) | S 10% · D 37% (eq D 38%; unc 5%) | S 4% · D 12% (eq D 13%; unc 0%) | S 4% · D 16% (eq D 16%; unc 0%) | S 1% · D 6% (eq D 6%; unc 0%) | S 4% · D 18% (eq D 19%; unc 4%) |
| decompressed spread, benchmarks only | S 20% · D 63% (eq D 61%; unc 10%) | S 13% · D 38% (eq D 39%; unc 4%) | S 22% · D 64% (eq D 63%; unc 3%) | S 18% · D 40% (eq D 37%; unc 39%) | S 21% · D 58% (eq D 57%; unc 11%) | S 34% · D 89% (eq D 89%; unc 5%) | S 16% · D 60% (eq D 61%; unc 0%) | S 30% · D 75% (eq D 74%; unc 0%) | S 18% · D 48% (eq D 47%; unc 0%) | S 38% · D 84% (eq D 85%; unc 4%) |
| lambda 0.25 | S 16% · D 57% (eq D 56%; unc 10%) | S 9% · D 34% (eq D 35%; unc 4%) | S 13% · D 56% (eq D 56%; unc 3%) | S 6% · D 33% (eq D 31%; unc 39%) | S 15% · D 52% (eq D 52%; unc 11%) | S 26% · D 74% (eq D 76%; unc 5%) | S 11% · D 38% (eq D 39%; unc 0%) | S 20% · D 67% (eq D 67%; unc 0%) | S 12% · D 41% (eq D 40%; unc 0%) | S 28% · D 81% (eq D 82%; unc 4%) |
| lambda 3 | S 12% · D 54% (eq D 53%; unc 10%) | S 8% · D 34% (eq D 34%; unc 4%) | S 12% · D 54% (eq D 55%; unc 3%) | S 6% · D 33% (eq D 31%; unc 39%) | S 14% · D 51% (eq D 50%; unc 11%) | S 20% · D 66% (eq D 67%; unc 5%) | S 10% · D 38% (eq D 39%; unc 0%) | S 19% · D 64% (eq D 64%; unc 0%) | S 12% · D 41% (eq D 40%; unc 0%) | S 28% · D 81% (eq D 82%; unc 4%) |
| fill from 2nd match | S 16% · D 61% (eq D 61%; unc 0%) | S 9% · D 34% (eq D 35%; unc 4%) | S 13% · D 57% (eq D 57%; unc 0%) | S 17% · D 54% (eq D 53%; unc 12%) | S 13% · D 49% (eq D 48%; unc 0%) | S 24% · D 74% (eq D 76%; unc 0%) | S 11% · D 38% (eq D 39%; unc 0%) | S 19% · D 66% (eq D 65%; unc 0%) | S 12% · D 41% (eq D 40%; unc 0%) | S 28% · D 81% (eq D 82%; unc 4%) |
| latest observed H (no date alignment) | S 8% · D 36% (eq D 35%; unc 10%) | S 5% · D 17% (eq D 17%; unc 4%) | S 5% · D 36% (eq D 37%; unc 3%) | S 0% · D 0% (eq D 0%; unc 39%) | S 7% · D 36% (eq D 35%; unc 11%) | S 12% · D 34% (eq D 37%; unc 5%) | S 6% · D 13% (eq D 15%; unc 0%) | S 9% · D 38% (eq D 38%; unc 0%) | S 5% · D 30% (eq D 29%; unc 0%) | S 11% · D 57% (eq D 58%; unc 4%) |
| +12 months (pooled trend) | S 36% · D 82% (eq D 80%; unc 10%) | S 27% · D 83% (eq D 84%; unc 4%) | S 31% · D 74% (eq D 73%; unc 3%) | S 19% · D 40% (eq D 37%; unc 39%) | S 30% · D 72% (eq D 70%; unc 11%) | S 45% · D 99% (eq D 99%; unc 5%) | S 31% · D 83% (eq D 83%; unc 0%) | S 39% · D 85% (eq D 84%; unc 0%) | S 25% · D 63% (eq D 62%; unc 0%) | S 47% · D 89% (eq D 89%; unc 4%) |

## Items (base scenario)

| item | type | work item | w | benchmark | H (min) | π at p50 | D | S | delegated lengths (min) |
|---|---|---|---|---|---|---|---|---|---|
| 21661a | DISC | one system recommendation with installation plan | 3.61 | gdpval | 4551.0 | 0.685 | 0.9921 | 0.2633 | 21.9–38874.8 |
| 21662a | DISC | one feasibility assessment of a proposed design | 4.08 | gdpval | 4551.0 | 0.825 | 0.9997 | 0.3888 | 13.5–31266.5 |
| 21665b | DISC | one technical question answered in writing | 1.35 | theagentcompany | 186.2 | 0.401 | 0.3326 | 0.019 | 3.9–50.1 |
| 21666a | DISC | one software system installation coordinated | 3.75 | theagentcompany | 186.2 | 0.061 | 0.1249 | 0.0018 | 30.0–485.0 |
| 21667a | DISC | one feature or module designed and implemented | 3.56 | swe_bench_pro | 295.8 | 0.051 | 0.0985 | 0.0019 | 35.1–823.5 |
| 21668a | DISC | one set of system performance standards | 3.53 | gdpval | 4551.0 | 0.631 | 0.9582 | 0.203 | 10.7–4970.9 |
| 21669a | DISC | one software test or validation procedure | 1.17 | swt_bench | 449.0 | 0.546 | 0.6731 | 0.0838 | 10.9–786.7 |
| 21669b | DISC | one software code change | 1.17 | swe_bench_pro | 295.8 | 0.18 | 0.0595 | 0.0008 | 39.1–160.2 |
| 21669c | DISC | one software documentation document or update | 0.78 | gdpval | 4551.0 | 0.894 | 0.9933 | 0.3534 | 11.7–8738.9 |
| 21670a | DISC | one change request or bug fix to existing software | 3.74 | swe_bench_pro | 295.8 | 0.147 | 0.1385 | 0.0026 | 40.9–346.8 |
| 21671a | DISC | one system or equipment monitoring exception assessed | 4.12 | itbench_sre | 75.6 | 0.198 | 0.0235 | 0.0002 | 7.4–17.2 |
| 21672a | DISC | one hardware configuration recommendation | 3.07 | gdpval | 4551.0 | 0.825 | 0.9978 | 0.3609 | 10.4–16695.6 |
| 21673a | DISC | one project report | 2.21 | gdpval | 4551.0 | 0.938 | 1.0 | 0.5036 | 4.1–3859.3 |
| 21673b | DISC | one piece of project correspondence | 1.47 | theagentcompany | 186.2 | 0.767 | 0.9808 | 0.2644 | 0.8–282.9 |
| 21676a | DISC | one data analysis of system capabilities or requirements | 3.59 | spider2 | 9828.3 | 0.766 | 0.9849 | 0.2962 | 15.4–8001.0 |
| 14694a | DISC | one website or feature design | 1.10 | gdpval | 4551.0 | 0.77 | 0.9707 | 0.2644 | 10.4–25380.1 |
| 14694b | DISC | one implemented website feature or component | 1.99 | swe_lancer | 3368.8 | 0.785 | 0.9972 | 0.352 | 10.8–23684.5 |
| 14694c | DISC | one website maintenance change | 2.26 | swe_lancer | 3368.8 | 0.921 | 0.9977 | 0.4471 | 6.0–11234.3 |
| 14698a | DISC | one website file backup completed | 4.35 | terminal_bench_1 | 1018.5 | 0.932 | 0.9983 | 0.389 | 2.1–959.8 |
| 14700a | DISC | one code change evaluated | 4.09 | sweeper_bench | 257.2 | 0.707 | 0.5201 | 0.0421 | 9.6–117.1 |
| 14702a | DISC | one set of technical requirements | 3.79 | gdpval | 4551.0 | 0.825 | 0.9978 | 0.3609 | 10.4–16695.6 |
| 14704a | DISC | one database or schema built or changed | 4.05 | spider2 | 9828.3 | 0.699 | 0.8906 | 0.1954 | 16.8–11662.0 |
| 14705a | DISC | one domain renewal | 3.67 | online_mind2web (no horizon) |  |  |  |  | – |
| 14706b | DISC | one e-commerce feature integrated | 1.77 | swe_lancer | 3368.8 | 0.671 | 0.972 | 0.2487 | 17.5–17336.4 |
| 14707a | DISC | one supporting code change | 4.58 | swe_lancer | 3368.8 | 0.785 | 0.9967 | 0.3436 | 13.6–25688.7 |
| 14708a | DISC | one hosting or network issue resolved | 3.57 | theagentcompany | 186.2 | 0.507 | 0.7792 | 0.1031 | 3.9–504.2 |
| 14710a | DISC | one website test run | 4.04 | sweeper_bench | 257.2 | 0.49 | 0.8907 | 0.1528 | 4.8–751.8 |
| 14711a | DISC | one tool or language selection | 4.17 | gdpval | 4551.0 | 0.894 | 0.999 | 0.4068 | 8.6–11548.0 |
| 14713a | DISC | one user email inquiry answered | 2.57 | gdpval | 4551.0 | 0.983 | 0.9971 | 0.4512 | 2.4–771.9 |
| 14713b | DISC | one automated response set up | 1.10 | terminal_bench_2 | 3944.5 | 0.93 | 0.9999 | 0.5625 | 4.3–7422.2 |
| 14714a | DISC | one website revision procedure | 3.29 | gdpval | 4551.0 | 0.724 | 0.9993 | 0.3405 | 25.4–26814.1 |
| 14717a | DISC | one server directory structure established | 3.47 | terminal_bench_1 | 1018.5 | 0.845 | 0.9996 | 0.3599 | 4.7–1348.9 |
| 14719a | DISC | one performance improvement recommendation | 1.02 | gdpval | 4551.0 | 0.796 | 0.9959 | 0.321 | 7.5–5153.1 |
| 14719b | DISC | one performance improvement implemented | 2.37 | swe_lancer | 3368.8 | 0.867 | 0.9893 | 0.3535 | 9.1–6917.3 |
| 14722a | DISC | one website specification document | 3.18 | gdpval | 4551.0 | 0.724 | 0.9865 | 0.2699 | 20.9–16709.6 |
| 14723a | DISC | one security log review | 2.98 | itbench_sre | 75.6 | 0.463 | 0.0 | 0.0 | – |
| 14723b | DISC | one security problem escalated | 0.75 | itbench_sre | 75.6 | 0.607 | 0.5199 | 0.0492 | 1.0–32.4 |
| 14724a | DISC | one web model or prototype | 3.19 | swe_lancer | 3368.8 | 0.722 | 0.9629 | 0.2363 | 25.8–24867.2 |
| 14725a | DISC | one server hardware or software recommendation | 3.11 | gdpval | 4551.0 | 0.825 | 0.9997 | 0.3888 | 13.5–31266.5 |
| 14726a | DISC | one test plan or procedure | 1.77 | gdpval | 4551.0 | 0.894 | 0.9995 | 0.4335 | 7.2–23326.1 |
| 14726b | DISC | one test results record | 1.77 | gdpval | 4551.0 | 0.964 | 1.0 | 0.5094 | 1.6–3711.1 |
| 14727a | DISC | one architecture or technology comparison | 2.75 | gdpval | 4551.0 | 0.724 | 0.9976 | 0.3188 | 25.4–18550.9 |
| 14728a | DISC | one technical factors report | 3.35 | gdpval | 4551.0 | 0.796 | 0.9971 | 0.3296 | 4.8–3281.7 |
| 14729a | DISC | one HTTP server installed and configured | 2.94 | terminal_bench_2 | 3944.5 | 0.842 | 1.0 | 0.4523 | 11.1–14668.2 |
| 14730a | DISC | one set of interaction or sequence diagrams | 2.73 | gdpval | 4551.0 | 0.915 | 0.9997 | 0.5422 | 9.9–7334.1 |
| 1317a | DISC | one backup job run and verified | 3.04 | terminal_bench_2 | 3944.5 | 0.977 | 1.0 | 0.4017 | 1.0–964.8 |
| 1317b | DISC | one restore or recovery operation | 1.30 | terminal_bench_2 | 3944.5 | 0.829 | 0.9544 | 0.2992 | 7.8–3719.6 |
| 1318a | DISC | one maintenance change implemented | 2.45 | terminal_bench_2 | 3944.5 | 0.829 | 0.9772 | 0.2971 | 5.8–2041.4 |
| 1318b | DISC | one administration request handled | 1.63 | workarena_pp | 144.2 | 0.676 | 0.8172 | 0.1616 | 2.4–284.0 |
| 1319a | DISC | one security measure planned and implemented | 4.56 | terminal_bench_2 | 3944.5 | 0.519 | 0.8382 | 0.1105 | 31.1–11706.6 |
| 1320a | DISC | one console alert handled | 2.24 | itbench_sre | 75.6 | 0.306 | 0.0 | 0.0 | – |
| 1320b | DISC | one access request coordinated | 1.49 | workarena_pp | 144.2 | 0.789 | 0.911 | 0.2096 | 1.1–107.6 |
| 1321a | DISC | one startup or shutdown procedure with record | 3.35 | terminal_bench_1 | 1018.5 | 0.736 | 0.9843 | 0.282 | 2.0–391.7 |
| 1322a | DISC | one tested network or operating system configuration | 2.44 | terminal_bench_2 | 3944.5 | 0.659 | 0.7612 | 0.1427 | 5.9–1994.8 |
| 1323a | DISC | one improvement recommendation | 3.32 | gdpval | 4551.0 | 0.825 | 0.9978 | 0.3609 | 10.4–16695.6 |
| 1324a | LIVE | one live conversation about a system problem | 1.57 | eva_bench | 142.7 | 0.725 | 0.6443 | 0.1735 | 1.1–38.8 |
| 1324b | DISC | one written follow-up on a system problem | 1.90 | workarena_pp | 144.2 | 0.762 | 0.9582 | 0.1622 | 1.2–65.1 |
| 1325a | DISC | one performance alert investigated | 1.78 | itbench_sre | 75.6 | 0.183 | 0.0 | 0.0 | – |
| 1325b | DISC | one periodic performance report | 1.78 | finch | 236.6 | 0.154 | 0.2578 | 0.0141 | 13.5–203.5 |
| 1327b | DISC | one software installation | 1.67 | terminal_bench_2 | 3944.5 | 0.965 | 1.0 | 0.5226 | 1.7–1608.0 |
| 1328a | DISC | one system requirements assessment | 3.29 | gdpval | 4551.0 | 0.489 | 0.9441 | 0.154 | 21.4–7781.0 |
| 1329a | DISC | one repair-or-replace assessment | 3.28 | gdpval | 4551.0 | 0.915 | 1.0 | 0.5792 | 5.5–7334.1 |
| 1330a | DISC | one network function log update | 1.82 | workarena_l1 | 372.2 | 0.855 | 0.992 | 0.3399 | 1.9–408.9 |
| 1330b | DISC | one maintenance or repair record | 1.82 | workarena_l1 | 372.2 | 0.954 | 1.0 | 0.3924 | 0.7–542.3 |
| 1332b | DISC | one inventory update | 2.06 | ui_cube | 55.0 | 0.749 | 0.7848 | 0.1448 | 1.4–104.4 |
| 1333a | DISC | one purchase coordinated | 3.32 | theagentcompany | 186.2 | 0.423 | 0.8389 | 0.1193 | 5.5–486.5 |
| 15205b | DISC | one system or network incident diagnosed and resolved or esc | 2.06 | itbench_sre | 75.6 | 0.149 | 0.0 | 0.0 | – |
| 15206a | DISC | one email or antivirus configuration change | 1.57 | terminal_bench_2 | 3944.5 | 0.96 | 0.999 | 0.5613 | 3.3–8128.9 |
| 15206b | DISC | one email or virus alert investigated | 2.35 | itbench_sre | 75.6 | 0.463 | 0.2911 | 0.0321 | 1.6–44.6 |
| 15207b | DISC | one new technology implementation recommendation | 0.91 | gdpval | 4551.0 | 0.724 | 0.9979 | 0.2944 | 23.8–53241.9 |
| 15207c | DISC | one new technology deployment or implementation change | 1.22 | terminal_bench_4 | 762.8 | 0.176 | 0.1867 | 0.0088 | 22.7–657.2 |
| 15208a | DISC | one voice service implementation or configuration change | 1.03 | terminal_bench_2 | 3944.5 | 0.731 | 0.983 | 0.297 | 10.9–3831.1 |
| 15208c | LIVE | one live voice service support contact | 0.59 | eva_bench | 142.7 | 0.725 | 0.6064 | 0.1628 | 1.0–39.1 |
| 15208d | DISC | one voice service support issue handled | 0.73 | workarena_pp | 144.2 | 0.298 | 0.2774 | 0.0202 | 2.8–72.5 |
| 1298a | DISC | one standard or guideline document | 3.43 | gdpval | 4551.0 | 0.489 | 0.9082 | 0.1326 | 27.6–5912.0 |
| 1299a | DISC | one database or DBMS change implemented | 2.80 | dba_bench | 52.3 | 0.067 | 0.0 | 0.0 | – |
| 1300a | DISC | one test round with fixes | 3.68 | swe_bench_pro | 295.8 | 0.236 | 0.3002 | 0.0103 | 22.8–293.0 |
| 1301a | DISC | one security measures plan | 1.57 | gdpval | 4551.0 | 0.489 | 0.8485 | 0.1293 | 20.4–4662.4 |
| 1301b | DISC | one security measure implemented | 2.36 | terminal_bench_2 | 3944.5 | 0.776 | 0.9483 | 0.2579 | 5.2–3121.0 |
| 1302a | DISC | one installation and testing plan with approval | 2.07 | gdpval | 4551.0 | 0.685 | 0.9767 | 0.2433 | 11.1–2389.3 |
| 1303b | LIVE | one user question answered during a live contact | 1.31 | eva_bench | 142.7 | 0.851 | 0.7853 | 0.2676 | 0.3–34.2 |
| 1303c | DISC | one written user question answered | 1.48 | spider2 | 9828.3 | 0.989 | 0.9969 | 0.5147 | 2.5–4868.1 |
| 1305a | DISC | one access specification or change | 3.80 | scuba (no horizon) |  |  |  |  | – |
| 1306a | DISC | one data model | 3.14 | spider2 | 9828.3 | 0.766 | 0.9468 | 0.2331 | 31.0–6248.9 |
| 1311a | DISC | one performance monitoring setup | 1.56 | dba_bench | 52.3 | 0.201 | 0.2089 | 0.0089 | 6.3–104.0 |
| 1311b | DISC | one production database created | 1.56 | terminal_bench_2 | 3944.5 | 0.905 | 0.9997 | 0.4411 | 7.3–7127.6 |
| 1312b | DISC | one trend briefing | 1.41 | gdpval | 4551.0 | 0.857 | 1.0 | 0.4833 | 13.5–8922.7 |
| 1313a | DISC | one coded set of database definitions | 2.21 | spider2 | 9828.3 | 0.953 | 0.9998 | 0.5042 | 3.5–16249.6 |
| 1315a | DISC | one data dictionary update | 2.70 | none (no horizon) |  |  |  |  | – |
| 21648a | DISC | one technology recommendation | 3.05 | gdpval | 4551.0 | 0.77 | 0.9963 | 0.3136 | 24.7–21063.3 |
| 21649a | DISC | one DBMS upgrade planned and installed | 3.86 | terminal_bench_4 | 762.8 | 0.106 | 0.3336 | 0.0143 | 49.2–1643.2 |
| 21651a | DISC | one change tested | 3.76 | swt_bench | 449.0 | 0.358 | 0.3991 | 0.0272 | 12.4–303.3 |
| 3464a | LIVE | one user problem fixed during a live contact | 1.62 | eva_bench | 142.7 | 0.725 | 0.6064 | 0.1628 | 1.0–39.1 |
| 3464b | DISC | one support ticket resolved | 2.43 | workarena_pp | 144.2 | 0.634 | 0.6255 | 0.0946 | 4.3–276.2 |
| 3465a | DISC | one program or system test cycle completed | 1.20 | swt_bench | 449.0 | 0.402 | 0.6878 | 0.0807 | 15.4–1299.9 |
| 3465b | DISC | one program or system maintenance change | 1.40 | terminal_bench_2 | 3944.5 | 0.776 | 0.9011 | 0.2191 | 6.7–2047.4 |
| 3465c | DISC | one monitoring alert or exception investigated | 0.80 | itbench_sre | 75.6 | 0.239 | 0.0 | 0.0 | – |
| 3465d | DISC | one installation or rollout coordinated | 0.60 | theagentcompany | 186.2 | 0.105 | 0.2324 | 0.0058 | 18.1–396.2 |
| 3466a | DISC | one program, module or feature coded | 3.71 | swe_bench_pro | 295.8 | 0.321 | 0.512 | 0.0465 | 9.2–963.0 |
| 3468a | DISC | one system-to-system integration or interface | 3.78 | terminal_bench_4 | 762.8 | 0.052 | 0.012 | 0.0001 | 153.7–670.4 |
| 3470a | DISC | one system enhancement delivered | 3.47 | swe_bench_pro | 295.8 | 0.043 | 0.0474 | 0.0008 | 38.2–704.4 |
| 3471a | DISC | one work-process investigation and its findings | 3.44 | gdpval | 4551.0 | 0.405 | 0.937 | 0.1329 | 44.4–6322.1 |
| 3472a | DISC | one set of hardware/software requirements for a system | 3.33 | gdpval | 4551.0 | 0.857 | 0.9972 | 0.368 | 8.8–8131.6 |
| 3474a | DISC | one system design | 3.60 | gdpval | 4551.0 | 0.24 | 0.4483 | 0.0323 | 92.3–4140.8 |
| 3475a | DISC | one package evaluation | 1.34 | gdpval | 4551.0 | 0.489 | 0.9755 | 0.1528 | 27.4–18595.8 |
| 3475b | DISC | one package configured for the user environment | 2.00 | terminal_bench_2 | 3944.5 | 0.333 | 0.5987 | 0.0552 | 23.9–10088.7 |
| 3476a | DISC | one system goals statement | 1.08 | gdpval | 4551.0 | 0.894 | 0.9994 | 0.392 | 10.5–7678.0 |
| 3476b | DISC | one program logic diagram or diagram set | 2.00 | none (no horizon) |  |  |  |  | – |
| 3477a | DISC | one procedure or standard written or revised | 3.21 | gdpval | 4551.0 | 0.77 | 0.9998 | 0.36 | 19.1–26382.6 |
| 3478a | DISC | one code defect located and corrected | 3.60 | swe_bench_verified | 4774.7 | 0.726 | 0.9199 | 0.2091 | 14.9–3959.8 |
| 3479a | DISC | one recommendation memo | 3.11 | gdpval | 4551.0 | 0.825 | 0.9978 | 0.3609 | 10.4–16695.6 |
| 3482a | DISC | one business problem analyzed and solved | 3.97 | spider2 | 9828.3 | 0.505 | 0.9237 | 0.1547 | 35.9–19785.2 |
| 3483a | DISC | one cost-benefit/ROI analysis | 2.78 | gdpval | 4551.0 | 0.825 | 0.9921 | 0.3369 | 10.2–10372.7 |
| 3484a | DISC | one input/output specification | 3.48 | gdpval | 4551.0 | 0.549 | 0.9344 | 0.1605 | 20.3–5877.2 |
| 20950a | DISC | one malfunction troubleshot and resolved | 4.24 | terminal_bench_2 | 3944.5 | 0.776 | 0.8479 | 0.1936 | 7.4–2224.7 |
| 2486a | DISC | one batch of entries checked and corrected | 4.68 | apex_accounting | 25.0 | 0.195 | 0.0 | 0.0 | – |
| 2487a | DISC | one batch of transactions recorded | 3.54 | apex_accounting | 25.0 | 0.195 | 0.0 | 0.0 | – |
| 2487b | DISC | one analysis or report query run | 1.43 | finch | 236.6 | 0.76 | 0.8978 | 0.2263 | 1.3–295.4 |
| 2490b | DISC | one period summary of financial data | 1.04 | apex_accounting | 25.0 | 0.119 | 0.0 | 0.0 | – |
| 2491a | DISC | one bill or invoice issued | 2.08 | starshell | 154.6 | 0.738 | 0.9015 | 0.1894 | 1.0–93.7 |
| 2491b | DISC | one account statement issued | 1.04 | apex_accounting | 25.0 | 0.379 | 0.097 | 0.0034 | 2.2–10.9 |
| 2491c | DISC | one financial statement prepared and issued | 1.04 | apex_accounting | 25.0 | 0.096 | 0.0 | 0.0 | – |
| 2492a | DISC | one financial report | 3.97 | apex_accounting | 25.0 | 0.16 | 0.0 | 0.0 | – |
| 2493a | DISC | one batch of documents coded | 4.32 | dualentry | 56.6 | 0.404 | 0.4638 | 0.0409 | 2.8–69.7 |
| 2494a | LIVE | one account question answered during a contact | 2.10 | eva_bench | 142.7 | 0.889 | 0.9985 | 0.5556 | 0.5–38.1 |
| 2494b | DISC | one written inquiry answered | 2.10 | crmarena_pro | 829.8 | 0.92 | 0.9987 | 0.4358 | 1.8–923.2 |
| 2495a | DISC | one set of calculations | 3.13 | dualentry | 56.6 | 0.885 | 0.9746 | 0.2227 | 1.4–78.0 |
| 2496a | DISC | one discrepancy reconciled or reported | 4.29 | apex_accounting | 25.0 | 0.211 | 0.0535 | 0.0024 | 2.5–23.0 |
| 2497a | DISC | one set of financial calculations | 4.32 | dualentry | 56.6 | 0.548 | 0.5359 | 0.0627 | 1.0–33.5 |
| 2498b | DISC | one document or batch filed electronically | 0.85 | osworld_verified | 166.6 | 0.883 | 0.9938 | 0.3656 | 1.2–205.9 |
| 2498c | LIVE | one routine incoming call handled | 1.06 | eva_bench | 142.7 | 0.962 | 0.9999 | 0.7176 | 0.2–116.6 |
| 2498d | DISC | one routine correspondence item sent | 1.27 | gdpval | 4551.0 | 0.994 | 1.0 | 0.495 | 1.0–267.1 |
| 2499a | DISC | one deposit batch compiled and balanced | 2.77 | apex_accounting | 25.0 | 0.462 | 0.319 | 0.0225 | 2.9–41.5 |
| 2500a | LIVE | one payment received at the counter | 0.89 | sopbench | 1041.1 | 0.993 | 1.0 | 0.844 | 0.5–35.0 |
| 2500b | DISC | one batch of received payments recorded | 2.01 | dualentry | 56.6 | 0.404 | 0.305 | 0.0242 | 3.0–34.0 |
| 2501a | DISC | one batch of payment checks prepared | 4.44 | apex_accounting | 25.0 | 0.195 | 0.0397 | 0.0007 | 5.6–20.8 |
| 2502a | DISC | one printout-to-journal comparison | 4.23 | spreadsheetbench_2 | 137.8 | 0.589 | 0.6517 | 0.0803 | 2.0–86.6 |
| 2503a | DISC | one bank account reconciliation | 4.38 | apex_accounting | 25.0 | 0.16 | 0.0 | 0.0 | – |
| 2504a | DISC | one trial balance | 4.08 | apex_accounting | 25.0 | 0.16 | 0.0 | 0.0 | – |
| 2505a | DISC | one account status review | 2.64 | apex_accounting | 25.0 | 0.254 | 0.1081 | 0.0033 | 4.1–23.1 |
| 2505b | DISC | one overdue account followed up | 1.76 | gdpval | 4551.0 | 0.985 | 1.0 | 0.5045 | 1.3–182.8 |
| 2506a | DISC | one batch of journal entries posted to the ledger | 4.20 | apex_accounting | 25.0 | 0.254 | 0.0 | 0.0 | – |
| 2507a | DISC | one budget package | 4.33 | finch | 236.6 | 0.18 | 0.4403 | 0.0226 | 27.4–1560.6 |
| 2508a | DISC | one cost calculation | 4.14 | finch | 236.6 | 0.692 | 0.879 | 0.1939 | 1.6–236.4 |
| 2509a | DISC | one batch of invoices matched to orders | 4.12 | apex_accounting | 25.0 | 0.195 | 0.063 | 0.001 | 7.6–26.4 |
| 2510a | DISC | one government form completed and submitted | 4.17 | osworld_2 (no horizon) |  |  |  |  | – |
| 2511a | DISC | one batch of inventory record updates | 3.57 | ui_cube | 55.0 | 0.342 | 0.5277 | 0.0401 | 3.9–94.6 |
| 2514a | DISC | one purchase order | 2.06 | starshell | 154.6 | 0.773 | 0.9927 | 0.2871 | 2.1–220.8 |
| 2514b | DISC | one expense report | 2.06 | ui_cube | 55.0 | 0.701 | 0.9485 | 0.2016 | 2.0–101.2 |
| 18561a | DISC | one payroll run | 4.71 | apex_accounting | 25.0 | 0.07 | 0.004 | 0.0001 | 13.5–40.2 |
| 23237a | DISC | one stop-payment notice posted | 2.99 | dualentry | 56.6 | 0.724 | 0.8622 | 0.1307 | 0.5–23.1 |
| 23238a | DISC | one batch of billing data verified and corrected | 4.66 | finch | 236.6 | 0.616 | 0.8605 | 0.1528 | 6.2–466.4 |
| 23239a | DISC | one batch of checks verified | 2.84 | none (no horizon) |  |  |  |  | – |
| 23240a | DISC | one batch of invoices prepared and recorded | 3.02 | starshell | 154.6 | 0.468 | 0.8485 | 0.1231 | 4.1–300.0 |
| 23241a | DISC | one batch of postings | 3.49 | dualentry | 56.6 | 0.325 | 0.4013 | 0.0268 | 3.5–70.4 |
| 23242a | DISC | one billing calculation or document processed using office e | 4.03 | dualentry | 56.6 | 0.753 | 0.781 | 0.0831 | 1.6–23.4 |
| 23243a | DISC | one discrepancy resolved | 3.71 | apex_accounting | 25.0 | 0.211 | 0.0 | 0.0 | – |
| 23244a | LIVE | one customer call about an account | 2.06 | tau_voice | 125.8 | 0.837 | 0.9843 | 0.436 | 0.7–34.1 |
| 23244b | DISC | one written customer message | 1.38 | crmarena_pro | 829.8 | 0.942 | 1.0 | 0.4097 | 1.0–267.1 |
| 23245a | DISC | one set of documents reviewed and charges computed | 3.84 | dualentry | 56.6 | 0.548 | 0.6502 | 0.0729 | 2.2–55.5 |
| 23246a | DISC | one batch of invoices and support documents filed | 4.13 | osworld_verified | 166.6 | 0.831 | 0.9282 | 0.2342 | 4.4–473.2 |
| 23247a | DISC | one batch of statements routed | 3.24 | none (no horizon) |  |  |  |  | – |
| 23249b | DISC | one major equipment fault reported | 0.83 | workarena_l1 | 372.2 | 0.962 | 1.0 | 0.4406 | 0.7–267.2 |
| 23251a | DISC | one bank statement reconciliation | 3.24 | apex_accounting | 25.0 | 0.16 | 0.0192 | 0.0005 | 4.1–21.0 |
| 23255a | DISC | one charge or rule determined | 3.92 | tau_banking | 99.4 | 0.732 | 0.8486 | 0.1032 | 3.7–86.1 |
| 23256a | DISC | one client job's fee calculated | 3.94 | finch | 236.6 | 0.692 | 0.9679 | 0.241 | 2.0–302.9 |
| 23257a | DISC | one manual update | 3.39 | officeval (no horizon) |  |  |  |  | – |
| 23258a | DISC | one billing document's charges computed | 3.50 | dualentry | 56.6 | 0.63 | 0.5199 | 0.0671 | 0.6–23.2 |
| 23260a | DISC | one rate decision | 4.35 | finch | 236.6 | 0.154 | 0.0853 | 0.0045 | 13.5–113.5 |
| 23262a | LIVE | one live rates, routing, or procedures inquiry answered | 3.17 | tau_voice | 125.8 | 0.857 | 0.9526 | 0.4213 | 0.4–34.2 |
| 23262b | DISC | one written rates, routing, or procedures inquiry answered | 1.06 | gdpval | 4551.0 | 0.98 | 0.9996 | 0.4694 | 1.8–964.8 |
| 23263a | DISC | one cost factor report | 3.78 | finch | 236.6 | 0.413 | 0.6591 | 0.0791 | 6.4–452.7 |
| 23264b | DISC | one shipping label created | 0.72 | ui_cube | 55.0 | 0.9 | 1.0 | 0.4359 | 0.5–73.1 |
| 23264c | DISC | one credit memorandum or credit form created | 1.08 | dualentry | 56.6 | 0.594 | 0.8778 | 0.123 | 2.0–59.4 |
| 23265a | LIVE | one general telephone call answered and handled | 1.25 | tau_voice | 125.8 | 0.958 | 0.9999 | 0.7062 | 0.2–104.1 |
| 23265b | LIVE | one appointment scheduled or changed during a contact | 0.72 | tau_voice | 125.8 | 0.948 | 1.0 | 0.7175 | 0.5–73.1 |
| 23265c | DISC | one appointment scheduled or changed from a written request | 0.54 | theagentcompany | 186.2 | 0.954 | 0.9994 | 0.4351 | 0.7–215.3 |
| 23265d | DISC | one supply or equipment order submitted | 1.07 | theagentcompany | 186.2 | 0.767 | 0.9789 | 0.2751 | 1.0–176.7 |
| 23266b | DISC | one account adjustment for a check-return error | 0.95 | apex_accounting | 25.0 | 0.379 | 0.2265 | 0.0121 | 1.5–15.6 |
| 23266c | LIVE | one live check-error inquiry answered | 0.79 | tau_retail_airline | 425.3 | 0.918 | 0.998 | 0.6007 | 0.7–114.9 |
| 23266d | DISC | one written check-error inquiry answered | 0.32 | tau_banking | 99.4 | 0.701 | 0.9394 | 0.1397 | 2.4–82.2 |
| 11401a | DISC | one batch of source documents entered | 4.52 | ui_cube | 55.0 | 0.482 | 0.7087 | 0.0913 | 4.6–259.2 |
| 11402b | DISC | One batch of source data compiled and checked before entry | 3.07 | officeval (no horizon) |  |  |  |  | – |
| 11403a | DISC | one batch verified | 4.54 | officeval (no horizon) |  |  |  |  | – |
| 11405a | DISC | one set of errors corrected or reported | 4.82 | ui_cube | 55.0 | 0.749 | 0.9431 | 0.221 | 1.9–177.6 |
| 11406a | DISC | one shift's work log | 4.21 | none (no horizon) |  |  |  |  | – |
| 11409a | DISC | one message resolved | 3.38 | cybench (no horizon) |  |  |  |  | – |
| 23313a | DISC | one claim form prepared and checked for completeness | 4.75 | healthadminbench | 43.8 | 0.389 | 0.512 | 0.0401 | 2.5–41.3 |
| 23314a | DISC | one claim amount calculated | 4.64 | dualentry | 56.6 | 0.548 | 0.2445 | 0.004 | 8.6–23.2 |
| 23315a | DISC | one batch of documents posted to claim files | 4.62 | ui_cube | 55.0 | 0.398 | 0.504 | 0.0442 | 2.3–62.6 |
| 23316a | DISC | one claim transmitted for payment or investigation | 4.61 | healthadminbench | 43.8 | 0.711 | 0.4404 | 0.0325 | 0.4–8.2 |
| 23317a | LIVE | one outbound call to obtain missing claim information | 2.24 | eva_bench | 142.7 | 0.833 | 0.9817 | 0.4253 | 0.8–38.3 |
| 23317b | DISC | one written request for missing information | 2.24 | theagentcompany | 186.2 | 0.767 | 0.9957 | 0.2659 | 1.5–242.7 |
| 23318a | DISC | one coverage determination | 4.46 | sopbench | 1041.1 | 0.887 | 0.9925 | 0.3077 | 1.6–802.1 |
| 23319a | DISC | one new policy processed and recorded | 2.23 | ui_cube | 55.0 | 0.435 | 0.409 | 0.0369 | 2.5–34.5 |
| 23319b | DISC | one new claim processed and recorded | 2.23 | ui_cube | 55.0 | 0.482 | 0.7673 | 0.099 | 2.0–53.9 |
| 23320a | DISC | one batch of records entered or filed | 3.36 | ui_cube | 55.0 | 0.398 | 0.2528 | 0.0086 | 7.0–35.5 |
| 23320b | DISC | one record retrieval request | 1.76 | crmarena_pro | 829.8 | 0.967 | 0.9977 | 0.4662 | 0.9–407.5 |
| 23321a | LIVE | one customer inquiry answered during a call | 3.28 | tau_voice | 125.8 | 0.818 | 0.972 | 0.3985 | 0.8–34.2 |
| 23321b | DISC | one written instruction or referral | 1.09 | gdpval | 4551.0 | 0.985 | 1.0 | 0.4089 | 0.7–542.3 |
| 23322a | DISC | one letter or email to an insured or agent | 4.29 | gdpval | 4551.0 | 0.98 | 0.9999 | 0.453 | 1.4–743.6 |
| 23323a | DISC | one application or policy verified | 4.22 | officeval (no horizon) |  |  |  |  | – |
| 23324a | DISC | one reinstatement request decided | 4.16 | sopbench | 1041.1 | 0.933 | 0.9982 | 0.399 | 0.8–638.7 |
| 23325a | DISC | one change request assessed | 4.14 | crmarena_pro | 829.8 | 0.883 | 0.9958 | 0.2676 | 2.0–363.8 |
| 23327a | DISC | one cancellation notice | 3.65 | gdpval | 4551.0 | 0.988 | 1.0 | 0.4391 | 0.7–267.2 |
| 23328a | DISC | one small claim paid | 4.69 | sopbench | 1041.1 | 0.944 | 1.0 | 0.3939 | 1.2–320.5 |
| 23329a | DISC | one form or application submitted | 4.45 | healthadminbench | 43.8 | 0.353 | 0.175 | 0.0065 | 4.7–27.9 |
| 23330a | LIVE | one premium taken and receipted during contact | 2.03 | tau_voice | 125.8 | 0.837 | 0.9962 | 0.4669 | 0.9–33.9 |
| 23330b | DISC | one batch of premiums receipted | 2.03 | apex_accounting | 25.0 | 0.195 | 0.1292 | 0.0078 | 3.4–34.5 |
| 23332a | LIVE | one client call or interview | 3.91 | eva_bench | 142.7 | 0.761 | 0.8389 | 0.2567 | 1.2–38.8 |
| 23333a | DISC | one policy-cancellation printout | 3.02 | workarena_l1 | 372.2 | 0.909 | 0.9996 | 0.3949 | 0.6–251.3 |
| 23334a | DISC | one letter drafted | 3.69 | gdpval | 4551.0 | 0.969 | 1.0 | 0.4688 | 2.5–667.7 |
| 22877a | DISC | one inpatient encounter assigned a DRG | 4.26 | healthadminbench | 43.8 | 0.711 | 0.0 | 0.0 | – |
| 22878a | DISC | one patient's encounter record compiled or updated | 4.45 | healthadminbench | 43.8 | 0.494 | 0.526 | 0.0468 | 2.4–40.7 |
| 22880a | DISC | one patient record's data entered | 4.42 | healthadminbench | 43.8 | 0.494 | 0.526 | 0.0468 | 2.4–40.7 |
| 22881a | DISC | one encounter abstracted and coded | 4.44 | healthadminbench | 43.8 | 0.494 | 0.526 | 0.0468 | 2.4–40.7 |
| 22882a | DISC | one batch of records indexed | 2.64 | healthadminbench | 43.8 | 0.353 | 0.1054 | 0.0012 | 9.0–22.4 |
| 22882b | DISC | one query or report | 1.76 | spider2 | 9828.3 | 0.981 | 0.9998 | 0.5607 | 2.6–3711.1 |
| 22884a | DISC | one form prepared and submitted | 4.07 | healthadminbench | 43.8 | 0.353 | 0.3405 | 0.0236 | 3.1–51.1 |
| 22885a | DISC | one patient's admission or discharge document set processed | 4.40 | healthadminbench | 43.8 | 0.494 | 0.3557 | 0.0349 | 1.1–21.3 |
| 22886b | DISC | one access audit or incident review | 1.44 | gdpval | 4551.0 | 0.894 | 0.9958 | 0.4365 | 13.2–11301.3 |
| 22887a | LIVE | one release made during contact | 0.90 | sopbench | 1041.1 | 0.96 | 0.9998 | 0.7083 | 0.6–286.9 |
| 22887b | DISC | one release request fulfilled | 3.60 | healthadminbench | 43.8 | 0.389 | 0.137 | 0.0017 | 8.9–21.7 |
| 22888a | DISC | one coding or diagnosis clarification issue resolved or refe | 4.54 | healthadminbench | 43.8 | 0.389 | 0.1423 | 0.008 | 2.5–19.2 |
| 22889a | DISC | one electronic patient record retrieved for a requester | 3.19 | healthadminbench | 43.8 | 0.678 | 0.6115 | 0.0594 | 1.1–17.3 |
| 22890a | DISC | one record reviewed | 4.68 | healthadminbench | 43.8 | 0.494 | 0.1359 | 0.0013 | 7.5–15.7 |
| 22891b | DISC | one batch of scans indexed and checked | 1.85 | healthadminbench | 43.8 | 0.353 | 0.3782 | 0.0271 | 2.5–47.5 |
| 22892a | LIVE | one appointment booked during contact | 2.24 | tau_voice | 125.8 | 0.948 | 1.0 | 0.7158 | 0.5–73.1 |
| 22892b | DISC | one batch of appointments scheduled | 1.49 | sopbench | 1041.1 | 0.848 | 0.9999 | 0.4324 | 3.4–1561.0 |
| 22893a | DISC | one report transcribed | 3.74 | gdpval | 4551.0 | 0.969 | 1.0 | 0.4393 | 2.3–1076.4 |
