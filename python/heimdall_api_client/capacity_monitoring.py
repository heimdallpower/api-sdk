from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from heimdall_api_client.assets_api_client.client import AuthenticatedClient
from heimdall_api_client.capacity_monitoring_api_client.api.line import (
    capacity_monitoring_v1_lines_get_latest_heimdall_aar as get_latest_aar,
)
from heimdall_api_client.capacity_monitoring_api_client.api.line import (
    capacity_monitoring_v1_lines_get_latest_heimdall_aar_forecasts as get_latest_aar_forecasts,
)
from heimdall_api_client.capacity_monitoring_api_client.api.line import (
    capacity_monitoring_v1_lines_get_latest_heimdall_dlr as get_latest_dlr,
)
from heimdall_api_client.capacity_monitoring_api_client.api.line import (
    capacity_monitoring_v1_lines_get_latest_heimdall_dlr_forecasts as get_latest_dlr_forecasts,
)

if TYPE_CHECKING:
    from heimdall_api_client.capacity_monitoring_api_client.models.capacity_monitoring_v1_facilities_get_latest_circuit_rating_forecasts_response_200 import (  # noqa: E501
        CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsResponse200,
    )
    from heimdall_api_client.capacity_monitoring_api_client.models.capacity_monitoring_v1_facilities_get_latest_circuit_rating_response_200 import (  # noqa: E501
        CapacityMonitoringV1FacilitiesGetLatestCircuitRatingResponse200,
    )
    from heimdall_api_client.capacity_monitoring_api_client.models.capacity_monitoring_v1_lines_get_latest_heimdall_aar_forecasts_response_200 import (  # noqa: E501
        CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsResponse200,
    )
    from heimdall_api_client.capacity_monitoring_api_client.models.capacity_monitoring_v1_lines_get_latest_heimdall_aar_response_200 import (  # noqa: E501
        CapacityMonitoringV1LinesGetLatestHeimdallAarResponse200,
    )
    from heimdall_api_client.capacity_monitoring_api_client.models.capacity_monitoring_v1_lines_get_latest_heimdall_dlr_forecasts_response_200 import (  # noqa: E501
        CapacityMonitoringV1LinesGetLatestHeimdallDlrForecastsResponse200,
    )
    from heimdall_api_client.capacity_monitoring_api_client.models.capacity_monitoring_v1_lines_get_latest_heimdall_dlr_response_200 import (  # noqa: E501
        CapacityMonitoringV1LinesGetLatestHeimdallDlrResponse200,
    )


def get_latest_heimdall_dlr(
    client: AuthenticatedClient, line_id: UUID, region: str
) -> CapacityMonitoringV1LinesGetLatestHeimdallDlrResponse200:
    response = get_latest_dlr.sync_detailed(client=client, line_id=line_id, x_region=region)
    if response.status_code != 200:
        raise Exception(f"Error fetching latest Heimdall DLR: {response.status_code} {response.text}")
    return response.parsed


def get_latest_heimdall_aar(
    client: AuthenticatedClient, line_id: UUID, region: str
) -> CapacityMonitoringV1LinesGetLatestHeimdallAarResponse200:
    response = get_latest_aar.sync_detailed(client=client, line_id=line_id, x_region=region)
    if response.status_code != 200:
        raise Exception(f"Error fetching latest Heimdall AAR: {response.status_code} {response.text}")
    return response.parsed


def get_latest_heimdall_dlr_forecasts(
    client: AuthenticatedClient, line_id: UUID, region: str
) -> CapacityMonitoringV1LinesGetLatestHeimdallDlrForecastsResponse200:
    response = get_latest_dlr_forecasts.sync_detailed(client=client, line_id=line_id, x_region=region)
    if response.status_code != 200:
        raise Exception(f"Error fetching latest Heimdall DLR forecasts: {response.status_code} {response.text}")
    return response.parsed


def get_latest_heimdall_arr_forecasts(
    client: AuthenticatedClient, line_id: UUID, region: str
) -> CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsResponse200:
    response = get_latest_aar_forecasts.sync_detailed(client=client, line_id=line_id, x_region=region)
    if response.status_code != 200:
        raise Exception(f"Error fetching latest Heimdall AAR forecasts: {response.status_code} {response.text}")
    return response.parsed


def get_latest_circuit_ratring(
    client: AuthenticatedClient, facility_id: UUID, x_region: str
) -> CapacityMonitoringV1FacilitiesGetLatestCircuitRatingResponse200:
    from heimdall_api_client.capacity_monitoring_api_client.api.facility import (
        capacity_monitoring_v1_facilities_get_latest_circuit_rating as get_latest_circuit_rating,
    )

    response = get_latest_circuit_rating.sync_detailed(client=client, facility_id=facility_id, x_region=x_region)
    if response.status_code != 200:
        raise Exception(f"Error fetching latest circuit rating: {response.status_code} {response.text}")
    return response.parsed


def get_latest_circuit_rating_forecasts(
    client: AuthenticatedClient, facility_id: UUID, x_region: str
) -> CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsResponse200:
    from heimdall_api_client.capacity_monitoring_api_client.api.facility import (
        capacity_monitoring_v1_facilities_get_latest_circuit_rating_forecasts as get_latest_circuit_rating_forecasts,
    )

    response = get_latest_circuit_rating_forecasts.sync_detailed(
        client=client, facility_id=facility_id, x_region=x_region
    )
    if response.status_code != 200:
        raise Exception(f"Error fetching latest circuit rating forecasts: {response.status_code} {response.text}")
    return response.parsed
