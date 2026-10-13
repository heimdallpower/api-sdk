"""
Unit tests for the Heimdall AAR endpoints: forwarding of `include`, and parsing of
`at_span_id` and the per-span breakdown.
"""

import datetime
from uuid import UUID

import pytest

from heimdall_api_client.capacity_monitoring_api_client.models.heimdall_aar_include import HeimdallAarInclude
from tests.unit._fake_transport import RecordingTransport, make_client

LINE_ID = UUID("d67d2205-6629-4bbd-aa9f-436bf22842ad")
SPAN_A = UUID("11111111-1111-1111-1111-111111111111")
SPAN_B = UUID("22222222-2222-2222-2222-222222222222")

_LINE_AAR = {"timestamp": "2026-01-01T12:00:00Z", "value": 375.4, "at_span_id": str(SPAN_A)}

_LATEST = {
    "data": {
        "metric": "Heimdall AAR",
        "unit": "Ampere",
        "heimdall_aar": _LINE_AAR,
        "heimdall_span_aars": [
            {
                "span_id": str(SPAN_A),
                "heimdall_aar": {"timestamp": "2026-01-01T12:00:00Z", "value": 375.4},
            },
            {
                "span_id": str(SPAN_B),
                "heimdall_aar": {"timestamp": "2026-01-01T12:00:00Z", "value": 412.8},
            },
        ],
    }
}

_LATEST_LINE_ONLY = {
    "data": {"metric": "Heimdall AAR", "unit": "Ampere", "heimdall_aar": _LINE_AAR, "heimdall_span_aars": None}
}

_HISTORICAL = {
    "data": {
        "metric": "Heimdall AAR",
        "unit": "Ampere",
        "heimdall_aars": [_LINE_AAR],
        "heimdall_span_aars": [
            {
                "span_id": str(SPAN_A),
                "heimdall_aars": [
                    {"timestamp": "2026-01-01T12:00:00Z", "value": 375.4},
                    {"timestamp": "2026-01-01T12:05:00Z", "value": 377.9},
                ],
            },
            {
                "span_id": str(SPAN_B),
                "heimdall_aars": [{"timestamp": "2026-01-01T12:00:00Z", "value": 412.8}],
            },
        ],
    }
}

_HISTORICAL_LINE_ONLY = {
    "data": {"metric": "Heimdall AAR", "unit": "Ampere", "heimdall_aars": [_LINE_AAR], "heimdall_span_aars": None}
}

_FROM = datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC)
_TO = datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC)


class TestLatestHeimdallAar:
    def test_omits_include_by_default(self):
        transport = RecordingTransport(_LATEST_LINE_ONLY)

        result = make_client(transport).get_latest_heimdall_aar(LINE_ID)

        assert transport.last_request.url.path == f"/capacity_monitoring/v1/lines/{LINE_ID}/heimdall_aars/latest"
        assert "include" not in transport.last_params
        assert result.data.heimdall_span_aars is None

    def test_parses_at_span_id(self):
        result = make_client(RecordingTransport(_LATEST_LINE_ONLY)).get_latest_heimdall_aar(LINE_ID)

        assert result.data.heimdall_aar.at_span_id == SPAN_A

    @pytest.mark.parametrize("include", ["spans", HeimdallAarInclude.SPANS])
    def test_forwards_include(self, include):
        transport = RecordingTransport(_LATEST)

        make_client(transport).get_latest_heimdall_aar(LINE_ID, include=include)

        assert transport.last_params["include"] == "spans"

    def test_rejects_unknown_include_value(self):
        transport = RecordingTransport(_LATEST)

        with pytest.raises(ValueError):
            make_client(transport).get_latest_heimdall_aar(LINE_ID, include="measurement_points")
        assert transport.requests == []

    def test_parses_span_breakdown(self):
        result = make_client(RecordingTransport(_LATEST)).get_latest_heimdall_aar(LINE_ID, include="spans")

        first, second = result.data.heimdall_span_aars
        assert first.span_id == SPAN_A
        assert first.heimdall_aar.timestamp == datetime.datetime(2026, 1, 1, 12, tzinfo=datetime.UTC)
        assert first.heimdall_aar.value == 375.4
        assert second.span_id == SPAN_B
        assert second.heimdall_aar.value == 412.8


class TestHeimdallAars:
    def test_omits_include_by_default(self):
        transport = RecordingTransport(_HISTORICAL_LINE_ONLY)

        result = make_client(transport).get_heimdall_aars(LINE_ID, _FROM, _TO)

        assert transport.last_request.url.path == f"/capacity_monitoring/v1/lines/{LINE_ID}/heimdall_aars"
        assert transport.last_params["from_timestamp"] == "2026-01-01T00:00:00Z"
        assert "include" not in transport.last_params
        assert result.data.heimdall_span_aars is None

    def test_parses_at_span_id(self):
        result = make_client(RecordingTransport(_HISTORICAL_LINE_ONLY)).get_heimdall_aars(LINE_ID, _FROM, _TO)

        assert [aar.at_span_id for aar in result.data.heimdall_aars] == [SPAN_A]

    def test_forwards_include(self):
        transport = RecordingTransport(_HISTORICAL)

        make_client(transport).get_heimdall_aars(LINE_ID, _FROM, _TO, include=HeimdallAarInclude.SPANS)

        assert transport.last_params["include"] == "spans"

    def test_rejects_unknown_include_value(self):
        transport = RecordingTransport(_HISTORICAL)

        with pytest.raises(ValueError):
            make_client(transport).get_heimdall_aars(LINE_ID, _FROM, _TO, include="measurement_points")
        assert transport.requests == []

    def test_parses_span_series(self):
        result = make_client(RecordingTransport(_HISTORICAL)).get_heimdall_aars(LINE_ID, _FROM, _TO, include="spans")

        first, second = result.data.heimdall_span_aars
        assert first.span_id == SPAN_A
        assert [(d.timestamp.minute, d.value) for d in first.heimdall_aars] == [(0, 375.4), (5, 377.9)]
        assert second.span_id == SPAN_B
        (aar,) = second.heimdall_aars
        assert aar.value == 412.8
