# Blind time estimates vs published times — validation

Estimate = median of three coders (two Sonnet, one Terra). Ratio = estimate / published.

## swe-bench-verified (48 items)
- Spearman with bucket order: 0.71
- Estimate inside the published bucket: 24/48
  - bucket 0–15 min: n 15, median estimate 20 min (range 12–60)
  - bucket 15–60 min: n 15, median estimate 60 min (range 25–90)
  - bucket 60–240 min: n 15, median estimate 90 min (range 25–150)
  - bucket 240–∞ min: n 3, median estimate 120 min (range 60–240)

## terminal-bench-2.0 (34 items)
- Spearman rank correlation: 0.64
- Median ratio (bias): ×0.83; middle half ×0.32–×2.41
- Within 2× of published: 12/34; within 3×: 23/34
  - coder s1: median ratio ×0.75, Spearman 0.65
  - coder s2: median ratio ×0.83, Spearman 0.60
  - coder t: median ratio ×2.00, Spearman 0.57
