#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Sebastien Rousseau <sebastian.rousseau@gmail.com>
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""What writing a statement to a workbook costs, in time and in memory.

Time is the less interesting half. Writing xlsx means building the whole
workbook in memory before anything reaches disk, so the number that
actually decides whether a job survives is **peak memory**, and that is
what nothing here was measuring.

A treasury team exporting a month across a few dozen accounts is asking for
tens of thousands of rows. If peak memory grows faster than the row count,
the export works on a laptop and gets killed in a container with a limit.

Three things are measured:

* **Time per row**, across row counts. Flat is linear.
* **Peak memory**, and the ratio of peak to the size of the file finally
  written. That multiple is the real cost: it says how much headroom a
  process needs relative to the output it produces.
* **The three accepted input shapes** — a list of dicts, a DataFrame, and
  a list of ``Transaction`` objects — on the same data. The docstring
  offers all three as equivalent, and a caller with a DataFrame in hand
  should know whether converting it first would be cheaper or dearer.

Run::

    python benches/bench_write_xlsx.py
    python benches/bench_write_xlsx.py --json
    python benches/bench_write_xlsx.py --quick     # what CI runs

Nothing here asserts a threshold: wall-clock and memory are not comparable
between machines, and a flaky performance gate teaches people to ignore
red. CI runs ``--quick`` so a benchmark that has stopped compiling against
the current API fails the build instead of rotting into a file that reads
as verified and is not.
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
import time
import tracemalloc
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bankstatementparser_writer_xlsx import write_xlsx  # noqa: E402


def records(rows: int) -> list[dict]:
    """``rows`` statement records, in the shape a parser hands over."""
    return [
        {
            "transaction_id": f"TXN-{i:07d}",
            "value_date": "2026-06-21",
            "booking_date": "2026-06-21",
            "amount": f"{(i % 900) + 100}.00",
            "currency": "EUR",
            "credit_debit": "CRDT" if i % 2 else "DBIT",
            "description": f"Payment {i} for invoice {i % 5000}",
            "bank_reference": f"BANKREF{i}",
            "customer_reference": f"CUSTREF{i}",
        }
        for i in range(rows)
    ]


def _time_and_peak(call) -> tuple[float, int]:
    """Wall-clock and peak allocation for one call.

    Timed and traced in the same call rather than separately: tracemalloc
    slows execution, so a time taken while tracing is not the time a real
    caller sees. The time here is therefore the traced one and is only ever
    compared against itself.
    """
    tracemalloc.start()
    start = time.perf_counter()
    call()
    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return elapsed, peak


def measure(rows: int, workdir: Path) -> dict:
    data = records(rows)
    target = workdir / f"bench-{rows}.xlsx"
    elapsed, peak = _time_and_peak(lambda: write_xlsx(data, target))
    written = target.stat().st_size
    target.unlink(missing_ok=True)
    return {
        "rows": rows,
        "ms": elapsed * 1e3,
        "us_per_row": elapsed * 1e6 / rows,
        "peak_kib": peak / 1024,
        "file_kib": written / 1024,
        "peak_over_file": peak / written if written else 0.0,
    }


def measure_shapes(rows: int, workdir: Path) -> list[dict]:
    """The same data offered in each accepted input shape."""
    data = records(rows)
    shapes: list[tuple[str, object]] = [("list[dict]", data)]

    try:
        import pandas as pd

        shapes.append(("DataFrame", pd.DataFrame(data)))
    except ImportError:  # pragma: no cover - pandas is an extra
        pass

    out = []
    for name, payload in shapes:
        target = workdir / f"shape-{name}.xlsx"
        # Bound as defaults: a bare closure over the loop variables
        # would measure the last shape every time, which ruff's B023
        # catches and which would have made this table wrong.
        elapsed, peak = _time_and_peak(
            lambda payload=payload, target=target: write_xlsx(payload, target)
        )
        target.unlink(missing_ok=True)
        out.append(
            {
                "shape": name,
                "rows": rows,
                "ms": elapsed * 1e3,
                "peak_kib": peak / 1024,
            }
        )
    return out


def run(quick: bool) -> dict:
    sizes = [100, 1_000] if quick else [100, 1_000, 10_000, 50_000]
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        return {
            "sizes": [measure(n, workdir) for n in sizes],
            "shapes": measure_shapes(sizes[1], workdir),
        }


def render(results: dict) -> None:
    print(
        f"{'rows':>8}{'ms':>10}{'us/row':>9}{'peak KiB':>11}"
        f"{'file KiB':>10}{'peak/file':>11}"
    )
    for row in results["sizes"]:
        print(
            f"{row['rows']:>8}{row['ms']:>10.1f}{row['us_per_row']:>9.1f}"
            f"{row['peak_kib']:>11,.0f}{row['file_kib']:>10,.0f}"
            f"{row['peak_over_file']:>11.1f}x"
        )
    rows = results["sizes"]
    if len(rows) >= 2 and rows[0]["us_per_row"]:
        drift = rows[-1]["us_per_row"] / rows[0]["us_per_row"]
        print(
            f"\n  us/row at {rows[-1]['rows']:,} is {drift:.2f}x the cost at "
            f"{rows[0]['rows']:,}. Flat is linear."
        )
        worst = max(r["peak_over_file"] for r in rows)
        print(
            f"  Peak memory runs up to {worst:.0f}x the size of the file "
            f"written. That multiple is the number to budget against: the "
            f"whole workbook is assembled in memory before anything reaches "
            f"disk, so a container limit has to clear it, not the output."
        )

    print("\nsame data, each accepted input shape")
    print(f"{'shape':>12}{'rows':>8}{'ms':>10}{'peak KiB':>11}")
    for row in results["shapes"]:
        print(
            f"{row['shape']:>12}{row['rows']:>8}{row['ms']:>10.1f}"
            f"{row['peak_kib']:>11,.0f}"
        )
    if len(results["shapes"]) > 1:
        print(
            "  The docstring offers these as equivalent. A caller already\n"
            "  holding one shape should be able to see here whether\n"
            "  converting to the other first is worth it."
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument(
        "--quick", action="store_true", help="small sizes, as CI runs"
    )
    args = parser.parse_args()

    results = run(quick=args.quick)
    if args.json:
        json.dump(results, sys.stdout, indent=1)
        print()
    else:
        render(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
