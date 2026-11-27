# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2023-2026 Sebastien Rousseau. All rights reserved.

"""Text an ``.xlsx`` cannot hold is refused with ``ValueError``.

OOXML is XML 1.0, which cannot carry most C0 control characters
(``\\x00``-``\\x08``, ``\\x0b``, ``\\x0c``, ``\\x0e``-``\\x1f``). Before
this was pinned, such a character anywhere in a value, a column name or
the summary escaped as openpyxl's ``IllegalCharacterError``, which is
not one of the errors ``write_xlsx`` documents.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from bankstatementparser_writer_xlsx import write_xlsx


@pytest.mark.parametrize("bad", ["a\x00b", "tab\x0bvertical", "\x1f"])
def test_control_character_in_a_value(tmp_path: Path, bad: str) -> None:
    """A control character in a row value is a ValueError."""
    with pytest.raises(ValueError, match="cannot be used"):
        write_xlsx([{"description": bad}], tmp_path / "out.xlsx")


def test_control_character_in_a_column_name(tmp_path: Path) -> None:
    """A control character in a dict key (the header) is a ValueError."""
    with pytest.raises(ValueError, match="cannot be used"):
        write_xlsx([{"desc\x07": "x"}], tmp_path / "out.xlsx")


def test_control_character_in_the_summary(tmp_path: Path) -> None:
    """A control character in a summary value is a ValueError."""
    with pytest.raises(ValueError, match="cannot be used"):
        write_xlsx(
            [{"a": 1}], tmp_path / "out.xlsx", summary={"note": "x\x01"}
        )


def test_tab_and_newline_are_kept(tmp_path: Path) -> None:
    """Tab, newline and carriage return are legal XML and still write."""
    out = write_xlsx([{"d": "a\tb\nc\rd"}], tmp_path / "out.xlsx")
    assert out.exists()
