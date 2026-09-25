"""
The API accepts `quantity=current|apparent_power` on every capacity monitoring
endpoint. These tests call each "latest" and forecast method through a fake
transport and assert that `quantity` is forwarded when given and omitted
otherwise (the API then defaults to amperes).
"""

from collections.abc import Callable
from typing import Any
from uuid import UUID

import pytest

from heimdall_api_client.capacity_monitoring_api_client.models.quantity import Quantity
from tests.unit._fake_transport import RecordingTransport, make_client

ASSET_ID = UUID("d67d2205-6629-4bbd-aa9f-436bf22842ad")
SPAN_ID = "11111111-1111-1111-1111-111111111111"

_AMPACITY = {"value": 375.4, "at_span_id": SPAN_ID}
_LINE_FORECAST = {
    "timestamp": "2026-01-01T12:00:00Z",
    **{key: _AMPACITY for key in ("prediction", "p80", "p90", "p95", "p99")},
}
_CIRCUIT_FORECAST = {
    "timestamp": "2026-01-01T12:00:00Z",
    **{key: {"value": 375.4, "at_facility_component_id": None} for key in ("prediction", "p80", "p90", "p95", "p99")},
}


def _body(key: str, value: Any) -> dict[str, Any]:
    return {"data": {"metric": "m", "unit": "MVA", key: value}}


def _forecast_body(key: str, item: dict[str, Any]) -> dict[str, Any]:
    return {"data": {"metric": "m", "unit": "MVA", "updated_timestamp": "2026-01-01T12:00:00Z", key: [item]}}


_CASES: list[tuple[str, dict[str, Any], str, Callable[..., Any]]] = [
    (
        "latest Heimdall DLR",
        _body(
            "heimdall_dlr",
            {"timestamp": "2026-01-01T12:00:00Z", "value": 1.0, "at_span_id": SPAN_ID, "is_fallback": False},
        ),
        f"/capacity_monitoring/v1/lines/{ASSET_ID}/heimdall_dlrs/latest",
        lambda client, **kw: client.get_latest_heimdall_dlr(ASSET_ID, **kw),
    ),
    (
        "latest Heimdall AAR",
        _body("heimdall_aar", {"timestamp": "2026-01-01T12:00:00Z", "value": 1.0}),
        f"/capacity_monitoring/v1/lines/{ASSET_ID}/heimdall_aars/latest",
        lambda client, **kw: client.get_latest_heimdall_aar(ASSET_ID, **kw),
    ),
    (
        "Heimdall DLR forecasts",
        _forecast_body("heimdall_dlr_forecasts", _LINE_FORECAST),
        f"/capacity_monitoring/v1/lines/{ASSET_ID}/heimdall_dlrs/forecasts",
        lambda client, **kw: client.get_latest_heimdall_dlr_forecasts(ASSET_ID, **kw),
    ),
    (
        "Heimdall AAR forecasts",
        _forecast_body("heimdall_aar_forecasts", _LINE_FORECAST),
        f"/capacity_monitoring/v1/lines/{ASSET_ID}/heimdall_aars/forecasts",
        lambda client, **kw: client.get_latest_heimdall_aar_forecasts(ASSET_ID, **kw),
    ),
    (
        "latest circuit rating",
        _body("circuit_rating", {"timestamp": "2026-01-01T12:00:00Z", "value": 1.0, "is_fallback": False}),
        f"/capacity_monitoring/v1/facilities/{ASSET_ID}/circuit_ratings/latest",
        lambda client, **kw: client.get_latest_circuit_rating(ASSET_ID, **kw),
    ),
    (
        "circuit rating forecasts",
        _forecast_body("circuit_rating_forecasts", _CIRCUIT_FORECAST),
        f"/capacity_monitoring/v1/facilities/{ASSET_ID}/circuit_ratings/forecasts",
        lambda client, **kw: client.get_latest_circuit_rating_forecasts(ASSET_ID, **kw),
    ),
]
_IDS = [case[0] for case in _CASES]


@pytest.mark.parametrize(("name", "body", "path", "call"), _CASES, ids=_IDS)
@pytest.mark.parametrize("quantity", ["apparent_power", Quantity.APPARENT_POWER])
def test_forwards_quantity(name, body, path, call, quantity):
    transport = RecordingTransport(body)

    call(make_client(transport), quantity=quantity)

    assert transport.last_request.url.path == path
    assert transport.last_params["quantity"] == "apparent_power"


@pytest.mark.parametrize(("name", "body", "path", "call"), _CASES, ids=_IDS)
def test_omits_quantity_by_default(name, body, path, call):
    transport = RecordingTransport(body)

    call(make_client(transport))

    assert "quantity" not in transport.last_params


@pytest.mark.parametrize(("name", "body", "path", "call"), _CASES, ids=_IDS)
def test_rejects_unknown_quantity(name, body, path, call):
    transport = RecordingTransport(body)

    with pytest.raises(ValueError):
        call(make_client(transport), quantity="watts")
    assert transport.requests == []


def test_latest_heimdall_dlr_keeps_since_alongside_quantity():
    import datetime

    transport = RecordingTransport(_CASES[0][1])

    make_client(transport).get_latest_heimdall_dlr(
        ASSET_ID, since=datetime.datetime(2026, 1, 1, 12, tzinfo=datetime.UTC), quantity="apparent_power"
    )

    assert transport.last_params["since"] == "2026-01-01T12:00:00Z"
    assert transport.last_params["quantity"] == "apparent_power"


@pytest.mark.parametrize(
    ("method", "parameter"),
    [
        ("get_latest_current", "include"),
        ("get_currents", "include"),
        ("get_latest_heimdall_dlr", "quantity"),
        ("get_latest_heimdall_aar", "quantity"),
        ("get_latest_heimdall_dlr_forecasts", "quantity"),
        ("get_latest_heimdall_aar_forecasts", "quantity"),
        ("get_latest_circuit_rating", "quantity"),
        ("get_latest_circuit_rating_forecasts", "quantity"),
    ],
)
def test_new_parameters_are_appended_as_optional_keywords(method: str, parameter: str):
    """New parameters must come last and default to None so existing positional calls keep working."""
    import inspect

    from heimdall_api_client import HeimdallApiClient

    parameters = list(inspect.signature(getattr(HeimdallApiClient, method)).parameters.values())
    assert parameters[-1].name == parameter
    assert parameters[-1].default is None
