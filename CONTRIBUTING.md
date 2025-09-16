# Contribution Guidelines

Please refer to the [Organization Docs](https://github.com/scadable/.github/blob/main/CONTRIBUTING.md) on how to
contribute to any project at Scadable.

## Codestyle

This project uses [ruff](https://github.com/astral-sh/ruff) to enforce style requirements. This is already configured in
a tool called [pre-commit](https://pre-commit.com/).

To validate your PR, you can use the [installation guide](https://pre-commit.com/#install) to setup pre-commit hooks.

To setup git pre-commit hooks, run:

```commandline
pre-commit install
```

To run codestyle validations without install hooks, run:

```commandline
pre-commit run --all-files
```

## Releases

To push a new version of this package to PyPi, create a Release on github to run the deployment workflow.
