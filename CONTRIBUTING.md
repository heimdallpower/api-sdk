# Contributing to Heimdall Power API SDK

Thank you for your interest in contributing!

This repository contains SDKs and example clients for accessing the [Heimdall Power External API](https://developer.heimdallcloud.com/docs/welcome).

---

## Pull Requests

- All pull requests must have a **clear title** (min. 5 characters).
- Include a short description of what the PR does and why.
- Pull requests targeting `main` must be reviewed by a **code owner**.

> Heimdall Power's software engineering team (`@heimdallpower/software-engineering`) is configured as the code owner. Reviews will be automatically requested when a PR is opened.
---

## Branching & Releases

- Contributions should be made as pull requests into `main`.
- Releases are managed using GitHub Releases.
- Tags must follow the format: `v<MAJOR>.<MINOR>.<PATCH>` (e.g., `v1.2.3`)
- A GitHub Release must be published for the package to be built and pushed to NuGet
- The `v` prefix is automatically stripped when packaging

---

## Python

The `python/` folder contains the Python SDK and related utilities.

### Requirements

- Python 3.11+
- Poetry (dependency and build management)

Install dependencies:

```bash
curl -sSL https://install.python-poetry.org | python3 -

poetry --version 

poetry install --with dev # Installs the dependecies
```

#### Update dependencies

```bash
poetry update --dry-run # view avaiables dependency updates
poetry update # updates all dependecies. Note, does not alter the pyproject.toml file
```

### Code Style & Linting

We use Ruff for formatting and linting.

```bash
poetry run ruff check . --fix 

poetry run ruff formate .
```

### Building the Package

The SDK is packaged using Poetry. A build step is included in the CI pipeline to validate packaging.

To build locally:

```bash
poetry build
```

This will produce .whl and .tar.gz files.
>Running poetry build locally is recommended to catch issues early, such as missing ```__init__.py``` files, bad version strings, or invalid metadata.

### Generating Clients from OpenAPI

New modules are generated using openapi-python-client.

To generate a module:

```bash
# Nagivate to the script folder and run
./generate_module.ps1 -Module assets
```

This will:

- Download the OpenAPI spec
- Generate a python client for the module
- Place the result under `python/heimdall_api_client/<module>`
