import logging
from typing import List, Optional
from heimdall_api_client.auth import AuthService
from heimdall_api_client.assets_api_client.api.assets import assets_v1_get_assets
from heimdall_api_client.assets_api_client.client import AuthenticatedClient


class HeimdallApiClient:
    """
    SDK entrypoint for interacting with the Heimdall Power External API.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        api_base_url: str = "https://external-api.heimdallcloud.com",
        auth_policy: str = "b2c_1a_clientcredentialsflow",
        tenant: str = "hpadb2cprod",
        auth_authority_domain: str = "hpadb2cprod.b2clogin.com",
        auth_scope: Optional[List[str]] = None,
        logger: Optional[logging.Logger] = None,
    ):
        self.logger = logger or logging.getLogger(__name__)

        self.auth_service = AuthService(
            client_id=client_id,
            client_secret=client_secret,
            auth_policy=auth_policy,
            tenant=tenant,
            authority_domain=auth_authority_domain,
            scope=auth_scope,
        )

        self.api_base_url = api_base_url

    def _get_authenticated_client(self) -> AuthenticatedClient:
        token = self.auth_service.get_valid_token()
        return AuthenticatedClient(base_url=self.api_base_url, token=token)

    def get_assets(self):
        """
        Returns the list of assets from the Assets API.
        """
        client = self._get_authenticated_client()
        response = assets_v1_get_assets.sync_detailed(client=client)
        if response.status_code != 200:
            self.logger.error(f"Failed to fetch assets: {response.status_code} {response.text}")
            raise Exception(f"Error fetching assets: {response.status_code} {response.text}")
        return response.parsed
