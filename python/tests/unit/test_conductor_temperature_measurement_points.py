"""
Unit tests for the conductor temperature endpoints: the query string the client
sends for each option (`since`, `unit_system`, `include`) and parsing of the
per-measurement-point breakdown and the span ids of the line aggregate.
"""

import datetime
from uuid import UUID

import pytest

from heimdall_api_client.grid_insights_api_client.models.conductor_temperature_include import (
    ConductorTemperatureInclude,
)
from heimdall_api_client.grid_insights_api_client.types import Unset
from tests.unit._fake_transport import RecordingTransport, make_client

LINE_ID = UUID("d67d2205-6629-4bbd-aa9f-436bf22842ad")
MAX_SPAN_ID = UUID("11111111-1111-1111-1111-111111111111")
MIN_SPAN_ID = UUID("22222222-2222-2222-2222-222222222222")
SPAN_PHASE_ID = UUID("33333333-3333-3333-3333-333333333333")
MEASUREMENT_POINT_A = UUID("44444444-4444-4444-4444-444444444444")
MEASUREMENT_POINT_B = UUID("55555555-5555-5555-5555-555555555555")

_LATEST_AGGREGATE_ONLY = {
    "data": {
        "metric": "Conductor temperature",
        "unit": "C",
        "conductor_temperature": {
            "timestamp": "2026-01-01T12:00:00Z",
            "max": 68.7,
            "min": 55.2,
            "max_at_span_id": str(MAX_SPAN_ID),
            "min_at_span_id": str(MIN_SPAN_ID),
        },
        "measurement_point_temperatures": None,
    }
}

_LATEST_WITH_MEASUREMENT_POINTS = {
    "data": {
        "metric": "Conductor temperature",
        "unit": "C",
        "conductor_temperature": {
            "timestamp": "2026-01-01T12:00:00Z",
            "max": 68.7,
            "min": None,
            "max_at_span_id": str(MAX_SPAN_ID),
            "min_at_span_id": None,
        },
        "measurement_point_temperatures": [
            {
                "span_id": str(MAX_SPAN_ID),
                "span_phases": [
                    {
                        "span_phase_id": str(SPAN_PHASE_ID),
                        "measurement_points": [
                            {
                                "measurement_point_id": str(MEASUREMENT_POINT_A),
                                "timestamp": "2026-01-01T11:58:00Z",
                                "value": 64.3,
                            },
                            {
                                "measurement_point_id": str(MEASUREMENT_POINT_B),
                                "timestamp": "2026-01-01T11:59:00Z",
                                "value": 68.7,
                            },
                        ],
                    }
                ],
            }
        ],
    }
}

