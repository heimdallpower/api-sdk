import datetime
from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.grid_insights_v1_lines_get_sag_and_clearance_response_200 import (
    GridInsightsV1LinesGetSagAndClearanceResponse200,
)
from ...models.grid_insights_v1_lines_get_sag_and_clearance_x_region import GridInsightsV1LinesGetSagAndClearanceXRegion
from ...models.problem_details import ProblemDetails
from ...models.unit_system import UnitSystem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    line_id: UUID,
    *,
    from_timestamp: datetime.datetime,
    to_timestamp: datetime.datetime,
    unit_system: UnitSystem | Unset = UNSET,
    x_region: GridInsightsV1LinesGetSagAndClearanceXRegion | Unset = GridInsightsV1LinesGetSagAndClearanceXRegion.EU,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_region, Unset):
        headers["x-region"] = str(x_region)

    params: dict[str, Any] = {}

    json_from_timestamp = from_timestamp.isoformat()
    params["from_timestamp"] = json_from_timestamp

    json_to_timestamp = to_timestamp.isoformat()
    params["to_timestamp"] = json_to_timestamp

    json_unit_system: str | Unset = UNSET
    if not isinstance(unit_system, Unset):
        json_unit_system = unit_system.value

    params["unit_system"] = json_unit_system

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/grid_insights/v1/lines/{line_id}/sag_and_clearance".format(
            line_id=quote(str(line_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | GridInsightsV1LinesGetSagAndClearanceResponse200 | ProblemDetails | None:
    if response.status_code == 200:
        response_200 = GridInsightsV1LinesGetSagAndClearanceResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ProblemDetails.from_dict(response.json())

        return response_400

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
) -> Response[Any | GridInsightsV1LinesGetSagAndClearanceResponse200 | ProblemDetails]:
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
    from_timestamp: datetime.datetime,
    to_timestamp: datetime.datetime,
    unit_system: UnitSystem | Unset = UNSET,
    x_region: GridInsightsV1LinesGetSagAndClearanceXRegion | Unset = GridInsightsV1LinesGetSagAndClearanceXRegion.EU,
) -> Response[Any | GridInsightsV1LinesGetSagAndClearanceResponse200 | ProblemDetails]:
    """Get sag and clearance

     This endpoint returns sag and clearance data for the line within a specified time range.

    The sag and clearance data is divided into three sections:

    - **`max_sag`**: The span phase with the maximum sag across all span phases on the line over the
    requested period.
    - **`min_clearance`**: The span phase with the minimum clearance across all span phases on the line
    over the requested period. Null if no span phase has clearance data.
    - **`spans`**: Sag and clearance data grouped by span, with each span listing its span phases and
    their measurements over time.

    Each span phase entry provides the following data:
    - **`sag`**: The maximum vertical deflection of the conductor from the straight line between its two
    support points.
    - **`clearance`**: The vertical distance between the conductor and the ground or objects below.
    - **`timestamp`**: Time (UTC) when the sag and clearance measurements were calculated for the span
    phase. Timestamps may differ per conductor due to data availability.

    The period between `from_timestamp` and `to_timestamp` must not exceed 30 days.

    If no sag and clearance data is available for the entire line within the period, the endpoint
    returns `404 Not Found`.

    Args:
        line_id (UUID):
        from_timestamp (datetime.datetime):  Example: 2024-07-01 00:00:00+00:00.
        to_timestamp (datetime.datetime):  Example: 2024-07-02 00:00:00+00:00.
        unit_system (UnitSystem | Unset):
        x_region (GridInsightsV1LinesGetSagAndClearanceXRegion | Unset):  Default:
            GridInsightsV1LinesGetSagAndClearanceXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GridInsightsV1LinesGetSagAndClearanceResponse200 | ProblemDetails]
    """

    kwargs = _get_kwargs(
        line_id=line_id,
        from_timestamp=from_timestamp,
        to_timestamp=to_timestamp,
        unit_system=unit_system,
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
    from_timestamp: datetime.datetime,
    to_timestamp: datetime.datetime,
    unit_system: UnitSystem | Unset = UNSET,
    x_region: GridInsightsV1LinesGetSagAndClearanceXRegion | Unset = GridInsightsV1LinesGetSagAndClearanceXRegion.EU,
) -> Any | GridInsightsV1LinesGetSagAndClearanceResponse200 | ProblemDetails | None:
    """Get sag and clearance

     This endpoint returns sag and clearance data for the line within a specified time range.

    The sag and clearance data is divided into three sections:

    - **`max_sag`**: The span phase with the maximum sag across all span phases on the line over the
    requested period.
    - **`min_clearance`**: The span phase with the minimum clearance across all span phases on the line
    over the requested period. Null if no span phase has clearance data.
    - **`spans`**: Sag and clearance data grouped by span, with each span listing its span phases and
    their measurements over time.

    Each span phase entry provides the following data:
    - **`sag`**: The maximum vertical deflection of the conductor from the straight line between its two
    support points.
    - **`clearance`**: The vertical distance between the conductor and the ground or objects below.
    - **`timestamp`**: Time (UTC) when the sag and clearance measurements were calculated for the span
    phase. Timestamps may differ per conductor due to data availability.

    The period between `from_timestamp` and `to_timestamp` must not exceed 30 days.

    If no sag and clearance data is available for the entire line within the period, the endpoint
    returns `404 Not Found`.

    Args:
        line_id (UUID):
        from_timestamp (datetime.datetime):  Example: 2024-07-01 00:00:00+00:00.
        to_timestamp (datetime.datetime):  Example: 2024-07-02 00:00:00+00:00.
        unit_system (UnitSystem | Unset):
        x_region (GridInsightsV1LinesGetSagAndClearanceXRegion | Unset):  Default:
            GridInsightsV1LinesGetSagAndClearanceXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | GridInsightsV1LinesGetSagAndClearanceResponse200 | ProblemDetails
    """

    return sync_detailed(
        line_id=line_id,
        client=client,
        from_timestamp=from_timestamp,
        to_timestamp=to_timestamp,
        unit_system=unit_system,
        x_region=x_region,
    ).parsed


