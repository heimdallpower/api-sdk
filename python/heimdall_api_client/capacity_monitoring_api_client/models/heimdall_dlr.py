from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="HeimdallDlr")


@_attrs_define
class HeimdallDlr:
    """
    Attributes:
        timestamp (datetime.datetime): Time (in UTC) when the Heimdall DLR was calculated. Example: 2024-07-01
            12:00:00.001000+00:00.
        value (float): The latest Heimdall DLR value at the given timestamp. The unit of this value is given by the
            sibling `unit` field on the response:
              - When `quantity=current` (default) → amperes.
              - When `quantity=apparent_power` → MVA.
             Example: 375.4.
        at_span_id (UUID): Identifier of the span at which the lowest ampacity was calculated. Example:
            00000000-0000-0000-0000-000000000000.
        is_fallback (bool): Indicates whether the Heimdall DLR is a fallback value. Only applies to grid owners opting
            in for this feature.
    """

    timestamp: datetime.datetime
    value: float
    at_span_id: UUID
    is_fallback: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        timestamp = self.timestamp.isoformat()

        value = self.value

        at_span_id = str(self.at_span_id)

        is_fallback = self.is_fallback

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timestamp": timestamp,
                "value": value,
                "at_span_id": at_span_id,
                "is_fallback": is_fallback,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        timestamp = isoparse(d.pop("timestamp"))

        value = d.pop("value")

        at_span_id = UUID(d.pop("at_span_id"))

        is_fallback = d.pop("is_fallback")

        heimdall_dlr = cls(
            timestamp=timestamp,
            value=value,
            at_span_id=at_span_id,
            is_fallback=is_fallback,
        )

        heimdall_dlr.additional_properties = d
        return heimdall_dlr

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