_HISTORICAL_WITH_MEASUREMENT_POINTS = {
    "data": {
        "metric": "Conductor temperature",
        "unit": "C",
        "conductor_temperatures": [
            {
                "timestamp": "2026-01-01T12:00:00Z",
                "max": 68.7,
                "min": 55.2,
                "max_at_span_id": str(MAX_SPAN_ID),
                "min_at_span_id": str(MIN_SPAN_ID),
            }
        ],
        "measurement_point_temperatures": [
            {
                "span_id": str(MAX_SPAN_ID),
                "span_phases": [
                    {
                        "span_phase_id": str(SPAN_PHASE_ID),
                        "measurement_points": [
                            {
                                "measurement_point_id": str(MEASUREMENT_POINT_A),
                                "temperatures": [
                                    {"timestamp": "2026-01-01T12:00:00Z", "value": 64.3},
                                    {"timestamp": "2026-01-01T12:05:00Z", "value": 65.1},
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


class TestLatestConductorTemperatureRequest:
    def test_omits_optional_parameters_by_default(self):
        transport = RecordingTransport(_LATEST_AGGREGATE_ONLY)

        make_client(transport).get_latest_conductor_temperature(LINE_ID)

        assert transport.last_request.url.path == f"/grid_insights/v1/lines/{LINE_ID}/conductor_temperatures/latest"
        assert "include" not in transport.last_params
        assert "since" not in transport.last_params
        assert "unit_system" not in transport.last_params

    @pytest.mark.parametrize("include", ["measurement_points", ConductorTemperatureInclude.MEASUREMENT_POINTS])
    def test_forwards_include_as_string_or_enum(self, include):
        transport = RecordingTransport(_LATEST_WITH_MEASUREMENT_POINTS)

        make_client(transport).get_latest_conductor_temperature(LINE_ID, include=include)

        assert transport.last_params["include"] == "measurement_points"

    def test_forwards_since_and_unit_system(self):
        transport = RecordingTransport(_LATEST_AGGREGATE_ONLY)
        oslo = datetime.timezone(datetime.timedelta(hours=1))

        make_client(transport).get_latest_conductor_temperature(
            LINE_ID, since=datetime.datetime(2026, 1, 1, 13, 30, tzinfo=oslo), unit_system="imperial"
        )

        assert transport.last_params["since"] == "2026-01-01T12:30:00Z"
        assert transport.last_params["unit_system"] == "imperial"

    def test_rejects_unknown_include_value(self):
        transport = RecordingTransport(_LATEST_AGGREGATE_ONLY)

        with pytest.raises(ValueError):
            make_client(transport).get_latest_conductor_temperature(LINE_ID, include="spans")
        assert transport.requests == []


class TestLatestConductorTemperatureResponse:
    def test_parses_span_ids_of_the_aggregate(self):
        result = make_client(RecordingTransport(_LATEST_AGGREGATE_ONLY)).get_latest_conductor_temperature(LINE_ID)

        assert result.data.conductor_temperature.max_at_span_id == MAX_SPAN_ID
        assert result.data.conductor_temperature.min_at_span_id == MIN_SPAN_ID

    def test_measurement_point_temperatures_is_none_when_not_included(self):
        result = make_client(RecordingTransport(_LATEST_AGGREGATE_ONLY)).get_latest_conductor_temperature(LINE_ID)

        assert result.data.measurement_point_temperatures is None

    def test_parses_measurement_point_breakdown(self):
        result = make_client(RecordingTransport(_LATEST_WITH_MEASUREMENT_POINTS)).get_latest_conductor_temperature(
            LINE_ID, include="measurement_points"
        )

        assert result.data.conductor_temperature.min_ is None
        assert result.data.conductor_temperature.min_at_span_id is None
        (span,) = result.data.measurement_point_temperatures
        assert span.span_id == MAX_SPAN_ID
        (span_phase,) = span.span_phases
        assert span_phase.span_phase_id == SPAN_PHASE_ID
        first, second = span_phase.measurement_points
        assert first.measurement_point_id == MEASUREMENT_POINT_A
        assert first.timestamp == datetime.datetime(2026, 1, 1, 11, 58, tzinfo=datetime.UTC)
        assert first.value == 64.3
        assert second.measurement_point_id == MEASUREMENT_POINT_B
        assert second.value == 68.7


class TestConductorTemperaturesRequest:
    def test_omits_include_by_default(self):
        transport = RecordingTransport(_HISTORICAL_WITH_MEASUREMENT_POINTS)

        make_client(transport).get_conductor_temperatures(LINE_ID, _FROM, _TO)

        assert transport.last_request.url.path == f"/grid_insights/v1/lines/{LINE_ID}/conductor_temperatures"
        assert transport.last_params["from_timestamp"] == "2026-01-01T00:00:00Z"
        assert transport.last_params["to_timestamp"] == "2026-01-02T00:00:00Z"
        assert "include" not in transport.last_params

    def test_forwards_include(self):
        transport = RecordingTransport(_HISTORICAL_WITH_MEASUREMENT_POINTS)

        make_client(transport).get_conductor_temperatures(
            LINE_ID, _FROM, _TO, include=ConductorTemperatureInclude.MEASUREMENT_POINTS
        )

        assert transport.last_params["include"] == "measurement_points"


class TestConductorTemperaturesResponse:
    def test_parses_measurement_point_time_series_and_span_ids(self):
        result = make_client(RecordingTransport(_HISTORICAL_WITH_MEASUREMENT_POINTS)).get_conductor_temperatures(
            LINE_ID, _FROM, _TO, include="measurement_points"
        )

        (reading,) = result.data.conductor_temperatures
        assert reading.max_at_span_id == MAX_SPAN_ID
        assert reading.min_at_span_id == MIN_SPAN_ID
        (span,) = result.data.measurement_point_temperatures
        (span_phase,) = span.span_phases
        (measurement_point,) = span_phase.measurement_points
        assert measurement_point.measurement_point_id == MEASUREMENT_POINT_A
        assert [(t.timestamp.minute, t.value) for t in measurement_point.temperatures] == [(0, 64.3), (5, 65.1)]

    def test_measurement_point_temperatures_is_unset_or_none_when_field_absent(self):
        body = {"data": {**_HISTORICAL_WITH_MEASUREMENT_POINTS["data"]}}
        del body["data"]["measurement_point_temperatures"]

        result = make_client(RecordingTransport(body)).get_conductor_temperatures(LINE_ID, _FROM, _TO)

        assert result.data.measurement_point_temperatures is None or isinstance(
            result.data.measurement_point_temperatures, Unset
        )
