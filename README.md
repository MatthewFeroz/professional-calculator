# Professional Calculator

A professional-grade command-line calculator built in Python with advanced
object-oriented design — an abstract `Calculation` hierarchy created through
the **Factory design pattern** — and a comprehensive pytest suite with
**100% test coverage enforced** locally and in CI.

This is the third iteration of my calculator series:
[calculator](https://github.com/MatthewFeroz/calculator) (basic functions) →
[calculator-pro](https://github.com/MatthewFeroz/calculator-pro) (OOP
operations + REPL) → **professional-calculator** (calculation objects,
factory pattern, history, mocking and fixtures in tests).

## Features

- **REPL interface** — single-line commands like `add 10 5`, plus `help`,
  `history`, and `exit` special commands.
- **Calculation objects** — every calculation is an object that carries its
  operands and knows how to `execute()` itself, print itself (`__str__`),
  and describe itself for debugging (`__repr__`).
- **Factory design pattern** — `CalculationFactory` builds the right
  `Calculation` subclass from a string. New operations register themselves
  with a decorator, so the factory never needs editing (open/closed
  principle).
- **Layered design (DRY)** — raw arithmetic lives in `Operation` static
  methods; calculation classes delegate to it; the REPL only talks to the
  factory. Each rule is written exactly once.
- **LBYL and EAFP error handling** — the REPL checks conditions up front
  where that is cheap (blank input, special commands) and catches
  exceptions where checking first would be complex (parsing, execution).
  Invalid input, unknown operations, and division by zero never crash it.
- **100% test coverage** — unit, parameterized, and negative tests, with
  `unittest.mock` to isolate layers and a pytest fixture to reset shared
  factory state between tests.

## Project structure

```
professional-calculator/
├── app/
│   ├── operation/__init__.py     # Operation: static arithmetic methods
│   ├── calculation/__init__.py   # Calculation ABC, concrete classes, factory
│   └── calculator/__init__.py    # REPL with help/history/exit
├── tests/
│   ├── conftest.py               # fixture resetting factory registrations
│   ├── test_operations.py        # parameterized + negative arithmetic tests
│   ├── test_calculations.py      # calculation classes + factory tests
│   └── test_calculator.py        # REPL + entry-point tests
├── main.py                       # program entry point
├── requirements.txt
├── pytest.ini                    # test + 100% coverage configuration
└── .github/workflows/ci.yml      # CI pipeline
```

## Setup

Requires Python 3.10+.

```bash
# 1. Clone and enter the project
git clone https://github.com/MatthewFeroz/professional-calculator.git
cd professional-calculator

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Example session:

```
Welcome to the Professional Calculator REPL!
Type 'help' for instructions or 'exit' to quit.

>> add 10 5
Result: AddCalculation: 10.0 Add 5.0 = 15.0

>> divide 5 0
Division by zero is not allowed.
Please enter a non-zero divisor.

>> history
Calculation History:
1. AddCalculation: 10.0 Add 5.0 = 15.0

>> exit
Exiting calculator. Goodbye!
```

## Running tests

```bash
pytest
```

`pytest.ini` measures coverage of `app/` and `main.py` and **fails the run
if coverage is below 100%**, so a plain `pytest` run reproduces exactly what
CI checks. For line-by-line detail:

```bash
pytest --cov-report=term-missing
```

### Coverage exceptions (`# pragma: no cover`)

Lines that are genuinely untestable (e.g. defensive `pass`/`continue`
statements or platform-specific code) can be excluded from coverage metrics
with a `# pragma: no cover` comment. **This project needed none**: every
line and every branch — including the `if __name__ == "__main__"` guard in
`main.py`, exercised in both directions via `runpy` and a plain import — is
covered by a real test, with branch coverage (`--cov-branch`) enabled.

## Continuous Integration

Every push and pull request triggers
[`.github/workflows/ci.yml`](.github/workflows/ci.yml), which installs
dependencies and runs the test suite. The build **fails if any test fails
or coverage drops below 100%**.
