"""A tiny scalar reverse-mode automatic differentiation engine.

The implementation is intentionally small enough to inspect in a lecture.  A
``Value`` stores one scalar, its parents, and a local backward function.  The
backward pass visits each node once in reverse topological order.
"""

from __future__ import annotations

import math
from typing import Callable, Iterable


class Value:
    """A scalar value in a differentiable computation graph."""

    def __init__(
        self,
        data: float,
        _children: Iterable["Value"] = (),
        _op: str = "",
    ) -> None:
        self.data = float(data)
        self.grad = 0.0
        self._prev = set(_children)
        self._op = _op
        self._backward: Callable[[], None] = lambda: None

    def __repr__(self) -> str:
        return f"Value(data={self.data!r}, grad={self.grad!r})"

    @staticmethod
    def _coerce(other: float | "Value") -> "Value":
        return other if isinstance(other, Value) else Value(other)

    def __add__(self, other: float | "Value") -> "Value":
        other = self._coerce(other)
        out = Value(self.data + other.data, (self, other), "+")

        def backward() -> None:
            self.grad += out.grad
            other.grad += out.grad

        out._backward = backward
        return out

    __radd__ = __add__

    def __neg__(self) -> "Value":
        return self * -1.0

    def __sub__(self, other: float | "Value") -> "Value":
        return self + -self._coerce(other)

    def __rsub__(self, other: float | "Value") -> "Value":
        return self._coerce(other) + -self

    def __mul__(self, other: float | "Value") -> "Value":
        other = self._coerce(other)
        out = Value(self.data * other.data, (self, other), "*")

        def backward() -> None:
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad

        out._backward = backward
        return out

    __rmul__ = __mul__

    def __truediv__(self, other: float | "Value") -> "Value":
        other = self._coerce(other)
        return self * other ** -1.0

    def __rtruediv__(self, other: float | "Value") -> "Value":
        return self._coerce(other) / self

    def __pow__(self, exponent: float) -> "Value":
        if not isinstance(exponent, (int, float)):
            raise TypeError("exponent must be a scalar number")
        if self.data == 0.0 and exponent < 1:
            raise ValueError("power is undefined for zero with exponent below 1")
        out = Value(self.data**exponent, (self,), f"**{exponent}")

        def backward() -> None:
            self.grad += exponent * self.data ** (exponent - 1) * out.grad

        out._backward = backward
        return out

    def exp(self) -> "Value":
        result = math.exp(self.data)
        out = Value(result, (self,), "exp")

        def backward() -> None:
            self.grad += result * out.grad

        out._backward = backward
        return out

    def log(self) -> "Value":
        if self.data <= 0.0:
            raise ValueError("log is only defined for positive values")
        out = Value(math.log(self.data), (self,), "log")

        def backward() -> None:
            self.grad += (1.0 / self.data) * out.grad

        out._backward = backward
        return out

    def backward(self) -> None:
        """Compute derivatives from this value to all graph leaves.

        Gradients are reset for every node reachable from ``self`` before the
        reverse pass. This makes repeated calls deterministic and prevents a
        shared intermediate node from propagating stale gradient more than
        once. Gradient contributions from multiple uses of a node within one
        graph are still accumulated normally.
        """
        topo: list[Value] = []
        visited: set[Value] = set()

        def build(node: Value) -> None:
            if node in visited:
                return
            visited.add(node)
            for parent in node._prev:
                build(parent)
            topo.append(node)

        build(self)
        for node in topo:
            node.grad = 0.0
        self.grad = 1.0
        for node in reversed(topo):
            node._backward()


def exp(value: float | Value) -> Value:
    """Functional spelling of :meth:`Value.exp`."""
    return Value._coerce(value).exp()


def log(value: float | Value) -> Value:
    """Functional spelling of :meth:`Value.log`."""
    return Value._coerce(value).log()
