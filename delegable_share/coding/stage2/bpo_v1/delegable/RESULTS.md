# Delegable shares — bpo_v1

D̄ = importance-weighted mean of D over items with a horizon (interpersonal, physical and no-deliverable items count as 0). Uncovered = share of weight whose matched benchmark has no horizon (or no match); it is excluded, not filled. S = expected net hours saved by delegating (gain minus review, and minus failure cost for live items), as a share of the item's unassisted hours, over the hours where delegation pays.

Headline measure: S; D alongside. Headline rows: the first two (ρ = 1, and ρ = 0.5 for benchmarks graded by tests or state checks). Other rows vary one setting from the first row.

| Scenario | Billing and Posting Clerks | Bookkeeping, Accounting, and Auditing Clerks | Computer Systems Analysts | Data Entry Keyers | Database Administrators | Insurance Claims and Policy Processing Clerks | Medical Records Specialists | Network and Computer Systems Administrators | Software Developers | Web Developers |
|---|---|---|---|---|---|---|---|---|---|---|
| base | S 14% · D 58% (eq D 56%; unc 10%) | S 9% · D 35% (eq D 35%; unc 4%) | S 13% · D 56% (eq D 56%; unc 3%) | S 7% · D 34% (eq D 32%; unc 39%) | S 14% · D 52% (eq D 52%; unc 11%) | S 24% · D 75% (eq D 76%; unc 5%) | S 11% · D 40% (eq D 41%; unc 0%) | S 20% · D 67% (eq D 66%; unc 0%) | S 12% · D 41% (eq D 41%; unc 0%) | S 29% · D 82% (eq D 83%; unc 0%) |
| base, rho 0.5 (tests/state) | S 6% · D 38% (eq D 37%; unc 10%) | S 5% · D 23% (eq D 23%; unc 4%) | S 10% · D 46% (eq D 47%; unc 3%) | S 0% · D 12% (eq D 11%; unc 39%) | S 11% · D 41% (eq D 42%; unc 11%) | S 10% · D 42% (eq D 44%; unc 5%) | S 5% · D 12% (eq D 13%; unc 0%) | S 8% · D 45% (eq D 45%; unc 0%) | S 12% · D 37% (eq D 36%; unc 0%) | S 21% · D 79% (eq D 80%; unc 0%) |
| beta 0.6 | S 21% · D 71% (eq D 70%; unc 10%) | S 13% · D 44% (eq D 45%; unc 4%) | S 22% · D 70% (eq D 70%; unc 3%) | S 13% · D 40% (eq D 37%; unc 39%) | S 22% · D 67% (eq D 66%; unc 11%) | S 30% · D 91% (eq D 91%; unc 5%) | S 14% · D 61% (eq D 61%; unc 0%) | S 28% · D 78% (eq D 78%; unc 0%) | S 18% · D 58% (eq D 57%; unc 0%) | S 37% · D 85% (eq D 85%; unc 0%) |
| beta 1.0 | S 12% · D 47% (eq D 45%; unc 10%) | S 8% · D 28% (eq D 29%; unc 4%) | S 9% · D 44% (eq D 45%; unc 3%) | S 4% · D 25% (eq D 24%; unc 39%) | S 11% · D 42% (eq D 42%; unc 11%) | S 22% · D 65% (eq D 67%; unc 5%) | S 10% · D 32% (eq D 33%; unc 0%) | S 16% · D 58% (eq D 57%; unc 0%) | S 10% · D 36% (eq D 35%; unc 0%) | S 25% · D 78% (eq D 78%; unc 0%) |
| decompressed spread, both sides | S 3% · D 11% (eq D 11%; unc 10%) | S 3% · D 9% (eq D 9%; unc 4%) | S 1% · D 5% (eq D 5%; unc 3%) | S 1% · D 5% (eq D 5%; unc 39%) | S 2% · D 7% (eq D 7%; unc 11%) | S 10% · D 34% (eq D 36%; unc 5%) | S 4% · D 11% (eq D 13%; unc 0%) | S 4% · D 15% (eq D 15%; unc 0%) | S 1% · D 6% (eq D 6%; unc 0%) | S 4% · D 19% (eq D 20%; unc 0%) |
| decompressed spread, benchmarks only | S 19% · D 62% (eq D 61%; unc 10%) | S 12% · D 37% (eq D 38%; unc 4%) | S 21% · D 63% (eq D 63%; unc 3%) | S 17% · D 40% (eq D 37%; unc 39%) | S 20% · D 57% (eq D 56%; unc 11%) | S 33% · D 88% (eq D 88%; unc 5%) | S 15% · D 56% (eq D 57%; unc 0%) | S 29% · D 74% (eq D 73%; unc 0%) | S 17% · D 46% (eq D 46%; unc 0%) | S 38% · D 84% (eq D 85%; unc 0%) |
| lambda 0.25 | S 16% · D 58% (eq D 57%; unc 10%) | S 9% · D 35% (eq D 35%; unc 4%) | S 14% · D 57% (eq D 57%; unc 3%) | S 7% · D 34% (eq D 32%; unc 39%) | S 15% · D 53% (eq D 52%; unc 11%) | S 27% · D 75% (eq D 77%; unc 5%) | S 11% · D 40% (eq D 41%; unc 0%) | S 20% · D 68% (eq D 67%; unc 0%) | S 12% · D 41% (eq D 41%; unc 0%) | S 29% · D 82% (eq D 83%; unc 0%) |
| lambda 3 | S 12% · D 55% (eq D 54%; unc 10%) | S 8% · D 34% (eq D 35%; unc 4%) | S 13% · D 55% (eq D 55%; unc 3%) | S 7% · D 34% (eq D 32%; unc 39%) | S 14% · D 51% (eq D 51%; unc 11%) | S 20% · D 67% (eq D 68%; unc 5%) | S 10% · D 40% (eq D 41%; unc 0%) | S 19% · D 65% (eq D 64%; unc 0%) | S 12% · D 41% (eq D 41%; unc 0%) | S 29% · D 82% (eq D 83%; unc 0%) |
| fill from 2nd match | S 17% · D 62% (eq D 61%; unc 0%) | S 9% · D 35% (eq D 35%; unc 4%) | S 14% · D 57% (eq D 57%; unc 0%) | S 17% · D 54% (eq D 54%; unc 12%) | S 13% · D 49% (eq D 48%; unc 0%) | S 25% · D 76% (eq D 77%; unc 0%) | S 11% · D 40% (eq D 41%; unc 0%) | S 20% · D 67% (eq D 66%; unc 0%) | S 12% · D 41% (eq D 41%; unc 0%) | S 29% · D 82% (eq D 83%; unc 0%) |
| latest observed H (no date alignment) | S 8% · D 36% (eq D 35%; unc 10%) | S 5% · D 17% (eq D 17%; unc 4%) | S 5% · D 36% (eq D 37%; unc 3%) | S 0% · D 0% (eq D 0%; unc 39%) | S 7% · D 36% (eq D 35%; unc 11%) | S 12% · D 34% (eq D 37%; unc 5%) | S 6% · D 13% (eq D 15%; unc 0%) | S 9% · D 38% (eq D 38%; unc 0%) | S 5% · D 30% (eq D 29%; unc 0%) | S 12% · D 58% (eq D 60%; unc 0%) |
| +12 months (pooled trend) | S 37% · D 82% (eq D 81%; unc 10%) | S 28% · D 84% (eq D 84%; unc 4%) | S 32% · D 74% (eq D 73%; unc 3%) | S 19% · D 40% (eq D 37%; unc 39%) | S 31% · D 72% (eq D 70%; unc 11%) | S 46% · D 99% (eq D 99%; unc 5%) | S 32% · D 83% (eq D 83%; unc 0%) | S 40% · D 85% (eq D 84%; unc 0%) | S 25% · D 64% (eq D 62%; unc 0%) | S 48% · D 89% (eq D 89%; unc 0%) |