async def asyncio_detailed(
    line_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    from_timestamp: datetime.datetime,
    to_timestamp: datetime.datetime,
    unit_system: UnitSystem | Unset = UNSET,
    x_region: GridInsightsV1LinesGetSagAndClearanceXRegion | Unset = GridInsightsV1LinesGetSagAndClearanceXRegion.EU,
) -> Response[Any | GridInsightsV1LinesGetSagAndClearanceResponse200 | ProblemDetails]:
    """Get sag and clearance

     This endpoint returns sag and clearance data for the line within a specified time range.

    The sag and clearance data is divided into three sections:

    - **`max_sag`**: The span phase with the maximum sag across all span phases on the line over the
    requested period.
    - **`min_clearance`**: The span phase with the minimum clearance across all span phases on the line
    over the requested period. Null if no span phase has clearance data.
    - **`spans`**: Sag and clearance data grouped by span, with each span listing its span phases and
    their measurements over time.

    Each span phase entry provides the following data:
    - **`sag`**: The maximum vertical deflection of the conductor from the straight line between its two
    support points.
    - **`clearance`**: The vertical distance between the conductor and the ground or objects below.
    - **`timestamp`**: Time (UTC) when the sag and clearance measurements were calculated for the span
    phase. Timestamps may differ per conductor due to data availability.

    The period between `from_timestamp` and `to_timestamp` must not exceed 30 days.

    If no sag and clearance data is available for the entire line within the period, the endpoint
    returns `404 Not Found`.

    Args:
        line_id (UUID):
        from_timestamp (datetime.datetime):  Example: 2024-07-01 00:00:00+00:00.
        to_timestamp (datetime.datetime):  Example: 2024-07-02 00:00:00+00:00.
        unit_system (UnitSystem | Unset):
        x_region (GridInsightsV1LinesGetSagAndClearanceXRegion | Unset):  Default:
            GridInsightsV1LinesGetSagAndClearanceXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GridInsightsV1LinesGetSagAndClearanceResponse200 | ProblemDetails]
    """

    kwargs = _get_kwargs(
        line_id=line_id,
        from_timestamp=from_timestamp,
        to_timestamp=to_timestamp,
        unit_system=unit_system,
        x_region=x_region,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    line_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    from_timestamp: datetime.datetime,
    to_timestamp: datetime.datetime,
    unit_system: UnitSystem | Unset = UNSET,
    x_region: GridInsightsV1LinesGetSagAndClearanceXRegion | Unset = GridInsightsV1LinesGetSagAndClearanceXRegion.EU,
) -> Any | GridInsightsV1LinesGetSagAndClearanceResponse200 | ProblemDetails | None:
    """Get sag and clearance

     This endpoint returns sag and clearance data for the line within a specified time range.

    The sag and clearance data is divided into three sections:

    - **`max_sag`**: The span phase with the maximum sag across all span phases on the line over the
    requested period.
    - **`min_clearance`**: The span phase with the minimum clearance across all span phases on the line
    over the requested period. Null if no span phase has clearance data.
    - **`spans`**: Sag and clearance data grouped by span, with each span listing its span phases and
    their measurements over time.

    Each span phase entry provides the following data:
    - **`sag`**: The maximum vertical deflection of the conductor from the straight line between its two
    support points.
    - **`clearance`**: The vertical distance between the conductor and the ground or objects below.
    - **`timestamp`**: Time (UTC) when the sag and clearance measurements were calculated for the span
    phase. Timestamps may differ per conductor due to data availability.

    The period between `from_timestamp` and `to_timestamp` must not exceed 30 days.

    If no sag and clearance data is available for the entire line within the period, the endpoint
    returns `404 Not Found`.

    Args:
        line_id (UUID):
        from_timestamp (datetime.datetime):  Example: 2024-07-01 00:00:00+00:00.
        to_timestamp (datetime.datetime):  Example: 2024-07-02 00:00:00+00:00.
        unit_system (UnitSystem | Unset):
        x_region (GridInsightsV1LinesGetSagAndClearanceXRegion | Unset):  Default:
            GridInsightsV1LinesGetSagAndClearanceXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | GridInsightsV1LinesGetSagAndClearanceResponse200 | ProblemDetails
    """

    return (
        await asyncio_detailed(
            line_id=line_id,
            client=client,
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
            unit_system=unit_system,
            x_region=x_region,
        )
    ).parsed
