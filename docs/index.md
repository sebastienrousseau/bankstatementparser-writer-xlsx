# bankstatementparser-writer-xlsx

**bankstatementparser-writer-xlsx** writes already-parsed bank-statement
records to an Excel `.xlsx` workbook: a bold header row, one row per
transaction, auto-sized columns and an optional `Summary` sheet. It
takes the output of a
[`bankstatementparser`](https://github.com/sebastienrousseau/bankstatementparser)
parser as a pandas `DataFrame`, a list of `Transaction` objects or a
list of plain `dict` records.

| Concern | How this writer handles it |
| :--- | :--- |
| Input shapes | `DataFrame` (its column order), `list[Transaction]` (the stable field order), `list[dict]` (keys in first-seen order) |
| Amounts | `Decimal` written as a number, so spreadsheets sort and sum it |
| Dates | `date` and `datetime` written as native Excel date cells |
| Layout | Bold header, columns auto-sized to the widest cell and capped at 60 characters |
| Summary | An optional mapping written to a second `Summary` sheet as key/value rows |
| Errors | `TypeError` for an unsupported container, `ValueError` for unsupported items or text an `.xlsx` cannot hold |

## In this manual

- [Workbook output](format.md): input shapes, value coercion, the
  summary sheet and errors.
- [The suite](suite.md): the `bankstatementparser` packages.
- [Comparison](COMPARISON.md) and [Benchmarks](BENCHMARKS.md).
- [Supported Python policy](POLICIES.md).
- [API reference](api.md): generated from the docstrings.
- [Roadmap](roadmap.md), [Changelog](changelog.md) and
  [Security policy](security.md).

The source, issues and releases live on
[GitHub](https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx);
the package is on
[PyPI](https://pypi.org/project/bankstatementparser-writer-xlsx/).
