"""
`include="spans"` on the latest and historical Heimdall DLR endpoints: the per-span
breakdown is absent unless requested, and when requested it refers only to spans of
the requested line. The breakdown may be empty, since per-span values are persisted
only by the fallback-enabled calculation path.
"""

import datetime

import pytest

from heimdall_api_client.capacity_monitoring_api_client.models.heimdall_dlr_include import HeimdallDlrInclude
from heimdall_api_client.capacity_monitoring_api_client.types import Unset


def _assert_spans_belong_to_line(breakdown, live_line):
    span_ids = [span.span_id for span in breakdown]
    assert len(span_ids) == len(set(span_ids)), "each span should be listed once"
    for span_id in span_ids:
        assert span_id in live_line.span_ids, f"span {span_id} is not on line {live_line.line_id}"


@pytest.mark.integration
def test_latest_heimdall_dlr_should_omit_spans_unless_requested(api_client, live_line, fetch_or_skip):
    response = fetch_or_skip(lambda: api_client.get_latest_heimdall_dlr(live_line.line_id), "latest Heimdall DLR")

    breakdown = response.data.heimdall_span_dlrs
    assert breakdown is None or isinstance(breakdown, Unset), "breakdown should be absent when not requested"


@pytest.mark.integration
@pytest.mark.parametrize("include", [HeimdallDlrInclude.SPANS, "spans"])
def test_latest_heimdall_dlr_should_break_down_by_spans_of_the_line(api_client, live_line, fetch_or_skip, include):
    response = fetch_or_skip(
        lambda: api_client.get_latest_heimdall_dlr(live_line.line_id, include=include), "latest Heimdall DLR"
    )

    breakdown = response.data.heimdall_span_dlrs
    assert isinstance(breakdown, list), "breakdown should be present when requested"
    _assert_spans_belong_to_line(breakdown, live_line)
    for span in breakdown:
        assert span.heimdall_dlr.timestamp == response.data.heimdall_dlr.timestamp, (
            f"span {span.span_id} DLR at {span.heimdall_dlr.timestamp} is not at the line timestamp"
        )
        assert span.heimdall_dlr.value > 0, f"DLR {span.heimdall_dlr.value} on span {span.span_id} is not positive"


@pytest.mark.integration
def test_historical_heimdall_dlrs_should_omit_spans_unless_requested(api_client, live_line, window):
    from_timestamp, to_timestamp = window

    response = api_client.get_heimdall_dlrs(live_line.line_id, from_timestamp, to_timestamp)

    breakdown = response.data.heimdall_span_dlrs
    assert breakdown is None or isinstance(breakdown, Unset), "breakdown should be absent when not requested"


@pytest.mark.integration
def test_historical_heimdall_dlrs_should_break_down_by_spans_within_the_window(api_client, live_line):
    # include=spans limits the period to 7 days.
    to_timestamp = datetime.datetime.now(datetime.UTC)
    from_timestamp = to_timestamp - datetime.timedelta(hours=6)

    response = api_client.get_heimdall_dlrs(
        live_line.line_id, from_timestamp, to_timestamp, include=HeimdallDlrInclude.SPANS
    )

    breakdown = response.data.heimdall_span_dlrs
    assert isinstance(breakdown, list), "breakdown should be present when requested"
    _assert_spans_belong_to_line(breakdown, live_line)
    for span in breakdown:
        timestamps = [dlr.timestamp for dlr in span.heimdall_dlrs]
        assert timestamps == sorted(timestamps), f"DLRs on span {span.span_id} are not ordered by timestamp"
        for dlr in span.heimdall_dlrs:
            assert dlr.value > 0, f"DLR {dlr.value} at {dlr.timestamp} on span {span.span_id} is not positive"
            assert from_timestamp <= dlr.timestamp <= to_timestamp, (
                f"DLR at {dlr.timestamp} is outside [{from_timestamp}, {to_timestamp}]"
            )
