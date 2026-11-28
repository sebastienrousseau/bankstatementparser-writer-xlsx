# Changelog

All notable changes to **bankstatementparser-writer-xlsx** are
documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed

- CI: four pinned actions move to their latest releases:
  codeql-action 4.39.5, markdownlint-cli2-action 25.1.0,
  cosign-installer 4.1.4 and sbom-action 0.24.4.

### Fixed

- The suite consistency check authenticates its GitHub API request
  with the workflow token, so the shared anonymous rate limit no
  longer fails it.

## [0.0.36] - 2026-11-27

### Security

- Spreadsheet formula injection (CWE-1236): openpyxl stores any `str`
  that starts with `=` as a formula, so a transaction description such
  as `=HYPERLINK("http://x","click")`, which a payer can partly choose,
  became a live formula in the exported workbook. Every string (values,
  column names, summary keys and values) is now written as a plain text
  cell with its text unchanged. `SECURITY.md`'s threat model claimed
  this already held; it now states the real guarantee.

### Fixed

- A value, column name or summary entry holding a control character an
  `.xlsx` cannot store (C0 characters other than tab, newline and
  carriage return) raised openpyxl's `IllegalCharacterError`, which is
  not among the errors `write_xlsx` documents. It now raises
  `ValueError` naming the text; nothing is altered silently.
- `benches/bench_write_xlsx.py`'s docstring claimed to time a list of
  `Transaction` objects; it times a list of dicts and a `DataFrame`.

### Added

- An Atheris fuzz target, `fuzz/fuzz_write_xlsx.py`, for `write_xlsx`
  over fuzzed records, summaries and sheet names; it fails on any
  exception but `TypeError` / `ValueError` and on a workbook that does
  not reopen with one row per record. CI runs it for 120 s on every
  change; `make fuzz` locally.
- A MkDocs Material user manual (`mkdocs.yml`, `docs/`) with an
  mkdocstrings API reference, built with `--strict` on every pull
  request and deployed to GitHub Pages from `main`
  (`.github/workflows/docs.yml`, `make docs`). It replaces a Sphinx
  configuration that nothing built.
- `docs/POLICIES.md`, `docs/BENCHMARKS.md` (a run of
  `benches/bench_write_xlsx.py` with its environment),
  `docs/COMPARISON.md`, `docs/format.md` and `docs/suite.md`.
- Signed releases: keyless cosign `.sig` and `.pem` per distribution,
  SLSA provenance
  (`bankstatementparser-writer-xlsx-vX.Y.Z.intoto.jsonl`,
  slsa-github-generator 2.1.0), CycloneDX and SPDX SBOMs and a licence
  manifest on every GitHub release, and PEP 740 attestations on PyPI.
- The OpenSSF Scorecard workflow, the suite's Docs Lint workflow
  (`scripts/readme-check.sh` and markdownlint), a Security workflow
  (Bandit and `pip-audit` on the locked sets), the portfolio pull
  request template, and `.github/demo.gif` rendered by `make demo` from
  `.github/demo.tape`.
- Hash-pinned requirement sets exported from the lock
  (`requirements/{runtime,ci,fuzz,docs}.txt`, by the suite's
  `scripts/export_locked_requirements.py`) and compiled release tooling
  (`requirements/{build,sbom}.txt`).

### Changed

- Require `bankstatementparser >= 0.0.35`, the newest core release, and
  align the version with the suite's 0.0.36 release; `poetry.lock`
  moves core to 0.0.35.
- CI pins every action by commit SHA, installs only the hashed lock
  exports, and tests CPython 3.10 to 3.14 on Ubuntu, macOS and Windows.
  Write permissions sit on the jobs that need them.
- `README.md` follows the portfolio template and states the
  Apache-2.0 OR MIT licence; the suite table moves to `docs/suite.md`.
  `CODE-OF-CONDUCT.md` is now `CODE_OF_CONDUCT.md`, the issue templates
  follow the suite kit, and `SECURITY.md`'s supported versions name
  0.0.36 and 0.0.35.
