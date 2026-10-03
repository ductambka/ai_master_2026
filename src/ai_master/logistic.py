from __future__ import annotations

import math
from dataclasses import dataclass, field


def _sigmoid(value: float) -> float:
    if value >= 0:
        z = math.exp(-value)
        return 1 / (1 + z)
    z = math.exp(value)
    return z / (1 + z)


@dataclass
class LogisticRegression:
    """Binary logistic regression with batch gradient descent.

    It intentionally exposes the training loop so learners can inspect gradients,
    regularisation and convergence before moving to a framework implementation.
    """

    learning_rate: float = 0.1
    epochs: int = 100
    l2: float = 0.0
    weights: list[float] = field(default_factory=list)
    bias: float = 0.0
    history: list[float] = field(default_factory=list)

    def fit(self, x: list[list[float]], y: list[int]) -> "LogisticRegression":
        if not math.isfinite(self.learning_rate) or self.learning_rate <= 0:
            raise ValueError("learning_rate must be a positive finite number")
        if not isinstance(self.epochs, int) or isinstance(self.epochs, bool) or self.epochs < 1:
            raise ValueError("epochs must be a positive integer")
        if not math.isfinite(self.l2) or self.l2 < 0:
            raise ValueError("l2 must be a non-negative finite number")
        if not isinstance(x, list) or not isinstance(y, list):
            raise ValueError("x and y must be lists")
        if not x or len(x) != len(y) or not isinstance(x[0], list) or not x[0] or any(
            not isinstance(row, list) or len(row) != len(x[0]) for row in x
        ):
            raise ValueError("x must be a non-empty rectangular matrix matching y")
        if any(
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not math.isfinite(value)
            for row in x
            for value in row
        ):
            raise ValueError("x must contain only finite numeric values")
        if any(not isinstance(label, int) or isinstance(label, bool) or label not in (0, 1) for label in y):
            raise ValueError("binary labels must be 0 or 1")
        self.weights = [0.0] * len(x[0])
        self.bias = 0.0
        self.history = []
        n = len(x)
        for _ in range(self.epochs):
            probabilities = [self.predict_proba_one(row) for row in x]
            errors = [p - target for p, target in zip(probabilities, y)]
            for j in range(len(self.weights)):
                gradient = sum(error * row[j] for error, row in zip(errors, x)) / n
                gradient += self.l2 * self.weights[j]
                self.weights[j] -= self.learning_rate * gradient
            self.bias -= self.learning_rate * sum(errors) / n
            loss = -sum(target * math.log(max(p, 1e-15)) + (1 - target) * math.log(max(1 - p, 1e-15)) for target, p in zip(y, probabilities)) / n
            loss += self.l2 * sum(w * w for w in self.weights) / 2
            self.history.append(loss)
        return self

    def predict_proba_one(self, row: list[float]) -> float:
        if not self.weights:
            raise ValueError("model is not fitted or feature count is wrong")
        if not isinstance(row, list) or len(row) != len(self.weights):
            raise ValueError("row must be a list with the fitted feature count")
        if any(
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not math.isfinite(value)
            for value in row
        ):
            raise ValueError("row must contain only finite numeric values")
        return _sigmoid(self.bias + sum(weight * value for weight, value in zip(self.weights, row)))

    def predict(self, x: list[list[float]], threshold: float = 0.5) -> list[int]:
        if not isinstance(threshold, (int, float)) or isinstance(threshold, bool) or not math.isfinite(threshold) or not 0 < threshold < 1:
            raise ValueError("threshold must be between 0 and 1")
        if not self.weights:
            raise ValueError("model is not fitted or feature count is wrong")
        if not isinstance(x, list):
            raise ValueError("x must be a list of rows")
        if any(not isinstance(row, list) for row in x):
            raise ValueError("x must contain only rows represented as lists")
        return [int(self.predict_proba_one(row) >= threshold) for row in x]
