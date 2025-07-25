from uuid import UUID
from heimdall_api_client.assets_api_client.client import AuthenticatedClient


def get_latest_conductor_temperature(client: AuthenticatedClient, line_id: UUID, region: str):
    from heimdall_api_client.grid_insights_api_client.api.line import (
        grid_insights_v1_lines_get_latest_conductor_temperature as get_latest_conductor_temperature
    )
    response = get_latest_conductor_temperature.sync_detailed(client=client, line_id=line_id, x_region=region)
    if response.status_code != 200:
        raise Exception(f"Error fetching latest conductor temperature: {response.status_code} {response.text}")
    return response.parsed

def get_latest_current(client: AuthenticatedClient, line_id: UUID, region: str):
    from heimdall_api_client.grid_insights_api_client.api.line import (
        grid_insights_v1_lines_get_latest_current as get_latest_current
    )
    response = get_latest_current.sync_detailed(client=client, line_id=line_id, x_region=region)
    if response.status_code != 200:
        raise Exception(f"Error fetching latest current: {response.status_code} {response.text}")
    return response.parsed