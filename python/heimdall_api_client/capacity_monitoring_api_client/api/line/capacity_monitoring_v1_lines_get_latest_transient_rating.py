import datetime
from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.capacity_monitoring_v1_lines_get_latest_transient_rating_response_200 import (
    CapacityMonitoringV1LinesGetLatestTransientRatingResponse200,
)
from ...models.capacity_monitoring_v1_lines_get_latest_transient_rating_x_region import (
    CapacityMonitoringV1LinesGetLatestTransientRatingXRegion,
)
from ...models.problem_details import ProblemDetails
from ...models.quantity import Quantity
from ...types import UNSET, Response, Unset


def _get_kwargs(
    line_id: UUID,
    *,
    quantity: Quantity | Unset = UNSET,
    since: datetime.datetime | Unset = UNSET,
    x_region: CapacityMonitoringV1LinesGetLatestTransientRatingXRegion
    | Unset = CapacityMonitoringV1LinesGetLatestTransientRatingXRegion.EU,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_region, Unset):
        headers["x-region"] = str(x_region)

    params: dict[str, Any] = {}

    json_quantity: str | Unset = UNSET
    if not isinstance(quantity, Unset):
        json_quantity = quantity.value

    params["quantity"] = json_quantity

    json_since: str | Unset = UNSET
    if not isinstance(since, Unset):
        json_since = since.isoformat()
    params["since"] = json_since

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/capacity_monitoring/v1/lines/{line_id}/transient_ratings/latest".format(
            line_id=quote(str(line_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | CapacityMonitoringV1LinesGetLatestTransientRatingResponse200 | ProblemDetails | None:
    if response.status_code == 200:
        response_200 = CapacityMonitoringV1LinesGetLatestTransientRatingResponse200.from_dict(response.json())

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
) -> Response[Any | CapacityMonitoringV1LinesGetLatestTransientRatingResponse200 | ProblemDetails]:
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
    quantity: Quantity | Unset = UNSET,
    since: datetime.datetime | Unset = UNSET,
    x_region: CapacityMonitoringV1LinesGetLatestTransientRatingXRegion
    | Unset = CapacityMonitoringV1LinesGetLatestTransientRatingXRegion.EU,
) -> Response[Any | CapacityMonitoringV1LinesGetLatestTransientRatingResponse200 | ProblemDetails]:
    r"""Get latest line transient rating

     This endpoint returns the most recent line transient rating for the line: the short-duration
    overload ampacity the line can sustain for each calculated duration.

    A transient rating is a set of per-duration values calculated at a single point in time. The
    response
    contains one `timestamp` and a `ratings` array with one entry per calculated duration (for example
    5, 10 or 15 minutes), and every calculated duration is returned. Transient ratings are calculated
    for
    the configured durations of one hour or shorter, so a configured duration longer than one hour is
    not
    calculated and is absent from the response.

    This endpoint returns real-time data and can be polled at short intervals (for example every 3–5
    minutes) for operational monitoring.

    ### Quantity
    Use the optional `quantity` query parameter to choose the quantity returned:
      - `current` (default) — line transient rating in amperes (`unit: \"Ampere\"`).
      - `apparent_power` — line transient rating converted to three-phase apparent power in MVA (`unit:
    \"MVA\"`) using `S = sqrt(3) * V * I / 1,000,000`.

    ### Voltage selection for `apparent_power`
    The line's **operational voltage** is used when it is set and positive; otherwise the **nominal
    voltage** is used.
    Both voltages are exposed on the facility in the `GET /assets/v1/assets` response so clients can
    verify which value the calculation would use.
    If neither voltage is usable, the response is `404`.

    Args:
        line_id (UUID):
        quantity (Quantity | Unset): Which quantity to return from a rating endpoint:
              - `current` — value in amperes.
              - `apparent_power` — value converted to MVA using `S = sqrt(3) * V * I / 1,000,000`.
        since (datetime.datetime | Unset):  Example: 2024-07-01 12:00:00.001000+00:00.
        x_region (CapacityMonitoringV1LinesGetLatestTransientRatingXRegion | Unset):  Default:
            CapacityMonitoringV1LinesGetLatestTransientRatingXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CapacityMonitoringV1LinesGetLatestTransientRatingResponse200 | ProblemDetails]
    """

    kwargs = _get_kwargs(
        line_id=line_id,
        quantity=quantity,
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
    quantity: Quantity | Unset = UNSET,
    since: datetime.datetime | Unset = UNSET,
    x_region: CapacityMonitoringV1LinesGetLatestTransientRatingXRegion
    | Unset = CapacityMonitoringV1LinesGetLatestTransientRatingXRegion.EU,
) -> Any | CapacityMonitoringV1LinesGetLatestTransientRatingResponse200 | ProblemDetails | None:
    r"""Get latest line transient rating

     This endpoint returns the most recent line transient rating for the line: the short-duration
    overload ampacity the line can sustain for each calculated duration.

    A transient rating is a set of per-duration values calculated at a single point in time. The
    response
    contains one `timestamp` and a `ratings` array with one entry per calculated duration (for example
    5, 10 or 15 minutes), and every calculated duration is returned. Transient ratings are calculated
    for
    the configured durations of one hour or shorter, so a configured duration longer than one hour is
    not
    calculated and is absent from the response.

    This endpoint returns real-time data and can be polled at short intervals (for example every 3–5
    minutes) for operational monitoring.

    ### Quantity
    Use the optional `quantity` query parameter to choose the quantity returned:
      - `current` (default) — line transient rating in amperes (`unit: \"Ampere\"`).
      - `apparent_power` — line transient rating converted to three-phase apparent power in MVA (`unit:
    \"MVA\"`) using `S = sqrt(3) * V * I / 1,000,000`.

    ### Voltage selection for `apparent_power`
    The line's **operational voltage** is used when it is set and positive; otherwise the **nominal
    voltage** is used.
    Both voltages are exposed on the facility in the `GET /assets/v1/assets` response so clients can
    verify which value the calculation would use.
    If neither voltage is usable, the response is `404`.

    Args:
        line_id (UUID):
        quantity (Quantity | Unset): Which quantity to return from a rating endpoint:
              - `current` — value in amperes.
              - `apparent_power` — value converted to MVA using `S = sqrt(3) * V * I / 1,000,000`.
        since (datetime.datetime | Unset):  Example: 2024-07-01 12:00:00.001000+00:00.
        x_region (CapacityMonitoringV1LinesGetLatestTransientRatingXRegion | Unset):  Default:
            CapacityMonitoringV1LinesGetLatestTransientRatingXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CapacityMonitoringV1LinesGetLatestTransientRatingResponse200 | ProblemDetails
    """

    return sync_detailed(
        line_id=line_id,
        client=client,
        quantity=quantity,
        since=since,
        x_region=x_region,
    ).parsed


