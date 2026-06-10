"""Tests for the calculator REPL and the program entry point.

The REPL is driven by replacing ``builtins.input`` with a scripted sequence
of lines (monkeypatch) and asserting on what was printed (capsys). Each test
ends its script with ``exit`` so the loop terminates.
"""

import runpy
from unittest.mock import patch

import pytest

from app.calculation import AddCalculation, SubtractCalculation
from app.calculator import calculator, display_help, display_history


def run_repl(monkeypatch, capsys, lines):
    """Feed ``lines`` to the REPL one input() call at a time, return output."""
    inputs = iter(lines)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    calculator()
    return capsys.readouterr().out


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def test_display_help(capsys):
    display_help()
    output = capsys.readouterr().out
    assert "Professional Calculator REPL" in output
    for operation in ("add", "subtract", "multiply", "divide"):
        assert operation in output


def test_display_history_empty(capsys):
    display_history([])
    assert "No calculations performed yet." in capsys.readouterr().out


def test_display_history_with_entries(capsys):
    history = [AddCalculation(2.0, 3.0), SubtractCalculation(10.0, 4.0)]
    display_history(history)
    output = capsys.readouterr().out
    assert "Calculation History:" in output
    assert "1. AddCalculation: 2.0 Add 3.0 = 5.0" in output
    assert "2. SubtractCalculation: 10.0 Subtract 4.0 = 6.0" in output


# ---------------------------------------------------------------------------
# REPL: happy paths
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "line, expected",
    [
        ("add 2 3", "AddCalculation: 2.0 Add 3.0 = 5.0"),
        ("subtract 10 4", "SubtractCalculation: 10.0 Subtract 4.0 = 6.0"),
        ("multiply 2 4", "MultiplyCalculation: 2.0 Multiply 4.0 = 8.0"),
        ("divide 9 3", "DivideCalculation: 9.0 Divide 3.0 = 3.0"),
    ],
)
def test_repl_performs_operations(monkeypatch, capsys, line, expected):
    output = run_repl(monkeypatch, capsys, [line, "exit"])
    assert f"Result: {expected}" in output


def test_repl_exit(monkeypatch, capsys):
    output = run_repl(monkeypatch, capsys, ["exit"])
    assert "Welcome to the Professional Calculator REPL!" in output
    assert "Exiting calculator. Goodbye!" in output


def test_repl_help_command(monkeypatch, capsys):
    output = run_repl(monkeypatch, capsys, ["help", "exit"])
    assert "Professional Calculator REPL" in output


def test_repl_history_tracks_calculations(monkeypatch, capsys):
    output = run_repl(
        monkeypatch, capsys, ["add 1 1", "multiply 3 3", "history", "exit"]
    )
    assert "Calculation History:" in output
    assert "1. AddCalculation: 1.0 Add 1.0 = 2.0" in output
    assert "2. MultiplyCalculation: 3.0 Multiply 3.0 = 9.0" in output


def test_repl_history_empty(monkeypatch, capsys):
    output = run_repl(monkeypatch, capsys, ["history", "exit"])
    assert "No calculations performed yet." in output


def test_repl_skips_blank_input(monkeypatch, capsys):
    output = run_repl(monkeypatch, capsys, ["", "   ", "exit"])
    assert "Invalid input" not in output
    assert "Exiting calculator. Goodbye!" in output


# ---------------------------------------------------------------------------
# REPL: error handling
# ---------------------------------------------------------------------------

def test_repl_invalid_format(monkeypatch, capsys):
    output = run_repl(monkeypatch, capsys, ["add 2", "exit"])
    assert "Invalid input. Please follow the format" in output


def test_repl_invalid_numbers(monkeypatch, capsys):
    output = run_repl(monkeypatch, capsys, ["add two three", "exit"])
    assert "Invalid input. Please follow the format" in output


def test_repl_unsupported_operation(monkeypatch, capsys):
    output = run_repl(monkeypatch, capsys, ["modulus 2 3", "exit"])
    assert "Unsupported calculation type: 'modulus'" in output
    assert "Type 'help' to see the list of supported operations." in output


def test_repl_division_by_zero(monkeypatch, capsys):
    output = run_repl(monkeypatch, capsys, ["divide 5 0", "exit"])
    assert "Division by zero is not allowed." in output
    assert "Please enter a non-zero divisor." in output


def test_repl_unexpected_error(monkeypatch, capsys):
    """An unforeseen exception is reported without crashing the loop."""
    with patch(
        "app.calculator.CalculationFactory.create_calculation"
    ) as mock_create:
        mock_create.return_value.__str__.side_effect = RuntimeError("boom")
        output = run_repl(monkeypatch, capsys, ["add 2 3", "exit"])
    assert "An error occurred during calculation: boom" in output
    assert "Exiting calculator. Goodbye!" in output


def test_repl_keyboard_interrupt(monkeypatch, capsys):
    def raise_interrupt(_):
        raise KeyboardInterrupt

    monkeypatch.setattr("builtins.input", raise_interrupt)
    calculator()
    output = capsys.readouterr().out
    assert "Keyboard interrupt detected. Exiting calculator. Goodbye!" in output


def test_repl_eof(monkeypatch, capsys):
    def raise_eof(_):
        raise EOFError

    monkeypatch.setattr("builtins.input", raise_eof)
    calculator()
    output = capsys.readouterr().out
    assert "EOF detected. Exiting calculator. Goodbye!" in output


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def test_main_runs_calculator(monkeypatch, capsys):
    """Running main.py as a script starts the REPL."""
    monkeypatch.setattr("builtins.input", lambda _: "exit")
    runpy.run_path("main.py", run_name="__main__")
    assert "Exiting calculator. Goodbye!" in capsys.readouterr().out


def test_main_import_does_not_start_repl(capsys):
    """Importing main as a module must NOT start the REPL.

    Together with the test above, this exercises both branches of the
    ``if __name__ == "__main__"`` guard.
    """
    import main  # noqa: F401  pylint: disable=import-outside-toplevel

    assert "Welcome" not in capsys.readouterr().out
