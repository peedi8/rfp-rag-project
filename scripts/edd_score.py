"""EDD(Eval/Evidence Driven Development) score helpers.

This project uses EDD as a compact comparison score for experiment rows.
The raw metrics remain the source of truth; EDD is only a decision aid.
"""
from __future__ import annotations


WEIGHTS = {
    "retrieval_coverage_avg": 0.20,
    "hit_all_targets_rate": 0.10,
    "mrr": 0.15,
    "groundedness_avg": 0.20,
    "relevance_avg": 0.20,
    "abstention_accuracy": 0.10,
    "latency_score": 0.05,
}


def _num(value, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def latency_score(latency_sec, best: float = 8.0, worst: float = 30.0) -> float:
    """Normalize latency to 0..1. <=8s is full score, >=30s is zero."""
    latency = _num(latency_sec, default=worst)
    if latency <= best:
        return 1.0
    if latency >= worst:
        return 0.0
    return _clamp((worst - latency) / (worst - best))


def components(metrics: dict) -> dict[str, float]:
    return {
        "retrieval_coverage_avg": _clamp(_num(metrics.get("retrieval_coverage_avg"))),
        "hit_all_targets_rate": _clamp(_num(metrics.get("hit_all_targets_rate"))),
        "mrr": _clamp(_num(metrics.get("mrr"))),
        "groundedness_avg": _clamp(_num(metrics.get("groundedness_avg")) / 5.0),
        "relevance_avg": _clamp(_num(metrics.get("relevance_avg")) / 5.0),
        "abstention_accuracy": _clamp(_num(metrics.get("abstention_accuracy"))),
        "latency_score": latency_score(metrics.get("latency_avg_sec")),
    }


def edd_score(metrics: dict) -> float:
    vals = components(metrics)
    score = sum(vals[k] * weight for k, weight in WEIGHTS.items()) * 100
    score -= _clamp(_num(metrics.get("false_abstention_rate"))) * 15
    score -= _clamp(_num(metrics.get("empty_answer_rate"))) * 25
    return round(max(0.0, score), 2)


def add_edd_columns(row: dict) -> dict:
    vals = components(row)
    out = dict(row)
    out["edd_score"] = edd_score(row)
    for key, value in vals.items():
        out[f"edd_{key}"] = round(value, 4)
    return out
