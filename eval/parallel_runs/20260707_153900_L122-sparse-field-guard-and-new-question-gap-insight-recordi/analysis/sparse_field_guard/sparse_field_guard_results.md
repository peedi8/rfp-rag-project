# L122 Sparse-Field Guard

No-API sparse-field readiness guard; not an answer run and not an EDD point.

## Summary
- case_count: `8`
- field_group_count: `31`
- source_visible_groups: `31`
- not_found_expected_groups: `0`
- csv_source_visible_groups: `4`
- csv_not_found_expected_groups: `27`
- cases_with_not_found_expected: `0`
- fixture_status: `pass`

## Policy
- This is a no-API preflight and scoring guard, not an answer-quality or EDD point.
- Secondary technical variants remain diagnostic-only.
- A not-found field is not a model failure by itself. It becomes a failure only if the answer fills the empty field with unsupported detail or omits the required absence caveat.

## Cases
| case | source | basis | present | not-found expected |
|---|---|---|---:|---:|
| l121_Q046_technical_add_transfer | Q046 | raw_file_text | 3 | 0 |
| l121_Q047_technical_add_transfer | Q047 | raw_file_text | 5 | 0 |
| l121_Q048_technical_add_transfer | Q048 | raw_file_text | 4 | 0 |
| l121_Q049_technical_add_transfer | Q049 | raw_file_text | 5 | 0 |
| l121_Q050_technical_add_transfer | Q050 | raw_file_text | 5 | 0 |
| l121_Q051_technical_add_transfer | Q051 | raw_file_text | 4 | 0 |
| l121_Q052_technical_add_transfer | Q052 | raw_file_text | 4 | 0 |
| l121_Q053_technical_add_transfer | Q053 | raw_file_text | 1 | 0 |

## Not-Found Field Groups
| case | field | status | hit tokens |
|---|---|---|---|
