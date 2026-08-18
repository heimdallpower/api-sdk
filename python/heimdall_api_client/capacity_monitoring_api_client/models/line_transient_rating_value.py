from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LineTransientRatingValue")


@_attrs_define
class LineTransientRatingValue:
    """
    Attributes:
        duration_minutes (int): The transient rating duration in minutes (for example 5, 10 or 15). Transient ratings
            are not calculated for durations longer than one hour. Example: 10.
        value (float): The line transient rating value for this duration at the given timestamp. The unit of this value
            is given by the sibling `unit` field on the response:
              - When `quantity=current` (default) → amperes.
              - When `quantity=apparent_power` → MVA.
             Example: 620.5.
    """

    duration_minutes: int
    value: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        duration_minutes = self.duration_minutes

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "duration_minutes": duration_minutes,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        duration_minutes = d.pop("duration_minutes")

        value = d.pop("value")

        line_transient_rating_value = cls(
            duration_minutes=duration_minutes,
            value=value,
        )

        line_transient_rating_value.additional_properties = d
        return line_transient_rating_value

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
