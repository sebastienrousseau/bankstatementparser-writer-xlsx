# bankstatementparser-writer-xlsx examples

Runnable, self-contained examples for the Excel writer. Together they
exercise every supported input shape and option of `write_xlsx`. Run any
of them from the repository root:

```sh
python examples/<name>.py
```

| Example | Demonstrates |
|---------|--------------|
| [`01_write_dataframe.py`](01_write_dataframe.py) | Writing a pandas `DataFrame` (the DataFrame's own column order) to a single-sheet workbook |
| [`02_write_transactions.py`](02_write_transactions.py) | Writing a list of `bankstatementparser.Transaction` objects with the stable field column order |
| [`03_write_dicts.py`](03_write_dicts.py) | Writing a list of plain `dict` records (header is the union of keys, first-seen order) |
| [`04_write_with_summary.py`](04_write_with_summary.py) | Adding a second `Summary` sheet via `summary=` (a `get_summary()`-style mapping) |
| [`05_custom_sheet_name.py`](05_custom_sheet_name.py) | Renaming the transactions sheet with `sheet_name=` |

Each script writes its workbook to a temporary file, reads it back with
`openpyxl` to prove it round-trips, prints a short summary, and exits 0.
No files are left behind and no network access is required. Every script
is exercised in CI on every commit.

Install this package (it pulls in `bankstatementparser`, `openpyxl`, and
`pandas`) first:

```sh
pip install bankstatementparser-writer-xlsx   # Python 3.10+
```