async def asyncio_detailed(
    line_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    quantity: Quantity | Unset = UNSET,
    since: datetime.datetime | Unset = UNSET,
    x_region: CapacityMonitoringV1LinesGetLatestTransientRatingXRegion
    | Unset = CapacityMonitoringV1LinesGetLatestTransientRatingXRegion.EU,
) -> Response[Any | CapacityMonitoringV1LinesGetLatestTransientRatingResponse200 | ProblemDetails]:
    r"""Get latest line transient rating

     This endpoint returns the most recent line transient rating for the line: the short-duration
    overload ampacity the line can sustain for each calculated duration.

    A transient rating is a set of per-duration values calculated at a single point in time. The
    response
    contains one `timestamp` and a `ratings` array with one entry per calculated duration (for example
    5, 10 or 15 minutes), and every calculated duration is returned. Transient ratings are calculated
    for
    the configured durations of one hour or shorter, so a configured duration longer than one hour is
    not
    calculated and is absent from the response.

    This endpoint returns real-time data and can be polled at short intervals (for example every 3–5
    minutes) for operational monitoring.

    ### Quantity
    Use the optional `quantity` query parameter to choose the quantity returned:
      - `current` (default) — line transient rating in amperes (`unit: \"Ampere\"`).
      - `apparent_power` — line transient rating converted to three-phase apparent power in MVA (`unit:
    \"MVA\"`) using `S = sqrt(3) * V * I / 1,000,000`.

    ### Voltage selection for `apparent_power`
    The line's **operational voltage** is used when it is set and positive; otherwise the **nominal
    voltage** is used.
    Both voltages are exposed on the facility in the `GET /assets/v1/assets` response so clients can
    verify which value the calculation would use.
    If neither voltage is usable, the response is `404`.

    Args:
        line_id (UUID):
        quantity (Quantity | Unset): Which quantity to return from a rating endpoint:
              - `current` — value in amperes.
              - `apparent_power` — value converted to MVA using `S = sqrt(3) * V * I / 1,000,000`.
        since (datetime.datetime | Unset):  Example: 2024-07-01 12:00:00.001000+00:00.
        x_region (CapacityMonitoringV1LinesGetLatestTransientRatingXRegion | Unset):  Default:
            CapacityMonitoringV1LinesGetLatestTransientRatingXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CapacityMonitoringV1LinesGetLatestTransientRatingResponse200 | ProblemDetails]
    """

    kwargs = _get_kwargs(
        line_id=line_id,
        quantity=quantity,
        since=since,
        x_region=x_region,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    line_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    quantity: Quantity | Unset = UNSET,
    since: datetime.datetime | Unset = UNSET,
    x_region: CapacityMonitoringV1LinesGetLatestTransientRatingXRegion
    | Unset = CapacityMonitoringV1LinesGetLatestTransientRatingXRegion.EU,
) -> Any | CapacityMonitoringV1LinesGetLatestTransientRatingResponse200 | ProblemDetails | None:
    r"""Get latest line transient rating

     This endpoint returns the most recent line transient rating for the line: the short-duration
    overload ampacity the line can sustain for each calculated duration.

    A transient rating is a set of per-duration values calculated at a single point in time. The
    response
    contains one `timestamp` and a `ratings` array with one entry per calculated duration (for example
    5, 10 or 15 minutes), and every calculated duration is returned. Transient ratings are calculated
    for
    the configured durations of one hour or shorter, so a configured duration longer than one hour is
    not
    calculated and is absent from the response.

    This endpoint returns real-time data and can be polled at short intervals (for example every 3–5
    minutes) for operational monitoring.

    ### Quantity
    Use the optional `quantity` query parameter to choose the quantity returned:
      - `current` (default) — line transient rating in amperes (`unit: \"Ampere\"`).
      - `apparent_power` — line transient rating converted to three-phase apparent power in MVA (`unit:
    \"MVA\"`) using `S = sqrt(3) * V * I / 1,000,000`.

    ### Voltage selection for `apparent_power`
    The line's **operational voltage** is used when it is set and positive; otherwise the **nominal
    voltage** is used.
    Both voltages are exposed on the facility in the `GET /assets/v1/assets` response so clients can
    verify which value the calculation would use.
    If neither voltage is usable, the response is `404`.

    Args:
        line_id (UUID):
        quantity (Quantity | Unset): Which quantity to return from a rating endpoint:
              - `current` — value in amperes.
              - `apparent_power` — value converted to MVA using `S = sqrt(3) * V * I / 1,000,000`.
        since (datetime.datetime | Unset):  Example: 2024-07-01 12:00:00.001000+00:00.
        x_region (CapacityMonitoringV1LinesGetLatestTransientRatingXRegion | Unset):  Default:
            CapacityMonitoringV1LinesGetLatestTransientRatingXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CapacityMonitoringV1LinesGetLatestTransientRatingResponse200 | ProblemDetails
    """

    return (
        await asyncio_detailed(
            line_id=line_id,
            client=client,
            quantity=quantity,
            since=since,
            x_region=x_region,
        )
    ).parsed
