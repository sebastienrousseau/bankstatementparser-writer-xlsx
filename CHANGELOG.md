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
- Two runnable examples (`01_minimal_write.py`,
  `02_write_with_summary.py`) exercised in CI.
- Quality gates: 100% line + branch test coverage, 100% docstring
  coverage (interrogate), `ruff` lint, and `mypy --strict`.

[0.0.1]: https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx/releases/tag/v0.0.1
