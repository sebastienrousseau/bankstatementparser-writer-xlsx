# Copyright (C) 2023-2026 Sebastien Rousseau.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example: write a DataFrame plus a Summary sheet.

This mirrors the real workflow: a ``bankstatementparser`` parser
returns a DataFrame from ``.parse()`` and a summary mapping from
``.get_summary()``. Here both are built inline so the script runs with
no input files.

Run with ``python examples/02_write_with_summary.py``. The output file
``out_summary.xlsx`` is written to the current directory.
"""

from datetime import date
from decimal import Decimal
from pathlib import Path

import pandas as pd

from bankstatementparser_writer_xlsx import write_xlsx


def main() -> None:
    """Write a DataFrame and an accompanying Summary sheet."""
    frame = pd.DataFrame(
        {
            "date": [date(2026, 6, 1), date(2026, 6, 3)],
            "description": ["Salary", "Coffee Shop"],
            "amount": [Decimal("3000.00"), Decimal("-4.20")],
            "currency": ["EUR", "EUR"],
        }
    )
    summary = {
        "account_id": "DE89370400440532013000",
        "transaction_count": len(frame),
        "total_amount": Decimal("2995.80"),
        "currency": "EUR",
    }
    out = Path("out_summary.xlsx")
    write_xlsx(frame, out, summary=summary)
    print(f"Wrote {out.resolve()} with Transactions + Summary sheets")


if __name__ == "__main__":
    main()
