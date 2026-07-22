"""Integration tests for Capacity Monitoring endpoints."""

import datetime
import uuid

import pytest

from heimdall_api_client import HeimdallApiError

# "Heimdall Power Line" – d67d2205-6629-4bbd-aa9f-436bf22842ad
_HEIMDALL_POWER_LINE_ID = uuid.UUID("d67d2205-6629-4bbd-aa9f-436bf22842ad")
# "Heimdall Power Line" facility – c0ad547d-0d06-4f4c-b5dc-d319430902d2
_HEIMDALL_POWER_FACILITY_ID = uuid.UUID("c0ad547d-0d06-4f4c-b5dc-d319430902d2")
_FROM = datetime.datetime(2026, 1, 1, 0, 0, 0, tzinfo=datetime.UTC)
_TO = datetime.datetime(2026, 1, 2, 0, 0, 0, tzinfo=datetime.UTC)


@pytest.mark.integration
def test_get_latest_heimdall_dlr_with_invalid_line_id_should_raise(api_client):
    with pytest.raises(HeimdallApiError) as exc_info:
        api_client.get_latest_heimdall_dlr(line_id=uuid.uuid4())
    assert exc_info.value.status_code in (404, 403), "Expected 404 or 403 for unknown line"


# ---------------------------------------------------------------------------
# get_heimdall_dlrs – historical
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def heimdall_dlrs_result(api_client):
    return api_client.get_heimdall_dlrs(
        line_id=_HEIMDALL_POWER_LINE_ID,
        from_timestamp=_FROM,
        to_timestamp=_TO,
    )


@pytest.mark.integration
def test_get_heimdall_dlrs_should_return_response(heimdall_dlrs_result):
    assert heimdall_dlrs_result is not None


@pytest.mark.integration
def test_get_heimdall_dlrs_result_should_have_metric(heimdall_dlrs_result):
    assert heimdall_dlrs_result.data.metric, "Metric should not be empty"


@pytest.mark.integration
def test_get_heimdall_dlrs_result_should_have_unit(heimdall_dlrs_result):
    assert heimdall_dlrs_result.data.unit, "Unit should not be empty"


@pytest.mark.integration
def test_get_heimdall_dlrs_result_should_have_dlrs_list(heimdall_dlrs_result):
    # The API returns HTTP 200 with a (possibly empty) list – an empty list is valid.
    assert heimdall_dlrs_result.data.heimdall_dlrs is not None


@pytest.mark.integration
def test_get_heimdall_dlrs_all_dlrs_should_have_timestamps_within_requested_range(heimdall_dlrs_result):
    for dlr in heimdall_dlrs_result.data.heimdall_dlrs:
        assert dlr.timestamp >= _FROM, f"Timestamp {dlr.timestamp} is before {_FROM}"
        assert dlr.timestamp <= _TO, f"Timestamp {dlr.timestamp} is after {_TO}"


@pytest.mark.integration
def test_get_heimdall_dlrs_all_dlrs_should_have_positive_values(heimdall_dlrs_result):
    for dlr in heimdall_dlrs_result.data.heimdall_dlrs:
        assert dlr.value > 0, f"DLR value {dlr.value} at {dlr.timestamp} should be positive"


# ---------------------------------------------------------------------------
# get_heimdall_aars – historical
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def heimdall_aars_result(api_client):
    return api_client.get_heimdall_aars(
        line_id=_HEIMDALL_POWER_LINE_ID,
        from_timestamp=_FROM,
        to_timestamp=_TO,
    )


@pytest.mark.integration
def test_get_heimdall_aars_should_return_response(heimdall_aars_result):
    assert heimdall_aars_result is not None


@pytest.mark.integration
def test_get_heimdall_aars_result_should_have_metric(heimdall_aars_result):
    assert heimdall_aars_result.data.metric, "Metric should not be empty"


@pytest.mark.integration
def test_get_heimdall_aars_result_should_have_unit(heimdall_aars_result):
    assert heimdall_aars_result.data.unit, "Unit should not be empty"


@pytest.mark.integration
def test_get_heimdall_aars_result_should_have_aars_list(heimdall_aars_result):
    # The API returns HTTP 200 with a (possibly empty) list – an empty list is valid.
    assert heimdall_aars_result.data.heimdall_aars is not None


@pytest.mark.integration
def test_get_heimdall_aars_all_aars_should_have_timestamps_within_requested_range(heimdall_aars_result):
    for aar in heimdall_aars_result.data.heimdall_aars:
        assert aar.timestamp >= _FROM, f"Timestamp {aar.timestamp} is before {_FROM}"
        assert aar.timestamp <= _TO, f"Timestamp {aar.timestamp} is after {_TO}"


@pytest.mark.integration
def test_get_heimdall_aars_all_aars_should_have_positive_values(heimdall_aars_result):
    for aar in heimdall_aars_result.data.heimdall_aars:
        assert aar.value > 0, f"AAR value {aar.value} at {aar.timestamp} should be positive"


# ---------------------------------------------------------------------------
# get_circuit_ratings – historical
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def circuit_ratings_result(api_client):
    return api_client.get_circuit_ratings(
        facility_id=_HEIMDALL_POWER_FACILITY_ID,
        from_timestamp=_FROM,
        to_timestamp=_TO,
    )


@pytest.mark.integration
def test_get_circuit_ratings_should_return_response(circuit_ratings_result):
    assert circuit_ratings_result is not None


@pytest.mark.integration
def test_get_circuit_ratings_result_should_have_metric(circuit_ratings_result):
    assert circuit_ratings_result.data.metric, "Metric should not be empty"


@pytest.mark.integration
def test_get_circuit_ratings_result_should_have_unit(circuit_ratings_result):
    assert circuit_ratings_result.data.unit, "Unit should not be empty"


@pytest.mark.integration
def test_get_circuit_ratings_result_should_have_circuit_ratings_list(circuit_ratings_result):
    # The API returns HTTP 200 with a (possibly empty) list – an empty list is valid.
    assert circuit_ratings_result.data.circuit_ratings is not None


@pytest.mark.integration
def test_get_circuit_ratings_all_circuit_ratings_should_have_timestamps_within_requested_range(
    circuit_ratings_result,
):
    for cr in circuit_ratings_result.data.circuit_ratings:
        assert cr.timestamp >= _FROM, f"Timestamp {cr.timestamp} is before {_FROM}"
        assert cr.timestamp <= _TO, f"Timestamp {cr.timestamp} is after {_TO}"


@pytest.mark.integration
def test_get_circuit_ratings_all_circuit_ratings_should_have_positive_values(circuit_ratings_result):
    for cr in circuit_ratings_result.data.circuit_ratings:
        assert cr.value > 0, f"Circuit rating value {cr.value} at {cr.timestamp} should be positive"
