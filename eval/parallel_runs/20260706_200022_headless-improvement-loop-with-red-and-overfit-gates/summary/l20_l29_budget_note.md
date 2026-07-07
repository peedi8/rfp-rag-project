# L20-L29 Budget Note

- user cap: `$14.00`
- hard-stop policy used for calibration calls: `$13.00`
- model pricing assumption: `gpt-5-mini` input `$0.75 / 1M`, output `$4.50 / 1M`

## Recorded Usage

The calibration runner records API usage per case.

- L20 original calibration actual cost: `$0.019861`
- L22 scale-guard original-pack rerun actual cost: `$0.022776`
- L24 strict-pack calibration actual cost: `$0.020890`
- recorded calibration total: `$0.063527`

## V4 Eval Cost Bound

The v4 evaluator currently does not persist OpenAI response usage, so L25-L28 cannot be reported as exact billed usage from local artifacts.

For a conservative bound:

- v4 runs: `4`
- cases per run: `10`
- answer turns per run: `11`
- answer calls total: `44`
- judge calls total: `36`
- conservative answer output ceiling: first call plus possible retry, `3072 + 6144` tokens per answer call
- judge output ceiling: `2400` tokens per judge call

This ceiling is still far below the `$14` cap for `gpt-5-mini`. The exact total should be considered "under budget by design, not exact-billed" unless future evaluator runs persist API usage like the calibration runner.

## Follow-up

Add usage capture to the main evaluator before any future budget-sensitive long run.
