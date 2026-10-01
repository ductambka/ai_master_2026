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
        if not x or len(x) != len(y) or any(len(row) != len(x[0]) for row in x):
            raise ValueError("x must be a non-empty rectangular matrix matching y")
        if any(label not in (0, 1) for label in y):
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
        if not self.weights or len(row) != len(self.weights):
            raise ValueError("model is not fitted or feature count is wrong")
        return _sigmoid(self.bias + sum(weight * value for weight, value in zip(self.weights, row)))

    def predict(self, x: list[list[float]], threshold: float = 0.5) -> list[int]:
        if not 0 < threshold < 1:
            raise ValueError("threshold must be between 0 and 1")
        return [int(self.predict_proba_one(row) >= threshold) for row in x]

