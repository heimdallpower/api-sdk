from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.capacity_monitoring_v1_lines_get_latest_heimdall_dlr_response_200 import (
    CapacityMonitoringV1LinesGetLatestHeimdallDlrResponse200,
)
from ...models.capacity_monitoring_v1_lines_get_latest_heimdall_dlr_x_region import (
    CapacityMonitoringV1LinesGetLatestHeimdallDlrXRegion,
)
from ...models.problem_details import ProblemDetails
from ...types import Unset
from uuid import UUID


def _get_kwargs(
    line_id: UUID,
    *,
    x_region: Union[
        Unset, CapacityMonitoringV1LinesGetLatestHeimdallDlrXRegion
    ] = CapacityMonitoringV1LinesGetLatestHeimdallDlrXRegion.EU,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_region, Unset):
        headers["x-region"] = str(x_region)

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/capacity_monitoring/v1/lines/{line_id}/heimdall_dlrs/latest".format(
            line_id=line_id,
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, CapacityMonitoringV1LinesGetLatestHeimdallDlrResponse200, ProblemDetails]]:
    if response.status_code == 200:
        response_200 = CapacityMonitoringV1LinesGetLatestHeimdallDlrResponse200.from_dict(response.json())

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


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, CapacityMonitoringV1LinesGetLatestHeimdallDlrResponse200, ProblemDetails]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    line_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    x_region: Union[
        Unset, CapacityMonitoringV1LinesGetLatestHeimdallDlrXRegion
    ] = CapacityMonitoringV1LinesGetLatestHeimdallDlrXRegion.EU,
) -> Response[Union[Any, CapacityMonitoringV1LinesGetLatestHeimdallDlrResponse200, ProblemDetails]]:
    """Get latest Heimdall DLR

     This endpoint returns the most recent Heimdall Dynamic Line Rating (DLR) for the line.

    Heimdall DLR is calculated according to our own proprietary method, based on the CIGRE TB-601
    standard for thermal calculation for OHLs.
    This method also takes the conductor temperature and current into account, and uses these to adjust
    the weather parameters during calculations.

    Heimdall DLR is aggregated over the entire line. Using a 5-minute sliding window, the minimum
    ampacity are calculated for each window.

    Args:
        line_id (UUID):
        x_region (Union[Unset, CapacityMonitoringV1LinesGetLatestHeimdallDlrXRegion]):  Default:
            CapacityMonitoringV1LinesGetLatestHeimdallDlrXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CapacityMonitoringV1LinesGetLatestHeimdallDlrResponse200, ProblemDetails]]
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
    client: Union[AuthenticatedClient, Client],
    x_region: Union[
        Unset, CapacityMonitoringV1LinesGetLatestHeimdallDlrXRegion
    ] = CapacityMonitoringV1LinesGetLatestHeimdallDlrXRegion.EU,
) -> Optional[Union[Any, CapacityMonitoringV1LinesGetLatestHeimdallDlrResponse200, ProblemDetails]]:
    """Get latest Heimdall DLR

     This endpoint returns the most recent Heimdall Dynamic Line Rating (DLR) for the line.

    Heimdall DLR is calculated according to our own proprietary method, based on the CIGRE TB-601
    standard for thermal calculation for OHLs.
    This method also takes the conductor temperature and current into account, and uses these to adjust
    the weather parameters during calculations.

    Heimdall DLR is aggregated over the entire line. Using a 5-minute sliding window, the minimum
    ampacity are calculated for each window.

    Args:
        line_id (UUID):
        x_region (Union[Unset, CapacityMonitoringV1LinesGetLatestHeimdallDlrXRegion]):  Default:
            CapacityMonitoringV1LinesGetLatestHeimdallDlrXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CapacityMonitoringV1LinesGetLatestHeimdallDlrResponse200, ProblemDetails]
    """

    return sync_detailed(
        line_id=line_id,
        client=client,
        x_region=x_region,
    ).parsed


async def asyncio_detailed(
    line_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    x_region: Union[
        Unset, CapacityMonitoringV1LinesGetLatestHeimdallDlrXRegion
    ] = CapacityMonitoringV1LinesGetLatestHeimdallDlrXRegion.EU,
) -> Response[Union[Any, CapacityMonitoringV1LinesGetLatestHeimdallDlrResponse200, ProblemDetails]]:
    """Get latest Heimdall DLR

     This endpoint returns the most recent Heimdall Dynamic Line Rating (DLR) for the line.

    Heimdall DLR is calculated according to our own proprietary method, based on the CIGRE TB-601
    standard for thermal calculation for OHLs.
    This method also takes the conductor temperature and current into account, and uses these to adjust
    the weather parameters during calculations.

    Heimdall DLR is aggregated over the entire line. Using a 5-minute sliding window, the minimum
    ampacity are calculated for each window.

    Args:
        line_id (UUID):
        x_region (Union[Unset, CapacityMonitoringV1LinesGetLatestHeimdallDlrXRegion]):  Default:
            CapacityMonitoringV1LinesGetLatestHeimdallDlrXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CapacityMonitoringV1LinesGetLatestHeimdallDlrResponse200, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        line_id=line_id,
        x_region=x_region,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    line_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    x_region: Union[
        Unset, CapacityMonitoringV1LinesGetLatestHeimdallDlrXRegion
    ] = CapacityMonitoringV1LinesGetLatestHeimdallDlrXRegion.EU,
) -> Optional[Union[Any, CapacityMonitoringV1LinesGetLatestHeimdallDlrResponse200, ProblemDetails]]:
    """Get latest Heimdall DLR

     This endpoint returns the most recent Heimdall Dynamic Line Rating (DLR) for the line.

    Heimdall DLR is calculated according to our own proprietary method, based on the CIGRE TB-601
    standard for thermal calculation for OHLs.
    This method also takes the conductor temperature and current into account, and uses these to adjust
    the weather parameters during calculations.

    Heimdall DLR is aggregated over the entire line. Using a 5-minute sliding window, the minimum
    ampacity are calculated for each window.

    Args:
        line_id (UUID):
        x_region (Union[Unset, CapacityMonitoringV1LinesGetLatestHeimdallDlrXRegion]):  Default:
            CapacityMonitoringV1LinesGetLatestHeimdallDlrXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CapacityMonitoringV1LinesGetLatestHeimdallDlrResponse200, ProblemDetails]
    """

    return (
        await asyncio_detailed(
            line_id=line_id,
            client=client,
            x_region=x_region,
        )
    ).parsed
