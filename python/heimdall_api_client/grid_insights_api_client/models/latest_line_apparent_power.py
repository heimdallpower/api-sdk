from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.line_apparent_power import LineApparentPower


T = TypeVar("T", bound="LatestLineApparentPower")


@_attrs_define
class LatestLineApparentPower:
    """
    Attributes:
        metric (str): What kind of data does this response contain. Example: Apparent power.
        unit (str): The unit of the value in the response. Example: MVA.
        apparent_power (LineApparentPower):
    """

    metric: str
    unit: str
    apparent_power: LineApparentPower
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        apparent_power = self.apparent_power.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metric": metric,
                "unit": unit,
                "apparent_power": apparent_power,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.line_apparent_power import LineApparentPower

        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        apparent_power = LineApparentPower.from_dict(d.pop("apparent_power"))

        latest_line_apparent_power = cls(
            metric=metric,
            unit=unit,
            apparent_power=apparent_power,
        )

        latest_line_apparent_power.additional_properties = d
        return latest_line_apparent_power

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
