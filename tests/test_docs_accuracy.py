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

"""Automated validation that README, docs, and examples stay in sync
with the actual codebase.

If any of these tests fail, the corresponding markdown file has a stale
claim that a human will trust and act on. Fix the docs, not the test.
"""

from __future__ import annotations

import re
from pathlib import Path

import bankstatementparser_writer_xlsx
from bankstatementparser_writer_xlsx import __version__
from bankstatementparser_writer_xlsx.writer import _MAX_COLUMN_WIDTH

REPO_ROOT = Path(__file__).resolve().parents[1]
README = REPO_ROOT / "README.md"
CHANGELOG = REPO_ROOT / "CHANGELOG.md"
PYPROJECT = REPO_ROOT / "pyproject.toml"
EXAMPLES_DIR = REPO_ROOT / "examples"
EXAMPLES_README = EXAMPLES_DIR / "README.md"


def _read(path: Path) -> str:
    """Read a UTF-8 text file."""
    return path.read_text(encoding="utf-8")


def _pyproject_version() -> str:
    """Extract the version string from pyproject.toml."""
    match = re.search(
        r'^version\s*=\s*"([^"]+)"', _read(PYPROJECT), re.MULTILINE
    )
    assert match is not None, "pyproject.toml has no version field"
    return match.group(1)


def _example_scripts() -> list[Path]:
    """Return every runnable example script (``examples/*.py``)."""
    return sorted(
        p for p in EXAMPLES_DIR.glob("*.py") if "__pycache__" not in str(p)
    )


# ----------------------------------------------------------------------
# 1. Version consistency
# ----------------------------------------------------------------------


class TestVersionConsistency:
    """The version string agrees across package, pyproject, README."""

    def test_package_version_matches_pyproject(self) -> None:
        """``__version__`` equals the pyproject ``version`` field."""
        assert __version__ == _pyproject_version()

    def test_dunder_version_is_module_attribute(self) -> None:
        """The package re-exports ``__version__`` at the top level."""
        assert bankstatementparser_writer_xlsx.__version__ == __version__

    def test_readme_mentions_current_version(self) -> None:
        """The README's release line shows the current version."""
        assert f"v{__version__}" in _read(
            README
        ), f"README should mention v{__version__}"

    def test_changelog_has_current_version_entry(self) -> None:
        """The CHANGELOG has a heading for the current version."""
        assert f"[{__version__}]" in _read(
            CHANGELOG
        ), f"CHANGELOG has no entry for current version {__version__}"


# ----------------------------------------------------------------------
# 2. Public API surface documented
# ----------------------------------------------------------------------


class TestApiSurface:
    """Every public symbol is mentioned in the README."""

    readme_text = _read(README)

    def test_all_public_symbols_documented(self) -> None:
        """Each name in ``__all__`` is documented in the README."""
        for name in bankstatementparser_writer_xlsx.__all__:
            if name == "__version__":
                continue  # the version is checked separately, by value
            assert name in self.readme_text, (
                f"README doesn't mention public symbol '{name}' "
                f"(exported in __all__)"
            )

    def test_write_xlsx_is_the_sole_public_callable(self) -> None:
        """The documented public callable is exactly ``write_xlsx``."""
        callables = [
            name
            for name in bankstatementparser_writer_xlsx.__all__
            if name != "__version__"
        ]
        assert callables == ["write_xlsx"]

    def test_signature_keywords_documented(self) -> None:
        """Every keyword argument of ``write_xlsx`` is documented."""
        for keyword in ("sheet_name", "summary"):
            assert (
                keyword in self.readme_text
            ), f"README doesn't document the '{keyword}' argument"


# ----------------------------------------------------------------------
# 3. Example paths referenced actually exist
# ----------------------------------------------------------------------


class TestExamplesExist:
    """Example scripts referenced in docs exist on disk."""

    readme_text = _read(README)
    examples_readme_text = _read(EXAMPLES_README)

    def _referenced_scripts(self, text: str) -> list[str]:
        """Pull ``NN_name.py`` example script names from markdown."""
        return re.findall(r"`(\d\d_[\w]+\.py)`", text)

    def test_readme_example_scripts_exist(self) -> None:
        """Every example script named in the README exists."""
        names = self._referenced_scripts(self.readme_text)
        assert names, "README should reference example scripts"
        for name in names:
            assert (
                EXAMPLES_DIR / name
            ).exists(), (
                f"README references examples/{name} but it doesn't exist"
            )

    def test_examples_readme_scripts_exist(self) -> None:
        """Every example script named in examples/README.md exists."""
        names = self._referenced_scripts(self.examples_readme_text)
        assert names, "examples/README.md should reference example scripts"
        for name in names:
            assert (
                EXAMPLES_DIR / name
            ).exists(), (
                f"examples/README.md references {name} but it doesn't exist"
            )

    def test_every_example_is_documented(self) -> None:
        """Every shipped example is listed in examples/README.md."""
        documented = set(self._referenced_scripts(self.examples_readme_text))
        for script in _example_scripts():
            assert (
                script.name in documented
            ), f"examples/{script.name} is not listed in examples/README.md"


# ----------------------------------------------------------------------
# 4. Numeric claims match reality
# ----------------------------------------------------------------------


class TestNumericClaims:
    """Numbers in the docs match the codebase."""

    readme_text = _read(README)
    changelog_text = _read(CHANGELOG)

    def test_example_count_claim_matches_reality(self) -> None:
        """The README's spelled-out example count matches the file count."""
        count = len(_example_scripts())
        words = {
            2: "Two",
            3: "Three",
            4: "Four",
            5: "Five",
            6: "Six",
        }
        assert count in words, f"unexpected example count {count}"
        assert f"{words[count]} runnable examples" in self.readme_text, (
            f"README should say '{words[count]} runnable examples' "
            f"(found {count} example scripts)"
        )

    def test_max_column_width_claim_matches_constant(self) -> None:
        """The documented column-width cap matches ``_MAX_COLUMN_WIDTH``."""
        assert f"{_MAX_COLUMN_WIDTH} characters" in self.changelog_text, (
            f"CHANGELOG should mention the {_MAX_COLUMN_WIDTH}-character "
            f"column-width cap"
        )

    def test_python_minimum_matches_pyproject(self) -> None:
        """The README's minimum Python version matches pyproject."""
        pyproject = _read(PYPROJECT)
        match = re.search(r'python\s*=\s*">=(\d+\.\d+)', pyproject)
        assert match is not None
        minimum = match.group(1)
        assert (
            minimum in self.readme_text
        ), f"README should mention Python {minimum} as the minimum"
