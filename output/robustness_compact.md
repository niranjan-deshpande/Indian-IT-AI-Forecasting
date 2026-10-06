| config                                            | S1-S2     | S1-S3        | S1-S4        | S2-S3      | S2-S4     | S3-S4        |
|:--------------------------------------------------|:----------|:-------------|:-------------|:-----------|:----------|:-------------|
| baseline                                          | 0.95 (2q) | 0.77 (never) | 0.85 (3q)    | 0.96 (2q)  | 0.97 (2q) | 0.86 (4q)    |
| noise x0.5                                        | 0.99 (1q) | 0.92 (3q)    | 0.88 (2q)    | 1.00 (2q)  | 1.00 (1q) | 0.95 (2q)    |
| noise x2.0                                        | 0.86 (4q) | 0.65 (never) | 0.79 (never) | 0.85 (5q)  | 0.86 (4q) | 0.76 (never) |
| effect 2.0%/yr                                    | 0.82 (8q) | 0.64 (never) | 0.70 (never) | 0.81 (9q)  | 0.82 (5q) | 0.70 (never) |
| effect 6.0%/yr                                    | 0.99 (2q) | 0.87 (4q)    | 0.94 (2q)    | 1.00 (2q)  | 1.00 (2q) | 0.94 (2q)    |
| labor cut also sluggish (lam_labor=0.5)           | 0.96 (2q) | 0.72 (never) | 0.85 (3q)    | 0.96 (3q)  | 0.97 (2q) | 0.84 (4q)    |
| partial pass-through (kappa=0.5)                  | 0.97 (2q) | 0.86 (4q)    | 0.85 (3q)    | 0.81 (10q) | 0.97 (2q) | 0.89 (3q)    |
| no nuisance drifts (tau=0)                        | 0.99 (2q) | 0.81 (11q)   | 0.98 (2q)    | 0.99 (2q)  | 0.99 (2q) | 0.97 (3q)    |
| wide common-drift prior (tau_b=4)                 | 0.93 (3q) | 0.76 (never) | 0.84 (3q)    | 0.94 (3q)  | 0.95 (2q) | 0.85 (4q)    |
| Part-4 timing: observe from quarter 6 after onset | 0.96 (1q) | 0.73 (never) | 0.84 (1q)    | 0.97 (1q)  | 0.97 (1q) | 0.84 (2q)    |
| AR(1) persistence +0.07 (small-sample bias)       | 0.94 (2q) | 0.74 (never) | 0.84 (3q)    | 0.93 (3q)  | 0.94 (2q) | 0.83 (4q)    |
| pre-COVID calibration                             | 0.96 (2q) | 0.77 (never) | 0.89 (2q)    | 0.96 (3q)  | 0.97 (2q) | 0.88 (3q)    |