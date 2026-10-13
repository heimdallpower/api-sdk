"""
`at_span_id` and `include="spans"` on the latest and historical Heimdall AAR endpoints:
the line value is limited at a span of the line, the per-span breakdown is absent unless
requested, and when requested it refers only to spans of the requested line, at the
line's timestamps.
"""

import datetime

import pytest

from heimdall_api_client.capacity_monitoring_api_client.models.heimdall_aar_include import HeimdallAarInclude
from heimdall_api_client.capacity_monitoring_api_client.types import Unset


def _assert_spans_belong_to_line(breakdown, live_line):
    span_ids = [span.span_id for span in breakdown]
    assert len(span_ids) == len(set(span_ids)), "each span should be listed once"
    for span_id in span_ids:
        assert span_id in live_line.span_ids, f"span {span_id} is not on line {live_line.line_id}"


@pytest.mark.integration
def test_latest_heimdall_aar_should_be_limited_at_a_span_and_omit_spans_unless_requested(
    api_client, live_line, fetch_or_skip
):
    response = fetch_or_skip(lambda: api_client.get_latest_heimdall_aar(live_line.line_id), "latest Heimdall AAR")

    at_span_id = response.data.heimdall_aar.at_span_id
    assert at_span_id in live_line.span_ids, f"at_span_id {at_span_id} is not on line {live_line.line_id}"
    breakdown = response.data.heimdall_span_aars
    assert breakdown is None or isinstance(breakdown, Unset), "breakdown should be absent when not requested"


@pytest.mark.integration
@pytest.mark.parametrize("include", [HeimdallAarInclude.SPANS, "spans"])
def test_latest_heimdall_aar_should_break_down_by_spans_of_the_line(api_client, live_line, fetch_or_skip, include):
    response = fetch_or_skip(
        lambda: api_client.get_latest_heimdall_aar(live_line.line_id, include=include), "latest Heimdall AAR"
    )

    breakdown = response.data.heimdall_span_aars
    assert isinstance(breakdown, list), "breakdown should be present when requested"
    _assert_spans_belong_to_line(breakdown, live_line)
    for span in breakdown:
        assert span.heimdall_aar.timestamp == response.data.heimdall_aar.timestamp, (
            f"span {span.span_id} AAR at {span.heimdall_aar.timestamp} is not at the line timestamp"
        )
        assert span.heimdall_aar.value > 0, f"AAR {span.heimdall_aar.value} on span {span.span_id} is not positive"


@pytest.mark.integration
def test_historical_heimdall_aars_should_be_limited_at_spans_and_omit_spans_unless_requested(
    api_client, live_line, window
):
    from_timestamp, to_timestamp = window

    response = api_client.get_heimdall_aars(live_line.line_id, from_timestamp, to_timestamp)

    for aar in response.data.heimdall_aars:
        assert aar.at_span_id in live_line.span_ids, (
            f"at_span_id {aar.at_span_id} at {aar.timestamp} is not on the line"
        )
    breakdown = response.data.heimdall_span_aars
    assert breakdown is None or isinstance(breakdown, Unset), "breakdown should be absent when not requested"


@pytest.mark.integration
def test_historical_heimdall_aars_should_break_down_by_spans_at_line_timestamps(api_client, live_line):
    # include=spans limits the period to 7 days.
    to_timestamp = datetime.datetime.now(datetime.UTC)
    from_timestamp = to_timestamp - datetime.timedelta(hours=6)

    response = api_client.get_heimdall_aars(
        live_line.line_id, from_timestamp, to_timestamp, include=HeimdallAarInclude.SPANS
    )

    breakdown = response.data.heimdall_span_aars
    assert isinstance(breakdown, list), "breakdown should be present when requested"
    _assert_spans_belong_to_line(breakdown, live_line)
    line_timestamps = {aar.timestamp for aar in response.data.heimdall_aars}
    for span in breakdown:
        timestamps = [aar.timestamp for aar in span.heimdall_aars]
        assert timestamps == sorted(timestamps), f"AARs on span {span.span_id} are not ordered by timestamp"
        for aar in span.heimdall_aars:
            assert aar.value > 0, f"AAR {aar.value} at {aar.timestamp} on span {span.span_id} is not positive"
            assert aar.timestamp in line_timestamps, (
                f"span {span.span_id} AAR at {aar.timestamp} is not at a timestamp where the line has a value"
            )