- `ROADMAP.md` no longer calls v0.0.10 current; `ARCHITECTURE.md` lists
  every module and tool.

## [0.0.35] - 2026-11-26

### Added

- `scripts/check_complexity.py`, the suite's standard-library
  complexity gate, copied byte for byte from `bankstatementparser`:
  cyclomatic 10, cognitive 15, Halstead difficulty 30 and 60 lines per
  function, 500 lines per file. The 4 functions and files already over
  a ceiling are recorded in `scripts/complexity_baseline.json`; CI and
  `make check` fail when one gets worse, a new one appears, or an
  improvement is left unrecorded, so the baseline can only shrink.

### Changed

- Require `bankstatementparser >= 0.0.34`, the newest core release, and
  align the version with the suite's 0.0.35 release, in which all
  fourteen packages and bankstatementparser.com share one version.
- `scripts/check_suite_consistency.py` now checks all fourteen suite
  packages on PyPI and the bankstatementparser.com GitHub release.
- Development dependency `ruff` updated from 0.17.5 to 0.17.6.

## [0.0.34] - 2026-11-18

### Changed

- Require `bankstatementparser >= 0.0.33`, the newest core release, and
  align the version with the suite's 0.0.34 release. No other changes.

## [0.0.33] - 2026-11-18

### Changed

- Require `bankstatementparser >= 0.0.32`, the newest core release, and
  align the version with the suite's 0.0.33 release. No other changes.

## [0.0.32] - 2026-11-18

### Changed

- Require `bankstatementparser >= 0.0.31`, the newest core release, and
  align the version with the suite's 0.0.32 release.
- Release notes are written by the release workflow. A final
  `release-notes` job runs after every asset is attached and rewrites
  the GitHub release in the suite's format: Highlights, What's Changed,
  New Contributors (when any), Checksums of every asset, and the Full
  Changelog link. Until now the body was the CHANGELOG section,
  with no Highlights or Checksums, so 0.0.31 had to be corrected by
  hand. `softprops/action-gh-release` is no longer used.
- The Highlights are the one hand-written part, kept in
  `.github/releases/<tag>.md`. The build refuses to publish when that
  file is missing, has fewer than 2 or more than 4
  `* **Headline**: text` bullets, or contains an em dash.
- `scripts/release_notes.py`, shared with every suite repository,
  composes the body from the GitHub API and the downloaded assets.

## [0.0.31] - 2026-11-18

### Changed

- Require `bankstatementparser >= 0.0.30`, the newest core release, and
  align the version with the suite's 0.0.31 release.
- Release titles read `bankstatementparser-writer-xlsx <version>` instead of the bare tag.

## [0.0.30] - 2026-11-18

### Changed

- Bumped dependency to `bankstatementparser >= 0.0.29`.
- Aligned version with `bankstatementparser` 0.0.30 suite release.
- Updated ruff to 0.17.5 (dev).
- 0.0.29 was prepared but never published; its changes ship in 0.0.30.

## [0.0.28] - 2026-10-11

### Changed

- Bumped dependency to `bankstatementparser >= 0.0.28`.
- Aligned version with `bankstatementparser` 0.0.28 suite release.

## [0.0.19] - 2026-08-31

### Added

- Registered entry point `bankstatementparser.writers` for `xlsx`.
- Bumped dependency to `bankstatementparser >= 0.0.19`.

## [0.0.18] - 2026-08-29

Aligns the `bankstatementparser` suite on one version number, and adds
the scheduled drift check this repository was missing.

### Added

- `scripts/check_suite_consistency.py` and a scheduled `Suite
  Consistency` workflow compare this tree, and every published member of
  the suite, against PyPI. A member left a release behind still installs
  and still passes its own tests; only the index disagrees, and only if
  somebody looks.

### Changed

