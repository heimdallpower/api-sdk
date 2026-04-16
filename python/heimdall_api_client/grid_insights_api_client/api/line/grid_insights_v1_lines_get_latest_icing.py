import datetime
from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.grid_insights_v1_lines_get_latest_icing_response_200 import GridInsightsV1LinesGetLatestIcingResponse200
from ...models.grid_insights_v1_lines_get_latest_icing_unit_system import GridInsightsV1LinesGetLatestIcingUnitSystem
from ...models.grid_insights_v1_lines_get_latest_icing_x_region import GridInsightsV1LinesGetLatestIcingXRegion
from ...models.problem_details import ProblemDetails
from ...types import UNSET, Response, Unset


def _get_kwargs(
    line_id: UUID,
    *,
    unit_system: GridInsightsV1LinesGetLatestIcingUnitSystem
    | Unset = GridInsightsV1LinesGetLatestIcingUnitSystem.METRIC,
    since: datetime.datetime | Unset = UNSET,
    x_region: GridInsightsV1LinesGetLatestIcingXRegion | Unset = GridInsightsV1LinesGetLatestIcingXRegion.EU,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_region, Unset):
        headers["x-region"] = str(x_region)

    params: dict[str, Any] = {}

    json_unit_system: str | Unset = UNSET
    if not isinstance(unit_system, Unset):
        json_unit_system = unit_system.value

    params["unit_system"] = json_unit_system

    json_since: str | Unset = UNSET
    if not isinstance(since, Unset):
        json_since = since.isoformat()
    params["since"] = json_since

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/grid_insights/v1/lines/{line_id}/icing/latest".format(
            line_id=quote(str(line_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | GridInsightsV1LinesGetLatestIcingResponse200 | ProblemDetails | None:
    if response.status_code == 200:
        response_200 = GridInsightsV1LinesGetLatestIcingResponse200.from_dict(response.json())

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
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | GridInsightsV1LinesGetLatestIcingResponse200 | ProblemDetails]:
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
    unit_system: GridInsightsV1LinesGetLatestIcingUnitSystem
    | Unset = GridInsightsV1LinesGetLatestIcingUnitSystem.METRIC,
    since: datetime.datetime | Unset = UNSET,
    x_region: GridInsightsV1LinesGetLatestIcingXRegion | Unset = GridInsightsV1LinesGetLatestIcingXRegion.EU,
) -> Response[Any | GridInsightsV1LinesGetLatestIcingResponse200 | ProblemDetails]:
    """Get latest icing

     This endpoint returns the most recent icing data for the line.

    The icing data is divided into two sections:

    - **`max`**: Maximum icing measurements, i.e. maximum ice weight, maximum tension and maximum
    tension percentage of break strength, with its associated span phase on the line.
    - **`spans`**:  Icing data grouped by span, with each span listing its span phases and their latest
    ice measurements.

    Each span phase provides the following data:
    - **`ice_weight`**: The mass of ice accumulated on the conductor.
    - **`tension`**: The mechanical tension force in the conductor, which increases as ice accumulates.
    - **`tension_percentage_of_break_strength`**: Safety-critical metric showing how close the conductor
    is to its breaking point.
    - **`timestamp`**: Time (UTC) when the icing measurements were calculated for the span phase.
    Timestamps may differ per conductor due to data availability.

    Query parameter `since` sets a cut-off time (UTC) for included icing measurements. Only measurements
    with timestamps at or after `since` are considered. If omitted, `since` defaults to 30 minutes ago.

    If the latest icing data for a span phase is older than `since`, that span phase is excluded.

    If no icing data is available for the entire line, the endpoint returns `404 Not Found`.

    Args:
        line_id (UUID):
        unit_system (GridInsightsV1LinesGetLatestIcingUnitSystem | Unset):  Default:
            GridInsightsV1LinesGetLatestIcingUnitSystem.METRIC.
        since (datetime.datetime | Unset):  Example: 2024-07-01 12:00:00.001000+00:00.
        x_region (GridInsightsV1LinesGetLatestIcingXRegion | Unset):  Default:
            GridInsightsV1LinesGetLatestIcingXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GridInsightsV1LinesGetLatestIcingResponse200 | ProblemDetails]
    """

    kwargs = _get_kwargs(
        line_id=line_id,
        unit_system=unit_system,
        since=since,
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
    unit_system: GridInsightsV1LinesGetLatestIcingUnitSystem
    | Unset = GridInsightsV1LinesGetLatestIcingUnitSystem.METRIC,
    since: datetime.datetime | Unset = UNSET,
    x_region: GridInsightsV1LinesGetLatestIcingXRegion | Unset = GridInsightsV1LinesGetLatestIcingXRegion.EU,
) -> Any | GridInsightsV1LinesGetLatestIcingResponse200 | ProblemDetails | None:
    """Get latest icing

     This endpoint returns the most recent icing data for the line.

    The icing data is divided into two sections:

    - **`max`**: Maximum icing measurements, i.e. maximum ice weight, maximum tension and maximum
    tension percentage of break strength, with its associated span phase on the line.
    - **`spans`**:  Icing data grouped by span, with each span listing its span phases and their latest
    ice measurements.

    Each span phase provides the following data:
    - **`ice_weight`**: The mass of ice accumulated on the conductor.
    - **`tension`**: The mechanical tension force in the conductor, which increases as ice accumulates.
    - **`tension_percentage_of_break_strength`**: Safety-critical metric showing how close the conductor
    is to its breaking point.
    - **`timestamp`**: Time (UTC) when the icing measurements were calculated for the span phase.
    Timestamps may differ per conductor due to data availability.

    Query parameter `since` sets a cut-off time (UTC) for included icing measurements. Only measurements
    with timestamps at or after `since` are considered. If omitted, `since` defaults to 30 minutes ago.

    If the latest icing data for a span phase is older than `since`, that span phase is excluded.

    If no icing data is available for the entire line, the endpoint returns `404 Not Found`.

    Args:
        line_id (UUID):
        unit_system (GridInsightsV1LinesGetLatestIcingUnitSystem | Unset):  Default:
            GridInsightsV1LinesGetLatestIcingUnitSystem.METRIC.
        since (datetime.datetime | Unset):  Example: 2024-07-01 12:00:00.001000+00:00.
        x_region (GridInsightsV1LinesGetLatestIcingXRegion | Unset):  Default:
            GridInsightsV1LinesGetLatestIcingXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | GridInsightsV1LinesGetLatestIcingResponse200 | ProblemDetails
    """

    return sync_detailed(
        line_id=line_id,
        client=client,
        unit_system=unit_system,
        since=since,
        x_region=x_region,
    ).parsed


