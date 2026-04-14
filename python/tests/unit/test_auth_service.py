from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch

import jwt

from heimdall_api_client.auth import AuthService


def _make_token(claims: dict) -> str:
    return jwt.encode(claims, key="not-a-real-secret-just-for-tests", algorithm="HS256")


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


class TestGetRegionFromToken:
    def test_defaults_to_eu_when_region_missing(self):
        auth = AuthService(client_id="test-id", client_secret="test-secret")
        auth._access_token = _make_token({"sub": "test"})

        assert auth.get_region_from_token() == "eu"
