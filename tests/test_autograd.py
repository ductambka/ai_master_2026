import math

import pytest

from ai_master.autograd import Value, exp, log


def numerical_derivative(function, x, epsilon=1e-6):
    return (function(x + epsilon) - function(x - epsilon)) / (2 * epsilon)


def test_backward_handles_branching_graph_and_accumulates_gradients():
    x = Value(2.0)
    y = x * x + x

    y.backward()

    assert y.data == pytest.approx(6.0)
    assert x.grad == pytest.approx(5.0)


def test_exp_log_graph_matches_finite_difference():
    def function(number):
        return math.log(math.exp(number) + number * number)

    x = Value(0.7)
    output = log(exp(x) + x * x)
    output.backward()

    expected = numerical_derivative(function, x.data)
    assert output.data == pytest.approx(function(x.data))
    assert x.grad == pytest.approx(expected, abs=1e-5)


def test_reverse_operations_and_shared_subgraph():
    x = Value(3.0)
    output = 2.0 * x + 4.0 + x * x
    output.backward()

    assert output.data == pytest.approx(19.0)
    assert x.grad == pytest.approx(8.0)


def test_repeated_backward_resets_intermediate_gradients():
    x = Value(2.0)
    shared = x * x
    output = shared + shared

    output.backward()
    assert x.grad == pytest.approx(8.0)
    output.backward()
    assert x.grad == pytest.approx(8.0)


def test_log_rejects_non_positive_values():
    with pytest.raises(ValueError, match="positive"):
        log(Value(0.0))
    with pytest.raises(ValueError, match="positive"):
        Value(-1.0).log()


@pytest.mark.parametrize("data", [True, float("nan"), float("inf"), "1"])
def test_value_rejects_non_finite_or_non_numeric_data(data):
    with pytest.raises(ValueError, match="finite number"):
        Value(data)  # type: ignore[arg-type]


def test_power_rejects_invalid_exponents_and_zero_domain():
    with pytest.raises(TypeError, match="scalar number"):
        Value(2.0) ** True  # type: ignore[operator]
    with pytest.raises(ValueError, match="finite"):
        Value(2.0) ** float("inf")
    with pytest.raises(ValueError, match="non-positive"):
        Value(0.0) ** 0.0


def test_power_and_exp_reject_non_finite_real_domain_results():
    with pytest.raises(ValueError, match="negative base"):
        Value(-1.0) ** 0.5
    with pytest.raises(ValueError, match="finite"):
        exp(Value(1000.0))
