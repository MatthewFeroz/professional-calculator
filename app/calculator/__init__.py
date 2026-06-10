"""Professional calculator REPL (Read-Eval-Print Loop).

The loop reads a whole command on one line — ``add 2 3`` — plus the special
commands ``help``, ``history``, and ``exit``. It demonstrates the two error
handling paradigms covered in this module:

- LBYL (Look Before You Leap): check a condition first, e.g. testing for
  empty input or special commands before trying to parse.
- EAFP (Easier to Ask Forgiveness than Permission): just try the operation
  and catch the exception, e.g. parsing numbers or executing a calculation.
"""

from typing import List

from app.calculation import Calculation, CalculationFactory


def display_help() -> None:
    """Print usage instructions and the supported operations."""
    print(
        """
Professional Calculator REPL
----------------------------
Usage:
    <operation> <number1> <number2>

Supported operations:
    add       : Add two numbers.
    subtract  : Subtract the second number from the first.
    multiply  : Multiply two numbers.
    divide    : Divide the first number by the second.

Special commands:
    help      : Show this message.
    history   : Show the calculations performed this session.
    exit      : Quit the calculator.

Examples:
    add 10 5
    divide 20 4
"""
    )


def display_history(history: List[Calculation]) -> None:
    """Print every calculation performed so far, or a friendly placeholder."""
    if not history:
        print("No calculations performed yet.")
    else:
        print("Calculation History:")
        for index, calculation in enumerate(history, start=1):
            print(f"{index}. {calculation}")


def calculator() -> None:
    """Run the calculator REPL until the user exits."""
    history: List[Calculation] = []

    print("Welcome to the Professional Calculator REPL!")
    print("Type 'help' for instructions or 'exit' to quit.\n")

    while True:
        try:
            user_input = input(">> ").strip()
        except KeyboardInterrupt:
            # EAFP: handle Ctrl+C as an exception rather than polling for it.
            print("\nKeyboard interrupt detected. Exiting calculator. Goodbye!")
            break
        except EOFError:
            # EAFP: Ctrl+D / end of piped input also exits cleanly.
            print("\nEOF detected. Exiting calculator. Goodbye!")
            break

        # LBYL: skip blank lines instead of trying to parse them.
        if not user_input:
            continue

        command = user_input.lower()
        if command == "help":
            display_help()
            continue
        if command == "history":
            display_history(history)
            continue
        if command == "exit":
            print("Exiting calculator. Goodbye!")
            break

        # EAFP: attempt to parse "<operation> <num1> <num2>" and recover
        # from any failure instead of pre-validating the format.
        try:
            operation, num1_str, num2_str = user_input.split()
            num1, num2 = float(num1_str), float(num2_str)
        except ValueError:
            print("Invalid input. Please follow the format: <operation> <num1> <num2>")
            print("Type 'help' for more information.\n")
            continue

        try:
            calculation = CalculationFactory.create_calculation(operation, num1, num2)
        except ValueError as error:
            print(error)
            print("Type 'help' to see the list of supported operations.\n")
            continue

        try:
            result_str = str(calculation)  # __str__ runs execute()
        except ZeroDivisionError as error:
            print(error)
            print("Please enter a non-zero divisor.\n")
            continue
        except Exception as error:  # pylint: disable=broad-except
            print(f"An error occurred during calculation: {error}")
            print("Please try again.\n")
            continue

        print(f"Result: {result_str}\n")
        history.append(calculation)
