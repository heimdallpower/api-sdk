from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.line_current import LineCurrent


T = TypeVar("T", bound="LineCurrents")


@_attrs_define
class LineCurrents:
    """
    Attributes:
        metric (str): What kind of data does this response contain. Example: Current.
        unit (str): The unit of the values in the response. Example: Ampere.
        currents (list[LineCurrent]): List of current measurements within the requested time range. May be empty if no
            data exists for the period.
    """

    metric: str
    unit: str
    currents: list[LineCurrent]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        currents = []
        for currents_item_data in self.currents:
            currents_item = currents_item_data.to_dict()
            currents.append(currents_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metric": metric,
                "unit": unit,
                "currents": currents,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.line_current import LineCurrent

        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        currents = []
        _currents = d.pop("currents")
        for currents_item_data in _currents:
            currents_item = LineCurrent.from_dict(currents_item_data)

            currents.append(currents_item)

        line_currents = cls(
            metric=metric,
            unit=unit,
            currents=currents,
        )

        line_currents.additional_properties = d
        return line_currents

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
