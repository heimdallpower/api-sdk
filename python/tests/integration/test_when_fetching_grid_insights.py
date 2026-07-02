"""Integration tests for Grid Insights endpoints."""

import datetime
import uuid

import pytest

from heimdall_api_client import HeimdallApiError

# "Heimdall Power Line" – d67d2205-6629-4bbd-aa9f-436bf22842ad
_HEIMDALL_POWER_LINE_ID = uuid.UUID("d67d2205-6629-4bbd-aa9f-436bf22842ad")
_FROM = datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
_TO = datetime.datetime(2026, 1, 2, 0, 0, 0, tzinfo=datetime.timezone.utc)


@pytest.mark.integration
def test_get_latest_current_with_invalid_line_id_should_raise(api_client):
    with pytest.raises(HeimdallApiError) as exc_info:
        api_client.get_latest_current(line_id=uuid.uuid4())
    assert exc_info.value.status_code in (404, 403), "Expected 404 or 403 for unknown line"


# ---------------------------------------------------------------------------
# get_currents – historical
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def currents_result(api_client):
    return api_client.get_currents(
        line_id=_HEIMDALL_POWER_LINE_ID,
        from_timestamp=_FROM,
        to_timestamp=_TO,
    )


@pytest.mark.integration
def test_get_currents_should_return_response(currents_result):
    assert currents_result is not None


@pytest.mark.integration
def test_get_currents_result_should_have_metric(currents_result):
    assert currents_result.data.metric, "Metric should not be empty"


@pytest.mark.integration
def test_get_currents_result_should_have_unit(currents_result):
    assert currents_result.data.unit, "Unit should not be empty"


@pytest.mark.integration
def test_get_currents_result_should_have_currents_list(currents_result):
    # The API returns HTTP 200 with a (possibly empty) list – an empty list is valid.
    assert currents_result.data.currents is not None


@pytest.mark.integration
def test_get_currents_all_currents_should_have_timestamps_within_requested_range(currents_result):
    for current in currents_result.data.currents:
        assert current.timestamp >= _FROM, f"Timestamp {current.timestamp} is before {_FROM}"
        assert current.timestamp <= _TO, f"Timestamp {current.timestamp} is after {_TO}"


# ---------------------------------------------------------------------------
# get_conductor_temperatures – historical
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def conductor_temperatures_result(api_client):
    return api_client.get_conductor_temperatures(
        line_id=_HEIMDALL_POWER_LINE_ID,
        from_timestamp=_FROM,
        to_timestamp=_TO,
    )


@pytest.mark.integration
def test_get_conductor_temperatures_should_return_response(conductor_temperatures_result):
    assert conductor_temperatures_result is not None


@pytest.mark.integration
def test_get_conductor_temperatures_result_should_have_metric(conductor_temperatures_result):
    assert conductor_temperatures_result.data.metric, "Metric should not be empty"


@pytest.mark.integration
def test_get_conductor_temperatures_result_should_have_unit(conductor_temperatures_result):
    assert conductor_temperatures_result.data.unit, "Unit should not be empty"


@pytest.mark.integration
def test_get_conductor_temperatures_result_should_have_list(conductor_temperatures_result):
    # The API returns HTTP 200 with a (possibly empty) list – an empty list is valid.
    assert conductor_temperatures_result.data.conductor_temperatures is not None


@pytest.mark.integration
def test_get_conductor_temperatures_all_readings_should_have_timestamps_within_requested_range(
    conductor_temperatures_result,
):
    for ct in conductor_temperatures_result.data.conductor_temperatures:
        assert ct.timestamp >= _FROM, f"Timestamp {ct.timestamp} is before {_FROM}"
        assert ct.timestamp <= _TO, f"Timestamp {ct.timestamp} is after {_TO}"


# ---------------------------------------------------------------------------
# get_icing – historical
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def icing_result(api_client):
    return api_client.get_icing(
        line_id=_HEIMDALL_POWER_LINE_ID,
        from_timestamp=_FROM,
        to_timestamp=_TO,
    )


@pytest.mark.integration
def test_get_icing_should_return_response(icing_result):
    assert icing_result is not None


@pytest.mark.integration
def test_get_icing_result_should_have_metric(icing_result):
    assert icing_result.data.metric, "Metric should not be empty"


@pytest.mark.integration
def test_get_icing_result_should_have_unit(icing_result):
    assert icing_result.data.unit, "Unit should not be empty"


@pytest.mark.integration
def test_get_icing_result_should_have_icing_data(icing_result):
    # The API returns HTTP 200 – icing is a nested object, not a flat list.
    assert icing_result.data.icing is not None


# ---------------------------------------------------------------------------
# get_sag_and_clearance – historical
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def sag_and_clearance_result(api_client):
    return api_client.get_sag_and_clearance(
        line_id=_HEIMDALL_POWER_LINE_ID,
        from_timestamp=_FROM,
        to_timestamp=_TO,
    )


