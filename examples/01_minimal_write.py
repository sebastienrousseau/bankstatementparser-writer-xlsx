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

"""Minimal example: write a list of Transactions to an Excel workbook.

Run with ``python examples/01_minimal_write.py``. The output file
``out_minimal.xlsx`` is written to the current directory.
"""

from datetime import date
from decimal import Decimal
from pathlib import Path

from bankstatementparser import Transaction

from bankstatementparser_writer_xlsx import write_xlsx


def main() -> None:
    """Build two transactions and write them to a workbook."""
    transactions = [
        Transaction(
            account_id="DE89370400440532013000",
            currency="EUR",
            amount=Decimal("1250.75"),
            booking_date=date(2026, 6, 1),
            description="ACME GmbH invoice 123",
            counterparty="ACME GmbH",
        ),
        Transaction(
            account_id="DE89370400440532013000",
            currency="EUR",
            amount=Decimal("-42.00"),
            booking_date=date(2026, 6, 3),
            description="Coffee Shop",
            counterparty="Coffee Shop",
        ),
    ]
    out = Path("out_minimal.xlsx")
    write_xlsx(transactions, out)
    print(f"Wrote {out.resolve()}")


if __name__ == "__main__":
    main()
