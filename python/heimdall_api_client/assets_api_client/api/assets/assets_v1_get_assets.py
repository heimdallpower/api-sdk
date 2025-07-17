from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.assets_v1_get_assets_response_200 import AssetsV1GetAssetsResponse200
from ...models.assets_v1_get_assets_x_region import AssetsV1GetAssetsXRegion
from ...models.problem_details import ProblemDetails
from ...types import Unset



def _get_kwargs(
    *,
    x_region: Union[Unset, AssetsV1GetAssetsXRegion] = AssetsV1GetAssetsXRegion.EU,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_region, Unset):
        headers["x-region"] = str(x_region)




    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/assets/v1/assets",
    }


    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Any, AssetsV1GetAssetsResponse200, ProblemDetails]]:
    if response.status_code == 200:
        response_200 = AssetsV1GetAssetsResponse200.from_dict(response.json())



        return response_200
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 403:
        response_403 = ProblemDetails.from_dict(response.json())



        return response_403
    if response.status_code == 500:
        response_500 = ProblemDetails.from_dict(response.json())



        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Any, AssetsV1GetAssetsResponse200, ProblemDetails]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    x_region: Union[Unset, AssetsV1GetAssetsXRegion] = AssetsV1GetAssetsXRegion.EU,

) -> Response[Union[Any, AssetsV1GetAssetsResponse200, ProblemDetails]]:
    """ Get assets

     This endpoint gets all assets you have access to, structured in the hierarchy described in the
    introduction.

    Args:
        x_region (Union[Unset, AssetsV1GetAssetsXRegion]):  Default: AssetsV1GetAssetsXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, AssetsV1GetAssetsResponse200, ProblemDetails]]
     """


    kwargs = _get_kwargs(
        x_region=x_region,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    x_region: Union[Unset, AssetsV1GetAssetsXRegion] = AssetsV1GetAssetsXRegion.EU,

) -> Optional[Union[Any, AssetsV1GetAssetsResponse200, ProblemDetails]]:
    """ Get assets

     This endpoint gets all assets you have access to, structured in the hierarchy described in the
    introduction.

    Args:
        x_region (Union[Unset, AssetsV1GetAssetsXRegion]):  Default: AssetsV1GetAssetsXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, AssetsV1GetAssetsResponse200, ProblemDetails]
     """


    return sync_detailed(
        client=client,
x_region=x_region,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    x_region: Union[Unset, AssetsV1GetAssetsXRegion] = AssetsV1GetAssetsXRegion.EU,

) -> Response[Union[Any, AssetsV1GetAssetsResponse200, ProblemDetails]]:
    """ Get assets

     This endpoint gets all assets you have access to, structured in the hierarchy described in the
    introduction.

    Args:
        x_region (Union[Unset, AssetsV1GetAssetsXRegion]):  Default: AssetsV1GetAssetsXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, AssetsV1GetAssetsResponse200, ProblemDetails]]
     """


    kwargs = _get_kwargs(
        x_region=x_region,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    x_region: Union[Unset, AssetsV1GetAssetsXRegion] = AssetsV1GetAssetsXRegion.EU,

) -> Optional[Union[Any, AssetsV1GetAssetsResponse200, ProblemDetails]]:
    """ Get assets

     This endpoint gets all assets you have access to, structured in the hierarchy described in the
    introduction.

    Args:
        x_region (Union[Unset, AssetsV1GetAssetsXRegion]):  Default: AssetsV1GetAssetsXRegion.EU.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, AssetsV1GetAssetsResponse200, ProblemDetails]
     """


    return (await asyncio_detailed(
        client=client,
x_region=x_region,

    )).parsed
