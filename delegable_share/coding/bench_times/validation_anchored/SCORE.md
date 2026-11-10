# Blind time estimates vs published times — validation_anchored

Estimate = median of three coders (two Sonnet, one Terra). Ratio = estimate / published.

## swe-bench-verified (48 items)
- Spearman with bucket order: 0.69
- Estimate inside the published bucket: 24/48
  - bucket 0–15 min: n 15, median estimate 25 min (range 10–90)
  - bucket 15–60 min: n 15, median estimate 75 min (range 25–150)
  - bucket 60–240 min: n 15, median estimate 90 min (range 35–180)
  - bucket 240–∞ min: n 3, median estimate 150 min (range 90–240)

## terminal-bench-2.0 (33 items)
- Spearman rank correlation: 0.67
- Median ratio (bias): ×1.00; middle half ×0.40–×2.74
- Within 2× of published: 14/33; within 3×: 22/33
  - coder s1: median ratio ×1.00, Spearman 0.64
  - coder s2: median ratio ×1.00, Spearman 0.66
  - coder t: median ratio ×1.67, Spearman 0.55