- Version aligned to `0.0.18` across all six `bankstatementparser`
  packages, which had drifted to `0.0.14`, `0.0.15`, `0.0.17`, `0.0.16`,
  `0.0.16` and `0.0.15`.
- Refreshed the vendored `tests/test_suite_conformance.py` to the current
  canonical copy. Its drift-check probe now matches the bare word `pypi`
  rather than the hostname, which CodeQL read as an incomplete URL
  sanitisation.

## [0.0.15] - 2026-08-29

Brings this repository onto the **suite conformance gate**.

### Added

- **`benches/bench_write_xlsx.py`** — time is the less interesting half.
  Writing xlsx means building the whole workbook in memory before
  anything reaches disk, so **peak memory** is what decides whether a job
  survives, and nothing was measuring it.

  **Peak memory runs about 65x the size of the file written.** A 2.2 MB
  workbook at 50,000 rows needs roughly **138 MB** of peak allocation.
  That multiple is the number to budget a container against — the limit
  has to clear the peak, not the output. It works on a laptop and gets
  killed in a constrained container, which is exactly the failure a test
  suite never sees.

  Time is linear (`us/row` moves 1.19x between 100 and 50,000 rows), and
  the accepted input shapes — a list of dicts and a DataFrame — are
  measured side by side, since the docstring offers them as equivalent
  and a caller holding one should be able to see whether converting is
  worth it.

  Nothing asserts a timing threshold — wall-clock is not comparable
  between machines, and a flaky performance gate teaches people to ignore
  red. CI runs `--quick`, so a benchmark that stops compiling fails the
  build rather than rotting into a file that reads as verified.

- **`tests/test_suite_conformance.py`** — invariants shared by every
  repository in the suite, vendored from one canonical copy and
  checksummed by its own test.

### Changed

- CI lints, formats and runs `benches/` alongside everything else.
- `tomli` (on 3.10) and `packaging` are named as dev dependencies; the
  conformance gate parses `pyproject.toml` and needs both.
- `tests/test_suite_conformance.py` is excluded from black: it is
  generated, and the suite uses three different line lengths.

## [0.0.14] - 2026-08-28

### Changed

- **A plain `pytest` now enforces the same 100% coverage floor CI does.**
  `--cov`, `--cov-branch` and `--cov-report=term-missing` move into
  `[tool.pytest.ini_options] addopts`. Before this, running `pytest`
  locally measured no coverage at all: the developer saw green and learned
  otherwise from the build.

  The gate itself was never missing — CI has always run
  `--cov-fail-under=100`, so nothing could regress onto `main` unnoticed.
  What was missing was the local half of it.

- **The floor is stated once.** It was in two places, the
  `--cov-fail-under` flag in `ci.yml` and `fail_under` under
  `[tool.coverage.report]`, which is how two numbers meant to be equal stop
  being equal. pytest-cov honours `fail_under` from the coverage config, so
  the flag is gone from both `addopts` and the workflow and the number lives
  in exactly one place.

  CI now runs `pytest tests/ --cov-report=xml -v`; only the XML report is
  CI-specific.

### Verification

Coverage was already 100% and remains so. The gate was mutation-tested:
adding a function no test calls drops coverage below the floor and fails
the run, locally as well as in CI.

## [0.0.13] - 2026-07-18

### Changed

- chore(deps): require `bankstatementparser>=0.0.11` (was `>=0.0.9`),
  keeping the writer in lockstep with the 0.0.11 core release. No
  functional or API changes.

## [0.0.12] - 2026-06-25

### Changed

- **Audit pass.** Documented and exampled `NaN`->blank, the 60-char column-width cap, and the `TypeError`/`ValueError` paths (new `examples/06_value_coercion_and_errors.py`); added docs-accuracy guards.

## [0.0.11] - 2026-06-24

### Added

- Install smoke-test CI job (`smoke`) that builds the wheel, installs it
  into a fresh virtualenv from PyPI (pulling `bankstatementparser`,
  `openpyxl`, and `pandas`), imports the package, and runs an example
  from a neutral working directory — proving the published artifact is
  importable and usable, not just the editable checkout.
