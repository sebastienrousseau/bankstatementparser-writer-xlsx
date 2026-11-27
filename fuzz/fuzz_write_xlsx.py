# Copyright (C) 2023-2026 Bank Statement Parser. All rights reserved.
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

"""Coverage-guided Atheris fuzz target for the XLSX writer.

``write_xlsx`` takes whatever a parser produced, and bank free text
reaches it unchanged. It promises two failure modes for bad input:
``TypeError`` (an unsupported container) and ``ValueError`` (mixed or
unsupported items, text an ``.xlsx`` cannot hold, an invalid sheet
name). Each input builds dict records with fuzzed keys and values
(text, ``Decimal``, integers, dates, ``None``), an optional summary
and a sheet name, and writes them. Any other exception escapes the
target and libFuzzer records it as a crash; so does a workbook that
does not reopen with one row per record under its header.

Run (Linux x86_64, Python 3.12+, ``poetry install --with fuzz``)::

    python fuzz/fuzz_write_xlsx.py -max_total_time=60
"""

from __future__ import annotations

import sys
import tempfile
from datetime import date
from decimal import Decimal
from pathlib import Path

import atheris

with atheris.instrument_imports():
    from openpyxl import load_workbook

    from bankstatementparser_writer_xlsx import write_xlsx

_OUT = Path(tempfile.mkdtemp()) / "fuzz.xlsx"


def _value(fdp: atheris.FuzzedDataProvider) -> object:
    """Draw one cell value of a type a parser can emit."""
    kind = fdp.ConsumeIntInRange(0, 4)
    if kind == 0:
        return fdp.ConsumeUnicodeNoSurrogates(24)
    if kind == 1:
        return Decimal(fdp.ConsumeIntInRange(-(10**12), 10**12)) / 100
    if kind == 2:
        return fdp.ConsumeInt(8)
    if kind == 3:
        return date.fromordinal(fdp.ConsumeIntInRange(1, 3_652_059))
    return None


def _records(fdp: atheris.FuzzedDataProvider) -> list[dict[str, object]]:
    """Draw up to four dict records over up to three fuzzed keys."""
    keys = [fdp.ConsumeUnicodeNoSurrogates(8) for _ in range(3)]
    return [
        {keys[fdp.ConsumeIntInRange(0, 2)]: _value(fdp) for _ in range(3)}
        for _ in range(fdp.ConsumeIntInRange(0, 4))
    ]


def test_one_input(data: bytes) -> None:
    """Write one fuzzed table (and maybe a summary) and reopen it."""
    fdp = atheris.FuzzedDataProvider(data)
    records = _records(fdp)
    summary = {"note": _value(fdp)} if fdp.ConsumeBool() else None
    sheet_name = fdp.ConsumeUnicodeNoSurrogates(12) or "Transactions"
    try:
        write_xlsx(records, _OUT, sheet_name=sheet_name, summary=summary)
    except (TypeError, ValueError):
        return
    expected = len(records) + 1 if records else 1
    rows = load_workbook(_OUT, read_only=True).worksheets[0].max_row
    if rows != expected:
        raise AssertionError(f"{rows} rows written, expected {expected}")


def main() -> None:
    """Hand the target to libFuzzer with the command-line options."""
    atheris.Setup(sys.argv, test_one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
