from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any, Iterable


class EvaluationError(ValueError):
    """Raised when an evaluation input does not satisfy the JSONL contract."""


_TOKEN_RE = re.compile(r"\w+", re.UNICODE)


def _tokens(text: str) -> set[str]:
    return {token.casefold() for token in _TOKEN_RE.findall(text)}


def _normalise(text: str) -> str:
    return " ".join(text.casefold().split())


def _read_jsonl(path: Path, kind: str) -> tuple[list[dict[str, Any]], bytes]:
    raw = path.read_bytes()
    records: list[dict[str, Any]] = []
    for line_no, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise EvaluationError(f"{kind} line {line_no} is not valid JSON: {exc.msg}") from exc
        if not isinstance(value, dict):
            raise EvaluationError(f"{kind} line {line_no} must be a JSON object")
        records.append(value)
    return records, raw


def _require_string(value: Any, field: str, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvaluationError(f"{context}.{field} must be a non-empty string")
    return value


def _require_string_list(value: Any, field: str, context: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise EvaluationError(f"{context}.{field} must be a list of non-empty strings")
    return value


def _validate_gold(record: dict[str, Any], context: str) -> None:
    _require_string(record.get("id"), "id", context)
    _require_string_list(record.get("relevant_ids", []), "relevant_ids", context)
    claims = record.get("claims", [])
    if not isinstance(claims, list):
        raise EvaluationError(f"{context}.claims must be a list")
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            raise EvaluationError(f"{context}.claims[{index}] must be an object")
        _require_string(claim.get("text"), "text", f"{context}.claims[{index}]")
        _require_string_list(claim.get("citation_ids", []), "citation_ids", f"{context}.claims[{index}]")


def _validate_prediction(record: dict[str, Any], context: str) -> None:
    _require_string(record.get("id"), "id", context)
    _require_string_list(record.get("retrieved_ids", []), "retrieved_ids", context)
    claims = record.get("claims", [])
    if not isinstance(claims, list):
        raise EvaluationError(f"{context}.claims must be a list")
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            raise EvaluationError(f"{context}.claims[{index}] must be an object")
        _require_string(claim.get("text"), "text", f"{context}.claims[{index}]")
        _require_string_list(claim.get("citation_ids", []), "citation_ids", f"{context}.claims[{index}]")


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def _semantic_matches(
    predictions: list[dict[str, Any]],
    gold_claims: list[dict[str, Any]],
    threshold: float,
) -> dict[int, int]:
    """Match claims one-to-one, allowing later predictions to displace a match.

    A simple greedy scan can consume a gold claim that is the only viable match
    for a later prediction. Kuhn-style augmentation keeps the metric
    deterministic while maximising the number of threshold-qualified matches.
    Candidate edges are considered by descending lexical similarity and then
    by source order for stable tie-breaking.
    """
    candidates: dict[int, list[tuple[float, int]]] = {}
    for prediction_index, prediction in enumerate(predictions):
        predicted_tokens = _tokens(prediction["text"])
        scored: list[tuple[float, int]] = []
        for gold_index, gold in enumerate(gold_claims):
            gold_tokens = _tokens(gold["text"])
            union = predicted_tokens | gold_tokens
            score = len(predicted_tokens & gold_tokens) / len(union) if union else 1.0
            if score >= threshold:
                scored.append((score, gold_index))
        candidates[prediction_index] = sorted(scored, key=lambda item: (-item[0], item[1]))

    gold_to_prediction: dict[int, int] = {}

    def augment(prediction_index: int, seen: set[int]) -> bool:
        for _, gold_index in candidates[prediction_index]:
            if gold_index in seen:
                continue
            seen.add(gold_index)
            previous = gold_to_prediction.get(gold_index)
            if previous is None or augment(previous, seen):
                gold_to_prediction[gold_index] = prediction_index
                return True
        return False

    for prediction_index in range(len(predictions)):
        augment(prediction_index, set())
    return {prediction_index: gold_index for gold_index, prediction_index in gold_to_prediction.items()}


def evaluate_records(
    gold_records: list[dict[str, Any]],
    prediction_records: list[dict[str, Any]],
    *,
    k: int = 3,
    seed: int = 0,
    input_checksum: str | None = None,
    semantic_threshold: float = 0.5,
) -> dict[str, Any]:
    """Evaluate provider output against a gold set using deterministic lexical metrics."""
    if not isinstance(k, int) or isinstance(k, bool) or k < 1:
        raise EvaluationError("k must be at least 1")
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise EvaluationError("seed must be an integer")
    if (
        not isinstance(semantic_threshold, (int, float))
        or isinstance(semantic_threshold, bool)
        or not math.isfinite(semantic_threshold)
        or not 0 <= semantic_threshold <= 1
    ):
        raise EvaluationError("semantic_threshold must be between 0 and 1")
    for index, record in enumerate(gold_records):
        _validate_gold(record, f"gold[{index}]")
    for index, record in enumerate(prediction_records):
        _validate_prediction(record, f"predictions[{index}]")

    gold_by_id = {record["id"]: record for record in gold_records}
    pred_by_id = {record["id"]: record for record in prediction_records}
    if len(gold_by_id) != len(gold_records) or len(pred_by_id) != len(prediction_records):
        raise EvaluationError("record ids must be unique within each input")
    unknown = sorted(set(pred_by_id) - set(gold_by_id))
    if unknown:
        raise EvaluationError(f"predictions contain unknown ids: {', '.join(unknown)}")

    recall_values: list[float] = []
    exact_covered = exact_total = semantic_covered = semantic_total = 0
    unsupported = total_claims = 0
    for gold in gold_records:
        prediction = pred_by_id.get(gold["id"], {"retrieved_ids": [], "claims": []})
        relevant = set(gold["relevant_ids"])
        retrieved = prediction["retrieved_ids"][:k]
        recall_values.append(len(relevant.intersection(retrieved)) / len(relevant) if relevant else 0.0)

        gold_claims = gold["claims"]
        exact_matches: set[int] = set()
        semantic_matches = _semantic_matches(prediction["claims"], gold_claims, semantic_threshold)
        for prediction_index, claim in enumerate(prediction["claims"]):
            total_claims += 1
            predicted_citations = set(claim["citation_ids"])
            exact_index = next(
                (
                    index
                    for index, gold_claim in enumerate(gold_claims)
                    if index not in exact_matches
                    and _normalise(gold_claim["text"]) == _normalise(claim["text"])
                ),
                None,
            )
            if exact_index is not None:
                exact_matches.add(exact_index)
                exact_total += 1
                exact_covered += bool(predicted_citations.intersection(gold_claims[exact_index]["citation_ids"]))

            matched_index = semantic_matches.get(prediction_index)
            candidate: tuple[float, int, dict[str, Any]] | None = None
            if matched_index is not None:
                matched = gold_claims[matched_index]
                predicted_tokens = _tokens(claim["text"])
                gold_tokens = _tokens(matched["text"])
                union = predicted_tokens | gold_tokens
                score = len(predicted_tokens & gold_tokens) / len(union) if union else 1.0
                candidate = (score, matched_index, matched)
            if candidate is not None:
                semantic_total += 1
                matched = candidate[2]
                semantic_covered += bool(predicted_citations.intersection(matched["citation_ids"]))
            if candidate is None or not predicted_citations.intersection(candidate[2]["citation_ids"]):
                unsupported += 1

    return {
        "version": "1.0",
        "seed": seed,
        "input_checksum": input_checksum or "",
        "records": len(gold_records),
        "metrics": {
            "recall_at_k": {"k": k, "value": _mean(recall_values)},
            "citation_coverage": {
                "exact": {"covered": exact_covered, "total": exact_total, "value": exact_covered / exact_total if exact_total else 0.0},
                "semantic_lite": {
                    "threshold": semantic_threshold,
                    "covered": semantic_covered,
                    "total": semantic_total,
                    "value": semantic_covered / semantic_total if semantic_total else 0.0,
                },
            },
            "unsupported_claim_rate": unsupported / total_claims if total_claims else 0.0,
            "claims": total_claims,
        },
    }


def evaluate_files(gold_path: str | Path, predictions_path: str | Path, *, k: int = 3, seed: int = 0, semantic_threshold: float = 0.5) -> dict[str, Any]:
    gold, gold_bytes = _read_jsonl(Path(gold_path), "gold")
    predictions, prediction_bytes = _read_jsonl(Path(predictions_path), "predictions")
    checksum = hashlib.sha256(gold_bytes + b"\n" + prediction_bytes).hexdigest()
    return evaluate_records(gold, predictions, k=k, seed=seed, input_checksum=checksum, semantic_threshold=semantic_threshold)
