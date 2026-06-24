# bankstatementparser-writer-xlsx: Excel writer for parsed bank statements

[![PyPI Version][pypi-badge]][pypi-url]
[![Python Versions][python-versions-badge]][pypi-url]
[![License][license-badge]][license-url]
[![Coverage][coverage-badge]][ci-url]

**An Excel `.xlsx` writer for data parsed by
[`bankstatementparser`][core]** — turn parsed transactions (a pandas
`DataFrame`, a list of `Transaction` objects, or a list of plain dicts)
into a polished workbook that accountants, auditors, and reconciliation
macros can open directly.

> **Latest release: v0.0.10** — single `write_xlsx(data, path, ...)`
> function, 100% line + branch coverage, 100% docstring coverage,
> `mypy --strict` clean.

## Contents

- [Overview](#overview)
- [Install](#install)
- [Quick start](#quick-start)
- [Input shapes](#input-shapes)
- [Value coercion](#value-coercion)
- [The summary sheet](#the-summary-sheet)
- [Examples](#examples)
- [When not to use this package](#when-not-to-use-this-package)
- [Development](#development)
- [Security](#security)
- [Documentation](#documentation)
- [License](#license)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)

## Overview

`bankstatementparser-writer-xlsx` is a small, focused companion to the
[`bankstatementparser`][core] library. It does one thing well: given
already-parsed bank-statement records, write a clean Excel workbook with
a bold header row, one row per transaction, auto-sized columns, and an
optional second `Summary` sheet.

The package consumes _parsed_ data — it does not read PDFs, CSVs, or
XML itself. Parsing (and the security surface that comes with untrusted
input) lives upstream in the [`bankstatementparser`][core] core.

## Install

`bankstatementparser-writer-xlsx` runs on macOS, Linux, and Windows and
requires **Python 3.10+**. It pulls in `bankstatementparser`,
`openpyxl`, and `pandas` automatically.

```bash
pip install bankstatementparser-writer-xlsx
```

## Quick start

```python
from bankstatementparser import CsvStatementParser
from bankstatementparser_writer_xlsx import write_xlsx

parser = CsvStatementParser("statement.csv")
df = parser.parse()                      # a pandas DataFrame
write_xlsx(df, "statement.xlsx")         # one polished workbook
```

That's an Excel workbook ready for your accountant. Add a summary sheet
in one extra argument:

```python
from bankstatementparser import CsvStatementParser
from bankstatementparser_writer_xlsx import write_xlsx

parser = CsvStatementParser("statement.csv")
df = parser.parse()
write_xlsx(df, "statement.xlsx", summary=parser.get_summary())
```

## Input shapes

`write_xlsx(data, path, *, sheet_name="Transactions", summary=None)`
accepts three input shapes and normalises each to a flat table:

| Input | Column order |
| :--- | :--- |
| `pandas.DataFrame` (from a parser's `.parse()`) | the DataFrame's own column order |
| `list[bankstatementparser.Transaction]` | the stable `Transaction` field order |
| `list[dict]` | the union of keys, in first-seen order |

A header row (bold) is written to the `sheet_name` sheet, followed by
one row per record. Columns are auto-sized to their widest cell (capped
so wide descriptions don't run off-screen).

**Empty input** is accepted: an empty `list` writes an empty sheet (no
header), while an empty `DataFrame` that still carries column labels
writes a header-only sheet.

## Value coercion

Spreadsheet cells can't hold arbitrary Python objects, so the writer
coerces the rich types the parser emits:

| Python type | Written as |
| :--- | :--- |
| `decimal.Decimal` | `float` (Excel has no decimal type; floats aggregate natively) |
| `datetime.date` / `datetime.datetime` | native Excel date cell (unchanged) |
| `str`, `int`, `float`, `bool`, `None` | unchanged |
| anything else | `str(value)` |

## The summary sheet

If you pass `summary=` a mapping (for example a parser's
`get_summary()` result), the writer adds a second sheet titled
`Summary` with a bold `Key` / `Value` header and one row per item:

```python
from decimal import Decimal

from bankstatementparser_writer_xlsx import write_xlsx

transactions = [
    {"date": "2026-06-01", "description": "Salary", "amount": Decimal("3000.00")},
    {"date": "2026-06-03", "description": "Coffee Shop", "amount": Decimal("-4.20")},
]

write_xlsx(
    transactions,
    "out.xlsx",
    summary={
        "account_id": "DE89370400440532013000",
        "transaction_count": 128,
        "total_amount": Decimal("12045.67"),
        "currency": "EUR",
    },
)
```

## Examples

Five runnable examples live in [`examples/`](examples/) and are
exercised in CI on every commit. Together they cover every supported
input shape and option of `write_xlsx`:

- [`01_write_dataframe.py`](examples/01_write_dataframe.py) — write a
  pandas `DataFrame` to a single sheet.
- [`02_write_transactions.py`](examples/02_write_transactions.py) —
  write a list of `Transaction` objects in stable field order.
- [`03_write_dicts.py`](examples/03_write_dicts.py) — write a list of
  plain `dict` records (union of keys).
- [`04_write_with_summary.py`](examples/04_write_with_summary.py) —
  write a DataFrame plus a second `Summary` sheet via `summary=`.
- [`05_custom_sheet_name.py`](examples/05_custom_sheet_name.py) — rename
  the transactions sheet with `sheet_name=`.

## When not to use this package

- **You need a custom sheet layout.** The single-sheet (+ optional
  Summary) structure is intentionally simple. Compose your own
  `openpyxl` workbook if you need pivot-ready, multi-sheet layouts.
- **You need `.xls` (legacy binary).** `openpyxl` writes `.xlsx` only;
  convert downstream if you must.
- **You need encrypted output.** Out of scope; encrypt the produced
  `.xlsx` downstream with a tool like `msoffcrypto-tool`.
- **You want to _read_ Excel.** This package is a writer.

## Development

```bash
git clone https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx
cd bankstatementparser-writer-xlsx
poetry env use python3.12
poetry install
poetry run pytest        # 100% line + branch coverage gate
poetry run ruff check bankstatementparser_writer_xlsx tests
poetry run mypy bankstatementparser_writer_xlsx
poetry run interrogate -c pyproject.toml bankstatementparser_writer_xlsx
```

## Security

`bankstatementparser-writer-xlsx` consumes already-parsed data, not raw
statement files — the PDF/CSV/XML parsing surface lives upstream in the
[`bankstatementparser`][core] core. Reporting practice, supported
versions, and supply-chain posture are documented in
[`SECURITY.md`](SECURITY.md).

## Documentation

- [`README.md`](README.md) — this file
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — module map and design decisions
- [`CHANGELOG.md`](CHANGELOG.md) — release notes
- [`ROADMAP.md`](ROADMAP.md) — what's next
- [`SECURITY.md`](SECURITY.md) — disclosure + supported versions
- [`examples/`](examples/) — runnable scripts, exercised in CI

## License

Licensed under the [Apache License, Version 2.0][license-url]. Any
contribution submitted for inclusion shall be licensed as above, without
additional terms.

## Contributing

Contributions are welcome — open an issue or PR on
[the repository](https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx).

## Acknowledgements

Built on the [`bankstatementparser`][core] library and
[openpyxl](https://openpyxl.readthedocs.io/).

[core]: https://github.com/sebastienrousseau/bankstatementparser
[pypi-url]: https://pypi.org/project/bankstatementparser-writer-xlsx/
[license-url]: https://opensource.org/license/apache-2-0/
[ci-url]: https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx/actions/workflows/ci.yml
[pypi-badge]: https://img.shields.io/pypi/v/bankstatementparser-writer-xlsx.svg?style=for-the-badge
[python-versions-badge]: https://img.shields.io/pypi/pyversions/bankstatementparser-writer-xlsx.svg?style=for-the-badge
[license-badge]: https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=for-the-badge
[coverage-badge]: https://img.shields.io/badge/Coverage-100%25-brightgreen?style=for-the-badge
