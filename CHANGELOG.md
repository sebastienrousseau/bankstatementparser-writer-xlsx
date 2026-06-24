# Changelog

All notable changes to **bankstatementparser-writer-xlsx** are
documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/).

## [0.0.1] - 2026-06-24

### Added

- Initial release of `bankstatementparser-writer-xlsx`, the Excel
  `.xlsx` writer companion to the
  [`bankstatementparser`](https://github.com/sebastienrousseau/bankstatementparser)
  library.
- `write_xlsx(data, path, *, sheet_name="Transactions", summary=None)`
  — serialises parsed bank-statement data to a polished workbook via
  [openpyxl](https://openpyxl.readthedocs.io/).
- Accepts three input shapes: a pandas `DataFrame` (from a parser's
  `.parse()`), a list of `bankstatementparser.Transaction` objects, or
  a list of plain dicts. Each normalises to a flat table with a stable,
  documented column order.
- Bold header row, one row per record, and auto-sized columns capped at
  60 characters.
- Optional second `Summary` sheet built from a `get_summary()`-style
  mapping (one `Key`/`Value` row per item).
- Spreadsheet-friendly value coercion: `Decimal` → `float`,
  `date`/`datetime` written as native Excel date cells, other scalars
  passed through, everything else stringified.
- Explicit error handling: `TypeError` for unsupported top-level types,
  `ValueError` for unsupported sequence items. Empty input writes an
  empty (or header-only) sheet.
- Five runnable examples covering every supported input shape and
  option (`01_write_dataframe.py`, `02_write_transactions.py`,
  `03_write_dicts.py`, `04_write_with_summary.py`,
  `05_custom_sheet_name.py`). Each writes to a temp file, reads it back
  with openpyxl, and is exercised in CI.
- Quality gates: 100% line + branch test coverage, 100% docstring
  coverage (interrogate), `ruff` lint, and `mypy --strict`. README,
  docs, and example consistency are enforced by an automated suite
  (`test_docs_accuracy.py`, `test_regression_docs.py`,
  `test_regression_examples.py`).

[0.0.1]: https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx/releases/tag/v0.0.1
