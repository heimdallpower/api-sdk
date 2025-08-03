import logging
import requests
import jwt
from datetime import datetime, timedelta
from typing import List, Optional


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
        scope: Optional[List[str]] = None,
        logger: Optional[logging.Logger] = None,
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
        self._access_token: Optional[str] = None
        self._expires_at: Optional[datetime] = None
        self.logger = logger or logging.getLogger(__name__)

    def get_token(self) -> str:
        """Fetches a new access token via client credentials flow."""
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": " ".join(self.scope),
        }

        try:
            response = requests.post(self.token_url, data=data, timeout=10)
            response.raise_for_status()
            token_json = response.json()
            access_token = token_json.get("access_token")
            if not access_token:
                self.logger.error("No access token found in response: %s", token_json)
                raise ValueError("Access token not found in response.")

            self._access_token = access_token

            expires_in = token_json.get("expires_in")
            if expires_in:
                self._expires_at = datetime.utcnow() + timedelta(seconds=int(expires_in))
                self.logger.debug(f"Token expires at {self._expires_at.isoformat()}")

            return self._access_token

        except requests.RequestException as e:
            self.logger.error("Token request failed: %s", e)
            raise
        except Exception as e:
            self.logger.error("Unexpected error during token retrieval: %s", e)
            raise

    def get_valid_token(self) -> str:
        """Returns a valid access token, refreshing it if necessary."""
        if not self._access_token or self.is_token_expired():
            return self.get_token()
        return self._access_token

    def is_token_expired(self) -> bool:
        """Returns True if the token is expired or missing."""
        if not self._expires_at:
            return True
        return datetime.utcnow() >= self._expires_at

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
    def expires_at(self) -> Optional[datetime]:
        """Public accessor for token expiration time."""
        return self._expires_at
