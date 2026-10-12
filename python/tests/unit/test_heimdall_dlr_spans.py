"""
Unit tests for the Heimdall DLR endpoints: forwarding of `include`, and parsing of
the per-span breakdown.
"""

import datetime
from uuid import UUID

import pytest

from heimdall_api_client.capacity_monitoring_api_client.models.heimdall_dlr_include import HeimdallDlrInclude
from tests.unit._fake_transport import RecordingTransport, make_client

LINE_ID = UUID("d67d2205-6629-4bbd-aa9f-436bf22842ad")
SPAN_A = UUID("11111111-1111-1111-1111-111111111111")
SPAN_B = UUID("22222222-2222-2222-2222-222222222222")

_LINE_DLR = {"timestamp": "2026-01-01T12:00:00Z", "value": 375.4, "at_span_id": str(SPAN_A), "is_fallback": False}

_LATEST = {
    "data": {
        "metric": "Heimdall DLR",
        "unit": "Ampere",
        "heimdall_dlr": _LINE_DLR,
        "heimdall_span_dlrs": [
            {
                "span_id": str(SPAN_A),
                "heimdall_dlr": {"timestamp": "2026-01-01T12:00:00Z", "value": 375.4, "is_fallback": False},
            },
            {
                "span_id": str(SPAN_B),
                "heimdall_dlr": {"timestamp": "2026-01-01T12:00:00Z", "value": 412.8, "is_fallback": True},
            },
        ],
    }
}

_LATEST_LINE_ONLY = {
    "data": {"metric": "Heimdall DLR", "unit": "Ampere", "heimdall_dlr": _LINE_DLR, "heimdall_span_dlrs": None}
}

_HISTORICAL = {
    "data": {
        "metric": "Heimdall DLR",
        "unit": "Ampere",
        "heimdall_dlrs": [_LINE_DLR],
        "heimdall_span_dlrs": [
            {
                "span_id": str(SPAN_A),
                "heimdall_dlrs": [
                    {"timestamp": "2026-01-01T12:00:00Z", "value": 375.4, "is_fallback": False},
                    {"timestamp": "2026-01-01T12:05:00Z", "value": 377.9, "is_fallback": False},
                ],
            },
            {
                "span_id": str(SPAN_B),
                "heimdall_dlrs": [{"timestamp": "2026-01-01T12:00:00Z", "value": 412.8, "is_fallback": True}],
            },
        ],
    }
}

_HISTORICAL_LINE_ONLY = {
    "data": {"metric": "Heimdall DLR", "unit": "Ampere", "heimdall_dlrs": [_LINE_DLR], "heimdall_span_dlrs": None}
}

_FROM = datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC)
_TO = datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC)


class TestLatestHeimdallDlr:
    def test_omits_include_by_default(self):
        transport = RecordingTransport(_LATEST_LINE_ONLY)

        result = make_client(transport).get_latest_heimdall_dlr(LINE_ID)

        assert transport.last_request.url.path == f"/capacity_monitoring/v1/lines/{LINE_ID}/heimdall_dlrs/latest"
        assert "include" not in transport.last_params
        assert result.data.heimdall_span_dlrs is None

    @pytest.mark.parametrize("include", ["spans", HeimdallDlrInclude.SPANS])
    def test_forwards_include(self, include):
        transport = RecordingTransport(_LATEST)

        make_client(transport).get_latest_heimdall_dlr(LINE_ID, include=include)

        assert transport.last_params["include"] == "spans"

    def test_rejects_unknown_include_value(self):
        transport = RecordingTransport(_LATEST)

        with pytest.raises(ValueError):
            make_client(transport).get_latest_heimdall_dlr(LINE_ID, include="measurement_points")
        assert transport.requests == []

    def test_parses_span_breakdown(self):
        result = make_client(RecordingTransport(_LATEST)).get_latest_heimdall_dlr(LINE_ID, include="spans")

        first, second = result.data.heimdall_span_dlrs
        assert first.span_id == SPAN_A
        assert first.heimdall_dlr.timestamp == datetime.datetime(2026, 1, 1, 12, tzinfo=datetime.UTC)
        assert (first.heimdall_dlr.value, first.heimdall_dlr.is_fallback) == (375.4, False)
        assert second.span_id == SPAN_B
        assert (second.heimdall_dlr.value, second.heimdall_dlr.is_fallback) == (412.8, True)


class TestHeimdallDlrs:
    def test_omits_include_by_default(self):
        transport = RecordingTransport(_HISTORICAL_LINE_ONLY)

        result = make_client(transport).get_heimdall_dlrs(LINE_ID, _FROM, _TO)

        assert transport.last_request.url.path == f"/capacity_monitoring/v1/lines/{LINE_ID}/heimdall_dlrs"
        assert transport.last_params["from_timestamp"] == "2026-01-01T00:00:00Z"
        assert "include" not in transport.last_params
        assert result.data.heimdall_span_dlrs is None

    def test_forwards_include(self):
        transport = RecordingTransport(_HISTORICAL)

        make_client(transport).get_heimdall_dlrs(LINE_ID, _FROM, _TO, include=HeimdallDlrInclude.SPANS)

        assert transport.last_params["include"] == "spans"

    def test_rejects_unknown_include_value(self):
        transport = RecordingTransport(_HISTORICAL)

        with pytest.raises(ValueError):
            make_client(transport).get_heimdall_dlrs(LINE_ID, _FROM, _TO, include="measurement_points")
        assert transport.requests == []

    def test_parses_span_series(self):
        result = make_client(RecordingTransport(_HISTORICAL)).get_heimdall_dlrs(LINE_ID, _FROM, _TO, include="spans")

        first, second = result.data.heimdall_span_dlrs
        assert first.span_id == SPAN_A
        assert [(d.timestamp.minute, d.value) for d in first.heimdall_dlrs] == [(0, 375.4), (5, 377.9)]
        assert second.span_id == SPAN_B
        (dlr,) = second.heimdall_dlrs
        assert dlr.is_fallback is True
