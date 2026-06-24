import datetime
from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.capacity_monitoring_v1_lines_get_heimdall_dlrs_response_200 import (
    CapacityMonitoringV1LinesGetHeimdallDlrsResponse200,
)
from ...models.capacity_monitoring_v1_lines_get_heimdall_dlrs_x_region import (
    CapacityMonitoringV1LinesGetHeimdallDlrsXRegion,
)
from ...models.problem_details import ProblemDetails
from ...models.quantity import Quantity
from ...types import UNSET, Response, Unset


def _get_kwargs(
    line_id: UUID,
    *,
    from_timestamp: datetime.datetime,
    to_timestamp: datetime.datetime,
    quantity: Quantity | Unset = UNSET,
    x_region: CapacityMonitoringV1LinesGetHeimdallDlrsXRegion
    | Unset = CapacityMonitoringV1LinesGetHeimdallDlrsXRegion.EU,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_region, Unset):
        headers["x-region"] = str(x_region)

    params: dict[str, Any] = {}

    json_from_timestamp = from_timestamp.isoformat()
    params["from_timestamp"] = json_from_timestamp

    json_to_timestamp = to_timestamp.isoformat()
    params["to_timestamp"] = json_to_timestamp

    json_quantity: str | Unset = UNSET
    if not isinstance(quantity, Unset):
        json_quantity = quantity.value

    params["quantity"] = json_quantity

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/capacity_monitoring/v1/lines/{line_id}/heimdall_dlrs".format(
            line_id=quote(str(line_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | CapacityMonitoringV1LinesGetHeimdallDlrsResponse200 | ProblemDetails | None:
    if response.status_code == 200:
        response_200 = CapacityMonitoringV1LinesGetHeimdallDlrsResponse200.from_dict(response.json())

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
) -> Response[Any | CapacityMonitoringV1LinesGetHeimdallDlrsResponse200 | ProblemDetails]:
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
    quantity: Quantity | Unset = UNSET,
    x_region: CapacityMonitoringV1LinesGetHeimdallDlrsXRegion
    | Unset = CapacityMonitoringV1LinesGetHeimdallDlrsXRegion.EU,
) -> Response[Any | CapacityMonitoringV1LinesGetHeimdallDlrsResponse200 | ProblemDetails]:
    r"""Get Heimdall DLRs

     This endpoint returns Heimdall Dynamic Line Rating (DLR) for the line within a specified time range.

    Heimdall DLR is calculated according to our own proprietary method, based on the CIGRE TB-601
    standard for thermal calculation for OHLs.
    This method also takes the conductor temperature and current into account, and uses these to adjust
    the weather parameters during calculations.

    Heimdall DLR is aggregated over the entire line. Using a 5-minute sliding window, the minimum
    ampacity are calculated for each window.

    The period between `from_timestamp` and `to_timestamp` must not exceed 30 days.

    ### Quantity
    Use the optional `quantity` query parameter to choose the quantity returned:
      - `current` (default) — Heimdall DLR in amperes (`unit: \"Ampere\"`).
      - `apparent_power` — Heimdall DLR converted to three-phase apparent power in MVA (`unit: \"MVA\"`)
    using `S = sqrt(3) * V * I / 1,000,000`.

    ### Voltage selection for `apparent_power`
    The line's **operational voltage** is used when it is set and positive; otherwise the **nominal
    voltage** is used.
    Both voltages are exposed on the facility in the `GET /assets/v1/assets` response so clients can
    verify which value the calculation would use.
    If neither voltage is usable, the response is `404`.

    Args:
        line_id (UUID):
        from_timestamp (datetime.datetime):  Example: 2024-07-01 00:00:00+00:00.
        to_timestamp (datetime.datetime):  Example: 2024-07-02 00:00:00+00:00.
        quantity (Quantity | Unset): Which quantity to return from a rating endpoint:
              - `current` — value in amperes.
              - `apparent_power` — value converted to MVA using `S = sqrt(3) * V * I / 1,000,000`.
        x_region (CapacityMonitoringV1LinesGetHeimdallDlrsXRegion | Unset):  Default:
            CapacityMonitoringV1LinesGetHeimdallDlrsXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CapacityMonitoringV1LinesGetHeimdallDlrsResponse200 | ProblemDetails]
    """

    kwargs = _get_kwargs(
        line_id=line_id,
        from_timestamp=from_timestamp,
        to_timestamp=to_timestamp,
        quantity=quantity,
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
    quantity: Quantity | Unset = UNSET,
    x_region: CapacityMonitoringV1LinesGetHeimdallDlrsXRegion
    | Unset = CapacityMonitoringV1LinesGetHeimdallDlrsXRegion.EU,
) -> Any | CapacityMonitoringV1LinesGetHeimdallDlrsResponse200 | ProblemDetails | None:
    r"""Get Heimdall DLRs

     This endpoint returns Heimdall Dynamic Line Rating (DLR) for the line within a specified time range.

    Heimdall DLR is calculated according to our own proprietary method, based on the CIGRE TB-601
    standard for thermal calculation for OHLs.
    This method also takes the conductor temperature and current into account, and uses these to adjust
    the weather parameters during calculations.

    Heimdall DLR is aggregated over the entire line. Using a 5-minute sliding window, the minimum
    ampacity are calculated for each window.

    The period between `from_timestamp` and `to_timestamp` must not exceed 30 days.

    ### Quantity
    Use the optional `quantity` query parameter to choose the quantity returned:
      - `current` (default) — Heimdall DLR in amperes (`unit: \"Ampere\"`).
      - `apparent_power` — Heimdall DLR converted to three-phase apparent power in MVA (`unit: \"MVA\"`)
    using `S = sqrt(3) * V * I / 1,000,000`.

    ### Voltage selection for `apparent_power`
    The line's **operational voltage** is used when it is set and positive; otherwise the **nominal
    voltage** is used.
    Both voltages are exposed on the facility in the `GET /assets/v1/assets` response so clients can
    verify which value the calculation would use.
    If neither voltage is usable, the response is `404`.

    Args:
        line_id (UUID):
        from_timestamp (datetime.datetime):  Example: 2024-07-01 00:00:00+00:00.
        to_timestamp (datetime.datetime):  Example: 2024-07-02 00:00:00+00:00.
        quantity (Quantity | Unset): Which quantity to return from a rating endpoint:
              - `current` — value in amperes.
              - `apparent_power` — value converted to MVA using `S = sqrt(3) * V * I / 1,000,000`.
        x_region (CapacityMonitoringV1LinesGetHeimdallDlrsXRegion | Unset):  Default:
            CapacityMonitoringV1LinesGetHeimdallDlrsXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CapacityMonitoringV1LinesGetHeimdallDlrsResponse200 | ProblemDetails
    """

    return sync_detailed(
        line_id=line_id,
        client=client,
        from_timestamp=from_timestamp,
        to_timestamp=to_timestamp,
        quantity=quantity,
        x_region=x_region,
    ).parsed


