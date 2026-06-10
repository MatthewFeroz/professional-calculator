"""Calculation classes and the factory that creates them.

This module adds an object-oriented layer on top of the raw arithmetic in
``app.operation``:

- ``Calculation`` is an abstract base class. It stores the two operands and
  defines the contract (``execute``) every concrete calculation must honor.
  Code that works with a ``Calculation`` never needs to know *which* one it
  has — that is polymorphism.
- ``CalculationFactory`` implements the Factory design pattern. Calculations
  register themselves under a name (``"add"``, ``"divide"``, ...) with a
  class decorator, and the factory builds the right instance from a string
  at runtime. New operations can be added without touching existing code
  (the open/closed principle).
"""

from abc import ABC, abstractmethod

from app.operation import Operation


class Calculation(ABC):
    """A single calculation: two operands plus an operation to perform."""

    def __init__(self, a: float, b: float) -> None:
        self.a = a
        self.b = b

    @abstractmethod
    def execute(self) -> float:
        """Perform the calculation and return the result."""

    def __str__(self) -> str:
        """Human-friendly form, e.g. ``AddCalculation: 2.0 Add 3.0 = 5.0``."""
        result = self.execute()
        operation_name = self.__class__.__name__.replace("Calculation", "")
        return f"{self.__class__.__name__}: {self.a} {operation_name} {self.b} = {result}"

    def __repr__(self) -> str:
        """Unambiguous developer-facing form for debugging."""
        return f"{self.__class__.__name__}(a={self.a}, b={self.b})"


class CalculationFactory:
    """Creates ``Calculation`` instances from a string operation name."""

    _calculations: dict = {}

    @classmethod
    def register_calculation(cls, calculation_type: str):
        """Class decorator that registers a Calculation subclass by name."""

        def decorator(subclass):
            key = calculation_type.lower()
            if key in cls._calculations:
                raise ValueError(
                    f"Calculation type '{calculation_type}' is already registered."
                )
            cls._calculations[key] = subclass
            return subclass

        return decorator

    @classmethod
    def create_calculation(cls, calculation_type: str, a: float, b: float) -> Calculation:
        """Build the calculation registered under ``calculation_type``.

        Raises:
            ValueError: if the type is unknown, with the supported types
                listed so the caller can tell the user what is valid.
        """
        calculation_class = cls._calculations.get(calculation_type.lower())
        if not calculation_class:
            available = ", ".join(sorted(cls._calculations))
            raise ValueError(
                f"Unsupported calculation type: '{calculation_type}'. "
                f"Available types: {available}"
            )
        return calculation_class(a, b)


@CalculationFactory.register_calculation("add")
class AddCalculation(Calculation):
    """Addition of the two operands."""

    def execute(self) -> float:
        return Operation.addition(self.a, self.b)


@CalculationFactory.register_calculation("subtract")
class SubtractCalculation(Calculation):
    """Subtraction of the second operand from the first."""

    def execute(self) -> float:
        return Operation.subtraction(self.a, self.b)


@CalculationFactory.register_calculation("multiply")
class MultiplyCalculation(Calculation):
    """Multiplication of the two operands."""

    def execute(self) -> float:
        return Operation.multiplication(self.a, self.b)


@CalculationFactory.register_calculation("divide")
class DivideCalculation(Calculation):
    """Division of the first operand by the second.

    The zero-divisor guard lives in ``Operation.division`` so the rule is
    written exactly once (DRY); this class simply delegates.
    """

    def execute(self) -> float:
        return Operation.division(self.a, self.b)
