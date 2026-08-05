"""
Endpoints that return the latest value for an asset, plus forecasts.
Windowed endpoints are covered in test_when_fetching_historical_data.py.
"""

import datetime

import pytest

from heimdall_api_client.grid_insights_api_client.models.unit_system import UnitSystem

_LATEST_LINE_METHODS_ACCEPTING_SINCE = [
    "get_latest_current",
    "get_latest_conductor_temperature",
    "get_latest_apparent_power",
    "get_latest_icing",
    "get_latest_sag_and_clearance",
    "get_latest_heimdall_dlr",
    "get_latest_heimdall_aar",
]


@pytest.mark.integration
@pytest.mark.parametrize(
    "method_name",
    [
        "get_latest_current",
        "get_latest_conductor_temperature",
        "get_latest_apparent_power",
        "get_latest_icing",
        "get_latest_sag_and_clearance",
        "get_latest_heimdall_dlr",
        "get_latest_heimdall_aar",
        "get_latest_heimdall_dlr_forecasts",
        "get_latest_heimdall_aar_forecasts",
    ],
)
def test_should_return_latest_line_data(api_client, line_id, assert_endpoint_responds, method_name):
    assert_endpoint_responds(
        lambda: getattr(api_client, method_name)(line_id),
        f"{method_name} on line {line_id}",
    )


@pytest.mark.integration
@pytest.mark.parametrize("method_name", ["get_latest_circuit_rating", "get_latest_circuit_rating_forecasts"])
def test_should_return_latest_facility_data(api_client, facility_id, assert_endpoint_responds, method_name):
    assert_endpoint_responds(
        lambda: getattr(api_client, method_name)(facility_id),
        f"{method_name} on facility {facility_id}",
    )


@pytest.mark.integration
@pytest.mark.parametrize("unit_system", [UnitSystem.METRIC, "imperial"])
def test_should_return_icing_forecast(api_client, line_id, assert_endpoint_responds, unit_system):
    assert_endpoint_responds(
        lambda: api_client.get_icing_forecast(line_id, unit_system=unit_system),
        f"icing forecast with unit_system={unit_system}",
    )


@pytest.mark.integration
@pytest.mark.parametrize("method_name", _LATEST_LINE_METHODS_ACCEPTING_SINCE)
def test_should_accept_since_on_latest_line_endpoints(api_client, line_id, assert_endpoint_responds, method_name):
    """
    `since` bounds how old the returned value may be. It is serialized with the
    same isoformat() the API rejects unless the SDK normalizes it, so a 404 here
    means no value is newer than `since` -- not that the parameter was dropped.
    """
    since = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=6)

    assert_endpoint_responds(
        lambda: getattr(api_client, method_name)(line_id, since=since),
        f"{method_name} with since={since.isoformat()}",
    )


@pytest.mark.integration
def test_should_accept_since_on_latest_circuit_rating(api_client, facility_id, assert_endpoint_responds):
    since = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=6)

    assert_endpoint_responds(
        lambda: api_client.get_latest_circuit_rating(facility_id, since=since),
        f"latest circuit rating with since={since.isoformat()}",
    )


@pytest.mark.integration
@pytest.mark.parametrize("method_name", _LATEST_LINE_METHODS_ACCEPTING_SINCE)
def test_should_return_a_value_older_than_a_generous_since(api_client, line_id, assert_endpoint_responds, method_name):
    """
    A `since` far enough back that any stored value qualifies. This distinguishes
    a working `since` from one the API rejects outright: a rejected timestamp
    fails with 400 regardless of how much data exists.
    """
    since = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=730)

    assert_endpoint_responds(
        lambda: getattr(api_client, method_name)(line_id, since=since),
        f"{method_name} with since={since.isoformat()}",
    )
