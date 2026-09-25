import datetime
import os

import pytest

from heimdall_api_client import HeimdallApiClient
from heimdall_api_client.errors import HeimdallApiError
from tests.integration._live_line import LiveLine

# The API rejects windows longer than 30 days.
_WINDOW = datetime.timedelta(days=1)

# How recent a line's latest current must be for the line to count as live.
_LIVE_WITHIN = datetime.timedelta(days=1)


@pytest.fixture(scope="session")
def api_client():
    return HeimdallApiClient(
        client_id=os.environ["HEIMDALL_CLIENT_ID"], client_secret=os.environ["HEIMDALL_CLIENT_SECRET"]
    )


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
def live_line(api_client):
    """The first line whose latest current is less than a day old, so data-dependent checks have data to check."""
    since = datetime.datetime.now(datetime.UTC) - _LIVE_WITHIN
    assets = api_client.get_assets()
    for grid_owner in assets.data.grid_owners:
        for facility in grid_owner.facilities:
            if not facility.line:
                continue
            try:
                api_client.get_latest_current(facility.line.id, since=since)
            except HeimdallApiError as e:
                if e.status_code == 404:
                    continue
                raise
            spans = facility.line.spans
            span_phases = [span_phase for span in spans for span_phase in span.span_phases]
            measurement_points = [mp for span_phase in span_phases for mp in span_phase.measurement_points]
            return LiveLine(
                line_id=facility.line.id,
                facility_id=facility.id,
                nominal_voltage=facility.nominal_voltage,
                # Unset when the facility has no operational voltage configured.
                operational_voltage=facility.operational_voltage or None,
                span_ids=frozenset(span.id for span in spans),
                span_phase_ids=frozenset(span_phase.id for span_phase in span_phases),
                measurement_point_ids=frozenset(mp.id for mp in measurement_points),
            )
    pytest.skip(f"No line with a current newer than {since.isoformat()} available for this client")


@pytest.fixture
def fetch_or_skip():
    """Returns the response of `call`, or skips the test when the endpoint reports 404 (no data for the asset)."""

    def fetch(call, description: str):
        try:
            return call()
        except HeimdallApiError as e:
            if e.status_code == 404:
                pytest.skip(f"No data available for {description}")
            raise

    return fetch


@pytest.fixture(scope="session")
def window():
    to_timestamp = datetime.datetime.now(datetime.UTC)
    return to_timestamp - _WINDOW, to_timestamp


@pytest.fixture
def assert_endpoint_responds():
    """
    Asserts the endpoint is wired up correctly: it must return a well-formed
    response, or report 404 because the asset has no data for this metric.
    Any other status means the wiring or the request itself is wrong.
    """

    def assert_responds(call, description: str):
        try:
            response = call()
        except HeimdallApiError as e:
            if e.status_code == 404:
                pytest.skip(f"No data available for {description}")
            raise

        assert response is not None, f"{description} should not return None"
        assert hasattr(response, "data"), f"{description} response should have a 'data' attribute"

    return assert_responds
