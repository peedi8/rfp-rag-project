# checkpoint_04_smoke.md

## Smoke Results

Status: pass

- L102 no-API fixture run passed `39/39`.
- L102 single qv8_a11 top5 probe completed with abstention `1.0`, latency `2.44s`, observed cost `$0.000002`.
- L103 full qv8 top5 after guard completed with EDD `98.71`, latency `13.656s`, abstention `1.0`, observed cost `$0.095118`.
- Aggregate summary completed with `rows=2`, `scoreboard_rows=0`, `diagnostic_only_rows=2`.
- `py_compile` passed for generator, evaluator, fixture, registry, worker, and aggregate scripts.
- JSON parse checks passed for the L102 probe file, exposure registry, and four worker contracts.
- No matching experiment processes remain running.
- Diary forbidden-term check passed.

This smoke result confirms artifact integrity and process cleanup. It does not promote L102 or L103 to strict validation.
