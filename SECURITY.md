<!-- SPDX-License-Identifier: Apache-2.0 -->

# Security Policy

## Supported versions

This package follows the
[`bankstatementparser`](https://github.com/sebastienrousseau/bankstatementparser)
suite cadence. Security patches are issued for the latest minor of the
latest major. While pre-`1.0`, that means **the latest released 0.0.x
and the immediately prior 0.0.x** receive security fixes; older 0.0.x
versions do not.

| Version | Status | Receives security fixes? |
| :--- | :--- | :--- |
| `0.0.1` (latest) | Current | ✅ Yes |
| _none yet_ | — | — |

## Reporting a vulnerability

**Do not open a public issue for security reports.**

Use one of the following private channels:

1. **GitHub Private Vulnerability Reporting (preferred)**
   <https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx/security/advisories/new>
2. **Email**: `security@bankstatementparser.com`

**Acknowledgement**: within 48 hours. **Triage**: within 7 days.
**Fix windows**: critical 7 days, high 30 days, medium 60 days, low
best-effort.

## Security posture

### Scope

This package exposes one function — `write_xlsx(data, path, ...)` —
that serialises already-parsed bank-statement data (a pandas
`DataFrame`, a list of `bankstatementparser.Transaction` objects, or a
list of dicts) to an `.xlsx` workbook. It does **not** parse PDFs, CSVs,
or XML, validate against schemas, or accept untrusted input directly:
every byte that reaches the writer has already been parsed and
normalised by the `bankstatementparser` core. The core enforces every
upstream security control; this package is a thin output adapter.

### Threat model

| Surface | How it's handled |
| :--- | :--- |
| **Untrusted statement files (PDF / CSV / XML)** | Out of scope. Input is already-parsed data, not raw files. The `bankstatementparser` core handles input parsing, validation, and zip/XML defence-in-depth. |
| **Path traversal** | The `path` argument is treated as a writer target. Callers must validate the path before invoking the writer. `openpyxl.save()` writes only to the supplied path. |
| **Formula injection** | All cell values are written as plain strings, numbers, dates, or booleans via `sheet.append([...])`. No formulas are constructed from input. |
| **Dependency CVEs** | `bankstatementparser >= 0.0.9`, `openpyxl >= 3.1, < 4`, and `pandas >= 2.0` are the direct deps, audited by GitHub Dependabot. |

### Cryptography status

This package implements **no** cryptographic functionality. `openpyxl`
writes the OOXML zip envelope without signing the workbook contents. If
you need signed-Excel output, sign the workbook downstream with a tool
like `msoffcrypto-tool`.

### Supply chain

- **PyPI Trusted Publishing** (OIDC, no long-lived tokens).
- **Sigstore attestations** for sdist + wheel via
  `pypa/gh-action-pypi-publish`.
- **Signed git tags**: every release tag is signed.
- **No `--no-verify` or `--allow-unverified` shortcuts** in any release
  workflow.

## Contact

- **GitHub Private Vulnerability Reporting (preferred):**
  <https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx/security/advisories/new>
- **Email:** `security@bankstatementparser.com`
