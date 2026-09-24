"""
Shared helpers for unit tests that drive HeimdallApiClient end to end over a fake
HTTP transport: the real generated endpoint code builds the request and parses the
response, but no network or authentication is involved.
"""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import MagicMock

import httpx

from heimdall_api_client.assets_api_client.client import AuthenticatedClient

BASE_URL = "https://fake-api.example.com"


class RecordingTransport(httpx.MockTransport):
    """Answers every request with a fixed JSON body and records the requests it saw."""

    def __init__(self, body: dict[str, Any], status_code: int = 200):
        self.requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            self.requests.append(request)
            return httpx.Response(status_code, content=json.dumps(body), headers={"content-type": "application/json"})

        super().__init__(handler)

    @property
    def last_request(self) -> httpx.Request:
        return self.requests[-1]

    @property
    def last_params(self) -> httpx.QueryParams:
        return self.last_request.url.params


def make_client(transport: RecordingTransport):
    """Returns a HeimdallApiClient whose authenticated client uses the given transport."""
    from heimdall_api_client.client import HeimdallApiClient

    client = HeimdallApiClient.__new__(HeimdallApiClient)
    client.logger = MagicMock()
    client.auth_service = MagicMock()
    client.api_base_url = BASE_URL
    client.client_metadata = {}
    client.timeout = None

    def authenticated_client() -> AuthenticatedClient:
        authenticated = AuthenticatedClient(base_url=BASE_URL, token="stub-token")
        authenticated.set_httpx_client(httpx.Client(base_url=BASE_URL, transport=transport))
        return authenticated

    client._get_authenticated_client = authenticated_client
    client._get_region = lambda: "eu"
    return client
