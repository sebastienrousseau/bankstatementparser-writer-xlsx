# Comparison

Where bankstatementparser-writer-xlsx fits next to `pandas`'
`DataFrame.to_excel`, the usual way to get a parsed statement into a
spreadsheet. The pandas column comes from writing one `DataFrame` with
`to_excel(path, index=False)` (pandas 2.3.3, openpyxl engine) and
reading the workbook back with openpyxl on 2026-11-27; nothing here is
a measured ranking.

| Capability | **bankstatementparser-writer-xlsx** | `pandas.DataFrame.to_excel` |
| :--- | :--- | :--- |
| Input | `DataFrame`, `list[Transaction]` or `list[dict]` | `DataFrame` |
| `Decimal` amounts | Number cells | Text cells, which a spreadsheet will not sum |
| Dates | Native date cells | Native date cells |
| Header row | Bold | Bold |
| Column widths | Auto-sized to the widest cell, capped at 60 characters | Left at the default |
| Summary sheet | `summary=` writes a `Summary` sheet | Not built in |
| Index column | Never written | Written unless `index=False` |

## When each fits

- **bankstatementparser-writer-xlsx**: you hold `Transaction` objects or
  a parser's output and want a workbook an accountant can sum and read
  without reformatting.
- **`DataFrame.to_excel`**: you already shape the frame yourself, need
  pandas' styling hooks or several frames on several sheets, and convert
  `Decimal` amounts to numbers first.

The wider family is listed in [The suite](suite.md).
