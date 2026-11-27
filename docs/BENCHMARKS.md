# Benchmarks

`benches/bench_write_xlsx.py` measures what writing a statement to a
workbook costs, in time and in memory. Writing `.xlsx` builds the whole
workbook in memory before anything reaches disk, so the number that
decides whether an export survives a container limit is **peak
memory**, reported beside the size of the file written. It also times
two of the accepted input shapes, a list of dicts and a `DataFrame`, on
the same data.

Nothing asserts a threshold: wall-clock and memory are not comparable
between machines. CI runs `python benches/bench_write_xlsx.py --quick`
on every push so the benchmark keeps running against the current API.

## Results

Run with `poetry run python benches/bench_write_xlsx.py` on 2026-11-27:
Apple M1 Pro, macOS 27.2.1, CPython 3.12.16,
bankstatementparser-writer-xlsx 0.0.36, openpyxl 3.1.5.

| Rows | ms | us per row | Peak KiB | File KiB | Peak / file |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 100 | 40.0 | 399.7 | 602 | 10 | 62.6x |
| 1,000 | 289.1 | 289.1 | 2,630 | 50 | 53.0x |
| 10,000 | 2,957.4 | 295.7 | 29,021 | 445 | 65.2x |
| 50,000 | 15,156.2 | 303.1 | 141,630 | 2,213 | 64.0x |

Time per row at 50,000 rows is 0.76x the cost at 100, so writing is
linear. Peak memory runs up to 65x the size of the file written: budget
a container's memory against that multiple, not against the output.

| Shape | Rows | ms | Peak KiB |
| :--- | ---: | ---: | ---: |
| `list[dict]` | 1,000 | 283.9 | 2,624 |
| `DataFrame` | 1,000 | 289.8 | 2,621 |

The two shapes cost the same, so converting one to the other first buys
nothing.

Reproduce with `python benches/bench_write_xlsx.py` (add `--json` for
machine-readable output).
