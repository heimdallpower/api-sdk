from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="MaxIcingTension")


@_attrs_define
class MaxIcingTension:
    """
    Attributes:
        timestamp (datetime.datetime): Time (in UTC) when the measurement was taken. Example: 2024-07-01 12:00:00+00:00.
        span_phase_id (UUID): The id of the span phase. Example: 00000000-0000-0000-0000-000000000000.
        value (float): The numerical value of the measurement.
        unit (str): The unit of measurement.
    """

    timestamp: datetime.datetime
    span_phase_id: UUID
    value: float
    unit: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        timestamp = self.timestamp.isoformat()

        span_phase_id = str(self.span_phase_id)

        value = self.value

        unit = self.unit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timestamp": timestamp,
                "span_phase_id": span_phase_id,
                "value": value,
                "unit": unit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        timestamp = isoparse(d.pop("timestamp"))

        span_phase_id = UUID(d.pop("span_phase_id"))

        value = d.pop("value")

        unit = d.pop("unit")

        max_icing_tension = cls(
            timestamp=timestamp,
            span_phase_id=span_phase_id,
            value=value,
            unit=unit,
        )

        max_icing_tension.additional_properties = d
        return max_icing_tension

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
