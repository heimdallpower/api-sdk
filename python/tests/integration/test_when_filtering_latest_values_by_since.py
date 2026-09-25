"""
`since` on the latest current, apparent power, Heimdall DLR, Heimdall AAR and circuit
rating endpoints: a returned value is never older than `since`, and a `since` newer
than any value yields 404 (no data) instead of a stale value.
"""

import datetime

import pytest

from heimdall_api_client.errors import HeimdallApiError

# (method, whether it takes a facility id rather than a line id, field holding the latest value)
_SINCE_METHODS = [
    ("get_latest_current", False, "current"),
    ("get_latest_apparent_power", False, "apparent_power"),
    ("get_latest_heimdall_dlr", False, "heimdall_dlr"),
    ("get_latest_heimdall_aar", False, "heimdall_aar"),
    ("get_latest_circuit_rating", True, "circuit_rating"),
]
_IDS = [m[0] for m in _SINCE_METHODS]


@pytest.mark.integration
@pytest.mark.parametrize(("method_name", "takes_facility", "field"), _SINCE_METHODS, ids=_IDS)
def test_latest_value_should_not_be_older_than_since(
    api_client, live_line, fetch_or_skip, method_name, takes_facility, field
):
    asset_id = live_line.facility_id if takes_facility else live_line.line_id
    since = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=1)

    response = fetch_or_skip(
        lambda: getattr(api_client, method_name)(asset_id, since=since),
        f"{method_name} on {asset_id} since {since.isoformat()}",
    )

    timestamp = getattr(response.data, field).timestamp
    assert timestamp >= since, f"{method_name} returned {timestamp.isoformat()}, older than since {since.isoformat()}"


@pytest.mark.integration
@pytest.mark.parametrize(("method_name", "takes_facility", "field"), _SINCE_METHODS, ids=_IDS)
def test_latest_value_should_be_not_found_for_a_future_since(api_client, live_line, method_name, takes_facility, field):
    """No value can be newer than a future `since`; a 200 here means `since` was not sent."""
    asset_id = live_line.facility_id if takes_facility else live_line.line_id
    since = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)

    with pytest.raises(HeimdallApiError) as excinfo:
        getattr(api_client, method_name)(asset_id, since=since)

    assert excinfo.value.status_code == 404
