from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.conductor_temperature_data_point import ConductorTemperatureDataPoint


T = TypeVar("T", bound="MeasurementPointConductorTemperature")


@_attrs_define
class MeasurementPointConductorTemperature:
    """
    Attributes:
        measurement_point_id (UUID): The id of the measurement point. Example: 00000000-0000-0000-0000-000000000000.
        temperatures (list[ConductorTemperatureDataPoint]): Conductor temperature readings for this measurement point
            within the requested time range.
    """

    measurement_point_id: UUID
    temperatures: list[ConductorTemperatureDataPoint]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        measurement_point_id = str(self.measurement_point_id)

        temperatures = []
        for temperatures_item_data in self.temperatures:
            temperatures_item = temperatures_item_data.to_dict()
            temperatures.append(temperatures_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "measurement_point_id": measurement_point_id,
                "temperatures": temperatures,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.conductor_temperature_data_point import ConductorTemperatureDataPoint

        d = dict(src_dict)
        measurement_point_id = UUID(d.pop("measurement_point_id"))

        temperatures = []
        _temperatures = d.pop("temperatures")
        for temperatures_item_data in _temperatures:
            temperatures_item = ConductorTemperatureDataPoint.from_dict(temperatures_item_data)

            temperatures.append(temperatures_item)

        measurement_point_conductor_temperature = cls(
            measurement_point_id=measurement_point_id,
            temperatures=temperatures,
        )

        measurement_point_conductor_temperature.additional_properties = d
        return measurement_point_conductor_temperature

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
