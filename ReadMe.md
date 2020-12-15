antiflash.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
============
~~[wheel (GitLab)](https://gitlab.com/KOLANICH-tools/antiflash.py/-/jobs/artifacts/master/raw/dist/antiflash-0.CI-py3-none-any.whl?job=build)~~
[wheel (GHA via `nightly.link`)](https://nightly.link/KOLANICH-tools/antiflash.py/workflows/CI/master/antiflash-0.CI-py3-none-any.whl)
~~![GitLab Build Status](https://gitlab.com/KOLANICH-tools/antiflash.py/badges/master/pipeline.svg)~~
~~![GitLab Coverage](https://gitlab.com/KOLANICH-tools/antiflash.py/badges/master/coverage.svg)~~
~~[![GitHub Actions](https://github.com/KOLANICH-tools/antiflash.py/workflows/CI/badge.svg)](https://github.com/KOLANICH-tools/antiflash.py/actions/)~~
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH-tools/antiflash.py.svg)](https://libraries.io/github/KOLANICH-tools/antiflash.py)
[![Code style: antiflash](https://img.shields.io/badge/code%20style-antiflash-FFF.svg)](https://codeberg.org/KOLANICH-tools/antiflash.py) 

A monkey-patch for `black` uncompromising Python source code reformatter, coercing it to use `tabs` for indentation instead of cargo cult `spaces`.

[`antiflash`](https://en.wikipedia.org/wiki/Anti-flash_white) is white coating applied to nuclear-carrying bombers to protect them from overheating from light emitted by nuclear explosion.

## Limitations
1. It monkey-patches `black` to use tabs. It doesn't create any branches in `black`. It just replaces hardcoded 4 spaces with a hardcoded `\t`. After the monkey-patch is applied, `black` itself will use tabs.
2. So, importing this package produces a side effect. So it is only useful in situations where only `antiflash` is needed, not `antiflash` and `black` simultaniously.
