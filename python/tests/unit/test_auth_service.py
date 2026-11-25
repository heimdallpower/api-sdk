import json
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, call, patch

import jwt
import pytest
import requests

from heimdall_api_client.auth import AuthService


def _make_token(claims: dict) -> str:
    return jwt.encode(claims, key="not-a-real-secret-just-for-tests", algorithm="HS256")


def _http_response(status_code: int, body: dict) -> requests.Response:
    """A real requests.Response, so raise_for_status() behaves as in production."""
    response = requests.Response()
    response.status_code = status_code
    response._content = json.dumps(body).encode()
    response.url = "https://fake-b2c.example.com/token"
    return response


def _token_response(access_token: str) -> requests.Response:
    return _http_response(200, {"access_token": access_token, "expires_in": 3600})


def _connection_reset() -> requests.ConnectionError:
    # The error a customer's batch job hit when the token endpoint dropped the connection.
    return requests.ConnectionError(("Connection aborted.", ConnectionResetError(104, "Connection reset by peer")))


def _mock_token_response(access_token: str, expires_in: int = 3600):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "access_token": access_token,
        "expires_in": expires_in,
    }
    return mock_response


class TestGetValidToken:
    @patch("heimdall_api_client.auth.requests.post")
    def test_returns_cached_token_when_not_expired(self, mock_post):
        token = _make_token({"sub": "test"})
        mock_post.return_value = _mock_token_response(token)

        auth = AuthService(client_id="test-id", client_secret="test-secret")
        auth.get_valid_token()
        auth.get_valid_token()

        mock_post.assert_called_once()

    @patch("heimdall_api_client.auth.requests.post")
    def test_refetches_when_token_expired(self, mock_post):
        token = _make_token({"sub": "test"})
        mock_post.return_value = _mock_token_response(token)

        auth = AuthService(client_id="test-id", client_secret="test-secret")
        auth.get_valid_token()

        auth._expires_at = datetime.now(UTC) - timedelta(seconds=1)
        auth.get_valid_token()

        assert mock_post.call_count == 2

    @patch("heimdall_api_client.auth.requests.post")
    def test_renews_token_within_two_minutes_of_expiry(self, mock_post):
        """A token that expires in under 2 minutes is renewed before it is used, though not yet expired."""
        token = _make_token({"sub": "test"})
        mock_post.return_value = _mock_token_response(token, expires_in=90)

        auth = AuthService(client_id="test-id", client_secret="test-secret")
        auth.get_valid_token()

        assert not auth.is_token_expired()
        auth.get_valid_token()

        assert mock_post.call_count == 2

    @patch("heimdall_api_client.auth.requests.post")
    def test_reuses_token_more_than_two_minutes_before_expiry(self, mock_post):
        """A token that expires in over 2 minutes is reused."""
        token = _make_token({"sub": "test"})
        mock_post.return_value = _mock_token_response(token, expires_in=180)

        auth = AuthService(client_id="test-id", client_secret="test-secret")
        auth.get_valid_token()
        auth.get_valid_token()

        mock_post.assert_called_once()


