"""Token usage and local USD cost helpers for experiment traces."""
from __future__ import annotations

from typing import Any


MODEL_PRICES_PER_MTOK = {
    "gpt-5-mini": {"input": 0.75, "output": 4.50},
    "text-embedding-3-small": {"input": 0.02, "output": 0.0},
}


def price_for_model(model: str) -> dict[str, float] | None:
    return MODEL_PRICES_PER_MTOK.get(model)


def usage_from_response(resp: Any) -> dict[str, int | None]:
    usage_obj = getattr(resp, "usage", None)
    if usage_obj is None:
        return {"prompt_tokens": None, "completion_tokens": None, "total_tokens": None}
    return {
        "prompt_tokens": getattr(usage_obj, "prompt_tokens", None),
        "completion_tokens": getattr(usage_obj, "completion_tokens", None),
        "total_tokens": getattr(usage_obj, "total_tokens", None),
    }


def cost_usd(model: str, prompt_tokens: int | None, completion_tokens: int | None) -> float | None:
    price = price_for_model(model)
    if price is None or prompt_tokens is None:
        return None
    completion_tokens = completion_tokens or 0
    return round(
        (prompt_tokens / 1_000_000) * price["input"]
        + (completion_tokens / 1_000_000) * price["output"],
        6,
    )


def traced_call(
    *,
    operation: str,
    model: str,
    resp: Any,
    elapsed_sec: float | None = None,
    meta: dict | None = None,
) -> dict:
    usage = usage_from_response(resp)
    row = {
        "operation": operation,
        "model": model,
        "usage": usage,
        "cost_usd": cost_usd(model, usage.get("prompt_tokens"), usage.get("completion_tokens")),
        "cost_basis": "local_price_table",
    }
    if elapsed_sec is not None:
        row["elapsed_sec"] = round(elapsed_sec, 3)
    if meta:
        row["meta"] = meta
    return row


def sum_cost(rows: list[dict]) -> float | None:
    values = [r.get("cost_usd") for r in rows if r.get("cost_usd") is not None]
    if not values:
        return None
    return round(sum(float(v) for v in values), 6)
