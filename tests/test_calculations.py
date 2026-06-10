"""Unit tests for the Calculation classes and the CalculationFactory."""

from unittest.mock import patch

import pytest

from app.calculation import (
    AddCalculation,
    Calculation,
    CalculationFactory,
    DivideCalculation,
    MultiplyCalculation,
    SubtractCalculation,
)


# ---------------------------------------------------------------------------
# Calculation abstract base class
# ---------------------------------------------------------------------------

def test_calculation_cannot_be_instantiated():
    """The ABC enforces its contract: no instance without execute()."""
    with pytest.raises(TypeError):
        Calculation(2.0, 3.0)  # pylint: disable=abstract-class-instantiated


def test_calculation_stores_operands():
    calculation = AddCalculation(2.0, 3.0)
    assert calculation.a == 2.0
    assert calculation.b == 3.0


# ---------------------------------------------------------------------------
# Concrete calculations delegate to Operation (verified with mocks)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "calculation_class, operation_name",
    [
        (AddCalculation, "addition"),
        (SubtractCalculation, "subtraction"),
        (MultiplyCalculation, "multiplication"),
        (DivideCalculation, "division"),
    ],
)
def test_execute_delegates_to_operation(calculation_class, operation_name):
    """Each calculation should call its Operation method exactly once.

    Mocking isolates the calculation layer: the test passes or fails based
    on the delegation logic alone, not on the arithmetic underneath.
    """
    with patch(f"app.calculation.Operation.{operation_name}") as mock_method:
        mock_method.return_value = 99.0
        calculation = calculation_class(8.0, 2.0)

        result = calculation.execute()

        mock_method.assert_called_once_with(8.0, 2.0)
        assert result == 99.0


@pytest.mark.parametrize(
    "calculation_class, a, b, expected",
    [
        (AddCalculation, 2.0, 3.0, 5.0),
        (AddCalculation, -2.0, -3.0, -5.0),
        (SubtractCalculation, 10.0, 4.0, 6.0),
        (SubtractCalculation, 4.0, 10.0, -6.0),
        (MultiplyCalculation, 2.5, 4.0, 10.0),
        (MultiplyCalculation, -2.0, 3.0, -6.0),
        (DivideCalculation, 9.0, 3.0, 3.0),
        (DivideCalculation, -9.0, 3.0, -3.0),
    ],
)
def test_execute_end_to_end(calculation_class, a, b, expected):
    """Parameterized integration check through the real Operation methods."""
    assert calculation_class(a, b).execute() == expected


def test_divide_calculation_by_zero():
    """Negative test: division by zero surfaces as ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError, match="Division by zero is not allowed."):
        DivideCalculation(5.0, 0.0).execute()


# ---------------------------------------------------------------------------
# String representations
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "calculation_class, a, b, expected_str",
    [
        (AddCalculation, 2.0, 3.0, "AddCalculation: 2.0 Add 3.0 = 5.0"),
        (SubtractCalculation, 10.0, 4.0, "SubtractCalculation: 10.0 Subtract 4.0 = 6.0"),
        (MultiplyCalculation, 2.0, 4.0, "MultiplyCalculation: 2.0 Multiply 4.0 = 8.0"),
        (DivideCalculation, 9.0, 3.0, "DivideCalculation: 9.0 Divide 3.0 = 3.0"),
    ],
)
def test_str_representation(calculation_class, a, b, expected_str):
    assert str(calculation_class(a, b)) == expected_str


@pytest.mark.parametrize(
    "calculation_class, a, b, expected_repr",
    [
        (AddCalculation, 2.0, 3.0, "AddCalculation(a=2.0, b=3.0)"),
        (DivideCalculation, 9.0, 3.0, "DivideCalculation(a=9.0, b=3.0)"),
    ],
)
def test_repr_representation(calculation_class, a, b, expected_repr):
    assert repr(calculation_class(a, b)) == expected_repr


# ---------------------------------------------------------------------------
# CalculationFactory
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "calculation_type, expected_class",
    [
        ("add", AddCalculation),
        ("subtract", SubtractCalculation),
        ("multiply", MultiplyCalculation),
        ("divide", DivideCalculation),
        ("ADD", AddCalculation),  # lookups are case-insensitive
    ],
)
def test_factory_creates_correct_class(calculation_type, expected_class):
    calculation = CalculationFactory.create_calculation(calculation_type, 2.0, 3.0)
    assert isinstance(calculation, expected_class)
    assert calculation.a == 2.0
    assert calculation.b == 3.0


def test_factory_rejects_unsupported_type():
    """Negative test: unknown types raise and list what IS supported."""
    with pytest.raises(ValueError) as exc_info:
        CalculationFactory.create_calculation("modulus", 2.0, 3.0)
    message = str(exc_info.value)
    assert "Unsupported calculation type: 'modulus'" in message
    for supported in ("add", "subtract", "multiply", "divide"):
        assert supported in message


def test_factory_rejects_duplicate_registration():
    """Negative test: a name can only be registered once."""
    with pytest.raises(ValueError, match="already registered"):

        @CalculationFactory.register_calculation("add")
        class DuplicateAddCalculation(Calculation):  # pylint: disable=unused-variable
            def execute(self) -> float:
                return 0.0


def test_factory_registers_new_calculation():
    """The factory is open for extension: new types plug in cleanly."""

    @CalculationFactory.register_calculation("power")
    class PowerCalculation(Calculation):
        def execute(self) -> float:
            return self.a ** self.b

    calculation = CalculationFactory.create_calculation("power", 2.0, 3.0)
    assert isinstance(calculation, PowerCalculation)
    assert calculation.execute() == 8.0
