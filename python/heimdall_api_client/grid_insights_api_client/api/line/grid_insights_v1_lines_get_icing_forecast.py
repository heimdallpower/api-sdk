from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.grid_insights_v1_lines_get_icing_forecast_response_200 import (
    GridInsightsV1LinesGetIcingForecastResponse200,
)
from ...models.grid_insights_v1_lines_get_icing_forecast_x_region import GridInsightsV1LinesGetIcingForecastXRegion
from ...models.problem_details import ProblemDetails
from ...models.unit_system import UnitSystem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    line_id: UUID,
    *,
    unit_system: UnitSystem | Unset = UNSET,
    x_region: GridInsightsV1LinesGetIcingForecastXRegion | Unset = GridInsightsV1LinesGetIcingForecastXRegion.EU,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_region, Unset):
        headers["x-region"] = str(x_region)

    params: dict[str, Any] = {}

    json_unit_system: str | Unset = UNSET
    if not isinstance(unit_system, Unset):
        json_unit_system = unit_system.value

    params["unit_system"] = json_unit_system

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/grid_insights/v1/lines/{line_id}/icing/forecast".format(
            line_id=quote(str(line_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | GridInsightsV1LinesGetIcingForecastResponse200 | ProblemDetails | None:
    if response.status_code == 200:
        response_200 = GridInsightsV1LinesGetIcingForecastResponse200.from_dict(response.json())

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
) -> Response[Any | GridInsightsV1LinesGetIcingForecastResponse200 | ProblemDetails]:
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
    unit_system: UnitSystem | Unset = UNSET,
    x_region: GridInsightsV1LinesGetIcingForecastXRegion | Unset = GridInsightsV1LinesGetIcingForecastXRegion.EU,
) -> Response[Any | GridInsightsV1LinesGetIcingForecastResponse200 | ProblemDetails]:
    """Get icing forecast

     This endpoint returns the icing forecast for the line.

    The forecast covers 72 hours in 30-minute intervals.

    The icing data is divided into two sections:

    - **`max`**: The peak forecasted ice weight across all span phases and all forecast time points,
    with the associated span phase and timestamp.
    - **`spans`**: Forecast data grouped by span, with each span listing its span phases and their full
    forecast time series.

    Each forecast data point provides the following data:
    - **`ice_weight`**: The forecasted mass of ice accumulated on the conductor.
    - **`timestamp`**: The forecasted time (UTC) for that data point.

    The forecast uses the latest measured current for the line. If no current measurement is available
    within 20 minutes of the request, the endpoint returns `404 Not Found`.

    If no icing data is available for the line, the endpoint returns `404 Not Found`.

    Args:
        line_id (UUID):
        unit_system (UnitSystem | Unset):
        x_region (GridInsightsV1LinesGetIcingForecastXRegion | Unset):  Default:
            GridInsightsV1LinesGetIcingForecastXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GridInsightsV1LinesGetIcingForecastResponse200 | ProblemDetails]
    """

    kwargs = _get_kwargs(
        line_id=line_id,
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
    unit_system: UnitSystem | Unset = UNSET,
    x_region: GridInsightsV1LinesGetIcingForecastXRegion | Unset = GridInsightsV1LinesGetIcingForecastXRegion.EU,
) -> Any | GridInsightsV1LinesGetIcingForecastResponse200 | ProblemDetails | None:
    """Get icing forecast

     This endpoint returns the icing forecast for the line.

    The forecast covers 72 hours in 30-minute intervals.

    The icing data is divided into two sections:

    - **`max`**: The peak forecasted ice weight across all span phases and all forecast time points,
    with the associated span phase and timestamp.
    - **`spans`**: Forecast data grouped by span, with each span listing its span phases and their full
    forecast time series.

    Each forecast data point provides the following data:
    - **`ice_weight`**: The forecasted mass of ice accumulated on the conductor.
    - **`timestamp`**: The forecasted time (UTC) for that data point.

    The forecast uses the latest measured current for the line. If no current measurement is available
    within 20 minutes of the request, the endpoint returns `404 Not Found`.

    If no icing data is available for the line, the endpoint returns `404 Not Found`.

    Args:
        line_id (UUID):
        unit_system (UnitSystem | Unset):
        x_region (GridInsightsV1LinesGetIcingForecastXRegion | Unset):  Default:
            GridInsightsV1LinesGetIcingForecastXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | GridInsightsV1LinesGetIcingForecastResponse200 | ProblemDetails
    """

    return sync_detailed(
        line_id=line_id,
        client=client,
        unit_system=unit_system,
        x_region=x_region,
    ).parsed


