from heimdall_api_client.assets_api_client.api.assets import assets_v1_get_assets
from heimdall_api_client.assets_api_client.client import AuthenticatedClient
from heimdall_api_client.assets_api_client.models.assets_v1_get_assets_response_200 import (
    AssetsV1GetAssetsResponse200,
)


def get_assets(client: AuthenticatedClient, x_region: str) -> AssetsV1GetAssetsResponse200:
    response = assets_v1_get_assets.sync_detailed(client=client, x_region=x_region)
    if response.status_code != 200:
        raise Exception(f"Error fetching assets: {response.status_code} {response.text}")
    return response.parsed
