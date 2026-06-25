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

The package can be downloaded and installed using the GitHub release artifacts:

```bash
pip install https://github.com/heimdallpower/api-sdk/releases/download/v1.2.3/heimdall_api_client-1.2.3-py3-none-any.whl
```

> Replace the version and filename with the latest from [Releases](https://github.com/heimdallpower/api-sdk/releases)

### Usage Example

```python
from heimdall_api_client import HeimdallApiClient
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

More examples can be seen in the [examples folder](examples).

## Error Handling and Retry

The SDK handles transient infrastructure errors automatically so your application does not have to.

### Automatic retry

All methods on `HeimdallApiClient` retry **up to 3 times** with **exponential backoff** (1 s → 2 s → 4 s) on the following transient conditions:

| Condition | Description |
|---|---|
| `502 Bad Gateway` | Reverse proxy / Application Gateway could not reach the upstream server |
| `503 Service Unavailable` | Server temporarily unavailable |
| `504 Gateway Timeout` | Upstream server did not respond in time |

A `WARNING` log line is emitted for each retry attempt.
If all 3 retry attempts are exhausted, a `HeimdallApiError` is raised with the status code of the last failed response.

> **Note:** `500 Internal Server Error` is **not** retried as it typically indicates a permanent application-level error.

### Exceptions

All methods raise `HeimdallApiError` on non-transient errors. The `status_code` attribute holds the HTTP status code.

```python
from heimdall_api_client import HeimdallApiClient, HeimdallApiError

client = HeimdallApiClient(client_id="...", client_secret="...")

try:
    dlr = client.get_latest_heimdall_dlr(line_id=line_id)
except HeimdallApiError as e:
    if e.status_code == 404:
        print("Line not found")
    else:
        print(f"API error {e.status_code}: {e}")
```