async def asyncio_detailed(
    line_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    unit_system: UnitSystem | Unset = UNSET,
    x_region: GridInsightsV1LinesGetIcingForecastXRegion | Unset = GridInsightsV1LinesGetIcingForecastXRegion.EU,
) -> Response[Any | GridInsightsV1LinesGetIcingForecastResponse200 | ProblemDetails]:
    """Get icing forecast

     This endpoint returns the icing forecast for the line.

    The forecast covers 72 hours in 30-minute intervals.

    The icing data is divided into two sections:

    - **`max`**: The peak forecasted ice weight across all span phases and all forecast time points,
    with the associated span phase and timestamp.
    - **`spans`**: Forecast data grouped by span, with each span listing its span phases and their full
    forecast time series.

    Each forecast data point provides the following data:
    - **`ice_weight`**: The forecasted mass of ice accumulated on the conductor.
    - **`timestamp`**: The forecasted time (UTC) for that data point.

    The forecast uses the latest measured current for the line. If no current measurement is available
    within 20 minutes of the request, the endpoint returns `404 Not Found`.

    If no icing data is available for the line, the endpoint returns `404 Not Found`.

    Args:
        line_id (UUID):
        unit_system (UnitSystem | Unset):
        x_region (GridInsightsV1LinesGetIcingForecastXRegion | Unset):  Default:
            GridInsightsV1LinesGetIcingForecastXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | GridInsightsV1LinesGetIcingForecastResponse200 | ProblemDetails]
    """

    kwargs = _get_kwargs(
        line_id=line_id,
        unit_system=unit_system,
        x_region=x_region,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    line_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    unit_system: UnitSystem | Unset = UNSET,
    x_region: GridInsightsV1LinesGetIcingForecastXRegion | Unset = GridInsightsV1LinesGetIcingForecastXRegion.EU,
) -> Any | GridInsightsV1LinesGetIcingForecastResponse200 | ProblemDetails | None:
    """Get icing forecast

     This endpoint returns the icing forecast for the line.

    The forecast covers 72 hours in 30-minute intervals.

    The icing data is divided into two sections:

    - **`max`**: The peak forecasted ice weight across all span phases and all forecast time points,
    with the associated span phase and timestamp.
    - **`spans`**: Forecast data grouped by span, with each span listing its span phases and their full
    forecast time series.

    Each forecast data point provides the following data:
    - **`ice_weight`**: The forecasted mass of ice accumulated on the conductor.
    - **`timestamp`**: The forecasted time (UTC) for that data point.

    The forecast uses the latest measured current for the line. If no current measurement is available
    within 20 minutes of the request, the endpoint returns `404 Not Found`.

    If no icing data is available for the line, the endpoint returns `404 Not Found`.

    Args:
        line_id (UUID):
        unit_system (UnitSystem | Unset):
        x_region (GridInsightsV1LinesGetIcingForecastXRegion | Unset):  Default:
            GridInsightsV1LinesGetIcingForecastXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | GridInsightsV1LinesGetIcingForecastResponse200 | ProblemDetails
    """

    return (
        await asyncio_detailed(
            line_id=line_id,
            client=client,
            unit_system=unit_system,
            x_region=x_region,
        )
    ).parsed
