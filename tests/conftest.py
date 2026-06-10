"""Shared pytest fixtures.

The CalculationFactory keeps its registrations in a class-level dictionary,
which is shared global state. A test that registers a calculation could
leak into the next test, so this autouse fixture resets the registry to the
four default calculations before every test.
"""

import pytest

from app.calculation import (
    AddCalculation,
    CalculationFactory,
    DivideCalculation,
    MultiplyCalculation,
    SubtractCalculation,
)


@pytest.fixture(autouse=True)
def reset_calculation_factory():
    """Restore the factory's default registrations before each test."""
    CalculationFactory._calculations.clear()
    CalculationFactory.register_calculation("add")(AddCalculation)
    CalculationFactory.register_calculation("subtract")(SubtractCalculation)
    CalculationFactory.register_calculation("multiply")(MultiplyCalculation)
    CalculationFactory.register_calculation("divide")(DivideCalculation)
