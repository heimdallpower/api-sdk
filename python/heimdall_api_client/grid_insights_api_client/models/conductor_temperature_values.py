from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConductorTemperatureValues")


@_attrs_define
class ConductorTemperatureValues:
    """
    Attributes:
        timestamp (datetime.datetime): Time (in UTC) when the conductor temperature was measured. Example: 2024-07-01
            12:00:00+00:00.
        max_ (float): The maximum conductor temperature measured for the line at the given timestamp. Example: 68.7.
        max_at_span_id (UUID): The id of the span where the maximum conductor temperature was measured. Example:
            00000000-0000-0000-0000-000000000000.
        min_ (float | None | Unset): The minimum conductor temperature measured for the line at the given timestamp.
            Example: 55.2.
        min_at_span_id (None | Unset | UUID): The id of the span where the minimum conductor temperature was measured.
            Example: 00000000-0000-0000-0000-000000000000.
    """

    timestamp: datetime.datetime
    max_: float
    max_at_span_id: UUID
    min_: float | None | Unset = UNSET
    min_at_span_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        timestamp = self.timestamp.isoformat()

        max_ = self.max_

        max_at_span_id = str(self.max_at_span_id)

        min_: float | None | Unset
        if isinstance(self.min_, Unset):
            min_ = UNSET
        else:
            min_ = self.min_

        min_at_span_id: None | str | Unset
        if isinstance(self.min_at_span_id, Unset):
            min_at_span_id = UNSET
        elif isinstance(self.min_at_span_id, UUID):
            min_at_span_id = str(self.min_at_span_id)
        else:
            min_at_span_id = self.min_at_span_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timestamp": timestamp,
                "max": max_,
                "max_at_span_id": max_at_span_id,
            }
        )
        if min_ is not UNSET:
            field_dict["min"] = min_
        if min_at_span_id is not UNSET:
            field_dict["min_at_span_id"] = min_at_span_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        timestamp = isoparse(d.pop("timestamp"))

        max_ = d.pop("max")

        max_at_span_id = UUID(d.pop("max_at_span_id"))

        def _parse_min_(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        min_ = _parse_min_(d.pop("min", UNSET))

        def _parse_min_at_span_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                min_at_span_id_type_0 = UUID(data)

                return min_at_span_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        min_at_span_id = _parse_min_at_span_id(d.pop("min_at_span_id", UNSET))

        conductor_temperature_values = cls(
            timestamp=timestamp,
            max_=max_,
            max_at_span_id=max_at_span_id,
            min_=min_,
            min_at_span_id=min_at_span_id,
        )

        conductor_temperature_values.additional_properties = d
        return conductor_temperature_values

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
