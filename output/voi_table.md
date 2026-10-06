| label                                                                     |   ('S1-S3', 5) |   ('S1-S3', 0) |   ('S1-S4', 5) |   ('S1-S4', 0) |   ('S3-S4', 5) |   ('S3-S4', 0) |
|:--------------------------------------------------------------------------|---------------:|---------------:|---------------:|---------------:|---------------:|---------------:|
| current public data (baseline)                                            |           0.74 |           0.77 |           0.86 |           0.86 |           0.84 |           0.85 |
| + hourly rate p/a (control), sd 1                                         |           0.74 |           0.78 |           0.86 |           0.87 |           0.85 |           0.88 |
| + output-price index, sd 0.5                                              |           0.95 |           0.96 |           0.92 |           0.91 |           0.99 |           0.99 |
| + output-price index, sd 1                                                |           0.88 |           0.89 |           0.87 |           0.88 |           0.96 |           0.96 |
| + output-price index, sd 2                                                |           0.79 |           0.83 |           0.85 |           0.86 |           0.89 |           0.9  |
| + output-price index, sd 4                                                |           0.75 |           0.79 |           0.85 |           0.86 |           0.86 |           0.86 |
| + output-price index, sd 1, cyclical eta=0.5                              |           0.74 |           0.78 |           0.94 |           0.93 |           0.92 |           0.93 |
| + output-price index, sd 1, visibility omega=0.25                         |           0.74 |           0.79 |           0.87 |           0.88 |           0.89 |           0.89 |
| + occupation contrast (8 firms), sd 2                                     |           1    |           0.99 |           0.86 |           0.87 |           1    |           1    |
| + occupation contrast (8 firms), sd 4                                     |           0.98 |           0.98 |           0.86 |           0.87 |           0.98 |           0.98 |
| + occupation contrast (8 firms), sd 8                                     |           0.9  |           0.9  |           0.86 |           0.87 |           0.93 |           0.94 |
| + occupation contrast (8 firms), sd 16                                    |           0.82 |           0.83 |           0.86 |           0.87 |           0.88 |           0.9  |
| + occupation contrast sd 4, demand confound zeta=0.3                      |           0.94 |           0.94 |           0.89 |           0.9  |           0.98 |           0.98 |
| + occupation contrast sd 4, GCC confound xi=0.5                           |           0.98 |           0.98 |           0.92 |           0.91 |           0.94 |           0.95 |
| + affiliated trade share (annual), sd 2                                   |           0.74 |           0.79 |           0.89 |           0.9  |           0.89 |           0.9  |
| + affiliated trade share (annual), sd 5                                   |           0.74 |           0.79 |           0.85 |           0.87 |           0.86 |           0.87 |
| + affiliated trade share (annual), sd 10                                  |           0.74 |           0.79 |           0.85 |           0.86 |           0.85 |           0.87 |
| + 4 more Indian firms (exposure 0.6-1.4)                                  |           0.8  |           0.82 |           0.86 |           0.87 |           0.88 |           0.89 |
| + 8 more Indian firms (exposure 0.6-1.4)                                  |           0.84 |           0.85 |           0.86 |           0.87 |           0.9  |           0.92 |
| combined: price sd 2 + occupation sd 8 + trade sd 5                       |           0.92 |           0.92 |           0.88 |           0.88 |           0.96 |           0.96 |
| + LCA occupation contrast, MEASURED per-firm noise                        |           0.76 |         nan    |           0.86 |         nan    |           0.86 |         nan    |
| + LCA occupation contrast, measured noise, attenuation 0.3 (validation r) |           0.74 |         nan    |           0.86 |         nan    |           0.85 |         nan    |
| + LCA occupation contrast, 2 best-coded firms only (HCL, TechM)           |           0.76 |         nan    |           0.86 |         nan    |           0.86 |         nan    |