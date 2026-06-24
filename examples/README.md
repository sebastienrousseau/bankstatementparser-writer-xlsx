# bankstatementparser-writer-xlsx examples

Runnable, self-contained examples for the Excel writer. Run any of them
from the repository root:

```sh
python examples/<name>.py
```

| Example | Demonstrates |
|---------|--------------|
| [`01_minimal_write.py`](01_minimal_write.py) | Writing a list of `bankstatementparser.Transaction` objects to a single-sheet workbook |
| [`02_write_with_summary.py`](02_write_with_summary.py) | Writing a pandas DataFrame plus a second `Summary` sheet built from a `get_summary()`-style mapping |

Each script writes its workbook (`out_minimal.xlsx`, `out_summary.xlsx`)
to the current directory and is exercised in CI on every commit.

Install this package (it pulls in `bankstatementparser`, `openpyxl`, and
`pandas`) first:

```sh
pip install bankstatementparser-writer-xlsx   # Python 3.10+
```
