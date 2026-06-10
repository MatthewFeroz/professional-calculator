"""Basic arithmetic operations grouped in a single utility class.

The ``Operation`` class encapsulates the raw math of the calculator. The
methods are *static* because they are stateless: they depend only on their
arguments, never on instance data, so no object needs to be created to use
them. Keeping the arithmetic here — separate from the ``Calculation``
classes that *use* it — follows the Single Responsibility Principle and
keeps each layer easy to test on its own.
"""


class Operation:
    """Stateless arithmetic helpers used by the calculation layer."""

    @staticmethod
    def addition(a: float, b: float) -> float:
        """Return the sum of ``a`` and ``b``."""
        return a + b

    @staticmethod
    def subtraction(a: float, b: float) -> float:
        """Return ``a`` minus ``b``."""
        return a - b

    @staticmethod
    def multiplication(a: float, b: float) -> float:
        """Return the product of ``a`` and ``b``."""
        return a * b

    @staticmethod
    def division(a: float, b: float) -> float:
        """Return ``a`` divided by ``b``.

        Raises:
            ZeroDivisionError: if ``b`` is zero, with a clear message instead
                of Python's default, so callers can show it to the user.
        """
        if b == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return a / b
