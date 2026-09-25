"""
Reproduces an inconsistency between the line-level current and the per-measurement-point
breakdown returned in the same `get_currents(..., include="measurement_points")` response.

The line current is documented as the maximum current measured on the line at a given
timestamp. On a fixed, settled window the two series disagree:

- the line value at `t` often equals a measurement point's reading one sample (about
  180 s) before `t`, while that measurement point's reading at `t` is different;
- at other timestamps the line value is exactly twice a single measurement point's reading.

The window is fixed in the past, so the response is identical on every run and the
failures are deterministic.
"""

import datetime
from uuid import UUID

import pytest

from heimdall_api_client.grid_insights_api_client.models.current_include import CurrentInclude

# "Heimdall Power Line", the line the .NET integration tests use.
_LINE_ID = UUID("d67d2205-6629-4bbd-aa9f-436bf22842ad")

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


def _fetch(api_client, from_timestamp, to_timestamp):
    data = api_client.get_currents(
        _LINE_ID, from_timestamp, to_timestamp, include=CurrentInclude.MEASUREMENT_POINTS
    ).data
    readings = {
        mp.measurement_point_id: {point.timestamp: point.value for point in mp.currents}
        for span in data.measurement_point_currents
        for span_phase in span.span_phases
        for mp in span_phase.measurement_points
    }
    if not data.currents:
        pytest.skip(f"No current on line {_LINE_ID} in [{from_timestamp}, {to_timestamp}]")
    return data.currents, readings


@pytest.mark.integration
@pytest.mark.parametrize(("from_timestamp", "to_timestamp"), _WINDOWS)
def test_line_current_should_be_the_max_of_measurement_points_at_the_same_timestamp(
    api_client, from_timestamp, to_timestamp
):
    line_currents, readings = _fetch(api_client, from_timestamp, to_timestamp)

    mismatches = []
    for point in line_currents:
        at_t = [series[point.timestamp] for series in readings.values() if point.timestamp in series]
        expected = max(at_t) if at_t else None
        if expected is None or point.value != pytest.approx(expected, abs=1e-6):
            mismatches.append(
                f"{point.timestamp.isoformat()}: line {point.value:.2f} A, max measurement point {expected}"
            )

    assert not mismatches, f"{len(mismatches)}/{len(line_currents)} line points differ:\n" + "\n".join(mismatches)


@pytest.mark.integration
@pytest.mark.parametrize(("from_timestamp", "to_timestamp"), _WINDOWS[:1])
def test_line_current_should_not_repeat_the_previous_measurement_point_reading(
    api_client, from_timestamp, to_timestamp
):
    line_currents, readings = _fetch(api_client, from_timestamp, to_timestamp)

    lagging = []
    for point in line_currents:
        for mp_id, series in readings.items():
            timestamps = sorted(series)
            if point.timestamp not in series:
                continue
            index = timestamps.index(point.timestamp)
            if index == 0:
                continue
            previous = series[timestamps[index - 1]]
            current = series[point.timestamp]
            if point.value == pytest.approx(previous, abs=1e-6) and point.value != pytest.approx(current, abs=1e-6):
                lagging.append(
                    f"{point.timestamp.isoformat()}: line {point.value:.2f} A equals measurement point {mp_id} "
                    f"at {timestamps[index - 1].isoformat()}, but it reads {current:.2f} A at this timestamp"
                )

    assert not lagging, f"{len(lagging)}/{len(line_currents)} line points lag one sample:\n" + "\n".join(lagging)
