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

"""Regression suite: every code example in the docs must actually work.

The docs-accuracy tests check that claims in the docs match the
codebase; this module goes further and *executes* the documented
``python`` examples themselves:

* Every fenced ``python`` block in README.md and ``docs/*.md`` must be
  classified in ``BLOCK_SPECS`` below. Adding a new python block to the
  docs without classifying it fails the suite -- examples cannot
  silently rot.
* ``run`` blocks are executed verbatim with the working directory set to
  a temp directory, so any ``write_xlsx(..., "name.xlsx")`` lands in the
  temp path and never touches the repository.
* Placeholder input paths (e.g. ``statement.csv``) are materialised as
  real fixture files in that temp directory before the block runs.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_FILES = ("README.md",) + tuple(
    str(p.relative_to(REPO_ROOT))
    for p in sorted((REPO_ROOT / "docs").glob("*.md"))
)

# A minimal, well-formed CSV the bankstatementparser CSV parser accepts.
_STATEMENT_CSV = (
    "date,description,amount,currency\n"
    "2026-06-01,Salary,3000.00,EUR\n"
    "2026-06-03,Coffee Shop,-4.20,EUR\n"
)


# ----------------------------------------------------------------------
# Block extraction
# ----------------------------------------------------------------------


@dataclass(frozen=True)
class DocBlock:
    """One fenced code block extracted from a documentation file."""

    doc: str
    line: int
    lang: str
    body: str

    @property
    def location(self) -> str:
        """A ``file:line`` label used as the pytest parametrize id."""
        return f"{self.doc}:{self.line}"


def _extract_blocks() -> list[DocBlock]:
    """Extract every fenced code block from the scanned doc files."""
    blocks: list[DocBlock] = []
    for rel in DOC_FILES:
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        for match in re.finditer(
            r"^```(\w*)\n(.*?)^```", text, re.DOTALL | re.MULTILINE
        ):
            blocks.append(
                DocBlock(
                    doc=rel,
                    line=text[: match.start()].count("\n") + 1,
                    lang=match.group(1),
                    body=match.group(2),
                )
            )
    return blocks


ALL_BLOCKS = _extract_blocks()
PYTHON_BLOCKS = [b for b in ALL_BLOCKS if b.lang == "python"]


# ----------------------------------------------------------------------
# Classification registry
# ----------------------------------------------------------------------


@dataclass(frozen=True)
class BlockSpec:
    """How to exercise one documented ``python`` block.

    ``marker`` is a substring unique to exactly one python block across
    all scanned docs; ``files`` maps placeholder paths used in the block
    to real fixture contents materialised in the working directory.
    """

    marker: str
    files: tuple[tuple[str, str], ...] = ()


BLOCK_SPECS: tuple[BlockSpec, ...] = (
    # README -- Quick start (parse a CSV, write a workbook).
    BlockSpec(
        marker='write_xlsx(df, "statement.xlsx")         # one polished',
        files=(("statement.csv", _STATEMENT_CSV),),
    ),
    # README -- Quick start, add a summary sheet.
    BlockSpec(
        marker="summary=parser.get_summary()",
        files=(("statement.csv", _STATEMENT_CSV),),
    ),
    # README -- The summary sheet (explicit summary mapping).
    BlockSpec(
        marker='"transaction_count": 128,',
    ),
)


def _matching_blocks(spec: BlockSpec) -> list[DocBlock]:
    """Return the python blocks whose body contains ``spec.marker``."""
    return [b for b in PYTHON_BLOCKS if spec.marker in b.body]


# ----------------------------------------------------------------------
# Structural guarantees
# ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "block", PYTHON_BLOCKS, ids=[b.location for b in PYTHON_BLOCKS]
)
def test_python_block_is_valid_syntax(block: DocBlock) -> None:
    """Every documented python block is syntactically valid."""
    ast.parse(block.body, filename=block.location)


def test_every_python_block_is_classified() -> None:
    """Each documented python block maps to exactly one BlockSpec."""
    unmatched = [
        b.location
        for b in PYTHON_BLOCKS
        if not any(spec.marker in b.body for spec in BLOCK_SPECS)
    ]
    assert not unmatched, (
        "Unclassified python blocks in docs (add a BlockSpec so the "
        f"example is executed by the regression suite): {unmatched}"
    )

    for spec in BLOCK_SPECS:
        matches = _matching_blocks(spec)
        assert len(matches) == 1, (
            f"BlockSpec marker {spec.marker!r} must match exactly one "
            f"block, matched {[b.location for b in matches]}"
        )


# ----------------------------------------------------------------------
# Execution
# ----------------------------------------------------------------------


def _spec_id(spec: BlockSpec) -> str:
    """Build a readable pytest id (the block location) for a spec."""
    blocks = _matching_blocks(spec)
    return blocks[0].location if blocks else spec.marker[:30]


@pytest.mark.parametrize(
    "spec", BLOCK_SPECS, ids=[_spec_id(s) for s in BLOCK_SPECS]
)
def test_documented_python_block(
    spec: BlockSpec,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Execute a documented python block against temp fixtures."""
    blocks = _matching_blocks(spec)
    assert len(blocks) == 1
    block = blocks[0]

    monkeypatch.chdir(tmp_path)
    for placeholder, contents in spec.files:
        target = tmp_path / placeholder
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(contents, encoding="utf-8")

    namespace: dict[str, object] = {"__name__": "bsp_xlsx_doc_example"}
    exec(compile(block.body, block.location, "exec"), namespace)
    capsys.readouterr()  # examples are allowed to print
