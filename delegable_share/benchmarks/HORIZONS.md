# Benchmark horizons (fixed β = 0.84/ln; location from overall scores)

Item times: coders' median estimates, run `main`. Snapshot = best model released by 2026-11-10.
Doubling = OLS on frontier models (blank if fewer than 3 frontier points or no growth).
H today = H latest moved forward to 2026-11-10 at the pooled doubling time (3.5 months; median over benchmarks with >= 4 frontier points).

| Benchmark | grading | items | median item (min) | H latest (min) | model (date, score) | models | own doubling (months) | H today (min) | β 0.6 / 1.0 (today) | decompressed (today) |
|---|---|---|---|---|---|---|---|---|---|---|
| crmarena_pro | exact_answer | 24 | 12.0 | 17.29 | gemini-2.5-pro (2025-03-25, 0.562) | 9 | 4.8 | 829.8 | 3940.28 / 533.36 | 5828.91 |
| eva_bench | state | 24 | 12.0 | 130.29 | Cartesia Managed Agents - GPT 5.5 (2026-10-27, 0.874) | 22 | 3.9 | 142.71 | 364.89 / 98.91 | 222.51 |
| finch | llm_judge | 24 | 40.0 | 24.11 | Claude Opus 4.5 (Claude product agent) (2025-11-24, 0.43) | 8 | 3.2 | 236.57 | 487.5 / 196.8 | 493.23 |
| gdpval | human_expert | 24 | 135.0 | 1230.77 | GPT-5.5 (2026-04-23, 0.849) | 13 | 2.3 | 4550.98 | 16420.93 / 2913.23 | 15257.93 |
| itbench_sre | exact_answer | 24 | 27.5 | 19.53 | Claude Opus 4.7 (Adaptive Reasoning, Max Effort) (2026-04-16, 0.418) | 23 | 2.1 | 75.58 | 107.0 / 70.03 | 150.61 |
| osworld_verified | state | 24 | 4.0 | 82.51 | Intelligence-Indeed Agent (2026-07-25, 0.902) | 66 | 4.1 | 166.59 | 554.35 / 109.28 | 1773.69 |
| sopbench | state | 24 | 6.0 | 25.03 | o4-mini-high (2025-04-16, 0.753) | 23 | 15.6 | 1041.07 | 7068.75 / 576.05 | 7279.93 |
| spreadsheetbench_2 | state | 24 | 55.0 | 22.58 | Claude Opus 4.6 (2026-02-05, 0.349) | 8 | 1.4 | 137.79 | 201.59 / 128.7 | 248.15 |
| starshell | state | 24 | 4.0 | 25.34 | Claude Opus 4.6 (2026-02-05, 0.814) | 6 |  | 154.63 | 604.29 / 97.78 | 470.15 |
| swe_bench_pro | tests | 24 | 75.0 | 132.01 | Muse Spark 1.1 (2026-07-09, 0.615) | 28 | 4.2 | 295.78 | 494.84 / 250.45 | 475.78 |
| sweeper_bench | llm_judge | 24 | 90.0 | 143.19 | Grok 4.6 (2026-08-12, 0.59) | 15 | 0.8 | 257.16 | 380.23 / 226.02 | 356.62 |
| swt_bench | tests | 24 | 20.0 | 339.4 | Claude Sonnet 5.5 + Claude Opus 5.5 (2026-09-28, 0.915) | 12 | 7.4 | 448.96 | 1529.25 / 279.33 | 600.31 |
| tau_banking | state | 24 | 30.0 | 95.62 | PrincipledMachines Cortex 0.1 (2026-11-04, 0.732) | 28 | 3.6 | 99.43 | 160.45 / 82.54 | 115.11 |
| tau_retail_airline | state | 24 | 10.0 | 74.86 | Qwen3.5-397B-A17B (2026-02-16, 0.835) | 21 | 8.2 | 425.27 | 1734.52 / 263.74 | 1338.43 |
| tau_telecom | state | 24 | 17.0 | 2099.82 | Qwen3-Max-Thinking (2026-01-23, 0.983) | 17 | 1.3 | 13944.6 | 188620.84 / 5396.95 | 44894.47 |
| tau_voice | state | 24 | 12.0 | 114.15 | Pine Voice 1.0 (2026-10-26, 0.863) | 20 | 2.8 | 125.85 | 308.46 / 88.65 | 182.68 |
| terminal_bench_1 | tests | 24 | 27.5 | 72.11 | Claude Sonnet 4.5 (2025-09-29, 0.645) | 6 | 5.3 | 1018.54 | 3509.57 / 705.04 | 6600.92 |
| terminal_bench_2 | tests | 24 | 52.5 | 1019.25 | Claude Opus 4.7 (2026-04-16, 0.909) | 27 | 1.6 | 3944.46 | 18419.21 / 2301.39 | 23677.53 |
| workarena_l1 | state | 24 | 3.0 | 44.06 | Gemini-3-Flash-preview (2025-12-17, 0.903) | 26 | 3.5 | 372.23 | 2353.69 / 197.18 | 1265.99 |
| workarena_pp | state | 24 | 12.0 | 7.23 | GPT-5 (2025-08-07, 0.405) | 12 | 2.6 | 144.17 | 367.27 / 113.84 | 499.92 |
