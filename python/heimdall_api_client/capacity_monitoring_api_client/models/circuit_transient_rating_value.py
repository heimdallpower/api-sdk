from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CircuitTransientRatingValue")


@_attrs_define
class CircuitTransientRatingValue:
    """
    Attributes:
        duration_minutes (int): The transient rating duration in minutes (for example 5, 10 or 15). Transient ratings
            are not calculated for durations longer than one hour. Example: 10.
        value (float): The circuit transient rating value for this duration at the given timestamp. The unit of this
            value is given by the sibling `unit` field on the response:
              - When `quantity=current` (default) → amperes.
              - When `quantity=apparent_power` → MVA.
             Example: 590.2.
        limiting_component_id (None | Unset | UUID): Identifier of the facility component that caps the circuit
            transient rating for this duration. When null, the value is not limited by a facility component (the line
            transient rating is the binding constraint). Example: 00000000-0000-0000-0000-000000000000.
    """

    duration_minutes: int
    value: float
    limiting_component_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        duration_minutes = self.duration_minutes

        value = self.value

        limiting_component_id: None | str | Unset
        if isinstance(self.limiting_component_id, Unset):
            limiting_component_id = UNSET
        elif isinstance(self.limiting_component_id, UUID):
            limiting_component_id = str(self.limiting_component_id)
        else:
            limiting_component_id = self.limiting_component_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "duration_minutes": duration_minutes,
                "value": value,
            }
        )
        if limiting_component_id is not UNSET:
            field_dict["limiting_component_id"] = limiting_component_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        duration_minutes = d.pop("duration_minutes")

        value = d.pop("value")

        def _parse_limiting_component_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                limiting_component_id_type_0 = UUID(data)

                return limiting_component_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        limiting_component_id = _parse_limiting_component_id(d.pop("limiting_component_id", UNSET))

        circuit_transient_rating_value = cls(
            duration_minutes=duration_minutes,
            value=value,
            limiting_component_id=limiting_component_id,
        )

        circuit_transient_rating_value.additional_properties = d
        return circuit_transient_rating_value

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
