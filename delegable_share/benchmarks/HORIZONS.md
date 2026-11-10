# Benchmark horizons (fixed β = 0.84/ln; location from overall scores)

Item times: coders' median estimates, run `main,bpo`. Snapshot = best model released by 2026-11-10.
Doubling = OLS on frontier models (blank if fewer than 3 frontier points or no growth).
H today = H latest moved forward to 2026-11-10 at the pooled doubling time (3.5 months; median over benchmarks with >= 4 frontier points).

| Benchmark | grading | items | median item (min) | H latest (min) | model (date, score) | models | own doubling (months) | H today (min) | β 0.6 / 1.0 (today) | decompressed (today) |
|---|---|---|---|---|---|---|---|---|---|---|
| apex_accounting | llm_judge | 10 | 95.0 | 19.16 | Gemini 4 Argon (high) (2026-09-30, 0.238) | 49 | 3.8 | 25.02 | 16.23 / 30.02 | 17.44 |
| crmarena_pro | exact_answer | 24 | 12.0 | 17.29 | gemini-2.5-pro (2025-03-25, 0.562) | 9 | 4.8 | 829.8 | 4382.04 / 510.42 | 5828.91 |
| dba_bench | state | 24 | 47.5 | 14.14 | GPT-5.5 (2026-04-23, 0.271) | 6 |  | 52.29 | 55.59 / 54.03 | 78.64 |
| dualentry | exact_answer | 8 | 3.0 | 47.2 | Gemini 4 Argon [Oct2026] (2026-10-13, 0.911) | 38 | 6.7 | 56.63 | 182.76 / 35.82 | 68.68 |
| eva_bench | state | 24 | 12.0 | 130.29 | Cartesia Managed Agents - GPT 5.5 (2026-10-27, 0.874) | 22 | 3.9 | 142.71 | 365.8 / 98.81 | 222.51 |
| finch | llm_judge | 24 | 40.0 | 24.11 | Claude Opus 4.5 (Claude product agent) (2025-11-24, 0.43) | 8 | 3.2 | 236.57 | 519.04 / 191.76 | 493.23 |
| gdpval | human_expert | 24 | 135.0 | 1230.77 | GPT-5.5 (2026-04-23, 0.849) | 13 | 2.3 | 4550.98 | 17021.11 / 2870.27 | 15257.93 |
| healthadminbench | state | 24 | 13.5 | 7.17 | Claude Opus 4.6 (Anthropic computer-use tool) (2026-02-05, 0.363) | 5 |  | 43.75 | 69.69 / 39.38 | 92.55 |
| itbench_sre | exact_answer | 24 | 27.5 | 19.53 | Claude Opus 4.7 (Adaptive Reasoning, Max Effort) (2026-04-16, 0.418) | 23 | 2.1 | 75.58 | 111.05 / 68.96 | 150.61 |
| osworld_verified | state | 24 | 4.0 | 82.51 | Intelligence-Indeed Agent (2026-07-25, 0.902) | 66 | 4.1 | 166.59 | 565.14 / 108.42 | 1773.69 |
| sopbench | state | 24 | 6.0 | 25.03 | o4-mini-high (2025-04-16, 0.753) | 23 | 15.6 | 1041.07 | 7830.44 / 552.17 | 7279.93 |
| spider2 | exact_answer | 24 | 35.0 | 963.32 | Gemini 3 Pro Preview [system: QUVI-3 (DAQUV)] (2025-11-18, 0.942) | 22 | 2.4 | 9828.3 | 92046.07 / 4487.68 | 36161.11 |
| spreadsheetbench_2 | state | 24 | 55.0 | 22.58 | Claude Opus 4.6 (2026-02-05, 0.349) | 8 | 1.4 | 137.79 | 211.85 / 126.09 | 248.15 |
| starshell | state | 24 | 4.0 | 25.34 | Claude Opus 4.6 (2026-02-05, 0.814) | 6 |  | 154.63 | 635.05 / 95.79 | 470.15 |
| swe_bench_pro | tests | 24 | 75.0 | 132.01 | Muse Spark 1.1 (2026-07-09, 0.615) | 28 | 4.2 | 295.78 | 505.92 / 248.16 | 475.78 |
| swe_bench_verified | tests | 24 | 40.0 | 2349.46 | Claude Opus 5 (2026-07-24, 0.96) | 55 | 3.5 | 4774.73 | 27534.14 / 2471.6 | 18520.25 |
| swe_lancer | tests | 24 | 90.0 | 147.37 | ChatGPT agent (2025-07-17, 0.6) | 12 | 2.7 | 3368.84 | 14220.81 / 2190.21 | 15546.32 |
| sweeper_bench | llm_judge | 24 | 90.0 | 143.19 | Grok 4.6 (2026-08-12, 0.59) | 15 | 0.8 | 257.16 | 386.39 / 224.52 | 356.62 |
| swt_bench | tests | 24 | 20.0 | 339.4 | Claude Sonnet 5.5 + Claude Opus 5.5 (2026-09-28, 0.915) | 12 | 7.4 | 448.96 | 1541.04 / 278.44 | 600.31 |
| tau_banking | state | 24 | 30.0 | 95.62 | PrincipledMachines Cortex 0.1 (2026-11-04, 0.732) | 28 | 3.6 | 99.43 | 160.62 / 82.5 | 115.11 |
| tau_retail_airline | state | 24 | 10.0 | 74.86 | Qwen3.5-397B-A17B (2026-02-16, 0.835) | 21 | 8.2 | 425.27 | 1819.24 / 258.58 | 1338.43 |
| tau_telecom | state | 24 | 17.0 | 2099.82 | Qwen3-Max-Thinking (2026-01-23, 0.983) | 17 | 1.3 | 13944.6 | 198682.92 / 5282.12 | 44894.47 |
| tau_voice | state | 24 | 12.0 | 114.15 | Pine Voice 1.0 (2026-10-26, 0.863) | 20 | 2.8 | 125.85 | 309.29 / 88.56 | 182.68 |
| terminal_bench_1 | tests | 24 | 27.5 | 72.11 | Claude Sonnet 4.5 (2025-09-29, 0.645) | 6 | 5.3 | 1018.54 | 3774.17 / 684.14 | 6600.92 |
| terminal_bench_2 | tests | 24 | 52.5 | 1019.25 | Claude Opus 4.7 (2026-04-16, 0.909) | 27 | 1.6 | 3944.46 | 19116.31 / 2266.28 | 23677.53 |
| terminal_bench_4 | tests | 24 | 240.0 | 554.58 | Claude Opus 5.5 (2026-09-22, 0.658) | 23 | 1.5 | 762.81 | 1173.2 / 652.79 | 1071.58 |
| theagentcompany | state | 24 | 20.0 | 13.18 | DeepSeek-V3.2 (2025-09-29, 0.429) | 16 | 3.3 | 186.17 | 480.68 / 143.33 | 460.66 |
| ui_cube | state | 24 | 1.0 | 2.76 | UIPathScreenAgent / GPT-5 (2025-08-07, 0.588) | 4 | 6.1 | 55.04 | 216.52 / 36.3 | 477.92 |
| vals_finance_agent | llm_judge | 24 | 13.5 | 33.3 | Claude Opus 4.7 [FA v1.1] (2026-04-16, 0.644) | 110 | 4.9 | 128.87 | 290.05 / 99.45 | 396.34 |
| workarena_l1 | state | 24 | 3.0 | 44.06 | Gemini-3-Flash-preview (2025-12-17, 0.903) | 26 | 3.5 | 372.23 | 2495.69 / 192.46 | 1265.99 |
| workarena_pp | state | 24 | 12.0 | 7.23 | GPT-5 (2025-08-07, 0.405) | 12 | 2.6 | 144.17 | 398.72 / 110.03 | 499.92 |
