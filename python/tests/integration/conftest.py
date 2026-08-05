import datetime
import os

import pytest

from heimdall_api_client import HeimdallApiClient
from heimdall_api_client.errors import HeimdallApiError

# The API rejects windows longer than 30 days.
_WINDOW = datetime.timedelta(days=1)


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
