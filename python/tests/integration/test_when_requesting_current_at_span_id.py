"""
`at_span_id` on the current and apparent power endpoints: the span where the line
current was measured is a span of the requested line, and apparent power, derived from
the line current, points at the same span as the current at the same timestamp.
"""

import datetime

import pytest


@pytest.mark.integration
def test_latest_current_and_apparent_power_should_be_measured_at_a_span_of_the_line(
    api_client, live_line, fetch_or_skip
):
    current = fetch_or_skip(lambda: api_client.get_latest_current(live_line.line_id), "latest current").data.current
    apparent_power = fetch_or_skip(
        lambda: api_client.get_latest_apparent_power(live_line.line_id), "latest apparent power"
    ).data.apparent_power

    assert current.at_span_id in live_line.span_ids, f"at_span_id {current.at_span_id} is not on the line"
    assert apparent_power.at_span_id in live_line.span_ids, f"at_span_id {apparent_power.at_span_id} is not on the line"
    if current.timestamp == apparent_power.timestamp:
        assert apparent_power.at_span_id == current.at_span_id, "apparent power should point at the current's span"


@pytest.mark.integration
def test_historical_current_and_apparent_power_should_be_measured_at_spans_of_the_line(api_client, live_line):
    to_timestamp = datetime.datetime.now(datetime.UTC)
    from_timestamp = to_timestamp - datetime.timedelta(hours=6)

    currents = api_client.get_currents(live_line.line_id, from_timestamp, to_timestamp).data.currents
    apparent_powers = api_client.get_apparent_power(
        live_line.line_id, from_timestamp, to_timestamp
    ).data.apparent_powers
    if not currents:
        pytest.skip(f"No current on line {live_line.line_id} in the last six hours")

    for current in currents:
        assert current.at_span_id in live_line.span_ids, (
            f"at_span_id {current.at_span_id} at {current.timestamp} is not on the line"
        )
    current_spans = {current.timestamp: current.at_span_id for current in currents}
    for apparent_power in apparent_powers:
        assert apparent_power.at_span_id in live_line.span_ids, (
            f"at_span_id {apparent_power.at_span_id} at {apparent_power.timestamp} is not on the line"
        )
        if apparent_power.timestamp in current_spans:
            assert apparent_power.at_span_id == current_spans[apparent_power.timestamp], (
                f"apparent power at {apparent_power.timestamp} should point at the current's span"
            )
