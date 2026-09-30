"""
Fetches the instrumented lines and the latest current for each, proving the helper
only returns lines with active measurement points that the data endpoints can serve.
"""

import datetime

import pytest

from heimdall_api_client.errors import HeimdallApiError


@pytest.fixture(scope="module")
def instrumented(api_client):
    return api_client.get_instrumented_lines()


@pytest.mark.integration
def test_every_line_has_an_active_measurement_point(instrumented):
    # The test client has lines with installed Neurons; an empty result means the filter dropped them all.
    assert instrumented, "expected at least one instrumented line"
    now = datetime.datetime.now(datetime.UTC)
    for item in instrumented:
        assert item.active_measurement_points, f"line {item.line.id} has no active measurement points"
        for mp in item.active_measurement_points:
            unregistered = mp.unregistered_timestamp
            assert not isinstance(unregistered, datetime.datetime) or unregistered > now, (
                f"measurement point {mp.id} on line {item.line.id} is retired"
            )


@pytest.mark.integration
def test_every_line_belongs_to_its_facility_in_the_assets(api_client, instrumented):
    facilities = {f.id: f for go in api_client.get_assets().data.grid_owners for f in go.facilities}
    for item in instrumented:
        assert item.facility.id in facilities, f"facility {item.facility.id} not in assets"
        line = facilities[item.facility.id].line
        assert line and line.id == item.line.id, f"facility {item.facility.id} should own line {item.line.id}"
        point_ids = {mp.id for span in line.spans for sp in span.span_phases for mp in sp.measurement_points}
        assert {mp.id for mp in item.active_measurement_points} <= point_ids


@pytest.mark.integration
def test_latest_current_succeeds_for_every_instrumented_line(api_client, instrumented):
    failures = {}
    for item in instrumented:
        try:
            api_client.get_latest_current(item.line.id)
        except HeimdallApiError as e:
            failures[item.line.id] = e.status_code
    assert not failures, f"latest current failed for lines: {failures}"
