"""
Unit tests for `at_span_id` on the current and apparent power endpoints: the span where
the line current was measured is parsed on the latest and historical responses.
"""

import datetime
from uuid import UUID

from tests.unit._fake_transport import RecordingTransport, make_client

LINE_ID = UUID("d67d2205-6629-4bbd-aa9f-436bf22842ad")
SPAN_A = UUID("11111111-1111-1111-1111-111111111111")
SPAN_B = UUID("22222222-2222-2222-2222-222222222222")

_FROM = datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC)
_TO = datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC)


def _point(minute: int, value: float, span: UUID) -> dict:
    return {"timestamp": f"2026-01-01T12:{minute:02d}:00Z", "value": value, "at_span_id": str(span)}


def test_parses_at_span_id_on_latest_current():
    body = {"data": {"metric": "Current", "unit": "Ampere", "current": _point(0, 452.3, SPAN_A)}}

    result = make_client(RecordingTransport(body)).get_latest_current(LINE_ID)

    assert result.data.current.at_span_id == SPAN_A


def test_parses_at_span_id_on_historical_currents():
    body = {
        "data": {
            "metric": "Current",
            "unit": "Ampere",
            "currents": [_point(0, 452.3, SPAN_A), _point(5, 460.0, SPAN_B)],
        }
    }

    result = make_client(RecordingTransport(body)).get_currents(LINE_ID, _FROM, _TO)

    assert [current.at_span_id for current in result.data.currents] == [SPAN_A, SPAN_B]


def test_parses_at_span_id_on_latest_apparent_power():
    body = {"data": {"metric": "Apparent power", "unit": "MVA", "apparent_power": _point(0, 156.7, SPAN_B)}}

    result = make_client(RecordingTransport(body)).get_latest_apparent_power(LINE_ID)

    assert result.data.apparent_power.at_span_id == SPAN_B


def test_parses_at_span_id_on_historical_apparent_powers():
    body = {
        "data": {
            "metric": "Apparent power",
            "unit": "MVA",
            "apparent_powers": [_point(0, 156.7, SPAN_A), _point(5, 159.4, SPAN_B)],
        }
    }

    result = make_client(RecordingTransport(body)).get_apparent_power(LINE_ID, _FROM, _TO)

    assert [apparent_power.at_span_id for apparent_power in result.data.apparent_powers] == [SPAN_A, SPAN_B]
