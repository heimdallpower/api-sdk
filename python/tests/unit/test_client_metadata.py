"""
Unit tests for the default client metadata headers sent by HeimdallApiClient.

Covers:
- x-client-version reflects the installed distribution version (not a hardcoded value)
- Fallback to "0.0.0" when the distribution is not installed (running from source)
- User-supplied client_metadata overrides the defaults
"""

from importlib.metadata import PackageNotFoundError

from heimdall_api_client.client import _SDK_VERSION, HeimdallApiClient


def _make_client(**kwargs) -> HeimdallApiClient:
    return HeimdallApiClient(client_id="fake-id", client_secret="fake-secret", **kwargs)


class TestClientMetadata:
    def test_default_metadata_uses_sdk_version(self):
        client = _make_client()

        assert client.client_metadata["x-client-name"] == "python-sdk"
        assert client.client_metadata["x-client-version"] == _SDK_VERSION

    def test_sdk_version_matches_installed_distribution(self):
        from importlib.metadata import version

        try:
            expected = version("heimdallpower-api-client")
        except PackageNotFoundError:
            expected = "0.0.0"

        assert _SDK_VERSION == expected

    def test_user_metadata_overrides_defaults(self):
        client = _make_client(client_metadata={"x-client-version": "9.9.9", "x-custom": "abc"})

        assert client.client_metadata["x-client-version"] == "9.9.9"
        assert client.client_metadata["x-custom"] == "abc"
        assert client.client_metadata["x-client-name"] == "python-sdk"