async def asyncio_detailed(
    line_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    from_timestamp: datetime.datetime,
    to_timestamp: datetime.datetime,
    quantity: Quantity | Unset = UNSET,
    x_region: CapacityMonitoringV1LinesGetHeimdallDlrsXRegion
    | Unset = CapacityMonitoringV1LinesGetHeimdallDlrsXRegion.EU,
) -> Response[Any | CapacityMonitoringV1LinesGetHeimdallDlrsResponse200 | ProblemDetails]:
    r"""Get Heimdall DLRs

     This endpoint returns Heimdall Dynamic Line Rating (DLR) for the line within a specified time range.

    Heimdall DLR is calculated according to our own proprietary method, based on the CIGRE TB-601
    standard for thermal calculation for OHLs.
    This method also takes the conductor temperature and current into account, and uses these to adjust
    the weather parameters during calculations.

    Heimdall DLR is aggregated over the entire line. Using a 5-minute sliding window, the minimum
    ampacity are calculated for each window.

    The period between `from_timestamp` and `to_timestamp` must not exceed 30 days.

    ### Quantity
    Use the optional `quantity` query parameter to choose the quantity returned:
      - `current` (default) — Heimdall DLR in amperes (`unit: \"Ampere\"`).
      - `apparent_power` — Heimdall DLR converted to three-phase apparent power in MVA (`unit: \"MVA\"`)
    using `S = sqrt(3) * V * I / 1,000,000`.

    ### Voltage selection for `apparent_power`
    The line's **operational voltage** is used when it is set and positive; otherwise the **nominal
    voltage** is used.
    Both voltages are exposed on the facility in the `GET /assets/v1/assets` response so clients can
    verify which value the calculation would use.
    If neither voltage is usable, the response is `404`.

    Args:
        line_id (UUID):
        from_timestamp (datetime.datetime):  Example: 2024-07-01 00:00:00+00:00.
        to_timestamp (datetime.datetime):  Example: 2024-07-02 00:00:00+00:00.
        quantity (Quantity | Unset): Which quantity to return from a rating endpoint:
              - `current` — value in amperes.
              - `apparent_power` — value converted to MVA using `S = sqrt(3) * V * I / 1,000,000`.
        x_region (CapacityMonitoringV1LinesGetHeimdallDlrsXRegion | Unset):  Default:
            CapacityMonitoringV1LinesGetHeimdallDlrsXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CapacityMonitoringV1LinesGetHeimdallDlrsResponse200 | ProblemDetails]
    """

    kwargs = _get_kwargs(
        line_id=line_id,
        from_timestamp=from_timestamp,
        to_timestamp=to_timestamp,
        quantity=quantity,
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
    quantity: Quantity | Unset = UNSET,
    x_region: CapacityMonitoringV1LinesGetHeimdallDlrsXRegion
    | Unset = CapacityMonitoringV1LinesGetHeimdallDlrsXRegion.EU,
) -> Any | CapacityMonitoringV1LinesGetHeimdallDlrsResponse200 | ProblemDetails | None:
    r"""Get Heimdall DLRs

     This endpoint returns Heimdall Dynamic Line Rating (DLR) for the line within a specified time range.

    Heimdall DLR is calculated according to our own proprietary method, based on the CIGRE TB-601
    standard for thermal calculation for OHLs.
    This method also takes the conductor temperature and current into account, and uses these to adjust
    the weather parameters during calculations.

    Heimdall DLR is aggregated over the entire line. Using a 5-minute sliding window, the minimum
    ampacity are calculated for each window.

    The period between `from_timestamp` and `to_timestamp` must not exceed 30 days.

    ### Quantity
    Use the optional `quantity` query parameter to choose the quantity returned:
      - `current` (default) — Heimdall DLR in amperes (`unit: \"Ampere\"`).
      - `apparent_power` — Heimdall DLR converted to three-phase apparent power in MVA (`unit: \"MVA\"`)
    using `S = sqrt(3) * V * I / 1,000,000`.

    ### Voltage selection for `apparent_power`
    The line's **operational voltage** is used when it is set and positive; otherwise the **nominal
    voltage** is used.
    Both voltages are exposed on the facility in the `GET /assets/v1/assets` response so clients can
    verify which value the calculation would use.
    If neither voltage is usable, the response is `404`.

    Args:
        line_id (UUID):
        from_timestamp (datetime.datetime):  Example: 2024-07-01 00:00:00+00:00.
        to_timestamp (datetime.datetime):  Example: 2024-07-02 00:00:00+00:00.
        quantity (Quantity | Unset): Which quantity to return from a rating endpoint:
              - `current` — value in amperes.
              - `apparent_power` — value converted to MVA using `S = sqrt(3) * V * I / 1,000,000`.
        x_region (CapacityMonitoringV1LinesGetHeimdallDlrsXRegion | Unset):  Default:
            CapacityMonitoringV1LinesGetHeimdallDlrsXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CapacityMonitoringV1LinesGetHeimdallDlrsResponse200 | ProblemDetails
    """

    return (
        await asyncio_detailed(
            line_id=line_id,
            client=client,
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
            quantity=quantity,
            x_region=x_region,
        )
    ).parsed
