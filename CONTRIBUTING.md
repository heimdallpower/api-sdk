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

Install dependencies:

```bash
curl -sSL https://install.python-poetry.org | python3 -

poetry --version 

poetry install # Installs the dependecies
```

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
