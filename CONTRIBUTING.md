# Contributing

Thank you for taking the time to improve TraceGuard Core.

## Before opening a pull request

1. Check existing issues and pull requests for related work.
2. Keep the change focused and describe the problem it addresses.
3. Add or update a regression test for behaviour changes.
4. Use synthetic data only. Do not include credentials, private keys, customer data, or production logs.
5. State any assumptions, limitations and compatibility impacts.

## Run the focused test suite

Use Python 3.10 or later:

```sh
python -m pip install -e '.[test]'
python -m pytest -q tests/test_engine_extra.py tests/test_mcp_gate.py
```

## Security reports

Do not report exploitable vulnerabilities in a public issue. Follow the private reporting instructions in [SECURITY.md](SECURITY.md).

## Scope

The MCP adapter is decision-only. Changes must not imply that it executes tools, validates every target tool's arguments, or provides an operating-system sandbox unless those capabilities are separately implemented and tested.

By submitting a contribution, you confirm that you have the right to submit it and that it contains no confidential or third-party material you are not authorised to publish.
