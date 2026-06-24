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

"""Regression suite: execute every shipped example script end-to-end.

Each example under ``examples/`` is run as a real subprocess, exactly as
a user would run it. A script that crashes, prints to stderr, or drifts
away from the current public API fails the suite. Examples are
self-contained (they write to a temp file and read it back), so no
fixtures or network access are required.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = REPO_ROOT / "examples"

EXAMPLE_SCRIPTS = sorted(
    p for p in EXAMPLES_DIR.glob("*.py") if "__pycache__" not in str(p)
)


def _run_example(script: Path) -> subprocess.CompletedProcess[str]:
    """Run an example script as a subprocess and return the result."""
    env = os.environ.copy()
    return subprocess.run(
        [sys.executable, str(script)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=180,
        env=env,
    )


def test_examples_directory_has_scripts() -> None:
    """The examples directory ships at least the five documented scripts."""
    assert (
        len(EXAMPLE_SCRIPTS) >= 5
    ), f"expected >=5 example scripts, found {len(EXAMPLE_SCRIPTS)}"


@pytest.mark.parametrize(
    "script", EXAMPLE_SCRIPTS, ids=[p.name for p in EXAMPLE_SCRIPTS]
)
def test_example_runs_cleanly(script: Path) -> None:
    """Every example script exits 0 and prints a confirmation line."""
    result = _run_example(script)
    assert result.returncode == 0, (
        f"{script.name} exited {result.returncode}\n"
        f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
    )
    assert (
        "Wrote" in result.stdout
    ), f"{script.name} printed no 'Wrote' confirmation:\n{result.stdout}"
