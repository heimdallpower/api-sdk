from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.grid_insights_v1_lines_get_latest_apparent_power_response_200 import (
    GridInsightsV1LinesGetLatestApparentPowerResponse200,
)
from ...models.grid_insights_v1_lines_get_latest_apparent_power_x_region import (
    GridInsightsV1LinesGetLatestApparentPowerXRegion,
)
from ...models.problem_details import ProblemDetails
from ...types import Response, Unset


def _get_kwargs(
    line_id: UUID,
    *,
    x_region: GridInsightsV1LinesGetLatestApparentPowerXRegion
    | Unset = GridInsightsV1LinesGetLatestApparentPowerXRegion.EU,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_region, Unset):
        headers["x-region"] = str(x_region)

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/grid_insights/v1/lines/{line_id}/apparent_power/latest".format(
            line_id=quote(str(line_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | GridInsightsV1LinesGetLatestApparentPowerResponse200 | ProblemDetails | None:
    if response.status_code == 200:
        response_200 = GridInsightsV1LinesGetLatestApparentPowerResponse200.from_dict(response.json())

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
) -> Response[Any | GridInsightsV1LinesGetLatestApparentPowerResponse200 | ProblemDetails]:
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
    x_region: GridInsightsV1LinesGetLatestApparentPowerXRegion
    | Unset = GridInsightsV1LinesGetLatestApparentPowerXRegion.EU,
) -> Response[Any | GridInsightsV1LinesGetLatestApparentPowerResponse200 | ProblemDetails]:
    """Get latest apparent power

     This endpoint returns the most recent apparent power for the line.

    Apparent power is derived from the line's latest current and its voltage, and is reported in
    megavolt-amperes (MVA), calculated as `S = sqrt(3) * V * I / 1,000,000`.

    The line's operational voltage is used when configured and positive; otherwise the nominal voltage
    is used.

    Args:
        line_id (UUID):
        x_region (GridInsightsV1LinesGetLatestApparentPowerXRegion | Unset):  Default:
            GridInsightsV1LinesGetLatestApparentPowerXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GridInsightsV1LinesGetLatestApparentPowerResponse200 | ProblemDetails]
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
    x_region: GridInsightsV1LinesGetLatestApparentPowerXRegion
    | Unset = GridInsightsV1LinesGetLatestApparentPowerXRegion.EU,
) -> Any | GridInsightsV1LinesGetLatestApparentPowerResponse200 | ProblemDetails | None:
    """Get latest apparent power

     This endpoint returns the most recent apparent power for the line.

    Apparent power is derived from the line's latest current and its voltage, and is reported in
    megavolt-amperes (MVA), calculated as `S = sqrt(3) * V * I / 1,000,000`.

    The line's operational voltage is used when configured and positive; otherwise the nominal voltage
    is used.

    Args:
        line_id (UUID):
        x_region (GridInsightsV1LinesGetLatestApparentPowerXRegion | Unset):  Default:
            GridInsightsV1LinesGetLatestApparentPowerXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | GridInsightsV1LinesGetLatestApparentPowerResponse200 | ProblemDetails
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
    x_region: GridInsightsV1LinesGetLatestApparentPowerXRegion
    | Unset = GridInsightsV1LinesGetLatestApparentPowerXRegion.EU,
) -> Response[Any | GridInsightsV1LinesGetLatestApparentPowerResponse200 | ProblemDetails]:
    """Get latest apparent power

     This endpoint returns the most recent apparent power for the line.

    Apparent power is derived from the line's latest current and its voltage, and is reported in
    megavolt-amperes (MVA), calculated as `S = sqrt(3) * V * I / 1,000,000`.

    The line's operational voltage is used when configured and positive; otherwise the nominal voltage
    is used.

    Args:
        line_id (UUID):
        x_region (GridInsightsV1LinesGetLatestApparentPowerXRegion | Unset):  Default:
            GridInsightsV1LinesGetLatestApparentPowerXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GridInsightsV1LinesGetLatestApparentPowerResponse200 | ProblemDetails]
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
    client: AuthenticatedClient | Client,
    x_region: GridInsightsV1LinesGetLatestApparentPowerXRegion
    | Unset = GridInsightsV1LinesGetLatestApparentPowerXRegion.EU,
) -> Any | GridInsightsV1LinesGetLatestApparentPowerResponse200 | ProblemDetails | None:
    """Get latest apparent power

     This endpoint returns the most recent apparent power for the line.

    Apparent power is derived from the line's latest current and its voltage, and is reported in
    megavolt-amperes (MVA), calculated as `S = sqrt(3) * V * I / 1,000,000`.

    The line's operational voltage is used when configured and positive; otherwise the nominal voltage
    is used.

    Args:
        line_id (UUID):
        x_region (GridInsightsV1LinesGetLatestApparentPowerXRegion | Unset):  Default:
            GridInsightsV1LinesGetLatestApparentPowerXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | GridInsightsV1LinesGetLatestApparentPowerResponse200 | ProblemDetails
    """

    return (
        await asyncio_detailed(
            line_id=line_id,
            client=client,
            x_region=x_region,
        )
    ).parsed
