"""
Unit tests for get_instrumented_lines(): only lines with an active measurement point
(unregistered timestamp unset or in the future) are returned, each mapped to its
facility, with only the active points.
"""

import datetime
from uuid import UUID

from heimdall_api_client import InstrumentedLine
from heimdall_api_client.assets import instrumented_lines
from heimdall_api_client.assets_api_client.models.assets import Assets
from tests.unit._fake_transport import RecordingTransport, make_client

FACILITY_WITH_ACTIVE = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
FACILITY_WITH_FUTURE_UNREGISTRATION = UUID("dddddddd-dddd-dddd-dddd-dddddddddddd")
LINE_WITH_ACTIVE = UUID("a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1")
LINE_WITH_FUTURE_UNREGISTRATION = UUID("d1d1d1d1-d1d1-d1d1-d1d1-d1d1d1d1d1d1")
ACTIVE_ON_FIRST_SPAN = UUID("44444444-4444-4444-4444-444444444444")
ACTIVE_ON_SECOND_SPAN = UUID("77777777-7777-7777-7777-777777777777")
UNREGISTERS_IN_FUTURE = UUID("88888888-8888-8888-8888-888888888888")

_FUTURE = (datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ")


def _line(line_id: str, name: str, spans: list[dict], available_forecast_hours: int = 72) -> dict:
    return {"id": line_id, "name": name, "available_forecast_hours": available_forecast_hours, "spans": spans}


def _span(span_id: str, phase_id: str, measurement_points: list[dict]) -> dict:
    return {"id": span_id, "span_phases": [{"id": phase_id, "measurement_points": measurement_points}]}


def _point(point_id, registered: str, unregistered: str | None = None, sub_conductor_number: int = 1) -> dict:
    return {
        "id": str(point_id),
        "sub_conductor_number": sub_conductor_number,
        "registered_timestamp": registered,
        "unregistered_timestamp": unregistered,
    }


def _facility(facility_id, name: str, line: dict | None, nominal_voltage: float = 132000) -> dict:
    return {"id": str(facility_id), "name": name, "nominal_voltage": nominal_voltage, "components": [], "line": line}


_ASSETS = {
    "data": {
        "grid_owners": [
            {
                "name": "Grid owner A",
                "facilities": [
                    _facility(
                        FACILITY_WITH_ACTIVE,
                        "Facility with active point",
                        _line(
                            str(LINE_WITH_ACTIVE),
                            "Line with active point",
                            [
                                _span(
                                    "11111111-1111-1111-1111-111111111111",
                                    "33333333-3333-3333-3333-333333333333",
                                    [
                                        _point(ACTIVE_ON_FIRST_SPAN, "2026-03-15T09:30:00Z"),
                                        _point(
                                            "55555555-5555-5555-5555-555555555555",
                                            "2024-07-01T12:00:00Z",
                                            "2026-03-15T09:00:00Z",
                                        ),
                                    ],
                                ),
                                _span(
                                    "22222222-2222-2222-2222-222222222222",
                                    "66666666-6666-6666-6666-666666666666",
                                    [_point(ACTIVE_ON_SECOND_SPAN, "2025-01-01T00:00:00Z", sub_conductor_number=2)],
                                ),
                            ],
                        ),
                    ),
                    _facility(
                        "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
                        "Facility with only retired points",
                        _line(
                            "b1b1b1b1-b1b1-b1b1-b1b1-b1b1b1b1b1b1",
                            "Decommissioned line",
                            [
                                _span(
                                    "b2b2b2b2-b2b2-b2b2-b2b2-b2b2b2b2b2b2",
                                    "b3b3b3b3-b3b3-b3b3-b3b3-b3b3b3b3b3b3",
                                    [
                                        _point(
                                            "b4b4b4b4-b4b4-b4b4-b4b4-b4b4b4b4b4b4",
                                            "2024-07-01T12:00:00Z",
                                            "2025-07-01T12:00:00Z",
                                        )
                                    ],
                                )
                            ],
                        ),
                    ),
                    _facility(
                        "cccccccc-cccc-cccc-cccc-cccccccccccc",
                        "Facility without neurons",
                        _line(
                            "c1c1c1c1-c1c1-c1c1-c1c1-c1c1c1c1c1c1",
                            "Line without neurons",
                            [_span("c2c2c2c2-c2c2-c2c2-c2c2-c2c2c2c2c2c2", "c3c3c3c3-c3c3-c3c3-c3c3-c3c3c3c3c3c3", [])],
                        ),
                    ),
                    _facility("eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee", "Facility without line", None, nominal_voltage=0),
                ],
            },
            {
                "name": "Grid owner B",
                "facilities": [
                    _facility(
                        FACILITY_WITH_FUTURE_UNREGISTRATION,
                        "Facility with future unregistration",
                        _line(
                            str(LINE_WITH_FUTURE_UNREGISTRATION),
                            "Line with future unregistration",
                            [
                                _span(
                                    "d2d2d2d2-d2d2-d2d2-d2d2-d2d2d2d2d2d2",
                                    "d3d3d3d3-d3d3-d3d3-d3d3-d3d3d3d3d3d3",
                                    [_point(UNREGISTERS_IN_FUTURE, "2025-01-01T00:00:00Z", _FUTURE)],
                                )
                            ],
                            available_forecast_hours=48,
                        ),
                        nominal_voltage=66000,
                    )
                ],
            },
        ]
    }
}


def _fetch() -> tuple[list[InstrumentedLine], RecordingTransport]:
    transport = RecordingTransport(_ASSETS)
    return make_client(transport).get_instrumented_lines(), transport


def test_requests_assets_once():
    _, transport = _fetch()

    assert len(transport.requests) == 1
    assert transport.last_request.url.path == "/assets/v1/assets"


def test_keeps_only_lines_with_active_measurement_points():
    lines, _ = _fetch()

    assert [instrumented.line.id for instrumented in lines] == [LINE_WITH_ACTIVE, LINE_WITH_FUTURE_UNREGISTRATION]


def test_maps_each_line_to_its_facility():
    first, second = _fetch()[0]

    assert first.facility.id == FACILITY_WITH_ACTIVE
    assert first.facility.name == "Facility with active point"
    assert first.facility.nominal_voltage == 132000
    assert first.line.name == "Line with active point"
    assert first.facility.line is first.line
    assert second.facility.id == FACILITY_WITH_FUTURE_UNREGISTRATION
    assert second.facility.name == "Facility with future unregistration"
    assert second.line.available_forecast_hours == 48
    assert second.facility.line is second.line


def test_returns_only_active_measurement_points_across_all_spans():
    lines, _ = _fetch()

    line = next(instrumented for instrumented in lines if instrumented.line.id == LINE_WITH_ACTIVE)
    first, second = line.active_measurement_points
    assert first.id == ACTIVE_ON_FIRST_SPAN
    assert first.unregistered_timestamp is None
    assert second.id == ACTIVE_ON_SECOND_SPAN
    assert second.sub_conductor_number == 2


def test_treats_future_unregistered_timestamp_as_active():
    lines, _ = _fetch()

    line = next(instrumented for instrumented in lines if instrumented.line.id == LINE_WITH_FUTURE_UNREGISTRATION)
    (point,) = line.active_measurement_points
    assert point.id == UNREGISTERS_IN_FUTURE
    assert point.unregistered_timestamp > datetime.datetime.now(datetime.UTC)


def test_instrumented_lines_matches_client_helper_when_called_on_assets():
    assets = make_client(RecordingTransport(_ASSETS)).get_assets().data

    lines = instrumented_lines(assets)

    assert [instrumented.line.id for instrumented in lines] == [LINE_WITH_ACTIVE, LINE_WITH_FUTURE_UNREGISTRATION]
    assert [instrumented.facility.id for instrumented in lines] == [
        FACILITY_WITH_ACTIVE,
        FACILITY_WITH_FUTURE_UNREGISTRATION,
    ]


def test_instrumented_lines_is_empty_when_no_grid_owners():
    assert instrumented_lines(Assets(grid_owners=[])) == []
