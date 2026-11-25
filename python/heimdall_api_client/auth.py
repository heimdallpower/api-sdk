import logging
import time
from datetime import UTC, datetime, timedelta

import jwt
import requests

_MAX_TOKEN_RETRY_ATTEMPTS = 3

# Renew the token this long before it expires: a token used up to its expiry can reach the API
# after it expired, and the API rejects it with 401. Matches the .NET SDK.
_TOKEN_RENEWAL_MARGIN = timedelta(minutes=2)

# Token endpoint responses worth retrying. 400/401 (bad credentials, bad scope) are not.
_TRANSIENT_TOKEN_STATUS_CODES = frozenset({429, 500, 502, 503, 504})

# Network failures before or while receiving the token response, e.g. "Connection reset by peer".
_TRANSIENT_TOKEN_ERRORS = (
    requests.ConnectionError,
    requests.Timeout,
    requests.exceptions.ChunkedEncodingError,
)


class AuthService:
    """
    Handles access token retrieval using Azure AD B2C client credentials flow.
    Automatically handles token expiration and region extraction from claims.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        auth_policy: str = "b2c_1a_clientcredentialsflow",
        tenant: str = "hpadb2cprod",
        authority_domain: str = "hpadb2cprod.b2clogin.com",
        scope: list[str] | None = None,
        logger: logging.Logger | None = None,
    ):
        if not client_id or not client_secret:
            raise ValueError("client_id and client_secret must be provided")

        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant = tenant
        self.auth_policy = auth_policy
        self.authority_domain = authority_domain
        self.scope = scope or ["https://hpadb2cprod.onmicrosoft.com/dc5758ae-4eea-416e-9e61-812914d9a49a/.default"]
        self.token_url = (
            f"https://{self.authority_domain}/{self.tenant}.onmicrosoft.com/{self.auth_policy}/oauth2/v2.0/token"
        )
        self._access_token: str | None = None
        self._expires_at: datetime | None = None
        self.logger = logger or logging.getLogger(__name__)

    def get_token(self) -> str:
        """
        Fetches a new access token via client credentials flow.

        Transient failures (connection errors, timeouts, HTTP 429, 500, 502, 503, 504) are retried
        up to 3 times with exponential backoff (1s, 2s, 4s). Other errors, such as 400 or 401 for
        invalid credentials, are raised immediately.
        """
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": " ".join(self.scope),
        }

        try:
            response = self._post_token_request_with_retry(data)
            response.raise_for_status()
            token_json = response.json()
            access_token = token_json.get("access_token")
            if not access_token:
                self.logger.error("No access token found in response: %s", token_json)
                raise ValueError("Access token not found in response.")

            self._access_token = access_token

            expires_in = token_json.get("expires_in")
            if expires_in:
                self._expires_at = datetime.now(UTC) + timedelta(seconds=int(expires_in))
                self.logger.debug(f"Token expires at {self._expires_at.isoformat()}")

            return self._access_token

        except requests.RequestException as e:
            self.logger.error("Token request failed: %s", e)
            raise
        except Exception as e:
            self.logger.error("Unexpected error during token retrieval: %s", e)
            raise

    def _post_token_request_with_retry(self, data: dict[str, str]) -> requests.Response:
        """
        Posts the token request and retries transient failures with exponential backoff (1s, 2s, 4s).
        Returns the last response once it is not transient or the retries are used up; the caller
        decides whether that response is an error.
        """
        attempt = 0
        while True:
            try:
                response = requests.post(self.token_url, data=data, timeout=10)
            except _TRANSIENT_TOKEN_ERRORS as exc:
                if attempt >= _MAX_TOKEN_RETRY_ATTEMPTS:
                    raise
                reason = str(exc)
            else:
                if response.status_code not in _TRANSIENT_TOKEN_STATUS_CODES or attempt >= _MAX_TOKEN_RETRY_ATTEMPTS:
                    return response
                reason = f"HTTP {response.status_code}"

            attempt += 1
            delay = 2 ** (attempt - 1)  # 1s, 2s, 4s
            self.logger.warning(
                "Transient token request error (%s) on attempt %d/%d. Retrying in %ds...",
                reason,
                attempt,
                _MAX_TOKEN_RETRY_ATTEMPTS,
                delay,
            )
            time.sleep(delay)

    def get_valid_token(self) -> str:
        """
        Returns a valid access token, refreshing it if necessary.

        The token is renewed 2 minutes before it expires, so requests don't use a token that is
        about to expire.
        """
        if not self._access_token or self._expires_within(_TOKEN_RENEWAL_MARGIN):
            return self.get_token()
        return self._access_token

    def is_token_expired(self) -> bool:
        """Returns True if the token is expired or missing."""
        return self._expires_within(timedelta(0))

    def _expires_within(self, margin: timedelta) -> bool:
        """Returns True if the token is missing or expires within ``margin`` from now."""
        if not self._expires_at:
            return True
        return datetime.now(UTC) >= self._expires_at - margin

    def get_token_claims(self) -> dict:
        """Returns the decoded claims from the current access token."""
        if not self._access_token:
            raise ValueError("Access token is not set. Call get_token() first.")
        return jwt.decode(self._access_token, options={"verify_signature": False})

    def get_region_from_token(self) -> str:
        """
        Extracts the 'region' claim from the access token.
        Defaults to 'eu' if the claim is missing or invalid.
        """
        if not self._access_token:
            raise ValueError("Access token is not set. Call get_token() first.")

        try:
            claims = self.get_token_claims()
            region = claims.get("region")
            if not region:
                self.logger.warning("Region not found in token claims, defaulting to 'eu'.")
                return "eu"
            return region.lower()
        except Exception as e:
            self.logger.error("Failed to decode region from access token: %s", e)
            return "eu"

    @property
    def expires_at(self) -> datetime | None:
        """Public accessor for token expiration time."""
        return self._expires_at
