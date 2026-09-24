"""
Unit tests for the current endpoints: forwarding of `since` and `include`, and
parsing of the per-measurement-point breakdown.
"""

import datetime
from uuid import UUID

import pytest

from heimdall_api_client.grid_insights_api_client.models.current_include import CurrentInclude
from tests.unit._fake_transport import RecordingTransport, make_client

LINE_ID = UUID("d67d2205-6629-4bbd-aa9f-436bf22842ad")
SPAN_ID = UUID("11111111-1111-1111-1111-111111111111")
SPAN_PHASE_ID = UUID("33333333-3333-3333-3333-333333333333")
MEASUREMENT_POINT_A = UUID("44444444-4444-4444-4444-444444444444")
MEASUREMENT_POINT_B = UUID("55555555-5555-5555-5555-555555555555")

_LATEST = {
    "data": {
        "metric": "Current",
        "unit": "Ampere",
        "current": {"timestamp": "2026-01-01T12:00:00Z", "value": 452.3},
        "measurement_point_currents": [
            {
                "span_id": str(SPAN_ID),
                "span_phases": [
                    {
                        "span_phase_id": str(SPAN_PHASE_ID),
                        "measurement_points": [
                            {
                                "measurement_point_id": str(MEASUREMENT_POINT_A),
                                "timestamp": "2026-01-01T11:58:00Z",
                                "value": 450.1,
                            },
                            {
                                "measurement_point_id": str(MEASUREMENT_POINT_B),
                                "timestamp": "2026-01-01T11:59:00Z",
                                "value": 452.3,
                            },
                        ],
                    }
                ],
            }
        ],
    }
}

_LATEST_AGGREGATE_ONLY = {
    "data": {
        "metric": "Current",
        "unit": "Ampere",
        "current": {"timestamp": "2026-01-01T12:00:00Z", "value": 452.3},
        "measurement_point_currents": None,
    }
}

_HISTORICAL = {
    "data": {
        "metric": "Current",
        "unit": "Ampere",
        "currents": [{"timestamp": "2026-01-01T12:00:00Z", "value": 452.3}],
        "measurement_point_currents": [
            {
                "span_id": str(SPAN_ID),
                "span_phases": [
                    {
                        "span_phase_id": str(SPAN_PHASE_ID),
                        "measurement_points": [
                            {
                                "measurement_point_id": str(MEASUREMENT_POINT_A),
                                "currents": [
                                    {"timestamp": "2026-01-01T12:00:00Z", "value": 450.1},
                                    {"timestamp": "2026-01-01T12:05:00Z", "value": 452.3},
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
    }
}

_FROM = datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC)
_TO = datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC)


class TestLatestCurrent:
    def test_omits_include_and_since_by_default(self):
        transport = RecordingTransport(_LATEST_AGGREGATE_ONLY)

        result = make_client(transport).get_latest_current(LINE_ID)

        assert transport.last_request.url.path == f"/grid_insights/v1/lines/{LINE_ID}/currents/latest"
        assert "include" not in transport.last_params
        assert "since" not in transport.last_params
        assert result.data.measurement_point_currents is None

    @pytest.mark.parametrize("include", ["measurement_points", CurrentInclude.MEASUREMENT_POINTS])
    def test_forwards_include_and_since(self, include):
        transport = RecordingTransport(_LATEST)

        make_client(transport).get_latest_current(
            LINE_ID, since=datetime.datetime(2026, 1, 1, 12, 30, tzinfo=datetime.UTC), include=include
        )

        assert transport.last_params["include"] == "measurement_points"
        assert transport.last_params["since"] == "2026-01-01T12:30:00Z"

    def test_rejects_unknown_include_value(self):
        transport = RecordingTransport(_LATEST)

        with pytest.raises(ValueError):
            make_client(transport).get_latest_current(LINE_ID, include="spans")
        assert transport.requests == []

    def test_parses_measurement_point_breakdown(self):
        result = make_client(RecordingTransport(_LATEST)).get_latest_current(LINE_ID, include="measurement_points")

        (span,) = result.data.measurement_point_currents
        assert span.span_id == SPAN_ID
        (span_phase,) = span.span_phases
        assert span_phase.span_phase_id == SPAN_PHASE_ID
        first, second = span_phase.measurement_points
        assert (first.measurement_point_id, first.value) == (MEASUREMENT_POINT_A, 450.1)
        assert first.timestamp == datetime.datetime(2026, 1, 1, 11, 58, tzinfo=datetime.UTC)
        assert (second.measurement_point_id, second.value) == (MEASUREMENT_POINT_B, 452.3)


class TestCurrents:
    def test_omits_include_by_default(self):
        transport = RecordingTransport(_HISTORICAL)

        make_client(transport).get_currents(LINE_ID, _FROM, _TO)

        assert transport.last_request.url.path == f"/grid_insights/v1/lines/{LINE_ID}/currents"
        assert transport.last_params["from_timestamp"] == "2026-01-01T00:00:00Z"
        assert "include" not in transport.last_params

    def test_forwards_include(self):
        transport = RecordingTransport(_HISTORICAL)

        make_client(transport).get_currents(LINE_ID, _FROM, _TO, include=CurrentInclude.MEASUREMENT_POINTS)

        assert transport.last_params["include"] == "measurement_points"

    def test_parses_measurement_point_time_series(self):
        result = make_client(RecordingTransport(_HISTORICAL)).get_currents(
            LINE_ID, _FROM, _TO, include="measurement_points"
        )

        (span,) = result.data.measurement_point_currents
        (span_phase,) = span.span_phases
        (measurement_point,) = span_phase.measurement_points
        assert measurement_point.measurement_point_id == MEASUREMENT_POINT_A
        assert [(c.timestamp.minute, c.value) for c in measurement_point.currents] == [(0, 450.1), (5, 452.3)]
