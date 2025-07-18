from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.grid_insights_v1_lines_get_latest_conductor_temperature_response_200 import GridInsightsV1LinesGetLatestConductorTemperatureResponse200
from ...models.grid_insights_v1_lines_get_latest_conductor_temperature_x_region import GridInsightsV1LinesGetLatestConductorTemperatureXRegion
from ...models.problem_details import ProblemDetails
from ...models.unit_system import UnitSystem
from ...types import Unset
from uuid import UUID



def _get_kwargs(
    line_id: UUID,
    *,
    unit_system: Union[Unset, UnitSystem] = UNSET,
    x_region: Union[Unset, GridInsightsV1LinesGetLatestConductorTemperatureXRegion] = GridInsightsV1LinesGetLatestConductorTemperatureXRegion.EU,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_region, Unset):
        headers["x-region"] = str(x_region)




    

    params: dict[str, Any] = {}

    json_unit_system: Union[Unset, str] = UNSET
    if not isinstance(unit_system, Unset):
        json_unit_system = unit_system.value

    params["unit_system"] = json_unit_system


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/grid_insights/v1/lines/{line_id}/conductor_temperatures/latest".format(line_id=line_id,),
        "params": params,
    }


    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Any, GridInsightsV1LinesGetLatestConductorTemperatureResponse200, ProblemDetails]]:
    if response.status_code == 200:
        response_200 = GridInsightsV1LinesGetLatestConductorTemperatureResponse200.from_dict(response.json())



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


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Any, GridInsightsV1LinesGetLatestConductorTemperatureResponse200, ProblemDetails]]:
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
    unit_system: Union[Unset, UnitSystem] = UNSET,
    x_region: Union[Unset, GridInsightsV1LinesGetLatestConductorTemperatureXRegion] = GridInsightsV1LinesGetLatestConductorTemperatureXRegion.EU,

) -> Response[Union[Any, GridInsightsV1LinesGetLatestConductorTemperatureResponse200, ProblemDetails]]:
    """ Get latest conductor temperature

     This endpoint returns the most recent conductor temperature for the line.

    Conductor temperature is defined as the maximum and minimum temperature measured on the line at a
    given timestamp.

    The conductor temperature is aggregated across the entire line using a 5-minute sliding window,
    where the maximum and minimum values are calculated for each window.

    Args:
        line_id (UUID):
        unit_system (Union[Unset, UnitSystem]):
        x_region (Union[Unset, GridInsightsV1LinesGetLatestConductorTemperatureXRegion]):
            Default: GridInsightsV1LinesGetLatestConductorTemperatureXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GridInsightsV1LinesGetLatestConductorTemperatureResponse200, ProblemDetails]]
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
    client: Union[AuthenticatedClient, Client],
    unit_system: Union[Unset, UnitSystem] = UNSET,
    x_region: Union[Unset, GridInsightsV1LinesGetLatestConductorTemperatureXRegion] = GridInsightsV1LinesGetLatestConductorTemperatureXRegion.EU,

) -> Optional[Union[Any, GridInsightsV1LinesGetLatestConductorTemperatureResponse200, ProblemDetails]]:
    """ Get latest conductor temperature

     This endpoint returns the most recent conductor temperature for the line.

    Conductor temperature is defined as the maximum and minimum temperature measured on the line at a
    given timestamp.

    The conductor temperature is aggregated across the entire line using a 5-minute sliding window,
    where the maximum and minimum values are calculated for each window.

    Args:
        line_id (UUID):
        unit_system (Union[Unset, UnitSystem]):
        x_region (Union[Unset, GridInsightsV1LinesGetLatestConductorTemperatureXRegion]):
            Default: GridInsightsV1LinesGetLatestConductorTemperatureXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GridInsightsV1LinesGetLatestConductorTemperatureResponse200, ProblemDetails]
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
    client: Union[AuthenticatedClient, Client],
    unit_system: Union[Unset, UnitSystem] = UNSET,
    x_region: Union[Unset, GridInsightsV1LinesGetLatestConductorTemperatureXRegion] = GridInsightsV1LinesGetLatestConductorTemperatureXRegion.EU,

) -> Response[Union[Any, GridInsightsV1LinesGetLatestConductorTemperatureResponse200, ProblemDetails]]:
    """ Get latest conductor temperature

     This endpoint returns the most recent conductor temperature for the line.

    Conductor temperature is defined as the maximum and minimum temperature measured on the line at a
    given timestamp.

    The conductor temperature is aggregated across the entire line using a 5-minute sliding window,
    where the maximum and minimum values are calculated for each window.

    Args:
        line_id (UUID):
        unit_system (Union[Unset, UnitSystem]):
        x_region (Union[Unset, GridInsightsV1LinesGetLatestConductorTemperatureXRegion]):
            Default: GridInsightsV1LinesGetLatestConductorTemperatureXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, GridInsightsV1LinesGetLatestConductorTemperatureResponse200, ProblemDetails]]
     """


    kwargs = _get_kwargs(
        line_id=line_id,
unit_system=unit_system,
x_region=x_region,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    line_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    unit_system: Union[Unset, UnitSystem] = UNSET,
    x_region: Union[Unset, GridInsightsV1LinesGetLatestConductorTemperatureXRegion] = GridInsightsV1LinesGetLatestConductorTemperatureXRegion.EU,

) -> Optional[Union[Any, GridInsightsV1LinesGetLatestConductorTemperatureResponse200, ProblemDetails]]:
    """ Get latest conductor temperature

     This endpoint returns the most recent conductor temperature for the line.

    Conductor temperature is defined as the maximum and minimum temperature measured on the line at a
    given timestamp.

    The conductor temperature is aggregated across the entire line using a 5-minute sliding window,
    where the maximum and minimum values are calculated for each window.

    Args:
        line_id (UUID):
        unit_system (Union[Unset, UnitSystem]):
        x_region (Union[Unset, GridInsightsV1LinesGetLatestConductorTemperatureXRegion]):
            Default: GridInsightsV1LinesGetLatestConductorTemperatureXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, GridInsightsV1LinesGetLatestConductorTemperatureResponse200, ProblemDetails]
     """


    return (await asyncio_detailed(
        line_id=line_id,
client=client,
unit_system=unit_system,
x_region=x_region,

    )).parsed