class TestTokenRequestRetry:
    """
    get_token retries transient token endpoint failures (connection errors, timeouts,
    429 and 5xx) up to 3 times with 1s, 2s, 4s backoff, and fails fast on 4xx.
    """

    @patch("heimdall_api_client.auth.time.sleep")
    @patch("heimdall_api_client.auth.requests.post")
    def test_retries_connection_reset_and_returns_token(self, mock_post, mock_sleep):
        token = _make_token({"sub": "test"})
        mock_post.side_effect = [_connection_reset(), _token_response(token)]
        logger = MagicMock()

        auth = AuthService(client_id="test-id", client_secret="test-secret", logger=logger)

        assert auth.get_token() == token
        assert mock_post.call_count == 2
        mock_sleep.assert_called_once_with(1)
        logger.warning.assert_called_once()
        logger.error.assert_not_called()

    @pytest.mark.parametrize(
        "error",
        [
            requests.ReadTimeout("Read timed out."),
            # Connection dropped while the response body was being read.
            requests.exceptions.ChunkedEncodingError("Connection broken: IncompleteRead"),
        ],
        ids=["read_timeout", "connection_broken_mid_body"],
    )
    @patch("heimdall_api_client.auth.time.sleep")
    @patch("heimdall_api_client.auth.requests.post")
    def test_retries_other_transport_errors_and_returns_token(self, mock_post, mock_sleep, error: Exception):
        token = _make_token({"sub": "test"})
        mock_post.side_effect = [error, _token_response(token)]

        auth = AuthService(client_id="test-id", client_secret="test-secret")

        assert auth.get_token() == token
        assert mock_post.call_count == 2

    @pytest.mark.parametrize("status_code", [429, 500, 502, 503, 504])
    @patch("heimdall_api_client.auth.time.sleep")
    @patch("heimdall_api_client.auth.requests.post")
    def test_retries_transient_status_and_returns_token(self, mock_post, mock_sleep, status_code: int):
        token = _make_token({"sub": "test"})
        mock_post.side_effect = [_http_response(status_code, {"error": "server_error"}), _token_response(token)]

        auth = AuthService(client_id="test-id", client_secret="test-secret")

        assert auth.get_token() == token
        assert mock_post.call_count == 2
        mock_sleep.assert_called_once_with(1)

    @patch("heimdall_api_client.auth.time.sleep")
    @patch("heimdall_api_client.auth.requests.post")
    def test_raises_connection_error_after_three_retries(self, mock_post, mock_sleep):
        mock_post.side_effect = [_connection_reset() for _ in range(4)]
        logger = MagicMock()

        auth = AuthService(client_id="test-id", client_secret="test-secret", logger=logger)

        with pytest.raises(requests.ConnectionError):
            auth.get_token()

        assert mock_post.call_count == 4  # 1 initial + 3 retries
        assert mock_sleep.call_args_list == [call(1), call(2), call(4)]
        assert logger.warning.call_count == 3
        logger.error.assert_called_once()
        assert auth.expires_at is None

    @patch("heimdall_api_client.auth.time.sleep")
    @patch("heimdall_api_client.auth.requests.post")
    def test_raises_http_error_after_three_retries_on_5xx(self, mock_post, mock_sleep):
        mock_post.side_effect = [_http_response(503, {"error": "temporarily_unavailable"}) for _ in range(4)]
        logger = MagicMock()

        auth = AuthService(client_id="test-id", client_secret="test-secret", logger=logger)

        with pytest.raises(requests.HTTPError) as exc_info:
            auth.get_token()

        assert exc_info.value.response.status_code == 503
        assert mock_post.call_count == 4
        assert mock_sleep.call_args_list == [call(1), call(2), call(4)]
        logger.error.assert_called_once()

    @pytest.mark.parametrize("status_code", [400, 401, 403, 404])
    @patch("heimdall_api_client.auth.time.sleep")
    @patch("heimdall_api_client.auth.requests.post")
    def test_does_not_retry_client_errors(self, mock_post, mock_sleep, status_code: int):
        mock_post.return_value = _http_response(status_code, {"error": "invalid_client"})
        logger = MagicMock()

        auth = AuthService(client_id="test-id", client_secret="wrong-secret", logger=logger)

        with pytest.raises(requests.HTTPError) as exc_info:
            auth.get_token()

        assert exc_info.value.response.status_code == status_code
        mock_post.assert_called_once()
        mock_sleep.assert_not_called()
        logger.warning.assert_not_called()

    @patch("heimdall_api_client.auth.time.sleep")
    @patch("heimdall_api_client.auth.requests.post")
    def test_does_not_retry_non_transient_request_errors(self, mock_post, mock_sleep):
        mock_post.side_effect = requests.exceptions.InvalidURL("Invalid URL")

        auth = AuthService(client_id="test-id", client_secret="test-secret")

        with pytest.raises(requests.exceptions.InvalidURL):
            auth.get_token()

        mock_post.assert_called_once()
        mock_sleep.assert_not_called()

    # auth.time and client.time are the same module, so one patch sees every sleep.
    @patch("heimdall_api_client.auth.time.sleep")
    @patch("heimdall_api_client.auth.requests.post")
    def test_client_call_does_not_multiply_token_retries(self, mock_post, mock_sleep):
        """The data API retry loop does not retry token failures again: 4 token attempts, not 16."""
        from heimdall_api_client.client import HeimdallApiClient

        mock_post.side_effect = [_connection_reset() for _ in range(4)]
        client = HeimdallApiClient(client_id="test-id", client_secret="test-secret")

        with pytest.raises(requests.ConnectionError):
            client.get_assets()

        assert mock_post.call_count == 4
        assert mock_sleep.call_args_list == [call(1), call(2), call(4)]

    @patch("heimdall_api_client.auth.time.sleep")
    @patch("heimdall_api_client.auth.requests.post")
    def test_client_logs_token_retries_to_its_logger(self, mock_post, mock_sleep):
        """The logger passed to HeimdallApiClient receives the token retry warnings and the final error."""
        from heimdall_api_client.client import HeimdallApiClient

        mock_post.side_effect = [_connection_reset() for _ in range(4)]
        logger = MagicMock()
        client = HeimdallApiClient(client_id="test-id", client_secret="test-secret", logger=logger)

        with pytest.raises(requests.ConnectionError):
            client.get_assets()

        assert logger.warning.call_count == 3  # one per retry
        assert "Transient token request error" in logger.warning.call_args_list[0].args[0]
        logger.error.assert_called_once()


class TestGetRegionFromToken:
    def test_defaults_to_eu_when_region_missing(self):
        auth = AuthService(client_id="test-id", client_secret="test-secret")
        auth._access_token = _make_token({"sub": "test"})

        assert auth.get_region_from_token() == "eu"
