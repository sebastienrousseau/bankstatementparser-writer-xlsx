# bankstatementparser-writer-xlsx Roadmap

This roadmap tracks the next set of capabilities for the Excel writer
companion of the
[bankstatementparser](https://github.com/sebastienrousseau/bankstatementparser)
library. The versions are **target** windows; releases ship when the
gates pass, not on a calendar.

## v0.0.1 - Initial release (current)

- Single `write_xlsx(data, path, *, sheet_name, summary)` function
  accepting a pandas `DataFrame`, a list of `Transaction` objects, or a
  list of plain dicts.
- Bold header, one row per record, auto-sized columns, and an optional
  `Summary` sheet from a `get_summary()`-style mapping.
- Decimal/date/datetime coercion to spreadsheet-friendly values.
- 100% line + branch coverage gate, 100% docstring coverage gate,
  `mypy --strict` clean.
- Two runnable examples exercised in CI.

## v0.0.2 - Formatting polish

- Number formats for currency/amount columns (thousands separators,
  configurable decimal places).
- A frozen header row and auto-filter on the Transactions sheet.
- Optional per-column overrides (label, width, number format).

## v0.1.0 - Richer outputs

- Multi-statement workbooks (one sheet per account / statement).
- A totals row and conditional formatting for credits vs. debits.
- Streaming writes for very large statements.

## Out of scope (handled elsewhere)

- **Parsing PDFs / CSVs / camt.053** — see the core
  [`bankstatementparser`](https://github.com/sebastienrousseau/bankstatementparser)
  library.
- **Reading `.xlsx` back into transactions** — not currently planned;
  open an issue if you'd find it useful.
