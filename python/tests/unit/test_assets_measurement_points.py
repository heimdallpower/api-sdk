"""
Unit tests for measurement points in the assets hierarchy: active and retired
points parse, and a span phase without a Neuron has an empty list.
"""

import datetime
from uuid import UUID

from heimdall_api_client.assets_api_client.types import Unset
from tests.unit._fake_transport import RecordingTransport, make_client

ACTIVE = UUID("44444444-4444-4444-4444-444444444444")
RETIRED = UUID("55555555-5555-5555-5555-555555555555")

_ASSETS = {
    "data": {
        "grid_owners": [
            {
                "name": "Grid owner A",
                "facilities": [
                    {
                        "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                        "name": "Facility A",
                        "nominal_voltage": 132000,
                        "operational_voltage": None,
                        "components": [],
                        "line": {
                            "id": "d67d2205-6629-4bbd-aa9f-436bf22842ad",
                            "name": "Line A",
                            "available_forecast_hours": 72,
                            "spans": [
                                {
                                    "id": "11111111-1111-1111-1111-111111111111",
                                    "mast_name_a": "Mast A",
                                    "mast_name_b": "Mast B",
                                    "span_phases": [
                                        {
                                            "id": "33333333-3333-3333-3333-333333333333",
                                            "name": "Phase A",
                                            "measurement_points": [
                                                {
                                                    "id": str(ACTIVE),
                                                    "sub_conductor_number": 1,
                                                    "registered_timestamp": "2026-03-15T09:30:00Z",
                                                    "unregistered_timestamp": None,
                                                },
                                                {
                                                    "id": str(RETIRED),
                                                    "sub_conductor_number": 1,
                                                    "registered_timestamp": "2024-07-01T12:00:00.001Z",
                                                    "unregistered_timestamp": "2026-03-15T09:00:00Z",
                                                },
                                            ],
                                        },
                                        {
                                            "id": "66666666-6666-6666-6666-666666666666",
                                            "name": "Phase B",
                                            "measurement_points": [],
                                        },
                                    ],
                                }
                            ],
                        },
                    }
                ],
            }
        ]
    }
}


def _span_phases():
    result = make_client(RecordingTransport(_ASSETS)).get_assets()
    return result.data.grid_owners[0].facilities[0].line.spans[0].span_phases


def test_parses_active_and_retired_measurement_points():
    active, retired = _span_phases()[0].measurement_points

    assert active.id == ACTIVE
    assert active.sub_conductor_number == 1
    assert active.registered_timestamp == datetime.datetime(2026, 3, 15, 9, 30, tzinfo=datetime.UTC)
    assert active.unregistered_timestamp is None or isinstance(active.unregistered_timestamp, Unset)
    assert retired.id == RETIRED
    assert retired.unregistered_timestamp == datetime.datetime(2026, 3, 15, 9, 0, tzinfo=datetime.UTC)


def test_span_phase_without_neuron_has_no_measurement_points():
    assert _span_phases()[1].measurement_points == []
