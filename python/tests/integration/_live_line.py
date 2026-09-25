"""Helpers shared by the integration tests that need a line with recent data."""

import dataclasses
import math
from uuid import UUID

import pytest

AMPERE_UNIT = "Ampere"
MVA_UNIT = "MVA"


@dataclasses.dataclass(frozen=True)
class LiveLine:
    """A line with recent data, and the ids of its facility and asset hierarchy from get_assets()."""

    line_id: UUID
    facility_id: UUID
    nominal_voltage: float
    operational_voltage: float | None
    span_ids: frozenset[UUID]
    span_phase_ids: frozenset[UUID]
    measurement_point_ids: frozenset[UUID]

    @property
    def apparent_power_voltage(self) -> float:
        """The voltage the API converts amperes to MVA with: operational when set and positive, else nominal."""
        if self.operational_voltage is not None and self.operational_voltage > 0:
            return self.operational_voltage
        return self.nominal_voltage

    def assert_is_apparent_power_of(self, mva: float, amperes: float, context: str) -> None:
        """Asserts S = sqrt(3) * V * I / 1e6 at this line's voltage."""
        voltage = self.apparent_power_voltage
        expected = math.sqrt(3) * voltage * amperes / 1_000_000
        assert mva == pytest.approx(expected, rel=5e-3, abs=1e-6), (
            f"{context}: {mva} MVA should equal sqrt(3) * {voltage} V * {amperes} A = {expected} MVA"
        )
