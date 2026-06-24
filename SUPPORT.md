<!-- SPDX-License-Identifier: Apache-2.0 -->

# Getting support

Thanks for using bankstatementparser-writer-xlsx. Here's the fastest way to get help, by need.

## Questions & how-to

- **Read first:** the [README](README.md), the runnable
  [`examples/`](examples/) (minimal write, write-with-summary), and the
  parent
  [`bankstatementparser`](https://github.com/sebastienrousseau/bankstatementparser)
  repo for parsing background.
- **Still stuck?** Open a
  [GitHub Discussion](https://github.com/sebastienrousseau/bankstatementparser/discussions)
  on the parent repo or a question issue here. Include your Python
  version, `bankstatementparser-writer-xlsx` version
  (`python -c "import bankstatementparser_writer_xlsx; print(bankstatementparser_writer_xlsx.__version__)"`),
  your input shape (DataFrame / Transaction list / dicts), and a minimal
  reproducer.

## Bugs

Open a bug report at
<https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx/issues/new>
with a minimal reproducer, your input shape, the arguments, and the full
traceback. A failing record set (with sensitive values redacted) helps
enormously.

## Feature requests

Open a feature request at
<https://github.com/sebastienrousseau/bankstatementparser-writer-xlsx/issues/new>.
New output formatting options and input shapes are especially welcome —
see [ARCHITECTURE.md](ARCHITECTURE.md) for the extension points and
[ROADMAP.md](ROADMAP.md) for what's planned.

## Security

**Do not** open public issues for vulnerabilities. Follow the private
disclosure process in [SECURITY.md](SECURITY.md).

## Contributing & maintaining

See [CONTRIBUTING.md](CONTRIBUTING.md) and [GOVERNANCE.md](GOVERNANCE.md).

## Supported versions

Fixes land on the latest release line. See [SECURITY.md](SECURITY.md) for
the supported-version policy. bankstatementparser-writer-xlsx requires Python 3.10+.
