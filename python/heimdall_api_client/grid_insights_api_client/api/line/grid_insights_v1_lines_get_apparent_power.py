import datetime
from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.grid_insights_v1_lines_get_apparent_power_response_200 import (
    GridInsightsV1LinesGetApparentPowerResponse200,
)
from ...models.grid_insights_v1_lines_get_apparent_power_x_region import GridInsightsV1LinesGetApparentPowerXRegion
from ...models.problem_details import ProblemDetails
from ...types import UNSET, Response, Unset


def _get_kwargs(
    line_id: UUID,
    *,
    from_timestamp: datetime.datetime,
    to_timestamp: datetime.datetime,
    x_region: GridInsightsV1LinesGetApparentPowerXRegion | Unset = GridInsightsV1LinesGetApparentPowerXRegion.EU,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_region, Unset):
        headers["x-region"] = str(x_region)

    params: dict[str, Any] = {}

    json_from_timestamp = from_timestamp.isoformat()
    params["from_timestamp"] = json_from_timestamp

    json_to_timestamp = to_timestamp.isoformat()
    params["to_timestamp"] = json_to_timestamp

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/grid_insights/v1/lines/{line_id}/apparent_power".format(
            line_id=quote(str(line_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | GridInsightsV1LinesGetApparentPowerResponse200 | ProblemDetails | None:
    if response.status_code == 200:
        response_200 = GridInsightsV1LinesGetApparentPowerResponse200.from_dict(response.json())

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
) -> Response[Any | GridInsightsV1LinesGetApparentPowerResponse200 | ProblemDetails]:
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
    x_region: GridInsightsV1LinesGetApparentPowerXRegion | Unset = GridInsightsV1LinesGetApparentPowerXRegion.EU,
) -> Response[Any | GridInsightsV1LinesGetApparentPowerResponse200 | ProblemDetails]:
    """Get apparent power

     This endpoint returns apparent power for the line within a specified time range.

    Apparent power is derived from the line's current and its voltage, and is reported in megavolt-
    amperes (MVA), calculated as `S = sqrt(3) * V * I / 1,000,000`.

    The line's operational voltage is used when configured and positive; otherwise the nominal voltage
    is used.

    The period between `from_timestamp` and `to_timestamp` must not exceed 30 days.

    Args:
        line_id (UUID):
        from_timestamp (datetime.datetime):  Example: 2024-07-01 00:00:00+00:00.
        to_timestamp (datetime.datetime):  Example: 2024-07-02 00:00:00+00:00.
        x_region (GridInsightsV1LinesGetApparentPowerXRegion | Unset):  Default:
            GridInsightsV1LinesGetApparentPowerXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GridInsightsV1LinesGetApparentPowerResponse200 | ProblemDetails]
    """

    kwargs = _get_kwargs(
        line_id=line_id,
        from_timestamp=from_timestamp,
        to_timestamp=to_timestamp,
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
    x_region: GridInsightsV1LinesGetApparentPowerXRegion | Unset = GridInsightsV1LinesGetApparentPowerXRegion.EU,
) -> Any | GridInsightsV1LinesGetApparentPowerResponse200 | ProblemDetails | None:
    """Get apparent power

     This endpoint returns apparent power for the line within a specified time range.

    Apparent power is derived from the line's current and its voltage, and is reported in megavolt-
    amperes (MVA), calculated as `S = sqrt(3) * V * I / 1,000,000`.

    The line's operational voltage is used when configured and positive; otherwise the nominal voltage
    is used.

    The period between `from_timestamp` and `to_timestamp` must not exceed 30 days.

    Args:
        line_id (UUID):
        from_timestamp (datetime.datetime):  Example: 2024-07-01 00:00:00+00:00.
        to_timestamp (datetime.datetime):  Example: 2024-07-02 00:00:00+00:00.
        x_region (GridInsightsV1LinesGetApparentPowerXRegion | Unset):  Default:
            GridInsightsV1LinesGetApparentPowerXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | GridInsightsV1LinesGetApparentPowerResponse200 | ProblemDetails
    """

    return sync_detailed(
        line_id=line_id,
        client=client,
        from_timestamp=from_timestamp,
        to_timestamp=to_timestamp,
        x_region=x_region,
    ).parsed


async def asyncio_detailed(
    line_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    from_timestamp: datetime.datetime,
    to_timestamp: datetime.datetime,
    x_region: GridInsightsV1LinesGetApparentPowerXRegion | Unset = GridInsightsV1LinesGetApparentPowerXRegion.EU,
) -> Response[Any | GridInsightsV1LinesGetApparentPowerResponse200 | ProblemDetails]:
    """Get apparent power

     This endpoint returns apparent power for the line within a specified time range.

    Apparent power is derived from the line's current and its voltage, and is reported in megavolt-
    amperes (MVA), calculated as `S = sqrt(3) * V * I / 1,000,000`.

    The line's operational voltage is used when configured and positive; otherwise the nominal voltage
    is used.

    The period between `from_timestamp` and `to_timestamp` must not exceed 30 days.

    Args:
        line_id (UUID):
        from_timestamp (datetime.datetime):  Example: 2024-07-01 00:00:00+00:00.
        to_timestamp (datetime.datetime):  Example: 2024-07-02 00:00:00+00:00.
        x_region (GridInsightsV1LinesGetApparentPowerXRegion | Unset):  Default:
            GridInsightsV1LinesGetApparentPowerXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GridInsightsV1LinesGetApparentPowerResponse200 | ProblemDetails]
    """

    kwargs = _get_kwargs(
        line_id=line_id,
        from_timestamp=from_timestamp,
        to_timestamp=to_timestamp,
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
    x_region: GridInsightsV1LinesGetApparentPowerXRegion | Unset = GridInsightsV1LinesGetApparentPowerXRegion.EU,
) -> Any | GridInsightsV1LinesGetApparentPowerResponse200 | ProblemDetails | None:
    """Get apparent power

     This endpoint returns apparent power for the line within a specified time range.

    Apparent power is derived from the line's current and its voltage, and is reported in megavolt-
    amperes (MVA), calculated as `S = sqrt(3) * V * I / 1,000,000`.

    The line's operational voltage is used when configured and positive; otherwise the nominal voltage
    is used.

    The period between `from_timestamp` and `to_timestamp` must not exceed 30 days.

    Args:
        line_id (UUID):
        from_timestamp (datetime.datetime):  Example: 2024-07-01 00:00:00+00:00.
        to_timestamp (datetime.datetime):  Example: 2024-07-02 00:00:00+00:00.
        x_region (GridInsightsV1LinesGetApparentPowerXRegion | Unset):  Default:
            GridInsightsV1LinesGetApparentPowerXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | GridInsightsV1LinesGetApparentPowerResponse200 | ProblemDetails
    """

    return (
        await asyncio_detailed(
            line_id=line_id,
            client=client,
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
            x_region=x_region,
        )
    ).parsed
