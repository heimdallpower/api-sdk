import logging
from typing import List, Optional
from uuid import UUID
from heimdall_api_client.auth import AuthService
from heimdall_api_client.assets import get_assets
from heimdall_api_client.capacity_monitoring import get_latest_heimdall_aar, get_latest_heimdall_arr_forecasts, get_latest_heimdall_dlr, get_latest_heimdall_dlr_forecasts
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
    
    def _get_region(self) -> str:
        return self.auth_service.get_region_from_token()

    def get_assets(self):
        """
        Returns the list of assets from the Assets API.
        """
        return get_assets(
            client=self._get_authenticated_client(), 
            x_region=self._get_region()
            )
    
    def get_latest_heimdall_dlr(self, line_id: UUID):
        """
        Returns the latest Heimdall DLR (Dynamic Line rating) data.
        """
        return get_latest_heimdall_dlr(
            client=self._get_authenticated_client(),
            line_id=line_id,
            region=self._get_region()
        )
    
    def get_latest_heimdall_aar(self, line_id: UUID):
        """
        Returns the latest Heimdall AAR (Available Ampacity Rating) data.
        """
        return get_latest_heimdall_aar(
            client=self._get_authenticated_client(),
            line_id=line_id,
            region=self._get_region()
        )
    
    def get_latest_heimdall_dlr_forecasts(self, line_id: UUID):
        """
        Returns the latest Heimdall DLR forecasts.
        """
        return get_latest_heimdall_dlr_forecasts(
            client=self._get_authenticated_client(),
            line_id=line_id,
            region=self._get_region()
        )
    
    def get_latest_heimdall_aar_forecasts(self, line_id: UUID):
        """
        Returns the latest Heimdall AAR forecasts.
        """
        return get_latest_heimdall_arr_forecasts(
            client=self._get_authenticated_client(),
            line_id=line_id,
            region=self._get_region()
        )
