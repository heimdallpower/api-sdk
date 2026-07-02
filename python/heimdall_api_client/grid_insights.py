from __future__ import annotations

import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from heimdall_api_client.assets_api_client.client import AuthenticatedClient
from heimdall_api_client.errors import HeimdallApiError, body_preview
from heimdall_api_client.grid_insights_api_client.models.unit_system import UnitSystem
from heimdall_api_client.grid_insights_api_client.types import UNSET

if TYPE_CHECKING:
    from heimdall_api_client.grid_insights_api_client.models.grid_insights_v1_lines_get_apparent_power_response_200 import (  # noqa: E501
        GridInsightsV1LinesGetApparentPowerResponse200,
    )
    from heimdall_api_client.grid_insights_api_client.models.grid_insights_v1_lines_get_conductor_temperatures_response_200 import (  # noqa: E501
        GridInsightsV1LinesGetConductorTemperaturesResponse200,
    )
    from heimdall_api_client.grid_insights_api_client.models.grid_insights_v1_lines_get_icing_forecast_response_200 import (  # noqa: E501
        GridInsightsV1LinesGetIcingForecastResponse200,
    )
    from heimdall_api_client.grid_insights_api_client.models.grid_insights_v1_lines_get_icing_response_200 import (  # noqa: E501
        GridInsightsV1LinesGetIcingResponse200,
    )
    from heimdall_api_client.grid_insights_api_client.models.grid_insights_v1_lines_get_latest_apparent_power_response_200 import (  # noqa: E501
        GridInsightsV1LinesGetLatestApparentPowerResponse200,
    )
    from heimdall_api_client.grid_insights_api_client.models.grid_insights_v1_lines_get_latest_conductor_temperature_response_200 import (  # noqa: E501
        GridInsightsV1LinesGetLatestConductorTemperatureResponse200,
    )
    from heimdall_api_client.grid_insights_api_client.models.grid_insights_v1_lines_get_latest_current_response_200 import (  # noqa: E501
        GridInsightsV1LinesGetLatestCurrentResponse200,
    )
    from heimdall_api_client.grid_insights_api_client.models.grid_insights_v1_lines_get_latest_icing_response_200 import (  # noqa: E501
        GridInsightsV1LinesGetLatestIcingResponse200,
    )
    from heimdall_api_client.grid_insights_api_client.models.grid_insights_v1_lines_get_sag_and_clearance_response_200 import (  # noqa: E501
        GridInsightsV1LinesGetSagAndClearanceResponse200,
    )


def get_latest_conductor_temperature(
    client: AuthenticatedClient, line_id: UUID, region: str
) -> GridInsightsV1LinesGetLatestConductorTemperatureResponse200:
    from heimdall_api_client.grid_insights_api_client.api.line import (
        grid_insights_v1_lines_get_latest_conductor_temperature as get_latest_conductor_temperature,
    )

    response = get_latest_conductor_temperature.sync_detailed(client=client, line_id=line_id, x_region=region)
    if response.status_code != 200:
        status = int(response.status_code)
        raise HeimdallApiError(
            f"Error fetching latest conductor temperature: {status} {response.status_code.phrase}"
            f" - {body_preview(response.content)}",
            status_code=status,
        )
    return response.parsed


def get_latest_current(
    client: AuthenticatedClient, line_id: UUID, region: str
) -> GridInsightsV1LinesGetLatestCurrentResponse200:
    from heimdall_api_client.grid_insights_api_client.api.line import (
        grid_insights_v1_lines_get_latest_current as get_latest_current,
    )

    response = get_latest_current.sync_detailed(client=client, line_id=line_id, x_region=region)
    if response.status_code != 200:
        status = int(response.status_code)
        raise HeimdallApiError(
            f"Error fetching latest current: {status} {response.status_code.phrase} - {body_preview(response.content)}",
            status_code=status,
        )
    return response.parsed


def get_latest_icing(
    client: AuthenticatedClient,
    line_id: UUID,
    region: str,
    unit_system: UnitSystem | str | None = None,
    since: datetime.datetime | None = None,
) -> GridInsightsV1LinesGetLatestIcingResponse200:
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
        status = int(response.status_code)
        raise HeimdallApiError(
            f"Error fetching latest icing: {status} {response.status_code.phrase} - {body_preview(response.content)}",
            status_code=status,
        )
    return response.parsed


def get_latest_sag_and_clearance(
    client: AuthenticatedClient,
    line_id: UUID,
    region: str,
    unit_system: UnitSystem | str | None = None,
    since: datetime.datetime | None = None,
):
    from heimdall_api_client.grid_insights_api_client.api.line import (
        grid_insights_v1_lines_get_latest_sag_and_clearance as get_latest_sag_and_clearance,
    )

    unit_system_value = UNSET
    if unit_system is not None:
        unit_system_value = unit_system if isinstance(unit_system, UnitSystem) else UnitSystem(unit_system)

    since_value = UNSET if since is None else since

    response = get_latest_sag_and_clearance.sync_detailed(
        client=client,
        line_id=line_id,
        x_region=region,
        unit_system=unit_system_value,
        since=since_value,
    )
    if response.status_code != 200:
        status = int(response.status_code)
        raise HeimdallApiError(
            f"Error fetching latest sag and clearance: {status} {response.status_code.phrase}"
            f" - {body_preview(response.content)}",
            status_code=status,
        )
    return response.parsed


