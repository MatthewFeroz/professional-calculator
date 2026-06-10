"""Unit and negative tests for the Operation arithmetic methods."""

import pytest

from app.operation import Operation


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2.0, 3.0, 5.0),          # two positives
        (-2.0, -3.0, -5.0),       # two negatives
        (5.0, -3.0, 2.0),         # mixed signs
        (7.5, 0.0, 7.5),          # zero identity
        (0.1, 0.2, pytest.approx(0.3)),  # floats need approx comparison
    ],
)
def test_addition(a, b, expected):
    assert Operation.addition(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10.0, 4.0, 6.0),
        (-10.0, -4.0, -6.0),
        (5.0, -3.0, 8.0),
        (7.5, 0.0, 7.5),
        (0.0, 3.0, -3.0),
    ],
)
def test_subtraction(a, b, expected):
    assert Operation.subtraction(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2.0, 3.0, 6.0),
        (-2.0, -3.0, 6.0),
        (5.0, -3.0, -15.0),
        (7.5, 0.0, 0.0),
        (0.5, 0.5, 0.25),
    ],
)
def test_multiplication(a, b, expected):
    assert Operation.multiplication(a, b) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10.0, 2.0, 5.0),
        (-10.0, -2.0, 5.0),
        (7.0, -2.0, -3.5),
        (0.0, 5.0, 0.0),     # zero numerator is fine
        (1.0, 3.0, pytest.approx(1 / 3)),
    ],
)
def test_division(a, b, expected):
    assert Operation.division(a, b) == expected


def test_division_by_zero_raises():
    """Negative test: dividing by zero must raise with a clear message."""
    with pytest.raises(ZeroDivisionError, match="Division by zero is not allowed."):
        Operation.division(10.0, 0.0)


@pytest.mark.parametrize(
    "method, a, b",
    [
        (Operation.addition, "2", 3.0),
        (Operation.subtraction, 2.0, None),
        (Operation.multiplication, "2", "3"),
        (Operation.division, None, 2.0),
    ],
)
def test_operations_reject_non_numeric_input(method, a, b):
    """Negative test: non-numeric operands raise TypeError."""
    with pytest.raises(TypeError):
        method(a, b)
