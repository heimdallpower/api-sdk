from uuid import UUID
import datetime
from heimdall_api_client.assets_api_client.client import AuthenticatedClient
from heimdall_api_client.grid_insights_api_client.models.unit_system import UnitSystem
from heimdall_api_client.grid_insights_api_client.types import UNSET


def get_latest_conductor_temperature(client: AuthenticatedClient, line_id: UUID, region: str):
    from heimdall_api_client.grid_insights_api_client.api.line import (
        grid_insights_v1_lines_get_latest_conductor_temperature as get_latest_conductor_temperature,
    )

    response = get_latest_conductor_temperature.sync_detailed(client=client, line_id=line_id, x_region=region)
    if response.status_code != 200:
        raise Exception(f"Error fetching latest conductor temperature: {response.status_code} {response.content}")
    return response.parsed


def get_latest_current(client: AuthenticatedClient, line_id: UUID, region: str):
    from heimdall_api_client.grid_insights_api_client.api.line import (
        grid_insights_v1_lines_get_latest_current as get_latest_current,
    )

    response = get_latest_current.sync_detailed(client=client, line_id=line_id, x_region=region)
    if response.status_code != 200:
        raise Exception(f"Error fetching latest current: {response.status_code} {response.text}")
    return response.parsed


def get_latest_icing(
    client: AuthenticatedClient,
    line_id: UUID,
    region: str,
    unit_system: UnitSystem | str | None = None,
    since: datetime.datetime | None = None,
):
    from heimdall_api_client.grid_insights_api_client.api.line import (
        grid_insights_v1_lines_get_latest_icing as get_latest_icing,
    )

    unit_system_value = UNSET
    if unit_system is not None:
        unit_system_value = unit_system if isinstance(unit_system, UnitSystem) else UnitSystem(unit_system)

    since_value = UNSET if since is None else since

    response = get_latest_icing.sync_detailed(
        client=client,
        line_id=line_id,
        x_region=region,
        unit_system=unit_system_value,
        since=since_value,
    )
    if response.status_code != 200:
        raise Exception(f"Error fetching latest icing: {response.status_code} {response.text}")
    return response.parsed
