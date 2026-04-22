from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CircuitRating")


@_attrs_define
class CircuitRating:
    """
    Attributes:
        timestamp (datetime.datetime): Time (in UTC) when the circuit rating was calculated. Example: 2024-07-01
            12:00:00.001000+00:00.
        value (float): The minimum calculated ampacity (in amperes) at the given timestamp. Example: 375.4.
        at_facility_component_id (None | Unset | UUID): Identifier of the facility component that determines the circuit
            rating at this timestamp. When null, the circuit rating is not limited by a facility component. Example:
            00000000-0000-0000-0000-000000000000.
        is_fallback (bool): Indicates whether the Heimdall DLR is a fallback value. Only applies to grid owners opting in for this feature. Example: false.
    """

    timestamp: datetime.datetime
    value: float
    is_fallback: bool
    at_facility_component_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        timestamp = self.timestamp.isoformat()

        value = self.value

        at_facility_component_id: None | str | Unset
        if isinstance(self.at_facility_component_id, Unset):
            at_facility_component_id = UNSET
        elif isinstance(self.at_facility_component_id, UUID):
            at_facility_component_id = str(self.at_facility_component_id)
        else:
            at_facility_component_id = self.at_facility_component_id

        is_fallback = self.is_fallback

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timestamp": timestamp,
                "value": value,
                "is_fallback": is_fallback,
            }
        )
        if at_facility_component_id is not UNSET:
            field_dict["at_facility_component_id"] = at_facility_component_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        timestamp = isoparse(d.pop("timestamp"))

        value = d.pop("value")

        def _parse_at_facility_component_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                at_facility_component_id_type_0 = UUID(data)

                return at_facility_component_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        at_facility_component_id = _parse_at_facility_component_id(d.pop("at_facility_component_id", UNSET))

        is_fallback = d.pop("is_fallback")

        circuit_rating = cls(
            timestamp=timestamp,
            value=value,
            at_facility_component_id=at_facility_component_id,
            is_fallback=is_fallback,
        )

        circuit_rating.additional_properties = d
        return circuit_rating

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
