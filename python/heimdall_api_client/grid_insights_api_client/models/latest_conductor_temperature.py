from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field



if TYPE_CHECKING:
  from ..models.conductor_temperature_values import ConductorTemperatureValues





T = TypeVar("T", bound="LatestConductorTemperature")



@_attrs_define
class LatestConductorTemperature:
    """ 
        Attributes:
            metric (str): What kind of data does this response contain. Example: Conductor temperature.
            unit (str): The unit of the values in the response. Example: C.
            conductor_temperature (ConductorTemperatureValues):
     """

    metric: str
    unit: str
    conductor_temperature: 'ConductorTemperatureValues'
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        conductor_temperature = self.conductor_temperature.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "metric": metric,
            "unit": unit,
            "conductor_temperature": conductor_temperature,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.conductor_temperature_values import ConductorTemperatureValues
        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        conductor_temperature = ConductorTemperatureValues.from_dict(d.pop("conductor_temperature"))




        latest_conductor_temperature = cls(
            metric=metric,
            unit=unit,
            conductor_temperature=conductor_temperature,
        )


        latest_conductor_temperature.additional_properties = d
        return latest_conductor_temperature

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
