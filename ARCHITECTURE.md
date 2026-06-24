<!-- SPDX-License-Identifier: Apache-2.0 -->

# bankstatementparser-writer-xlsx Architecture

A map of the codebase for new contributors and maintainers. The goal is
that anyone can navigate, extend, and reason about the writer without
prior context.

## The pipeline

```
bankstatementparser parser (.parse() / .get_summary())
        |  DataFrame / list[Transaction] / list[dict]   +   summary mapping
        v
bankstatementparser_writer_xlsx.write_xlsx(data, path, *, sheet_name, summary)
        |  normalise -> (columns, rows) -> openpyxl
        v
.xlsx workbook  (Transactions sheet [+ optional Summary sheet])
```

The writer is deliberately thin: it consumes data that the
[`bankstatementparser`](https://github.com/sebastienrousseau/bankstatementparser)
core has already parsed and normalised, then emits a clean Excel file.
It performs no parsing, no validation of untrusted input, and no
network I/O.

## Module map

| Area | Module | Responsibility |
| :--- | :--- | :--- |
| **Public API** | `bankstatementparser_writer_xlsx/writer.py` | `write_xlsx()` plus private normalisation, coercion, and layout helpers |
| **Package surface** | `bankstatementparser_writer_xlsx/__init__.py` | Re-exports `write_xlsx`; single source of truth for `__version__` |
| **Tests** | `tests/test_writer.py` | Round-trips every input shape and reads the workbook back with `openpyxl.load_workbook` |
| **Examples** | `examples/` | One runnable script per usage shape (minimal write, write-with-summary) |
| **Release helpers** | `scripts/verify_versions.py` | Asserts `__version__`, `pyproject.toml`, and `CHANGELOG.md` agree |

## How `write_xlsx` works

1. **Normalise.** `_normalise()` dispatches on the input type:
   - a `pandas.DataFrame` keeps its own column order
     (`_normalise_dataframe`);
   - a `list`/`tuple` is turned into ordered dict records
     (`_normalise_sequence` → `_to_record`), where `Transaction`
     objects are serialised via `model_dump()` in a stable field order
     and plain dicts contribute the union of their keys in first-seen
     order.
2. **Coerce.** Every cell passes through `_coerce()`: `Decimal` →
   `float`, `date`/`datetime` left as native Excel date cells, scalars
   passed through, everything else stringified.
3. **Write.** `_write_table()` appends a bold header and the data rows,
   then `_autosize()` widens each column to its widest cell (capped at
   60 characters). When a `summary` mapping is supplied,
   `_write_summary()` adds a second `Summary` sheet of key/value rows.
4. **Return.** The resolved output `Path` is returned so callers can
   chain on it.

## Key design decisions

- **Three input shapes, one table.** A parser's `.parse()` returns a
  DataFrame, but callers may already hold `Transaction` objects or raw
  dicts. All three normalise to the same `(columns, rows)` pair.
- **Stable column order.** `Transaction` rows follow a fixed field
  order, so two runs over the same data always produce the same
  workbook layout — friendly to diffs and downstream column-by-name
  tooling.
- **Decimal → float, documented and tested.** Excel has no decimal
  type. Floats sort and aggregate natively in spreadsheets; the choice
  is exercised by an explicit test.
- **Errors are explicit.** Unsupported top-level types raise
  `TypeError`; unsupported sequence items raise `ValueError`. Empty
  input is a valid, documented path, not an error.
- **Coverage enforced at 100%** line + branch and docstring.

## Extension points

- **A new input shape:** add a branch in `_normalise()` and a matching
  `_normalise_*` helper, then a round-trip test.
- **A new sheet:** add a `_write_*` helper and create the sheet in
  `write_xlsx()`.

## Where to look first

- Runnable examples: [`examples/`](examples/)
- Roadmap: [`ROADMAP.md`](ROADMAP.md)
- Release process: [`RELEASING.md`](RELEASING.md)
- Parent library: [`bankstatementparser`](https://github.com/sebastienrousseau/bankstatementparser)
