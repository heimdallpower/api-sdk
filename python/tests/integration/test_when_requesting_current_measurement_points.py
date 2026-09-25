"""
`include="measurement_points"` on the latest and historical current endpoints: the
per-measurement-point breakdown is absent unless requested, and when requested it
refers only to spans, span phases and measurement points of the requested line.
"""

import datetime

import pytest

from heimdall_api_client.grid_insights_api_client.models.current_include import CurrentInclude
from heimdall_api_client.grid_insights_api_client.types import Unset


def _assert_ids_belong_to_line(breakdown, live_line):
    for span in breakdown:
        assert span.span_id in live_line.span_ids, f"span {span.span_id} is not on line {live_line.line_id}"
        for span_phase in span.span_phases:
            assert span_phase.span_phase_id in live_line.span_phase_ids, (
                f"span phase {span_phase.span_phase_id} is not on line {live_line.line_id}"
            )
            for mp in span_phase.measurement_points:
                assert mp.measurement_point_id in live_line.measurement_point_ids, (
                    f"measurement point {mp.measurement_point_id} is not on line {live_line.line_id}"
                )


def _measurement_points(breakdown):
    return [mp for span in breakdown for span_phase in span.span_phases for mp in span_phase.measurement_points]


@pytest.mark.integration
def test_latest_current_should_omit_measurement_points_unless_requested(api_client, live_line, fetch_or_skip):
    response = fetch_or_skip(lambda: api_client.get_latest_current(live_line.line_id), "latest current")

    breakdown = response.data.measurement_point_currents
    assert breakdown is None or isinstance(breakdown, Unset), "breakdown should be absent when not requested"


@pytest.mark.integration
@pytest.mark.parametrize("include", [CurrentInclude.MEASUREMENT_POINTS, "measurement_points"])
def test_latest_current_should_break_down_by_measurement_points_of_the_line(
    api_client, live_line, fetch_or_skip, include
):
    response = fetch_or_skip(
        lambda: api_client.get_latest_current(live_line.line_id, include=include), "latest current"
    )

    breakdown = response.data.measurement_point_currents
    # A latest line current exists (the call returned 200), so at least one measurement point measured it.
    assert _measurement_points(breakdown), "breakdown should list at least one measurement point when requested"
    _assert_ids_belong_to_line(breakdown, live_line)
    for mp in _measurement_points(breakdown):
        assert mp.value >= 0, f"current {mp.value} at measurement point {mp.measurement_point_id} is negative"
        assert mp.timestamp.utcoffset() == datetime.timedelta(0), f"timestamp {mp.timestamp} is not UTC"


@pytest.mark.integration
def test_historical_currents_should_omit_measurement_points_unless_requested(api_client, live_line, window):
    from_timestamp, to_timestamp = window

    response = api_client.get_currents(live_line.line_id, from_timestamp, to_timestamp)

    breakdown = response.data.measurement_point_currents
    assert breakdown is None or isinstance(breakdown, Unset), "breakdown should be absent when not requested"


@pytest.mark.integration
def test_historical_currents_should_break_down_by_measurement_points_within_the_window(api_client, live_line):
    to_timestamp = datetime.datetime.now(datetime.UTC)
    from_timestamp = to_timestamp - datetime.timedelta(hours=6)

    response = api_client.get_currents(
        live_line.line_id, from_timestamp, to_timestamp, include=CurrentInclude.MEASUREMENT_POINTS
    )

    breakdown = response.data.measurement_point_currents
    assert isinstance(breakdown, list), "breakdown should be present when requested"
    if not response.data.currents:
        pytest.skip(f"No current on line {live_line.line_id} in the last six hours")

    readings = [reading for mp in _measurement_points(breakdown) for reading in mp.currents]
    # The line-level series is derived from the measurement points, so readings on the line imply readings here.
    assert readings, "breakdown should hold readings when the line has currents in the window"
    _assert_ids_belong_to_line(breakdown, live_line)
    for reading in readings:
        assert reading.value >= 0, f"current {reading.value} at {reading.timestamp} is negative"
        assert from_timestamp <= reading.timestamp <= to_timestamp, (
            f"reading at {reading.timestamp} is outside [{from_timestamp}, {to_timestamp}]"
        )
