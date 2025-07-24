# Heimdall API SDK for Python

This folder contains the Python SDK for accessing the [Heimdall Power External API](https://developer.heimdallcloud.com/docs/welcome).

## Getting Started

### Requirements

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation)

Install dependencies:

```bash
curl -sSL https://install.python-poetry.org | python3 -
poetry install
```

### Installing the SDK

The package can be downloaded and installed unsing the github relase artifacts

```bash
pip install https://github.com/heimdallpower/api-sdk/releases/download/v1.2.3/heimdall_api_sdk-1.2.3-py3-none-any.whl
```

> Replace the version and filename with the latest from [Releases](https://github.com/heimdallpower/api-sdk/releases)

### Usage Example

```python
from heimdall_api_client.client import HeimdallApiClient
import logging
import pprint

logging.basicConfig(level=logging.INFO)

client = HeimdallApiClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
)

assets = client.get_assets()
pprint.pprint(assets)

```

more examples can be seen in the [examples folder](examples).
