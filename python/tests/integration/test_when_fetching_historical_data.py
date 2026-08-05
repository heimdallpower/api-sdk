import datetime

import pytest

from heimdall_api_client.capacity_monitoring_api_client.models.quantity import Quantity
from heimdall_api_client.errors import HeimdallApiError
from heimdall_api_client.grid_insights_api_client.models.unit_system import UnitSystem

# The API rejects windows longer than 30 days.
_WINDOW = datetime.timedelta(days=1)


@pytest.fixture(scope="session")
def line_id(api_client):
    """The first line found on any facility of the first grid owner."""
    assets = api_client.get_assets()
    for grid_owner in assets.data.grid_owners:
        for facility in grid_owner.facilities:
            if facility.line:
                return facility.line.id
    pytest.skip("No facility with a line available for this client")


@pytest.fixture(scope="session")
def facility_id(api_client):
    assets = api_client.get_assets()
    for grid_owner in assets.data.grid_owners:
        if grid_owner.facilities:
            return grid_owner.facilities[0].id
    pytest.skip("No facility available for this client")


@pytest.fixture(scope="session")
def window():
    to_timestamp = datetime.datetime.now(datetime.UTC)
    return to_timestamp - _WINDOW, to_timestamp


def _assert_endpoint_responds(call, description: str):
    """
    Asserts the endpoint is wired up correctly: it must return a well-formed
    response, or report 404 because the asset has no data for this metric.
    Any other status means the wiring or the request itself is wrong.
    """
    try:
        response = call()
    except HeimdallApiError as e:
        if e.status_code == 404:
            pytest.skip(f"No data available for {description}")
        raise

    assert response is not None, f"{description} should not return None"
    assert hasattr(response, "data"), f"{description} response should have a 'data' attribute"


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
def test_should_return_historical_line_data(api_client, line_id, window, method_name):
    from_timestamp, to_timestamp = window

    _assert_endpoint_responds(
        lambda: getattr(api_client, method_name)(line_id, from_timestamp, to_timestamp),
        f"{method_name} on line {line_id}",
    )


@pytest.mark.integration
def test_should_return_historical_circuit_ratings(api_client, facility_id, window):
    from_timestamp, to_timestamp = window

    _assert_endpoint_responds(
        lambda: api_client.get_circuit_ratings(facility_id, from_timestamp, to_timestamp),
        f"circuit ratings on facility {facility_id}",
    )


@pytest.mark.integration
def test_should_accept_naive_and_offset_timestamps(api_client, line_id):
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
        _assert_endpoint_responds(
            lambda f=from_timestamp, t=to_timestamp: api_client.get_currents(line_id, f, t),
            f"currents with from={from_timestamp.isoformat()} to={to_timestamp.isoformat()}",
        )


@pytest.mark.integration
@pytest.mark.parametrize("method_name", ["get_conductor_temperatures", "get_icing", "get_sag_and_clearance"])
@pytest.mark.parametrize("unit_system", [UnitSystem.METRIC, "imperial"])
def test_should_accept_unit_system(api_client, line_id, window, method_name, unit_system):
    from_timestamp, to_timestamp = window

    _assert_endpoint_responds(
        lambda: getattr(api_client, method_name)(line_id, from_timestamp, to_timestamp, unit_system=unit_system),
        f"{method_name} with unit_system={unit_system}",
    )


@pytest.mark.integration
@pytest.mark.parametrize("method_name", ["get_heimdall_dlrs", "get_heimdall_aars"])
@pytest.mark.parametrize("quantity", [Quantity.CURRENT, "apparent_power"])
def test_should_accept_quantity_for_line_ratings(api_client, line_id, window, method_name, quantity):
    from_timestamp, to_timestamp = window

    _assert_endpoint_responds(
        lambda: getattr(api_client, method_name)(line_id, from_timestamp, to_timestamp, quantity=quantity),
        f"{method_name} with quantity={quantity}",
    )


@pytest.mark.integration
@pytest.mark.parametrize("quantity", [Quantity.CURRENT, "apparent_power"])
def test_should_accept_quantity_for_circuit_ratings(api_client, facility_id, window, quantity):
    from_timestamp, to_timestamp = window

    _assert_endpoint_responds(
        lambda: api_client.get_circuit_ratings(facility_id, from_timestamp, to_timestamp, quantity=quantity),
        f"circuit ratings with quantity={quantity}",
    )


@pytest.mark.integration
def test_should_return_latest_apparent_power(api_client, line_id):
    _assert_endpoint_responds(
        lambda: api_client.get_latest_apparent_power(line_id),
        f"latest apparent power on line {line_id}",
    )


@pytest.mark.integration
@pytest.mark.parametrize("unit_system", [UnitSystem.METRIC, "imperial"])
def test_should_return_icing_forecast(api_client, line_id, unit_system):
    _assert_endpoint_responds(
        lambda: api_client.get_icing_forecast(line_id, unit_system=unit_system),
        f"icing forecast with unit_system={unit_system}",
    )


@pytest.mark.integration
@pytest.mark.parametrize("method_name", ["get_latest_heimdall_dlr", "get_latest_heimdall_aar", "get_latest_icing"])
def test_should_accept_since_on_latest_endpoints(api_client, line_id, method_name):
    """`since` is serialized with the same isoformat() the API rejects unless normalized."""
    since = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=6)

    _assert_endpoint_responds(
        lambda: getattr(api_client, method_name)(line_id, since=since),
        f"{method_name} with since={since.isoformat()}",
    )


@pytest.mark.integration
def test_should_accept_since_on_latest_circuit_rating(api_client, facility_id):
    since = datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=6)

    _assert_endpoint_responds(
        lambda: api_client.get_latest_circuit_rating(facility_id, since=since),
        f"latest circuit rating with since={since.isoformat()}",
    )


@pytest.mark.integration
def test_should_reject_window_longer_than_30_days(api_client, line_id):
    """The API caps the range at 30 days; the SDK surfaces that as HeimdallApiError."""
    to_timestamp = datetime.datetime.now(datetime.UTC)
    from_timestamp = to_timestamp - datetime.timedelta(days=45)

    with pytest.raises(HeimdallApiError) as excinfo:
        api_client.get_currents(line_id, from_timestamp, to_timestamp)

    assert excinfo.value.status_code == 400
