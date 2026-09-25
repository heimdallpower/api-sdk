"""
Checks that the line-level current can be reconciled with the per-measurement-point
breakdown returned in the same `get_currents(..., include="measurement_points")` response.

Observed behaviour, which the API documentation does not describe:

- A line value at `t` is the maximum over the preceding five minutes, not the maximum at `t`.
  A point is emitted only when that maximum changes, and it is stamped with the newest reading.
- The line value is a phase current: each measurement point reading is multiplied by the
  number of sub-conductors of its span phase. The breakdown returns the raw per-sub-conductor
  reading, and the assets hierarchy does not expose the number of sub-conductors, so a client
  cannot reproduce the line value from public data.

The window is fixed in the past, so the response is identical on every run and the result
is deterministic.
"""

import datetime
from uuid import UUID

import pytest

from heimdall_api_client.grid_insights_api_client.models.current_include import CurrentInclude

# "Heimdall Power Line", the line the .NET integration tests use.
_LINE_ID = UUID("d67d2205-6629-4bbd-aa9f-436bf22842ad")
_LINE_CURRENT_WINDOW = datetime.timedelta(minutes=5)

_WINDOWS = [
    pytest.param(
        datetime.datetime(2026, 9, 25, 7, 0, tzinfo=datetime.UTC),
        datetime.datetime(2026, 9, 25, 8, 0, tzinfo=datetime.UTC),
        id="2026-09-25T07",
    ),
    pytest.param(
        datetime.datetime(2026, 9, 24, 0, 0, tzinfo=datetime.UTC),
        datetime.datetime(2026, 9, 24, 1, 0, tzinfo=datetime.UTC),
        id="2026-09-24T00",
    ),
]


def _number_of_sub_conductors(api_client):
    """Number of sub-conductors per measurement point, as published by the assets endpoint."""
    counts = {}
    for grid_owner in api_client.get_assets().data.grid_owners:
        for facility in grid_owner.facilities:
            if not facility.line or facility.line.id != _LINE_ID:
                continue
            for span in facility.line.spans:
                for span_phase in span.span_phases:
                    for mp in span_phase.measurement_points:
                        counts[mp.id] = mp.additional_properties.get("number_of_sub_conductors")
    return counts


@pytest.mark.integration
@pytest.mark.parametrize(("from_timestamp", "to_timestamp"), _WINDOWS)
def test_line_current_should_be_reconcilable_from_the_measurement_point_breakdown(
    api_client, from_timestamp, to_timestamp
):
    sub_conductors = _number_of_sub_conductors(api_client)
    missing = sorted(str(mp_id) for mp_id, count in sub_conductors.items() if count is None)
    assert not missing, (
        "assets expose no number_of_sub_conductors, but the line current multiplies each "
        f"per-sub-conductor reading by it; measurement points without it: {missing}"
    )

    # Fetch five extra minutes so the first line points have their full window.
    data = api_client.get_currents(
        _LINE_ID, from_timestamp - _LINE_CURRENT_WINDOW, to_timestamp, include=CurrentInclude.MEASUREMENT_POINTS
    ).data
    phase_readings = [
        (point.timestamp, point.value * sub_conductors[mp.measurement_point_id])
        for span in data.measurement_point_currents
        for span_phase in span.span_phases
        for mp in span_phase.measurement_points
        for point in mp.currents
    ]

    mismatches = []
    for point in (p for p in data.currents if p.timestamp >= from_timestamp):
        window = [v for ts, v in phase_readings if point.timestamp - _LINE_CURRENT_WINDOW <= ts <= point.timestamp]
        expected = max(window) if window else None
        if expected is None or point.value != pytest.approx(expected, abs=1e-6):
            mismatches.append(f"{point.timestamp.isoformat()}: line {point.value:.2f} A, window max {expected}")

    assert not mismatches, "\n".join(mismatches)
