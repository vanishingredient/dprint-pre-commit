# dprint-pre-commit

[dprint](https://dprint.dev/) integration for [pre-commit](https://pre-commit.com/).

This repository uses the [dprint-py](https://pypi.org/project/dprint-py/) package, which provides
the dprint executable through prebuilt Python wheels. Tags in this repository mirror dprint-py
release versions.

## Prerequisites

Your project must have a [dprint configuration file](https://dprint.dev/config/) (`dprint.json`,
`dprint.jsonc`, or `.dprint.json`) in the repository root for dprint to know which plugins and
formatting rules to apply.

## Using with pre-commit

Add the following configuration to your `.pre-commit-config.yaml` to enable the `dprint` formatter:

```yaml
repos:
  - repo: https://github.com/vanishingredient/dprint-pre-commit
    rev: 0.52.0.0 # Use a dprint-py release version
    hooks:
      - id: dprint-fmt
```

To enforce formatting in CI pipelines without altering files, use the `dprint-check` hook instead:

```yaml
repos:
  - repo: https://github.com/vanishingredient/dprint-pre-commit
    rev: 0.52.0.0
    hooks:
      - id: dprint-check # Fails if files are not properly formatted
```

> [!WARNING]
> In sandboxed environments like the hosted `pre-commit.ci` service, network access is blocked
> during hook execution. Because `dprint` downloads its language plugins on-the-fly at runtime, it
> will fail to execute in these environments.

Possible workarounds:

1. **Use the official GitHub Action:** Replace the `pre-commit.ci` service with the official
   [pre-commit GitHub Action](https://github.com/pre-commit/action). This action executes within
   your own CI workflow, where network requests are permitted.

2. **Commit plugins locally:** Download the required `.wasm` plugin files into your repository and
   update your `dprint.json` to reference their local file paths instead of URLs. This enables
   offline execution but increases your repository size.

3. **Disable the hooks for `pre-commit.ci`:** If you still want to use `pre-commit.ci` for other
   tools but bypass `dprint` checks, you can explicitly configure it to skip the `dprint` hooks in
   your `.pre-commit-config.yaml`:
   ```yaml
   ci:
     skip: [dprint-fmt, dprint-check]
   ```

## Using with prek

If you use [prek](https://github.com/j178/prek) (which is compatible with
`.pre-commit-config.yaml`), you can also natively define your hooks in `prek.toml`:

```toml
[[repos]]
repo = "https://github.com/vanishingredient/dprint-pre-commit"
rev = "0.52.0.0"
hooks = [
  { id = "dprint-fmt" },
]
```
