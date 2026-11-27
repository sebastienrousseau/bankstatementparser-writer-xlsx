# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2023-2026 Sebastien Rousseau. All rights reserved.

"""Text is never written as a formula (CWE-1236).

Bank free text reaches ``write_xlsx`` unchanged, and a payer can choose
part of it. openpyxl stores any ``str`` that starts with ``=`` as a
formula, so before this was pinned a description such as
``=HYPERLINK("http://x","click")`` became a live formula in the
exported workbook. Every string must be a plain string cell holding
exactly the original text.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from openpyxl import load_workbook

from bankstatementparser_writer_xlsx import write_xlsx

_PAYLOADS = [
    '=HYPERLINK("http://x","click")',
    "=1+1",
    "+1+1",
    "-2+3",
    "@SUM(1)",
    "\t=1+1",
    "\r=1+1",
    "-12.50",
]


def _cells(path: Path) -> list:
    """Every non-empty cell of every sheet in the workbook at ``path``."""
    workbook = load_workbook(path)
    return [
        cell
        for sheet in workbook.worksheets
        for row in sheet.iter_rows()
        for cell in row
        if cell.value is not None
    ]


@pytest.mark.parametrize("text", _PAYLOADS)
def test_value_is_plain_text(tmp_path: Path, text: str) -> None:
    """A row value round-trips as the exact string, never a formula."""
    out = write_xlsx([{"description": text}], tmp_path / "out.xlsx")
    cell = load_workbook(out).active["A2"]
    assert cell.data_type == "s"
    assert cell.value == text


def test_header_and_summary_are_plain_text(tmp_path: Path) -> None:
    """Column names, summary keys and summary values are text too."""
    out = write_xlsx(
        [{"=cmd": "=1+1"}],
        tmp_path / "out.xlsx",
        summary={"=key": '=HYPERLINK("http://x","click")'},
    )
    cells = _cells(out)
    assert all(cell.data_type != "f" for cell in cells)
    values = {cell.value for cell in cells}
    assert {"=cmd", "=1+1", "=key"} <= values
    assert '=HYPERLINK("http://x","click")' in values
