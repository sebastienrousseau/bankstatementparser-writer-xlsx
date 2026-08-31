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

"""Hypothesis property and fuzz tests for bankstatementparser-writer-xlsx."""

from __future__ import annotations

import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st
from openpyxl.utils.exceptions import IllegalCharacterError

from bankstatementparser_writer_xlsx.writer import (
    _coerce,
    write_xlsx,
)


@settings(max_examples=50, deadline=None)
@given(
    st.lists(
        st.dictionaries(
            st.text(min_size=1, max_size=20),
            st.one_of(
                st.none(),
                st.booleans(),
                st.integers(-1000, 1000),
                st.floats(allow_nan=False, allow_infinity=False),
                st.decimals(
                    min_value=-1000,
                    max_value=1000,
                    allow_nan=False,
                    allow_infinity=False,
                ),
                st.text(max_size=50),
            ),
            max_size=10,
        ),
        max_size=20,
    )
)
def test_fuzz_write_xlsx_arbitrary_records(records: list[dict]) -> None:
    """write_xlsx writes valid XLSX workbooks for arbitrary record lists."""
    with tempfile.NamedTemporaryFile("wb", suffix=".xlsx", delete=False) as f:
        f_path = f.name
    try:
        try:
            write_xlsx(records, f_path)
            assert Path(f_path).stat().st_size > 0
        except (IllegalCharacterError, ValueError):
            pass
    finally:
        Path(f_path).unlink(missing_ok=True)


@settings(max_examples=30, deadline=None)
@given(
    st.dictionaries(
        st.text(min_size=1, max_size=30),
        st.one_of(st.text(max_size=50), st.integers(-100, 100), st.none()),
        max_size=10,
    )
)
def test_fuzz_write_xlsx_with_summary(summary_dict: dict) -> None:
    """write_xlsx handles arbitrary summary mappings cleanly."""
    with tempfile.NamedTemporaryFile("wb", suffix=".xlsx", delete=False) as f:
        f_path = f.name
    try:
        try:
            write_xlsx([{"col1": "val1"}], f_path, summary=summary_dict)
            assert Path(f_path).stat().st_size > 0
        except (IllegalCharacterError, ValueError):
            pass
    finally:
        Path(f_path).unlink(missing_ok=True)


@settings(max_examples=30, deadline=None)
@given(st.text(min_size=1, max_size=31))
def test_fuzz_write_xlsx_arbitrary_sheet_name(name: str) -> None:
    """write_xlsx handles arbitrary sheet names safely."""
    with tempfile.NamedTemporaryFile("wb", suffix=".xlsx", delete=False) as f:
        f_path = f.name
    try:
        try:
            write_xlsx([{"a": 1}], f_path, sheet_name=name)
            assert Path(f_path).stat().st_size > 0
        except (IllegalCharacterError, ValueError):
            pass
    finally:
        Path(f_path).unlink(missing_ok=True)


@settings(max_examples=50, deadline=None)
@given(
    st.one_of(st.none(), st.booleans(), st.integers(), st.floats(), st.text())
)
def test_fuzz_coerce_cell_value(val) -> None:
    """_coerce handles any primitive without raising."""
    res = _coerce(val)
    assert res is not None or val is None
