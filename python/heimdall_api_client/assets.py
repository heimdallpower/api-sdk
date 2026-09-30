from __future__ import annotations

import dataclasses
import datetime

from heimdall_api_client.assets_api_client.api.assets import assets_v1_get_assets
from heimdall_api_client.assets_api_client.client import AuthenticatedClient
from heimdall_api_client.assets_api_client.models.assets import Assets
from heimdall_api_client.assets_api_client.models.assets_v1_get_assets_response_200 import (
    AssetsV1GetAssetsResponse200,
)
from heimdall_api_client.assets_api_client.models.facility import Facility
from heimdall_api_client.assets_api_client.models.line_type_0 import LineType0
from heimdall_api_client.assets_api_client.models.measurement_point import MeasurementPoint
from heimdall_api_client.errors import HeimdallApiError, body_preview


def get_assets(client: AuthenticatedClient, x_region: str) -> AssetsV1GetAssetsResponse200:
    response = assets_v1_get_assets.sync_detailed(client=client, x_region=x_region)
    if response.status_code != 200:
        status = int(response.status_code)
        raise HeimdallApiError(
            f"Error fetching assets: {status} {response.status_code.phrase} - {body_preview(response.content)}",
            status_code=status,
        )
    return response.parsed


@dataclasses.dataclass(frozen=True)
class InstrumentedLine:
    """
    A line with at least one active measurement point, together with its facility.

    Attributes
    ----------
    facility:
        The facility the line belongs to. Use its id for facility endpoints such as circuit ratings.
    line:
        The line. Use its id for line endpoints such as currents and DLR.
    active_measurement_points:
        The line's active measurement points across all spans and span phases: those whose
        ``unregistered_timestamp`` is unset or in the future. Never empty.
    """

    facility: Facility
    line: LineType0
    active_measurement_points: list[MeasurementPoint]


def _is_active(measurement_point: MeasurementPoint, now: datetime.datetime) -> bool:
    unregistered = measurement_point.unregistered_timestamp
    if not isinstance(unregistered, datetime.datetime):
        return True
    if unregistered.tzinfo is None:
        unregistered = unregistered.replace(tzinfo=datetime.UTC)
    return unregistered > now


def instrumented_lines(assets: Assets) -> list[InstrumentedLine]:
    """
    Returns the lines that have at least one active measurement point, with their facility.

    A measurement point is active while its ``unregistered_timestamp`` is unset or in the future.
    Lines with no measurement points, or only retired ones, are left out: data endpoints return
    404 or no data for them.

    Example::

        for instrumented in instrumented_lines(client.get_assets().data):
            current = client.get_latest_current(instrumented.line.id)
    """
    now = datetime.datetime.now(datetime.UTC)
    result: list[InstrumentedLine] = []
    for grid_owner in assets.grid_owners:
        for facility in grid_owner.facilities:
            line = facility.line
            if not isinstance(line, LineType0):
                continue
            active = [
                measurement_point
                for span in line.spans
                for span_phase in span.span_phases
                for measurement_point in span_phase.measurement_points
                if _is_active(measurement_point, now)
            ]
            if active:
                result.append(InstrumentedLine(facility=facility, line=line, active_measurement_points=active))
    return result
