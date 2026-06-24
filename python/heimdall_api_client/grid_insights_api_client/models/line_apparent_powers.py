from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.line_apparent_power import LineApparentPower


T = TypeVar("T", bound="LineApparentPowers")


@_attrs_define
class LineApparentPowers:
    """
    Attributes:
        metric (str): What kind of data does this response contain. Example: Apparent power.
        unit (str): The unit of the values in the response. Example: MVA.
        apparent_powers (list[LineApparentPower]): List of apparent power values within the requested time range. May be
            empty if no data exists for the period.
    """

    metric: str
    unit: str
    apparent_powers: list[LineApparentPower]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        apparent_powers = []
        for apparent_powers_item_data in self.apparent_powers:
            apparent_powers_item = apparent_powers_item_data.to_dict()
            apparent_powers.append(apparent_powers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metric": metric,
                "unit": unit,
                "apparent_powers": apparent_powers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.line_apparent_power import LineApparentPower

        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        apparent_powers = []
        _apparent_powers = d.pop("apparent_powers")
        for apparent_powers_item_data in _apparent_powers:
            apparent_powers_item = LineApparentPower.from_dict(apparent_powers_item_data)

            apparent_powers.append(apparent_powers_item)

        line_apparent_powers = cls(
            metric=metric,
            unit=unit,
            apparent_powers=apparent_powers,
        )

        line_apparent_powers.additional_properties = d
        return line_apparent_powers

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
