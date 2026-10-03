from __future__ import annotations

from collections import Counter
from math import isfinite, sqrt
from typing import Iterable, Sequence


def accuracy(y_true: Sequence[int], y_pred: Sequence[int]) -> float:
    if len(y_true) != len(y_pred) or not y_true:
        raise ValueError("y_true and y_pred must have the same non-zero length")
    if any(isinstance(value, bool) or not isinstance(value, int) for value in (*y_true, *y_pred)):
        raise ValueError("accuracy labels must be integers")
    return sum(a == b for a, b in zip(y_true, y_pred)) / len(y_true)


def macro_f1(y_true: Sequence[int], y_pred: Sequence[int]) -> float:
    if len(y_true) != len(y_pred) or not y_true:
        raise ValueError("y_true and y_pred must have the same non-zero length")
    if any(isinstance(value, bool) or not isinstance(value, int) for value in (*y_true, *y_pred)):
        raise ValueError("macro_f1 labels must be integers")
    labels = sorted(set(y_true) | set(y_pred))
    scores = []
    for label in labels:
        tp = sum(a == label and b == label for a, b in zip(y_true, y_pred))
        fp = sum(a != label and b == label for a, b in zip(y_true, y_pred))
        fn = sum(a == label and b != label for a, b in zip(y_true, y_pred))
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        scores.append(2 * precision * recall / (precision + recall) if precision + recall else 0.0)
    return sum(scores) / len(scores)


def rmse(y_true: Sequence[float], y_pred: Sequence[float]) -> float:
    if len(y_true) != len(y_pred) or not y_true:
        raise ValueError("y_true and y_pred must have the same non-zero length")
    values = (*y_true, *y_pred)
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value) for value in values):
        raise ValueError("rmse values must be finite numbers")
    return sqrt(sum((a - b) ** 2 for a, b in zip(y_true, y_pred)) / len(y_true))


def confusion_matrix(y_true: Iterable[int], y_pred: Iterable[int]) -> dict[tuple[int, int], int]:
    return Counter(zip(y_true, y_pred))
