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
    rev: 0.51.0.0 # Use a dprint-py release version
    hooks:
      - id: dprint-fmt
```

To enforce formatting in CI pipelines without altering files, use the `dprint-check` hook instead:

```yaml
repos:
  - repo: https://github.com/vanishingredient/dprint-pre-commit
    rev: 0.51.0.0
    hooks:
      - id: dprint-check # Fails if files are not properly formatted
```

## Using with prek

If you use [prek](https://github.com/j178/prek) (which is currently compatible with
`.pre-commit-config.yaml`), you can also natively define your hooks in `prek.toml`:

```toml
[[repos]]
repo = "https://github.com/vanishingredient/dprint-pre-commit"
rev = "0.51.0.0"
hooks = [
  { id = "dprint-fmt" },
  { id = "dprint-check" },
]
```

## Known Limitations

> [!NOTE]
> In strictly sandboxed environment applications like `pre-commit.ci`, dprint may fail to
> dynamically download language plugins due to network constraints enforced after the environment is
> initially built. This limitation is inherent to dprint's on-the-fly plugin architecture.
