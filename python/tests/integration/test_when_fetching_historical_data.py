"""
Endpoints that return a series of measurements over a from/to window.
Latest-value endpoints are covered in test_when_fetching_latest_data.py.
"""

import datetime

import pytest

from heimdall_api_client.capacity_monitoring_api_client.models.quantity import Quantity
from heimdall_api_client.errors import HeimdallApiError
from heimdall_api_client.grid_insights_api_client.models.unit_system import UnitSystem


@pytest.mark.integration
@pytest.mark.parametrize(
    "method_name",
    [
        "get_currents",
        "get_conductor_temperatures",
        "get_icing",
        "get_sag_and_clearance",
        "get_apparent_power",
        "get_heimdall_dlrs",
        "get_heimdall_aars",
    ],
)
def test_should_return_historical_line_data(api_client, line_id, window, assert_endpoint_responds, method_name):
    from_timestamp, to_timestamp = window

    assert_endpoint_responds(
        lambda: getattr(api_client, method_name)(line_id, from_timestamp, to_timestamp),
        f"{method_name} on line {line_id}",
    )


@pytest.mark.integration
def test_should_return_historical_circuit_ratings(api_client, facility_id, window, assert_endpoint_responds):
    from_timestamp, to_timestamp = window

    assert_endpoint_responds(
        lambda: api_client.get_circuit_ratings(facility_id, from_timestamp, to_timestamp),
        f"circuit ratings on facility {facility_id}",
    )


@pytest.mark.integration
def test_should_accept_naive_and_offset_timestamps(api_client, line_id, assert_endpoint_responds):
    """
    The API accepts only Z-suffixed UTC, so the SDK must normalize whatever the
    caller passes -- naive, UTC-aware, or another offset -- to the same window.
    """
    oslo = datetime.timezone(datetime.timedelta(hours=2))
    naive_from = datetime.datetime(2026, 7, 1, 10, 0, 0)
    naive_to = datetime.datetime(2026, 7, 2, 10, 0, 0)

    equivalent_windows = [
        (naive_from, naive_to),
        (naive_from.replace(tzinfo=datetime.UTC), naive_to.replace(tzinfo=datetime.UTC)),
        (naive_from.replace(tzinfo=oslo), naive_to.replace(tzinfo=oslo)),
        (naive_from.replace(microsecond=123456, tzinfo=datetime.UTC), naive_to.replace(tzinfo=datetime.UTC)),
    ]

    for from_timestamp, to_timestamp in equivalent_windows:
        assert_endpoint_responds(
            lambda f=from_timestamp, t=to_timestamp: api_client.get_currents(line_id, f, t),
            f"currents with from={from_timestamp.isoformat()} to={to_timestamp.isoformat()}",
        )


@pytest.mark.integration
@pytest.mark.parametrize("method_name", ["get_conductor_temperatures", "get_icing", "get_sag_and_clearance"])
@pytest.mark.parametrize("unit_system", [UnitSystem.METRIC, "imperial"])
def test_should_accept_unit_system(api_client, line_id, window, assert_endpoint_responds, method_name, unit_system):
    from_timestamp, to_timestamp = window

    assert_endpoint_responds(
        lambda: getattr(api_client, method_name)(line_id, from_timestamp, to_timestamp, unit_system=unit_system),
        f"{method_name} with unit_system={unit_system}",
    )


@pytest.mark.integration
@pytest.mark.parametrize("method_name", ["get_heimdall_dlrs", "get_heimdall_aars"])
@pytest.mark.parametrize("quantity", [Quantity.CURRENT, "apparent_power"])
def test_should_accept_quantity_for_line_ratings(
    api_client, line_id, window, assert_endpoint_responds, method_name, quantity
):
    from_timestamp, to_timestamp = window

    assert_endpoint_responds(
        lambda: getattr(api_client, method_name)(line_id, from_timestamp, to_timestamp, quantity=quantity),
        f"{method_name} with quantity={quantity}",
    )


@pytest.mark.integration
@pytest.mark.parametrize("quantity", [Quantity.CURRENT, "apparent_power"])
def test_should_accept_quantity_for_circuit_ratings(
    api_client, facility_id, window, assert_endpoint_responds, quantity
):
    from_timestamp, to_timestamp = window

    assert_endpoint_responds(
        lambda: api_client.get_circuit_ratings(facility_id, from_timestamp, to_timestamp, quantity=quantity),
        f"circuit ratings with quantity={quantity}",
    )


@pytest.mark.integration
def test_should_reject_window_longer_than_30_days(api_client, line_id):
    """The API caps the range at 30 days; the SDK surfaces that as HeimdallApiError."""
    to_timestamp = datetime.datetime.now(datetime.UTC)
    from_timestamp = to_timestamp - datetime.timedelta(days=45)

    with pytest.raises(HeimdallApiError) as excinfo:
        api_client.get_currents(line_id, from_timestamp, to_timestamp)

    assert excinfo.value.status_code == 400