## Items (base scenario)

| item | type | work item | w | benchmark | H (min) | π at p50 | D | S | delegated lengths (min) |
|---|---|---|---|---|---|---|---|---|---|
| 21661a | DISC | one system recommendation with installation plan | 3.61 | gdpval | 4729.4 | 0.692 | 0.9925 | 0.2683 | 21.9–39794.2 |
| 21662a | DISC | one feasibility assessment of a proposed design | 4.08 | gdpval | 4729.4 | 0.829 | 0.9997 | 0.3936 | 13.5–32649.1 |
| 21665b | DISC | one technical question answered in writing | 1.35 | theagentcompany | 201.2 | 0.417 | 0.3698 | 0.023 | 3.7–55.2 |
| 21666a | DISC | one software system installation coordinated | 3.75 | theagentcompany | 201.2 | 0.065 | 0.1514 | 0.0025 | 27.4–558.0 |
| 21667a | DISC | one feature or module designed and implemented | 3.56 | swe_bench_pro | 302.9 | 0.052 | 0.102 | 0.002 | 35.1–843.0 |
| 21668a | DISC | one set of system performance standards | 3.53 | gdpval | 4729.4 | 0.639 | 0.96 | 0.2079 | 10.7–5079.6 |
| 21669a | DISC | one software test or validation procedure | 1.17 | swt_bench | 452.7 | 0.548 | 0.6731 | 0.0845 | 10.9–786.7 |
| 21669b | DISC | one software code change | 1.17 | swe_bench_pro | 302.9 | 0.183 | 0.0654 | 0.001 | 36.9–169.7 |
| 21669c | DISC | one software documentation document or update | 0.78 | gdpval | 4729.4 | 0.897 | 0.9936 | 0.3577 | 11.7–8945.6 |
| 21670a | DISC | one change request or bug fix to existing software | 3.74 | swe_bench_pro | 302.9 | 0.149 | 0.1479 | 0.003 | 39.9–366.0 |
| 21671a | DISC | one system or equipment monitoring exception assessed | 4.12 | itbench_sre | 78.7 | 0.203 | 0.0314 | 0.0004 | 6.9–19.5 |
| 21672a | DISC | one hardware configuration recommendation | 3.07 | gdpval | 4729.4 | 0.829 | 0.9981 | 0.3657 | 10.4–17433.8 |
| 21673a | DISC | one project report | 2.21 | gdpval | 4729.4 | 0.94 | 1.0 | 0.5061 | 4.1–3859.3 |
| 21673b | DISC | one piece of project correspondence | 1.47 | theagentcompany | 201.2 | 0.779 | 0.9843 | 0.2747 | 0.8–305.7 |
| 21676a | DISC | one data analysis of system capabilities or requirements | 3.59 | spider2 | 10523.2 | 0.776 | 0.987 | 0.3058 | 15.4–8537.5 |
| 14694a | DISC | one website or feature design | 1.10 | gdpval | 4729.4 | 0.776 | 0.9732 | 0.2692 | 10.4–26763.7 |
| 14694b | DISC | one implemented website feature or component | 1.99 | swe_lancer | 3693.6 | 0.798 | 0.9978 | 0.3648 | 10.8–26005.9 |
| 14694c | DISC | one website maintenance change | 2.26 | swe_lancer | 3693.6 | 0.927 | 0.998 | 0.4573 | 6.0–12102.0 |
| 14698a | DISC | one website file backup completed | 4.35 | terminal_bench_1 | 1101.0 | 0.936 | 0.9985 | 0.3955 | 2.1–1037.2 |
| 14700a | DISC | one code change evaluated | 4.09 | sweeper_bench | 261.6 | 0.71 | 0.5281 | 0.0435 | 9.6–119.8 |
| 14702a | DISC | one set of technical requirements | 3.79 | gdpval | 4729.4 | 0.829 | 0.9981 | 0.3657 | 10.4–17433.8 |
| 14704a | DISC | one database or schema built or changed | 4.05 | spider2 | 10523.2 | 0.711 | 0.8979 | 0.2036 | 16.8–12310.1 |
| 14705a | DISC | one domain renewal | 3.67 | online_mind2web | 262.6 | 0.949 | 0.9993 | 0.5084 | 1.2–433.8 |
| 14706b | DISC | one e-commerce feature integrated | 1.77 | swe_lancer | 3693.6 | 0.688 | 0.9767 | 0.2612 | 17.5–19035.6 |
| 14707a | DISC | one supporting code change | 4.58 | swe_lancer | 3693.6 | 0.798 | 0.9974 | 0.3564 | 13.6–28263.4 |
| 14708a | DISC | one hosting or network issue resolved | 3.57 | theagentcompany | 201.2 | 0.523 | 0.7966 | 0.111 | 3.8–539.5 |
| 14710a | DISC | one website test run | 4.04 | sweeper_bench | 261.6 | 0.493 | 0.8944 | 0.1551 | 4.8–766.5 |
| 14711a | DISC | one tool or language selection | 4.17 | gdpval | 4729.4 | 0.897 | 0.9991 | 0.4109 | 8.6–12058.7 |
| 14713a | DISC | one user email inquiry answered | 2.57 | gdpval | 4729.4 | 0.984 | 0.9971 | 0.4521 | 2.4–771.9 |
| 14713b | DISC | one automated response set up | 1.10 | terminal_bench_2 | 4104.6 | 0.933 | 0.9999 | 0.5659 | 4.3–7422.2 |
| 14714a | DISC | one website revision procedure | 3.29 | gdpval | 4729.4 | 0.731 | 0.9994 | 0.3458 | 25.4–27874.4 |
| 14717a | DISC | one server directory structure established | 3.47 | terminal_bench_1 | 1101.0 | 0.854 | 0.9997 | 0.3691 | 4.7–1462.9 |
| 14719a | DISC | one performance improvement recommendation | 1.02 | gdpval | 4729.4 | 0.801 | 0.9963 | 0.326 | 7.5–5381.0 |
| 14719b | DISC | one performance improvement implemented | 2.37 | swe_lancer | 3693.6 | 0.876 | 0.9913 | 0.3651 | 9.1–7595.3 |
| 14722a | DISC | one website specification document | 3.18 | gdpval | 4729.4 | 0.731 | 0.9872 | 0.275 | 20.9–17075.0 |
| 14723a | DISC | one security log review | 2.98 | itbench_sre | 78.7 | 0.472 | 0.0 | 0.0 | – |
| 14723b | DISC | one security problem escalated | 0.75 | itbench_sre | 78.7 | 0.615 | 0.5359 | 0.0523 | 1.0–33.5 |
| 14724a | DISC | one web model or prototype | 3.19 | swe_lancer | 3693.6 | 0.737 | 0.9689 | 0.248 | 25.8–27708.0 |
| 14725a | DISC | one server hardware or software recommendation | 3.11 | gdpval | 4729.4 | 0.829 | 0.9997 | 0.3936 | 13.5–32649.1 |
| 14726a | DISC | one test plan or procedure | 1.77 | gdpval | 4729.4 | 0.897 | 0.9995 | 0.4378 | 7.2–24442.5 |
| 14726b | DISC | one test results record | 1.77 | gdpval | 4729.4 | 0.965 | 1.0 | 0.5113 | 1.6–3711.1 |
| 14727a | DISC | one architecture or technology comparison | 2.75 | gdpval | 4729.4 | 0.731 | 0.9978 | 0.3241 | 25.4–19284.5 |
| 14728a | DISC | one technical factors report | 3.35 | gdpval | 4729.4 | 0.801 | 0.9974 | 0.3346 | 4.8–3411.5 |
| 14729a | DISC | one HTTP server installed and configured | 2.94 | terminal_bench_2 | 4104.6 | 0.846 | 1.0 | 0.4573 | 11.1–14668.2 |
| 14730a | DISC | one set of interaction or sequence diagrams | 2.73 | gdpval | 4729.4 | 0.917 | 0.9997 | 0.546 | 9.9–7334.1 |
| 1317a | DISC | one backup job run and verified | 3.04 | terminal_bench_2 | 4104.6 | 0.978 | 1.0 | 0.4031 | 1.0–964.8 |
| 1317b | DISC | one restore or recovery operation | 1.30 | terminal_bench_2 | 4104.6 | 0.834 | 0.9562 | 0.3049 | 7.8–3821.6 |
| 1318a | DISC | one maintenance change implemented | 2.45 | terminal_bench_2 | 4104.6 | 0.834 | 0.9792 | 0.3024 | 5.8–2135.6 |
| 1318b | DISC | one administration request handled | 1.63 | workarena_pp | 157.4 | 0.692 | 0.8375 | 0.1732 | 2.4–313.6 |
| 1319a | DISC | one security measure planned and implemented | 4.56 | terminal_bench_2 | 4104.6 | 0.528 | 0.843 | 0.114 | 31.1–12048.5 |
| 1320a | DISC | one console alert handled | 2.24 | itbench_sre | 78.7 | 0.313 | 0.0 | 0.0 | – |
| 1320b | DISC | one access request coordinated | 1.49 | workarena_pp | 157.4 | 0.801 | 0.926 | 0.2221 | 1.0–119.0 |
| 1321a | DISC | one startup or shutdown procedure with record | 3.35 | terminal_bench_1 | 1101.0 | 0.749 | 0.9878 | 0.2943 | 2.0–426.8 |
| 1322a | DISC | one tested network or operating system configuration | 2.44 | terminal_bench_2 | 4104.6 | 0.667 | 0.7673 | 0.1472 | 5.9–2044.9 |
| 1323a | DISC | one improvement recommendation | 3.32 | gdpval | 4729.4 | 0.829 | 0.9981 | 0.3657 | 10.4–17433.8 |
| 1324a | LIVE | one live conversation about a system problem | 1.57 | eva_bench | 143.1 | 0.725 | 0.6443 | 0.1741 | 1.1–38.8 |
| 1324b | DISC | one written follow-up on a system problem | 1.90 | workarena_pp | 157.4 | 0.775 | 0.9679 | 0.173 | 1.2–70.8 |
| 1325a | DISC | one performance alert investigated | 1.78 | itbench_sre | 78.7 | 0.188 | 0.0 | 0.0 | – |
| 1325b | DISC | one periodic performance report | 1.78 | finch | 253.0 | 0.161 | 0.2843 | 0.0162 | 13.5–217.2 |
| 1327b | DISC | one software installation | 1.67 | terminal_bench_2 | 4104.6 | 0.966 | 1.0 | 0.5245 | 1.7–1608.0 |
| 1328a | DISC | one system requirements assessment | 3.29 | gdpval | 4729.4 | 0.497 | 0.9463 | 0.1583 | 21.4–7947.2 |
| 1329a | DISC | one repair-or-replace assessment | 3.28 | gdpval | 4729.4 | 0.917 | 1.0 | 0.5831 | 5.5–7334.1 |
| 1330a | DISC | one network function log update | 1.82 | workarena_l1 | 396.3 | 0.861 | 0.9932 | 0.3484 | 1.9–433.4 |
| 1330b | DISC | one maintenance or repair record | 1.82 | workarena_l1 | 396.3 | 0.957 | 1.0 | 0.3955 | 0.7–542.3 |
| 1332b | DISC | one inventory update | 2.06 | ui_cube | 60.1 | 0.762 | 0.8129 | 0.1561 | 1.4–116.1 |
| 1333a | DISC | one purchase coordinated | 3.32 | theagentcompany | 201.2 | 0.439 | 0.8622 | 0.1293 | 5.5–532.2 |
| 15205b | DISC | one system or network incident diagnosed and resolved or esc | 2.06 | itbench_sre | 78.7 | 0.154 | 0.0 | 0.0 | – |
| 15206a | DISC | one email or antivirus configuration change | 1.57 | terminal_bench_2 | 4104.6 | 0.961 | 0.999 | 0.5644 | 3.3–8503.9 |
| 15206b | DISC | one email or virus alert investigated | 2.35 | itbench_sre | 78.7 | 0.472 | 0.3121 | 0.0343 | 1.6–47.3 |
| 15207b | DISC | one new technology implementation recommendation | 0.91 | gdpval | 4729.4 | 0.731 | 0.9982 | 0.2994 | 23.8–55790.2 |
| 15207c | DISC | one new technology deployment or implementation change | 1.22 | terminal_bench_4 | 770.0 | 0.177 | 0.1867 | 0.009 | 22.7–657.2 |
| 15208a | DISC | one voice service implementation or configuration change | 1.03 | terminal_bench_2 | 4104.6 | 0.738 | 0.9846 | 0.3032 | 10.9–4000.5 |
| 15208c | LIVE | one live voice service support contact | 0.59 | eva_bench | 143.1 | 0.725 | 0.6064 | 0.1634 | 1.0–39.1 |
| 15208d | DISC | one voice service support issue handled | 0.73 | workarena_pp | 157.4 | 0.314 | 0.3119 | 0.0241 | 2.8–81.2 |
| 1298a | DISC | one standard or guideline document | 3.43 | gdpval | 4729.4 | 0.497 | 0.9146 | 0.1369 | 27.6–6167.2 |
| 1299a | DISC | one database or DBMS change implemented | 2.80 | dba_bench | 54.3 | 0.069 | 0.0 | 0.0 | – |
| 1300a | DISC | one test round with fixes | 3.68 | swe_bench_pro | 302.9 | 0.239 | 0.3147 | 0.0111 | 22.2–307.9 |
| 1301a | DISC | one security measures plan | 1.57 | gdpval | 4729.4 | 0.497 | 0.8532 | 0.1334 | 20.4–4764.4 |
| 1301b | DISC | one security measure implemented | 2.36 | terminal_bench_2 | 4104.6 | 0.782 | 0.9504 | 0.2632 | 5.2–3199.3 |
| 1302a | DISC | one installation and testing plan with approval | 2.07 | gdpval | 4729.4 | 0.692 | 0.9789 | 0.2486 | 11.1–2476.7 |
| 1303b | LIVE | one user question answered during a live contact | 1.31 | eva_bench | 143.1 | 0.851 | 0.7911 | 0.2681 | 0.3–34.9 |
| 1303c | DISC | one written user question answered | 1.48 | spider2 | 10523.2 | 0.99 | 0.9969 | 0.5164 | 2.5–4868.1 |
| 1305a | DISC | one access specification or change | 3.80 | scuba (no horizon) |  |  |  |  | – |
| 1306a | DISC | one data model | 3.14 | spider2 | 10523.2 | 0.776 | 0.9529 | 0.2424 | 31.0–6702.8 |
| 1311a | DISC | one performance monitoring setup | 1.56 | dba_bench | 54.3 | 0.206 | 0.2265 | 0.0099 | 6.1–110.3 |
| 1311b | DISC | one production database created | 1.56 | terminal_bench_2 | 4104.6 | 0.908 | 0.9997 | 0.4451 | 7.3–7409.4 |
| 1312b | DISC | one trend briefing | 1.41 | gdpval | 4729.4 | 0.861 | 1.0 | 0.4874 | 13.5–8922.7 |
| 1313a | DISC | one coded set of database definitions | 2.21 | spider2 | 10523.2 | 0.956 | 0.9998 | 0.5095 | 3.5–17387.1 |
| 1315a | DISC | one data dictionary update | 2.70 | none (no horizon) |  |  |  |  | – |
| 21648a | DISC | one technology recommendation | 3.05 | gdpval | 4729.4 | 0.776 | 0.9967 | 0.3187 | 24.7–21994.7 |
| 21649a | DISC | one DBMS upgrade planned and installed | 3.86 | terminal_bench_4 | 770.0 | 0.107 | 0.3409 | 0.0145 | 49.2–1675.9 |
| 21651a | DISC | one change tested | 3.76 | swt_bench | 452.7 | 0.36 | 0.3991 | 0.0277 | 12.4–303.3 |
| 3464a | LIVE | one user problem fixed during a live contact | 1.62 | eva_bench | 143.1 | 0.725 | 0.6064 | 0.1634 | 1.0–39.1 |
| 3464b | DISC | one support ticket resolved | 2.43 | workarena_pp | 157.4 | 0.651 | 0.6556 | 0.1035 | 4.2–308.8 |
| 3465a | DISC | one program or system test cycle completed | 1.20 | swt_bench | 452.7 | 0.404 | 0.6878 | 0.0815 | 15.4–1299.9 |
| 3465b | DISC | one program or system maintenance change | 1.40 | terminal_bench_2 | 4104.6 | 0.782 | 0.9079 | 0.2242 | 6.7–2151.5 |
| 3465c | DISC | one monitoring alert or exception investigated | 0.80 | itbench_sre | 78.7 | 0.245 | 0.0 | 0.0 | – |
| 3465d | DISC | one installation or rollout coordinated | 0.60 | theagentcompany | 201.2 | 0.111 | 0.2641 | 0.0073 | 16.9–445.3 |
| 3466a | DISC | one program, module or feature coded | 3.71 | swe_bench_pro | 302.9 | 0.326 | 0.5199 | 0.0479 | 9.2–985.8 |
| 3468a | DISC | one system-to-system integration or interface | 3.78 | terminal_bench_4 | 770.0 | 0.053 | 0.0127 | 0.0001 | 150.2–686.2 |
| 3470a | DISC | one system enhancement delivered | 3.47 | swe_bench_pro | 302.9 | 0.043 | 0.0494 | 0.0009 | 38.2–722.4 |
| 3471a | DISC | one work-process investigation and its findings | 3.44 | gdpval | 4729.4 | 0.413 | 0.9418 | 0.1372 | 44.4–6553.4 |
| 3472a | DISC | one set of hardware/software requirements for a system | 3.33 | gdpval | 4729.4 | 0.861 | 0.9976 | 0.3725 | 8.8–8467.1 |
| 3474a | DISC | one system design | 3.60 | gdpval | 4729.4 | 0.246 | 0.4641 | 0.0342 | 92.3–4307.2 |
| 3475a | DISC | one package evaluation | 1.34 | gdpval | 4729.4 | 0.497 | 0.9777 | 0.1568 | 27.4–19485.8 |
| 3475b | DISC | one package configured for the user environment | 2.00 | terminal_bench_2 | 4104.6 | 0.341 | 0.6141 | 0.0574 | 23.9–10686.6 |
| 3476a | DISC | one system goals statement | 1.08 | gdpval | 4729.4 | 0.897 | 0.9994 | 0.3959 | 10.5–7981.6 |
| 3476b | DISC | one program logic diagram or diagram set | 2.00 | none (no horizon) |  |  |  |  | – |
| 3477a | DISC | one procedure or standard written or revised | 3.21 | gdpval | 4729.4 | 0.776 | 0.9998 | 0.3651 | 19.1–27425.8 |
| 3478a | DISC | one code defect located and corrected | 3.60 | swe_bench_verified | 4875.4 | 0.729 | 0.9228 | 0.2118 | 14.9–4059.2 |
| 3479a | DISC | one recommendation memo | 3.11 | gdpval | 4729.4 | 0.829 | 0.9981 | 0.3657 | 10.4–17433.8 |
| 3482a | DISC | one business problem analyzed and solved | 3.97 | spider2 | 10523.2 | 0.519 | 0.9319 | 0.1624 | 35.9–21222.5 |
| 3483a | DISC | one cost-benefit/ROI analysis | 2.78 | gdpval | 4729.4 | 0.829 | 0.9929 | 0.3418 | 10.2–10831.4 |
| 3484a | DISC | one input/output specification | 3.48 | gdpval | 4729.4 | 0.557 | 0.9394 | 0.165 | 20.3–6137.1 |
| 20950a | DISC | one malfunction troubleshot and resolved | 4.24 | terminal_bench_2 | 4104.6 | 0.782 | 0.8571 | 0.1984 | 7.4–2348.3 |
| 2486a | DISC | one batch of entries checked and corrected | 4.68 | apex_accounting | 25.2 | 0.196 | 0.0 | 0.0 | – |
| 2487a | DISC | one batch of transactions recorded | 3.54 | apex_accounting | 25.2 | 0.196 | 0.0 | 0.0 | – |
| 2487b | DISC | one analysis or report query run | 1.43 | finch | 253.0 | 0.77 | 0.9081 | 0.236 | 1.3–316.1 |
| 2490b | DISC | one period summary of financial data | 1.04 | apex_accounting | 25.2 | 0.12 | 0.0 | 0.0 | – |
| 2491a | DISC | one bill or invoice issued | 2.08 | starshell | 163.1 | 0.747 | 0.9115 | 0.1972 | 1.0–98.7 |
| 2491b | DISC | one account statement issued | 1.04 | apex_accounting | 25.2 | 0.381 | 0.1006 | 0.0035 | 2.1–11.1 |
| 2491c | DISC | one financial statement prepared and issued | 1.04 | apex_accounting | 25.2 | 0.097 | 0.0 | 0.0 | – |
| 2492a | DISC | one financial report | 3.97 | apex_accounting | 25.2 | 0.161 | 0.0 | 0.0 | – |
| 2493a | DISC | one batch of documents coded | 4.32 | dualentry | 56.9 | 0.405 | 0.4718 | 0.0413 | 2.8–71.1 |
| 2494a | LIVE | one account question answered during a contact | 2.10 | eva_bench | 143.1 | 0.889 | 0.9986 | 0.5561 | 0.5–38.5 |
| 2494b | DISC | one written inquiry answered | 2.10 | crmarena_pro | 929.9 | 0.927 | 0.9989 | 0.4471 | 1.8–1037.2 |
| 2495a | DISC | one set of calculations | 3.13 | dualentry | 56.9 | 0.885 | 0.9746 | 0.2233 | 1.4–78.0 |
| 2496a | DISC | one discrepancy reconciled or reported | 4.29 | apex_accounting | 25.2 | 0.212 | 0.0535 | 0.0024 | 2.5–23.0 |
| 2497a | DISC | one set of financial calculations | 4.32 | dualentry | 56.9 | 0.549 | 0.5359 | 0.0632 | 1.0–33.5 |
| 2498b | DISC | one document or batch filed electronically | 0.85 | osworld_verified | 170.1 | 0.885 | 0.9938 | 0.368 | 1.2–209.6 |
| 2498c | LIVE | one routine incoming call handled | 1.06 | eva_bench | 143.1 | 0.963 | 0.9999 | 0.7179 | 0.2–116.6 |
| 2498d | DISC | one routine correspondence item sent | 1.27 | gdpval | 4729.4 | 0.994 | 1.0 | 0.4953 | 1.0–267.1 |
| 2499a | DISC | one deposit batch compiled and balanced | 2.77 | apex_accounting | 25.2 | 0.464 | 0.319 | 0.023 | 2.9–41.5 |
| 2500a | LIVE | one payment received at the counter | 0.89 | sopbench | 1161.7 | 0.993 | 1.0 | 0.8457 | 0.5–35.0 |
| 2500b | DISC | one batch of received payments recorded | 2.01 | dualentry | 56.9 | 0.405 | 0.305 | 0.0245 | 3.0–34.0 |
| 2501a | DISC | one batch of payment checks prepared | 4.44 | apex_accounting | 25.2 | 0.196 | 0.0415 | 0.0007 | 5.6–21.2 |
| 2502a | DISC | one printout-to-journal comparison | 4.23 | spreadsheetbench_2 | 145.3 | 0.599 | 0.6737 | 0.0856 | 2.0–91.2 |
| 2503a | DISC | one bank account reconciliation | 4.38 | apex_accounting | 25.2 | 0.161 | 0.0 | 0.0 | – |
| 2504a | DISC | one trial balance | 4.08 | apex_accounting | 25.2 | 0.161 | 0.0 | 0.0 | – |
| 2505a | DISC | one account status review | 2.64 | apex_accounting | 25.2 | 0.256 | 0.1081 | 0.0034 | 4.1–23.1 |
| 2505b | DISC | one overdue account followed up | 1.76 | gdpval | 4729.4 | 0.986 | 1.0 | 0.5051 | 1.3–182.8 |
| 2506a | DISC | one batch of journal entries posted to the ledger | 4.20 | apex_accounting | 25.2 | 0.256 | 0.0 | 0.0 | – |
| 2507a | DISC | one budget package | 4.33 | finch | 253.0 | 0.188 | 0.464 | 0.0254 | 26.7–1674.0 |
| 2508a | DISC | one cost calculation | 4.14 | finch | 253.0 | 0.704 | 0.8944 | 0.2038 | 1.6–255.5 |
| 2509a | DISC | one batch of invoices matched to orders | 4.12 | apex_accounting | 25.2 | 0.196 | 0.0658 | 0.0011 | 7.5–26.9 |
| 2510a | DISC | one government form completed and submitted | 4.17 | osworld_2 (no horizon) |  |  |  |  | – |
| 2511a | DISC | one batch of inventory record updates | 3.57 | ui_cube | 60.1 | 0.359 | 0.5752 | 0.0476 | 3.8–105.4 |
| 2514a | DISC | one purchase order | 2.06 | starshell | 163.1 | 0.781 | 0.9936 | 0.2953 | 2.1–232.4 |
| 2514b | DISC | one expense report | 2.06 | ui_cube | 60.1 | 0.716 | 0.96 | 0.2153 | 2.0–110.0 |
| 18561a | DISC | one payroll run | 4.71 | apex_accounting | 25.2 | 0.071 | 0.004 | 0.0001 | 13.5–40.2 |
| 23237a | DISC | one stop-payment notice posted | 2.99 | dualentry | 56.9 | 0.725 | 0.8622 | 0.1315 | 0.5–23.1 |
| 23238a | DISC | one batch of billing data verified and corrected | 4.66 | finch | 253.0 | 0.629 | 0.8774 | 0.1623 | 6.2–508.6 |
| 23239a | DISC | one batch of checks verified | 2.84 | none (no horizon) |  |  |  |  | – |
| 23240a | DISC | one batch of invoices prepared and recorded | 3.02 | starshell | 163.1 | 0.479 | 0.8622 | 0.1304 | 4.1–315.8 |
| 23241a | DISC | one batch of postings | 3.49 | dualentry | 56.9 | 0.326 | 0.4013 | 0.0271 | 3.5–70.4 |
| 23242a | DISC | one billing calculation or document processed using office e | 4.03 | dualentry | 56.9 | 0.754 | 0.781 | 0.0838 | 1.6–23.4 |
| 23243a | DISC | one discrepancy resolved | 3.71 | apex_accounting | 25.2 | 0.212 | 0.0 | 0.0 | – |
| 23244a | LIVE | one customer call about an account | 2.06 | tau_voice | 126.2 | 0.837 | 0.9843 | 0.4368 | 0.7–34.1 |
| 23244b | DISC | one written customer message | 1.38 | crmarena_pro | 929.9 | 0.947 | 1.0 | 0.4156 | 1.0–267.1 |
| 23245a | DISC | one set of documents reviewed and charges computed | 3.84 | dualentry | 56.9 | 0.549 | 0.6502 | 0.0736 | 2.2–55.5 |
| 23246a | DISC | one batch of invoices and support documents filed | 4.13 | osworld_verified | 170.1 | 0.833 | 0.9307 | 0.2371 | 4.4–484.0 |
| 23247a | DISC | one batch of statements routed | 3.24 | none (no horizon) |  |  |  |  | – |
| 23249b | DISC | one major equipment fault reported | 0.83 | workarena_l1 | 396.3 | 0.964 | 1.0 | 0.4431 | 0.7–267.2 |
| 23251a | DISC | one bank statement reconciliation | 3.24 | apex_accounting | 25.2 | 0.161 | 0.0202 | 0.0006 | 4.1–21.4 |
| 23255a | DISC | one charge or rule determined | 3.92 | tau_banking | 99.5 | 0.733 | 0.8528 | 0.1033 | 3.7–87.9 |
| 23256a | DISC | one client job's fee calculated | 3.94 | finch | 253.0 | 0.704 | 0.9732 | 0.2518 | 2.0–324.4 |
| 23257a | DISC | one manual update | 3.39 | officeval (no horizon) |  |  |  |  | – |
| 23258a | DISC | one billing document's charges computed | 3.50 | dualentry | 56.9 | 0.631 | 0.5279 | 0.0676 | 0.6–23.7 |
| 23260a | DISC | one rate decision | 4.35 | finch | 253.0 | 0.161 | 0.0985 | 0.0054 | 13.5–121.1 |
| 23262a | LIVE | one live rates, routing, or procedures inquiry answered | 3.17 | tau_voice | 126.2 | 0.857 | 0.9526 | 0.422 | 0.4–34.2 |
| 23262b | DISC | one written rates, routing, or procedures inquiry answered | 1.06 | gdpval | 4729.4 | 0.98 | 0.9996 | 0.4704 | 1.8–964.8 |
| 23263a | DISC | one cost factor report | 3.78 | finch | 253.0 | 0.426 | 0.6879 | 0.0862 | 6.4–489.2 |
| 23264b | DISC | one shipping label created | 0.72 | ui_cube | 60.1 | 0.907 | 1.0 | 0.4435 | 0.5–73.1 |
| 23264c | DISC | one credit memorandum or credit form created | 1.08 | dualentry | 56.9 | 0.595 | 0.8778 | 0.1238 | 2.0–59.4 |
| 23265a | LIVE | one general telephone call answered and handled | 1.25 | tau_voice | 126.2 | 0.959 | 0.9999 | 0.7066 | 0.2–104.1 |
| 23265b | LIVE | one appointment scheduled or changed during a contact | 0.72 | tau_voice | 126.2 | 0.948 | 1.0 | 0.7178 | 0.5–73.1 |
| 23265c | DISC | one appointment scheduled or changed from a written request | 0.54 | theagentcompany | 201.2 | 0.957 | 0.9994 | 0.4395 | 0.7–215.3 |
| 23265d | DISC | one supply or equipment order submitted | 1.07 | theagentcompany | 201.2 | 0.779 | 0.9834 | 0.287 | 1.0–192.5 |
| 23266b | DISC | one account adjustment for a check-return error | 0.95 | apex_accounting | 25.2 | 0.381 | 0.2326 | 0.0124 | 1.5–15.9 |
| 23266c | LIVE | one live check-error inquiry answered | 0.79 | tau_retail_airline | 447.6 | 0.921 | 0.9984 | 0.6097 | 0.7–121.9 |
| 23266d | DISC | one written check-error inquiry answered | 0.32 | tau_banking | 99.5 | 0.701 | 0.9394 | 0.1399 | 2.4–82.2 |
| 11401a | DISC | one batch of source documents entered | 4.52 | ui_cube | 60.1 | 0.5 | 0.7421 | 0.1017 | 4.6–285.6 |
| 11402b | DISC | One batch of source data compiled and checked before entry | 3.07 | officeval (no horizon) |  |  |  |  | – |
| 11403a | DISC | one batch verified | 4.54 | officeval (no horizon) |  |  |  |  | – |
| 11405a | DISC | one set of errors corrected or reported | 4.82 | ui_cube | 60.1 | 0.762 | 0.9535 | 0.2344 | 1.9–195.7 |
| 11406a | DISC | one shift's work log | 4.21 | none (no horizon) |  |  |  |  | – |
| 11409a | DISC | one message resolved | 3.38 | cybench (no horizon) |  |  |  |  | – |
| 23313a | DISC | one claim form prepared and checked for completeness | 4.75 | healthadminbench | 46.1 | 0.399 | 0.5517 | 0.045 | 2.5–44.3 |
| 23314a | DISC | one claim amount calculated | 4.64 | dualentry | 56.9 | 0.549 | 0.2515 | 0.0042 | 8.6–23.6 |
| 23315a | DISC | one batch of documents posted to claim files | 4.62 | ui_cube | 60.1 | 0.416 | 0.5517 | 0.052 | 2.3–69.3 |
| 23316a | DISC | one claim transmitted for payment or investigation | 4.61 | healthadminbench | 46.1 | 0.72 | 0.4721 | 0.036 | 0.4–8.7 |
| 23317a | LIVE | one outbound call to obtain missing claim information | 2.24 | eva_bench | 143.1 | 0.834 | 0.9817 | 0.426 | 0.8–38.3 |
| 23317b | DISC | one written request for missing information | 2.24 | theagentcompany | 201.2 | 0.779 | 0.9968 | 0.2761 | 1.5–263.2 |
| 23318a | DISC | one coverage determination | 4.46 | sopbench | 1161.7 | 0.896 | 0.9946 | 0.3189 | 1.6–901.1 |
| 23319a | DISC | one new policy processed and recorded | 2.23 | ui_cube | 60.1 | 0.454 | 0.4562 | 0.0438 | 2.5–37.5 |
| 23319b | DISC | one new claim processed and recorded | 2.23 | ui_cube | 60.1 | 0.5 | 0.8024 | 0.1111 | 2.0–58.7 |
| 23320a | DISC | one batch of records entered or filed | 3.36 | ui_cube | 60.1 | 0.416 | 0.3078 | 0.013 | 6.6–40.7 |
| 23320b | DISC | one record retrieval request | 1.76 | crmarena_pro | 929.9 | 0.97 | 0.9977 | 0.4718 | 0.9–407.5 |
| 23321a | LIVE | one customer inquiry answered during a call | 3.28 | tau_voice | 126.2 | 0.819 | 0.9732 | 0.3993 | 0.8–34.7 |
| 23321b | DISC | one written instruction or referral | 1.09 | gdpval | 4729.4 | 0.986 | 1.0 | 0.4096 | 0.7–542.3 |
| 23322a | DISC | one letter or email to an insured or agent | 4.29 | gdpval | 4729.4 | 0.98 | 0.9999 | 0.4539 | 1.4–743.6 |
| 23323a | DISC | one application or policy verified | 4.22 | officeval (no horizon) |  |  |  |  | – |
| 23324a | DISC | one reinstatement request decided | 4.16 | sopbench | 1161.7 | 0.939 | 0.9987 | 0.4088 | 0.8–703.8 |
| 23325a | DISC | one change request assessed | 4.14 | crmarena_pro | 929.9 | 0.892 | 0.9972 | 0.2781 | 2.0–406.1 |
| 23327a | DISC | one cancellation notice | 3.65 | gdpval | 4729.4 | 0.988 | 1.0 | 0.4396 | 0.7–267.2 |
| 23328a | DISC | one small claim paid | 4.69 | sopbench | 1161.7 | 0.949 | 1.0 | 0.4003 | 1.2–320.5 |
| 23329a | DISC | one form or application submitted | 4.45 | healthadminbench | 46.1 | 0.363 | 0.2022 | 0.0083 | 4.5–30.4 |
| 23330a | LIVE | one premium taken and receipted during contact | 2.03 | tau_voice | 126.2 | 0.837 | 0.9965 | 0.4677 | 0.9–34.3 |
| 23330b | DISC | one batch of premiums receipted | 2.03 | apex_accounting | 25.2 | 0.196 | 0.1292 | 0.0079 | 3.4–34.5 |
| 23332a | LIVE | one client call or interview | 3.91 | eva_bench | 143.1 | 0.761 | 0.8389 | 0.2574 | 1.2–38.8 |
| 23333a | DISC | one policy-cancellation printout | 3.02 | workarena_l1 | 396.3 | 0.913 | 0.9997 | 0.4009 | 0.6–264.1 |
| 23334a | DISC | one letter drafted | 3.69 | gdpval | 4729.4 | 0.97 | 1.0 | 0.47 | 2.5–667.7 |
| 22877a | DISC | one inpatient encounter assigned a DRG | 4.26 | healthadminbench | 46.1 | 0.72 | 0.0 | 0.0 | – |
| 22878a | DISC | one patient's encounter record compiled or updated | 4.45 | healthadminbench | 46.1 | 0.505 | 0.5499 | 0.0517 | 2.3–43.1 |
| 22880a | DISC | one patient record's data entered | 4.42 | healthadminbench | 46.1 | 0.505 | 0.5499 | 0.0517 | 2.3–43.1 |
| 22881a | DISC | one encounter abstracted and coded | 4.44 | healthadminbench | 46.1 | 0.505 | 0.5499 | 0.0517 | 2.3–43.1 |
| 22882a | DISC | one batch of records indexed | 2.64 | healthadminbench | 46.1 | 0.363 | 0.1375 | 0.0024 | 8.4–25.2 |
| 22882b | DISC | one query or report | 1.76 | spider2 | 10523.2 | 0.982 | 0.9998 | 0.5631 | 2.6–3711.1 |
| 22884a | DISC | one form prepared and submitted | 4.07 | healthadminbench | 46.1 | 0.363 | 0.3703 | 0.0267 | 3.0–55.2 |
| 22885a | DISC | one patient's admission or discharge document set processed | 4.40 | healthadminbench | 46.1 | 0.505 | 0.3783 | 0.0383 | 1.1–22.3 |
| 22886b | DISC | one access audit or incident review | 1.44 | gdpval | 4729.4 | 0.897 | 0.9962 | 0.4416 | 13.2–11842.2 |
| 22887a | LIVE | one release made during contact | 0.90 | sopbench | 1161.7 | 0.963 | 0.9999 | 0.7206 | 0.6–316.8 |
| 22887b | DISC | one release request fulfilled | 3.60 | healthadminbench | 46.1 | 0.399 | 0.1827 | 0.0032 | 8.2–24.9 |
| 22888a | DISC | one coding or diagnosis clarification issue resolved or refe | 4.54 | healthadminbench | 46.1 | 0.399 | 0.1611 | 0.0092 | 2.5–20.3 |
| 22889a | DISC | one electronic patient record retrieved for a requester | 3.19 | healthadminbench | 46.1 | 0.688 | 0.6419 | 0.0649 | 1.1–18.6 |
| 22890a | DISC | one record reviewed | 4.68 | healthadminbench | 46.1 | 0.505 | 0.1839 | 0.0028 | 6.8–18.0 |
| 22891b | DISC | one batch of scans indexed and checked | 1.85 | healthadminbench | 46.1 | 0.363 | 0.409 | 0.0306 | 2.4–50.9 |
| 22892a | LIVE | one appointment booked during contact | 2.24 | tau_voice | 126.2 | 0.948 | 1.0 | 0.7162 | 0.5–73.1 |
| 22892b | DISC | one batch of appointments scheduled | 1.49 | sopbench | 1161.7 | 0.859 | 0.9999 | 0.4464 | 3.4–1748.8 |
| 22893a | DISC | one report transcribed | 3.74 | gdpval | 4729.4 | 0.97 | 1.0 | 0.4406 | 2.3–1076.4 |
