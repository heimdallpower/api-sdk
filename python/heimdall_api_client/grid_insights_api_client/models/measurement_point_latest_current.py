from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="MeasurementPointLatestCurrent")


@_attrs_define
class MeasurementPointLatestCurrent:
    """
    Attributes:
        measurement_point_id (UUID): The id of the measurement point. Example: 00000000-0000-0000-0000-000000000000.
        timestamp (datetime.datetime): Time (in UTC) when the current was measured. Example: 2024-07-01 12:00:00+00:00.
        value (float): The latest current measured at this measurement point. Example: 452.3.
    """

    measurement_point_id: UUID
    timestamp: datetime.datetime
    value: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        measurement_point_id = str(self.measurement_point_id)

        timestamp = self.timestamp.isoformat()

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "measurement_point_id": measurement_point_id,
                "timestamp": timestamp,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        measurement_point_id = UUID(d.pop("measurement_point_id"))

        timestamp = isoparse(d.pop("timestamp"))

        value = d.pop("value")

        measurement_point_latest_current = cls(
            measurement_point_id=measurement_point_id,
            timestamp=timestamp,
            value=value,
        )

        measurement_point_latest_current.additional_properties = d
        return measurement_point_latest_current

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
