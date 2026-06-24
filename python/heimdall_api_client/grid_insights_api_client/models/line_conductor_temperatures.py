from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.conductor_temperature_values import ConductorTemperatureValues


T = TypeVar("T", bound="LineConductorTemperatures")


@_attrs_define
class LineConductorTemperatures:
    """
    Attributes:
        metric (str): What kind of data does this response contain. Example: Conductor temperature.
        unit (str): The unit of the values in the response. Example: C.
        conductor_temperatures (list[ConductorTemperatureValues]): List of conductor temperature measurements within the
            requested time range. May be empty if no data exists for the period.
    """

    metric: str
    unit: str
    conductor_temperatures: list[ConductorTemperatureValues]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        conductor_temperatures = []
        for conductor_temperatures_item_data in self.conductor_temperatures:
            conductor_temperatures_item = conductor_temperatures_item_data.to_dict()
            conductor_temperatures.append(conductor_temperatures_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "metric": metric,
                "unit": unit,
                "conductor_temperatures": conductor_temperatures,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.conductor_temperature_values import ConductorTemperatureValues

        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        conductor_temperatures = []
        _conductor_temperatures = d.pop("conductor_temperatures")
        for conductor_temperatures_item_data in _conductor_temperatures:
            conductor_temperatures_item = ConductorTemperatureValues.from_dict(conductor_temperatures_item_data)

            conductor_temperatures.append(conductor_temperatures_item)

        line_conductor_temperatures = cls(
            metric=metric,
            unit=unit,
            conductor_temperatures=conductor_temperatures,
        )

        line_conductor_temperatures.additional_properties = d
        return line_conductor_temperatures

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