- Expanded edge-case tests that read each workbook back and assert exact
  cells: empty list vs. empty `DataFrame`-with-columns; Unicode text and
  a string longer than the 60-character column-width cap; `None`/`NaN`
  cells; `list[dict]` with differing/missing keys (union, first-seen
  order); large and negative `Decimal` amounts; `date` vs. `datetime`
  cells; and a custom `sheet_name` combined with a `summary=` sheet.
- Sixth example, `06_value_coercion_and_errors.py`, exercising the value
  coercion rules (`Decimal`→`float`, `date`/`datetime`, `None`/`NaN`/
  missing keys → blank), the 60-character column-width cap, and the
  `TypeError`/`ValueError` error paths end-to-end.
- README now documents the exact 60-character column-width cap, the
  `None`/`NaN`→blank coercion rule, and the `TypeError`/`ValueError`
  error paths (with a runnable, regression-tested example). New
  docs-accuracy tests pin these README claims to the code.

### Changed

- Pruned over-scaffolded CI: removed the `nightly.yml` and `docs.yml`
  workflows. The retained workflows are `ci.yml`, `pr.yml`, `codeql.yml`,
  `security.yml`, and `release.yml`.

## [0.0.10] - 2026-06-24

### Added

- Initial release of `bankstatementparser-writer-xlsx`, the Excel
  `.xlsx` writer companion to the
  [`bankstatementparser`](https://github.com/sebastienrousseau/bankstatementparser)
  library.
- `write_xlsx(data, path, *, sheet_name="Transactions", summary=None)`
  — serialises parsed bank-statement data to a polished workbook via
  [openpyxl](https://openpyxl.readthedocs.io/).
- Accepts three input shapes: a pandas `DataFrame` (from a parser's
  `.parse()`), a list of `bankstatementparser.Transaction` objects, or
  a list of plain dicts. Each normalises to a flat table with a stable,
  documented column order.
- Bold header row, one row per record, and auto-sized columns capped at
  60 characters.
- Optional second `Summary` sheet built from a `get_summary()`-style
  mapping (one `Key`/`Value` row per item).
- Spreadsheet-friendly value coercion: `Decimal` → `float`,
  `date`/`datetime` written as native Excel date cells, other scalars
  passed through, everything else stringified.
- Explicit error handling: `TypeError` for unsupported top-level types,
  `ValueError` for unsupported sequence items. Empty input writes an
  empty (or header-only) sheet.
- Five runnable examples covering every supported input shape and
  option (`01_write_dataframe.py`, `02_write_transactions.py`,
  `03_write_dicts.py`, `04_write_with_summary.py`,
  `05_custom_sheet_name.py`). Each writes to a temp file, reads it back
  with openpyxl, and is exercised in CI.
- Quality gates: 100% line + branch test coverage, 100% docstring
  coverage (interrogate), `ruff` lint, and `mypy --strict`. README,
  docs, and example consistency are enforced by an automated suite
  (`test_docs_accuracy.py`, `test_regression_docs.py`,
  `test_regression_examples.py`).

[0.0.36]: https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx/releases/tag/v0.0.36
[0.0.35]: https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx/releases/tag/v0.0.35
[0.0.34]: https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx/releases/tag/v0.0.34
[0.0.33]: https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx/releases/tag/v0.0.33
[0.0.32]: https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx/releases/tag/v0.0.32
[0.0.31]: https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx/releases/tag/v0.0.31
[0.0.30]: https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx/releases/tag/v0.0.30
[0.0.28]: https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx/releases/tag/v0.0.28
[0.0.19]: https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx/releases/tag/v0.0.19
[0.0.18]: https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx/releases/tag/v0.0.18
[0.0.11]: https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx/releases/tag/v0.0.11
[0.0.10]: https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx/releases/tag/v0.0.10
