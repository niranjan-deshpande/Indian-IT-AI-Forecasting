# Benchmark horizons (fixed β = 0.84/ln; location from overall scores)

Item times: coders' median estimates, run `main,bpo,comp`. Snapshot = best model released by 2026-11-10.
Doubling = OLS on frontier models (blank if fewer than 3 frontier points or no growth).
H today = H latest moved forward to 2026-11-10 at the pooled doubling time (3.4 months; median over benchmarks with >= 4 frontier points).

| Benchmark | grading | items | median item (min) | H latest (min) | model (date, score) | models | own doubling (months) | H today (min) | β 0.6 / 1.0 (today) | decompressed (today) |
|---|---|---|---|---|---|---|---|---|---|---|
| apex_accounting | llm_judge | 10 | 95.0 | 19.16 | Gemini 4 Argon (high) (2026-09-30, 0.238) | 49 | 3.8 | 25.21 | 16.23 / 30.11 | 17.05 |
| apex_agents | llm_judge | 24 | 60.0 | 449.38 | Gemini 4 Carbon (2026-10-28, 0.842) | 59 | 2.1 | 490.26 | 1095.14 / 358.07 | 723.23 |
| crmarena_pro | exact_answer | 24 | 12.0 | 17.29 | gemini-2.5-pro (2025-03-25, 0.562) | 9 | 4.8 | 929.87 | 4382.04 / 533.36 | 4181.85 |
| dba_bench | state | 24 | 47.5 | 14.14 | GPT-5.5 (2026-04-23, 0.271) | 6 |  | 54.34 | 55.59 / 54.84 | 70.3 |
| dualentry | exact_answer | 8 | 3.0 | 47.2 | Gemini 4 Argon [Oct2026] (2026-10-13, 0.911) | 38 | 6.7 | 56.94 | 182.76 / 35.89 | 67.62 |
| eva_bench | state | 24 | 12.0 | 130.29 | Cartesia Managed Agents - GPT 5.5 (2026-10-27, 0.874) | 22 | 3.9 | 143.1 | 365.8 / 98.91 | 220.78 |
| finch | llm_judge | 24 | 40.0 | 24.11 | Claude Opus 4.5 (Claude product agent) (2025-11-24, 0.43) | 8 | 3.2 | 253.0 | 519.04 / 196.8 | 405.49 |
| gdpval | human_expert | 24 | 135.0 | 1230.77 | GPT-5.5 (2026-04-23, 0.849) | 13 | 2.3 | 4729.43 | 17021.11 / 2913.23 | 13638.81 |
| healthadminbench | state | 24 | 13.5 | 7.17 | Claude Opus 4.6 (Anthropic computer-use tool) (2026-02-05, 0.363) | 5 |  | 46.14 | 69.69 / 40.2 | 79.25 |
| itbench_sre | exact_answer | 24 | 27.5 | 19.53 | Claude Opus 4.7 (Adaptive Reasoning, Max Effort) (2026-04-16, 0.418) | 23 | 2.1 | 78.65 | 111.05 / 70.03 | 134.1 |
| jobbench | llm_judge | 24 | 360.0 | 1500.62 | Claude Opus 5.5 (2026-09-22, 0.754) | 40 | 3.9 | 2083.5 | 3985.31 / 1617.01 | 2855.9 |
| online_mind2web | llm_judge | 24 | 4.0 | 146.63 | Hark (Hark Handoff) (2026-08-15, 0.953) | 20 | 3.3 | 262.59 | 1330.62 / 139.18 | 442.42 |
| osworld_verified | state | 24 | 4.0 | 82.51 | Intelligence-Indeed Agent (2026-07-25, 0.902) | 66 | 4.1 | 170.07 | 565.14 / 109.28 | 1669.94 |
| sopbench | state | 24 | 6.0 | 25.03 | o4-mini-high (2025-04-16, 0.753) | 23 | 15.6 | 1161.71 | 7830.44 / 576.05 | 5287.39 |
| spider2 | exact_answer | 24 | 35.0 | 963.32 | Gemini 3 Pro Preview [system: QUVI-3 (DAQUV)] (2025-11-18, 0.942) | 22 | 2.4 | 10523.16 | 92046.07 / 4607.66 | 29628.55 |
| spreadsheetbench_2 | state | 24 | 55.0 | 22.58 | Claude Opus 4.6 (2026-02-05, 0.349) | 8 | 1.4 | 145.32 | 211.85 / 128.7 | 212.48 |
| starshell | state | 24 | 4.0 | 25.34 | Claude Opus 4.6 (2026-02-05, 0.814) | 6 |  | 163.08 | 635.05 / 97.78 | 402.58 |
| swe_bench_pro | tests | 24 | 75.0 | 132.01 | Muse Spark 1.1 (2026-07-09, 0.615) | 28 | 4.2 | 302.88 | 505.92 / 250.45 | 443.97 |
| swe_bench_verified | tests | 24 | 40.0 | 2349.46 | Claude Opus 5 (2026-07-24, 0.96) | 55 | 3.5 | 4875.36 | 27534.14 / 2491.59 | 17427.17 |
| swe_lancer | tests | 24 | 90.0 | 147.37 | ChatGPT agent (2025-07-17, 0.6) | 12 | 2.7 | 3693.62 | 14220.81 / 2269.47 | 11886.13 |
| sweeper_bench | llm_judge | 24 | 90.0 | 143.19 | Grok 4.6 (2026-08-12, 0.59) | 15 | 0.8 | 261.63 | 386.39 / 226.02 | 339.15 |
| swt_bench | tests | 24 | 20.0 | 339.4 | Claude Sonnet 5.5 + Claude Opus 5.5 (2026-09-28, 0.915) | 12 | 7.4 | 452.67 | 1541.04 / 279.33 | 586.07 |
| tau_banking | state | 24 | 30.0 | 95.62 | PrincipledMachines Cortex 0.1 (2026-11-04, 0.732) | 28 | 3.6 | 99.54 | 160.62 / 82.54 | 114.73 |
| tau_retail_airline | state | 24 | 10.0 | 74.86 | Qwen3.5-397B-A17B (2026-02-16, 0.835) | 21 | 8.2 | 447.56 | 1819.24 / 263.74 | 1153.13 |
| tau_telecom | state | 24 | 17.0 | 2099.82 | Qwen3-Max-Thinking (2026-01-23, 0.983) | 17 | 1.3 | 14743.11 | 198682.92 / 5396.95 | 38164.45 |
| tau_voice | state | 24 | 12.0 | 114.15 | Pine Voice 1.0 (2026-10-26, 0.863) | 20 | 2.8 | 126.21 | 309.29 / 88.65 | 181.16 |
| terminal_bench_1 | tests | 24 | 27.5 | 72.11 | Claude Sonnet 4.5 (2025-09-29, 0.645) | 6 | 5.3 | 1101.04 | 3774.17 / 705.04 | 5259.62 |
| terminal_bench_2 | tests | 24 | 52.5 | 1019.25 | Claude Opus 4.7 (2026-04-16, 0.909) | 27 | 1.6 | 4104.62 | 19116.31 / 2301.39 | 21082.42 |
| terminal_bench_4 | tests | 24 | 240.0 | 554.58 | Claude Opus 5.5 (2026-09-22, 0.658) | 23 | 1.5 | 769.99 | 1173.2 / 655.16 | 1042.67 |
| theagentcompany | state | 24 | 20.0 | 13.18 | DeepSeek-V3.2 (2025-09-29, 0.429) | 16 | 3.3 | 201.24 | 480.68 / 147.7 | 367.06 |
| ui_cube | state | 24 | 1.0 | 2.76 | UIPathScreenAgent / GPT-5 (2025-08-07, 0.588) | 4 | 6.1 | 60.1 | 216.52 / 37.56 | 369.7 |
| vals_finance_agent | llm_judge | 24 | 13.5 | 33.3 | Claude Opus 4.7 [FA v1.1] (2026-04-16, 0.644) | 110 | 4.9 | 134.1 | 290.05 / 100.99 | 352.9 |
| workarena_l1 | state | 24 | 3.0 | 44.06 | Gemini-3-Flash-preview (2025-12-17, 0.903) | 26 | 3.5 | 396.34 | 2495.69 / 197.18 | 1054.21 |
| workarena_pp | state | 24 | 12.0 | 7.23 | GPT-5 (2025-08-07, 0.405) | 12 | 2.6 | 157.43 | 398.72 / 113.84 | 386.73 |
