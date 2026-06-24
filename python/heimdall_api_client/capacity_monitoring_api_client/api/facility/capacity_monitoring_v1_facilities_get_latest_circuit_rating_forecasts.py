from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.capacity_monitoring_v1_facilities_get_latest_circuit_rating_forecasts_response_200 import (
    CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsResponse200,
)
from ...models.capacity_monitoring_v1_facilities_get_latest_circuit_rating_forecasts_x_region import (
    CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsXRegion,
)
from ...models.problem_details import ProblemDetails
from ...models.quantity import Quantity
from ...types import UNSET, Response, Unset


def _get_kwargs(
    facility_id: UUID,
    *,
    quantity: Quantity | Unset = UNSET,
    x_region: CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsXRegion
    | Unset = CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsXRegion.EU,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_region, Unset):
        headers["x-region"] = str(x_region)

    params: dict[str, Any] = {}

    json_quantity: str | Unset = UNSET
    if not isinstance(quantity, Unset):
        json_quantity = quantity.value

    params["quantity"] = json_quantity

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/capacity_monitoring/v1/facilities/{facility_id}/circuit_ratings/forecasts".format(
            facility_id=quote(str(facility_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsResponse200 | ProblemDetails | None:
    if response.status_code == 200:
        response_200 = CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsResponse200.from_dict(
            response.json()
        )

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
) -> Response[Any | CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsResponse200 | ProblemDetails]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    facility_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    quantity: Quantity | Unset = UNSET,
    x_region: CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsXRegion
    | Unset = CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsXRegion.EU,
) -> Response[Any | CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsResponse200 | ProblemDetails]:
    r"""Get latest circuit rating forecasts

     This endpoint returns the most recent circuit rating forecasts for the facility.

    The forecasted hours returned by the endpoint are set to 72 hours, and are provided in 1-hour
    intervals.

    The response contains a series of buckets, each with a timestamp and predictions based on different
    values of confidence levels `p80`, `p90`, `p95` and `p99`.

    The circuit rating forecast is defined as the Heimdall DLR forecast limited by the facility
    component steady state ratings and the upper limit, similar to the real time
    circuit rating.

    To calculate the upper limit, we use the Steady State Line Ratings, as they also contain forecasted
    values.

    The upper limit can be either:
      - A fixed value
      - A percentage of the line's steady-state rating

    If the predictions contains no facility component id, then the dimensioning component is the line
    itself.

    ### Quantity
    Use the optional `quantity` query parameter to choose the quantity returned:
      - `current` (default) — circuit rating forecast in amperes (`unit: \"Ampere\"`).
      - `apparent_power` — circuit rating forecast converted to three-phase apparent power in MVA
    (`unit: \"MVA\"`) using `S = sqrt(3) * V * I / 1,000,000`.

    ### Voltage selection for `apparent_power`
    The line's **operational voltage** is used when it is set and positive; otherwise the **nominal
    voltage** is used.
    Both voltages are exposed on the facility in the `GET /assets/v1/assets` response so clients can
    verify which value the calculation would use.
    If neither voltage is usable, the response is `404`.

    Args:
        facility_id (UUID):
        quantity (Quantity | Unset): Which quantity to return from a rating endpoint:
              - `current` — value in amperes.
              - `apparent_power` — value converted to MVA using `S = sqrt(3) * V * I / 1,000,000`.
        x_region (CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsXRegion | Unset):
            Default: CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsResponse200 | ProblemDetails]
    """

    kwargs = _get_kwargs(
        facility_id=facility_id,
        quantity=quantity,
        x_region=x_region,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    facility_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    quantity: Quantity | Unset = UNSET,
    x_region: CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsXRegion
    | Unset = CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsXRegion.EU,
) -> Any | CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsResponse200 | ProblemDetails | None:
    r"""Get latest circuit rating forecasts

     This endpoint returns the most recent circuit rating forecasts for the facility.

    The forecasted hours returned by the endpoint are set to 72 hours, and are provided in 1-hour
    intervals.

    The response contains a series of buckets, each with a timestamp and predictions based on different
    values of confidence levels `p80`, `p90`, `p95` and `p99`.

    The circuit rating forecast is defined as the Heimdall DLR forecast limited by the facility
    component steady state ratings and the upper limit, similar to the real time
    circuit rating.

    To calculate the upper limit, we use the Steady State Line Ratings, as they also contain forecasted
    values.

    The upper limit can be either:
      - A fixed value
      - A percentage of the line's steady-state rating

    If the predictions contains no facility component id, then the dimensioning component is the line
    itself.

    ### Quantity
    Use the optional `quantity` query parameter to choose the quantity returned:
      - `current` (default) — circuit rating forecast in amperes (`unit: \"Ampere\"`).
      - `apparent_power` — circuit rating forecast converted to three-phase apparent power in MVA
    (`unit: \"MVA\"`) using `S = sqrt(3) * V * I / 1,000,000`.

    ### Voltage selection for `apparent_power`
    The line's **operational voltage** is used when it is set and positive; otherwise the **nominal
    voltage** is used.
    Both voltages are exposed on the facility in the `GET /assets/v1/assets` response so clients can
    verify which value the calculation would use.
    If neither voltage is usable, the response is `404`.

    Args:
        facility_id (UUID):
        quantity (Quantity | Unset): Which quantity to return from a rating endpoint:
              - `current` — value in amperes.
              - `apparent_power` — value converted to MVA using `S = sqrt(3) * V * I / 1,000,000`.
        x_region (CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsXRegion | Unset):
            Default: CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsResponse200 | ProblemDetails
    """

    return sync_detailed(
        facility_id=facility_id,
        client=client,
        quantity=quantity,
        x_region=x_region,
    ).parsed


