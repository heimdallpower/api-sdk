from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.capacity_monitoring_v1_lines_get_latest_heimdall_aar_forecasts_response_200 import CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsResponse200
from ...models.capacity_monitoring_v1_lines_get_latest_heimdall_aar_forecasts_x_region import CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsXRegion
from ...models.problem_details import ProblemDetails
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    line_id: UUID,
    *,
    x_region: CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsXRegion | Unset = CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsXRegion.EU,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_region, Unset):
        headers["x-region"] = str(x_region)




    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/capacity_monitoring/v1/lines/{line_id}/heimdall_aars/forecasts".format(line_id=quote(str(line_id), safe=""),),
    }


    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsResponse200 | ProblemDetails | None:
    if response.status_code == 200:
        response_200 = CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401

    if response.status_code == 403:
        response_403 = ProblemDetails.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if response.status_code == 500:
        response_500 = ProblemDetails.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsResponse200 | ProblemDetails]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    line_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    x_region: CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsXRegion | Unset = CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsXRegion.EU,

) -> Response[Any | CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsResponse200 | ProblemDetails]:
    """ Get latest Heimdall AAR forecasts

     This endpoint returns the most recent Heimdall Ambient-Adjusted Rating (AAR) forecasts for the line.

    The forecasted hours returned by the endpoint are defined by the line’s `available_forecast_hours`
    configuration, typically 72 or 240, and are provided in 1-hour intervals.

    The response contains a series of buckets, each with a timestamp and predictions based on different
    values of confidence levels `p80`, `p90`, `p95` and `p99`.

    For each unique timestamp and confidence level, we pick the value from the span which has the lowest
    ampacity value as this will be the dimensioning value for the line.

    Args:
        line_id (UUID):
        x_region (CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsXRegion | Unset):
            Default: CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsResponse200 | ProblemDetails]
     """


    kwargs = _get_kwargs(
        line_id=line_id,
x_region=x_region,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    line_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    x_region: CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsXRegion | Unset = CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsXRegion.EU,

) -> Any | CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsResponse200 | ProblemDetails | None:
    """ Get latest Heimdall AAR forecasts

     This endpoint returns the most recent Heimdall Ambient-Adjusted Rating (AAR) forecasts for the line.

    The forecasted hours returned by the endpoint are defined by the line’s `available_forecast_hours`
    configuration, typically 72 or 240, and are provided in 1-hour intervals.

    The response contains a series of buckets, each with a timestamp and predictions based on different
    values of confidence levels `p80`, `p90`, `p95` and `p99`.

    For each unique timestamp and confidence level, we pick the value from the span which has the lowest
    ampacity value as this will be the dimensioning value for the line.

    Args:
        line_id (UUID):
        x_region (CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsXRegion | Unset):
            Default: CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsResponse200 | ProblemDetails
     """


    return sync_detailed(
        line_id=line_id,
client=client,
x_region=x_region,

    ).parsed

async def asyncio_detailed(
    line_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    x_region: CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsXRegion | Unset = CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsXRegion.EU,

) -> Response[Any | CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsResponse200 | ProblemDetails]:
    """ Get latest Heimdall AAR forecasts

     This endpoint returns the most recent Heimdall Ambient-Adjusted Rating (AAR) forecasts for the line.

    The forecasted hours returned by the endpoint are defined by the line’s `available_forecast_hours`
    configuration, typically 72 or 240, and are provided in 1-hour intervals.

    The response contains a series of buckets, each with a timestamp and predictions based on different
    values of confidence levels `p80`, `p90`, `p95` and `p99`.

    For each unique timestamp and confidence level, we pick the value from the span which has the lowest
    ampacity value as this will be the dimensioning value for the line.

    Args:
        line_id (UUID):
        x_region (CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsXRegion | Unset):
            Default: CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsResponse200 | ProblemDetails]
     """


    kwargs = _get_kwargs(
        line_id=line_id,
x_region=x_region,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    line_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    x_region: CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsXRegion | Unset = CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsXRegion.EU,

) -> Any | CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsResponse200 | ProblemDetails | None:
    """ Get latest Heimdall AAR forecasts

     This endpoint returns the most recent Heimdall Ambient-Adjusted Rating (AAR) forecasts for the line.

    The forecasted hours returned by the endpoint are defined by the line’s `available_forecast_hours`
    configuration, typically 72 or 240, and are provided in 1-hour intervals.

    The response contains a series of buckets, each with a timestamp and predictions based on different
    values of confidence levels `p80`, `p90`, `p95` and `p99`.

    For each unique timestamp and confidence level, we pick the value from the span which has the lowest
    ampacity value as this will be the dimensioning value for the line.

    Args:
        line_id (UUID):
        x_region (CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsXRegion | Unset):
            Default: CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CapacityMonitoringV1LinesGetLatestHeimdallAarForecastsResponse200 | ProblemDetails
     """


    return (await asyncio_detailed(
        line_id=line_id,
client=client,
x_region=x_region,

    )).parsed