@pytest.mark.integration
def test_get_sag_and_clearance_should_return_response(sag_and_clearance_result):
    assert sag_and_clearance_result is not None


@pytest.mark.integration
def test_get_sag_and_clearance_result_should_have_metric(sag_and_clearance_result):
    assert sag_and_clearance_result.data.metric, "Metric should not be empty"


@pytest.mark.integration
def test_get_sag_and_clearance_result_should_have_unit(sag_and_clearance_result):
    assert sag_and_clearance_result.data.unit, "Unit should not be empty"


@pytest.mark.integration
def test_get_sag_and_clearance_result_should_have_sag_and_clearance_data(sag_and_clearance_result):
    # The API returns HTTP 200 – sag_and_clearance is a nested object, not a flat list.
    assert sag_and_clearance_result.data.sag_and_clearance is not None


# ---------------------------------------------------------------------------
# get_apparent_power – historical
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def apparent_power_result(api_client):
    return api_client.get_apparent_power(
        line_id=_HEIMDALL_POWER_LINE_ID,
        from_timestamp=_FROM,
        to_timestamp=_TO,
    )


@pytest.mark.integration
def test_get_apparent_power_should_return_response(apparent_power_result):
    assert apparent_power_result is not None


@pytest.mark.integration
def test_get_apparent_power_result_should_have_metric(apparent_power_result):
    assert apparent_power_result.data.metric, "Metric should not be empty"


@pytest.mark.integration
def test_get_apparent_power_result_should_have_unit(apparent_power_result):
    assert apparent_power_result.data.unit, "Unit should not be empty"


@pytest.mark.integration
def test_get_apparent_power_result_should_have_apparent_powers_list(apparent_power_result):
    # The API returns HTTP 200 with a (possibly empty) list – an empty list is valid.
    assert apparent_power_result.data.apparent_powers is not None


@pytest.mark.integration
def test_get_apparent_power_all_readings_should_have_timestamps_within_requested_range(apparent_power_result):
    for ap in apparent_power_result.data.apparent_powers:
        assert ap.timestamp >= _FROM, f"Timestamp {ap.timestamp} is before {_FROM}"
        assert ap.timestamp <= _TO, f"Timestamp {ap.timestamp} is after {_TO}"



# ---------------------------------------------------------------------------
# get_currents – historical
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def currents_result(api_client):
    return api_client.get_currents(
        line_id=_HEIMDALL_POWER_LINE_ID,
        from_timestamp=_FROM,
        to_timestamp=_TO,
    )


@pytest.mark.integration
def test_get_currents_should_return_response(currents_result):
    assert currents_result is not None


@pytest.mark.integration
def test_get_currents_result_should_have_metric(currents_result):
    assert currents_result.data.metric, "Metric should not be empty"


@pytest.mark.integration
def test_get_currents_result_should_have_unit(currents_result):
    assert currents_result.data.unit, "Unit should not be empty"


@pytest.mark.integration
def test_get_currents_result_should_have_currents_list(currents_result):
    # The API returns HTTP 200 with a (possibly empty) list – an empty list is valid.
    assert currents_result.data.currents is not None


@pytest.mark.integration
def test_get_currents_all_currents_should_have_timestamps_within_requested_range(currents_result):
    for current in currents_result.data.currents:
        assert current.timestamp >= _FROM, f"Timestamp {current.timestamp} is before {_FROM}"
        assert current.timestamp <= _TO, f"Timestamp {current.timestamp} is after {_TO}"


# ---------------------------------------------------------------------------
# get_conductor_temperatures – historical
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def conductor_temperatures_result(api_client):
    return api_client.get_conductor_temperatures(
        line_id=_HEIMDALL_POWER_LINE_ID,
        from_timestamp=_FROM,
        to_timestamp=_TO,
    )


@pytest.mark.integration
def test_get_conductor_temperatures_should_return_response(conductor_temperatures_result):
    assert conductor_temperatures_result is not None


@pytest.mark.integration
def test_get_conductor_temperatures_result_should_have_metric(conductor_temperatures_result):
    assert conductor_temperatures_result.data.metric, "Metric should not be empty"


@pytest.mark.integration
def test_get_conductor_temperatures_result_should_have_unit(conductor_temperatures_result):
    assert conductor_temperatures_result.data.unit, "Unit should not be empty"


@pytest.mark.integration
def test_get_conductor_temperatures_result_should_have_list(conductor_temperatures_result):
    # The API returns HTTP 200 with a (possibly empty) list – an empty list is valid.
    assert conductor_temperatures_result.data.conductor_temperatures is not None


@pytest.mark.integration
def test_get_conductor_temperatures_all_readings_should_have_timestamps_within_requested_range(
    conductor_temperatures_result,
):
    for ct in conductor_temperatures_result.data.conductor_temperatures:
        assert ct.timestamp >= _FROM, f"Timestamp {ct.timestamp} is before {_FROM}"
        assert ct.timestamp <= _TO, f"Timestamp {ct.timestamp} is after {_TO}"