def get_icing(
    client: AuthenticatedClient,
    line_id: UUID,
    region: str,
    from_timestamp: datetime.datetime,
    to_timestamp: datetime.datetime,
    unit_system: UnitSystem | str | None = None,
) -> GridInsightsV1LinesGetIcingResponse200:
    from heimdall_api_client.grid_insights_api_client.api.line import (
        grid_insights_v1_lines_get_icing as _get_icing,
    )

    unit_system_value = UNSET
    if unit_system is not None:
        unit_system_value = unit_system if isinstance(unit_system, UnitSystem) else UnitSystem(unit_system)

    response = _get_icing.sync_detailed(
        client=client,
        line_id=line_id,
        x_region=region,
        from_timestamp=from_timestamp,
        to_timestamp=to_timestamp,
        unit_system=unit_system_value,
    )
    if response.status_code != 200:
        status = int(response.status_code)
        raise HeimdallApiError(
            f"Error fetching icing: {status} {response.status_code.phrase}"
            f" - {body_preview(response.content)}",
            status_code=status,
        )
    return response.parsed


def get_sag_and_clearance(
    client: AuthenticatedClient,
    line_id: UUID,
    region: str,
    from_timestamp: datetime.datetime,
    to_timestamp: datetime.datetime,
    unit_system: UnitSystem | str | None = None,
) -> GridInsightsV1LinesGetSagAndClearanceResponse200:
    from heimdall_api_client.grid_insights_api_client.api.line import (
        grid_insights_v1_lines_get_sag_and_clearance as _get_sag_and_clearance,
    )

    unit_system_value = UNSET
    if unit_system is not None:
        unit_system_value = unit_system if isinstance(unit_system, UnitSystem) else UnitSystem(unit_system)

    response = _get_sag_and_clearance.sync_detailed(
        client=client,
        line_id=line_id,
        x_region=region,
        from_timestamp=from_timestamp,
        to_timestamp=to_timestamp,
        unit_system=unit_system_value,
    )
    if response.status_code != 200:
        status = int(response.status_code)
        raise HeimdallApiError(
            f"Error fetching sag and clearance: {status} {response.status_code.phrase}"
            f" - {body_preview(response.content)}",
            status_code=status,
        )
    return response.parsed


def get_apparent_power(
    client: AuthenticatedClient,
    line_id: UUID,
    region: str,
    from_timestamp: datetime.datetime,
    to_timestamp: datetime.datetime,
) -> GridInsightsV1LinesGetApparentPowerResponse200:
    from heimdall_api_client.grid_insights_api_client.api.line import (
        grid_insights_v1_lines_get_apparent_power as _get_apparent_power,
    )

    response = _get_apparent_power.sync_detailed(
        client=client,
        line_id=line_id,
        x_region=region,
        from_timestamp=from_timestamp,
        to_timestamp=to_timestamp,
    )
    if response.status_code != 200:
        status = int(response.status_code)
        raise HeimdallApiError(
            f"Error fetching apparent power: {status} {response.status_code.phrase}"
            f" - {body_preview(response.content)}",
            status_code=status,
        )
    return response.parsed


def get_latest_apparent_power(
    client: AuthenticatedClient, line_id: UUID, region: str
) -> GridInsightsV1LinesGetLatestApparentPowerResponse200:
    from heimdall_api_client.grid_insights_api_client.api.line import (
        grid_insights_v1_lines_get_latest_apparent_power as _get_latest_apparent_power,
    )

    response = _get_latest_apparent_power.sync_detailed(client=client, line_id=line_id, x_region=region)
    if response.status_code != 200:
        status = int(response.status_code)
        raise HeimdallApiError(
            f"Error fetching latest apparent power: {status} {response.status_code.phrase}"
            f" - {body_preview(response.content)}",
            status_code=status,
        )
    return response.parsed


def get_icing_forecast(
    client: AuthenticatedClient,
    line_id: UUID,
    region: str,
    unit_system: UnitSystem | str | None = None,
) -> GridInsightsV1LinesGetIcingForecastResponse200:
    from heimdall_api_client.grid_insights_api_client.api.line import (
        grid_insights_v1_lines_get_icing_forecast as _get_icing_forecast,
    )

    unit_system_value = UNSET
    if unit_system is not None:
        unit_system_value = unit_system if isinstance(unit_system, UnitSystem) else UnitSystem(unit_system)

    response = _get_icing_forecast.sync_detailed(
        client=client,
        line_id=line_id,
        x_region=region,
        unit_system=unit_system_value,
    )
    if response.status_code != 200:
        status = int(response.status_code)
        raise HeimdallApiError(
            f"Error fetching icing forecast: {status} {response.status_code.phrase}"
            f" - {body_preview(response.content)}",
            status_code=status,
        )
    return response.parsed


def get_conductor_temperatures(
    client: AuthenticatedClient,
    line_id: UUID,
    region: str,
    from_timestamp: datetime.datetime,
    to_timestamp: datetime.datetime,
) -> GridInsightsV1LinesGetConductorTemperaturesResponse200:
    from heimdall_api_client.grid_insights_api_client.api.line import (
        grid_insights_v1_lines_get_conductor_temperatures as _get_conductor_temperatures,
    )

    response = _get_conductor_temperatures.sync_detailed(
        client=client,
        line_id=line_id,
        x_region=region,
        from_timestamp=from_timestamp,
        to_timestamp=to_timestamp,
    )
    if response.status_code != 200:
        status = int(response.status_code)
        raise HeimdallApiError(
            f"Error fetching conductor temperatures: {status} {response.status_code.phrase}"
            f" - {body_preview(response.content)}",
            status_code=status,
        )
    return response.parsed
