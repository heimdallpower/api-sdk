from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast, Union
from uuid import UUID






T = TypeVar("T", bound="ProbabilisticCircuitRatingAmpacity")



@_attrs_define
class ProbabilisticCircuitRatingAmpacity:
    """ 
        Attributes:
            value (float): The ampacity value (in amperes) for the facility component id. Example: 375.4.
            at_facility_component_id (Union[None, UUID, Unset]): Identifier of the facility component at which this ampacity
                forecast was calculated. The forecast is computed per facility component and timestamp, and the final
                dimensioning value is determined by selecting the facility component with the lowest ampacity. Example:
                00000000-0000-0000-0000-000000000000.
     """

    value: float
    at_facility_component_id: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        value = self.value

        at_facility_component_id: Union[None, Unset, str]
        if isinstance(self.at_facility_component_id, Unset):
            at_facility_component_id = UNSET
        elif isinstance(self.at_facility_component_id, UUID):
            at_facility_component_id = str(self.at_facility_component_id)
        else:
            at_facility_component_id = self.at_facility_component_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "value": value,
        })
        if at_facility_component_id is not UNSET:
            field_dict["at_facility_component_id"] = at_facility_component_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value")

        def _parse_at_facility_component_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                at_facility_component_id_type_0 = UUID(data)



                return at_facility_component_id_type_0
            except: # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        at_facility_component_id = _parse_at_facility_component_id(d.pop("at_facility_component_id", UNSET))


        probabilistic_circuit_rating_ampacity = cls(
            value=value,
            at_facility_component_id=at_facility_component_id,
        )


        probabilistic_circuit_rating_ampacity.additional_properties = d
        return probabilistic_circuit_rating_ampacity

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
