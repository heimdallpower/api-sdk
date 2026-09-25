"""
`quantity="apparent_power"` on the latest rating endpoints and the rating forecasts:
the unit switches from amperes to MVA, the metric stays the same, and every MVA value
is the three-phase apparent power of the ampere value at the facility voltage.
"""

import pytest

from heimdall_api_client.capacity_monitoring_api_client.models.quantity import Quantity
from tests.integration._live_line import AMPERE_UNIT, MVA_UNIT


def _latest(field):
    """Reads (calculation timestamp, [(label, value)]) from a latest-value response."""

    def read(data):
        point = getattr(data, field)
        return point.timestamp, [(f"{field} at {point.timestamp}", point.value)]

    return read


def _forecasts(field):
    """Reads (forecast run timestamp, [(label, value)]) for every percentile of every forecast."""

    def read(data):
        values = [
            (f"{field} {percentile} at {forecast.timestamp}", getattr(forecast, percentile).value)
            for forecast in getattr(data, field)
            for percentile in ("prediction", "p80", "p90", "p95", "p99")
        ]
        return data.updated_timestamp, values

    return read


# (method, whether it takes a facility id rather than a line id, reader)
_RATING_METHODS = [
    ("get_latest_heimdall_dlr", False, _latest("heimdall_dlr")),
    ("get_latest_heimdall_aar", False, _latest("heimdall_aar")),
    ("get_latest_circuit_rating", True, _latest("circuit_rating")),
    ("get_latest_heimdall_dlr_forecasts", False, _forecasts("heimdall_dlr_forecasts")),
    ("get_latest_heimdall_aar_forecasts", False, _forecasts("heimdall_aar_forecasts")),
    ("get_latest_circuit_rating_forecasts", True, _forecasts("circuit_rating_forecasts")),
]
_IDS = [m[0] for m in _RATING_METHODS]


def _fetch_both_quantities(fetch, read):
    """
    Fetches amperes and MVA, retrying when a new calculation lands between the two
    calls so both describe the same calculation.
    """
    for _ in range(3):
        amperes = fetch(Quantity.CURRENT).data
        mva = fetch("apparent_power").data
        if read(amperes)[0] == read(mva)[0]:
            break
    return amperes, mva


@pytest.mark.integration
@pytest.mark.parametrize(("method_name", "takes_facility", "read"), _RATING_METHODS, ids=_IDS)
def test_apparent_power_should_be_three_phase_conversion_of_amperes(
    api_client, live_line, fetch_or_skip, method_name, takes_facility, read
):
    asset_id = live_line.facility_id if takes_facility else live_line.line_id
    method = getattr(api_client, method_name)
    amperes, mva = _fetch_both_quantities(
        lambda quantity: fetch_or_skip(lambda: method(asset_id, quantity=quantity), f"{method_name} on {asset_id}"),
        read,
    )

    assert (amperes.unit, mva.unit) == (AMPERE_UNIT, MVA_UNIT), "unit should follow the requested quantity"
    assert mva.metric == amperes.metric, "metric should not depend on the quantity"

    ampere_timestamp, ampere_values = read(amperes)
    mva_timestamp, mva_values = read(mva)
    assert mva_timestamp == ampere_timestamp, "both quantities should describe the same calculation"
    assert [label for label, _ in mva_values] == [label for label, _ in ampere_values], "forecast steps should match"
    for (label, ampere_value), (_, mva_value) in zip(ampere_values, mva_values, strict=True):
        assert mva_value > 0, f"{label}: apparent power {mva_value} should be positive"
        live_line.assert_is_apparent_power_of(mva_value, ampere_value, f"{method_name} {label}")


@pytest.mark.integration
def test_latest_heimdall_dlr_should_be_limited_at_a_span_on_the_line(api_client, live_line, fetch_or_skip):
    amperes, mva = _fetch_both_quantities(
        lambda quantity: fetch_or_skip(
            lambda: api_client.get_latest_heimdall_dlr(live_line.line_id, quantity=quantity), "latest Heimdall DLR"
        ),
        _latest("heimdall_dlr"),
    )

    assert amperes.heimdall_dlr.at_span_id in live_line.span_ids, (
        f"at_span_id {amperes.heimdall_dlr.at_span_id} is not a span on line {live_line.line_id}"
    )
    assert mva.heimdall_dlr.at_span_id == amperes.heimdall_dlr.at_span_id, "limiting span should not depend on quantity"


@pytest.mark.integration
@pytest.mark.parametrize(
    ("method_name", "field"),
    [
        ("get_latest_heimdall_dlr_forecasts", "heimdall_dlr_forecasts"),
        ("get_latest_heimdall_aar_forecasts", "heimdall_aar_forecasts"),
    ],
)
def test_line_forecasts_should_be_limited_at_spans_on_the_line(
    api_client, live_line, fetch_or_skip, method_name, field
):
    for quantity in (Quantity.CURRENT, Quantity.APPARENT_POWER):
        response = fetch_or_skip(
            lambda q=quantity: getattr(api_client, method_name)(live_line.line_id, quantity=q), f"{method_name}"
        )

        at_span_ids = {
            getattr(forecast, percentile).at_span_id
            for forecast in getattr(response.data, field)
            for percentile in ("prediction", "p80", "p90", "p95", "p99")
        }
        unknown = at_span_ids - live_line.span_ids
        assert not unknown, f"{method_name} ({quantity}) references spans not on line {live_line.line_id}: {unknown}"