async def asyncio_detailed(
    line_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    unit_system: GridInsightsV1LinesGetLatestIcingUnitSystem
    | Unset = GridInsightsV1LinesGetLatestIcingUnitSystem.METRIC,
    since: datetime.datetime | Unset = UNSET,
    x_region: GridInsightsV1LinesGetLatestIcingXRegion | Unset = GridInsightsV1LinesGetLatestIcingXRegion.EU,
) -> Response[Any | GridInsightsV1LinesGetLatestIcingResponse200 | ProblemDetails]:
    """Get latest icing

     This endpoint returns the most recent icing data for the line.

    The icing data is divided into two sections:

    - **`max`**: Maximum icing measurements, i.e. maximum ice weight, maximum tension and maximum
    tension percentage of break strength, with its associated span phase on the line.
    - **`spans`**:  Icing data grouped by span, with each span listing its span phases and their latest
    ice measurements.

    Each span phase provides the following data:
    - **`ice_weight`**: The mass of ice accumulated on the conductor.
    - **`tension`**: The mechanical tension force in the conductor, which increases as ice accumulates.
    - **`tension_percentage_of_break_strength`**: Safety-critical metric showing how close the conductor
    is to its breaking point.
    - **`timestamp`**: Time (UTC) when the icing measurements were calculated for the span phase.
    Timestamps may differ per conductor due to data availability.

    Query parameter `since` sets a cut-off time (UTC) for included icing measurements. Only measurements
    with timestamps at or after `since` are considered. If omitted, `since` defaults to 30 minutes ago.

    If the latest icing data for a span phase is older than `since`, that span phase is excluded.

    If no icing data is available for the entire line, the endpoint returns `404 Not Found`.

    Args:
        line_id (UUID):
        unit_system (GridInsightsV1LinesGetLatestIcingUnitSystem | Unset):  Default:
            GridInsightsV1LinesGetLatestIcingUnitSystem.METRIC.
        since (datetime.datetime | Unset):  Example: 2024-07-01 12:00:00.001000+00:00.
        x_region (GridInsightsV1LinesGetLatestIcingXRegion | Unset):  Default:
            GridInsightsV1LinesGetLatestIcingXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GridInsightsV1LinesGetLatestIcingResponse200 | ProblemDetails]
    """

    kwargs = _get_kwargs(
        line_id=line_id,
        unit_system=unit_system,
        since=since,
        x_region=x_region,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    line_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    unit_system: GridInsightsV1LinesGetLatestIcingUnitSystem
    | Unset = GridInsightsV1LinesGetLatestIcingUnitSystem.METRIC,
    since: datetime.datetime | Unset = UNSET,
    x_region: GridInsightsV1LinesGetLatestIcingXRegion | Unset = GridInsightsV1LinesGetLatestIcingXRegion.EU,
) -> Any | GridInsightsV1LinesGetLatestIcingResponse200 | ProblemDetails | None:
    """Get latest icing

     This endpoint returns the most recent icing data for the line.

    The icing data is divided into two sections:

    - **`max`**: Maximum icing measurements, i.e. maximum ice weight, maximum tension and maximum
    tension percentage of break strength, with its associated span phase on the line.
    - **`spans`**:  Icing data grouped by span, with each span listing its span phases and their latest
    ice measurements.

    Each span phase provides the following data:
    - **`ice_weight`**: The mass of ice accumulated on the conductor.
    - **`tension`**: The mechanical tension force in the conductor, which increases as ice accumulates.
    - **`tension_percentage_of_break_strength`**: Safety-critical metric showing how close the conductor
    is to its breaking point.
    - **`timestamp`**: Time (UTC) when the icing measurements were calculated for the span phase.
    Timestamps may differ per conductor due to data availability.

    Query parameter `since` sets a cut-off time (UTC) for included icing measurements. Only measurements
    with timestamps at or after `since` are considered. If omitted, `since` defaults to 30 minutes ago.

    If the latest icing data for a span phase is older than `since`, that span phase is excluded.

    If no icing data is available for the entire line, the endpoint returns `404 Not Found`.

    Args:
        line_id (UUID):
        unit_system (GridInsightsV1LinesGetLatestIcingUnitSystem | Unset):  Default:
            GridInsightsV1LinesGetLatestIcingUnitSystem.METRIC.
        since (datetime.datetime | Unset):  Example: 2024-07-01 12:00:00.001000+00:00.
        x_region (GridInsightsV1LinesGetLatestIcingXRegion | Unset):  Default:
            GridInsightsV1LinesGetLatestIcingXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | GridInsightsV1LinesGetLatestIcingResponse200 | ProblemDetails
    """

    return (
        await asyncio_detailed(
            line_id=line_id,
            client=client,
            unit_system=unit_system,
            since=since,
            x_region=x_region,
        )
    ).parsed
