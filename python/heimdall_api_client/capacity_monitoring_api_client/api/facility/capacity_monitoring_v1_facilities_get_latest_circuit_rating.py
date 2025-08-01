from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.capacity_monitoring_v1_facilities_get_latest_circuit_rating_response_200 import CapacityMonitoringV1FacilitiesGetLatestCircuitRatingResponse200
from ...models.capacity_monitoring_v1_facilities_get_latest_circuit_rating_x_region import CapacityMonitoringV1FacilitiesGetLatestCircuitRatingXRegion
from ...models.problem_details import ProblemDetails
from ...types import Unset
from uuid import UUID



def _get_kwargs(
    facility_id: UUID,
    *,
    x_region: Union[Unset, CapacityMonitoringV1FacilitiesGetLatestCircuitRatingXRegion] = CapacityMonitoringV1FacilitiesGetLatestCircuitRatingXRegion.EU,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_region, Unset):
        headers["x-region"] = str(x_region)




    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/capacity_monitoring/v1/facilities/{facility_id}/circuit_ratings/latest".format(facility_id=facility_id,),
    }


    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Any, CapacityMonitoringV1FacilitiesGetLatestCircuitRatingResponse200, ProblemDetails]]:
    if response.status_code == 200:
        response_200 = CapacityMonitoringV1FacilitiesGetLatestCircuitRatingResponse200.from_dict(response.json())



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


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Any, CapacityMonitoringV1FacilitiesGetLatestCircuitRatingResponse200, ProblemDetails]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    facility_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    x_region: Union[Unset, CapacityMonitoringV1FacilitiesGetLatestCircuitRatingXRegion] = CapacityMonitoringV1FacilitiesGetLatestCircuitRatingXRegion.EU,

) -> Response[Union[Any, CapacityMonitoringV1FacilitiesGetLatestCircuitRatingResponse200, ProblemDetails]]:
    """ Get latest circuit rating

     This endpoint returns the most recent circuit rating for the facility.

    The circuit rating is defined as the lowest of:
      - Heimdall DLR
      - The facility's upper limit
      - The lowest steady-state rating among all facility components

    The upper limit can be either:
      - A fixed value
      - A percentage of the line's steady-state rating

    Note: The circuit rating is the only rating provided by the Heimdall Power API that is not a line
    rating.
      It reflects the facility's constraints and does not represent the capacity of the line itself. Use
    a line rating method to obtain that.

    Args:
        facility_id (UUID):
        x_region (Union[Unset, CapacityMonitoringV1FacilitiesGetLatestCircuitRatingXRegion]):
            Default: CapacityMonitoringV1FacilitiesGetLatestCircuitRatingXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CapacityMonitoringV1FacilitiesGetLatestCircuitRatingResponse200, ProblemDetails]]
     """


    kwargs = _get_kwargs(
        facility_id=facility_id,
x_region=x_region,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    facility_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    x_region: Union[Unset, CapacityMonitoringV1FacilitiesGetLatestCircuitRatingXRegion] = CapacityMonitoringV1FacilitiesGetLatestCircuitRatingXRegion.EU,

) -> Optional[Union[Any, CapacityMonitoringV1FacilitiesGetLatestCircuitRatingResponse200, ProblemDetails]]:
    """ Get latest circuit rating

     This endpoint returns the most recent circuit rating for the facility.

    The circuit rating is defined as the lowest of:
      - Heimdall DLR
      - The facility's upper limit
      - The lowest steady-state rating among all facility components

    The upper limit can be either:
      - A fixed value
      - A percentage of the line's steady-state rating

    Note: The circuit rating is the only rating provided by the Heimdall Power API that is not a line
    rating.
      It reflects the facility's constraints and does not represent the capacity of the line itself. Use
    a line rating method to obtain that.

    Args:
        facility_id (UUID):
        x_region (Union[Unset, CapacityMonitoringV1FacilitiesGetLatestCircuitRatingXRegion]):
            Default: CapacityMonitoringV1FacilitiesGetLatestCircuitRatingXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CapacityMonitoringV1FacilitiesGetLatestCircuitRatingResponse200, ProblemDetails]
     """


    return sync_detailed(
        facility_id=facility_id,
client=client,
x_region=x_region,

    ).parsed

async def asyncio_detailed(
    facility_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    x_region: Union[Unset, CapacityMonitoringV1FacilitiesGetLatestCircuitRatingXRegion] = CapacityMonitoringV1FacilitiesGetLatestCircuitRatingXRegion.EU,

) -> Response[Union[Any, CapacityMonitoringV1FacilitiesGetLatestCircuitRatingResponse200, ProblemDetails]]:
    """ Get latest circuit rating

     This endpoint returns the most recent circuit rating for the facility.

    The circuit rating is defined as the lowest of:
      - Heimdall DLR
      - The facility's upper limit
      - The lowest steady-state rating among all facility components

    The upper limit can be either:
      - A fixed value
      - A percentage of the line's steady-state rating

    Note: The circuit rating is the only rating provided by the Heimdall Power API that is not a line
    rating.
      It reflects the facility's constraints and does not represent the capacity of the line itself. Use
    a line rating method to obtain that.

    Args:
        facility_id (UUID):
        x_region (Union[Unset, CapacityMonitoringV1FacilitiesGetLatestCircuitRatingXRegion]):
            Default: CapacityMonitoringV1FacilitiesGetLatestCircuitRatingXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, CapacityMonitoringV1FacilitiesGetLatestCircuitRatingResponse200, ProblemDetails]]
     """


    kwargs = _get_kwargs(
        facility_id=facility_id,
x_region=x_region,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    facility_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    x_region: Union[Unset, CapacityMonitoringV1FacilitiesGetLatestCircuitRatingXRegion] = CapacityMonitoringV1FacilitiesGetLatestCircuitRatingXRegion.EU,

) -> Optional[Union[Any, CapacityMonitoringV1FacilitiesGetLatestCircuitRatingResponse200, ProblemDetails]]:
    """ Get latest circuit rating

     This endpoint returns the most recent circuit rating for the facility.

    The circuit rating is defined as the lowest of:
      - Heimdall DLR
      - The facility's upper limit
      - The lowest steady-state rating among all facility components

    The upper limit can be either:
      - A fixed value
      - A percentage of the line's steady-state rating

    Note: The circuit rating is the only rating provided by the Heimdall Power API that is not a line
    rating.
      It reflects the facility's constraints and does not represent the capacity of the line itself. Use
    a line rating method to obtain that.

    Args:
        facility_id (UUID):
        x_region (Union[Unset, CapacityMonitoringV1FacilitiesGetLatestCircuitRatingXRegion]):
            Default: CapacityMonitoringV1FacilitiesGetLatestCircuitRatingXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, CapacityMonitoringV1FacilitiesGetLatestCircuitRatingResponse200, ProblemDetails]
     """


    return (await asyncio_detailed(
        facility_id=facility_id,
client=client,
x_region=x_region,

    )).parsed
