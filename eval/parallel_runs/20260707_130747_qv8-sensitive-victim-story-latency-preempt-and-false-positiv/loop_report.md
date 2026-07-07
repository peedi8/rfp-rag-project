# L104-L105 Loop Points

| point | type | EDD | latency | decision |
|---|---|---:|---:|---|
| L98 | diagnostic raw | 95.81 | 17.645s | baseline only |
| L99 | measurement correction | 97.81 | 17.645s | do not promote |
| L103 | diagnostic rerun | 98.71 | 13.656s | candidate keep |
| L104 | no-judge targeted probe | 60.00 | 2.120s | targeted success |
| L105 | diagnostic rerun | 99.13 | 11.813s | diagnostic best, not strict |

L105 is the best qv8 diagnostic point so far, but it is not strict validation. The next loop should leave qv8 score chasing and test whether the same guards behave on non-qv8 unsupported-result and sensitive-story prompts.