async def asyncio_detailed(
    facility_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    quantity: Quantity | Unset = UNSET,
    x_region: CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsXRegion
    | Unset = CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsXRegion.EU,
) -> Response[Any | CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsResponse200 | ProblemDetails]:
    r"""Get latest circuit rating forecasts

     This endpoint returns the most recent circuit rating forecasts for the facility.

    The forecasted hours returned by the endpoint are set to 72 hours, and are provided in 1-hour
    intervals.

    The response contains a series of buckets, each with a timestamp and predictions based on different
    values of confidence levels `p80`, `p90`, `p95` and `p99`.

    The circuit rating forecast is defined as the Heimdall DLR forecast limited by the facility
    component steady state ratings and the upper limit, similar to the real time
    circuit rating.

    To calculate the upper limit, we use the Steady State Line Ratings, as they also contain forecasted
    values.

    The upper limit can be either:
      - A fixed value
      - A percentage of the line's steady-state rating

    If the predictions contains no facility component id, then the dimensioning component is the line
    itself.

    ### Quantity
    Use the optional `quantity` query parameter to choose the quantity returned:
      - `current` (default) — circuit rating forecast in amperes (`unit: \"Ampere\"`).
      - `apparent_power` — circuit rating forecast converted to three-phase apparent power in MVA
    (`unit: \"MVA\"`) using `S = sqrt(3) * V * I / 1,000,000`.

    ### Voltage selection for `apparent_power`
    The line's **operational voltage** is used when it is set and positive; otherwise the **nominal
    voltage** is used.
    Both voltages are exposed on the facility in the `GET /assets/v1/assets` response so clients can
    verify which value the calculation would use.
    If neither voltage is usable, the response is `404`.

    Args:
        facility_id (UUID):
        quantity (Quantity | Unset): Which quantity to return from a rating endpoint:
              - `current` — value in amperes.
              - `apparent_power` — value converted to MVA using `S = sqrt(3) * V * I / 1,000,000`.
        x_region (CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsXRegion | Unset):
            Default: CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsResponse200 | ProblemDetails]
    """

    kwargs = _get_kwargs(
        facility_id=facility_id,
        quantity=quantity,
        x_region=x_region,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    facility_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    quantity: Quantity | Unset = UNSET,
    x_region: CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsXRegion
    | Unset = CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsXRegion.EU,
) -> Any | CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsResponse200 | ProblemDetails | None:
    r"""Get latest circuit rating forecasts

     This endpoint returns the most recent circuit rating forecasts for the facility.

    The forecasted hours returned by the endpoint are set to 72 hours, and are provided in 1-hour
    intervals.

    The response contains a series of buckets, each with a timestamp and predictions based on different
    values of confidence levels `p80`, `p90`, `p95` and `p99`.

    The circuit rating forecast is defined as the Heimdall DLR forecast limited by the facility
    component steady state ratings and the upper limit, similar to the real time
    circuit rating.

    To calculate the upper limit, we use the Steady State Line Ratings, as they also contain forecasted
    values.

    The upper limit can be either:
      - A fixed value
      - A percentage of the line's steady-state rating

    If the predictions contains no facility component id, then the dimensioning component is the line
    itself.

    ### Quantity
    Use the optional `quantity` query parameter to choose the quantity returned:
      - `current` (default) — circuit rating forecast in amperes (`unit: \"Ampere\"`).
      - `apparent_power` — circuit rating forecast converted to three-phase apparent power in MVA
    (`unit: \"MVA\"`) using `S = sqrt(3) * V * I / 1,000,000`.

    ### Voltage selection for `apparent_power`
    The line's **operational voltage** is used when it is set and positive; otherwise the **nominal
    voltage** is used.
    Both voltages are exposed on the facility in the `GET /assets/v1/assets` response so clients can
    verify which value the calculation would use.
    If neither voltage is usable, the response is `404`.

    Args:
        facility_id (UUID):
        quantity (Quantity | Unset): Which quantity to return from a rating endpoint:
              - `current` — value in amperes.
              - `apparent_power` — value converted to MVA using `S = sqrt(3) * V * I / 1,000,000`.
        x_region (CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsXRegion | Unset):
            Default: CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CapacityMonitoringV1FacilitiesGetLatestCircuitRatingForecastsResponse200 | ProblemDetails
    """

    return (
        await asyncio_detailed(
            facility_id=facility_id,
            client=client,
            quantity=quantity,
            x_region=x_region,
        )
    ).parsed
