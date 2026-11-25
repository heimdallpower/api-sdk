# Heimdall API SDK for Python

Official Python SDK for the Heimdall Power External API.

## Documentation

- [Getting started](https://developer.heimdallcloud.com/docs/welcome) and [authentication](https://developer.heimdallcloud.com/docs/authentication)
- [Concepts](https://developer.heimdallcloud.com/docs/concepts): assets, measurement points and API modules.
- [Use cases](https://developer.heimdallcloud.com/docs/use-cases): integration flows, [aggregation](https://developer.heimdallcloud.com/docs/use-cases#aggregation) and polling cadence.
- [User Guide](https://heimdallbrain.atlassian.net/servicedesk/customer/portal/1/article/4095541249) (customer login required): DLR and fallback rating details.
- [Examples](https://github.com/heimdallpower/api-sdk/tree/main/python/examples)

## Installation

Requires Python 3.11+.

```bash
pip install heimdallpower-api-client
```

Wheels are also attached to each [GitHub release](https://github.com/heimdallpower/api-sdk/releases), e.g.:

```bash
pip install https://github.com/heimdallpower/api-sdk/releases/download/python-v1.2.3/heimdallpower_api_client-1.2.3-py3-none-any.whl
```

## Quick start

```python
from heimdall_api_client import HeimdallApiClient

client = HeimdallApiClient(client_id="your_client_id", client_secret="your_client_secret")
assets = client.get_assets()
```

## Iterate over instrumented lines

Not every line has Neurons installed.
Data endpoints return 404 or no data for lines without active measurement points.
`get_instrumented_lines()` returns only lines with at least one active measurement point, with their facility.

```python
for instrumented in client.get_instrumented_lines():
    current = client.get_latest_current(instrumented.line.id)
    print(instrumented.facility.name, instrumented.line.name, current.data.current.value, current.data.unit)
```

Already have the assets? Use `instrumented_lines(assets.data)` from `heimdall_api_client.assets`.

## Error handling and retry

### Automatic retry

All methods retry **up to 3 times** with exponential backoff (1 s → 2 s → 4 s) on these transient errors:

| Condition | Description |
|---|---|
| `502 Bad Gateway` | The gateway could not reach the upstream server |
| `503 Service Unavailable` | Server temporarily unavailable |
| `504 Gateway Timeout` | Upstream server did not respond in time |

- Each retry logs a `WARNING`.
- After 3 failed retries, the last `HeimdallApiError` is raised.
- `500 Internal Server Error` is not retried.

### Token renewal

The access token is renewed 2 minutes before it expires, so requests don't use a token that is about to expire. A `401` from the API is not retried; it is raised as `HeimdallApiError`.

### Token request retry

The access token request is retried the same way (up to 3 times, 1 s → 2 s → 4 s) on connection errors and timeouts (for example `Connection reset by peer`), and on `429`, `500`, `502`, `503` and `504` from the token endpoint.

- `400` and `401` (for example invalid credentials) are not retried.
- Each retry logs a `WARNING`; the final failure logs an `ERROR`. Both go to the `logger` passed to `HeimdallApiClient`, if any.
- After 3 failed retries, the last `requests.RequestException` is raised (for example `requests.ConnectionError`, `requests.Timeout` or `requests.HTTPError`).

### Exceptions

All methods raise `HeimdallApiError` on non-transient errors. `status_code` holds the HTTP status.

```python
from heimdall_api_client import HeimdallApiClient, HeimdallApiError

client = HeimdallApiClient(client_id="...", client_secret="...")

try:
    dlr = client.get_latest_heimdall_dlr(line_id=line_id)
except HeimdallApiError as e:
    if e.status_code == 404:
        print("No data for the line in the requested window, or unknown line")
    else:
        print(f"API error {e.status_code}: {e}")
```

### Timeouts

Pass `timeout` (seconds) to the constructor. It applies to every request and each retry.

```python
import httpx
from heimdall_api_client import HeimdallApiClient

# Simple: abort any request that takes longer than 10 s
client = HeimdallApiClient(client_id="...", client_secret="...", timeout=10.0)

# Fine-grained: separate connect and read timeouts
client = HeimdallApiClient(
    client_id="...",
    client_secret="...",
    timeout=httpx.Timeout(connect=5.0, read=30.0),
)
```

- There is no cancellation token; use `timeout` to bound each request.
- `httpx.TimeoutException` is raised when the timeout is exceeded.

## License

This SDK is licensed under the [Apache License 2.0](https://github.com/heimdallpower/api-sdk/blob/main/LICENSE).
