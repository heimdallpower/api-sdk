from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field



if TYPE_CHECKING:
  from ..models.circuit_rating import CircuitRating





T = TypeVar("T", bound="LatestCircuitRating")



@_attrs_define
class LatestCircuitRating:
    """ 
        Attributes:
            metric (str): What kind of data does this response contain. Example: Circuit rating.
            unit (str): The unit of the value in the response. Example: Ampere.
            circuit_rating (CircuitRating):
     """

    metric: str
    unit: str
    circuit_rating: 'CircuitRating'
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        metric = self.metric

        unit = self.unit

        circuit_rating = self.circuit_rating.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "metric": metric,
            "unit": unit,
            "circuit_rating": circuit_rating,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.circuit_rating import CircuitRating
        d = dict(src_dict)
        metric = d.pop("metric")

        unit = d.pop("unit")

        circuit_rating = CircuitRating.from_dict(d.pop("circuit_rating"))




        latest_circuit_rating = cls(
            metric=metric,
            unit=unit,
            circuit_rating=circuit_rating,
        )


        latest_circuit_rating.additional_properties = d
        return latest_circuit_rating

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
